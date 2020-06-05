#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uiautomator2 as u2
from time import sleep
from traceback import format_exc

PACKAGE_JD = 'com.jingdong.app.mall'


class JingDong(object):
    __button_sign_position = (0.501, 0.676)
    __game_main_entry = '浮层活动'
    __game_host_entry = ''
    __game_close = '//*[@content-desc="　"]/android.view.View[10]/android.view.View[1]'
    __game_task_haoyou = '//*[@content-desc="　"]/android.view.View[10]/android.view.View[17]'
    __game_task_other = '//*[@content-desc="　"]/android.view.View[10]/android.view.View[25]'
    __game_task_return = 'com.jingdong.app.mall:id/fe'
    __bottom_home = '//*[@resource-id="com.jingdong.app.mall:id/tj"]/android.widget.FrameLayout[1]'

    def __init__(self, device=None):
        self.mator = UiAutoMator()
        if not device:
            device = self.mator.connect()
        self.jd = device

    def device(self, dev):
        self.jd = dev

    def click_button(self, path):
        try:
            self.jd.xpath(path).click()
        except Exception as e:
            _ = e

    def click_position(self, x, y):
        try:
            self.jd.click(x, y)
        except Exception as e:
            _ = e

    def click_description(self, text):
        try:
            self.jd(description=text).click()
        except Exception as e:
            _ = e

    def task(self):
        _cur_idx = 16
        _cur_text = '//*[@content-desc="　"]/android.view.View[10]/android.view.View[{}]'
        while True:
            _cur_idx += 8
            if _cur_idx > 1000:
                break
            try:
                _info = self.jd.xpath(_cur_text.format(_cur_idx-1)).info['contentDescription']
                if '秒' not in _info:
                    continue
                _info = self.jd.xpath(_cur_text.format(_cur_idx)).info['contentDescription']
                if '去完成' not in _info:
                    continue
                if not bool(_info['enabled']):
                    continue
                self.jd.xpath(_cur_text.format(_cur_idx)).click()
                sleep(15)
                self.jd.xpath(self.__game_task_return).click()
                _cur_idx -= 8
            except Exception as e:
                print('{}\n{}'.format(e,format_exc()))


class AndroidAssist(object):
    def __init__(self):
        self.device = None

    def connect(self, ip=None):
        self.device = None
        try:
            self.device = u2.connect(ip)
        except Exception as e:
            print('{}\n{}'.format(e, format_exc()))
        return self.device

    def lock_unlock(self):
        if not self.device:
            return False
        try:
            self.device.unlock()
            self.device.settings['wait_timeout'] = 0.1
            self.device.xpath('//*[@text="1"]').click()
            self.device.xpath('//*[@text="2"]').click()
            self.device.xpath('//*[@text="3"]').click()
            self.device.xpath('//*[@text="4"]').click()
            self.device.xpath('//*[@text="5"]').click()
            self.device.xpath('//*[@text="6"]').click()
            return True
        except Exception as e:
            print('{}\n{}'.format(e, format_exc()))
        return False

    def app_start(self, pkt):
        if not self.device:
            return False
        try:
            self.device.app_start(pkt)
            return True
        except Exception as e:
            print('{}\n{}'.format(e, format_exc()))
        return False

    def app_stop(self, pkt):
        if not self.device:
            return False
        try:
            self.device.app_stop(pkt)
            return True
        except Exception as e:
            print('{}\n{}'.format(e, format_exc()))
        return False


if __name__ == '__main__':
    # python -m weditor
    ui = JingDong()
    ui.task()
