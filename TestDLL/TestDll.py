# -*- coding: utf-8 -*-

from ctypes import WinDLL

dll = WinDLL('DllTest.dll')
k = dll.myadd(11, 57)
print(k)
