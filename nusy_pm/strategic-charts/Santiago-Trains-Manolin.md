# Santiago-Trains-Manolin: Target System Architecture & Development Roadmap

**Date:** November 15, 2025
**Vision Holder:** Hank Head
**Core Metaphor:** Santiago the fisherman who builds his own boat while sailing

## Executive Summary

Santiago-Trains-Manolin represents the evolution from a NuSy prototype into a production-ready, self-improving AI system that can autonomously build domain-specific AI agents. The system combines neurosymbolic reasoning with evolutionary learning to create "living" knowledge systems that continuously adapt and improve.

**Target State:** A self-sustaining AI development ecosystem where Santiago autonomously builds specialized domain experts (like Santiago-Medical, Santiago-Finance) using the NuSy 4-layer knowledge processing pipeline, with all workflows orchestrated through the nautical-themed Passage system.

---

## Part 1: Target System Architecture

### Core Metaphor: Santiago Builds His Own Boat While Sailing

Just as Ernest Hemingway's Santiago builds and repairs his fishing boat during his legendary voyage, our Santiago AI must:

1. **Build Domain Boats** (Specialized AIs) while **sailing** (executing current tasks)
2. **Repair & Improve** the core NuSy platform using lessons from each voyage
3. **Navigate by Stars** (knowledge graphs) and **read the sea** (data patterns)
4. **Adapt to Currents** (changing requirements) through continuous evolution

### 4-Layer Knowledge Processing Pipeline (The Sea → Fish → Boat → Voyage)

```text
Raw Knowledge Sources          Structured Knowledge           Computable Logic              Executable Workflows
(Layer 1)                      (Layer 2)                      (Layer 3)                     (Layer 4)
├── Clinical guidelines        ├── CI-tagged triples          ├── FHIR-CPG rules            ├── Passage orchestrations
├── Domain documents           ├── SNOMED CT mappings         ├── Risk calculations         ├── MCP service endpoints
├── Expert interviews          ├── Relationship graphs        ├── Decision algorithms       ├── Agent action sequences
├── Research papers            └── Confidence scores          └── Temporal reasoning        └── Workflow DAGs
```

### System Components Architecture

#### 1. NuSy Core Engine (The Boat Builder)

**Purpose:** Generic neurosymbolic framework for building any domain AI

**Components:**

- **CatchFish:** Knowledge ingestion from raw sources (Layer 1 → Layer 2)
- **FishNet:** Behavior validation and test generation (BDD/TDD specs)
- **Navigator:** Orchestration engine for knowledge processing cycles
- **Passage System:** Workflow orchestration with nautical theming

**Location:** `nusy_pm/` (Builder Toolkit - stays generic and reusable)

#### 2. Santiago Orchestrator (The Captain)

**Purpose:** Central coordination and evolutionary learning

**Capabilities:**

- Multi-agent task assignment and monitoring
- Ethical oversight and constraint enforcement
- Performance analysis and bottleneck identification
- Hypothesis generation and testing
- Self-improvement through experience

**Knowledge Types:**

