#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import logging
import logging.config
import traceback


class Logging(object):
    config_path = 'md_logging.json'
    default_level = logging.DEBUG

    def __init__(self, name):
        self.log = logging
        self.setup()
        self.print = self.log.getLogger(name)

    def setup(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    log_config = json.load(f)
                if not os.path.isdir(log_config['path']):
                    os.mkdir(log_config['path'])
                logging.config.dictConfig(log_config)
            except Exception as e:
                print('{}\n{}'.format(e, traceback.format_exc()))
        else:
            log_config = {'path': 'log/'}
            logging.basicConfig(
                filename=log_config['path'] + 'debug.log',
                level=self.default_level,
                format="[%(asctime)s - %(levelname)s  - line(%(lineno)d) - %(filename)s]: %(message)s"
            )

    def debug(self, context):
        self.print.debug(context)

    def info(self, context):
        self.print.info(context)

    def warn(self, context):
        self.print.warn(context)

    def warning(self, context):
        self.print.warning(context)

    def error(self, context):
        self.print.error(context)

    def critical(self, context):
        self.print.critical(context)


logging_example = Logging('Example')


def example_error():
    try:
        a = 1/0
        logging_example.info('error')
    except Exception as e:
        logging_example.error('{}\n{}'.format(e, traceback.format_exc()))


if __name__ == '__main__':
    logging_example.debug('Debug')
    logging_example.info('Start')
    example_error()
