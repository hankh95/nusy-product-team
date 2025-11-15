Feature: NuSy PM as Central Knowledge Service

  As a Santiago agent
  I want the NuSy PM to run continuously as a central knowledge service
  So that all project knowledge is always available and queryable

  Background:
    Given the NuSy PM system exists
    And it manages knowledge graphs and artifacts
    And Santiago agents need persistent knowledge access

  Scenario: PM service runs continuously
    Given the PM system is deployed
    When the service starts
    Then it maintains persistent KG storage
    And provides real-time knowledge queries
    And supports concurrent agent access
    And handles knowledge updates automatically

  Scenario: MCP integration for external tools
    Given external tools need project knowledge
    When MCP protocol is enabled
    Then expose KG as MCP resources
    And allow tool registration and discovery
    And support knowledge push notifications
    And maintain security boundaries

  Scenario: Background knowledge processing
    Given new artifacts are created
    When background processing runs
    Then automatically extract ontologies
    And establish semantic relations
    And update knowledge indexes
    And notify subscribed agents

  Scenario: Service health and monitoring
    Given the service is running
    When health checks execute
    Then verify KG integrity
    And check agent connectivity
    And monitor resource usage
    And provide diagnostic endpoints