from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from workflow.state import AgentState
from config.settings import settings
from utils.logging_config import setup_logger, global_metrics

logger = setup_logger("decision_agent")

def run_decision(state: AgentState) -> AgentState:
    logger.info("Decision Agent started.")
    
    if state.get("decision"):
        logger.info("Decision already exists. Skipping LLM call.")
        return state

    try:
        llm = ChatGroq(api_key=settings.GROQ_API_KEY, model=settings.DEFAULT_MODEL)
        
        system_msg = SystemMessage(content="""You are the Decision Agent.
Evaluate the analysis provided and formulate a final recommendation/decision.
Compare available options and explain your reasoning clearly.
Provide a complete, final user-facing response.
""")
        human_msg = HumanMessage(content=f"User Request: {state['user_request']}\nAnalysis: {state['analysis']}")
        
        logger.info("Calling Groq API for decision.")
        response = llm.invoke([system_msg, human_msg])
        global_metrics.increment_llm()
        
        state["decision"] = response.content
        state["workflow_status"] = "Completed"
        
    except Exception as e:
        logger.error(f"Decision Agent failed: {e}")
        state["errors"].append(f"Decision Error: {str(e)}")
        state["workflow_status"] = "Error"
        
    return state
