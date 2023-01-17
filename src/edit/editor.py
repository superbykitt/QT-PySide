#codeing: utf-8

"""

"""

from PySide6.QtWidgets import QWidget,QBoxLayout
from view import VisualGrpahView
from scene import VisualGraphScene

from node import GraphNode


class VisualGraphEditor(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)
        self.setup_editor()
    
    def setup_editor(self):
        self.setGeometry(400,200,1260,720)
        self.setWindowTitle('Visual  Graph')

        self.layout=QBoxLayout(QBoxLayout.LeftToRight,self)    
        self.layout.setContentsMargins(0,0,0,0)

        self.scene=VisualGraphScene()
        self.view=VisualGrpahView(self.scene,self)
        self.layout.addWidget(self.view)



        self.debug_add_node()
        self.show()

    def debug_add_node(self):
        node=GraphNode(title='Area')
        self.view.add_graph_node(node,[0,0])
