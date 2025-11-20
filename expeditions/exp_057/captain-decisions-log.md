# Expedition EXP-057: Architecture Redux 3 – Target Runtime & Repo Alignment

## Expedition Overview

**Objective:** Align repository structure and runtime with the merged architecture vision, implementing the two-namespace model (`domain/*` vs `self-improvement/*`) and establishing the canonical self-improvement scaffold.

**Status:** Phase 1 (Planning) Complete ✅ | Ready for Phase 2 Execution

**Branch:** `exp-057-architecture-redux-3-migration`
**Start Date:** November 20, 2025
**Lead:** Santiago-PM (Autonomous Agent)
**Captain:** Hank

---

## Phase 1: Planning & Documentation (COMPLETED)

### 1.1 Architecture Document Analysis
- **Reviewed:** `arch-vision-merged-plan.md` and `arch-migration-plan.md`
- **Key Findings:**
  - Two-namespace model: `domain/*` (production) vs `self-improvement/*` (autonomous improvement)
  - Canonical scaffold: `santiago-pm/` as self-improvement template
  - Always-on DGX runtime with in-memory Git + KG
  - Nautical theming for agent navigation

### 1.2 Root Artifact Triage Report
- **Generated:** `expeditions/exp_057/triage-report.md`
- **Coverage:** 25+ root-level files analyzed
- **Categories:**
  - Keep in root: Infrastructure files (`.env`, `Dockerfile`, `README.md`, etc.)
  - Move to `domain/`: Production code (`features/`, `models/`, `nusy_orchestrator/`, etc.)
  - Move to `self-improvement/`: PM scaffold (`santiago-pm/`, `kanban-boards.md`, etc.)
  - Archive: Historical docs (`ARCHITECTURE.md`, `DEVELOPMENT_PLAN.md`, etc.)

### 1.3 Documentation Updates
- **Updated:** `santiago-pm/tackle/folder-structure.md`
  - Added two-namespace model explanation
  - Documented migration status and agent discovery patterns
- **Extended:** `GLOSSARY.md`
  - Added terms: Two-namespace model, Domain namespace, Self-improvement namespace
  - Added: Canonical scaffold, Santiago-PM scaffold, Runtime architecture
  - Added: Self-improving multi-agent system, Expedition pattern, Triage report

### 1.4 Kanban Epic Creation
- **Created:** `santiago-pm/cargo-manifests/architecture-migration-epic.md`
- **Structure:** 4-phase implementation plan with BDD scenarios
- **Coverage:** Planning, non-destructive moves, documentation consolidation, validation

### 1.5 Captain Review Process
- **Generated:** `docs-arch-redux-3/questions.md` with 5 key questions
- **Questions Covered:**
  1. Namespace structure for `santiago-pm/`
  2. Demo scripts handling
  3. Test file distribution
  4. Documentation consolidation
  5. Phase 2 approval

---

## Captain Decisions (Finalized)

### Decision 1: Namespace Structure
**Question:** Should `santiago-pm/` remain at root or move to `self-improvement/`?

**Captain Response:** Option B - Move to `self-improvement/santiago-pm/` for cleaner architecture and full namespace separation.

**Rationale:**
- Aligns with two-namespace model principles
- Clear separation between production domain and self-improvement
- Maintains canonical scaffold pattern for future Santiago domains
- Agent navigation becomes more predictable

### Decision 2: Demo Scripts Handling
**Question:** How should demo scripts (`demo_*.py`) be handled?

**Captain Response:** Option A - Move all to `domain/examples/`.

**Rationale:**
- Demo scripts are user-facing examples, not core autonomous code
- Educational and testing value should be preserved
- Domain namespace is appropriate for operational examples
- Keeps them separate from production runtime code

### Decision 3: Test File Distribution
**Question:** How should `tests/` directory be reorganized?

**Captain Response:** Option B - Tests co-located with code (e.g., `domain/*/tests/`).

