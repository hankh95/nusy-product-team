# Ship's Log - UARS System Implementation
**Stardate**: 2025-01-16
**Log Entry**: F-031 - Unified Agent Role Specification System
**Captain**: Product Manager (Santiago-PM)
**Status**: ✅ Complete

---

## Executive Summary

Implemented the **Unified Agent Role Specification (UARS)** system, creating a reference-based architecture that bridges human-readable role definitions with machine-executable MCP manifests. This establishes single-source-of-truth for agent coordination while respecting knowledge graph principles (no duplication).

**Impact**: All 7 roles now have clear specifications (UARS), user personas, and AI prompts, enabling structured agent coordination for F-030 (Team Workflow System).

---

## Mission Context

**Original Question**: "Crew manifests describe agents right now, but what would they need to turn into for us to use them to describe the roles and responsibilities of this role? Is this actually an early skeleton of the MCP manifest?"

**Challenge**: How do we evolve crew manifests (human-readable narratives) into actionable specifications that can coordinate agent behavior AND generate machine-executable MCP manifests?

**Solution**: UARS - a reference-based specification format that:
1. Defines agent roles and responsibilities clearly
2. References (not duplicates) canonical sources for capabilities
3. Provides behavioral and governance specifications
4. Serves as single source for both human understanding and machine coordination

---

## What Was Built

### 1. UARS Specifications (7 agents)
**Location**: `santiago-pm/uars/`

Created comprehensive role specifications for all team members:

- **santiago-pm.uars.yaml** (540+ lines) - Product Manager
  - Purpose: Strategic planning, feature prioritization, team coordination
  - Authority: Can approve features, schedule work, coordinate agents
  - References: F-027, F-029, F-030, F-031 cargo manifests
  
- **architect-nusy.uars.yaml** (420+ lines) - Knowledge Graph Architect
  - Purpose: Knowledge graph design, semantic modeling
  - Authority: Can define schemas, approve graph structures
  - References: F-032 (KG infrastructure) cargo manifest
  
- **architect-systems.uars.yaml** (380+ lines) - Systems/Platform Architect
  - Purpose: System design, architecture decisions
  - Authority: Can approve architectural changes, define standards
  - References: Infrastructure-related cargo manifests
  
- **developer.uars.yaml** (350+ lines) - Software Developer
  - Purpose: Feature implementation, testing, documentation
  - Authority: Can implement approved features, create tests
  - References: Active feature cargo manifests
  
- **qa-specialist.uars.yaml** (330+ lines) - QA Specialist
  - Purpose: Testing, quality assurance, validation
  - Authority: Can block releases, approve quality gates
  - References: Testing-related features
  
- **platform-engineer.uars.yaml** (320+ lines) - Platform/Deployment Engineer
  - Purpose: Infrastructure, deployment, operations
  - Authority: Can approve deployments, modify infrastructure
  - References: Deployment and operations manifests
  
- **ux-researcher-designer.uars.yaml** (310+ lines) - UX Researcher/Designer
  - Purpose: User research, interface design, usability
  - Authority: Can approve UI changes, conduct user research
  - References: UX-related feature manifests

**UARS Schema** includes:
```yaml
schema_version: 1.0.0
agent_id: <unique-id>
role: <role-name>
rank: journeyman | senior | master
specialization: <domain>
status: active | development | deprecated

role_definition:
  purpose: <mission statement>
  responsibilities:
    primary: [list]
    secondary: [list]
  scope_of_authority:
    can_decide_independently: [list]
    requires_approval: [list]
    must_escalate: [list]

capability_references:
  implemented_tools:
    source: knowledge/catches/<agent>/mcp-manifest.json
    type: mcp-manifest
  features_in_development:
    - feature_id: F-XXX
      source: santiago-pm/cargo-manifests/<feature>.md
  discovered_opportunities:
    source: santiago-pm/discovery-results.json

behavioral_specification:
  communication_style: <description>
  decision_criteria: [list]
  ethical_framework: [list]
  collaboration_patterns:
    - works_with: <role>
      interaction_type: <type>
      frequency: <frequency>

governance:
  approval_gates: [list]
  escalation_rules: [list]
  audit_requirements: [list]
```

### 2. User Personas (7 personas)
**Location**: `santiago-pm/personas/`

