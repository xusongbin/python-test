#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from PyQt5.QtCore import *
from PyQt5.QtNetwork import *


def get_user():
    envs = ["USERNAME", "USER", "HOSTNAME", "DOMAINNAME"]
    env = QProcess.systemEnvironment()
    for var in env:
        varlist = var.split('=')
        if varlist[0] in envs:
            return varlist[1]
    return 'unkonwn'


def get_ip():
    addlist = QNetworkInterface.allAddresses()
    for addr in addlist:
        if addr.protocol() != QAbstractSocket.IPv4Protocol:
            continue
        ip = addr.toString()
        ipbuf = [int(x) for x in ip.split('.')]
        if ipbuf[3] == 1 or ipbuf[3] == 255:
            continue
        return ip
    return '0.0.0.0'


def get_mac():
    interface = QNetworkInterface.allInterfaces()
    for i in interface:
        assert isinstance(i, QNetworkInterface)
        print(i.humanReadableName(), ' ', i.hardwareAddress())


if __name__ == '__main__':
    print(get_user())
    print(get_ip())
    print(get_mac())
