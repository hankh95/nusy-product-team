"""Project Scaffold Generator."""

import os
import shutil
from pathlib import Path
from typing import Dict, Any, Optional
import json
from datetime import datetime, timezone

from .development_plans import DevelopmentPlansService
from .issues import IssuesService
from .notes import NotesManager
from .models.issue import IssuePriority


class ScaffoldGenerator:
    """Generates complete NuSy project scaffolds."""

    def __init__(self, template_dir: Optional[Path] = None):
        self.template_dir = template_dir or Path(__file__).resolve().parents[2] / "templates"
        self.template_dir.mkdir(parents=True, exist_ok=True)

    def generate_project(self, project_name: str, target_dir: Optional[Path] = None) -> Path:
        """Generate a complete NuSy project scaffold."""
        if target_dir:
            project_dir = target_dir / project_name
        else:
            project_dir = Path.cwd() / project_name
        project_dir.mkdir(parents=True, exist_ok=True)

        # Create directory structure
        self._create_directory_structure(project_dir)

        # Create configuration files
        self._create_config_files(project_dir, project_name)

        # Create initial data
        self._create_initial_data(project_dir, project_name)

        # Create documentation
        self._create_documentation(project_dir, project_name)

        # Create web interfaces
        self._create_web_interfaces(project_dir)

        # Create scripts
        self._create_scripts(project_dir)

        return project_dir

    def _create_directory_structure(self, target_dir: Path) -> None:
        """Create the basic directory structure."""
        dirs = [
            "src/project_core",
            "src/project_core/models",
            "src/project_core/adapters",
            "src/project_core/knowledge",
            "data",
            "notes",
            "features",
            "tests",
            "docs",
            "scripts"
        ]

        for dir_name in dirs:
            (target_dir / dir_name).mkdir(parents=True, exist_ok=True)

    def _create_config_files(self, target_dir: Path, project_name: str) -> None:
        """Create configuration files."""
        # requirements.txt
        requirements = """fastapi
uvicorn
typer
pydantic
python-dotenv
rdflib
networkx
pytest
pytest-bdd
"""
        (target_dir / "requirements.txt").write_text(requirements)

        # pyproject.toml
        pyproject = f"""[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{project_name}"
version = "0.1.0"
description = "NuSy-powered project management system"
authors = [
    {{name = "NuSy", email = "nusy@example.com"}},
]
dependencies = [
    "fastapi",
    "uvicorn",
    "typer",
    "pydantic",
    "python-dotenv",
    "rdflib",
    "networkx",
    "pytest",
    "pytest-bdd",
]

[project.scripts]
{project_name} = "project_core.cli:main"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"
"""
        (target_dir / "pyproject.toml").write_text(pyproject)

        # .env.example
        env_example = """# Database configuration
DATABASE_URL=sqlite:///data/project.db

# Knowledge Graph configuration
KG_FILE=data/kg.ttl

# Server configuration
HOST=127.0.0.1
PORT=8000

# Development settings
DEBUG=true
"""
        (target_dir / ".env.example").write_text(env_example)

    def _create_initial_data(self, target_dir: Path, project_name: str) -> None:
        """Create initial project data."""
        # Initialize services
        data_dir = target_dir / "data"
        plans_service = DevelopmentPlansService(data_dir / "development_plans.json")
        issues_service = IssuesService(data_dir / "issues.json")
        notes_manager = NotesManager(data_dir / "notes_manifest.json")

        # Create initial development plan
        plan = plans_service.create_plan(
            f"{project_name.title()} Development Plan",
            f"Initial development plan for {project_name}"
        )

        # Add initial milestones
        milestone1 = plans_service.add_milestone(
            plan.id,
            "Project Setup",
            "Set up development environment and basic structure",
            "2025-12-01"
        )

        milestone2 = plans_service.add_milestone(
            plan.id,
            "Core Features",
            "Implement core domain features",
            "2026-01-15"
        )

        # Add initial tasks
        if milestone1:
            plans_service.add_task(
                plan.id, milestone1.id,
                "Install dependencies",
                "Install all required dependencies",
                "developer"
            )

            plans_service.add_task(
                plan.id, milestone1.id,
                "Configure environment",
                "Set up development environment",
                "developer"
            )

        # Create initial issues
        issue1 = issues_service.create_issue(
            "Set up CI/CD pipeline",
            "Configure automated testing and deployment",
            "project-manager",
            IssuePriority.HIGH
        )

        issue2 = issues_service.create_issue(
            "Create user documentation",
            "Write comprehensive user documentation",
            "technical-writer",
            IssuePriority.MEDIUM
        )

        # Create initial notes
        note1 = notes_manager.add_note(
            "Project Kickoff",
            "project-manager",
            f"Starting development of {project_name} using NuSy framework",
            source_links=["README.md"],
            tags=["kickoff", "planning"]
        )

        # Save all data (services save automatically, but ensure KG is saved)
        plans_service.kg.save()
        issues_service.kg.save()

    def _create_documentation(self, target_dir: Path, project_name: str) -> None:
        """Create documentation files."""
        # README.md
        readme = f"""# {project_name.title()}

A NuSy-powered project management system for tracking development plans, issues, and knowledge.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the development server:**
   ```bash
   python -m project_core.cli serve
   ```

3. **Open the web interface:**
   - Open `nusy_query_interface.html` in your browser
   - Access API at `http://127.0.0.1:8000`

## Features

- **Development Plans**: Track milestones, tasks, and project progress
- **Issues Management**: Create, assign, and track issues with comments
- **Knowledge Graph**: Query project knowledge using natural language
- **Notes System**: Capture and link project documentation
- **Web Interface**: Interactive UI for all features

## Project Structure

```
{project_name}/
├── src/project_core/          # Core application code
├── data/                      # Data storage (KG, issues, plans)
├── notes/                     # Project notes and documentation
├── nusy_pm/cargo-manifests/   # BDD feature specifications
├── tests/                     # Test suite
├── docs/                      # Documentation
└── scripts/                   # Utility scripts
```

## Usage

### CLI Commands

```bash
# Start web server
python -m project_core.cli serve

# Manage development plans
python -m project_core.cli plans create "New Feature" "Description"
python -m project_core.cli plans list

# Manage issues
python -m project_core.cli issues create "Bug title" "Description" --reporter "you"
python -m project_core.cli issues list

# Query knowledge graph
python -m project_core.cli query "What is the current project status?"
```

### API Endpoints

- `GET /health` - Health check
- `POST /api/query` - Natural language queries
- `GET /api/plans` - List development plans
- `GET /api/issues` - List issues
- `POST /api/pipeline/run` - Run data processing pipeline

## Development

This project uses:
- **TDD/BDD**: Tests first, features in `nusy_pm/cargo-manifests/`
- **Knowledge Graph**: RDF-based knowledge storage
- **FastAPI**: Modern Python web framework
- **Typer**: Command-line interface framework

Run tests:
```bash
pytest tests/
```

## License

MIT License - see LICENSE file for details.
"""
        (target_dir / "README.md").write_text(readme)

        # DEVELOPMENT_PRACTICES.md (copy from template)
        practices_content = """# Development Practices

## Core Principles

1. **TDD/BDD First** – Every new capability starts with executable specifications
2. **Knowledge Graph as Source of Truth** – Capture decisions in the KG
3. **Small Batch, Fast Feedback** – Ship incremental slices
4. **Transparent Team Coordination** – Document handoffs in Git

## Quality Gates

- Tests must pass before merging
- Knowledge capture required for features
- Code review mandatory

## Santiago Notes Ritual

- Write session notes after work
- Link notes to KG entities
- Keep chronological narrative
"""
        (target_dir / "DEVELOPMENT_PRACTICES.md").write_text(practices_content)

    def _create_web_interfaces(self, target_dir: Path) -> None:
        """Create web interface files."""
        # Copy the query interface from the current project
        source_interface = Path(__file__).resolve().parents[2] / "nusy_query_interface.html"
        if source_interface.exists():
            shutil.copy(source_interface, target_dir / "nusy_query_interface.html")

    def _create_scripts(self, target_dir: Path) -> None:
        """Create utility scripts."""
        # Copy template files
        self._copy_template_files(target_dir)

        # setup.py for easy installation
        setup_script = f'''#!/usr/bin/env python3
"""Setup script for {target_dir.name}."""

import subprocess
import sys
from pathlib import Path

def main():
    """Set up the project."""
    print("🚀 Setting up {target_dir.name}...")

    # Install dependencies
    print("📦 Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)

    # Create .env file
    if not Path(".env").exists():
        print("⚙️  Creating .env file...")
        shutil.copy(".env.example", ".env")

    # Initialize data directory
    print("📁 Initializing data directory...")
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    print("✅ Setup complete!")
    print("\\n🎯 Next steps:")
    print("1. Start the server: python -m project_core.cli serve")
    print("2. Open nusy_query_interface.html in your browser")
    print("3. Begin development!")

if __name__ == "__main__":
    main()
'''
        (target_dir / "scripts" / "setup.py").write_text(setup_script)

        # Make setup script executable
        import stat
        setup_file = target_dir / "scripts" / "setup.py"
        setup_file.chmod(setup_file.stat().st_mode | stat.S_IEXEC)

    def _copy_template_files(self, target_dir: Path) -> None:
        """Copy template files to the scaffolded project."""
        # Copy CLI template
        cli_template = self.template_dir / "cli.py"
        if cli_template.exists():
            cli_content = cli_template.read_text()
            cli_content = cli_content.replace("{project_name}", target_dir.name)
            (target_dir / "src" / "project_core" / "cli.py").write_text(cli_content)

        # Copy API template
        api_template = self.template_dir / "api.py"
        if api_template.exists():
            api_content = api_template.read_text()
            api_content = api_content.replace("{project_name}", target_dir.name)
            (target_dir / "src" / "project_core" / "api.py").write_text(api_content)