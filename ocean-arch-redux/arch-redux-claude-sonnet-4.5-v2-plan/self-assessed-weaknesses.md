# Self-Assessed Weaknesses — Claude Sonnet 4.5 Architecture Plan

**Date:** 2025-11-16  
**Plan Commit:** a86c0b2

## Critical Weaknesses

### 1. RDF/Turtle Team Roster Adds Unnecessary Complexity

**Issue:** The plan mandates `team-roster-and-capabilities.ttl` in RDF/Turtle format with SPARQL queries for capability discovery.

**Why This Is Problematic:**
- RDF tooling has a steep learning curve (rdflib, SPARQL query syntax, triple store setup)
- The team roster use case is simple: "list agents, their skill levels, scopes, and tools"
- JSON or YAML would provide identical functionality with zero learning curve
- The "semantic queries" benefit (e.g., "find all Master-level agents in Sea scope") can be trivially implemented with `jq` or Python list comprehensions
- Validation is easier: JSON Schema vs Turtle syntax errors

**Recommendation:** Replace RDF roster with `team-roster-and-capabilities.json` or `.yaml`:
```json
{
  "agents": [
    {
      "id": "santiago-pm",
      "role": "PM",
      "skill_level": "Master",
      "knowledge_scope": "Sea",
      "tools": ["read_working_agreements", "propose_evolution_cycle"],
      "mcp_manifest": "mcp/manifests/pm.json"
    }
  ]
}
```

No loss of functionality, massive reduction in tooling complexity.

---

### 2. Milestone 3 Is Oversized and Will Bottleneck Progress

**Issue:** Milestone 3 bundles:
- Queued write API design
- Queue implementation with conflict detection
- Provenance tracking system
- Schema validation engine
- Refactoring all existing KG service calls

**Why This Is Problematic:**
- This is 3-4 weeks of work disguised as one milestone
- Milestones 1 and 2 are lightweight (1-2 weeks each), creating uneven velocity
- Downstream milestones (M4 orchestrator, M5 tests) are blocked until M3 completes
- High risk of scope creep: "Let's also add KG versioning, backup hooks, migration scripts..."

**Recommendation:** Split into two phases:
- **M3a: Queued Writes (2 weeks)** — Core queueing with basic conflict detection; good enough for MVP
- **M3b: Provenance & Validation (2 weeks)** — Add audit trails and schema enforcement after queued writes are proven stable

This unblocks M4 orchestrator work sooner and reduces integration risk.

---

### 3. Ethics Gating Policy Is Underspecified

**Issue:** The plan requires "Ethics & Concurrency Gating" but doesn't define:
- Which operations are "high-risk" vs "low-risk"
- Who sets the thresholds (Hank? PM? Ethicist? Config file?)
- How does Hank's approval flow work technically (blocking queue? webhook? Slack notification?)
- What happens if Ethicist is unavailable (fail-safe open? fail-safe closed?)

**Why This Is Problematic:**
- Implementation teams will make arbitrary decisions without clear policy
- Different developers might classify the same operation differently
- No way to test ethics gating without a concrete policy definition
- Risk of either over-gating (everything blocks on Hank → bottleneck) or under-gating (nothing gets reviewed → defeats purpose)

**Recommendation:** Add a "Milestone 0" decision phase that produces:
- `ethics-gating-policy.yaml` defining risk levels and approval flows
- Concrete examples: "Writing to production KG = high-risk", "Reading shared memory = low-risk"
- Hank approval mechanism spec (webhook URL? approval queue API? manual gate?)

---

### 4. Vector DB and Graph DB Choices Deferred But Block Later Work

**Issue:** Open Questions lists "Which Vector DB? Which Graph DB?" as unresolved, but:
- M3 unified KG layer depends on Graph DB choice (API surface differs: Neo4j vs Blazegraph vs GraphDB)
- M6 DGX deployment provisions these services in `docker-compose.yml`
- Performance characteristics affect M3 queue flushing strategy

**Why This Is Problematic:**
- Can't write M3 KG queue code without knowing target DB API
- Can't write M6 provisioning scripts without knowing container images and config
- Risk of "pick one arbitrarily then regret it" decisions made under pressure

**Recommendation:** Make this an explicit pre-M1 decision (or early M1 task):
- Run quick benchmark: Blazegraph (RDF-native, simpler) vs Neo4j (property graph, richer queries)
- Test with sample NuSy ontology: 10K triples, concurrent writes, SPARQL vs Cypher
- Document decision rationale in `infra/dgx/db-technology-selection.md`

---

### 5. No Rollback or Revert Strategy

