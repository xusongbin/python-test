#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def handle_name(name):
    try:
        name = name.strip()
        name = re.sub(r'[？\\*|“<>:/]', '', name)
        name = name.replace('标题：', '')
        if re.match(r'.*\((\d+|图\d+)\)', name):
            name = name[:name.find('(')]
        if re.match(r'【.*】.*', name):
            name = name[name.rfind('】') + 1:]
        if re.match(r'\[.*\].*', name):
            name = name[name.rfind(']') + 1:]
        if re.match(r'.* \d+', name):
            name = name[: name.rfind(' ')]
        return name.strip()
    except Exception as e:
        pass
    return ''
