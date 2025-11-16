# Santiago Architecture Review — Prompt v3

**Version:** 3.0  
**Target Model:** Claude Sonnet 4.5 / GPT-4 / Other LLMs  
**Last Updated:** 2025-11-16

---

## ⚠️ CRITICAL — READ THIS FIRST ⚠️

**BEFORE scanning any code, read:**

📘 **[ocean-research/00-ARCHITECTURE-PATTERN.md](ocean-research/00-ARCHITECTURE-PATTERN.md)**

This document explains THE critical architectural insight that all previous architecture reviews missed:

> **Santiago is NOT a fixed team of agents.**  
> **Santiago is a SELF-BOOTSTRAPPING FACTORY that generates domain-specific Santiagos on demand.**

If you proceed without reading this document, your architecture plan WILL be incorrect.

---

## Critical Architectural Insight

### What Every Model Gets Wrong:

❌ **Assumption:** Santiago is a fixed team (PM + Architect + Developer + QA + UX + Platform + Ethicist)  
❌ **Assumption:** Humans manually author `knowledge/domains/pm/`, `knowledge/domains/architect/`, etc.  
❌ **Assumption:** Fake team is a fallback plan if DGX is delayed

### The Reality:

✅ **Santiago is a factory** — Navigator + Catchfish + Fishnet components that generate domain-specific Santiagos  
✅ **Fake team builds the factory** — Thin MCP proxies to external APIs (OpenAI, Claude, Copilot) implement factory code  
✅ **Factory catches real Santiagos** — Takes 30-60m to extract domain knowledge from sources, runs 3-5 validation cycles  
✅ **Real Santiagos replace fake team** — Progressive replacement via A/B testing (≥90% performance parity)  
✅ **System becomes self-sustaining** — Real Santiagos eventually improve the factory itself

### The Bootstrapping Sequence:

```
Phase 0 (Week 1): Deploy fake team (proxy MCP services to external APIs)
      ↓
Phase 1 (Weeks 2-6): Fake team builds factory (Navigator/Catchfish/Fishnet)
      ↓
Phase 2 (Weeks 7-8): Factory catches first real Santiago (e.g., santiago-pm-safe-xp)
      ↓
      A/B test: Fake Santiago-PM vs Real Santiago-PM
      ↓
      If Real ≥ 90% of Fake → Replace the proxy
      ↓
Phase 3 (Weeks 9-20): Repeat for each role (progressive replacement)
      ↓
Phase 4 (Week 20+): Real Santiagos improve factory (self-sustaining)
```

**Evidence:** Clinical prototype converted guidelines to 4-layer knowledge in 30-60m per guideline, required 3 validation cycles. This IS the factory workflow.

---

## Mission

You are conducting an architecture review of the **Santiago Project** — a self-bootstrapping AI factory that:

1. Starts with "fake" Santiagos (MCP proxies to external APIs)
2. Uses fake team to build factory infrastructure
3. Uses factory to generate real domain-specific Santiagos
4. Progressively replaces fake team with real Santiagos via experiments
5. Achieves self-improvement (real Santiagos enhance factory)

Your task is to:

