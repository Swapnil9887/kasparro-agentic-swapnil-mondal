from abc import ABC, abstractmethod
from typing import Any, Dict


class Agent(ABC):
    """Base contract for all agents."""

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent with the given payload."""
        raise NotImplementedError


