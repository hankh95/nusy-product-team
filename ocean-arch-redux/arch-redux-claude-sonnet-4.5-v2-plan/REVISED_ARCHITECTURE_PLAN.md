# Revised Architecture Plan — Post-Meta-Discovery

**Date:** 2025-11-16  
**Original Plan Commit:** a86c0b2  
**Revision Trigger:** Discovery of "Santiago Factory" pattern from "Old Man and the Sea" metaphor

## Critical Meta-Insight

**The Original Plan Missed the Core Architecture:**

The initial plan assumed we're building **specific Santiagos** (PM, Ethicist, Architect, etc.) with hand-authored domain knowledge in `knowledge/domains/`.

**The Actual Architecture:**

We're building a **Santiago Factory** that generates domain-specific Santiagos on-demand through a "fishing expedition" process. Santiago is a **template**, not a set of pre-built agents.

## The True Architecture: Santiago Factory

### Core Components

1. **Navigator** — Orchestrates the 10-step fishing process from raw materials to deployed MCP service
2. **Catchfish** — Converts raw sources (PDFs, APIs, docs) into structured 4-layer knowledge (the 30-60m bottleneck)
3. **Fishnet** — Generates BDD tests from knowledge graph to validate quality
4. **Santiago Template** — Base structure for any domain-specific Santiago

### The Fishing Process (10 Steps)

```
User Request: "Create a Product Manager Santiago who knows SAFe and XP"
    ↓
1. Vision Gathering: What does this Santiago need to do? (MCP services, behaviors)
    ↓
2. Raw Materials: Collect sources (PDFs, APIs, docs, expert interviews)
    ↓
3. Catchfish: Process raw materials → structured 4-layer knowledge (30-60m per source)
    ↓
4. Indexing: Make knowledge highly referenceable
    ↓
5. Ontology Loading: Apply naming conventions, models, schemas
    ↓
6. KG Building: Store structured knowledge in knowledge graph
    ↓
7. Fishnet: Generate BDD tests to validate KG and MCP services
    ↓
8. Navigator: Orchestrate validation cycles until quality threshold met (typically 3 cycles)
    ↓
9. Deployment: Generate MCP manifest, deploy as service
    ↓
10. Learning: Use logs and metrics to improve the fishing process itself
```

### Revised Folder Structure

```
nusy_orchestrator/
  santiago_builder/          # The factory
    navigator.py             # Step 8: Orchestration loop
    catchfish.py             # Step 3: Knowledge extraction engine
    fishnet.py               # Step 7: BDD test generator
    ontology_loader.py       # Step 5: Load domain ontologies
    kg_builder.py            # Step 6: Build knowledge graph
    
knowledge/
  templates/
    santiago-template/       # Base template for any Santiago
      mcp-manifest-template.json
      domain-knowledge-structure.md
      
  catches/                   # Generated Santiagos (NOT pre-authored)
    santiago-pm-safe-xp/     # Created from fishing expedition
      domain-knowledge/
        safe-patterns-4layer.md
        xp-practices-4layer.md
      bdd-tests/
        pm-scenarios.feature
      mcp-manifest.json      # Auto-generated
      provenance.yaml        # Fishing expedition metadata
      
    santiago-cardiologist-aha/
      domain-knowledge/
        aha-stroke-2024-4layer.md
        aha-heart-failure-2023-4layer.md
      bdd-tests/
        cardiology-scenarios.feature
      mcp-manifest.json
      provenance.yaml
      
.nusy/fishing-expeditions/   # Ephemeral (deleted after catch)
  {expedition-id}/
    raw-materials/
    extraction-attempts/
    test-results/
```

### Key Architectural Changes

#### Change 1: No Pre-Built Domain Knowledge

**Original Plan:**
- Manually author `knowledge/domains/pm/`, `knowledge/domains/ethics/`, etc.
- Hand-write MCP manifests for each role

**Revised:**
- `knowledge/catches/` stores **generated** Santiagos from fishing expeditions
- MCP manifests are **auto-generated** from discovered capabilities
- No manual authoring—everything comes from the fishing process

#### Change 2: Catchfish is the Core Innovation

**Original Plan:**
- Focus on MCP service infrastructure, orchestrator, ethics gating

**Revised:**
- **Catchfish** is the competitive advantage—the proven algorithm that converts clinical guidelines to 4-layer model in 30-60m
- Primary optimization target: reduce 30-60m to <15m through automation
- The "3 validation cycles until quality threshold" is the core loop

#### Change 3: Santiago is a Product, Not a Team

**Original Plan:**
- Build a team of Santiagos: PM, Ethicist, Architect, Developer, QA, UX, Platform

**Revised:**
- Build the **factory** (Navigator + Catchfish + Fishnet)
- The factory **produces** domain-specific Santiagos on-demand
- "Santiago-PM" and "Santiago-Cardiologist" are **catches**, not hard-coded roles

#### Change 4: Knowledge Storage is the Catch

**Original Plan:**
- `knowledge/shared/` for team working agreements
- `knowledge/domains/` for role-specific expertise

