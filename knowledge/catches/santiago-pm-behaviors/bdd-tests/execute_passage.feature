@passage_orchestration @capability_master @knowledge_scope_sea @mutates_kg
Feature: Execute passage
  Start passage execution with trigger conditions, orchestrate steps, manage state transitions, track artifacts
  
  Background:
    Given Santiago PM MCP is running
    And the knowledge graph is initialized
    And the user has Master capability level

  Scenario: Execute passage with valid inputs (happy path)
    Given the user provides valid input data for execute_passage
    When the execute_passage behavior is invoked
    Then a new Passage node is created in the knowledge graph
    And the response contains the expected output fields
    And the operation completes successfully

  Scenario: Execute passage with edge case inputs (edge case)
    Given the user provides minimal or optional field data for execute_passage
    When the execute_passage behavior is invoked
    Then the operation handles the edge case gracefully
    And default values are applied where appropriate
    And the response indicates partial success or warnings

  Scenario: Execute passage with missing required fields (error handling)
    Given the user provides incomplete data missing required fields
    When the execute_passage behavior is invoked
    Then an error is returned with message "Missing required field"
    And the knowledge graph remains unchanged
    And the error includes details about which fields are missing
