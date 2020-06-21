#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyautogui
import pyperclip


class KeyBoard(object):
    def __init__(self):
        pass

    def key(self, k):
        pyautogui.typewrite(k)


class ClipBoard(object):
    def __init__(self):
        pass

    def copy(self, msg):
        try:
            pyperclip.copy(msg)
            return True
        except Exception as e:
            _ = e
        return False

    def parse(self):
        try:
            return pyperclip.paste()
        except Exception as e:
            _ = e
        return ''


if __name__ == '__main__':
    cb = ClipBoard()
    cb.copy(0x11)
    print(cb.parse())
