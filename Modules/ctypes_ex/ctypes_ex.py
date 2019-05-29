# -*- coding: utf-8 -*-

# 调用dll库功能函数

from ctypes import WinDLL

dll = WinDLL('ctypes_ex.dll')
k = dll.myadd(11, 57)
print(k)
