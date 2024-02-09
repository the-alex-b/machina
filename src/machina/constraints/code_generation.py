# from jinja2 import Template
from point import Point

# # Jinja2 template for generating Python code
# template_string = """
# points = [
# {% for pt in points %}
#     Point({{pt.provisional_x}}, {{pt.provisional_y}})

# {% endfor %}
# ]
# """

# # Dictionary to dynamically create functions
# functions = {"square_times_two": 2, "square_times_three": 3, "square_times_four": 4}

# # Render the template
# template = Template(template_string)
# rendered_code = template.render(functions=functions)

# print(rendered_code)

# # # Execute the generated code
# exec(rendered_code)

# # # Test the dynamically created functions
# print(square_times_two(5))  # Expected output: 50
# print(square_times_three(5))  # Expected output: 75
# print(square_times_four(5))  # Expected output: 100
a = """
points = [
    Point(4.494030517780757, 4.4160583941605855),
    Point(7.773095830939157, 4.653284671532848),
    Point(4.923067100810829, 7.098540145985403),
    Point(2.195620251548235, 2.3357664233576654),
    Point(2.645087148055928, 5.748175182481753),
    Point(4.974142884504885, 2.3175182481751833),
]

"""

exec(a)

print(points)
