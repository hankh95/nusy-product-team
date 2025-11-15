"""
Knowledge Graph for PM Domain

This module provides RDF-based knowledge graph implementation for the PM domain
using RDFLib for semantic relationships and reasoning.
"""

import logging
from typing import List, Dict, Optional, Set
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL
from datetime import datetime

from .pm_domain_model import PMDomainOntology, PMConcept, PMMethodology

logger = logging.getLogger(__name__)

# Define PM namespace
PM = Namespace("http://santiago.pm/ontology#")
BAHAI = Namespace("http://santiago.pm/ethics#")


class PMKnowledgeGraph:
    """Knowledge graph for PM domain concepts and relationships."""
    
    def __init__(self):
        self.graph = Graph()
        self._bind_namespaces()
        self._initialize_schema()
    
    def _bind_namespaces(self):
        """Bind standard and custom namespaces."""
        self.graph.bind("pm", PM)
        self.graph.bind("bahai", BAHAI)
        self.graph.bind("rdf", RDF)
        self.graph.bind("rdfs", RDFS)
        self.graph.bind("owl", OWL)
    
    def _initialize_schema(self):
        """Initialize the knowledge graph schema."""
        # Define top-level classes
        self.graph.add((PM.Concept, RDF.type, OWL.Class))
        self.graph.add((PM.Methodology, RDF.type, OWL.Class))
        self.graph.add((PM.Practice, RDF.type, OWL.Class))
        self.graph.add((PM.Ceremony, RDF.type, OWL.Class))
        self.graph.add((PM.Artifact, RDF.type, OWL.Class))
        self.graph.add((PM.Role, RDF.type, OWL.Class))
        
        # Define properties
        self.graph.add((PM.relatedTo, RDF.type, OWL.ObjectProperty))
        self.graph.add((PM.partOf, RDF.type, OWL.ObjectProperty))
        self.graph.add((PM.usedIn, RDF.type, OWL.ObjectProperty))
        self.graph.add((PM.requires, RDF.type, OWL.ObjectProperty))
        self.graph.add((PM.supports, RDF.type, OWL.ObjectProperty))
        
        # Ethical properties
        self.graph.add((BAHAI.alignsWith, RDF.type, OWL.ObjectProperty))
        self.graph.add((BAHAI.promotes, RDF.type, OWL.ObjectProperty))
        
        logger.info("PM knowledge graph schema initialized")
    
    def add_concept(self, concept: PMConcept) -> URIRef:
        """Add a PM concept to the knowledge graph."""
        concept_uri = PM[concept.id]
        
        # Add type and basic properties
        self.graph.add((concept_uri, RDF.type, PM.Concept))
        self.graph.add((concept_uri, RDFS.label, Literal(concept.name)))
        self.graph.add((concept_uri, RDFS.comment, Literal(concept.description)))
        self.graph.add((concept_uri, PM.methodology, Literal(concept.methodology.value)))
        
        if concept.source:
            self.graph.add((concept_uri, PM.source, Literal(concept.source)))
        
        # Add relationships
        for related_id in concept.related_concepts:
            related_uri = PM[related_id]
            self.graph.add((concept_uri, PM.relatedTo, related_uri))
        
        logger.debug(f"Added concept: {concept.name}")
        return concept_uri
    
    def add_ontology(self, ontology: PMDomainOntology):
        """Add an entire ontology to the knowledge graph."""
        for concept in ontology.concepts.values():
            self.add_concept(concept)
        
        logger.info(f"Added {len(ontology.concepts)} concepts to knowledge graph")
    
    def query_related_concepts(self, concept_id: str, depth: int = 1) -> List[str]:
        """Query concepts related to a given concept up to a certain depth."""
        concept_uri = PM[concept_id]
        related = set()
        
        # Direct relationships
        for s, p, o in self.graph.triples((concept_uri, PM.relatedTo, None)):
            related.add(str(o).split('#')[-1])
        
        # Inverse relationships
        for s, p, o in self.graph.triples((None, PM.relatedTo, concept_uri)):
            related.add(str(s).split('#')[-1])
        
        if depth > 1:
            # Recursively get related concepts
            for rel_id in list(related):
                deeper = self.query_related_concepts(rel_id, depth - 1)
                related.update(deeper)
        
        return list(related)
    
    def query_by_methodology(self, methodology: PMMethodology) -> List[str]:
        """Query all concepts for a specific methodology."""
        results = []
        
        for s, p, o in self.graph.triples((None, PM.methodology, Literal(methodology.value))):
            concept_id = str(s).split('#')[-1]
            results.append(concept_id)
        
        return results
    
    def get_concept_info(self, concept_id: str) -> Optional[Dict]:
        """Get comprehensive information about a concept."""
        concept_uri = PM[concept_id]
        
        # Check if concept exists
        if (concept_uri, RDF.type, PM.Concept) not in self.graph:
            return None
        
        info = {
            'id': concept_id,
            'name': None,
            'description': None,
            'methodology': None,
            'source': None,
            'related': []
        }
        
        # Get properties
        for s, p, o in self.graph.triples((concept_uri, None, None)):
            pred_name = str(p).split('#')[-1] if '#' in str(p) else str(p).split('/')[-1]
            
            if pred_name == 'label':
                info['name'] = str(o)
            elif pred_name == 'comment':
                info['description'] = str(o)
            elif pred_name == 'methodology':
                info['methodology'] = str(o)
            elif pred_name == 'source':
                info['source'] = str(o)
            elif pred_name == 'relatedTo':
                related_id = str(o).split('#')[-1]
                info['related'].append(related_id)
        
        return info
    
    def export_to_ttl(self, filepath: str):
        """Export the knowledge graph to Turtle format."""
        self.graph.serialize(destination=filepath, format='turtle')
        logger.info(f"Knowledge graph exported to {filepath}")
    
    def import_from_ttl(self, filepath: str):
        """Import knowledge graph from Turtle format."""
        self.graph.parse(filepath, format='turtle')
        logger.info(f"Knowledge graph imported from {filepath}")
    
    def get_statistics(self) -> Dict[str, int]:
        """Get statistics about the knowledge graph."""
        stats = {
            'total_triples': len(self.graph),
            'concepts': 0,
            'methodologies': 0,
            'relationships': 0
        }
        
        # Count concepts
        for s, p, o in self.graph.triples((None, RDF.type, PM.Concept)):
            stats['concepts'] += 1
        
        # Count unique methodologies
        methodologies = set()
        for s, p, o in self.graph.triples((None, PM.methodology, None)):
            methodologies.add(str(o))
        stats['methodologies'] = len(methodologies)
        
        # Count relationships
        for s, p, o in self.graph.triples((None, PM.relatedTo, None)):
            stats['relationships'] += 1
        
        return stats


def create_pm_knowledge_graph(ontology: Optional[PMDomainOntology] = None) -> PMKnowledgeGraph:
    """Create and initialize a PM knowledge graph."""
    kg = PMKnowledgeGraph()
    
    if ontology:
        kg.add_ontology(ontology)
    
    return kg
