from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
from workflow.agent_workflow import run_agent_workflow
from config.settings import settings
import uuid

app = FastAPI(
    title="AgentSync Enterprise API",
    description="API layer for AgentSync Coordination & Decision Engine",
    version="1.0.0"
)

# Mock in-memory state store for status endpoints
workflow_jobs: Dict[str, Any] = {}

class WorkflowRequest(BaseModel):
    request_text: str

class WorkflowResponse(BaseModel):
    job_id: str
    status: str
    plan: str = ""
    research_results: str = ""
    analysis: str = ""
    decision: str = ""
    execution_metrics: Dict[str, Any] = {}
    errors: List[str] = []

@app.on_event("startup")
async def startup_event():
    try:
        settings.validate()
    except ValueError as e:
        print(f"Startup Error: {e}")

@app.post("/workflow/run", response_model=WorkflowResponse)
async def run_workflow(req: WorkflowRequest):
    if not req.request_text:
        raise HTTPException(status_code=400, detail="request_text is required.")
        
    job_id = str(uuid.uuid4())
    workflow_jobs[job_id] = {"status": "Running"}
    
    try:
        final_state = run_agent_workflow(req.request_text)
        
        response = WorkflowResponse(
            job_id=job_id,
            status=final_state.get("workflow_status", "Completed"),
            plan=final_state.get("plan", ""),
            research_results=final_state.get("research_results", ""),
            analysis=final_state.get("analysis", ""),
            decision=final_state.get("decision", ""),
            execution_metrics=final_state.get("execution_metadata", {}),
            errors=final_state.get("errors", [])
        )
        
        workflow_jobs[job_id] = response.dict()
        return response
        
    except Exception as e:
        error_msg = f"Workflow failed: {str(e)}"
        workflow_jobs[job_id] = {"status": "Error", "errors": [error_msg]}
        raise HTTPException(status_code=500, detail=error_msg)

@app.get("/workflow/status/{job_id}")
async def get_workflow_status(job_id: str):
    job = workflow_jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.get("/agents")
async def list_agents():
    return {
        "agents": [
            {"id": "planner", "description": "Breaks down requests into tasks"},
            {"id": "research", "description": "Gathers required information using tools"},
            {"id": "analysis", "description": "Identifies patterns, risks, and factors"},
            {"id": "decision", "description": "Formulates final recommendations"}
        ]
    }
