#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import time
from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException 
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
reload(sys)
sys.setdefaultencoding('utf8')

head = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'Accept-Language':
    'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
    'Accept':
    'application/json, text/javascript, */*; q=0.01',
}

root_url = 'https://www.shiyanlou.com/'
# driver = webdriver.Chrome(
#     r"E:\tools\google driver\chromedriver_win32\chromedriver.exe")
driver = webdriver.Firefox()


def register():
    driver.get(root_url)
    time.sleep(2)
    sign_ups = driver.find_elements_by_class_name('sign-up')
    # print 'sign_up 0', sign_ups[0].get_attribute("text")
    sign_ups[1].click()
    # driver.switch_to_window(driver.window_handles[0])
    time.sleep(2)
    email = driver.find_element_by_name('email')
    email.send_keys('xxxxx@qq.com')
    password = driver.find_elements_by_name('password')
    password[1].send_keys('xxxxxxx')
    
    drap_screen = driver.find_elements_by_class_name('nc-lang-cnt')[0]


    action = webdriver.ActionChains(driver)
    action.click_and_hold(drap_screen).perform()  #鼠标左键按下不放

    
    for item in range(200):
        try:
            print 'item', item
            action.move_by_offset(2, 0).perform()  #平行移动鼠标
        except UnexpectedAlertPresentException as e: 
            break
        except StaleElementReferenceException as e: 
            break
        except MoveTargetOutOfBoundsException as e:
            print 'cow  *'*10
        action.reset_actions()
        # time.sleep(0.1)

    time.sleep(2)

    print 'register 1', driver.find_elements_by_name('submit')[1].get_attribute('value')
    register = driver.find_elements_by_name('submit')[1]


    action = webdriver.ActionChains(driver)
    
    res = action.click(register).perform()
    print 'res', res
    driver.quit()


if __name__ == '__main__':
    register()

