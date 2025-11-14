import typer
from typing import List, Optional

from nusy_pm_core.notes import NotesManager

app = typer.Typer(help="NuSy Product Team CLI")

__VERSION__ = "0.1.0"

def get_version() -> str:
    return __VERSION__

@app.command()
def version():
    """Show CLI and core service version."""
    typer.echo(f"NuSy Product Team CLI v{__VERSION__}")

notes_app = typer.Typer(name="notes", help="Manage NuSy notes and knowledge graph links.")

@app.command()
def scaffold_project(
    name: str = typer.Argument(..., help="Project name to scaffold"),
):
    """
    Scaffold a new NuSy product project using the 'scaffold the project' feature.

    In early versions this will:
    - Validate repo structure.
    - Ensure core docs and directories exist.
    - Optionally create initial features and tests.
    """
    typer.echo(f"[scaffold_project] Would scaffold project '{name}' here.")

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

app.add_typer(notes_app)

if __name__ == "__main__":
    app()
