__author__ = "Mai Pham And Ngoc Thien"

from selenium import webdriver
from time import sleep
from re import findall
from selenium.common.exceptions import NoSuchElementException
import datetime
from selenium.webdriver.common.keys import Keys
from store_data import *
from selenium.webdriver.common.action_chains import ActionChains


re_id  = r"id=(.+)&extragetparams=(.+)"
re_id_only = r"id=(.+)"


### read list userID from text ###
def read_list_user():
    list_user = []
    with open("ListUser.txt", 'r') as file:
        for userID in file:
            list_user.append(userID.strip('\n'))
    return list_user


### read list account from csv ###
def read_list_acct():
    list_acct = []
    with open("acc.csv", 'r') as file:
        for acct in file:
            user, password = acct.strip("\n").split(",")
            list_acct.append({
                "user": user,
                "pass": password
            })
    return list_acct


### sign_in ####
def sign_in(acct, current_user, current_field, current_info):

    username = acct['user']
    password = acct['pass']

    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(CHROME_DRIVER, chrome_options=chrome_options)
    driver.get(URL)

    driver.find_element_by_id('email').send_keys(username)
    driver.find_element_by_id('pass').send_keys(password)

    try:
        driver.find_element_by_id('loginbutton').click()
    except NoSuchElementException:
        driver.find_element_by_css_selector("#u_0_a > div:nth-child(5) > button").click()

    sleep(0.25)
    # return next user to crawl #
    next_user, next_field_to_crawl, next_info = crawl_profile_checkin_posts(driver, current_user, current_field, current_info)

    # driver.close()

    return next_user, next_field_to_crawl, next_info


## crawl user post, if not blocked, return true, if blocked, return false
def crawl_user_profile_posts(driver, userId):
    print(URL + userId)
    driver.get(URL + userId)
    sleep(0.25)
    try:
        blocked = driver.find_element_by_xpath("//div[@class='mvl ptm uiInterstitial uiInterstitialLarge uiBoxWhite']")
        return False
    except NoSuchElementException:
        body = driver.find_element_by_tag_name("body")
        body.send_keys(Keys.ESCAPE)
        body.send_keys(Keys.PAGE_DOWN)
        sleep(0.25)
        # get current year
        current_year = datetime.datetime.now().year
        ## get year in user profile ##
        year = driver.find_element_by_xpath("//span[@class='uiButtonGroup fbStickyHeaderBreadcrumb uiButtonGroupOverlay']//span[3]")
        number_scroll = 0
        while not year.text.isdigit() or int(year.text) >= current_year-2:
            body.send_keys(Keys.PAGE_DOWN)
            number_scroll += 1
            sleep(0.25)
            year = driver.find_element_by_xpath("//span[@class='uiButtonGroup fbStickyHeaderBreadcrumb uiButtonGroupOverlay']//span[3]")
            if number_scroll >= 500:
                try:
                    end_post = driver.find_element_by_xpath("//i[@class='img sp_jgaSVtiDmn__1_5x sx_dd9709']")
                    break
                except NoSuchElementException:
                    pass

        ## get posts ##
        post_links = driver.find_elements_by_xpath("//div[@class='_5pcb _4b0l _2q8l']//div[@class='_6a _5u5j _6b']//a[@class='_5pcq']")
        user_posts_dict = {"userId": userId}

        # get info from each link #
        try:
            profile_posts_solution(driver, user_posts_dict, post_links)
        except Exception:
            pass
    return True


def cmt_resolution(driver):
    while True:
        try:
            reply_element = driver.find_element_by_xpath("//a[@class='_4sxc _42ft' and @role='button']")
            action = ActionChains(driver)
            action.click(reply_element).perform()
            sleep(0.25)
        except NoSuchElementException:
            break

    cmt_types = []
    sign_elements = driver.find_elements_by_xpath("//li//div[1]//div[@role='article']")
    for sign_element in sign_elements:
        sign_cmt = sign_element.get_attribute("aria-label")
        if sign_element:
            cmt_types.append(sign_cmt)

    comment_elements = driver.find_elements_by_xpath("//ul[@class='_7791']//li//div[1]//a")
    comments = []
    user_tagged = []
    not_append = -1


    for comment_element in comment_elements[::-1]:
        id_attr = comment_element.get_attribute("data-hovercard")
        if id_attr and comment_elements.index(comment_element) != not_append:
            if findall(re_id, id_attr):
                comment = dict()
                comment_Id = (findall(re_id, id_attr)[0])[0]
                comment['userId-commented'] = comment_Id
                comment['userId-isTagged'] = user_tagged[::-1]
                comments = [comment] + comments
                user_tagged = []
                not_append = comment_elements.index(comment_element)-1
            else:
                user_tagged.append(findall(re_id_only, id_attr)[0])


    current_cmt = 0
    has_replies = []
    for i in range(0, len(comments)):
        comments[i]['comment_no'] = i
        if 'Bình luận' == cmt_types[i]:
            if i != 0:
                comments[current_cmt]['has_replies'] = has_replies[:]
            current_cmt = i
            has_replies = []
        else:
            has_replies.append(i)
            comments[i]['is_reply_of'] = current_cmt
    comments[current_cmt]['has_replies'] = has_replies[:]

    return comments


