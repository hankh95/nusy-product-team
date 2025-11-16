#!/usr/bin/env python3
"""
NuSy PM Status Knowledge Graph Integration

Converts status information to RDF triples for the knowledge graph.
"""

from typing import List, Dict, Any
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, XSD

from .status_model import ArtifactStatus, Status, StateReason

# Define namespaces
NUSY = Namespace("https://nusy.ai/pm#")
KG = Namespace("https://nusy.ai/kg#")

class StatusRDFConverter:
    """Converts ArtifactStatus objects to RDF triples."""

    def __init__(self):
        self.graph = Graph()
        self.graph.bind("nusy", NUSY)
        self.graph.bind("kg", KG)

    def status_to_rdf(self, status: ArtifactStatus) -> Graph:
        """Convert a single ArtifactStatus to RDF triples."""
        g = Graph()
        g.bind("nusy", NUSY)
        g.bind("kg", KG)

        # Create URIs
        artifact_uri = URIRef(f"https://nusy.ai/pm/{status.type}/{status.id}")

        # Basic type and properties
        g.add((artifact_uri, RDF.type, getattr(NUSY, status.type.capitalize())))
        g.add((artifact_uri, KG.hasId, Literal(status.id)))
        g.add((artifact_uri, KG.hasStatus, Literal(status.status.value)))
        g.add((artifact_uri, KG.createdAt, Literal(status.created_at.isoformat(), datatype=XSD.dateTime)))
        g.add((artifact_uri, KG.updatedAt, Literal(status.updated_at.isoformat(), datatype=XSD.dateTime)))

        # State reason if present
        if status.state_reason:
            g.add((artifact_uri, KG.hasStateReason, Literal(status.state_reason.value)))

        # Assignees
        for assignee in status.assignees:
            g.add((artifact_uri, KG.hasAssignee, Literal(assignee)))

        # Labels
        for label in status.labels:
            g.add((artifact_uri, KG.hasLabel, Literal(label)))

        # Epic relationship
        if status.epic:
            epic_uri = URIRef(f"https://nusy.ai/pm/epic/{status.epic}")
            g.add((artifact_uri, KG.belongsToEpic, epic_uri))

        # Related experiments
        for exp_id in status.related_experiments:
            exp_uri = URIRef(f"https://nusy.ai/pm/experiment/{exp_id}")
            g.add((artifact_uri, KG.relatedTo, exp_uri))

        # Related artifacts
        for art_id in status.related_artifacts:
            art_uri = URIRef(f"https://nusy.ai/pm/artifact/{art_id}")
            g.add((artifact_uri, KG.relatedTo, art_uri))

        return g

    def add_status_to_graph(self, status: ArtifactStatus):
        """Add status triples to the main graph."""
        status_graph = self.status_to_rdf(status)
        self.graph += status_graph

    def serialize_turtle(self) -> str:
        """Serialize the graph as Turtle format."""
        return self.graph.serialize(format='turtle')

    def serialize_jsonld(self) -> str:
        """Serialize the graph as JSON-LD format."""
        return self.graph.serialize(format='json-ld')

