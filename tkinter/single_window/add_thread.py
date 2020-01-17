#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Thread
from tkinter import *
from tkinter import ttk


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

        self.entry_thread1_text = StringVar()
        self.entry_thread2_text = StringVar()

        # self.init_tk_ui()
        self.init_ttk_ui()

    def init_tk_ui(self):
        frame_left = Frame(self)
        frame_right = Frame(self)
        frame_left.grid(row=0, column=1)
        frame_right.grid(row=0, column=2)

        frame_left_line1 = Frame(frame_left)
        frame_left_line1.pack(side=TOP)
        frame_left_line2 = Frame(frame_left)
        frame_left_line2.pack(side=TOP)

        button_dec1 = Button(
            frame_left_line1, text='-', width=2, height=1,
            command=lambda x=('-', 1): self.change_thread(x)
        )
        entry_thread1 = Entry(
            frame_left_line1, textvariable=self.entry_thread1_text
        )

        button_dec1.pack(side=LEFT)
        entry_thread1.pack(side=RIGHT)

        button_dec2 = Button(
            frame_left_line2, text='-', width=2, height=1,
            command=lambda x=('-', 2): self.change_thread(x)
        )
        entry_thread2 = Entry(
            frame_left_line2, textvariable=self.entry_thread2_text
        )

        button_dec2.pack(side=LEFT)
        entry_thread2.pack(side=RIGHT)

        button_add = Button(
            frame_right, text='增加',
            command=lambda x=('+', 1): self.change_thread(x)
        )
        button_add.pack()

    def init_ttk_ui(self):
        frame_left = Frame(self)
        frame_right = Frame(self)
        frame_left.grid(row=0, column=1)
        frame_right.grid(row=0, column=2)
        frame_left_line1 = Frame(frame_left)
        frame_left_line1.pack(side=TOP)
        frame_left_line2 = Frame(frame_left)
        frame_left_line2.pack(side=TOP)

        button_dec1 = ttk.Button(
            frame_left_line1, text='-', width=2,
            command=lambda x=('-', 1): self.change_thread(x)
        )
        entry_thread1 = ttk.Entry(
            frame_left_line1, textvariable=self.entry_thread1_text
        )

        button_dec1.pack(side=LEFT)
        entry_thread1.pack(side=RIGHT)

        button_dec2 = ttk.Button(
            frame_left_line2, text='-', width=2,
            command=lambda x=('-', 2): self.change_thread(x)
        )
        entry_thread2 = ttk.Entry(
            frame_left_line2, textvariable=self.entry_thread2_text
        )

        button_dec2.pack(side=LEFT)
        entry_thread2.pack(side=RIGHT)

        button_add = ttk.Button(
            frame_right, text='增加',
            command=lambda x=('+', 1): self.change_thread(x)
        )
        button_add.pack()

    def change_thread(self, args):
        print(args)


if __name__ == '__main__':
    tt = TestThread()
    tt.mainloop()
