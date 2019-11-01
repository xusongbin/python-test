#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('test window')
        self.geometry('400x300')
        self.resizable(0, 0)

        self.label_usr = tk.Label(self, text='用户名：', width=6)
        self.label_usr.place(x=10, y=10)

        self.entry_usr = tk.Entry(self, text='', width=18)
        self.entry_usr.place(x=60, y=10)

        self.button_usr = tk.Button(self, text='确认', width=6, height=1, command=self.on_btn_usr_clicked)
        self.button_usr.place(x=200, y=6)

    def on_btn_usr_clicked(self):
        print('button clicked')

    def run(self):
        self.mainloop()


if __name__ == '__main__':
    window = MainWindow()
    window.run()
