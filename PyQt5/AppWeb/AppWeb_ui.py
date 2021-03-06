# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AppWeb_ui.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButtonHome = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonHome.setMinimumSize(QtCore.QSize(0, 24))
        self.pushButtonHome.setMaximumSize(QtCore.QSize(16777215, 24))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/res/res/home.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonHome.setIcon(icon)
        self.pushButtonHome.setObjectName("pushButtonHome")
        self.horizontalLayout.addWidget(self.pushButtonHome)
        self.pushButtonNew = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonNew.setMinimumSize(QtCore.QSize(0, 24))
        self.pushButtonNew.setMaximumSize(QtCore.QSize(16777215, 24))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/res/res/new.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonNew.setIcon(icon1)
        self.pushButtonNew.setObjectName("pushButtonNew")
        self.horizontalLayout.addWidget(self.pushButtonNew)
        self.pushButtonFresh = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonFresh.setMinimumSize(QtCore.QSize(0, 24))
        self.pushButtonFresh.setMaximumSize(QtCore.QSize(16777215, 24))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/res/res/reload.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonFresh.setIcon(icon2)
        self.pushButtonFresh.setObjectName("pushButtonFresh")
        self.horizontalLayout.addWidget(self.pushButtonFresh)
        self.pushButtonForward = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonForward.setMinimumSize(QtCore.QSize(0, 24))
        self.pushButtonForward.setMaximumSize(QtCore.QSize(16777215, 24))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/res/res/forward.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonForward.setIcon(icon3)
        self.pushButtonForward.setObjectName("pushButtonForward")
        self.horizontalLayout.addWidget(self.pushButtonForward)
        self.pushButtonBack = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonBack.setMinimumSize(QtCore.QSize(0, 24))
        self.pushButtonBack.setMaximumSize(QtCore.QSize(16777215, 24))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/res/res/back.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonBack.setIcon(icon4)
        self.pushButtonBack.setObjectName("pushButtonBack")
        self.horizontalLayout.addWidget(self.pushButtonBack)
        self.pushButtonStop = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonStop.setMinimumSize(QtCore.QSize(0, 24))
        self.pushButtonStop.setMaximumSize(QtCore.QSize(16777215, 24))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/res/res/stop.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonStop.setIcon(icon5)
        self.pushButtonStop.setObjectName("pushButtonStop")
        self.horizontalLayout.addWidget(self.pushButtonStop)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 20))
        self.lineEdit.setMaximumSize(QtCore.QSize(16777215, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setMinimumSize(QtCore.QSize(87, 20))
        self.progressBar.setMaximumSize(QtCore.QSize(87, 20))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout.addWidget(self.progressBar)
        self.pushButtonGo = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonGo.setMinimumSize(QtCore.QSize(0, 24))
        self.pushButtonGo.setMaximumSize(QtCore.QSize(16777215, 24))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/res/res/go.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonGo.setIcon(icon6)
        self.pushButtonGo.setObjectName("pushButtonGo")
        self.horizontalLayout.addWidget(self.pushButtonGo)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButtonHome.setText(_translate("MainWindow", "主页"))
        self.pushButtonNew.setText(_translate("MainWindow", "新页面"))
        self.pushButtonFresh.setText(_translate("MainWindow", "刷新"))
        self.pushButtonForward.setText(_translate("MainWindow", "前进"))
        self.pushButtonBack.setText(_translate("MainWindow", "后退"))
        self.pushButtonStop.setText(_translate("MainWindow", "停止"))
        self.pushButtonGo.setText(_translate("MainWindow", "GO"))


import AppWeb_qrc_rc
