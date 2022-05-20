from collections import defaultdict
from nodes import Node
from edge import Edge
from typing import Iterable


class Stynker:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.graph: defaultdict = defaultdict(set)
        self.current_cycle: int = 0
        self.period: str

    def get_nodes(self) -> Iterable[Node]:
        return self.graph.keys()

    def get_empty_nodes(self) -> Iterable[Node]:
        empty_nodes = (
            node
            for node in self.get_nodes()
            if node.is_empty()
        )
        return empty_nodes

    def add_edge(self, node_1: Node, node_2: Node, **kwargs):
        edge = Edge(node_2, **kwargs)
        self.graph[node_1].add(edge)

    def remake(self, nodes: Iterable[Node]) -> None:
        for node in nodes:
            # Remake node's attributes
            node.remake()
            # Remake edges
            self.remake(node)

    def remake_edges(self, nodes: Iterable[Node]) -> None:
        # TODO: this should create new edges for selected nodes
        # - Create new edges from `nodes`
        # - Create new edges to `nodes`
        pass
    
    def run_cycle(self) -> None:
        self.current_cycle += 1
        if self.period == "dream":
            self._run_dream_cycle()
        elif self.period == "sleep":
            self._run_sleep_cycle()
        elif self.period == "wake":
            self._run_wake_cycle

    def _run_dream_cycle(self) -> None:
        for node in self.get_nodes():
            # Increase the level of each node
            node.dream_cycle()
            for edge in self.graph[node]:
                # Check if trickles arrive to nodes
                edge.dream_cycle()
            # Check the inputs for T values
            if node.is_input() and node.active: 
                node.increase_level(10)
                node.active = False
        
        for node in self.get_nodes():
            # Check if the node is full
            if node.is_full():
                # Mark output node as active if it spills
                if node.is_output():
                    node.activate = True
                # Spill full nodes
                node.spill()
                for edge in self.graph[node]:
                    # Edges get loaded with trickles
                    edge.load()
            elif node.is_output():
                node.active = False
                

    def _run_sleep_cycle(self, n_remakes: int = 1) -> None:
        # Sort list of nodes by damage
        damage_order = lambda node: node.damage
        ordered_nodes = sorted(
            [node for node in self.get_nodes()],
            key=damage_order
        )
        
        # Pick first n nodes with less damage and remake
        self.remake(ordered_nodes[:n_remakes])

    def _run_wake_cycle(self) -> None:
        # TODO: basically remake empty nodes
        for node in self.get_empty_nodes():
            # This remake may be different 
            node.remake()

    def __repr__(self) -> str:
        import json
        status = {
            "cycle": self.current_cycle,
            "period": self.period,
        }
        nodes_info = [
            [
                json.loads(str(node)),
                [
                    json.loads(str(edge))
                    for edge in edges
                ],
            ]
            for node, edges in self.graph.items()
        ]

        repr_ = (
            json.dumps(status, indent=4)
            + "\n" +
            json.dumps(nodes_info, indent=4)
        )

        return repr_
