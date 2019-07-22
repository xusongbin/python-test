#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
except:
    pass

print(ip)
