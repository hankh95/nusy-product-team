# Recommendations for Prompt & Context Improvements

**Goal:** Help AI models discover the "Santiago Factory" pattern on first pass instead of assuming hand-built agents.

## Problem Analysis

All AI models (including Claude Sonnet 4.5) made the same error:
1. Read research docs mentioning Santiago-PM, Santiago-Ethicist, roles, etc.
2. Assumed these are **pre-built agents** requiring manual implementation
3. Missed that Santiago is a **template** for generating domain-specific agents
4. Didn't connect the clinical prototype (30-60m conversion + 3 cycles) to the core architecture

## Recommended Changes

### 1. Update Architecture Redux Prompt v2

**Add to "Mission" Section (after step 1):**

```markdown
## CRITICAL ARCHITECTURAL INSIGHT

Before proceeding, understand this fundamental pattern:

**Santiago is NOT a set of pre-built agents (PM, Ethicist, Architect, etc.).**

Santiago is a **FACTORY** that generates domain-specific agents on-demand through a "fishing expedition" process. When someone says "Create a Santiago who knows cardiology," the system:

1. Gathers raw materials (clinical guidelines, research papers)
2. Runs Catchfish to convert raw sources → structured 4-layer knowledge (30-60m per source)
3. Runs Fishnet to generate BDD tests validating the knowledge
4. Runs Navigator to orchestrate validation cycles (typically 3) until quality threshold met
5. Deploys as an MCP service with auto-generated manifest

**Key Evidence:**
- The clinical prototype converted guidelines to 4-layer models in 30-60m each
- 3 validation cycles were needed to reach quality threshold
- The system loaded all converted knowledge in-memory and answered questions in real-time
- This workflow is the ACTUAL architecture, not a one-time prototype

**Therefore:**
- Your plan should focus on building the **factory** (Navigator, Catchfish, Fishnet)
- NOT on manually authoring `knowledge/domains/pm/`, `knowledge/domains/ethics/`, etc.
- Santiago-PM and Santiago-Cardiologist are **generated outputs**, not hardcoded roles
```

### 2. Create a Mandatory Pre-Reading Document

**Location:** `ocean-research/ARCHITECTURE_PATTERN.md`

```markdown
# The Santiago Factory Pattern - READ THIS FIRST

## What This System Actually Does

NuSy does NOT build a fixed team of AI agents (PM, Ethicist, Architect).

NuSy builds a **factory** that generates domain-specific AI agents on-demand.

## Real-World Example

User: "I need a Santiago who understands AHA stroke guidelines and can answer questions about treatment protocols."

System: 
1. Downloads AHA stroke guideline PDFs
2. Runs **Catchfish** to extract structured knowledge (30-60m)
3. Builds knowledge graph from extracted facts and rules
4. Generates **Fishnet** BDD tests to validate knowledge
5. Runs **Navigator** validation cycles until 95%+ tests pass
6. Deploys `santiago-cardiologist-aha` as an MCP service

Total time: ~2 hours
Output: A working MCP service that can answer stroke protocol questions

## The Factory Components

- **Navigator**: Orchestrates the 10-step fishing process
- **Catchfish**: Converts raw sources → 4-layer structured knowledge
- **Fishnet**: Generates BDD tests from knowledge graph
- **Santiago Template**: Base structure for any generated Santiago

## What You Should Design

1. The factory infrastructure (Navigator, Catchfish, Fishnet)
2. The 4-layer knowledge extraction pipeline (optimize the 30-60m bottleneck)
3. The validation loop (3-5 cycles until quality threshold)
4. Storage for "catches" (generated Santiagos)
5. Auto-generation of MCP manifests from BDD tests

## What You Should NOT Design

1. Manually authored `knowledge/domains/pm/` folders
2. Hand-written MCP manifests for specific roles
3. A fixed team of Santiago-PM, Santiago-Ethicist, etc.
4. Pre-defined agent capabilities

These emerge FROM the factory, not before it.
```

**Update prompt to require reading this:**

```markdown
1. Load the repo root (`nusy-product-team`). **Before scanning any code:**
   - **MUST READ:** `ocean-research/ARCHITECTURE_PATTERN.md` — explains the factory pattern
   - Then scan at minimum:
     - `santiago-pm/strategic-charts/Old man and the sea.md` — the fishing process metaphor
     - Clinical prototype evidence (30-60m conversion time, 3 validation cycles)
```

### 3. Add Explicit Anti-Patterns Section to Prompt

**Add to "Behavioral Guardrails" Section:**

```markdown
## Anti-Patterns to Avoid

❌ **DON'T:** Design manual authoring of `knowledge/domains/pm/core-practices.md`
✅ **DO:** Design Catchfish to auto-generate this from source materials

❌ **DON'T:** Hand-write MCP manifests for Santiago-PM, Santiago-Ethicist
✅ **DO:** Design auto-generation of manifests from BDD test analysis

❌ **DON'T:** Plan to "implement Santiago-PM agent with these tools..."
✅ **DO:** Plan to "implement factory that can generate Santiago-PM when requested"

❌ **DON'T:** Focus on team coordination (PM → Dev → QA handoffs)
✅ **DO:** Focus on factory optimization (reduce 30-60m Catchfish time to <15m)

❌ **DON'T:** Treat Santiago-PM as a separate service to code
✅ **DO:** Treat Santiago-PM as an example output of the factory
```

