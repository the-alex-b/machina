import importlib

sp = importlib.import_module("sympy")


from machina.constraints.point import Point


class Line:
    def __init__(self, point1=None, point2=None):
        if point1 == None:
            point1 = Point()

        if point2 == None:
            point2 = Point()

        self.points = [point1, point2]
        self.line = sp.Line(point1(), point2())

        self.line_constraints = []

    def __call__(self):
        return self.line

    @property
    def constraints(self):
        for point in self.points:
            self.line_constraints.extend(point.constraints)
        return self.line_constraints

    @property
    def symbols(self):
        symbols = []
        for point in self.points:
            symbols.extend(point.symbols)
        return symbols

    # -- Constraints --
    def set_length(self, length):
        constraint = sp.Eq(self.line.points[0].distance(self.line.points[1]), length)
        self.line_constraints.append(constraint)

    def set_perpendicular(self, other_line):
        constraint = sp.Eq(self.line.direction.dot(other_line().direction), 0)
        self.line_constraints.append(constraint)

    def sub(self, solution):
        self.line = self.line.subs(solution)
