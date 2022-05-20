class Node:
    def __init__(self):
        # TODO: decide how to define this
        self.name: str
        self.level: int
        self.damage: int
        self.size: int
        self.endo: int
        self.status: str

        self.type: str
        self.active: bool

    def is_full(self) -> bool:
        return self.level >= self.size

    def spill(self) -> None:
        self.level = 0
        self.damage += 1

    def dream_cycle(self):
        self.increase_level(self.endo)
    
    def increase_level(self, q: int) -> None:
        self.level += q

    def dream_check(self) -> bool:
        return self.level >= self.size

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
