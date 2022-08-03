# Information about number of cycles
cycles = [
    ("dream", 1000),
    ("sleep", 1),
    ("wake", 1000),
    ("sleep", 1),
] * 500

# Information about Stynker's parameters.
# Assuming both will use the same
mind_parameters = {
    "n_nodes": 1000,
    "n_remakes": 50,
    "n_input": 8,
    "n_output": 64,
    "random_sleep": False,
}

# Information about the environment
environment_parameters = {
    "environment": "simple_maze",
    "initial_position": (0, 0),
    "show_route": True,
}

stynker_parameters = {
    **mind_parameters,
    **environment_parameters,
}
