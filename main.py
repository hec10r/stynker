import json
import turtle
from src import Stynker
from src import Environment


if __name__ == "__main__":
    # Initialize Stynkers
    stynker_1 = Stynker(
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

    stynker_2 = Stynker(
        n_nodes=1000,
        period="dream",
        n_remakes=10,
        n_input=5,
        n_output=5,
        color="purple",
        initial_position=(0, 0),
        show_route=False,
        random_sleep=False,
    )

    environment = Environment()
    environment.draw_borders()

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
    # stynker.period = "wake"
    # for _ in range(100):
    #     stynker.run_cycle()

    stynker_1.period = "wake"
    stynker_2.period = "wake"
    g1 = -0.5
    g2 = -0.8
    for _ in range(1000):
        stynker_1.run_cycle(gravity=g1)
        stynker_2.run_cycle(gravity=g2)
        if environment.touch_border(stynker_1.turtle):
            g1 = -g1
        if environment.touch_border(stynker_2.turtle):
            g2 = -g2
        environment.window.update()

    turtle.done()