Created evidence-based user personas for each role:

- **product-owner-hank.md** - Primary user persona
  - Based on real pain points from logs and commits
  - Goals: Build AI agents, manage workflow, ship features
  - Pain points: Context switching, coordination overhead, workflow friction
  
- **knowledge-architect-user.md** - KG architect needs
  - Goals: Design knowledge graphs, ensure semantic correctness
  - Pain points: Schema evolution, data migration, query performance
  
- **systems-architect-user.md** - Systems architect needs
  - Goals: Design scalable systems, ensure reliability
  - Pain points: Complexity management, technical debt
  
- **developer-user.md** - Developer needs
  - Goals: Implement features, write tests, ship code
  - Pain points: Unclear requirements, context gathering, test maintenance
  
- **qa-specialist-user.md** - QA specialist needs
  - Goals: Ensure quality, catch bugs, validate features
  - Pain points: Test coverage gaps, regression testing
  
- **platform-engineer-user.md** - Platform engineer needs
  - Goals: Maintain infrastructure, ensure uptime
  - Pain points: Deployment complexity, monitoring gaps
  
- **ux-researcher-user.md** - UX researcher needs
  - Goals: Understand users, design interfaces
  - Pain points: Limited user research, usability testing

Each persona includes:
- Profile (background, experience, context)
- Goals (what they want to accomplish)
- Pain points (current frustrations)
- Needs (how UARS system helps)
- Success metrics (how to measure success)
- User journey (typical interaction flow)

### 3. GitHub Agent Prompts (6 new agents)
**Location**: `.github/agents/`

Created AI agent prompts for GitHub Copilot:

- `santiago-pm.agent.md` - Product Manager prompt
- `architect-nusy.agent.md` - KG Architect prompt
- `architect-systems.agent.md` - Systems Architect prompt
- `qa-specialist.agent.md` - QA Specialist prompt
- `platform-engineer.agent.md` - Platform Engineer prompt
- `ux-researcher.agent.md` - UX Researcher prompt

**Note**: `developer.agent.md` already exists (created earlier)

Each prompt follows **chatagent format**:
```markdown
# <Role Name>

<Mission statement>

## Inputs
- User request
- Current workspace state
- Relevant documentation

## Outputs
- Implementation
- Tests
- Documentation

## Practices
- <Best practices for this role>
- <Collaboration patterns>
- <Decision criteria>

## References
- UARS: santiago-pm/uars/<role>.uars.yaml
- Persona: santiago-pm/personas/<role>-user.md
- Cargo manifests: santiago-pm/cargo-manifests/
```

**Strategy**: During "fake it till you make it" phase, these prompts are manually maintained. Later, they'll be auto-generated from UARS when MCP is fully implemented.

### 4. Archived Old Crew Manifests
**Location**: `santiago-pm/crew-manifests/_archive/`

Archived 7 old crew manifest files:
- `nusy-product-manager.role-spec.md`
- `architect-nusy.agent.instructions.md`
- `architect-systems.agent.instructions.md`
- `developer.agent.instructions.md`
- `qa.agent.instructions.md`
- `platform.agent.instructions.md`
- `ux.agent.instructions.md`

**Reason**: These mixed concerns (agent specs + user needs). Now separated into UARS (agent specs) + personas (user needs).

### 5. Documentation
Created 3 README files:
- `santiago-pm/uars/README.md` - Explains UARS system, benefits, usage
- `santiago-pm/personas/README.md` - Explains persona methodology
- `santiago-pm/crew-manifests/README.md` - Explains migration to UARS

### 6. F-031 Cargo Manifest
**Location**: `santiago-pm/cargo-manifests/unified-agent-role-specification.md`

Created comprehensive feature manifest with:
- Feature overview and purpose
- 5 user stories (define, validate, evolve, compile, coordinate)
- Technical design (YAML schema, reference pattern)
- 4 implementation phases (15-20 hours total)
- Integration with F-027, F-029, F-030

---

## Key Architecture Decisions

### 1. Reference-Based Architecture
**Decision**: UARS points to canonical sources, doesn't duplicate data

**Problem**: Initial approach listed features directly in UARS, violating knowledge graph principle

**User Insight**: "We want one representation... listing proposed features in UARS does not seem right"

