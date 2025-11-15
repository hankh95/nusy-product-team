Feature: Project Scaffold Generation
  As a new user
  I want to generate a complete project scaffold
  So that I can start using NuSy immediately

  Background:
    Given NuSy is installed
    And the scaffold generator is available

  Scenario: Generate basic NuSy project scaffold
    When I run the scaffold command with project name "my-nusy-project"
    Then a complete project structure should be created
    And all necessary configuration files should be generated
    And initial development plan should be created
    And knowledge graph should be initialized
    And web interfaces should be ready to run

  Scenario: Scaffold includes domain services
    Given a project scaffold is generated
    Then development plans service should be configured
    And issues service should be configured
    And notes service should be available
    And all services should be integrated with the knowledge graph

  Scenario: Scaffold provides working local server
    Given a scaffolded project exists
    When I start the local server
    Then all web interfaces should be accessible
    And API endpoints should be available
    And the knowledge graph should be queryable
    And development can begin immediately

  Scenario: Scaffold includes documentation and examples
    Given a scaffolded project exists
    Then README files should explain how to use each service
    And example issues and plans should be created
    And API documentation should be available
    And getting started guide should be provided