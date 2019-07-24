#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from time import time, strftime, localtime, mktime, strptime


def write_log(_str):
    _data = strftime("%Y-%m-%d %H:%M:%S", localtime())
    _data += '.%03d ' % (int(time() * 1000) % 1000)
    _data += _str
    try:
        print(_data)
        with open('out.log', 'a+') as f:
            f.write(_data + '\n')
            f.flush()
    except Exception as e:
        print('write log exception %s' % e)

class App(object):
    def __init__(self):
        pass


def main():
    try:
        app = App()
    except Exception as e:
        write_log('app except: %s' % e)


if __name__ == '__main__':
    main()