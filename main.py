import json
import time
import turtle
from utils import get_environment_inputs
from src import Stynker
from src import Environment

# Win / Lose logic
cnt_win = 0
cnt_lose = 0

# Rendering and results logic
rendering_rate = 1
results_cycles = 100000

num_run_cycles = 0
results = dict()

cycles = [
    ("dream", 100),
    ("sleep", 1),
    ("wake", 500000),
]

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
    n_remakes = 10
    n_input = 8
    n_output = 8
    initial_position = (0, 0)
    random_sleep = True

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
