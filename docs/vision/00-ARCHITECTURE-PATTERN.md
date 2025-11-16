# The Santiago Factory Architecture — READ THIS FIRST

**Last Updated:** 2025-11-16  
**Critical:** Read this document BEFORE scanning any code or making architectural decisions.

---

## What You're Actually Building

You are NOT building a fixed team of AI agents (PM, Ethicist, Architect, Developer, QA, UX, Platform).

You ARE building a **self-bootstrapping Santiago factory** that:
1. Starts with "fake" Santiagos (proxies to external AI APIs)
2. Uses fake Santiagos to build the factory infrastructure
3. Uses the factory to generate real domain-specific Santiagos
4. Progressively replaces fake Santiagos with real ones
5. Eventually has real Santiagos maintaining and improving the factory itself

---

## The Bootstrapping Sequence

### Phase 0: Hire Contractors (Weeks 1-2)

**Problem:** You need a development team to build the factory, but the factory is what produces the team!

**Solution:** Create "fake team" — thin MCP wrappers that proxy to external AI APIs:

```python
# santiago_core/agents/_proxy/pm_proxy.py
class FakeSantiagoPM:
    """Temporary contractor until real Santiago-PM is caught"""
    def invoke_tool(self, request):
        instructions = load("knowledge/proxy-instructions/pm-role.md")
        return openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": request}
            ]
        )
```

**Key Characteristics:**
- Minimal code (just MCP endpoint + API call)
- Fast to deploy (hours, not weeks)
- Expensive to run (API costs per request)
- **Purpose:** Build the factory, then get replaced

**Not a Fallback:** This isn't what you do if DGX is delayed. This is **Phase 0 of every Santiago deployment**, always.

---

### Phase 1: Build the Shipyard (Weeks 3-6)

**Task:** The fake team implements the factory infrastructure

The fake team treats factory-building as a regular development project:

1. **Fake Santiago-PM** writes hypothesis: "If we build Catchfish, we can extract structured knowledge from sources in <60m"
2. **Fake Santiago-PM** writes BDD scenarios for factory behavior
3. **Fake Santiago-Architect** designs Navigator, Catchfish, Fishnet components
4. **Fake Santiago-Developer** implements the Python code
5. **Fake Santiago-QA** validates with test cases
6. **Iterate** until factory is operational

**Deliverables:**
- `nusy_orchestrator/santiago_builder/navigator.py` — Orchestrates fishing expeditions
- `nusy_orchestrator/santiago_builder/catchfish.py` — Extracts knowledge from sources (30-60m → <15m optimization target)
- `nusy_orchestrator/santiago_builder/fishnet.py` — Generates BDD tests from knowledge graph

**Why this works:** Fake team runs on powerful external models (GPT-4, Claude Opus) so development is FAST.

---

### Phase 2: Catch the First Real Santiago (Weeks 7-8)

**Hypothesis:** "A factory-generated Santiago-PM will match or exceed the fake Santiago-PM's capabilities while eliminating API costs."

**Process:**
1. Gather PM domain sources (SAFe Framework PDF, Extreme Programming book, Lean Startup)
2. Run factory:
   - Navigator orchestrates
   - Catchfish extracts structured knowledge → 4-layer markdown
   - Build knowledge graph
   - Fishnet generates BDD tests
   - Validate until ≥95% pass rate (typically 3-5 cycles)
3. Deploy as `santiago-pm-safe-xp` MCP service
4. **A/B test:** Run same 10 PM tasks through fake vs real Santiago
5. **If real ≥ 90% of fake performance → replace the proxy**
6. Route all PM requests to santiago-pm-safe-xp, deprecate fake Santiago-PM

**Outcome:**
- First contractor replaced with permanent worker
- Factory validated with real catch
- API costs reduced by 1/7th (one of seven roles replaced)

---

### Phase 3: Progressive Replacement (Weeks 9-20)

**Strategy:** Don't replace all at once—each replacement is an experiment

Repeat Phase 2 for each role:
- Santiago-Architect-NuSy (ontology expert)
- Santiago-Architect-Systems (infrastructure expert)
- Santiago-Developer-Python (coding expert)
- Santiago-QA-Testing (test automation expert)
- Santiago-UX-Research (user experience expert)
- Santiago-Platform (deployment/operations expert)

**Decision Logic:** Replace if Real ≥ Fake on A/B tests, otherwise keep fake team member

**Possible Outcomes:**
- Some roles fully replaced (e.g., PM, Developer)
- Some roles kept as fake (e.g., if sources insufficient or external models significantly better)
- Hybrid team during transition

