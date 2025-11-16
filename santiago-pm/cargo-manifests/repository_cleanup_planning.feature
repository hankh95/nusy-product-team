---
id: repository-cleanup-planning-001
type: feature
status: open
state_reason: null
created_at: 2025-11-16T00:00:00Z
updated_at: 2025-11-16T00:00:00Z
assignees: ["santiago-pm", "santiago-ethicist"]
labels: ["type:feature", "priority:high", "component:repository-management", "phase:planning-only"]
epic: nusy-v2-architecture
related_experiments: []
related_artifacts:
  - ../../ocean-research/
  - ../../ocean-research/GPT-revised-architecture/
  - ../../ocean-research/building-on-DGX/
  - REPOSITORY_CLEANUP_PLAN.md
  - FOLDER_LAYOUT_PROPOSAL.md
  - MIGRATION_STEPS_FOR_CLEANUP.md
---

Feature: Repository cleanup planning led by Santiago-PM
  As Santiago-PM
  I want to analyze the existing repository and propose a cleanup and migration plan
  So that future agents and humans do not have to wade through obsolete or stray files

  Background:
    Given the project root is the "nusy-product-team" repository
    And the "ocean-research" folder contains the latest architecture and platform research
    And Santiago-PM has access to the shared knowledge folder layout specification
    And Santiago-PM MUST NOT delete, move, or rename any existing files in this phase

  @analysis
  Scenario: Identify candidate files and folders for archival or deprecation
    When Santiago-PM scans the repository structure and key code/knowledge directories
    Then Santiago-PM MUST produce a "REPOSITORY_CLEANUP_PLAN.md" in the ocean-arch-redux area
    And the plan MUST list files and folders grouped into the following categories:
      | category          |
      | Safe to keep      |
      | Safe to archive   |
      | Needs review      |
      | Likely deprecate  |
    And each item in the plan MUST include:
      | field                 |
      | path                  |
      | reasoning             |
      | suggested_category    |
      | suggested_new_location |
    And the plan MUST explicitly state that no files were modified in this phase

  @architecture
  Scenario: Propose a target folder structure for nusy-v2
    When Santiago-PM compares the current repository structure
      And the desired architecture from the ocean-research documents
    Then Santiago-PM MUST propose a canonical "nusy-v2" folder layout
    And the layout MUST support:
      | requirement                                 |
      | Santiago-PM and Santiago-Ethicist agents    |
      | MCP-exposed role agents (PM, Architect, Dev, QA, etc.) |
      | Shared knowledge and ships-log folders      |
      | Domain-specific knowledge per Santiago      |
      | Future DGX / Manolin deployment             |
    And the proposed layout MUST be written to "FOLDER_LAYOUT_PROPOSAL.md"
      in the same ocean-arch-redux planning area

  @migration
  Scenario: Plan a safe migration and deprecation strategy
    Given the "REPOSITORY_CLEANUP_PLAN.md" exists
      And the "FOLDER_LAYOUT_PROPOSAL.md" exists
    When Santiago-PM designs a migration strategy
    Then Santiago-PM MUST create a "MIGRATION_STEPS_FOR_CLEANUP.md"
      in the ocean-arch-redux planning area
    And the migration plan MUST be broken into 3 to 7 milestones
    And each milestone MUST include:
      | field                 |
      | milestone_name        |
      | goals                 |
      | affected_paths        |
      | actions               |
      | risks                 |
      | rollback_considerations |
    And the plan MUST explicitly state:
      """
      Actual file moves and deletions will be performed later
      by Santiago-PM and development agents with human approval from Hank.
      This phase is planning-only.
      """

  @ethics
  Scenario: Require ethical and historical review before destructive cleanup
    Given Santiago-Ethicist is available as a team member
    And the cleanup plan and migration steps have been drafted
    When Santiago-PM marks certain files or folders as "Likely deprecate"
    Then Santiago-PM MUST request an ethics review from Santiago-Ethicist
    And Santiago-Ethicist MUST write an entry in "evolution-reviews.md"
      explaining any risks of losing historical knowledge or provenance
    And Santiago-Ethicist MAY recommend:
      | action                         |
      | archival instead of deletion   |
      | stricter review requirements   |
      | additional logging or backup   |

  @approval
  Scenario: Require Hank’s approval before any destructive changes
    Given the repository cleanup plan and migration steps are ready
      And Santiago-Ethicist has completed the ethics review
    When Santiago-PM is ready to initiate actual file moves or deletions
    Then Santiago-PM MUST present a human-readable summary of the plan to Hank
    And Santiago-PM MUST record Hank’s approval status in the ships-log
    And no destructive actions MAY be taken unless Hank has explicitly approved
      the corresponding milestone or step