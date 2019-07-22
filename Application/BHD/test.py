#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib import request
from urllib.parse import quote
from urllib.request import urlopen
import hashlib

accesskey = 'c4c93b56-7bf1-4b11-8fa4-db6075f096b2'
randstr = '22fe319c-505a-11e9-a16c-f44d30581234'
timestamp = '1561628611'
secretkey = '577d2b39-5c9e-426d-b912-06ce4b5bb18d'

ue = 'accesskey=%s&randstr=%s&timestamp=%s&secretkey=%s' % (accesskey, randstr, timestamp, secretkey)
ue = quote(ue)
ue = ue.lower()
ue = ue.encode()
m = hashlib.md5()
m.update(ue)
str_md5 = m.hexdigest()

print(str_md5)
