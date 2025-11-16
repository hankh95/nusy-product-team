# Architecture Redux Prompt v2 — AI Comparison Ready (2025-11-16)

Paste this prompt into any AI tool while seated at the root of `nusy-product-team`. It encodes updated guidance from the v2 analysis and research set, and standardizes outputs for fair cross-AI comparison.

---

You are an AI Software Architect & Refactoring Planner for the `nusy-product-team` repository.

## Mission

1. Load the repo root (`nusy-product-team`). Scan at minimum:
   - `src/nusy_pm_core/`
   - `santiago_core/`
   - `knowledge/` (if missing, note it as a gap)
   - `notes/`, `DEVELOPMENT_PLAN.md`, `DEVELOPMENT_PRACTICES.md`
   - Skip reading `ocean-arch-redux/` entirely until you finish your initial deliverables (see Independence below). You will write your outputs there.
2. Digest research under `ocean-research/` (DGX/Manolin, fake-team packs, shared memory specs, Santiago role descriptions). Treat these as the target-state truth.
3. Compare current vs desired architecture focusing on:
   - MCP-based Santiago agents (PM, Ethicist, Architect, Developers, QA/UX, Hank-as-Captain)
   - Shared team memory: `knowledge/shared/*`, `knowledge/domains/*`, `knowledge/shared/team-roster-and-capabilities.ttl`, and `knowledge/shared/ships-log/`
   - Apprentice/Journeyman/Master skill levels + Pond/Lake/Sea/Ocean knowledge scopes
   - DGX Spark / Manolin cluster deployment expectations
4. Produce planning artifacts only inside `ocean-arch-redux/arch-redux-<model_name>-v2-plan/`.

## Required Deliverables (Use today’s date in headings)

1. `ARCHITECTURE_PLAN.md`
   - Current architecture summary (FastAPI orchestrator, `santiago_core` local agents, lack of shared knowledge).
   - Target architecture (MCP services per role, shared knowledge tree, ethics guardrails, DGX deployment).
   - Key deltas: MCP manifests, shared memory contracts, orchestrator evolution, DGX readiness, concurrency + ethics enforcement.
2. `MIGRATION_STEPS.md`
   - 3–7 milestones. For each: goals, affected paths, concrete tasks (checklists or BDD scenarios), and acceptance criteria.
   - Ensure coverage of: shared knowledge folder, MCP manifests (PM and Ethicist first), NuSy orchestrator refactor, concurrency/test harness, DGX deployment.
3. `FOLDER_LAYOUT_PROPOSAL.md` (strongly recommended)
   - Proposed tree for `knowledge/`, `santiago_core/agents/<role>/service`, MCP registry, infrastructure scripts.
   - Mapping table from current paths to target locations with actions (extract, consolidate, deprecate).
4. `RELEVANCE_MAP.md`
   - Classify folders/files as Relevant / Peripheral / Legacy-Duplicate / Irrelevant with short rationale.
5. `ASSUMPTIONS_AND_RISKS.md` (1 page)
   - Explicit assumptions, key risks, mitigations, and open questions.

## Independence & Calibration

- Independence: Do not read any prior outputs in `ocean-arch-redux/` until all deliverables above are drafted.
- Calibration (optional, after submission): Compare your `RELEVANCE_MAP.md` against `ocean-arch-redux/arch-redux-gpt-5-v2-plan/RELEVANCE_MAP.md`. Record any confirmations or justified divergences in a short appendix at the bottom of your own relevance map. Do not copy prior content verbatim.

## Behavioral Guardrails

- Plan-only phase: Do not modify existing core code outside `ocean-arch-redux/`.
- Reference research facts explicitly (cite filenames) when recommending changes, e.g., `ocean-research/nusy_manolin_architecture.md`.
- Encode role metadata (skill level + knowledge scope) in every roster/manifests you scaffold.
- Describe how fake-team mode works today vs the DGX/Manolin future; provide interim steps if DGX is unavailable.
- Surface risks: missing `knowledge/` folder, lack of MCP manifests, absent DGX runbooks, insufficient audit/ethics enforcement.
- Outputs must be lint-friendly Markdown; any TTL scaffolds must be valid Turtle.

## Reference Threads (must use and cite)

- `ocean-research/dgx_spark_nusy_report.md`
- `ocean-research/nusy_manolin_architecture.md`
- `ocean-research/nusy_manolin_provisioning_automation.md`
- `ocean-research/nusy_manolin_multi_agent_test_plans.md`
- `ocean-research/fake_team_feature_plan.md`
- `ocean-research/fake_team_steps_for_hank_and_copilot.md`
- `ocean-research/.../feature/capability specs for Santiago-PM/Ethicist and shared memory`

## Output Expectations

- Use today’s date in top-level headings across all deliverables.
- Cross-link tasks to the knowledge folder (e.g., “Writes to `knowledge/shared/ships-log/YYYY-MM-DD-<slug>.md`).
- Call out how Hank (Captain) participates (ships logs, approvals, DGX ordering).
- Emphasize concurrency + ethics gating derived from `ocean-research/nusy_manolin_multi_agent_test_plans.md`.
- Note the existence of scaffolds: `scaffolds/mcp-manifest-template.json` and `scaffolds/roster-entry-template.ttl` for reuse by future agents.

## Scoring Rubric (for AI comparison)

- Coverage: MCP, knowledge, DGX, ethics/concurrency all addressed.
- Evidence: Specific citations to `ocean-research/*` and concrete code paths.
- Specificity: Clear interfaces/contracts and actionable migration tasks.
- Feasibility: Sensible sequencing, risks, and acceptance criteria.
- Independence: Own relevance map produced before calibration.
- Quality: Lint-ready Markdown and coherent cross-linking.

## Submission Checklist

- [ ] All required deliverables present under `ocean-arch-redux/arch-redux-<model_name>-v2-plan/`.
- [ ] Each doc includes today’s date in a heading.
- [ ] Citations to `ocean-research/*` provided for major claims.
- [ ] `RELEVANCE_MAP.md` completed independently; optional calibration appendix included if performed.
- [ ] No changes outside `ocean-arch-redux/`.
- [ ] Markdown lints pass; any Turtle snippets validate.
