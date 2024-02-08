import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

# Show a picture .
# Left mouse click to draw scatter dots on the picture. Hold down the left mouse button and drag to move the screen.
# Hold down the right mouse button to select a scatter point and drag the scatter point to the release position.
# The current coordinates are displayed when the mouse moves.
# Mouse wheel zooms in or out, screen.


class MovableScatterPlotItem(pg.ScatterPlotItem):
    def __init__(self, *args, imageSizeXy, **kargs):
        super().__init__(*args, **kargs)
        self.target = pg.TargetItem()
        self.target.setParentItem(self)
        self.target.sigPositionChanged.connect(self.targetMoved)
        self.target.hide()
        self.selectedPoint = None
        self.coordinateLabel = pg.TextItem()
        self.coordinateLabel.setParentItem(self.target)
        self.coordinateLabel.setAnchor((0, 1))
        self.imageSizeXy = imageSizeXy

    def boundingRect(self):
        return QtCore.QRectF(0, 0, *self.imageSizeXy)

    def targetMoved(self, target):
        if self.target.isVisible() and self.selectedPoint is not None:
            self.data[["x", "y"]][self.selectedPoint.index()] = tuple(target.pos())
            self.updateSpots()
            self.invalidate()
            label = f"{tuple(map(lambda el: round(el, 2), target.pos()))}"
            self.coordinateLabel.setHtml(
                "<div style='color: red; background: black;'>%s</div>" % label
            )

    def mouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.MouseButton.RightButton:
            points = self.pointsAt(ev.pos())
            if len(points):
                self.target.setPos(ev.pos())
                self.selectedPoint = points[-1]
                self.target.show()
                ev.accept()
        elif ev.button() == QtCore.Qt.MouseButton.LeftButton:
            if self.target.isVisible():
                self.target.hide()
            else:
                newData = np.r_[np.c_[self.getData()], np.atleast_2d(ev.pos())]
                self.setData(*newData.T)
            ev.accept()
        else:
            super().mouseClickEvent(ev)


pg.mkQApp()
plot = pg.PlotWidget()
imageItem = pg.ImageItem(np.random.randint(256, size=(512, 512)))
# plot.addItem(imageItem)
scatter = MovableScatterPlotItem(
    imageSizeXy=imageItem.image.shape[:2][::-1], pen="w", brush="r", size=12
)
# Init 3 random points across the image
randomPoints = np.random.randint(512, size=(2, 3))
scatter.setData(*randomPoints)
plot.addItem(scatter)
plot.show()
pg.exec()