## solution for posts in user profile ###
def profile_posts_solution(driver, user_posts_dict, post_links):

    urls = [] # list url in text #
    for link in post_links:
        urls.append(link.get_attribute('href'))

    for url in urls:
        driver.get(url)
        body = driver.find_element_by_tag_name('body')
        sleep(0.5)
        body.send_keys(Keys.ESCAPE)
        if 'photo' in url:
            try:
                cancel_butt = driver.find_element_by_xpath("//a[@class='_xlt _418x']")
                action = ActionChains(driver)
                action.click(cancel_butt).perform()
                sleep(0.25)
            except Exception:
                pass
        userIds_tagged = []

        # find tag in post-message #
        tags_in_post_message = driver.find_elements_by_xpath("//div[@data-testid='post_message']//a")
        tagged = False
        for tag_in_post in tags_in_post_message:
            userId_attr = tag_in_post.get_attribute('data-hovercard')
            if not userId_attr:
                continue
            tagId = (findall(re_id, userId_attr)[0])[0]
            if tagId != user_posts_dict.get('userId') and tagId not in userIds_tagged:
                userIds_tagged.append(tagId)
            elif tagId == user_posts_dict.get('userId'):
                tagged = True

        # structure: A with B, C and n others at/in place D
        # find tag "with" in post header #
        len_tag = 0
        if not tagged:
            try:
                tag_with_element = driver.find_element_by_xpath("//span[@class='fcg']")
                if 'với' not in tag_with_element.text and 'cùng' not in tag_with_element.text:
                    continue
                if "ở" in tag_with_element.text or "tại" in tag_with_element.text:
                    len_tag = -1
            except NoSuchElementException:
                continue
        tag_elements = driver.find_elements_by_xpath("//h5[@class='_7tae _14f3 _14f5 _5pbw _5vra']//a")
        len_tag = len(tag_elements) if len_tag == 0 else len_tag

        for tag_element in tag_elements[:len_tag]:
            if tag_element.get_attribute('role') == 'button':
                action = ActionChains(driver)
                action.click(tag_element).perform()
                sleep(2)
                tags = driver.find_elements_by_xpath("//li[@class='fbProfileBrowserListItem']//a[@class='_8o _8t lfloat _ohe']")
                # print(tags)
                for tag in tags:
                    tag_attr = tag.get_attribute('data-hovercard')
                    if not tag_attr:
                        continue
                    tagId = (findall(re_id, tag_attr)[0])[0]
                    if tagId != user_posts_dict.get('userId') and tagId not in userIds_tagged:
                        userIds_tagged.append(tagId)
            else:
                attr = tag_element.get_attribute('data-hovercard')
                if not attr:
                    continue
                userId_tag = (findall(re_id, attr)[0])[0]
                if userId_tag != user_posts_dict.get('userId') and userId_tag not in userIds_tagged:
                    userIds_tagged.append(userId_tag)


        # find comment userId in post #
        cmt = cmt_resolution(driver)


        print(url)
        print(userIds_tagged)

        user_post_dict = dict()
        user_post_dict['userId'] = user_posts_dict.get('userId')
        user_post_dict['post'] = url
        user_post_dict['userId-tagged'] = userIds_tagged
        user_post_dict['comment-info'] = cmt
        store_tagged_user_into_mongo(user_post_dict)



##### cong viec va hoc van ######### education
def crawl_education(driver, userid, info):
    driver.get(URL + userid + "/about?section=education")
    sleep(1)
    try:
        blocked = driver.find_element_by_xpath("//div[@class='mvl ptm uiInterstitial uiInterstitialLarge uiBoxWhite']")
        return False
    except NoSuchElementException:
        text_element = driver.find_elements_by_xpath("//div[@class='_4qm1']")
        for element in text_element:
            field_and_description = element.text.split("\n")
            if "Không có" in field_and_description[1]:
                continue
            info[field_and_description[0]] = field_and_description[1:]
        return True



