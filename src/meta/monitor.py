# src/meta/monitor.py

import datetime
from typing import List, Dict, Any

class MetacognitiveMonitor:
    """
    MetacognitiveMonitor v0.1: State Tracking & Introspection.

    This module acts as the system's internal observer. It logs every
    significant action taken by other modules to create a "Chain of
    Consciousness" (CoC). This provides a fully transparent and auditable
    record of the system's reasoning process.
    """

    def __init__(self):
        """Initializes the monitor with an empty log."""
        self._chain_of_consciousness: List[Dict[str, Any]] = []
        print("MetacognitiveMonitor v0.1 initialized.")

    def log_event(self, module: str, action: str, params: Dict[str, Any], result: Any):
        """
        Logs a single computational event.

        Args:
            module (str): The name of the module generating the event (e.g., "MemoryCore").
            action (str): The name of the function or method called (e.g., "add_relationship").
            params (dict): The parameters passed to the function.
            result (any): The result returned by the function.
        """
        event = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "module": module,
            "action": action,
            "params": params,
            "result": result
        }
        self._chain_of_consciousness.append(event)

    def get_chain_of_consciousness(self) -> List[Dict[str, Any]]:
        """Returns the raw, structured log of all events."""
        return self._chain_of_consciousness

    def get_formatted_chain(self) -> str:
        """Returns a human-readable string of the entire reasoning process."""
        if not self._chain_of_consciousness:
            return "No events logged."

        formatted_lines = []
        for event in self._chain_of_consciousness:
            ts = datetime.datetime.fromisoformat(event['timestamp']).strftime('%H:%M:%S.%f')[:-3]
            param_str = ", ".join(f"{k}={v}" for k, v in event['params'].items())
            line = f"[{ts}] {event['module']}: Called {event['action']}({param_str}). Result -> {event['result']}"
            formatted_lines.append(line)
        
        return "\n".join(formatted_lines)

    def clear_log(self):
        """Clears all events from the log."""
        self._chain_of_consciousness = []