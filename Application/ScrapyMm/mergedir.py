#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import shutil


def move_to_dest(src_dir, dest_dir):
    if not os.path.isdir(dest_dir):
        os.mkdir(dest_dir)
    for this_file in os.listdir(src_dir):
        this_file_path = os.path.join(src_dir, this_file)
        dest_file_path = os.path.join(dest_dir, this_file)
        shutil.move(this_file_path, dest_file_path)
        print('MOVE {} TO {}'.format(this_file_path, dest_file_path))
    os.rmdir(src_dir)


base_path = 'D:/Program Files/Picture/'
for this_name in os.listdir(base_path):
    next_name = this_name
    if re.match(r'.*\((\d+|图\d+)\)', next_name):
        next_name = next_name[:next_name.rfind('(')]
    if re.match(r'【.*】.*', next_name):
        next_name = next_name[next_name.rfind('】')+1:]
    if re.match(r'\[.*\].*', next_name):
        next_name = next_name[next_name.rfind(']')+1:]
    if re.match(r'.* \d+', next_name):
        next_name = next_name[:next_name.rfind(' ')]
    if re.match(r'.*图片', next_name):
        next_name = next_name[:next_name.rfind('图')]
    if re.match(r'.*图片\d+', next_name):
        next_name = next_name[:next_name.rfind('图')]
    if re.match(r'.*第\d+张', next_name):
        next_name = next_name[:next_name.rfind('第')]
    this_path = base_path + this_name
    next_path = base_path + next_name
    if this_path != next_path:
        move_to_dest(this_path, next_path)
