#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
from traceback import format_exc

from myDriver.hhLog import write_log


class Requests(object):
    def post(self, url, data, headers=None, timeout=3):
        # _respond.text
        # _respond.content
        # _respond.json()
        # data = json.dumps(data)
        # data = bytes(pkt, 'utf-8')
        try:
            _respond = requests.post(url, data, headers=headers, timeout=timeout)
            return _respond
        except Exception as e:
            write_log('{}\n{}'.format(e, format_exc()))
        return None

    def get(self, url, headers=None, timeout=3):
        # _respond.text
        # _respond.content
        # _respond.json()
        try:
            _respond = requests.get(url, headers=headers, timeout=timeout)
            return _respond
        except Exception as e:
            write_log('{}\n{}'.format(e, format_exc()))
        return None

    def upload(self, url, file, headers=None):
        try:
            _respond = requests.post(url=url, file={'file': open(file, 'rb')}, headers=headers)
            return _respond
        except Exception as e:
            write_log('{}\n{}'.format(e, format_exc()))
        return None


if __name__ == '__main__':
    req = Requests()
    _headers = {'x-access-token': 'qUakJaDGxmb6CcOdqvanpw=='}
    _url = 'http://192.168.0.223:7070/openapi/device/downlink/create'
    _post_data = {
        'devEUI': '477CBB8800380022',
        'confirmed': False,
        'fPort': 8,
        'data': 'MTIz'
    }
    # resp = req.post(_url, json.dumps(_post_data), _headers)
    _get_url = 'http://ifconfig.me/ip'
    _get_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)', 'Host': 'ifconfig.me'}
    resp = req.get(_get_url, _get_headers)
    print(resp.text)
