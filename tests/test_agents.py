import pytest
from unittest.mock import patch, MagicMock
from workflow.state import AgentState
from workflow.agent_workflow import run_agent_workflow, evaluate_risk
from agents.planner_agent import run_planner

@pytest.fixture
def empty_state() -> AgentState:
    return {
        "user_request": "Analyze sales in North America for Q1.",
        "plan": "",
        "research_results": "",
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
    mock_response.content = "1. Research NA Q1 sales. 2. Analyze data."
    mock_llm.invoke.return_value = mock_response
    mock_chatgroq.return_value = mock_llm

    result_state = run_planner(empty_state)
    
    assert result_state["plan"] == "1. Research NA Q1 sales. 2. Analyze data."
    assert result_state["workflow_status"] == "Planned"

def test_risk_evaluation_high_risk():
    state: AgentState = {
        "user_request": "Test", "plan": "", "research_results": "",
        "analysis": "This indicates a high risk of failure.", "decision": "",
        "workflow_status": "Analyzed", "errors": [], "execution_metadata": {}
    }
    result = evaluate_risk(state)
    assert result["workflow_status"] == "High Risk - Human Review Required"

def test_risk_evaluation_low_risk():
    state: AgentState = {
        "user_request": "Test", "plan": "", "research_results": "",
        "analysis": "Everything looks stable.", "decision": "",
        "workflow_status": "Analyzed", "errors": [], "execution_metadata": {}
    }
    result = evaluate_risk(state)
    assert result["workflow_status"] == "Low Risk"

@patch("workflow.agent_workflow.run_decision")
@patch("workflow.agent_workflow.run_analysis")
@patch("workflow.agent_workflow.run_research")
@patch("workflow.agent_workflow.run_planner")
def test_workflow_execution(mock_planner, mock_research, mock_analysis, mock_decision):
    # Mock the agents to just pass through state modifications
    def mock_planner_side_effect(state):
        state["plan"] = "Plan."
        return state
    def mock_research_side_effect(state):
        state["research_results"] = "Data."
        return state
    def mock_analysis_side_effect(state):
        state["analysis"] = "Low risk analysis."
        return state
    def mock_decision_side_effect(state):
        state["decision"] = "Proceed."
        state["workflow_status"] = "Completed"
        return state

    mock_planner.side_effect = mock_planner_side_effect
    mock_research.side_effect = mock_research_side_effect
    mock_analysis.side_effect = mock_analysis_side_effect
    mock_decision.side_effect = mock_decision_side_effect
    
    final_state = run_agent_workflow("Test workflow")
    
    assert final_state["plan"] == "Plan."
    assert final_state["research_results"] == "Data."
    assert "Low risk analysis" in final_state["analysis"]
    assert final_state["decision"] == "Proceed."
    assert final_state["workflow_status"] == "Completed"
    assert mock_planner.called
    assert mock_research.called
    assert mock_analysis.called
    assert mock_decision.called
