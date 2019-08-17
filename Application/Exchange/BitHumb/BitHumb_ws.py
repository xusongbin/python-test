#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from md_logging import setup_log

setup_log()
write_log = logging.getLogger('BITHUMB_WS')


class BitHumbWs(object):
    def __init__(self):
        self.depth_ws =


if __name__ == '__main__':
    bh_ws = BitHumbWs()
