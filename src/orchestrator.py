from pathlib import Path
from typing import Any, Dict

from src.agents.comparison_agent import ComparisonAgent
from src.agents.data_ingestion_agent import DataIngestionAgent
from src.agents.faq_agent import FaqAgent
from src.agents.product_page_agent import ProductPageAgent
from src.agents.question_generation_agent import QuestionGenerationAgent
from src.automation_graph import AutomationGraph, Node
from src.templates import build_engine


class Orchestrator:
    """Configures agents and executes the automation graph."""

    def __init__(self, data_path: Path) -> None:
        engine = build_engine()
        self.graph = AutomationGraph(
            nodes=[
                Node("ingest", DataIngestionAgent(data_path=data_path), depends_on=[]),
                Node("questions", QuestionGenerationAgent(), depends_on=["ingest"]),
                Node("faq", FaqAgent(engine), depends_on=["questions"]),
                Node("product_page", ProductPageAgent(engine), depends_on=["ingest"]),
                Node("comparison", ComparisonAgent(engine), depends_on=["ingest"]),
            ]
        )

    def run(self) -> Dict[str, Any]:
        return self.graph.run(payload={})


