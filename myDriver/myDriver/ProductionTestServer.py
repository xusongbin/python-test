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
    ERROR_CODE = {
        0:    "ok",
        1001: "系统繁忙",
        1002: "缺少token，请重新登录",
        1003: "无效token，请重新登录",
        1004: "空参数",
        1005: "参数错误",
        1006: "权限错误",
        1007: "查询错误",

        2001: "无效账号",
        2002: "账号名或密码错误",
        2003: "账号已存在",
        2004: "账号不存在",
        2005: "账号被禁用",
        2006: "上位机账户禁止登录",
        2007: "禁止更新超级管理员信息",
        2008: "新密码和旧密码一样",

        3001: "工厂名或编码已存在",
        3002: "工厂不存在",
        3003: "工厂已关联批次，不允许更新或删除",

        3201: "型号已存在",
        3202: "型号不存在",
        3203: "型号已关联批次，不允许更新或删除",
        3204: "型号类型不匹配",
        3205: "产品标识已存在",
        3206: "型号已关联文件",

        3401: "批次已存在",
        3402: "批次不存在",
        3403: "批次已结束",
        3404: "批次阶段不匹配",
        3405: "批次已关联数据，不允许更新或删除",
        3406: "批次已启动，不允许更新",
        3407: "批次已关联文件",
        3408: "批次查询错误",

        3601: "MAC地址已关联测试数据，不允许删除",

        4001: "文件摘要不存在",
        4002: "文件已存在",
        4003: "文件摘要错误",
        4004: "文件获取错误",
        4005: "文件读取错误",

        4201: "图片摘要不存在",
        4202: "图片已存在",
        4203: "图片摘要错误",
        4204: "图片被关联，不允许删除",

        5001: "DevEUI重复",
        5002: "UUID重复",
        5003: "DevEUI和UUID都重复",
        5004: "MAC地址重复",
        5005: "第一阶段数据未找到",
        5006: "跳过测试步骤",
        5007: "打开sqlite数据库错误",
        5008: "读取表数据错误",
        5009: "插入表数据错误",
        5010: "更新表数据错误",
        5011: "合并表数据错误",
        5012: "SN码重复",
        5013: "MAC地址和SN码都重复",
        5014: "TUUID重复",
        5015: "重复测试",
    }
    TYPE_NODE_MODULE = 'node_module'
    TYPE_CARRY_BOARD = 'carry_board'
    TYPE_NODE_PRODUCT = 'node_product'
    TYPE_GATEWAY_MODULE = 'gateway_module'
    TYPE_GATEWAY_PRODUCT = 'gateway_product'

    __api_check = '/api/product/hostcomputer/check'
    __api_create = '/api/product/hostcomputer/create'
    __api_dbfile = '/api/product/hostcomputer/dbfile'
    __api_logfile = '/api/product/hostcomputer/logfile'

    __path = os.getcwd()
    __aes_key = b'\x07\x09\x31\x21\x75\x67\x3b\x5d\x4f\x21\xab\x9b\xff\xff\xff\xff'
    __aes_iv = b'\xa7\xbc\xdc\x3e\x1f\x27\x43\x73\x88\x51\xad\x36\xff\xff\xff\xff'

    def debug(self, msg):
        if self.__log:
            write_log(msg)

    def __init__(self, config=None, log=False):
        self.__online = False
        self.__log = log
        self.__config = self.__load_config(config)

    def is_valid(self):
        if self.__config:
            return True
        return False

    def is_online(self):
        if self.__online:
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
                self.__config['serverIP'] + self.__api_check,
                json.dumps(data),
                headers={'x-access-token': self.__config['token']},
                timeout=3.05
            )
            json_data = resp.json()
            self.debug('PtServer check result:{}'.format(json_data))
            if 'code' not in json_data.keys():
                return False
            if 0 < int(json_data['code']) < 5000:
                return False
            self.__online = True
            return json_data
        except Exception as e:
            self.debug('{}\n{}'.format(e, format_exc()))
        self.__online = False
        self.debug('PtServer check error!')
        return False

    def create(self, data, ip=None, token=None):
        if not ip and not token:
            if not self.__config:
                return False
            ip = self.__config['serverIP']
            token = self.__config['token']
        self.debug('PtServer create:{}'.format(data))
        try:
            resp = requests.post(
                ip + self.__api_create,
                json.dumps(data),
                headers={'x-access-token': token},
                timeout=3.05
            )
            json_data = resp.json()
            self.debug('PtServer create result:{}'.format(json_data))
            return json_data
        except Exception as e:
            self.debug('{}\n{}'.format(e, format_exc()))
        self.debug('PtServer create error!')
        return False

    def upload_db(self, file):
        if not self.__config:
            return False
        self.debug('PtServer upload_db:{}'.format(os.path.basename(file)))
        try:
            with open(file, 'rb') as f:
                _md5 = File.md5_encode(f.read())
            data = {
                'batchName': self.batch_name(),
                'modelName': self.model_name(),
                'modelType': self.model_type(),
                'fileName': os.path.basename(file),
                'fileType': 4,
                'fileMode': True,
                'digest': _md5
            }
            print(data)
            resp = requests.post(
                self.__config['serverIP'] + self.__api_dbfile,
                data,
                files={'file': open(file, 'rb')},
                headers={'x-access-token': self.__config['token']}
            )
            json_data = resp.json()
            self.debug('PtServer upload_db result:{}'.format(json_data))
            return json_data
        except Exception as e:
            self.debug('{}\n{}'.format(e, format_exc()))
        self.debug('PtServer upload_db error!')
        return False

    def upload_log(self, file):
        if not self.__config:
            return False
        self.debug('PtServer upload_log:{}'.format(os.path.basename(file)))
        try:
            with open(file, 'rb') as f:
                _md5 = File.md5_encode(f.read())
            data = {
                'batchName': self.batch_name(),
                'modelName': self.model_name(),
                'modelType': self.model_type(),
                'fileName': os.path.basename(file),
                'fileType': 5,
                'fileMode': True,
                'digest': _md5
            }
            resp = requests.post(
                self.__config['serverIP'] + self.__api_logfile,
                data,
                files={'file': open(file, 'rb')},
                headers={'x-access-token': self.__config['token']}
            )
            json_data = resp.json()
            self.debug('PtServer upload_log result:{}'.format(json_data))
            return json_data
        except Exception as e:
            self.debug('{}\n{}'.format(e, format_exc()))
        self.debug('PtServer upload_log error!')
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

    def server_ip(self):
        if not self.__config:
            return ''
        return self.__config['serverIP']

    def token(self):
        if not self.__config:
            return ''
        return self.__config['token']


def test_check(f):
    pts = PtServer(f)
    print(pts.config())
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


def test_upload(f):
    pts = PtServer(f, True)
    print(pts.upload_db(r'C:\Users\Administrator\Desktop\jig.db'))


if __name__ == '__main__':
    # test_check(r'C:\Users\Administrator\Desktop\configfile_rhf0m003_0m00320110_2020-09-18_11_19_57.json')
    # test_create()
    # test_config(r'C:\Users\Administrator\Desktop\12.json')
    test_upload(r'C:\Users\Administrator\Desktop\configfile_rhf0m003_0m0032084c_2020-09-18_12_07_54.json')
