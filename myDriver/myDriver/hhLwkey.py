#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from traceback import format_exc
from myDriver.hhFile import File
from myDriver.hhTransform import Transform
from myDriver.hhLog import write_log


class LwKey(object):
    def __init__(self, path='lwkey.exe', key='2B7E151628AED2A6ABF7158809CF4F3C'):
        self.path = path    # 'lwkey.exe'
        self.key = key
        self.tf = Transform()

    @staticmethod
    def check_eui(data):
        if type(data) is not str:
            raise Exception("EUI must be string")
        data = data.replace(':', '').replace('-', '').upper()
        if not re.match(r'[0-9A-F]{16}', data):
            raise Exception("EUI format error")
        return data

    def get(self, deveui, appeui='52:69:73:69:6E:67:48:46', devaddr=0):
        deveui = self.check_eui(deveui)
        appeui = self.check_eui(appeui)
        if type(devaddr) == str:
            devaddr = str(devaddr).replace(':', '').replace('-', '')
        if not File.exists(self.path):
            write_log('{} not exists!'.format(self.path))
            return ''
        data = ''
        cmd = '{} -a {} -d {} -D {} -k {} -n {}'.format(
            self.path, appeui, deveui, devaddr, self.key, 1)
        print(cmd)
        try:
            key_respond = os.popen(cmd).read().strip()
            key_file = str(key_respond).split('\n')[1].split(' ')[-1]
            with open(key_file, 'r') as f:
                data = f.read().split('\n')[1]
            os.remove(key_file)
        except Exception as e:
            write_log('{}\n{}'.format(e, format_exc()))
        print('deveui, appeui, appkey, devaddr, nwkskey, appskey')
        appeui, deveui, devaddr, nwkskey, appskey, appkey = data.split(',')
        return '{},{},{},{},{},{}'.format(
            deveui, appeui, appkey, devaddr, nwkskey, appskey
        )

    def generate(self, deveui, appeui='52:69:73:69:6E:67:48:46', devaddr=0):
        deveui = self.check_eui(deveui)
        appeui = self.check_eui(appeui)
        dd = self.tf.hex_to_dec(deveui[8:], little=False)
        devaddr_int = (dd & 0x0FFFFF) + devaddr
        devaddr = self.tf.bytes_to_hex(self.tf.int_to_bytes(devaddr_int, order='big', sign=False)).upper()
        b = b'\x11\xAA\x1A\xA1' + self.tf.str_to_bytes(deveui) + self.tf.str_to_bytes(deveui)[4:]
        nwkskey = self.tf.bytes_to_hex(File.aes_encrypt(b, key=self.tf.str_to_bytes(self.key))).upper()
        b = b'\x22\xBB\x2B\xB2' + self.tf.str_to_bytes(deveui) + self.tf.str_to_bytes(deveui)[4:]
        appskey = self.tf.bytes_to_hex(File.aes_encrypt(b, key=self.tf.str_to_bytes(self.key))).upper()
        b = b'\x33\xCC\x3C\xC3' + self.tf.str_to_bytes(deveui) + self.tf.str_to_bytes(deveui)[4:]
        appkey = self.tf.bytes_to_hex(File.aes_encrypt(b, key=self.tf.str_to_bytes(self.key))).upper()
        print('DEVEUI, APPEUI, APPKEY, DEVADDR, NWKSKEY, APPSKEY')
        return '{},{},{},{},{},{}'.format(
            deveui, appeui, appkey, devaddr, nwkskey, appskey
        )

    def idall(self, deveui, appeui='52:69:73:69:6E:67:48:46', devaddr=0):
        deveui = self.check_eui(deveui)
        appeui = self.check_eui(appeui)
        dd = self.tf.hex_to_dec(deveui[8:], little=False)
        devaddr_int = (dd & 0x0FFFFF) + devaddr
        devaddr = self.tf.bytes_to_hex(self.tf.int_to_bytes(devaddr_int, order='big', sign=False)).upper()
        b = b'\x11\xAA\x1A\xA1' + self.tf.str_to_bytes(deveui) + self.tf.str_to_bytes(deveui)[4:]
        nwkskey = self.tf.bytes_to_hex(File.aes_encrypt(b, key=self.tf.str_to_bytes(self.key))).upper()
        b = b'\x22\xBB\x2B\xB2' + self.tf.str_to_bytes(deveui) + self.tf.str_to_bytes(deveui)[4:]
        appskey = self.tf.bytes_to_hex(File.aes_encrypt(b, key=self.tf.str_to_bytes(self.key))).upper()
        b = b'\x33\xCC\x3C\xC3' + self.tf.str_to_bytes(deveui) + self.tf.str_to_bytes(deveui)[4:]
        appkey = self.tf.bytes_to_hex(File.aes_encrypt(b, key=self.tf.str_to_bytes(self.key))).upper()
        print('APPEUI, DEVEUI, DEVADDR, NWKSKEY, APPSKEY, APPKEY')
        return '{}{}{}{}{}{}'.format(
            appeui, deveui, devaddr, nwkskey, appskey, appkey
        )

    def default(self, deveui, appeui='8CF9572000000000'):
        deveui = self.check_eui(deveui)
        appeui = self.check_eui(appeui)
        appkey = '2B7E151628AED2A6ABF7158809CF4F3C'
        devaddr = deveui[8:]
        nwkskey = '2B7E151628AED2A6ABF7158809CF4F3C'
        appskey = '2B7E151628AED2A6ABF7158809CF4F3C'
        return '{},{},{},{},{},{}'.format(deveui, appeui, appkey, devaddr, nwkskey, appskey)


class LwSign(object):
    def __init__(self, path='lwsign.exe'):
        self.path = path    # 'lwsign.exe'

    @staticmethod
    def check_eui(data):
        if type(data) is not str:
            raise Exception("EUI must be string")
        data = data.replace(':', '').replace('-', '').upper()
        if not re.match(r'[0-9A-F]{16}', data):
            raise Exception("EUI format error")
        return data

    def get(self, deveui, appeui='52:69:73:69:6E:67:48:46'):
        deveui = self.check_eui(deveui)
        appeui = self.check_eui(appeui)
        if not File.exists(self.path):
            write_log('{} not exists!'.format(self.path))
            return ''
        data = {}
        cmd = '{} -d {} -a {} -K'.format(self.path, deveui, appeui)
        print(cmd)
        key_respond = str(os.popen(cmd).read()).strip()
        for line in key_respond.split('\n'):
            name, context = line.split(',')
            data[name.strip()] = context.strip()
        print('deveui, appeui, appkey, devaddr, nwkskey, appskey, sign')
        return '{},{},{},{},{},{},{}'.format(
            data['deveui'], data['appeui'], data['appkey'],
            data['devaddr'], data['nwkskey'], data['appskey'], data['sign']
        )


if __name__ == '__main__':
    # appeui	deveui	devaddr	nwkskey	appskey	appkey
    lwkey = LwKey()
    # print(lwkey.get('8C-F9-57-20-00-03-6E-EF', '526973696E6748468', 0))
    print(lwkey.generate('8cf9572000036eef'))
    # lwsign = LwSign()
    # print(lwsign.get('8CF957200001057B', '8CF9572000000000'))
