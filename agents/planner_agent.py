from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from workflow.state import AgentState
from config.settings import settings
from utils.logging_config import setup_logger, global_metrics

logger = setup_logger("planner_agent")

def run_planner(state: AgentState) -> AgentState:
    logger.info("Planner Agent started.")
    
    # Check if a plan already exists to avoid duplicate LLM calls
    if state.get("plan"):
        logger.info("Plan already exists. Skipping LLM call.")
        return state

    try:
        llm = ChatGroq(api_key=settings.GROQ_API_KEY, model=settings.DEFAULT_MODEL)
        
        system_msg = SystemMessage(content="""You are the Planner Agent. 
Your job is to understand the business request and break it down into a clear, structured plan.
Identify which tools and steps are required (e.g., research, analysis, decision).
Do not perform the research or analysis yourself. Just output the step-by-step plan.
""")
        human_msg = HumanMessage(content=f"Business Request: {state['user_request']}")
        
        logger.info("Calling Groq API for planning.")
        response = llm.invoke([system_msg, human_msg])
        global_metrics.increment_llm()
        
        state["plan"] = response.content
        state["workflow_status"] = "Planned"
        
    except Exception as e:
        logger.error(f"Planner Agent failed: {e}")
        state["errors"].append(f"Planner Error: {str(e)}")
        state["workflow_status"] = "Error"
        
    return state
