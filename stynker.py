import json
from collections import defaultdict
from random import randint, choice
from nodes import Node
from edge import Edge
from typing import Iterable, List
from constants import edge_constants, node_constants


class Stynker:
    def __init__(self, n_nodes: int, **kwargs):
        self.__dict__.update(kwargs)
        self.n_nodes = n_nodes
        self.current_cycle: int = 0
        self.graph: defaultdict = defaultdict(set) # Node -> {set of Edges}
        self.reverse_graph: defaultdict = defaultdict(set) # Node -> {set of Nodes}
        self.nodes_dict = dict()
        self.period: str


        # Make graph
        for i in range(self.n_nodes):
            node = Node(
                name=i,
                size=randint(*node_constants["size_range"]),
                endo=randint(*node_constants["endo_range"]),
            )
            self.graph[node] = set()
            self.nodes_dict[i] = node
            self.make_random_outcoming_edges(node)

    def get_nodes(self) -> Iterable[Node]:
        return self.graph.keys()

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

        # Clean reverse_graph
        self.reverse_graph[node] = set()

        # Add random edges from `node`
        self.make_random_outcoming_edges(node)

        # Add random edges to `node`
        self.make_random_incoming_edges(node)
        
    def make_random_outcoming_edges(self, node: Node) -> None:
        n_edges = randint(*edge_constants["n_edges_range"])
        for _ in range(n_edges):
            destination_node = self.get_random_node(node.name)
            self.add_edge(
                node,
                destination_node,
                weight=randint(*edge_constants["weight_range"]),
                length=randint(*edge_constants["length_range"]),
            )

    def make_random_incoming_edges(self, node):
        n_edges = randint(*edge_constants["n_edges_range"])
        for _ in range(n_edges):
            source_node = self.get_random_node(node.name)
            self.add_edge(
                source_node,
                node,
                weight=randint(*edge_constants["weight_range"]),
                length=randint(*edge_constants["length_range"]),
            )

    def get_random_node(self, current_name: int):
        options = [i for i in range(self.n_nodes) if i != current_name]
        random_number = choice(options)
        return self.nodes_dict[random_number]

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
                

    def _run_sleep_cycle(
        self,
        n_remakes: int = 1,
        select_random: bool = False
    ) -> None:
        if select_random:
            # TODO: Add support to this
            raise NotImplementedError
            nodes_to_remake = 1
        else:
            # Sort list of nodes by damage
            damage_order = lambda node: node.damage
            ordered_nodes = sorted(
                [node for node in self.get_nodes()],
                key=damage_order
            )
            # Pick first n nodes with less damage
            nodes_to_remake = ordered_nodes[:n_remakes]
        
        # Remake selected nodes
        self.remake(nodes_to_remake)

        # Restart damage to 0
        for node in self.get_nodes():
            node.damage = 0

    def _run_wake_cycle(self) -> None:
        # TODO: basically remake empty nodes
        # for node in self.empty_nodes:
            # This remake may be different 
            # node.remake()
        pass

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
