# Workflow Naming Thought Experiment

## Context

**Date**: November 15, 2025
**Experiment**: Evaluating nautical naming alternatives for "workflows" in NuSy PM
**Source**: ChatGPT analysis of nautical metaphors for multi-step processes
**Goal**: Find domain-fitting name that enhances Santiago's autonomous workflow capabilities

## Current Naming Context

- **Tackle**: Domain implementations (nautical rigging equipment)
- **Workflows**: Multi-step processes coordinating humans, agents, MCP services
- **Theme**: Nautical/shipping with Santiago the autonomous agent

## ChatGPT's Nautical Workflow Analogues

### Primary Candidates

#### 1. Passage ⭐⭐⭐⭐⭐ (RECOMMENDED)

"A deliberate, planned sequence of navigational steps to get from one point to another"

**Why it fits NuSy PM workflows**:

- **Multi-step journey**: Perfect for workflow sequences (spec → design → implement → test → deploy)
- **Dynamic adaptation**: "Evolves with new information (winds, tides)" = iterative development cycles
- **Planning artifact**: "Every passage has a passage plan" = development plans we already have
- **Quality aspects**: Starting point, waypoints, hazards, conditions, destination = workflow triggers, steps, quality gates, transitions, outputs

**NuSy PM mapping**:

- Workflow = Passage
- Step = Waypoint (subset of passage)
- Development Plan = Passage Plan
- Quality Gate = Hazard check/Navigation decision
- Workflow execution = Making passage

**Examples**:

- `nusy_pm/passages/tackle-development-passage.yaml`
- `santiago-passage-engine`
- "Plotting the passage" = designing workflows

#### 2. Waypoints ⭐⭐⭐⭐

"Defined steps along a route, each one a checkpoint or decision point"

**Strengths**: Maps 1:1 to BDD/workflow nodes
**Weaknesses**: Focuses on individual steps rather than the overall process
**Fit**: Good for step-level naming, but not comprehensive enough for the system

#### 3. Course ⭐⭐⭐

"The planned direction through the water"

**Strengths**: Great for decision logic ("change course", "hold course", "course correction")
**Weaknesses**: More about direction than multi-step execution
**Fit**: Good for workflow logic, but not the full process

#### 4. Sailing Orders ⭐⭐⭐⭐

"Captain issues the Sailing Orders, crew executes them step-by-step"

**Strengths**: Perfect for AI PM → AI developer handoffs
**Weaknesses**: More task-focused than process-focused
**Fit**: Excellent for individual workflow steps/tasks

### Secondary Candidates

#### 5. Logbook Entries ⭐⭐⭐

"Every action, change, and event recorded in narrative, timestamped form"

**Strengths**: Natural for audit trails and documentation
**Weaknesses**: More about recording than execution
**Fit**: Good for workflow logging, not the workflow itself

#### 6. Lifelines ⭐⭐⭐

"Safety procedures and guardrails in nautical operations"

**Strengths**: Perfect for workflow invariants and validation
**Weaknesses**: Too narrow (only safety aspects)
**Fit**: Good for quality gates, not the full workflow

#### 7. Ship's Tack ⭐⭐⭐⭐

"Changing direction in deliberate steps (tacking/jibing)"

**Strengths**: Perfect for iteration and hypothesis testing
**Weaknesses**: More about pivoting than full processes
**Fit**: Good for agile development cycles

#### 8. Running Rigging ⭐⭐⭐⭐⭐

"Adjustable lines used to sail the ship (vs standing rigging = permanent structure)"

**Strengths**:

- **Architecture distinction**: Standing rigging = framework/core, Running rigging = workflows/operations
- **Perfect metaphor**: Infrastructure vs execution layers
- **Domain fit**: Already using "tackle" (rigging equipment)

**Weaknesses**: Less intuitive than "passage"
**Fit**: Excellent technical metaphor, but "passage" is more accessible

#### 9. Charting ⭐⭐⭐

"Mapping territory, noting hazards, showing channels, recommended tracks"

**Strengths**: Perfect for knowledge graph modeling and system architecture
**Weaknesses**: More about mapping than execution
**Fit**: Good for design phase, not runtime workflows

## Recommendation: Rename "Workflows" to "Passages"

### Rationale

**Passage** is the strongest nautical analogue because:

1. **Comprehensive Coverage**: Captures the full multi-step process (not just steps or decisions)
2. **Domain Alignment**: Fits perfectly with existing nautical theme (tackle, voyages, etc.)
3. **Process Metaphor**: "Making a passage" feels like executing a workflow
4. **Planning Integration**: "Passage plans" align with our development plans
5. **Quality Integration**: Natural fit for waypoints, hazards, conditions
6. **Santiago Personality**: "Santiago's Passages" has legendary/Hemingway resonance

### Implementation Impact

#### File Structure Changes

```text
nusy_pm/
├── passages/                    # was: workflows/
│   ├── passage-system.md       # was: workflow-system.md
│   ├── examples/
│   │   ├── santiago-general-code-generation.yaml
│   │   └── nusy-pm-tackle-development.yaml
│   └── README.md
└── tackle/
    ├── passages/               # was: workflows/
    │   └── development-plan.md
    └── ...
```

#### Naming Changes

- **Passage Engine**: Workflow execution system
- **Passage Plan**: Development plan template
- **Making Passage**: Executing a workflow
- **Plotting the Passage**: Designing workflows
- **Passage Waypoints**: Workflow steps
- **Passage Hazards**: Quality gates/risk points

#### Code/CLI Changes

- `nusy passage list` (was: `nusy workflow list`)
- `santiago-passage-engine` (was: workflow-engine)
- Passage YAML schema (was: workflow YAML)

### Alternative Consideration: "Running Rigging"

**Running Rigging** is technically more precise:
- Standing rigging = tackle (permanent structure)
- Running rigging = passages (operational processes)

But **Passage** wins because:
- More intuitive and accessible
- Better Hemingway/Santiago resonance
- Clearer process metaphor
- Easier to understand for new team members

## Implementation Plan

### Phase 1: Analysis Complete ✅
- Documented all nautical analogues
- Evaluated fit for NuSy PM context
- Made recommendation with rationale

### Phase 2: Prototype (1-2 days)
- Rename workflow directory to passages
- Update key files with passage terminology
- Test basic functionality

### Phase 3: Full Migration (if approved)
- Update all references in codebase
- Update documentation and examples
- Update development plans and manifests

## Success Criteria

- **Intuitive**: New name feels natural in nautical theme
- **Comprehensive**: Covers full workflow concept (not just parts)
- **Memorable**: Sticks in mind, enhances Santiago personality
- **Functional**: Doesn't break existing metaphors or systems

## Conclusion

Recommendation: Rename "workflows" to "passages"

This maintains nautical authenticity while providing a comprehensive, intuitive metaphor for multi-step processes. "Passage" captures the journey aspect of workflows better than any other nautical concept, and "Santiago's Passages" has the perfect legendary resonance for an autonomous development system.

---

*This thought experiment can be referenced when deciding whether to implement the passage naming system or stick with "workflows" for familiarity.*
