"""LangChain tools for content generation logic blocks."""

from typing import Dict, List

from langchain.tools import tool
from pydantic import BaseModel, Field

from src.models import Product


class ProductInput(BaseModel):
    """Input schema for product-based tools."""

    product: Dict = Field(description="Product data dictionary")


class ComparisonInput(BaseModel):
    """Input schema for comparison tools."""

    product_a: Dict = Field(description="First product data")
    product_b: Dict = Field(description="Second product data")


@tool
def build_core_summary(product: Dict) -> Dict[str, str]:
    """Builds a high-level product summary with name, tagline, and price."""
    p = Product(**product)
    return {
        "name": p.name,
        "tagline": f"{p.concentration} serum formulated for {', '.join(p.skin_type)} skin.",
        "price": p.price,
    }


@tool
def build_usage_block(product: Dict) -> Dict[str, str]:
    """Builds usage instructions block with how-to-use and tips."""
    p = Product(**product)
    return {
        "how_to_use": p.how_to_use,
        "usage_tips": [
            "Use on clean, dry skin.",
            "Follow with moisturizer and sunscreen.",
            "Introduce gradually if skin is sensitive.",
        ],
    }


@tool
def build_safety_block(product: Dict) -> Dict[str, List[str]]:
    """Builds safety and side-effects information block."""
    p = Product(**product)
    return {
        "side_effects": p.side_effects,
        "safety_notes": [
            "Patch test before first use.",
            "Avoid mixing with strong exfoliants in the same routine.",
        ],
    }


@tool
def build_ingredient_block(product: Dict) -> Dict[str, List[str]]:
    """Builds ingredient-focused content block."""
    p = Product(**product)
    return {
        "key_ingredients": p.key_ingredients,
        "ingredient_focus": [
            "Vitamin C supports brightening and even tone.",
            "Hyaluronic Acid supports hydration without heaviness.",
        ],
    }


@tool
def build_benefits_block(product: Dict) -> Dict[str, List[str]]:
    """Builds benefits and ideal-for information block."""
    p = Product(**product)
    return {
        "benefits": p.benefits,
        "ideal_for": p.skin_type,
    }


@tool
def build_comparison_block(product_a: Dict, product_b: Dict) -> Dict:
    """Builds comparison block between two products."""
    p_a = Product(**product_a)
    p_b = Product(**product_b)
    return {
        "products": {
            "primary": {
                "name": p_a.name,
                "concentration": p_a.concentration,
                "key_ingredients": p_a.key_ingredients,
                "benefits": p_a.benefits,
                "price": p_a.price,
            },
            "alternative": {
                "name": p_b.name,
                "concentration": p_b.concentration,
                "key_ingredients": p_b.key_ingredients,
                "benefits": p_b.benefits,
                "price": p_b.price,
            },
        },
        "recommendation_logic": [
            "Pick the primary serum for brightening and spot fading with lightweight feel.",
            "Pick the alternative for first-time Vitamin C users wanting lower strength with added soothing.",
        ],
    }


def get_all_tools():
    """Returns all available content generation tools."""
    return [
        build_core_summary,
        build_usage_block,
        build_safety_block,
        build_ingredient_block,
        build_benefits_block,
        build_comparison_block,
    ]

