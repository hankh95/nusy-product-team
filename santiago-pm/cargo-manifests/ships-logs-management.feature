---
id: ships-logs-management-001
type: feature
status: open
state_reason: null
created_at: 2025-11-15T12:00:00Z
updated_at: 2025-11-15T12:00:00Z
assignees: ["architect", "developer"]
labels: ["type:feature", "priority:medium", "component:ships-logs"]
epic: nusy-pm-core
related_experiments: []
related_artifacts:
  - ../ships-logs/README.md
  - ../ships-logs/ships-log-slug.md
---

Feature: Ships Logs Management System
  As a NuSy development team member
  I want to manage ships logs through CLI and knowledge graph
  So that I can track issues, tasks, and progress effectively

  Background:
    Given the ships logs system is initialized
    And the knowledge graph is available
    And CLI tools are configured

  Scenario: Create a new ships log via CLI
    When I run `nusy ships-log create --agent santiago --description "component-diagrams"`
    Then a new ships log file is created with today's date
    And the log follows the standard template format
    And the log is registered in the knowledge graph
    And the log status is set to "open"

  Scenario: List ships logs by status
    Given there are ships logs with different statuses
    When I run `nusy ships-log list --status open`
    Then I see all open ships logs
    And each log shows its ID, title, assignee, and creation date
    And the results are sorted by creation date descending

  Scenario: Update ships log status
    Given a ships log exists with status "open"
    When I run `nusy ships-log update 2025-11-15-santiago-component-diagrams.md --status completed`
    Then the log status is updated to "completed"
    And the knowledge graph is updated with the new status
    And a timestamp is recorded for the status change

  Scenario: Search ships logs by assignee
    Given ships logs exist with different assignees
    When I run `nusy ships-log search --assignee santiago`
    Then I see all logs assigned to the Santiago agent
    And the results include logs from all time periods

  Scenario: Link ships log to related artifacts
    Given a ships log exists
    When I run `nusy ships-log link 2025-11-15-santiago-component-diagrams.md --artifact ../expeditions/autonomous-multi-agent-swarm/`
    Then the artifact relationship is recorded in the knowledge graph
    And the ships log shows the linked artifact
    And bidirectional navigation is possible

  Scenario: Generate ships log report
    Given ships logs exist over a time period
    When I run `nusy ships-log report --period 2025-11`
    Then a report is generated showing:
      | Metric | Value |
      | Total logs created | X |
      | Logs completed | Y |
      | Average completion time | Z days |
      | Top assignees | List |
      | Status distribution | Chart data |

  Scenario: Migrate numbered logs to date-based system
    Given numbered ships logs exist (001-011)
    When I run `nusy ships-log migrate`
    Then all numbered logs are converted to date-based names
    And original content is preserved
    And knowledge graph references are updated
    And backward compatibility redirects are created

  Scenario: Knowledge graph integration
    Given a ships log is created or updated
    When the knowledge graph processes the log
    Then the following triples are created:
      | Subject | Predicate | Object |
      | log-uuid | hasAssignee | agent-name |
      | log-uuid | hasStatus | status-value |
      | log-uuid | createdOn | date |
      | log-uuid | hasLabel | label-value |
    And the log is queryable through SPARQL
    And relationships to other artifacts are maintained