@passage_orchestration @capability_journeyman @knowledge_scope_lake
Feature: Validate passage
  Check passage definition for completeness, consistency, reachability, and termination
  
  Background:
    Given Santiago PM MCP is running
    And the knowledge graph is initialized
    And the user has Journeyman capability level

  Scenario: Validate passage with valid inputs (happy path)
    Given the user provides valid input data for validate_passage
    When the validate_passage behavior is invoked
    Then a new Passage node is queried in the knowledge graph
    And the response contains the expected output fields
    And the operation completes successfully

  Scenario: Validate passage with edge case inputs (edge case)
    Given the user provides minimal or optional field data for validate_passage
    When the validate_passage behavior is invoked
    Then the operation handles the edge case gracefully
    And default values are applied where appropriate
    And the response indicates partial success or warnings

  Scenario: Validate passage with missing required fields (error handling)
    Given the user provides incomplete data missing required fields
    When the validate_passage behavior is invoked
    Then an error is returned with message "Missing required field"
    And the knowledge graph remains unchanged
    And the error includes details about which fields are missing
