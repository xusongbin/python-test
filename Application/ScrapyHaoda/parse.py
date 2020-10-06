#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil


def type_cnt():
    with open('haoda2.csv', 'r') as f:
        data = f.read()
    # print(data)
    _context = {}
    for line in data.split('\n'):
        line = line.strip()
        if not line:
            continue
        _type = line.split(',')[0]
        _url = line.split(',')[1]
        if _type not in _context.keys():
            _context[_type] = []
        _context[_type].append(_url)
    for key in _context.keys():
        print('{}:{}'.format(key, len(_context[key])))


def split_dir():
    with open('haoda2.csv', 'r') as f:
        data = f.read()
    img = os.listdir('img')
    for line in data.split('\n'):
        line = line.strip()
        if not line:
            continue
        _type = line.split(',')[0]
        _url = line.split(',')[1]
        _name = line.split(',')[2]
        _dest_dir = 'img/{}'.format(_type)
        if not os.path.isdir(_dest_dir):
            os.mkdir(_dest_dir)
        if '{}.jpg'.format(_name) in img:
            print(_name)
            try:
                shutil.move('img/{}.jpg'.format(_name), '{}/{}.jpg'.format(_dest_dir, _name))
                with open('{}/list.csv'.format(_dest_dir), 'a+') as f:
                    f.write('{}\n'.format(line))
            except Exception as e:
                _ = e


def restore_img():
    for d in os.listdir('img'):
        if '.jpg' in d:
            continue
        for f in os.listdir(os.path.join('img', d)):
            if '.jpg' not in f:
                continue
            shutil.move('{}/{}/{}'.format('img', d, f), '{}/{}'.format('img', f))


def clean_link():
    dir_list = 'xvcg,dfsa,casd,asda'
    for d in dir_list.split(','):
        with open('{}/{}/list.csv'.format('img', d), 'r') as f:
            data = f.read()
        with open('{}/{}/clean.csv'.format('img', d), 'w') as f:
            for i in data.split('\n'):
                if 'mp4' in i:
                    f.write('{}\n'.format(i.split(',')[1]))


if __name__ == '__main__':
    # type_cnt()
    # split_dir()
    # restore_img()
    clean_link()
