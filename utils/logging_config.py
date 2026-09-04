import logging
import sys

def setup_logger(name: str) -> logging.Logger:
    """Sets up a lightweight logger for the AgentSync project."""
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
        
    return logger

# Global metrics tracker (in a real app this would be in a DB or proper metrics registry, 
# but for a lightweight prototype, an in-memory struct is fine to pass to Streamlit).
class ExecutionMetrics:
    def __init__(self):
        self.llm_calls = 0
        self.tool_calls = 0
        
    def reset(self):
        self.llm_calls = 0
        self.tool_calls = 0
        
    def increment_llm(self):
        self.llm_calls += 1
        
    def increment_tool(self):
        self.tool_calls += 1

global_metrics = ExecutionMetrics()
