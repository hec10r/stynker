import json
import math
import turtle
from collections import defaultdict
from random import choice, randint, sample, random
from .node import Node
from .edge import Edge
from typing import Iterable, Tuple
from constants import edge_constants, node_constants


class Stynker:
    """Main object that represents intelligent life"""
    def __init__(
        self,
        n_nodes: int,
        period: str,
        n_remakes: int,
        n_input: int,
        n_output: int,
        color: str,
        initial_position: Tuple[int, int] = (0, 0),
        show_route: bool = False,
        random_sleep: bool = False,
        **kwargs
    ) -> None:
        """
        Graph that represent an intelligent life

        Args:
            n_nodes: number of nodes to initialize the graph with.
                If -1, an empty graph is created
            period: name of the period to initialize the graph with.
                Must be one of the following: dream | sleep | wake
            n_remakes: number of nodes to remake in the sleep cycle
            n_input: number of node of type input
            n_output: number of node of type output
            random_sleep: if True, remake random nodes while in sleep cycle.
                If False, remake those with less damage
            **kwargs:
        """
        self.__dict__.update(kwargs)

        # Mind of the Stynker
        self.n_nodes = n_nodes
        self.period = period
        self.n_remakes = n_remakes
        self.random_sleep = random_sleep
        self.current_cycle: int = 0
        self.graph: defaultdict = defaultdict(set)  # Node -> {set of Edges}
        self.reverse_graph: defaultdict = defaultdict(set)  # Node -> {set of Nodes}
        self.nodes_dict = dict()

        # Body of the Stynker
        self.n_input = n_input
        self.n_output = n_output
        self.input_nodes = [i for i in range(self.n_input)]
        self.output_nodes = [i for i in range(self.n_input, self.n_input + self.n_output)]
        self.kick_dictionary = dict()

        # Create turtle object
        self.turtle = turtle.Turtle()
        self.turtle.color(color)
        self.turtle.shape("circle")
        if not show_route:
            self.turtle.penup()
        self.turtle.setposition(*initial_position)
        self.velocity_vector = (0, 0)
        self.vector_magnitude = 2.0
        # Radius of the Stynker
        self.radius = 10

        if self.n_nodes == -1:
            return

        # Make graph
        for i in range(self.n_nodes):
            # Mark first `n_input` nodes as input
            if i in self.input_nodes:
                node_type = "input"
            # Mark following `n_output` nodes as output
            elif i in self.output_nodes:
                node_type = "output"
                self.update_kick_dictionary(i)
            # Mark the rest as regular
            else:
                node_type = "regular"

            node = Node(
                name=i,
                size=randint(*node_constants["size_range"]),
                endo=randint(*node_constants["endo_range"]),
                node_type=node_type,
            )
            self.graph[node] = set()
            self.nodes_dict[i] = node

        # Make random outcoming edges
        for node in self.graph.keys():
            self.make_random_outcoming_edges(node)

    def run_cycle(self, **kwargs) -> None:
        """
        Depending on the `period` run the required logic
        """
        self.current_cycle += 1
        if self.period == "dream":
            self._run_dream_cycle(**kwargs)
        elif self.period == "sleep":
            self._run_sleep_cycle(**kwargs)
        elif self.period == "wake":
            self._run_wake_cycle(**kwargs)

    def _run_wake_cycle(self, **kwargs) -> None:
        """Run the wake cycle"""
        # Load nodes
        self.load_nodes()

        # Check nodes
        for node in self.get_nodes():
            # Check if the node is full
            if node.is_full():
                # Mark output node as active if it spills
                if node.is_output:
                    node.activate()
                # Spill full nodes
                node.spill()
                for edge in self.graph[node]:
                    # Load edges with trickles
                    edge.load()
            if node.is_output and node.is_active:
                self.kick(node.name)
                node.deactivate()

        # Move in the environment
        self.update_position()

    def _run_dream_cycle(self, **kwargs) -> None:
        """Run the dream cycle"""
        # Load nodes
        self.load_nodes()

        # Check nodes
        for node in self.get_nodes():
            # Check if the node is full
            if node.is_full():
                # Mark output node as active if it spills
                if node.is_output:
                    node.activate()
                # Spill full nodes
                node.spill()
                for edge in self.graph[node]:
                    # Load edges with trickles
                    edge.load()
            elif node.is_output:
                node.deactivate()

    def _run_sleep_cycle(self, **kwargs) -> None:
        """Run the sleep cycle"""
        if self.random_sleep:
            nodes_to_remake = sample(list(self.get_nodes()), self.n_remakes)
        else:
            # Sort list of nodes by damage
            damage_order = lambda node: node.damage
            ordered_nodes = sorted(
                [node for node in self.get_nodes()],
                key=damage_order
            )
            # Pick first n nodes with less damage
            nodes_to_remake = ordered_nodes[:self.n_remakes]

        # Remake selected nodes
        self.remake(nodes_to_remake)

        # Restart damage to 0
        for node in self.get_nodes():
            node.damage = 0

    def update_position(self, velocity_vector: Tuple[float, float] = None) -> None:
        """
        Updates the position of the Stynker. By default, uses the velocity_vector
        attribute, but receives an optional parameter to replace it.

        Note: this method does NOT overwrite the velocity_vector attribute
        Args:
            velocity_vector: optional parameter to move the Stynker in a different
                direction than its current velocity_vector
        """
        velocity_vector = velocity_vector or self.velocity_vector
        x, y = velocity_vector
        self.turtle.setx(self.turtle.xcor() + x)
        self.turtle.sety(self.turtle.ycor() + y)

    def load_nodes(self, **kwargs) -> None:
        """Run logic for loading nodes"""
        for node in self.get_nodes():
            # Load based on `endo`
            node.run_cycle()
            for edge in self.graph[node]:
                # Load based on incoming trickles
                edge.run_cycle()
            # Load based on input value
            if node.is_input and node.is_active:
                node.increase_level(10)
                node.deactivate()

    def kick(self, n: int) -> None:
        current_vector = self.velocity_vector
        kick_vector = self.kick_dictionary[n]
        new_vector_raw = (
            current_vector[0] + kick_vector[0],
            current_vector[1] + kick_vector[1]
        )
        # Normalize vector
        a, b = new_vector_raw
        norm = (a ** 2 + b ** 2) ** 0.5
        new_vector = (
            self.vector_magnitude * a / norm,
            self.vector_magnitude * b / norm
        )
        # Updates velocity vector
        self.velocity_vector = new_vector

    def update_kick_dictionary(self, i: int) -> None:
        """
        Updates the dictionary with the information about kick vector.
        Currently, the kick vectors are defined geometrically, by
        splitting a unitary circle in `self.n_output` equal parts
        and getting the normal vector from the center of the arc
        to the origin
        Args:
            i: node to update
        """
        j = self.output_nodes.index(i)
        # Calculate angle. It basically splits the circle
        # in `self.n_output` equal arcs, and get the angle
        # from the center of the arc with the x-axis
        alpha = 2 * math.pi * (j + 0.5) / self.n_output

        # Get kick vector. It is the vector from the middle
        # of the arc to the origin
        kick_vector = (
            -math.cos(alpha),
            -math.sin(alpha)
        )
        self.kick_dictionary[i] = kick_vector

    def add_edge(self, node_1: Node, node_2: Node, **kwargs) -> None:
        """
        Add an edge between two existing nodes with
        additional keyword arguments

        Args:
            node_1: source node
            node_2: destination node
            **kwargs: keywords to pass to the Edge constructor
        """
        edge = Edge(node_2, **kwargs)
        self.graph[node_1].add(edge)
        self.reverse_graph[node_2].add(node_1)

    def get_nodes(self) -> Iterable[Node]:
        """Return the nodes of the graph"""
        return sample(self.graph.keys(), self.n_nodes)

    def get_random_node(self, current_name: int) -> Node:
        """
        Get a random node except for a given one
        Args:
            current_name: integer that represents a node in the graph
        """
        options = [i for i in range(self.n_nodes) if i != current_name]
        random_number = choice(options)
        return self.nodes_dict[random_number]

    def activate_node(self, n: int) -> None:
        """
        Mark a given node as active if it is input or output
        Args:
            n: name of the node to activate
        """
        node = self.nodes_dict[n]
        node.activate()

    def remake(self, nodes: Iterable[Node]) -> None:
        """
        Remake a list of nodes using `Node.remake()` method
        Args:
            nodes: Iterable with instances of `Node`
        """
        for node in nodes:
            print(f"Remaking node: {node}")
            # Remake node's attributes
            node.remake()
            # Remake edges
            self.remake_edges(node)

    def remake_edges(self, node: Node) -> None:
        """
        Remake incoming and outcoming edges for `node`.
        Args:
            node: instance of `Node`
        """
        # Delete existing edges from `node`
        del self.graph[node]
        for source_node in self.reverse_graph[node]:
            # If two nodes: `a`, and `b` are being remake,
            # and there is an Edge between them, then this
            # will try to remove an Edge that was already
            # removed. Skipping this error
            try:
                self.graph[source_node].remove(Edge(node))
            except KeyError:
                pass

        # Clean reverse_graph
        self.reverse_graph[node] = set()

        # Add random edges from `node`
        self.make_random_outcoming_edges(node)

        # Add random edges to `node`
        self.make_random_incoming_edges(node)

    def make_random_outcoming_edges(self, node: Node) -> None:
        """
        For a given node, creates random outcoming edges to other nodes.
        The number of edges, the weight, and the length are chosen
        randomly from predefined ranges specified in the constants.py file
        Args:
            node: instance of `Node` to create edges from
        """
        n_edges = randint(*edge_constants["n_edges_range"])
        for _ in range(n_edges):
            destination_node = self.get_random_node(node.name)
            self.add_edge(
                node,
                destination_node,
                weight=randint(*edge_constants["weight_range"]),
                length=randint(*edge_constants["length_range"]),
            )

    def make_random_incoming_edges(self, node: Node) -> None:
        """
        For a given node, creates random incoming edges to the current node.
        The number of edges, the weight, and the length are chosen
        randomly from predefined ranges specified in the constants.py file
        Args:
            node: instance of `Node` to create edges to
        """
        n_edges = randint(*edge_constants["n_edges_range"])
        for _ in range(n_edges):
            source_node = self.get_random_node(node.name)
            self.add_edge(
                source_node,
                node,
                weight=randint(*edge_constants["weight_range"]),
                length=randint(*edge_constants["length_range"]),
            )

    def __repr__(self) -> str:
        """
        Overload the repr method to display useful information
        about the `Stynker`
        Returns:
            JSON representation of a `Stynker`
        """
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
