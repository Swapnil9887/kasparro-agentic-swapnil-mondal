# Kasparro Agentic Content Generation System

Repository name: `kasparro-agentic-swapnil-mondal`

## What it does
A modular, LangChain-based agentic system that ingests a small product JSON dataset and generates machine-readable content pages:
- `faq.json` (FAQ page, 15+ Q&A generated across categories using LLM)
- `product_page.json` (structured product description page)
- `comparison_page.json` (GlowBoost vs. fictional Product B)

## Architecture
Built with **LangChain** and **LangGraph** for proper agent orchestration:

- **LangChain Agents**: Each agent uses LangChain's agent framework with tools and LLM calls
  - `DataIngestionAgent`: Parses product data
  - `QuestionGenerationAgent`: Uses LLM to generate categorized questions
  - `FaqAgent`: Uses LLM + tools to generate FAQ answers
  - `ProductPageAgent`: Uses LLM + tools to build product page
  - `ComparisonAgent`: Uses LLM + tools to create comparison page

- **LangGraph Workflow**: Orchestrates agents in a sequential DAG (`src/workflow.py`)
  - State management handled by LangGraph
  - Clear agent boundaries and dependencies

- **LangChain Tools**: Reusable content logic blocks exposed as tools (`src/tools.py`)
  - Tools can be used by agents for structured content generation

- **LLM-Driven Content**: All content generation uses OpenAI models (not hardcoded strings)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=your_key_here" > .env
```

## Run the pipeline
```bash
python -m src.main
```
Outputs land in `output/`.

## Key Components
- **LangChain Agents**: `src/agents_langchain.py`
- **LangGraph Workflow**: `src/workflow.py`
- **Tools**: `src/tools.py`
- **Data**: `data/product_data.json`
- **Entry Point**: `src/main.py`
- **Documentation**: `docs/projectdocumentation.md`


