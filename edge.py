import json
from nodes import Node


class Edge:
    """"""
    ALLOWED_ATTRIBUTES = {"weight", "length"}
    def __init__(
        self,
        node: Node,
        weight: int = None,
        length: int = None,
        **kwargs
    ) -> None:

        self.node = node
        self.weight = weight
        self.lenght = length

        self.next_steps: list = list()

    def __hash__(self) -> int:
        return hash(self.node.name)

    def dream_cycle(self) -> None:
        cnt = sum([1 for el in self.next_steps if el == 1])
        self.node.level += cnt * self.weight
        self.next_steps = [el - 1 for el in self.next_steps if el != 1]

    def load(self) -> None:
        self.next_steps.append(self.lenght)

    def __hash__(self) -> int:
        return hash(self.node.name)

    def __eq__(self, other_edge: object) -> bool:
        return self.node.name == other_edge.node.name

    def __repr__(self) -> str:
        repr_ = {
            "to_node": self.node.name,
            "weight": self.weight,
            "lenght": self.lenght,
            "next_steps": self.next_steps,
        }
        return json.dumps(repr_, indent=2)
