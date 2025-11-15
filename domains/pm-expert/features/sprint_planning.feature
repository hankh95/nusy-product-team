Feature: PM Domain Sprint Planning
  As a product team using Santiago PM
  I want autonomous sprint planning facilitation
  So that we can plan sprints effectively with AI guidance

  Background:
    Given the PM domain expert is initialized
    And the Pilot agent is available
    And the Quartermaster ethical overseer is available
    And the knowledge graph contains sprint planning concepts

  Scenario: Basic sprint planning facilitation
    Given a team with velocity of 30 story points
    And a backlog with 10 ready items
    When the Pilot facilitates sprint planning
    Then sprint planning guidance should be provided
    And the guidance should include sprint goal recommendations
    And the guidance should include item selection criteria
    And the Quartermaster should approve the approach ethically
    And the approach should ensure fair work distribution
    And the approach should promote sustainable pace

  Scenario: Sprint planning with unclear goal
    Given a team with velocity of 25 story points
    And a backlog with ready items
    But no sprint goal is defined
    When the Pilot facilitates sprint planning
    Then the Pilot should help define a clear sprint goal
    And the goal should align with product objectives
    And the goal should be achievable within the sprint
    And team commitment should be sought

  Scenario: Sprint planning with capacity constraints
    Given a team with reduced capacity due to holidays
    And historical velocity of 30 story points
    And current capacity is 20 story points
    When the Pilot facilitates sprint planning
    Then the Pilot should recommend adjusting commitments
    And the ethical review should validate sustainable pace
    And the plan should account for team wellbeing

  Scenario: Sprint planning with high-risk items
    Given a backlog containing high-risk items
    And dependencies between multiple items
    When the Pilot facilitates sprint planning
    Then risk mitigation strategies should be included
    And dependencies should be identified
    And contingency plans should be recommended

  Scenario: Ethical validation of sprint planning
    Given a proposed sprint plan
    When the Quartermaster reviews the plan
    Then Baha'i principles should be applied
    And service to humanity should be validated
    And fair work distribution should be confirmed
    And consultation approach should be verified
    And team wellbeing should be assessed
