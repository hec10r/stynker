from collections import defaultdict
from nodes import Node
from edge import Edge
from typing import List, Iterable


class Stynker:
    def __init__(self):
        self._graph: defaultdict = defaultdict(set)
        self.current_cycle: int = 0
        self.period: str

    def get_nodes(self) -> Iterable[Node]:
        return self._graph.keys()

    def add_edge(self, node_1: Node, node_2: Node, **kwargs):
        edge = Edge(node_2, **kwargs)
        self._graph[node_1].add(edge)

    def remake(self, nodes: Iterable[Node]) -> None:
        for node in nodes:
            # Remake node's attributes
            node.remake()
            # Remake edges
            self.remake(node)
        pass

    def remake_edges(self, nodes: Iterable[Node]) -> None:
        # TODO: this should create new edges for selected nodes
        # - Create new edges from `nodes`
        # - Create new edges to `nodes`
        pass
    
    def run_cycle(self):
        if self.period == "dream":
            self._run_dream_cycle()
        elif self.period == "sleep":
            self._run_sleep_cycle()
        elif self.period == "wake":
            self._run_wake_period

    def _run_dream_cycle(self):
        for node in self.get_nodes():
            node.dream_cycle()
            for edge in self._graph[node]:
                edge.dream_cycle()
        
        for node in self.get_nodes():
            if node.is_full():
                node.spill()
                (edge.spill() for edge in self._graph[node])

    def _run_sleep_cycle(self, n_remakes: int = 1):
        _damage_order = lambda node: node.damage
        order_nodes = sorted(
            [node for node in self.get_nodes()],
            key=_damage_order
        )
        
        # Remake nodes with the least damage
        self.remake(order_nodes[:n_remakes])

    def _run_wake_period(self):
        # TODO: basically remake empty nodes
        pass


