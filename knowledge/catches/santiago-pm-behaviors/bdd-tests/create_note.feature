@knowledge_capture @capability_journeyman @knowledge_scope_lake @mutates_kg
Feature: Create note
  Capture insight, learning, or decision in captain's journal with metadata
  
  Background:
    Given Santiago PM MCP is running
    And the knowledge graph is initialized
    And the user has Journeyman capability level

  Scenario: Create note with valid inputs (happy path)
    Given the user provides valid input data for create_note
    When the create_note behavior is invoked
    Then a new Note node is created in the knowledge graph
    And the response contains the expected output fields
    And the operation completes successfully

  Scenario: Create note with edge case inputs (edge case)
    Given the user provides minimal or optional field data for create_note
    When the create_note behavior is invoked
    Then the operation handles the edge case gracefully
    And default values are applied where appropriate
    And the response indicates partial success or warnings

  Scenario: Create note with missing required fields (error handling)
    Given the user provides incomplete data missing required fields
    When the create_note behavior is invoked
    Then an error is returned with message "Missing required field"
    And the knowledge graph remains unchanged
    And the error includes details about which fields are missing
