import json
from typing import Dict, List, Tuple
from stynker import Stynker
from node import Node


def get_edges() -> List[Tuple[Node, Node, Dict[str, int]]]:
    # Create nodes as specified in the slides
    node_2: Node = Node(size=13, endo=1, name=2)
    node_5: Node = Node(size=17, endo=3, name=5)
    node_8: Node = Node(size=15, endo=2, name=8)
    node_11: Node = Node(size=15, endo=2, name=11)
    # Create edges as specified in the slides
    edge_info = [
        (node_11, node_2, {"weight": 1, "length": 2}),
        (node_2, node_11, {"weight": 1, "length": 1}),
        (node_2, node_8, {"weight": 2, "length": 1}),
        (node_5, node_2, {"weight": 3, "length": 2}),
        (node_5, node_11, {"weight": 1, "length": 1}),
        (node_5, node_8, {"weight": 1, "length": 3}),
        (node_8, node_5, {"weight": 3, "length": 1}),
    ]
    return edge_info


if __name__ == "__main__":
    # Initialize graph
    stynker = Stynker(
        n_nodes=1000,
        period="dream",
        n_remakes=10,
        n_input=5,
        n_output=5,
        random_sleep=False,
    )

    # Variable to save final results
    results = [json.loads(str(stynker))]
    for _ in range(100):
        stynker.run_cycle()
        results.append(json.loads(str(stynker)))

    # Run one sleep cycle
    stynker.period = "sleep"
    stynker.run_cycle()
    results.append(json.loads(str(stynker)))

    # Save results as json file
    with open("results.json", "w") as f:
        f.write(json.dumps(results, indent=2))
