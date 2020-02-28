#!/usr/bin/env python
# -*- coding: utf-8 -*-

import win32api
import win32gui
import win32con
import win32clipboard

from my_driver import *
from vk_code import VK_CODE


class ControlWindows(object):
    __app_text = '同花顺(v8.80.24)'
    __usdcnh_text = '同花顺(v8.80.24)'     # '同花顺(v8.80.24) - 外汇技术分析'
    __1A0001_text = '同花顺(v8.80.24)'     # '同花顺(v8.80.24) - 指数技术分析'
    __881155_text = '同花顺(v8.80.24)'     # '同花顺(v8.80.24) - 综合指数技术分析'

    def __init__(self):
        _handle = self.get()
        write_log('Window get handle {}'.format(_handle))

    def get(self):
        _handle = None
        _app = self.find_window(self.__app_text)
        try:
            _handle = _app['handle']
        except Exception as e:
            write_log('{}\n{}'.format(e, format_exc()))
        return _handle

    def switch_usdcnh(self):
        _start = time()
        while (time() - _start) < 5:
            self.set_force_window()
            sleep(0.5)
            self.push_message('usdcnh')
            if self.find_window(self.__usdcnh_text):
                self.push_message('32')
                return True
        return False

    def switch_1A0001(self):
        _start = time()
        while (time() - _start) < 5:
            self.set_force_window()
            sleep(0.5)
            self.push_message('1a0001')
            if self.find_window(self.__1A0001_text):
                self.push_message('32')
                return True
        return False

    def switch_881155(self):
        _start = time()
        while (time() - _start) < 5:
            self.set_force_window()
            sleep(0.5)
            self.push_message('881155')
            if self.find_window(self.__881155_text):
                self.push_message('32')
                return True
        return False

    def find_window(self, info, key='Text'):
        _windows = self.enum_windows()
        if len(_windows) > 0 and key in _windows[0].keys():
            for win in _windows:
                if info in win[key]:
                    return win
        return None

    def set_force_window(self):
        _handle = self.get()
        if _handle:
            # win32gui.SendMessage(_handle, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
            win32gui.SetForegroundWindow(_handle)
            return True
        return False

    @staticmethod
    def push_message(code):
        for c in code:
            win32api.keybd_event(VK_CODE[c], 0, 0, 0)
            win32api.keybd_event(VK_CODE[c], 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(VK_CODE['enter'], 0, 0, 0)
        win32api.keybd_event(VK_CODE['enter'], 0, win32con.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def copy_to_clipboard(data):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, data)
        win32clipboard.CloseClipboard()

    @staticmethod
    def mouse_click(x, y, delay=0.2):
        _pos = win32api.GetCursorPos()
        win32api.SetCursorPos([x, y])
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        sleep(delay)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        sleep(delay)
        win32api.SetCursorPos([_pos[0], _pos[1]])

    @staticmethod
    def enum_child_windows(hd,  text=None, cname=None, num=0):
        _list = []
        win32gui.EnumChildWindows(hd, lambda i, param: param.append(i), _list)
        for idx, handle in enumerate(_list):
            if not handle:
                continue
            if not text and not cname:
                if idx == num:
                    return handle
            if text == win32gui.GetWindowText(handle):
                return handle
            if cname == win32gui.GetClassName(handle):
                return handle
        return 0

    def enum_windows(self):
        _list = []
        _result = []
        win32gui.EnumWindows(lambda i, param: param.append(i), _list)
        for handle in _list:
            if not handle:
                continue
            _dict = {
                'handle': handle,
                'Handle': self.handle_to_hex(handle),
                'Text': win32gui.GetWindowText(handle),
                'ClassName': win32gui.GetClassName(handle)
            }
            _result.append(_dict)
            # print('窗口句柄：{}'.format(_dict['Handle']))
            # print('窗口标题：{}'.format(_dict['Text']))
            # print('窗口类名：{}'.format(_dict['ClassName']))
        return _result

    @staticmethod
    def handle_to_hex(handle):
        if handle > 0:
            return hex(handle).split('x')[1].rjust(8, '0').upper()
        return '00000000'


if __name__ == '__main__':
    cw = ControlWindows()
    if cw.get():
        cw.switch_1A0001()
    else:
        print('App not found')
