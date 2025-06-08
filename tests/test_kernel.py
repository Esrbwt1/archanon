# tests/test_kernel.py

import pytest
from kernel import ArchanonKernel

def test_kernel_initialization():
    """Tests if the kernel and its sub-modules initialize correctly."""
    kernel = ArchanonKernel()
    assert kernel.memory is not None
    assert kernel.causal is not None
    assert kernel.monitor is not None

def test_end_to_end_socrates_syllogism():
    """
    Tests the full end-to-end reasoning process:
    1. Add facts to memory.
    2. Ask a question that requires deduction.
    3. Verify the answer.
    4. Inspect the reasoning trace.
    """
    kernel = ArchanonKernel()

    # Step 1: Add facts
    kernel.add_fact("Socrates", "human", "is_a")
    kernel.add_fact("human", "mortal", "is_a")

    # Step 2: Ask a question
    is_mortal = kernel.ask_question("Socrates", "mortal")

    # Step 3: Verify the answer
    assert is_mortal is True

    # Step 4: Inspect the reasoning trace
    trace = kernel.get_reasoning_trace()
    print(f"\n--- Reasoning Trace ---\n{trace}\n---------------------")

    assert "MemoryCore" in trace
    assert "add_relationship" in trace
    assert "Socrates" in trace
    assert "human" in trace
    assert "CausalEngine" in trace
    assert "deduce_property" in trace
    assert "Result -> True" in trace

# tests/test_kernel.py

def test_kernel_reset():
    """Tests if the kernel's state can be fully reset."""
    kernel = ArchanonKernel()
    
    # Use the 'is_a' relationship that the Causal Engine understands
    kernel.add_fact("fact1", "fact2", "is_a")
    is_true = kernel.ask_question("fact1", "fact2")
    
    # Now, this assertion should pass
    assert is_true is True
    assert len(kernel.monitor.get_chain_of_consciousness()) > 1

    kernel.reset()
    
    # After reset, the fact should be gone
    is_true_after_reset = kernel.ask_question("fact1", "fact2")
    assert is_true_after_reset is False

    # The log should only contain the reset event and the last question
    trace = kernel.get_reasoning_trace()
    
    # Let's refine this assertion to be more precise
    log_events = kernel.monitor.get_chain_of_consciousness()
    assert len(log_events) == 2 # The reset event and the ask_question event
    assert log_events[0]['action'] == 'reset'
    assert "fact1" not in log_events[0]['params'] # Old facts should not be in the reset log