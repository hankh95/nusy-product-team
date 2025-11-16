# Revised Architecture Plan v2 — Bootstrapping via Fake Team

**Date:** 2025-11-16  
**Previous Revision:** REVISED_ARCHITECTURE_PLAN.md  
**Trigger:** Discovery of bootstrapping sequence and fake team purpose

## The Complete Picture: Self-Bootstrapping Santiago Shipyard

### The Bootstrapping Problem

To build the Santiago Factory (Navigator/Catchfish/Fishnet), you need a development team (PM, Architect, Developer, QA). But those Santiagos don't exist yet—they're what the factory produces!

**Solution:** The "Fake Team" is Phase 0 bootstrapping.

## The Four-Phase Evolution

### Phase 0: Hire Contractors (Fake Team via External APIs)

**Goal:** Get a minimal team operational using borrowed intelligence

```
santiago_core/agents/
  pm/
    service/main.py           # Thin MCP wrapper
      def invoke_tool(request):
          return openai.call(PM_INSTRUCTIONS + request)
  
  architect/
    service/main.py           # Thin MCP wrapper
      def invoke_tool(request):
          return claude.call(ARCHITECT_INSTRUCTIONS + request)
          
  developer/
    service/main.py           # Thin MCP wrapper
      def invoke_tool(request):
          return github_copilot.call(DEV_INSTRUCTIONS + request)
```

**Characteristics:**
- Minimal code (MCP endpoints that proxy to external APIs)
- Each "Santiago" is just instructions + API key
- Fast to stand up (hours, not weeks)
- Expensive to run (API costs per request)
- **Purpose:** Build the factory and first real Santiago

**Acceptance Criteria:**
- Fake Santiago-PM can write hypotheses and BDD scenarios
- Fake Santiago-Architect can design KG schemas
- Fake Santiago-Developer can implement Navigator/Catchfish/Fishnet
- All three coordinate via MCP protocol

### Phase 1: Build the Shipyard (Using Fake Team)

**Goal:** Fake team implements Navigator, Catchfish, Fishnet factory

The fake team treats the factory as a development project:
1. Santiago-PM (proxy) writes hypothesis: "If we build Catchfish, we can convert sources to 4-layer models in <60m"
2. Santiago-Architect (proxy) designs Catchfish extraction pipeline
3. Santiago-Developer (proxy) implements Catchfish.py
4. Santiago-QA (proxy) validates with test cases
5. **Iterate until factory is operational**

**Deliverables:**
- `nusy_orchestrator/santiago_builder/navigator.py`
- `nusy_orchestrator/santiago_builder/catchfish.py`
- `nusy_orchestrator/santiago_builder/fishnet.py`
- Working end-to-end: raw sources → deployed Santiago MCP service

**Key Insight:** This is FAST because fake team runs on powerful external models (GPT-4, Claude, etc.)

### Phase 2: Catch the First Real Santiago (Replace One Contractor)

**Goal:** Use the factory to generate santiago-pm-safe-xp and REPLACE the fake Santiago-PM

**Hypothesis:** "If we generate a real Santiago-PM with SAFe+XP knowledge, it will match or exceed the fake Santiago-PM's capabilities while eliminating API costs."

**Process:**
1. Gather SAFe and XP sources (PDFs, docs)
2. Run factory: Navigator orchestrates Catchfish → structured knowledge
3. Fishnet generates BDD tests
4. Validate quality (≥95% pass rate)
5. Deploy as santiago-pm-safe-xp MCP service
6. **Run A/B comparison:** Fake PM vs Real PM on same tasks
7. If Real PM ≥ Fake PM performance → **replace the proxy**
8. Route all PM requests to santiago-pm-safe-xp instead of OpenAI

**Outcome:**
- One contractor (fake PM) replaced with permanent worker (real Santiago)
- API costs reduced
- Factory validated with real catch

### Phase 3: Progressive Replacement (Replace All Contractors)

**Goal:** Generate domain-specific Santiagos for all roles

