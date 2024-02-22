import sys
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QListWidget
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt


from machina.constraints.drawing import Drawing
from machina.constraints.point import Point
from machina.constraints.line import Line

# from machina.constraints.draggable import DraggableScatter


class CustomPlotWidget(
    pg.PlotWidget,
):
    def __init__(self, plot, *args, **kwargs):
        self.plot = plot

        super(CustomPlotWidget, self).__init__(*args, **kwargs)

    def mouseMoveEvent(self, event):  # Allows cursor change when hovering over point
        # Change the cursor when the mouse moves
        self.setCursor(QCursor(Qt.CrossCursor))

        pos_in_plot = self.plot.plot.vb.mapSceneToView(event.pos())
        if len(self.plot.scatter.pointsAt(pos_in_plot)) > 0:
            self.setCursor(
                QCursor(Qt.PointingHandCursor)
            )  # Change cursor to pointing hand

        # Send event to parent
        super(CustomPlotWidget, self).mouseMoveEvent(event)


class ClickablePlot(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the size of the main window
        self.setGeometry(100, 100, 1000, 600)

        # Create the plot widget and set it as the central widget
        self.plot_widget = CustomPlotWidget(self)
        self.setCentralWidget(self.plot_widget)
        self.plot_widget.setMenuEnabled(False)

        # Fix viewport
        self.plot_widget.setMouseEnabled(x=False, y=False)
        self.plot_widget.setXRange(0, 10, padding=0)
        self.plot_widget.setYRange(0, 10, padding=0)

        # Set up the plot
        self.plot = self.plot_widget.getPlotItem()
        self.plot.setTitle("Machina")

        self.scatter = pg.ScatterPlotItem(
            size=20, pen=pg.mkPen(width=5, color="r"), symbol="o"
        )

        self.scatter.setParent(self)  # Set the parent to the main window
        self.plot.addItem(self.scatter)

        self.selected_point_scatter = pg.ScatterPlotItem(
            size=20, pen=pg.mkPen(width=7, color="b"), symbol="o"
        )

        self.selected_point_scatter.setParent(self)  # Set the parent to the main window
        self.plot.addItem(self.selected_point_scatter)

        # Event handler for mouse clicks
        self.plot_widget.scene().sigMouseClicked.connect(self.on_mouse_click)

        # Store the points and the line
        self.points = []
        self.line = pg.PlotDataItem(pen=pg.mkPen(width=2, color="g"))
        self.plot.addItem(self.line)

        # Create and position the clear button
        self.clear_button = QPushButton("Clear", self)
        self.clear_button.setGeometry(800, 10, 60, 30)
        self.clear_button.clicked.connect(self.clear_drawing)

        #  Create and position the list widget
        self.list_widget = QListWidget(self)
        self.list_widget.setToolTip("Points")
        self.list_widget.setGeometry(
            800, 50, 180, 500
        )  # Adjust size and position as needed

        self.selected_point = None

    def on_mouse_click(self, event):
        self.selected_point = None
        # LEFT MOUSE BUTTON -> create point
        if event.button() == 1:  # left mouse button
            # Convert the clicked position to plot coordinates
            pos = event.scenePos()
            pos_in_plot = self.plot.vb.mapSceneToView(pos)

            pts = self.scatter.pointsAt(pos_in_plot)

            # no point
            if len(pts) == 0:
                # Add point and update the plot
                self.points.append(Point(pos_in_plot.x(), pos_in_plot.y()))

            else:
                self.selected_point = pts[0].index()
                print("selected point at index", self.selected_point)

            self.update_plot()

        # RIGHT MOUSE BUTTON -> Remove point
        if event.button() == 2:
            pos_in_plot = self.plot.vb.mapSceneToView(event.scenePos())
            pts = self.scatter.pointsAt(pos_in_plot)

            if len(pts) > 0:
                self.points.pop(pts[0].index())
            self.update_plot()

        # DRAG -> move point

    def update_plot(self):
        # Clear selected point
        print("IN UPDATE", self.selected_point)
        self.selected_point_scatter.setData()
        # Draw points
        self.scatter.setData(
            [
                {"pos": (pt.provisional_x, pt.provisional_y), "data": 1}
                for pt in self.points
            ]
        )

        if self.selected_point is not None:
            print("Point has been selected")
            selected_pt = self.points[self.selected_point]

            # Draw selected point
            self.selected_point_scatter.setData(
                [
                    {
                        "pos": (selected_pt.provisional_x, selected_pt.provisional_y),
                        "data": 1,
                    }
                ]
            )

        # Draw lines
        if len(self.points) > 1:
            x_coords = [pt.provisional_x for pt in self.points]
            y_coords = [pt.provisional_y for pt in self.points]
            self.line.setData(x_coords, y_coords)
        else:
            self.line.setData()

        self.update_list_widget()

    def update_list_widget(self):
        # Update the list widget with the current points
        self.list_widget.clear()
        for pt in self.points:
            self.list_widget.addItem(
                f"({pt.provisional_x:.2f}, {pt.provisional_y:.2f})"
            )

    def clear_drawing(self):
        # Clear the points and update the plot
        self.points = []

        self.controller.code = self.controller.to_code

        self.update_plot()

    def updatePointPosition(self, index, newPos):
        if 0 <= index < len(self.points):
            self.points[index].provisional_x, self.points[index].provisional_y = newPos
            self.update_plot()

    @property  # TODO, make this better
    def code_representation(self):
        return f"points = {[pt.code for pt in self.points]}"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = ClickablePlot()
    main.show()
    sys.exit(app.exec_())
