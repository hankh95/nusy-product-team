@issue_tracking @capability_apprentice @knowledge_scope_pond @mutates_kg
Feature: Log issue
  Create ship's log entry for bugs, blockers, technical debt
  
  Background:
    Given Santiago PM MCP is running
    And the knowledge graph is initialized
    And the user has Apprentice capability level

  Scenario: Log issue with valid inputs (happy path)
    Given the user provides valid input data for log_issue
    When the log_issue behavior is invoked
    Then a new Issue node is created in the knowledge graph
    And the response contains the expected output fields
    And the operation completes successfully

  Scenario: Log issue with edge case inputs (edge case)
    Given the user provides minimal or optional field data for log_issue
    When the log_issue behavior is invoked
    Then the operation handles the edge case gracefully
    And default values are applied where appropriate
    And the response indicates partial success or warnings

  Scenario: Log issue with missing required fields (error handling)
    Given the user provides incomplete data missing required fields
    When the log_issue behavior is invoked
    Then an error is returned with message "Missing required field"
    And the knowledge graph remains unchanged
    And the error includes details about which fields are missing
