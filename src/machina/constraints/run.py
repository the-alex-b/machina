import importlib

sp = importlib.import_module("sympy")  # pylance fix

from machina.constraints.point import Point
from machina.constraints.drawing import Drawing
from machina.constraints.line import Line


drawing = Drawing()

pt1 = Point()
pt1.set_x(0)
pt1.set_y(0)

pt2 = Point()
pt2.set_x(5)
pt2.set_y(0)

pt2.set_distance(pt1, 5)

line = Line(pt1, pt2)
drawing.add(line)

drawing.solve()
drawing.visualize()

# # pt3 = Point()
# # # pt3.set_x(2)
# # # pt3.set_y(8)

# line1 = Line(pt1, pt2)
# line2 = Line(pt2)
# # line2 = Line(pt2, pt3)
# # line3 = Line(pt3, pt1)

# # line1.set_length(2)
# line2.set_length(6)

# line1.set_perpendicular(line2)


# drawing.add(line1)
# drawing.add(line2)
# # drawing.add(line3)

# print(drawing.all_symbols)
# print(drawing.all_constraints)
# print("----- \n")
# print(f" {len(drawing.all_constraints)} constraints")
# print(f" {len(drawing.all_symbols)} symbols")

# drawing.solve()
# points = drawing.points

# print(points)
# drawing.visualize()
