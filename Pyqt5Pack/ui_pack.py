# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_pack.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setEnabled(True)
        Form.resize(400, 300)
        Form.setMinimumSize(QtCore.QSize(400, 300))
        Form.setMaximumSize(QtCore.QSize(400, 300))
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(75, 105, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(75, 80, 113, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(75, 140, 40, 12))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.labelKeyText = QtWidgets.QLabel(Form)
        self.labelKeyText.setGeometry(QtCore.QRect(115, 140, 54, 12))
        self.labelKeyText.setObjectName("labelKeyText")
        self.labelKeyValue = QtWidgets.QLabel(Form)
        self.labelKeyValue.setGeometry(QtCore.QRect(115, 160, 54, 12))
        self.labelKeyValue.setObjectName("labelKeyValue")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(75, 160, 40, 12))
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.labelPosValue = QtWidgets.QLabel(Form)
        self.labelPosValue.setGeometry(QtCore.QRect(10, 10, 54, 12))
        self.labelPosValue.setObjectName("labelPosValue")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "UI测试"))
        self.pushButton.setText(_translate("Form", "PushButton"))
        self.label.setText(_translate("Form", "文本："))
        self.labelKeyText.setText(_translate("Form", "0"))
        self.labelKeyValue.setText(_translate("Form", "0"))
        self.label_4.setText(_translate("Form", "键值："))
        self.labelPosValue.setText(_translate("Form", "0"))


