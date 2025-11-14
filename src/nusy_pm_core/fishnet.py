"""FishNet Module: Generate BDD scenarios for note behaviors."""

from typing import List, Dict


class FishNetGenerator:
    """Generates BDD scenarios for note system behaviors."""

    def generate_scenarios(self, kg_graph) -> List[str]:
        """Generate BDD scenarios based on KG content."""
        scenarios = []

        # Basic note scenarios
        scenarios.extend(self._generate_basic_note_scenarios())

        # Query scenarios
        scenarios.extend(self._generate_query_scenarios())

        # KG scenarios
        scenarios.extend(self._generate_kg_scenarios())

        return scenarios

    def _generate_basic_note_scenarios(self) -> List[str]:
        """Generate basic note creation and management scenarios."""
        return [
            """
Feature: Note Creation
  As a PM agent
  I want to create notes
  So that I can capture project knowledge

  Scenario: Create a new note
    Given the notes system is initialized
    When I create a note with title "Test Note" and contributor "Agent"
    Then the note should be stored with correct metadata
    And the note should be retrievable by ID
            """,
            """
Feature: Note Linking
  As a PM agent
  I want to link notes to KG nodes
  So that knowledge is connected

  Scenario: Link note to KG node
    Given a note exists
    When I link it to a KG node with rationale
    Then the link should be stored
    And the link should be retrievable
            """
        ]

    def _generate_query_scenarios(self) -> List[str]:
        """Generate query-related scenarios."""
        return [
            """
Feature: Note Queries
  As a PM agent
  I want to query notes
  So that I can find relevant information

  Scenario: Query notes by contributor
    Given multiple notes exist from different contributors
    When I query notes by contributor "Alice"
    Then only Alice's notes should be returned
            """,
            """
Feature: Neurosymbolic Queries
  As a PM agent
  I want to query the KG neurosymbolically
  So that I can get evidence-based answers

  Scenario: Ask about note content
    Given notes exist in the KG
    When I ask "What notes are about Santiago?"
    Then relevant entities and triples should be returned
            """
        ]

    def _generate_kg_scenarios(self) -> List[str]:
        """Generate KG-related scenarios."""
        return [
            """
Feature: Knowledge Graph Storage
  As a PM agent
  I want notes stored in KG
  So that they can be queried relationally

  Scenario: Note storage in KG
    Given a note is created
    Then it should appear in the KG with correct triples
    And relationships should be established
            """
        ]