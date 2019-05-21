# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyQToolBox_ui.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(349, 319)
        self.toolBox = QtWidgets.QToolBox(Form)
        self.toolBox.setGeometry(QtCore.QRect(120, 55, 69, 231))
        self.toolBox.setObjectName("toolBox")
        self.page = QtWidgets.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 83, 100))
        self.page.setObjectName("page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.page)
        self.verticalLayout.setObjectName("verticalLayout")
        self.toolButtonBaidu = QtWidgets.QToolButton(self.page)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/se/pyQToolBox/baidu.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButtonBaidu.setIcon(icon)
        self.toolButtonBaidu.setIconSize(QtCore.QSize(32, 32))
        self.toolButtonBaidu.setAutoRaise(True)
        self.toolButtonBaidu.setObjectName("toolButtonBaidu")
        self.verticalLayout.addWidget(self.toolButtonBaidu)
        self.toolButtonSougo = QtWidgets.QToolButton(self.page)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/se/pyQToolBox/sougo.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButtonSougo.setIcon(icon1)
        self.toolButtonSougo.setIconSize(QtCore.QSize(32, 32))
        self.toolButtonSougo.setAutoRaise(True)
        self.toolButtonSougo.setObjectName("toolButtonSougo")
        self.verticalLayout.addWidget(self.toolButtonSougo)
        self.toolBox.addItem(self.page, "")
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 69, 179))
        self.page_2.setObjectName("page_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.page_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.toolButtonTengxun = QtWidgets.QToolButton(self.page_2)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/v/pyQToolBox/tengxun.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButtonTengxun.setIcon(icon2)
        self.toolButtonTengxun.setIconSize(QtCore.QSize(32, 32))
        self.toolButtonTengxun.setAutoRaise(True)
        self.toolButtonTengxun.setObjectName("toolButtonTengxun")
        self.verticalLayout_2.addWidget(self.toolButtonTengxun)
        self.toolBox.addItem(self.page_2, "")

        self.retranslateUi(Form)
        self.toolBox.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.toolButtonBaidu.setText(_translate("Form", "..."))
        self.toolButtonSougo.setText(_translate("Form", "..."))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), _translate("Form", "搜索引擎"))
        self.toolButtonTengxun.setText(_translate("Form", "..."))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), _translate("Form", "视频网站"))


import pyQToolBox_qrc_rc
