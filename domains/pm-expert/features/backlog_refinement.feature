Feature: PM Domain Backlog Refinement
  As a product team using Santiago PM
  I want autonomous backlog refinement guidance
  So that our backlog stays healthy and prioritized

  Background:
    Given the PM domain expert is initialized
    And the Pilot agent is available

  Scenario: Basic backlog refinement
    Given a backlog with 50 items
    And prioritization criteria include value and risk
    When the Pilot facilitates backlog refinement
    Then refinement guidance should be provided
    And acceptance criteria clarification should be suggested
    And effort estimation guidance should be included
    And prioritization recommendations should be made

  Scenario: Refining large backlog items
    Given backlog items that are too large
    And items estimated at 20+ story points
    When the Pilot facilitates backlog refinement
    Then the Pilot should recommend breaking down large items
    And vertical slicing guidance should be provided
    And each slice should deliver value

  Scenario: Identifying dependencies
    Given backlog items with technical dependencies
    And items that must be completed in sequence
    When the Pilot facilitates backlog refinement
    Then dependencies should be identified
    And proper ordering should be recommended
    And risk mitigation should be suggested

  Scenario: Removing outdated items
    Given backlog items created 6+ months ago
    And items no longer aligned with product vision
    When the Pilot facilitates backlog refinement
    Then outdated items should be identified
    And removal or archival should be recommended
    And backlog health should improve

  Scenario: Prioritization by value
    Given multiple high-value features
    And limited team capacity
    When the Pilot facilitates prioritization
    Then value assessment framework should be applied
    And trade-offs should be analyzed
    And recommendations should maximize user value
    And ethical implications should be considered
