# AgentSync: Comprehensive Technical Scope & Architecture Specification

## 1. Executive Summary & Objective

**Platform Name:** AgentSync  
**Domain:** Autonomous AI Multi-Agent Coordination, IT Incident Resolution & Human Capital Management (HCM) Decision Engine  

Modern digital enterprises depend on distributed microservices, databases, and third-party APIs. When system anomalies, latency spikes, or outages occur, diagnosing and resolving them requires multi-disciplinary coordination: analyzing diagnostic logs, verifying service health, cross-referencing previous post-mortems, evaluating downstream risks, and executing mitigation strategies.

Traditional incident response workflows suffer from **uncoordinated dispatch**—alerting on-call engineers without insight into active workloads, technical skill compatibility, or cognitive fatigue. This leads to alert fatigue, increased MTTR, and engineering burnout.

**AgentSync** addresses this challenge through a **Dual-Stack Integration** that connects:
1. **Autonomous Incident Triage (AgentSync)**: A LangGraph state machine orchestrating specialized AI agents (Planner, Investigation, Analysis, Decision) equipped with enterprise tools to diagnose root causes and formulate mitigation plans.
2. **Resource Allocation & Decision Engine (HCM)**: A skill-aware human capital matrix that tracks employee capacities, enforces strict workload headroom thresholds (`< 100%`), disqualifies overloaded personnel, and packages contextual telemetry directly into tickets for instant handoff.
3. **Intent Classification & Safe Query Routing**: An intelligent classifier that separates general informational questions from infrastructure incidents, providing direct answers with zero engineering workload impact.

---

## 2. Milestone Implementation & Verification (Milestones 1–4: 100% Complete)

The platform was built and validated against all project requirements and evaluation criteria:

### Milestone 1 (Weeks 1–2): Agent Foundation Development — **100% Complete**
- **Objective:** Establish the core agent framework, development environment, and prompt pipelines.
- **Deliverables:**
  - Configured LangChain Core, LangGraph, and ChatGroq with high-throughput inference models.
  - Implemented foundational AI agents with specialized system prompts and typed `AgentState` schemas.
  - Built prompt templates for incident decomposition, evidence synthesis, and risk evaluation.
  - Established testing harnesses with automated test suites (`tests/test_agents.py`).

### Milestone 2 (Weeks 3–4): Tool Integration & Action Execution — **100% Complete**
- **Objective:** Enable agents to interact with external enterprise services, databases, and diagnostic tools.
- **Deliverables:**
  - Implemented 7 enterprise tools: `service_health_tool`, `log_analyzer_tool`, `incident_history_tool`, `knowledge_base_tool`, `external_api_tool`, `incident_action_tool`, and `resource_matrix_tool`.
  - Configured ReAct autonomous tool selection in `investigation_agent.py` to iteratively gather logs, probe APIs, and consult runbooks.
  - Implemented structured error handling, network failure fallbacks, and real-time execution telemetry.
  - Validated tool execution accuracy via `tests/test_tools.py`.

### Milestone 3 (Weeks 5–6): Agent Coordination & Memory Management — **100% Complete**
- **Objective:** Build multi-agent collaboration mechanisms and memory management.
- **Deliverables:**
  - Implemented specialized agent fleet: Planner, Investigation, Analysis, Decision, Workload, Project Fit, Performance, Availability, and Wellbeing agents.
  - Engineered LangGraph state passing with conditional edges for risk escalation and general query routing.
  - Configured dual-layer memory:
    - **Short-Term Conversational Memory:** Interactive resolution copilot (`/workflow/chat/{job_id}`).
    - **Long-Term Episodic Memory:** SQLite persistence (`agentsync_memory.db`) storing past workflows and retrieving historical precedents via keyword indexing.

### Milestone 4 (Weeks 7–8): Workflow Automation & Deployment — **100% Complete**
- **Objective:** Deliver a production-ready AI coordination platform with APIs, dashboards, and cloud deployment.
- **Deliverables:**
  - REST API layer built with FastAPI (`api/main.py`) exposing 20+ endpoints with OpenAPI documentation.
  - Single-interface React 19 + Vite dashboard with live telemetry, capacity matrices, talent scout search, and ticket records.
  - Cloud deployment on Vercel (frontend) and Render (backend).
  - Authenticated HR personnel management with username/password checkpoint (`admin` / `admin123`) for adding and deleting employees.
  - Automated test suite with **41 passing tests** covering 100% of core workflows.

