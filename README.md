# AgentSync: AI Agent Coordination & Decision Engine

AgentSync is an enterprise AI agent orchestration and decision engine that integrates autonomous incident management with Human Capital Management (HCM) resource allocation. The platform pairs LangGraph-orchestrated multi-agent workflows with an interactive capacity matrix and evidence-based HR decision agents. It automates end-to-end incident triage, diagnostic evidence collection, root-cause analysis, and capacity-headroom-aware engineer assignment, while preserving team wellbeing and avoiding burnout.

---

## 📋 Core Capabilities

- **Intelligent Request Classification & Triage**: Evaluates incoming prompts to distinguish between operational IT incidents and general informational inquiries. General inquiries are answered directly with zero workload consumption, while infrastructure disruptions trigger autonomous multi-agent triage.
- **Autonomous Multi-Agent Investigation**: LangGraph agents autonomously parse application logs, execute service health checks, query historical incident databases, and inspect runbooks using integrated enterprise tools.
- **Capacity-Headroom & Burnout Prevention**: Enforces a strict operational capacity threshold (`< 100%`). Overloaded personnel (e.g., personnel at $\ge 100\%$ capacity) are automatically disqualified from incident paging to prevent fatigue and burnout.
- **Contextual Handoff & Diagnostic Bundles**: Packages diagnosed root causes, relevant stack traces, affected service identifiers, and recommended standard operating procedures (SOPs) directly into generated incident tickets and assignment handoffs.
- **Authenticated HR Personnel Management**: Provides secure team roster management (adding and deleting team members with technical skill profiles, departments, and initial capacity) gated by an HR administrator authentication checkpoint.
- **Interactive Project Allocation Matrix**: Real-time allocation grid enabling team managers to toggle project assignments, recalculating capacity headroom, stress indexes, and telemetry streams on the fly.
- **Dual-Stack Integration & In-Process Fallback**: Integrates Python/FastAPI incident workflows with Node.js/Express HCM services, equipped with an automatic in-process fallback engine ensuring continuous operation without external dependencies.
- **Enterprise Web Console**: A responsive React 19 interface providing operations dashboards, incident tickets, past incident archives, team capacity matrices, talent scout search, and system guidelines.

---

## ⚙️ System Architecture & Workflow

```
[ Incoming Request / Operational Alert ]
                   │
                   ▼
        ┌──────────────────────┐
        │    Planner Agent     │ ── Classifies Intent: IT Incident vs General Inquiry
        └──────────┬───────────┘
                   │
         ┌─────────┴────────────────────────┐
         │ (General Inquiry)                │ (IT Incident / Outage)
         ▼                                  ▼
┌──────────────────────────────┐   ┌──────────────────────────────┐
│  Direct Response Formulated  │   │     Investigation Agent      │ ── Calls diagnostic tools
│  (0% Capacity Impact / Safe) │   └──────────────┬───────────────┘    (Logs, Health, DB, APIs)
└──────────────┬───────────────┘                  │
               │                                  ▼
               │                   ┌──────────────────────────────┐
               │                   │        Analysis Agent        │ ── Isolates root cause & risk
               │                   └──────────────┬───────────────┘
               │                                  ▼
               │                   ┌──────────────────────────────┐
               │                   │       Risk Evaluation        │ ── Routes: High Risk -> Immediate
               │                   └──────────────┬───────────────┘            Med Risk  -> Re-investigate
               │                                  ▼
               │                   ┌──────────────────────────────┐
               │                   │        Decision Agent        │ ── Prescribes remediation &
               │                   └──────────────┬───────────────┘    triggers Resource Matcher
               │                                  │
               │                                  ▼
               │                   ┌──────────────────────────────┐
               │                   │    Resource Matrix Match     │ ── Skill-aware matching +
               │                   └──────────────┬───────────────┘    enforces <100% capacity cap
               │                                  │
               │                        ┌─────────┴─────────┐
               │                        ▼                   ▼
               │               [ Optimal Engineer ]  [ Overloaded Personnel ]
               │               (e.g., Tariq @ 75%)   (Disqualified @ >=100%)
               │                        │
               │                        ▼
               │               [ Context Bundle ] ── Root cause + SOP + Logs
               │               [ Ticket Created ]    attached to ticket
               ▼                        ▼
       [ Final Execution State & Episodic Memory Persistence ]
```

