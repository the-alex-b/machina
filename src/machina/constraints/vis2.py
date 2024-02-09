import sys
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QListWidget
from PyQt5.QtGui import QCursor, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.Qsci import QsciScintilla, QsciLexerPython
import sys
from PyQt5.QtGui import QFontDatabase

from machina.constraints.drawing import Drawing
from machina.constraints.point import Point
from machina.constraints.line import Line

from jinja2 import Template
import black


class Collection:
    def __init__(self):
        # Collect objects
        self.points = []
        self.lines = []
        self.constraints = []

        # Initialize viewer
        self.window = ClickablePlot(self)
        self.window.show()

        # Initialize code
        self.code = None

    def sync_code(self):
        # Go from generated_code back to python objects and mutate
        if self.code:
            local_vars = {}
            exec(self.code, globals(), local_vars)

            points = local_vars.get("points", None)
            lines = local_vars.get("lines", None)

            self.lines = lines
            self.points = points

    def add_point(self, location):
        self.sync_code()
        self.points.append(Point(location.x(), location.y()))
        self.code = self.to_code()

    def add_line(self, points):
        self.sync_code()
        self.lines.append(
            Line(self.points[points[0]], self.points[points[1]], points[0], points[1])
        )
        self.code = self.to_code()

    def to_code(self):
        # POINTS
        template_string = """points = [{% for pt in points %}Point({{pt.provisional_x}}, {{pt.provisional_y}}),{% endfor %}]"""
        template = Template(template_string)
        points_rendered_code = black.format_str(
            template.render(points=self.points), mode=black.FileMode()
        )

        # LINES
        line_template_string = """lines = [{% for line in lines %}Line(points{{[line.idx1]}}, points{{[line.idx2]}}, {{line.idx1}}, {{line.idx2}}),{% endfor %}]"""
        line_template = Template(line_template_string)
        lines_rendered_code = black.format_str(
            line_template.render(lines=self.lines), mode=black.FileMode()
        )

        return points_rendered_code + lines_rendered_code


class ClickablePlot(QMainWindow):
    def __init__(self, collection):
        super().__init__()

        self.collection = collection

        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create a QScintilla widget for code editing
        self.code_editor = QsciScintilla()
        self.code_editor.setLexer(QsciLexerPython())

        self.code_editor.textChanged.connect(self.update_code_text)

        # Set caret color
        self.code_editor.setCaretForegroundColor(
            QColor("#ff0000")
        )  # Bright red for visibility

        # Set the size of the main window
        self.setGeometry(100, 100, 1000, 600)

        # Create the plot widget and set it as the central widget
        self.plot_widget = pg.PlotWidget(self)

        # Fix viewport
        self.plot_widget.setMenuEnabled(False)
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

        # Drawing lines
        self.line = pg.PlotDataItem(pen=pg.mkPen(width=2, color="g"))
        self.plot.addItem(self.line)

        # Event handler for mouse clicks
        self.plot_widget.scene().sigMouseClicked.connect(self.on_mouse_click)

        # Button to execute code
        self.update_button = QPushButton("Update")
        self.update_button.clicked.connect(self.update_plot)

        # Add widgets to layout
        layout.addWidget(self.plot_widget)
        layout.addWidget(self.code_editor)
        layout.addWidget(self.update_button)

        self.selected_points = []

    def on_mouse_click(self, event):
        if event.button() == 1:  # left mouse button
            pos = event.scenePos()
            position_in_plot = self.plot.vb.mapSceneToView(pos)

            # Find near points
            pts = self.scatter.pointsAt(position_in_plot)
            if len(pts) > 0:
                if len(self.selected_points) == 1:
                    self.selected_points.append(pts[0].index())
                    print("Add line")
                    self.collection.add_line(self.selected_points)
                    self.selected_points = []
                else:
                    self.selected_points.append(pts[0].index())
            else:
                self.selected_points = []
                self.collection.add_point(position_in_plot)

        print("Selected points", self.selected_points)

        self.update_plot()

    def update_code_text(self):
        self.collection.code = self.code_editor.text()

    def update_plot(self):
        code = self.collection.code

        # Update code window
        self.code_editor.setText(code)

        # Read the code generated by the collection and generate points
        local_vars = {}
        exec(code, globals(), local_vars)
        points = local_vars.get("points", None)

        # Draw the points generated by the code
        self.scatter.setData(
            [{"pos": (pt.provisional_x, pt.provisional_y), "data": 1} for pt in points]
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    collection = Collection()
    sys.exit(app.exec_())
