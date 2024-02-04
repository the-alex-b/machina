from __future__ import annotations
import numpy as np
import trimesh
from manifold3d import Manifold, CrossSection, Mesh
from typing import Self, Optional
import io
import base64
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from machina import Sketch


# from manispline.sketch import Sketch


# TODO: implement https://github.com/elalish/manifold/blob/master/bindings/python/examples/all_apis.py
class Object:
    def __init__(
        self,
        cross_section: Optional[CrossSection] = None,
        manifold: Optional[Manifold] = None,
    ) -> None:
        self.cross_section: CrossSection = cross_section
        self.manifold: Manifold = manifold

    @classmethod
    def from_manifold(cls, manifold: Manifold) -> Self:
        return cls(manifold=manifold)

    @classmethod
    def from_stp(
        cls,
        file_location: str,
        max_mesh_length: float = 1,
        min_mesh_length: float = 0.1,
    ) -> Self:
        mesh = trimesh.Trimesh(
            **trimesh.interfaces.gmsh.load_gmsh(
                file_location,
                gmsh_args=[
                    ("Mesh.CharacteristicLengthMax", max_mesh_length),
                    ("Mesh.CharacteristicLengthMin", min_mesh_length),
                ],
            )
        )
        manifold = Manifold(
            mesh=Mesh(
                vert_properties=np.asarray(mesh.vertices, dtype="float32"),
                tri_verts=np.asarray(mesh.faces, dtype="int32"),
            )
        )
        return cls(manifold=manifold)

    def store(self, file_path: str = "object.stl", refinement_factor: int = 2):
        self.manifold = self.manifold.refine(refinement_factor)
        mesh = self.manifold.to_mesh()
        out_mesh = trimesh.Trimesh(
            vertices=mesh.vert_properties, faces=mesh.tri_verts
        )  # TODO: can we remove trimesh dependecy here?
        out_mesh.export(file_path)

    @property
    def base64(self):
        mesh = self.manifold.to_mesh()
        out_mesh = trimesh.Trimesh(vertices=mesh.vert_properties, faces=mesh.tri_verts)

        # Create a BytesIO object to act as a file in memory
        buffer = io.BytesIO()

        # Export the mesh into the buffer
        out_mesh.export(file_obj=buffer, file_type="stl")

        # It's important to seek back to the start of the BytesIO object
        buffer.seek(0)

        return base64.b64encode(buffer.getvalue()).decode("utf-8")

    # Set location
    def at(self, location: tuple[float, float, float]):
        return self.from_manifold(self.manifold.translate(location))

    def __matmul__(self, location: tuple[float, float, float]):
        return self.at(location)

    def translate(self, translation) -> Self:
        return self.from_manifold(self.manifold.translate(translation))

    def transform(self, transformation: np.ndarray) -> Self:
        return self.from_manifold(self.manifold.transform(transformation))

    # Boolean operations
    def difference(self, other: Manifold) -> Self:
        return self.from_manifold(self.manifold - other.manifold)

    def __sub__(self, other):
        return self.difference(other)

    def union(self, other: Manifold) -> Self:
        return self.from_manifold(self.manifold + other.manifold)

    def __add__(self, other):
        return self.union(other)

    def intersection(self, other: Manifold) -> Self:
        return self.from_manifold(self.manifold ^ other.manifold)

    def __xor__(self, other):
        return self.intersection(other)

    def slice(self, height: float) -> Sketch:
        from machina import (
            Sketch,
        )  # load sketch here to prevent circular import TODO: make better

        cross_section = self.manifold.slice(height)
        return Sketch.from_cross_section(cross_section)

    def smooth(self, edges, smoothing_factor):
        smoothed_manifold = Manifold.smooth(
            self.manifold.to_mesh(), edges, smoothing_factor
        )
        return self.from_manifold(smoothed_manifold)

    @property
    def number_of_triangles(self):
        return self.manifold.num_tri()
