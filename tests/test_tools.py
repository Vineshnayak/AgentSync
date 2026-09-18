import pytest
from unittest.mock import patch, mock_open

from tools.log_analyzer_tool import analyze_logs
from tools.service_health_tool import check_health
from tools.incident_history_tool import search_incident_history
from tools.knowledge_base_tool import search_runbooks
from tools.incident_action_tool import manage_incident

MOCK_JSON_DATA = """
{
    "logs": {
        "Payment API": [
            {"timestamp": "2026-09-18T10:00:00Z", "level": "ERROR", "message": "500 Error"}
        ]
    },
    "health": {
        "Payment API": {"status": "Down", "metrics": {"latency_ms": 5000}}
    },
    "incidents": [
        {"id": "INC-001", "service": "Payment API", "description": "Failure", "resolution": "Fixed"}
    ],
    "runbooks": {
        "Payment API": ["1. Check DB"]
    }
}
"""

@patch("builtins.open", new_callable=mock_open, read_data=MOCK_JSON_DATA)
def test_log_analyzer_tool_success(mock_file):
    result = analyze_logs.invoke({"service": "Payment API", "time_range": "last 1h"})
    assert "500 Error" in result
    assert "Payment API" in result

@patch("builtins.open", new_callable=mock_open, read_data=MOCK_JSON_DATA)
def test_log_analyzer_tool_not_found(mock_file):
    result = analyze_logs.invoke({"service": "Unknown API", "time_range": "last 1h"})
    assert "No logs found for service" in result

@patch("builtins.open", new_callable=mock_open, read_data=MOCK_JSON_DATA)
def test_service_health_tool_success(mock_file):
    result = check_health.invoke({"service": "Payment API"})
    assert "Status: Down" in result
    assert "latency_ms: 5000" in result

@patch("builtins.open", new_callable=mock_open, read_data=MOCK_JSON_DATA)
def test_incident_history_tool_success(mock_file):
    result = search_incident_history.invoke({"query": "payment"})
    assert "INC-001" in result
    assert "Failure" in result

@patch("builtins.open", new_callable=mock_open, read_data=MOCK_JSON_DATA)
def test_knowledge_base_tool_success(mock_file):
    result = search_runbooks.invoke({"query": "payment"})
    assert "1. Check DB" in result

def test_incident_action_tool_success():
    result = manage_incident.invoke({"action": "create", "details": "API is down"})
    assert "Incident created successfully" in result
    assert "Ticket ID: INC-" in result

def test_incident_action_tool_invalid_action():
    result = manage_incident.invoke({"action": "delete", "details": "API is down"})
    assert "Invalid action" in result
