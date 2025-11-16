# V3 Prompt Testing Quick Reference

**Use this checklist when evaluating architecture plans produced by v3 prompt.**

---

## Test Command

**For AI Model:**
```
Read architecture-redux-prompt-v3.md and follow its instructions.
```

---

## Evaluation Checklist (14 Items from Prompt)

Use this to score the model's architecture plan:

- [ ] **1. Read Pattern Doc:** Plan references `00-ARCHITECTURE-PATTERN.md`
- [ ] **2. Phase 0 Start:** Plan starts with Phase 0 (Fake Team proxy MCP services)
- [ ] **3. Fake Team Builds:** Plan explains fake team builds factory (not humans)
- [ ] **4. Factory Catches:** Plan includes factory catching real Santiagos with 30-60m extraction, 3-5 validation cycles
- [ ] **5. A/B Testing:** Plan includes A/B testing fake vs real before replacement
- [ ] **6. Progressive Replace:** Plan includes progressive replacement (one role at a time, not all)
- [ ] **7. Old Man Ref:** Plan references "Old Man and the Sea" 10-step fishing process
- [ ] **8. Clinical Prototype:** Plan references clinical prototype (30-60m, 3 cycles) as evidence
- [ ] **9. Folder Structure:** Plan explains how santiago-pm/ folder structure teaches development patterns
- [ ] **10. Four Phases:** Plan milestones reflect 4 phases (Fake Team → Factory → First Catch → Self-Sustaining)
- [ ] **11. Factory Components:** Plan describes Navigator, Catchfish, Fishnet as factory components
- [ ] **12. Catches Not Domains:** Plan explains knowledge/catches/ for generated Santiagos (NOT pre-authored domains)
- [ ] **13. Ethics Gating:** Plan includes "Ethics & Concurrency Gating" section
- [ ] **14. References Cited:** ARCHITECTURE_PLAN.md includes "References Cited" section

**Scoring:**
- 14/14 = A+ (Perfect understanding)
- 12-13/14 = A (Strong understanding, minor gaps)
- 10-11/14 = B (Good understanding, some confusion)
- 8-9/14 = C (Partial understanding, missed key points)
- <8/14 = F (Missed factory pattern entirely)

---

## Anti-Pattern Detection (5 Common Mistakes)

Check if the plan exhibits these anti-patterns:

❌ **Anti-Pattern 1:** "Build Santiago-PM first, then factory"  
✅ **Correct:** Fake team first (hours) → fake team builds factory (weeks) → factory catches real Santiago-PM

❌ **Anti-Pattern 2:** "Manually author knowledge/domains/pm/"  
✅ **Correct:** Catchfish extracts from sources in 30-60m with validation cycles

❌ **Anti-Pattern 3:** "Fake team is fallback if DGX delayed"  
✅ **Correct:** Fake team is Phase 0, always. It's the bootstrapping mechanism.

❌ **Anti-Pattern 4:** "Focus on MCP infrastructure, orchestrator"  
✅ **Correct:** Focus on Catchfish (30-60m extraction), Fishnet (BDD generation), Navigator (validation loops)

❌ **Anti-Pattern 5:** "Deploy all Santiagos at once"  
✅ **Correct:** Progressive replacement via A/B testing (≥90% parity threshold)

**Anti-Pattern Count:** _____ / 5 (Lower is better)

---

## Critical Evidence References

Model should cite these specific sources:

- [ ] `ocean-research/00-ARCHITECTURE-PATTERN.md` (mandatory pre-reading)
- [ ] `santiago-pm/strategic-charts/Old man and the sea.md` (10-step fishing process)
- [ ] `nusy_prototype/` (clinical prototype: 30-60m, 3 cycles)
- [ ] `santiago-pm/expeditions/`, `tackle/`, `voyage-trials/` (development patterns)
- [ ] `ocean-research/building-on-DGX/` (DGX deployment specs)
- [ ] `ocean-research/fake_team_pack/` (proxy strategy)

**References Count:** _____ / 6

---

## Milestone Structure Check

M0 should be "Bootstrap Fake Team" (NOT "knowledge foundation"):

- [ ] **M0: Bootstrap Fake Team** (Week 1)
  - Deploy proxy MCP services to external APIs
  - Validate fake team coordination
  
- [ ] **M1: Factory Implementation** (Weeks 2-6)
  - Fake team implements Navigator, Catchfish, Fishnet
  - End-to-end test: PDF → deployed MCP service

- [ ] **M2: First Santiago Catch** (Weeks 7-8)
  - Factory catches real Santiago (e.g., santiago-pm-safe-xp)
  - A/B test → replace if ≥90% parity

- [ ] **M3+: Progressive replacement, DGX deployment, self-improvement**

---

