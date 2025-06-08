# tests/memory/test_core.py

import pytest
from memory.core import MemoryCore

@pytest.fixture
def populated_memory():
    """Provides a MemoryCore instance pre-populated with a classic syllogism."""
    memory = MemoryCore()
    # Add the facts
    memory.add_relationship("Socrates", "human", "is_a")
    memory.add_relationship("human", "mortal", "is_a")
    # Add an attribute
    memory.add_node("Socrates", attributes={"born_in": "Athens"})
    return memory

def test_initialization():
    """Tests if the MemoryCore initializes without errors."""
    memory = MemoryCore()
    assert memory._graph is not None
    assert memory._graph.number_of_nodes() == 0

def test_add_relationship_and_nodes(populated_memory):
    """Tests if nodes and relationships are added correctly."""
    assert populated_memory._graph.has_node("Socrates")
    assert populated_memory._graph.has_node("human")
    assert populated_memory._graph.has_node("mortal")
    assert populated_memory._graph.has_edge("Socrates", "human")

def test_get_node_attributes(populated_memory):
    """Tests retrieving attributes from a node."""
    attrs = populated_memory.get_node_attributes("Socrates")
    assert attrs is not None
    assert attrs["born_in"] == "Athens"

def test_query_relationships(populated_memory):
    """Tests the querying of direct relationships."""
    result = populated_memory.query_relationships("Socrates", "is_a")
    assert result == ["human"]
    
    result_empty = populated_memory.query_relationships("Socrates", "causes")
    assert result_empty == []

def test_find_path_inference(populated_memory):
    """Tests the ability to find a path, demonstrating simple inference."""
    # This is the core test: Can the system infer Socrates is mortal?
    path = populated_memory.find_path("Socrates", "mortal")
    assert path is not None
    assert path == ["Socrates", "human", "mortal"]

def test_find_path_no_path(populated_memory):
    """Tests that no path is found where none exists."""
    # Add a disconnected concept
    populated_memory.add_node("logic")
    path = populated_memory.find_path("Socrates", "logic")
    assert path is None