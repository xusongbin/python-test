#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from threading import Thread
from tkinter import *
from time import sleep


class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title('test window')
        self.geometry('400x300')
        self.resizable(0, 0)
        self.thread_run = True

        self.task_list = []
        self.taks_idx = 0

        self.label_usr = Label(self, text='1', width=10)
        self.label_usr.grid(row=1, column=1)

        self.entry_usr_ver = StringVar()
        self.entry_usr = Entry(self, textvariable=self.entry_usr_ver, width=20)
        self.entry_usr.grid(row=1, column=2)
        self.entry_usr.focus()

        self.button_usr = Button(self, text='确认', width=6, height=1, command=self.on_btn_usr_clicked)
        self.button_usr.grid(row=1, column=3)

    def on_btn_usr_clicked(self):
        print('button clicked')
        self.entry_usr_ver.set('{}'.format(int(random.random()*100)))
        self.task_list.append(Thread(target=self.on_thread_test, args=(self.taks_idx, )))
        self.task_list[self.taks_idx].start()
        # self.task_list[self.taks_idx].join()
        self.taks_idx += 1

    def on_thread_test(self, task):
        tick = 0
        while self.thread_run:
            print('Thread {} tick:{}'.format(task, tick))
            sleep(1)
            tick += 1

    def run(self):
        self.mainloop()

    def exit(self):
        self.thread_run = False


if __name__ == '__main__':
    window = MainWindow()
    window.run()
    window.exit()
