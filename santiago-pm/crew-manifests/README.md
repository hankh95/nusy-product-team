# Crew Manifests Archive

This directory contains archived crew manifest files that have been superseded by the UARS (Unified Agent Role Specification) system.

## Why Archived?

These files represented an early approach to defining agent roles, but mixed concerns:
- Agent specifications (what agents ARE) ← Now in `santiago-pm/uars/`
- User personas (who agents SERVE) ← Now in `santiago-pm/personas/`

## Migration

The content has been reorganized:

### Agent Specifications → UARS
- `nusy-product-manager.role-spec.md` → `santiago-pm/uars/santiago-pm.uars.yaml`
- `architect-nusy.agent.instructions.md` → `santiago-pm/uars/architect-nusy.uars.yaml`
- `architect-systems.agent.instructions.md` → `santiago-pm/uars/architect-systems.uars.yaml`
- `developer.agent.instructions.md` → `santiago-pm/uars/developer.uars.yaml`
- `qa.agent.instructions.md` → `santiago-pm/uars/qa-specialist.uars.yaml`
- `platform.agent.instructions.md` → `santiago-pm/uars/platform-engineer.uars.yaml`
- `ux.agent.instructions.md` → `santiago-pm/uars/ux-researcher-designer.uars.yaml`

### GitHub Agent Prompts
Agent instructions have also been copied to `.github/agents/` for AI agent use:
- `.github/agents/santiago-pm.agent.md`
- `.github/agents/architect-nusy.agent.md`
- `.github/agents/architect-systems.agent.md`
- `.github/agents/qa-specialist.agent.md`
- `.github/agents/platform-engineer.agent.md`
- `.github/agents/ux-researcher.agent.md`

### User Personas Created
New persona files capture user needs:
- `santiago-pm/personas/product-owner-hank.md`
- `santiago-pm/personas/knowledge-architect-user.md`
- `santiago-pm/personas/systems-architect-user.md`
- `santiago-pm/personas/developer-user.md`
- `santiago-pm/personas/qa-specialist-user.md`
- `santiago-pm/personas/platform-engineer-user.md`
- `santiago-pm/personas/ux-researcher-user.md`

## When to Reference

These archived files can be referenced for:
- Historical context on role evolution
- Original phrasing and intent
- Comparison with current UARS

## Do Not Edit

These files are archived and should not be edited. All updates go to:
- **Agent specs**: `santiago-pm/uars/*.uars.yaml`
- **User personas**: `santiago-pm/personas/*.md`
- **AI prompts**: `.github/agents/*.agent.md`

Archived: 2025-11-17
