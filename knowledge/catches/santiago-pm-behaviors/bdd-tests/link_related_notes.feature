@knowledge_capture @capability_journeyman @knowledge_scope_lake @mutates_kg
Feature: Link related notes
  Create semantic relationships between notes (6 types: relatedTo, follows, references, elaborates, contradicts, supports)
  
  Background:
    Given Santiago PM MCP is running
    And the knowledge graph is initialized
    And the user has Journeyman capability level

  Scenario: Link related notes with valid inputs (happy path)
    Given the user provides valid input data for link_related_notes
    When the link_related_notes behavior is invoked
    Then a new Note node is created in the knowledge graph
    And the response contains the expected output fields
    And the operation completes successfully

  Scenario: Link related notes with edge case inputs (edge case)
    Given the user provides minimal or optional field data for link_related_notes
    When the link_related_notes behavior is invoked
    Then the operation handles the edge case gracefully
    And default values are applied where appropriate
    And the response indicates partial success or warnings

  Scenario: Link related notes with missing required fields (error handling)
    Given the user provides incomplete data missing required fields
    When the link_related_notes behavior is invoked
    Then an error is returned with message "Missing required field"
    And the knowledge graph remains unchanged
    And the error includes details about which fields are missing
