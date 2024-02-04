from machina.line import Line
from machina.object import Object
import numpy as np
from typing import Sequence, List
from manifold3d import Manifold, CrossSection, Mesh, set_circular_segments
from typing import Self, Optional
from machina.point import Point
from enum import Enum, auto
from machina.utils import get_transformation_to_xz, get_transformation_to_zy
from functools import wraps

# Make circles better
set_circular_segments(128)
EXTRUDE_DIVISIONS = 8


# TODO: make this beter and more concise?
def preserve_plane_orientation(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Call the original method
        result = method(self, *args, **kwargs)
        # If the result is a Sketch instance, update its plane orientation
        if isinstance(result, Sketch):
            result.plane = self.plane
        return result

    return wrapper


class Plane(Enum):
    XY = auto()
    XZ = auto()
    ZY = auto()


class Sketch:
    def __init__(self, cross_section: CrossSection, plane: Plane = Plane.XY) -> None:
        self.cross_section = cross_section

        self.plane = plane

    @preserve_plane_orientation
    def transform(self, transformation: np.ndarray) -> Self:
        return self.from_cross_section(self.cross_section.transform(transformation))

    @preserve_plane_orientation
    def translate(self, translation: tuple[float, float]) -> Self:
        return self.from_cross_section(self.cross_section.translate(translation))

    # Set location
    def at(self, location: tuple[float, float]):
        # TODO: make sure that this takes global location into account.. this is just a wrapper on translate right now
        return self.from_cross_section(self.cross_section.translate(location))

    def __matmul__(self, location: tuple[float, float]):
        return self.at(location)

    # Initialization
    @classmethod
    def circle(cls, radius: float = 1) -> Self:
        return cls(cross_section=CrossSection.circle(radius))

    @classmethod
    def rectangle(cls, w: float = 1, h: float = 1) -> Self:
        return cls(cross_section=CrossSection.square((w, h)))

    @classmethod
    def from_lines(cls, lines: Sequence[Line]) -> Self:
        coords = []
        for line in lines:
            coords.extend(line.evaluate_curve())

        return cls(cross_section=CrossSection([coords]))

    @classmethod
    def from_points(cls, points: list[Point]) -> Self:
        return cls(cross_section=CrossSection([[point.xy for point in points]]))

    @classmethod
    def from_cross_section(cls, cross_section: CrossSection):
        return cls(cross_section)

    # Cross Section -> Manifold
    def extrude(self, n: float, twist_degrees: float = 0) -> Object:
        manifold = self.cross_section.extrude(
            n, n_divisions=EXTRUDE_DIVISIONS, twist_degrees=twist_degrees
        )
        if self.plane == Plane.XY:
            pass
        if self.plane == Plane.ZY:
            manifold = manifold.transform(get_transformation_to_zy())
        if self.plane == Plane.XZ:
            manifold = manifold.transform(get_transformation_to_xz())
        return Object.from_manifold(manifold)

    def revolve(self) -> Object:
        manifold = self.cross_section.revolve()
        return Object.from_manifold(manifold)

    # Boolean operations
    def difference(self, other: Self) -> Self:
        return self.from_cross_section(self.cross_section - other.cross_section)

    def __sub__(self, other):
        return self.difference(other)

    def union(self, other: Self) -> Self:
        return self.from_cross_section(self.cross_section + other.cross_section)

    def __add__(self, other):
        return self.union(other)

    def intersection(self, other: Self) -> Self:
        return self.from_cross_section(self.cross_section ^ other.cross_section)

    def __xor__(self, other):
        return self.intersection(other)

    @preserve_plane_orientation
    def set_plane(self, plane: Plane) -> Self:
        self.plane = plane
        return self.from_cross_section(self.cross_section)

    # @preserve_plane_orientation
    # def translate(self, translation: tuple[float, float]) -> Self:
    #     return self.from_cross_section(self.cross_section.translate(translation))
