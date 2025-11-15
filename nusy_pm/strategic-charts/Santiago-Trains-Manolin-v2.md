# Santiago-Trains-Manolin v2: Updated System Architecture & Development Roadmap

**Date:** November 15, 2025
**Vision Holder:** Hank Head
**Core Metaphor:** Santiago the fisherman who builds his own boat while sailing
**Version:** v2 - Incorporated user feedback and clarified Santiago hierarchy

## Executive Summary

Santiago-Trains-Manolin v2 represents the clarified evolution from a NuSy prototype into a production-ready, self-improving AI system that can autonomously build domain-specific AI agents. The system combines neurosymbolic reasoning with evolutionary learning to create "living" knowledge systems that continuously adapt and improve.

**Target State:** A self-sustaining AI ecosystem where **Santiago (the core NuSy AI)** autonomously builds specialized domain experts like **Santiago-PM (product management)**, **Santiago-Medical (healthcare)**, and others, with all workflows orchestrated through the nautical-themed Passage system.

**Key Clarifications from v1:**
- **Santiago** = Core NuSy AI system (the boat builder)
- **santiago-pm** = Product management domain AI (what we're building in current `nusy_pm/`)
- **santiago-core/** = Separate directory for the core Santiago system
- **MVP Team:** Start with 3 core roles, expand to 7+ as system matures
- **Ethical oversight** built into every agent from the beginning

---

## Part 1: Updated System Architecture

### Core Metaphor: Santiago Builds His Own Boat While Sailing

Just as Ernest Hemingway's Santiago builds and repairs his fishing boat during his legendary voyage, our **Santiago AI** must:

1. **Build Domain Boats** (Specialized AIs like Santiago-PM, Santiago-Medical) while **sailing** (executing current tasks)
2. **Repair & Improve** the core Santiago platform using lessons from each voyage
3. **Navigate by Stars** (knowledge graphs) and **read the sea** (data patterns)
4. **Adapt to Currents** (changing requirements) through continuous evolution

### Updated 4-Layer Knowledge Processing Pipeline (The Sea → Fish → Boat → Voyage)

```text
Raw Knowledge Sources          Structured Knowledge           Computable Logic              Executable Workflows
(Layer 1)                      (Layer 2)                      (Layer 3)                     (Layer 4)
├── Clinical guidelines        ├── CI-tagged triples          ├── FHIR-CPG rules            ├── Passage orchestrations
├── Domain documents           ├── SNOMED CT mappings         ├── Risk calculations         ├── MCP service endpoints
├── Expert interviews          ├── Relationship graphs        ├── Decision algorithms       ├── Agent action sequences
├── Research papers            └── Confidence scores          └── Temporal reasoning        └── Workflow DAGs
```

### Updated System Components Architecture

#### 1. Santiago Core Engine (The Boat Builder)

**Purpose:** The core NuSy AI system that builds domain-specific AIs

**Components:**
- **CatchFish:** Knowledge ingestion from raw sources (Layer 1 → Layer 2)
- **FishNet:** Behavior validation and test generation (BDD/TDD specs)
- **Navigator:** Orchestration engine for knowledge processing cycles
- **Passage System:** Workflow orchestration with nautical theming

**Location:** `santiago-core/` (New separate directory for core system)

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
- Ethical frameworks (Baha'i principles) - built into every agent
- Domain expertise maps and capability assessments
- Evolutionary learning patterns from past voyages

#### 3. Domain Santiago Instances (Specialized Boats)

**Purpose:** Domain-specific AI agents built by Santiago Core

**Current Focus:** Santiago-PM (Product Management)
**Future Domains:** Santiago-Medical, Santiago-Finance, Santiago-Legal, etc.

**Examples:**
- **santiago-pm:** Product management and development coordination
- **santiago-medical:** Clinical decision support and guideline processing
- **santiago-finance:** Risk assessment and regulatory compliance

**Creation Process:**
1. Domain analysis and knowledge ingestion
2. Agent specialization using Santiago's 4-layer pipeline
3. Workflow adaptation via Passage system
4. Validation and deployment

**Directory Structure:**
```
santiago-core/          # Core Santiago system
santiago-pm/            # Product management domain AI
santiago-medical/       # Healthcare domain AI (future)
santiago-finance/       # Finance domain AI (future)
```

#### 4. Autonomous Development Team (The Crew)

**Purpose:** AI agents that collaboratively build and improve the Santiago ecosystem

**MVP Team (Start Here):**
- **Product Manager:** Manages work flow, assigns tasks, monitors progress
- **Software Architect:** Creates plans, designs systems, answers technical questions
- **Software Developer:** Implements features, writes code, follows development practices

**Full Team Vision:**
- **Quality Assurance Specialist:** BDD/TDD testing, behavior validation
- **Knowledge Engineer:** Knowledge graph management, ontology development
- **DevOps Engineer:** CI/CD, infrastructure, deployment
- **Ethical Oversight Officer:** Reviews plans and decisions for ethical alignment

**Development Approach:**
- Start with 3 core roles to establish autonomous collaboration
- Add roles incrementally as system matures
- Each agent includes ethical guidelines in prompts from day one
- Follow development practices: version control, code reviews, testing, documentation

#### 5. Knowledge Graph Ecosystem (The Ocean)

**Purpose:** Unified symbolic knowledge representation across all Santiago instances

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

#### 6. MCP Service Layer (The Nets & Harpoons)

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

#### 7. Evolutionary Engine (The Learning from Each Voyage)

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

### Updated Integration Architecture

```
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
│Santiago│   │Santiago    │   │   Domain        │   │                MCP Service Layer                        │
│Core    │   │Orchestrator│   │   Santiagos     │   │  ┌─────────────────────────────────────────────────┐    │
│Engine  │   │            │   │   (PM, Medical, │   │  │              Service Endpoints                    │    │
└───┬──┘   └──────┬──────┘   └─────────┬───────┘   │  │  • /api/v1/query/chat (NL queries)             │    │
    │             │                    │            │  │  • /api/v1/cds/patient-bundle (CDS)            │    │
    └─────────────┼────────────────────┼────────────┤  │  • /api/v1/analysis/full-chart (comprehensive) │    │
                  │                    │            │  │  • /api/v1/mcp/tools (tool calling)            │    │
          ┌───────▼────────────────────▼───────┐    │  └─────────────────────────────────────────────────┘    │
          │     Autonomous Development Team     │    │                                                         │
          │  ┌─────────────────────────────────┐    │  ┌─────────────────────────────────────────────────┐    │
          │  │ MVP: PM + Architect + Developer │    │  │            Tool Integration Layer               │    │
          │  │ Full: + QA + Knowledge + DevOps │    │  │  • Git (version control)                        │    │
          │  │       + Ethics Officer          │    │  │  • Taiga (product management)                  │    │
          │  └─────────────────────────────────┘    │  │  • Matrix (chat/collaboration)                │    │
          └─────────────────────────────────────────┘    │  • Vault (secrets management)                  │    │
                                                         │  └─────────────────────────────────────────────────┘    │
                                                         └─────────────────────────────────────────────────────────┘
```

---

## Part 2: Updated Development Roadmap

### Phase 1: Foundation (Weeks 1-4) - Build the Autonomous Team
**Goal:** Establish autonomous AI team collaboration and rename directories

**Step 1.1: Directory Restructuring** *(Week 1)*
- ✅ **COMPLETED:** Rename `nusy_pm/` → `santiago-pm/` to clarify it's the PM domain AI
- Create `santiago-core/` directory for the core Santiago system
- Update all references and imports to use new directory structure

**Step 1.2: MVP Autonomous Team Setup** *(Week 1-2)*
- **3 Core Agents:** Product Manager, Software Architect, Software Developer
- **Ethical Foundation:** Build ethical guidelines into every agent prompt from day one
- **Development Practices:** Version control, code reviews, testing, documentation
- **Infrastructure:** Hank sets up APIs, secrets (Doppler), DGX environment

**Step 1.3: Autonomous Team Workflow Experiment** *(Week 2-3)*
- **Experiment Design:** 3 agents working together on Santiago-PM development
- **Workflow:** Architect creates plans (B) + PM manages flow and assigns tasks (C)
- **Checkpoints:** Daily progress reviews + breakthroughs with Hank
- **Success Metrics:** Agents following development practices, ethical decision-making

**Step 1.4: Santiago-PM Domain Specialization** *(Week 3-4)*
- Move PM-specific passages and knowledge to `santiago-pm/`
- Create Santiago-PM's domain knowledge graph schema
- Implement Santiago-PM's specialized agent behaviors
- Test autonomous team building Santiago-PM features

### Phase 2: Santiago Core Development (Weeks 5-8) - Build the Boat Builder
**Goal:** Develop the core Santiago system using the autonomous team

**Step 2.1: Santiago Core Architecture** *(Week 5)*
- Define Santiago core components in `santiago-core/`
- Implement core knowledge processing pipeline
- Build Passage system integration
- Create core agent framework

**Step 2.2: Autonomous Team Expansion** *(Week 6)*
- Add Quality Assurance agent (focus on BDD/TDD)
- Add Ethical Oversight Officer (reviews plans and decisions)
- Test expanded team collaboration
- Refine workflow based on experiment results

**Step 2.3: Santiago Core MVP** *(Week 7)*
- Core Santiago can ingest domain knowledge
- Can build basic domain-specific agents
- Implements 4-layer knowledge processing
- Provides MCP services

**Step 2.4: Santiago-PM Integration** *(Week 8)*
- Santiago core builds and improves Santiago-PM
- Test full cycle: Santiago → builds Santiago-PM → improves Santiago
- Validate autonomous development capabilities

### Phase 3: Multi-Domain Expansion (Weeks 9-12) - Build Multiple Boats
**Goal:** Expand to full 7-agent team and multiple domain Santiagos

**Step 3.1: Full Development Team** *(Week 9)*
- Add Knowledge Engineer (knowledge graph management)
- Add DevOps Engineer (CI/CD, infrastructure)
- Complete 7-agent autonomous development team
- Test full team collaboration on complex features

**Step 3.2: Santiago-Medical Development** *(Week 10)*
- Use Santiago core to build Santiago-Medical
- Ingest clinical guidelines and medical knowledge
- Test healthcare domain specialization
- Validate clinical decision support capabilities

**Step 3.3: Additional Domain Santiagos** *(Week 11)*
- Build Santiago-Finance or Santiago-Legal
- Test domain-agnostic architecture
- Refine domain specialization process
- Optimize knowledge ingestion pipelines

**Step 3.4: Cross-Domain Learning** *(Week 12)*
- Implement learning across domain Santiagos
- Test knowledge sharing between domains
- Validate evolutionary improvements
- Prepare for marketplace capabilities

### Phase 4: Production & Marketplace (Weeks 13-16) - Launch the Fleet
**Goal:** Deploy production systems and enable marketplace

**Step 4.1: Production Infrastructure** *(Week 13)*
- Deploy Santiago core and domain instances
- Implement production MCP services
- Set up monitoring and logging
- Enable high-availability operations

**Step 4.2: Marketplace Preparation** *(Week 14)*
- Design domain Santiago packaging and deployment
- Create client onboarding processes
- Implement fine-tuning capabilities
- Test multi-tenant architecture

**Step 4.3: Continuous Evolution** *(Week 15)*
- Deploy self-improvement mechanisms
- Enable field learning from deployed Santiagos
- Implement cross-domain knowledge sharing
- Monitor and optimize performance

**Step 4.4: Marketplace Launch** *(Week 16)*
- Launch marketplace for domain Santiagos
- Enable client deployments and updates
- Implement usage analytics and feedback
- Scale autonomous development capabilities

---

## Part 3: Updated Critical Architecture Decisions

### Decision 1: Directory Structure & Naming
**Question:** How to structure directories to reflect Santiago hierarchy?

**Resolution:** ✅ **APPROVED**
- `santiago-core/` - Core Santiago system (boat builder)
- `santiago-pm/` - Product management domain AI (formerly `nusy_pm/`)
- `santiago-{domain}/` - Future domain-specific AIs
- **Rationale:** Clear separation between core system and domain implementations

### Decision 2: Autonomous Team Development
**Question:** MVP team size and expansion strategy?

**Resolution:** ✅ **APPROVED**
- **Start with 3 core roles:** PM + Architect + Developer
- **Add roles incrementally:** QA, Ethics Officer, Knowledge Engineer, DevOps
- **Ethical oversight from day one:** Built into every agent prompt
- **Rationale:** Get autonomous collaboration working quickly, expand as system matures

### Decision 3: Workflow Experiment
**Question:** Which autonomous workflow to try first?

**Resolution:** ✅ **APPROVED**
- **Combined B+C approach:** Architect creates plans + PM manages flow
- **Experiment framework:** 3-agent collaboration with daily checkpoints
- **Infrastructure setup:** Hank handles APIs, secrets, DGX environment
- **Rationale:** Balances planning with dynamic task assignment

### Decision 4: Ethical Integration
**Question:** How to integrate ethical oversight?

**Resolution:** ✅ **APPROVED**
- **Built into every agent:** Ethical guidelines in all prompts from beginning
- **Dedicated Ethics Officer:** Reviews plans and decisions
- **Feature reviews:** Human + QA + Ethics Officer
- **Architect tags:** "ethical considerations" for focused review
- **Rationale:** Ethics as foundational, not add-on

### Decision 5: Marketplace Timing
**Question:** When to focus on marketplace architecture?

**Resolution:** ✅ **APPROVED**
- **Focus on Santiago-PM first:** Get core process working
- **Design for modularity:** Architecture supports multiple domains
- **Marketplace after full team:** Complete 7-agent team + multiple domains working
- **Rationale:** Validate core capabilities before scaling

---

## Part 4: Updated Success Metrics & Validation

### Technical Metrics
- **Knowledge Processing Accuracy:** >95% extraction accuracy, >90% logic formalization
- **Workflow Execution:** >99% passage completion rate, <5min average execution time
- **Autonomous Development:** 3-agent team successfully builds features following practices
- **System Availability:** >99.9% uptime, <1s average response time
- **Evolution Effectiveness:** >20% improvement in cycle times over 6 months

### Business Metrics
- **Domain AI Creation:** Time to build new domain Santiago <2 weeks (after core working)
- **Autonomous Team Efficiency:** >70% reduction in human intervention for routine tasks
- **Quality Assurance:** 100% evidence-based recommendations
- **Marketplace Readiness:** Multiple domain Santiagos deployed and learning

### Validation Experiments
1. **3-Agent Autonomous Development:** MVP team builds Santiago-PM features
2. **Santiago Core Bootstrapping:** Core system builds itself using autonomous team
3. **Domain Specialization:** Santiago core builds Santiago-Medical autonomously
4. **Ethical Development:** All agents demonstrate ethical decision-making
5. **Cross-Domain Learning:** Knowledge sharing between Santiago-PM and Santiago-Medical

---

## Part 5: Updated Risk Mitigation

### Technical Risks
- **Autonomous Team Coordination:** Start with 3 agents, add complexity gradually
- **Ethical Implementation:** Guidelines built into prompts from day one
- **Knowledge Accuracy:** Multi-layer validation and human oversight
- **System Complexity:** Maintain modular architecture with clear interfaces
- **Performance Scaling:** Design for horizontal scaling from day one
- **Integration Complexity:** Use adapter pattern for all external integrations

### Operational Risks
- **Team Development Pace:** Daily checkpoints and Hank availability for infrastructure
- **Role Specialization:** Scaffold each new role with clear responsibilities
- **Quality Consistency:** BDD/TDD practices enforced by QA agent
- **Ethical Boundaries:** Ethics Officer reviews all major decisions
- **Evolution Stability:** Safe experimentation frameworks with rollback capabilities

### Business Risks
- **Marketplace Timing:** Focus on core capabilities before scaling
- **Client Adoption:** Validate with real use cases before broad deployment
- **Regulatory Compliance:** Built-in compliance checking for healthcare domains
- **Vendor Lock-in:** Open standards and modular design for flexibility

---

## Version History

### v1 → v2 Changes
- **Clarified Santiago Hierarchy:** Core Santiago vs domain Santiagos
- **Directory Restructuring:** `nusy_pm/` → `santiago-pm/`, added `santiago-core/`
- **Autonomous Team Focus:** MVP 3-agent team, expand to 7+ roles
- **Ethical Integration:** Built into every agent from beginning
- **Workflow Experiment:** Combined architect planning + PM task management
- **Marketplace Timing:** After full team and multiple domains working
- **Development Phases:** Restructured around autonomous team development

---

*This v2 document incorporates user feedback and clarifies the Santiago ecosystem architecture. The vision is a self-sustaining AI development ecosystem where Santiago autonomously builds specialized domain experts while continuously improving itself, much like Santiago building and repairing his boat during his legendary voyage.*</content>
<parameter name="filePath">/Users/hankhead/Projects/Personal/nusy-product-team/nusy_pm/strategic-charts/Santiago-Trains-Manolin-v2.md