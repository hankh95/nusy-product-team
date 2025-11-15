import typer
from typing import List, Optional
from pathlib import Path

from nusy_pm_core.notes import NotesManager

app = typer.Typer(help="NuSy Product Team CLI")

__VERSION__ = "0.1.0"

def get_version() -> str:
    return __VERSION__

@app.command()
def version():
    """Show CLI and core service version."""
    typer.echo(f"NuSy Product Team CLI v{__VERSION__}")

@app.command()
def serve(host: str = "127.0.0.1", port: int = 8000):
    """Start the FastAPI web server."""
    import uvicorn
    from nusy_pm_core.api import app
    typer.echo(f"Starting NuSy API server on http://{host}:{port}")
    typer.echo("Press Ctrl+C to stop")
    uvicorn.run(app, host=host, port=port)

plans_app = typer.Typer(name="plans", help="Manage development plans")
issues_app = typer.Typer(name="issues", help="Manage issues")
experiments_app = typer.Typer(name="experiments", help="Manage experiments")

notes_app = typer.Typer(name="notes", help="Manage NuSy notes and knowledge graph links.")

@app.command()
def scaffold_project(
    name: str = typer.Argument(..., help="Project name to scaffold"),
    target_dir: Optional[Path] = typer.Option(None, help="Target directory (defaults to current directory)"),
):
    """
    Scaffold a new NuSy-powered project with all services and interfaces.
    """
    from .scaffold import ScaffoldGenerator

    generator = ScaffoldGenerator()
    project_dir = generator.generate_project(name, target_dir)

    typer.secho(f"✅ Project '{name}' scaffolded successfully!", fg=typer.colors.GREEN)
    typer.echo(f"📁 Created at: {project_dir}")
    typer.echo("\n🚀 Next steps:")
    typer.echo("1. cd " + str(project_dir.name))
    typer.echo("2. python scripts/setup.py  # Install dependencies")
    typer.echo("3. python -m project_core.cli serve  # Start the server")
    typer.echo("4. Open nusy_query_interface.html in your browser")

@notes_app.command("create")
def create(
    title: str = typer.Argument(..., help="Note title"),
    contributor: str = typer.Option(..., help="Contributor name", prompt=True),
    summary: str = typer.Option(..., help="Brief summary"),
    source_link: Optional[List[str]] = typer.Option(
        None, "--source-link", help="Files, tickets, or URLs referenced in the note"
    ),
    next_step: Optional[List[str]] = typer.Option(
        None, "--next-step", help="Next steps this note sets up"
    ),
    tag: Optional[List[str]] = typer.Option(None, "--tag", help="Arbitrary tag for the note"),
):
    """Create a NuSy note and persist it in the notes manifest."""
    manager = NotesManager()
    note = manager.add_note(
        title=title,
        contributor=contributor,
        summary=summary,
        source_links=source_link,
        next_steps=next_step,
        tags=tag,
    )
    typer.secho(f"Created note {note.id}", fg=typer.colors.GREEN)

@notes_app.command("list")
def list_notes(latest_only: bool = typer.Option(False, help="Show only recent notes")) -> None:
    """List the stored NuSy notes."""
    manager = NotesManager()
    entries = manager.latest_notes() if latest_only else manager.list_notes()
    if not entries:
        typer.echo("No notes recorded yet.")
        raise typer.Exit()
    for note in entries:
        typer.echo(f"- {note.id} | {note.title} ({note.contributor})")
        typer.echo(f"  Created: {note.created_at}")
        typer.echo(f"  Summary: {note.summary}")
        if note.tags:
            typer.echo(f"  Tags: {', '.join(note.tags)}")
        if note.source_links:
            typer.echo(f"  Sources: {', '.join(note.source_links)}")
        if note.next_steps:
            typer.echo(f"  Next: {', '.join(note.next_steps)}")

