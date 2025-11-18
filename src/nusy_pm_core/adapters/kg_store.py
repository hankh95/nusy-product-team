"""
Knowledge Graph Storage Adapter
================================
Provides persistent RDF triple storage for Santiago's knowledge accumulation.

Architecture:
- RDFLib backend (pure Python, serializable)
- Turtle format for human-readable storage
- SPARQL query interface
- Provenance tracking via named graphs
- Thread-safe operations

Usage:
    kg = KGStore(workspace_path=".")
    kg.add_triples([(subject, predicate, object)])
    results = kg.query("SELECT ?s ?p ?o WHERE { ?s ?p ?o }")
    kg.save()
    kg.load()
"""

from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any
from datetime import datetime
import json
from dataclasses import dataclass, asdict
import threading

from rdflib import Graph, Namespace, URIRef, Literal, BNode
from rdflib.namespace import RDF, RDFS, XSD, OWL
from rdflib.plugins.sparql import prepareQuery


@dataclass
class KGTriple:
    """Represents a single RDF triple with provenance"""
    subject: str
    predicate: str
    object: str
    source: Optional[str] = None
    extracted_at: Optional[str] = None
    confidence: float = 1.0


@dataclass
class KGStats:
    """Knowledge Graph statistics"""
    total_triples: int
    unique_subjects: int
    unique_predicates: int
    unique_objects: int
    namespaces: List[str]
    last_updated: str


