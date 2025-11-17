# Feature: Unified Agent Role Specification (UARS)

```yaml
---
artifact_type: cargo-manifest
feature_id: F-031
feature_name: unified-agent-role-specification
priority: 0.80 (HIGH)
status: discovery
created: 2025-11-17
created_by: Hank
source: Discussion about crew manifest evolution and MCP manifest convergence
related_features:
  - F-030 (PR/Issue Workflow Management - defines agent work patterns)
  - F-027 (Personal Log Feature - agents document their work)
  - F-029 (Continuous Discovery - finds capability gaps)
  - Navigator (orchestration needs role clarity)
  - Fishnet (generates tests based on capabilities)
kerievsky_principles:
  - "Make Work Visible" (explicit roles, responsibilities, capabilities)
  - "Deliver Value Continuously" (agents know their scope)
  - "Experiment & Learn Rapidly" (agents evolve capabilities)
system_component: santiago-core (affects all Santiago agents)
---
```

---

## Feature Overview

**Problem**: We have two disconnected manifest systems:
- **Crew Manifests** (santiago_core/crew-manifests/): Human-readable role descriptions
  - Purpose, responsibilities, behavioral guidelines
  - Rank, specialization, scope of authority
  - But NO executable specification
  
- **MCP Manifests** (knowledge/catches/*/mcp-manifest.json): Machine-executable tool definitions
  - Tools, parameters, return types
  - Capability level, knowledge scope
  - But NO role context or responsibilities

**Gap**: When a new Santiago agent is created:
1. We write a crew manifest (who are you? what do you do?)
2. We write an MCP manifest (what tools do you expose?)
3. **These drift apart** - no single source of truth
4. Unclear: What's the agent's **scope of authority**? When should it **escalate**?
5. Hard to validate: Does this agent have the **right tools** for its **stated role**?

**Key Insight**: Crew manifests are the **embryo** of MCP manifests. They define:
- Role → MCP service_name
- Core capabilities → MCP tools
- Specialization → MCP capability_level + knowledge_scope
- Scope of authority → Which tools require approval/escalation
- Integration points → Which other MCP services this agent calls

**Unified Agent Role Specification (UARS)** should be the **single source** that:
1. Defines the agent's role and responsibilities (human-readable)
2. Specifies the agent's tools and capabilities (machine-executable)
3. Maps role responsibilities → MCP tools (traceability)
4. Includes governance (scope of authority, escalation rules)
5. Supports evolution (agents gain capabilities over time)

---

## User Stories

### Story 1: Define Agent Role with Executable Capabilities (MVP)

**As Santiago-PM**
**I want to define a new agent role with both human-readable responsibilities AND machine-executable tools**
**So that the role specification is the single source of truth**

**Given** I need to create a new Santiago agent for a specific domain:
```yaml
new_agent:
  domain: "code-review"
  purpose: "Automated code quality checks and architectural guidance"
  rank: "journeyman"  # Can handle standard reviews, escalates complex cases
  specialization: "python-typescript-architecture"
```

**When** I create a Unified Agent Role Specification

**Then** the system should generate:

1. **Role Definition** (Human-readable):
```yaml
agent_id: santiago-code-reviewer
role: Code Review Agent
rank: journeyman
specialization: python-typescript-architecture
purpose: |
  Automated code quality checks, architectural pattern validation,
  and best practice enforcement for Python and TypeScript codebases.

responsibilities:
  primary:
    - Review code changes for quality and standards compliance
    - Validate architectural patterns match project conventions
    - Suggest improvements for maintainability
    - Flag security vulnerabilities and anti-patterns
  
  secondary:
    - Document review decisions and rationale
    - Learn from accepted/rejected suggestions
    - Contribute to coding standards knowledge base

scope_of_authority:
  can_approve:
    - Style fixes (formatting, naming conventions)
    - Documentation improvements
    - Test additions (no logic changes)
  
  must_escalate:
    - Breaking API changes
    - Security-critical code
    - Major architectural decisions
    - Performance-critical paths

escalation_criteria:
    - complexity_score > 8/10
    - affects_multiple_modules: true
    - security_implications: true
    - breaks_existing_tests: true
```

2. **Capability Specification** (Machine-executable):
```yaml
mcp_service:
  service_name: santiago-code-reviewer
  version: 1.0.0
  capability_level: journeyman  # From rank
  knowledge_scope: lake  # Bounded to codebase, not cross-domain

tools:
  # Mapped from responsibilities
  - name: review_pull_request
    responsibility_link: "Review code changes for quality"
    description: "Analyze code changes and provide structured feedback"
    tool_type: "input-output"
    parameters:
      pr_number: integer
      focus_areas: array<string>  # ["style", "architecture", "security"]
    returns:
      review_result: object
      approval_decision: enum[APPROVE, REQUEST_CHANGES, ESCALATE]
      rationale: string
    concurrency_risk: false
    mutates_kg: true  # Records review in knowledge graph
    requires_approval: false  # Can run autonomously
    
  - name: validate_architecture_patterns
    responsibility_link: "Validate architectural patterns"
    description: "Check if code follows project architecture conventions"
    tool_type: "input"
    parameters:
      file_paths: array<string>
      patterns_to_check: array<string>
    returns:
      validation_result: object
      violations: array<object>
      suggestions: array<object>
    concurrency_risk: false
    mutates_kg: false
    requires_approval: false
    
  - name: escalate_for_human_review
    responsibility_link: "Must escalate (scope of authority)"
    description: "Escalate complex/security-critical code to human reviewer"
    tool_type: "output"
    parameters:
      pr_number: integer
      escalation_reason: string
      complexity_score: float
      risk_factors: array<string>
    returns:
      escalation_ticket: object
    concurrency_risk: false
    mutates_kg: true
    requires_approval: false  # Escalation itself doesn't need approval

behavioral_constraints:
  communication_style: "Professional, constructive, evidence-based"
  decision_criteria:
    - "Code quality standards defined in project"
    - "Security best practices (OWASP, etc.)"
    - "Performance implications documented"
  ethical_framework:
    - "Never approve code with known security vulnerabilities"
    - "Always explain rationale for rejections"
    - "Escalate when uncertain rather than block"

governance:
  approval_required_for:
    - Approving PRs that modify core architecture
    - Suggesting major refactorings
    - Changing project-wide standards
  
  auto_escalate_if:
    - complexity_score > 8
    - security_critical_path: true
    - affects_api_contract: true
    - test_coverage_drops_below: 80%
```

**Acceptance Criteria**:
- [ ] Single YAML file defines both role and capabilities
- [ ] Role responsibilities map to MCP tools (traceability)
- [ ] Scope of authority explicit (can approve vs must escalate)
- [ ] Governance rules enforceable (auto-escalate conditions)
- [ ] Can generate MCP manifest JSON from UARS YAML

---

### Story 2: Validate Tool Coverage for Role Responsibilities

**As Santiago-PM**
**I want to validate that an agent's tools fully cover its stated responsibilities**
**So that role definitions don't drift from actual capabilities**

**Given** an agent with defined responsibilities:
```yaml
responsibilities:
  primary:
    - "Review code changes for quality and standards compliance"
    - "Validate architectural patterns match project conventions"
    - "Suggest improvements for maintainability"
  
  tools:
    - review_pull_request  # Covers responsibility 1
    - validate_architecture_patterns  # Covers responsibility 2
    # Missing: Tool for responsibility 3 (suggest improvements)
```

**When** I run capability coverage analysis

**Then** the system should report:
```yaml
coverage_analysis:
  status: INCOMPLETE
  coverage_percentage: 66.7  # 2 of 3 responsibilities covered
  
  gaps:
    - responsibility: "Suggest improvements for maintainability"
      mapped_tools: []
      recommendation: "Add tool: suggest_code_improvements"
  
  overlaps:
    - tools: ["review_pull_request", "validate_architecture_patterns"]
      both_cover: "Code quality analysis"
      recommendation: "Consider consolidating or clarifying distinction"
```

**Acceptance Criteria**:
- [ ] Can analyze responsibility → tool mapping
- [ ] Reports gaps (responsibilities without tools)
- [ ] Reports overlaps (tools covering same responsibility)
- [ ] Suggests missing tools based on responsibility text
- [ ] Validates tool parameters match responsibility requirements

---

### Story 3: Agent Capability Evolution Tracking

**As Santiago-PM**
**I want to track how agent capabilities evolve over time**
**So that I understand agent maturity progression**

**Given** an agent that has been operational for 6 months:
```yaml
capability_timeline:
  v1.0.0 (2025-11-01):
    rank: apprentice
    tools: ["review_pull_request", "escalate_for_human_review"]
    scope_of_authority: "Must escalate all non-trivial PRs"
    approval_required: true
  
  v1.5.0 (2025-12-15):
    rank: journeyman
    tools: ["review_pull_request", "validate_architecture_patterns", "escalate_for_human_review"]
    scope_of_authority: "Can approve style/doc changes, escalate architecture"
    approval_required: false  # Gained autonomy
  
  v2.0.0 (2026-01-30):
    rank: journeyman
    tools: ["review_pull_request", "validate_architecture_patterns", "suggest_code_improvements", "escalate_for_human_review"]
    scope_of_authority: "Can approve most PRs, escalate security/performance"
    approval_required: false
```

**When** I query agent capability evolution

**Then** the system should show:
```yaml
evolution_summary:
  agent_id: santiago-code-reviewer
  time_in_service: 90 days
  
  progression:
    - date: 2025-12-15
      event: "Promoted to Journeyman"
      reason: "85% approval rate, 95% human agreement on escalations"
      tools_added: ["validate_architecture_patterns"]
      authority_expanded: "Can now approve style/doc changes without human approval"
    
    - date: 2026-01-30
      event: "Tool Addition"
      reason: "High demand for improvement suggestions (200 requests)"
      tools_added: ["suggest_code_improvements"]
  
  learning_metrics:
    human_agreement_rate: 0.92  # How often humans agree with agent decisions
    escalation_precision: 0.88  # How often escalations were necessary
    false_positive_rate: 0.05  # How often agent blocked valid code
    tool_usage:
      review_pull_request: 1500 invocations
      validate_architecture_patterns: 800 invocations
      suggest_code_improvements: 200 invocations
      escalate_for_human_review: 120 invocations
```

**Acceptance Criteria**:
- [ ] Track all UARS versions with timestamps
- [ ] Link version changes to triggering events (metrics, feedback)
- [ ] Show tool addition/removal history
- [ ] Track scope of authority expansions
- [ ] Calculate maturity metrics (human agreement, escalation precision)

---

### Story 4: Generate MCP Manifest from UARS

**As a Developer**
**I want to generate a deployable MCP manifest from a UARS definition**
**So that the MCP server matches the role specification**

**Given** a complete UARS file:
```yaml
# uars-santiago-code-reviewer.yaml
agent_id: santiago-code-reviewer
role: Code Review Agent
rank: journeyman
# ... (full UARS as in Story 1)
```

**When** I run the UARS compiler:
```bash
python -m santiago_core.uars.compiler \
  --input uars-santiago-code-reviewer.yaml \
  --output mcp-manifest.json \
  --format mcp-manifest
```

**Then** the system should generate:
```json
{
  "service_name": "santiago-code-reviewer",
  "version": "1.0.0",
  "description": "Automated code quality checks and architectural guidance for Python and TypeScript codebases",
  "capability_level": "journeyman",
  "knowledge_scope": "lake",
  "tools": [
    {
      "name": "review_pull_request",
      "description": "Analyze code changes and provide structured feedback",
      "tool_type": "input-output",
      "parameters": {
        "pr_number": "integer",
        "focus_areas": "array"
      },
      "returns": {
        "review_result": "object",
        "approval_decision": "string",
        "rationale": "string"
      },
      "concurrency_risk": false,
      "mutates_kg": true,
      "metadata": {
        "responsibility_link": "Review code changes for quality",
        "requires_approval": false,
        "escalation_conditions": [
          "complexity_score > 8",
          "security_critical_path"
        ]
      }
    }
    // ... other tools
  ],
  "governance": {
    "scope_of_authority": {
      "can_approve": ["style_fixes", "documentation", "test_additions"],
      "must_escalate": ["breaking_changes", "security_critical", "architecture_decisions"]
    },
    "auto_escalate_conditions": {
      "complexity_threshold": 8,
      "security_critical": true,
      "api_contract_change": true,
      "test_coverage_drop_below": 0.8
    }
  },
  "metadata": {
    "generated_from": "uars-santiago-code-reviewer.yaml",
    "generated_at": "2025-11-17T12:00:00Z",
    "uars_version": "1.0.0"
  }
}
```

**Acceptance Criteria**:
- [ ] UARS compiler generates valid MCP manifest JSON
- [ ] All tools from UARS included with correct signatures
- [ ] Governance rules translated to metadata
- [ ] Can round-trip: UARS → MCP manifest → validation
- [ ] Compiler validates UARS completeness before generation

---

### Story 5: Multi-Agent Coordination from Role Specifications

**As Navigator**
**I want to query agent role specifications to coordinate multi-agent workflows**
**So that I can assign work to agents based on their responsibilities and authority**

**Given** a complex task requiring multiple agents:
```yaml
task:
  name: "Review and merge PR #123 (new authentication system)"
  complexity: HIGH
  security_critical: true
  modules_affected: ["auth", "api", "database"]
```

**When** Navigator queries agent capabilities

**Then** the system should recommend workflow:
```yaml
workflow_plan:
  agents_required:
    - agent: santiago-code-reviewer
      role: "Initial code quality review"
      can_complete_independently: false
      reason: "Security-critical changes exceed scope of authority"
      escalation_required: true
    
    - agent: santiago-security-reviewer
      role: "Security-focused review"
      can_complete_independently: true
      reason: "Specialization: security-critical-systems, rank: senior"
      escalation_required: false
    
    - agent: santiago-architect
      role: "Architectural impact assessment"
      can_complete_independently: true
      reason: "Authentication system affects multiple modules"
      escalation_required: false
  
  coordination_sequence:
    1:
      agent: santiago-code-reviewer
      action: "review_pull_request"
      expected_outcome: "ESCALATE (security-critical)"
    
    2:
      agent: santiago-security-reviewer
      action: "security_audit_pr"
      depends_on: [1]
      expected_outcome: "APPROVE or REQUEST_CHANGES"
    
    3:
      agent: santiago-architect
      action: "assess_architectural_impact"
      depends_on: [1]
      parallel_with: [2]
      expected_outcome: "APPROVE or REQUEST_CHANGES"
    
    4:
      condition: "All reviews APPROVED"
      action: "merge_pull_request"
      requires_human: true  # Final merge of security-critical code
```

**Acceptance Criteria**:
- [ ] Can query agent capabilities by responsibility
- [ ] Matches task requirements to agent scope of authority
- [ ] Identifies when escalation is required
- [ ] Recommends coordination sequence (serial vs parallel)
- [ ] Validates that agent set has complete coverage for task

---

## Technical Architecture

### UARS Schema (YAML)

```yaml
# Unified Agent Role Specification
schema_version: 1.0.0
agent_id: string  # Unique identifier
role: string  # Human-readable role title
rank: enum[apprentice, journeyman, senior, master, captain]
specialization: string  # Domain expertise
status: enum[active, standby, development, retired]

# Human-readable role definition
role_definition:
  purpose: string  # Why this agent exists
  responsibilities:
    primary: array<string>  # Core duties
    secondary: array<string>  # Additional duties
  
  scope_of_authority:
    can_decide_independently: array<string>
    requires_approval: array<string>
    must_escalate: array<string>
  
  escalation_criteria:
    conditions: array<object>  # When to escalate
    thresholds: object  # Numeric thresholds
  
  behavioral_constraints:
    communication_style: string
    decision_criteria: array<string>
    ethical_framework: array<string>

# Machine-executable capability specification  
capability_specification:
  mcp_service:
    service_name: string
    version: string
    capability_level: enum[apprentice, journeyman, master, expert]
    knowledge_scope: enum[pond, lake, sea, ocean]
  
  tools:
    - name: string
      responsibility_link: string  # Maps to role_definition.responsibilities
      description: string
      tool_type: enum[input, output, communication, input-output]
      parameters: object
      returns: object
      concurrency_risk: boolean
      mutates_kg: boolean
      requires_approval: boolean
      escalation_conditions: array<string>
  
  behavioral_implementation:
    communication_patterns: object
    decision_algorithms: object
    ethical_guardrails: object

# Governance and evolution
governance:
  approval_gates:
    tool_invocations: array<string>  # Which tools need approval
    conditions: array<object>  # When to require approval
  
  auto_escalate_rules:
    - condition: string
      trigger: object
      escalate_to: string

evolution:
  version_history:
    - version: string
      date: iso8601
      changes: string
      reason: string
      metrics: object
  
  maturity_metrics:
    human_agreement_rate: float
    escalation_precision: float
    false_positive_rate: float
    tool_usage_stats: object

# Integration
integration:
  collaborates_with:
    - agent_id: string
      nature_of_collaboration: string
      shared_tools: array<string>
  
  knowledge_graph_integration:
    contributes: array<string>  # What KG nodes this agent creates
    queries: array<string>  # What KG patterns this agent reads
  
  dependencies:
    required_services: array<string>
    optional_services: array<string>

metadata:
  created_at: iso8601
  updated_at: iso8601
  created_by: string
  tags: array<string>
  related_experiments: array<string>
  related_artifacts: array<string>
```

### System Components

```
santiago-core/
  uars/  # NEW - Unified Agent Role Specifications
    __init__.py
    schema.py           # UARS schema validation
    compiler.py         # UARS → MCP manifest
    validator.py        # Validate responsibility-tool coverage
    evolution.py        # Track capability progression
    governance.py       # Enforce escalation rules
    
    specifications/     # UARS files for all agents
      santiago-pm.yaml
      santiago-architect.yaml
      santiago-code-reviewer.yaml
      santiago-security-reviewer.yaml
      # ... one per agent
    
    README.md           # UARS documentation
  
  crew-manifests/       # DEPRECATED - replaced by UARS
    # Keep for backward compatibility initially
  
  mcp-manifests/        # GENERATED from UARS
    # Auto-generated, do not edit manually
```

### UARS Compiler

```python
# santiago_core/uars/compiler.py
from pathlib import Path
from typing import Dict, Any
import yaml
import json

class UARSCompiler:
    """Compile UARS YAML to deployable formats"""
    
    def compile_to_mcp_manifest(
        self,
        uars_file: Path
    ) -> Dict[str, Any]:
        """
        Generate MCP manifest JSON from UARS YAML.
        
        Transformations:
        - role_definition → metadata
        - capability_specification.tools → tools array
        - governance → tools[].metadata
        - behavioral_constraints → service metadata
        """
        uars = yaml.safe_load(uars_file.read_text())
        
        mcp_manifest = {
            "service_name": uars["agent_id"],
            "version": uars["capability_specification"]["mcp_service"]["version"],
            "description": uars["role_definition"]["purpose"],
            "capability_level": uars["capability_specification"]["mcp_service"]["capability_level"],
            "knowledge_scope": uars["capability_specification"]["mcp_service"]["knowledge_scope"],
            "tools": self._compile_tools(uars),
            "governance": self._compile_governance(uars),
            "metadata": {
                "generated_from": str(uars_file),
                "generated_at": datetime.now().isoformat(),
                "uars_version": uars["schema_version"],
                "role": uars["role"],
                "rank": uars["rank"],
                "specialization": uars["specialization"]
            }
        }
        
        return mcp_manifest
    
    def _compile_tools(self, uars: Dict) -> list:
        """Transform UARS tools to MCP tool format"""
        tools = []
        for tool in uars["capability_specification"]["tools"]:
            mcp_tool = {
                "name": tool["name"],
                "description": tool["description"],
                "tool_type": tool["tool_type"],
                "parameters": tool["parameters"],
                "returns": tool["returns"],
                "concurrency_risk": tool["concurrency_risk"],
                "mutates_kg": tool["mutates_kg"],
                "metadata": {
                    "responsibility_link": tool["responsibility_link"],
                    "requires_approval": tool["requires_approval"],
                    "escalation_conditions": tool.get("escalation_conditions", [])
                }
            }
            tools.append(mcp_tool)
        return tools
    
    def _compile_governance(self, uars: Dict) -> Dict:
        """Extract governance rules for MCP metadata"""
        return {
            "scope_of_authority": uars["role_definition"]["scope_of_authority"],
            "auto_escalate_conditions": uars["governance"]["auto_escalate_rules"]
        }
```

---

## Integration Points

### With F-030 (PR/Issue Workflow)
- **Agent work completion**: UARS defines which tools agent can use autonomously
- **Escalation triggers**: UARS governance rules trigger human review
- **Role context in PRs**: PR includes agent's role and authority for reviewer

### With F-027 (Personal Logs)
- **Session logs reference role**: "As santiago-code-reviewer (journeyman)"
- **Capability evolution tracked**: Logs show when agent gained new tools
- **Decision rationale**: Logs explain why agent escalated vs approved

### With F-029 (Continuous Discovery)
- **Capability gaps discovered**: Scanner finds responsibilities without tools
- **New tool suggestions**: Discovers patterns suggesting new capabilities
- **Agent maturity tracking**: Monitors tool usage to suggest promotions

### With Navigator
- **Task-agent matching**: Navigator queries UARS to assign work
- **Coordination planning**: Uses scope of authority to plan workflows
- **Escalation routing**: Knows which agent to escalate to

### With Fishnet
- **Test generation from responsibilities**: BDD scenarios for each responsibility
- **Tool contract testing**: Validates tool signatures match UARS
- **Governance testing**: Tests that escalation rules are enforced

---

## Implementation Phases

### Phase 1: UARS Schema and Compiler (MVP)
**Time Estimate**: 8-10 hours

**Deliverables**:
- [ ] UARS YAML schema definition
- [ ] Schema validator (check completeness, consistency)
- [ ] UARS → MCP manifest compiler
- [ ] Create UARS for santiago-pm (reference implementation)
- [ ] Unit tests for compiler

**Success Criteria**:
- Can define agent role in single UARS YAML file
- Compiler generates valid MCP manifest
- Santiago-PM UARS covers all existing MCP tools

### Phase 2: Responsibility-Tool Coverage Validation
**Time Estimate**: 5-6 hours

**Deliverables**:
- [ ] Coverage analyzer (responsibility → tool mapping)
- [ ] Gap detection (responsibilities without tools)
- [ ] Overlap detection (redundant tools)
- [ ] Recommendation engine (suggest missing tools)

**Success Criteria**:
- Reports coverage percentage for agent
- Identifies gaps and suggests fixes
- Validates all santiago-pm responsibilities are covered

### Phase 3: Capability Evolution Tracking
**Time Estimate**: 6-8 hours

**Deliverables**:
- [ ] Version history in UARS
- [ ] Evolution metrics calculation
- [ ] Maturity progression tracking
- [ ] Promotion recommendation engine

**Success Criteria**:
- Track agent capability changes over time
- Calculate human agreement rate, escalation precision
- Recommend rank promotions based on metrics

### Phase 4: Multi-Agent Coordination
**Time Estimate**: 8-10 hours

**Deliverables**:
- [ ] Navigator UARS query interface
- [ ] Task-agent matching algorithm
- [ ] Workflow planning from UARS
- [ ] Escalation routing logic

**Success Criteria**:
- Navigator assigns tasks based on UARS
- Plans multi-agent coordination sequences
- Respects scope of authority boundaries

---

## Success Metrics

### UARS Adoption
- **Target**: 100% of Santiago agents have UARS
- **Baseline**: 0% (currently crew manifests only)
- **Measurement**: Count UARS files vs active agents

### Responsibility Coverage
- **Target**: 95% of responsibilities have mapped tools
- **Baseline**: Unknown (need to audit)
- **Measurement**: Coverage analyzer reports

### Drift Prevention
- **Target**: <5% drift between UARS and actual MCP manifest
- **Baseline**: Unknown (manual MCP manifests drift)
- **Measurement**: Diff UARS-generated vs deployed manifests

### Escalation Precision
- **Target**: >85% of escalations were necessary
- **Baseline**: Unknown (no tracking currently)
- **Measurement**: Human review of escalated cases

---

## Risks and Mitigations

### Risk 1: UARS too complex to maintain
**Likelihood**: Medium
**Impact**: High
**Mitigation**: 
- Start with minimal schema (Phase 1)
- Add complexity only when needed
- Provide UARS templates and examples
- Build tooling to simplify editing (VS Code extension?)

### Risk 2: Existing crew manifests/MCP manifests out of sync
**Likelihood**: High
**Impact**: Medium
**Mitigation**:
- Migration tool: crew manifest + MCP manifest → UARS
- Gradual migration (one agent at a time)
- Keep crew manifests initially for reference
- Document migration process

### Risk 3: Governance rules too rigid
**Likelihood**: Medium
**Impact**: Medium
**Mitigation**:
- Make escalation conditions configurable
- Allow override with justification
- Track override frequency to tune rules
- Human can always override agent decision

---

## Questions for User Consultation

### Q1 (HIGH PRIORITY): Schema granularity?
**Options**:
- A) Minimal schema (role, tools, governance only)
- B) Comprehensive schema (includes all crew manifest fields)
- C) Extensible schema (core + plugins for specialized agents)

**Recommendation**: C (Extensible) - start minimal, allow domain-specific extensions

### Q2 (MEDIUM): Migration strategy?
**Options**:
- A) Big bang (convert all agents at once)
- B) Gradual (one agent per sprint)
- C) Hybrid (new agents use UARS, old agents migrate as needed)

**Recommendation**: C (Hybrid) - new agents UARS-first, migrate critical agents gradually

### Q3 (MEDIUM): UARS storage location?
**Options**:
- A) santiago_core/uars/ (system-level)
- B) santiago-pm/uars/ (pm-owned)
- C) Distributed (each agent repo has its own UARS)

**Recommendation**: A (santiago_core) - central authority for all agent specifications

### Q4 (LOW): YAML vs JSON for UARS?
**Options**:
- A) YAML (human-friendly, comments)
- B) JSON (machine-friendly, strict)
- C) Both (YAML source, JSON compiled)

**Recommendation**: C (Both) - YAML for editing, JSON for deployment

---

## Related Work

**Standards to consider**:
- MCP Protocol specification (tools, capabilities)
- OpenAPI (API contract specifications)
- Kubernetes Pod/Service specs (resource limits, health checks)
- Docker Compose (service orchestration)

**Similar systems**:
- Kubernetes RBAC (role-based access control)
- AWS IAM roles (permissions and policies)
- GitHub Actions (workflow definitions)

---

## Next Steps

1. **Validate concept**: Review UARS schema with team
2. **Build MVP**: Implement Phase 1 (schema, compiler, santiago-pm UARS)
3. **Test with real agent**: Convert santiago-pm crew manifest → UARS
4. **Iterate on schema**: Adjust based on real-world usage
5. **Expand to other agents**: Create UARS for santiago-architect, navigator, etc.

---

## Appendix: Example UARS (santiago-pm)

See next comment for full santiago-pm UARS specification.
