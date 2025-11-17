@passage_orchestration @capability_journeyman @knowledge_scope_lake
Feature: Monitor passage execution
  Query execution status, view step history, track completion percentage, receive notifications
  
  Background:
    Given Santiago PM MCP is running
    And the knowledge graph is initialized
    And the user has Journeyman capability level

  Scenario: Monitor passage execution with valid inputs (happy path)
    Given the user provides valid input data for monitor_passage_execution
    When the monitor_passage_execution behavior is invoked
    Then a new Passage node is queried in the knowledge graph
    And the response contains the expected output fields
    And the operation completes successfully

  Scenario: Monitor passage execution with edge case inputs (edge case)
    Given the user provides minimal or optional field data for monitor_passage_execution
    When the monitor_passage_execution behavior is invoked
    Then the operation handles the edge case gracefully
    And default values are applied where appropriate
    And the response indicates partial success or warnings

  Scenario: Monitor passage execution with missing required fields (error handling)
    Given the user provides incomplete data missing required fields
    When the monitor_passage_execution behavior is invoked
    Then an error is returned with message "Missing required field"
    And the knowledge graph remains unchanged
    And the error includes details about which fields are missing
