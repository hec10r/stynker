from __future__ import annotations
import json
from typing import Tuple, Union
from random import randint
from constants import node_constants


class Node:
    def __init__(
        self,
        name: int,
        size: int,
        endo: int,
        **kwargs
    ):        
        self.name: str = name
        self.size: int = size
        self.endo: int = endo
        self.type: Union[str, None] = None
        self.active: Union[bool, None] = None
        self.__dict__.update(**kwargs)

        self.level: int = 0
        self.damage: int = 0
        

    def is_full(self) -> bool:
        return self.level >= self.size

    def spill(self) -> None:
        self.level = 0
        self.damage += 1

    def dream_cycle(self):
        """Increase the `level` by `endo`"""
        self.increase_level(self.endo)
    
    def increase_level(self, q: int) -> None:
        self.level = max(self.level + q, 0)

    def remake(self) -> None:
        self.size = randint(*node_constants["size_range"])
        self.endo = randint(*node_constants["endo_range"])

    def is_input(self) -> bool:
        return self.type == "input"
        
    def is_output(self) -> bool:
        return self.type == "output"

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other_node: Node) -> bool:
        if isinstance(other_node, Node):
            return self.name == other_node.name
        raise TypeError(f"Node is not comparable to type {type(other_node)}")

    def __repr__(self) -> str:
        repr_ = {
            "name": self.name,
            "size": self.size,
            "endo": self.endo,
            "type": self.type,
            "active": self.active,
            "level": self.level,
            "damage": self.damage,
        }
        return json.dumps(repr_, indent=2)