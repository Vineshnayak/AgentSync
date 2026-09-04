from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from workflow.state import AgentState
from config.settings import settings
from utils.logging_config import setup_logger, global_metrics

logger = setup_logger("analysis_agent")

def run_analysis(state: AgentState) -> AgentState:
    logger.info("Analysis Agent started.")
    
    if state.get("analysis"):
        logger.info("Analysis already exists. Skipping LLM call.")
        return state

    try:
        llm = ChatGroq(api_key=settings.GROQ_API_KEY, model=settings.DEFAULT_MODEL)
        
        system_msg = SystemMessage(content="""You are the Analysis Agent.
Your job is to analyze the information produced by the Research Agent.
Identify patterns, risks, factors, and key findings. Produce structured analysis.
Do not make the final decision; leave that for the Decision Agent.
""")
        human_msg = HumanMessage(content=f"User Request: {state['user_request']}\nResearch Data: {state['research_results']}")
        
        logger.info("Calling Groq API for analysis.")
        response = llm.invoke([system_msg, human_msg])
        global_metrics.increment_llm()
        
        state["analysis"] = response.content
        state["workflow_status"] = "Analyzed"
        
    except Exception as e:
        logger.error(f"Analysis Agent failed: {e}")
        state["errors"].append(f"Analysis Error: {str(e)}")
        state["workflow_status"] = "Error"
        
    return state
