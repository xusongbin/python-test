
import os
import sys
import threading
from time import sleep, time

from cv2 import cv2
from PIL import Image
from face_recognition import load_image_file, face_encodings, compare_faces, face_distance

import ui_face
from PyQt5.QtWidgets import (QApplication, QWidget, QFileDialog)
from PyQt5.QtCore import Qt, QRect, QTimer
from PyQt5.QtGui import QIcon, QPixmap, QImage

face_path = 'face/'


def cmp_video_and_img():
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(r'haarcascades/haarcascade_frontalface_default.xml')
    # face_cascade.load(r'haarcascade_frontalface_default.xml')

    # if not os.path.exists('face/xjpic_head.jpg'):
    #     im = cv2.imread('face/xjpic.jpg')
    #     faces = face_cascade.detectMultiScale(im, scaleFactor=1.2, minNeighbors=5, minSize=(5, 5))
    #     for (x, y, w, h) in faces:
    #         img = Image.open('face/xjpic.jpg')
    #         img = img.crop((x, y, x+w, y+h))
    #         img.save('face/xjpic_head.jpg')

    if not os.path.exists('face/123_head.jpg'):
        im = cv2.imread('face/123.jpg')
        faces = face_cascade.detectMultiScale(im, scaleFactor=1.2, minNeighbors=5, minSize=(5, 5))
        for (x, y, w, h) in faces:
            img = Image.open('face/123.jpg')
            img = img.crop((x, y, x+w, y+h))
            img.save('face/123_head.jpg')
            print('get known face 123_head.jpg')

    lenna_img = cv2.imread("lena.jpg")
    while cap.isOpened():
        ret, frame = cap.read()
        if frame.ndim == 3:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            gray = frame

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(5, 5))  # 检测人脸
        for (x, y, w, h) in faces:
            cv2.imwrite('face/songbin.jpg', frame)
            img = Image.open('face/songbin.jpg')
            img = img.crop((x, y, x+w, y+h))
            img.save('face/songbin_head.jpg')

            try:
                known_img = load_image_file('face/123_head.jpg')
                unknown_img = load_image_file('face/songbin_head.jpg')

                known_encoding = face_encodings(known_img)[0]
                unknown_encoding = face_encodings(unknown_img)[0]

                results = compare_faces([known_encoding], unknown_encoding)
                print(results)
            except:
                pass

            cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow('frame', gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


def cmp_img_and_img():
    face_cascade = cv2.CascadeClassifier(r'haarcascades/haarcascade_frontalface_default.xml')

    if not os.path.exists('face/123_head.jpg'):
        im = cv2.imread('face/123.jpg')
        faces = face_cascade.detectMultiScale(im, scaleFactor=1.2, minNeighbors=5, minSize=(5, 5))
        for (x, y, w, h) in faces:
            img = Image.open('face/123.jpg')
            img = img.crop((x, y, x+w, y+h))
            img.save('face/123_head.jpg')
            print('get known face 123_head.jpg')

    if not os.path.exists('face/1234_head.jpg'):
        im = cv2.imread('face/1234.jpg')
        faces = face_cascade.detectMultiScale(im, scaleFactor=1.2, minNeighbors=5, minSize=(5, 5))
        for (x, y, w, h) in faces:
            img = Image.open('face/1234.jpg')
            img = img.crop((x, y, x+w, y+h))
            img.save('face/1234_head.jpg')
            print('get known face 1234_head.jpg')

    try:
        known_img = load_image_file('face/123_head.jpg')
        unknown_img = load_image_file('face/1234_head.jpg')

        known_encoding = face_encodings(known_img)[0]
        unknown_encoding = face_encodings(unknown_img)[0]

        results = compare_faces([known_encoding], unknown_encoding)
        print(results)
    except:
        pass


class FaceForm(object):
    def __init__(self):
        self.work_widget = QWidget()
        self.work_widget.setWindowFlag(Qt.WindowMinimizeButtonHint)
        self.work_widget.setWindowIcon(QIcon('ico_main.ico'))
        self.work_ui = ui_face.Ui_Form()
        self.work_ui.setupUi(self.work_widget)
        self.work_ui.pushButtonGet.clicked.connect(self.work_fun_button_get)
        self.work_ui.pushButtonRead.clicked.connect(self.work_fun_button_read)
        self.work_file_dialog = QFileDialog()

        self.face_cascade = cv2.CascadeClassifier(r'haarcascades/haarcascade_frontalface_default.xml')

        self.work_thread = threading.Thread(target=self.work_thread_event)
        self.work_thread.setDaemon(True)
        self.work_thread.start()

        self.work_thread1 = threading.Thread(target=self.work_thread1_event)
        self.work_thread1.setDaemon(True)
        self.work_thread1.start()

        self.work_uitimer = QTimer()
        self.work_uitimer.timeout.connect(self.work_uitimer_event)
        self.work_uitimer.start(5)

    def run(self):
        self.work_widget.show()

    def work_fun_button_get(self):
        if not os.path.exists(face_path + 'xsb_head.jpg'):
            print('head not exist')
            im = cv2.imread(face_path + 'xsb.jpg')
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(5, 5))
            for (x, y, w, h) in faces:
                img = Image.open(face_path + 'xsb.jpg')
                img = img.crop((x, y, x + w, y + h))
                k = h / w
                img = img.resize((125, int(125 * k)))
                img.save(face_path + 'xsb_head.jpg')
        self.work_ui.labelImage3.setPixmap(QPixmap(face_path + 'xsb_head.jpg'))

    def work_fun_button_read(self):
        path, _type = QFileDialog.getOpenFileName(
            self.work_file_dialog,
            '选择图片', './', 'JPG Files(*.jpg);;JPEG Files(*.jpeg)')
        if path != '':
            img = Image.open(path)
            w, h = img.size
            k = h / w
            img = img.resize((250, int(250 * k)))
            img.save(face_path + 'tmp.jpg')
            self.work_ui.labelImage1.setPixmap(QPixmap(face_path + 'tmp.jpg'))

            im = cv2.imread(path)
            faces = self.face_cascade.detectMultiScale(im, scaleFactor=1.2, minNeighbors=5, minSize=(5, 5))
            for (x, y, w, h) in faces:
                img = Image.open(path)
                img = img.crop((x, y, x + w, y + h))
                k = h / w
                img = img.resize((125, int(125 * k)))
                img.save(face_path + 'cmp.jpg')
            self.work_ui.labelImage2.setPixmap(QPixmap(face_path + 'cmp.jpg'))

            try:
                known_img = load_image_file(face_path + 'xsb_head.jpg')
                unknown_img = load_image_file(face_path + 'cmp.jpg')

                known_encoding = face_encodings(known_img)[0]
                unknown_encoding = face_encodings(unknown_img)[0]

                rate = face_distance([known_encoding], unknown_encoding)[0]
                rate = 1 - float(rate)
                rate = float('%.1f' % (rate * 100))
                self.work_ui.labelSameRate.setText('%.1f' % rate)
                if rate > 60:
                    self.work_ui.labelSamePass.setText('审核通过')
                else:
                    self.work_ui.labelSamePass.setText('审核失败')
            except Exception as e:
                print('compare except: %s' % e)

    def work_fun_compare(self):
        im = cv2.imread(face_path + 'show.jpg')
        faces = self.face_cascade.detectMultiScale(im, scaleFactor=1.2, minNeighbors=5, minSize=(5, 5))
        if faces:
            cv2.imwrite(face_path + 'face.jpg', im)
            for (x, y, w, h) in faces:
                img = Image.open(face_path + 'face.jpg')
                img = img.crop((x, y, x + w, y + h))
                img = img.resize((125, 250))
                img.save(face_path + 'face.jpg')
            self.work_ui.labelImage2.setPixmap(QPixmap(face_path + 'face.jpg'))

        try:
            known_img = load_image_file(face_path + 'xsb_head.jpg')
            unknown_img = load_image_file(face_path + 'cmp.jpg')

            known_encoding = face_encodings(known_img)[0]
            unknown_encoding = face_encodings(unknown_img)[0]

            rate = face_distance([known_encoding], unknown_encoding)[0]
            rate = 1 - float(rate)
            rate = float('%.1f' % (rate * 100))
            self.work_ui.labelSameRate.setText('%.1f' % rate)
            if rate > 60:
                self.work_ui.labelSamePass.setText('审核通过')
            else:
                self.work_ui.labelSamePass.setText('审核失败')
        except Exception as e:
            print('compare except: %s' % e)

    def work_uitimer_event(self):
        if os.path.exists(face_path + 'show.jpg'):
            self.work_ui.labelImage1.setPixmap(QPixmap(face_path + 'show.jpg'))
            os.remove(face_path + 'show.jpg')

        if os.path.exists(face_path + 'face.jpg'):
            self.work_ui.labelImage2.setPixmap(QPixmap(face_path + 'face.jpg'))
            os.remove(face_path + 'face.jpg')

    def work_thread1_event(self):
        while True:
            start_time = time()
            try:
                if not os.path.exists(face_path + 'check.jpg'):
                    continue
                frame = cv2.imread(face_path + 'check.jpg')
                os.remove(face_path + 'check.jpg')
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

                known_img = load_image_file(face_path + 'xsb_head.jpg')
                unknown_img = load_image_file(face_path + 'face.jpg')

                known_encoding = face_encodings(known_img)[0]
                unknown_encoding = face_encodings(unknown_img)[0]

                rate = face_distance([known_encoding], unknown_encoding)[0]
                rate = 1 - float(rate)
                rate = float('%.1f' % (rate * 100))
                self.work_ui.labelSameRate.setText('%.1f' % rate)
                if rate > 60:
                    self.work_ui.labelSamePass.setText('审核通过')
                else:
                    self.work_ui.labelSamePass.setText('审核失败')
            except Exception as e:
                print('compare except: %s' % e)
            stop_time = time()
            print('use time: %.3f' % (stop_time - start_time))
            sleep(0.05)

    def work_thread_event(self):
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
                if not os.path.exists(face_path + 'show.jpg'):
                    img.save(face_path + 'show.jpg')
                if not os.path.exists(face_path + 'check.jpg'):
                    img.save(face_path + 'check.jpg')
            cv2.waitKey(1)


def app_run():
    app = QApplication(sys.argv)
    ff = FaceForm()
    ff.run()
    sys.exit(app.exec_())


if __name__ == '__main__':
    app_run()
