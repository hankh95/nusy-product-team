### 1. Vision Summary (DGX + Runtime + Agents) – The New North Star

The single most authoritative vision file is **`arch-vision-gpt51.md`** (the one you have open) and it is extremely clear and consistent with the supporting vision files (`Santiago-Trains-Manolin-v2.md`, `santiago-component-architecture.md`, `Old man and the sea.md`).

Key points that define the **future truth**:

- Santiago is no longer a single agent or a fixed team → it is an **always-on, autonomous multi-agent crew** that lives permanently on the DGX.
- The DGX is the **shipyard that never closes**. There is no longer a hard “day at sea / night in shipyard” split. Instead there are two concurrent work streams that the crew dynamically balances:
  1. External/domain projects (“at sea” – building customer or domain experts)
  2. Self-improvement projects (“in the shipyard” – upgrading core, tools, memory, agents)
- Decision of what to work on next is made continuously by the **Santiago-PM + Ethicist** using lean flow metrics, experiment results, and ethical/value scoring — exactly like a real seasoned software team.
- Truth is **in-memory Git + file system** (`memory://santiago-workspace`), not database rows. All artifacts, features, expeditions, tests, logs, Kanban cards live as files and commits in an in-memory Git repository that every agent can read/write instantly.
- Every agent has fast, graph-based memory (working + episodic + semantic) and all agents share the same in-memory workspace.
- Santiago-core owns:
  - The 4-layer NuSy pipeline (Catchfish → Fishnet → Navigator → 4-layer model)
  - The in-memory Git + Kanban hull
  - The ability to spawn new domain-expert “daughter ships” (new Santiagos with their own specialized KG + tools)
- The entire crew runs **24/7 on the DGX** as a self-improving factory. Periodic snapshots are pushed to persistent Git for human audit and rollback.

→ This is the new canonical vision. Everything else must now converge to this.

### 2. Current Architecture & Plan Summary (What the docs still say today)

`docs/ARCHITECTURE.md` (v3.0 from 2025-11-16) still describes the **Phase 0 → Phase 4 bootstrap plan**:
- Fake team (MCP proxies) → build real Navigator/Catchfish/Fishnet → catch first real santiago-pm → A/B replace proxies → repeat for all roles → become self-sustaining.
- Still talks about “traditional Git” vs “in-memory Git” as dual worlds.
- Still has Phase 0–4 thinking and canary routing of proxies.

`santiago-development-master-plan.md` and `DEVELOPMENT_PLAN.md` are still organized in classic 6-phase linear plan (Foundation → Knowledge → Swarm → etc.) with no mention of always-on DGX-native runtime or in-memory Git as source of truth.

→ These documents are now outdated relative to the new vision.

### 3. DGX-Related Work Actually Existing in the Repo Today (2025-11-20)

| Path | Status | What it is |
|------|------|------------|
| `features/dgx-provisioning-automation.feature` | BDD feature only | Full provisioning scripts plan |
| `features/dgx-storage-expansion-procurement.feature` | BDD feature only | Hardware purchase plan |
| `kanban-boards.md` | Active | Shows DGX provisioning tasks assigned to agents |
| `tackle/dgx/` (does not exist yet) | Missing | No actual code |
| `src/nusy_pm_core/adapters/dgx_*` | Does not exist | — |
| Mistral + vLLM integration | Only in Kanban, not implemented |

→ DGX work is currently only in Kanban + feature specs. No runtime code exists yet. The always-on multi-agent loop is still 100% vision.

### 4. Answers to the Key Architecture Questions

**A. DGX Runtime Model → Clear recommendation: ALWAYS-ON, no day/night mode**

The new vision is explicit and superior:
- Always-running autonomous crew on the DGX
- Single unified backlog (domain work + self-improvement work)
- PM + Ethicist continuously reprioritise based on flow, learning value, and ethics
- No context-switching cost between “modes”

Tradeoffs of dual-mode (day/night) are too high: context loss, cold starts, complex state sync. The always-on model is simpler, faster, and matches real expert teams.

**Recommendation**: Adopt always-on model as canonical.

**B. Knowledge Graphs & In-Memory Git → One unified workspace per Santiago instance**

