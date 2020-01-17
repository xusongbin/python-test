#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import time
import gevent
from gevent import monkey
monkey.patch_socket()


def do_something(title):
    for i in range(100):
        print('{} {}'.format(int(time()), title))


for _ in range(10):
    gt = []
    for k in range(10):
        gt.append(gevent.spawn(do_something, k))
    gevent.joinall(gt, timeout=10)

