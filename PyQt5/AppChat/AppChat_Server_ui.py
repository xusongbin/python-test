# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AppChat_Server_ui.ui'
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
        self.pushButtonSend = QtWidgets.QPushButton(Form)
        self.pushButtonSend.setGeometry(QtCore.QRect(215, 150, 75, 23))
        self.pushButtonSend.setObjectName("pushButtonSend")
        self.pushButtonClose = QtWidgets.QPushButton(Form)
        self.pushButtonClose.setGeometry(QtCore.QRect(300, 150, 75, 23))
        self.pushButtonClose.setObjectName("pushButtonClose")
        self.pushButtonOpen = QtWidgets.QPushButton(Form)
        self.pushButtonOpen.setGeometry(QtCore.QRect(130, 150, 75, 23))
        self.pushButtonOpen.setObjectName("pushButtonOpen")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "发送端"))
        self.label.setText(_translate("Form", "请选择要发送的文件......"))
        self.pushButtonSend.setText(_translate("Form", "发送"))
        self.pushButtonClose.setText(_translate("Form", "关闭"))
        self.pushButtonOpen.setText(_translate("Form", "打开"))