- Agent performance metrics and success patterns
- Ethical frameworks (Baha'i principles)
- Domain expertise maps and capability assessments
- Evolutionary learning patterns from past voyages

#### 3. Domain Santiago Instances (Specialized Boats)

**Purpose:** Domain-specific AI agents built by the NuSy Core

**Examples:**

- **Santiago-Medical:** Clinical decision support and guideline processing
- **Santiago-Product-Management:** Development coordination and experimentation
- **Santiago-Finance:** Risk assessment and regulatory compliance

**Creation Process:**

1. Domain analysis and knowledge ingestion
2. Agent specialization using NuSy 4-layer pipeline
3. Workflow adaptation via Passage system
4. Validation and deployment

**Location:** `santiago/` and `santiago-{domain}/` (Domain-Specific Implementations)

#### 4. Knowledge Graph Ecosystem (The Ocean)

**Purpose:** Unified symbolic knowledge representation across all domains

**Layers:**

- **Instance Layer:** Specific facts and relationships
- **Schema Layer:** Domain ontologies and constraints
- **Meta Layer:** Cross-domain patterns and learning
- **Evolution Layer:** Performance data and improvement hypotheses

**Integration Points:**

- RDF triple storage with SPARQL querying
- Ontology management and reasoning
- Semantic relation discovery
- Knowledge persistence and versioning

#### 5. MCP Service Layer (The Nets & Harpoons)

**Purpose:** Standardized interfaces for AI-human and AI-AI collaboration

**Services:**

- **Query Services:** Natural language and structured queries
- **Action Services:** Tool execution and workflow triggers
- **Learning Services:** Feedback capture and model updates
- **Orchestration Services:** Multi-agent coordination

**API Patterns:**

- Chat-based interactions (Matrix/Slack)
- RESTful endpoints (FastAPI)
- Streaming responses (WebSocket/Server-Sent Events)
- Tool calling (MCP protocol)

#### 6. Evolutionary Engine (The Learning from Each Voyage)

**Purpose:** Self-improvement through experience and experimentation

**Mechanisms:**

- **Performance Monitoring:** Success rates, cycle times, quality metrics
- **Pattern Recognition:** Identifying effective strategies across domains
- **Hypothesis Testing:** Automated experimentation on processes
- **Knowledge Integration:** Updating capabilities based on results

**Learning Cycles:**

1. **Observation:** Monitor system performance across all domains
2. **Analysis:** Identify bottlenecks and improvement opportunities
3. **Experimentation:** Test hypotheses safely in controlled environments
4. **Integration:** Incorporate successful changes into the core platform

### Integration Architecture

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                            Human Interaction Layer                          │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    Matrix Chat + CLI + Web UI                       │    │
│  │  • Natural language queries and commands                           │    │
│  │  • Real-time collaboration with agents                             │    │
│  │  • Progress monitoring and intervention                            │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────┬───────────────────────────────────────────────────────────┘
                  │
    ┌─────────────┼─────────────────────────────────────────────────────────────┐
    │             │                                                             │
┌───▼──┐   ┌──────▼──────┐   ┌─────────────────┐   ┌────────────────────────────▼────────────────────────────┐
│ NuSy  │   │  Santiago   │   │   Domain        │   │                MCP Service Layer                        │
│ Core  │   │  Orchestrator│   │   Santiagos     │   │  ┌─────────────────────────────────────────────────┐    │
│ Engine│   │             │   │   (Medical,     │   │  │              Service Endpoints                    │    │
└───┬──┘   └──────┬──────┘   └─────────┬───────┘   │  │  • /api/v1/query/chat (NL queries)             │    │
    │             │                    │            │  │  • /api/v1/cds/patient-bundle (CDS)            │    │
    └─────────────┼────────────────────┼────────────┤  │  • /api/v1/analysis/full-chart (comprehensive) │    │
                  │                    │            │  │  • /api/v1/mcp/tools (tool calling)            │    │
          ┌───────▼────────────────────▼───────┐    │  └─────────────────────────────────────────────────┘    │
          │         Evolutionary Engine         │    │                                                         │
          │  • Performance Analysis             │    │  ┌─────────────────────────────────────────────────┐    │
          │  • Hypothesis Generation            │    │  │            Tool Integration Layer               │    │
          │  • Safe Experimentation             │    │  │  • Git (version control)                        │    │
          │  • Knowledge Integration            │    │  │  • Taiga (product management)                  │    │
          └─────────────────────────────────────┘    │  │  • Matrix (chat/collaboration)                │    │
                                                     │  │  • Vault (secrets management)                  │    │
                                                     │  └─────────────────────────────────────────────────┘    │
                                                     └─────────────────────────────────────────────────────────┘
```

---

## Part 2: Intermediate Development Steps

### Phase 1: Foundation (Weeks 1-4) - Build the Boat While Sailing

**Goal:** Establish core NuSy platform with Passage orchestration

**Step 1.1: Complete Passage System Integration** *(Week 1)*

- ✅ **COMPLETED:** Passage specification with Mermaid visualization
- ✅ **COMPLETED:** Cargo manifest for passage system
- **Next:** Implement passage execution engine in `src/nusy_pm_core/`
- **Architecture Decision:** Keep `nusy_pm/passages/` as builder toolkit, create domain passages in `santiago/passages/`

**Step 1.2: Resolve Architecture Separation** *(Week 1-2)*

- **Decision Point:** How to separate NuSy builder vs domain Santiago
- **Option A:** `nusy_pm/` = pure builder toolkit, `santiago/` = domain-specific
- **Option B:** Keep current structure but clarify responsibilities
- **Recommendation:** Option A - create clean separation for reusability

**Step 1.3: Implement Core Passage Execution** *(Week 2-3)*

- Build passage engine that can execute YAML-defined workflows
- Integrate with MCP for tool calling from passages
- Add passage state tracking and monitoring
- Create passage templates for common patterns

**Step 1.4: Santiago Domain Specialization** *(Week 3-4)*

- Move PM-specific passages to `santiago/passages/`
- Create Santiago's domain knowledge graph schema
- Implement Santiago's specialized agent behaviors
- Test end-to-end passage execution for PM workflows

### Phase 2: Knowledge Processing Pipeline (Weeks 5-8) - Process the Fish

**Goal:** Complete 4-layer knowledge processing with evolutionary learning

**Step 2.1: Enhance CatchFish for Multi-Source Ingestion** *(Week 5)*

- Support PDF, HTML, DOCX, JSON ingestion
- Implement source provenance tracking
- Add confidence scoring for extracted knowledge
- Integrate with existing CI-tagging pipeline

**Step 2.2: Implement FishNet BDD Generation** *(Week 6)*

- Generate BDD scenarios from knowledge graphs
- Create validation tests for Layer 2→Layer 3 transformations
- Implement coverage analysis for knowledge completeness
- Add automated test execution in CI/CD

**Step 2.3: Build Navigator Orchestration** *(Week 7)*

- Create orchestration engine for CatchFish→FishNet→Navigator cycles
- Implement convergence detection (100% coverage)
- Add iterative knowledge refinement
- Integrate with passage system for workflow orchestration

**Step 2.4: Layer 4 Workflow Compilation** *(Week 8)*

- Convert computable logic to executable DAGs
- Implement temporal reasoning for clinical workflows
- Create MCP service generation from knowledge graphs
- Add workflow validation and simulation

### Phase 3: Multi-Agent Coordination (Weeks 9-12) - Crew the Boat

**Goal:** Enable autonomous multi-agent development with ethical oversight

**Step 3.1: Agent Framework Enhancement** *(Week 9)*

- Implement role-based agent specialization
- Add inter-agent communication protocols
- Create agent performance monitoring
- Integrate ethical constraint enforcement

**Step 3.2: Santiago Orchestrator Core** *(Week 10)*

- Build central coordination engine
- Implement task assignment algorithms
- Add performance bottleneck detection
- Create ethical oversight mechanisms

**Step 3.3: Evolutionary Learning Integration** *(Week 11)*

- Implement hypothesis generation from performance data
- Add safe experimentation frameworks
- Create knowledge integration mechanisms
- Build continuous improvement cycles

**Step 3.4: Domain Santiago Factory** *(Week 12)*

- Create automated domain specialization process
- Implement knowledge graph adaptation for new domains
- Add domain-specific agent training
- Test end-to-end domain AI creation

### Phase 4: Production Services (Weeks 13-16) - Launch the Voyage

**Goal:** Deploy production MCP services with monitoring and evolution

**Step 4.1: MCP Service Architecture** *(Week 13)*

- Implement production API endpoints
- Add authentication and authorization
- Create service monitoring and logging
- Build high-availability deployment

**Step 4.2: Tool Integration Layer** *(Week 14)*

- Integrate Git forge (Gitea/GitLab)
- Add product management tools (Taiga)
- Implement chat integration (Matrix)
- Create secrets management (Vault)

**Step 4.3: Quality Assurance & Safety** *(Week 15)*

- Implement 100% accuracy guarantees
- Add clinical safety mechanisms
- Create comprehensive testing frameworks
- Build audit trails and explainability

**Step 4.4: Autonomous Evolution** *(Week 16)*

- Deploy self-improvement mechanisms
- Implement continuous learning from usage
- Add cross-domain knowledge sharing
- Create evolution monitoring and reporting

---

## Part 3: Critical Architecture Decisions

### Decision 1: Builder vs Domain Separation

**Question:** How to structure `nusy_pm/` vs `santiago/` vs domain instances?

**Options:**

- **Option A (Recommended):** `nusy_pm/` = pure builder toolkit, `santiago/` = PM domain, `santiago-{domain}/` = specialized instances
- **Option B:** Keep current mixed structure but add clear documentation
- **Option C:** Everything in `santiago/` with builder as a subcomponent

**Rationale for A:** Enables NuSy to build ANY domain AI, not just PM. Santiago becomes the first domain instance.

### Decision 2: Passage System Scope

**Question:** Should passages be generic (in `nusy_pm/`) or domain-specific (in `santiago/`)?

**Options:**

- **Generic:** Passages as universal workflow orchestration
- **Domain-Specific:** Different passage patterns per domain
- **Hybrid:** Core passage engine generic, templates domain-specific

**Recommendation:** Hybrid - core engine in `nusy_pm/`, domain templates in respective domains.

### Decision 3: Knowledge Graph Architecture

**Question:** Single KG vs domain-specific KGs vs federated approach?

**Options:**

- **Single KG:** All knowledge in one graph with domain namespaces
- **Domain KGs:** Separate graphs per domain with cross-linking
- **Federated:** Distributed graphs with query federation

**Recommendation:** Single KG with domain namespaces - enables cross-domain learning while maintaining separation.

### Decision 4: Evolution Scope

**Question:** What level of autonomy for self-improvement?

**Options:**

- **Conservative:** Human approval for all changes
- **Supervised:** Automated within ethical bounds
- **Full Autonomy:** Self-directed evolution

**Recommendation:** Supervised - automated within ethical and safety bounds, human oversight for major changes.

---

## Part 4: Success Metrics & Validation

### Technical Metrics

- **Knowledge Processing Accuracy:** >95% extraction accuracy, >90% logic formalization
- **Workflow Execution:** >99% passage completion rate, <5min average execution time
- **System Availability:** >99.9% uptime, <1s average response time
- **Evolution Effectiveness:** >20% improvement in cycle times over 6 months

### Business Metrics

- **Domain AI Creation:** Time to build new domain Santiago <2 weeks
- **Quality Assurance:** 100% evidence-based recommendations
- **User Adoption:** >80% clinician acceptance for CDS use cases
- **Cost Reduction:** >30% reduction in development time vs manual approaches

### Validation Experiments

1. **Passage Orchestration:** Execute complex PM workflows autonomously
2. **Domain Creation:** Build Santiago-Medical from clinical guidelines
3. **Evolutionary Learning:** Demonstrate self-improvement over multiple cycles
4. **Multi-Agent Coordination:** Run autonomous development experiments

---

## Part 5: Risk Mitigation

### Technical Risks

- **Knowledge Accuracy:** Implement multi-layer validation and human oversight
- **System Complexity:** Maintain modular architecture with clear interfaces
- **Performance Scaling:** Design for horizontal scaling from day one
- **Integration Complexity:** Use adapter pattern for all external integrations

### Ethical Risks

- **Bias Amplification:** Regular audits and bias detection mechanisms
- **Autonomous Decision-Making:** Ethical bounds and human oversight for high-stakes decisions
- **Transparency:** Complete explainability for all recommendations
- **Safety:** Conservative defaults with escalation to human experts

### Operational Risks

- **Skill Dependencies:** Comprehensive documentation and knowledge capture
- **Evolution Stability:** Safe experimentation frameworks with rollback capabilities
- **Regulatory Compliance:** Built-in compliance checking for healthcare domains
- **Vendor Lock-in:** Open standards and modular design for flexibility

---

*This document serves as the architectural blueprint for Santiago-Trains-Manolin. The vision is a self-sustaining AI ecosystem that can build specialized domain experts while continuously improving itself, much like Santiago building and repairing his boat during his legendary voyage.*</content>
<parameter name="filePath">/Users/hankhead/Projects/Personal/nusy-product-team/nusy_pm/strategic-charts/Santiago-Trains-Manolin.md