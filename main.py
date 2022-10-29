import json
import logging
import time
from src import Stynker
from parameters import cycles, stynker_parameters
from utils import parse_args
from datetime import datetime

# Win / Lose logic
cnt_win = 0
cnt_lose = 0

# Rendering and results logic
rendering_rate = 1000000000
results_cycles = 200

# Variables for the results
num_run_cycles = 0
results = dict()


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s] %(message)s',
                        datefmt='%Y-%m-%d,%H:%M:%S', level=logging.DEBUG)
    # Read parameters from command line
    args = parse_args()

    # Get parameters passed by command line
    # and use them over the
    args_dict = {
        key: val
        for key, val in vars(args).items()
        if val is not None
    }
    stynker_parameters.update(args_dict)

    # Dropping None values
    stynker_parameters = {
        key: val
        for key, val in stynker_parameters.items()
        if val is not None
    }
    logging.info(f"Running program with the following parameters: {stynker_parameters}")

    # Initialize Stynkers
    stynker_1 = Stynker(
        color="blue",
        **stynker_parameters,
    )

    stynker_2 = Stynker(
        color="purple",
        **stynker_parameters,
    )

    environment = stynker_1.environment

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
                    logging.info(f"{num_run_cycles} Wins: {cnt_win} Losses: {cnt_lose} Ratio: {ratio}")
                    # Print current time
                    print("Time:", datetime.now())

        else:
            for _ in range(n_cycles):
                stynker_1.run_cycle()
                stynker_2.run_cycle()

    # Final timestamp
    print("Time: ", datetime.now())

    # Saving the results with the current timestamp
    with open(f"results_{int(time.time())}.json", "w") as f:
        json.dump(results, f)

    # Saving Stynkers state
    stynker_1.to_pkl("latest_stynker_1.pkl")
