class Point:
    """
    Class to hold points, should function as an interface between Sketch class and the GUI/code representation.
    """

    def __init__(self, x, y):
        self.xy = (x, y)

    def __repr__(self):
        return self.xy