@notes_app.command("link")
def link(
    note_id: str = typer.Argument(..., help="Note identifier"),
    kg_node_id: str = typer.Argument(..., help="Knowledge graph node ID"),
    rationale: str = typer.Argument(..., help="Why this link matters"),
) -> None:
    """Link a note to a KG node so the graph understands the decision source."""
    manager = NotesManager()
    manager.link_to_graph(note_id=note_id, kg_node_id=kg_node_id, rationale=rationale)
    typer.secho(f"Linked note {note_id} to {kg_node_id}", fg=typer.colors.CYAN)

@notes_app.command("query-contributor")
def query_contributor(contributor: str = typer.Argument(..., help="Contributor name")) -> None:
    """Query notes by contributor."""
    manager = NotesManager()
    notes = manager.query_notes_by_contributor(contributor)
    if not notes:
        typer.echo(f"No notes found for contributor '{contributor}'.")
        return
    for note in notes:
        typer.echo(f"- {note.id} | {note.title}")
        typer.echo(f"  Summary: {note.summary}")

@notes_app.command("query")
def query(question: str = typer.Argument(..., help="Question to ask the KG")) -> None:
    """Query the knowledge graph using NeurosymbolicClinicalReasoner."""
    manager = NotesManager()
    result = manager.neurosymbolic_query(question)
    typer.echo(f"Keywords: {', '.join(result['keywords'])}")
    typer.echo(f"Triples: {result['triples']}")
    typer.echo(f"Entities: {', '.join(result['entities'])}")

@notes_app.command("run-pipeline")
def run_pipeline() -> None:
    """Run the complete Neurosymbolic pipeline."""
    manager = NotesManager()
    result = manager.run_pipeline()
    typer.secho("Pipeline completed successfully!", fg=typer.colors.GREEN)
    typer.echo(f"L0 content processed: {len(result['l0_content'])} sections")
    typer.echo(f"Triples added: {result['triples_added']}")
    typer.echo(f"BDD scenarios generated: {len(result['scenarios'])}")

@notes_app.command("validate-coverage")
def validate_coverage() -> None:
    """Validate pipeline coverage."""
    manager = NotesManager()
    coverage = manager.validate_coverage()
    typer.echo("Coverage Report:")
    typer.echo(f"- Total scenarios: {coverage['total_scenarios']}")
    typer.echo(f"- KG triples: {coverage['kg_triples']}")
    typer.echo(f"- Notes processed: {coverage['notes_processed']}")

@notes_app.command("sparql")
def sparql_query(query: str = typer.Argument(..., help="SPARQL query to execute")) -> None:
    """Execute a SPARQL query on the knowledge graph."""
    manager = NotesManager()
    results = manager.kg.sparql_query(query)
    if not results:
        typer.echo("No results found.")
        return
    for row in results:
        typer.echo(f"- {', '.join(str(cell) for cell in row)}")

app.add_typer(notes_app)

plans_app = typer.Typer(name="plans", help="Manage development plans")
issues_app = typer.Typer(name="issues", help="Manage issues")

app.add_typer(plans_app)
app.add_typer(issues_app)
app.add_typer(experiments_app)

@plans_app.command("list")
def list_plans():
    """List all development plans."""
    from nusy_pm_core.development_plans import DevelopmentPlansService
    service = DevelopmentPlansService()
    plans = service.list_plans()
    if not plans:
        typer.echo("No development plans found.")
        return
    for plan in plans:
        typer.echo(f"- {plan.title} (ID: {plan.id}) - Status: {plan.status.value}")

@plans_app.command("create")
def create_plan(title: str, description: str = ""):
    """Create a new development plan."""
    from nusy_pm_core.development_plans import DevelopmentPlansService
    service = DevelopmentPlansService()
    plan = service.create_plan(title, description)
    typer.echo(f"Created development plan: {plan.title} (ID: {plan.id})")

