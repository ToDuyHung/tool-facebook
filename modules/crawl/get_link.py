from re import search, findall

from selenium.webdriver.common.keys import Keys
from time import sleep
from random import seed
from random import random
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains

import settings
from pymongo import MongoClient

# re_mogi = r"mogivietnam"
# re_mogi = r"groups/nhatros"
# re_mogi = r"vinhomes.vn"
from modules.crawl.crawl_comm import crawl_comm

re_id = r"\/(\d+)"
re_id_2 = r"(id=\d+)+"


# re_mogi = r"nhadattayninhgiare"
# re_mogi = r"muabannhadattn"
# re_mogi = r"1398281840492052"
# re_mogi = r"muabannhadattayninh"
# re_mogi = r"Neunhu"
# re_mogi = r"132157674161952"
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('headless')
# chrome_options.add_argument("--disable-infobars")
# chrome_options.add_argument("start-maximized")
# chrome_options.add_argument("--disable-extensions")

# # Pass the argument 1 to allow and 2 to block
# chrome_options.add_experimental_option("prefs", { 
#     "profile.default_content_setting_values.notifications": 2
# })

# signin_driver = webdriver.Chrome(executable_path=settings.CHROME_DRIVER, chrome_options=chrome_options)
# get_link(signin_driver)
def random_waiting(min, max):
    return min + (random() * (max - min))


def check_old_ID(id):
    """Check if the id is already in database

    :Args:
    id - an ID of post 
       
    :Return:
    True - there is no post having given ID
    False - otherwise
    """
    client = MongoClient("mongodb://localhost:27017")
    # records = list(client['re']['posts_no_rent2'].find({"post_id" : id}))
    records = list(client['re']['posts_ai_engineer'].find({"post_id": id}))
    client.close()

    if len(records) == 0:
        # no post has that ID
        return True
    else:
        return False


def get_link(signin_driver):
    seed(342)

    for group in settings.GROUPS:
        print("\n=== Start {} ===\n".format(group))
        sleep(0.1)
        signin_driver.get(group)
        body = signin_driver.find_element_by_tag_name('body')

        for i in range(10):
            body.send_keys(Keys.ESCAPE)  # close popup

        for i in range(settings.SCROLLS):
            body.send_keys(Keys.PAGE_DOWN)
            body.send_keys(Keys.ESCAPE)
            # try:
            #     require_login = signin_driver.find_element_by_xpath("//div[@class='_62up']//a[@role='button']")
            #     sleep(2)
            #     try:
            #         require_login.click()
            #         sleep(0.75)
            #     except WebDriverException:
            #         pass
            # except NoSuchElementException:
            #     pass
            # if i % 8 == 0:
            #     sleep(random_waiting(0.3, 0.6))
            sleep(0.1)

        posts_link = []
        permalinkFormat = r"groups\/(.+)\/permalink\/(.+)\/"
        count = 0

        # classes = signin_driver.find_elements_by_xpath("//*[@class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql gk29lw5a a8c37x1j keod5gw0 nxhoafnm aigsh9s9 tia6h79c fe6kdd0r mau55g9w c8b282yb iv3no6db e9vueds3 j5wam9gi knj5qynh m9osqain hzawbc8m']//span//span[2]//a")
        classes = signin_driver.find_elements_by_xpath("//a[@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw']")

        for c in classes:
            if count > settings.SCROLLS: break
            count+=1
            hover = ActionChains(signin_driver).move_to_element(c)
            ################################## ERROR ##################3
            hover.perform()
            sleep(1)
            link = c.get_attribute('href')
            if search(pattern=permalinkFormat, string=link) is None:
                continue
            else:
                id = findall(pattern=permalinkFormat, string=link)[0][1]
                print("id : ", id)
                # ## check whether the post is already crawled by checking ID
                # if check_old_ID(id):
                #     # no post in database has this ID
                #     posts_link.append(link)
                # else:
                #     print("This link has already crawled.")

                posts_link.append(link)

        crawl_comm(signin_driver, posts_link)