class KGStore:
    """
    RDFLib-based knowledge graph storage with persistence.
    
    Features:
    - Triple storage and retrieval
    - SPARQL query interface
    - Turtle serialization
    - Provenance tracking
    - Incremental updates
    """
    
    def __init__(self, workspace_path: str = "."):
        """
        Initialize KG store.
        
        Args:
            workspace_path: Root path for workspace (stores KG in knowledge/kg/)
        """
        self.workspace_path = Path(workspace_path)
        self.kg_dir = self.workspace_path / "knowledge" / "kg"
        self.kg_dir.mkdir(parents=True, exist_ok=True)
        
        # Primary knowledge graph
        self.graph = Graph()
        
        # Define namespaces
        self.SANTIAGO = Namespace("https://nusy.dev/santiago/")
        self.PM = Namespace("https://nusy.dev/pm/")
        self.PROV = Namespace("http://www.w3.org/ns/prov#")
        
        self.graph.bind("santiago", self.SANTIAGO)
        self.graph.bind("pm", self.PM)
        self.graph.bind("prov", self.PROV)
        self.graph.bind("rdf", RDF)
        self.graph.bind("rdfs", RDFS)
        self.graph.bind("owl", OWL)
        
        # Thread safety
        self.lock = threading.RLock()
        
        # Paths
        self.kg_file = self.kg_dir / "santiago_kg.ttl"
        self.stats_file = self.kg_dir / "kg_stats.json"
        self.provenance_file = self.kg_dir / "provenance.json"
        
        # Load existing data if available
        if self.kg_file.exists():
            self.load()
    
    def add_triple(
        self, 
        subject: str, 
        predicate: str, 
        obj: str,
        source: Optional[str] = None,
        confidence: float = 1.0
    ) -> None:
        """
        Add a single triple to the knowledge graph.
        
        Args:
            subject: Subject URI or identifier
            predicate: Predicate URI or identifier
            obj: Object URI, identifier, or literal value
            source: Source document/file (for provenance)
            confidence: Confidence score (0.0-1.0)
        """
        with self.lock:
            # Convert to RDF terms
            s = self._to_uri_ref(subject)
            p = self._to_uri_ref(predicate)
            o = self._to_term(obj)
            
            # Add triple
            self.graph.add((s, p, o))
            
            # Add provenance if source provided
            if source:
                self._add_provenance(s, p, o, source, confidence)
    
    def add_triples(self, triples: List[KGTriple]) -> int:
        """
        Add multiple triples to the knowledge graph.
        
        Args:
            triples: List of KGTriple objects
            
        Returns:
            Number of triples added
        """
        with self.lock:
            count = 0
            for triple in triples:
                self.add_triple(
                    subject=triple.subject,
                    predicate=triple.predicate,
                    obj=triple.object,
                    source=triple.source,
                    confidence=triple.confidence
                )
                count += 1
            return count
    
    def query(self, sparql_query: str) -> List[Dict[str, Any]]:
        """
        Execute SPARQL query on knowledge graph.
        
        Args:
            sparql_query: SPARQL SELECT query
            
        Returns:
            List of result bindings as dictionaries
        """
        with self.lock:
            results = []
            qres = self.graph.query(sparql_query)
            
            for row in qres:
                result_dict = {}
                for var in qres.vars:
                    value = row[var]
                    result_dict[str(var)] = self._term_to_value(value)
                results.append(result_dict)
            
            return results
    
    def get_entities_by_type(self, entity_type: str) -> List[str]:
        """
        Get all entities of a specific type.
        
        Args:
            entity_type: RDF type (e.g., "pm:Feature", "pm:Behavior")
            
        Returns:
            List of entity URIs
        """
        query = f"""
        SELECT ?entity WHERE {{
            ?entity rdf:type {entity_type} .
        }}
        """
        results = self.query(query)
        return [r["entity"] for r in results]
    
    def get_entity_properties(self, entity_uri: str) -> Dict[str, Any]:
        """
        Get all properties of an entity.
        
        Args:
            entity_uri: Entity URI
            
        Returns:
            Dictionary of property-value pairs
        """
        query = f"""
        SELECT ?property ?value WHERE {{
            <{entity_uri}> ?property ?value .
        }}
        """
        results = self.query(query)
        
        properties = {}
        for r in results:
            prop = r["property"]
            val = r["value"]
            
            # Group multiple values for same property
            if prop in properties:
                if not isinstance(properties[prop], list):
                    properties[prop] = [properties[prop]]
                properties[prop].append(val)
            else:
                properties[prop] = val
        
        return properties
    
    def save(self) -> None:
        """Persist knowledge graph to disk (Turtle format)."""
        with self.lock:
            # Save graph
            self.graph.serialize(destination=str(self.kg_file), format="turtle")
            
            # Save statistics
            stats = self.get_statistics()
            with open(self.stats_file, "w") as f:
                json.dump(asdict(stats), f, indent=2)
            
            print(f"✅ KG saved: {self.kg_file}")
            print(f"   📊 Triples: {stats.total_triples}")
    
    def load(self) -> None:
        """Load knowledge graph from disk."""
        with self.lock:
            if self.kg_file.exists():
                self.graph.parse(str(self.kg_file), format="turtle")
                stats = self.get_statistics()
                print(f"✅ KG loaded: {self.kg_file}")
                print(f"   📊 Triples: {stats.total_triples}")
            else:
                print("ℹ️  No existing KG found, starting fresh")
    
    def get_statistics(self) -> KGStats:
        """Get knowledge graph statistics."""
        with self.lock:
            total = len(self.graph)
            subjects = set(s for s, _, _ in self.graph)
            predicates = set(p for _, p, _ in self.graph)
            objects = set(o for _, _, o in self.graph)
            namespaces = [str(ns) for _, ns in self.graph.namespaces()]
            
            return KGStats(
                total_triples=total,
                unique_subjects=len(subjects),
                unique_predicates=len(predicates),
                unique_objects=len(objects),
                namespaces=namespaces,
                last_updated=datetime.now().isoformat()
            )
    
    def export_domain_knowledge(self, domain_name: str, output_path: Optional[Path] = None) -> str:
        """
        Export all knowledge related to a specific domain.
        
        Args:
            domain_name: Domain identifier
            output_path: Optional output file path
            
        Returns:
            Path to exported file
        """
        with self.lock:
            # Query all triples related to domain
            query = f"""
            SELECT ?s ?p ?o WHERE {{
                ?s ?p ?o .
                FILTER(CONTAINS(STR(?s), "{domain_name}") || 
                       CONTAINS(STR(?o), "{domain_name}"))
            }}
            """
            
            # Create new graph with filtered triples
            domain_graph = Graph()
            for prefix, namespace in self.graph.namespaces():
                domain_graph.bind(prefix, namespace)
            
            results = self.graph.query(query)
            for row in results:
                domain_graph.add((row.s, row.p, row.o))
            
            # Export
            if output_path is None:
                output_path = self.kg_dir / f"{domain_name}_export.ttl"
            
            domain_graph.serialize(destination=str(output_path), format="turtle")
            print(f"✅ Domain knowledge exported: {output_path}")
            print(f"   📊 Triples: {len(domain_graph)}")
            
            return str(output_path)
    
    def clear(self) -> None:
        """Clear all triples from knowledge graph."""
        with self.lock:
            self.graph = Graph()
            for prefix, namespace in [
                ("santiago", self.SANTIAGO),
                ("pm", self.PM),
                ("prov", self.PROV),
                ("rdf", RDF),
                ("rdfs", RDFS),
                ("owl", OWL)
            ]:
                self.graph.bind(prefix, namespace)
            print("🗑️  KG cleared")
    
    # Private helper methods
    
    def _to_uri_ref(self, value: str) -> URIRef:
        """Convert string to URIRef, handling namespaces."""
        if value.startswith("http://") or value.startswith("https://"):
            return URIRef(value)
        elif ":" in value:
            # Handle namespace prefix
            prefix, local = value.split(":", 1)
            if prefix == "pm":
                return self.PM[local]
            elif prefix == "santiago":
                return self.SANTIAGO[local]
            elif prefix == "prov":
                return self.PROV[local]
            elif prefix == "rdf":
                return RDF[local]
            elif prefix == "rdfs":
                return RDFS[local]
            elif prefix == "owl":
                return OWL[local]
        
        # Default to santiago namespace
        return self.SANTIAGO[value]
    
    def _to_term(self, value: str):
        """Convert string to appropriate RDF term (URIRef or Literal)."""
        # Check if it's a URI
        if value.startswith("http://") or value.startswith("https://") or ":" in value:
            return self._to_uri_ref(value)
        
        # Otherwise treat as literal
        return Literal(value)
    
    def _term_to_value(self, term) -> str:
        """Convert RDF term to string value."""
        if isinstance(term, Literal):
            return str(term)
        elif isinstance(term, URIRef):
            return str(term)
        elif isinstance(term, BNode):
            return str(term)
        else:
            return str(term)
    
    def _add_provenance(
        self, 
        subject: URIRef, 
        predicate: URIRef, 
        obj, 
        source: str,
        confidence: float
    ) -> None:
        """Add provenance metadata for a triple."""
        # Create a blank node for the provenance statement
        stmt = BNode()
        
        # Statement about the triple
        self.graph.add((stmt, RDF.type, RDF.Statement))
        self.graph.add((stmt, RDF.subject, subject))
        self.graph.add((stmt, RDF.predicate, predicate))
        self.graph.add((stmt, RDF.object, obj))
        
        # Provenance info
        self.graph.add((stmt, self.PROV.wasDerivedFrom, Literal(source)))
        self.graph.add((stmt, self.PROV.generatedAtTime, Literal(datetime.now().isoformat(), datatype=XSD.dateTime)))
        self.graph.add((stmt, self.SANTIAGO.confidence, Literal(confidence, datatype=XSD.float)))


# Factory function
def create_kg_store(workspace_path: str = ".") -> KGStore:
    """
    Factory function to create KGStore instance.
    
    Args:
        workspace_path: Root path for workspace
        
    Returns:
        Configured KGStore instance
    """
    return KGStore(workspace_path=workspace_path)
