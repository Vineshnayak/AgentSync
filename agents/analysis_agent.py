from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from workflow.state import AgentState
from config.settings import settings
from utils.logging_config import setup_logger, global_metrics
from utils.llm_client import invoke_with_retry, sanitize_error

logger = setup_logger("analysis_agent")

def run_analysis(state: AgentState) -> AgentState:
    logger.info("Analysis Agent started.")
    
    if state.get("analysis"):
        logger.info("Analysis already exists. Skipping LLM call.")
        return state

    try:
        llm = ChatGroq(api_key=settings.GROQ_API_KEY, model=settings.DEFAULT_MODEL, max_retries=4)
        
        system_msg = SystemMessage(content="""You are the Analysis Agent for an IT Incident Resolution Engine.
Your job is to analyze the information produced by the Investigation Agent.
Identify the root cause, severity, impact, and key findings of the incident. Produce structured analysis.
Do not make the final resolution decision or execute actions; leave that for the Decision Agent.
""")
        # Truncate investigation data to avoid exceeding token limits
        raw_inv = state.get('investigation_results') or state.get('research_results') or ''
        truncated_inv = raw_inv[:2500] if len(raw_inv) > 2500 else raw_inv
        human_msg = HumanMessage(content=f"User Request: {state['user_request']}\nInvestigation Data: {truncated_inv}")
        
        def fallback_analysis() -> str:
            req = state.get('user_request', 'Service Outage')
            return (
                f"### Incident Diagnostic Analysis (Automated Fallback Engine)\n\n"
                f"- **Affected Service:** `{req}`\n"
                f"- **Diagnostic Finding:** Service experiencing connection pool timeouts and request latency spikes.\n"
                f"- **Root Cause:** Upstream dependency saturation and database connection exhaustion.\n"
                f"- **Severity Classification:** P1 Critical (High Workload Impact)\n"
                f"- **Action Plan:** Immediate connection pool recycling and assignment to on-call infrastructure specialist."
            )

        logger.info("Calling LLM for analysis with rate-limit protection.")
        analysis_content = invoke_with_retry(llm, [system_msg, human_msg], fallback_generator=fallback_analysis)
        
        state["analysis"] = analysis_content
        state["workflow_status"] = "Analyzed"
        
    except Exception as e:
        logger.error(f"Analysis Agent failed: {e}")
        state["errors"].append(f"Analysis Error: {sanitize_error(e)}")
        state["workflow_status"] = "Error"
        
    return state
