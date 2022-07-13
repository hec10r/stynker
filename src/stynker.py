import json
import math
import turtle
from collections import defaultdict
from copy import deepcopy
from random import choice, randint, random, sample
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
        vector_magnitude: float = 2.0,
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

        # Create "body" of the Stynker: turtle object
        self.turtle = turtle.Turtle()
        self.turtle.color(color)
        self.turtle.shape("circle")
        self.show_route = show_route
        if not self.show_route:
            self.turtle.penup()
        self.initial_position = initial_position
        self.turtle.setposition(*self.initial_position)
        self.vector_magnitude = vector_magnitude
        self.velocity_vector = (0, 0)
        # Radius of the Stynker
        self.radius = 10

        # Create "mind" of the Stynker
        self.n_nodes = n_nodes
        self.period = period
        self.n_remakes = n_remakes
        self.random_sleep = random_sleep
        self.current_cycle: int = 0
        self.graph: defaultdict = defaultdict(set)  # Node -> {set of Edges}
        self.reverse_graph: defaultdict = defaultdict(set)  # Node -> {set of Nodes}
        self.nodes_dict = dict()

        # Input/output logic
        self.n_input = n_input
        self.n_output = n_output
        self.input_nodes = list()
        self.output_nodes = list()
        self.kick_dictionary = dict()
        self.input_points = dict()

        # When the n_nodes is equal to -1, no graph is created
        if self.n_nodes == -1:
            return

        if (self.n_input + self.n_output) > self.n_nodes:
            raise ValueError(
                "The total number of nodes must be greater or equal"
                "than the sum of the input and output nodes"
            )

        if self.n_input % 2:
            raise ValueError(
                "The number of input nodes must be even, since currently"
                "they are defined as two rings"
            )

        # Make graph
        for i in range(self.n_nodes):
            # Mark first `n_input` nodes as input
            if i in range(n_input):
                node_type = "input"
                # The input points are defined as two rings.
                # One defined by the radius and the other by twice
                # the radius. The first `self.n_input / 2` nodes are
                # in the inner ring, and the others in the outer

                # If 1: inner, if 2: outer
                in_out = (i // (self.n_input / 2) + 1)

                # Get the angle
                alpha = 2 * math.pi * i * 2 / self.n_input

                # Get point coordinates
                input_point = (
                    round(in_out * self.radius * math.cos(alpha), 5),
                    round(in_out * self.radius * math.sin(alpha), 5)
                )
                self.input_points[i] = input_point
            # Mark following `n_output` nodes as output
            elif i in range(n_input, n_input + n_output):
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
        x_vector, y_vector = self.velocity_vector

        # Load nodes
        self.load_nodes()

        # Check nodes
        for node in self.get_nodes():
            # Check if the node is full
            if node.is_full():
                # Mark output node as active if it spills
                if node.is_output:
                    kick_vector = self.kick_dictionary[node.name]
                    x_vector += kick_vector[0]
                    y_vector += kick_vector[1]
                # Spill full nodes
                node.spill()
                for edge in self.graph[node]:
                    # Load edges with trickles
                    edge.load()
        self.velocity_vector = (x_vector, y_vector)

    def _run_dream_cycle(self, **kwargs) -> None:
        """Run the dream cycle"""
        # Load nodes
        self.load_nodes()

        # Check nodes
        for node in self.get_nodes():
            # Check if the node is full
            if node.is_full():
                # Spill full nodes
                node.spill()
                for edge in self.graph[node]:
                    # Load edges with trickles
                    edge.load()

    def _run_sleep_cycle(self, **kwargs) -> None:
        """Run the sleep cycle"""
        if self.random_sleep:
            nodes_to_remake = sample(list(self.get_nodes()), self.n_remakes)
        else:
            # Sort list of nodes by damage
            damage_order = lambda node: (node.damage, node.name)
            ordered_nodes = sorted(
                [node for node in self.get_nodes()],
                key=damage_order
            )
            # Pick first n nodes with less damage
            nodes_to_remake = ordered_nodes[:self.n_remakes]

        # Remake selected nodes
        self.remake(nodes_to_remake)

        # Restart damage to 0
        self.reset_damage()

    def reset_damage(self) -> None:
        """Set the damage from all nodes to 0"""
        for node in self.get_nodes():
            node.damage = 0

    def move(self, velocity_vector: Tuple[float, float] = None) -> None:
        """
        Updates the position of the Stynker. By default, uses the velocity_vector
        attribute, but receives an optional parameter to replace it.

        Note: this method does NOT overwrite the velocity_vector attribute
        Args:
            velocity_vector: optional parameter to move the Stynker in a different
                direction than its current velocity_vector
        """
        velocity_vector = velocity_vector or self.velocity_vector
        dx, dy = velocity_vector
        self.update_position(self.turtle.xcor() + dx, self.turtle.ycor() + dy)

    def update_position(self, x: float, y: float) -> None:
        """
        Change the position of the Stynker to (x, y)
        Args:
            x: new x coordinate
            y: new y coordinate
        """
        self.turtle.setx(x)
        self.turtle.sety(y)

    def update_velocity_vector(self, new_vector: Tuple[float, float]) -> None:
        """
        Updates the velocity vector. Uses the direction from new_vector,
        but keeps the magnitude* as specified in `self.vector_magnitude`.
        *Except when `new_vector` is (0, 0), then the velocity vector
        becomes (0, 0)
        Args:
            new_vector: vector with the desired direction
        """
        a, b = new_vector
        norm = math.sqrt(a ** 2 + b ** 2)
        if norm == 0:
            self.velocity_vector = (0, 0)
            return
        self.velocity_vector = (
            round(self.vector_magnitude * a / norm, 6),
            round(self.vector_magnitude * b / norm, 6)
        )

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
        """
        Change the direction of the velocity_vector based on the logic
        described in the kick_dictionary
        Args:
            n: output node that was triggered
        """
        current_vector = self.velocity_vector
        kick_vector = self.kick_dictionary[n]
        new_vector = (
            current_vector[0] + kick_vector[0],
            current_vector[1] + kick_vector[1]
        )
        # Updates velocity vector
        self.update_velocity_vector(new_vector)

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
        j = i - self.n_input
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
        return self.graph.keys()

    def get_random_node(self, current_name: int) -> Node:
        """
        Get a random node except for a given one
        Args:
            current_name: integer that represents a node in the graph
        """
        options = [i.name for i in self.graph.keys() if i.name != current_name]
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

    def reset_position(self):
        """
        Move back the Stynker to the initial position without drawing
        """
        self.turtle.penup()
        self.turtle.setposition(self.initial_position)
        if self.show_route:
            self.turtle.pendown()

    def reset_vector(self):
        """
        Change velocity vector to (0, 0)
        """
        self.update_velocity_vector((0, 0))

    def clone_from(self, stk, **kwargs) -> None:
        """
        Redesign the current Stynker based on other
        Args:
            stk: Stynker to clone from
            **kwargs: Additional key word arguments
        """
        self.reset_position()
        self.n_nodes = stk.n_nodes
        self.graph = deepcopy(stk.graph)
        self.reverse_graph = deepcopy(stk.reverse_graph)
        self.nodes_dict = deepcopy(stk.nodes_dict)
        self.kick_dictionary = deepcopy(stk.kick_dictionary)
        self.__dict__.update(kwargs)

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
            "position": self.turtle.position(),
            "velocity": self.velocity_vector,
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
