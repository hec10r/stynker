import math
import turtle
from collections import deque


class Environment:
    def __init__(
        self,
        radius: int = 360,
        **kwargs
    ):
        # Initialize window
        width = 960
        height = 960
        self.window = turtle.Screen()
        self.window.setup(width, height)
        self.window.tracer(0)

        # Hexagon coordinates
        self.hexagon_coordinates = [
            (
                math.cos(math.radians(alpha)) * radius,
                math.sin(math.radians(alpha)) * radius
            )
            for alpha in range(0, 420, 60)
        ]

        rotated_coordinates = deque(self.hexagon_coordinates)
        rotated_coordinates.rotate(-1)

        # Lists to store parameters of general form equations
        a_list = list()
        b_list = list()
        c_list = list()

        for p1, p2 in zip(self.hexagon_coordinates[:6], list(rotated_coordinates)[:6]):
            # Slope of the line
            a = (p2[1] - p1[1]) / (p2[0] - p1[0])
            # -1 constant
            b = -1
            # Solving for c
            c = p1[1] - a * p1[0]
            a_list.append(a)
            b_list.append(b)
            c_list.append(c)

        # For each side of the hexagon, we are getting the
        # a, b, c parameters who satisfy ax + by + c = 0
        self.border_parameters = list(zip(a_list[:6], b_list[:6], c_list[:6]))

    def draw_borders(self):
        """Draw the borders of the environment"""
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

    @staticmethod
    def distance_to_line(x0, y0, a, b, c) -> float:
        """
        Given a point and a line represented in a general form (ax + by + c = 0),
        get the closest distance from the point to the line
        Args:
            x0: x coordinate of the point
            y0: y coordinate of the point
            a: `a` parameter from the general form
            b: `b` parameter from the general form
            c: `c` parameter from the general form
        Returns:
            Distance from the point (x0, y0) to the line represented by the equation
            ax + by + c = 0
        """
        distance = abs((a * x0 + b * y0 + c)) / (math.sqrt(a * a + b * b))
        return distance

    def touch_border(self, stk: turtle.Turtle) -> bool:
        """
        Return whether the Stynker is touching the borders of the environment.
        Notice that a turtle is a point, not a circle.
        Args:
            stk: Turtle that represents the Stynker
        Returns:
            True if the distance between the Stynker and any of the
            borders is less than a given threshold. False otherwise
        """
        x0, y0 = stk.position()
        for a, b, c in self.border_parameters:
            distance = self.distance_to_line(x0, y0, a, b, c)
            if distance < 10:
                return True
        return False

    @staticmethod
    def is_in_origin(stk: turtle.Turtle) -> bool:
        """
        Return whether the turtle is in (0, 0)
        Args:
            stk: Turtle that represents the Stynker
        Returns:
            True if the distance between the Stynker and the origin
            is less than a given threshold. False otherwise
        """
        return stk.distance((0, 0)) < 10
