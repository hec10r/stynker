import json
import time
import turtle
from argparse import ArgumentParser, Namespace
from src import Stynker
from src import Environment

# Win / Lose logic
cnt_win = 0
cnt_lose = 0

# Rendering and results logic
rendering_rate = 100
results_cycles = 10000

num_run_cycles = 0
results = dict()

cycles = [
    ("dream", 1000),
    ("sleep", 1),
    ("wake", 1000),
    ("sleep", 1),
] * 500


def parse_args() -> Namespace:
    """
    """
    parser = ArgumentParser(description="Run Stynker main program")

    parser.add_argument(
        "-n", "--nodes", type=int,
        required=False,
        help="Number of nodes to use"
    )

    parser.add_argument(
        "-r", "--remakes", type=int,
        required=False,
        help="Number of nodes to remake in each sleep cycle"
    )

    parser.add_argument(
        "-i", "--input", type=int,
        required=False,
        help="Number of input nodes"
    )

    parser.add_argument(
        "-o", "--output", type=int,
        required=False,
        help="Number of output nodes"
    )

    parser.add_argument(
        "-e", "--environment", type=str,
        required=False,
        help="Name of the environment to use"
    )

    parser.add_argument(
        "-sr", "--show_route", type=bool,
        required=False,
        help="Whether to show the route"
    )

    parser.add_argument(
        "-rs", "--random_sleep", type=bool,
        required=False,
        help="Whether to show the route"
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    # Initialize environment
    environment = Environment.get_environment(env_name="simple_maze")
    environment.draw_borders()

    # Input parameters
    n_nodes = int(turtle.textinput("Input", "Number of nodes for the Stynkers:"))

    # Other parameters
    show_route = True
    n_remakes = 100
    n_input = 8
    n_output = 64
    initial_position = (0, 0)
    random_sleep = False

    # Initialize Stynkers
    stynker_1 = Stynker(
        n_nodes=n_nodes,
        n_remakes=n_remakes,
        n_input=n_input,
        n_output=n_output,
        color="blue",
        environment=environment,
        initial_position=initial_position,
        show_route=show_route,
        random_sleep=random_sleep,
    )

    stynker_2 = Stynker(
        n_nodes=n_nodes,
        n_remakes=n_remakes,
        n_input=n_input,
        n_output=n_output,
        color="purple",
        environment=environment,
        initial_position=initial_position,
        show_route=show_route,
        random_sleep=random_sleep,
    )

    # Saving used parameters
    stynker_1.to_json("last_parameters_used_stynker_1.json")
    stynker_2.to_json("last_parameters_used_stynker_2.json")

    for period, n_cycles in cycles:
        stynker_1.assign_period(period)
        stynker_2.assign_period(period)

        if period == "wake":
            for n in range(n_cycles):
                num_run_cycles += 1
                info_1 = stynker_1.run_cycle()
                info_2 = stynker_2.run_cycle()

                # Win / Lose logic
                # There is a tiny possibility where two of these events happen at the same
                # time. Since this is once in a million, we are ignoring it
                if info_1["won"]:
                    cnt_win += 1
                    stynker_1.reset_position()
                    stynker_2.clone_from(stynker_1)
                    stynker_1.reset_vector()
                    stynker_2.reset_vector()
                elif info_1["lost"]:
                    cnt_lose += 1
                    stynker_2.reset_position()
                    stynker_1.clone_from(stynker_2)
                    stynker_1.reset_vector()
                    stynker_2.reset_vector()
                elif info_2["won"]:
                    cnt_win += 1
                    stynker_2.reset_position()
                    stynker_1.clone_from(stynker_2)
                    stynker_1.reset_vector()
                    stynker_2.reset_vector()
                elif info_2["lost"]:
                    cnt_lose += 1
                    stynker_1.reset_position()
                    stynker_2.clone_from(stynker_1)
                    stynker_1.reset_vector()
                    stynker_2.reset_vector()

                if (n + 1) % rendering_rate == 0:
                    environment.window.update()

                if num_run_cycles % results_cycles == 0:
                    try:
                        ratio = cnt_win / cnt_lose
                    except ZeroDivisionError:
                        ratio = -1
                    results[num_run_cycles] = (cnt_win, cnt_lose, ratio)
                    # Restart counter after `results_cycles`
                    cnt_win = 0
                    cnt_lose = 0
                    print(results)
        else:
            for _ in range(n_cycles):
                stynker_1.run_cycle()
                stynker_2.run_cycle()

    # Saving the results with the current timestamp
    with open(f"results_{int(time.time())}.json", "w") as f:
        json.dump(results, f)
