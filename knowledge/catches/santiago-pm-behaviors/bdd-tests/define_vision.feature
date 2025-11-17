@strategic_planning @capability_expert @knowledge_scope_ocean @mutates_kg
Feature: Define vision
  Create high-level strategic vision with goals, principles, success metrics
  
  Background:
    Given Santiago PM MCP is running
    And the knowledge graph is initialized
    And the user has Expert capability level

  Scenario: Define vision with valid inputs (happy path)
    Given the user provides valid input data for define_vision
    When the define_vision behavior is invoked
    Then a new Plan node is created in the knowledge graph
    And the response contains the expected output fields
    And the operation completes successfully

  Scenario: Define vision with edge case inputs (edge case)
    Given the user provides minimal or optional field data for define_vision
    When the define_vision behavior is invoked
    Then the operation handles the edge case gracefully
    And default values are applied where appropriate
    And the response indicates partial success or warnings

  Scenario: Define vision with missing required fields (error handling)
    Given the user provides incomplete data missing required fields
    When the define_vision behavior is invoked
    Then an error is returned with message "Missing required field"
    And the knowledge graph remains unchanged
    And the error includes details about which fields are missing
