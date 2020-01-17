#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gevent_ex import *
from gc_ex import *
from urllib_ex import *


if __name__ == '__main__':
    gc.set_threshold(10, 10, 10)
    get_unreachable_memory_len()
    # for i in range(10):
    gt = []
    for j in range(10):
        gt.append(gevent.spawn(do_get_page, 'http://www.baidu.com'))
    gevent.joinall(gt, timeout=5)
    sleep(10)
    get_unreachable_memory_len()
