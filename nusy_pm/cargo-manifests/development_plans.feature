Feature: Development Plans Management
  As a PM agent
  I want to manage development plans
  So that I can track project milestones, tasks, and dependencies

  Background:
    Given the development plans service is initialized
    And the knowledge graph is available

  Scenario: Create a new development plan
    When I create a development plan with title "Santiago MVP" and description "Build the first Santiago iteration"
    Then the plan should be stored with correct metadata
    And the plan should be retrievable by ID
    And the plan should appear in the knowledge graph

  Scenario: Add milestone to development plan
    Given a development plan exists
    When I add a milestone "Complete web interface" with due date and description
    Then the milestone should be linked to the plan
    And the milestone status should be tracked
    And dependencies between milestones should be manageable

  Scenario: Track task progress
    Given a milestone exists with tasks
    When I update a task status to "completed"
    Then the milestone progress should be recalculated
    And the plan progress should be updated
    And the knowledge graph should reflect current status

  Scenario: Query plan status
    Given multiple plans exist with different statuses
    When I query for active plans
    Then I should get plans with incomplete milestones
    And I should see progress indicators
    And I should be able to filter by various criteria