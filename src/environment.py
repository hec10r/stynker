import math
import turtle
from collections import deque
from typing import List, Tuple


class Environment:
    def __init__(
        self,
        border_coordinates: List[Tuple[float, float]],
        winning_segment: int,
        losing_segment: int,
    ):
        # Initialize window
        width = 960
        height = 960
        self.window = turtle.Screen()
        self.window.setup(width, height)
        self.window.tracer(0)

        # Information about the environment
        self.border_coordinates = border_coordinates
        self.winning_segment = winning_segment
        self.losing_segment = losing_segment

        rotated_coordinates = deque(self.border_coordinates)
        rotated_coordinates.rotate(-1)

        # Lists to store parameters of general form equations
        a_list = list()
        b_list = list()
        c_list = list()

        for p1, p2 in zip(self.border_coordinates, list(rotated_coordinates)):
            a, b, c = self.get_general_form(p1, p2)
            a_list.append(a)
            b_list.append(b)
            c_list.append(c)

        # For each border of the environment, we are getting the
        # a, b, c parameters who satisfy ax + by + c = 0
        self.border_parameters = list(zip(a_list[:-1], b_list[:-1], c_list[:-1]))

    def draw_borders(self):
        """Draw the borders of the environment"""
        border = turtle.Turtle()
        border.speed(0)
        border.penup()
        border.pensize(5)
        # The coordinates of the environment must be `closed`: last one equals to first
        for i, coord in enumerate(self.border_coordinates):
            if i == self.winning_segment:
                border.pencolor("#2dc937")
            elif i == self.losing_segment:
                border.pencolor("#cc3232")
            else:
                border.pencolor("black")
                border.pensize()
            border.setposition(*coord)
            border.pendown()
        self.window.update()
        return border

    @staticmethod
    def calculate_velocity_vector(velocity_vector, a, b) -> Tuple[float, float]:
        """
        Given a velocity vector, and the constants that describe a 'wall' in its
        general form (ax + by + c = 0), returns the new velocity vector after
        bouncing with the wall

        Args:
            velocity_vector: velocity vector before the collision
            a: 'a' from the equation of the wall: ax + by + c = 0
            b: 'b' from the equation of the wall: ax + by + c = 0

        Returns:
            The new velocity vector after bouncing with the wall described
            by the equation ax + by + c = 0
        """
        # Notice that (a, b) is orthogonal to the wall represented
        # by the equation ax + by + c = 0
        norm = Environment.get_norm((a, b))
        normal_vector = (a / norm, b / norm)

        dot_product = normal_vector[0] * velocity_vector[0] + normal_vector[1] * velocity_vector[1]
        new_velocity_vector = (
            velocity_vector[0] - 2 * dot_product * normal_vector[0],
            velocity_vector[1] - 2 * dot_product * normal_vector[1]
        )
        return new_velocity_vector

    @staticmethod
    def distance_to_segment(x0, y0, p1, p2):
        """
        Given a point and a segment defined by the points p1 and p2,
        get the shortest distance to the segment
        Args:
            x0: x coordinate of the point
            y0: y coordinate of the point
            p1: first point that defines the segment
            p2: second point that defines the segment
        Returns:
            Shortest distance between the point and the segment
        """
        a, b, c = Environment.get_general_form(p1, p2)
        d_line = Environment.distance_to_line(x0, y0, a, b, c)
        d1 = Environment.distance_to_point(x0, y0, *p1)
        d2 = Environment.distance_to_point(x0, y0, *p2)
        d_segment = min(d1, d2)
        x, y = Environment.projection(x0, y0, a, b, c)
        is_between_x = p1[0] <= x <= p2[0] or p2[0] <= x <= p1[0]
        is_between_y = p1[1] <= y <= p2[1] or p2[1] <= y <= p1[1]

        if is_between_x and is_between_y:
            return d_line
        return d_segment

    @staticmethod
    def get_general_form(p1: Tuple[float, float], p2: Tuple[float, float]) -> Tuple[float, float, float]:
        """
        Given two points, return the general form of the line defined
        by them
        Args:
            p1: coordinates of the first point
            p2: coordinates of the second point
        Returns:
            a, b, c values such that ax + by + c = 0 represents the line
            defined by the two points
        """
        x1, y1 = p1
        x2, y2 = p2
        a = y1 - y2
        b = x2 - x1
        c = -a * x1 - b * y1
        return a, b, c

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
        return abs(Environment._distance_to_line(x0, y0, a, b, c))

    @staticmethod
    def _distance_to_line(x0, y0, a, b, c) -> float:
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
        distance = (a * x0 + b * y0 + c) / Environment.get_norm((a, b))
        return distance

    @staticmethod
    def distance_to_point(x0, y0, x1, y1) -> float:
        """
        Given a pair of points, get the distance between them
        Args:
            x0: x coordinate of the first point
            y0: y coordinate of the first point
            x1: x coordinate of the second point
            y1: y coordinate of the second point
        Returns:
            Distance from point (x0, y0) to point (x1, y1)
        """
        return Environment.get_norm(((x0-x1), (y0-y1)))

    @staticmethod
    def projection(x0, y0, a, b, c) -> Tuple[float, float]:
        """
        Get the projection of the point (x0, y0) over the line described
        by ax + by + c = 0
        Args:
            x0: x coordinate of the point
            y0: y coordinate of the point
            a: `a` parameter from the general form
            b: `b` parameter from the general form
            c: `c` parameter from the general form
        Returns:
            Point projected onto the line
        """
        d = Environment._distance_to_line(x0, y0, a, b, c)
        norm = Environment.get_norm((a, b))
        x = x0 - a*d/norm
        y = y0 - b*d/norm
        return x, y

    @staticmethod
    def reflect_point_over_line(x0, y0, a, b, c) -> Tuple[float, float]:
        """
        Given a point and a line represented in a general form (ax + by + c = 0),
        get the reflection of the point over the line
        Args:
            x0: x coordinate of the point
            y0: y coordinate of the point
            a: `a` parameter from the general form
            b: `b` parameter from the general form
            c: `c` parameter from the general form
        Returns:
            Position of the point reflected over the line
        """
        norm = Environment.get_norm((a, b))
        x = x0 * (b ** 2 - a ** 2) - 2 * a * (b * y0 + c)
        y = y0 * (a ** 2 - b ** 2) - 2 * b * (a * x0 + c)
        return x / norm, y / norm

    @staticmethod
    def get_norm(vector: Tuple[float, float]) -> float:
        """
        Get the euclidean norm of a (x, y) vector
        Args:
            vector: (x, y) pair
        Returns:
            Euclidean norm of the (x, y) vector
        """
        x, y = vector
        return (x * x + y * y) ** 0.5