---

## 3. Workflow State Machine & Dynamic Routing

The coordination engine is orchestrated by **LangGraph**, routing state across specialized agent nodes:

```
                  ┌─────────────────────────┐
                  │      Incoming Event     │
                  │  (User / System Query)  │
                  └────────────┬────────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │      Planner Agent      │ ── Evaluates Intent
                  └────────────┬────────────┘
                               │
            ┌──────────────────┴──────────────────┐
            │ [Informational / General Query]     │ [IT Incident Outage]
            ▼                                     ▼
┌──────────────────────────────┐       ┌─────────────────────────┐
│  Direct Answer Formulated    │       │   Investigation Agent   │ ── Calls tools (Logs,
│  (0% Capacity Impact / Safe) │       │ (ReAct Multi-Tool Calls)│    Health, DB, APIs)
└───────────┬──────────────────┘       └────────────┬────────────┘
            │                                       │
            │                                       ▼
            │                          ┌─────────────────────────┐
            │                          │     Analysis Agent      │ ── Root-cause diagnosis
            │                          │  (Impact & Risk Scoring)│
            │                          └────────────┬────────────┘
            │                                       │
            │                                       ▼
            │                          ┌─────────────────────────┐
            │               ┌──────────┤     Risk Evaluation     ├──────────┐
            │               │          │   (Conditional Router)  │          │
            │               │          └─────────────────────────┘          │
            │               ▼                                               ▼
            │      [High / Standard Path]                          [Medium Path - Re-investigate]
            │               │                                               │
            │               ▼                                               │
            │          ┌────────────────┐                                   │
            │          │ Decision Agent │ ◄─────────────────────────────────┘
            │          └──────┬─────────┘
            │                 │
            │                 ▼
            │          ┌───────────────────────┐
            │          │ Resource Matrix Match │ ── Skill Matching + <100% Headroom
            │          └──────┬────────────────┘
            │                 │
            │           ┌─────┴────────────────────────┐
            │           ▼                              ▼
            │      [ Optimal Engineer ]     [ Overloaded Personnel ]
            │      (Assigned with Headroom) (Disqualified @ >=100%)
            │           │
            │           ▼
            │      [ Context Bundle & Ticket ]
            ▼           ▼
    [ Final State Saved to Long-Term Memory ]
```

---

## 4. Intelligent Request Classification & Safe Query Routing

When user inputs are received by the engine:
1. **General Informational Queries** (e.g., factual queries like *"capital of india"*, company policies, general chat):
   - Classified immediately by the Planner Agent.
   - Generates a direct, accurate answer.
   - **Routes directly to END:** Does not trigger log analyzers, does not probe health endpoints, and does not page engineers.
   - **Zero Capacity Impact:** Employee workloads remain completely untouched ($0\%$ capacity consumed, maintaining existing headroom).
2. **IT Incident Disruption** (e.g., *"Payment API failing with 500 database timeouts"*):
   - Classified as an operational incident.
   - Generates structured diagnostic checklist.
   - Routes through Investigation, Analysis, Risk Evaluation, and Decision Agents.
   - Assigns the best available engineer with $<100\%$ capacity and pre-packages the context bundle.

---

## 5. Human Capital Management (HCM) & Workload Safeguards

### Capacity Headroom Rules
- **Safe Zone ($< 85\%$ Load):** Nominal operational capacity. Eligible for incident paging.
- **Elevated Zone ($85\% - 99\%$ Load):** Workload triggers proactive managerial notification.
- **Capacity Lockout ($\ge 100\%$ Load):** Strict burnout safeguard. Employee is automatically disqualified from incident dispatch.

### HR Administrator Security Checkpoint
- Adding and deleting team members is protected by authentication:
  - **Endpoint:** `POST /auth/admin-login`
  - **Credentials:** `admin` / `admin123`
  - **Add Member:** Allows specifying name, role, department, email, technical skills, and initial capacity.
  - **Delete Member:** Safely removes employee, cleans up project allocations across all projects, recalculates capacity metrics, and logs an HR telemetry event.

---

## 6. Verification Summary

- **Automated Tests:** 41/41 passing unit and integration tests.
- **Frontend Build:** Verified via `npm run build` with zero compilation errors.
- **Continuous Deployment:** Synchronized with Vercel and Render via `origin main`.
