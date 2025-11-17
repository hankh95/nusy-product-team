@santiago-pm @contract-test
Feature: Status Query
  Tests for Status Query behavior in santiago-pm

  @happy-path
  Scenario: Successfully status query
    Given the status query service is available
    Given valid input parameters are provided
    When I request to status query
    Then the operation succeeds
    Then a valid response is returned
    Then the result matches expected format

  @edge-case
  Scenario: Status Query with edge cases
    Given the status query service is available
    Given edge case parameters are provided
    When I request to status query with edge data
    Then the operation handles edge cases correctly
    Then appropriate warnings or notifications are given
    Then the system remains stable

  @error-handling
  Scenario: Status Query error handling
    Given the status query service is available
    Given invalid parameters are provided
    When I request to status query with invalid data
    Then the operation fails gracefully
    Then a clear error message is returned
    Then no data corruption occurs
