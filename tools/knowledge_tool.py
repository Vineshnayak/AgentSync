from langchain_core.tools import tool
from utils.logging_config import setup_logger, global_metrics

logger = setup_logger("knowledge_tool")

# Mock simple knowledge base
KNOWLEDGE_BASE = {
    "company policy": "Employees are entitled to 20 days of paid leave per year. Overtime is compensated at 1.5x regular pay.",
    "product roadmap": "Q1: Launch new AgentSync platform. Q2: Integrate with CRM systems. Q3: Expand API support.",
    "support contacts": "IT Support: it-help@company.com. HR: hr@company.com."
}

@tool
def retrieve_knowledge(topic: str) -> str:
    """Useful for retrieving static knowledge about the company, policies, or roadmaps.
    Input should be a simple topic keyword like 'company policy', 'product roadmap', or 'support contacts'.
    """
    logger.info(f"Tool called: retrieve_knowledge with topic: {topic}")
    global_metrics.increment_tool()
    
    topic_lower = topic.lower()
    for key, value in KNOWLEDGE_BASE.items():
        if key in topic_lower or topic_lower in key:
            return f"Knowledge found for '{topic}': {value}"
            
    return f"No knowledge found for topic: '{topic}'"
