# Phase 2 Questions: Non-Destructive Restructuring

## Expedition EXP-057: Architecture Redux 3 – Target Runtime & Repo Alignment

**Phase 2 Status:** Major directory restructuring completed, import updates and test distribution pending.

## Completed Phase 2 Work

✅ **Directory Structure Created:**

- `domain/` with subdirectories (domain-knowledge, domain-features, domain-expeditions, examples)
- `self-improvement/` with santiago-pm scaffold
- `knowledge/`, `tools/`, `configs/`, `_archive/` structure

✅ **Major File Moves Completed:**

- Demo scripts (`demo_*.py`) → `domain/examples/`
- `santiago-pm/` → `self-improvement/santiago-pm/`
- Production code: `features/`, `models/`, `nusy_orchestrator/`, `roles/`, `src/`, `templates/` → `domain/`
- Knowledge: `knowledge-graph/` → `domain/domain-knowledge/kg_views/`
- PM tools: `kanban-boards.md`, `kanban_regenerator.py`, `load_pm_knowledge.py` → `self-improvement/santiago-pm/tackle/tools/`
- Scripts: `scripts/` → `domain/`
- Config: `config/` contents → `configs/`

✅ **Archival Completed:**

- Historical docs → `_archive/legacy-docs/`
- Experimental code → `_archive/legacy-code/`

✅ **Documentation Consolidation Started:**

- Primary architecture docs → `docs/architecture/`
- Glossary → `docs/glossary/santiago-glossary.md`

## Questions Requiring Captain Approval

### 1. Test File Distribution Strategy

**Question:** How should the `tests/` directory be distributed to match the co-located testing principle?

**Current Status:** All tests still in root-level `tests/` directory with subdirectories `bdd/` and `integration/`.

**Analysis of Test Files:**

- `test_kanban_service.py` - Tests for `santiago_core/services/kanban_service.py` → should go to `santiago_core/tests/`
- `test_*_proxy.py` files - Test Santiago core proxy agents → `santiago_core/tests/`
- `test_api_clients.py` - Tests API client functionality → `domain/tests/` (if domain) or `santiago_core/tests/`
- `test_pr_workflow_manager.py` - Tests workflow management → `self-improvement/santiago-pm/tests/`
- `test_self_questioning_tool.py` - Tests self-improvement tools → `self-improvement/santiago-pm/tests/`
- `tests/bdd/` - BDD tests, need to determine which domain they test
- `tests/integration/` - Integration tests, need domain assignment

**Options:**

- **Option A**: Create `santiago_core/tests/`, `domain/tests/`, `self-improvement/santiago-pm/tests/` and distribute files
- **Option B**: Keep all tests in root `tests/` but reorganize subdirectories by domain
- **Option C**: Co-locate tests with source code (e.g., `santiago_core/tests/`, `domain/*/tests/`)

**Captain Response:** [Option A becuase I like the idea of keeping a domains experts tests close to their definitio. the self improvement tests should be close to the self improvement code and the santiago core tests should be close to the santiago core code.]]

### 2. Import Path Updates Strategy

**Question:** How should import statements be updated for moved modules?

**Current Issues Identified:**

- Files in `domain/src/` likely import from `santiago_core` - these paths should still work
- Files in `self-improvement/santiago-pm/tackle/` may need path updates
- Any imports of moved modules (like `nusy_orchestrator`) need updates

**Options:**

- **Option A**: Update all import statements to use absolute paths from repository root
- **Option B**: Add symbolic links or PYTHONPATH adjustments to maintain compatibility
- **Option C**: Update imports systematically with find/replace operations

**Captain Response:** [Option A - with an easily accessible guide for developers on how to structure imports in the new architecture. This ensures clarity and consistency across the codebase. AND a record of all the changes made for future reference.]]

### 3. Santiago-dev Directory Handling

**Question:** How should `santiago-dev/` be handled in the migration?

**Current Status:** `santiago-dev/` still exists at root level with autonomous workspace and development tools.

