#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
from time import strftime, localtime
from traceback import format_exc

import gc
gc.set_threshold(50, 10, 10)
gc.enable()


class DingPost(object):
    __robot = (
        'https://oapi.dingtalk.com/robot/send?access_token='
        '7a45b3d175f5060361726500dab381992d0547bc185ae5d15eb5744ce70adbb1'
    )
    __markdown_file = 'property.md'

    def __init__(self):
        pass

    @staticmethod
    def __markdown_msg(context=''):
        _time = strftime("%Y-%m-%d %H:%M:%S", localtime())
        _pack = {
            'msgtype': 'markdown',
            'markdown': {'title': _time, 'text': '#### {}\n{}'.format(_time, context)}
        }
        try:
            return json.dumps(_pack)
        except Exception as e:
            print('{}\n{}'.format(e, format_exc()))
        return None

    def __list_to_md_string(self, data):
        with open(self.__markdown_file, 'r', encoding='utf-8') as f:
            md = f.read()
        return md.format(*data)

    def post_md_msg(self, context=''):
        headers = {
            'Content-Type': 'application/json;charset=utf-8'
        }
        _data = self.__markdown_msg(context)
        try:
            _respond = requests.post(self.__robot, data=_data, headers=headers, timeout=3)
            context = _respond.json()
            if context['errcode'] == 0:
                return True
        except Exception as e:
            print('{}\n{}'.format(e, format_exc()))
        return False

    def post_md_list(self, _data):
        return self.post_md_msg(self.__list_to_md_string(_data))


if __name__ == '__main__':
    dp = DingPost()
    # dp.post_md_msg('123')
    dp.post_md_list([i for i in range(32)])
