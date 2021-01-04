# -*- coding: utf-8 -*-
from selenium import webdriver
from time import sleep
import traceback
import logging
import settings
# from modules.crawl.get_link import get_link
from re import findall
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, WebDriverException, \
    StaleElementReferenceException, ElementNotVisibleException
from time import sleep
from datetime import datetime
from selenium.webdriver.common.keys import Keys
import re
from PostInfo import PostInfo
import pymongo
from random import randrange

from modules.api.api_NLP_communicate import get_from_api
from modules.crawl.crawl_users import crawl_users

from pymongo import MongoClient
client = MongoClient('localhost',27017)
# Posts
db = client.re
collection = db.posts_ai_engineer
# collection = db.posts_no_rent2
# Users
collection_user = db.user_ai_engineer
# from modules.data_backup.store_data import store_data

# =============== Mai ================ #
re_group_member  = r"member_id="                        # regex string to find whether the post's owner is group member
re_post_owner_id = r"member_id=(\d+)"                   # regex string to find the id of post's owner

re_group_post_id = r"groups\/(.+)\/permalink\/(.+)\/"   #regex string to find the group name and post id

re_comm_user_id  = r"id=(.+)&extragetparams=(.+)"
re_tag_user_id = r"id=(.+)"
_re_user_id = r"id=(.+)&extragetparams=(.+)"
# ===================================== #

# =============== Henry ================ #
_base_url = 'https://facebook.com'
_user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
               "AppleWebKit/537.36 (KHTML, like Gecko) "
               "Chrome/76.0.3809.87 Safari/537.36")
_headers = {'User-Agent': _user_agent, 'Accept-Language': 'en-US,en;q=0.5'}

_session = None
_timeout = None

_likes_regex = re.compile(r'([0-9,.]+)\s+Like')
_comments_regex = re.compile(r'([0-9,.]+)\s+bình luận')
_shares_regex = re.compile(r'([0-9,.]+)\s+Shares')
_link_regex = re.compile(r"href=\"https:\/\/lm\.facebook\.com\/l\.php\?u=(.+?)\&amp;h=")

_cursor_regex = re.compile(r'href:"(/page_content[^"]+)"')  # First request
_cursor_regex_2 = re.compile(r'href":"(\\/page_content[^"]+)"')  # Other requests

_photo_link = re.compile(r"<a href=\"(/[^\"]+/photos/[^\"]+?)\"")
_image_regex = re.compile(
    r"<a href=\"([^\"]+?)\" target=\"_blank\" class=\"sec\">View Full Size<\/a>"
)
_image_regex_lq = re.compile(r"background-image: url\('(.+)'\)")
_post_url_regex = re.compile(r'/story.php\?story_fbid=')

re_phone = '\d{10}'
# ===================================== #

# =============== Henry ================ #
# def get_posts(account, pages=10, timeout=5, sleep=0):
#     """Gets posts for a given account."""
#     global _session, _timeout

#     # _url = f'{_base_url}/{account}/posts/'
#     url = f'{_base_url}/pg/{account}/posts/'
#     print("\n==== url:{} ====".format(url))
#     _session = HTMLSession()
#     _session.headers.update(_headers)

#     _timeout = timeout
#     response = _session.get(url, timeout=_timeout)
#     html = response.html
#     cursor_blob = html.html


#     # ********** Selenium *********** #
#     driver.get(url)
#     # ********** ******** *********** #

#     while True:
#         for article in html.find('._4-u2 ._4-u8'):
#             # print("\n==== article:{} ====".format(article))
#             yield _extract_post(article,html)

#         pages -= 1
#         if pages == 0:
#             return

#         cursor = _find_cursor(cursor_blob)
#         next_url = f'{_base_url}{cursor}'

#         if sleep:
#             time.sleep(sleep)

#         try:
#             response = _session.get(next_url, timeout=timeout)
#             response.raise_for_status()
#             data = json.loads(response.text.replace('for (;;);', '', 1))
#         except (RequestException, ValueError):
#             return

#         for action in data['payload']['actions']:
#             if action['cmd'] == 'replace':
#                 html = HTML(html=action['html'], url=_base_url)
#             elif action['cmd'] == 'script':
#                 cursor_blob = action['code']
def get_phone(text):
    match = re.search(re_phone,text)
    if match:
        return match.group()
    else:
        return ''
