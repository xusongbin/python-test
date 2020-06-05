#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from time import sleep
from phone import *


class Dy(object):
    __phone_ip = '192.168.31.81'
    __pkt_name = 'com.ss.android.ugc.aweme'

    __text_qingshaonian = '进入儿童/青少年模式'
    __xpath_know_qingshaonian = '//*[@resource-id="com.ss.android.ugc.aweme:id/com"]/android.widget.LinearLayout[1]'

    __text_guanzhu = '关注'
    __text_tuijian = '推荐'
    __descript_sousuo = '搜索'

    __resourceId_duifang = 'com.ss.android.ugc.aweme:id/emy'
    __resourceId_guanzhu = 'com.ss.android.ugc.aweme:id/b6q'
    __resourceId_zang = 'com.ss.android.ugc.aweme:id/alx'
    __resourceId_zangliang = 'com.ss.android.ugc.aweme:id/aly'
    __resourceId_pinlun = 'com.ss.android.ugc.aweme:id/a7l'
    __resourceId_pinlunliang = 'com.ss.android.ugc.aweme:id/a7n'
    __resourceId_zhuanfa = 'com.ss.android.ugc.aweme:id/dbv'
    __resourceId_zhuanfaliang = 'com.ss.android.ugc.aweme:id/ekt'

    __resourceId_neirong = 'com.ss.android.ugc.aweme:id/gjr'

    __resourceId_biaoti = 'com.ss.android.ugc.aweme:id/title'
    __resourceId_shijian = 'com.ss.android.ugc.aweme:id/g2t'
    __resourceId_jianjie = 'com.ss.android.ugc.aweme:id/a90'
    __resourceId_gequ = 'com.ss.android.ugc.aweme:id/d5h'

    __resourceId_shouye = 'com.ss.android.ugc.aweme:id/f36'
    __text_wo = '我'

    def __init__(self):
        self.device = Device()
        self.device.connect(self.__phone_ip)
        if not self.device.is_running():
            raise Exception('not run')
        print('connect successfully')

    def app_on(self):
        self.device.start(self.__pkt_name)

    def app_off(self):
        self.device.stop(self.__pkt_name)

    def app_info(self):
        _title = self.device.target(resourceId=self.__resourceId_biaoti).info['text']
        _context = self.device.target(resourceId=self.__resourceId_neirong).info['text']
        _zang = self.device.target(resourceId=self.__resourceId_zangliang).info['text']
        _ping = self.device.target(resourceId=self.__resourceId_pinlunliang).info['text']
        print('标题:{} 赞:{} 评论:{} 内容:{}'.format(_title, _zang, _ping, _context))

    def app_next(self):
        # 获取内容区域尺寸
        try:
            _from = [0.500 + random.randrange(-30, 30) / 1000, 0.700 + random.randrange(-10, 10) / 1000]
            _to = [0.500 + random.randrange(-30, 30) / 1000, 0.230 + random.randrange(-10, 10) / 1000]
            self.device.target.swipe(_from[0], _from[1], _to[0], _to[1], random.randrange(100, 250) / 1000)
            print('swipe {} to {}'.format(_from, _to))
            return True
        except Exception as e:
            print('{}\n{}'.format(e, format_exc()))
        return False

    def run(self):
        while True:
            sleep(5 + random.randrange(-1000, 3000) / 10000)
            self.app_next()
            self.app_info()


if __name__ == '__main__':
    dy = Dy()
    dy.run()
