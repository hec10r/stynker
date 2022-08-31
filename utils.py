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
            # Assuming that the radius of the Stynker is 10, define
            # the 'inner' borders where the Stynker will bounce,
            # so it doesn't pass through the 'real' borders
            "inner_segments": [
                ((350, -360), (350, 350)),
                ((350, 350), (-110, 350)),
                ((-110, 350), (-110, -190)),
                ((-110, -190), (-130, -190)),
                ((-130, -190), (-130, 360)),
                ((-130, 360), (-350, 360)),
                ((-350, 360), (-350, -350)),
                ((-350, -350), (110, -350)),
                ((110, -350), (110, 190)),
                ((110, 190), (130, 190)),
                ((130, 190), (130, -360)),
                ((130, -360), (350, -360)),
            ],
            # These are used to color the environment borders
            "winning_segment": ((-120, 360), (-360, 360)),
            "losing_segment": ((120, -360), (360, -360)),

            # These are used to know when the Stynker win/loss.
            # This logic assumes that the Stynker radius is 10
            "winning_inner_segment": ((-130, 360), (-350, 360)),
            "losing_inner_segment": ((130, -360), (350, -360)),
            "name": env_name,
        }
        return simple_maze

    raise NotImplementedError(f"The environment {env_name} is not supported")
