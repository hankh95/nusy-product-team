from fastapi import FastAPI
from nusy_pm_core.cli import get_version
from nusy_pm_core.notes import NotesManager
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI(title="NuSy Product Manager Core")

class QueryRequest(BaseModel):
    question: str

class SparqlRequest(BaseModel):
    query: str

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
