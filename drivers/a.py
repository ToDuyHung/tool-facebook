from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

if __name__ == '__main__':
    ## get driver for win ###
    #driver = webdriver.Chrome('./drivers/chromedriver.exe')

    ## get driver for linux ##
    driver = webdriver.Chrome('./chromedriver')

    ## access link ###
    driver.get('https://nha.chotot.com/tp-ho-chi-minh/thue-bat-dong-san?page=1&f=p&fbclid=IwAR1Lgz_PxD7s107rsqn8OqsRoAbNpwBD5kV7Ti9UvmxpFSmCW9AQfYeFOgs')
    sleep(1)

    body = driver.find_element_by_tag_name('body')
    for scroll in range(10):
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.ESCAPE)

    sleep(1)

    links_element = driver.find_elements_by_xpath("//a[(@class='ctAdListingItem' and @rel='nofollow') or (@class='_3JMKvS6hucA6KaM9tX3Qb1')]")

    links = []
    for link in links_element:
        links.append(link.get_attribute("href"))



    print(links)