**Rationale:**
- Maintains principle of keeping tests close to code they test
- Improves discoverability and maintainability
- Supports two-namespace model
- Preserves CI/CD integration capabilities

### Decision 4: Documentation Consolidation
**Question:** What should be the final structure for consolidated documentation?

**Captain Response:** Option A - `docs/architecture/` with merged plan as primary.

**Rationale:**
- Creates clear hierarchy with merged plan as single source of truth
- Preserves historical context in archive
- Improves discoverability for both humans and agents
- Aligns with overall documentation organization

### Decision 5: Migration Phase Approval
**Question:** Should the expedition proceed to Phase 2?

**Captain Response:** Approve - Proceed with Phase 2 implementation.

**Rationale:**
- All decisions are documented and justified
- Triage plan is comprehensive and reviewed
- Phase 2 operations are non-destructive
- Clear rollback paths and validation criteria established

---

## Implementation Roadmap

### Phase 2: Non-Destructive Restructuring (NEXT)
**Objective:** Create new directory structure and move artifacts without breaking functionality

**Tasks:**
1. Create `domain/` and `self-improvement/` directories
2. Move production code to `domain/` (features, models, orchestrator, etc.)
3. Move self-improvement code to `self-improvement/` (santiago-pm, kanban tools, etc.)
4. Update import statements and references
5. Validate no breaking changes

**Success Criteria:**
- All files moved to correct locations per triage report
- No import errors or broken references
- CI/CD pipelines still functional
- Agents can navigate new structure

### Phase 3: Documentation Consolidation
**Objective:** Establish single source of truth for documentation

**Tasks:**
1. Move `GLOSSARY.md` to `docs/glossary/`
2. Create `docs/architecture/` with merged plan as primary
3. Consolidate architecture docs with clear hierarchy
4. Update all references and links
5. Archive superseded documentation

### Phase 4: Runtime Validation
**Objective:** Ensure autonomous agents work in new structure

**Tasks:**
1. Test autonomous agent operations
2. Validate CI/CD pipelines
3. Monitor for breaking changes
4. Document lessons learned

---

## Risk Assessment & Mitigation

### High-Risk Items
1. **Import/Reference Updates:** Systematic update plan required
   - Mitigation: Phase-by-phase updates with validation
2. **CI/CD Pipeline:** Must pass for all moved code
   - Mitigation: Comprehensive testing before Phase 3
3. **Agent Navigation:** Autonomous agents must adapt
   - Mitigation: Clear documentation and gradual transition
4. **Historical Access:** Archived files must remain accessible
   - Mitigation: Maintain reference links and searchability

### Success Metrics
- Repository structure matches target architecture (95% alignment)
- Zero production outages during migration
- Agent autonomy maintained or improved
- Documentation provides clear guidance

---

## Deliverables Created

### Documentation
- `expeditions/exp_057/README.md` - Expedition overview
- `expeditions/exp_057/triage-report.md` - Root artifact analysis
- `docs-arch-redux-3/questions.md` - Captain review questions & responses
- `santiago-pm/cargo-manifests/architecture-migration-epic.md` - Kanban epic

### Code Changes
- Updated `santiago-pm/tackle/folder-structure.md` - Two-namespace documentation
- Extended `GLOSSARY.md` - New architecture terms

### Analysis
- Comprehensive artifact triage with 25+ files categorized
- 5 key decisions documented with rationale
- Implementation roadmap with 4 phases
- Risk assessment and mitigation strategies

---

## Next Steps

1. **Phase 2 Execution:** Begin non-destructive restructuring
2. **Validation:** Test all changes incrementally
3. **Captain Check-ins:** Regular progress updates
4. **Phase Transitions:** Clear go/no-go criteria for each phase

**Expedition Lead:** Santiago-PM (Autonomous Agent)
**Captain:** Hank
**Status:** Ready for Phase 2 - Awaiting execution approval</content>
<parameter name="filePath">/Users/hankhead/Projects/Personal/nusy-product-team/expeditions/exp_057/expedition-logs.md