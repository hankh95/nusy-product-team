# Questions for Captain Review

## Expedition EXP-057: Architecture Redux 3 – Target Runtime & Repo Alignment

This document contains questions that require Captain (Hank) review and approval before proceeding with the next phases of the architecture migration.

## Completed Work Summary

✅ **Expedition Infrastructure**: Created branch `exp-057-architecture-redux-3-migration` and expedition directory  
✅ **Document Review**: Analyzed `arch-vision-merged-plan.md` and `arch-migration-plan.md`  
✅ **Triage Report**: Generated comprehensive analysis of root-level artifacts with proposed target homes  
✅ **Documentation Updates**: Updated `santiago-pm/tackle/folder-structure.md` with two-namespace model  
✅ **Glossary Extension**: Added new terms for migration concepts  
✅ **Kanban Epic**: Created `architecture-migration-epic.md` with implementation phases  

## Questions Requiring Captain Approval

### 1. Namespace Structure Decision

**Question:** Should `santiago-pm/` remain as the canonical scaffold at root level, or should it be moved under `self-improvement/` to fully implement the two-namespace model?

**Context:**
- Current proposal: Keep `santiago-pm/` at root as canonical scaffold
- Alternative: Move to `self-improvement/santiago-pm/` for cleaner separation
- Impact: Affects all references and agent navigation patterns

**Options:**
- **Option A**: Keep at root (current proposal) - maintains existing references, easier transition
- **Option B**: Move to `self-improvement/` - cleaner architecture, full namespace separation

**Captain Response:** [Option B - see the diagram below]
```text
├─ docs/
│  ├─ ARCHITECTURE/
│  │  ├─ arch-vision-merged-plan.md        # (move this here)
│  │  ├─ arch-migration-plan.md            # (move this here)
│  │  └─ index.md                          # architecture map/TOC
│  └─ GLOSSARY/
│     └─ santiago-glossary.md              # shared terms: agents, KGs, shipyard, etc.
│
├─ santiago_core/
│  ├─ runtime/                             # main DGX / Noesis runtime wiring
│  ├─ services/                            # knowledge_graph, kanban, eval, etc.
│  ├─ agents/                              # core Santiago agent types & base classes
│  ├─ orchestration/                       # multi-agent orchestration / workflows
│  ├─ adapters/                            # EHR, Git, MCP, external APIs, etc.
│  ├─ knowledge/
│  │  ├─ kg/                               # core/global KG files (e.g. santiago_kg.ttl)
│  │  └─ caches/                           # embeddings, indices, transient stores
│  └─ tests/                               # unit/integration tests for core
│
├─ domain/                                 # "operational" / customer-facing side
│  ├─ domain-knowledge/
│  │  ├─ raw_sources/                      # imported guidelines / PDFs / repos
│  │  ├─ curated/                          # cleaned / curated domain content
│  │  └─ kg_views/                         # domain-specific KG slices / projections
│  ├─ domain-features/
│  │  ├─ specs/                            # feature & capability specs (md/yaml)
│  │  └─ bdd/                              # *.feature files tied to domain behavior
│  └─ domain-expeditions/
│     ├─ active/                           # in-flight projects / experiments
│     └─ archive/                          # completed domain expeditions
│
├─ self-improvement/                       # Santiago improving Santiago
│  ├─ santiago-pm/                         # canonical PM/self-improvement scaffold
│  │  ├─ cargo-manifests/                  # feature/epic/roadmap docs
│  │  ├─ ships-logs/                       # daily/weekly logs of work & learning
│  │  ├─ voyage-trials/                    # experiments / A/B tests / pilots
│  │  ├─ navigation-charts/                # roadmaps, dependency maps, story maps
│  │  ├─ captains-journals/                # retros, decisions, ethics reviews
│  │  ├─ tackle/
│  │  │  ├─ folder-structure/              # docs & tools for repo/org structure
│  │  │  └─ tools/                         # PM utilities, scripts, prompt packs
│  │  └─ tests/
│  │     └─ bdd/                           # *.feature files for self-improvement flows
│  └─ knowledge/
│     ├─ experiments/                      # experiment definitions & configs
│     ├─ evals/                            # evaluation harnesses, metrics configs
│     └─ retros/                           # postmortems, design critiques
│
├─ knowledge/                              # cross-cutting knowledge assets
│  ├─ global-kg/                           # shared/global KG (RDF, TTL, etc.)
│  ├─ vocab/                               # shared vocabularies, schemas
│  └─ ontologies/                          # domain ontologies, reasoner configs
│
├─ tools/
│  ├─ cli/                                 # CLI entrypoints (e.g. santiago-cli)
│  ├─ scripts/                             # maintenance/migration scripts
│  └─ mcp/                                 # Model Context Protocol tool defs
│
├─ configs/
│  ├─ dgx/                                 # DGX runtime configs, profiles, docker/compose
│  ├─ mcp/                                 # MCP service configs
│  └─ ci-cd/                               # CI/CD pipelines, linting, gates
│
└─ _archive/                               # old but preserved materials
   ├─ legacy-docs/
   └─ legacy-code/
```

