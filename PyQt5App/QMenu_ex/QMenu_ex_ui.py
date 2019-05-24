# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyContextMenu_ui.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(169, 415)
        self.toolBox = QtWidgets.QToolBox(Form)
        self.toolBox.setGeometry(QtCore.QRect(35, 30, 91, 346))
        self.toolBox.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.toolBox.setObjectName("toolBox")
        self.page = QtWidgets.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 91, 320))
        self.page.setObjectName("page")
        self.toolBox.addItem(self.page, "")

        self.retranslateUi(Form)
        self.toolBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), _translate("Form", "我的好友"))


