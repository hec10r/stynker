from __future__ import annotations
import turtle
from collections import deque
from typing import Union

from utils import get_environment_inputs


class Environment:
    def __init__(
        self,
        border_coordinates: list[tuple[float, float]],
        winning_segment: int,
        losing_segment: int,
        name: str = None,
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
        self.name = name

        rotated_coordinates = deque(self.border_coordinates)
        rotated_coordinates.rotate(-1)

        # Since the coordinates are circular, it is necessary to
        # ignore the last segment
        self.segments = list(zip(self.border_coordinates, list(rotated_coordinates)))[:-1]

        # Lists to store parameters of general form equations
        a_list = list()
        b_list = list()
        c_list = list()

        for p1, p2 in self.segments:
            a, b, c = self.get_general_form(p1, p2)
            a_list.append(a)
            b_list.append(b)
            c_list.append(c)

        # For each border of the environment, we are getting the
        # a, b, c parameters who satisfy ax + by + c = 0
        self.border_parameters = list(zip(a_list, b_list, c_list))

    def draw_borders(self) -> turtle.Turtle:
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
    def calculate_velocity_vector(
        velocity_vector: tuple[float, float],
        a: float,
        b: float
    ) -> tuple[float, float]:
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
    def distance_to_segment(
        x0: float,
        y0: float,
        p1: tuple[float, float],
        p2: tuple[float, float]
    ) -> float:
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
    def get_general_form(
        p1: tuple[float, float],
        p2: tuple[float, float]
    ) -> tuple[float, float, float]:
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
    def distance_to_line(
        x0: float,
        y0: float,
        a: float,
        b: float,
        c: float
    ) -> float:
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
    def _distance_to_line(
        x0: float,
        y0: float,
        a: float,
        b: float,
        c: float
    ) -> float:
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
    def distance_to_point(
        x0: float,
        y0: float,
        x1: float,
        y1: float
    ) -> float:
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
    def projection(
        x0: float,
        y0: float,
        a: float,
        b: float,
        c: float
    ) -> tuple[float, float]:
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
    def reflect_point_over_line(
        x0: float,
        y0: float,
        a: float,
        b: float,
        c: float
    ) -> tuple[float, float]:
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
        z = a*a + b*b
        x = x0 * (b ** 2 - a ** 2) - 2 * a * (b * y0 + c)
        y = y0 * (a ** 2 - b ** 2) - 2 * b * (a * x0 + c)
        return x / z, y / z

    @staticmethod
    def get_norm(vector: tuple[float, float]) -> float:
        """
        Get the euclidean norm of a (x, y) vector
        Args:
            vector: (x, y) pair
        Returns:
            Euclidean norm of the (x, y) vector
        """
        x, y = vector
        return (x * x + y * y) ** 0.5

    @staticmethod
    def are_ccw(
        p1: tuple[float, float],
        p2: tuple[float, float],
        p3: tuple[float, float]
    ) -> bool:
        """
        Given three points: p1, p2, and p3, determine
        if they are listed in counterclockwise order
        Args:
            p1: first point
            p2: second point
            p3: third point

        Returns:
            True if they are listed in counterclockwise order,
            False otherwise
        """
        p1x, p1y = p1
        p2x, p2y = p2
        p3x, p3y = p3
        return (p3y-p1y) * (p2x-p1x) > (p2y-p1y)*(p3x-p1x)

    @staticmethod
    def intersect(
        p1: tuple[float, float],
        p2: tuple[float, float],
        q1: tuple[float, float],
        q2: tuple[float, float],
    ) -> bool:
        """
        Given two segments P and Q, defined by two points each one:
        {p1, p2}, and {q1, q2} respectively, return whether they
        intersect.

        It uses the logic described here:
        https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/

        Args:
            p1: first point of segment P
            p2: second point of segment P
            q1: first point of segment Q
            q2: second point of segment Q

        Returns:
            True if they intersect, False otherwise
        """
        cond1 = Environment.are_ccw(p1, q1, q2) != Environment.are_ccw(p2, q1, q2)
        cond2 = Environment.are_ccw(p1, p2, q1) != Environment.are_ccw(p1, p2, q2)
        return cond1 and cond2

    @staticmethod
    def get_segment_intersection(
        p1: tuple[float, float],
        p2: tuple[float, float],
        q1: tuple[float, float],
        q2: tuple[float, float],
    ) -> Union[tuple[float, float], None]:
        """
        Given two segments P and Q, defined by two points each one:
        {p1, p2}, and {q1, q2} respectively, return the point where
        they intersect
        Args:
            p1: first point of segment P
            p2: second point of segment P
            q1: first point of segment Q
            q2: second point of segment Q

        Returns:
            The point where both segments intersect, if they don't,
            return None
        """
        # TODO: is this really necessary?
        pass

    @classmethod
    def get_environment(cls, env_name: str) -> Environment:
        """
        Get the environment to use
        Args:
            env_name: name of the environment to get
        Returns:
            Instance of the Environment identified by `env_name`
        """
        parameters = get_environment_inputs(env_name=env_name)
        return cls(**parameters)
