@feature_management @capability_journeyman @knowledge_scope_lake @mutates_kg
Feature: Define acceptance criteria
  Write testable, BDD-format acceptance criteria for features
  
  Background:
    Given Santiago PM MCP is running
    And the knowledge graph is initialized
    And the user has Journeyman capability level

  Scenario: Define acceptance criteria with valid inputs (happy path)
    Given the user provides valid input data for define_acceptance_criteria
    When the define_acceptance_criteria behavior is invoked
    Then a new Feature node is created in the knowledge graph
    And the response contains the expected output fields
    And the operation completes successfully

  Scenario: Define acceptance criteria with edge case inputs (edge case)
    Given the user provides minimal or optional field data for define_acceptance_criteria
    When the define_acceptance_criteria behavior is invoked
    Then the operation handles the edge case gracefully
    And default values are applied where appropriate
    And the response indicates partial success or warnings

  Scenario: Define acceptance criteria with missing required fields (error handling)
    Given the user provides incomplete data missing required fields
    When the define_acceptance_criteria behavior is invoked
    Then an error is returned with message "Missing required field"
    And the knowledge graph remains unchanged
    And the error includes details about which fields are missing
