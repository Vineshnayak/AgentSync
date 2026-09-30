from workflow.agent_workflow import run_agent_workflow
import traceback
try:
    print(run_agent_workflow("Why website is so laggy?"))
except Exception as e:
    traceback.print_exc()
