# Architecture Review Evaluation Harness

This harness compares multi-model outputs produced from `architecture-redux-prompt-v2.md`.

## Directory Conventions

Each model writes deliverables under:

```text
ocean-arch-redux/arch-redux-<model_name>-v2-plan/
```

Required files (from prompt):

- ARCHITECTURE_PLAN.md
- MIGRATION_STEPS.md
- FOLDER_LAYOUT_PROPOSAL.md (recommended but scored if present)
- RELEVANCE_MAP.md
- ASSUMPTIONS_AND_RISKS.md

## Metrics (Automated)

1. presence.required_files: Boolean per required artifact.
2. headings.date_present: Date token (YYYY-MM-DD) appears in top-level heading of each file.
3. coverage.sections: Counts of rubric areas addressed (MCP, knowledge, DGX, ethics/concurrency) in ARCHITECTURE_PLAN.md.
4. citations.total & citations.coverage: Number of distinct `ocean-research/` references; ratio vs expected reference list.
5. specificity.interfaces: Count of lines mentioning `manifest`, `interface`, `contract`, `TTL`, `service`.
6. migration.milestone_count: Number of milestones (MIGRATION_STEPS.md).
7. migration.avg_tasks_per_milestone: Derived from checklist items per milestone.
8. migration.acceptance_criteria_count: Lines containing `Acceptance` or checklist items tagged.
9. relevance.independence: Calibration appendix appears only after core map content (heuristic: `## Calibration` after first classification table).
10. risks.count: Number of lines containing `risk` (case-insensitive) in ASSUMPTIONS_AND_RISKS.md.
11. mitigations.count: Lines containing `mitigation`.
12. knowledge.cross_links: References to `knowledge/` paths.
13. ships_log.links: References to `ships-log`.
14. lexical.token_count & lexical.type_token_ratio.
15. readability.flesch (approximate; English assumptions).
16. lint.markdown_pass: Markdown lint result (requires markdownlint CLI installed) – optional fallback: skipped.
17. novelty.embedding_similarity: Placeholder; compute cosine similarity to baseline model output (requires embedding provider).
18. ethics.concurrency_mentions: Count of lines referencing both `ethic` and `concurrency` or gating terms.
19. assumptions.count: Lines containing `assumption`.
20. checklist.total: All `- [ ]` occurrences across files.

## Metrics (Manual / Semi-Automated)

- feasibility.score (1–5)
- clarity.score (1–5)
- risk_depth.score (1–5)
- delta_quality.notes

Manual scores are appended to results JSON after review using `evaluation/manual_scores.yaml`.

## JSON Schema (results)

Stored at `evaluation/review_output_schema.json` for aggregator validation.

## Workflow

1. Generate model outputs by running the prompt separately for each model.
2. Place plan directory under `ocean-arch-redux/` exactly matching naming convention.
3. Configure models/weights in `evaluation/models-config.yaml`.
4. Run metrics collection:

```bash
python evaluation/evaluate_arch_reviews.py --plans-root ocean-arch-redux --config evaluation/models-config.yaml --out evaluation/results/metrics-$(date +%Y%m%d-%H%M%S).json
```

5. (Optional) Append manual scores:

```bash
python evaluation/evaluate_arch_reviews.py --append-manual --input evaluation/results/metrics-<timestamp>.json --manual evaluation/manual_scores.yaml
```

6. View weighted leaderboard:

```bash
python evaluation/evaluate_arch_reviews.py --leaderboard evaluation/results/metrics-<timestamp>.json
```

## Extensibility

- Add embedding similarity by configuring provider env vars (see script header).
- Add semantic concept coverage by supplying a glossary file (`evaluation/concepts.txt`).

## Baseline

The directory `arch-redux-gpt-5-v2-plan` is treated as baseline for novelty calculations.

## Security / Independence

The script does not modify plan directories; it only reads. Ensure independence rules are respected during generation before running evaluations.

## Next Steps

- Implement concept glossary parsing.
- Add Turtle validation counts if TTL snippets are introduced.
