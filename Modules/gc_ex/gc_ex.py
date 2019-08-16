#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gc
from time import time, sleep


def get_unreachable_memory_len():
    # check memory on memory leaks
    gc.set_debug(gc.DEBUG_SAVEALL)
    gc.collect()
    unreachable = []
    for it in gc.garbage:
        unreachable.append(it)
    print('{}:{}'.format(int(time()), str(unreachable)))
    return len(str(unreachable))


if __name__ == '__main__':
    print(gc.get_threshold())
    # gc.set_threshold(650, 10, 10)
    gc.enable()
    get_unreachable_memory_len()
    for i in range(500):
        mydict = [x for x in range(5)]
        del mydict
    get_unreachable_memory_len()
