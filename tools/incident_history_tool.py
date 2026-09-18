import json
import os
from langchain_core.tools import tool
from utils.logging_config import setup_logger

logger = setup_logger("incident_history_tool")

MOCK_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "utils", "mock_data.json")

def load_mock_data():
    try:
        with open(MOCK_DATA_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load mock data: {e}")
        return {}

@tool
def search_incident_history(query: str) -> str:
    """
    Searches historical incidents for similar issues and their resolutions.
    
    Args:
        query: The search term, such as a service name or error description (e.g., 'Payment API', 'latency').
        
    Returns:
        A formatted string of matching historical incidents.
    """
    logger.info(f"Searching incident history for: {query}")
    query = query.lower()
    
    try:
        data = load_mock_data()
        incidents = data.get("incidents", [])
        
        matches = []
        for inc in incidents:
            if query in inc.get("service", "").lower() or query in inc.get("description", "").lower():
                matches.append(inc)
                
        if not matches:
            return f"No historical incidents found matching: {query}"
            
        result = f"Found {len(matches)} historical incident(s) matching '{query}':\n\n"
        for inc in matches:
            result += f"ID: {inc.get('id')}\n"
            result += f"Service: {inc.get('service')}\n"
            result += f"Description: {inc.get('description')}\n"
            result += f"Resolution: {inc.get('resolution')}\n"
            result += "-" * 20 + "\n"
            
        return result
        
    except Exception as e:
        error_msg = f"Error searching incident history: {str(e)}"
        logger.error(error_msg)
        return error_msg
