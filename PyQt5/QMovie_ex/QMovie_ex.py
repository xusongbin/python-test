
# gif图片展示

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QMovie


class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.lb = QLabel(self)
        self.lb.setGeometry(100, 50, 300, 200)

        self.bt1 = QPushButton('开始', self)
        self.bt1.move(100, 20)
        self.bt2 = QPushButton('停止', self)
        self.bt2.move(200, 20)
        self.pix = QPixmap('gif/1.gif')
        self.lb.setPixmap(self.pix)
        self.lb.setScaledContents(True)
        self.bt1.clicked.connect(self.run)
        self.bt2.clicked.connect(self.run)
        self.show()

        self.movie = QMovie('gif/1.gif')
        self.movie.setSpeed(500)
        self.movie.updated.connect(self.fun_movie_updated)

    def fun_movie_updated(self):
        _num = self.movie.currentFrameNumber()
        _img = self.movie.currentImage()
        # _img.save('%d.jpg' % _num)
        print('current num {}:{}'.format(self.movie.frameCount(), _num))
        if _num == self.movie.frameCount()-1:
            self.movie.jumpToFrame(0)
            self.movie.stop()

    def run(self):
        self.lb.setMovie(self.movie)
        if self.sender() == self.bt1:
            self.movie.start()
        else:
            self.movie.stop()
            self.lb.setPixmap(self.pix)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    run = Example()
    sys.exit(app.exec_())