**Analysis:**

- Contains `autonomous_workspace/`, `continuous_autonomous_service.py`, development tools
- Seems to be development/testing environment for Santiago
- Could be self-improvement (development tools) or domain (testing environment)

**Options:**

- **Option A**: Move to `self-improvement/` as development infrastructure
- **Option B**: Move to `domain/` as testing/development environment
- **Option C**: Keep at root as development tooling (like `tools/`)

**Captain Response:** [Try to run the code to see what it does and then decide. My hunch is that it should go to self improvement but I want to be sure.]]

### 4. Remaining Root Artifacts

**Question:** How should these remaining root-level files be handled?

**Files Still at Root:**

- `API_CLIENT_IMPLEMENTATION.md` - API documentation
- `COMMIT_MESSAGE.txt` - Temporary file
- `CONTRIBUTING.md` - Contribution guidelines
- `examples/poll_pr_example.sh` - Example script
- `expeditions/` - Experimental work (should stay)
- `zarchive/migration-artifacts/` - Migration artifacts

**Options:**

- **Option A**: Move docs to `docs/`, examples to `domain/examples/`, archive temporaries
- **Option B**: Keep most at root as repository-level artifacts
- **Option C**: Move all to appropriate domain/self-improvement locations

**Captain Response:** [Try to uderstand the purpose of each file and move accordingly. My initial thought is that docs should go to docs, examples to domain/examples, and anything temporary or migration-related to _archive/. but this has to be tempered with what it's role is in the new architecture. Contributing.md should probably stay at root as it's a repository-level artifact, but really needs to be cleaned up OR write a link in it to where the master of "how to work on this team" lives - I think this is actually the kanban workflows etc. But we may want a human readable version with the link to the real thing (eg the kanban or other methods we develop for the process of getting work done.]

### 5. Phase 2 Completion Criteria

**Question:** What validation should be performed before declaring Phase 2 complete?

**Proposed Validation:**

- Directory structure matches target architecture
- No broken imports (basic syntax check)
- CI/CD still functional
- Key files accessible in new locations

**Options:**

- **Option A**: Basic validation (directory structure, import syntax)
- **Option B**: Full validation (run tests, check CI/CD, verify agent navigation)
- **Option C**: Minimal validation (just directory structure)

**Captain Response:** [Option B - but to do this right, we have to understand if the code we are tring to run is actually aligned with the new architecture. So we may have to do some code updates as part of this validation. But I want to be sure that the core capabilities (autonomous agents, knowledge ingestion, reasoning, kanban and other PM services) is working as expected before we move on to phase 3. Create check points if it is taking too long to do all at once.] 

## Risk Assessment

### High-Risk Items

1. **Import Path Breaking:** Moved modules may break existing code
2. **Test Distribution Errors:** Incorrect test placement could hide issues
3. **Agent Navigation:** Autonomous agents may not find moved artifacts
4. **CI/CD Pipeline:** Build/test scripts may reference old paths

**Captain Response:** [What are good software practices here? One idea would be to move the files AND keep them in the old location as symlinks for a period of time while we validate everything is working. This would reduce risk of breaking things while we do the transition. We could also have a mapping document that shows old paths to new paths for reference during this period that we tie to each running module or test. Third idea is to keep a working version of the old structure in a branch while we validate the new one and then switch over when we are sure everything is working.]

### Success Criteria

- Repository structure aligns with two-namespace model
- No immediate import errors
- Basic functionality preserved
- Clear path for Phase 3 import updates

## Next Steps After Captain Review

1. **Apply Captain Decisions:** Implement the approved distribution strategies
2. **Update Imports:** Fix import paths based on chosen strategy
3. **Validation:** Run basic checks to ensure no breaking changes
4. **Phase 3 Preparation:** Prepare for systematic import updates and reference fixes

## Contact

**Expedition Lead:** Santiago-PM (Autonomous Agent)
**Captain:** Hank
**Branch:** `exp-057-architecture-redux-3-migration`
