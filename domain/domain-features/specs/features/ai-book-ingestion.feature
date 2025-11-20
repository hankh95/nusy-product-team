Feature: AI Book Ingestion and Reading
  As the Santiago team
  We want Santiago to legally ingest and read books and clinical textbooks
  So that domain knowledge from high-quality EPUB sources can be used in DGX and NuSy-Core workflows

  Background:
    Given we have identified legal EPUB and clinical book sources
    And we have APIs or retrieval mechanisms for those sources

  # High-level capability
  Scenario: Ingest a clinical EPUB book into the knowledge system
    Given a clinical-grade book is available from NCBI Bookshelf or another licensed source
    When the ingestion pipeline retrieves the EPUB and associated metadata
    Then the content should be parsed into L0/L1/L2/L3 representations (or equivalent)
    And provenance (source, license, retrieval date, edition) should be stored
    And the book's knowledge should be queryable via NuSy-Core / DGX pipelines

  Scenario: Respect legal and licensing constraints when reading books
    Given a potential book source has licensing restrictions
    When we configure a new book ingestion source
    Then the system MUST verify license compatibility and access rights
    And MUST NOT ingest or expose restricted content without appropriate agreements
    And provenance must clearly reflect licensing terms

  Scenario: Expose book knowledge to DGX pipelines
    Given a set of ingested books for a clinical domain
    When the DGX BMJ voyage runs for a topic
    Then the DGX pipelines should be able to:
      | capability                    |
      | look up definitions           |
      | cross-check guideline logic   |
      | enrich frames with textbook context |
    And the additional knowledge usage should be logged and attributable to specific sources

  # Future work: specific EPUB APIs and sources
  # See archived research in _archive/legacy-docs/Epub-books-feature-memory.md
  # for concrete source lists (NCBI Bookshelf, DOAB, Open Textbook Library, etc.)


