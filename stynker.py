import json
from collections import defaultdict
from random import randint, choice
from nodes import Node
from edge import Edge
from typing import Iterable, List, Tuple


class Stynker:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.graph: defaultdict = defaultdict(set) # Node -> {set of Edges}
        self.reverse_graph: defaultdict = defaultdict(set) # Node -> {set of Nodes}
        self.current_cycle: int = 0
        self.period: str
        self.empty_nodes: List[Node] = list()

        self.edge_range: Tuple[int] = (1, 3)
        self.weight_range: Tuple[int] = (10, 20)
        self.length_range: Tuple[int] = (1, 3)

    def add_empty_node(self, node: Node) -> None:
        self.empty_nodes.append(node)

    def get_nodes(self) -> Iterable[Node]:
        return self.graph.keys()

    def get_empty_nodes(self) -> Iterable[Node]:
        # TODO: deprecate?
        empty_nodes = (
            node
            for node in self.get_nodes()
            if node.is_empty()
        )
        return empty_nodes

    def add_edge(self, node_1: Node, node_2: Node, **kwargs):
        edge = Edge(node_2, **kwargs)
        self.graph[node_1].add(edge)
        self.reverse_graph[node_2].add(node_1)

    def remake(self, nodes: Iterable[Node]) -> None:
        for node in nodes:
            print(f"Remaking node: {node}")
            # Remake node's attributes
            node.remake()
            # Remake edges
            self.remake_edges(node)

    def remake_edges(self, node: Node) -> None:
        # Delete existing edges from `node`
        del self.graph[node]
        for source_node in self.reverse_graph[node]:
            self.graph[source_node].remove(Edge(node))

        # Update reverse_graph
        del self.reverse_graph[node]

        for _ in range(randint(*self.edge_range)):
            # A node can be connected to itself?
            # Add edges from `node`
            destination_node = choice(list(self.get_nodes()))
            self.add_edge(
                node,
                destination_node,
                weight=randint(*self.weight_range),
                length=randint(*self.length_range),
            )

        # Using different loops since the number of
        # incoming/outcoming edges may be different
        for _ in range(randint(*self.edge_range)):
            # A node can be connected to itself?
            # # Add edges to `node`
            source_node = choice(list(self.get_nodes()))
            self.add_edge(
                source_node,
                node,
                weight=randint(*self.weight_range),
                length=randint(*self.length_range),
            )

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
        for node in self.empty_nodes:
            # This remake may be different 
            node.remake()

    def __repr__(self) -> str:
        repr_ = {
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
        repr_["nodes_info"] = nodes_info
        return json.dumps(repr_, indent=4)
