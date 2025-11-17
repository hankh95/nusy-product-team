@experiment_management @capability_master @knowledge_scope_sea @mutates_kg
Feature: Analyze experiment outcomes
  Statistical analysis of experiment data, hypothesis validation, recommendation generation
  
  Background:
    Given Santiago PM MCP is running
    And the knowledge graph is initialized
    And the user has Master capability level

  Scenario: Analyze experiment outcomes with valid inputs (happy path)
    Given the user provides valid input data for analyze_experiment_outcomes
    When the analyze_experiment_outcomes behavior is invoked
    Then a new Experiment node is created in the knowledge graph
    And the response contains the expected output fields
    And the operation completes successfully

  Scenario: Analyze experiment outcomes with edge case inputs (edge case)
    Given the user provides minimal or optional field data for analyze_experiment_outcomes
    When the analyze_experiment_outcomes behavior is invoked
    Then the operation handles the edge case gracefully
    And default values are applied where appropriate
    And the response indicates partial success or warnings

  Scenario: Analyze experiment outcomes with missing required fields (error handling)
    Given the user provides incomplete data missing required fields
    When the analyze_experiment_outcomes behavior is invoked
    Then an error is returned with message "Missing required field"
    And the knowledge graph remains unchanged
    And the error includes details about which fields are missing
