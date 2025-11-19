#!/usr/bin/env python3
"""
Santiago Core API Server

Provides REST API endpoints for Santiago multi-agent system.
"""

import os
import asyncio
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uvicorn

from santiago_core.agents.factory import SantiagoFactory
from santiago_core.services.llm_router import LLMRouter


class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str
    services: Dict[str, bool]


class TaskRequest(BaseModel):
    task_description: str
    priority: Optional[str] = "medium"
    assignee: Optional[str] = None


app = FastAPI(
    title="Santiago Core API",
    description="Multi-agent AI factory for autonomous development",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Santiago factory
factory = SantiagoFactory()
llm_router = LLMRouter()


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        # Check core services
        services_status = {
            "llm_router": True,  # Always available if app starts
            "factory": True,     # Always available if app starts
        }

        # Check LLM connectivity (basic)
        try:
            # This is a lightweight check - actual API calls happen during task execution
            services_status["llm_openai"] = bool(os.getenv("OPENAI_API_KEY"))
            services_status["llm_xai"] = bool(os.getenv("XAI_API_KEY"))
        except:
            services_status["llm_openai"] = False
            services_status["llm_xai"] = False

        return HealthResponse(
            status="healthy",
            version="1.0.0",
            environment=os.getenv("NUSY_ENV", "development"),
            services=services_status
        )
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")


@app.post("/tasks")
async def create_task(task: TaskRequest):
    """Create a new development task"""
    try:
        # This would integrate with the kanban service
        # For now, return a placeholder response
        return {
            "task_id": f"task_{hash(task.task_description) % 10000}",
            "status": "created",
            "description": task.task_description,
            "priority": task.priority,
            "assignee": task.assignee,
            "message": "Task created successfully. Santiago agents will begin work shortly."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create task: {str(e)}")


@app.get("/tasks")
async def list_tasks():
    """List all active tasks"""
    try:
        # This would integrate with kanban service
        # For now, return placeholder
        return {
            "tasks": [],
            "total": 0,
            "message": "Task listing not yet implemented - use kanban service directly"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list tasks: {str(e)}")


@app.get("/agents")
async def list_agents():
    """List available Santiago agents"""
    try:
        agents = factory.list_available_agents()
        return {
            "agents": agents,
            "total": len(agents)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list agents: {str(e)}")


@app.post("/agents/{agent_name}/execute")
async def execute_agent_task(agent_name: str, task: TaskRequest):
    """Execute a task with a specific agent"""
    try:
        result = await factory.execute_task_with_agent(
            agent_name=agent_name,
            task_description=task.task_description,
            priority=task.priority,
            assignee=task.assignee
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to execute task: {str(e)}")


if __name__ == "__main__":
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    workers = int(os.getenv("WORKERS", "1"))

    # Start server
    uvicorn.run(
        "santiago_core.api:app",
        host=host,
        port=port,
        workers=workers,
        reload=os.getenv("NUSY_ENV") == "development"
    )