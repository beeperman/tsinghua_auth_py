#!/usr/bin/env python3
from selenium import webdriver
import os

# use your own credentials
usernm = 'username'
passwd = 'password'
url = 'http://auth4.tsinghua.edu.cn'

browser = webdriver.PhantomJS(service_log_path=os.devnull)

browser.get(url)
browser.implicitly_wait(3)

is_pswd_found = False
try:
    # do login
    username = browser.find_element_by_id('username')
    password = browser.find_element_by_id('password')
    connect = browser.find_element_by_id('connect')
    is_pswd_found = True

    username.clear()
    username.send_keys(usernm)

    password.clear()
    password.send_keys(passwd)

    connect.submit()
    print('successfully pressed connect button')

    # check login status
    browser.get(url)
    browser.implicitly_wait(3)

    disconnect = browser.find_element_by_class_name('disconnect')
    print('login success')
except Exception as e:
    # some failure
    if is_pswd_found:
        print('login failure. please check your credentials')
        print(e.__str__())
    else:
        print('already logged in.')

browser.close()
