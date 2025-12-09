from typing import Any, Dict, List

from src.agents.base import Agent
from src.models import Product, QA, Question
from src.template_engine import TemplateEngine


class FaqAgent(Agent):
    """Turns questions into structured FAQs using deterministic logic."""

    def __init__(self, engine: TemplateEngine) -> None:
        super().__init__(name="faq_agent")
        self.engine = engine

    def _answer(self, question: Question, product: Product) -> str:
        if question.category == "Informational":
            return (
                f"{product.name} uses {product.concentration} with {', '.join(product.key_ingredients)} "
                f"to deliver {', '.join(product.benefits).lower()}."
            )
        if question.category == "Usage":
            return f"{product.how_to_use} Use on clean skin and seal with moisturizer plus sunscreen."
        if question.category == "Safety":
            return (
                f"Designed for {', '.join(product.skin_type)} skin. Side effects can include "
                f"{', '.join(product.side_effects)}. Patch test before full use."
            )
        if question.category == "Purchase":
            return f"The serum is priced at {product.price} and has a lightweight, non-sticky texture."
        if question.category == "Comparison":
            return (
                "GlowBoost focuses on brightening and fading spots. Compare concentration, price, "
                "and soothing ingredients when choosing an alternative."
            )
        return "Information unavailable."

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        product: Product = payload["product"]
        questions: List[Question] = payload["questions"]

        faqs: List[Dict[str, str]] = []
        for q in questions:
            answer = self._answer(q, product)
            faqs.append(QA(question=q.text, answer=answer, category=q.category).__dict__)

        rendered = self.engine.render(
            template_name="faq_page",
            context={"product": product, "faqs": faqs},
        )
        return {"product": product, "questions": questions, "faq_page": rendered}


