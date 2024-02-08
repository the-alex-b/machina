import importlib

sp = importlib.import_module("sympy")
import uuid


class Point:
    def __init__(self, x=None, y=None):
        self.provisional_x = x
        self.provisional_y = y

        self.sym_x, self.sym_y = sp.symbols(
            f"{str(uuid.uuid4())[:4]} {str(uuid.uuid4())[:4]}"
        )
        self.point = sp.Point(self.sym_x, self.sym_y)

        self.constraints = []

    def __call__(self):
        """
        Call to get the sympy point
        """
        return self.point

    @property
    def symbols(self):
        return [self.sym_x, self.sym_y]

    def set_x(self, value):
        constraint = sp.Eq(self.point.x, value)
        self.constraints.append(constraint)

    def set_y(self, value):
        constraint = sp.Eq(self.point.y, value)
        self.constraints.append(constraint)

    def sub(self, solution):
        self.point = self.point.subs(solution)

    def set_distance(self, other, distance):
        constraint = sp.Eq(self.point.distance(other()), 5)
        self.constraints.append(constraint)

    @property
    def code(self):
        return f"Point({self.provisional_x},{self.provisional_y})"
