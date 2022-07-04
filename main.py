import json
import time
import turtle
from typing import Tuple
from utils import get_environment_inputs
from src import Stynker
from src import Environment

cnt_win = 0
cnt_lose = 0
num_run_cycles = 0
results = dict()

cycles = [
    ("dream", 100),
    ("sleep", 1),
    ("wake", 500000),
]


def run_wake_cycle(
        stk_1: Stynker,
        stk_2: Stynker,
        n_cycles: int,
        rendering_rate: int = 1,
        results_cycles: int = 100000,
) -> Tuple[Stynker, Stynker]:
    """
    Run the wake cycle, and updates the Stynkers if required.

    Store the information about the
    Args:
        stk_1: Stynker # 1
        stk_2: Stynker # 2
        n_cycles: number of cycles to run
        rendering_rate: how often the visuals are rendered
        results_cycles: how often to store te results
    Returns:
        Tuple of the two Stynkers updated
    """
    global cnt_win
    global cnt_lose
    global num_run_cycles
    global results

    stk_1.period = "wake"
    stk_2.period = "wake"
    for n in range(n_cycles):
        # Updates the 'mind'
        stk_1.run_cycle()
        stk_2.run_cycle()

        # Updates the 'body'
        # Check if the stynker bounces and calculate new velocity vector
        info_1 = environment.get_interaction_information(stk_1)
        info_2 = environment.get_interaction_information(stk_2)

        # Update position
        stk_1.update_position(*info_1["new_position"])
        stk_2.update_position(*info_2["new_position"])

        # Update vector
        stk_1.update_velocity_vector(info_1["final_velocity_vector"])
        stk_2.update_velocity_vector(info_2["final_velocity_vector"])

        # Handle input logic
        if (closest_input_node := info_1["closest_input_node"]) is not None:
            stk_1.activate_node(closest_input_node)
        if (closest_input_node := info_2["closest_input_node"]) is not None:
            stk_2.activate_node(closest_input_node)

        # Win / Lose logic
        # There is a tiny possibility where two of these events happen at the same
        # time. Since this is once in a million, we are ignoring it
        if info_1["won"]:
            cnt_win += 1
            stk_1.reset_position()
            stk_2.clone_from(stk_1)
            stk_1.reset_vector()
            stk_2.reset_vector()
        elif info_1["lost"]:
            cnt_lose += 1
            stk_2.reset_position()
            stk_1.clone_from(stk_2)
            stk_1.reset_vector()
            stk_2.reset_vector()
        elif info_2["won"]:
            cnt_win += 1
            stk_2.reset_position()
            stk_1.clone_from(stk_2)
            stk_1.reset_vector()
            stk_2.reset_vector()
        elif info_2["lost"]:
            cnt_lose += 1
            stk_1.reset_position()
            stk_2.clone_from(stk_1)
            stk_1.reset_vector()
            stk_2.reset_vector()

        if (n + 1) % rendering_rate == 0:
            environment.window.update()

        if (n + 1) % results_cycles == 0:
            try:
                ratio = cnt_win / cnt_lose
            except ZeroDivisionError:
                ratio = -1
            # Restart counter after `results_cycles`
            cnt_win = 0
            cnt_lose = 0
            results[n + 1] = (cnt_win, cnt_lose, ratio)
            print(results)

    return stk_1, stk_2


if __name__ == "__main__":
    environment_inputs = get_environment_inputs(env_name="simple_maze")
    # Initialize environment
    environment = Environment(**environment_inputs)
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

    for period, n_cycles in cycles:
        stynker_1.period = period
        stynker_2.period = period

        if period == "wake":
            stynker_1, stynker_2 = run_wake_cycle(
                stk_1=stynker_1,
                stk_2=stynker_2,
                n_cycles=n_cycles,
                rendering_rate=1000,
                results_cycles=10000,
            )
        else:
            for _ in range(n_cycles):
                stynker_1.run_cycle()
                stynker_2.run_cycle()

    # Saving the results with the current timestamp
    with open(f"results_{int(time.time())}.json", "w") as f:
        json.dump(results, f)