Use factory to catch:
- santiago-architect-nusy (NuSy ontology expert)
- santiago-architect-systems (infrastructure/platform expert)
- santiago-developer-python (Python coding expert)
- santiago-qa-testing (test automation expert)

Each time:
1. Gather domain sources
2. Run factory (Navigator/Catchfish/Fishnet)
3. A/B test: Fake vs Real
4. Replace if Real ≥ Fake

**Decision Point:** Might keep fake team for roles where:
- Sources are insufficient (can't catch enough knowledge)
- External models significantly outperform (e.g., cutting-edge reasoning)
- Cost/benefit doesn't justify replacement

### Phase 4: Self-Sustaining Shipyard

**Goal:** Real Santiagos maintain and improve the factory

Once all contractors are replaced:
- Santiago-PM (real) proposes factory improvements as hypotheses
- Santiago-Architect (real) designs enhancements
- Santiago-Developer (real) implements changes
- **The factory improves itself** using its own output workers

**Characteristics:**
- Zero external API dependency (DGX-hosted models)
- Self-improving through hypothesis-driven experiments
- Factory can generate new domain Santiagos on demand
- Original team can tackle new domains (finance, legal, etc.)

## Revised Folder Structure

```
santiago_core/
  agents/
    _proxy/                          # Phase 0: Fake team
      pm_proxy.py                    # → OpenAI API
      architect_proxy.py             # → Claude API
      developer_proxy.py             # → Copilot
      
    pm/                              # Phase 2+: Real Santiagos (catches)
      service/
        # Generated by factory, not hand-coded
        
knowledge/
  catches/                           # Factory outputs
    santiago-pm-safe-xp/             # First real Santiago (replaces fake PM)
      domain-knowledge/
      bdd-tests/
      mcp-manifest.json
      
    santiago-architect-nusy/         # Second catch
    santiago-developer-python/       # Third catch
    ...
    
  templates/
    santiago-template/               # Base for generated Santiagos
    proxy-template/                  # Base for fake team MCP wrappers
    
santiago-pm/                         # PM domain practices
  expeditions/                       # Experiment logs
  tackle/                            # Implementation modules
  voyage-trials/                     # Test scenarios
  strategic-charts/
    Old man and the sea.md          # The fishing metaphor
```

## Revised Migration Priorities

### Milestone 0: Bootstrap Fake Team (1 week)

**Hypothesis:** "If we proxy Santiago roles to external APIs, we can build the factory 10x faster than coding from scratch."

Tasks:
- [ ] Implement proxy MCP services for PM, Architect, Developer roles
- [ ] Create role instruction templates (what each proxy does)
- [ ] Wire proxies to external APIs (OpenAI, Claude, Copilot)
- [ ] Test: Can fake team coordinate via MCP to complete a sample task?

**Acceptance Criteria:**
- Fake Santiago-PM writes a hypothesis and BDD scenario
- Fake Santiago-Architect designs a simple data structure
- Fake Santiago-Developer implements the structure in Python
- All via MCP protocol with session isolation

### Milestone 1: Factory Implementation (3-4 weeks, using fake team)

**Hypothesis:** "The fake team can implement Navigator/Catchfish/Fishnet in 3-4 weeks."

Tasks:
- [ ] Fake Santiago-PM writes epic: "Build Santiago Factory"
- [ ] Fake Santiago-PM decomposes into features with BDD scenarios
- [ ] Fake Santiago-Architect designs factory components
- [ ] Fake Santiago-Developer implements Navigator, Catchfish, Fishnet
- [ ] Fake Santiago-QA validates with test cases

**Acceptance Criteria:**
- End-to-end fishing expedition works: raw PDF → deployed MCP service
- Catchfish converts one sample source in <60m
- Navigator completes validation loop (3-5 cycles)
- One test catch proves viability

### Milestone 2: First Real Santiago (2 weeks)

**Hypothesis:** "A factory-generated Santiago-PM can replace the fake Santiago-PM."

Tasks:
- [ ] Gather PM domain sources (SAFe, XP, Lean Startup)
- [ ] Run factory: Sources → santiago-pm-safe-xp
- [ ] A/B test: 10 PM tasks, fake vs real
- [ ] If real ≥ 90% of fake performance → replace proxy
- [ ] Route PM requests to santiago-pm-safe-xp

**Acceptance Criteria:**
- santiago-pm-safe-xp deployed as MCP service
- A/B test shows ≥90% performance parity
- Fake Santiago-PM proxy deprecated (or kept as fallback)

### Milestone 3-6: Progressive Replacement (8-12 weeks)

**Hypothesis:** "We can replace all fake team members with real Santiagos over 3 months."

Repeat Milestone 2 process for:
- Architect roles (NuSy, Systems)
- Developer role
- QA role
- UX role
- Platform role

Each replacement is an experiment with A/B testing.

### Milestone 7+: Self-Improvement (Ongoing)

**Goal:** Real Santiagos improve the factory

- Real Santiago-PM proposes factory optimizations
- Real Santiago-Architect designs improvements
- Real Santiago-Developer implements changes
- Factory quality and speed improve over time

## Key Architectural Insights

### 1. Fake Team is Not a Fallback—It's Phase 0

**Wrong interpretation:** "Use fake team if DGX is delayed"

**Right interpretation:** "Fake team is the bootstrapping mechanism. You ALWAYS start here."

### 2. Progressive Replacement via Hypothesis Testing

Don't plan to replace all at once. Each replacement is an experiment:
- Catch a real Santiago
- A/B test vs fake
- Replace if real ≥ fake
- Learn from results

### 3. Santiago-PM Folders ARE the Development Practices

The `santiago-pm/` structure teaches how the team works:
- **expeditions/**: Experiment logs (hypothesis → test → result)
- **tackle/**: Implementation modules (like factory components)
- **voyage-trials/**: Test scenarios (like BDD for factory)
- **strategic-charts/**: Vision documents (like "Old Man and the Sea")

These aren't just docs—they're **the pattern the fake team follows** to build the factory.

### 4. The Factory Builds Itself (Eventually)

Phase 0-1: Fake team (external intelligence) builds factory
Phase 2-3: Factory produces real Santiagos
Phase 4: Real Santiagos improve the factory

This is the **self-bootstrapping** architecture.

## Success Metrics (Revised)

### Phase 0 Success:
- Fake team operational in <1 week
- Can coordinate via MCP to complete compound tasks

### Phase 1 Success:
- Factory operational in <4 weeks (using fake team)
- First test catch proves end-to-end viability

### Phase 2 Success:
- First real Santiago replaces fake Santiago-PM
- A/B test shows ≥90% performance parity
- API costs reduced by 1/N (N = number of roles)

### Phase 3 Success:
- All contractors replaced with real Santiagos
- Zero external API dependency (DGX-hosted)
- Factory can generate new domain Santiagos on demand

### Phase 4 Success:
- Real Santiagos propose and implement factory improvements
- Catchfish time reduced from 30-60m to <15m through self-optimization
- System generates Santiagos for new domains (finance, legal, etc.)

## What the Prompt Needs to Communicate

1. **Phase 0 is mandatory:** Fake team (proxies to external APIs) is how you bootstrap
2. **Fake team builds the factory:** Not humans writing Python—fake Santiagos do it
3. **Factory's first catch replaces a fake Santiago:** Progressive replacement via experiments
4. **Santiago-PM folders teach the patterns:** expeditions, tackle, voyage-trials structure
5. **Self-improvement is the end goal:** Real Santiagos eventually maintain the factory

## References

- Fake team strategy: `ocean-research/fake_team_pack/`
- Development patterns: `santiago-pm/expeditions/`, `santiago-pm/tackle/`, `santiago-pm/voyage-trials/`
- Fishing metaphor: `santiago-pm/strategic-charts/Old man and the sea.md`
- Clinical prototype: 30-60m conversion, 3 validation cycles, real-time query
