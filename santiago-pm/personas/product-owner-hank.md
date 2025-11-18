---
artifact_type: persona
persona_id: product-owner-hank
role: Product Owner & Vision Holder
created: 2025-11-17
created_by: Copilot
status: active
tags:
  - product-owner
  - vision-holder
  - lean-hypothesis-testing
---

# Persona: Hank — Product Owner & Vision Holder

## Demographics
- **Role**: Product Owner, System Architect, Principal Engineer
- **Experience**: 15+ years in software development, product management
- **Technical Background**: Deep technical expertise, neurosymbolic systems
- **Domain Expertise**: Healthcare (clinical informatics), AI/ML, product development

## Goals & Motivations

### Primary Goals
1. **Build neurosymbolic PM system** that combines symbolic reasoning (KG) with AI agents
2. **Validate lean hypothesis-driven development** works with AI-assisted teams
3. **Create reusable patterns** for multi-agent product development
4. **Maintain high quality** through BDD/TDD and continuous validation

### Secondary Goals
- Learn from PM thought leaders (Goethelf, Kerievsky, Patton)
- Document patterns for future projects
- Build sustainable development practices
- Create tools that serve humanity (Baha'i principles)

## Pain Points & Frustrations

### Context Loss Problem (CRITICAL)
> "As I use Copilot with different models and switch between them, I lose track of what context each model has. Sometimes I have to re-explain things or remind the model of prior decisions, which wastes time and breaks my flow."

**Impact**: 15+ minutes per session re-explaining, broken flow state

### Backlog Management Challenges
- Discovering work items scattered across logs, comments, conversations
- Prioritizing features without clear decision framework
- Knowing what agents can/should do autonomously

### Multi-Agent Coordination
- Unclear when to escalate vs. decide independently
- Agents lack understanding of their scope of authority
- Workflow from code completion to issue closure is manual

## Needs & Requirements

### Must Have
- **Context preservation**: Restore full context when switching AI models
- **Autonomous agents**: Agents that can work independently within scope
- **Clear authority boundaries**: UARS defining what each agent can decide
- **Provenance**: Always know why decisions were made
- **Quality gates**: Never compromise on testing and validation

### Nice to Have
- Automated backlog discovery and grooming
- Temporal reasoning (what was the backlog on DATE?)
- Conversational interfaces for PM tasks
- Vector DB for semantic search across artifacts

## Behaviors & Patterns

### Work Style
- **Hypothesis-driven**: Every feature starts with a hypothesis
- **Evidence-based**: Prioritize based on data, not opinions
- **Quality-focused**: TDD/BDD, red-green-refactor cycle mandatory
- **Iterative**: Small batches, rapid feedback, continuous learning

### Decision Making
- Uses 4-factor prioritization: customer_value, unblock_impact, worker_availability, learning_value
- Escalates when uncertain rather than guessing
- Documents decisions in KG for future reference
- Values explainability over black-box decisions

### Communication Preferences
- Structured artifacts (YAML frontmatter + markdown)
- Clear reasoning with cited sources
- Proactive escalation when needed
- Transparent progress tracking

## Tools & Technology

### Currently Uses
- Copilot (multiple models: GPT-4, Claude, etc.)
- Git/GitHub for version control
- Python for implementation
- BDD (Gherkin) for specs
- Knowledge graph for reasoning

### Wants to Use
- Santiago-PM MCP service
- Continuous backlog discovery
- Automated PR/issue workflow
- Personal log system for context

## Success Metrics

### Personal Success
- Context restoration < 2 seconds (vs. 15+ minutes)
- Can switch AI models without re-explaining
- Agents work autonomously 80% of time
- Clear provenance for all decisions

### Team Success
- Cycle time reduced by 20%
- Team effectiveness up 90%
- Experiment success rate > 70%
- All work traceable to hypotheses

## Quotes

> "I want agents to know their scope of authority so they don't ask me every time."

> "Context loss is killing my productivity. I need to preserve session history."

> "Every feature should start with a hypothesis we can test."

> "Make work visible through specs, tests, and KG triples."

## User Journey Touchpoints

### Daily Workflow
1. **Morning**: Review discovery results, prioritize backlog
2. **Work Session**: Collaborate with AI agents on features
3. **Context Switch**: Change AI models, need fast context restore
4. **End of Day**: Save session logs, review progress

### Feature Development
1. Discovery (scan logs, manifests, KG)
2. Hypothesis formulation
3. Prioritization (4-factor algorithm)
4. BDD scenario creation
5. Implementation (with agents)
6. Validation (tests, experiments)
7. Learning (capture in KG)

## Design Implications

### For Santiago-PM
- Must support context preservation (F-027)
- Must expose clear authority boundaries (UARS)
- Must explain all decisions (neurosymbolic reasoning)
- Must be fast (<2s for common operations)

### For UX
- CLI-first, conversational UI later
- Structured outputs (YAML + markdown)
- Clear status visibility
- Proactive escalation prompts

## Related Artifacts
- Personal logs: `santiago-pm/personal-logs/humans/`
- Hypotheses: `santiago-pm/cargo-manifests/`
- Discovery results: `santiago-pm/discovery-results.json`
- Session logs: `santiago-pm/personal-logs/agents/`
