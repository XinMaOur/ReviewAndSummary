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

root_url = 'https://www.shiyanlou.com/'
driver = webdriver.Firefox()


def register():
    driver.get(root_url)
    time.sleep(2)
    sign_ups = driver.find_elements_by_class_name('sign-up')
    sign_ups[1].click()
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
            action.move_by_offset(2, 0).perform()  #平行移动鼠标
        except UnexpectedAlertPresentException as e: 
            break
        except StaleElementReferenceException as e: 
            break
        action.reset_actions()

    time.sleep(2)

    register = driver.find_elements_by_name('submit')[1]
    action = webdriver.ActionChains(driver)
    action.click(register).perform()
    driver.quit()


if __name__ == '__main__':
    register()

