#!/usr/bin/env python
# -*- coding: utf-8 -*-

import win32api
import win32gui
import win32con
import win32clipboard
from vk_code import VK_CODE
from traceback import format_exc
from time import time, sleep


class ControlWindows(object):
    __app_text = ['同花顺(v8.80.50)']
    __usdcnh_text = ['同花顺(v8.80.50) - 外汇技术分析']
    __1A0001_text = ['同花顺(v8.80.50) - 指数技术分析', '同花顺(v8.80.50) - 上证指数']
    __881155_text = ['同花顺(v8.80.50) - 综合指数技术分析']
    __399001_text = ['同花顺(v8.80.50) - 综合指数技术分析']

    def __init__(self):
        pass

    def test(self):
        self.switch_399001()

    def switch_usdcnh(self):
        _start = time()
        while (time() - _start) < 5:
            _handle = self.__find_handle(self.__app_text)
            if not self.__set_force_window(_handle):
                return False
            sleep(0.5)
            self.__push_message('usdcnh')
            if self.__find_window(self.__usdcnh_text):
                self.__push_message('32')
                return True
        return False

    def switch_1a0001(self):
        _handle = self.__find_handle(self.__app_text)
        if not self.__set_force_window(_handle):
            return False
        sleep(0.5)
        self.__push_message('1a0001')
        self.__push_message('32')
        return True

    def switch_399001(self):
        _handle = self.__find_handle(self.__app_text)
        if not self.__set_force_window(_handle):
            return False
        sleep(0.5)
        self.__push_message('399001')
        self.__push_message('32')
        return True

    def switch_881155(self):
        _handle = self.__find_handle(self.__app_text)
        if not self.__set_force_window(_handle):
            return False
        sleep(0.5)
        self.__push_message('881155')
        self.__push_message('32')
        return True

    def __find_handle(self, text):
        try:
            return self.__find_window(text)['handle']
        except Exception as e:
            print('{}\n{}'.format(e, format_exc()))
        return 0

    def __find_window(self, info, key='Text'):
        _windows = self.__enum_windows()
        if len(_windows) > 0 and key in _windows[0].keys():
            for win in _windows:
                for _x in info:
                    if _x in win[key]:
                        return win
        return None

    @staticmethod
    def __set_force_window(hand):
        try:
            # win32gui.SendMessage(hand, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
            win32gui.SetForegroundWindow(hand)
            return True
        except Exception as e:
            print('{}\n{}'.format(e, format_exc()))
        return False

    @staticmethod
    def __push_message(code):
        for c in code:
            win32api.keybd_event(VK_CODE[c], 0, 0, 0)
            win32api.keybd_event(VK_CODE[c], 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(VK_CODE['enter'], 0, 0, 0)
        win32api.keybd_event(VK_CODE['enter'], 0, win32con.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def __mouse_click(x, y, delay=0.2):
        _pos = win32api.GetCursorPos()
        win32api.SetCursorPos([x, y])
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        sleep(delay)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        sleep(delay)
        win32api.SetCursorPos([_pos[0], _pos[1]])

    @staticmethod
    def __enum_child_windows(hd,  text=None, cname=None, num=0):
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

    def __enum_windows(self):
        _list = []
        _result = []
        win32gui.EnumWindows(lambda i, param: param.append(i), _list)
        for handle in _list:
            if not handle:
                continue
            _dict = {
                'handle': handle,
                'Handle': self.__handle_to_hex(handle),
                'Text': win32gui.GetWindowText(handle),
                'ClassName': win32gui.GetClassName(handle)
            }
            _result.append(_dict)
            # print('窗口句柄：{}'.format(_dict['Handle']))
            # print('窗口标题：{}'.format(_dict['Text']))
            # print('窗口类名：{}'.format(_dict['ClassName']))
        return _result

    @staticmethod
    def __handle_to_hex(handle):
        if handle > 0:
            return hex(handle).split('x')[1].rjust(8, '0').upper()
        return '00000000'


if __name__ == '__main__':
    cw = ControlWindows()
    cw.test()