### 2. Demo Scripts Handling

**Question:** How should demo scripts (`demo_*.py`) be handled in the migration?

**Context:**
- Triage report proposes moving to `examples/` or archiving
- Some demos may be valuable for testing, others are historical
- Need to determine which have ongoing value

**Options:**
- **Option A**: Move all to `domain/examples/` - preserve for testing/documentation
- **Option B**: Archive most, keep select few in `domain/examples/`
- **Option C**: Move to `self-improvement/examples/` if they demonstrate agent capabilities

**Captain Response:** [Option A - Move all to `domain/examples/` - these are user-facing demonstration scripts showing how to interact with and test the Santiago system, not core autonomous code. They have educational and testing value that should be preserved in the domain namespace.]

### 3. Test File Distribution

**Question:** How should `tests/` directory be reorganized?

**Context:**
- Currently all tests in one root-level directory
- Migration plan suggests distributing to appropriate domain/self-improvement locations
- Need to maintain test discoverability and CI/CD integration

**Options:**
- **Option A**: `domain/tests/` and `self-improvement/tests/` subdirectories
- **Option B**: Tests co-located with code (e.g., `domain/*/tests/`)
- **Option C**: Keep centralized but reorganize by namespace

**Captain Response:** [Option B - Tests co-located with code (e.g., `domain/*/tests/`) - this maintains the principle of keeping tests close to the code they test, improves discoverability, and supports the two-namespace model while preserving CI/CD integration.]

### 4. Documentation Consolidation Strategy

**Question:** What should be the final structure for consolidated documentation?

**Context:**
- Multiple docs exist: `ARCHITECTURE.md`, `docs/`, `docs-arch-redux-3/`, `GLOSSARY.md`
- Need single source of truth with clear hierarchy

**Options:**
- **Option A**: `docs/architecture/` with merged plan as primary, others as historical
- **Option B**: Keep `docs-arch-redux-3/` as active, archive others
- **Option C**: `docs/` as main, with architecture subsection

**Captain Response:** [Option A - `docs/architecture/` with merged plan as primary, others as historical - this creates a clear hierarchy with the merged plan as the single source of truth, while preserving historical context in the archive.]

### 5. Migration Phase Approval

**Question:** Should the expedition proceed to Phase 2 (Non-Destructive Restructuring) with the current triage plan?

**Context:**
- Phase 1 (Planning) is complete
- Phase 2 involves creating directories and moving artifacts
- All Phase 2 operations are designed to be non-destructive

**Options:**
- **Approve**: Proceed with Phase 2 implementation
- **Revise**: Modify triage plan based on answers above
- **Hold**: Additional analysis needed before structural changes

**Captain Response:** [Approve - Proceed with Phase 2 implementation. All decisions are documented, the triage plan is comprehensive, and Phase 2 operations are designed to be non-destructive with clear rollback paths.]

## Risk Assessment

### High-Risk Items Requiring Review
1. **Import/Reference Updates**: Moving files may break imports - need systematic update plan
2. **CI/CD Pipeline**: Ensure all moved code still builds and tests pass
3. **Agent Navigation**: Autonomous agents must adapt to new structure
4. **Historical Access**: Archived files should remain accessible for reference

### Success Criteria Review
- Repository structure matches target architecture
- Zero production outages during migration
- Agents can navigate and operate in new structure
- Documentation provides clear guidance

## Next Steps After Captain Review

1. **Incorporate Answers**: Update triage report and implementation plan
2. **Phase 2 Execution**: Begin non-destructive restructuring
3. **Validation**: Test all changes before Phase 3
4. **Captain Check-in**: Regular updates on progress and issues

## Contact
**Expedition Lead:** Santiago-PM (Autonomous Agent)  
**Captain:** Hank  
**Branch:** `exp-057-architecture-redux-3-migration`