**Solution**: UARS uses references:
```yaml
capability_references:
  implemented_tools:
    source: knowledge/catches/santiago-pm/mcp-manifest.json
    type: mcp-manifest
  features_in_development:
    - feature_id: F-027
      source: santiago-pm/cargo-manifests/personal-log-feature.md
  discovered_opportunities:
    source: santiago-pm/discovery-results.json
```

**Benefits**:
- Single source of truth maintained
- Update source → UARS reflects change automatically
- No sync issues between manifests
- Simpler maintenance (UARS stays small)

### 2. Semantic Separation
**Decision**: Separate UARS (agent specs) from Personas (user needs)

**Problem**: Old crew manifests mixed agent specifications with user needs

**User Insight**: "Crew manifests should actually be user personas"

**Solution**: Three distinct artifact types:
- **UARS** = What agents ARE (role definitions, capabilities, behavior)
- **Personas** = Who needs the agents (stakeholder goals, pain points)
- **GitHub Agents** = How agents behave (AI prompts for GitHub Copilot)

**Benefits**:
- Clear semantic boundaries
- Proper separation of concerns
- Each artifact serves distinct purpose
- Easier to maintain and evolve

### 3. Domain-Specific Location
**Decision**: Place UARS in `santiago-pm/uars/` (domain-specific) not `santiago_core/crew-manifests/` (centralized)

**Problem**: Where should UARS live?

**User Insight**: "Santiago-pm artifacts are all things we need to build santiago-pm"

**Rationale**: UARS defines what santiago-pm IS (part of building it), not just describes how it works (documentation)

**Benefits**:
- Consistent with project structure
- Scalable (other agents can have their own UARS directories)
- Clear ownership (santiago-pm owns its specs)

### 4. Manual Then Automated
**Decision**: Manually maintain GitHub agent prompts during facade phase

**Strategy**: "Fake it till you make it" - prompts simulate MCP behavior until MCP is fully implemented

**Future**: When MCP is ready, auto-generate prompts from UARS:
```python
# Future: UARS → GitHub Agent Prompt
def generate_prompt_from_uars(uars_path):
    uars = load_yaml(uars_path)
    
    # Query referenced sources
    mcp_manifest = load_json(uars.capability_references.implemented_tools.source)
    cargo_manifests = [load_md(ref.source) for ref in uars.capability_references.features_in_development]
    
    # Generate prompt
    return f"""
    # {uars.role}
    {uars.role_definition.purpose}
    
    ## Capabilities
    {format_tools(mcp_manifest.tools)}
    
    ## Features in Development
    {format_features(cargo_manifests)}
    
    ## Behavior
    {uars.behavioral_specification.communication_style}
    ...
    """
```

**Benefits**:
- Ship working system now (with manual prompts)
- Prepare for automation later (UARS as source)
- No rework needed (prompts already reference UARS)

---

## How UARS Solves Problems

### Problem 1: Crew Manifest Evolution
**Before**: Crew manifests were human-readable narratives mixing agent specs with user needs

**After**: 
- UARS = Structured agent specifications (role, capabilities, behavior, governance)
- Personas = User needs and pain points
- GitHub Agents = AI prompts referencing UARS

**Benefit**: Clear separation enables both human understanding and machine coordination

### Problem 2: MCP Manifest Generation
**Before**: No clear path from human intent to machine-executable MCP manifest

**After**: UARS bridges the gap:
```
Human Intent → UARS (role definition) → MCP Manifest (tool implementations)
             → GitHub Agent Prompts (AI behavior)
```

**Future**: UARS compiler will generate MCP manifest from UARS:
1. Read UARS (role definition, capabilities, behavior)
2. Query referenced sources (cargo manifests, discovery results)
3. Generate MCP manifest (tools, resources, prompts)

**Benefit**: Single source (UARS) generates multiple derived assets

### Problem 3: Capability Planning
**Before**: No clear way to track implemented vs planned capabilities

**After**: UARS has three capability sections:
```yaml
capability_references:
  implemented_tools:      # What we HAVE (MCP manifest)
    source: knowledge/catches/santiago-pm/mcp-manifest.json
  features_in_development: # What we're BUILDING (cargo manifests)
    - feature_id: F-027
      source: santiago-pm/cargo-manifests/personal-log-feature.md
  discovered_opportunities: # What we COULD build (discovery results)
    source: santiago-pm/discovery-results.json
```

