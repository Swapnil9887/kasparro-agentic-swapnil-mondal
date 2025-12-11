"""LangGraph workflow for orchestrating the multi-agent content generation system."""

from typing import Annotated, TypedDict

from langgraph.graph import END, StateGraph

from src.agents_langchain import (
    ComparisonAgent,
    DataIngestionAgent,
    FaqAgent,
    ProductPageAgent,
    QuestionGenerationAgent,
)


class WorkflowState(TypedDict, total=False):
    """State passed between agents in the workflow."""

    product: Annotated[dict, "Parsed product data"]
    questions: Annotated[list, "Generated questions"]
    faqs: Annotated[list, "FAQ entries"]
    faq_page: Annotated[dict, "Rendered FAQ page"]
    product_page: Annotated[dict, "Rendered product page"]
    comparison_page: Annotated[dict, "Rendered comparison page"]


def build_workflow(data_path):
    """Builds and returns the LangGraph workflow.
    
    Sequential execution ensures all outputs are generated:
    ingest -> generate_questions -> generate_faq -> generate_product_page -> generate_comparison -> END
    """
    # Initialize agents
    ingest_agent = DataIngestionAgent(data_path)
    question_agent = QuestionGenerationAgent()
    faq_agent = FaqAgent()
    product_page_agent = ProductPageAgent()
    comparison_agent = ComparisonAgent()

    # Define workflow graph
    workflow = StateGraph(WorkflowState)

    # Add nodes
    workflow.add_node("ingest", ingest_agent.run)
    workflow.add_node("generate_questions", question_agent.run)
    workflow.add_node("generate_faq", faq_agent.run)
    workflow.add_node("generate_product_page", product_page_agent.run)
    workflow.add_node("generate_comparison", comparison_agent.run)

    # Set entry point
    workflow.set_entry_point("ingest")

    # Sequential execution: ensures all outputs are generated
    workflow.add_edge("ingest", "generate_questions")
    workflow.add_edge("generate_questions", "generate_faq")
    workflow.add_edge("generate_faq", "generate_product_page")
    workflow.add_edge("generate_product_page", "generate_comparison")
    workflow.add_edge("generate_comparison", END)

    return workflow.compile()

