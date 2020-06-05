#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uiautomator2 as u2
from traceback import format_exc


class Device(object):

    def __init__(self):
        self.target = None
        self.running = False

    def is_running(self):
        return self.running

    def unlock_pwd(self, pwd, reset=False):
        try:
            if reset:
                self.target.screen_off()
            self.target.unlock()
            for i in pwd:
                self.target.xpath('//*[@text="{}"]'.format(i)).click()
            return True
        except Exception as e:
            print('{}\n{}'.format(e, format_exc()))
        return False

    def connect(self, info):
        try:
            self.target = u2.connect(info)
            self.running = True
            return True
        except Exception as e:
            print('{}\n{}'.format(e, format_exc()))
        return False

    def start(self, pkt):
        try:
            self.target.app_start(pkt)
            return True
        except Exception as e:
            print('{}\n{}'.format(e, format_exc()))
        return False

    def stop(self, pkt=None):
        try:
            if not pkt:
                self.target.app_stop_all()
            else:
                self.target.app_stop(pkt)
            return True
        except Exception as e:
            print('{}\n{}'.format(e, format_exc()))
        return False

    def click_path(self, path):
        try:
            self.target.xpath(path).click()
            return True
        except Exception as e:
            print('{}\n{}'.format(e, format_exc()))
        return False

    def click_position(self, position):
        try:
            x, y = position
            self.target.click(x, y)
            return True
        except Exception as e:
            print('{}\n{}'.format(e, format_exc()))
        return False

    def click_text(self, text):
        try:
            self.target(text=text).click()
            return True
        except Exception as e:
            print('{}\n{}'.format(e, format_exc()))
        return False

    def click_resourceId(self, click_resourceId):
        try:
            self.target(resourceId=click_resourceId).click()
            return True
        except Exception as e:
            print('{}\n{}'.format(e, format_exc()))
        return False
