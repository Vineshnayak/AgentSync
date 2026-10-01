# Final Project Documentation

This file contains the final results and documentation to be copied into the provided project templates (`Agile_Template`, `Defect_Tracker Template`, `Unit_Test_Plan`).

## 1. Unit Test Plan Results
The unit tests have been executed successfully against the implemented AgentSync framework.

**Test Environment:** macOS M1, Python 3.x, Pytest.

| Sl: No: | Test Case Name | Test Procedure | Condition to be tested | Expected Result | Actual Result |
|---|---|---|---|---|---|
| 1 | Verifying agents | Run `test_planner_agent` passing an empty state. | Verify Planner agent generates a plan without calling Research | Plan string generated | Plan string generated |
| 2 | Workflow Routing (High Risk) | Run `test_risk_evaluation_high_risk` passing state with "high risk" text. | Verify `evaluate_risk` routes to 'Human Review Required' | Status updated to 'High Risk - Human Review Required' | Status updated to 'High Risk - Human Review Required' |
| 3 | Workflow Routing (Low Risk) | Run `test_risk_evaluation_low_risk` passing state with stable text. | Verify `evaluate_risk` routes to 'Low Risk' | Status updated to 'Low Risk' | Status updated to 'Low Risk' |
| 4 | End-to-End Workflow Execution | Run `test_workflow_execution` with mocked sub-agents. | Verify all nodes are executed in sequence passing state | All agent nodes called, final status 'Completed' | All agent nodes called, final status 'Completed' |
| 5 | Log Analyzer Tool Execution | Run `test_log_analyzer` fetching logs for a mocked service. | Verify the tool successfully parses mock_data.json and returns the log string. | Returns mocked log data string | Returned mocked log data string |
| 6 | Incident Action Invalid Input | Run `test_incident_action_tool_invalid_action` with action "delete". | Verify tool handles invalid actions without crashing. | Returns "Invalid action" error message | Returned "Invalid action" error message |
| 7 | External API HTTP Success | Run `test_external_api_tool_success` with mocked 200 OK response. | Verify the tool successfully parses standard HTTP responses. | Returns status code and latency string | Returned status code and latency string |
| 8 | External API Timeout | Run `test_external_api_tool_timeout` simulating a timeout exception. | Verify the tool safely catches requests.exceptions.Timeout. | Returns "timed out after 5 seconds" error | Caught timeout and returned error |
| 9 | Investigation Agent ReAct Integration | Run agent with ReAct framework passing a mocked plan. | Verify the agent correctly identifies which tool to call based on the input text. | Tool is invoked and evidence string is returned | Tool invoked and evidence string is returned |
| 10 | Memory Manager Integration | Run `test_memory_manager_save` with mock workflow data. | Verify past workflows are successfully inserted into `agentsync_memory.db`. | SQL INSERT succeeds and ID is returned | SQL INSERT succeeds and ID is returned |
| 11 | Out of Context Ticket Escalation | Run `test_decision_agent_unmonitored` passing "Service not found". | Verify Decision agent auto-generates `INC-XXXX.md` ticket file via Python logic. | Markdown ticket file is successfully created | Markdown ticket file is successfully created |

## 2. Defect Tracker
No critical defects remain in the final implementation. Minor defects identified and fixed during development:

| Sl No | Submitted By | Submitted Date | Description | Detected Sprint | Assigned To | Type Of Defect | Action Taken | Action Taken Date | Status(Open/Closed) | Remarks |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | AgentSync Dev | 2026-09-03 | LangGraph duplicate tool execution error | Sprint 1 | Lead Developer | Logic / Execution | Switched to `create_react_agent` from LangGraph prebuilt. | 2026-09-03 | Closed | Resolved |
| 2 | AgentSync Dev | 2026-09-03 | SQLite thread lock error during memory save | Sprint 1 | Lead Developer | Database | Added try/except blocks and ensured `conn.close()` is called on every transaction. | 2026-09-03 | Closed | Resolved |

## 3. Agile Documentation (Product Backlog)

| Planned Sprint | Actual Sprint | US ID | User Story Description | MOSCOW | Dependency | Assignee | Status |
|---|---|---|---|---|---|---|---|
| Sprint 3 | Sprint 3 | US-11 | Develop specialized agents (Planner, Investigation, Analysis, Decision) with distinct business roles | MUST HAVE | US-10 | Vinesh | 3- Completed |
| Sprint 3 | Sprint 3 | US-12 | Implement long-term memory system (SQLite) to track past workflows and enable context-aware decisions | MUST HAVE | US-11 | Vinesh | 3- Completed |
| Sprint 3 | Sprint 3 | US-13 | Implement out-of-context ticket escalation (auto-generating markdown files for unmonitored services) | MUST HAVE | US-12 | Vinesh | 3- Completed |

