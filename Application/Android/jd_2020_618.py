#!/usr/bin/env python
# -*- coding: utf-8 -*-

from phone import *


class Jd(object):
    def __init__(self):
        self.device = Device()
        self.device.connect('192.168.31.130')
        if not self.device.is_running():
            raise Exception('phone not connect')

    def go_activity(self):
        self.device.click_path('//*[@content-desc="浮层活动"]')
