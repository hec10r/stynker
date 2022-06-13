import math
import turtle

# Initialize window
width = 960
height = 960
window = turtle.Screen()
window.setup(width, height)
window.tracer(0)

# Hexagon coordinates
radius = 360
HEXAGON_COORDINATES = [
    (
        math.cos(math.radians(alpha)) * radius,
        math.sin(math.radians(alpha)) * radius
    )
    for alpha in range(0, 420, 60)
]


# Initialize borders of the environment
def draw_environment():
    # Initialize borders
    border = turtle.Turtle()
    border.speed(0)
    border.penup()
    border.pensize(5)
    for i, coord in enumerate(HEXAGON_COORDINATES):
        if i == 2:
            border.pencolor("#2dc937")
        elif i == 5:
            border.pencolor("#cc3232")
        else:
            border.pencolor("black")
            border.pensize()
        border.setposition(*coord)
        border.pendown()
    window.update()
    return border


def create_stynker(color: str, show_route: bool = False) -> turtle.Turtle:
    stk = turtle.Turtle()
    stk.color(color)
    stk.shape("circle")
    if not show_route:
        stk.penup()
    stk.setposition(0, 0)
    return stk


def is_in_origin(stk: turtle.Turtle) -> bool:
    return stk.distance((0, 0)) < 25


environment = draw_environment()

# Initialize stynker
stk_1 = create_stynker("blue")
G = -0.05
velocity = 0
are_two_stynkers = False
while True:
    stk_1.sety(stk_1.ycor() + G)
    if not are_two_stynkers and not is_in_origin(stk_1):
        stk_2 = create_stynker("purple")
        are_two_stynkers = True
    window.update()
    # velocity += G
turtle.done()
