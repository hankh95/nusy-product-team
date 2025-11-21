"""
Catchfish Demo - 4-Layer Knowledge Extraction

Demonstrates Catchfish extracting domain knowledge through 4 layers:
1. Raw Text - Extract content from source files
2. Entities - Identify concepts, actors, relationships
3. Structured Docs - Create Markdown + YAML packages
4. KG Triples - Generate knowledge graph triples

Shows:
- Progressive extraction through all layers
- Provenance tracking with source hashes
- Time tracking against 15-minute target
- Entity and relationship extraction
- Structured document generation
"""

import asyncio
from pathlib import Path

from domain.nusy_orchestrator.santiago_builder.catchfish import (
    Catchfish,
    ExtractionLayer,
    ExtractionMethod,
)


async def main():
    """Run Catchfish demonstration"""
    
    print("="*80)
    print("         Catchfish 4-Layer Knowledge Extraction Demo")
    print("="*80)
    
    # Initialize Catchfish
    workspace_path = Path(__file__).parent
    catchfish = Catchfish(
        workspace_path=workspace_path,
        default_method=ExtractionMethod.LLM_SUMMARIZATION,
        target_time_per_source=900,  # 15 minutes
    )
    
    # Use existing demo sources or create them
    sources_dir = workspace_path / "test_workspace" / "demo_sources"
    sources_dir.mkdir(parents=True, exist_ok=True)
    
    source_path = sources_dir / "agile_practices.md"
    
    # Create sample source if it doesn't exist
    if not source_path.exists():
        source_path.write_text("""# Agile Development Practices

## SAFe Framework

SAFe (Scaled Agile Framework) involves Program Increment Planning and Strategic Themes.
The Product Manager requires backlog prioritization and value stream mapping.

## Extreme Programming

XP (Extreme Programming) includes Test-First Development and Continuous Integration.
User Stories should follow INVEST criteria and maintain Small Batch Sizes.

## Key Principles

1. Customer Collaboration - Working with stakeholders requires frequent feedback
2. Responding to Change - Adaptation involves continuous planning
3. Working Software - Delivery includes automated testing
4. Sustainable Pace - Team Velocity requires realistic estimation
""")
    
    print(f"\n📚 Extracting Knowledge From:")
    print(f"   Source: {source_path.name}")
    print(f"   Target: All 4 Layers")
    print(f"   Method: LLM Summarization\n")
    
    try:
        # Extract through all 4 layers
        results = await catchfish.extract_from_source(
            source_path=source_path,
            target_layer=ExtractionLayer.KG_TRIPLES,
        )
        
        print("\n" + "="*80)
        print("                    Extraction Results")
        print("="*80)
        
        # Layer 1: Raw Text
        if len(results) > 0:
            layer1 = results[0]
            print(f"\n📄 Layer 1: Raw Text Extraction")
            print(f"   Characters: {len(layer1.raw_text)}")
            print(f"   Time: {layer1.extraction_time_seconds:.3f}s")
            print(f"   Preview: {layer1.raw_text[:100]}...")
        
        # Layer 2: Entities
        if len(results) > 1:
            layer2 = results[1]
            print(f"\n🏷️  Layer 2: Entity Extraction")
            print(f"   Entities: {len(layer2.entities)}")
            print(f"   Relationships: {len(layer2.relationships)}")
            print(f"   Avg Confidence: {layer2.confidence_avg:.2f}")
            print(f"   Time: {layer2.extraction_time_seconds:.3f}s")
            
            if layer2.entities:
                print(f"\n   Sample Entities:")
                for entity in layer2.entities[:5]:
                    print(f"      • {entity.name} ({entity.entity_type}, confidence: {entity.confidence:.2f})")
            
            if layer2.relationships:
                print(f"\n   Sample Relationships:")
                for rel in layer2.relationships[:3]:
                    print(f"      • {rel.subject_id} → {rel.predicate} → {rel.object_id}")
        
        # Layer 3: Structured Docs
        if len(results) > 2:
            layer3 = results[2]
            print(f"\n📝 Layer 3: Structured Documentation")
            print(f"   Document: {layer3.structured_doc_path}")
            print(f"   Time: {layer3.extraction_time_seconds:.3f}s")
            
            if layer3.structured_doc_path and layer3.structured_doc_path.exists():
                with open(layer3.structured_doc_path, 'r') as f:
                    content = f.read()
                print(f"   Content Length: {len(content)} characters")
                print(f"\n   Frontmatter Preview:")
                lines = content.split('\n')[:10]
                for line in lines:
                    print(f"      {line}")
        
        # Layer 4: KG Triples
        if len(results) > 3:
            layer4 = results[3]
            print(f"\n🔗 Layer 4: Knowledge Graph Triples")
            print(f"   Triples Generated: {len(layer4.kg_triples)}")
            print(f"   Time: {layer4.extraction_time_seconds:.3f}s")
            
            if layer4.kg_triples:
                print(f"\n   Sample Triples:")
                for triple in layer4.kg_triples[:5]:
                    print(f"      • ({triple.subject}) --[{triple.predicate}]--> ({triple.object})")
        
        # Overall metrics
        total_time = sum(r.extraction_time_seconds for r in results)
        print(f"\n📊 Overall Metrics:")
        print(f"   Total Extraction Time: {total_time:.2f}s ({total_time / 60:.1f}m)")
        print(f"   Target Time: {catchfish.target_time_per_source}s (15m)")
        print(f"   Under Target: {total_time <= catchfish.target_time_per_source} ✅" if total_time <= catchfish.target_time_per_source else f"   Over Target: ⚠️")
        print(f"   Layers Completed: {len(results)}/4")
        
        # Provenance
        provenance_dir = workspace_path / "test_workspace" / "ships-logs" / "catchfish"
        provenance_files = list(provenance_dir.glob("*_provenance.json"))
        if provenance_files:
            print(f"\n💾 Provenance:")
            print(f"   Saved to: {provenance_files[-1]}")
        
        print("\n" + "="*80)
        print("                🎉 Extraction Complete! 🎉")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ Extraction failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
