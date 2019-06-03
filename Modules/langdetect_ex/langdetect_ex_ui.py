# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'langdetect_ex_ui.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(285, 107)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(35, 30, 54, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(35, 55, 54, 20))
        self.label_2.setObjectName("label_2")
        self.lineEditInput = QtWidgets.QLineEdit(Form)
        self.lineEditInput.setGeometry(QtCore.QRect(90, 30, 151, 20))
        self.lineEditInput.setObjectName("lineEditInput")
        self.lineEditResult = QtWidgets.QLineEdit(Form)
        self.lineEditResult.setGeometry(QtCore.QRect(90, 55, 151, 20))
        self.lineEditResult.setObjectName("lineEditResult")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "检测内容："))
        self.label_2.setText(_translate("Form", "检测结果："))


