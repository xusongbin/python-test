#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import logging
import logging.config
import traceback


def setup_log():
    config_path = 'md_logging.json'
    default_level = logging.DEBUG
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
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
            level=default_level,
            format="[%(asctime)s - %(levelname)s  - line(%(lineno)d) - %(filename)s]: %(message)s"
        )
