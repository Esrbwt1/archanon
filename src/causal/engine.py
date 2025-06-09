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

    # In src/causal/engine.py

    def deduce_property(self, source_id: str, property_label: str) -> bool:
        """
        Deduces if a node has a property, either directly or via inheritance.
        v1.1: Now checks for direct 'has_property' relationships first.

        Args:
            source_id (str): The starting node (e.g., "Socrates", "The cat").
            property_label (str): The property we are checking for (e.g., "mortal", "fluffy").

        Returns:
            True if the property is held, False otherwise.
        """
        # --- NEW: Step 1: Check for direct properties ---
        direct_properties = self._memory.query_relationships(source_id, "has_property")
        if property_label in direct_properties:
            return True # Found a direct property, reasoning is complete.

        # --- EXISTING: Step 2: Check for inherited properties via 'is_a' ---
        # First, check if the node itself is the property (e.g., ask_question("cat", "animal"))
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
                    return True  # Found the property via inheritance
                
                if parent not in visited_nodes:
                    visited_nodes.add(parent)
                    nodes_to_visit.append(parent)
        
        return False # Checked direct and inherited properties, found nothing.