def check_old_ID(id):
    """Check if the id is already in database

    :Args:
    id - an ID of post 
       
    :Return:
    True - there is no post having given ID
    False - otherwise
    """
    client = MongoClient("mongodb://localhost:27017")
    records = list(client['re']['user_ai_engineer'].find({"user_id" : id}))
    client.close()

    if len(records) == 0:
        # no post has that ID
        return True
    else:
        return False
# ===================================== #
# =============== Mai ================ #

######## function to get user id react ###
def get_people_react(signin_driver):

    list_like = []

    try:
        react = signin_driver.find_element_by_xpath("//a[@class='_3dlf']").get_attribute("href")
        signin_driver.get(react)

        i = 0

        while True:
            try:
                see_more = signin_driver.find_element_by_xpath("//div//a[@rel='async']")
                try:
                    see_more.click()
                    sleep(1)
                    i += 1
                    if i > 2:
                        break
                except (StaleElementReferenceException, ElementNotVisibleException, WebDriverException):
                    pass

            except NoSuchElementException:
                break

        try:
            people_react = signin_driver.find_elements_by_xpath("//div[@class='_5j0e fsl fwb fcb']")
            for each_person in people_react:
                fr_tmp = each_person.find_element_by_tag_name('a').get_attribute("data-hovercard")
                friend_id = (re.findall(_re_user_id, fr_tmp)[0])[0]
                list_like.append(friend_id)


        except NoSuchElementException:
            pass

    except NoSuchElementException:
        pass
    print("\n------ List like:{}------\n".format(list_like))
    return list_like
