from __future__ import annotations
import json
from random import randint
from typing import Dict, Any

from constants import node_constants


class Node:
    """Node object that represents a neurone"""
    def __init__(
        self,
        name: int,
        size: int,
        endo: int,
        node_type: str = "regular",
        level: int = 0,
        damage: int = 0,
        is_active: bool = False,
    ) -> None:
        """

        Args:
            name: integer to identify a node
            size: capacity of the node
            endo: how much juice is added to the node after a cycle
            node_type: type of the node: input | output | regular
        """
        self.name = name
        self.size = size
        self.endo = endo
        self.type = node_type
        self.level = level
        self.damage = damage
        self.is_active = is_active
        self.is_input = node_type == "input"
        self.is_output = node_type == "output"

        allowed_types = ("input", "output", "regular")

        if node_type not in allowed_types:
            raise ValueError(
                f"Node type should be one of the following: {', '.join(allowed_types)}"
                f", not {node_type}"
            )

    def is_full(self) -> bool:
        """
        Whether the node is `full`
        Returns:
            True if the current level is higher than the size.
            False otherwise
        """
        return self.level >= self.size

    def spill(self) -> None:
        """Reset the current level to 0 and increase damage by 1"""
        self.level = 0
        self.damage += 1

    def run_cycle(self) -> None:
        """Increase the `level` by `endo`"""
        self.increase_level(self.endo)
    
    def increase_level(self, q: int) -> None:
        """
        Increase the `level` by a given quantity.
        The final `level` must remain positive
        """
        self.level = max(self.level + q, 0)

    def remake(self) -> None:
        """
        Change `size` and `endo` for a random value
        specified in `node_constants`
        """
        self.size = randint(*node_constants["size_range"])
        self.endo = randint(*node_constants["endo_range"])

    def activate(self) -> None:
        """Mark node as active if it is input or output"""
        if self.type not in ("input", "output"):
            raise ValueError("Attempting to activate a 'regular' node")
        self.is_active = True

    def deactivate(self) -> None:
        """
        Mark node as active if it is input or output
        """
        self.is_active = False

    def to_json(self, json_path: str) -> None:
        parameters = self.to_dict()
        with open(json_path, "w") as f:
            json.dump(parameters, f)

    def to_dict(self) -> Dict[str, Any]:
        parameters = {
            "name": self.name,
            "size": self.size,
            "endo": self.endo,
            "node_type": self.type,
            "level": self.level,
            "damage": self.damage,
            "is_active": self.is_active,
        }
        return parameters

    @classmethod
    def from_dict(cls, parameters_dict: Dict[str, Any]) -> Node:
        return cls(**parameters_dict)

    def __hash__(self) -> int:
        """
        Use the name of the node as its hash.
        Notice that two nodes with the same name will be considered
        equal independently of their `level`, `size`, `endo`, etc
        """
        return hash(self.name)

    def __eq__(self, other_node: Node) -> bool:
        """
        Overload the equal operator based on the following:
        Two nodes are considered equal if they have the same name.
        See `__hash__` method

        Args:
            other_node: Node to be compared with the current

        Returns:
            Whether the nodes have the same name

        Raises:
            TypeError: when comparing with an object that is not
            instance of `Node`
        """

        if isinstance(other_node, Node):
            return self.name == other_node.name
        raise TypeError(f"Node is not comparable to type {type(other_node)}")

    def __repr__(self) -> str:
        """
        Overload the repr method to display useful information
        about the Node

        Returns:
            JSON representation of a Node
        """
        repr_ = {
            "name": self.name,
            "size": self.size,
            "endo": self.endo,
            "type": self.type,
            "active": self.is_active,
            "level": self.level,
            "damage": self.damage,
        }
        return json.dumps(repr_, indent=2)
