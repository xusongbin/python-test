
# 浏览器

import sys
import sqlite3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *

from AppWeb_ui import *


class CookieRead(object):
    def __init__(self, view):
        self.view = view
        self.cookie = {}
        self.js_flag = False
        self.js_ts = 0

    def get_by_sqlite(self):
        _path = self.view.page().profile().defaultProfile().persistentStoragePath() + '/Cookies'
        conn = sqlite3.connect(_path)
        cursor = conn.cursor()
        try:
            cookies = cursor.execute('select name,value from cookies').fetchall()
            for key, value in cookies:
                self.cookie[key] = value
        except:
            pass
        cursor.close()
        conn.close()
        return self.cookie

    def get_by_js(self):
        self.view.page().runJavaScript("function test(){return document.cookie}")
        self.view.page().runJavaScript("test();", self.on_js_test_call)

    def on_js_test_call(self, result):
        self.cookie = result
        print(self.cookie)


class Web(QMainWindow):
    def __init__(self):
        super().__init__()

        self.wui = Ui_MainWindow()
        self.wui.setupUi(self)

        self.message_box = QMessageBox(self)
        self.file_dialog = QFileDialog(self)

        self.wui.tabWidget.tabCloseRequested.connect(self.on_tw_close_requested)
        self.wui.tabWidget.currentChanged.connect(self.on_tw_current_changed)
        self.wui.lineEdit.setMouseTracking(True)
        self.wui.lineEdit.installEventFilter(self)
        self.wui.lineEdit.textChanged.connect(self.on_le_text_changed)
        self.wui.pushButtonNew.clicked.connect(self.on_pb_new_clicked)
        self.wui.pushButtonForward.clicked.connect(self.on_pb_forward_clicked)
        self.wui.pushButtonBack.clicked.connect(self.on_pb_back_clicked)
        self.wui.pushButtonFresh.clicked.connect(self.on_pb_fresh_clicked)
        self.wui.pushButtonStop.clicked.connect(self.on_pb_stop_clicked)
        self.wui.pushButtonGo.clicked.connect(self.on_pb_go_clicked)
        self.wui.pushButtonHome.clicked.connect(self.on_pb_home_clicked)

        settings = QWebEngineSettings.defaultSettings()
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.m_model = QStandardItemModel(0, 1, self)
        m_completer = QCompleter(self.m_model, self)
        self.wui.lineEdit.setCompleter(m_completer)
        m_completer.activated.connect(self.on_url_choose)

        self.log = True

        self.view = QWebEngineView()
        self.view.load(QUrl("https://www.baidu.com/"))
        # self.view.load(QUrl("https://blog.csdn.net/"))
        self.new_tab(self.view)

    def new_tab(self, view):
        self.wui.pushButtonBack.setEnabled(False)
        self.wui.pushButtonForward.setEnabled(False)
        view.titleChanged.connect(self.on_view_title_changed)
        view.iconChanged.connect(self.on_view_icon_changed)
        view.loadProgress.connect(self.on_view_load_progress)
        view.loadFinished.connect(self.on_view_load_finished)
        view.urlChanged.connect(self.on_view_url_changed)
        view.page().linkHovered.connect(self.on_view_show_url)
        url = self.get_url(view)
        self.wui.lineEdit.setText(url)
        self.wui.tabWidget.addTab(view, "新标签页")
        self.wui.tabWidget.setCurrentWidget(view)
        view.setObjectName(str(self.wui.tabWidget.currentIndex()))

    def get_url(self, view):
        if self.log:
            pass
        url = view.url().toString()
        return url

    def on_tw_close_requested(self, idx):
        if self.wui.tabWidget.count() > 1:
            self.wui.tabWidget.widget(idx).deleteLater()
            self.wui.tabWidget.removeTab(idx)
        elif self.wui.tabWidget.count() == 1:
            self.wui.tabWidget.removeTab(0)
            self.on_pb_new_clicked()

    def on_tw_current_changed(self, idx):
        view = self.wui.tabWidget.widget(idx)
        if view:
            url = self.get_url(view)
            self.wui.lineEdit.setText(url)

    def closeEvent(self, e):
        num = self.wui.tabWidget.count()
        msg = "你打开了{}个标签页，现在确认关闭？".format(num)
        if num > 1:
            r = self.message_box.question(
                self, "关闭浏览器", msg, QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel
            )
            if r == QMessageBox.Ok:
                e.accept()
            elif r == QMessageBox.Cancel:
                e.ignore()
        else:
            e.accept()

    def eventFilter(self, obj, e):
        if obj == self.wui.lineEdit:
            if e.type() == QEvent.MouseButtonRelease:
                self.wui.lineEdit.selectAll()
            elif e.type() == QEvent.KeyPress:
                if e.key() == Qt.Key_Return:
                    self.on_pb_go_clicked()
        return QObject.eventFilter(self, obj, e)

    def on_view_title_changed(self, title):
        index = int(self.sender().objectName())
        if len(title) > 16:
            title = title[0:17]
        self.wui.tabWidget.setTabText(index, title)

    def on_view_icon_changed(self, icon):
        index = int(self.sender().objectName())
        self.wui.tabWidget.setTabIcon(index, icon)

    def on_view_load_progress(self, progress):
        self.wui.progressBar.show()
        self.wui.progressBar.setValue(progress)

    def on_view_load_finished(self, finished):
        if finished:
            cr = CookieRead(self.sender())
            print(cr.get_by_js())
            # self.view.page().profile().defaultProfile().persistentStoragePath()
            self.wui.progressBar.setValue(100)
            self.wui.progressBar.hide()
            self.wui.progressBar.setValue(0)

    def on_view_url_changed(self, url):
        self.wui.lineEdit.setText(url.toString())
        index = self.wui.tabWidget.currentIndex()
        view = self.wui.tabWidget.currentWidget()
        history = view.history()
        if history.count() > 1:
            if history.currentItemIndex() == history.count()-1:
                self.wui.pushButtonBack.setEnabled(True)
                self.wui.pushButtonForward.setEnabled(False)
            elif history.currentItemIndex() == 0:
                self.wui.pushButtonBack.setEnabled(False)
                self.wui.pushButtonForward.setEnabled(True)
            else:
                self.wui.pushButtonBack.setEnabled(True)
                self.wui.pushButtonForward.setEnabled(True)

    def on_view_show_url(self, url):
        self.wui.statusBar.showMessage(url)

    def on_url_choose(self, url):
        self.wui.lineEdit.setText(url)

    def on_le_text_changed(self, text):
        group = text.split('.')
        if len(group) == 3 and group[-1]:
            return
        elif len(group) == 3 and not (group[-1]):
            suffix = ["com", "cn", "net", "org", "gov", "cc"]
            self.m_model.removeRows(0, self.m_model.rowCount())
            for i in range(0, len(suffix)):
                self.m_model.insertRow(0)
                self.m_model.setData(self.m_model.index(0, 0), text + suffix[i])

    def on_pb_new_clicked(self):
        view = QWebEngineView()
        self.new_tab(view)
        view.load(QUrl(''))

    def on_pb_forward_clicked(self):
        self.wui.tabWidget.currentWidget().forward()

    def on_pb_back_clicked(self):
        self.wui.tabWidget.currentWidget().back()

    def on_pb_fresh_clicked(self):
        self.wui.tabWidget.currentWidget().reload()

    def on_pb_stop_clicked(self):
        self.wui.tabWidget.currentWidget().stop()

    def on_pb_go_clicked(self):
        url = self.wui.lineEdit.text()
        if url[0:7] == "http://" or url[0:8] == "https://":
            q_url = QUrl(url)
        else:
            q_url = QUrl("http://" + url)
        self.wui.tabWidget.currentWidget().load(q_url)

    def on_pb_home_clicked(self):
        url = QUrl("http://www.baidu.com")
        if self.wui.tabWidget.currentWidget().title() == "about:blank":
            self.wui.tabWidget.currentWidget().load(url)
        else:
            view = QWebEngineView()            self.new_tab(view)
            view.load(url)

    def __del__(self):
        self.view.deleteLater()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    exe = Web()
    exe.show()
    sys.exit(app.exec_())