- **Scan the repository** to understand current state
- **Read ocean-research/** to understand vision
- **Read santiago-pm/ folder structure** to understand development patterns
- **Design the architecture** for the self-bootstrapping factory
- **Produce 5 deliverables** (detailed below)

**Key Constraint:** Your design must enable the fake team to build the factory, NOT humans manually coding everything.

---

## Context: Repository Tour

### Core Directories

**`santiago_core/`** — Current implementation (active development)  
**`src/nusy_pm_core/`** — Legacy prototype (archived, reference only)  
**`santiago-code/`** — Early experiments (archived, reference only)

**`ocean-research/`** — Vision documents, architecture proposals, research  
- **00-ARCHITECTURE-PATTERN.md** ← START HERE (mandatory reading)
- `building-on-DGX/` — DGX Spark deployment specs (128GB RAM, 4TB+8TB NVMe, vLLM/TensorRT)
- `manolin_multi_agent_architecture.md` — Shared memory & concurrency patterns
- `nusy_manolin_multi_agent_test_plans.md` — Multi-agent testing strategy
- `fake_team_pack/` — Proxy strategy (Phase 0 bootstrapping)

**`santiago-pm/`** — Development practices encoded as folder structure  
- `expeditions/` — Hypothesis-driven experiments (how fake team improves factory)
- `tackle/` — Modular implementation units (how fake team structures code)
- `voyage-trials/` — BDD test scenarios (how fake team validates work)
- `strategic-charts/` — Vision & process docs
  - **"Old man and the sea.md"** ← 10-step fishing process (literal factory workflow)

**`nusy_prototype/`** — Clinical reasoning prototype  
- **EVIDENCE:** 30-60m conversion time per guideline, 3 validation cycles to quality threshold
- **INSIGHT:** This workflow IS the factory. Industrialize it.

**`knowledge/` (MISSING)** — Where generated Santiagos will be stored
- `knowledge/catches/` — Generated domain-specific Santiagos (factory outputs)
- `knowledge/templates/` — Base structures for generating Santiagos
- `knowledge/proxy-instructions/` — Role definitions for fake team

**`config/`, `notes/`, `backlog/`, `experiments/`, `reports/`** — Peripheral (context only)

---

## Output Expectations

Produce **5 deliverables** in a new directory:

```
ocean-arch-redux/arch-redux-<model-name>-v3-plan/
├── ARCHITECTURE_PLAN.md
├── MIGRATION_STEPS.md
├── FOLDER_LAYOUT_PROPOSAL.md
├── RELEVANCE_MAP.md
└── ASSUMPTIONS_AND_RISKS.md
```

### 1. ARCHITECTURE_PLAN.md

**Template:**

```markdown
# Santiago Factory Architecture Plan

**Prepared by:** <model-name>
**Date:** <YYYY-MM-DD>
**Version:** 3.0

---

## Executive Summary

[1-2 paragraphs explaining: Santiago is factory, fake team builds it, progressive replacement]

---

## Current Architecture

[Describe: santiago_core/ structure, missing knowledge/, legacy archives]

---

## Target Architecture

### Phase 0: Fake Team (Contractor Proxies)

[Describe: MCP proxy services to OpenAI/Claude/Copilot, thin wrappers, role instructions]

### Phase 1: Factory Components (Built by Fake Team)

[Describe: Navigator, Catchfish, Fishnet, validation loops, provenance tracking]

### Phase 2: First Catch & Replacement

[Describe: First fishing expedition, A/B testing, replacing fake Santiago-PM]

### Phase 3: Progressive Replacement

[Describe: Repeat for each role, hypothesis-driven experiments, hybrid team during transition]

### Phase 4: Self-Sustaining

[Describe: Real Santiagos propose factory improvements, self-optimization]

---

## Key Architectural Components

### Navigator

[Describe: Orchestrates 10-step fishing process from "Old Man and the Sea"]

### Catchfish

[Describe: Extracts structured knowledge from sources, 30-60m → <15m optimization target, 4-layer model]

### Fishnet

[Describe: Generates BDD tests from knowledge graph, infers MCP tool capabilities]

### Fake Team Proxies

[Describe: santiago_core/agents/_proxy/, MCP protocol, API routing]

### Knowledge Storage

[Describe: knowledge/catches/, Markdown + YAML frontmatter, upgrade path to JSON/vector]

---

## MCP Integration

[Describe: Each Santiago as independent MCP service, auto-generated manifests, coordination patterns]

---

## DGX Deployment

[Describe: Mistral-7B-Instruct shared instance, vLLM batching, memory architecture]

---

## Ethics & Concurrency Gating

[Describe: Pre-execution review, Santiago-Ethicist role, evolutionary monitoring]

---

## References Cited

- ocean-research/00-ARCHITECTURE-PATTERN.md
- santiago-pm/strategic-charts/Old man and the sea.md
- ocean-research/building-on-DGX/dgx_spark_nusy_report.md
- nusy_prototype/ (clinical prototype evidence: 30-60m, 3 cycles)
- santiago-pm/expeditions/, tackle/, voyage-trials/ (development patterns)
```

**Critical Requirements:**

- Must reference **00-ARCHITECTURE-PATTERN.md** and explain factory pattern
- Must reference **"Old Man and the Sea"** 10-step fishing process
- Must reference **clinical prototype** (30-60m conversion, 3 validation cycles)
- Must explain **4 phases** (Fake Team → Factory → First Catch → Progressive Replacement)
- Must include section titled **"Ethics & Concurrency Gating"**
- Must have **"References Cited"** section at end

---

### 2. MIGRATION_STEPS.md

**Structure:**

- **7 milestones** maximum (avoid milestone bloat)
- Each milestone: **Goal, Affected Paths, Tasks (- [ ] syntax), Acceptance Criteria**
- Headings: `## Milestone <n>: <Title>` (exactly this format)

**Required Milestones:**

1. **Milestone 0: Bootstrap Fake Team** (Week 1)
   - Deploy proxy MCP services to external APIs
   - Load role instructions for each fake Santiago
   - Validate fake team can coordinate on compound tasks

2. **Milestone 1: Implement Factory Infrastructure** (Weeks 2-6)
   - Fake team implements Navigator, Catchfish, Fishnet
   - Fake team writes BDD tests for factory behavior
   - End-to-end test: PDF → deployed MCP service

3. **Milestone 2: First Santiago Catch** (Weeks 7-8)
   - Factory catches santiago-pm-safe-xp from SAFe/XP sources
   - A/B test fake vs real Santiago-PM
   - Replace fake Santiago-PM if ≥90% parity

4-7. **Progressive replacement, DGX deployment, self-improvement**

**Critical Requirements:**

- Milestone 0 must be "Bootstrap Fake Team" (not "knowledge foundation")
- Milestone 1 must be "Fake team builds factory" (not "manual development")
- Milestone 2 must include A/B testing and replacement logic
- Tasks must use `- [ ]` syntax for tracking

---

### 3. FOLDER_LAYOUT_PROPOSAL.md

**Structure:**

- Proposed directory tree with annotations
- Mapping table: Current Path → Target Path → Action (refactor, split, extract, deprecate)

**Required Directories:**

```
knowledge/
├── catches/                    # Generated Santiagos (factory outputs)
│   └── santiago-pm-safe-xp/
│       ├── domain-knowledge/  # Markdown + YAML extracted from sources
│       ├── bdd-tests/         # Feature files from Fishnet
│       ├── mcp-manifest.json  # Auto-generated
│       └── provenance.yaml    # Fishing expedition metadata
├── templates/                  # Base structures for generating Santiagos
└── proxy-instructions/         # Role definitions for fake team
    ├── pm-role.md
    ├── architect-role.md
    └── ...

santiago_core/
├── agents/
│   ├── _proxy/                # Phase 0: Fake team (MCP proxies)
│   │   ├── pm_proxy.py
│   │   ├── architect_proxy.py
│   │   └── ...
│   └── santiago-pm-safe-xp/   # Phase 2+: Real Santiagos (factory-generated)
│       └── service/           # MCP service implementation
└── ...

nusy_orchestrator/
└── santiago_builder/          # Factory components
    ├── navigator.py           # Orchestrates fishing expeditions
    ├── catchfish.py           # Knowledge extraction (30-60m → <15m)
    └── fishnet.py             # BDD test generation
```

**Critical Requirements:**

- `knowledge/catches/` for generated Santiagos (NOT `knowledge/domains/` for pre-authored)
- `santiago_core/agents/_proxy/` for fake team
- `nusy_orchestrator/santiago_builder/` for factory components
- Mapping table showing how to refactor existing code

---

### 4. RELEVANCE_MAP.md

**Structure:**

- **Relevant:** Files/directories critical to architecture decisions
- **Peripheral:** Context that informs but doesn't drive decisions
- **Legacy-Duplicate:** Archived code to preserve but not use
- **GAP:** Missing items that should exist

**Required Classifications:**

- **Relevant:**
  - `ocean-research/00-ARCHITECTURE-PATTERN.md` ← Mandatory reading
  - `santiago-pm/strategic-charts/Old man and the sea.md` ← Fishing process
  - `santiago-pm/expeditions/`, `tackle/`, `voyage-trials/` ← Development patterns
  - `ocean-research/building-on-DGX/` ← Deployment specs
  - `nusy_prototype/` ← Clinical prototype evidence

- **GAP:**
  - `knowledge/` folder (missing, needs creation)
  - `santiago_core/agents/_proxy/` (fake team, needs creation)
  - `nusy_orchestrator/santiago_builder/` (factory, needs fake team to build)

---

### 5. ASSUMPTIONS_AND_RISKS.md

**Structure:**

- **Assumptions:** Things you're assuming are true (with validation strategy)
- **Risks:** Things that could go wrong (with mitigation)
- **Provenance & Queued Writes:** How to avoid KG corruption

**Required Sections:**

- Assumption: Fake team (external APIs) can build factory in 4-6 weeks
- Assumption: Clinical prototype evidence (30-60m, 3 cycles) generalizes to all domains
- Assumption: A/B testing at ≥90% parity is sufficient replacement threshold
- Risk: Catchfish extraction quality degrades without proper validation
- Risk: Fake team API costs exceed budget before first replacement
- Risk: Real Santiagos fail to match fake performance (no replacement)
- Mitigation: Unified KG layer with queued writes, provenance tracking, schema validation

---

## Validation Checklist

**Before submitting your architecture plan, verify:**

- [ ] I read **ocean-research/00-ARCHITECTURE-PATTERN.md** BEFORE scanning code
- [ ] My plan starts with **Phase 0: Fake Team** (proxy MCP services)
- [ ] My plan explains **fake team builds factory** (not humans manually coding)
- [ ] My plan includes **factory catches real Santiagos** (30-60m extraction, 3-5 validation cycles)
- [ ] My plan includes **A/B testing** (fake vs real) before replacement
- [ ] My plan includes **progressive replacement** (one role at a time, not all at once)
- [ ] I referenced **"Old Man and the Sea"** 10-step fishing process
- [ ] I referenced **clinical prototype** (30-60m, 3 cycles) as evidence
- [ ] I explained how **santiago-pm/ folder structure** teaches development patterns to fake team
- [ ] My milestones reflect **4 phases** (Fake Team → Factory → First Catch → Self-Sustaining)
- [ ] I described **Navigator, Catchfish, Fishnet** as factory components
- [ ] I explained **knowledge/catches/** stores generated Santiagos (NOT pre-authored domains)
- [ ] I included **"Ethics & Concurrency Gating"** section
- [ ] I included **"References Cited"** section in ARCHITECTURE_PLAN.md

**If any checkbox is unchecked, STOP and re-read 00-ARCHITECTURE-PATTERN.md.**

---

## Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: "Build Santiago-PM agent first, then others"

**Problem:** Treats roles as if they're prerequisites for the factory.

**Correct Approach:**  
Phase 0: Deploy fake Santiago-PM (hours)  
Phase 1: Fake Santiago-PM helps fake team build factory (weeks)  
Phase 2: Factory catches real Santiago-PM → replace fake if ≥90% parity

---

### ❌ Anti-Pattern 2: "Manually author knowledge/domains/pm/core-practices.md"

**Problem:** Humans writing domain knowledge defeats the purpose of the factory.

**Correct Approach:**  
Catchfish extracts structured knowledge from SAFe Framework PDF, Extreme Programming book, Lean Startup. This takes 30-60m per source with 3-5 validation cycles. Optimization target: <15m per source.

---

### ❌ Anti-Pattern 3: "Fake team is a fallback if DGX is delayed"

**Problem:** Misunderstands fake team as contingency plan.

**Correct Approach:**  
Fake team is **Phase 0 of every Santiago deployment**, always. It's the bootstrapping mechanism. Without fake team, there's no one to build the factory.

---

### ❌ Anti-Pattern 4: "Focus on MCP infrastructure, orchestrator, ethics gating"

**Problem:** These are generic distributed systems concerns, not the core innovation.

**Correct Approach:**  
Focus on **Catchfish** (optimize 30-60m → <15m), **Fishnet** (generate BDD tests from KG), **Navigator** (orchestrate 3-5 validation cycles until quality threshold). These ARE the factory.

---

### ❌ Anti-Pattern 5: "Deploy all Santiagos at once, then test"

**Problem:** Big-bang replacement is risky and unscientific.

**Correct Approach:**  
Progressive replacement via A/B testing experiments. Each replacement is a hypothesis: "Real Santiago-X will match or exceed fake Santiago-X." Test, measure, replace if validated.

---

## Example: What a Correct Architecture Looks Like

### Phase 0: Fake Team Deployment (Week 1)

**Task:** Deploy thin MCP wrappers proxying to external APIs

```python
# santiago_core/agents/_proxy/pm_proxy.py
from mcp import MCPService
import openai

class FakeSantiagoPM(MCPService):
    def __init__(self):
        self.instructions = load("knowledge/proxy-instructions/pm-role.md")
    
    def invoke_tool(self, tool_name, params):
        """All tools proxy to OpenAI GPT-4"""
        return openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": f"{tool_name}: {params}"}
            ]
        )
```

**Characteristics:**
- Minimal code (20-30 lines per role)
- Fast to deploy (hours, not days)
- Expensive (API costs per request)
- **Purpose:** Build the factory, then get replaced

---

### Phase 1: Factory Implementation (Weeks 2-6)

**Hypothesis (from Fake Santiago-PM):**  
"If we implement Catchfish with 4-layer extraction, Navigator with 3-5 validation cycles, and Fishnet with BDD generation, we can catch domain-specific Santiagos in <60m."

**BDD Scenario (from Fake Santiago-PM):**

```gherkin
Feature: Santiago Factory Fishing Expedition
  Scenario: Catch Santiago-PM from SAFe and XP sources
    Given sources: ["SAFe Framework 6.0.pdf", "Extreme Programming Explained.pdf"]
    When Catchfish extracts structured knowledge
    And Navigator validates with 3 cycles
    And Fishnet generates BDD tests
    Then santiago-pm-safe-xp MCP service is deployed
    And service passes ≥95% of BDD tests
```

**Implementation (by Fake Santiago-Architect + Developer):**

```python
# nusy_orchestrator/santiago_builder/catchfish.py
class Catchfish:
    """Extracts structured 4-layer knowledge from sources"""
    def extract(self, sources, domain):
        # Layer 1: Raw text extraction
        # Layer 2: Entity/relationship identification
        # Layer 3: Semantic structuring (Markdown + YAML)
        # Layer 4: Knowledge graph integration
        # Target: <60m per source → optimize to <15m
        pass
```

**Validation (by Fake Santiago-QA):**  
Run end-to-end test: PDF → deployed MCP service in <60m

---

### Phase 2: First Santiago Catch (Weeks 7-8)

**Fishing Expedition:**

1. Navigator receives request: "Catch Santiago-PM with SAFe + XP knowledge"
2. Catchfish extracts from sources (30-60m per source = 60-120m total)
3. Build knowledge graph
4. Fishnet generates BDD tests from KG (10-15 test scenarios)
5. Navigator runs validation cycle 1 → 78% pass rate → identify gaps
6. Navigator runs validation cycle 2 → 89% pass rate → refine extraction
7. Navigator runs validation cycle 3 → 96% pass rate → threshold met
8. Deploy as `santiago-pm-safe-xp` MCP service
9. Store in `knowledge/catches/santiago-pm-safe-xp/`

**A/B Testing:**

Run 10 identical PM tasks through:
- Fake Santiago-PM (proxy to GPT-4)
- Real Santiago-PM (santiago-pm-safe-xp on Mistral-7B)

**Metrics:**
- Task completion quality (scored by fake Santiago-QA)
- Response time
- Cost per request

**Decision Rule:**  
If Real ≥ 90% of Fake on quality, replace the proxy.

**Outcome:**  
Real Santiago-PM scores 92% → replacement approved → all PM requests now route to santiago-pm-safe-xp → API costs reduced by 1/7th.

---

### Phase 3-4: Progressive Replacement & Self-Improvement

Repeat Phase 2 for each role. Eventually, real Santiagos propose and implement factory improvements.

---

## Deliverables Checklist

- [ ] Created `ocean-arch-redux/arch-redux-<model-name>-v3-plan/` directory
- [ ] ARCHITECTURE_PLAN.md (with factory pattern, 4 phases, References Cited, Ethics & Concurrency Gating)
- [ ] MIGRATION_STEPS.md (M0: Fake Team, M1: Factory, M2: First Catch, standardized headings)
- [ ] FOLDER_LAYOUT_PROPOSAL.md (knowledge/catches/, santiago_core/agents/_proxy/, factory components)
- [ ] RELEVANCE_MAP.md (00-ARCHITECTURE-PATTERN.md as Relevant, knowledge/ as GAP)
- [ ] ASSUMPTIONS_AND_RISKS.md (fake team assumptions, A/B testing threshold, Catchfish quality risks)

---

## Final Reminder

**You are not designing a team of AI agents.**  
**You are designing a SELF-BOOTSTRAPPING FACTORY that generates AI agents on demand.**

- Start with fake team (Phase 0)
- Fake team builds factory (Phase 1)
- Factory catches real Santiagos (Phase 2)
- Real Santiagos replace fake team (Phase 3)
- System becomes self-improving (Phase 4)

**This is the way.**

---

## Appendix: Key References

- **[ocean-research/00-ARCHITECTURE-PATTERN.md](ocean-research/00-ARCHITECTURE-PATTERN.md)** ← Mandatory reading
- **[santiago-pm/strategic-charts/Old man and the sea.md](santiago-pm/strategic-charts/Old man and the sea.md)** ← 10-step fishing process
- **[ocean-research/building-on-DGX/dgx_spark_nusy_report.md](ocean-research/building-on-DGX/dgx_spark_nusy_report.md)** ← DGX deployment
- **[ocean-research/manolin_multi_agent_architecture.md](ocean-research/manolin_multi_agent_architecture.md)** ← Shared memory
- **[ocean-research/fake_team_pack/](ocean-research/fake_team_pack/)** ← Proxy strategy
- **nusy_prototype/** ← Clinical prototype (30-60m, 3 cycles)
- **santiago-pm/expeditions/**, **santiago-pm/tackle/**, **santiago-pm/voyage-trials/** ← Development patterns

Good luck, and may your fishing expeditions be fruitful! 🎣
