class Node:
    def __init__(self):
        # TODO: decide how to define this
        self.name: str
        self.level: int
        self.damage: int
        self.size: int
        self.endo: int
        self.status: str

    def is_full(self) -> bool:
        return self.level >= self.size

    def spill(self) -> None:
        self.level = 0
        self.damage += 1

    def dream_cycle(self):
        self.level += self.endo

    def dream_check(self) -> bool:
        return self.level >= self.size

    def remake(self) -> None:
        # TODO:
        # - Update size
        # - Update endo
        pass

    def is_empty(self) -> bool:
        # TODO:
        # Logic to define if a node is empty
        pass

    def __hash__(self) -> int:
        return hash(self.name)
