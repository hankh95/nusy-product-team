"""API for {project_name}."""

from fastapi import FastAPI
from project_core.notes import NotesManager
from project_core.development_plans import DevelopmentPlansService
from project_core.issues import IssuesService
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

app = FastAPI(title="{project_name}")

class QueryRequest(BaseModel):
    question: str

class SparqlRequest(BaseModel):
    query: str

class CreatePlanRequest(BaseModel):
    title: str
    description: str = ""

class CreateIssueRequest(BaseModel):
    title: str
    description: str = ""
    reporter: str
    priority: str = "medium"
    labels: List[str] = []

class AddCommentRequest(BaseModel):
    author: str
    content: str

@app.get("/health")
def health():
    return {{"status": "ok", "component": "{project_name}"}}

@app.post("/api/query")
def query_notes(request: QueryRequest):
    """Query the knowledge graph."""
    manager = NotesManager()
    result = manager.neurosymbolic_query(request.question)
    return {{
        "question": request.question,
        "keywords": result["keywords"],
        "triples": result["triples"],
        "entities": result["entities"],
        "relationships": result["relationships"]
    }}

@app.get("/api/plans")
def list_plans():
    """List all development plans."""
    service = DevelopmentPlansService()
    plans = service.list_plans()
    return {{
        "plans": [
            {{
                "id": plan.id,
                "title": plan.title,
                "description": plan.description,
                "status": plan.status.value,
                "progress": plan.progress,
                "milestones_count": len(plan.milestones),
                "created_at": plan.created_at,
                "updated_at": plan.updated_at
            }}
            for plan in plans
        ]
    }}

@app.get("/api/issues")
def list_issues():
    """List all issues."""
    service = IssuesService()
    issues = service.list_issues()
    return {{
        "issues": [
            {{
                "id": issue.id,
                "title": issue.title,
                "description": issue.description,
                "status": issue.status.value,
                "priority": issue.priority.value,
                "reporter": issue.reporter,
                "assignee": issue.assignee,
                "labels": issue.labels,
                "comments_count": len(issue.comments),
                "created_at": issue.created_at,
                "updated_at": issue.updated_at
            }}
            for issue in issues
        ]
    }}