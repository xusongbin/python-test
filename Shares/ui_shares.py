# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_shares.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(520, 350)
        Form.setMinimumSize(QtCore.QSize(520, 350))
        Form.setMaximumSize(QtCore.QSize(520, 350))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Stocks.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Form)
        self.plainTextEdit.setGeometry(QtCore.QRect(5, 5, 401, 316))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(107, 325, 21, 16))
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(5, 325, 96, 16))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.labelImageName = QtWidgets.QLabel(Form)
        self.labelImageName.setGeometry(QtCore.QRect(0, 355, 236, 16))
        self.labelImageName.setText("")
        self.labelImageName.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelImageName.setObjectName("labelImageName")
        self.labelTime = QtWidgets.QLabel(Form)
        self.labelTime.setGeometry(QtCore.QRect(275, 320, 131, 16))
        self.labelTime.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTime.setObjectName("labelTime")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(425, 110, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.checkBoxUpdate = QtWidgets.QCheckBox(Form)
        self.checkBoxUpdate.setGeometry(QtCore.QRect(430, 20, 71, 16))
        self.checkBoxUpdate.setObjectName("checkBoxUpdate")
        self.checkBoxSend = QtWidgets.QCheckBox(Form)
        self.checkBoxSend.setGeometry(QtCore.QRect(430, 55, 71, 16))
        self.checkBoxSend.setObjectName("checkBoxSend")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "0"))
        self.label_2.setText(_translate("Form", "获取数据倒计时："))
        self.labelTime.setText(_translate("Form", "2019-3-22 21:16:48"))
        self.pushButton.setText(_translate("Form", "启动"))
        self.checkBoxUpdate.setText(_translate("Form", "更新表格"))
        self.checkBoxSend.setText(_translate("Form", "发到微信"))