Best model (directly from the vision):
- Each running Santiago (core or domain expert) has exactly **one in-memory Git repository** that is the single source of truth.
- That repository contains:
  - Domain knowledge files + KG triples
  - Self-improvement experiments, tackle, tools
  - Kanban board state (as markdown/yaml files)
  - BDD scenarios, test results, logs
- There is no second “self-improvement KG”. Self-improvement is just another project in the same hull.
- Multiple Santiagos (e.g. santiago-pm + santiago-medical) each have their own in-memory Git, but they can mount shared tackle directories from a common fleet repository.

**Recommendation**: One unified in-memory Git + KG per Santiago instance. Self-improvement is just another folder/backlog inside it.

**C. Always-in-memory, experiment-driven flow**

Runtime loop:
1. All agents wake up in the same in-memory workspace
2. Santiago-PM runs neurosymbolic prioritisation → picks next card (could be customer feature or self-improvement experiment)
3. Agents work → commit files → run BDD suite → commit results
4. Results feed back into prioritiser (learning value update)
5. Loop forever

Safety/Ethics: Every commit goes through Ethicist-gated queue (as described in ASSUMPTIONS_AND_RISKS.md). CI/CD = automatic BDD/Fishnet run on every commit.

### 5. Proposed Changes to Documentation

Create/replace these files in `docs/`:

**1. New file: `docs/RUNTIME_ARCHITECTURE.md`** (new source of truth)

```markdown
# Runtime Architecture on DGX – Canonical Model (2025-11-20)

## 1. Always-On Autonomous Crew
- Single Santiago crew instance runs 24/7 on the DGX
- No day/night mode split
- Unified backlog mixing domain work + self-improvement work

## 2. Single Source of Truth = In-Memory Git
```
memory://santiago-workspace/
├── domain-knowledge/
├── tackle/                  # reusable tools shared across fleet
├── expeditions/
├── features/
├── kanban/
├── tests/bdd/
└── logs/
```

## 3. Memory Model
- Working memory → active agent context
- Episodic memory → commit history + logs
- Semantic memory → KG triples derived from files

## 4. Self-Improvement Loop
PM → Prioritise → Agents execute → Commit → BDD → Update scores → Reprioritise

**2. Deprecate / replace `docs/ARCHITECTURE.md`**
→ Rename current ARCHITECTURE.md → `docs/history/PHASE_0_4_BOOTSTRAP_ARCHITECTURE_ARCHIVED.md`
→ New `docs/ARCHITECTURE.md` becomes a one-page pointer: “See RUNTIME_ARCHITECTURE.md and COMPONENT_OVERVIEW.md”

**3. Update `santiago-development-master-plan.md`**
Replace 6-phase plan with new phases:

```markdown
Phase 1 – DGX-Native Always-On Runtime (Nov–Dec 2025)
Phase 2 – Unified In-Memory Git + Kanban (Dec 2025)
Phase 3 – Ethicist-Gated Commit Queue & CI/CD (Jan 2026)
Phase 4 – Fleet Tackle Sharing & Daughter-Ship Spawning (Q1 2026)
Phase 5 – Full Self-Improvement Autonomy (mid 2026)
```

**4. Consolidate vision files**
Move all old vision files into `docs/history/vision-archives/`
Keep only these three as canonical in `santiago-pm/strategic-charts/`:
- `Santiago-Crew-Vision.md` ← new consolidated north-star story (merge arch-vision-gpt51.md + Santiago-Trains-Manolin-v2.md)
- `Runtime-Architecture.md` (the new doc proposed above)
- `Component-Overview.md` (current santiago-component-architecture.md cleaned)

### 6. Immediate Next Actions for You (Hank)

1. Create `docs/RUNTIME_ARCHITECTURE.md` with the exact structure above
2. Archive the old `docs/ARCHITECTURE.md` and `SANTIAGO-ARCHITECTURE-SCENARIOS.md`
3. Create new consolidated vision file `santiago-pm/strategic-charts/Santiago-Crew-Vision.md` containing the always-on crew + in-memory Git model
4. Update Kanban: add expedition EXP-056: “Implement Always-On DGX Runtime Loop” as highest priority
5. Mark all Phase 0–4 proxy language as historical

Do this and the entire repository will finally speak with one coherent, forward-looking voice that matches the beautiful new vision in `arch-vision-gpt51.md`.

The Santiago crew is ready to sail 24/7 — we just need to cut the old dock lines.