---

## 🤖 Multi-Agent Architecture

The coordination engine deploys 9 specialized agents across two collaborating tiers:

### 1. Incident Resolution & Orchestration Tier (LangGraph)
| Agent | Role | Key Responsibilities |
| :--- | :--- | :--- |
| **Planner Agent** | Strategy & Triage | Evaluates incoming requests, separates general queries from incidents, decomposes issues into structured investigation checklists. |
| **Investigation Agent** | ReAct Research | Autonomously invokes diagnostic tools (service health, log analysis, past history, runbooks, external API checks). |
| **Analysis Agent** | Diagnostics | Synthesizes tool outputs to determine root causes, affected systems, impact severity, and failure modes. |
| **Decision Agent** | Mitigation & Dispatch | Formulates mitigation plans, coordinates with the HCM resource matrix, and pre-packages diagnostic context bundles. |

### 2. Human Capital Management (HCM) Decision Tier
| Agent | Role | Key Responsibilities |
| :--- | :--- | :--- |
| **Workload Agent** | Capacity Enforcement | Tracks employee allocation percentages, enforces the `< 100%` hard headroom threshold, and manages overload alerts. |
| **Project Fit Agent** | Skill Matching | Analyzes required incident technologies against employee skill profiles to calculate match fit scores. |
| **Performance Agent** | Operational Metrics | Evaluates historical incident resolution performance and delivery track records. |
| **Availability Agent** | Schedule Coordination | Validates on-call commitments, project milestones, and current bandwidth availability. |
| **Employee Wellbeing Agent** | Stress & Burnout | Assesses stress indices, flags rapid capacity increases, and issues managerial wellbeing recommendations. |

---

## 🛠️ Integrated Enterprise Tools (7 Tools)

1. **`service_health_tool`**: Probes real-time service uptime, latency, CPU utilization, memory pressure, and operational status.
2. **`log_analyzer_tool`**: Analyzes system logs across configurable timeframes (30m, 1h, 24h) to isolate stack traces and failure signatures.
3. **`incident_history_tool`**: Queries historical outage records to cross-reference previous failure modes and proven remediation tactics.
4. **`knowledge_base_tool`**: Searches standard operating procedure (SOP) runbooks to locate approved mitigation playbooks.
5. **`external_api_tool`**: Validates third-party and upstream endpoint reachability via live network probes.
6. **`incident_action_tool`**: Creates, updates, and tracks incident tickets with persistent markdown records (`tickets/INC-*.md`).
7. **`resource_matrix_tool` (`query_resource_matrix`)**: Inspects current team capacity, available headroom, and technical skill sets.

---

## 🎯 Milestone & Requirements Verification (Milestones 1–4)

The project satisfies 100% of the milestone and module specifications:

| Milestone / Module | Requirement Scope | Implementation Evidence | Status |
| :--- | :--- | :--- | :--- |
| **Milestone 1** (Weeks 1–2)<br>*Agent Foundations* | Core agent framework, LangChain/LLM environment, prompt templates, structured state, interaction pipeline. | Implemented via `ChatGroq`, LangChain Core, Pydantic schemas, and structured `AgentState` in `workflow/state.py`. | **100% Complete** |
| **Milestone 2** (Weeks 3–4)<br>*Tool Integration* | Custom enterprise tools, dynamic tool selection, external API connections, monitoring, error handling. | 7 custom enterprise tools in `tools/`, ReAct agent loop in `investigation_agent.py`, full exception handling. | **100% Complete** |
| **Milestone 3** (Weeks 5–6)<br>*Coordination & Memory* | Specialized multi-agent roles, inter-agent communication, short-term conversational & long-term episodic memory. | LangGraph state graph coordination (`agent_workflow.py`), SQLite episodic memory (`agentsync_memory.db`), copilot chat API. | **100% Complete** |
| **Milestone 4** (Weeks 7–8)<br>*Automation & Deployment* | Dynamic workflow orchestration, REST API, monitoring dashboard, cloud deployment, and performance validation. | FastAPI service (`api/main.py`), React 19 UI, cloud hosting (Vercel + Render), and 41 passing automated tests. | **100% Complete** |

