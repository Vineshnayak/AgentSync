# AgentSync

An AI-Powered IT Incident Resolution & Coordination Engine.

## Project Overview

AgentSync is an enterprise-grade multi-agent system designed to autonomously coordinate and resolve IT incidents. By utilizing a network of specialized AI agents, AgentSync can plan investigation workflows, securely gather evidence from internal IT systems, perform root cause analysis, and recommend actionable mitigation strategies.

## Architecture

The system logic is built around `workflow/agent_workflow.py`, which manages state transitions across four primary agents using LangGraph:

1. **Planner Agent**: Parses incoming IT incident requests and structures a clear, step-by-step investigation plan.
2. **Investigation Agent**: Intelligently selects and utilizes integrated IT service management tools (Log Analyzer, Service Health, Incident History, Knowledge Base, Incident Action) to gather evidence.
3. **Analysis Agent**: Evaluates the retrieved evidence to identify root causes, impact, and operational risks.
4. **Decision Agent**: Formulates a comprehensive mitigation and resolution strategy, determining whether automated ticket creation or human escalation is required.

## Technology Stack

- **Language**: Python 3.10+
- **LLM Provider**: Groq API
- **Orchestration**: LangChain & LangGraph
- **Interfaces**: Streamlit (Dashboard) & FastAPI (REST API)
- **Data Backend**: Local JSON/SQLite architecture (Simulated Enterprise ITSM integration)

## Core Capabilities

- **Intelligent Tool Selection**: Dynamic evidence gathering using ReAct paradigms.
- **Robust Error Handling**: Type-safe tool inputs and graceful fallback mechanisms.
- **State Management**: Optimized context sharing between LLM calls using LangGraph state objects.
- **Telemetry**: Built-in tracking for execution metrics, latency, and token consumption.

## Setup & Execution

1. **Configure Environment:**
   Copy `.env.example` to `.env` and provide your `GROQ_API_KEY`.
   
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the API:**
   Start the FastAPI backend service:
   ```bash
   uvicorn api.main:app --reload
   ```

4. **Launch the Dashboard:**
   In a separate terminal, start the Streamlit UI:
   ```bash
   streamlit run app.py
   ```

5. **Execute Test Suite:**
   Run the test suite using pytest to verify agent reasoning and tool logic:
   ```bash
   pytest tests/
   ```
