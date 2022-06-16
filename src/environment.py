import math
import turtle
from collections import deque
from .stynker import Stynker


class Environment:
    def __init__(
        self,
        stk1: Stynker,
        stk2: Stynker = None,
        radius: int = 360,
        **kwargs
    ):
        # Initialize window
        width = 960
        height = 960
        self.window = turtle.Screen()
        self.window.setup(width, height)
        self.window.tracer(0)

        # Initialize constants
        self.gravity = -0.05
        self.velocity = 0

        # Hexagon coordinates
        self.hexagon_coordinates = [
            (
                math.cos(math.radians(alpha)) * radius,
                math.sin(math.radians(alpha)) * radius
            )
            for alpha in range(0, 420, 60)
        ]

    def draw_borders(self):
        """Draw the borders of the environment"""
        # Initialize borders
        border = turtle.Turtle()
        border.speed(0)
        border.penup()
        border.pensize(5)
        for i, coord in enumerate(self.hexagon_coordinates):
            if i == 2:
                border.pencolor("#2dc937")
            elif i == 5:
                border.pencolor("#cc3232")
            else:
                border.pencolor("black")
                border.pensize()
            border.setposition(*coord)
            border.pendown()
        self.window.update()
        return border

    def touch_border(self, stk: turtle.Turtle) -> bool:
        # TODO:
        # Rotate coordinates
        rotated_coordinates = deque(self.hexagon_coordinates)
        rotated_coordinates.rotate(1)
        print(rotated_coordinates)
        for p1, p2 in zip(self.hexagon_coordinates, rotated_coordinates):
            p0 = stk.pos()
            # if height_triangle(p0, p1, p2) < 20:
            #     return True
        return False

    @staticmethod
    def is_in_origin(stk: turtle.Turtle) -> bool:
        return stk.distance((0, 0)) < 25
