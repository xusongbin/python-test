#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Thread
from tkinter import *


class ManageThread(object):
    def __init__(self):
        self.__alive = []
        self.__index = 0

    def on_loop_evt(self, args):
        __thread_idx, __args = args
        __function, __args = __args
        __thread_alive = True
        while __thread_alive:
            if not self.__alive[__thread_idx]:
                __thread_alive = False
            __function(__args)

    def create(self, args):
        args = (args, self.__index)
        _t = Thread(target=self.on_loop_evt, args=(args, ))
        _t.start()
        _idx = self.__index
        self.__alive.append(True)
        self.__index += 1
        return _idx

    def delete(self, index):
        self.__alive[index] = False


class TestThread(Tk):
    def __init__(self):
        super().__init__()
        self.title('test window')
        self.geometry('400x300')
        self.resizable(0, 0)

        self.button_add = Button(self, text='增加', width=6, height=1, command=lambda x=('+', 1): self.change_thread(x))
        self.button_add.grid(row=1, column=4)
        self.button_dec1 = Button(self, text='-', width=3, height=1, command=lambda x=('-', 1): self.change_thread(x))
        self.button_dec1.grid(row=1, column=1)
        self.button_dec2 = Button(self, text='-', width=3, height=1, command=lambda x=('-', 2): self.change_thread(x))
        self.button_dec2.grid(row=2, column=1)

    def change_thread(self, args):
        print(args)


if __name__ == '__main__':
    tt = TestThread()
    tt.mainloop()
