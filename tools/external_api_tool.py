import requests
from requests.exceptions import Timeout, HTTPError, ConnectionError
from langchain_core.tools import tool
from utils.logging_config import setup_logger

logger = setup_logger("external_api_tool")

@tool
def check_external_service_status(service_url: str) -> str:
    """
    Makes a real HTTP GET request to check if an external dependency or third-party service is up and running.
    
    Args:
        service_url: The URL of the external service to check (e.g., 'https://httpbin.org/status/200').
        
    Returns:
        A string indicating the HTTP status code and response time, or an error message if the service is unreachable.
    """
    logger.info(f"Checking external service status for URL: {service_url}")
    
    # Simple validation to ensure it's a URL
    if not service_url.startswith("http://") and not service_url.startswith("https://"):
        return f"Error: Invalid URL '{service_url}'. URL must start with http:// or https://"
        
    try:
        response = requests.get(service_url, timeout=5)
        response.raise_for_status()
        
        elapsed_ms = int(response.elapsed.total_seconds() * 1000)
        result = f"External service {service_url} is reachable. Status code: {response.status_code}. Latency: {elapsed_ms}ms"
        logger.info(result)
        return result
        
    except Timeout:
        error_msg = f"Error: Request to {service_url} timed out after 5 seconds."
        logger.error(error_msg)
        return error_msg
    except HTTPError as e:
        error_msg = f"Error: HTTP Error occurred when contacting {service_url}: {e.response.status_code}"
        logger.error(error_msg)
        return error_msg
    except ConnectionError:
        error_msg = f"Error: Failed to establish a connection to {service_url}."
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Error: An unexpected error occurred when checking {service_url}: {str(e)}"
        logger.error(error_msg)
        return error_msg
