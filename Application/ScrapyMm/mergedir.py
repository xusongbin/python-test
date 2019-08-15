#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import shutil

base_path = 'D:/Program Files/Picture/'
keyword = [
]


def move_to_dest(src_dir, dest_dir):
    if not os.path.isdir(dest_dir):
        os.mkdir(dest_dir)
    for this_file in os.listdir(src_dir):
        this_file_path = os.path.join(src_dir, this_file)
        dest_file_path = os.path.join(dest_dir, this_file)
        shutil.move(this_file_path, dest_file_path)
        print('MOVE {} TO {}'.format(this_file_path, dest_file_path))
    os.rmdir(src_dir)


def handle_name(src_name):
    dst_name = src_name.strip()
    for kw in keyword:
        if kw in dst_name:
            return kw
    if re.match(r'.*\((\d+|图\d+)\)$', dst_name):
        dst_name = dst_name[:dst_name.rfind('(')]
    if re.match(r'^【.*】.*', dst_name):
        dst_name = dst_name[dst_name.rfind('】')+1:]
    if re.match(r'^\[.*\].*', dst_name):
        dst_name = dst_name[dst_name.rfind(']')+1:]
    if re.match(r'.* \d+$', dst_name):
        dst_name = dst_name[:dst_name.rfind(' ')]
    if re.match(r'.*图片$', dst_name):
        dst_name = dst_name[:dst_name.rfind('图')]
    if re.match(r'.*图片\d+$', dst_name):
        dst_name = dst_name[:dst_name.rfind('图')]
    if re.match(r'.*写真\d+$', dst_name):
        dst_name = dst_name[:dst_name.rfind('写')]
    if re.match(r'.*第\d+张$', dst_name):
        dst_name = dst_name[:dst_name.rfind('第')]
    return dst_name


def check_directory():
    for this_name in os.listdir(base_path):
        next_name = handle_name(this_name)
        this_path = base_path + this_name
        next_path = base_path + next_name
        if next_name != '' and this_path != next_path:
            move_to_dest(this_path, next_path)


def read_directory():
    with open('dir.csv', 'w', encoding='UTF-8') as f:
        for this_name in os.listdir(base_path):
            f.write(this_name + '\n')


if __name__ == '__main__':
    check_directory()
    # read_directory()
