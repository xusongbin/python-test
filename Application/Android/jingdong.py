#!/usr/bin/env python
# -*- coding: utf-8 -*-

from phone import *


class Jd(object):
    __phone_ip = '192.168.31.81'
    __pkt_name = 'com.jingdong.app.mall'

    __text_wo = '我的'
    __text_gouwuche = '购物车'

    def __init__(self):
        self.device = Device()
        self.device.connect(self.__phone_ip)
        if not self.device.is_running():
            raise Exception('connect failure')
        print('connect successfully')

    def app_on(self):
        assert isinstance(self.device.target, u2.Device)
        self.device.start(self.__pkt_name)
        while True:
            try:
                info = self.device.target(text=self.__text_wo)
                if info:
                    break
            except Exception as e:
                _ = e
            try:
                info = self.device.target(text=self.__text_gouwuche)
                if info:
                    break
            except Exception as e:
                _ = e
            sleep(1)
        print('app into main page')


if __name__ == '__main__':
    jd = Jd()
    jd.app_on()
