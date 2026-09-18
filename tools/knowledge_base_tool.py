import json
import os
from langchain_core.tools import tool
from utils.logging_config import setup_logger

logger = setup_logger("knowledge_base_tool")

MOCK_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "utils", "mock_data.json")

def load_mock_data():
    try:
        with open(MOCK_DATA_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load mock data: {e}")
        return {}

@tool
def search_runbooks(query: str) -> str:
    """
    Retrieves troubleshooting steps and runbooks from the knowledge base.
    
    Args:
        query: The service name or error topic to find runbooks for (e.g., 'Payment API', 'Auth Service').
        
    Returns:
        A formatted string containing the runbook steps, or a not-found message.
    """
    logger.info(f"Searching runbooks for: {query}")
    query = query.lower()
    
    try:
        data = load_mock_data()
        runbooks = data.get("runbooks", {})
        
        matches = []
        for service, steps in runbooks.items():
            if query in service.lower():
                matches.append((service, steps))
                
        if not matches:
            return f"No runbooks found matching: {query}. Available runbooks for: {list(runbooks.keys())}"
            
        result = ""
        for service, steps in matches:
            result += f"Runbook for {service}:\n"
            for step in steps:
                result += f"{step}\n"
            result += "\n"
            
        return result
        
    except Exception as e:
        error_msg = f"Error searching knowledge base: {str(e)}"
        logger.error(error_msg)
        return error_msg
