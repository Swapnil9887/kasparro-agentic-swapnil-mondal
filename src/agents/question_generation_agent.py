from typing import Any, Dict, List

from src.agents.base import Agent
from src.models import Product, Question


class QuestionGenerationAgent(Agent):
    """Generates categorized user questions from product context."""

    def __init__(self) -> None:
        super().__init__(name="question_generation_agent")

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        product: Product = payload["product"]
        questions: List[Question] = []

        info_questions = [
            f"What does {product.name} do for the skin?",
            f"Is the {product.concentration} level gentle enough for daily use?",
            f"How long until I see results from {product.name}?",
        ]

        usage_questions = [
            f"How should I apply {product.name} in my routine?",
            "Can I layer this serum with moisturizer and sunscreen?",
            f"How many drops of {product.name} should I use each time?",
            f"Should I use {product.name} in the morning or at night?",
        ]

        safety_questions = [
            f"Is {product.name} suitable for {', '.join(product.skin_type)} skin?",
            "Will this serum cause purging or breakouts?",
            "What side effects should I watch out for?",
            "Do I need to patch test before using this serum?",
        ]

        purchase_questions = [
            f"What is the price of {product.name}?",
            "Does the serum come in a dropper bottle?",
            "Is the formula lightweight and non-sticky?",
        ]

        comparison_questions = [
            f"How does {product.name} compare to another Vitamin C serum?",
            "Which serum is better for beginners with sensitive skin?",
        ]

        def to_objects(items: List[str], category: str) -> List[Question]:
            return [Question(text=item, category=category) for item in items]

        questions.extend(to_objects(info_questions, "Informational"))
        questions.extend(to_objects(usage_questions, "Usage"))
        questions.extend(to_objects(safety_questions, "Safety"))
        questions.extend(to_objects(purchase_questions, "Purchase"))
        questions.extend(to_objects(comparison_questions, "Comparison"))

        return {"product": product, "questions": questions}


