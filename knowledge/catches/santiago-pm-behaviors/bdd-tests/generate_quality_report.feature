@quality_assurance @capability_journeyman @knowledge_scope_sea @mutates_kg
Feature: Generate quality report
  Aggregate quality metrics across artifacts with trend analysis, recommendations
  
  Background:
    Given Santiago PM MCP is running
    And the knowledge graph is initialized
    And the user has Journeyman capability level

  Scenario: Generate quality report with valid inputs (happy path)
    Given the user provides valid input data for generate_quality_report
    When the generate_quality_report behavior is invoked
    Then a new QualityAssessment node is created in the knowledge graph
    And the response contains the expected output fields
    And the operation completes successfully

  Scenario: Generate quality report with edge case inputs (edge case)
    Given the user provides minimal or optional field data for generate_quality_report
    When the generate_quality_report behavior is invoked
    Then the operation handles the edge case gracefully
    And default values are applied where appropriate
    And the response indicates partial success or warnings

  Scenario: Generate quality report with missing required fields (error handling)
    Given the user provides incomplete data missing required fields
    When the generate_quality_report behavior is invoked
    Then an error is returned with message "Missing required field"
    And the knowledge graph remains unchanged
    And the error includes details about which fields are missing
