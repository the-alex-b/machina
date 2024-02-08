import importlib

sp = importlib.import_module("sympy")
import matplotlib.pyplot as plt

from machina.line import StraightLine
import numpy as np


class Drawing:
    def __init__(self):
        self.objects: list = []

        self.solution = None

    def add(self, object):
        self.objects.append(object)

    def solve(self):
        solutions = sp.solve(
            self.all_constraints, self.all_symbols, dict=True
        )  # for now get first solution
        if len(solutions) == 0:
            print("Over constrained, no solution possible")
            return

        print(f"{len(solutions)} solution(s) found substituting the first")
        self.solution = solutions[0]
        for obj in self.objects:
            obj.sub(
                solutions[0]
            )  # TODO: make sure we also sub in the point descriptions, these are now unsubstituted

    def visualize(self):
        if self.solution == None:
            print("No solution found so can't draw")
            return

        # Create a plot
        fig, ax = plt.subplots()

        # Function to plot a line TODO: draw more objects
        def plot_line(ax, line, color="blue", label=None):
            p1, p2 = line.points
            ax.plot([p1.x, p2.x], [p1.y, p2.y], color=color, label=label)

        # Plot each line in the array
        for i, line in enumerate(self.objects):
            plot_line(ax, line(), label=f"Line {i+1}")

        # Set equal aspect ratio
        ax.set_aspect("equal")

        # Show plot
        plt.show()

    @property
    def all_constraints(self):
        constraints = []
        _ = [constraints.extend(x.constraints) for x in self.objects]

        return list(set(constraints))  # TODO make better

    @property
    def all_symbols(self):
        symbols = []
        _ = [symbols.extend(x.symbols) for x in self.objects]

        return list(set(symbols))  # TODO make better

    @property
    def points(self):
        pts = []
        for obj in self.objects:
            for point in obj().points:
                pts.append((point.x, point.y))

        return pts

    @property
    def lines(self):
        lines = []
        for obj in self.objects:
            pt1 = (obj().points[0].x, obj().points[0].y)
            pt2 = (obj().points[1].x, obj().points[1].y)
            lines.append(StraightLine(np.array([pt1, pt2])))  #  TODO: Is this right?
        return lines

    # @property
    # def polygon(self):
    #     all_points = []
    #     for line in self.objects:
    #         all_points.extend(line.points)
    #     # all_points = [line.points for line in self.objects]
    #     polygon = sp.Polygon([pt().subs(self.solution) for pt in all_points])
    #     print(polygon)
