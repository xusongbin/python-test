#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time
from urllib import request, parse
from contextlib import closing


def do_get_page(open_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)'}
    t = int(time())
    try:
        req = request.Request(url=open_url, headers=headers)
        respond = request.urlopen(req, timeout=3)
        source = respond.read().decode('utf-8', 'ignore')
        print('{}:{}'.format(t, len(source)))
    except Exception as e:
        print('{}:{}'.format(t, 'error'))


def do_get_page_close(open_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)'}
    t = int(time())
    try:
        req = request.Request(url=open_url, headers=headers)
        with closing(request.urlopen(req, timeout=5)) as respond:
            source = respond.read().decode('utf-8')
            print('{}:{}'.format(t, len(source)))
    except:
        print('{}:{}'.format(t, 'error'))


def do_post_page(open_url):
    headers = {
        'Accept': 'text/html',
        'Host': 'tool.chinaz.com',
        'Referer': 'http://tool.chinaz.com/Tools/httptest.aspx',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)'
    }
    url = 'http://tool.chinaz.com/Tools/httptest.aspx'
    data = {
        'method': 0,
        'host': parse.urlparse(open_url).netloc,
        'hideRAW': ''
    }
    t = int(time())
    try:
        data = parse.urlencode(data).encode('utf-8')
        req = request.Request(url, data=data, headers=headers)
        respond = request.urlopen(req, timeout=3)
        source = respond.read().decode('utf-8')
        print('{}:{}'.format(t, len(source)))
    except Exception as e:
        print('{}:{}'.format(t, 'error'))


def do_post_page_close(open_url):
    headers = {
        'Accept': 'text/html',
        'Host': 'tool.chinaz.com',
        'Referer': 'http://tool.chinaz.com/Tools/httptest.aspx',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)'
    }
    url = 'http://tool.chinaz.com/Tools/httptest.aspx'
    data = {
        'method': 0,
        'host': parse.urlparse(open_url).netloc,
        'hideRAW': ''
    }
    t = int(time())
    try:
        data = parse.urlencode(data).encode('utf-8')
        req = request.Request(url, data=data, headers=headers)
        with closing(request.urlopen(req, timeout=5)) as respond:
            source = respond.read().decode('utf-8')
            print('{}:{}'.format(t, len(source)))
    except:
        print('{}:{}'.format(t, 'error'))


if __name__ == '__main__':
    do_get_page('http://www.baidu.com')
    do_get_page_close('http://www.baidu.com')
    do_post_page('http://www.baidu.com')
    do_post_page_close('http://www.baidu.com')

