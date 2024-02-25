# Machina

Machina is CAD software with a code interface. It stems from frustration with using expensive and complex software tools to create and design simple objects to print on my 3D printer. Machina will be an opensource python library that will allow scriptable parametric design in the spirit of existing solutions like CadQuery, OpenSCAD, FreeCAD, etc. Defining objects in code will unlock automation (build pipelines), LLM interfacing and easy diff-inspection. Crucial to cad software is the geometric kernel, Machina is built upon the excellent [Manifold](https://github.com/elalish/manifold) library that is [100-1000x](https://elalish.blogspot.com/2022/03/manifold-performance.html) faster than other open source kernels.

## Demo
![Demo image](docs/images/machina.png)
[Try it here](https://machina.autnms.com/)

## Installation
``` bash
pip install git+https://github.com/the-alex-b/machina
```
## Example

``` python
from machina.sketch import Sketch


rectangle = Sketch.rectangle(10, 10)
rectangle = rectangle.extrude(0.1)


hole = Sketch.circle(0.3)

holes = [hole.at((i + 1, j + 1)).extrude(3) for i in range(9) for j in range(9)]

for hole in holes:
    rectangle = rectangle - hole

rectangle.store()
```


## Status
For now Machina is very alpha and very 'work in progress'.