from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from workflow.state import AgentState
from config.settings import settings
from utils.logging_config import setup_logger, global_metrics

from tools.log_analyzer_tool import analyze_logs
from tools.service_health_tool import check_health
from tools.incident_history_tool import search_incident_history
from tools.knowledge_base_tool import search_runbooks
from tools.incident_action_tool import manage_incident
from tools.external_api_tool import check_external_service_status

from utils.llm_client import sanitize_error

logger = setup_logger("investigation_agent")

def run_investigation(state: AgentState) -> AgentState:
    logger.info("Investigation Agent started.")
    
    if state.get("investigation_results"):
        logger.info("Investigation results already exist. Skipping LLM call.")
        return state

    try:
        llm = ChatGroq(api_key=settings.GROQ_API_KEY, model=settings.DEFAULT_MODEL, max_retries=4)
        
        tools = [analyze_logs, check_health, search_incident_history, search_runbooks, manage_incident, check_external_service_status]
        
        system_msg = (
            "You are the Investigation Agent for IT Incident Resolution. "
            "Select 2 to 3 essential tools (such as check_health, analyze_logs, search_runbooks) to gather evidence. "
            "Do not execute more than 3 tool calls. "
            "Immediately synthesize the gathered logs and metrics into your final evidence summary."
        )
        
        agent = create_react_agent(llm, tools, prompt=system_msg)
        
        logger.info("Calling Groq API for investigation via React Agent.")
        
        req_snippet = state['user_request'][:500]
        plan_snippet = state['plan'][:1000]
        inputs = {"messages": [HumanMessage(content=f"User Request: {req_snippet}\nPlan: {plan_snippet}")]}
        result = agent.invoke(inputs, {"recursion_limit": 10})
        
        final_message = result["messages"][-1].content
        
        ai_msg_count = sum(1 for m in result["messages"] if m.type == "ai")
        for _ in range(ai_msg_count):
            global_metrics.increment_llm()
            
        tool_msg_count = sum(1 for m in result["messages"] if m.type == "tool")
        for _ in range(tool_msg_count):
            global_metrics.increment_tool()
            
        state["investigation_results"] = final_message
        state["workflow_status"] = "Investigated"
        
    except Exception as e:
        logger.error(f"Investigation Agent failed: {e}")
        state["errors"].append(f"Investigation Error: {sanitize_error(e)}")
        state["workflow_status"] = "Error"
        
    return state
