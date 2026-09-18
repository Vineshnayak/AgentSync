import json
import os
from langchain_core.tools import tool
from utils.logging_config import setup_logger

logger = setup_logger("service_health_tool")

MOCK_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "utils", "mock_data.json")

def load_mock_data():
    try:
        with open(MOCK_DATA_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load mock data: {e}")
        return {}

@tool
def check_health(service: str) -> str:
    """
    Checks the current health status and metrics of a service.
    
    Args:
        service: The name of the service to check (e.g., 'Payment API', 'Auth Service', 'Web Frontend').
        
    Returns:
        A formatted string detailing the service status and key metrics.
    """
    logger.info(f"Checking health for service: {service}")
    
    try:
        data = load_mock_data()
        health_data = data.get("health", {})
        
        if service not in health_data:
            return f"Service not found: {service}. Available services: {list(health_data.keys())}"
            
        health = health_data[service]
        status = health.get("status", "Unknown")
        metrics = health.get("metrics", {})
        
        result = f"Service: {service}\nStatus: {status}\nMetrics:\n"
        for k, v in metrics.items():
            result += f"- {k}: {v}\n"
            
        return result
        
    except Exception as e:
        error_msg = f"Error checking service health: {str(e)}"
        logger.error(error_msg)
        return error_msg
