#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import logging
import logging.config
import traceback


def setup_log(config_file='logging.json', default_level=logging.DEBUG):
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            if not os.path.isdir(config['path']):
                os.mkdir(config['path'])
            logging.config.dictConfig(config)
        except Exception as e:
            print('setup_log: {}\n{}'.format(e, traceback.format_exc()))
    else:
        logging.basicConfig(level=default_level)


setup_log()


def fun1():
    logging.info('fun1 run!')


def fun2():
    try:
        a = 1/0
        logging.info('fun2 run!')
    except Exception as e:
        logging.error('{}\n{}'.format(e, traceback.format_exc()))


if __name__ == '__main__':
    logging.debug('test 01')
    fun1()
    logging.debug('test 02')
    fun2()
