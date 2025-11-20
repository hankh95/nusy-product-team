# Import Structure Guide: Architecture Redux 3

## Overview

Following the completion of EXP-057 Architecture Redux 3, the repository now implements a two-namespace model with clear separation between production domain code and autonomous self-improvement processes. This guide establishes the canonical import structure for the new architecture.

## Repository Structure

```
nusy-product-team/
├── domain/                          # Production domain code
│   ├── src/                         # Core domain logic
│   ├── models/                      # Domain models
│   ├── nusy_orchestrator/           # Orchestration components
│   ├── roles/                       # Domain roles
│   ├── scripts/                     # Domain scripts
│   ├── templates/                   # Domain templates
│   ├── examples/                    # Domain examples
│   ├── domain-features/             # Feature specifications
│   ├── domain-knowledge/            # Knowledge artifacts
│   └── tests/                       # Domain tests
├── self-improvement/                # Autonomous self-improvement
│   ├── santiago-pm/                 # PM scaffold
│   │   ├── tackle/                  # PM tools
│   │   └── tests/                   # PM tests
│   └── santiago-dev/                # Development infrastructure
├── santiago_core/                   # Santiago core services
│   ├── services/                    # Core services
│   ├── agents/                      # Core agents
│   └── tests/                       # Core tests
├── knowledge/                       # Global knowledge graph
├── tools/                           # Development tools
├── configs/                         # Configuration files
└── docs/                            # Documentation
```

## Import Conventions

### 1. Absolute Imports from Repository Root

**Always use absolute imports** starting from the repository root. This ensures clarity and consistency across the codebase.

```python
# ✅ CORRECT: Absolute import from repo root
from domain.src.nusy_pm_core.adapters.kg_store import KGStore
from santiago_core.services.llm_router import LLMRouter
from self_improvement.santiago_pm.tackle.kanban.kanban_service import KanbanService

# ❌ AVOID: Relative imports
from ..adapters.kg_store import KGStore  # Relative import
from .llm_router import LLMRouter        # Relative import

# ❌ AVOID: Implicit relative imports
import kg_store  # Unclear origin
```

### 2. Namespace-Based Organization

Imports should reflect the two-namespace architecture:

```python
# Domain namespace imports
from domain.models.clinical_intelligence import ClinicalCase
from domain.nusy_orchestrator.catchfish import CatchFish
from domain.src.nusy_pm_core.tools.self_questioning_tool import SelfQuestioningTool

# Self-improvement namespace imports
from self_improvement.santiago_pm.tackle.kanban.kanban_service import KanbanService
from self_improvement.santiago_pm.tackle.personal_logging.personal_logger import PersonalLogger

# Santiago core imports
from santiago_core.services.llm_router import LLMRouter
from santiago_core.agents.architect import ArchitectAgent
```

### 3. Import Grouping and Ordering

Follow this standard import order:

```python
# 1. Standard library imports
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

# 2. Third-party imports
import yaml
import requests
from pydantic import BaseModel

# 3. Local absolute imports (grouped by namespace)
# Domain imports
from domain.src.nusy_pm_core.adapters.kg_store import KGStore
from domain.models.clinical_intelligence import ClinicalCase

# Santiago core imports
from santiago_core.services.llm_router import LLMRouter

# Self-improvement imports
from self_improvement.santiago_pm.tackle.kanban.kanban_service import KanbanService
```

### 4. Import Aliases

Use clear, descriptive aliases when needed:

```python
# ✅ Clear aliases
from domain.src.nusy_pm_core.adapters.kg_store import KGStore as KnowledgeGraphStore
from santiago_core.services.llm_router import LLMRouter as LanguageModelRouter

# ❌ Unclear aliases
from domain.src.nusy_pm_core.adapters.kg_store import KGStore as KS
from santiago_core.services.llm_router import LLMRouter as LMR
```

## Migration Examples

### Before (Old Structure)

```python
# Old imports (relative to file location)
from adapters.kg_store import KGStore
from services.llm_router import LLMRouter
from tackle.kanban.kanban_service import KanbanService
```

### After (New Structure)

```python
# New imports (absolute from repo root)
from domain.src.nusy_pm_core.adapters.kg_store import KGStore
from santiago_core.services.llm_router import LLMRouter
from self_improvement.santiago_pm.tackle.kanban.kanban_service import KanbanService
```

## Common Import Patterns

### 1. Domain Component Imports

```python
# Knowledge operations
from domain.src.nusy_pm_core.adapters.kg_store import KGStore
from domain.domain_knowledge.kg_views.knowledge_graph import KnowledgeGraph

# Orchestration
from domain.nusy_orchestrator.catchfish import CatchFish
from domain.nusy_orchestrator.fishnet import FishNet

# Tools
from domain.src.nusy_pm_core.tools.self_questioning_tool import SelfQuestioningTool
```

### 2. Santiago Core Service Imports

```python
# LLM and routing
from santiago_core.services.llm_router import LLMRouter, TaskComplexity
from santiago_core.services.message_bus import MessageBus

# Agent interfaces
from santiago_core.agents.architect import ArchitectAgent
from santiago_core.agents.developer import DeveloperAgent
```

### 3. Self-Improvement Tool Imports

```python
# PM tools
from self_improvement.santiago_pm.tackle.kanban.kanban_service import KanbanService
from self_improvement.santiago_pm.tackle.question_answering.question_answering_service import QuestionAnsweringService

# Development infrastructure
from self_improvement.santiago_dev.tackle.qa_integration.qa_integration_service import QAIntegrationService
```

## Testing Import Structure

Tests should import from the same absolute paths:

```python
# In domain/tests/test_clinical_intelligence.py
from domain.models.clinical_intelligence import ClinicalCase
from domain.src.nusy_pm_core.adapters.kg_store import KGStore

# In santiago_core/tests/test_llm_router.py
from santiago_core.services.llm_router import LLMRouter, TaskComplexity

# In self-improvement/santiago-pm/tests/test_kanban_service.py
from self_improvement.santiago_pm.tackle.kanban.kanban_service import KanbanService
```

## Development Workflow Integration

### 1. IDE Configuration

Configure your IDE to recognize the repository root as the source root for proper import resolution.

### 2. PYTHONPATH Setup

The repository root should be in PYTHONPATH for development:

```bash
# Add to your shell profile or virtual environment activation
export PYTHONPATH="${PYTHONPATH}:/path/to/nusy-product-team"
```

### 3. Import Validation

Run import validation as part of development:

```bash
# Check for import issues
python -c "import domain.src.nusy_pm_core.adapters.kg_store; print('Domain imports OK')"
python -c "import santiago_core.services.llm_router; print('Core imports OK')"
python -c "import self_improvement.santiago_pm.tackle.kanban.kanban_service; print('Self-improvement imports OK')"
```

## Migration Tracking

All import updates are tracked in this document. When updating imports:

1. **Update the import statement** to use absolute path
2. **Test the import** to ensure it resolves correctly
3. **Update any dependent code** that may be affected
4. **Document the change** in commit messages

## Contact

**Architecture Lead:** Santiago-PM (Autonomous Agent)
**Captain:** Hank
**Reference:** EXP-057 Architecture Redux 3
