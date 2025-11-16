# Santiago Project Scaffold Template

This template defines the folder structure and initial files for a new Santiago domain expert project.

## Project Structure

```
{{project_name}}/
├── README.md                    # Project overview and setup
├── pyproject.toml              # Python project configuration
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore patterns
├── .env.example               # Environment variables template
├── santiago-core/             # AI implementation (KG + agents)
│   ├── README.md
│   ├── __init__.py
│   ├── agents/                 # Autonomous agents
│   ├── core/                   # Core AI functionality
│   ├── interfaces/             # External interfaces
│   ├── knowledge/              # Knowledge graph
│   └── services/               # Core services
├── cargo-manifests/           # Feature specifications
├── ships-logs/                # Issues and incidents
├── voyage-trials/             # Experiments
├── navigation-charts/         # Development plans
├── captains-journals/         # Knowledge capture
├── crew-manifests/            # Agent roles
├── strategic-charts/          # Vision and strategy
├── quality-assessments/       # QA and testing
└── research-logs/             # Research findings
```

## Initial Files to Create

### README.md
```markdown
# {{project_name}}

A Santiago domain expert for [domain description].

## Overview

[Brief description of what this domain expert does]

## Architecture

- **santiago-core/**: Contains the AI implementation with knowledge graph and autonomous agents
- **PM Folders**: Human-readable artifacts for product management and development coordination

## Getting Started

1. Set up environment: `pip install -r requirements.txt`
2. Configure environment variables: `cp .env.example .env`
3. Start the core: `python -m santiago_core.run_team`

## Development

This project follows the Santiago PM methodology with nautical theming for all artifacts.
```

### pyproject.toml
```toml
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{{project_name}}"
version = "0.1.0"
description = "Santiago domain expert for {{domain}}"
authors = [
    {name = "Santiago PM", email = "santiago-pm@domain.com"}
]
dependencies = [
    "fastapi",
    "uvicorn",
    "pydantic",
    "rdflib",
    "typer",
    "python-dotenv"
]

[project.scripts]
{{project_name}} = "{{project_name}}.cli:main"

[tool.setuptools.packages.find]
where = ["."]
```

### requirements.txt
```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
rdflib==7.0.0
typer==0.9.0
python-dotenv==1.0.0
```

### .gitignore
```
# Environment variables
.env
.env.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Temporary files
temp/
tmp/
```

### .env.example
```
# Knowledge Graph Configuration
KG_PATH=./santiago-core/knowledge/
KG_FORMAT=turtle

# Agent Configuration
AGENT_LOG_LEVEL=INFO
AGENT_WORKSPACE=./

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Development
DEBUG=true
```

## PM Folder Templates

Each PM folder should contain:

### README.md (for each PM folder)
```markdown
# [Folder Name]

[Brief description of this PM artifact type]

## Template

Use `[folder-name]-template.md` as the starting point for new artifacts.

## Structure

[Description of expected content structure]

## Related

[Relationships to other PM artifacts and KG integration]
```

### Template Files
Each folder should have a corresponding template file (e.g., `cargo-manifest-template.md`) that follows the established scaffold pattern with YAML frontmatter.

## Initialization Process

When santiago-pm scaffolds a new project:

1. Create the folder structure
2. Copy template files to each PM folder
3. Initialize santiago-core with basic agent framework
4. Create initial KG with project metadata
5. Set up basic configuration files
6. Initialize git repository
7. Create initial PM artifacts for project setup

## Metadata

```yaml
template_id: santiago-project-scaffold-v1
description: Scaffold template for new Santiago domain expert projects
created_by: santiago-pm
created_at: 2025-11-16T00:00:00Z
version: 1.0.0
```