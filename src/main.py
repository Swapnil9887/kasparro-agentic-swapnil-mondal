"""Main entry point for the LangChain-based agentic content generation system."""

import json
import os
from pathlib import Path

from dotenv import load_dotenv

from src.workflow import build_workflow

# Load environment variables for API keys
load_dotenv()


def write_json(path: Path, payload) -> None:
    """Write payload as formatted JSON to file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def run_pipeline() -> None:
    """Execute the LangGraph workflow to generate all content pages."""
    base_dir = Path(__file__).resolve().parent.parent
    data_path = base_dir / "data" / "product_data.json"
    output_dir = base_dir / "output"

    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError(
            "OPENAI_API_KEY not found. Please set it in your environment or .env file."
        )

    # Build and run LangGraph workflow
    workflow = build_workflow(data_path)
    
    # Execute workflow - sequential execution ensures all outputs are generated
    initial_state = {}
    final_state = workflow.invoke(initial_state)

    # Write outputs
    if "faq_page" in final_state and final_state["faq_page"]:
        write_json(output_dir / "faq.json", final_state["faq_page"])
    
    if "product_page" in final_state and final_state["product_page"]:
        write_json(output_dir / "product_page.json", final_state["product_page"])
    
    if "comparison_page" in final_state and final_state["comparison_page"]:
        write_json(output_dir / "comparison_page.json", final_state["comparison_page"])


if __name__ == "__main__":
    run_pipeline()