**Revised:**
- `knowledge/catches/` for fishing expedition results
- Each catch includes: domain knowledge (markdown), BDD tests, MCP manifest, provenance
- Provenance tracks: sources, conversion date, catchfish version, validation cycles, quality score

#### Change 5: MCP Manifests are Derived, Not Declared

**Original Plan:**
```json
// Hand-written mcp/manifests/pm.json
{
  "role": "PM",
  "skill_level": "Master",
  "tools": ["read_working_agreements", "propose_evolution_cycle"]
}
```

**Revised:**
```python
# Auto-generated from BDD tests
def generate_mcp_manifest(bdd_tests, domain_knowledge):
    tools = fishnet.infer_tools_from_scenarios(bdd_tests)
    # "Given PM evaluates backlog" → tool: "evaluate_backlog"
    
    skill_level = assess_complexity(domain_knowledge)
    # SAFe + XP = "Master"; Basic Scrum = "Journeyman"
    
    return auto_generate_manifest(tools, skill_level)
```

## Revised Migration Priorities

### Phase 1: Build the Factory (Milestone 1-2)

**Goal:** Implement Navigator + Catchfish + Fishnet pipeline

- [ ] Implement `nusy_orchestrator/santiago_builder/catchfish.py`
  - Core extraction: raw source → 4-layer markdown
  - Optimize the 30-60m bottleneck
  - Support multiple source formats (PDF, API, web scraping)
  
- [ ] Implement `nusy_orchestrator/santiago_builder/fishnet.py`
  - Generate BDD tests from knowledge graph
  - Infer MCP tools from test scenarios
  
- [ ] Implement `nusy_orchestrator/santiago_builder/navigator.py`
  - Orchestrate 10-step fishing process
  - Quality validation loop (3-5 cycles until threshold met)
  - Provenance tracking
  
- [ ] Create `knowledge/templates/santiago-template/`
  - Base structure for generated Santiagos
  - MCP manifest template
  
- [ ] Create `knowledge/catches/` directory structure

**Acceptance Criteria:**
- End-to-end fishing expedition: raw sources → deployed MCP service
- One sample catch: `santiago-pm-safe-xp` generated and validated
- Quality threshold: 95%+ BDD test pass rate after ≤5 cycles

### Phase 2: Optimize Catchfish (Milestone 3)

**Goal:** Reduce knowledge extraction time from 30-60m to <15m

- [ ] Semi-automated first-pass extraction with human validation
- [ ] Template-based scaffolding for 4-layer structure
- [ ] Incremental refinement based on test failures
- [ ] Provenance tracking for every extraction decision

### Phase 3: Production Infrastructure (Milestone 4-6)

**Goal:** Deploy factory and support multiple concurrent fishing expeditions

- [ ] NuSy orchestrator with fishing expedition API
- [ ] Session management for concurrent expeditions
- [ ] DGX deployment for model serving (shared Mistral-7B-Instruct)
- [ ] Ethics gating for source validation and quality thresholds

### Phase 4: Self-Improvement (Milestone 7+)

**Goal:** Factory improves itself through learning

- [ ] Log all fishing expeditions (Step 10)
- [ ] Analyze: Which sources convert fastest? Which patterns work best?
- [ ] Evolve Catchfish algorithms based on learning
- [ ] Santiago-PM manages the factory's own development

## What We Got Wrong in Original Plan

1. **Built agents, not factory** — Focused on hand-crafting PM, Ethicist, Architect roles
2. **Missed Catchfish centrality** — Didn't recognize the 30-60m knowledge extraction as the core innovation
3. **Pre-authored knowledge** — Assumed `knowledge/domains/` would be manually written
4. **Static MCP manifests** — Hand-wrote capability declarations instead of auto-generating
5. **Team metaphor dominated** — "Santiago team" obscured the factory pattern
6. **Missed the clinical prototype insight** — The 30-60m per guideline + 3 validation cycles is the ACTUAL architecture

## Success Metrics (Revised)

1. **Time to Fish:** Minutes from user request to deployed Santiago MCP service
   - Target: 45 minutes for small domain (1-2 sources)
   - Target: 2 hours for medium domain (5-10 sources)

2. **Catch Quality:** BDD test pass rate after fishing expedition
   - Target: ≥95% pass rate within 5 validation cycles

3. **Factory Reuse:** Number of distinct Santiagos caught
   - Target: 10 domain-specific Santiagos in first 6 months

4. **Catchfish Efficiency:** Knowledge extraction time per source
   - Baseline: 30-60m (clinical prototype)
   - Target: <15m through automation

5. **Self-Improvement:** Factory learns from each expedition
   - Measure: Catchfish efficiency improves over time
   - Measure: Validation cycles decrease (fewer refinements needed)

## References

- Clinical guidelines prototype: 30-60m per guideline conversion + 3 validation cycles
- "Old Man and the Sea" metaphor: `santiago-pm/strategic-charts/Old man and the sea.md`
- Original architecture plan: `ARCHITECTURE_PLAN.md` (commit a86c0b2)
