#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import pandas as pd

pd.set_option('display.width', 1000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


class App(object):
    def __init__(self):
        self.max_deadline = 31536000
        self.limit_deadline = 10000
        self.path_base = 'scavenger/'
        self.path_log = self.path_base + 'scavenger.1.log'
        self.path_xlsx_bhd = self.path_base + 'bhd.xlsx'
        self.path_xlsx_burst = self.path_base + 'burst.xlsx'
        self.path_xlsx_boom = self.path_base + 'boom.xlsx'
        self.data_rule = (
            r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
            r' \[INFO\] deadline accepted: account=\d+'
            r', nonce=\d+'
            r', deadline=\d+'
        )
        self.block_rule = (
            r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
            r' \[INFO\] new block: height=\d+'
            r', scoop=\d+'
        )

        self.log_to_xlsx()
        self.parse_xlsx(self.path_xlsx_bhd)

    def log_to_xlsx(self):
        # parse log file, save to bhd.xlsx boom.xlsx burst.xlsx
        try:
            path_csv_bhd = self.path_base + 'bhd.csv'
            path_csv_burst = self.path_base + 'burst.csv'
            path_csv_boom = self.path_base + 'boom.csv'
            with open(path_csv_bhd, 'w') as cf:
                cf.write('time,account,nonce,deadline,block\n')
            with open(path_csv_boom, 'w') as cf:
                cf.write('time,account,nonce,deadline,block\n')
            with open(path_csv_burst, 'w') as cf:
                cf.write('time,account,nonce,deadline,block\n')
            with open(self.path_log, 'r') as lf:
                block = 0
                while lf.readable():
                    line = lf.readline()
                    if not line:
                        break
                    line = line.strip()
                    if not line:
                        continue
                    line = str(line)
                    if re.match(self.block_rule, line):
                        block = int(line.split('=')[1].split(',')[0])
                    if not re.match(self.data_rule, line):
                        continue
                    split_rule = r',|=|\['
                    line_list = re.split(split_rule, line)
                    line_data = '{},{},{},{},{}\n'.format(line_list[0], line_list[2], line_list[4], line_list[6], block)
                    if 100000 > block:
                        save_path = path_csv_boom
                    elif 600000 < block:
                        save_path = path_csv_burst
                    else:
                        save_path = path_csv_bhd
                    with open(save_path, 'a+') as cf:
                        cf.write(line_data)
            pd.read_csv(path_csv_bhd, dtype=str).to_excel(self.path_xlsx_bhd)
            pd.read_csv(path_csv_boom, dtype=str).to_excel(self.path_xlsx_boom)
            pd.read_csv(path_csv_burst, dtype=str).to_excel(self.path_xlsx_burst)
            os.remove(path_csv_bhd)
            os.remove(path_csv_boom)
            os.remove(path_csv_burst)
        except Exception as e:
            print('conversion_format except:%s' % e)

    def parse_xlsx(self, path_xlsx):
        data_frame = pd.read_excel(path_xlsx)
        nonces = data_frame['nonce']
        deadline = data_frame['deadline']
        dl_dict = {}
        for idx, ns in enumerate(nonces):
            if ns not in dl_dict.keys():
                dl_dict[ns] = 0
            dl = int(deadline[idx])
            if dl > self.limit_deadline:
                continue
            dl_dict[ns] += self.max_deadline - dl
        dl_frame = pd.DataFrame(dl_dict.items(), columns=['nonce', 'deadline'])
        print(dl_frame.sort_values('deadline', ascending=False))


if __name__ == '__main__':
    app = App()