## 4. Agile Documentation (Sprint Backlogs)

### SPRINT 1 BACKLOG
| US ID | Task ID | Task Description | Task Start Date | Task Completion Date | Team Member | Activity | Status | Original Estimate Effort (In Hours) | Day 1 | Day 2 | Day 3 | Day 4 | Day 5 | Day 6 | Day 7 | Day 8 | Day 9 | Day 10 | Day 11 | Day 12 | Day 13 | Day 14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| US-01 | T-01 | Agent Environment Setup (LangChain, Groq, basic Agent classes and state) | 02/09/2026 | 03/09/2026 | Vinesh | Build | 3- Completed | 12 | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| US-02 | T-02 | Tool Integration (Calculator, Mock Business DB, Knowledge Retrieval) | 04/09/2026 | 05/09/2026 | Vinesh | Build | 3- Completed | 8 | 0 | 0 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| US-03 | T-03 | Agent Coordination (LangGraph node graph, short/long-term memory) | 06/09/2026 | 06/09/2026 | Vinesh | Build | 3- Completed | 5 | 0 | 0 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

### SPRINT 2 BACKLOG
| US ID | Task ID | Task Description | Task Start Date | Task Completion Date | Team Member | Activity | Status | Original Estimate Effort (In Hours) | Day 1 | Day 2 | Day 3 | Day 4 | Day 5 | Day 6 | Day 7 | Day 8 | Day 9 | Day 10 | Day 11 | Day 12 | Day 13 | Day 14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| US-06 | T-01 | Create mock_data.json with realistic IT incident scenarios. | 16/09/2026 | 16/09/2026 | Vinesh | Build | 3- Completed | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| US-07 | T-02 | Develop IT Incident Tools (Logs, Health, History, Runbooks, Action) | 17/09/2026 | 18/09/2026 | Vinesh | Build | 3- Completed | 10 | 0 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| US-08 | T-03 | Develop External API Connector Tool handling real HTTP requests | 19/09/2026 | 19/09/2026 | Vinesh | Build | 3- Completed | 4 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

### SPRINT 3 BACKLOG
| US ID | Task ID | Task Description | Task Start Date | Task Completion Date | Team Member | Activity | Status | Original Estimate Effort (In Hours) | Day 1 | Day 2 | Day 3 | Day 4 | Day 5 | Day 6 | Day 7 | Day 8 | Day 9 | Day 10 | Day 11 | Day 12 | Day 13 | Day 14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| US-11 | T-01 | Develop Planner, Investigation, Analysis, and Decision agents using LangGraph. | 25/09/2026 | 27/09/2026 | Vinesh | Build | 3- Completed | 12 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 5 | 3 | 0 | 0 |
| US-12 | T-02 | Setup agentsync_memory.db and wire up long-term memory retrieval in decision node. | 28/09/2026 | 29/09/2026 | Vinesh | Build | 3- Completed | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 4 |
| US-13 | T-03 | Add unmonitored service detection and auto-generate markdown incident tickets. | 30/09/2026 | 30/09/2026 | Vinesh | Build | 3- Completed | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 |
## 5. Agile Documentation (Stand up Meeting - All Sprints)

