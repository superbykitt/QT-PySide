#codeing: utf-8

"""

"""
import sys
from PySide6.QtWidgets import QApplication
from editor import VisualGraphEditor

if __name__== '__main__':
    app=QApplication([])
    
    _vg=VisualGraphEditor()
    print(_vg)
    sys.exit(app.exec())  