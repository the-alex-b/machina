import sys
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QListWidget
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt


class DraggableScatter(pg.ScatterPlotItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dragIndex = None
        self.dragOffset = None

    def mouseClickEvent(self, ev):
        if ev.button() == Qt.LeftButton:
            print("Mouse click")
            # Check if we clicked on a point
            pts = self.pointsAt(ev.pos())
            if len(pts) > 0:
                self.dragPoint = pts[0]
                ev.accept()
            else:
                self.parent.on_mouse_click(ev)

    # def mouseMoveEvent(self, ev):
    #     print(ev)
    #     # Check if the cursor is over a point
    #     if len(self.pointsAt(ev.pos())) > 0:
    #         self.setCursor(
    #             QCursor(Qt.PointingHandCursor)
    #         )  # Change cursor to pointing hand
    #     else:
    #         self.unsetCursor()  # Restore the default cursor

    def mouseDragEvent(self, ev):
        if ev.button() == Qt.LeftButton and self.dragIndex is not None:
            if ev.isStart():
                # We are starting a drag
                self.dragOffset = self.data[self.dragIndex].pos() - ev.pos()
            ev.accept()
            newPos = ev.pos() + self.dragOffset
            self.parent().updatePointPosition(self.dragIndex, (newPos.x(), newPos.y()))

    # def updatePositions(self):
    #     if self.dragPoint:
    #         # Update the positions in your main application
    #         index = self.data.index(self.dragPoint.data())
    #         print(f"Index {index}")
    #         new_pos = self.dragPoint.pos()
    #         print(f"New pos {new_pos}")
    #         self.parent().updatePointPosition(index, (new_pos.x(), new_pos.y()))
