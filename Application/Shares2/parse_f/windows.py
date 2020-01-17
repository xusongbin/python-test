#!/usr/bin/env python
# -*- coding: utf-8 -*-

import win32api
import win32gui
import win32con
import win32clipboard
from vk_code import VK_CODE

from time import sleep


class AutoWindow(object):
    def __init__(self):
        self.Text = '同花顺(v8.80.24)'
        self.app_handle = self.find_app()['handle']
        if not self.app_handle:
            return
        # self.switch_1A0001()
        # self.switch_881155()
        # self.switch_usdcnh()

    def switch_usdcnh(self, delay=0.2):
        while True:
            self.set_force_window()
            self.push_message('USDCNH')
            if '外汇技术分析' in self.find_app()['Text']:
                self.push_message('32')
                break
            sleep(delay)

    def switch_1A0001(self, delay=0.2):
        while True:
            self.set_force_window()
            self.push_message('1a0001')
            if '指数技术分析' in self.find_app()['Text']:
                self.push_message('32')
                break
            sleep(delay)

    def switch_881155(self, delay=0.2):
        while True:
            self.set_force_window()
            self.push_message('881155')
            if '综合指数技术分析' in self.find_app()['Text']:
                self.push_message('32')
                break
            sleep(delay)

    def push_message(self, code):
        _edit_bar = self.find_edit_bar()
        _rect = win32gui.GetWindowRect(_edit_bar)
        _x = int((_rect[0] + _rect[2]) / 2)
        _y = int((_rect[1] + _rect[3]) / 2)
        self.mouse_click(_x, _y)
        for c in code:
            win32api.keybd_event(VK_CODE[c], 0, 0, 0)
            win32api.keybd_event(VK_CODE[c], 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(VK_CODE['enter'], 0, 0, 0)
        win32api.keybd_event(VK_CODE['enter'], 0, win32con.KEYEVENTF_KEYUP, 0)

    def swtich_symbol(self, code):
        _edit_bar = self.find_edit_bar()
        self.send_msg(_edit_bar, code)

    def find_edit_bar(self):
        _status_bar = self.enum_child_windows(self.app_handle, cname='msctls_statusbar32')
        _search_bar = self.enum_child_windows(_status_bar)
        _edit_bar = self.enum_child_windows(_search_bar, cname='Edit')
        return _edit_bar

    def find_app(self):
        _windows = self.enum_windows()
        for win in _windows:
            # print(win)
            if self.Text in win['Text']:
                return win
        return 0

    def send_msg(self, hd, data, delay=0.2):
        _rect = win32gui.GetWindowRect(hd)
        _x = int((_rect[0] + _rect[2]) / 2)
        _y = int((_rect[1] + _rect[3]) / 2)
        self.mouse_click(_x, _y)
        self.copy_to_clipboard(data)
        win32api.keybd_event(0x11, 0, 0, 0)
        win32api.keybd_event(0x56, 0, 0, 0)
        sleep(delay)
        win32api.keybd_event(0x56, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(0x11, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(0x0D, 0, 0, 0)

    def set_force_window(self):
        # win32gui.SendMessage(self.app_handle, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
        win32gui.SetForegroundWindow(self.app_handle)

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
    def handle_to_hex(handle):
        if handle > 0:
            return hex(handle).split('x')[1].rjust(8, '0').upper()
        return '00000000'

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

    @staticmethod
    def enum_windows():
        _list = []
        _result = []
        win32gui.EnumWindows(lambda i, param: param.append(i), _list)
        for handle in _list:
            if not handle:
                continue
            _dict = {
                'handle': handle,
                'Handle': hex(handle).split('x')[1].rjust(8, '0').upper(),
                'Text': win32gui.GetWindowText(handle),
                'ClassName': win32gui.GetClassName(handle)
            }
            _result.append(_dict)
            # print('窗口句柄：{}'.format(_dict['Handle']))
            # print('窗口标题：{}'.format(_dict['Text']))
            # print('窗口类名：{}'.format(_dict['ClassName']))
        return _result


if __name__ == '__main__':
    aw = AutoWindow()
