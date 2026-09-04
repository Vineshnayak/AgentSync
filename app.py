import streamlit as st
from config.settings import settings
import time
from workflow.agent_workflow import run_agent_workflow

st.set_page_config(page_title="AgentSync", page_icon="🤖", layout="wide")

st.title("🤖 AgentSync Dashboard")
st.markdown("An AI Agent Coordination & Decision Engine")

# Check config
try:
    settings.validate()
except ValueError as e:
    st.error(str(e))
    st.stop()

st.sidebar.header("Configuration")
st.sidebar.info(f"Model: {settings.DEFAULT_MODEL}")
st.sidebar.info(f"Database: {settings.DATABASE_URL}")

user_request = st.text_area("Business Request", height=100, placeholder="Enter a business problem for the agents to solve...")

if st.button("Run AgentSync", type="primary"):
    if not user_request.strip():
        st.warning("Please enter a business request.")
    else:
        with st.spinner("Agents are coordinating..."):
            
            # Run Workflow
            final_state = run_agent_workflow(user_request)
            
            st.success("Workflow Complete!")
            
            # Display metrics
            metrics = final_state.get("execution_metadata", {})
            col1, col2, col3 = st.columns(3)
            col1.metric("Execution Time", f"{metrics.get('duration_seconds', 0)}s")
            col2.metric("LLM Calls", metrics.get("llm_calls", 0))
            col3.metric("Tool Calls", metrics.get("tool_calls", 0))
            
            # Display errors if any
            if final_state.get("errors"):
                st.error("Errors encountered during execution:")
                for err in final_state["errors"]:
                    st.write(f"- {err}")
                    
            st.divider()
            
            # Display workflow results
            tabs = st.tabs(["Planner", "Research", "Analysis", "Decision"])
            
            with tabs[0]:
                st.subheader("Plan")
                st.write(final_state.get("plan", "No plan generated."))
                
            with tabs[1]:
                st.subheader("Research Results")
                st.write(final_state.get("research_results", "No research data."))
                
            with tabs[2]:
                st.subheader("Analysis")
                st.write(final_state.get("analysis", "No analysis available."))
                
            with tabs[3]:
                st.subheader("Final Decision")
                st.write(final_state.get("decision", "No decision made."))
