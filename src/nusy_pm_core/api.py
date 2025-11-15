from fastapi import FastAPI
from nusy_pm_core.cli import get_version
from nusy_pm_core.notes import NotesManager
from nusy_pm_core.development_plans import DevelopmentPlansService
from nusy_pm_core.issues import IssuesService
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

app = FastAPI(title="NuSy Product Manager Core")

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
    return {"status": "ok", "component": "nusy-pm-core"}

@app.get("/version")
def version():
    return {"version": get_version()}

@app.post("/api/query")
def query_notes(request: QueryRequest):
    """Query the knowledge graph using NeurosymbolicClinicalReasoner."""
    manager = NotesManager()
    result = manager.neurosymbolic_query(request.question)
    return {
        "question": request.question,
        "keywords": result["keywords"],
        "triples": result["triples"],
        "entities": result["entities"],
        "relationships": result["relationships"]
    }

@app.post("/api/sparql")
def sparql_query(request: SparqlRequest):
    """Execute a SPARQL query on the knowledge graph."""
    manager = NotesManager()
    results = manager.kg.sparql_query(request.query)
    return {
        "query": request.query,
        "results": [{"row": [str(cell) for cell in row]} for row in results]
    }

@app.get("/api/notes")
def list_notes():
    """List all notes."""
    manager = NotesManager()
    notes = manager.list_notes()
    return {
        "notes": [
            {
                "id": note.id,
                "title": note.title,
                "contributor": note.contributor,
                "summary": note.summary,
                "tags": note.tags,
                "created_at": note.created_at
            }
            for note in notes
        ]
    }

@app.post("/api/pipeline/run")
def run_pipeline():
    """Run the complete Neurosymbolic pipeline."""
    manager = NotesManager()
    result = manager.run_pipeline()
    return {
        "status": "completed",
        "l0_sections_processed": len(result["l0_content"]),
        "triples_added": result["triples_added"],
        "scenarios_generated": len(result["scenarios"])
    }

@app.get("/api/coverage")
def get_coverage():
    """Get pipeline coverage report."""
    manager = NotesManager()
    coverage = manager.validate_coverage()
    return {
        "total_scenarios": coverage["total_scenarios"],
        "kg_triples": coverage["kg_triples"],
        "notes_processed": coverage["notes_processed"]
    }

# Development Plans API
@app.get("/api/plans")
def list_plans():
    """List all development plans."""
    service = DevelopmentPlansService()
    plans = service.list_plans()
    return {
        "plans": [
            {
                "id": plan.id,
                "title": plan.title,
                "description": plan.description,
                "status": plan.status.value,
                "progress": plan.progress,
                "milestones_count": len(plan.milestones),
                "created_at": plan.created_at,
                "updated_at": plan.updated_at
            }
            for plan in plans
        ]
    }

@app.post("/api/plans")
def create_plan(request: CreatePlanRequest):
    """Create a new development plan."""
    service = DevelopmentPlansService()
    plan = service.create_plan(request.title, request.description)
    return {
        "id": plan.id,
        "title": plan.title,
        "description": plan.description,
        "status": plan.status.value,
        "created_at": plan.created_at
    }

@app.get("/api/plans/{plan_id}")
def get_plan(plan_id: str):
    """Get a specific development plan."""
    service = DevelopmentPlansService()
    plan = service.get_plan(plan_id)
    if not plan:
        return {"error": "Plan not found"}, 404
    
    return {
        "id": plan.id,
        "title": plan.title,
        "description": plan.description,
        "status": plan.status.value,
        "progress": plan.progress,
        "milestones": [
            {
                "id": m.id,
                "title": m.title,
                "description": m.description,
                "status": m.status.value,
                "progress": m.progress,
                "due_date": m.due_date,
                "tasks_count": len(m.tasks),
                "tasks": [
                    {
                        "id": t.id,
                        "title": t.title,
                        "description": t.description,
                        "status": t.status.value,
                        "assignee": t.assignee,
                        "created_at": t.created_at,
                        "updated_at": t.updated_at
                    }
                    for t in m.tasks
                ],
                "created_at": m.created_at,
                "updated_at": m.updated_at
            }
            for m in plan.milestones
        ],
        "created_at": plan.created_at,
        "updated_at": plan.updated_at
    }

# Issues API
@app.get("/api/issues")
def list_issues():
    """List all issues."""
    service = IssuesService()
    issues = service.list_issues()
    return {
        "issues": [
            {
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
            }
            for issue in issues
        ]
    }

@app.post("/api/issues")
def create_issue(request: CreateIssueRequest):
    """Create a new issue."""
    from nusy_pm_core.models.issue import IssuePriority
    service = IssuesService()
    
    priority = IssuePriority(request.priority.lower()) if request.priority else IssuePriority.MEDIUM
    issue = service.create_issue(request.title, request.description, request.reporter, priority)
    
    # Add labels if provided
    for label in request.labels:
        service.add_label(issue.id, label)
    
    return {
        "id": issue.id,
        "title": issue.title,
        "description": issue.description,
        "status": issue.status.value,
        "priority": issue.priority.value,
        "reporter": issue.reporter,
        "labels": issue.labels,
        "created_at": issue.created_at
    }

@app.get("/api/issues/{issue_id}")
def get_issue(issue_id: str):
    """Get a specific issue."""
    service = IssuesService()
    issue = service.get_issue(issue_id)
    if not issue:
        return {"error": "Issue not found"}, 404
    
    return {
        "id": issue.id,
        "title": issue.title,
        "description": issue.description,
        "status": issue.status.value,
        "priority": issue.priority.value,
        "reporter": issue.reporter,
        "assignee": issue.assignee,
        "labels": issue.labels,
        "comments": [
            {
                "id": c.id,
                "author": c.author,
                "content": c.content,
                "created_at": c.created_at
            }
            for c in issue.comments
        ],
        "created_at": issue.created_at,
        "updated_at": issue.updated_at
    }

@app.post("/api/issues/{issue_id}/comments")
def add_comment(issue_id: str, request: AddCommentRequest):
    """Add a comment to an issue."""
    service = IssuesService()
    comment = service.add_comment(issue_id, request.author, request.content)
    if not comment:
        return {"error": "Issue not found"}, 404
    
    return {
        "id": comment.id,
        "author": comment.author,
        "content": comment.content,
        "created_at": comment.created_at
    }
