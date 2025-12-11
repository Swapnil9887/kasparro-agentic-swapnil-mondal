"""LangChain-based agents for the content generation system."""

import json
from pathlib import Path
from typing import Any, Dict, List

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from src.models import Product, QA, Question
from src.tools import get_all_tools


class DataIngestionAgent:
    """Agent that parses and validates product data."""

    def __init__(self, data_path: Path):
        self.data_path = data_path

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Load and parse product data into internal model."""
        data = json.loads(self.data_path.read_text())
        product = Product(**data)
        # Store as dict for LangGraph state compatibility
        return {**state, "product": product.__dict__}


class QuestionGenerationAgent:
    """Agent that generates categorized user questions using LLM."""

    def __init__(self):
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a question generation agent. Given product information, generate at least 15 user questions across these categories:
- Informational: Questions about what the product does, how it works, ingredients
- Safety: Questions about side effects, skin compatibility, precautions
- Usage: Questions about how to apply, when to use, routine integration
- Purchase: Questions about price, packaging, availability
- Comparison: Questions comparing this product to alternatives

Return ONLY a JSON array of objects with "text" and "category" fields. Example:
[{"text": "What does this product do?", "category": "Informational"}, ...]""",
                ),
                ("human", "Product: {product_info}\n\nGenerate categorized questions:"),
            ]
        )
        chain = prompt | llm
        self.chain = chain

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate questions from product data."""
        product_dict = state["product"]
        product = Product(**product_dict)
        product_info = f"""
Name: {product.name}
Concentration: {product.concentration}
Skin Type: {', '.join(product.skin_type)}
Ingredients: {', '.join(product.key_ingredients)}
Benefits: {', '.join(product.benefits)}
How to Use: {product.how_to_use}
Side Effects: {', '.join(product.side_effects)}
Price: {product.price}
"""
        response = self.chain.invoke({"product_info": product_info})
        content = response.content.strip()
        # Extract JSON from markdown code blocks if present
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        questions_data = json.loads(content)
        questions = [Question(**q) for q in questions_data]
        # Store as list of dicts for LangGraph state compatibility
        return {**state, "questions": [q.__dict__ for q in questions]}


class FaqAgent:
    """Agent that generates FAQ answers using LLM."""

    def __init__(self):
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are an FAQ generation agent. Given a product and a list of questions, generate accurate, helpful answers.

Rules:
- Use ONLY the provided product information - do not invent facts
- Answers should be concise but informative
- Match the tone and category of each question
- For Safety questions, emphasize patch testing and precautions
- For Usage questions, provide clear step-by-step guidance
- For Comparison questions, focus on what makes this product unique

Return ONLY a JSON array of FAQ objects with "question", "answer", and "category" fields. Example:
[{"question": "What does this product do?", "answer": "...", "category": "Informational"}, ...]""",
                ),
                ("human", "Product: {product_info}\n\nQuestions: {questions}\n\nGenerate FAQ answers as JSON array:"),
            ]
        )
        self.chain = prompt | llm

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate FAQ answers for questions."""
        product_dict = state["product"]
        product = Product(**product_dict)
        questions_data = state["questions"]
        questions = [Question(**q) for q in questions_data]

        product_info = f"""
