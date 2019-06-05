# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AppJigsaw_ui.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(10, 5, 701, 491))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        MainWindow.setMenuBar(self.menubar)
        self.dockWidgetStatus = QtWidgets.QDockWidget(MainWindow)
        self.dockWidgetStatus.setMinimumSize(QtCore.QSize(40, 50))
        self.dockWidgetStatus.setMaximumSize(QtCore.QSize(524287, 50))
        self.dockWidgetStatus.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.dockWidgetStatus.setObjectName("dockWidgetStatus")
        self.dockWidgetContentsStatus = QtWidgets.QWidget()
        self.dockWidgetContentsStatus.setObjectName("dockWidgetContentsStatus")
        self.label = QtWidgets.QLabel(self.dockWidgetContentsStatus)
        self.label.setGeometry(QtCore.QRect(10, 0, 441, 25))
        self.label.setObjectName("label")
        self.dockWidgetStatus.setWidget(self.dockWidgetContentsStatus)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dockWidgetStatus)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidgetPicture = QtWidgets.QDockWidget(MainWindow)
        self.dockWidgetPicture.setObjectName("dockWidgetPicture")
        self.dockWidgetContentsPicture = QtWidgets.QWidget()
        self.dockWidgetContentsPicture.setObjectName("dockWidgetContentsPicture")
        self.dockWidgetPicture.setWidget(self.dockWidgetContentsPicture)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidgetPicture)
        self.actionaction_o = QtWidgets.QAction(MainWindow)
        self.actionaction_o.setObjectName("actionaction_o")
        self.actionaction_e = QtWidgets.QAction(MainWindow)
        self.actionaction_e.setObjectName("actionaction_e")
        self.actionaction_j = QtWidgets.QAction(MainWindow)
        self.actionaction_j.setObjectName("actionaction_j")
        self.actionaction_r = QtWidgets.QAction(MainWindow)
        self.actionaction_r.setObjectName("actionaction_r")
        self.actionaciotn_s = QtWidgets.QAction(MainWindow)
        self.actionaciotn_s.setObjectName("actionaciotn_s")
        self.menu.addAction(self.actionaction_o)
        self.menu.addAction(self.actionaction_e)
        self.menu_2.addAction(self.actionaction_r)
        self.menu_2.addAction(self.actionaciotn_s)
        self.menu_3.addAction(self.actionaction_j)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menu.setTitle(_translate("MainWindow", "文件(&F)"))
        self.menu_2.setTitle(_translate("MainWindow", "游戏(&G)"))
        self.menu_3.setTitle(_translate("MainWindow", "关于(&A)"))
        self.dockWidgetStatus.setWindowTitle(_translate("MainWindow", "游戏时间"))
        self.label.setText(_translate("MainWindow", "time"))
        self.dockWidgetPicture.setWindowTitle(_translate("MainWindow", "完成的图片"))
        self.actionaction_o.setText(_translate("MainWindow", "打开图片(&O)"))
        self.actionaction_o.setToolTip(_translate("MainWindow", "打开图片"))
        self.actionaction_e.setText(_translate("MainWindow", "退出游戏(&E)"))
        self.actionaction_e.setToolTip(_translate("MainWindow", "退出游戏"))
        self.actionaction_j.setText(_translate("MainWindow", "关于拼图小游戏(J)"))
        self.actionaction_j.setToolTip(_translate("MainWindow", "关于拼图小游戏"))
        self.actionaction_r.setText(_translate("MainWindow", "重新开始(&R)"))
        self.actionaction_r.setToolTip(_translate("MainWindow", "重新开始"))
        self.actionaciotn_s.setText(_translate("MainWindow", "难度选择(&S)"))
        self.actionaciotn_s.setToolTip(_translate("MainWindow", "难度选择"))


