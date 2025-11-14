"""CatchFish Module: Convert L0 content to knowledge graph triples."""

from typing import Dict, List
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS


NUSY = Namespace("http://nusy.ai/")


class CatchFishProcessor:
    """Processes L0 content into knowledge graph triples."""

    def __init__(self):
        self.graph = Graph()
        self.graph.bind("nusy", NUSY)

    def process_l0_content(self, l0_content: List[Dict], kg) -> int:
        """Process L0 content into KG triples and return count added."""
        triples_before = len(kg.g)
        for item in l0_content:
            if item['type'] == 'section':
                self._process_section(item, kg)
        triples_after = len(kg.g)
        return triples_after - triples_before

    def _process_section(self, section: Dict, kg):
        """Process a section into triples."""
        section_uri = URIRef(f"{NUSY}section/{hash(section['title'])}")
        kg.g.add((section_uri, RDF.type, NUSY.Section))
        kg.g.add((section_uri, RDFS.label, Literal(section['title'])))
        kg.g.add((section_uri, NUSY.content, Literal(section['content'])))

        # Link to source
        source_uri = URIRef(f"{NUSY}source/{hash(section['source']['path'])}")
        kg.g.add((source_uri, RDF.type, NUSY.Source))
        kg.g.add((source_uri, RDFS.label, Literal(section['source']['filename'])))
        kg.g.add((section_uri, NUSY.fromSource, source_uri))