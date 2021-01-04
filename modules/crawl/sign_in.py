from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import settings


def sign_in(user, password):
    ''' Sign in to Facebook.

    :Args:
    - user - user name
    - password - password of user

    :Returns:
    - signin_driver - a driver that has been already logged in
    - None - if the account is locked
    '''

    print("========================= SIGN IN ===========================")

    # FOR CHROME
    chrome_options = Options()
    chrome_options.add_argument("--disable-infobars")
    # chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--disable-extensions")

    # Pass the argument 1 to allow and 2 to block
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2
    })
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(executable_path=settings.CHROME_DRIVER, options=chrome_options)

    driver.get(settings.URL)
    # sleep(3)

    # type user name and password to TextField
    driver.find_element_by_name('email').send_keys(user)
    # sleep(3)
    driver.find_element_by_name('pass').send_keys(password)
    # sleep(3)

    driver.find_element_by_name('login').click()
    # check whether the account is locked
    # if check_isLock(driver) is False:
    #     driver.quit()
    #     return None
    # else:
    #     return driver
    sleep(1)

    return driver
