# Information about number of cycles
cycles = ([
    ("wake", 100),
    ("sleep", 1)
] * 40 +
[  ("dream", 100),
   ("sleep", 1)
] * 40
          ) * 10000

# Information about Stynker's parameters.
# Assuming both will use the same
mind_parameters = {
    "n_nodes": 48,
    "n_remakes": 4,
    "n_input": 32,
    "n_output": 16,
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
