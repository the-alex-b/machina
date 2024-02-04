from machina.sketch import Sketch


rectangle = Sketch.rectangle(10, 10)
rectangle = rectangle.extrude(0.1)


hole = Sketch.circle(0.3)

holes = [hole.at((i + 1, j + 1)).extrude(3) for i in range(9) for j in range(9)]

for hole in holes:
    rectangle = rectangle - hole

rectangle.store()
