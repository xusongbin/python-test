import sys
from PyQt5.QtCore import QUrl

from PyQt5 import QtCore, QtWidgets
from PyQt5 import QtQml, QtQuick

app = QtWidgets.QApplication(sys.argv)
engine = QtQml.QQmlApplicationEngine(QUrl('qml_hello.qml'))
sys.exit(app.exec_())