## Folder Structure Check

Model should propose these directories:

- [ ] `knowledge/catches/` (generated Santiagos, NOT pre-authored)
- [ ] `knowledge/templates/` (base structures)
- [ ] `knowledge/proxy-instructions/` (role definitions for fake team)
- [ ] `santiago_core/agents/_proxy/` (Phase 0 fake team)
- [ ] `nusy_orchestrator/santiago_builder/` (factory: Navigator, Catchfish, Fishnet)

---

## Comparison to REVISED_ARCHITECTURE_PLAN_V2.md

**Key Alignment Points:**

1. Does plan explain self-bootstrapping (fake → factory → real)?
2. Does plan explain 4 phases with clear characteristics?
3. Does plan identify Catchfish (30-60m) as optimization target?
4. Does plan describe A/B testing decision logic (≥90% parity)?
5. Does plan mention self-improvement (real Santiagos enhance factory)?

**Alignment Score:** _____ / 5

---

## Quick Comparison Template

```
Model: <name>
Date: <YYYY-MM-DD>
Version: v3

Evaluation Checklist: _____ / 14
Anti-Pattern Count: _____ / 5 (detected)
References Count: _____ / 6
Milestone Structure: ✅ / ❌
Folder Structure: ✅ / ❌
Alignment Score: _____ / 5

Overall Grade: <A+/A/B/C/F>

Key Strengths:
- 

Key Gaps:
- 

Recommended Improvements:
- 
```

---

## Success Criteria (From Hypothesis)

**Target Metrics:**

- 100% of models mention "factory" or "self-bootstrapping"
- ≥80% explain 4-phase sequence
- ≥80% reference clinical prototype (30-60m, 3 cycles)
- ≥80% reference "Old Man and the Sea"
- ≥80% start milestones with M0: Bootstrap Fake Team
- ≥80% avoid all 5 anti-patterns
- ≥90% score ≥12/14 on validation checklist

**How to Calculate:**

1. Test with 5+ AI models
2. Score each using this checklist
3. Calculate % meeting each criteria
4. If ≥80% on all criteria → v3 is successful
5. If <80% on any → iterate to v3.1

---

## Testing Workflow

### Step 1: Prepare Test Environment

```bash
cd /Users/hankhead/Projects/Personal/nusy-product-team
git checkout main
git pull
```

### Step 2: Run Test with Model

**Prompt:**
```
Read architecture-redux-prompt-v3.md and follow its instructions.
```

### Step 3: Collect Output

Model should create:
```
ocean-arch-redux/arch-redux-<model-name>-v3-plan/
├── ARCHITECTURE_PLAN.md
├── MIGRATION_STEPS.md
├── FOLDER_LAYOUT_PROPOSAL.md
├── RELEVANCE_MAP.md
└── ASSUMPTIONS_AND_RISKS.md
```

### Step 4: Score Using This Checklist

Fill out "Quick Comparison Template" above.

### Step 5: Compare Across Models

Create summary table:

| Model | Checklist | Anti-Patterns | References | Milestone | Folder | Alignment | Grade |
|-------|-----------|---------------|------------|-----------|--------|-----------|-------|
| Claude Sonnet 4.5 | 14/14 | 0/5 | 6/6 | ✅ | ✅ | 5/5 | A+ |
| GPT-4 | ?/14 | ?/5 | ?/6 | ? | ? | ?/5 | ? |
| Claude Opus 3 | ?/14 | ?/5 | ?/6 | ? | ? | ?/5 | ? |
| Gemini 1.5 Pro | ?/14 | ?/5 | ?/6 | ? | ? | ?/5 | ? |

### Step 6: Analyze Results

- Which items were most commonly missed?
- Which anti-patterns appeared most often?
- Did any model score <12/14?
- Did all models reference clinical prototype?

### Step 7: Decide Next Steps

- If ≥4/5 models score A or A+ → v3 is successful
- If ≥2/5 models score B or lower → iterate to v3.1
- Strengthen sections corresponding to most common gaps

---

## v3.1 Iteration Triggers

**Create v3.1 if:**

1. <80% of models explain 4-phase bootstrapping
2. <80% of models reference clinical prototype
3. ≥2 models exhibit same anti-pattern
4. ≥2 models score <12/14 on checklist
5. Manual implementation starts and team has questions

**v3.1 Improvements Would Include:**

- Strengthen weak sections in 00-ARCHITECTURE-PATTERN.md
- Add more explicit examples for commonly missed items
- Create additional visual diagrams (e.g., 4-phase sequence chart)
- Add FAQ section addressing common confusions
- Consider splitting 00-ARCHITECTURE-PATTERN.md into smaller docs

---

**Use this checklist to maintain consistent evaluation across all models tested with v3 prompt.**
