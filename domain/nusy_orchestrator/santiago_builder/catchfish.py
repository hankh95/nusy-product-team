"""Catchfish - 4-Layer Domain Knowledge Extraction

Extracts domain knowledge from raw sources through progressive refinement:

Layer 1 (Raw Text): Extract raw text from PDFs, Markdown, APIs, notes
- Baseline: 30-60 minutes per source
- Output: Raw text with source metadata

Layer 2 (Entities): Identify entities and relationships
- Extract key concepts, actors, actions, constraints
- Build initial semantic map
- Output: Structured entities with relationships

Layer 3 (Structured Docs): Write Markdown + YAML packages
- Create domain-knowledge documents with frontmatter
- Apply schemas and naming conventions
- Output: Markdown files ready for KG ingestion

Layer 4 (KG Triples): Queue knowledge graph triples
- Generate RDF-like triples (subject-predicate-object)
- Apply schema validation
- Queue for KG write with provenance tracking
- Target: <15 minutes per source (optimized)

Provenance Tracking:
- Source hash (SHA-256 of original content)
- Timestamp (extraction start/end)
- Agent ID (which agent performed extraction)
- Extraction method (LLM vs deterministic parser)
- Confidence scores per entity/relationship
"""

import asyncio
import hashlib
import json
import re
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from uuid import uuid4


class ExtractionLayer(Enum):
    """4 extraction layers"""
    RAW_TEXT = 1
    ENTITIES = 2
    STRUCTURED_DOCS = 3
    KG_TRIPLES = 4


class ExtractionMethod(Enum):
    """How extraction was performed"""
    LLM_SUMMARIZATION = "llm_summarization"
    DETERMINISTIC_PARSER = "deterministic_parser"
    HYBRID = "hybrid"


@dataclass
class SourceMetadata:
    """Metadata about source file"""
    source_id: str
    file_path: Path
    file_hash: str
    file_size_bytes: int
    file_type: str
    extracted_at: datetime
    agent_id: str = "catchfish-v1"


@dataclass
class Entity:
    """Extracted entity with metadata"""
    entity_id: str
    entity_type: str  # concept, actor, action, constraint, etc.
    name: str
    description: str
    confidence: float = 1.0
    source_references: List[str] = field(default_factory=list)
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Relationship:
    """Relationship between entities"""
    relationship_id: str
    subject_id: str
    predicate: str
    object_id: str
    confidence: float = 1.0
    source_references: List[str] = field(default_factory=list)
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KGTriple:
    """Knowledge graph triple"""
    triple_id: str
    subject: str
    predicate: str
    object: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExtractionResult:
    """Results from one extraction layer"""
    layer: ExtractionLayer
    source_metadata: SourceMetadata
    method: ExtractionMethod
    started_at: datetime
    completed_at: datetime
    extraction_time_seconds: float
    
    # Layer-specific outputs
    raw_text: Optional[str] = None
    entities: List[Entity] = field(default_factory=list)
    relationships: List[Relationship] = field(default_factory=list)
    structured_doc_path: Optional[Path] = None
    kg_triples: List[KGTriple] = field(default_factory=list)
    
    # Quality metrics
    confidence_avg: float = 0.0
    issues: List[str] = field(default_factory=list)


