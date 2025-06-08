# src/kernel.py

from memory.core import MemoryCore
from causal.engine import CausalEngine
from meta.monitor import MetacognitiveMonitor
from typing import List, Optional, Dict, Any

class ArchanonKernel:
    """
    ArchanonKernel v1.0: The Integrated Cognitive Core.

    This class acts as a facade, integrating the MemoryCore, CausalEngine,
    and MetacognitiveMonitor into a single, cohesive system. It provides
    high-level methods for interacting with the AGI core and ensures that
    all actions are monitored and logged.
    """

    def __init__(self):
        """Initializes all sub-modules of the cognitive kernel."""
        self.memory = MemoryCore()
        self.causal = CausalEngine(self.memory)
        self.monitor = MetacognitiveMonitor()
        print("ArchanonKernel v1.0 initialized and online.")

    def _log(self, module: str, action: str, params: Dict[str, Any], result: Any):
        """A helper method to standardize logging."""
        self.monitor.log_event(module, action, params, result)

    def add_fact(self, source_id: str, target_id: str, label: str):
        """
        Adds a factual relationship to memory and logs the action.

        Example: kernel.add_fact("Socrates", "human", "is_a")
        """
        params = {"source_id": source_id, "target_id": target_id, "label": label}
        self.memory.add_relationship(source_id, target_id, label)
        # Log this event after it has been executed.
        self._log("MemoryCore", "add_relationship", params, "Success")

    def ask_question(self, source_id: str, property_label: str) -> bool:
        """
        Asks the kernel if a node has a certain property, using causal deduction.
        The entire process is logged.

        Example: kernel.ask_question("Socrates", "mortal") -> True

        Returns:
            The boolean result of the deduction.
        """
        params = {"source_id": source_id, "property_label": property_label}
        result = self.causal.deduce_property(source_id, property_label)
        # Log this event after it has been executed.
        self._log("CausalEngine", "deduce_property", params, result)
        return result

    def get_reasoning_trace(self) -> str:
        """
        Returns the full, human-readable Chain of Consciousness for the last
        set of operations.
        """
        return self.monitor.get_formatted_chain()

    def reset(self):
        """Resets the kernel's memory and log to a clean state."""
        self.memory = MemoryCore()
        self.causal = CausalEngine(self.memory)
        self.monitor.clear_log()
        self._log("ArchanonKernel", "reset", {}, "System reset to initial state.")