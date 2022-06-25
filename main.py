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

    # Define two different initial velocity vectors
    stynker_1.velocity_vector = (stynker_1.vector_magnitude, 0)
    stynker_2.velocity_vector = (0, -stynker_2.vector_magnitude)

    # Run wake cycles
    for _ in range(100000):
        stynker_1.run_cycle()
        stynker_2.run_cycle()

        # Check if the stynker bounces and calculate new velocity vector
        info_1 = environment.get_interaction_information(stynker_1)
        info_2 = environment.get_interaction_information(stynker_2)

        # Update vector
        stynker_1.velocity_vector = info_1["final_velocity_vector"]
        stynker_2.velocity_vector = info_2["final_velocity_vector"]

        environment.window.update()

    turtle.done()