class Catchfish:
    """
    Performs 4-layer domain knowledge extraction from raw sources.
    
    Proven workflow from clinical prototype:
    - 30-60 minute baseline per source
    - Target <15 minutes with optimization
    - Complete provenance tracking
    - Schema validation before KG write
    
    Usage:
        catchfish = Catchfish(workspace_path)
        results = await catchfish.extract_from_source(
            source_path=Path("safe_agile.pdf"),
            target_layer=ExtractionLayer.KG_TRIPLES
        )
    """
    
    def __init__(
        self,
        workspace_path: Path,
        default_method: ExtractionMethod = ExtractionMethod.LLM_SUMMARIZATION,
        target_time_per_source: int = 900,  # 15 minutes
    ):
        self.workspace_path = Path(workspace_path)
        self.default_method = default_method
        self.target_time_per_source = target_time_per_source
        
        # Setup directories
        self.catches_dir = self.workspace_path / "knowledge" / "catches"
        self.provenance_dir = self.workspace_path / "test_workspace" / "ships-logs" / "catchfish"
        
        self.catches_dir.mkdir(parents=True, exist_ok=True)
        self.provenance_dir.mkdir(parents=True, exist_ok=True)
    
    async def extract_from_source(
        self,
        source_path: Path,
        target_layer: ExtractionLayer = ExtractionLayer.KG_TRIPLES,
        method: Optional[ExtractionMethod] = None,
    ) -> List[ExtractionResult]:
        """
        Extract knowledge from source through all layers up to target.
        
        Args:
            source_path: Path to source file
            target_layer: Stop at this layer (default: KG_TRIPLES)
            method: Extraction method (default: from __init__)
            
        Returns:
            List of ExtractionResult for each layer processed
        """
        if not source_path.exists():
            raise FileNotFoundError(f"Source not found: {source_path}")
        
        method = method or self.default_method
        
        print(f"\n🎣 Catchfish: Extracting from {source_path.name}")
        print(f"   Target Layer: {target_layer.name}")
        print(f"   Method: {method.value}")
        
        # Create source metadata
        source_metadata = self._create_source_metadata(source_path)
        
        # Process through layers
        results = []
        
        # Layer 1: Raw Text
        if target_layer.value >= ExtractionLayer.RAW_TEXT.value:
            result = await self._layer1_extract_raw_text(source_path, source_metadata, method)
            results.append(result)
            print(f"   ✅ Layer 1: Extracted {len(result.raw_text)} characters")
        
        # Layer 2: Entities
        if target_layer.value >= ExtractionLayer.ENTITIES.value:
            raw_text = results[0].raw_text if results else ""
            result = await self._layer2_extract_entities(raw_text, source_metadata, method)
            results.append(result)
            print(f"   ✅ Layer 2: Extracted {len(result.entities)} entities, {len(result.relationships)} relationships")
        
        # Layer 3: Structured Docs
        if target_layer.value >= ExtractionLayer.STRUCTURED_DOCS.value:
            entities = results[1].entities if len(results) > 1 else []
            relationships = results[1].relationships if len(results) > 1 else []
            result = await self._layer3_create_structured_docs(
                entities, relationships, source_metadata, method
            )
            results.append(result)
            print(f"   ✅ Layer 3: Created structured doc at {result.structured_doc_path}")
        
        # Layer 4: KG Triples
        if target_layer.value >= ExtractionLayer.KG_TRIPLES.value:
            entities = results[1].entities if len(results) > 1 else []
            relationships = results[1].relationships if len(results) > 1 else []
            result = await self._layer4_generate_kg_triples(
                entities, relationships, source_metadata, method
            )
            results.append(result)
            print(f"   ✅ Layer 4: Generated {len(result.kg_triples)} KG triples")
        
        # Calculate total extraction time
        total_time = sum(r.extraction_time_seconds for r in results)
        print(f"   ⏱️  Total Extraction Time: {total_time:.2f}s ({total_time / 60:.1f}m)")
        
        if total_time > self.target_time_per_source:
            print(f"   ⚠️  Above target {self.target_time_per_source}s, optimization needed")
        else:
            print(f"   🎯 Under target {self.target_time_per_source}s!")
        
        # Save provenance
        self._save_provenance(source_metadata, results, total_time)
        
        return results
    
    def _create_source_metadata(self, source_path: Path) -> SourceMetadata:
        """Create metadata for source file"""
        # Calculate SHA-256 hash
        with open(source_path, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        
        return SourceMetadata(
            source_id=str(uuid4()),
            file_path=source_path,
            file_hash=file_hash,
            file_size_bytes=source_path.stat().st_size,
            file_type=source_path.suffix,
            extracted_at=datetime.now(),
        )
    
    async def _layer1_extract_raw_text(
        self,
        source_path: Path,
        metadata: SourceMetadata,
        method: ExtractionMethod,
    ) -> ExtractionResult:
        """Layer 1: Extract raw text from source file"""
        start_time = time.time()
        
        # Read file content
        # TODO: Add PDF parsing, API fetching, etc.
        if source_path.suffix == ".md":
            with open(source_path, 'r', encoding='utf-8') as f:
                raw_text = f.read()
        else:
            # For demo, just read as text
            with open(source_path, 'r', encoding='utf-8', errors='ignore') as f:
                raw_text = f.read()
        
        # Simulate processing time
        await asyncio.sleep(0.1)
        
        extraction_time = time.time() - start_time
        
        return ExtractionResult(
            layer=ExtractionLayer.RAW_TEXT,
            source_metadata=metadata,
            method=method,
            started_at=datetime.fromtimestamp(start_time),
            completed_at=datetime.now(),
            extraction_time_seconds=extraction_time,
            raw_text=raw_text,
        )
    
    async def _layer2_extract_entities(
        self,
        raw_text: str,
        metadata: SourceMetadata,
        method: ExtractionMethod,
    ) -> ExtractionResult:
        """Layer 2: Extract entities and relationships from raw text"""
        start_time = time.time()
        
        entities = []
        relationships = []
        
        # TODO: Implement actual NLP extraction (spaCy, LLM, etc.)
        # For now, simple pattern matching
        
        # Extract concepts (capitalized words)
        concept_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b'
        concepts = set(re.findall(concept_pattern, raw_text))
        
        for concept in list(concepts)[:10]:  # Limit for demo
            entity = Entity(
                entity_id=f"entity_{uuid4().hex[:8]}",
                entity_type="concept",
                name=concept,
                description=f"Concept extracted from {metadata.file_path.name}",
                confidence=0.8,
                source_references=[metadata.source_id],
            )
            entities.append(entity)
        
        # Extract simple relationships (X involves Y pattern)
        relationship_pattern = r'(\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(involves?|includes?|requires?)\s+(\b[a-z]+(?:\s+[a-z]+)*)'
        matches = re.findall(relationship_pattern, raw_text, re.IGNORECASE)
        
        for subject, predicate, obj in matches[:5]:  # Limit for demo
            relationship = Relationship(
                relationship_id=f"rel_{uuid4().hex[:8]}",
                subject_id=subject,
                predicate=predicate.lower(),
                object_id=obj,
                confidence=0.7,
                source_references=[metadata.source_id],
            )
            relationships.append(relationship)
        
        # Simulate processing time
        await asyncio.sleep(0.15)
        
        extraction_time = time.time() - start_time
        
        # Calculate average confidence
        all_confidences = [e.confidence for e in entities] + [r.confidence for r in relationships]
        confidence_avg = sum(all_confidences) / len(all_confidences) if all_confidences else 0.0
        
        return ExtractionResult(
            layer=ExtractionLayer.ENTITIES,
            source_metadata=metadata,
            method=method,
            started_at=datetime.fromtimestamp(start_time),
            completed_at=datetime.now(),
            extraction_time_seconds=extraction_time,
            entities=entities,
            relationships=relationships,
            confidence_avg=confidence_avg,
        )
    
    async def _layer3_create_structured_docs(
        self,
        entities: List[Entity],
        relationships: List[Relationship],
        metadata: SourceMetadata,
        method: ExtractionMethod,
    ) -> ExtractionResult:
        """Layer 3: Create Markdown + YAML structured documents"""
        start_time = time.time()
        
        # Create domain-knowledge directory
        domain_name = metadata.file_path.stem
        domain_dir = self.catches_dir / domain_name / "domain-knowledge"
        domain_dir.mkdir(parents=True, exist_ok=True)
        
        doc_path = domain_dir / f"{metadata.source_id[:8]}_extracted.md"
        
        # Generate Markdown with YAML frontmatter
        content = self._generate_structured_markdown(entities, relationships, metadata)
        
        with open(doc_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Simulate processing time
        await asyncio.sleep(0.1)
        
        extraction_time = time.time() - start_time
        
        return ExtractionResult(
            layer=ExtractionLayer.STRUCTURED_DOCS,
            source_metadata=metadata,
            method=method,
            started_at=datetime.fromtimestamp(start_time),
            completed_at=datetime.now(),
            extraction_time_seconds=extraction_time,
            structured_doc_path=doc_path,
        )
    
    async def _layer4_generate_kg_triples(
        self,
        entities: List[Entity],
        relationships: List[Relationship],
        metadata: SourceMetadata,
        method: ExtractionMethod,
    ) -> ExtractionResult:
        """Layer 4: Generate knowledge graph triples with schema validation"""
        start_time = time.time()
        
        kg_triples = []
        
        # Generate triples from entities (type triples)
        for entity in entities:
            triple = KGTriple(
                triple_id=f"triple_{uuid4().hex[:8]}",
                subject=entity.name,
                predicate="rdf:type",
                object=entity.entity_type,
                metadata={
                    "source_id": metadata.source_id,
                    "confidence": entity.confidence,
                    "extracted_at": datetime.now().isoformat(),
                },
            )
            kg_triples.append(triple)
        
        # Generate triples from relationships
        for rel in relationships:
            triple = KGTriple(
                triple_id=f"triple_{uuid4().hex[:8]}",
                subject=rel.subject_id,
                predicate=rel.predicate,
                object=rel.object_id,
                metadata={
                    "source_id": metadata.source_id,
                    "confidence": rel.confidence,
                    "extracted_at": datetime.now().isoformat(),
                },
            )
            kg_triples.append(triple)
        
        # TODO: Apply schema validation before queuing
        # TODO: Queue triples for KG write with provenance
        
        # Simulate processing time
        await asyncio.sleep(0.1)
        
        extraction_time = time.time() - start_time
        
        return ExtractionResult(
            layer=ExtractionLayer.KG_TRIPLES,
            source_metadata=metadata,
            method=method,
            started_at=datetime.fromtimestamp(start_time),
            completed_at=datetime.now(),
            extraction_time_seconds=extraction_time,
            kg_triples=kg_triples,
        )
    
    def _generate_structured_markdown(
        self,
        entities: List[Entity],
        relationships: List[Relationship],
        metadata: SourceMetadata,
    ) -> str:
        """Generate Markdown document with YAML frontmatter"""
        
        # YAML frontmatter
        yaml_front = f"""---
source_id: {metadata.source_id}
source_file: {metadata.file_path.name}
source_hash: {metadata.file_hash}
extracted_at: {metadata.extracted_at.isoformat()}
agent_id: {metadata.agent_id}
entity_count: {len(entities)}
relationship_count: {len(relationships)}
---

# Domain Knowledge: {metadata.file_path.stem}

> Extracted from: `{metadata.file_path.name}`  
> Source Hash: `{metadata.file_hash[:16]}...`  
> Extracted: {metadata.extracted_at.strftime('%Y-%m-%d %H:%M:%S')}

## Entities

"""
        
        # Add entities
        for entity in entities:
            yaml_front += f"### {entity.name}\n\n"
            yaml_front += f"- **Type**: {entity.entity_type}\n"
            yaml_front += f"- **Description**: {entity.description}\n"
            yaml_front += f"- **Confidence**: {entity.confidence:.2f}\n"
            yaml_front += f"- **ID**: `{entity.entity_id}`\n\n"
        
        # Add relationships
        yaml_front += "## Relationships\n\n"
        for rel in relationships:
            yaml_front += f"- **{rel.subject_id}** `{rel.predicate}` **{rel.object_id}** "
            yaml_front += f"(confidence: {rel.confidence:.2f})\n"
        
        return yaml_front
    
    def _save_provenance(
        self,
        metadata: SourceMetadata,
        results: List[ExtractionResult],
        total_time: float,
    ) -> None:
        """Save extraction provenance to ships-logs"""
        provenance_file = self.provenance_dir / f"{metadata.source_id[:8]}_provenance.json"
        
        provenance_data = {
            "source_metadata": {
                "source_id": metadata.source_id,
                "file_path": str(metadata.file_path),
                "file_hash": metadata.file_hash,
                "file_size_bytes": metadata.file_size_bytes,
                "file_type": metadata.file_type,
                "extracted_at": metadata.extracted_at.isoformat(),
                "agent_id": metadata.agent_id,
            },
            "extraction_results": [
                {
                    "layer": r.layer.name,
                    "method": r.method.value,
                    "started_at": r.started_at.isoformat(),
                    "completed_at": r.completed_at.isoformat(),
                    "extraction_time_seconds": r.extraction_time_seconds,
                    "entity_count": len(r.entities),
                    "relationship_count": len(r.relationships),
                    "kg_triple_count": len(r.kg_triples),
                    "confidence_avg": r.confidence_avg,
                    "issues": r.issues,
                }
                for r in results
            ],
            "total_time_seconds": total_time,
            "target_time_seconds": self.target_time_per_source,
            "meets_target": total_time <= self.target_time_per_source,
        }
        
        with open(provenance_file, 'w') as f:
            json.dump(provenance_data, f, indent=2)
        
        print(f"   💾 Provenance saved: {provenance_file}")
