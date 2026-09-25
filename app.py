import streamlit as st
from config.settings import settings
import time
from workflow.agent_workflow import run_agent_workflow

st.set_page_config(
    page_title="AgentSync Enterprise", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Minimalist Enterprise Look
st.markdown("""
<style>
    /* Hide Streamlit default branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Clean up the main container padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Typography adjustments */
    h1 {
        font-weight: 600;
        font-size: 2.2rem;
        color: #111827;
        margin-bottom: 0.2rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #E5E7EB;
    }
    
    .subtitle {
        color: #6B7280;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Cards for metrics to look cleaner */
    [data-testid="metric-container"] {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
    
    /* Input area adjustments */
    .stTextArea textarea {
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)

st.title("AgentSync")
st.markdown('<p class="subtitle">AI-Assisted IT Incident Resolution Engine</p>', unsafe_allow_html=True)

# Check config
try:
    settings.validate()
except ValueError as e:
    st.error(str(e))
    st.stop()

# Sidebar Styling
with st.sidebar:
    st.markdown("### System Configuration")
    st.markdown(f"**Model Deployment**<br/><span style='color:#6B7280;font-size:0.9em;'>{settings.DEFAULT_MODEL}</span>", unsafe_allow_html=True)
    st.markdown(f"**Database Connection**<br/><span style='color:#6B7280;font-size:0.9em;'>{settings.DATABASE_URL}</span>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<span style='color:#9CA3AF;font-size:0.8em;'>AgentSync Engine v1.0.0</span>", unsafe_allow_html=True)

st.markdown("### Incident Registration")
user_request = st.text_area(
    "Describe the IT incident or request:", 
    height=120, 
    placeholder="e.g., 'Payment API is returning 500 errors during checkout process'...",
    label_visibility="collapsed"
)

# Use columns for action buttons to make it look neater
col_btn, _ = st.columns([2, 8])
with col_btn:
    run_workflow = st.button("Initialize Workflow", type="primary", use_container_width=True)

if run_workflow:
    if not user_request.strip():
        st.warning("Please provide an incident description to initialize the workflow.")
    else:
        with st.status("Executing AgentSync Workflow...", expanded=True) as status:
            st.write("Initializing agent coordination...")
            
            # Run Workflow
            final_state = run_agent_workflow(user_request)
            
            status.update(label="Workflow Execution Complete", state="complete", expanded=False)
            
        # Display metrics
        st.markdown("### Execution Metrics")
        metrics = final_state.get("execution_metadata", {})
        col1, col2, col3 = st.columns(3)
        col1.metric("Execution Time", f"{metrics.get('duration_seconds', 0)}s")
        col2.metric("LLM Operations", metrics.get("llm_calls", 0))
        col3.metric("Tool Invocations", metrics.get("tool_calls", 0))
        
        # Display errors if any
        if final_state.get("errors"):
            st.error("Workflow encountered errors during execution:")
            for err in final_state["errors"]:
                st.write(f"- {err}")
                
        st.markdown("---")
        
        # Display workflow results using clean tabs
        st.markdown("### Resolution Details")
        tabs = st.tabs(["Plan Generation", "Investigation Results", "Root Cause Analysis", "Proposed Decision"])
        
        with tabs[0]:
            st.markdown("#### Execution Plan")
            st.write(final_state.get("plan", "No plan generated."))
            
        with tabs[1]:
            st.markdown("#### Data Gathering")
            st.write(final_state.get("investigation_results", "No investigation data available."))
            
        with tabs[2]:
            st.markdown("#### Technical Analysis")
            st.write(final_state.get("analysis", "No analysis available."))
            
        with tabs[3]:
            st.markdown("#### Final Recommendation")
            st.write(final_state.get("decision", "No decision formulated."))
