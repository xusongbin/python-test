# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AppChat_Client_ui.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(536, 208)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(40, 35, 456, 36))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.progressBar = QtWidgets.QProgressBar(Form)
        self.progressBar.setGeometry(QtCore.QRect(90, 100, 366, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.pushButtonCancel = QtWidgets.QPushButton(Form)
        self.pushButtonCancel.setGeometry(QtCore.QRect(155, 155, 75, 23))
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.pushButtonClose = QtWidgets.QPushButton(Form)
        self.pushButtonClose.setGeometry(QtCore.QRect(265, 155, 75, 23))
        self.pushButtonClose.setObjectName("pushButtonClose")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "接收端"))
        self.label.setText(_translate("Form", "等待接收文件......"))
        self.pushButtonCancel.setText(_translate("Form", "取消"))
        self.pushButtonClose.setText(_translate("Form", "关闭"))


