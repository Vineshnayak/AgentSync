# Milestone 2: Excel Updates (IT Incident Resolution Engine)

Here is the row and column data reflecting our latest progress for Milestone 2 based on the shift to the **IT Incident Resolution** use-case. You can copy and paste these tables directly into your respective Excel/Word files.

## 1. Agile Template (`Agile_Template_v0.1 InfySpringboard.xlsm`)
*Use this for your Sprint Backlog or Task Tracking sheet.*

| Planned Sprint | Actual Sprint | US ID | User Story Description | MOSCOW | Dependency | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Sprint 2 | Sprint 2 | US - 06 | Develop Mock Enterprise Backend (mock_data.json) for IT Incidents | MUST HAVE | US - 01 | Vinesh | 3- Completed |
| Sprint 2 | Sprint 2 | US - 07 | Develop IT Incident Tools (Logs, Health, History, Runbooks, Action) | MUST HAVE | US - 06 | Vinesh | 3- Completed |
| Sprint 2 | Sprint 2 | US - 08 | Develop External API Connector Tool handling real HTTP requests | MUST HAVE | US - 01 | Vinesh | 3- Completed |
| Sprint 2 | Sprint 2 | US - 09 | Integrate tools into Investigation Agent using ReAct framework | MUST HAVE | US - 07, US-08 | Vinesh | 3- Completed |
| Sprint 2 | Sprint 2 | US - 10 | Write Pytest unit tests validating success and exception paths | MUST HAVE | US - 09 | Vinesh | 3- Completed |

---

## 2. Defect Tracker Template (`Defect_Tracker Template_v0.1 InfySpringboard.xlsx`)
*Use this to log issues we encountered and fixed during tool integration.*

| Sl No | Submitted By | Submitted Date | Description | Detected Sprint | Assigned To | Type Of Defect | Action Taken | Action Taken Date | Status(Open/Closed) | Remarks |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 3 | Vinesh | 18/09/2026 | Streamlit UI showing "0 Tool Calls" even when tools are executed. | Sprint 2 | Vinesh | Logical | Updated `investigation_agent.py` to count `m.type == "tool"` from React agent messages and increment `global_metrics`. | 18/09/2026 | Closed | Resolved |
| 4 | Vinesh | 18/09/2026 | Groq API throwing "Rate Limit Exceeded (429)" / "Request too large" errors. | Sprint 2 | Vinesh | Integration | Switched `DEFAULT_MODEL` to `llama3-8b-8192` to leverage higher free-tier token limits and removed restrictive `max_tokens`. | 18/09/2026 | Closed | Resolved |
| 5 | Vinesh | 18/09/2026 | `manage_incident` tool crashing when provided an invalid action type. | Sprint 2 | Vinesh | Logical | Added validation to return an "Invalid action" error string instead of crashing. | 18/09/2026 | Closed | Resolved |

---

## 3. Unit Test Plan Template (`Unit_Test_Plan_v0.1 InfySpringboard.xlsx`)
*Use this for your Test Cases / Unit Test tracking sheet.*

| Sl: No: | Test Case Name | Test Procedure | Condition to be tested | Expected Result | Actual Result |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 5 | Log Analyzer Tool Execution | Run test_log_analyzer fetching logs for a mocked service. | Verify the tool successfully parses `mock_data.json` and returns the log string. | Returns mocked log data string | Returned mocked log data string |
| 6 | Incident Action Invalid Input | Run test_incident_action_tool_invalid_action with action "delete". | Verify tool handles invalid actions without crashing. | Returns "Invalid action" error message | Returned "Invalid action" error message |
| 7 | External API HTTP Success | Run test_external_api_tool_success with mocked 200 OK response. | Verify the tool successfully parses standard HTTP responses. | Returns status code and latency string | Returned status code and latency string |
| 8 | External API Timeout | Run test_external_api_tool_timeout simulating a timeout exception. | Verify the tool safely catches requests.exceptions.Timeout. | Returns "timed out after 5 seconds" error | Caught timeout and returned error string |
| 9 | Investigation Agent ReAct Integration | Run agent with ReAct framework passing a mocked plan. | Verify the agent correctly identifies which tool to call based on the input text. | Tool is invoked and evidence string is returned | Tool invoked and evidence string returned |

