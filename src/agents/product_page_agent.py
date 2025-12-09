from typing import Any, Dict

from src.agents.base import Agent
from src.models import Product
from src.template_engine import TemplateEngine


class ProductPageAgent(Agent):
    """Builds the product description page using templates and blocks."""

    def __init__(self, engine: TemplateEngine) -> None:
        super().__init__(name="product_page_agent")
        self.engine = engine

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        product: Product = payload["product"]
        rendered = self.engine.render(
            template_name="product_page",
            context={"product": product},
        )
        return {**payload, "product_page": rendered}


