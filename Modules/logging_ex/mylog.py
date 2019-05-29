#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging


class MyLog(object):
    def __init__(self):
        self.log = logging
        self.log.basicConfig(
            filename='log_debug.log',
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.print = self.log.getLogger(__name__)

    def set_logger(self, name):
        self.print = self.log.getLogger(name)

    def debug(self, text):
        self.print.debug(text)
