# src/causal/engine.py

from memory.core import MemoryCore
from typing import List, Optional

class CausalEngine:
    """
    CausalEngine v0.1: Logical Inference.

    This engine performs basic logical deductions on the knowledge graph
    stored in the MemoryCore. Its initial capability is property inheritance.
    """

    def __init__(self, memory_core: MemoryCore):
        """
        Initializes the CausalEngine with a reference to a MemoryCore instance.

        Args:
            memory_core (MemoryCore): The memory system to reason over.
        """
        self._memory = memory_core
        print("CausalEngine v0.1 initialized.")

    def deduce_property(self, source_id: str, property_label: str) -> bool:
        """
        Deduces if a node inherits a property through 'is_a' relationships.

        This method traverses the graph upwards from the source_id along 'is_a'
        edges. If it finds a parent node that has the target property, it
        returns True.

        Example:
        - Graph: Socrates -> is_a -> human -> is_a -> mortal
        - Query: deduce_property("Socrates", "mortal")
        - Result: True

        Args:
            source_id (str): The starting node (e.g., "Socrates").
            property_label (str): The property we are checking for (e.g., "mortal").

        Returns:
            True if the property is inherited, False otherwise.
        """
        # First, check if the node itself is the property.
        if source_id == property_label:
            return True

        # Use a queue for a breadth-first search up the 'is_a' hierarchy.
        nodes_to_visit = [source_id]
        visited_nodes = {source_id}

        while nodes_to_visit:
            current_node = nodes_to_visit.pop(0)

            # Query the memory for parents in the 'is_a' hierarchy.
            parents = self._memory.query_relationships(current_node, "is_a")
            for parent in parents:
                if parent == property_label:
                    return True  # Found the property
                
                if parent not in visited_nodes:
                    visited_nodes.add(parent)
                    nodes_to_visit.append(parent)
        
        return False # Traversed the whole relevant hierarchy and didn't find the property.