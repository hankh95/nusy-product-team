"""Minimal NuSy prototype implementation used by the verification script."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, List, Optional

from rdflib import BNode, Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, RDFS

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
        for s, p, o in target_graph.triples((None, None, None)):
            triples.append((str(s), str(p), str(o)))
            if isinstance(s, (URIRef, BNode)):
                entities.add(str(s))
        result = {
            "keywords": self._extract_keywords(question),
            "triples": len(triples),
            "entities": sorted(entities),
        }
        return result


def load_ci_tagged_graph(source: Optional[str] = None) -> Graph:
    """Load a knowledge graph from a file or create a sample graph."""
    graph = Graph()
    graph.bind("ex", DEFAULT_NAMESPACE)
    if source and Path(source).exists():
        graph.parse(source, format=Path(source).suffix.lstrip("."))
        return graph

    # Build a minimal sample graph for demonstration purposes
    stroke = DEFAULT_NAMESPACE.stroke
    headache = DEFAULT_NAMESPACE.headache
    graph.add((stroke, RDF.type, DEFAULT_NAMESPACE.MedicalCondition))
    graph.add((stroke, RDFS.label, Literal("Ischemic Stroke")))
    graph.add((stroke, DEFAULT_NAMESPACE.hasSymptom, headache))
    graph.add((headache, RDF.type, DEFAULT_NAMESPACE.Symptom))
    graph.add((headache, RDFS.label, Literal("Headache")))
    return graph