**Benefit**: Complete view of capability landscape (current + planned + potential)

### Problem 4: Agent Coordination
**Before**: No clear role boundaries, approval gates, escalation rules

**After**: UARS governance section specifies:
```yaml
scope_of_authority:
  can_decide_independently:
    - Approve personal log entries
    - Schedule feature work
  requires_approval:
    - Feature creation
    - Architectural changes
  must_escalate:
    - Major architectural decisions
    - Cross-team conflicts

governance:
  approval_gates:
    - Before feature implementation: architect approval
  escalation_rules:
    - Conflicting priorities → escalate to PM
```

**Benefit**: Clear rules prevent conflicts, enable autonomous work within boundaries

---

## Integration with Other Features

### F-027: Personal Log System
**Connection**: UARS references F-027 in santiago-pm capabilities
- Santiago-PM uses personal log to document decision rationale
- UARS specifies when logs should be created (after major decisions)
- Personas show user needs for context preservation

### F-029: State Machine Workflow
**Connection**: UARS provides role context for workflow transitions
- Each UARS specifies which workflow states agent can control
- Approval gates defined in UARS map to workflow approval points
- Future: Workflow engine queries UARS to validate transitions

### F-030: Team Workflow System
**Connection**: UARS enables multi-agent coordination
- Each role has clear responsibilities and authority
- Collaboration patterns specify how agents work together
- Escalation rules prevent conflicts
- Next step: Build workflow orchestrator using UARS

### F-032: Knowledge Graph Infrastructure
**Connection**: Architect-Nusy UARS references F-032
- KG Architect UARS specifies schema design authority
- UARS itself could be stored in knowledge graph
- Future: Query UARS from KG for dynamic agent coordination

---

## What Changed

**Files Created** (31 total):
```
.github/agents/
├── architect-nusy.agent.md (NEW)
├── architect-systems.agent.md (NEW)
├── platform-engineer.agent.md (NEW)
├── qa-specialist.agent.md (NEW)
├── santiago-pm.agent.md (NEW)
└── ux-researcher.agent.md (NEW)

santiago-pm/cargo-manifests/
└── unified-agent-role-specification.md (NEW - F-031)

santiago-pm/crew-manifests/
├── README.md (UPDATED)
└── _archive/
    ├── architect-nusy.agent.instructions.md (ARCHIVED)
    ├── architect-systems.agent.instructions.md (ARCHIVED)
    ├── developer.agent.instructions.md (ARCHIVED)
    ├── nusy-product-manager.role-spec.md (ARCHIVED)
    ├── platform.agent.instructions.md (ARCHIVED)
    ├── qa.agent.instructions.md (ARCHIVED)
    └── ux.agent.instructions.md (ARCHIVED)

santiago-pm/personas/
├── README.md (NEW)
├── developer-user.md (NEW)
├── knowledge-architect-user.md (NEW)
├── platform-engineer-user.md (NEW)
├── product-owner-hank.md (NEW)
├── qa-specialist-user.md (NEW)
├── systems-architect-user.md (NEW)
└── ux-researcher-user.md (NEW)

santiago-pm/uars/
├── README.md (NEW)
├── architect-nusy.uars.yaml (NEW)
├── architect-systems.uars.yaml (NEW)
├── developer.uars.yaml (NEW)
├── platform-engineer.uars.yaml (NEW)
├── qa-specialist.uars.yaml (NEW)
├── santiago-pm.uars.yaml (NEW)
└── ux-researcher-designer.uars.yaml (NEW)
```

**Commit**: 87bf100
**Insertions**: 3,287 lines
**Files Changed**: 31

---

## Team Impact

### All Roles Now Have:
1. **UARS Specification**: Clear role definition, capabilities, behavior, governance
2. **User Persona**: Evidence-based needs, pain points, success metrics
3. **GitHub Agent Prompt**: AI instructions referencing UARS

### Santiago-PM Can Now:
- Coordinate agents using UARS specifications
- Validate authority boundaries before delegating work
- Track implemented vs planned capabilities per role
- Generate MCP manifests from UARS (future)

### Development Process Improved:
- **Before**: Ad-hoc agent coordination, unclear responsibilities
- **After**: Structured coordination with clear rules and boundaries

