
import re
from tkinter import *


class MyWidget(object):
    def __init__(self):
        self.root = Tk()
        self.fun_root_init()

        self.root.after(30, self.timer_ui_event)

        self.rt_set = Toplevel(self.root)
        self.fun_rt_set_init()
        self.rt_set_flag = True
        self.fun_rt_btn_commit()

        self.root_btn_commit = Button(self.root, text="点我", width=5, height=1, command=self.fun_rt_btn_commit)
        self.root_btn_commit.place(x=10, y=10)

        # bmpng = PhotoImage(file='28429.png')
        # self.root_lb_png = Label(self.root, image=bmpng, width=128, height=128)
        # self.root_lb_png.bm = bmpng
        # self.root_lb_png.place(x=10, y=50)

        self.root_lb_gif = Label(self.root)
        self.root_lb_gif.place(x=10, y=50)
        self.root_lb_gif_idx = 0
        self.root_lb_gif_frames = [PhotoImage(file='timg.gif', format='gif -index %i' % i) for i in range(48)]

    def fun_root_init(self):
        self.root.title('Tkinter study!')
        _width = 600
        _height = 600
        _left = int(self.root.winfo_screenwidth() - _width) / 2
        _top = int(self.root.winfo_screenheight() - _height) / 2
        self.root.geometry('%dx%d+%d+%d' % (_width, _height, _left, _top))
        self.root.resizable(False, False)

    def fun_rt_set_init(self):
        _root_size = [int(x) for x in re.findall(r'(\d+)', self.root.geometry())]
        _width = 100
        _height = 100
        _left = int(_root_size[0] / 2) + _root_size[2] - int(_width / 2)
        _top = int(_root_size[1] / 2) + _root_size[3] - int(_height / 2)
        self.rt_set.geometry('%dx%d+%d+%d' % (_width, _height, _left, _top))
        self.rt_set.resizable(False, False)
        self.rt_set.protocol("WM_DELETE_WINDOW", self.fun_rt_btn_commit)
        self.rt_set.withdraw()

    def timer_ui_event(self):
        self.root_lb_gif.configure(image=self.root_lb_gif_frames[self.root_lb_gif_idx])
        self.root_lb_gif_idx += 1
        if self.root_lb_gif_idx >= 48:
            self.root_lb_gif_idx = 0
        self.root.after(30, self.timer_ui_event)

    def fun_rt_btn_commit(self):
        if self.rt_set_flag:
            self.rt_set.withdraw()
            self.rt_set_flag = False
        else:
            _root_size = [int(x) for x in re.findall(r'(\d+)', self.root.geometry())]
            _width = 100
            _height = 100
            _left = int(_root_size[0] / 2) + _root_size[2] - int(_width / 2)
            _top = int(_root_size[1] / 2) + _root_size[3] - int(_height / 2)
            self.rt_set.geometry('%dx%d+%d+%d' % (_width, _height, _left, _top))
            self.rt_set.update()
            self.rt_set.deiconify()
            self.rt_set_flag = True

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = MyWidget()
    app.run()
