#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import queue
import threading
import hmac
from hashlib import sha256
from urllib import parse
from time import time, sleep

import websocket

import logging
import traceback
from md_logging import setup_log

setup_log()
write_log = logging.getLogger('BITHUMB_WS')


class BitHumbWs(object):
    def __init__(self):
        self.depth_ws =


if __name__ == '__main__':
    bh_ws = BitHumbWs()
