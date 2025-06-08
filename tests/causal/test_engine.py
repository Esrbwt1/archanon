# tests/causal/test_engine.py

import pytest
from memory.core import MemoryCore
from causal.engine import CausalEngine

@pytest.fixture
def reasoning_setup():
    """Provides a MemoryCore and a CausalEngine for testing."""
    memory = MemoryCore()
    # Fact: Socrates is a human.
    memory.add_relationship("Socrates", "human", "is_a")
    # Fact: A human is a mammal.
    memory.add_relationship("human", "mammal", "is_a")
    # Fact: A mammal is an animal.
    memory.add_relationship("mammal", "animal", "is_a")
    # Fact: An animal is mortal.
    memory.add_relationship("animal", "mortal", "is_a")

    # Add a different branch for negative testing
    memory.add_relationship("stone", "inanimate", "is_a")

    engine = CausalEngine(memory)
    return memory, engine

def test_initialization(reasoning_setup):
    """Tests that the engine initializes correctly."""
    _, engine = reasoning_setup
    assert engine._memory is not None

def test_deduce_direct_property(reasoning_setup):
    """Tests deduction of a direct parent property."""
    _, engine = reasoning_setup
    assert engine.deduce_property("Socrates", "human") is True

def test_deduce_inherited_property_long_chain(reasoning_setup):
    """Tests deduction over a multi-step inheritance chain."""
    _, engine = reasoning_setup
    # The core test: Can the engine deduce that Socrates is mortal?
    assert engine.deduce_property("Socrates", "mortal") is True

def test_deduce_inherited_property_mid_chain(reasoning_setup):
    """Tests deduction to a property in the middle of the chain."""
    _, engine = reasoning_setup
    assert engine.deduce_property("Socrates", "mammal") is True

def test_deduce_false_property(reasoning_setup):
    """Tests that a false property is not deduced."""
    _, engine = reasoning_setup
    assert engine.deduce_property("Socrates", "inanimate") is False

def test_deduce_on_unrelated_node(reasoning_setup):
    """Tests deduction on a node from a completely different branch."""
    _, engine = reasoning_setup
    assert engine.deduce_property("stone", "mortal") is False

def test_deduce_on_nonexistent_node(reasoning_setup):
    """Tests behavior with a node that does not exist in memory."""
    _, engine = reasoning_setup
    assert engine.deduce_property("Plato", "mortal") is False