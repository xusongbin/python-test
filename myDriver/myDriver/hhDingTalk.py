#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
from time import time
from myDriver.hhRequests import Requests
from traceback import format_exc


class DingTalk(object):
    __url_head = 'https://oapi.dingtalk.com/robot/send?access_token'
    __headers = {'Content-Type': 'application/json;charset=utf-8'}

    def __init__(self, url, limit=15):
        self.__requests = Requests()
        if re.match(r'^[0-9a-f]+$', url):
            self.__web_hook = '{}={}'.format(self.__url_head, url)
        elif '=' in url and url.split('=')[0] == self.__url_head:
            self.__web_hook = url
        else:
            raise Exception('url error')
        self.__post_list = []
        self.__limit = limit

    def check_idle(self):
        while len(self.__post_list) >= self.__limit:
            if time() - self.__post_list[0] > 60:
                self.__post_list.remove(self.__post_list[0])
            else:
                break
        if len(self.__post_list) < self.__limit:
            self.__post_list.append(time())
            return True
        return False

    def send(self, data, msgtype='text'):
        '''
        :param data:
        :param msgtype: text / markdown
        :return:
        '''
        if not self.check_idle():
            print('Wait for idle!')
            return False
        _pack = {
            'msgtype': msgtype,
            msgtype: {'content': data}
        }
        _pack_str = json.dumps(_pack)
        try:
            _recv = self.__requests.post(self.__web_hook, bytes(_pack_str, 'utf-8'), self.__headers).json()
            if _recv['errmsg'] == 'ok':
                return True
        except Exception as e:
            print('{}\n{}'.format(e, format_exc()))
        return False


if __name__ == '__main__':
    dt = DingTalk('1893559e78c465f77b33c3376c7ee85927897717d1f5b604933bd352cbee6018')
    dt.send('PER:123')
