# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Rock-paper-scissors_ui.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(45, 105, 301, 61))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton1 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton1.setObjectName("pushButton1")
        self.horizontalLayout.addWidget(self.pushButton1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton2.setObjectName("pushButton2")
        self.horizontalLayout.addWidget(self.pushButton2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButton3 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton3.setObjectName("pushButton3")
        self.horizontalLayout.addWidget(self.pushButton3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton1.setText(_translate("Form", "石头"))
        self.pushButton2.setText(_translate("Form", "剪刀"))
        self.pushButton3.setText(_translate("Form", "布"))


