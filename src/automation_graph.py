from dataclasses import dataclass
from typing import Any, Dict, List, Set


@dataclass
class Node:
    name: str
    agent: Any
    depends_on: List[str]


class AutomationGraph:
    """Lightweight DAG runner."""

    def __init__(self, nodes: List[Node]) -> None:
        self.nodes = {node.name: node for node in nodes}

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        executed: Set[str] = set()

        while len(executed) < len(self.nodes):
            progressed = False
            for name, node in self.nodes.items():
                if name in executed:
                    continue
                if not set(node.depends_on).issubset(executed):
                    continue
                payload = node.agent.run(payload)
                executed.add(name)
                progressed = True
            if not progressed:
                unresolved = set(self.nodes.keys()) - executed
                raise RuntimeError(f"Circular or missing dependencies: {unresolved}")
        return payload


