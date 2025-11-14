from dataclasses import dataclass
from typing import List, Optional
from rdflib import Graph, URIRef, Literal, Namespace, BNode
from rdflib.namespace import RDF, RDFS
import json
import re
from pathlib import Path

from ..models.kg import KGNode, KGRelation

NUSY = Namespace("http://nusy.ai/")
DEFAULT_NAMESPACE = Namespace("http://example.org/")


class NeurosymbolicClinicalReasoner:
    """A lightweight stub of the Neurosymbolic Clinical Reasoner."""

    def __init__(self, graph: Optional[Graph] = None) -> None:
        self.graph = graph or Graph()
        self.graph.bind("ex", DEFAULT_NAMESPACE)

    def _extract_keywords(self, question: str) -> List[str]:
        """Return a short list of keywords from the question text."""
        tokens = re.findall(r"\b[\w']+\b", question.lower())
        keywords = [token for token in tokens if len(token) > 3]
        if not keywords:
            keywords = tokens[:1]
        return keywords

    def query_graph(self, question: str, graph: Optional[Graph] = None) -> dict:
        """Run a simple graph scan and return keyword-aligned triples."""
        target_graph = graph or self.graph
        triples = []
        entities = set()
        relationships = set()
        for s, p, o in target_graph.triples((None, None, None)):
            triples.append((str(s), str(p), str(o)))
            if isinstance(s, (URIRef, BNode)):
                entities.add(str(s))
            if isinstance(o, (URIRef, BNode)):
                entities.add(str(o))
            relationships.add(str(p))
        result = {
            "keywords": self._extract_keywords(question),
            "triples": len(triples),
            "entities": sorted(entities),
            "relationships": sorted(relationships),
        }
        return result

    def sparql_query(self, query: str, graph: Optional[Graph] = None) -> List:
        """Execute a SPARQL query on the graph."""
        target_graph = graph or self.graph
        return list(target_graph.query(query))

@dataclass
class Feature:
    id: str
    title: str
    description: str


def get_initial_features() -> List[Feature]:
    return [
        Feature(
            id="NUSY-FEAT-001",
            title="Scaffold the NuSy Product Project",
            description="Create core repo structure, docs, and first BDD feature.",
        )
    ]


class KnowledgeGraph:
    def __init__(self, graph_path: Optional[Path] = None):
        self.graph_path = graph_path or Path(__file__).resolve().parents[3] / "notes" / "kg.ttl"
        self.graph_path.parent.mkdir(parents=True, exist_ok=True)
        self.g = Graph()
        if self.graph_path.exists():
            self.g.parse(self.graph_path, format="turtle")
        else:
            self._init_graph()
        self.reasoner = NeurosymbolicClinicalReasoner(self.g)

    def _init_graph(self):
        # Add initial triples
        pass

    def add_node(self, node: KGNode):
        for triple in node.to_triples():
            self.g.add(triple)

    def add_relation(self, relation: KGRelation):
        for triple in relation.to_triples():
            self.g.add(triple)

    def query(self, sparql: str):
        return list(self.g.query(sparql))

    def save(self):
        self.g.serialize(destination=self.graph_path, format="turtle")

    def query_notes_by_contributor(self, contributor: str):
        q = f"""
        SELECT ?note ?title ?summary
        WHERE {{
            ?note <{NUSY}contributor> "{contributor}" .
            ?note <{RDFS}label> ?title .
            ?note <{NUSY}summary> ?summary .
        }}
        """
        return self.query(q)

    def query_notes_by_tag(self, tag: str):
        q = f"""
        SELECT ?note ?title
        WHERE {{
            ?note <{NUSY}hasTag> "{tag}" .
            ?note <{RDFS}label> ?title .
        }}
        """
        return self.query(q)

    def neurosymbolic_query(self, question: str):
        """Use the NeurosymbolicClinicalReasoner to query the graph."""
        return self.reasoner.query_graph(question, self.g)

    def sparql_query(self, query: str):
        """Execute SPARQL query using the reasoner."""
        return self.reasoner.sparql_query(query, self.g)
