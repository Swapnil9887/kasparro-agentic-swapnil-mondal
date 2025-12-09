import json
from pathlib import Path
from typing import Any, Dict

from src.agents.base import Agent
from src.models import Product


class DataIngestionAgent(Agent):
    """Parses raw product JSON into a normalized Product model."""

    def __init__(self, data_path: Path) -> None:
        super().__init__(name="data_ingestion_agent")
        self.data_path = data_path

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        del payload  # unused
        raw = json.loads(self.data_path.read_text(encoding="utf-8"))
        product = Product(
            name=raw["product_name"],
            concentration=raw["concentration"],
            skin_type=list(raw["skin_type"]),
            key_ingredients=list(raw["key_ingredients"]),
            benefits=list(raw["benefits"]),
            how_to_use=raw["how_to_use"],
            side_effects=list(raw["side_effects"]),
            price=raw["price"],
        )
        return {"product": product}


