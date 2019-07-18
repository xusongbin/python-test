#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import base64
from selenium import webdriver
from time import time, sleep


class Main(object):
    def __init__(self):
        opt = webdriver.ChromeOptions()
        opt.set_headless()
        self.driver = webdriver.Chrome(executable_path=r'chromedriver.exe', options=opt)
        # self.driver.set_page_load_timeout(10)
        # self.driver.set_script_timeout(10)
        self.username = 'mark3333520@163.com'
        self.password = 'myhdpool=2019.'

        self.url = 'https://hdpool.com/#/login'
        self.open()
        self.close()

    def open(self):
        try:
            self.driver.get(self.url)
            self.driver.implicitly_wait(10)
            self.driver.get_cookies()
            source = self.driver.page_source
            # print(source)
            if re.match(r'.*<div .* class=\"logined\">.*', source, re.S):
                print('logined')
            elif re.match(r'.*<section .* class=\"home-page\">.*', source, re.S):
                print('home page')
            elif re.match(r'.*<section .* class=\"login-page\">.*', source, re.S):
                print('login page')
                p1 = self.driver.find_element_by_xpath('//div[@class="loginp"]/div[1]/div')
                print(p1.text)
                p2 = self.driver.find_element_by_xpath('//div[@class="loginp"]/div[2]')
                print(p2.text)
                p3 = self.driver.find_element_by_xpath('//div[@class="loginp"]/div[5]/img')
                psrc = p3.get_attribute('src')
                print(psrc)
                if re.match(r'data:image/png;base64,.*', psrc):
                    ele_user = self.driver.find_element_by_xpath('//div[@class="loginp"]/div[3]/div[2]/input')
                    ele_user.send_keys(self.username)
                    ele_pwd = self.driver.find_element_by_xpath('//div[@class="loginp"]/div[4]/div[2]/input')
                    ele_pwd.send_keys(self.password)
                    ptype = psrc.split(';')[0].split('/')[1]
                    pbs64 = psrc.split(',')[1]
                    print(p3.get_attribute('src'))
                    with open('code.'+ptype, 'wb') as f:
                        f.write(base64.b64decode(pbs64))
                    code = input('请输入验证码:')
                    ele_code = self.driver.find_element_by_xpath('//div[@class="loginp"]/div[5]/div[2]/input')
                    ele_code.send_keys(code)
                    ele_login = self.driver.find_element_by_xpath('//div[@class="loginp"]/div[7]')
                    ele_login.click()
                    sleep(5)
                    source = self.driver.page_source
                    if re.match(r'.*<div .* class=\"logined\">.*', source, re.S):
                        print('logined')
                    sleep(5)
                else:
                    print('code fetch error!')
            self.driver.close()
            self.driver.quit()
        except Exception as e:
            print('open except:%s' % e)

    def close(self):
        os.system('taskkill /im chrome.exe -f')
        os.system('taskkill /im chromedriver.exe -f')


if __name__ == '__main__':
    app = Main()
