#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from urllib import request

url = 'https://ss0.bdstatic.com/k4oZeXSm1A5BphGlnYG/newmusic/english.png'

path = os.path.basename(url)
print(os.path.split(url))

# request.urlretrieve(url, path)
