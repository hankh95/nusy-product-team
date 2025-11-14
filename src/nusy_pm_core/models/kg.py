from dataclasses import dataclass
from typing import Optional
from rdflib import URIRef, Literal, BNode
from rdflib.namespace import RDF, RDFS, XSD


@dataclass
class KGNode:
    uri: URIRef
    label: str
    type: URIRef

    def to_triples(self):
        return [
            (self.uri, RDF.type, self.type),
            (self.uri, RDFS.label, Literal(self.label)),
        ]


@dataclass
class KGRelation:
    subject: URIRef
    predicate: URIRef
    object: URIRef
    label: Optional[str] = None

    def to_triples(self):
        triples = [(self.subject, self.predicate, self.object)]
        if self.label:
            triples.append((self.subject, self.predicate, Literal(self.label)))
        return triples