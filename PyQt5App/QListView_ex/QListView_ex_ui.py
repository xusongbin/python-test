# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QListView_ex_ui.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 304)
        self.listView = QtWidgets.QListView(Form)
        self.listView.setGeometry(QtCore.QRect(55, 45, 256, 192))
        self.listView.setAcceptDrops(False)
        self.listView.setModelColumn(0)
        self.listView.setObjectName("listView")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))


