"""CLI for {project_name}."""

import typer
from pathlib import Path
from typing import Optional

app = typer.Typer(help="{project_name} CLI")

__VERSION__ = "0.1.0"

def main():
    """Main entry point."""
    app()

@app.command()
def version():
    """Show version."""
    typer.echo(f"{__VERSION__}")

@app.command()
def serve(host: str = "127.0.0.1", port: int = 8000):
    """Start the web server."""
    import uvicorn
    from project_core.api import app
    typer.echo(f"Starting {__VERSION__} on http://{host}:{port}")
    typer.echo("Press Ctrl+C to stop")
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    main()