| Sprint | Day | Impediments | Action Taken |
|---|---|---|---|
| Sprint 1 | Day 1 | LangChain dependency conflicts with existing Python environment. | Created a clean virtual environment and pinned specific versions of langchain-core and langgraph in requirements.txt. |
| Sprint 1 | Day 2 | Planner Agent hallucinated investigative data instead of strictly generating a plan. | Refined the system prompt to explicitly state: "Do not perform the investigation yourself. Just output the step-by-step plan." |
| Sprint 1 | Day 3 | LangGraph nodes lost context when transitioning between Planner and Investigation agents. | Standardized the AgentState TypedDict to ensure critical fields are explicitly passed across all state transitions. |
| Sprint 2 | Day 1 | Unsure how to simulate real enterprise APIs without expensive infrastructure. | Created utils/mock_data.json to act as a local, lightweight database representing 3 core IT services. |
| Sprint 2 | Day 2 | Groq API throwing Rate Limit Exceeded (429) errors because 4 agents are running in rapid sequence. | Switched DEFAULT_MODEL to llama3-8b-8192 to leverage higher free-tier token limits. |
| Sprint 2 | Day 3 | Streamlit Dashboard is showing "0 Tool Calls" even though the Investigation Agent is using tools. | Wrote custom parsing logic in investigation_agent.py to count m.type == "tool" messages and update UI metrics. |
| Sprint 3 | Day 1 | FastAPI server blocked all traffic and crashed ('Connection reset') when running complex 4-agent investigations. | Refactored the `/workflow/run` API endpoint from an `async def` to a standard `def` thread pool worker to prevent the event loop from blocking. |
| Sprint 3 | Day 2 | SQLite connection leaks caused "database is locked" errors when the Investigation Agent executed tools rapidly. | Added explicit `conn.close()` calls inside all early return paths within the SQLite-backed tools (health, logs, history, runbooks). |
| Sprint 3 | Day 3 | The system crashed or hallucinated when users asked about completely unmonitored services not in the DB. | Implemented a CRITICAL RULE prompt in the Decision Agent and Python parsing logic to auto-generate markdown escalation tickets (`INC-XXXX.md`). |

## 6. Agile Documentation (Retrospection)

| SL # | Sprint # | Sprint start date | Sprint end date | Team member name | Start Doing | Stop Doing | Continue Doing | Action taken |
|---|---|---|---|---|---|---|---|---|
| 1 | Sprint 1 | 02/09/2026 | 06/09/2026 | Vinesh | Using strictly typed dictionaries (AgentState) for LangGraph node communication. | Hardcoding agent prompts without clear boundaries. | Writing rapid prototype scripts to test LLM logic before full integration. | Refactored prompt templates to include strict role boundaries. |
| 2 | Sprint 1 | 02/09/2026 | 06/09/2026 | Vinesh | Implementing centralized logging to track which agent is executing at any time. | Relying on simple print statements which get lost in concurrent execution. | Breaking down complex workflows into smaller, specialized agents. | Added `utils/logging_config.py` and integrated standard Python logger. |
| 3 | Sprint 2 | 09/09/2026 | 13/09/2026 | Vinesh | Implementing comprehensive error handling inside Python tool executions to prevent agent crashes. | Relying on mocked JSON files that don't scale or handle concurrency well. | Validating tool execution with automated Pytest suites. | Migrated mock_data.json to SQLite (enterprise_mock.db) for robust data handling. |
| 4 | Sprint 2 | 09/09/2026 | 13/09/2026 | Vinesh | Parsing LLM outputs natively to capture tool usage metrics for the UI Dashboard. | Exceeding API rate limits by spamming heavy models for simple tasks. | Using ReAct Agent frameworks (`create_react_agent`) for dynamic tool selection. | Downgraded DEFAULT_MODEL to a faster, higher-limit tier for basic investigations. |
| 5 | Sprint 2 | 09/09/2026 | 13/09/2026 | Vinesh | Mocking external API responses to simulate network latency gracefully. | Allowing agents to hang indefinitely when an external service times out. | Structuring external API tools to return fallback data on failure. | Added a timeout parameter to the `check_external_service_status` tool. |
| 6 | Sprint 3 | 16/09/2026 | 20/09/2026 | Vinesh | Releasing database connections explicitly (`conn.close()`) to avoid SQLite thread locks. | Running long, blocking synchronous agent workflows inside FastAPI's async event loop. | Enforcing strict rule-based formatting in system prompts. | Converted `/workflow/run` endpoint to a standard thread-pool `def` to prevent connection resets. |
| 7 | Sprint 3 | 16/09/2026 | 20/09/2026 | Vinesh | Actively generating artifact tickets (Markdown files) when out-of-context services are queried. | Allowing agents to hallucinate responses when database metrics return empty. | Integrating long-term SQLite memory into planning and decision nodes for contextual awareness. | Implemented Python parsing logic to catch unmonitored systems and auto-escalate tickets (`INC-XXXX.md`). |
| 8 | Sprint 3 | 16/09/2026 | 20/09/2026 | Vinesh | Conditionally routing state directly from Analysis to Completed if risk is evaluated as 'Low'. | Forcing every request through the expensive Decision agent if it's a trivial query. | Persisting all workflow histories to the `agentsync_memory.db` for future context retrieval. | Added a risk-evaluation conditional edge in LangGraph to bypass the decision node. |