---

### Phase 4: Self-Sustaining Shipyard (Week 20+)

**Characteristics:**
- All (or most) contractors replaced with real Santiagos
- Real Santiago-PM proposes factory improvements as hypotheses
- Real Santiago-Architect designs enhancements
- Real Santiago-Developer implements changes
- **Factory improves itself** through self-directed experiments

**Examples:**
- Real Santiago-PM: "Hypothesis: If we parallelize Catchfish extraction, time drops from 30m to 10m"
- Real Santiago-Developer implements parallel processing
- Real Santiago-QA validates improvement
- Factory now generates Santiagos 3x faster

**Ultimate Goal:** Zero external API dependency, self-improving system, can generate Santiagos for any domain on demand.

---

## The Clinical Prototype: Evidence for This Architecture

**What Happened:**
- Converted clinical guidelines to 4-layer structured knowledge
- **30-60 minutes per guideline** (the actual conversion time)
- **3 validation cycles** needed to reach quality threshold (23 clinical scenarios)
- Once converted, system loaded all guidelines in-memory and answered questions in real-time

**What This Proves:**
1. **Catchfish is viable** — Knowledge extraction works, but needs optimization
2. **30-60m is the bottleneck** — This is where you optimize
3. **3 validation cycles is the pattern** — Navigator's quality loop works
4. **In-memory domain knowledge works** — No need for complex retrieval at runtime

**Architectural Implication:**
This workflow (extract → validate → deploy) IS the factory. The prototype proved the factory works; now you industrialize it.

---

## The "Old Man and the Sea" Fishing Process

Located in: `santiago-pm/strategic-charts/Old man and the sea.md`

**The 10 Steps:**

1. **Vision**: What does this Santiago need to do? (MCP services, behaviors)
2. **Raw Materials**: Collect sources (PDFs, APIs, docs, expert interviews)
3. **Catchfish**: Process raw materials → structured 4-layer knowledge
4. **Indexing**: Make knowledge highly referenceable
5. **Ontology Loading**: Apply naming conventions, models, schemas
6. **KG Building**: Store structured knowledge in knowledge graph
7. **Fishnet**: Generate BDD tests to validate KG and MCP services
8. **Navigator**: Orchestrate validation cycles until quality threshold met
9. **Deployment**: Generate MCP manifest, deploy as service
10. **Learning**: Use logs and metrics to improve the fishing process

This isn't a metaphor—it's the **literal sequence** the factory executes for each Santiago catch.

---

## Santiago-PM Folder Structure: Development Patterns

The `santiago-pm/` folder structure isn't just documentation—it teaches the **pattern the fake team follows**:

### `santiago-pm/expeditions/`
Experiment logs following hypothesis-driven development:
- Hypothesis → Experiment → Result
- Example: "If we implement queued KG writes, conflicts reduce by 80%"
- This is how fake team improves the factory

### `santiago-pm/tackle/`
Implementation modules (analogous to factory components):
- Modular, testable, incrementally deliverable
- Example: "Status tackle" = one feature with BDD tests
- This is how fake team structures factory code

### `santiago-pm/voyage-trials/`
Test scenarios (analogous to factory validation):
- BDD-style scenarios testing system behavior
- Example: "Given PM proposes feature, when validated, then backlog updated"
- This is how fake team validates factory works

### `santiago-pm/strategic-charts/`
Vision and direction documents:
- "Old Man and the Sea" = the fishing process metaphor
- "Santiago Trains Manolin" = the bootstrapping vision
- This is what fake team PM uses to guide factory development

**Key Insight:** These aren't just docs for humans to read. They're **training material for the fake team** on how to build and operate the factory.

---

## What You Should Design

### Priority 1: Fake Team Infrastructure (Phase 0)
- MCP proxy services for each role (PM, Architect, Developer, QA)
- Role instruction templates (what each proxy does)
- API integration (OpenAI, Claude, Copilot)
- MCP protocol coordination between fake team members

### Priority 2: Factory Components (Phase 1)
- **Navigator**: Orchestrates 10-step fishing process
- **Catchfish**: Extracts structured knowledge from sources (optimize 30-60m → <15m)
- **Fishnet**: Generates BDD tests from knowledge graph
- Quality validation loop (3-5 cycles until threshold)
- Provenance tracking (sources, dates, versions)

### Priority 3: Catch Storage & Deployment (Phase 2)
- `knowledge/catches/` directory structure
- Generated Santiago MCP service template
- A/B testing framework (fake vs real comparison)
- Progressive replacement strategy

