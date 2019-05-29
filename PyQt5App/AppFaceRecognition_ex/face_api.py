
import os
import sys
import threading
from time import sleep
from face_match import face_cmp

from cv2 import cv2
from PIL import Image

import ui_face
from PyQt5.QtWidgets import (QApplication, QWidget, QFileDialog)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QPixmap

face_path = 'face/'


def dir_access(path):
    _list = path.split('/')
    _idx = path.find(_list[len(_list) - 1])
    _dir = path[0:_idx]
    if _dir != '' and os.path.isdir(_dir) is False:
        try:
            os.makedirs(_dir)
            return True
        except:
            return False
    return True

class FaceForm(object):
    def __init__(self):
        self.work_widget = QWidget()
        self.work_widget.setWindowFlag(Qt.WindowMinimizeButtonHint)
        self.work_widget.setWindowIcon(QIcon('ico_main.ico'))
        self.work_ui = ui_face.Ui_Form()
        self.work_ui.setupUi(self.work_widget)
        self.work_ui.pushButtonRead.clicked.connect(self.work_fun_button_read)
        self.work_file_dialog = QFileDialog()

        self.work_get_image = False
        self.work_get_cmp = False

        self.face_cascade = cv2.CascadeClassifier(r'haarcascades/haarcascade_frontalface_default.xml')

        self.work_thread_video = threading.Thread(target=self.thread_get_video)
        self.work_thread_video.setDaemon(True)
        self.work_thread_video.start()

        self.work_thread_compare = threading.Thread(target=self.thread_compare_image)
        self.work_thread_compare.setDaemon(True)
        self.work_thread_compare.start()

        self.work_uitimer = QTimer()
        self.work_uitimer.timeout.connect(self.work_uitimer_event)
        self.work_uitimer.start(5)

    def run(self):
        self.work_widget.show()

    def work_fun_button_read(self):
        path, _type = QFileDialog.getOpenFileName(
            self.work_file_dialog,
            '选择图片', './', 'JPG Files(*.jpg);;JPEG Files(*.jpeg)')
        if path != '':
            img = Image.open(path)
            w, h = img.size
            k = h / w
            img = img.resize((125, int(125 * k)))
            img.save(face_path + 'tmp.jpg')

            im = cv2.imread(face_path + 'tmp.jpg')
            faces = self.face_cascade.detectMultiScale(im, scaleFactor=1.2, minNeighbors=5, minSize=(5, 5))
            self.work_get_cmp = False
            for (x, y, w, h) in faces:
                img.save(face_path + 'cmp.jpg')
                self.work_get_cmp = True
            if self.work_get_cmp:
                self.work_ui.labelImage3.setPixmap(QPixmap(face_path + 'cmp.jpg'))
            os.remove(face_path + 'tmp.jpg')

    def work_uitimer_event(self):
        if os.path.exists(face_path + 'show.jpg'):
            self.work_ui.labelImage1.setPixmap(QPixmap(face_path + 'show.jpg'))

        if os.path.exists(face_path + 'face.jpg'):
            self.work_ui.labelImage2.setPixmap(QPixmap(face_path + 'face.jpg'))

    def thread_compare_image(self):
        while True:
            try:
                if not self.work_get_image:
                    continue
                frame = cv2.imread(face_path + 'check.jpg')
                os.remove(face_path + 'check.jpg')
                self.work_get_image = False
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(5, 5))
                cv2.imwrite(face_path + 'face_tmp.jpg', frame)
                img = Image.open(face_path + 'face_tmp.jpg')
                for (x, y, w, h) in faces:
                    if w*1.2 < h:
                        x -= int((h / 1.2 - w) / 2)
                        w = int(h / 1.2)
                    elif w*1.2 > h:
                        y -= int((w * 1.2 - h) / 2)
                        h = int(w * 1.2)
                    img.crop((x, y, x + w, y + h)).resize((125, 150)).save(face_path + 'face.jpg')

                rate = face_cmp(face_path + 'face.jpg', face_path + 'cmp.jpg')
                self.work_ui.labelSameRate.setText('%.1f' % rate)
                if rate > 80:
                    self.work_ui.labelSamePass.setText('审核通过')
                else:
                    self.work_ui.labelSamePass.setText('审核失败')
            except Exception as e:
                print('compare except: %s' % e)
            sleep(0.05)

    def thread_get_video(self):
        cap = cv2.VideoCapture(0)
        while True:
            if cap.isOpened():
                ret, frame = cap.read()
                frame = cv2.flip(frame, 1, dst=None)  # 水平镜像
                height = len(frame)
                width = len(frame[0])
                x = 0
                y = 0
                w = width
                h = height
                # print('{},{}'.format(w, h))
                if (width * 1.2) > height:
                    x = int((width - int(height / 1.2)) / 2)
                    w = int(height / 1.2)
                elif (width * 1.2) < height:
                    y = int((height - int(width * 1.2)) / 2)
                    h = int(width * 1.2)
                cv2.imwrite(face_path + 'show_tmp.jpg', frame)
                img = Image.open(face_path + 'show_tmp.jpg')
                img = img.crop((x, y, x + w, y + h))
                img = img.resize((250, 300))
                img.save(face_path + 'show.jpg')
                if not self.work_get_image:
                    img.save(face_path + 'check.jpg')
                    self.work_get_image = True
            cv2.waitKey(1)


def app_run():
    app = QApplication(sys.argv)
    ff = FaceForm()
    ff.run()
    sys.exit(app.exec_())


if __name__ == '__main__':
    app_run()
