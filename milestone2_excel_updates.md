# Milestone 2: Excel Updates

Here is the row and column data reflecting today's progress for Milestone 2. You can copy and paste these tables directly into your respective Excel files.

## 1. Agile Template (`Agile_Template_v0.1 InfySpringboard.xlsm`)
*Use this for your Sprint Backlog or Task Tracking sheet.*

| Task ID | Task Description | Status | Owner | Comments |
| :--- | :--- | :--- | :--- | :--- |
| **M2-01** | Create API Connector Tool using `requests` library | Done | [Your Name] | Implemented `fetch_public_data` with HTTP exception handling. |
| **M2-02** | Integrate API Tool with Research Agent | Done | [Your Name] | Registered tool in `create_react_agent` for Groq LLM tool selection. |
| **M2-03** | Develop unit tests for `calculator_tool` | Done | [Your Name] | Validated success paths and safe evaluation exceptions. |
| **M2-04** | Develop unit tests for `business_tool` | Done | [Your Name] | Validated DB querying and simulated connection errors. |
| **M2-05** | Develop unit tests for `api_connector_tool` | Done | [Your Name] | Validated handling of HTTP errors, timeouts, and JSON/Text responses. |

---

## 2. Defect Tracker Template (`Defect_Tracker Template_v0.1 InfySpringboard.xlsx`)
*Use this to log issues we encountered and fixed during tool integration.*

| Defect ID | Description | Component | Severity | Status | Resolution |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **DEF-001** | Missing `langgraph` dependency in virtual environment causing tests to fail | Environment Setup | Medium | Closed | Activated the `.venv` where `langgraph` and `requests` are properly installed. |
| **DEF-002** | Unhandled exceptions crashing the agent during invalid tool inputs | Tool Execution | High | Closed | Added try-catch blocks to all tools; they now return error strings instead of halting the agent workflow. |

---

## 3. Unit Test Plan Template (`Unit_Test_Plan_v0.1 InfySpringboard.xlsx`)
*Use this for your Test Cases / Unit Test tracking sheet.*

| Test Case ID | Module / Component | Test Description | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Tools / Calculator | Test valid math expression | Returns correctly calculated numerical string | Returned correctly | **Pass** |
| **TC-02** | Tools / Calculator | Test division by zero or invalid input | Returns "Error evaluating expression" string | Returned error string | **Pass** |
| **TC-03** | Tools / Business | Test valid region and quarter | Returns revenue data for the requested period | Returned revenue | **Pass** |
| **TC-04** | Tools / Business | Test missing region data | Returns "No sales data found" message | Returned fallback msg | **Pass** |
| **TC-05** | Tools / Business | Test DB connection failure | Catches exception and returns "Database error" | Caught exception | **Pass** |
| **TC-06** | Tools / API Connector | Test valid JSON API response | Returns stringified JSON payload | Returned string | **Pass** |
| **TC-07** | Tools / API Connector | Test HTTP Error (e.g., 404 Not Found) | Returns "HTTP Error" string | Caught HTTP error | **Pass** |
| **TC-08** | Tools / API Connector | Test Timeout Error | Returns "API Request timed out" string | Caught timeout error | **Pass** |
| **TC-09** | Tools / Knowledge | Test valid knowledge retrieval | Returns policy information from local dict | Returned policy info | **Pass** |
