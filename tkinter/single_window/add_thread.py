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

        self.frame_left_fill = Frame(self, width=10)
        self.frame_left_fill.grid(row=0, column=0)
        # self.frame_left_fill_entry = Entry(self.frame_left_fill, width=)
        self.frame_left = Frame(self)
        self.frame_left.grid(row=0, column=1)
        self.frame_left_line1 = Frame(self.frame_left)
        self.frame_left_line1.pack(side=TOP)
        self.frame_left_line2 = Frame(self.frame_left)
        self.frame_left_line2.pack(side=TOP)
        self.frame_right = Frame(self)
        self.frame_right.grid(row=0, column=2)

        self.button_dec1 = Button(
            self.frame_left_line1, text='-', width=2, height=1,
            command=lambda x=('-', 1): self.change_thread(x)
        ).pack(side=LEFT)
        self.entry_thread1_text = StringVar()
        self.entry_thread1 = Entry(
            self.frame_left_line1, textvariable=self.entry_thread1_text
        ).pack(side=RIGHT)

        self.button_dec2 = Button(
            self.frame_left_line2, text='-', width=2, height=1,
            command=lambda x=('-', 2): self.change_thread(x)
        ).pack(side=LEFT)
        self.entry_thread2_text = StringVar()
        self.entry_thread2 = Entry(
            self.frame_left_line2, textvariable=self.entry_thread2_text
        ).pack(side=RIGHT)

        self.button_add = Button(
            self.frame_right, text='增加',
            command=lambda x=('+', 1): self.change_thread(x)
        ).pack()

    def change_thread(self, args):
        print(args)


if __name__ == '__main__':
    tt = TestThread()
    tt.mainloop()
