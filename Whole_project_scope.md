# AgentSync: Comprehensive Project Scope & Architecture

## 1. Project Objective & Vision
**Project Name:** AgentSync
**Primary Objective:** To develop an AI Agent Coordination & Decision Engine that enables multiple specialized AI agents to collaborate intelligently across complex enterprise workflows. 

Modern enterprises require workflows where multiple specialized agents share information, utilize external tools, and make coordinated decisions. AgentSync serves as an orchestration platform to automate these multi-step business processes, specifically tailored (in this implementation) to **Automated IT Incident Resolution**.

## 2. Core Modules & Milestones (Implemented)
The project is structured around specific modules designed to build a robust foundation before layering on complex orchestration.

- **Module 1: Agent Environment Setup & Foundation:** Established the Python/LangChain environment and built foundational agents capable of distinct reasoning.
- **Module 2: Tool Integration & Intelligent Action:** Developed custom enterprise tools and integrated them using ReAct (Reasoning and Acting) paradigms so agents can dynamically gather evidence.
- **Module 3: Agent Coordination & Memory Systems:** Wired the agents together using a LangGraph state graph. Implemented short-term context passing and a long-term SQLite database (`agentsync_memory.db`) to enable context-aware decision making.

*(Milestones 4 and 5 involving full enterprise API deployments and broader workflow automation are the next steps.)*

## 3. System Architecture & Workflow

The architecture is driven by **LangGraph**, which passes a shared `AgentState` object between specialized nodes (agents). 

### 3.1 The AgentState
The state acts as the short-term memory during a single execution run. It tracks:
- `user_request`: The original incident description.
- `plan`: The step-by-step strategy.
- `investigation_results`: The evidence gathered from tools.
- `analysis`: The root cause and risk assessment.
- `decision`: The final mitigation strategy.
- `workflow_status`: The current state of the pipeline (e.g., "Started", "High Risk - Human Review Required").
- `errors`: Any execution exceptions.

### 3.2 The Multi-Agent Pipeline
The workflow (`workflow/agent_workflow.py`) coordinates four primary agents sequentially:

1. **Planner Agent:**
   - **Role:** Analyzes the raw `user_request` and generates a structured, step-by-step investigation plan. It does *not* execute tools; it only plans.

2. **Investigation Agent (Research):**
   - **Role:** Takes the `plan` and acts on it. It operates as a ReAct agent, meaning it autonomously decides *which* tools to call, *when* to call them, and parses their outputs.
   - **Output:** A comprehensive summary of gathered evidence (`investigation_results`).

3. **Analysis Agent:**
   - **Role:** Reviews the `investigation_results` against the original request. It identifies the root cause, evaluates the business impact, and determines the risk level (e.g., High, Medium, Low).

4. **Risk Evaluation (Conditional Edge):**
   - **Role:** A deterministic Python function that evaluates the text produced by the Analysis Agent. 
   - **Routing Logic:** If the risk is "High Risk", the workflow halts and routes for human review. If "Medium Risk", it loops back to the Investigation Agent. If "Low/Normal", it proceeds to the Decision Agent.

5. **Decision Agent:**
   - **Role:** Formulates the final resolution strategy.
   - **Long-Term Memory Integration:** Before generating a decision, this agent queries `agentsync_memory.db` for past workflows involving similar keywords. It uses past decisions as context to maintain consistency.
   - **Unmonitored Service Escalation:** If the system determines the incident involves a service not found in the local enterprise database, the Decision Agent automatically generates an escalated Markdown ticket (`tickets/INC-XXXX.md`) for manual engineering review.

## 4. Tool Integrations (Enterprise Simulation)
To interact with the outside world, the Investigation Agent is equipped with 6 custom tools found in the `tools/` directory:

1. **Log Analyzer Tool:** Parses JSON log files to find application exceptions and tracebacks.
2. **Service Health Tool:** Queries the mocked enterprise DB to check the real-time status of internal services (e.g., CPU load, memory, status).
3. **Incident History Tool:** Retrieves past incident records for specific services to find recurring patterns.
4. **Knowledge Base / Runbook Tool:** Fetches standard operating procedures (SOPs) for known issues.
5. **Incident Action Tool:** Allows the agent to simulate taking action (e.g., restarting a service or clearing a cache).
6. **External API Tool:** Makes actual HTTP `GET` requests to external URLs to verify if third-party dependencies are reachable, handling timeouts and HTTP errors gracefully.

## 5. Memory Management

- **Short-Term Memory:** Handled natively by LangGraph. As the state flows from node to node, each agent appends its findings, creating a unified conversational context.
- **Long-Term Memory:** Managed by `memory/memory_manager.py`. Once a workflow completes successfully, the final state (Request, Plan, Analysis, Decision, Metrics) is securely committed to a local SQLite database (`agentsync_memory.db`). This allows future executions to recall how past similar incidents were resolved.

### 5.1 Database Schemas (Data Persistence)
The system utilizes two distinct SQLite databases to simulate an enterprise environment and maintain agent context.

#### 1. `enterprise_mock.db` (Simulated IT Infrastructure)
This database acts as the external knowledge base and status tracker for the Investigation Agent.
- **`service_health`**: Tracks real-time metrics (`service` TEXT PRIMARY KEY, `status` TEXT, `latency_ms` REAL, `error_rate` REAL).
- **`service_logs`**: Stores application event logs (`id` INTEGER PRIMARY KEY, `service` TEXT, `timestamp` TEXT, `level` TEXT, `message` TEXT).
- **`historical_incidents`**: Logs past outages (`incident_id` TEXT PRIMARY KEY, `service` TEXT, `description` TEXT, `resolution` TEXT).
- **`service_runbooks`**: Contains standard operating procedures (`id` INTEGER PRIMARY KEY, `service` TEXT, `step_number` INTEGER, `step_description` TEXT).
- **`sales`**: Basic mock table for regional revenue (`id` INTEGER PRIMARY KEY, `region` TEXT, `revenue` REAL, `quarter` TEXT).

#### 2. `agentsync_memory.db` (Long-Term Memory)
This database persists the conversational context of past agent workflows for the Decision Agent to reference.
- **`workflow_history`**: Saves the full lifecycle of an incident resolution (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `user_request` TEXT, `plan` TEXT, `research_results` TEXT, `analysis` TEXT, `decision` TEXT, `timestamp` DATETIME).


## 6. Technology Stack
- **Core Language:** Python 3.10+
- **LLM Provider:** Groq API (utilizing `llama3-8b-8192` for high-speed, high-context reasoning).
- **Orchestration & Agents:** LangChain Core, LangChain Groq, and LangGraph.
- **User Interface:** React/Vite (Provides a clean, enterprise-style dashboard to submit incidents and view real-time agent metrics).
- **API Layer:** FastAPI / Uvicorn (Provides REST endpoints to trigger workflows programmatically).
- **Data Persistence:** SQLite3 (Handles both the simulated enterprise ITSM database and the AgentSync long-term memory).
- **Testing:** Pytest (Validates agent reasoning, tool execution, and workflow routing).

## 7. Next Steps & Expansion
With Milestones 1 through 3 complete, the project is ready to scale into:
- Broader deployment via Docker/Cloud (AWS/Azure/GCP).
- Expanding the API layer to support webhooks from real ITSM tools like Jira or ServiceNow.
- Implementing more complex, non-linear agent graphs (e.g., parallel investigation teams).
