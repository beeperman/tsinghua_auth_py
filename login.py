#!/usr/bin/env python3
from selenium import webdriver
import sys
import os

# off-campus network access
off_camp = True

# use your own credentials
usernm = 'username'
passwd = 'password'
url = 'http://auth4.tsinghua.edu.cn'

# or import from credentials.py
try:
    from credentials import *
    print('loading settings from credentials.py')
except Exception as e:
    print('not loading anything from credentials.py')
    print(e.__str__(), file=sys.stderr)

xor = lambda x, y: bool(x) != bool(y)

browser = webdriver.PhantomJS(service_log_path=os.devnull)
#browser = webdriver.Firefox()

browser.get(url)
browser.implicitly_wait(3)

is_pswd_found = False
try:
    # network access type
    off_campus = browser.find_element_by_name('save_me')
    if xor(off_camp, off_campus.is_selected()):
        off_campus.click()
    assert(off_camp == off_campus.is_selected())
    print('set network access type to ' + 'off_campus' if off_camp else 'on_campus only')

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
        print(e.__str__(), file=sys.stderr)
    else:
        print('already logged in.')

browser.close()
