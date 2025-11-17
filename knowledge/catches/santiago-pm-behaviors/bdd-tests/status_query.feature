@status_management @capability_apprentice @knowledge_scope_pond
Feature: Query artifacts by status
  Query artifacts by status, assignee, update date, or artifact type
  
  Background:
    Given Santiago PM MCP is running
    And the knowledge graph is initialized
    And the user has Apprentice capability level

  Scenario: Query artifacts by status with valid inputs (happy path)
    Given the user provides valid input data for status_query
    When the status_query behavior is invoked
    Then a new StatusTransition node is queried in the knowledge graph
    And the response contains the expected output fields
    And the operation completes successfully

  Scenario: Query artifacts by status with edge case inputs (edge case)
    Given the user provides minimal or optional field data for status_query
    When the status_query behavior is invoked
    Then the operation handles the edge case gracefully
    And default values are applied where appropriate
    And the response indicates partial success or warnings

  Scenario: Query artifacts by status with missing required fields (error handling)
    Given the user provides incomplete data missing required fields
    When the status_query behavior is invoked
    Then an error is returned with message "Missing required field"
    And the knowledge graph remains unchanged
    And the error includes details about which fields are missing