---

## 4. Stand Up Meeting (`Agile_Template_v0.1 InfySpringboard.xlsm`)
*Use this for the 'Stand up Meeting' tab in your Agile template.*

| Sprint | Day | Impediments | Action Taken |
| :--- | :--- | :--- | :--- |
| Sprint 2 | Day 1 | Unsure how to simulate real enterprise APIs without expensive infrastructure. | Created `utils/mock_data.json` to act as a local, lightweight database representing 3 core IT services. |
| Sprint 2 | Day 2 | Groq API throwing Rate Limit Exceeded (429) errors because 4 agents are running in rapid sequence. | Switched `DEFAULT_MODEL` to `llama3-8b-8192` to leverage higher free-tier token limits. |
| Sprint 2 | Day 3 | Streamlit Dashboard is showing "0 Tool Calls" even though the Investigation Agent is using tools. | Wrote custom parsing logic in `investigation_agent.py` to count `m.type == "tool"` messages and update UI metrics. |

---

## 5. Sprint Backlog (`Agile_Template_v0.1 InfySpringboard.xlsm`)
*Use this for the 'Sprint Backlog' tab in your Agile template.*

| US ID | Task ID | Task Description | Task Start Date | Task Completion Date | Team Member | Activity | Status | Original Estimate | Day 1 | Day 2 | Day 3 | Day 4 | Day 5 | Day 6 | Day 7 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| US - 06 | T-01 | Create `mock_data.json` with realistic IT incident scenarios. | 16/09/2026 | 16/09/2026 | Vinesh | Development | Completed | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| US - 07 | T-02 | Code 5 Python tools for local JSON parsing. | 17/09/2026 | 17/09/2026 | Vinesh | Development | Completed | 5 | 0 | 5 | 0 | 0 | 0 | 0 | 0 |
| US - 08 | T-03 | Use `requests` library to build External API connector. | 18/09/2026 | 18/09/2026 | Vinesh | Development | Completed | 3 | 0 | 0 | 3 | 0 | 0 | 0 | 0 |
| US - 09 | T-04 | Implement LangGraph `create_react_agent` for tool routing. | 18/09/2026 | 18/09/2026 | Vinesh | Integration | Completed | 4 | 0 | 0 | 4 | 0 | 0 | 0 | 0 |
| US - 10 | T-05 | Write Pytest test cases in `test_tools.py`. | 18/09/2026 | 18/09/2026 | Vinesh | Testing | Completed | 3 | 0 | 0 | 3 | 0 | 0 | 0 | 0 |

---

## 6. Retrospection (`Agile_Template_v0.1 InfySpringboard.xlsm`)
*Use this for the 'Retrospection' tab in your Agile template.*

| SL # | Sprint # | Sprint start date | Sprint end date | Team member name | Start Doing | Stop Doing | Continue Doing | Action taken |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Sprint 1 | 02/09/2026 | 15/09/2026 | Vinesh | Better modularizing of Python logic and prompts. | Hardcoding database connection logic directly inside agent files. | Fast prototyping of basic agent structures using LangChain. | Created `utils/mock_data.json` to keep logic fully separated from agents. |
| 2 | Sprint 2 | 16/09/2026 | 18/09/2026 | Vinesh | Using real LLM API rate-limit testing before running multi-agent workflows. | Using restrictive `max_tokens` for agents that need to generate complex reasoning. | Writing comprehensive Pytest cases to validate every tool response. | Switched default model to `llama3-8b-8192` to permanently resolve Groq rate limit crashes. |
