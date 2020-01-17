#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re


def get_process_memoey(name):
    pattern = re.compile(r'([^\s]+)\s+(\d+)\s.*\s([^\s]+\sK)')
    cmd = 'tasklist /fi "imagename eq ' + name + '"' + ' | findstr.exe ' + name
    result = os.popen(cmd).read()
    for line in result.split("\n"):
        line = "".join(line.split('\n'))
        if len(line) == 0:
            break
        m = pattern.search(line)
        if not m:
            continue
        #由于是查看python进程所占内存，因此通过pid将本程序过滤掉
        if str(os.getpid()) == m.group(2):
            continue
        ori_mem = m.group(3).replace(',', '')
        ori_mem = ori_mem.replace(' K', '')
        ori_mem = ori_mem.replace(r'\sK', '')
        mem = int(ori_mem)
        # 'ProcessName:'+ m.group(1) + '\tPID:' + m.group(2) + '\tmemory size:%.2f'% (memEach * 1.0 /1024), 'M'
        print('ProcessName: {}\tPID:{}\tmemory size:{:.2f} k'.format(
            m.group(1),
            m.group(2),
            mem * 1.0
        ))

    # {name:{pid:n, conv:x, idx:m, ram:k}}
    process_dict = {}
    result = os.popen('tasklist').read()
    for line in result.split('\n'):
        line_list = line.split(' ')
        if not re.match(r'.*\.exe', line_list[0]):
            continue
        line_list = [x for x in line_list if x]
        process_dict[line_list[0]] = {
            'PID': line_list[1],
            'CONV': line_list[2],
            'INDEX': line_list[3],
            'RAM': line_list[4]
        }
    # all system process
    # print(process_dict)
    if name in process_dict.keys():
        print('ProcessName: {}\tPID:{}\tmemory size:{} K'.format(
            name,
            process_dict[name]['PID'],
            process_dict[name]['RAM']
        ))


if __name__ == '__main__':
    process = 'python.exe'
    get_process_memoey(process)
