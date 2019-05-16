import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QMenuBar, QToolBar, QTextEdit, QAction, QApplication, qApp, QMessageBox
from PyQt5.QtCore import Qt

import threading
import time

songs = ['爱情买卖', '朋友', '回家过年', '好日子']
films = ['阿凡达', '猩球崛起']


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(677, 442)
        self.setWindowTitle("我的程序")

        self.createUI()
        self.createAction()
        self.createStatusbar()
        self.createMenu()
        self.createToolbar()

    def createUI(self):
        self.textedit = QTextEdit()
        self.setCentralWidget(self.textedit)

    # 动作
    def createAction(self):
        self.exit_action = QAction(QIcon("ico_new.jpg"), "退出", self, triggered=qApp.quit)
        self.exit_action.setStatusTip("退出程序")
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.triggered.connect(qApp.quit)

    # 状态栏
    def createStatusbar(self):
        self.statusBar()

    # 菜单栏
    def createMenu(self):
        # menubar = QMenuBar(self)
        menubar = self.menuBar()
        menu = menubar.addMenu("文件(F)")
        menu.addAction(QAction(QIcon("ico_new_16_16.jpg"), "新建", self, triggered=qApp.quit))  # 带图标，文字
        menu.addAction(QAction(QIcon("ico_open_16_16.jpg"), "打开", self, triggered=qApp.quit))
        menu.addAction(QAction(QIcon("ico_save_16_16.jpg"), "保存", self, triggered=qApp.quit))
        menu.addSeparator()
        menu.addAction(
            QAction(QIcon("ico_close_16_16.jpg"), "关闭", self, triggered=lambda: QMessageBox.about(self, '关闭', '关闭。。。')))

        menu = menubar.addMenu("编辑(E)")
        menu.addAction(QAction("撤销", self, triggered=qApp.quit))  # 不带图标
        menu.addAction(QAction("剪切", self, triggered=qApp.quit))
        menu.addAction(QAction("复制", self, triggered=qApp.quit))
        menu.addAction(QAction("粘贴", self, triggered=qApp.quit))

        menu = menubar.addMenu("娱乐(S)")
        menu.addAction(QAction("音乐", self, triggered=lambda: self.thread_it(self.music, songs)))  # 线程
        menu.addAction(QAction("电影", self, triggered=lambda: self.thread_it(self.movie, films)))

        menu = menubar.addMenu("帮助(H)")
        menu.addAction('&New', lambda: QMessageBox.about(self, 'New', '新建。。。'), Qt.CTRL + Qt.Key_N)  # 注意快捷键
        menu.addAction('关于', lambda: QMessageBox.about(self, '关于', '关于。。。'), Qt.CTRL + Qt.Key_Q)

    # 工具栏
    def createToolbar(self):
        toolbar = self.addToolBar('文件')
        toolbar.addAction(QAction(QIcon("ico_new_16_16.jpg"), "新建", self, triggered=qApp.quit))  # 带图标，文字
        toolbar.addAction(QAction(QIcon("ico_open_16_16.jpg"), "打开", self, triggered=qApp.quit))
        toolbar.addSeparator()
        toolbar.addAction(QAction(QIcon("ico_save_16_16.jpg"), "打开", self, triggered=qApp.quit))

        toolbar = self.addToolBar("编辑")
        toolbar.addAction(QAction("撤销", self, triggered=qApp.quit))  # 不带图标
        toolbar.addAction(QAction("剪切", self, triggered=qApp.quit))

    # 逻辑：听音乐
    def music(self, songs):
        for x in songs:
            self.textedit.append("听音乐：%s \t-- %s" % (x, time.ctime()))
            time.sleep(3)

    # 逻辑：看电影
    def movie(self, films):
        for x in films:
            self.textedit.append("看电影：%s \t-- %s" % (x, time.ctime()))
            time.sleep(5)

    # 打包进线程（耗时的操作）
    @staticmethod
    def thread_it(func, *args):
        t = threading.Thread(target=func, args=args)
        t.setDaemon(True)  # 守护--就算主界面关闭，线程也会留守后台运行（不对!）
        t.start()  # 启动
        # t.join()          # 阻塞--会卡死界面！


app = QApplication(sys.argv)
win = MyWindow()
win.show()
sys.exit(app.exec_())