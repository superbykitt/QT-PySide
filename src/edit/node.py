#codeing: utf-8

"""

"""

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QPainter, QPen, QColor, QBrush, QPainterPath, QFont
from PySide6.QtWidgets import QGraphicsItem, QGraphicsTextItem

class GraphNode(QGraphicsItem):

    def __init__(self, title='', parent=None):

        super().__init__(parent)

        # 定义node的大小
        self._node_width = 240
        self._node_height = 160
        self._node_radius = 10

        # node 边框
        self._pen_default = QPen(QColor('#151515'))
        self._pen_selected = QPen(QColor('#aaffee00'))
        # node 的背景
        self._brush_background = QBrush(QColor('#aa151515'))
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)

        # 节点的title
        self._title = title
        self._title_height = 35
        self._title_font = QFont('Arial', 13)
        self._title_color = Qt.white
        self._title_padding = 3
        self._brush_title_back = QBrush(QColor('#aa00003f'))

        self.init_title()



    def init_title(self):
        self._title_item = QGraphicsTextItem(self)
        self._title_item.setPlainText(self._title)
        self._title_item.setFont(self._title_font)
        self._title_item.setDefaultTextColor(self._title_color)
        self._title_item.setPos(self._title_padding, self._title_padding)

    def boundingRect(self) -> QRectF:
        print('vg_node ->boundingRect')
        return QRectF(0, 0, self._node_width, self._node_height)

    def paint(self, painter: QPainter, option, widget):
        print('vg_node ->paint')
        # 画背景颜色
        node_outline = QPainterPath()
        node_outline.addRoundedRect(0, 0, self._node_width, self._node_height, self._node_radius, self._node_radius)

        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(node_outline.simplified())
'''
        title_outline = QPainterPath()
        title_outline.setFillRule(Qt.windowFill)
        node_outline.addRoundedRect(0, 0, self._node_width, self._node_height, self._node_radius, self._node_radius)
        title_outline.addRect(0, self._title_height - self._node_radius, self._node_radius, self._node_radius)
        title_outline.addRect(self._node_width - self._node_radius, self._title_height - self._node_radius,
                              self._node_radius, self._node_radius)

        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title_back)

        painter.drawPath(title_outline.simplified())

'''      