##### noi o hien tai va que quan ########### living
def crawl_living(driver, userid, info):
    driver.get(URL + userid + "/about?section=living")
    sleep(1)
    try:
        blocked = driver.find_element_by_xpath("//div[@class='mvl ptm uiInterstitial uiInterstitialLarge uiBoxWhite']")
        return False
    except NoSuchElementException:
        try:
            text_element = driver.find_element_by_xpath("//div[@class='_4qm1']")
            field_and_description = text_element.text.split("\n")
            if "Không có" in field_and_description[1]:
                return True
            info[field_and_description[0]] = field_and_description[1::2]
            return True
        except NoSuchElementException:
            return None



#### thong tin lien he co ban############# contact-info
def crawl_contact_info(driver, userid, info):
    driver.get(URL + userid + "/about?section=contact-info")
    sleep(1)
    try:
        blocked = driver.find_element_by_xpath("//div[@class='mvl ptm uiInterstitial uiInterstitialLarge uiBoxWhite']")
        return False
    except NoSuchElementException:
        info_contacts = driver.find_elements_by_xpath("//li[@class='_3pw9 _2pi4 _2ge8']")
        for info_contact in info_contacts:
            field_and_detail = info_contact.text.split("\n")
            if len(field_and_detail) == 1:
                continue
            info[field_and_detail[0]] = field_and_detail[1:] if len(field_and_detail) > 2 else field_and_detail[1]
        return True



#### moi quan he bao gom: tinh trang quan he va thanh vien trong gia dinh####
def crawl_relationship(driver, userid, info):
    driver.get(URL + userid + "/about?section=relationship")
    sleep(1)

    try:
        blocked = driver.find_element_by_xpath("//div[@class='mvl ptm uiInterstitial uiInterstitialLarge uiBoxWhite']")
        return False
    except NoSuchElementException:
        # tinh trang moi quan he
        relationship_elements = driver.find_elements_by_xpath("//li[@class='_3pw9 _2pi4 _2ge8']")
        relation_list = []
        for relation_element in relationship_elements:
            relation_text = relation_element.text
            text_list = relation_text.split("\n")
            if len(text_list) == 1: # if there is no one related, example: Single
                relation_list.append(relation_text)
            else:
                ID_element = driver.find_element_by_xpath("//a[@title='"+ text_list[0] +"']")
                ID_attribute = ID_element.get_attribute('data-hovercard')
                realID = (findall(re_id, ID_attribute)[0])[0] # get ID of user related, example: married with sb
                relation_list.append(tuple([realID, relation_text]))
        if relation_list:
            info["TÌNH TRẠNG MỐI QUAN HỆ"] = relation_list[0] if len(relation_list) == 1 else relation_list

        # thanh vien trong gia dinh
        family_elements = driver.find_elements_by_xpath("//li[@class='_43c8 _2ge8']")
        member_list = []
        for family_element in family_elements:
            each_member_text = family_element.text
            text_list = each_member_text.split("\n")
            if len(text_list) == 1: # if there is no one related
                member_list.append(each_member_text)
            else:
                ID_element = driver.find_element_by_xpath("//a[@title='"+ text_list[0] +"']")
                ID_attribute = ID_element.get_attribute('data-hovercard')
                realID = (findall(re_id, ID_attribute)[0])[0] # get ID of family members
                member_list.append(tuple([realID, each_member_text]))
        if member_list:
            info["THÀNH VIÊN TRONG GIA ĐÌNH"] = member_list[0] if len(member_list) == 1 else member_list

        return True



#### chi tiet ve user####
def crawl_bio(driver, userid, info):
    driver.get(URL + userid + "/about?section=bio")
    sleep(1)
    try:
        blocked = driver.find_element_by_xpath("//div[@class='mvl ptm uiInterstitial uiInterstitialLarge uiBoxWhite']")
        return False
    except NoSuchElementException:
        intro_elements = driver.find_elements_by_xpath("//div[@class='_4qm1']")
        for intro_element in intro_elements:
            intro_list = intro_element.text.split("\n")
            if "Không có" in intro_list[1]:
                continue
            if intro_list[0] == "CÁC TÊN KHÁC":
                info[intro_list[0]] = intro_list[1::2]
            else:
                if len(intro_list) == 1:
                    continue
                info[intro_list[0]] = intro_list[1] if len(intro_list) == 2 else intro_list[1:]
        return True



### su kien trong doi ######
def crawl_year_overviews(driver, userid, info):
    driver.get(URL + userid + "/about?section=year-overviews")
    sleep(1)
    try:
        blocked = driver.find_element_by_xpath("//div[@class='mvl ptm uiInterstitial uiInterstitialLarge uiBoxWhite']")
        return False
    except NoSuchElementException:
        years_ow_elements = driver.find_elements_by_xpath("//li[@class='_2pi4']")
        yearList = []
        for years_ow_element in years_ow_elements:
            overview_text = years_ow_element.text.split("\n")
            if len(overview_text) <= 1:
                continue
            overview2 = overview_text[1] if len(overview_text) == 2 else overview_text[1:]
            yearList.append(tuple([overview_text[0], overview2]))

        if yearList:
            info["SỰ KIỆN TRONG ĐỜI"] = yearList if len(yearList) > 1 else yearList[0]

        return True


