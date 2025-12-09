# Kasparro Agentic Content Generation System

## Problem Statement
Automate generation of structured, machine-readable product content (FAQ, product, comparison pages) from a small JSON dataset using a modular, multi-agent system rather than a monolith or single prompt.

## Solution Overview
The solution builds a lightweight agentic pipeline orchestrated via a DAG. Dedicated agents ingest data, generate categorized questions, and assemble pages through reusable content blocks and templates. A template engine wires blocks into JSON outputs. Running `python -m src.main` produces `output/faq.json`, `output/product_page.json`, and `output/comparison_page.json`.

## Scopes & Assumptions
- Input is a single JSON file matching the provided product schema.
- No external calls or research; all content derives from the dataset and deterministic rules.
- Product B for comparison is fictional but statically defined and structured.
- Execution is single-threaded but graph-driven; agents are stateless across runs.

## System Design
- **Agents (single responsibility):**
  - `DataIngestionAgent`: parse raw JSON into a normalized `Product`.
  - `QuestionGenerationAgent`: create 15+ user questions across Informational, Usage, Safety, Purchase, Comparison.
  - `FaqAgent`: convert questions into Q&A using deterministic logic and render the FAQ template.
  - `ProductPageAgent`: render the product description template using reusable blocks.
  - `ComparisonAgent`: inject fictional Product B and render the comparison template.
- **Automation Graph:** `AutomationGraph` defines DAG nodes with dependencies and executes agents in topological order. Nodes: ingest → questions → faq, ingest → product_page, ingest → comparison.
- **Content Logic Blocks (`src/content_blocks.py`):** reusable functions (core summary, benefits, ingredients, usage, safety, comparison) that transform `Product` data into structured snippets.
- **Template Engine (`src/template_engine.py` + `src/templates.py`):** custom template/field definitions with resolvers that call logic blocks. Templates: `faq_page`, `product_page`, `comparison_page`.
- **Orchestrator (`src/orchestrator.py`):** boots the template engine, wires agents into the DAG, runs the pipeline, and returns all page payloads.
- **Outputs:** JSON pages written by `src/main.py` to `output/faq.json`, `output/product_page.json`, and `output/comparison_page.json`.


