---
id: pm-artifact-linting-001
type: feature
status: open
state_reason: null
created_at: 2025-11-16T00:00:00Z
updated_at: 2025-11-16T00:00:00Z
assignees: ["santiago-pm"]
labels: ["type:feature", "priority:medium", "component:standards", "nautical:theming"]
epic: nusy-v2-architecture
domain: product-management
owners: ["santiago-pm"]
stakeholders: ["santiago-architect", "santiago-ethicist"]
skill_level: journeyman
knowledge_scope: lake
artifact_kinds: ["lint", "validation", "report"]
related_experiments: []
related_artifacts:
  - ./pm-artifact-templates-and-standards.feature
  - ./pm-artifact-validation.feature
---

Feature: Lint existing PM artifacts for compliance with standards

  As Santiago-PM
  I want to lint existing PM artifacts for compliance
  So that I can report inconsistencies and guide cleanup and migration

  Background:
    Given the PM artifact templates and standards are defined
    And validation rules for metadata, naming, and theming are available
    And Santiago-PM MUST NOT modify artifacts during linting
    And linting results are written to ships-logs for later review

  Scenario: Run a non-destructive lint pass over PM artifacts
    Given existing PM artifacts are stored under the santiago-pm folders
    When a PM artifact lint run is triggered
    Then Santiago-PM MUST scan all artifacts in:
      | path                    |
      | ./                      |
      | ../                     |
      | ../../templates/        |
      | ../../knowledge/shared/ |
    And Santiago-PM MUST identify violations in at least these categories:
      | rule_category              |
      | missing_metadata_fields    |
      | invalid_metadata_format    |
      | invalid_naming_convention  |
      | missing_nautical_theming   |
      | inconsistent_labels        |
      | missing_related_artifacts  |
    And Santiago-PM MUST produce a lint report at:
      """ships-logs/pm-standards-lint.md"""

  Scenario: Structure of the lint report
    Given the lint report has been generated
    When a crew member opens ships-logs/pm-standards-lint.md
    Then the report MUST contain entries grouped by severity:
      | severity   |
      | error      |
      | warning    |
      | info       |
    And each entry MUST include:
      | field          |
      | artifact_path  |
      | rule_category  |
      | severity       |
      | message        |
      | suggested_fix  |
    And the report MUST include a summary section with:
      | summary_field       |
      | total_artifacts     |
      | total_errors        |
      | total_warnings      |
      | total_infos         |

  Scenario: Support for future automated remediation
    Given Santiago-PM has produced a lint report
    When a future remediation feature is implemented
    Then the lint report structure MUST support:
      | requirement                     |
      | mapping to cleanup milestones   |
      | mapping to specific rules       |
      | mapping to specific features    |
    And the lint report MUST be suitable input for:
      | consumer             |
      | Santiago-PM cleanup planning |
      | Santiago-TeamCoordinator     |
      | Santiago-Ethicist review     |