### Knowledge Graph Benefits:
- Single source of truth (UARS)
- Derived assets (MCP manifests, prompts) reference UARS
- Update UARS → all derived assets reflect change

---

## Next Steps

### Immediate (This Sprint)
1. **Update DEVELOPMENT_PLAN.md** with UARS system
2. **Test UARS usage** in F-030 (Team Workflow System)
3. **Validate personas** with actual usage patterns

### Short-term (Next 2-3 Weeks)
4. **Implement UARS compiler** (UARS → MCP manifest generator)
   - Parse UARS YAML
   - Query referenced sources (cargo manifests, discovery results)
   - Generate MCP manifest JSON
   
5. **Implement prompt generator** (UARS → GitHub Agent Prompt)
   - Read UARS specifications
   - Format as chatagent markdown
   - Auto-update prompts when UARS changes

6. **Build workflow orchestrator** (F-030)
   - Query UARS for role capabilities
   - Validate approval gates
   - Route work to appropriate agents

### Long-term (Future Sprints)
7. **UARS validation tools** (lint, test, verify)
8. **UARS evolution tracking** (version history, change log)
9. **UARS discovery** (auto-generate from usage patterns)
10. **Knowledge graph integration** (store UARS in graph)

---

## Lessons Learned

### Architectural Insights

1. **Reference-based > Duplication**
   - Learned: Listing features directly in UARS violates single-source-of-truth
   - Solution: UARS points to canonical sources
   - Benefit: No sync issues, simpler maintenance

2. **Separate Concerns Early**
   - Learned: Crew manifests mixed agent specs with user needs
   - Solution: UARS (agent) vs Personas (user) vs Prompts (AI)
   - Benefit: Clear boundaries, easier to maintain

3. **Domain-Specific > Centralized**
   - Learned: Centralized location doesn't reflect ownership
   - Solution: Each agent owns its UARS directory
   - Benefit: Scalable, clear ownership

4. **Manual Then Automated**
   - Learned: Can't build automation before understanding
   - Solution: Manual prompts now, auto-generation later
   - Benefit: Ship working system, prepare for automation

### Process Insights

1. **User Challenge Led to Better Design**
   - User questioned: "Listing proposed features in UARS does not seem right"
   - Resulted in: Reference-based architecture (much better)
   - Lesson: Challenge assumptions, iterate on design

2. **Semantic Clarity Matters**
   - User insight: "Crew manifests should actually be user personas"
   - Resulted in: Proper separation of UARS vs Personas
   - Lesson: Clear names prevent mixed concerns

3. **Location Reflects Purpose**
   - User insight: "Santiago-pm artifacts are all things we need to build santiago-pm"
   - Resulted in: Domain-specific location strategy
   - Lesson: File location should reflect artifact purpose

---

## Metrics

**Time Investment**: ~4 hours
- Architecture design: 1 hour
- UARS creation: 1.5 hours
- Personas creation: 45 minutes
- GitHub agent prompts: 30 minutes
- Documentation: 15 minutes

**Files Created**: 31
**Lines Written**: 3,287

**Estimated Time Saved** (per coordination cycle):
- Before: 30-60 minutes per agent coordination (unclear roles, manual lookup)
- After: 5-10 minutes (clear UARS specs, reference-based)
- **Net Savings**: 20-50 minutes per coordination

**Break-even**: After ~5-10 coordination cycles (within 1-2 weeks)

---

## Conclusion

The UARS system establishes a foundation for structured agent coordination by providing:
1. **Clear role definitions** (purpose, responsibilities, authority)
2. **Reference-based architecture** (single source of truth)
3. **Semantic separation** (UARS vs personas vs prompts)
4. **Governance specifications** (approval gates, escalation rules)

This enables the next major milestone: **F-030 Team Workflow System**, where multiple agents coordinate autonomously using UARS specifications.

The reference-based approach respects knowledge graph principles while providing practical benefits:
- No duplication → no sync issues
- Single source → simpler maintenance
- Derived assets → automatic updates

Next: Use UARS to build the workflow orchestrator that coordinates all seven agents.

---

**Log Entry End**

*Logged by: Santiago-PM (Product Manager)*
*Date: 2025-01-16*
*Commit: 87bf100*
