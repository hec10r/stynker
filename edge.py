from nodes import Node
class Edge:
    """"""
    ALLOWED_ATTRIBUTES = {"weight", "length"}
    def __init__(
        self,
        node: Node,
        weight: int,
        length: int,
        **kwargs
    ) -> None:

        self.node = node
        self.weight = weight
        self.lenght = length
        self.original_kwargs = kwargs.copy()
        self.__dict__.update(kwargs)

        self.next_steps: list

    def __hash__(self) -> int:
        return hash(self.node.name)

    def dream_cycle(self):
        cnt = sum([1 for el in self.next_steps if el == 0])
        self.node.level += cnt * self.weight
        self.next_steps = [el - 1 for el in self.next_steps if el != 0]

    def spill(self):
        self.next_steps.append(self.lenght)