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
    server = get_server()
    if server:
        addr, port, pwd = server[0], server[1], server[2]
    else:
        addr, port, pwd = '', '', ''
    while True:
        if elapsed(tms) > 1000 * 60:
            tms = millis()

            server = get_account()
            if not server:
                continue
            a, b, c = server[0][2], server[1][2], server[2][2]
            if not any([addr != a, port != b, pwd != c]):
                continue
            if set_server(a, b, c):
                addr, port, pwd = a, b, c
        sleep(5)


if __name__ == '__main__':
    run()