Name: {product.name}
Concentration: {product.concentration}
Skin Type: {', '.join(product.skin_type)}
Ingredients: {', '.join(product.key_ingredients)}
Benefits: {', '.join(product.benefits)}
How to Use: {product.how_to_use}
Side Effects: {', '.join(product.side_effects)}
Price: {product.price}
"""
        questions_text = "\n".join([f"- [{q.category}] {q.text}" for q in questions])

        # Generate answers using LLM chain
        response = self.chain.invoke(
            {
                "product_info": product_info,
                "questions": questions_text,
            }
        )
        answer_text = response.content.strip()

        # Parse LLM response to extract FAQs
        # Try to extract JSON from response
        if "```json" in answer_text:
            answer_text = answer_text.split("```json")[1].split("```")[0].strip()
        elif "```" in answer_text:
            answer_text = answer_text.split("```")[1].split("```")[0].strip()

        try:
            faqs_data = json.loads(answer_text)
        except json.JSONDecodeError:
            # Fallback: create FAQs from questions with generated answers
            faqs_data = []
            for q in questions:
                # Use a simpler prompt for individual answers
                simple_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
                answer_prompt = ChatPromptTemplate.from_messages(
                    [
                        (
                            "system",
                            "Answer this question about the product using ONLY the provided information. Be concise.",
                        ),
                        ("human", "Product: {product_info}\n\nQuestion: {question}\n\nAnswer:"),
                    ]
                )
                answer_chain = answer_prompt | simple_llm
                answer_response = answer_chain.invoke({"product_info": product_info, "question": q.text})
                answer = answer_response.content.strip()
                faqs_data.append({"question": q.text, "answer": answer, "category": q.category})

        faqs = [QA(**faq) for faq in faqs_data]
        faq_page = {
            "template": "faq_page",
            "product": {"name": product.name},
            "faqs": [faq.__dict__ for faq in faqs],
        }
        return {**state, "faqs": [faq.__dict__ for faq in faqs], "faq_page": faq_page}


class ProductPageAgent:
    """Agent that generates product page using tools and LLM."""

    def __init__(self):
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
        tools = get_all_tools()
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a product page generation agent. Use the available tools to build structured content blocks, then assemble them into a complete product page.

Use these tools:
- build_core_summary: Get name, tagline, price
- build_benefits_block: Get benefits and ideal_for
- build_ingredient_block: Get ingredients and their focus
- build_usage_block: Get usage instructions
- build_safety_block: Get safety information

After using tools, assemble the results into a JSON structure matching the product_page template.""",
                ),
                ("human", "Product data: {product_dict}\n\nGenerate product page:"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )
        agent = create_openai_tools_agent(llm, tools, prompt)
        self.executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate product page."""
        product_dict = state["product"]

        response = self.executor.invoke({"product_dict": json.dumps(product_dict)})
        output = response["output"]

        # Extract JSON from response
        if "```json" in output:
            output = output.split("```json")[1].split("```")[0].strip()
        elif "```" in output:
            output = output.split("```")[1].split("```")[0].strip()

        try:
            product_page = json.loads(output)
        except json.JSONDecodeError:
            # Fallback: build using tools directly
            from src.tools import (
                build_benefits_block,
                build_core_summary,
                build_ingredient_block,
                build_safety_block,
                build_usage_block,
            )

            product_page = {
                "template": "product_page",
                "summary": build_core_summary.invoke(product_dict),
                "benefits": build_benefits_block.invoke(product_dict),
                "ingredients": build_ingredient_block.invoke(product_dict),
                "usage": build_usage_block.invoke(product_dict),
                "safety": build_safety_block.invoke(product_dict),
            }

        return {**state, "product_page": product_page}


class ComparisonAgent:
    """Agent that generates comparison page using tools and LLM."""

    def __init__(self):
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
        tools = get_all_tools()
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a comparison page generation agent. Given Product A (GlowBoost) and a fictional Product B, use the build_comparison_block tool to create a structured comparison.

Product B should be fictional but realistic:
- Name: Something like "CalmRadiance Gentle C Serum" or similar
- Concentration: Lower than Product A (e.g., 5% Vitamin C)
- Ingredients: Similar but with variations (e.g., add Aloe or Chamomile)
- Benefits: Similar but positioned differently (e.g., "Gradual brightening" vs "Fast brightening")
- Price: Different price point (e.g., ₹549 or ₹899)

After using the comparison tool, add a "who_should_choose_which" section with recommendations.""",
                ),
                ("human", "Product A (primary): {product_a_dict}\n\nGenerate comparison with fictional Product B:"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )
        agent = create_openai_tools_agent(llm, tools, prompt)
        self.executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comparison page."""
        product_a_dict = state["product"]

        # Create fictional Product B
        product_b_dict = {
            "name": "CalmRadiance Gentle C Serum",
            "concentration": "5% Vitamin C",
            "skin_type": ["Sensitive", "Dry"],
            "key_ingredients": ["Vitamin C", "Aloe", "Hyaluronic Acid"],
            "benefits": ["Gradual brightening", "Soothing hydration"],
            "how_to_use": "Apply 3-4 drops in the morning or evening, after cleansing",
            "side_effects": ["Rare mild redness"],
            "price": "₹549",
        }

        response = self.executor.invoke({"product_a_dict": json.dumps(product_a_dict)})
        output = response["output"]

        # Extract JSON from response
        if "```json" in output:
            output = output.split("```json")[1].split("```")[0].strip()
        elif "```" in output:
            output = output.split("```")[1].split("```")[0].strip()

        try:
            comparison_page = json.loads(output)
        except json.JSONDecodeError:
            # Fallback: build using tool directly
            from src.tools import build_comparison_block

            comparison = build_comparison_block.invoke(product_a_dict, product_b_dict)
            comparison_page = {
                "template": "comparison_page",
                "comparison": comparison,
                "who_should_choose_which": {
                    "primary": "Choose GlowBoost for faster brightening and spot fading.",
                    "alternative": "Choose Product B if you want a gentler start with Vitamin C.",
                },
            }

        return {**state, "comparison_page": comparison_page}

