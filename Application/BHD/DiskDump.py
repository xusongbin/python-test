#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import json
import pandas as pd
from time import time, strftime, localtime


def write_log(_str):
    _data = strftime("%Y-%m-%d %H:%M:%S", localtime())
    _data += '.%03d ' % (int(time() * 1000) % 1000)
    _data += _str
    try:
        print(_data)
        with open('out.log', 'a+') as f:
            f.write(_data + '\n')
            f.flush()
    except Exception as e:
        print('write log exception %s' % e)


class DiskDump(object):
    json_file = 'DiskDump.json'

    def __init__(self):
        self.file_path = self.get_file_path()
        self.nonce_to_excel()

    def get_file_path(self):
        try:
            js = ''
            with open(self.json_file, 'r') as f:
                while f.readable():
                    line = f.readline()
                    if not line:
                        break
                    line = line.strip()
                    if not line:
                        continue
                    if line[0] == '#':
                        continue
                    js += line
            jd = json.loads(js)
            return jd['disk_path']
        except Exception as e:
            write_log('get_file_path except: %s' % e)
        return []

    def nonce_to_excel(self):
        if not self.file_path:
            write_log('nonce_to_excel file path not exist!')
        # load file to dict, keys is the file path
        dirs_dict = {}
        for path in self.file_path:
            try:
                if path not in dirs_dict.keys():
                    dirs_dict[path] = []
                for d in os.listdir(path):
                    if re.match(r'\d+_\d+_\d+', d):
                        dirs_dict[path].append(path)
                        dirs_dict[path].append(d.split('_'))
            except:
                pass
        try:
            dirs_frame = pd.DataFrame(dirs_dict, columns=['path', 'id', 'nonce', 'size'], dtype=str)
            dirs_frame.to_excel('DiskDump.xlsx')
            write_log('nonce_to_excel done.')
        except Exception as e:
            write_log('nonce_to_excel except: %s' % e)


if __name__ == '__main__':
    dd = DiskDump()
