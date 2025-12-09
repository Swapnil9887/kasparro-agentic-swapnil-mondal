from typing import Any, Dict

from src.agents.base import Agent
from src.models import Product
from src.template_engine import TemplateEngine


class ComparisonAgent(Agent):
    """Creates a comparison page between the primary serum and a fictional alternative."""

    def __init__(self, engine: TemplateEngine) -> None:
        super().__init__(name="comparison_agent")
        self.engine = engine
        self.alternative = Product(
            name="CalmRadiance Gentle C Serum",
            concentration="5% Vitamin C",
            skin_type=["Sensitive", "Combination"],
            key_ingredients=["Vitamin C", "Aloe", "Hyaluronic Acid"],
            benefits=["Gradual brightening", "Soothing hydration"],
            how_to_use="Apply 2–3 drops in the evening on clean skin.",
            side_effects=["Rare mild tingling"],
            price="₹549",
        )

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        product: Product = payload["product"]
        rendered = self.engine.render(
            template_name="comparison_page",
            context={"product": product, "alternative": self.alternative},
        )
        payload["comparison_page"] = rendered
        payload["alternative"] = self.alternative
        return payload


