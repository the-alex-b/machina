import numpy as np


class Line:
    def __init__(self, control_points, weights, knot_vector, degree):
        self.control_points = control_points
        self.weights = weights
        self.knot_vector = knot_vector
        self.degree = degree

    def evaluate_curve(self, num_points=100):
        """Evaluate a NURBS curve at a given set of parameters."""
        n = len(self.control_points)
        domain = np.linspace(
            self.knot_vector[self.degree], self.knot_vector[n], num_points
        )
        curve = np.zeros((num_points, 2))

        for i, xi in enumerate(domain):
            numerator = np.zeros(2)
            denominator = 0
            for j in range(n):
                b = self.cox_de_boor(xi, j, self.degree)
                wb = self.weights[j] * b
                numerator += wb * np.array(self.control_points[j])
                denominator += wb
            curve[i] = numerator / denominator if denominator != 0 else numerator

        # Ensuring the curve starts at the first control point and ends at the last
        curve[0] = self.control_points[0]
        curve[-1] = self.control_points[-1]

        return curve

    def cox_de_boor(self, x, k, degree):
        """Calculation of the Cox-De Boor basis functions."""
        if degree == 0:
            return 1.0 if self.knot_vector[k] <= x < self.knot_vector[k + 1] else 0.0
        else:
            d1 = self.knot_vector[k + self.degree] - self.knot_vector[k]
            d2 = self.knot_vector[k + self.degree + 1] - self.knot_vector[k + 1]
            e1 = (
                0
                if d1 == 0
                else ((x - self.knot_vector[k]) / d1)
                * self.cox_de_boor(x, k, degree - 1)
            )
            e2 = (
                0
                if d2 == 0
                else ((self.knot_vector[k + degree + 1] - x) / d2)
                * self.cox_de_boor(x, k + 1, degree - 1)
            )
            return e1 + e2


class StraightLine(Line):
    def __init__(self, control_points):
        self.control_points = control_points
        self.degree = 1
        self.weights = [1, 1]
        self.knot_vector = [0, 0, 1, 1]


class RoundedLine(Line):
    def __init__(self, control_points):
        self.control_points = control_points
        self.degree = 2
        self.weights = [1, 2, 1]
        self.knot_vector = [0, 0, 0, 1, 1, 1]
