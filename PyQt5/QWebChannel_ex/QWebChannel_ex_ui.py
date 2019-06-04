# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QWebChannel_ex_ui.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(440, 440)
        Form.setMinimumSize(QtCore.QSize(440, 440))
        Form.setMaximumSize(QtCore.QSize(440, 440))
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(20, 120, 400, 300))
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 55, 40, 20))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.lineEditUser = QtWidgets.QLineEdit(Form)
        self.lineEditUser.setGeometry(QtCore.QRect(55, 25, 113, 20))
        self.lineEditUser.setObjectName("lineEditUser")
        self.pushButtonCommit = QtWidgets.QPushButton(Form)
        self.pushButtonCommit.setGeometry(QtCore.QRect(25, 90, 75, 23))
        self.pushButtonCommit.setObjectName("pushButtonCommit")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(20, 25, 40, 20))
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.lineEditPwd = QtWidgets.QLineEdit(Form)
        self.lineEditPwd.setGeometry(QtCore.QRect(55, 55, 113, 20))
        self.lineEditPwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEditPwd.setObjectName("lineEditPwd")
        self.pushButtonCancel = QtWidgets.QPushButton(Form)
        self.pushButtonCancel.setGeometry(QtCore.QRect(110, 90, 75, 23))
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.labelInfo = QtWidgets.QLabel(Form)
        self.labelInfo.setGeometry(QtCore.QRect(195, 55, 216, 20))
        self.labelInfo.setText("")
        self.labelInfo.setObjectName("labelInfo")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "密码："))
        self.pushButtonCommit.setText(_translate("Form", "发送到网页"))
        self.label_2.setText(_translate("Form", "账户："))
        self.pushButtonCancel.setText(_translate("Form", "重置"))


