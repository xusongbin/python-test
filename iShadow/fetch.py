#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests import get
from lxml import etree

URL = 'https://d.ishadowx.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3676.400 QQBrowser/10.4.3469.400'
}


def get_account():
    resp = get(URL, headers=headers)
    selector = etree.HTML(resp.text)
    addr = selector.xpath('//h4[text()="IP Address:"]/span/text()')
    port = selector.xpath('//h4[text()="Port:"]/span/text()')
    pwd = selector.xpath('//h4[text()="Password:"]/span/text()')
    return addr, port, pwd


if __name__ == '__main__':
    get_account()