class StatusSPARQLQueries:
    """Common SPARQL queries for status information."""

    @staticmethod
    def find_by_status(status_value: str) -> str:
        """Find all artifacts with a specific status."""
        return f"""
        PREFIX kg: <https://nusy.ai/kg#>
        SELECT ?artifact ?id ?type WHERE {{
          ?artifact kg:hasStatus "{status_value}" .
          ?artifact kg:hasId ?id .
          ?artifact a ?typeClass .
          BIND(STRAFTER(STR(?typeClass), "#") AS ?type)
        }}
        """

    @staticmethod
    def find_by_assignee(assignee: str) -> str:
        """Find all artifacts assigned to a specific person."""
        return f"""
        PREFIX kg: <https://nusy.ai/kg#>
        SELECT ?artifact ?id ?type ?status WHERE {{
          ?artifact kg:hasAssignee "{assignee}" .
          ?artifact kg:hasId ?id .
          ?artifact kg:hasStatus ?status .
          ?artifact a ?typeClass .
          BIND(STRAFTER(STR(?typeClass), "#") AS ?type)
        }}
        """

    @staticmethod
    def find_closed_with_reason(reason: str) -> str:
        """Find all closed artifacts with a specific reason."""
        return f"""
        PREFIX kg: <https://nusy.ai/kg#>
        SELECT ?artifact ?id ?type WHERE {{
          ?artifact kg:hasStatus "closed" .
          ?artifact kg:hasStateReason "{reason}" .
          ?artifact kg:hasId ?id .
          ?artifact a ?typeClass .
          BIND(STRAFTER(STR(?typeClass), "#") AS ?type)
        }}
        """

    @staticmethod
    def get_status_summary() -> str:
        """Get a summary of all statuses."""
        return """
        PREFIX kg: <https://nusy.ai/kg#>
        SELECT ?status (COUNT(?artifact) AS ?count) WHERE {
          ?artifact kg:hasStatus ?status .
        } GROUP BY ?status ORDER BY ?status
        """

    @staticmethod
    def find_recently_updated(days: int = 7) -> str:
        """Find artifacts updated within the last N days."""
        return f"""
        PREFIX kg: <https://nusy.ai/kg#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        SELECT ?artifact ?id ?type ?status ?updated WHERE {{
          ?artifact kg:hasId ?id .
          ?artifact kg:hasStatus ?status .
          ?artifact kg:updatedAt ?updated .
          ?artifact a ?typeClass .
          BIND(STRAFTER(STR(?typeClass), "#") AS ?type)
          FILTER (?updated >= NOW() - "{days}"^^xsd:dayTimeDuration)
        }} ORDER BY DESC(?updated)
        """

def generate_status_ontology() -> str:
    """Generate the status ontology in Turtle format."""
    ontology = f"""
@prefix nusy: <https://nusy.ai/pm#> .
@prefix kg: <https://nusy.ai/kg#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# Base classes
kg:Artifact a rdfs:Class ;
    rdfs:label "Artifact" ;
    rdfs:comment "Base class for all NuSy PM artifacts" .

nusy:Feature a rdfs:Class ;
    rdfs:subClassOf kg:Artifact ;
    rdfs:label "Feature" .

nusy:Experiment a rdfs:Class ;
    rdfs:subClassOf kg:Artifact ;
    rdfs:label "Experiment" .

nusy:ShipsLog a rdfs:Class ;
    rdfs:subClassOf kg:Artifact ;
    rdfs:label "Ships Log" .

nusy:QualityAssessment a rdfs:Class ;
    rdfs:subClassOf kg:Artifact ;
    rdfs:label "Quality Assessment" .

# Properties
kg:hasId a rdf:Property ;
    rdfs:label "has ID" ;
    rdfs:domain kg:Artifact ;
    rdfs:range xsd:string .

kg:hasStatus a rdf:Property ;
    rdfs:label "has status" ;
    rdfs:domain kg:Artifact ;
    rdfs:range xsd:string .

kg:hasStateReason a rdf:Property ;
    rdfs:label "has state reason" ;
    rdfs:domain kg:Artifact ;
    rdfs:range xsd:string .

kg:hasAssignee a rdf:Property ;
    rdfs:label "has assignee" ;
    rdfs:domain kg:Artifact ;
    rdfs:range xsd:string .

kg:hasLabel a rdf:Property ;
    rdfs:label "has label" ;
    rdfs:domain kg:Artifact ;
    rdfs:range xsd:string .

kg:belongsToEpic a rdf:Property ;
    rdfs:label "belongs to epic" ;
    rdfs:domain kg:Artifact ;
    rdfs:range kg:Artifact .

kg:relatedTo a rdf:Property ;
    rdfs:label "related to" ;
    rdfs:domain kg:Artifact ;
    rdfs:range kg:Artifact .

kg:createdAt a rdf:Property ;
    rdfs:label "created at" ;
    rdfs:domain kg:Artifact ;
    rdfs:range xsd:dateTime .

kg:updatedAt a rdf:Property ;
    rdfs:label "updated at" ;
    rdfs:domain kg:Artifact ;
    rdfs:range xsd:dateTime .
"""
    return ontology