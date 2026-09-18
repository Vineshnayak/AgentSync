import json
import os
from langchain_core.tools import tool
from utils.logging_config import setup_logger

logger = setup_logger("log_analyzer_tool")

MOCK_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "utils", "mock_data.json")

def load_mock_data():
    try:
        with open(MOCK_DATA_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load mock data: {e}")
        return {}

@tool
def analyze_logs(service: str, time_range: str = "last 24 hours") -> str:
    """
    Analyzes service logs for errors or anomalies.
    
    Args:
        service: The name of the service to analyze (e.g., 'Payment API', 'Auth Service').
        time_range: The time range to analyze logs for.
        
    Returns:
        A formatted string of logs or an error message if the service is not found.
    """
    logger.info(f"Analyzing logs for service: {service}, time_range: {time_range}")
    
    try:
        data = load_mock_data()
        logs_data = data.get("logs", {})
        
        if service not in logs_data:
            return f"No logs found for service: {service}. Available services: {list(logs_data.keys())}"
        
        logs = logs_data[service]
        
        if not logs:
            return f"No recent logs for {service}."
            
        result = f"Logs for {service} ({time_range}):\n"
        for log in logs:
            result += f"[{log['timestamp']}] {log['level']}: {log['message']}\n"
            
        return result
        
    except Exception as e:
        error_msg = f"Error analyzing logs: {str(e)}"
        logger.error(error_msg)
        return error_msg
