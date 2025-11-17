@santiago-pm @contract-test
Feature: Log Issue
  Tests for Log Issue behavior in santiago-pm

  @happy-path
  Scenario: Successfully log issue
    Given the log issue service is available
    Given valid input parameters are provided
    When I request to log issue
    Then the operation succeeds
    Then a valid response is returned
    Then the result matches expected format

  @edge-case
  Scenario: Log Issue with edge cases
    Given the log issue service is available
    Given edge case parameters are provided
    When I request to log issue with edge data
    Then the operation handles edge cases correctly
    Then appropriate warnings or notifications are given
    Then the system remains stable

  @error-handling
  Scenario: Log Issue error handling
    Given the log issue service is available
    Given invalid parameters are provided
    When I request to log issue with invalid data
    Then the operation fails gracefully
    Then a clear error message is returned
    Then no data corruption occurs
