Feature: Knowledge Ingestion and Semantic Wiki

  As a Santiago domain expert
  I want a semantic wiki interface for knowledge ingestion
  So that domain knowledge can be captured and processed intelligently

  Background:
    Given the NuSy PM system has KG capabilities
    And Santiago can process various knowledge formats
    And domain standards need to be captured

  Scenario: AI-powered knowledge requests
    Given a knowledge gap is identified
    When AI learning request is made
    Then Santiago researches the subject
    And extracts key concepts and relations
    And adds to KG with proper ontologies
    And creates wiki entries automatically

  Scenario: Document ingestion (PDF/Markdown)
    Given a document contains domain knowledge
    When document is ingested
    Then extract text and structure
    And identify ontologies and standards
    And establish semantic relations
    And create searchable wiki entries

  Scenario: Domain standards discovery
    Given a domain has specific standards (e.g., FHIR)
    When standards are referenced
    Then locate and ingest standard specifications
    And map to existing KG concepts
    And create validation rules
    And update agent knowledge bases

  Scenario: Semantic wiki interface
    Given users/agents need to access knowledge
    When wiki interface is used
    Then provide natural language search
    And show concept relationships
    And allow knowledge linking
    And support collaborative editing