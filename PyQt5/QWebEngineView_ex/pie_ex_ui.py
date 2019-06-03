# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pie_ex_ui.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(661, 463)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 146, 441))
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 35, 54, 12))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 54, 12))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 105, 54, 12))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(10, 140, 54, 12))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(10, 175, 54, 12))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(10, 210, 54, 12))
        self.label_6.setObjectName("label_6")
        self.spinBox_1 = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_1.setGeometry(QtCore.QRect(65, 30, 71, 22))
        self.spinBox_1.setMaximum(1000000)
        self.spinBox_1.setProperty("value", 1500)
        self.spinBox_1.setObjectName("spinBox_1")
        self.spinBox_2 = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_2.setGeometry(QtCore.QRect(65, 65, 71, 22))
        self.spinBox_2.setMaximum(1000000)
        self.spinBox_2.setProperty("value", 300)
        self.spinBox_2.setObjectName("spinBox_2")
        self.spinBox_3 = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_3.setGeometry(QtCore.QRect(65, 100, 71, 22))
        self.spinBox_3.setMaximum(1000000)
        self.spinBox_3.setProperty("value", 500)
        self.spinBox_3.setObjectName("spinBox_3")
        self.spinBox_4 = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_4.setGeometry(QtCore.QRect(65, 135, 71, 22))
        self.spinBox_4.setMaximum(1000000)
        self.spinBox_4.setProperty("value", 2000)
        self.spinBox_4.setObjectName("spinBox_4")
        self.spinBox_5 = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_5.setGeometry(QtCore.QRect(65, 170, 71, 22))
        self.spinBox_5.setMaximum(1000000)
        self.spinBox_5.setProperty("value", 500)
        self.spinBox_5.setObjectName("spinBox_5")
        self.spinBox_6 = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_6.setGeometry(QtCore.QRect(65, 205, 71, 22))
        self.spinBox_6.setMaximum(1000000)
        self.spinBox_6.setProperty("value", 300)
        self.spinBox_6.setObjectName("spinBox_6")
        self.checkBox = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox.setGeometry(QtCore.QRect(35, 245, 71, 16))
        self.checkBox.setObjectName("checkBox")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(160, 15, 491, 436))
        self.widget.setObjectName("widget")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "消费类别"))
        self.label.setText(_translate("Form", "伙食消费"))
        self.label_2.setText(_translate("Form", "房屋租金"))
        self.label_3.setText(_translate("Form", "水电煤气"))
        self.label_4.setText(_translate("Form", "交通费用"))
        self.label_5.setText(_translate("Form", "人情往来"))
        self.label_6.setText(_translate("Form", "淘宝网购"))
        self.checkBox.setText(_translate("Form", "自动演示"))


