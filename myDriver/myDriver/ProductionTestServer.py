#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import uuid
import json
import requests
from time import time
from traceback import format_exc

from myDriver.hhLog import write_log
from myDriver.hhFile import File


class PtServer(object):
    TYPE_NODE_MODULE = 'node_module'
    TYPE_CARRY_BOARD = 'carry_board'
    TYPE_NODE_PRODUCT = 'node_product'
    TYPE_GATEWAY_MODULE = 'gateway_module'
    TYPE_GATEWAY_PRODUCT = 'gateway_product'

    __path = os.getcwd()
    __aes_key = b'\x07\x09\x31\x21\x75\x67\x3b\x5d\x4f\x21\xab\x9b\xff\xff\xff\xff'
    __aes_iv = b'\xa7\xbc\xdc\x3e\x1f\x27\x43\x73\x88\x51\xad\x36\xff\xff\xff\xff'

    def debug(self, msg):
        if self.__log:
            write_log(msg)

    def __init__(self, config=None, log=False):
        self.__log = log
        self.__config = self.__load_config(config)

    def is_valid(self):
        if self.__config:
            return True
        return False

    def __load_config(self, config):
        _config_ts = 0
        if config:
            _config_file = config
        else:
            _config_file = ''
            for path in os.listdir(self.__path):
                if not re.match(r'configfile[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}_[0-9]{2}_[0-9]{2}\.json', path):
                    continue
                _ts = int(path.split('.')[0][10:].replace('-', '').replace('_', ''))
                if _ts < _config_ts:
                    continue
                _config_ts = _ts
                _config_file = path
        if not File.exists(_config_file):
            self.debug('PtServer not found config!')
            return None
        with open(_config_file, 'rb') as f:
            _edata = f.read()
        try:
            bin_data = File.aes_decrypt(_edata, 'CBC', self.__aes_key, self.__aes_iv)
            str_data = bin_data.decode('utf-8', 'ignore').strip()
            json_data = json.loads(str_data[:str_data.rfind('}')+1])
        except Exception as e:
            self.debug('PtServer config decrypt error!\n{}\n{}'.format(e, format_exc()))
            json_data = {}
        self.debug('PtServer config:{}'.format(json_data))
        return json_data

    def check(self, ptype='node_module', deveui='', uuid='', mac=''):
        if not self.__config:
            return False
        _api_check = '/api/product/hostcomputer/check'
        if not deveui:
            deveui = '{}'.format(time()*1000)
        if not uuid:
            uuid = '{}'.format(time()*1000)
        if not mac:
            mac = '{}'.format(time()*1000)
        if ptype in [self.TYPE_NODE_MODULE, self.TYPE_CARRY_BOARD, self.TYPE_NODE_PRODUCT]:
            data = {
                'model_type': ptype,
                'data': {'deveui': deveui, 'uuid': uuid}
            }
            self.debug('PtServer check {} {} {}'.format(ptype, deveui, uuid))
        elif ptype in [self.TYPE_GATEWAY_MODULE, self.TYPE_GATEWAY_PRODUCT]:
            data = {
                'model_type': ptype,
                'data': {'mac': mac}
            }
            self.debug('PtServer check {} {}'.format(ptype, mac))
        else:
            self.debug('PtServer check type error!')
            return False
        try:
            resp = requests.post(
                self.__config['serverIP'] + _api_check,
                json.dumps(data),
                headers={'x-access-token': self.__config['token']},
                timeout=1
            )
            json_data = resp.json()
            self.debug('PtServer check result:{}'.format(json_data))
            return json_data
        except Exception as e:
            self.debug('{}\n{}'.format(e, format_exc()))
        self.debug('PtServer check error!')
        return False

    def create(self, data):
        if not self.__config:
            return False
        _api_create = '/api/product/hostcomputer/create'
        self.debug('PtServer create:{}'.format(data))
        try:
            resp = requests.post(
                self.__config['serverIP'] + _api_create,
                json.dumps(data),
                headers={'x-access-token': self.__config['token']},
                timeout=1
            )
            json_data = resp.json()
            self.debug('PtServer create result:{}'.format(json_data))
            return json_data
        except Exception as e:
            self.debug('{}\n{}'.format(e, format_exc()))
        self.debug('PtServer create error!')
        return False

    def config(self):
        return self.__config

    def batch_name(self):
        if not self.__config:
            return ''
        return self.__config['batchName']

    def model_name(self):
        if not self.__config:
            return ''
        return self.__config['modelName']

    def model_type(self):
        if not self.__config:
            return ''
        return self.__config['modelType']


def test_check(f):
    pts = PtServer(f)
    print(pts.check('node_product', '478E26DD00280020', '1'))


def test_create():
    from time import time
    pts = PtServer()
    _data = {
        'model_type': 'node_product',
        'tuuid': str(uuid.uuid1()).replace('-', ''),
        'time': int(time()*1000),
        'p_time': int(time()*1000),
        'p_model': 'RHF1SFE0',
        'batch': pts.batch_name(),
        'p_batch': pts.batch_name(),
        'p_test_stage': '1',
        'uuid': '323947083335343720002800',
        'deveui': '478E26DD00280020',
        'p_deveui': '478E26DD00280020',
        'appeui': '526973696E674846',
        'appkey': '526973696E674846478E26DD00280020',
        'version': '1.2.1',
        'p_inter_func1': '25',      # temp
        'p_inter_func2': '103',     # ap
        'p_inter_func3': '1060',    # acc
        'p_ns_rssi': '-80',
        'p_result': 'OK',
        'p_err': '0',
        'p_tms': '12345',
    }
    print(_data)
    print(pts.create(_data))


def test_config(f):
    pts = PtServer(f, True)
    print(json.dumps(pts.config()))


if __name__ == '__main__':
    test_check(r'C:\Users\Administrator\Desktop\12.json')
    # test_create()
    # test_config(r'C:\Users\Administrator\Desktop\12.json')
