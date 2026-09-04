from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from workflow.state import AgentState
from config.settings import settings
from utils.logging_config import setup_logger, global_metrics

from tools.calculator_tool import calculate
from tools.knowledge_tool import retrieve_knowledge
from tools.business_tool import query_sales_data

logger = setup_logger("research_agent")

def run_research(state: AgentState) -> AgentState:
    logger.info("Research Agent started.")
    
    if state.get("research_results"):
        logger.info("Research results already exist. Skipping LLM call.")
        return state

    try:
        llm = ChatGroq(api_key=settings.GROQ_API_KEY, model=settings.DEFAULT_MODEL)
        
        tools = [calculate, retrieve_knowledge, query_sales_data]
        
        system_msg = "You are the Research Agent. Use available tools to gather required information based on the plan. Do not provide analysis, only facts and data."
        
        # create_react_agent handles the tool loop automatically
        agent = create_react_agent(llm, tools, prompt=system_msg)
        
        logger.info("Calling Groq API for research via React Agent.")
        
        # We invoke the agent with the user request and plan
        inputs = {"messages": [HumanMessage(content=f"User Request: {state['user_request']}\nPlan: {state['plan']}")]}
        result = agent.invoke(inputs)
        
        # The result["messages"] contains the conversation, the last AI message is the final output
        final_message = result["messages"][-1].content
        
        # increment LLM calls approximately (react agent may make multiple, but we just bump it by 1 for simplicity or count messages)
        # To be precise, we'd count the AI messages in the result
        ai_msg_count = sum(1 for m in result["messages"] if m.type == "ai")
        for _ in range(ai_msg_count):
            global_metrics.increment_llm()
            
        state["research_results"] = final_message
        state["workflow_status"] = "Researched"
        
    except Exception as e:
        logger.error(f"Research Agent failed: {e}")
        state["errors"].append(f"Research Error: {str(e)}")
        state["workflow_status"] = "Error"
        
    return state
