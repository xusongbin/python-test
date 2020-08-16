#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import base64
from traceback import format_exc

from Crypto.Cipher import AES
from configparser import ConfigParser


class File(object):
    @staticmethod
    def exists(file):
        try:
            return os.path.exists(file)
        except Exception as e:
            _ = e
        return False

    @staticmethod
    def create(file):
        try:
            os.makedirs(os.path.split(file)[0], exist_ok=True)
            f = open(file, 'w')
            f.close()
            return True
        except Exception as e:
            _ = e
        return False

    @staticmethod
    def delete(file):
        try:
            if os.path.exists(file) is True:
                os.remove(file)
            return True
        except Exception as e:
            _ = e
        return False

    @staticmethod
    def size(file):
        return os.path.getsize(file)
    @staticmethod
    def name(file):
        return os.path.basename(file)

    def read(self, file, mode='r'):
        if not self.exists(file):
            return False
        with open(file, mode) as f:
            return f.read()

    def write(self, file, data, mode='w'):
        if not self.create(file):
            return False
        with open(file, mode) as f:
            f.write(data)
        return True

    def copy(self, src, des):
        if not self.exists(src):
            return False
        if not self.create(des):
            return False
        with open(src, 'rb') as fr:
            fw = open(des, 'wb')
            while True:
                data = fr.read(1000)
                if not data:
                    break
                fw.write(data)
            fw.close()

    def move(self, src, des):
        if not self.copy(src, des):
            return False
        return self.delete(src)

    @staticmethod
    def find(src=None, fm=None):
        _files = []
        if not src:
            src = os.getcwd()
        try:
            for s in os.listdir(src):
                if '.' not in s:
                    continue
                _fm = s.split('.')[1]
                if not fm:
                    _files.append(s)
                    continue
                if _fm in fm:
                    _files.append(s)
                    continue
        except Exception as e:
            _ = e
        return _files
    @staticmethod
    def aes_encrypt(bin_data, mode='ECB', key=b'RisingHF20150203', iv=b''):
        if mode.upper() == 'ECB':
            aes = AES.new(key, AES.MODE_ECB)
        elif mode.upper() == 'CBC':
            aes = AES.new(key, AES.MODE_CBC, iv)
        else:
            return None
        try:
            add = len(bin_data) % 16
            if add:
                bin_data += b'\x00' * (16 - add)
            return aes.encrypt(bin_data)
        except Exception as e:
            _ = e
        return None

    @staticmethod
    def aes_decrypt(bin_data, mode='ECB', key=b'RisingHF20150203', iv=b''):
        if mode.upper() == 'ECB':
            aes = AES.new(key, AES.MODE_ECB)
        elif mode.upper() == 'CBC':
            aes = AES.new(key, AES.MODE_CBC, iv)
        else:
            return None
        try:
            return aes.decrypt(bin_data)
        except Exception as e:
            _ = e
        return None

    @staticmethod
    def base64_encode(data, byte=False):
        if type(data) is str:
            data = data.encode()
        out = base64.b64encode(data)
        if not byte:
            out = out.decode()
        return out

    @staticmethod
    def base64_decode(data, byte=False):
        if type(data) is str:
            data = data.encode()
        out = base64.b64decode(data)
        if not byte:
            out = out.decode()
        return out
class Directory(object):
    @staticmethod
    def exist(path):
        if os.path.isdir(path):
            return True
        return False
    @staticmethod
    def create(path):
        if os.path.isdir(path):
            return True
        try:
            os.makedirs(path)
            return True
        except Exception as e:
            _ = e
        return False


class Ini(object):
    def __init__(self, path='config.ini', erase=False):
        self.__file = File()
        self.__path = path
        self.__erase = erase
        self.__config = ConfigParser()
        self.__load()

    def __load(self):
        if not self.__file.exists(self.__path):
            self.__file.create(self.__path)
        self.__config.read(self.__path)

    def write(self, section, name, data):
        if self.__file.exists(self.__path) and self.__erase:
            self.__file.delete(self.__path)
            self.__load()
        if data == self.read(section, name):
            return True
        try:
            self.__config.add_section(section)
        except Exception as e:
            _ = e
        self.__config.set(section, name, data)
        self.__config.write(open(self.__path, 'w'))
        return True

    def read(self, section, name):
        try:
            return self.__config.get(section, name)
        except Exception as e:
            _ = e
        return ''


if __name__ == '__main__':
    ftest = File()
    print(ftest.base64_encode('123', True))
    print(ftest.base64_decode('MTIz'))
    print(ftest.find(fm=['py']))

    fini = Ini()
    fini.write('MODULE', 'name', 'COM12')
    print(fini.read('MODULE', 'PORT'))
