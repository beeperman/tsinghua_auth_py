#!/usr/bin/env python3
from selenium import webdriver
import time
import sys
import os

# off-campus network access
off_camp = True

# re-login time (in hour) 0: don't re-login
re_login_time = 0

# use your own credentials
usernm = 'username'
passwd = 'password'
url = 'http://auth4.tsinghua.edu.cn'

# or import from credentials.py (will override the settings above)
# create credentials.py and assign values to setting variables above (e.g. usernm, passwd) in it
try:
    from credentials import *
    print('loading settings from credentials.py')
except Exception as e:
    print('not loading anything from credentials.py')
    print(e.__str__(), file=sys.stderr)

xor = lambda x, y: bool(x) != bool(y)

browser = webdriver.PhantomJS(service_log_path=os.devnull)
#browser = webdriver.Firefox()

def headless_login():
    browser.get(url)
    browser.implicitly_wait(3)

    def check_login(auto_logout = False):
        # check login status helper function
        browser.get(url)
        browser.implicitly_wait(3)

        disconnect = browser.find_element_by_id('form3')
        clock = browser.find_element_by_id('clock')


        if auto_logout and re_login_time != 0:
            hour = clock.text.split(':')[0]
            if off_camp and (hour == '' or hour == 'NaN'
                or int(hour) >= re_login_time):
                print('Has been logged in for ' + clock.text + '. Performing re-login.')
                disconnect.submit()
                return True

        return False

    is_pswd_found = False
    try:
        # do login
        username = browser.find_element_by_id('username')
        password = browser.find_element_by_id('password')
        connect = browser.find_element_by_id('connect')
        is_pswd_found = True

        # network access type
        off_campus = browser.find_element_by_name('save_me')
        if xor(off_camp, off_campus.is_selected()):
            off_campus.click()
        assert (off_camp == off_campus.is_selected())
        print('set network access type to ' + 'off_campus' if off_camp else 'on_campus only')

        username.clear()
        username.send_keys(usernm)

        password.clear()
        password.send_keys(passwd)

        connect.submit()
        print('successfully pressed connect button')

        time.sleep(2)
        check_login()
        print('login success')
    except Exception as e:
        # some failure
        if is_pswd_found:
            print('login failure. please check your credentials')
            print(e.__str__(), file=sys.stderr)
        else:
            print('already logged in.')
            return check_login(auto_logout=True)
    return False

# re-run login if login time exceed time limit
if headless_login():
    time.sleep(10)
    headless_login()

browser.close()
