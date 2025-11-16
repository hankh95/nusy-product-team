---
id: ci-lint-changed-markdown-001
type: feature
status: open
state_reason: null
created_at: 2025-11-16T00:00:00Z
updated_at: 2025-11-16T00:00:00Z
assignees: ["platform", "santiago-pm"]
labels: ["type:feature", "priority:medium", "component:ci", "component:linting"]
epic: nusy-v2-architecture
domain: platform-engineering
owners: ["platform"]
stakeholders: ["santiago-pm", "santiago-architect"]
skill_level: journeyman
knowledge_scope: lake
artifact_kinds: ["ci", "lint", "workflow"]
related_experiments: []
related_artifacts:
  - ../../calibration/README.md
  - ../../architecture-redux-prompt-v2.md
---

Feature: CI lints only changed Markdown files

  As a Platform Engineer
  I want CI to lint only changed Markdown files on PRs
  So that legacy docs don’t block progress while we harden them separately

  Background:
    Given repo-wide Markdown linting is configured via markdownlint-cli2
    And independence/calibration rules are documented for AI runs
    And legacy docs may intentionally violate style until hardened

  @ci @lint @pull_request
  Scenario: Lint changed Markdown files on pull_request events
    Given a GitHub Actions workflow is triggered on pull_request
    And the event type is one of: opened, reopened, synchronize
    When the workflow computes the list of changed files since the base branch
    Then it MUST filter for paths matching "**/*.md"
    And if the filtered list is non-empty, it MUST run:
      """
      npx markdownlint-cli2 <CHANGED_MD_FILE_LIST>
      """
    And it MUST fail the job on lint errors
    And it MUST post a concise summary with the failing paths

  @ci @lint
  Scenario: Skip markdown lint step when no Markdown changed
    Given the computed changed file list contains no "*.md" files
    Then the markdown lint step MUST be skipped
    And the job MUST succeed with a note "no markdown changes detected"

  @local @make
  Scenario: Provide a local helper to lint only changed/staged Markdown
    Given a developer runs a make target named "lint-changed"
    When the target resolves the list of staged or HEAD~..HEAD changed "*.md" files
    Then it MUST run markdownlint-cli2 against that list
    And return a non-zero exit code on failures

  @acceptance
  Scenario: Acceptance criteria for completion
    Then a new or updated workflow under ".github/workflows/" implements the changed-file lint behavior
    And the Makefile exposes a target "lint-changed" to lint staged/HEAD changes locally
    And documentation in "README.md" or "calibration/README.md" references this behavior
    And CI on PRs no longer fails due to untouched legacy Markdown files
