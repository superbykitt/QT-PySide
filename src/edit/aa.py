from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import sys


class MyRect(QGraphicsItem):
    def __init__(
        self,
        rectCenter=QPointF(0, 0),
        rectSize=QSize(100, 100),
        rectFillColor=QColor(25, 25, 25, 100),
        rectPenColor=Qt.black,
        rectPenWidth=2,
        scene=None,
        cornerSize=QSize(10, 10),
        cornerFillColor=QColor(0, 0, 0, 255),
        cornerPenColor=Qt.black,
        cornerPenWidth=2
    ):
        super().__init__()
        self.scene = scene
        self.rectFillColor = rectFillColor
        self.rectPenWidth = rectPenWidth
        self.rectPenColor = rectPenColor
        self.cornerFillColor = cornerFillColor
        self.cornerPenWidth = cornerPenWidth
        self.cornerPenColor = cornerPenColor

        cx = rectCenter.x()
        cy = rectCenter.y()
        rw = rectSize.width()
        rh = rectSize.height()
        cw = cornerSize.width()
        ch = cornerSize.height()

        self.diff = None
        self.flag = None

        # 定义四个矩形
        # 中间的大矩形
        self.ce = QRectF(cx - rw / 2, cy - rh / 2, rw, rh)
        # 四个边角的拖动把手
        self.lt = QRectF(cx - (rw + cw) / 2, cy - (rh + ch) / 2, cw, ch)
        self.rt = QRectF(cx + (rw - cw) / 2, cy - (rh + ch) / 2, cw, ch)
        self.lb = QRectF(cx - (rw + cw) / 2, cy + (rh - ch) / 2, cw, ch)
        self.rb = QRectF(cx + (rw - cw) / 2, cy + (rh - ch) / 2, cw, ch)

    # 判断各个点的位置关系，返回正确的矩形大小
    def boundingRect(self):
        centerRectSize = self.ce.size()
        if centerRectSize.width() >= 0:
            if centerRectSize.height() >= 0:
                ltp = self.lt.topLeft()
                rbp = self.rb.bottomRight()
            else:
                ltp = self.lb.topLeft()
                rbp = self.rt.bottomRight()
            
        elif centerRectSize.width() < 0:
            if centerRectSize.height() >= 0:
                ltp = self.rt.topLeft()
                rbp = self.lb.bottomRight()
            else:
                ltp = self.rb.topLeft()
                rbp = self.lt.bottomRight()        
        
        return QRectF(ltp, rbp)

    def paint(self, painter, option, widget):
        painter.setPen(QPen(self.rectPenColor, self.rectPenWidth))
        painter.setBrush(QBrush(self.rectFillColor))
        painter.drawRect(self.ce)

        painter.setPen(QPen(self.cornerPenColor, self.cornerPenWidth))
        painter.setBrush(QBrush(self.cornerFillColor))

        painter.drawRoundedRect(self.lt, 5, 5)
        painter.drawRoundedRect(self.rt, 5, 5)
        painter.drawRoundedRect(self.lb, 5, 5)
        painter.drawRect(self.rb)

    # 判断拖动的是哪个位置
    def mousePressEvent(self, event):
        if not event.button() == Qt.LeftButton:
            return

        mousePressScenePos = event.scenePos()

        if self.lt.contains(mousePressScenePos):
            self.flag = "dragLeftTop"
            self.diff = mousePressScenePos - self.lt.center()
        elif self.rt.contains(mousePressScenePos):
            self.flag = "dragRightTop"
            self.diff = mousePressScenePos - self.rt.center()
        elif self.lb.contains(mousePressScenePos):
            self.flag = "dragLeftBottom"
            self.diff = mousePressScenePos - self.lb.center()
        elif self.rb.contains(mousePressScenePos):
            self.flag = "dragRightBottom"
            self.diff = mousePressScenePos - self.rb.center()
        elif self.ce.contains(mousePressScenePos):
            self.flag = "dragCenter"
            self.diff = mousePressScenePos - self.ce.center()
        else:
            self.flag = None
        
    def mouseMoveEvent(self, event):
        mouseCurPos = event.scenePos()

        match self.flag:
            case "dragLeftTop":
                leftTopCenter = mouseCurPos - self.diff
                rightBottomCenter = self.rb.center()
                self.lt.moveCenter(leftTopCenter)
                self.rt.moveCenter(QPointF(rightBottomCenter.x(), leftTopCenter.y()))
                self.lb.moveCenter(QPointF(leftTopCenter.x(), rightBottomCenter.y()))
                self.ce.setSize(QSizeF(rightBottomCenter.x() - leftTopCenter.x(), rightBottomCenter.y() - leftTopCenter.y()))
                self.ce.moveTopLeft(leftTopCenter)
                
            case "dragRightTop":
                rightTopCenter = mouseCurPos - self.diff
                leftBottomCenter = self.lb.center()
                self.lt.moveCenter(QPointF(leftBottomCenter.x(), rightTopCenter.y()))
                self.rt.moveCenter(rightTopCenter)
                self.rb.moveCenter(QPointF(rightTopCenter.x(), leftBottomCenter.y()))
                self.ce.setSize(QSizeF(rightTopCenter.x() - leftBottomCenter.x(), leftBottomCenter.y() - rightTopCenter.y()))
                self.ce.moveTopLeft(QPointF(leftBottomCenter.x(), rightTopCenter.y()))
                
            case "dragLeftBottom":
                leftBottomCenter = mouseCurPos - self.diff
                rightTopCenter = self.rt.center()
                self.lt.moveCenter(QPointF(leftBottomCenter.x(), rightTopCenter.y()))
                self.lb.moveCenter(leftBottomCenter)
                self.rb.moveCenter(QPointF(rightTopCenter.x(), leftBottomCenter.y()))
                self.ce.setSize(QSizeF(rightTopCenter.x() - leftBottomCenter.x(), leftBottomCenter.y() - rightTopCenter.y()))
                self.ce.moveTopLeft(QPointF(leftBottomCenter.x(), rightTopCenter.y()))
                
            case "dragRightBottom":
                rightBottomCenter = mouseCurPos - self.diff
                leftTopCenter = self.lt.center()
                self.rt.moveCenter(QPointF(rightBottomCenter.x(), leftTopCenter.y()))
                self.lb.moveCenter(QPointF(leftTopCenter.x(), rightBottomCenter.y()))
                self.rb.moveCenter(rightBottomCenter)
                self.ce.setSize(QSizeF(rightBottomCenter.x() - leftTopCenter.x(), rightBottomCenter.y() - leftTopCenter.y()))

            case "dragCenter":
                centerRectCenter = mouseCurPos - self.diff
                self.ce.moveCenter(centerRectCenter)
                self.lt.moveCenter(self.ce.topLeft())
                self.rt.moveCenter(self.ce.topRight())
                self.lb.moveCenter(self.ce.bottomLeft())
                self.rb.moveCenter(self.ce.bottomRight())
            
        self.scene.update()

    def mouseReleaseEvent(self, event):
        self.flag = None        


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.resize(500, 400)
        self.show()

        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        layout.addWidget(self.view)

        self.item = MyRect(scene=self.scene)
        self.scene.addItem(self.item)


if __name__ == "__main__":
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    window = MainWindow()
    sys.exit(app.exec())