def crawl_comm(signin_driver, links):
    """Crawl users' post and comment

    :Args:
     - links - link of posts found

    :Returns:
   """

    # this list contains info of posts
    posts_info = []
    list_users = []


    for link in links:

        post_info = PostInfo()
        # for link in links:
        signin_driver.get(link)
        sleep(3)
        ### Post #####
        try:
            body = signin_driver.find_element_by_tag_name('body')
            body.send_keys(Keys.ESCAPE)
            print('----- Link post in group ------')
            print(link)

            # try:
            #     # content = signin_driver.find_element_by_xpath("//*[@class='rq0escxv l9j0dhe7 du4w35lb qmfd67dx hpfvmrgz gile2uim buofh1pr g5gj957u aov4n071 oi9244e8 bi6gxh9e h676nmdw aghb5jc5']")

            #     message = signin_driver.find_elements_by_tag_name('p')
            #     msg = signin_driver.find_elements_by_xpath('//span[@class="_5z6m"]//span[@class="_4a6n"]')
            #     text = ''
            #     if message:
            #         print("^^^ IN p ^^^")
            #         for post in message:
            #             # print("\n=== post:{} ===\n".format(post.text))
            #             text += post.text + "\n"
            #     if msg:
            #         print("^^^ IN _4a6n ^^^",msg)
            #         for post in msg:
            #             text = post.text + "\n"
            #     print("\n=== text:{} ===\n".format(text))
            # except NoSuchElementException:
            #     print("No Posts")
            #     text = ''
            #     pass

            try:
                # post = signin_driver.find_elements_by_xpath('//*[@class="ecm0bbzt hv4rvrfc ihqw7lf3 dati1w0a"]')
                # if not post:
                #     post = signin_driver.find_elements_by_xpath('//*[@class="k4urcfbm kr520xx4 j9ispegn pmk7jnqg taijpn5t datstx6m cbu4d94t j83agx80 bp9cbjyn"]')
                post_content = signin_driver.find_element_by_xpath('//div[contains(@class,"kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql")]')
                print('----------Post content-------')
                text = post_content.get_attribute('innerHTML')
                print("\n=== text:{} ===\n".format(text))
            except NoSuchElementException:
                print("No Posts")
                text = ''
                # pass

            ### Time-Date #####

            try:
                post_date = signin_driver.find_elements_by_xpath('//span[@class="timestampContent"]')
                print("\n=== post_date:{} ===\n".format(post_date[0]))
                time_date = post_date[-1].text

            except Exception as e:
                logging.error(traceback.format_exc())
                time_date = ''
                pass

            ### Post_id #####

            re_post_id = r'\/\d+(\/)?'
            # match = re.search(re_post_id,link)
            # match = re.search(re_group_post_id,link)

            if findall(pattern=re_group_post_id, string=link):
                # post_id = match.group().replace("/","")
                post_id = findall(pattern=re_group_post_id, string=link)[0][1]
            else:
                post_id = ''
            print("\n=== post_id:{} ===\n".format(post_id))

            ### Post User Id #####
            user_ajax = signin_driver.find_element_by_xpath("//h5//a[1]").get_attribute("data-hovercard")

            post_info.posts_info['post_owner_id'] = findall(r"id=\d+", user_ajax)[0].replace("id=","")
            post_info.posts_info['message'] = text
            post_info.posts_info['post_date'] = time_date
            post_info.posts_info['post_url'] = link
            post_info.posts_info['post_id'] = post_id
            post_info.posts_info['_id'] = \
                    str(post_id) if post_id!='' else str(randrange(1,1000000))
            post_info.posts_info['attributes'] = \
                    get_from_api(text)
            post_info.posts_info['phone'] = get_phone(text)

            #### click to show cmt ####
            # body = signin_driver.find_element_by_tag_name('body')
            check_val = False
            try:
                check_cmt_element = signin_driver.find_element_by_xpath("//div[@class='_3w53']")
                check_val = True
            except:pass

            if not check_val:
                sleep(4)
                try:
                    sleep(3)
                    body.send_keys(Keys.PAGE_DOWN)
                    click_cmt_element = signin_driver.find_element_by_xpath("//div[@class='_14i5 _1qkq _1qkx']//a[@class='_3hg- _42ft' and @role='button']")

                    print(type(click_cmt_element).__name__)
                    sleep(3)
                    # num_cmt_text = click_cmt_element.text
                    # tmp = num_cmt_text.split(" ")
                    # num_cmt = int(tmp[0])
                    try:
                        sleep(3)
                        click_cmt_element.click()
                        sleep(1)
                        print("\n &&&&&&& \n")

                    except WebDriverException:
                        pass

                except NoSuchElementException:
                    pass

            while True:
                try:
                    # a[@class='_4sxc _42ft'] : "See more replies" button
                    # a[@class='_5v47 fss'] : "Show more content" button
                    a_tag = signin_driver.find_element_by_xpath("//a[(@class='_4sxc _42ft' or @class='_5v47 fss') and @role='button']")
                    check = False


                    try:
                        a_tag.click()
                        sleep(4)
                        check = True
                    except WebDriverException:
                        pass
                    if check == False:
                        body.send_keys(Keys.PAGE_DOWN)

                    try:
                        require_login = signin_driver.find_element_by_xpath("//div[@class='_62up']//a[@role='button']")
                        sleep(4)
                        try:
                            require_login.click()
                            sleep(2)
                        except WebDriverException:
                            pass

                    except NoSuchElementException:
                        pass

                except (NoSuchElementException, ElementNotInteractableException):
                    break




            ### number of react #####

            try:
                num_react_ele = signin_driver.find_element_by_xpath("//div[@class='_14i5 _1qkq _1qkx']//span[@class='_3dlh _3dli']//span[@class='_81hb']")
                num_react = num_react_ele.text
                print(num_react)

            except NoSuchElementException:
                print("No react")
                num_react = 0
                pass

            ### number of share ###
            try:
                num_share_element = signin_driver.find_element_by_xpath("//div[@class='_14i5 _1qkq _1qkx']//a[@class='_3rwx _42ft']")
                num_share = num_share_element.text
                print(num_share)
            except NoSuchElementException:
                print("No share")
                num_share = 0
                pass

            # cmts = signin_driver.find_elements_by_xpath("//u1[@class='_7a9a']//li")
            # for cmt in cmts:
            #     print(cmt.text)
            # print(len(cmts))
            # Show all comments and replies
            all_comments = signin_driver.find_elements_by_xpath("//li//div[@aria-label='Comment' or @aria-label='Comment reply' or @aria-label='Trả lời bình luận' or @aria-label='Bình luận']")
            # for cmt in all_comments:
            #     print(cmt.text)
            num_cmt = len(all_comments)
            print(num_cmt)

            post_info.posts_info['n_react'] = num_react
            post_info.posts_info['n_shares'] = num_share
            post_info.posts_info['n_comments'] = num_cmt


            list_cmt = []

            if len(all_comments) > 0:
                comm_count = 0
                # flag_comment_reply = True                       # True: the current is comment, False: otherwise
                comm_replies = []

                cmt_rep_content = ""
                cmt_rep_user = ""
                cmt_rep_tag = ""

                for comment_reply in all_comments:

                    comm_count += 1


                    # this is comment
                    if comment_reply.get_attribute('aria-label') == "Comment" or comment_reply.get_attribute('aria-label') == "Bình luận":
                        # print("This is comment")
                        # global flag_comment_reply
                        flag_comment_reply = False
                        # if this is not first comment
                        # print(comm_count)
                        tags = findall(re_tag_user_id, cmt_rep_content)
                        cmt_rep_tag = tags if tags else ''
                        print("\n\n\n @@@@ cmt_rep_tag:{} @@@@".format(cmt_rep_tag))
                        if comm_count > 1:
                            # print("found")
                            # print(cmt_rep_content)
                            # post_info.add_comment(cmt_rep_user, cmt_rep_content, cmt_rep_tag, comm_replies)
                            # print(cmt_rep_content)
                            list_users.append(cmt_rep_user)
                            list_cmt.append({
                                "cmt_rep_user": cmt_rep_user,
                                "cmt_rep_content": cmt_rep_content,
                                "cmt_phone": get_phone(cmt_rep_content),
                                "cmt_rep_tag": cmt_rep_tag,
                                "cmt_attributes": get_from_api(cmt_rep_content),
                                "comm_replies": comm_replies})
                            comm_replies = []

                    # this is reply of comment
                    else:
                        # print("This is reply")
                        flag_comment_reply = True


                    # extract data of reply or comment

                    ## get comment's or reply's owner ID

                    tmp = comment_reply.find_element_by_class_name('_6qw4')
                    try:
                        tmp_attr = tmp.get_attribute('data-hovercard')
                        comm_rep_user = (findall(re_comm_user_id, tmp_attr)[0])[0]

                    except TypeError:
                        comm_rep_user = tmp.text

                    # print("Comm user id: ", comm_rep_user)

                    ## get content and (or) tagged user of comment or reply
                    comm_rep_content = ""
                    comm_rep_tag     = []
                    try:
                        comment_class = comment_reply.find_element_by_class_name('_3l3x')

                        # get text in comment
                        text = comment_class.text
                        if text != None:
                            comm_rep_content = comm_rep_content + text
                        # print(comm_rep_content)
                        # try:
                        #     comm_rep_content = comment_class.find_element_by_tag_name('span').text
                        #     # print("Text: ", comm_rep_content)
                        # except NoSuchElementException:
                        #     pass


                        # get tag in comment
                        try:

                            tag = comment_class.find_element_by_tag_name('a').get_attribute('data-hovercard')

                            comm_rep_tag.append(findall(re_tag_user_id, tag)[0])

                            # print("Tag id: ", comm_rep_tag)
                        except NoSuchElementException:
                            pass
                        except TypeError:
                            pass

                    except NoSuchElementException:
                        pass


                    # if the current is reply, add reply to list comm_replies
                    if flag_comment_reply:
                        comm_replies.append({
                            'reply_user'   : comm_rep_user,
                            'reply_comment': comm_rep_content,
                            'reply_tag'    : comm_rep_tag
                        })

                    else:
                        cmt_rep_user = comm_rep_user
                        cmt_rep_tag = comm_rep_tag
                        cmt_rep_content = comm_rep_content
                        # print(cmt_rep_content)

                    if comm_count >= num_cmt:
                        # post_info.add_comment(cmt_rep_user, cmt_rep_content, cmt_rep_tag, comm_replies)
                        list_users.append(cmt_rep_user)
                        list_cmt.append(
                            {
                                "cmt_rep_user": cmt_rep_user,
                                "cmt_rep_content": cmt_rep_content,
                                "cmt_rep_tag": cmt_rep_tag,
                                "comm_replies": comm_replies}
                        )


            # append to posts_info
            print(list_cmt)
            post_info.posts_info['post_comments'] = list_cmt
            list_user_like = get_people_react(signin_driver)
            post_info.posts_info['list_user_like'] = list_user_like
        #     posts_info.append(post_info)
            print('==== posts_info:{} ==== '.format(post_info.posts_info))
            try:
                collection.insert_one(post_info.posts_info)
            except:pass
            sleep(3)
        except:
        # for user in list_user_like:
        #     if check_old_ID(user):
        #         crawl_users(signin_driver,user)
        #         # collection_user.insert_one(dict_users)
        #     else:
        #         print("This user has already crawled.")

            posts_info.append(post_info.posts_info)
    print('==== posts_info:{} ==== '.format(posts_info))

    # return posts_info.posts_info

    # # collection.insert_one(posts_info.posts_info)
    # try:
    #     collection.insert_one(posts_info.posts_info)
    # except pymongo.errors.DuplicateKeyError:
    #     # skip document because it already exists in new collection
    #     pass
    # try:
    #     collection.insert_one(posts_info.posts_info)
    # except:
    #     pass

    signin_driver.quit()
# ===================================== #


