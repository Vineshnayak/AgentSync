import pytest
from unittest.mock import patch, MagicMock
from workflow.state import AgentState
from workflow.agent_workflow import run_agent_workflow, evaluate_risk
from agents.planner_agent import run_planner

@pytest.fixture
def empty_state() -> AgentState:
    return {
        "user_request": "Payment API is returning 500 errors. Investigate.",
        "plan": "",
        "investigation_results": "",
        "analysis": "",
        "decision": "",
        "workflow_status": "Started",
        "errors": [],
        "execution_metadata": {}
    }

@patch("agents.planner_agent.ChatGroq")
def test_planner_agent(mock_chatgroq, empty_state):
    # Mock LLM response
    mock_llm = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "1. Check health. 2. Analyze logs."
    mock_llm.invoke.return_value = mock_response
    mock_chatgroq.return_value = mock_llm

    result_state = run_planner(empty_state)
    
    assert result_state["plan"] == "1. Check health. 2. Analyze logs."
    assert result_state["workflow_status"] == "Planned"

def test_risk_evaluation_high_risk():
    state: AgentState = {
        "user_request": "Test", "plan": "", "investigation_results": "",
        "analysis": "This indicates a high risk of failure.", "decision": "",
        "workflow_status": "Analyzed", "errors": [], "execution_metadata": {}
    }
    result = evaluate_risk(state)
    assert result["workflow_status"] == "High Risk - Human Review Required"

def test_risk_evaluation_low_risk():
    state: AgentState = {
        "user_request": "Test", "plan": "", "investigation_results": "",
        "analysis": "Everything looks stable.", "decision": "",
        "workflow_status": "Analyzed", "errors": [], "execution_metadata": {}
    }
    result = evaluate_risk(state)
    assert result["workflow_status"] == "Low Risk"

@patch("workflow.agent_workflow.run_decision")
@patch("workflow.agent_workflow.run_analysis")
@patch("workflow.agent_workflow.run_investigation")
@patch("workflow.agent_workflow.run_planner")
def test_workflow_execution(mock_planner, mock_investigation, mock_analysis, mock_decision):
    # Mock the agents to just pass through state modifications
    def mock_planner_side_effect(state):
        state["plan"] = "Plan."
        return state
    def mock_investigation_side_effect(state):
        state["investigation_results"] = "Data."
        return state
    def mock_analysis_side_effect(state):
        state["analysis"] = "Low risk analysis."
        return state
    def mock_decision_side_effect(state):
        state["decision"] = "Proceed."
        state["workflow_status"] = "Completed"
        return state

    mock_planner.side_effect = mock_planner_side_effect
    mock_investigation.side_effect = mock_investigation_side_effect
    mock_analysis.side_effect = mock_analysis_side_effect
    mock_decision.side_effect = mock_decision_side_effect
    
    final_state = run_agent_workflow("Test workflow")
    
    assert final_state["plan"] == "Plan."
    assert final_state["investigation_results"] == "Data."
    assert "Low risk analysis" in final_state["analysis"]
    assert final_state["decision"] == "Proceed."
    assert final_state["workflow_status"] == "Completed"
    assert mock_planner.called
    assert mock_investigation.called
    assert mock_analysis.called
    assert mock_decision.called
