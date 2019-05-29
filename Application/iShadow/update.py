#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
from subprocess import Popen
import win32gui
import win32api
import win32con


def set_server(addr, port, pwd):
    try:
        name = 'Shadowsocks.exe'
        path = r'E:\Program Files\ss-v4.0.6\Shadowsocks.exe'
        cfg = r'E:\Program Files\ss-v4.0.6\gui-config.json'

        # 1.close 2.setting 3.open
        print('addr:{} port:{} pwd:{}'.format(addr, port, pwd))
        # kill app
        os.system('taskkill /f /im "{}"'.format(name))

        # change setting
        with open(cfg, 'r') as f:
            js = json.loads(f.read())
        js['configs'][0]['server'] = str(addr).strip()
        js['configs'][0]['server_port'] = str(port).strip()
        js['configs'][0]['password'] = str(pwd).strip()
        js['configs'][0]['method'] = 'aes-256-cfb'
        js['configs'][0]['plugin'] = ''
        js['configs'][0]['plugin_opts'] = ''
        js['configs'][0]['remarks'] = ''
        js['configs'][0]['timeout'] = 5
        with open(cfg, 'w') as f:
            f.write(json.dumps(js))

        # run app
        Popen(path)
        return True
    except:
        pass
    return False


def get_server():
    try:
        cfg = r'E:\Program Files\ss-v4.0.6\gui-config.json'
        with open(cfg, 'r') as f:
            js = json.loads(f.read())
        addr = js['configs'][0]['server']
        port = js['configs'][0]['server_port']
        pwd = js['configs'][0]['password']
        return addr, port, pwd
    except:
        pass
    return False


def cls_tray():
    # print(hex(toolbar)[2:].upper())
    tray = win32gui.FindWindowEx(0, None, 'Shell_TrayWnd', None)
    notify = win32gui.FindWindowEx(tray, None, 'TrayNotifyWnd', None)
    button = win32gui.FindWindowEx(notify, None, 'Button', None)
    if button:
        shape = win32gui.GetWindowRect(button)
        print(shape)
        x = int((shape[2] - shape[0]) / 2)
        y = int((shape[3] - shape[1]) / 2)
        _list = []
        win32gui.EnumChildWindows(0, lambda i, param: param.append(i), _list)
        print([hex(x)[2:].upper() for x in _list])
        win32api.SendMessage(button, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, win32api.MAKELONG(x, y))
        win32api.SendMessage(button, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, win32api.MAKELONG(x, y))
        _list = []
        win32gui.EnumChildWindows(0, lambda i, param: param.append(i), _list)
        print([hex(x)[2:].upper() for x in _list])
    else:
        pager = win32gui.FindWindowEx(notify, None, 'SysPager', None)
        if pager:
            toolbar = win32gui.FindWindowEx(pager, None, 'ToolbarWindow32', None)
        else:
            toolbar = win32gui.FindWindowEx(notify, None, 'ToolbarWindow32', None)
        if toolbar:
            shape = win32gui.GetWindowRect(toolbar)
            for x in range(shape[0], shape[2]):
                y = int((shape[3] + shape[1]) / 2)
                win32api.SendMessage(toolbar, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x, y))


if __name__ == '__main__':
    # set_server(1, 2, 3)
    cls_tray()
