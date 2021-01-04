import random
from time import sleep
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException

time_now = datetime.now()
random.seed(time_now.microsecond + time_now.day * (time_now.month - time_now.hour))

def random_time(a, b):
    '''Return time in seconds between a and b
    '''

    return random.random() + random.randint(a, b-1)

def check_isLock(signin_driver):
    """Find must-have elements in page.

    :Args:
     - signin_driver - Selenium driver

    :Returns:
     - True: if the page contains must-have elements, in other word, the account is not locked
     - False: otherwise
    """
    for i in range(3):
        try: 
            signin_driver.find_element_by_xpath("//div[@class='_3qcu _cy7']").get_attribute("innerHTML")
            signin_driver.find_element_by_xpath("//div[@class='_6a uiPopover _cy7 _5v-0']").get_attribute("innerHTML")

            return True
        except NoSuchElementException:
            if i == 2:
                return False
            else:
                sleep(random_time(1, 2))
                signin_driver.refresh()
                continue
