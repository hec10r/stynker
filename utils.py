import math
from typing import Dict, Any


def get_environment_inputs(env_name: str) -> Dict[str, Any]:
    """
    Get the environment to use
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
        }
        return simple_maze

    raise NotImplementedError(f"The environment {env_name} is not supported")
