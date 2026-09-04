# AgentSync

An AI Agent Coordination & Decision Engine.

## Project Overview
AgentSync is a multi-agent system designed to coordinate business workflows. It uses specialized AI agents to plan tasks, retrieve information, analyze data, and generate recommendations.

## Technology Stack
- **Language**: Python 3.x
- **LLM Provider**: Groq API
- **Orchestration**: LangChain & LangGraph
- **Interface**: Streamlit (Dashboard) & FastAPI (REST API)
- **Database**: SQLite (Local memory & mock enterprise data)

## Architecture
The system logic is built around `workflow/agent_workflow.py` which manages state transitions across four primary agents:
1. **Planner**: Parses the initial business request into a structured action plan.
2. **Research**: Utilizes integrated tools to retrieve necessary data.
3. **Analysis**: Evaluates the retrieved data for patterns and risks.
4. **Decision**: Formulates a final recommendation based on the analysis.

## Setup & Execution
1. Copy `.env.example` to `.env` and add your `GROQ_API_KEY`.
2. Install dependencies: `pip install -r requirements.txt`
3. Launch the dashboard: `streamlit run app.py`
4. Launch the API: `uvicorn api.main:app --reload`
5. Execute unit tests: `pytest tests/`

## Efficiency Mechanisms
- **State Management**: Uses LangGraph to pass a shared state object between nodes, minimizing redundant context sharing across LLM calls.
- **Tool Integration**: Stores tool outputs in short-term memory to prevent duplicate external queries.
- **Telemetry**: Tracks and logs execution metrics, including workflow duration and total LLM call counts.
