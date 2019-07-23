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
    dump_json_path = 'DiskDump.json'
    dump_xlsx_path = 'DiskDump.xlsx'
    scavenger_all_file = 'scavenger/all.xlsx'
    scavenger_bhd_file = 'scavenger/bhd.xlsx'
    scavenger_boom_file = 'scavenger/boom.xlsx'
    scavenger_burst_file = 'scavenger/burst.xlsx'

    def __init__(self):
        self.file_path = self.get_file_path()
        self.nonce_to_excel()
        self.count_nonce_dl(self.scavenger_bhd_file)

    def get_file_path(self):
        try:
            js = ''
            with open(self.dump_json_path, 'r') as f:
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
            dirs_frame.to_excel(self.dump_xlsx_path)
            write_log('nonce_to_excel done.')
        except Exception as e:
            write_log('nonce_to_excel except: %s' % e)

    def count_nonce_dl(self, path):
        # need run scavenger.py first!
        if not os.path.isfile(path):
            write_log('RERROR: need run scavenger.py first!')
            return False
        write_log('count_nonce_dl:{}'.format(path))
        try:
            disk_info = pd.read_excel(self.dump_xlsx_path)
            disk_info['count'] = [0 for _ in range(disk_info['nonce'].size)]
            disk_info['dl'] = [31536000 for _ in range(disk_info['nonce'].size)]

            data_frame = pd.read_excel(path)
            for data_idx, data_nonce in enumerate(data_frame['nonce']):
                for disk_idx, disk_nonce in enumerate(disk_info['nonce']):
                    if disk_nonce <= data_nonce < (disk_nonce + disk_info.loc[disk_idx, 'size']):
                        disk_info.loc[disk_idx, 'count'] += 1
                        if disk_info.loc[disk_idx, 'dl'] > data_frame.loc[data_idx, 'deadline']:
                            disk_info.loc[disk_idx, 'dl'] = data_frame.loc[data_idx, 'deadline']
            disk_info.to_excel('result_' + path)
        except Exception as e:
            write_log('count_nonce_dl except: %s' % e)


if __name__ == '__main__':
    dd = DiskDump()
