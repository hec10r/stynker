import json
import turtle
from src import Stynker
from src import Environment


if __name__ == "__main__":
    # Initialize Stynker
    stynker = Stynker(
        n_nodes=1000,
        period="dream",
        n_remakes=10,
        n_input=5,
        n_output=5,
        color="blue",
        initial_position=(0, 0),
        show_route=False,
        random_sleep=False,
    )

    environment = Environment(stynker)
    environment.draw_borders()

    # Run dream cycles
    for _ in range(100):
        stynker.run_cycle()

    # Run one sleep cycle
    stynker.period = "sleep"
    stynker.run_cycle()

    # # Run wake cycles
    # stynker.period = "wake"
    # for _ in range(100):
    #     stynker.run_cycle()

    turtle.done()
