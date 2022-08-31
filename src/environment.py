from __future__ import annotations
import turtle
from typing import Any

from utils import get_environment_inputs


class Environment:
    def __init__(
        self,
        border_coordinates: list[tuple[float, float]],
        winning_segment: tuple[tuple[float, float], tuple[float, float]],
        losing_segment: tuple[tuple[float, float], tuple[float, float]],
        inner_segments: tuple[tuple[float, float], ...],
        winning_inner_segment: tuple[tuple[float, float], tuple[float, float]],
        losing_inner_segment: tuple[tuple[float, float], tuple[float, float]],
        name: str = None,
    ):
        """
        Initialize an environment with the coordinates specified
        in `border_coordinates` variable.

        The format of the coordinates must be a list of points,
        where each point represents a 'corner' of the environment.

        The easiest way to think about the border, is to draw it
        mentally without lifting the pencil.

        Other important concept is a 'segment'. A segment is
        basically the line that connects to consecutive `corners`.
        If when drawing the environment, the pen passes over
        the same segment more than once, it is still considered
        a single segment. This implies that usually the number of
        segments is less than the number of coordinates.

        Args:
            border_coordinates: list of points where the borders
                are specified
            winning_segment: tuple with the two pair of points
                used to define the color of the segment (green)
            losing_segment: tuple with the two pair of points
                used to define the color of the segment (red)
            inner_segments: inner borders used to make the Stynker
                bounces. Assumes that its radius is 10
            winning_inner_segment: tuple with the two pair of points
                that define the winning segment
            losing_inner_segment: tuple with the two pair of points
                that define the losing segment
            name: name of the environment
        """
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
        self.inner_segments = inner_segments
        self.winning_inner_segment = winning_inner_segment
        self.losing_inner_segment = losing_inner_segment
        self.outer_segments = self.get_segments()

    def draw_borders(self) -> turtle.Turtle:
        """Draw the borders of the environment"""
        border = turtle.Turtle()
        border.speed(0)
        border.penup()
        border.pensize(5)
        previous_coord = None
        for i, coord in enumerate(self.border_coordinates):
            segment = (previous_coord, coord)
            if (
                previous_coord is not None
                and segment == self.winning_segment
            ):
                border.pencolor("#2dc937")
            elif (
                previous_coord is not None
                and segment == self.losing_segment
            ):
                border.pencolor("#cc3232")
            else:
                border.pencolor("black")
                border.pensize()
            border.setposition(*coord)
            border.pendown()
            previous_coord = coord
        self.window.update()
        return border

    def get_segments(self) -> list[tuple[tuple[float, float], tuple[float, float]]]:
        """
        From the corners of the border, create the list
        of different segments used to draw the environment
        """
        segments = list()
        num_points = len(self.border_coordinates)
        for i, coordinate in enumerate(self.border_coordinates):
            # The segments must be closed, so the last
            # coordinate has to connect with the first
            next_coordinate = self.border_coordinates[(i + 1) % num_points]
            segment = (coordinate, next_coordinate)
            reverse_segment = (next_coordinate, coordinate)
            # Ignore segments that are already included
            if segment in segments or reverse_segment in segments:
                continue
            # If the segments are equal, ignore them
            else:
                segments.append(segment)
        return segments

    def get_first_intersection_info(
        self,
        initial_position: tuple[float, float],
        final_position: tuple[float, float],
    ) -> dict[str, Any]:
        """
        Given two points (positions of the ball) in the environment,
        return useful information about its first interaction with
        the environment border

        Args:
            initial_position: initial position of the ball
            final_position: final position of the ball

        Returns:
            Dictionary with useful information about the interaction
            with the environment border.

        """
        intersection_info = {
            "intersection_point": None,
            "distance": None,
            "segment": None,
            "segment_parameters": None,
        }
        min_distance = 1e8
        for (p1, p2) in self.inner_segments:
            if self.intersect(p1, p2, initial_position, final_position):
                # Ignore a segment if the point relies on it
                if self.distance_to_segment(*initial_position, p1, p2) < 1e-12:
                    continue
                intersection = self.get_segment_intersection(p1, p2, initial_position, final_position)
                d = self.distance_to_point(*initial_position, *intersection)
                if d < min_distance:
                    first_intersection = intersection
                    min_distance = d

                    # Save info
                    intersection_info["intersection_point"] = first_intersection
                    intersection_info["distance"] = min_distance
                    intersection_info["segment"] = (p1, p2)
                    intersection_info["segment_parameters"] = self.get_general_form(p1, p2)

        return intersection_info

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
    ) -> tuple[float, float]:
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
            raises an Error
        """
        if not Environment.intersect(p1, p2, q1, q2):
            raise ValueError("Segments don't intersect")

        a1, b1, c1 = Environment.get_general_form(p1, p2)
        a2, b2, c2 = Environment.get_general_form(q1, q2)

        determinant = a1*b2-a2*b1
        x = (b1*c2 - b2*c1) / determinant
        y = (c1*a2 - c2*a1) / determinant
        return x, y

    @staticmethod
    def segment_contained(
        big_segment: tuple[tuple[float, float], tuple[float, float]],
        small_segment: tuple[tuple[float, float], tuple[float, float]],
    ) -> bool:
        """
        Check if `small_segment` is a 'subsegment' of `big_segment`.
        That means: every point that belongs to `small_segment`,
        belongs to `big_segment`.

        Currently, only supports vertical and horizontal lines
        Args:
            big_segment: tuple of two points defining a segment
            small_segment: tuple of two points defining a segment

        Returns:
            Boolean indicating if `small_segment` is geometrically
            contained in `big_segment`
        """
        big_segment = sorted(big_segment)
        small_segment = sorted(small_segment)

        # Check if the two lines have the same slope
        if not Environment.get_slope(*big_segment) == Environment.get_slope(*big_segment):
            return False

        p1, p2 = big_segment
        q1, q2 = small_segment

        are_in_interval = (p1 <= q1 <= p2) and (p1 <= q1 <= p2)
        same_axis = p1[0] == q1[0] or p1[1] == q1[1]

        return are_in_interval and same_axis

    @staticmethod
    def get_slope(p1: tuple[float, float], p2: tuple[float, float]) -> float:
        """
        Given two points, p1 and p2, return the slope
        of the line defined by them

        Args:
            p1: first point
            p2: second point

        Returns:
            Float representing the slope of the line that passes
            through both point. float("inf") if line is vertical
        """
        x1, y1 = p1
        x2, y2 = p2
        try:
            m = (y2 - y1) / (x2 - x1)
        except ZeroDivisionError:
            m = float("inf")
        return m

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
