import sqlite3
import os
from langchain_core.tools import tool
from utils.logging_config import setup_logger

logger = setup_logger("incident_history_tool")

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "enterprise_mock.db")

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
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        search_pattern = f"%{query}%"
        cursor.execute(
            "SELECT incident_id, service, description, resolution FROM historical_incidents WHERE LOWER(service) LIKE ? OR LOWER(description) LIKE ?",
            (search_pattern, search_pattern)
        )
        matches = cursor.fetchall()
        
        if not matches:
            conn.close()
            return f"No historical incidents found matching: {query}"
            
        result = f"Found {len(matches)} historical incident(s) matching '{query}':\n\n"
        for incident_id, service, description, resolution in matches:
            result += f"ID: {incident_id}\n"
            result += f"Service: {service}\n"
            result += f"Description: {description}\n"
            result += f"Resolution: {resolution}\n"
            result += "-" * 20 + "\n"
            
        conn.close()
        return result
        
    except Exception as e:
        error_msg = f"Error searching incident history: {str(e)}"
        logger.error(error_msg)
        return error_msg