@plans_app.command("show")
def show_plan(plan_id: str):
    """Show details of a development plan."""
    from nusy_pm_core.development_plans import DevelopmentPlansService
    service = DevelopmentPlansService()
    plan = service.get_plan(plan_id)
    if not plan:
        typer.echo(f"Plan with ID {plan_id} not found.")
        return
    typer.echo(f"Plan: {plan.title}")
    typer.echo(f"Description: {plan.description}")
    typer.echo(f"Status: {plan.status.value}")
    typer.echo(f"Progress: {plan.progress:.1f}%")
    typer.echo(f"Milestones: {len(plan.milestones)}")
    for milestone in plan.milestones:
        typer.echo(f"  - {milestone.title} ({milestone.status.value}) - {len(milestone.tasks)} tasks")

@issues_app.command("list")
def list_issues():
    """List all issues."""
    from nusy_pm_core.issues import IssuesService
    service = IssuesService()
    issues = service.list_issues()
    if not issues:
        typer.echo("No issues found.")
        return
    for issue in issues:
        typer.echo(f"- {issue.title} (ID: {issue.id}) - Status: {issue.status.value}")

@issues_app.command("create")
def create_issue(title: str, description: str = "", labels: str = ""):
    """Create a new issue."""
    from nusy_pm_core.issues import IssuesService
    service = IssuesService()
    label_list = [label.strip() for label in labels.split(",") if label.strip()]
    issue = service.create_issue(title, description, label_list)
    typer.echo(f"Created issue: {issue.title} (ID: {issue.id})")

@issues_app.command("show")
def show_issue(issue_id: str):
    """Show details of an issue."""
    from nusy_pm_core.issues import IssuesService
    service = IssuesService()
    issue = service.get_issue(issue_id)
    if not issue:
        typer.echo(f"Issue with ID {issue_id} not found.")
        return
    typer.echo(f"Issue: {issue.title}")
    typer.echo(f"Description: {issue.description}")
    typer.echo(f"Status: {issue.status.value}")
    typer.echo(f"Priority: {issue.priority.value}")
    typer.echo(f"Labels: {', '.join(issue.labels)}")
    typer.echo(f"Comments: {len(issue.comments)}")
    for comment in issue.comments:
        typer.echo(f"  - {comment.author}: {comment.body[:50]}...")

@experiments_app.command("list")
def list_experiments():
    """List all experiments."""
    from nusy_pm_core.experiments import ExperimentsService
    service = ExperimentsService()
    experiments = service.list_experiments()
    if not experiments:
        typer.echo("No experiments found.")
        return
    for exp in experiments:
        typer.echo(f"- {exp.experiment_name} - Status: {exp.status}, Phases: {exp.phases_completed}/{exp.total_phases}")

@experiments_app.command("start")
def start_experiment(experiment_name: str):
    """Start a new experiment."""
    from nusy_pm_core.experiments import ExperimentsService
    service = ExperimentsService()
    exp = service.start_experiment(experiment_name)
    if not exp:
        typer.echo(f"Experiment config for {experiment_name} not found.")
        return
    typer.echo(f"Started experiment: {exp.experiment_name}")

@experiments_app.command("show")
def show_experiment(experiment_name: str):
    """Show details of an experiment."""
    from nusy_pm_core.experiments import ExperimentsService
    service = ExperimentsService()
    exp = service.get_experiment(experiment_name)
    if not exp:
        typer.echo(f"Experiment {experiment_name} not found.")
        return
    typer.echo(f"Experiment: {exp.experiment_name}")
    typer.echo(f"Status: {exp.status}")
    typer.echo(f"Phases: {exp.phases_completed}/{exp.total_phases}")
    typer.echo(f"Start: {exp.start_time}")
    if exp.end_time:
        typer.echo(f"End: {exp.end_time}")
    typer.echo(f"Success Metrics: {exp.success_metrics}")

if __name__ == "__main__":
    app()

def main():
    """Main entry point for the CLI."""
    app()
