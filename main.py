import math
import turtle
from src import Stynker
from src import Environment


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

    # Initialize Stynkers
    stynker_1 = Stynker(
        n_nodes=n_nodes,
        period="dream",
        n_remakes=10,
        n_input=8,
        n_output=8,
        color="blue",
        vector_magnitude=2.0,
        initial_position=(0, 0),
        show_route=True,
        random_sleep=False,
    )

    stynker_2 = Stynker(
        n_nodes=n_nodes,
        period="dream",
        n_remakes=10,
        n_input=8,
        n_output=8,
        color="purple",
        vector_magnitude=2.0,
        initial_position=(0, 0),
        show_route=True,
        random_sleep=False,
    )

    # Run dream cycles
    for _ in range(100):
        stynker_1.run_cycle()
        stynker_2.run_cycle()

    # Change 'period' to sleep
    stynker_1.period = "sleep"
    stynker_2.period = "sleep"

    # Run sleep cycles
    stynker_1.run_cycle()
    stynker_2.run_cycle()

    # Change 'period' to wake
    stynker_1.period = "wake"
    stynker_2.period = "wake"

    # Run wake cycles
    for _ in range(100000):
        stynker_1.run_cycle()
        stynker_2.run_cycle()

        # Check if the stynker bounces and calculate new velocity vector
        info_1 = environment.get_interaction_information(stynker_1)
        info_2 = environment.get_interaction_information(stynker_2)

        # Update position
        stynker_1.update_position(*info_1["new_position"])
        stynker_2.update_position(*info_2["new_position"])

        # Update vector
        stynker_1.update_velocity_vector(info_1["final_velocity_vector"])
        stynker_2.update_velocity_vector(info_2["final_velocity_vector"])

        from copy import deepcopy
        # Win / Lose logic
        if info_1["won"]:
            stynker_2 = deepcopy(stynker_1)
            stynker_2.update_position(0, 0)
        elif info_1["lost"]:
            stynker_1 = deepcopy(stynker_2)
            stynker_1.update_position(0, 0)
        elif info_2["won"]:
            stynker_1 = deepcopy(stynker_2)
            stynker_1.update_position(0, 0)
        elif info_2["lost"]:
            stynker_2 = deepcopy(stynker_1)
            stynker_2.update_position(0, 0)

        environment.window.update()

    turtle.done()