---

## 💻 Technology Stack

- **Backend**: Python 3.10+, FastAPI, Uvicorn, Pydantic v2
- **Agent Orchestration**: LangGraph, LangChain Core
- **LLM Engine**: Groq API (`openai/gpt-oss-20b` high-throughput inference)
- **Frontend Console**: React 19, Vite, Lucide React, Axios, CSS Design System
- **Dual-Stack Integration**: Node.js/Express HCM API + In-Process Python Fallback Singleton
- **Data Persistence**: SQLite3 (`agentsync_memory.db` for episodic memory, `enterprise_mock.db` for telemetry)
- **Testing**: Pytest (41 unit and integration tests, 100% pass rate)

---

## 📁 Repository Structure

```
AgentSync/
├── agents/                     # LangGraph incident agents
│   ├── planner_agent.py        # Intent classification & investigation planning
│   ├── investigation_agent.py  # ReAct multi-tool investigation
│   ├── analysis_agent.py       # Root-cause diagnosis & impact analysis
│   └── decision_agent.py       # Mitigation planning & engineer assignment
├── api/                        # FastAPI REST API layer
│   └── main.py                 # Workflow endpoints, HCM routes, admin authentication
├── config/                     # Environment and model settings
│   └── settings.py
├── frontend/                   # React 19 + Vite operations console
│   ├── src/
│   │   ├── App.jsx             # Main application, dashboard, matrix, modals
│   │   ├── App.css             # Enterprise dark-mode design system
│   │   └── main.jsx
│   ├── package.json
│   ├── vercel.json             # Vercel deployment rewrites
│   └── vite.config.js
├── hcm/                        # Human Capital Management subsystem
│   ├── hcm_manager.py          # Employee roster, capacity matrix, headroom locks
│   └── hr_agents.py            # 5 evidence-based situational review agents
├── memory/                     # Episodic long-term memory
│   └── memory_manager.py
├── tests/                      # Automated test suite (41 tests)
│   ├── test_agents.py
│   ├── test_api.py
│   ├── test_hcm.py
│   └── test_tools.py
├── tickets/                    # Generated incident tickets with diagnostic bundles
├── tools/                      # 7 integrated enterprise diagnostic tools
├── utils/                      # Logging and telemetry metrics
├── workflow/                   # LangGraph state machine definition
│   ├── agent_workflow.py       # StateGraph definition and dynamic routing
│   └── state.py                # TypedDict AgentState schema
├── requirements.txt            # Python dependencies
├── setup_db.py                 # SQLite database initialization
├── Whole_project_scope.md      # Full architecture and scope document
└── FINAL_PROJECT_DOCUMENTATION.md
```

---

## 🚀 Local Setup & Quick Start

### 1. Prerequisites
- Python 3.10+
- Node.js 18+ and npm
- Groq Cloud API key ([console.groq.com](https://console.groq.com))

### 2. Environment Configuration
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
DEFAULT_MODEL=openai/gpt-oss-20b
```

### 3. Backend Setup
```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize databases
python setup_db.py

# Launch FastAPI server
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```
Interactive OpenAPI documentation will be available at `http://localhost:8000/docs`.

### 4. Frontend Setup
In a separate terminal window:
```bash
cd frontend
npm install
npm run dev
```
The operations dashboard will be live at `http://localhost:5173`.

---

## 🧪 Verification & Testing

Run the full automated test suite:
```bash
pytest tests/ -v
```
All **41 unit and integration tests** pass verified.

---

## 🔒 HR Administrator Authentication

Personnel management actions (adding new team members and deleting members) are protected behind an authentication gate:
- **Default Username:** `admin`
- **Default Passwords:** `admin123` / `adminpassword` / `agentsync2026`
- **Session Persistence:** Successfully authenticated administrators retain active access in the browser session, with immediate manual locking controls in the topbar and settings.

---

## 🌐 Production Deployment

- **Frontend:** Hosted on **Vercel** (`https://agent-sync.vercel.app`) with SPA routing rules.
- **Backend:** Hosted on **Render** running `uvicorn api.main:app --host 0.0.0.0 --port $PORT`.
