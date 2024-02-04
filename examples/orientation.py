from machina.sketch import Sketch, Plane

sketch = Sketch.rectangle(3, 3)

block1 = sketch.set_plane(Plane.XY).extrude(5)
block2 = sketch.set_plane(Plane.ZY).extrude(7)
block3 = sketch.set_plane(Plane.XZ).extrude(7)

hole_sketch = Sketch.circle(1.2).at((1.5, 1.5))

hole1 = hole_sketch.set_plane(Plane.ZY).extrude(10)
hole2 = hole_sketch.set_plane(Plane.XZ).extrude(10)
hole3 = hole_sketch.set_plane(Plane.XY).extrude(10)

res = block1 + block2 + block3 - hole1 - hole2 - hole3

res.store()
