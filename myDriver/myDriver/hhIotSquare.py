#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
from time import strftime, strptime, mktime, time, localtime
from myDriver.hhFile import File
from myDriver.hhRequests import Requests
from traceback import format_exc


class IotSquare(object):
    # web api
    # if you use web api, you must get token by debugging the web page
    __dev_ul_history = '/api/device/history'
    __dev_dl_history = '/api/device/downlink/history'
    # openapi
    __dev_dl_create = '/openapi/device/downlink/create'
    __dev_mcdl_create = '/openapi/mcdownlink/create'
    # token
    __headers = {
        'x-access-token': ''
    }

    def __init__(self, token, url='http://192.168.0.223:7070'):
        self.__url = url
        self.__token = token
        self.__request = Requests()
        self.__headers['x-access-token'] = self.__token

    def his_uplink(self, deveui, start=None, stop=None, size=10000, page=1):
        deveui = deveui.strip().replace(':', '').replace('-', '')
        if not re.match(r'^[0-9a-fA-F]{16}$', deveui):
            raise Exception("DevEui must be 8 bytes")
        if start and not re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', start):
            raise Exception("start except.Datetime must be of type %Y-%m-%d %H:%M:%S")
        if stop and not re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', stop):
            raise Exception("stop except.Datetime must be of type %Y-%m-%d %H:%M:%S")
        if start:
            _ts_start = int(mktime(strptime(start, "%Y-%m-%d %H:%M:%S")))
        else:
            _ts_start = int(time() / 86400) * 86400 - 8 * 3600
        if stop:
            _ts_stop = int(mktime(strptime(stop, "%Y-%m-%d %H:%M:%S")))
        else:
            _ts_stop = int(time() / 86400) * 86400 + 86400 - 1 - 8 * 3600
        _url = '{}?devEUI={}&pageNo={}&pageSize={}&startTime={}&endTime={}'.format(
            self.__url + self.__dev_ul_history,
            deveui,
            page,
            size,
            _ts_start,
            _ts_stop
        )
        try:
            recv = self.__request.get(_url, headers=self.__headers).json()
            print(recv)
        except Exception as e:
            print('{}\n{}'.format(e, format_exc()))
            return None
        if not recv:
            print('Function not respond')
            return None
        if not type(recv) is dict:
            print('Respond not dict')
            return None
        if 'msg' not in recv.keys():
            print('Respond has not key: msg')
            return None
        if 'amount' not in recv.keys():
            print('Respond has not key: amount')
            return None
        if 'data' not in recv.keys():
            print('Respond has not key: data')
            return None
        if not recv['msg'] == 'ok':
            print('Respond error:{}'.format(recv['msg']))
            return None
        _start = strftime("%Y-%m-%d %H:%M:%S", localtime(_ts_start))
        _stop = strftime("%Y-%m-%d %H:%M:%S", localtime(_ts_stop))
        return _start, _stop, recv['amount'], recv['data']

    def his_downlink(self, deveui, start=None, stop=None, size=10000, page=1):
        deveui = deveui.strip().replace(':', '').replace('-', '')
        if not re.match(r'^[0-9a-fA-F]{16}$', deveui):
            raise Exception("DevEui must be 8 bytes")
        if start and not re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', start):
            raise Exception("start except.Datetime must be of type %Y-%m-%d %H:%M:%S")
        if stop and not re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', stop):
            raise Exception("stop except.Datetime must be of type %Y-%m-%d %H:%M:%S")
        if start:
            _ts_start = int(mktime(strptime(start, "%Y-%m-%d %H:%M:%S")))
        else:
            _ts_start = int(time() / 86400) * 86400 - 8 * 3600
        if stop:
            _ts_stop = int(mktime(strptime(stop, "%Y-%m-%d %H:%M:%S")))
        else:
            _ts_stop = int(time() / 86400) * 86400 + 86400 - 1 - 8 * 3600
        _url = '{}?devEUI={}&pageNo={}&pageSize={}&startTime={}&endTime={}'.format(
            self.__url + self.__dev_dl_history,
            deveui,
            page,
            size,
            _ts_start,
            _ts_stop
        )
        try:
            recv = self.__request.get(_url, headers=self.__headers).json()
            print(recv)
        except Exception as e:
            print('{}\n{}'.format(e, format_exc()))
            return None
        if not recv:
            print('Function not respond')
            return None
        if not type(recv) is dict:
            print('Respond not dict')
            return None
        if 'msg' not in recv.keys():
            print('Respond has not key: msg')
            return None
        if 'amount' not in recv.keys():
            print('Respond has not key: amount')
            return None
        if 'data' not in recv.keys():
            print('Respond has not key: data')
            return None
        if not recv['msg'] == 'ok':
            print('Respond error:{}'.format(recv['msg']))
            return None
        _start = strftime("%Y-%m-%d %H:%M:%S", localtime(_ts_start))
        _stop = strftime("%Y-%m-%d %H:%M:%S", localtime(_ts_stop))
        return _start, _stop, recv['amount'], recv['data']

    def downlink(self, deveui, msg, port=8, confirmed=False):
        deveui = deveui.strip().replace(':', '').replace('-', '')
        if not re.match(r'^[0-9a-fA-F]{16}$', deveui):
            raise Exception("DevEui must be 8 bytes")
        _data = {
            'devEUI': deveui,
            'confirmed': confirmed,
            'fPort': port,
            'data': File.base64_encode(msg)
        }
        try:
            recv = self.__request.post(self.__url + self.__dev_dl_create, json.dumps(_data), self.__headers).json()
            print(recv)
        except Exception as e:
            print('{}\n{}'.format(e, format_exc()))
            return None
        if not recv:
            print('Function not respond')
            return None
        if not type(recv) is dict:
            print('Respond not dict')
            return None
        if 'fCnt' not in recv.keys():
            print('Respond has not fCnt')
            return None
        if not recv['msg'] == 'ok':
            print('Respond error:{}'.format(recv['msg']))
            return None
        return recv['fCnt']

    def mcdownlink(self, deveui, msg, port=8):
        deveui = deveui.strip().replace(':', '').replace('-', '')
        if not re.match(r'^[0-9a-fA-F]{16}$', deveui):
            raise Exception("DevEui must be 8 bytes")
        _data = {
            'mcEUI': deveui,
            'fPort': port,
            'data': File.base64_encode(msg)
        }
        try:
            recv = self.__request.post(self.__url + self.__dev_dl_create, json.dumps(_data), self.__headers).json()
            print(recv)
        except Exception as e:
            print('{}\n{}'.format(e, format_exc()))
            return None
        if not recv:
            print('Function not respond')
            return None
        if not type(recv) is dict:
            print('Respond not dict')
            return None
        if 'fCnt' not in recv.keys():
            print('Respond has not fCnt')
            return None
        if not recv['msg'] == 'ok':
            print('Respond error:{}'.format(recv['msg']))
            return None
        return recv['fCnt']


if __name__ == '__main__':
    # iot = IotSquare(token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MDAwNzU3MTAsImlkIjoxLCJ0b2tlbiI6IjZmNjU2NjZjNTc1MzYyNmM0OTQ0NGY3NSJ9.swCbIPnEs0RuHkP-7xJtZAJWKWT3OkijoCK4vn1GdwY')
    # data = iot.get_uplink('8C-F9-57-20-00-03-6E-B9', '2020-09-01 00:00:00', size=100)
    # if data:
    #     start, stop, amount, data = data
    #     print(start)
    #     print(stop)
    #     print(amount)
    #     for d in data:
    #         print(d)
    # data = iot.get_downlink('8C-F9-57-20-00-03-6E-B9', '2020-09-01 00:00:00', size=100)
    # if data:
    #     start, stop, amount, data = data
    #     print(start)
    #     print(stop)
    #     print(amount)
    #     for d in data:
    #         print(d)
    iot = IotSquare('qUakJaDGxmb6CcOdqvanpw==')
    print(iot.downlink('8C-F9-57-20-00-03-6E-AA', '123'))
