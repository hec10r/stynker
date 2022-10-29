# Information about number of cycles
cycles = [
    ("wake", 1000),
    ("sleep", 1),
    ("dream", 1000),
    ("sleep", 1),
    ("dream", 1000),
    ("sleep", 1)
] * 1000

# Information about Stynker's parameters.
# Assuming both will use the same
mind_parameters = {
    "n_nodes": 800,
    "n_remakes": 10,
    "n_input": 256,
    "n_output": 32,
    "random_sleep": False,
}

# Information about the environment
environment_parameters = {
    "environment": "simple_maze",
    "initial_position": (0, 0),
    "show_route": False,
    "friction_coefficient": 1.0
}

stynker_parameters = {
    **mind_parameters,
    **environment_parameters,
}