##### checkin ###
def crawl_places_recent(driver, userid, info):
    driver.get(URL + userid + "/places_recent")
    sleep(1)
    try:
        blocked = driver.find_element_by_xpath("//div[@class='mvl ptm uiInterstitial uiInterstitialLarge uiBoxWhite']")
        return False
    except NoSuchElementException:
        checkin_elements = driver.find_elements_by_xpath("//li[@class='_5rz']")
        checkins = []
        for checkin_element in checkin_elements:
            checkin = dict()
            place_and_time = checkin_element.text.split("\n")
            if len(place_and_time) == 2:
                place, time = place_and_time
            else:
                continue
            checkin['post checkin'] = checkin_element.find_element_by_partial_link_text(time).get_attribute('href')
            checkin['link địa điểm'] = checkin_element.find_element_by_partial_link_text(place).get_attribute('href')
            checkin["Địa Điểm"] = place
            checkin["Thời gian"] = time
            checkins.append(checkin)

        if checkins:
            info["CHECKIN"] = checkins

        return True


### source to crawl profile ###
def crawl_profile_checkin_posts(driver, current_user, current_field, info_crawling):

    # user to crawl #
    user_number = current_user
    for userid in LIST_USER_ID[current_user:]:

        # get profile info, each profile is a dictionary
        info = info_crawling if userid == current_user else dict()

        tmp = 0
        if userid == current_user and current_field:
            switcher = {
                "post": 0,
                "education": 1,
                "living": 2,
                "contact-info":3,
                "relationship":4,
                "bio": 5,
                "year-overviews": 6,
                "places_recent": 7
            }
            tmp = switcher.get(current_field, 0)

        ### crawl posts in user wall ###
        if tmp == 0:
            notBlocked = crawl_user_profile_posts(driver, userid)
            if not notBlocked:
                return user_number, "post", dict() ## notify that blocked when crawl post


        ### crawl user education####
        if tmp <= 1:
            notBlocked = crawl_education(driver, userid, info)
            if not notBlocked:
                return user_number, "education", info


        ### crawl user living####
        if tmp <= 2:
            notBlocked = crawl_living(driver, userid, info)
            if notBlocked is None:
                continue
            if not notBlocked:
                return user_number, "living", info # notify blocked when crawling living


        ### crawl user contact-info####
        if tmp <= 3:
            notBlocked = crawl_contact_info(driver, userid, info)
            if not notBlocked:
                return user_number, "contact-info", info # notify blocked when crawling contact-info


        ### crawl user relationship####
        if tmp <= 4:
            notBlocked = crawl_relationship(driver, userid, info)
            if not notBlocked:
                return user_number, "relationship", info # notify blocked when crawling relationship


        ### crawl user bio####
        if tmp <= 5:
            notBlocked = crawl_bio(driver, userid, info)
            if not notBlocked:
                return user_number, "bio", info # notify blocked when crawling bio


        ### crawl user year-overviews####
        if tmp <= 6:
            notBlocked = crawl_year_overviews(driver, userid, info)
            if not notBlocked:
                return user_number, "year-overviews", info # notify blocked when crawling year-overviews


        ### crawl user places_recent####
        if tmp <= 7:
            notBlocked = crawl_places_recent(driver, userid, info)
            if not notBlocked:
                return user_number, "places_recent", info # notify blocked when crawling places_recent



        ## debug info ###
        print(info)

        ## save in file ##
        if info:
            info_to_store = {"userId": userid}
            info_to_store.update(info)
            with open("profile_user.txt", 'a', encoding='utf-8') as file:
                print(userid, file=file)
                print(info, end="\n\n", file=file)
            store_profile_into_mongo(info_to_store)



        ## next user ##
        user_number += 1


if __name__ == "__main__":


    # settings
    ACCTS         = read_list_acct()
    URL           = "https://www.facebook.com/"
    CHROME_DRIVER = "drivers/chromedriver.exe"
    LIST_USER_ID = read_list_user()[1:]


    current_acct = 0
    next_user = 0
    tmp_field = None
    tmp_info = dict()
    while True:
        # switch account in case user is not accessed ##
        next_user, tmp_field, tmp_info = sign_in(ACCTS[current_acct], next_user, tmp_field, tmp_info)
        current_acct += 1
        if current_acct == len(ACCTS):
            current_acct = 0
            sleep(1000)

