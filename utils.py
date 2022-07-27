import math
from argparse import Namespace, ArgumentParser
from typing import Dict, Any


def parse_args() -> Namespace:
    """Parse arguments passed in the command line"""
    parser = ArgumentParser(description="Run Stynker main program")

    parser.add_argument(
        "-n", "--n_nodes", type=int,
        required=False,
        help="Number of nodes to use"
    )

    parser.add_argument(
        "-r", "--n_remakes", type=int,
        required=False,
        help="Number of nodes to remake in each sleep cycle"
    )

    parser.add_argument(
        "-i", "--n_input", type=int,
        required=False,
        help="Number of input nodes"
    )

    parser.add_argument(
        "-o", "--n_output", type=int,
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


def get_environment_inputs(env_name: str) -> Dict[str, Any]:
    """
    Get the inputs of the environment to use
    Args:
        env_name: name of the environment to get
    Returns:
        Information about the environment
    """
    if env_name == "hexagon":
        hexagonal_radius = 360
        hexagonal_environment = {
            "border_coordinates": [
                (
                    math.cos(math.radians(alpha)) * hexagonal_radius,
                    math.sin(math.radians(alpha)) * hexagonal_radius
                )
                for alpha in range(0, 420, 60)
            ],
            "winning_segment": 2,
            "losing_segment": 5,
            "name": env_name,
        }
        return hexagonal_environment

    if env_name == "simple_maze":
        simple_maze = {
            "border_coordinates": [
                (360, -360),
                (360, 360),
                (-120, 360),
                (-120, -180),
                (-120, 360),
                (-360, 360),
                (-360, -360),
                (120, -360),
                (120, 180),
                (120, -360),
                (360, -360),
            ],
            "winning_segment": 5,
            "losing_segment": 10,
            "name": env_name,
        }
        return simple_maze

    raise NotImplementedError(f"The environment {env_name} is not supported")
