from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class Product:
    """Normalized product representation."""

    name: str
    concentration: str
    skin_type: List[str]
    key_ingredients: List[str]
    benefits: List[str]
    how_to_use: str
    side_effects: List[str]
    price: str


@dataclass
class Question:
    """User question with a category label."""

    text: str
    category: str


@dataclass
class QA:
    """FAQ entry."""

    question: str
    answer: str
    category: str


@dataclass
class Page:
    """Rendered page payload."""

    kind: str
    content: Dict[str, Any] = field(default_factory=dict)


