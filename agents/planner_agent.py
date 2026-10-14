from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from workflow.state import AgentState
from config.settings import settings
from utils.logging_config import setup_logger, global_metrics
from memory.memory_manager import memory_manager
from utils.llm_client import invoke_with_retry, sanitize_error

logger = setup_logger("planner_agent")

def run_planner(state: AgentState) -> AgentState:
    logger.info("Planner Agent started.")
    
    # Check if a plan already exists to avoid duplicate LLM calls
    if state.get("plan"):
        logger.info("Plan already exists. Skipping LLM call.")
        return state

    try:
        llm = ChatGroq(api_key=settings.GROQ_API_KEY, model=settings.DEFAULT_MODEL, max_retries=4)
        
        system_msg = SystemMessage(content="""You are the Lead Planning & Triage Agent for an Enterprise Multi-Agent Coordination Engine.
Analyze the user request to determine whether it is an IT Incident or a General/Informational Inquiry.

1. CATEGORY 1: IT INCIDENT OR INFRASTRUCTURE ISSUE
   Examples: service outages, 500 errors, database timeouts, latency spikes, pod crashes, memory leaks, unmonitored server issues, network drops.
   Instruction: Formulate a structured, step-by-step technical investigation plan specifying diagnostic tools to use (check health, examine logs, query past incident history, search runbooks). Do not include any prefix.

2. CATEGORY 2: GENERAL INQUIRY / FACTUAL QUESTION / NON-INCIDENT
   Examples: general knowledge questions (e.g. 'capital of india', 'what is 2+2', 'who is the CEO'), questions about company policies, greetings, or non-outage prompts.
   Instruction: Start your response with `[INFORMATIONAL_QUERY]` on the very first line. On subsequent lines, provide the direct, accurate, and concise answer to the user's question.
""")
        
        # Retrieve long-term memory for context-aware planning
        keywords = state['user_request'].split()
        search_keyword = keywords[0] if keywords else ""
        if len(keywords) > 2:
             search_keyword = max(keywords[:5], key=len)
             
        past_plans = memory_manager.get_past_decisions(search_keyword) 
        memory_context = ""
        if past_plans:
            memory_context = "\n\nPast Historical Context:\n"
            for req, dec in past_plans:
                memory_context += f"- Past Request: {req}\n"
                
        human_msg = HumanMessage(content=f"Business Request: {state['user_request']}{memory_context}")
        
        def fallback_plan() -> str:
            req = state.get('user_request', 'Service Outage')
            return (
                f"1. Probe service health and verify response codes for '{req}'.\n"
                f"2. Inspect recent server logs for connection and timeout exceptions.\n"
                f"3. Query historical incident database for matching failure signatures.\n"
                f"4. Search knowledge base runbooks for approved mitigation procedures."
            )

        logger.info("Calling LLM for planning with rate-limit protection.")
        content = invoke_with_retry(llm, [system_msg, human_msg], fallback_generator=fallback_plan).strip()
        
        is_info = (
            "[INFORMATIONAL_QUERY]" in content
            or "This interface is for IT Incident Resolution" in content
        )
        
        if is_info:
            direct_ans = content.replace("[INFORMATIONAL_QUERY]", "").strip()
            if "This interface is for IT Incident Resolution" in direct_ans and len(direct_ans.splitlines()) <= 2:
                direct_ans = f"Inquiry noted for: \"{state['user_request']}\". No IT service outage or infrastructure anomaly was detected. If you are reporting a system issue, please include the service name or error details."
                
            state["is_general_query"] = True
            state["severity"] = "Informational"
            state["plan"] = "Informational Request: Direct response formulated. No incident investigation plan required."
            state["investigation_results"] = "No infrastructure logs or metrics were probed (non-incident query)."
            state["analysis"] = "Request classified as General Inquiry. Zero operational risk or service degradation detected."
            state["decision"] = f"{direct_ans}\n\n*(Note: This query was processed as an informational inquiry. Since no infrastructure outage or service degradation was detected, no engineering personnel have been dispatched, and zero capacity was consumed.)*"
            state["workflow_status"] = "Completed (Informational)"
            state["assigned_engineer"] = None
            state["context_bundle"] = None
            state["wellbeing_alert"] = None
        else:
            state["is_general_query"] = False
            state["severity"] = "P1"
            state["plan"] = content
            state["workflow_status"] = "Planned"
        
    except Exception as e:
        logger.error(f"Planner Agent failed: {e}")
        state["errors"].append(f"Planner Error: {sanitize_error(e)}")
        state["workflow_status"] = "Error"
        
    return state