### Priority 4: Self-Improvement Infrastructure (Phase 4)
- Factory improvement proposals (hypotheses)
- Real Santiago coordination patterns
- Learning from fishing expedition logs

---

## What You Should NOT Design

❌ Manually authored `knowledge/domains/pm/core-practices.md`  
✅ Catchfish auto-generates this from SAFe/XP sources

❌ Hand-written MCP manifests for specific roles  
✅ Fishnet auto-generates manifests from BDD test analysis

❌ Implementation of Santiago-PM agent class  
✅ Factory generates santiago-pm-safe-xp as a catch

❌ Fixed team coordination (PM → Dev → QA handoffs)  
✅ Fake team coordination via MCP, later replaced by real Santiagos

❌ Pre-defined agent capabilities  
✅ Capabilities discovered from sources during fishing expedition

---

## Architecture Validation Checklist

Before submitting your architecture plan, verify:

- [ ] Your plan starts with **Phase 0: Fake Team** (proxy MCP services to external APIs)
- [ ] Fake team **builds the factory** (not humans writing Python manually)
- [ ] Factory's **first catch replaces** a fake team member (progressive replacement)
- [ ] You reference **clinical prototype** (30-60m conversion, 3 validation cycles)
- [ ] You reference **"Old Man and the Sea"** 10-step fishing process
- [ ] You explain how **santiago-pm/ folder structure** teaches development patterns
- [ ] Your milestones reflect **4 phases** (Fake Team → Factory → First Catch → Progressive Replacement)
- [ ] You mention **A/B testing** fake vs real Santiagos before replacement
- [ ] You describe **self-improvement** (real Santiagos eventually improve factory)
- [ ] You optimize **Catchfish** (the 30-60m bottleneck, not pre-authoring domains)

If any are missing, re-read this document and revise.

---

## Common Mistakes to Avoid

### Mistake 1: "Build Santiago-PM first, then factory"
**Wrong:** Treating roles as prerequisites  
**Right:** Build fake team (hours) → fake team builds factory (weeks) → factory catches real Santiagos

### Mistake 2: "Fake team is a fallback if DGX delayed"
**Wrong:** Treating proxies as contingency plan  
**Right:** Fake team is Phase 0, always. It's the bootstrapping mechanism.

### Mistake 3: "Manually author domain knowledge for PM"
**Wrong:** Writing `knowledge/domains/pm/` by hand  
**Right:** Catchfish generates it from SAFe/XP sources during fishing expedition

### Mistake 4: "Focus on MCP infrastructure, orchestrator, ethics gating"
**Wrong:** Generic distributed systems concerns  
**Right:** Focus on Catchfish (30-60m extraction), Fishnet (BDD generation), Navigator (validation loop)

### Mistake 5: "Build all Santiagos, then deploy"
**Wrong:** Big-bang replacement  
**Right:** Progressive replacement via A/B testing experiments

---

## Success Criteria

### Phase 0 Success:
- Fake team operational in <1 week
- Can coordinate via MCP to complete compound tasks
- Fake PM writes hypothesis, fake Architect designs, fake Developer implements

### Phase 1 Success:
- Factory operational in <6 weeks (using fake team)
- End-to-end fishing expedition: PDF → deployed MCP service
- First test catch validates viability

### Phase 2 Success:
- First real Santiago (PM) replaces fake Santiago-PM
- A/B test shows ≥90% performance parity
- API costs reduced by 1/7th (one role replaced)

### Phase 3 Success:
- All (or most) contractors replaced with real Santiagos
- System runs on DGX without external API dependency (or minimal)
- Factory can generate new domain Santiagos on demand

### Phase 4 Success:
- Real Santiagos propose and implement factory improvements
- Catchfish time reduced from 30-60m to <15m through self-optimization
- System generates Santiagos for new domains (finance, legal, healthcare)

---

## Key References

- **Fake Team Strategy**: `ocean-research/fake_team_pack/`
- **Fishing Process**: `santiago-pm/strategic-charts/Old man and the sea.md`
- **Development Patterns**: `santiago-pm/expeditions/`, `santiago-pm/tackle/`, `santiago-pm/voyage-trials/`
- **Clinical Prototype**: Evidence of 30-60m conversion time, 3 validation cycles
- **DGX Deployment**: `ocean-research/building-on-DGX/dgx_spark_nusy_report.md`
- **Concurrency Testing**: `ocean-research/nusy_manolin_multi_agent_test_plans.md`

---

**You are building a self-bootstrapping AI factory. Start with fake team, build factory, catch real Santiagos, achieve self-improvement. This is the way.**
