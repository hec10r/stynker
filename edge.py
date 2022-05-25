from __future__ import annotations
import json
from nodes import Node


class Edge:
    """"""
    def __init__(
        self,
        node: Node,
        weight: int = None,
        length: int = None,
    ) -> None:
        self.node = node
        self.weight = weight
        self.length = length
        self.next_steps: list = list()

    def dream_cycle(self) -> None:
        trickles_arriving = 1 in self.next_steps
        if trickles_arriving:
            self.node.level += self.weight
        self.next_steps = [el - 1 for el in self.next_steps if el != 1]

    def load(self) -> None:
        self.next_steps.append(self.length)

    def __hash__(self) -> int:
        return hash(self.node.name)

    def __eq__(self, other_edge: Edge) -> bool:
        return self.node.name == other_edge.node.name

    def __repr__(self) -> str:
        repr_ = {
            "to_node": self.node.name,
            "weight": self.weight,
            "length": self.length,
            "next_steps": self.next_steps,
        }
        return json.dumps(repr_, indent=2)
