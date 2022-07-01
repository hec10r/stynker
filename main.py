import math
import turtle
from copy import deepcopy
from typing import Tuple

from src import Stynker
from src import Environment


def clone_stynker(stk: Stynker, color: str, show_route: bool = False):
    required_parameters = [
        "n_input",
        "n_output",
        "n_remakes",
        "vector_magnitude",
        "period",
        "velocity_vector",
    ]
    kwargs = {
        key: val
        for key, val in stk.__dict__.items()
        if key in required_parameters
    }
    kwargs["n_nodes"] = -1
    kwargs["initial_position"] = stk.initial_position
    kwargs["show_route"] = show_route
    kwargs["color"] = color

    new_stynker = Stynker(**kwargs)
    new_stynker.graph = deepcopy(stk.graph)
    new_stynker.kick_dictionary = deepcopy(stk.kick_dictionary)
    new_stynker.reverse_graph = deepcopy(stk.reverse_graph)
    new_stynker.nodes_dict = deepcopy(stk.nodes_dict)
    return new_stynker


def run_wake_cycle(
        stk_1: Stynker,
        stk_2: Stynker,
        n_cycle: int,
        rendering_rate: int = 1,
) -> Tuple[Stynker, Stynker]:
    stk_1.period = "wake"
    stk_2.period = "wake"
    for n in range(n_cycle):
        # TODO: Change logic keep the win/loss counter
        # TODO: input logic
        stk_1.run_cycle()
        stk_2.run_cycle()

        # Check if the stynker bounces and calculate new velocity vector
        info_1 = environment.get_interaction_information(stk_1)
        info_2 = environment.get_interaction_information(stk_2)

        # Update position
        stk_1.update_position(*info_1["new_position"])
        stk_2.update_position(*info_2["new_position"])

        # Update vector
        stk_1.update_velocity_vector(info_1["final_velocity_vector"])
        stk_2.update_velocity_vector(info_2["final_velocity_vector"])

        # Win / Lose logic
        if info_1["won"]:
            stk_1.reset_position()
            stk_2 = clone_stynker(stk_1, "purple")
        elif info_1["lost"]:
            stk_2.reset_position()
            stk_1 = clone_stynker(stk_2, "blue")
        elif info_2["won"]:
            stk_2.reset_position()
            stk_1 = clone_stynker(stk_2, "blue")
        elif info_2["lost"]:
            stk_1.reset_position()
            stk_2 = clone_stynker(stk_1, "purple")

        if n % rendering_rate == 0:
            environment.window.update()

    return stk_1, stk_2


if __name__ == "__main__":
    maze_environment = {
        "border_coordinates": [
            (360, -360),
            (360, 360),
            (-120, 360),
            (-120, -180),
            (-120, 360),
            (-360, 360),
            (-360, -360),
            (120, -360),
            (120, 180),
            (120, -360),
            (360, -360),
        ],
        "winning_segment": 5,
        "losing_segment": 10,
    }
    hexagonal_radius = 360
    hexagonal_environment = {
        "border_coordinates": [
            (
                math.cos(math.radians(alpha)) * hexagonal_radius,
                math.sin(math.radians(alpha)) * hexagonal_radius
            )
            for alpha in range(0, 420, 60)
        ],
        "winning_segment": 2,
        "losing_segment": 5,
    }
    # Initialize environment
    environment = Environment(**maze_environment)
    environment.draw_borders()

    # Input parameters
    n_nodes = int(turtle.textinput("Input", "Number of nodes for the Stynkers:"))

    # Other parameters
    show_route = False
    vector_magnitude = 2.0

    # Initialize Stynkers
    stynker_1 = Stynker(
        n_nodes=n_nodes,
        period="dream",
        n_remakes=10,
        n_input=8,
        n_output=8,
        color="blue",
        vector_magnitude=vector_magnitude,
        initial_position=(0, 0),
        show_route=show_route,
        random_sleep=False,
    )

    stynker_2 = Stynker(
        n_nodes=n_nodes,
        period="dream",
        n_remakes=10,
        n_input=8,
        n_output=8,
        color="purple",
        vector_magnitude=vector_magnitude,
        initial_position=(0, 0),
        show_route=show_route,
        random_sleep=False,
    )

    cycles = [
        ("dream", 100),
        ("sleep", 1),
        ("wake", 100000),
    ]

    for period, n_cycles in cycles:
        stynker_1.period = period
        stynker_2.period = period

        if period == "wake":
            stynker_1, stynker_2 = run_wake_cycle(stynker_1, stynker_2, n_cycles)

        for _ in range(n_cycles):
            stynker_1.run_cycle()
            stynker_2.run_cycle()

    turtle.done()
