# Kasparro Agentic Content Generation System

Repository name (per brief): `kasparro-ai-agentic-content-generation-system-<first_name-last_name>`.

## What it does
A modular, agent-driven pipeline that ingests a small product JSON dataset and generates machine-readable pages:
- `faq.json` (FAQ page, 15 Q&A generated across categories)
- `product_page.json` (description page)
- `comparison_page.json` (GlowBoost vs. fictional Product B)

## How it works
- Agents with single responsibilities (ingestion, question generation, FAQ assembly, product page, comparison).
- A DAG-based automation graph orchestrates agents (`src/automation_graph.py`).
- Reusable content logic blocks (`src/content_blocks.py`) feed a custom template engine (`src/template_engine.py`) with templates defined in `src/templates.py`.
- Outputs are rendered to JSON by the orchestrator pipeline.

## Run the pipeline
```bash
cd "/Users/swapnil/Kasparro Agentic AI"
python -m src.main
```
Outputs land in `output/`.

## Key paths
- Data: `data/product_data.json`
- Entry point: `src/main.py`
- Agents: `src/agents/`
- Templates & blocks: `src/templates.py`, `src/content_blocks.py`
- Docs: `docs/projectdocumentation.md`


