# Santiago Factory v2.0 Migration Instructions

**Purpose:** Restructure repository from research/exploration mode → production implementation mode  
**Date:** 2025-11-16  
**Estimated Time:** Automated via script (5 minutes)

---

## What's Happening

We're restructuring the repository to:
1. **Preserve** all domain knowledge in `santiago-pm/` (your PM/development patterns)
2. **Keep** core vision artifacts that align with hybrid architecture
3. **Archive** research artifacts, old plans, and legacy code
4. **Promote** the hybrid v3 plan as the canonical architecture
5. **Create** foundation structure for implementation

---

## What Gets Kept (Active Workspace)

### Domain Knowledge & Patterns (KEEP ALL)
- `santiago-pm/` — **ALL subdirectories preserved**
  - `captains-journals/`, `cargo-manifests/`, `crew-manifests/`
  - `expeditions/`, `navigation-charts/`, `passages/`
  - `quality-assessments/`, `research-logs/`, `ships-logs/`
  - `strategic-charts/` (includes "Old Man and the Sea")
  - `tackle/`, `templates/`, `voyage-trials/`
  - `notes-domain-model.md`, `README.md`

### Core Vision (KEEP, Move to `docs/vision/`)
- `ocean-research/00-ARCHITECTURE-PATTERN.md` ✅ **Canonical factory pattern**
- `ocean-research/README-START-HERE.md` ✅ **Entry point for AI models**
- `ocean-research/building-on-DGX/` ✅ **DGX deployment specs (referenced in architecture)**
  - `dgx_spark_nusy_report.md`
  - `nusy_manolin_architecture.md`
  - `nusy_manolin_multi_agent_test_plans.md`
  - `nusy_manolin_provisioning_automation.md`
- `ocean-research/fake_team_pack/` ✅ **Proxy patterns (Phase 0 implementation)**
- `ocean-research/nusy_manolin_architecture.md` ✅ **Shared memory patterns**
- `ocean-research/nusy_manolin_multi_agent_test_plans.md` ✅ **Concurrency tests**

### Hybrid Plan (PROMOTE to Root)
- `ocean-arch-redux/arch-redux-hybrid-v3-plan/` → Root docs

### Active Code & Config (KEEP)
- `santiago_core/` — Will house agents
- `nusy_orchestrator/` — Will house factory (may need rename/create)
- `config/`, `tools/`, `docs/`, `evaluation/`
- `pyproject.toml`, `requirements.txt`, `Makefile`, `CONTRIBUTING.md`

---

## What Gets Archived

### Research Artifacts (ARCHIVE to `_archive/research/`)
- `ocean-research/GPT-revised-architecture/` — Historical research
- `ocean-research/grok-architecture-redux/` — Historical research
- `ocean-research/features-capabilities-for-shared-memory-and-evolution.md` — Subsumed by hybrid plan
- All `architecture-redux-prompt*.md` — Prompt engineering artifacts

### Old Plans (ARCHIVE to `_archive/plans/`)
- `ocean-arch-redux/` — All plans EXCEPT hybrid-v3
  - `arch-redux-claude-sonnet-4.5-v3-plan/`
  - `arch-redux-combined-v3-plan/`
  - `arch-redux-copilot-gpt-5-v2-plan/`
  - `arch-redux-gemini-2.5-Pro-v3-plan/`
  - `arch-redux-gpt-5-v2-plan/`
  - `arch-redux-gpt-5-v3-plan/`
  - `arch-redux-gpt-5.1-codex-v3-plan/`
  - `arch-redux-grok-code-fast-1-v3-plan/`
  - `architecture-redux-grok-4/`
  - `TESTING-CHECKLIST-V3.md`

### Legacy Code (ARCHIVE to `_archive/legacy/`)
- `santiago-code/` — Early experiments (already marked legacy)
- `src/nusy_pm_core/` — Legacy prototype (already marked legacy)
- `nusy_prototype/` — Clinical prototype (evidence preserved, but code archived)

### Development History (ARCHIVE to `_archive/development/`)
- `experiments/` — Historical experiments
- `calibration/` — Old calibration work
- `notes/` — Development notes
- `reports/` — Old assessment reports
- `chat-history/` — Conversation logs
- `backlog/` — Old backlog (will create new from hybrid plan)

### Superseded Docs (ARCHIVE to `_archive/docs/`)
- `DEVELOPMENT_PLAN.md` — Superseded by `MIGRATION_ROADMAP.md`
- `DEVELOPMENT_PRACTICES.md` — Relevant bits merged into `CONTRIBUTING.md`
- `EXPERIMENT_SETUP.md` — Old experiment setup
- `copilot-auto-approve-settings-guide.md` — Old settings guide

