@issue_tracking @capability_journeyman @knowledge_scope_lake @mutates_kg
Feature: Link issue to feature
  Create bidirectional relationship between issue and feature
  
  Background:
    Given Santiago PM MCP is running
    And the knowledge graph is initialized
    And the user has Journeyman capability level

  Scenario: Link issue to feature with valid inputs (happy path)
    Given the user provides valid input data for link_issue_to_feature
    When the link_issue_to_feature behavior is invoked
    Then a new Issue node is created in the knowledge graph
    And the response contains the expected output fields
    And the operation completes successfully

  Scenario: Link issue to feature with edge case inputs (edge case)
    Given the user provides minimal or optional field data for link_issue_to_feature
    When the link_issue_to_feature behavior is invoked
    Then the operation handles the edge case gracefully
    And default values are applied where appropriate
    And the response indicates partial success or warnings

  Scenario: Link issue to feature with missing required fields (error handling)
    Given the user provides incomplete data missing required fields
    When the link_issue_to_feature behavior is invoked
    Then an error is returned with message "Missing required field"
    And the knowledge graph remains unchanged
    And the error includes details about which fields are missing
