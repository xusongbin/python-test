# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QMdiArea_ex_ui.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.mdiArea = QtWidgets.QMdiArea(self.centralwidget)
        self.mdiArea.setGeometry(QtCore.QRect(-1, -1, 501, 466))
        self.mdiArea.setObjectName("mdiArea")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(130, 255, 120, 80))
        self.widget.setObjectName("widget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setMovable(False)
        self.toolBar.setAllowedAreas(QtCore.Qt.TopToolBarArea)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionaction1 = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/image/image/1.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionaction1.setIcon(icon)
        self.actionaction1.setObjectName("actionaction1")
        self.actionaction2 = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/image/image/2.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionaction2.setIcon(icon1)
        self.actionaction2.setObjectName("actionaction2")
        self.actionaction3 = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/image/image/3.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionaction3.setIcon(icon2)
        self.actionaction3.setObjectName("actionaction3")
        self.actionaction4 = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/image/image/4.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionaction4.setIcon(icon3)
        self.actionaction4.setObjectName("actionaction4")
        self.toolBar.addAction(self.actionaction1)
        self.toolBar.addAction(self.actionaction2)
        self.toolBar.addAction(self.actionaction3)
        self.toolBar.addAction(self.actionaction4)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionaction1.setText(_translate("MainWindow", "发一张牌"))
        self.actionaction2.setText(_translate("MainWindow", "随机5张牌"))
        self.actionaction3.setText(_translate("MainWindow", "清除牌"))
        self.actionaction4.setText(_translate("MainWindow", "收牌"))


import QMdiArea_rc_rc
