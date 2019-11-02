#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psutil

for d in psutil.process_iter():
    print(d)

p = psutil.Process(13060)
print(p.memory_percent(memtype="rss")/2)

