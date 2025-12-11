# Kasparro Agentic Content Generation System

## Problem Statement
Automate generation of structured, machine-readable product content (FAQ, product, comparison pages) from a small JSON dataset using a modular, multi-agent system built with established agent frameworks (LangChain/LangGraph) rather than custom orchestration or hardcoded content.

## Solution Overview
The solution uses **LangChain** for agent implementation and **LangGraph** for workflow orchestration. Each agent is a proper LangChain agent with tools and LLM integration. Content generation is LLM-driven rather than hardcoded. The system runs a LangGraph workflow that orchestrates agents sequentially, ensuring all three content pages are generated as structured JSON outputs.

## Scopes & Assumptions
- Input is a single JSON file matching the provided product schema.
- OpenAI API key is required (set via environment variable or .env file).
- Content generation uses LLM calls (GPT-4o-mini) - not hardcoded strings.
- Product B for comparison is fictional but generated/structured by the comparison agent.
- Agents use LangChain's agent framework with proper tool integration.

## System Design

### Framework Choice: LangChain + LangGraph
The system uses **LangChain** (required) for agent implementation and **LangGraph** for orchestration. This demonstrates:
- Use of established frameworks instead of reinventing orchestration
- Proper agent boundaries with LangChain's agent framework
- State management via LangGraph's state graph
- Tool-based architecture for reusable content logic

### Agent Architecture

All agents are implemented as **LangChain agents** with clear responsibilities:

1. **DataIngestionAgent** (`src/agents_langchain.py`)
   - Parses raw JSON into normalized `Product` model
   - No LLM calls (pure data transformation)
   - Output: product dict in workflow state

2. **QuestionGenerationAgent** (`src/agents_langchain.py`)
   - Uses LangChain chain with GPT-4o-mini
   - Generates 15+ categorized questions (Informational, Safety, Usage, Purchase, Comparison)
   - LLM-driven: prompts model to generate questions from product data
   - Output: list of question dicts in workflow state

3. **FaqAgent** (`src/agents_langchain.py`)
   - LangChain agent with tools (AgentExecutor)
   - Uses LLM to generate FAQ answers for questions
   - Has access to content generation tools
   - LLM-driven: generates answers based on product data and question context
   - Output: FAQ page JSON structure

4. **ProductPageAgent** (`src/agents_langchain.py`)
   - LangChain agent with tools (AgentExecutor)
   - Uses tools to build structured content blocks
   - LLM orchestrates tool usage to assemble product page
   - Output: product page JSON structure

5. **ComparisonAgent** (`src/agents_langchain.py`)
   - LangChain agent with tools (AgentExecutor)
   - Generates fictional Product B using LLM
   - Uses comparison tool to create structured comparison
   - LLM-driven: creates realistic alternative product
   - Output: comparison page JSON structure

### LangGraph Workflow (`src/workflow.py`)

The workflow is built using **LangGraph's StateGraph**:

- **State Definition**: `WorkflowState` TypedDict defines state schema
- **Node Execution**: Each agent is a node in the graph
- **Sequential Flow**: 
  ```
  ingest → generate_questions → generate_faq → generate_product_page → generate_comparison → END
  ```
- **State Management**: LangGraph handles state passing between nodes
- **Type Safety**: TypedDict ensures state structure consistency

### Tools (`src/tools.py`)

Content logic blocks are exposed as **LangChain tools**:
- `build_core_summary`: Product summary block
- `build_usage_block`: Usage instructions block
- `build_safety_block`: Safety information block
- `build_ingredient_block`: Ingredient-focused block
- `build_benefits_block`: Benefits block
- `build_comparison_block`: Comparison block

Tools can be used by agents via LangChain's tool calling mechanism, enabling reusable content logic.

### LLM Integration

- **Model**: GPT-4o-mini (via `langchain-openai`)
- **Temperature**: Varied by agent (0.3-0.7 depending on creativity needs)
- **Prompt Engineering**: Structured prompts for each agent's role
- **JSON Output**: LLM responses parsed to extract structured JSON

### Execution Flow

1. **Entry Point** (`src/main.py`):
   - Loads environment variables (OpenAI API key)
   - Builds LangGraph workflow
   - Invokes workflow with initial empty state
   - Extracts final state and writes JSON outputs

2. **Workflow Execution**:
   - LangGraph executes nodes sequentially
   - Each agent receives state, processes it, returns updated state
   - State accumulates all outputs (product, questions, faqs, pages)

3. **Output Generation**:
   - Final state contains all three page structures
   - JSON files written to `output/` directory

### Key Design Decisions

1. **Framework-Based**: Uses LangChain/LangGraph instead of custom orchestration
2. **LLM-Driven**: Content generation uses models, not hardcoded strings
3. **Tool Architecture**: Reusable logic exposed as LangChain tools
4. **State Management**: LangGraph handles state passing (no global state)
5. **Agent Boundaries**: Each agent has single responsibility with defined I/O
6. **Type Safety**: TypedDict for state schema validation

### Output Structure

All outputs are machine-readable JSON:
- `output/faq.json`: FAQ page with questions, answers, categories
- `output/product_page.json`: Product page with summary, benefits, ingredients, usage, safety
- `output/comparison_page.json`: Comparison page with product comparison and recommendations
