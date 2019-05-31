#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
from math import sin, cos, pi

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Example(QWidget):
    def __init__(self):
        super().__init__()

        timer = QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(100)

        self.setWindowTitle("叮当猫")
        self.resize(400, 500)

        self.draw_pen = QPen(Qt.black, 3)
        self.head_color = QColor(156, 214, 239)
        self.face_color = QColor(255, 255, 255)
        self.mouth_color = QColor(180, 10, 10)
        self.nose_color = QColor(200, 50, 50)
        self.neck_color = QColor(220, 90, 90)
        self.pupil_color = QColor(0, 0, 0)

        self.eye_color = self.face_color
        self.nose_light_color = self.face_color
        self.nose_line_color = self.pupil_color
        self.beard_color = self.pupil_color
        self.body_color = self.head_color
        self.foot_color = self.face_color
        self.chest_color = self.face_color
        self.pocket_color = self.chest_color

    def draw_head(self, qp, x, y, r):     # 画头部
        path = QPainterPath()
        # 计算右下角绘图起始坐标
        cx, cy = x, y + r
        ox = cx + r * cos(45 * pi / 180)
        oy = cy + r * sin(45 * pi / 180)
        path.moveTo(ox, oy)
        # 计算头部的矩形信息 fx,fy,fw,fh， 设置绘图起始到结束角度
        fx, fy, fw, fh = x - r, y, r * 2,  r * 2
        path.arcTo(QRectF(fx, fy, fw, fh), -45, 270)
        # 设置封闭绘图形状
        path.closeSubpath()
        # 设置绘图颜色
        qp.restore()
        qp.setPen(self.draw_pen)
        qp.setBrush(self.head_color)
        qp.save()
        # 设置以上绘图信息给QPainter
        qp.drawPath(path)
        return (cx, cy), (ox, oy)

    def draw_face(self, qp, head, r):     # 画脸部
        cx, cy = head[0]
        ox, oy = head[1]
        path = QPainterPath()
        # 计算脸部与头部的半径差值
        r0 = r / 8
        # 计算脸部起始绘图坐标
        ox = ox - r0
        oy = oy
        path.moveTo(ox, oy)
        # 计算脸部的矩形信息 fx,fy,fw,fh, 设置绘图起始到结束角度
        cx = cx
        r = (ox - cx) / cos(45 * pi / 180)
        cy = oy - r * sin(45 * pi / 180)
        fx, fy, fw, fh = cx - r, cy - r, r * 2,  r * 2
        path.arcTo(QRectF(fx, fy, fw, fh), -45, 270)
        # 设置封闭绘图形状
        path.closeSubpath()
        # 设置绘图颜色
        qp.restore()
        qp.setPen(self.draw_pen)
        qp.setBrush(self.face_color)
        qp.save()
        # 设置以上绘图信息给QPainter
        qp.drawPath(path)
        return cx, cy, r

    def draw_mouth(self, qp, face):
        cx, cy, r = face
        path = QPainterPath()
        # 计算嘴巴半径
        r = r / 2
        # 计算左边绘图起始坐标
        ox = cx + r * cos(180 * pi / 180)
        oy = cy + r * sin(180 * pi / 180)
        path.moveTo(ox, oy)
        # 计算嘴部的矩形信息 fx,fy,fw,fh， 设置绘图起始到结束角度
        fx, fy, fw, fh = cx - r, cy - r, r * 2,  r * 2
        path.arcTo(QRectF(fx, fy, fw, fh), -180, 180)
        # 设置封闭绘图形状
        path.closeSubpath()
        # 设置绘图颜色
        qp.restore()
        qp.setPen(self.draw_pen)
        qp.setBrush(self.mouth_color)
        qp.save()
        # 设置以上绘图信息给QPainter
        qp.drawPath(path)
        return cx, cy, r

    def draw_nose(self, qp, face):
        cx, cy, r = face
        path = QPainterPath()
        # 计算鼻子半径
        r = r / 8
        # 计算鼻子中心位置
        cx = cx
        cy = cy - r * 5
        # 计算左边绘图起始坐标
        ox = cx + r * cos(180 * pi / 180)
        oy = cy + r * sin(180 * pi / 180)
        path.moveTo(ox, oy)
        # 计算鼻子的矩形信息 fx,fy,fw,fh， 设置绘图起始到结束角度
        fx, fy, fw, fh = cx - r, cy - r, r * 2,  r * 2
        path.arcTo(QRectF(fx, fy, fw, fh), -180, 360)
        # 设置封闭绘图形状
        path.closeSubpath()
        # 设置绘图颜色
        qp.restore()
        qp.setPen(self.draw_pen)
        qp.setBrush(self.nose_color)
        qp.save()
        # 设置以上绘图信息给QPainter
        qp.drawPath(path)
        return cx, cy, r

    def draw_nose_light(self, qp, nose):
        cx, cy, r = nose
        path = QPainterPath()
        # 计算鼻子反光半径
        r = r / 3
        # 计算鼻子反光中心位置
        cx = cx - r * 0.7
        cy = cy - r * 0.2
        # 计算左边绘图起始坐标
        ox = cx + r * cos(180 * pi / 180)
        oy = cy + r * sin(180 * pi / 180)
        path.moveTo(ox, oy)
        # 计算鼻子反光的矩形信息 fx,fy,fw,fh， 设置绘图起始到结束角度
        fx, fy, fw, fh = cx - r, cy - r, r * 2,  r * 2
        path.arcTo(QRectF(fx, fy, fw, fh), -180, 360)
        # 设置封闭绘图形状
        path.closeSubpath()
        # 设置绘图颜色
        qp.restore()
        qp.setPen(Qt.NoPen)
        qp.setBrush(self.nose_light_color)
        qp.save()
        # 设置以上绘图信息给QPainter
        qp.drawPath(path)
        return cx, cy, r

    def draw_eye(self, qp, nose):
        cx, cy, r = nose
        path = QPainterPath()
        # 计算眼睛椭圆宽a高b
        a, b = r * 1.2, r * 1.6
        # 计算眼睛中心位置
        cx1, cy1 = cx - a, cy - b * 1.5
        cx2, cy2 = cx + a, cy - b * 1.5
        # 计算左边绘图起始坐标
        ox1, oy1 = cx1, cy1 + b
        ox2, oy2 = cx2, cy2 + b
        # 计算眼睛的矩形信息 fx,fy,fw,fh， 设置绘图起始到结束角度
        fw, fh = a * 2, b * 2
        fx1, fy1 = cx1 - a, cy1 - b
        fx2, fy2 = cx2 - a, cy2 - b
        # 设置封闭绘图形状
        path.closeSubpath()
        # 设置绘图颜色
        qp.restore()
        qp.setPen(self.draw_pen)
        qp.setBrush(self.eye_color)
        qp.save()
        # 设置以上绘图信息给QPainter
        path.moveTo(ox1, oy1)
        path.arcTo(QRectF(fx1, fy1, fw, fh), -90, 360)
        qp.drawPath(path)
        path.moveTo(ox2, oy2)
        path.arcTo(QRectF(fx2, fy2, fw, fh), -90, 360)
        qp.drawPath(path)
        return (cx1, cy1), (cx2, cy2), (a, b)

    def draw_pupil(self, qp, eye):
        cx1, cy1 = eye[0]
        cx2, cy2 = eye[1]
        a, b = eye[2]
        path = QPainterPath()
        # 计算眼瞳椭圆宽a高b
        a, b = a / 3, b / 3
        # 计算眼睛中心位置
        cx1, cy1 = cx1 + a, cy1 + b * 0.6
        cx2, cy2 = cx2 - a, cy2 + b * 0.6
        # 计算左边绘图起始坐标
        ox1, oy1 = cx1, cy1 + b
        ox2, oy2 = cx2, cy2 + b
        # 计眼瞳的矩形信息 fx,fy,fw,fh， 设置绘图起始到结束角度
        fw, fh = a * 2, b * 2
        fx1, fy1 = cx1 - a, cy1 - b
        fx2, fy2 = cx2 - a, cy2 - b
        # 设置封闭绘图形状
        path.closeSubpath()
        # 设置绘图颜色
        qp.restore()
        qp.setPen(self.draw_pen)
        qp.setBrush(self.pupil_color)
        qp.save()
        # 设置以上绘图信息给QPainter
        path.moveTo(ox1, oy1)
        path.arcTo(QRectF(fx1, fy1, fw, fh), -90, 360)
        qp.drawPath(path)
        path.moveTo(ox2, oy2)
        path.arcTo(QRectF(fx2, fy2, fw, fh), -90, 360)
        qp.drawPath(path)
        return (cx1, cy1), (cx2, cy2), (a, b)

    def draw_nose_line(self, qp, mouth, nose):    # 画鼻子下面的线
        # 计算线信息
        x1, y1, r1 = mouth
        x2, y2, r2 = nose
        y2 = y2 + r2
        # 设置绘图颜色
        qp.restore()
        qp.setPen(self.draw_pen)
        qp.setBrush(self.nose_line_color)
        qp.save()
        qp.drawLine(x1, y1, x2, y2)

    def draw_beard(self, qp, mouth):    # 画胡须
        _list = []
        # 计算线信息
        x, y, r = mouth
        x1, y1 = x - r * 0.9, y - r * 0.3
        x2, y2 = x - r * 2.2, y + r * 0.1
        _list.append((x1, y1, x2, y2))
        x1, y1 = x1 + r * 0.1, y1 - r * 0.3
        x2, y2 = x2 + r * 0.1, y2 - r * 0.6
        _list.append((x1, y1, x2, y2))
        x1, y1 = x1 - r * 0.03, y1 - r * 0.26
        x2, y2 = x2 + r * 0.16, y2 - r * 0.66
        _list.append((x1, y1, x2, y2))
        x1, y1 = x + r * 0.95, y - r * 0.31
        x2, y2 = x + r * 2.1, y - r * 0.05
        _list.append((x1, y1, x2, y2))
        x1, y1 = x1 - r * 0.19, y1 - r * 0.32
        x2, y2 = x2 + r * 0.15, y2 - r * 0.7
        _list.append((x1, y1, x2, y2))
        x1, y1 = x1 - r * 0.17, y1 - r * 0.35
        x2, y2 = x2 - r * 0.45, y2 - r * 0.65
        _list.append((x1, y1, x2, y2))
        # 设置绘图颜色
        qp.restore()
        qp.setPen(self.draw_pen)
        qp.setBrush(self.beard_color)
        qp.save()
        for line in _list:
            qp.drawLine(line[0], line[1], line[2], line[3])

    def draw_body(self, qp, head):  # 画身体
        cx, cy = head[0]
        ox, oy = head[1]
        a = cx - ox
        b = oy - cy
        path = QPainterPath()
        # 计算多边形4个点
        x1, y1 = ox, oy
        x2, y2 = cx + a, y1
        x3, y3 = x2 - a * 0.05, y2 + b * 1.5
        x4, y4 = x1 + a * 0.04, y3
        body_pg = QPolygonF()
        body_pg << QPointF(x1, y1) << QPointF(x2, y2) << QPointF(x3, y3) << QPointF(x4, y4)
        path.addPolygon(body_pg)
        path.closeSubpath()
        # 设置绘图颜色
        qp.restore()
        qp.setPen(self.draw_pen)
        qp.setBrush(self.body_color)
        qp.save()
        # 设置以上绘图信息给QPainter
        qp.drawPath(path)
        return (x1, y1), (x2, y2), (x3, y3), (x4, y4)

    def draw_foot(self, qp, body):    # 画脚
        p3 = body[2]
        p4 = body[3]
        path = QPainterPath()
        # 计算脚椭圆宽a高b
        cx = (p4[0] + p3[0]) / 2
        cy = p4[1]
        r = (p4[0] - p3[0]) / 2
        a = (r / 2) * 1.3
        b = (r / 2) * 0.6
        # 计算脚中心位置
        cx1, cy1 = cx - a, cy
        cx2, cy2 = cx + a, cy
        # 计算左边绘图起始坐标
        ox1, oy1 = cx1, cy1 + b
        ox2, oy2 = cx2, cy2 + b
        # 计算脚的矩形信息 fx,fy,fw,fh， 设置绘图起始到结束角度
        fw, fh = a * 2, b * 2
        fx1, fy1 = cx1 - a, cy1 - b
        fx2, fy2 = cx2 - a, cy2 - b
        # 设置封闭绘图形状
        path.closeSubpath()
        # 设置绘图颜色
        qp.restore()
        qp.setPen(self.draw_pen)
        qp.setBrush(self.foot_color)
        qp.save()
        # 设置以上绘图信息给QPainter
        path.moveTo(ox1, oy1)
        path.arcTo(QRectF(fx1, fy1, fw, fh), -90, 360)
        qp.drawPath(path)
        path.moveTo(ox2, oy2)
        path.arcTo(QRectF(fx2, fy2, fw, fh), -90, 360)
        qp.drawPath(path)
        return (cx1, cy1), (cx2, cy2), (a, b)

    def draw_chest(self, qp, head):    # 画胸
        cx, cy = head[0]
        ox, oy = head[1]
        path = QPainterPath()
        # 计算胸椭圆宽a高b
        a = ox - cx
        cx = cx
        a = a * 0.75
        b = a * 1.2
        cy = oy + b * 0.15
        # 计算左边绘图起始坐标
        ox = cx - a * 0.92
        oy = oy
        path.moveTo(ox, oy)
        # 计算胸的矩形信息 fx,fy,fw,fh， 设置绘图起始到结束角度
        fx, fy, fw, fh = cx - a, cy - b, a * 2,  b * 2
        path.arcTo(QRectF(fx, fy, fw, fh), -189, 198)
        # 设置封闭绘图形状
        path.closeSubpath()
        # 设置绘图颜色
        qp.restore()
        qp.setPen(self.draw_pen)
        qp.setBrush(self.chest_color)
        qp.save()
        # 设置以上绘图信息给QPainter
        qp.drawPath(path)
        return (cx, cy), (a, b)

    def draw_pocket(self, qp, chest):   # 画口袋
        cx, cy = chest[0]
        a, b = chest[1]
        path = QPainterPath()
        # 计算口袋椭圆宽a高b
        a = a * 0.7
        b = b * 0.5
        cx = cx
        cy = cy + b * 0.6
        # 计算左边绘图起始坐标
        ox = cx - a
        oy = cy
        path.moveTo(ox, oy)
        # 计算口袋的矩形信息 fx,fy,fw,fh， 设置绘图起始到结束角度
        fx, fy, fw, fh = cx - a, cy - b, a * 2,  b * 2
        path.arcTo(QRectF(fx, fy, fw, fh), -180, 180)
        # 设置封闭绘图形状
        path.closeSubpath()
        # 设置绘图颜色
        qp.restore()
        qp.setPen(self.draw_pen)
        qp.setBrush(self.pocket_color)
        qp.save()
        # 设置以上绘图信息给QPainter
        qp.drawPath(path)
        return (cx, cy), (a, b)

    def draw_neck(self, qp, head, pocket):    # 画围脖
        cx, cy = head[0]
        ox, oy = head[1]    # 右边
        cx1, cy1 = pocket[0]
        r = ox - cx
        path = QPainterPath()
        # 计算多边形3个点
        x1, y1 = ox, oy
        x2, y2 = cx, oy + (cy1 - oy) * 0.6
        x3, y3 = cx - r, oy
        body_pg = QPolygonF()
        body_pg << QPointF(x1, y1) << QPointF(x2, y2) << QPointF(x3, y3)
        path.addPolygon(body_pg)
        path.closeSubpath()
        # 设置绘图颜色
        qp.restore()
        qp.setPen(self.draw_pen)
        qp.setBrush(self.neck_color)
        qp.save()
        # 设置以上绘图信息给QPainter
        qp.drawPath(path)
        return (x1, y1), (x2, y2), (x3, y3)

    def paintEvent(self, e):
        w = self.size().width()
        h = self.size().height()
        x, y = w / 2, h / 10    # 头顶坐标
        r = w * 2 / 6   # 头部半径，整体比例以这个参数做调整
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)
        head = self.draw_head(qp, x, y, r)   # 画头部
        face = self.draw_face(qp, head, r)   # 画脸部
        mouth = self.draw_mouth(qp, face)  # 画嘴部
        nose = self.draw_nose(qp, face)  # 画鼻子
        self.draw_nose_light(qp, nose)  # 画鼻子反光
        eye = self.draw_eye(qp, nose)  # 画眼睛
        self.draw_pupil(qp, eye)    # 画眼瞳
        self.draw_nose_line(qp, mouth, nose)   # 画鼻子下面的线
        self.draw_beard(qp, mouth)  # 画胡须
        body = self.draw_body(qp, head)    # 画身体
        self.draw_foot(qp, body)    # 画脚
        chest = self.draw_chest(qp, head)   # 画胸
        pocket = self.draw_pocket(qp, chest)     # 画口袋
        self.draw_neck(qp, head, pocket)    # 画围脖


if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = Example()
    clock.show()
    sys.exit(app.exec_())
