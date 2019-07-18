#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import threading
from selenium import webdriver
from my_driver import *


class Main(object):
    web_hook = ('https://oapi.dingtalk.com/robot/send?'
                'access_token=836c4833037901bb7c077e402ccea800094a1b524ee4108344c6feb1489ab8f1')
    account_id = 'QWUP-Q2G8-8P8T-68JKP'
    boom_url = 'http://boom.onepool.co/'
    burst_url = 'http://brs.kuangjiwan.com/'

    def __init__(self):
        opt = webdriver.ChromeOptions()
        # opt.set_headless()
        self.web = webdriver.Chrome(executable_path=r'chromedriver.exe', options=opt)
        self.dt = MyDingTalk(self.web_hook)

        self.get_burst()

        os.system('taskkill /im chrome.exe -f')
        os.system('taskkill /im chromedriver.exe -f')

    def get_boom(self):
        self.web.get(self.boom_url)
        self.web.get_cookies()
        self.web.find_element_by_id('account-id-input').send_keys(self.account_id)
        self.web.find_element_by_id('subscribe-button').click()
        print(self.web.find_element_by_id('miner-pending').text)
        print(self.web.page_source)
        self.web.close()

    def get_burst(self):
        self.web.get(self.burst_url)
        self.web.get_cookies()
        self.web.find_element_by_id('account-id-input').send_keys(self.account_id)
        self.web.find_element_by_id('subscribe-button').click()
        print(self.web.find_element_by_id('miner-pending').text)
        print(self.web.page_source)
        self.web.close()


if __name__ == '__main__':
    app = Main()
