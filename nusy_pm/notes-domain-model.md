# NuSy PM Notes Domain Model

## Overview

The Notes Domain Model defines the semantic structure for notes within the NuSy PM knowledge graph. It provides a formal ontology for representing notes, their relationships, and metadata to enable intelligent linking, querying, and knowledge discovery across the project.

## Core Concepts

### Note

Represents a single note or knowledge artifact in the system.

**Properties:**

- `id`: Unique identifier (UUID)
- `title`: Human-readable title
- `summary`: Brief description or abstract
- `content`: Full note content (optional, may reference external files)
- `contributor`: Agent who created/contributed to the note
- `created_at`: Creation timestamp
- `updated_at`: Last modification timestamp
- `tags`: Array of topic/category tags
- `source_links`: References to source materials or files

### Contributor

Represents an agent (person or AI) who contributes to notes.

**Properties:**

- `name`: Display name
- `type`: "human" or "ai"
- `role`: Role in the project (e.g., "architect", "developer")

### Tag

Represents a topic or category for organizing notes.

**Properties:**

- `name`: Tag name
- `description`: Optional description
- `category`: Grouping category for tags

## Relationships Between Notes

### Related Notes Feature

The core innovation of this domain model is the **Related Notes** feature, which enables semantic linking between notes to create a knowledge network.

#### Relationship Types

1. **relatedTo** - General relationship indicating notes are thematically connected
   - **Inverse**: `relatedTo`
   - **Use case**: Notes on similar topics, complementary information

2. **follows** - Temporal sequence relationship
   - **Inverse**: `precededBy`
   - **Use case**: Chronological progression of ideas, follow-up notes

3. **references** - Citation or reference relationship
   - **Inverse**: `referencedBy`
   - **Use case**: One note cites or builds upon another

4. **contradicts** - Conflicting information relationship
   - **Inverse**: `contradictedBy`
   - **Use case**: Notes with opposing viewpoints or findings

5. **supports** - Supporting evidence relationship
   - **Inverse**: `supportedBy`
   - **Use case**: Notes providing evidence for claims in other notes

6. **elaborates** - Detailed explanation relationship
   - **Inverse**: `elaboratedBy`
   - **Use case**: High-level notes with detailed elaborations

#### Relationship Metadata

Each relationship can include:

- `strength`: Confidence level (0.0-1.0)
- `context`: Description of how the notes are related
- `created_at`: When the relationship was established
- `created_by`: Agent who created the relationship

## Knowledge Graph Integration

### Semantic Triples

Notes and relationships are represented as RDF triples in the knowledge graph:

```turtle
# Note triples
<note:uuid-123> rdf:type notes:Note
<note:uuid-123> notes:title "Project Architecture Decision"
<note:uuid-123> notes:summary "Decision on microservices architecture"
<note:uuid-123> notes:contributor <agent:human-architect>
<note:uuid-123> notes:created_at "2025-11-15T10:00:00Z"

# Relationship triples
<note:uuid-123> notes:relatedTo <note:uuid-456>
<note:uuid-123> notes:supports <note:uuid-789>
_:rel1 rdf:type notes:Relationship
_:rel1 notes:from <note:uuid-123>
_:rel1 notes:to <note:uuid-456>
_:rel1 notes:relationshipType notes:relatedTo
_:rel1 notes:strength "0.8"
_:rel1 notes:context "Both discuss system architecture"
```

### SPARQL Queries

#### Find Related Notes

```sparql
SELECT ?related_note ?title ?strength
WHERE {
  <note:uuid-123> notes:relatedTo ?related_note .
  ?related_note notes:title ?title .
  OPTIONAL { ?related_note notes:strength ?strength }
}
```

#### Find Notes by Topic Network

```sparql
SELECT ?note ?title ?depth
WHERE {
  <note:uuid-123> notes:relatedTo+ ?note .
  ?note notes:title ?title .
  # Calculate relationship depth
}
```

#### Find Contradictory Information

```sparql
SELECT ?note1 ?note2 ?context
WHERE {
  ?note1 notes:contradicts ?note2 .
  ?rel notes:from ?note1 ;
       notes:to ?note2 ;
       notes:context ?context .
}
```

## Implementation

### Data Structure

The notes manifest (`notes_manifest.json`) stores notes and relationships:

```json
{
  "notes": [
    {
      "id": "uuid-123",
      "title": "Architecture Decision",
      "summary": "Microservices adoption",
      "contributor": "architect-agent",
      "created_at": "2025-11-15T10:00:00Z",
      "tags": ["architecture", "microservices"],
      "source_links": ["docs/architecture.md"]
    }
  ],
  "links": [
    {
      "id": "rel-uuid-456",
      "from": "uuid-123",
      "to": "uuid-789",
      "type": "relatedTo",
      "strength": 0.8,
      "context": "Both address system scalability",
      "created_at": "2025-11-15T10:30:00Z",
      "created_by": "architect-agent"
    }
  ]
}
```

### CLI Integration

The notes system integrates with the existing CLI tools:

```bash
# Query related notes
python -m nusy_pm status_query.py --related-to uuid-123

# Add relationship
python -m nusy_pm status_query.py --link-notes uuid-123 uuid-789 --type relatedTo --context "Architecture discussion"

# Find contradictions
python -m nusy_pm status_query.py --find-contradictions
```

## Best Practices

### Relationship Creation

1. **Explicit Context**: Always provide context when creating relationships
2. **Strength Rating**: Use strength values to indicate relationship confidence
3. **Bidirectional Awareness**: Consider both directions of relationships
4. **Temporal Tracking**: Record when relationships are created/updated

### Query Patterns

1. **Transitive Queries**: Use property paths for network traversal
2. **Filtered Results**: Apply strength thresholds for relevance
3. **Context Preservation**: Include relationship context in results
4. **Graph Visualization**: Support visual exploration of note networks

### Maintenance

1. **Regular Review**: Periodically validate relationship accuracy
2. **Strength Updates**: Adjust relationship strengths based on usage
3. **Dead Link Removal**: Clean up relationships to deleted notes
4. **Metadata Enrichment**: Add additional relationship properties as needed

## Integration with Status System

Notes integrate with the universal status system:

```yaml
---
id: "uuid-123"
title: "Architecture Decision"
status: "approved"
assignee: "architect-agent"
related_notes:
  - id: "uuid-456"
    type: "supports"
    strength: 0.9
  - id: "uuid-789"
    type: "relatedTo"
    strength: 0.7
---
```

## Future Extensions

### Advanced Relationship Types

- **Temporal**: `happenedBefore`, `caused`
- **Semantic**: `isA`, `partOf`, `instanceOf`
- **Collaborative**: `agreesWith`, `disagreesWith`, `extends`

### Machine Learning Integration

- **Automatic Relationship Discovery**: ML models to suggest relationships
- **Strength Prediction**: Algorithms to predict relationship strengths
- **Network Analysis**: Graph algorithms for knowledge discovery

### Multi-Modal Notes

- **Code References**: Links to specific code locations
- **Data Dependencies**: Connections to datasets and models
- **External Resources**: Links to web resources, papers, etc.

---

*This domain model enables the NuSy PM system to maintain a rich, interconnected knowledge graph of notes that supports intelligent discovery, validation, and knowledge synthesis.*
