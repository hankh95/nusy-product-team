---
id: status-system-001
type: feature
status: closed
state_reason: completed
created_at: 2025-11-15T12:30:00Z
updated_at: 2025-11-15T12:30:00Z
assignees: ["architect"]
labels: ["type:feature", "priority:high", "component:status-system"]
epic: nusy-pm-core
related_experiments: []
related_artifacts:
  - ../tackle/status/status-system.md
---

Feature: NuSy PM Status System
  As a NuSy PM service
  I want to track status of all artifacts
  So that the system can query and report on work progress

  Background:
    Given the status system is implemented
    And all artifacts have YAML frontmatter
    And the knowledge graph is available

  Scenario: Query feature status via CLI
    When I run `nusy query status --type feature --status open`
    Then I see all features with status "open"
    And each result includes id, title, assignees, and labels
    And results are sorted by updated_at descending

  Scenario: Update artifact status
    Given an artifact exists with status "open"
    When I update its status to "in_progress"
    Then the YAML frontmatter is updated
    And the knowledge graph triples are updated
    And the updated_at timestamp is refreshed

  Scenario: Close artifact with reason
    Given an artifact exists with status "in_progress"
    When I close it with reason "completed"
    Then the status becomes "closed"
    And state_reason is set to "completed"
    And the knowledge graph reflects the final state

  Scenario: Status dashboard generation
    Given multiple artifacts exist with different statuses
    When I run `nusy dashboard status`
    Then I see a summary of all artifact types
    And status distributions are shown
    And recent updates are highlighted

  Scenario: Knowledge graph status queries
    Given artifacts are stored in the knowledge graph
    When I query for "in_progress" features
    Then I get all features with that status
    And related triples are included in results

  Scenario: Status validation on file changes
    Given an artifact file is modified
    When the status fields are invalid
    Then validation fails
    And appropriate error messages are shown
    And the file is not accepted until fixed