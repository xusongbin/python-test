# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QTreeWidget_ex_ui.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 304)
        self.treeWidget = QtWidgets.QTreeWidget(Form)
        self.treeWidget.setGeometry(QtCore.QRect(65, 70, 256, 192))
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.pushButtonAdd = QtWidgets.QPushButton(Form)
        self.pushButtonAdd.setGeometry(QtCore.QRect(65, 35, 75, 23))
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.pushButtonUpd = QtWidgets.QPushButton(Form)
        self.pushButtonUpd.setGeometry(QtCore.QRect(155, 35, 75, 23))
        self.pushButtonUpd.setObjectName("pushButtonUpd")
        self.pushButtonDel = QtWidgets.QPushButton(Form)
        self.pushButtonDel.setGeometry(QtCore.QRect(245, 35, 75, 23))
        self.pushButtonDel.setObjectName("pushButtonDel")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButtonAdd.setText(_translate("Form", "添加"))
        self.pushButtonUpd.setText(_translate("Form", "修改"))
        self.pushButtonDel.setText(_translate("Form", "删除"))


