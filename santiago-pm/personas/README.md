# Santiago-PM Personas

This directory contains user personas for stakeholders who need Santiago-PM capabilities.

## What are Personas?

Personas are evidence-based representations of user types who interact with or need the capabilities of Santiago-PM agents. These are NOT agent specifications (those are in `santiago-pm/uars/`), but rather descriptions of the **humans** or **user types** who benefit from agent capabilities.

## Persona Files

### Primary Persona
- `product-owner-hank.md` - Primary user and vision holder (based on real pain points and needs)

### Secondary Personas (Agent Users)
- `knowledge-architect-user.md` - User who needs KG architecture capabilities
- `systems-architect-user.md` - User who needs systems/platform architecture capabilities
- `developer-user.md` - User who needs development support
- `qa-specialist-user.md` - User who needs testing/validation support
- `platform-engineer-user.md` - User who needs deployment/monitoring support
- `ux-researcher-user.md` - User who needs UX research support

## Persona Structure

Each persona follows UX research best practices:

```yaml
---
artifact_type: persona
persona_id: unique-id
role: User Role Title
created: 2025-11-17
created_by: Copilot
status: active
tags: [relevant, tags]
---

# Persona: Name

## Demographics / Profile
## Goals & Motivations
## Pain Points & Frustrations
## Needs & Requirements
## Behaviors & Patterns
## Tools & Technology
## Success Metrics
## User Journey
## Design Implications
```

## Evidence Sources

Personas are derived from:
- **Direct quotes**: From product owner (Hank) sessions
- **Personal logs**: Pain points documented in `santiago-pm/personal-logs/`
- **Discovery results**: Discovered needs in `santiago-pm/discovery-results.json`
- **Domain knowledge**: Best practices from PM/UX/Dev domains

## Usage

### For Feature Design
Reference personas when creating cargo manifests to ensure features serve real user needs.

### For Prioritization
Use persona pain points and goals to inform prioritization decisions.

### For UX Design
Use personas to design interfaces and workflows that match user mental models.

### For Validation
Test features against persona goals to ensure they solve real problems.

## Relationship to UARS

```
Personas (santiago-pm/personas/)
    ↓ describe needs/goals of
Agent Roles (santiago-pm/uars/)
    ↓ define capabilities to serve
Features (santiago-pm/cargo-manifests/)
    ↓ implement with
MCP Tools (knowledge/catches/*/mcp-manifest.json)
```

## Evolution

Personas should evolve based on:
- New user research findings
- Discovered pain points in personal logs
- Changes in user workflows
- Feedback from real usage

Update personas when evidence suggests user needs have changed.
