"""Reusable content logic blocks that transform structured product data."""

from typing import Dict, List

from src.models import Product


def build_core_summary(product: Product) -> Dict[str, str]:
    """High-level summary block."""
    return {
        "name": product.name,
        "tagline": f"{product.concentration} serum formulated for {', '.join(product.skin_type)} skin.",
        "price": product.price,
    }


def build_usage_block(product: Product) -> Dict[str, str]:
    """Usage instructions block."""
    return {
        "how_to_use": product.how_to_use,
        "usage_tips": [
            "Use on clean, dry skin.",
            "Follow with moisturizer and sunscreen.",
            "Introduce gradually if skin is sensitive.",
        ],
    }


def build_safety_block(product: Product) -> Dict[str, List[str]]:
    """Safety and side-effects block."""
    return {
        "side_effects": product.side_effects,
        "safety_notes": [
            "Patch test before first use.",
            "Avoid mixing with strong exfoliants in the same routine.",
        ],
    }


def build_ingredient_block(product: Product) -> Dict[str, List[str]]:
    """Ingredient-oriented block."""
    return {
        "key_ingredients": product.key_ingredients,
        "ingredient_focus": [
            "Vitamin C supports brightening and even tone.",
            "Hyaluronic Acid supports hydration without heaviness.",
        ],
    }


def build_benefits_block(product: Product) -> Dict[str, List[str]]:
    """Benefit claims block."""
    return {
        "benefits": product.benefits,
        "ideal_for": product.skin_type,
    }


def build_comparison(product_a: Product, product_b: Product) -> Dict[str, Dict[str, str]]:
    """Comparison block between two products."""
    return {
        "products": {
            "primary": {
                "name": product_a.name,
                "concentration": product_a.concentration,
                "key_ingredients": product_a.key_ingredients,
                "benefits": product_a.benefits,
                "price": product_a.price,
            },
            "alternative": {
                "name": product_b.name,
                "concentration": product_b.concentration,
                "key_ingredients": product_b.key_ingredients,
                "benefits": product_b.benefits,
                "price": product_b.price,
            },
        },
        "recommendation_logic": [
            "Pick the primary serum for brightening and spot fading with lightweight feel.",
            "Pick the alternative for first-time Vitamin C users wanting lower strength with added soothing.",
        ],
    }


