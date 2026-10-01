# AgentSync: AI Agent Coordination & Decision Engine

## Project Overview

AgentSync is an AI-powered coordination and decision engine designed to automate complex business workflows and IT incident resolution. By coordinating multiple specialized AI agents, the platform enables intelligent collaboration, information retrieval, analysis, and decision support across functional domains. 

The system leverages Large Language Models (LLMs), orchestration frameworks, memory systems, and external tool integrations to automate multi-step processes and provide context-aware recommendations.

## System Architecture

The core orchestration is managed by a state graph (`workflow/agent_workflow.py`), which coordinates four specialized agents:

1. **Planner Agent**: Analyzes incoming requests and formulates a structured, step-by-step execution plan.
2. **Investigation Agent**: Autonomously selects and executes integrated tools (e.g., Log Analyzer, Service Health, External API checks) to gather necessary context and evidence.
3. **Analysis Agent**: Evaluates the gathered data to identify root causes, assess impact, and determine risk levels.
4. **Decision Agent**: Formulates a final resolution strategy and determines whether automated ticketing or human escalation is required. It utilizes a long-term memory database to ensure consistent decision-making based on past workflows.

## Core Features

- **Multi-Agent Coordination**: Agents collaborate in a sequential pipeline, passing context via a shared state object.
- **Intelligent Tool Integration**: The system natively integrates with simulated enterprise services, databases, and external APIs with built-in error handling.
- **Shared Knowledge & Memory**: Implements short-term state memory and long-term SQLite-backed memory (`agentsync_memory.db`) for context-aware decision support.
- **Dynamic Workflow Routing**: Includes conditional logic to route tasks (e.g., routing back for further investigation or escalating unmonitored systems by auto-generating markdown tickets).

## Technology Stack

- **Language**: Python 3.10+
- **LLM Provider**: Groq API
- **Orchestration**: LangChain & LangGraph
- **User Interface**: React/Vite (Dashboard)
- **Data Persistence**: SQLite

## Setup & Execution

### 1. Configure Environment
Create a `.env` file in the root directory and provide your Groq API key:
```env
GROQ_API_KEY=your_api_key_here
```

### 2. Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### 3. Launch the API
Start the FastAPI backend service:
```bash
uvicorn api.main:app --reload
```

### 4. Launch the Frontend
In a separate terminal, navigate to the frontend directory and start the React app:
```bash
cd frontend
npm install
npm run dev
```

### 4. Execute Test Suite
Run the automated test suite to validate agent logic, workflow routing, and tool execution:
```bash
pytest tests/
```
