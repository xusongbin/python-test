# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyQSlider_ui.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.dial = QtWidgets.QDial(Form)
        self.dial.setGeometry(QtCore.QRect(150, 130, 50, 64))
        self.dial.setObjectName("dial")
        self.horizontalSlider = QtWidgets.QSlider(Form)
        self.horizontalSlider.setGeometry(QtCore.QRect(200, 250, 160, 19))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.verticalSlider = QtWidgets.QSlider(Form)
        self.verticalSlider.setGeometry(QtCore.QRect(90, 80, 19, 160))
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName("verticalSlider")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(200, 230, 156, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(120, 90, 156, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(210, 150, 156, 16))
        self.label_3.setObjectName("label_3")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "TextLabel"))
        self.label_2.setText(_translate("Form", "TextLabel"))
        self.label_3.setText(_translate("Form", "TextLabel"))


