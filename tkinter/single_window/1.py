#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
import random


class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title('test window')
        self.geometry('400x300')
        self.resizable(0, 0)

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
        msg = str(random.random()*10000)
        print(msg)
        self.entry_usr_ver.set(msg)
        # self.entry_usr.set(msg)

    def run(self):
        self.mainloop()


if __name__ == '__main__':
    window = MainWindow()
    window.run()
