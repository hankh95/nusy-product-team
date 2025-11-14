import typer

app = typer.Typer(help="NuSy Product Team CLI")

__VERSION__ = "0.1.0"

def get_version() -> str:
    return __VERSION__

@app.command()
def version():
    """Show CLI and core service version."""
    typer.echo(f"NuSy Product Team CLI v{__VERSION__}")

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

if __name__ == "__main__":
    app()
