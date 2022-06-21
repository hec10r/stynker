import turtle
from src import Stynker
from src import Environment


if __name__ == "__main__":
    # Initialize environment
    environment = Environment()
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
        initial_position=(0, 0),
        show_route=False,
        random_sleep=False,
    )

    stynker_2 = Stynker(
        n_nodes=n_nodes,
        period="dream",
        n_remakes=10,
        n_input=8,
        n_output=8,
        color="purple",
        initial_position=(0, 0),
        show_route=False,
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

    # Define two different gravities for the stynkers
    stynker_1.vector = (1.5, 0.1)
    stynker_2.vector = (-2.3, 0.2)

    # Run wake cycles
    for _ in range(100000):
        stynker_1.run_cycle()
        stynker_2.run_cycle()

        # Check if the stynker bounces and calculate new velocity vector
        vector_1 = environment.calculate_velocity_vector(stynker_1)
        vector_2 = environment.calculate_velocity_vector(stynker_2)

        # Update vector
        stynker_1.vector = vector_1
        stynker_2.vector = vector_2

        environment.window.update()

    turtle.done()
