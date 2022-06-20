from __future__ import annotations
import json
from .node import Node


class Edge:
    """Edge object that represents a connection to a node (neurone)"""
    def __init__(
        self,
        node: Node,
        weight: int = None,
        length: int = None,
    ) -> None:
        """

        Args:
            node: destination `Node` of the current `Edge`
            weight: how much juice it carries each time it trickles
            length: how many cycles it takes for a trickle of juice to
                travel down this `Edge` and arrive at destination `Node`
        """
        self.node = node
        self.weight = weight
        self.length = length

        # Variable to store when to increment the `level` of `node`
        # based on `weight` and `length`
        self.next_steps: list = list()

    def run_cycle(self) -> None:
        """Handles the dream/wake cycles"""
        trickles_arriving = 1 in self.next_steps
        if trickles_arriving:
            self.node.level += self.weight
        self.next_steps = [el - 1 for el in self.next_steps if el != 1]

    def load(self) -> None:
        """
        Load the Edge when the source node spills.
        Updates the `next_steps` variable to represent the
        desired behavior
        """
        self.next_steps.append(self.length)

    def __hash__(self) -> int:
        """
        Use the name of the destination node as its hash.

        Have in mind that this only makes sense in the context of
        this implementation, since the Edge object is implicitly
        related to an existing Node

        Notice that two ed with the same name will be considered
        equal independently of their `weight` and `length`
        """
        return hash(self.node)

    def __eq__(self, other_edge: Edge) -> bool:
        """
        Overload the equal operator based on the following:
        Two edges are considered equal if they have the same destination node.
        See `__hash__` method

        Args:
            other_edge: Edge to be compared with the current

        Returns:
            Whether the edges have the same destination node

        Raises:
            TypeError: when comparing with an object that is not
            instance of `Edge`
        """

        if isinstance(other_edge, Edge):
            return self.node == other_edge.node
        raise TypeError(f"Edge is not comparable to type {type(other_edge)}")

    def __repr__(self) -> str:
        """
        Overload the repr method to display useful information
        about the Node

        Returns:
            JSON representation of a Node
        """
        repr_ = {
            "to_node": self.node.name,
            "weight": self.weight,
            "length": self.length,
            "next_steps": self.next_steps,
        }
        return json.dumps(repr_, indent=2)
