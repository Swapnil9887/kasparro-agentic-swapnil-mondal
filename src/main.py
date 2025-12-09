import json
from pathlib import Path

from src.orchestrator import Orchestrator


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def run_pipeline() -> None:
    base_dir = Path(__file__).resolve().parent.parent
    data_path = base_dir / "data" / "product_data.json"
    output_dir = base_dir / "output"

    orchestrator = Orchestrator(data_path=data_path)
    result = orchestrator.run()

    write_json(output_dir / "faq.json", result["faq_page"])
    write_json(output_dir / "product_page.json", result["product_page"])
    write_json(output_dir / "comparison_page.json", result["comparison_page"])


if __name__ == "__main__":
    run_pipeline()


