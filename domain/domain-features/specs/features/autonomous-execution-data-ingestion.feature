Feature: Autonomous Execution Data Ingestion
  As a Santiago autonomous synthesis agent
  I want to ingest chat history, decisions, and execution logs
  So that I can learn from past autonomous operations and improve future performance

  Background:
    Given Santiago has access to data/chat_history.json
    And Santiago has access to data/decisions.json
    And Santiago has access to logs/autonomous_runner.log
    And the knowledge graph is initialized

  @chat_history
  Scenario: Ingest chat history into knowledge graph
    When Santiago processes the chat history file
    Then each conversation entry should be stored as a KG triple
    And conversation metadata (timestamp, participants, topics) should be captured
    And relationships between related conversations should be established
    And the ingestion should be logged in the autonomous runner logs

  @decisions
  Scenario: Ingest decision data into knowledge graph
    When Santiago processes the decisions file
    Then each decision should be stored with context and outcomes
    And decision rationale should be linked to KG concepts
    And decision patterns should be identified for future learning
    And ethical considerations should be flagged for Quartermaster review

  @execution_logs
  Scenario: Ingest execution logs into knowledge graph
    When Santiago processes the autonomous runner logs
    Then execution steps should be stored as temporal sequences
    And error patterns should be identified and categorized
    And performance metrics should be extracted and stored
    And learning opportunities should be flagged for future improvements

  @integration
  Scenario: Integrate all autonomous data sources
    Given all data sources have been ingested
    When Santiago analyzes the integrated data
    Then cross-references between chat, decisions, and logs should be established
    And performance insights should be generated
    And recommendations for system improvements should be produced
    And the knowledge graph should reflect the complete autonomous execution history
