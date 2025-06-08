# tests/meta/test_monitor.py

import pytest
from meta.monitor import MetacognitiveMonitor

def test_initialization():
    """Tests if the monitor initializes with an empty log."""
    monitor = MetacognitiveMonitor()
    assert monitor.get_chain_of_consciousness() == []
    assert "No events logged" in monitor.get_formatted_chain()

def test_log_single_event():
    """Tests if a single event is logged correctly."""
    monitor = MetacognitiveMonitor()
    params = {"source_id": "Socrates", "label": "is_a"}
    result = ["human"]
    
    monitor.log_event(
        module="MemoryCore",
        action="query_relationships",
        params=params,
        result=result
    )
    
    coc = monitor.get_chain_of_consciousness()
    assert len(coc) == 1
    event = coc[0]
    assert event["module"] == "MemoryCore"
    assert event["action"] == "query_relationships"
    assert event["params"] == params
    assert event["result"] == result

def test_get_formatted_chain():
    """Tests the human-readable formatting of the log."""
    monitor = MetacognitiveMonitor()
    monitor.log_event(
        module="CausalEngine",
        action="deduce_property",
        params={"source_id": "Socrates", "property_label": "mortal"},
        result=True
    )
    
    formatted_log = monitor.get_formatted_chain()
    assert "CausalEngine" in formatted_log
    assert "deduce_property" in formatted_log
    assert "Socrates" in formatted_log
    assert "mortal" in formatted_log
    assert "Result -> True" in formatted_log

def test_clear_log():
    """Tests if the log can be cleared."""
    monitor = MetacognitiveMonitor()
    monitor.log_event("TestModule", "test_action", {}, "test_result")
    assert len(monitor.get_chain_of_consciousness()) == 1
    
    monitor.clear_log()
    assert len(monitor.get_chain_of_consciousness()) == 0