from typing import Union


class Node:
    def __init__(self, **kwargs):
        # TODO: decide how to define this
        self.__dict__.update(**kwargs)
        self.name: str
        self.size: int
        self.endo: int
        self.type: Union[str, None]
        self.active: bool

        self.type = None
        self.active = None
        self.level: int = 0
        self.damage: int = 0
        

    def is_full(self) -> bool:
        return self.level >= self.size

    def spill(self) -> None:
        self.level = 0
        self.damage += 1

    def dream_cycle(self):
        self.increase_level(self.endo)
    
    def increase_level(self, q: int) -> None:
        self.level += q

    def remake(self) -> None:
        # TODO:
        # - Update size
        # - Update endo
        pass

    def is_input(self) -> bool:
        return self.type == "input"
        
    def is_output(self) -> bool:
        return self.type == "output"

    def is_empty(self) -> bool:
        # TODO:
        # Logic to define if a node is empty
        pass

    def __hash__(self) -> int:
        return hash(self.name)

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
        import json
        return json.dumps(repr_, indent=2)