---

## New Structure After Migration

```
/santiago-factory/
├── README.md                      # NEW: Project overview + quickstart
├── ARCHITECTURE.md                # PROMOTED: From hybrid plan
├── MIGRATION_ROADMAP.md           # PROMOTED: From hybrid plan  
├── ASSUMPTIONS_AND_RISKS.md       # PROMOTED: From hybrid plan
├── CONTRIBUTING.md                # KEPT: Still relevant
├── pyproject.toml                 # KEPT
├── requirements.txt               # KEPT
├── Makefile                       # KEPT
├──
├── docs/                          # KEPT + ENHANCED
│   ├── vision/                    # NEW: Core vision artifacts
│   │   ├── 00-ARCHITECTURE-PATTERN.md  # FROM ocean-research
│   │   ├── README-START-HERE.md        # FROM ocean-research
│   │   ├── building-on-DGX/            # FROM ocean-research
│   │   ├── fake_team_pack/             # FROM ocean-research
│   │   └── multi-agent-patterns/       # FROM ocean-research (renamed)
│   ├── FOLDER_LAYOUT.md           # PROMOTED: From hybrid plan
│   └── RELEVANCE_MAP.md           # PROMOTED: From hybrid plan
│
├── santiago-pm/                   # KEPT: ALL subdirectories
│   ├── captains-journals/
│   ├── cargo-manifests/
│   ├── crew-manifests/
│   ├── expeditions/
│   ├── navigation-charts/
│   ├── passages/
│   ├── quality-assessments/
│   ├── research-logs/
│   ├── ships-logs/
│   ├── strategic-charts/
│   ├── tackle/
│   ├── templates/
│   ├── voyage-trials/
│   ├── notes-domain-model.md
│   └── README.md
│
├── knowledge/                     # NEW: Factory structure
│   ├── catches/
│   │   └── index.yaml             # NEW: Trust registry placeholder
│   ├── templates/
│   └── proxy-instructions/
│
├── santiago_core/                 # KEPT: Will house agents
│   └── agents/
│       └── _proxy/                # NEW: Fake team stubs
│
├── nusy_orchestrator/             # KEPT/CREATED
│   └── santiago_builder/          # NEW: Factory components
│       ├── navigator.py           # NEW: Stub
│       ├── catchfish.py           # NEW: Stub
│       └── fishnet.py             # NEW: Stub
│
├── config/                        # KEPT
├── tools/                         # KEPT
├── evaluation/                    # KEPT
│
└── _archive/                      # NEW: Everything archived
    ├── research/                  # Ocean research artifacts
    ├── plans/                     # All non-hybrid plans
    ├── legacy/                    # Old code
    ├── development/               # Experiments, notes, etc.
    └── docs/                      # Superseded documentation
```

---

## Migration Steps (Automated)

**I will execute these steps via script. You just need to approve.**

1. Create `v1-archive` branch (safety backup)
2. Create `_archive/` directory structure
3. Move archived items per above classification
4. Create `docs/vision/` and move core vision artifacts
5. Promote hybrid plan documents to root
6. Create `knowledge/` structure with placeholder files
7. Create factory stub files in `nusy_orchestrator/santiago_builder/`
8. Create proxy stub files in `santiago_core/agents/_proxy/`
9. Create new `README.md` with quickstart
10. Update `.vscode/settings.json` for Copilot context
11. Commit with detailed message
12. Push to origin

---

## Post-Migration Actions (Manual)

After automation completes, you'll need to:

1. **Review `README.md`** — Customize project description
2. **Update `CONTRIBUTING.md`** — Merge any practices from old `DEVELOPMENT_PRACTICES.md`
3. **Create backlog from `MIGRATION_ROADMAP.md`** — M0 and M1 tasks
4. **Configure Copilot context** — Verify `.vscode/settings.json` points to new docs

---

## Rollback Plan

If anything goes wrong:

```bash
# Option 1: Reset to v1-archive branch
git checkout v1-archive
git branch -D main
git checkout -b main
git push origin main --force

# Option 2: Revert the migration commit
git revert <migration-commit-sha>
git push origin main
```

---

## Ready to Execute?

**Approve migration?** I will:
- ✅ Preserve ALL santiago-pm/ domain knowledge
- ✅ Keep core vision artifacts in docs/vision/
- ✅ Archive research/old plans cleanly
- ✅ Promote hybrid plan as canonical docs
- ✅ Create foundation structure for M0/M1

**This is a BIG change. Confirm you have a backup and are ready to proceed.**