**Issue:** None of the milestones include rollback procedures. Example failure scenarios:
- M3's queued writes introduce subtle KG corruption → how to revert to direct writes?
- M4's orchestrator has session isolation bug → how to roll back to local agent execution?
- M6's DGX deployment has config error → how to restore working state?

**Why This Is Problematic:**
- A bad milestone can strand the project in a broken state
- No "safe checkpoint" to revert to if integration fails
- Developers will be hesitant to merge risky changes without escape hatch

**Recommendation:** For each milestone, add:
- **Rollback Procedure** task (e.g., "Feature flag to toggle queued vs direct KG writes")
- **Acceptance Criteria** must include: "Rollback procedure tested and documented"
- Git tags at milestone boundaries (e.g., `milestone-2-complete`) for easy revert

---

### 6. DGX Storage Layout Lacks Operational Details

**Issue:** The plan mentions "4 TB internal + 8-16 TB external NVMe RAID" but M6 doesn't specify:
- Exact mount points (`/mnt/internal-nvme`, `/mnt/external-raid`?)
- Backup schedules and retention policies
- Capacity monitoring thresholds (alert at 80% full?)
- Who has write permissions to which paths
- Snapshot strategy for KG backups

**Why This Is Problematic:**
- Operations team will have to make these decisions ad-hoc during deployment
- Risk of inconsistent paths across services (model expects `/models`, container mounts `/data/models`)
- No proactive monitoring → disk fills up → service crashes

**Recommendation:** Expand M6 `storage-layout.md` to include:
```markdown
## Mount Points
- `/mnt/dgx-internal` (4 TB) — OS, repos, active models, hot KG
- `/mnt/dgx-external` (16 TB RAID) — model zoo, archives, backups

## Backup Schedule
- KG snapshots: hourly to `/mnt/dgx-external/backups/kg/`
- Model checkpoints: on change to `/mnt/dgx-external/model-archive/`

## Monitoring
- Alert if `/mnt/dgx-internal` > 80% full
- Alert if `/mnt/dgx-external` > 90% full
```

---

### 7. Apprentice/Journeyman/Master Metaphor Not Operationalized

**Issue:** The plan uses skill levels (Apprentice/Journeyman/Master) and knowledge scopes (Pond/Lake/Sea/Ocean) extensively, but doesn't define:
- How to measure when an agent graduates from Apprentice → Journeyman
- What behavioral differences exist (does an Apprentice refuse certain tasks? flag for review?)
- Who decides promotions (Santiago-PM? Hank? Metrics-based?)

**Why This Is Problematic:**
- These are treated as metadata labels without operational meaning
- Risk of becoming "documentation theater" — nice metaphor but no enforcement
- No clear path for evolutionary growth if graduation criteria are undefined

**Recommendation:** Add to M2 or M7:
- `knowledge/shared/skill-progression-rubric.md` defining:
  - Apprentice: Can execute well-defined tasks with supervision
  - Journeyman: Can work independently on scoped problems
  - Master: Can propose new capabilities and mentor other agents
- Metrics for promotion (e.g., "10 successful tasks with zero escalations → Journeyman")

---

## Minor Weaknesses

### 8. Fake Team Strategy Lacks Transition Plan Details

The interim fake-team mode (external LLM API proxy) is mentioned but:
- No specification for how to detect "DGX is now available"
- No migration script to switch from proxy to local model
- Risk of proxy API keys expiring mid-development

**Fix:** Add to M6: "Proxy-to-DGX migration checklist and cutover script"

---

### 9. Santiago-Ethicist Starting as "Journeyman" Seems Optimistic

If this is the **first** Ethicist implementation, shouldn't it start as Apprentice with limited scope?

**Fix:** Consider downgrading to Apprentice initially, then promote after validation.

---

### 10. Concurrency Test SLOs Are Aspirational Without Baseline

M5 defines "P95 latency < 4 seconds" but provides no baseline measurement. Is the current system at 2 seconds? 10 seconds?

**Fix:** Add to M5: "Measure baseline latency before optimizations to set realistic targets"

---

## Summary

**High-Priority Fixes:**
1. Replace RDF roster with JSON/YAML
2. Split M3 into two phases
3. Define ethics gating policy explicitly
4. Make DB technology choices early
5. Add rollback procedures to all milestones

**Medium-Priority:**
6. Expand storage layout operational details
7. Operationalize skill progression rubric

**Low-Priority:**
8-10. Minor specification gaps

**Overall:** Solid architectural vision undermined by operational underspecification and complexity overreach. With targeted fixes, this becomes an A-grade plan.
