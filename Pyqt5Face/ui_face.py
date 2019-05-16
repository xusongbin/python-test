# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_face.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(743, 457)
        self.labelImage1 = QtWidgets.QLabel(Form)
        self.labelImage1.setGeometry(QtCore.QRect(45, 20, 250, 300))
        self.labelImage1.setStyleSheet("border-width: 2px;\n"
"border-style: solid;\n"
"border-color: rgb(225, 225, 225);")
        self.labelImage1.setText("")
        self.labelImage1.setAlignment(QtCore.Qt.AlignCenter)
        self.labelImage1.setObjectName("labelImage1")
        self.labelImage2 = QtWidgets.QLabel(Form)
        self.labelImage2.setGeometry(QtCore.QRect(320, 30, 125, 150))
        self.labelImage2.setStyleSheet("border-width: 2px;\n"
"border-style: solid;\n"
"border-color: rgb(225, 225, 225);")
        self.labelImage2.setText("")
        self.labelImage2.setAlignment(QtCore.Qt.AlignCenter)
        self.labelImage2.setObjectName("labelImage2")
        self.labelSameTitle = QtWidgets.QLabel(Form)
        self.labelSameTitle.setGeometry(QtCore.QRect(460, 85, 54, 12))
        self.labelSameTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.labelSameTitle.setObjectName("labelSameTitle")
        self.textEditImage1 = QtWidgets.QTextEdit(Form)
        self.textEditImage1.setEnabled(False)
        self.textEditImage1.setGeometry(QtCore.QRect(40, 15, 260, 310))
        self.textEditImage1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.textEditImage1.setObjectName("textEditImage1")
        self.textEditImage1_2 = QtWidgets.QTextEdit(Form)
        self.textEditImage1_2.setEnabled(False)
        self.textEditImage1_2.setGeometry(QtCore.QRect(305, 15, 366, 176))
        self.textEditImage1_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.textEditImage1_2.setObjectName("textEditImage1_2")
        self.labelImage3 = QtWidgets.QLabel(Form)
        self.labelImage3.setGeometry(QtCore.QRect(530, 30, 125, 150))
        self.labelImage3.setStyleSheet("border-width: 2px;\n"
"border-style: solid;\n"
"border-color: rgb(225, 225, 225);")
        self.labelImage3.setText("")
        self.labelImage3.setAlignment(QtCore.Qt.AlignCenter)
        self.labelImage3.setObjectName("labelImage3")
        self.labelSameRate = QtWidgets.QLabel(Form)
        self.labelSameRate.setGeometry(QtCore.QRect(460, 110, 54, 12))
        self.labelSameRate.setAlignment(QtCore.Qt.AlignCenter)
        self.labelSameRate.setObjectName("labelSameRate")
        self.labelSamePass = QtWidgets.QLabel(Form)
        self.labelSamePass.setGeometry(QtCore.QRect(375, 240, 216, 66))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.labelSamePass.setFont(font)
        self.labelSamePass.setAlignment(QtCore.Qt.AlignCenter)
        self.labelSamePass.setObjectName("labelSamePass")
        self.pushButtonRead = QtWidgets.QPushButton(Form)
        self.pushButtonRead.setGeometry(QtCore.QRect(560, 195, 75, 23))
        self.pushButtonRead.setObjectName("pushButtonRead")
        self.textEditImage1_2.raise_()
        self.textEditImage1.raise_()
        self.labelImage1.raise_()
        self.labelImage2.raise_()
        self.labelSameTitle.raise_()
        self.labelImage3.raise_()
        self.labelSameRate.raise_()
        self.labelSamePass.raise_()
        self.pushButtonRead.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.labelSameTitle.setText(_translate("Form", "相似度"))
        self.labelSameRate.setText(_translate("Form", "0"))
        self.labelSamePass.setText(_translate("Form", "审核失败"))
        self.pushButtonRead.setText(_translate("Form", "导入模板"))

