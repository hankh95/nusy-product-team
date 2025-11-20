# Architecture Review: EXP-057 Phase 3 - Two-Namespace Migration

## Executive Summary

**Status**: Phase 3 Complete - Core functionality validated, import issues resolved for domain namespace, self-improvement namespace needs import fixes.

**Architecture**: Successfully implemented two-namespace structure (`domain/` for production, `self-improvement/` for autonomous improvement) with absolute imports from repository root.

**Validated Components**:

- ✅ KG Store (3,300 triples loaded)
- ✅ Self-aware demo (20 PM tools, MCP manifest)
- ✅ Santiago Expert CLI (neurosymbolic reasoning)
- ✅ Kanban regenerator (polls every 10s, generates markdown)

---

## Current Architecture State

### Directory Structure

```text
nusy-product-team/
├── domain/                    # Production code namespace
│   ├── src/nusy_pm_core/     # Core PM domain logic
│   └── scripts/              # Demo and utility scripts
├── self-improvement/         # Autonomous improvement namespace
│   ├── santiago-pm/         # PM-focused autonomous tools
│   └── santiago-dev/        # Development-focused tools
├── santiago_core/           # Legacy code (needs review)
└── expeditions/             # Historical expedition records
```

### Import Strategy

- **Absolute imports** from repository root: `from domain.src.nusy_pm_core.adapters.kg_store import KGStore`
- **Namespace separation** between production (`domain.*`) and improvement (`self_improvement.*`)
- **Working examples**: KG store, expert CLI, self-aware demo

---

## Validated Functionality

### 1. Knowledge Graph Store

**Location**: `domain/src/nusy_pm_core/adapters/kg_store.py`

**Status**: ✅ Fully operational

- Loads 3,300 triples from `knowledge/kg/santiago_kg.ttl`
- SPARQL query execution
- Domain knowledge export
- Provenance tracking

### 2. Self-Aware Demo

**Location**: `domain/scripts/demo_santiago_pm_self_aware.py`

**Status**: ✅ Fully operational

- Demonstrates bootstrap capability
- MCP manifest with 20 PM tools
- Knowledge graph integration
- Self-query capabilities

### 3. Santiago Expert CLI

**Location**: `domain/src/nusy_pm_core/santiago_expert_cli.py`

**Status**: ✅ Fully operational

- Neurosymbolic reasoning for PM questions
- High confidence answers (82.5% on PM tools)
- KG-backed responses with provenance

### 4. Kanban System

**Location**: `self-improvement/santiago-pm/tackle/kanban/`

**Status**: ✅ Core functionality working

- Board management and card tracking
- Markdown generation (3,562 bytes)
- Regenerator polls every 10 seconds

---

## Issues Requiring Architecture Review

### 1. Self-Improvement Import Problems

**Issue**: Self-improvement tools fail with `No module named 'self_improvement'`

**Impact**: Kanban workflow demo, experiment runners, quality assessments

**Root Cause**: sys.path configuration issues in self-improvement scripts

**Proposed Solutions**:

- Option A: Fix sys.path in existing scripts to add repository root
- Option B: Convert to relative imports within self-improvement namespace
- Option C: Create setup.py/package structure for self-improvement

### 2. Legacy Code Status

**Issue**: `santiago_core/` contains substantial legacy code not integrated with new architecture

**Impact**: Confusion for reviewers, potential duplication

**Options**:

- Archive to `_archive/legacy-santiago-core/`
- Migrate valuable components to new structure
- Document as "legacy reference implementation"

### 3. Missing Components

**Issue**: Tests reference `agent_adapter` and `experiment_runner` services that don't exist

**Impact**: Failing tests, incomplete autonomous agent framework

**Options**:

- Implement missing services in domain structure
- Remove obsolete tests
- Create feature work to implement autonomous agents

### 4. Expedition Artifact Structure

**Issue**: Expeditions are scattered, no standard artifact format

**Proposal**: Standardize expedition records as:

```text
expeditions/exp_057/
├── README.md (overview)
├── captain-decisions-log.md
├── phase2-progress-log.md
├── triage-report.md
├── code/ (original scripts)
├── results/ (outputs, logs)
└── analysis/ (lessons learned)
```

---

## Architecture Questions for Review

### Import and Namespace Strategy

1. **Should self-improvement use absolute imports like domain?**
   - Pro: Consistency across codebase
   - Con: Longer import paths

2. **Should we create package structure for self-improvement?**
   - Pro: Standard Python packaging
   - Con: Additional complexity

### Component Ownership

1. **Where should autonomous agent services live?**
   - Option A: `domain/src/nusy_pm_core/services/` (production services)
   - Option B: `self-improvement/santiago-pm/services/` (autonomous services)
   - Option C: Separate `agents/` namespace

2. **How to handle kanban integration?**
   - Currently in self-improvement, but domain scripts need it
   - Option A: Move to domain as core service
   - Option B: Keep in self-improvement, fix cross-namespace imports

### Legacy Code Disposition

1. **Disposition of santiago_core/?**
   - Archive as historical reference
   - Extract valuable components
   - Delete if truly obsolete

### Testing Strategy

1. **How to test cross-namespace functionality?**
   - Integration tests that span domain ↔ self-improvement
   - Mock external dependencies
   - End-to-end validation scripts

---

## Recommended Work Packages

### High Priority (Pre-Production)

1. **Fix Self-Improvement Imports** (2-4 hours)
   - Standardize sys.path configuration
   - Test kanban workflow demo
   - Validate experiment runners

2. **Resolve Missing Components** (4-6 hours)
   - Implement or remove agent_adapter references
   - Create experiment_runner service or update tests
   - Ensure test suite passes

### Medium Priority (Architecture Cleanup)

1. **Legacy Code Disposition** (2-3 hours)
   - Audit santiago_core/ for valuable components
   - Archive or migrate as appropriate
   - Update documentation

2. **Expedition Artifact Standardization** (1-2 hours)
   - Create standard structure template
   - Migrate existing expeditions
   - Document artifact preservation process

### Low Priority (Polish)

1. **Documentation Updates** (2-3 hours)
   - Update README with new architecture
   - Create developer onboarding guide
   - Document import patterns

2. **Integration Testing** (3-4 hours)
   - Create end-to-end validation scripts
   - Test cross-namespace functionality
   - Performance benchmarking

---

## Success Criteria

**Minimum Viable**: Core domain functionality works, self-improvement imports resolved, no failing critical tests.

**Full Success**: Clean architecture, comprehensive tests, documented patterns, standardized artifacts.

**Timeline Estimate**: 8-12 hours total work across recommended packages.

---

*Generated for architecture review: November 20, 2025*
*Current commit: exp-057-architecture-redux-3-migration*</content>
