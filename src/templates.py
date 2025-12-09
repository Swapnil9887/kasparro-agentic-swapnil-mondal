"""Template definitions and registry bootstrap."""

from typing import Dict

from src import content_blocks
from src.template_engine import Template, TemplateEngine, TemplateField, TemplateRegistry


def build_registry() -> TemplateRegistry:
    registry = TemplateRegistry()

    faq_template = Template(
        name="faq_page",
        fields=[
            TemplateField("product", lambda ctx: {"name": ctx["product"].name}),
            TemplateField("faqs", lambda ctx: ctx["faqs"]),
        ],
    )

    product_template = Template(
        name="product_page",
        fields=[
            TemplateField("summary", lambda ctx: content_blocks.build_core_summary(ctx["product"])),
            TemplateField("benefits", lambda ctx: content_blocks.build_benefits_block(ctx["product"])),
            TemplateField("ingredients", lambda ctx: content_blocks.build_ingredient_block(ctx["product"])),
            TemplateField("usage", lambda ctx: content_blocks.build_usage_block(ctx["product"])),
            TemplateField("safety", lambda ctx: content_blocks.build_safety_block(ctx["product"])),
        ],
    )

    comparison_template = Template(
        name="comparison_page",
        fields=[
            TemplateField(
                "comparison",
                lambda ctx: content_blocks.build_comparison(ctx["product"], ctx["alternative"]),
            ),
            TemplateField(
                "who_should_choose_which",
                lambda ctx: {
                    "primary": "Choose GlowBoost for faster brightening and spot fading.",
                    "alternative": "Choose Product B if you want a gentler start with Vitamin C.",
                },
            ),
        ],
    )

    registry.register(faq_template)
    registry.register(product_template)
    registry.register(comparison_template)
    return registry


def build_engine() -> TemplateEngine:
    return TemplateEngine(build_registry())