### 4. Restructure ocean-research/ Directory

**Current Problem:** Research docs scattered, "Old Man and the Sea" is buried in `santiago-pm/strategic-charts/`

**Proposed Structure:**

```
ocean-research/
  00-START-HERE.md                    # ← NEW: "You are building a factory"
  ARCHITECTURE_PATTERN.md             # ← NEW: Detailed factory explanation
  clinical-prototype-findings.md      # ← NEW: Extract 30-60m insight
  
  fishing-process/
    old-man-and-the-sea.md            # ← Moved from santiago-pm/
    catchfish-specification.md        # ← NEW: Detailed Catchfish design
    fishnet-specification.md          # ← NEW: Detailed Fishnet design
    navigator-specification.md        # ← NEW: Detailed Navigator design
  
  deployment/
    dgx_spark_nusy_report.md
    nusy_manolin_architecture.md
    ...
```

**Update prompt to read in order:**

```markdown
2. Digest research under `ocean-research/` **in this order**:
   a. `00-START-HERE.md` — factory pattern overview
   b. `ARCHITECTURE_PATTERN.md` — detailed factory explanation
   c. `clinical-prototype-findings.md` — evidence (30-60m, 3 cycles)
   d. `fishing-process/old-man-and-the-sea.md` — 10-step metaphor
   e. DGX/Manolin specs — deployment targets
```

### 5. Add Concrete Factory Example to Prompt

**Add to "Output Expectations" Section:**

```markdown
## Example: What "Factory-First" Looks Like

Instead of this (agent-first thinking):

> "Milestone 2: Implement Santiago-PM MCP Service
> - Write `knowledge/domains/pm/hypothesis-patterns.md`
> - Create MCP manifest declaring PM tools
> - Implement PM agent class"

Write this (factory-first thinking):

> "Milestone 2: Implement Catchfish Knowledge Extraction
> - Input: Raw sources (PDFs, APIs, docs)
> - Output: 4-layer structured markdown
> - Optimization target: Reduce 30-60m to <15m
> - Example: Process 'SAFe Framework v6.pdf' → `safe-patterns-4layer.md`"

The PM knowledge emerges FROM Catchfish processing SAFe sources, not from manual authoring.
```

### 6. Create a Validation Checklist in Prompt

**Add to "Submission Checklist" Section:**

```markdown
## Factory Pattern Validation

Before submitting your plan, verify:

- [ ] Your ARCHITECTURE_PLAN describes Navigator, Catchfish, Fishnet as core components
- [ ] Your MIGRATION_STEPS prioritize building the factory (not individual agents)
- [ ] Your FOLDER_LAYOUT includes `knowledge/catches/` (generated Santiagos) not `knowledge/domains/pm/` (pre-authored)
- [ ] Your migration mentions optimizing the "30-60m knowledge extraction bottleneck"
- [ ] Your plan treats MCP manifests as auto-generated outputs, not hand-written artifacts
- [ ] You reference the clinical prototype findings (30-60m, 3 cycles, real-time query)
- [ ] You explain how Santiago-PM would be **generated** via factory, not **implemented** as code

If any of these are false, you've missed the factory pattern. Re-read `ocean-research/ARCHITECTURE_PATTERN.md`.
```

### 7. Strengthen "Independence & Calibration" Section

**Current Text:**
```markdown
- Independence: Do not read any prior outputs in `ocean-arch-redux/` until all deliverables above are drafted.
```

**Enhanced Text:**
```markdown
- Independence: Do not read any prior outputs in `ocean-arch-redux/` until all deliverables above are drafted.
- Factory Pattern Check: Before finalizing, verify you understood the factory pattern by answering:
  1. "Is Santiago a fixed set of agents or a template for generating agents?" (Answer: template)
  2. "What is Catchfish and why is it central?" (Answer: Converts raw sources → 4-layer knowledge in 30-60m)
  3. "Where does Santiago-PM's knowledge come from?" (Answer: Generated via Catchfish from PM methodology sources)
  
  If your answers don't match, re-read `ocean-research/ARCHITECTURE_PATTERN.md` and revise.
```

## Summary of Changes

| Change | Impact | Effort |
|--------|--------|--------|
| 1. Add "CRITICAL INSIGHT" to prompt | High - immediate framing | 5 min |
| 2. Create `ARCHITECTURE_PATTERN.md` | High - mandatory reading | 15 min |
| 3. Add anti-patterns section | Medium - clarifies mistakes | 10 min |
| 4. Restructure ocean-research/ | Medium - better organization | 20 min |
| 5. Add factory example to prompt | Medium - concrete guidance | 10 min |
| 6. Add validation checklist | High - forces self-check | 5 min |
| 7. Strengthen independence section | Low - minor improvement | 5 min |

**Recommended Priority:**
1. Create `ARCHITECTURE_PATTERN.md` (15 min) - **Most important**
2. Update prompt with "CRITICAL INSIGHT" section (5 min)
3. Add validation checklist to prompt (5 min)
4. Add anti-patterns section (10 min)
5. Remaining changes as time permits

**Total time to implement high-priority changes: ~35 minutes**

This should dramatically increase the probability that AI models discover the factory pattern on first pass.
