@santiago-pm @contract-test
Feature: Link Issue To Feature
  Tests for Link Issue To Feature behavior in santiago-pm

  @happy-path
  Scenario: Successfully link issue to feature
    Given the link issue to feature service is available
    Given valid input parameters are provided
    When I request to link issue to feature
    Then the operation succeeds
    Then a valid response is returned
    Then the result matches expected format

  @edge-case
  Scenario: Link Issue To Feature with edge cases
    Given the link issue to feature service is available
    Given edge case parameters are provided
    When I request to link issue to feature with edge data
    Then the operation handles edge cases correctly
    Then appropriate warnings or notifications are given
    Then the system remains stable

  @error-handling
  Scenario: Link Issue To Feature error handling
    Given the link issue to feature service is available
    Given invalid parameters are provided
    When I request to link issue to feature with invalid data
    Then the operation fails gracefully
    Then a clear error message is returned
    Then no data corruption occurs
