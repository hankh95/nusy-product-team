Feature: Issues Management
  As a development team member
  I want to manage issues
  So that I can track bugs, features, and tasks

  Background:
    Given the issues service is initialized
    And the knowledge graph is available

  Scenario: Create a new issue
    When I create an issue with title "Fix login bug" and description "Users cannot log in with valid credentials"
    Then the issue should be stored with correct metadata
    And the issue should have a unique ID
    And the issue should appear in the knowledge graph

  Scenario: Assign issue to team member
    Given an issue exists
    When I assign it to a team member "alice"
    Then the assignee should be recorded
    And the assignment should be tracked in the knowledge graph
    And notifications should be possible

  Scenario: Add labels and status to issue
    Given an issue exists
    When I add labels ["bug", "high-priority"] and set status to "in-progress"
    Then the labels should be attached to the issue
    And the status should be updated
    And the issue should be queryable by labels and status

  Scenario: Add comments to issue
    Given an issue exists
    When I add a comment "Investigating the root cause"
    Then the comment should be attached to the issue
    And the comment should have timestamp and author
    And the comment thread should be maintained

  Scenario: Link issue to code changes
    Given an issue exists
    When I link it to commits or pull requests
    Then the links should be stored
    And the issue status should reflect code changes
    And the knowledge graph should connect issues to code artifacts

  Scenario: Query issues by various criteria
    Given multiple issues exist with different labels and statuses
    When I query issues by label "bug" and status "open"
    Then I should get matching issues
    And I should be able to sort by priority, creation date, etc.
    And I should see issue relationships and dependencies