# src/memory/core.py

import networkx as nx
from typing import List, Tuple, Dict, Any, Optional

class MemoryCore:
    """
    MemoryCore v0.1: The Explicit Graph.

    This class manages the foundational knowledge graph of ARCHANON.
    It stores concepts as nodes and explicit relationships as directed, labeled edges.
    
    - Nodes represent concepts (e.g., "Socrates", "human").
    - Edges represent relationships (e.g., "is_a", "has_property").
    """

    def __init__(self):
        """Initializes the MemoryCore with an empty directed graph."""
        self._graph = nx.DiGraph()
        print("MemoryCore v0.1 initialized.")

    def add_node(self, node_id: str, attributes: Optional[Dict[str, Any]] = None):
        """
        Adds a concept node to the memory graph.
        If the node already exists, it updates its attributes.
        
        Args:
            node_id (str): The unique identifier for the concept.
            attributes (dict, optional): A dictionary of properties for the node.
        """
        if attributes is None:
            attributes = {}
        self._graph.add_node(node_id, **attributes)

    def add_relationship(self, source_id: str, target_id: str, label: str):
        """
        Adds a directed, labeled relationship between two nodes.
        If the nodes do not exist, they are created automatically.

        Args:
            source_id (str): The starting node of the relationship.
            target_id (str): The ending node of the relationship.
            label (str): The type of relationship (e.g., "is_a", "causes").
        """
        self._graph.add_edge(source_id, target_id, label=label)

    def query_relationships(self, source_id: str, label: str) -> List[str]:
        """
        Finds all nodes connected from a source node by a specific relationship label.

        Example: query_relationships("Socrates", "is_a") -> ["human"]

        Args:
            source_id (str): The node to start the query from.
            label (str): The relationship label to filter by.

        Returns:
            A list of target node IDs.
        """
        if not self._graph.has_node(source_id):
            return []
        
        targets = []
        for _, target, data in self._graph.out_edges(source_id, data=True):
            if data.get("label") == label:
                targets.append(target)
        return targets

    def find_path(self, source_id: str, target_id: str) -> Optional[List[str]]:
        """
        Finds the shortest path of concepts connecting a source to a target.
        This demonstrates basic inferential chaining.

        Args:
            source_id (str): The starting node.
            target_id (str): The ending node.

        Returns:
            A list of node IDs representing the path, or None if no path exists.
        """
        try:
            path = nx.shortest_path(self._graph, source=source_id, target=target_id)
            return path
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return None

    def get_node_attributes(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves the attributes of a specific node."""
        if self._graph.has_node(node_id):
            return self._graph.nodes[node_id]
        return None