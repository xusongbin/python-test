#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fetch import get_account
from update import set_server, get_server


from time import time, sleep


def millis():
    return int(time() * 1000)


def elapsed(t):
    return millis()-t


def run():
    tms = 0
    addr, port, pwd = get_server()
    while True:
        if elapsed(tms) > 1000 * 60:
            tms = millis()

            a, b, c = get_account()
            a, b, c = a[2], b[2], c[2]
            if any([addr != a, port != b, pwd != c]):
                addr = a
                port = b
                pwd = c
                set_server(a, b, c)
        sleep(5)


if __name__ == '__main__':
    run()
