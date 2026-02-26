import sys
import os
from pathlib import Path

# Add services directory to Python path
services_path = Path(__file__).parent / "services"
sys.path.insert(0, str(services_path))
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from core.logger import get_logger
from core.config import settings
from core.langsmith import setup_langsmith
from core.llm import get_llm

# Initialize FastAPI app
app = FastAPI(
    title="Task Automation Agent",
    description="AI-powered task automation agent with LangGraph",
    version="1.0.0"
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup logging
logger = get_logger("fastapi_app")

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting Task Automation Agent...")
    
    # Setup LangSmith tracing
    try:
        setup_langsmith()
        logger.info("LangSmith tracing configured")
    except Exception as e:
        logger.error(f"Failed to setup LangSmith: {e}")
    
    # Test LLM connection
    try:
        # Lazy load LLM to avoid startup issues
        logger.info(f"LLM model from settings: {settings.MODEL_NAME}")
        if settings.MODEL_NAME:
            llm = get_llm()
            logger.info(f"LLM initialized with model: {settings.MODEL_NAME}")
        else:
            logger.warning("MODEL_NAME not set, skipping LLM initialization")
    except Exception as e:
        logger.error(f"Failed to initialize LLM: {e}")
    
    logger.info("Task Automation Agent started successfully!")

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Task Automation Agent is running"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "task-automation-agent"}

@app.post("/execute")
async def execute_task(task: dict):
    """Execute a task"""
    try:
        logger.info(f"Executing task: {task}")
        # TODO: Implement task execution logic
        return {"status": "success", "message": "Task executed successfully"}
    except Exception as e:
        logger.error(f"Task execution failed: {e}")
        return {"status": "error", "message": str(e)}

@app.post("/run")
async def run_task(task_request: dict):
    """Run a task through the agent workflow"""
    try:
        logger.info(f"Running task: {task_request}")
        
        # Import and run the agent graph
        from agent.graph import create_graph
        
        # Create the workflow graph
        graph = create_graph()
        
        # Process the task through the agent workflow
        # Accept both "task" and "input" as the user input field
        user_input = task_request.get("task") or task_request.get("input", "")
        result = graph.invoke({
            "user_input": user_input,
            "plan": [],
            "current_step": 0,
            "tool_result": None,
            "history": []
        })
        
        return {
            "status": "success", 
            "result": result,
            "message": "Task completed successfully"
        }
    except Exception as e:
        logger.error(f"Task run failed: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)