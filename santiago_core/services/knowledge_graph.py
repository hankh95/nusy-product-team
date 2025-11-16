"""
Santiago Knowledge Graph Service

Manages the RDF knowledge graph for persistent learning and agent memory.
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from rdflib import Graph, Literal, Namespace, RDF, RDFS, URIRef, BNode
from rdflib.namespace import FOAF, XSD


class SantiagoKnowledgeGraph:
    """RDF-based knowledge graph for Santiago agents"""

    # Define namespaces
    SANTIAGO = Namespace("https://santiago.ai/ontology/")
    PROJECT = Namespace("https://santiago.ai/project/")
    AGENT = Namespace("https://santiago.ai/agent/")
    TASK = Namespace("https://santiago.ai/task/")
    CONCEPT = Namespace("https://santiago.ai/concept/")

    def __init__(self, workspace_path: Path):
        self.workspace_path = workspace_path
        self.logger = logging.getLogger("santiago-kg")

        # Initialize RDF graph
        self.graph = Graph()
        self._bind_namespaces()

        # Knowledge graph file
        self.kg_file = workspace_path / "santiago_core" / "knowledge" / "santiago_kg.ttl"
        self.kg_file.parent.mkdir(parents=True, exist_ok=True)

        # Load existing knowledge if available
        self._load_knowledge()

    def _bind_namespaces(self):
        """Bind RDF namespaces"""
        self.graph.bind("santiago", self.SANTIAGO)
        self.graph.bind("project", self.PROJECT)
        self.graph.bind("agent", self.AGENT)
        self.graph.bind("task", self.TASK)
        self.graph.bind("concept", self.CONCEPT)
        self.graph.bind("foaf", FOAF)
        self.graph.bind("rdf", RDF)
        self.graph.bind("rdfs", RDFS)

    def _load_knowledge(self):
        """Load existing knowledge from file"""
        if self.kg_file.exists():
            try:
                self.graph.parse(str(self.kg_file), format="turtle")
                self.logger.info(f"Loaded {len(self.graph)} triples from knowledge graph")
            except Exception as e:
                self.logger.error(f"Error loading knowledge graph: {e}")
        else:
            self.logger.info("No existing knowledge graph found, starting fresh")

    def save_knowledge(self):
        """Save knowledge graph to file"""
        try:
            self.graph.serialize(destination=str(self.kg_file), format="turtle")
            self.logger.info(f"Saved {len(self.graph)} triples to knowledge graph")
        except Exception as e:
            self.logger.error(f"Error saving knowledge graph: {e}")

    # Agent-related methods
    def register_agent(self, agent_name: str, agent_type: str, capabilities: List[str]):
        """Register an agent in the knowledge graph"""
        agent_uri = self.AGENT[agent_name]

        self.graph.add((agent_uri, RDF.type, self.SANTIAGO.Agent))
        self.graph.add((agent_uri, self.SANTIAGO.agentType, Literal(agent_type)))
        self.graph.add((agent_uri, self.SANTIAGO.name, Literal(agent_name)))
        self.graph.add((agent_uri, self.SANTIAGO.registrationTime, Literal(datetime.now().isoformat(), datatype=XSD.dateTime)))

        for capability in capabilities:
            self.graph.add((agent_uri, self.SANTIAGO.capability, Literal(capability)))

        self.save_knowledge()
        self.logger.info(f"Registered agent: {agent_name}")

    def get_agent_capabilities(self, agent_name: str) -> List[str]:
        """Get capabilities for an agent"""
        agent_uri = self.AGENT[agent_name]
        capabilities = []

        for s, p, o in self.graph.triples((agent_uri, self.SANTIAGO.capability, None)):
            capabilities.append(str(o))

        return capabilities

    # Task-related methods
    def record_task(self, task_id: str, title: str, description: str, assigned_to: Optional[str] = None):
        """Record a task in the knowledge graph"""
        task_uri = self.TASK[task_id]

        self.graph.add((task_uri, RDF.type, self.SANTIAGO.Task))
        self.graph.add((task_uri, self.SANTIAGO.taskId, Literal(task_id)))
        self.graph.add((task_uri, self.SANTIAGO.title, Literal(title)))
        self.graph.add((task_uri, self.SANTIAGO.description, Literal(description)))
        self.graph.add((task_uri, self.SANTIAGO.status, Literal("created")))
        self.graph.add((task_uri, self.SANTIAGO.createdTime, Literal(datetime.now().isoformat(), datatype=XSD.dateTime)))

        if assigned_to:
            agent_uri = self.AGENT[assigned_to]
            self.graph.add((task_uri, self.SANTIAGO.assignedTo, agent_uri))

        self.save_knowledge()

    def update_task_status(self, task_id: str, status: str, completed_by: Optional[str] = None):
        """Update task status in knowledge graph"""
        task_uri = self.TASK[task_id]

        # Remove old status
        self.graph.remove((task_uri, self.SANTIAGO.status, None))

        # Add new status
        self.graph.add((task_uri, self.SANTIAGO.status, Literal(status)))
        self.graph.add((task_uri, self.SANTIAGO.updatedTime, Literal(datetime.now().isoformat(), datatype=XSD.dateTime)))

        if completed_by:
            agent_uri = self.AGENT[completed_by]
            self.graph.add((task_uri, self.SANTIAGO.completedBy, agent_uri))

        self.save_knowledge()

    def get_task_history(self, agent_name: Optional[str] = None) -> List[Dict]:
        """Get task history, optionally filtered by agent"""
        tasks = []

        query = """
        SELECT ?task ?title ?status ?assignedTo ?completedBy
        WHERE {
            ?task rdf:type santiago:Task .
            ?task santiago:title ?title .
            ?task santiago:status ?status .
            OPTIONAL { ?task santiago:assignedTo ?assignedTo }
            OPTIONAL { ?task santiago:completedBy ?completedBy }
        }
        """

        if agent_name:
            agent_uri = self.AGENT[agent_name]
            query = f"""
            SELECT ?task ?title ?status ?assignedTo ?completedBy
            WHERE {{
                ?task rdf:type santiago:Task .
                ?task santiago:title ?title .
                ?task santiago:status ?status .
                OPTIONAL {{ ?task santiago:assignedTo ?assignedTo }}
                OPTIONAL {{ ?task santiago:completedBy ?completedBy }}
                FILTER (?assignedTo = <{agent_uri}> || ?completedBy = <{agent_uri}>)
            }}
            """

        results = self.graph.query(query)

        for row in results:
            tasks.append({
                "task_id": str(row[0]).split("/")[-1],
                "title": str(row[1]),
                "status": str(row[2]),
                "assigned_to": str(row[3]).split("/")[-1] if row[3] else None,
                "completed_by": str(row[4]).split("/")[-1] if row[4] else None
            })

        return tasks

    # Learning methods
    def record_learning(self, agent_name: str, concept: str, experience: str, outcome: str):
        """Record a learning experience"""
        learning_uri = BNode()  # Use blank node for learning events

        agent_uri = self.AGENT[agent_name]
        concept_uri = self.CONCEPT[concept]

        self.graph.add((learning_uri, RDF.type, self.SANTIAGO.Learning))
        self.graph.add((learning_uri, self.SANTIAGO.agent, agent_uri))
        self.graph.add((learning_uri, self.SANTIAGO.concept, concept_uri))
        self.graph.add((learning_uri, self.SANTIAGO.experience, Literal(experience)))
        self.graph.add((learning_uri, self.SANTIAGO.outcome, Literal(outcome)))
        self.graph.add((learning_uri, self.SANTIAGO.timestamp, Literal(datetime.now().isoformat(), datatype=XSD.dateTime)))

        self.save_knowledge()

    def get_similar_experiences(self, concept: str, limit: int = 5) -> List[Dict]:
        """Get similar learning experiences for a concept"""
        concept_uri = self.CONCEPT[concept]
        experiences = []

        query = f"""
        SELECT ?experience ?outcome ?agent
        WHERE {{
            ?learning rdf:type santiago:Learning .
            ?learning santiago:concept <{concept_uri}> .
            ?learning santiago:experience ?experience .
            ?learning santiago:outcome ?outcome .
            ?learning santiago:agent ?agent .
        }}
        LIMIT {limit}
        """

        results = self.graph.query(query)

        for row in results:
            experiences.append({
                "experience": str(row[0]),
                "outcome": str(row[1]),
                "agent": str(row[2]).split("/")[-1]
            })

        return experiences

    # Concept relationship methods
    def add_concept_relationship(self, concept1: str, relationship: str, concept2: str):
        """Add relationship between concepts"""
        c1_uri = self.CONCEPT[concept1]
        c2_uri = self.CONCEPT[concept2]

        # Define relationship URI
        rel_uri = self.SANTIAGO[relationship]

        self.graph.add((c1_uri, rel_uri, c2_uri))
        self.save_knowledge()

    def get_related_concepts(self, concept: str, relationship: Optional[str] = None) -> List[Tuple[str, str]]:
        """Get concepts related to the given concept"""
        concept_uri = self.CONCEPT[concept]
        related = []

        if relationship:
            rel_uri = self.SANTIAGO[relationship]
            for s, p, o in self.graph.triples((concept_uri, rel_uri, None)):
                related.append((str(o).split("/")[-1], relationship))
            for s, p, o in self.graph.triples((None, rel_uri, concept_uri)):
                related.append((str(s).split("/")[-1], f"inverse_{relationship}"))
        else:
            # Get all relationships
            for s, p, o in self.graph.triples((concept_uri, None, None)):
                if str(p).startswith(str(self.SANTIAGO)):
                    rel = str(p).split("/")[-1]
                    related.append((str(o).split("/")[-1], rel))
            for s, p, o in self.graph.triples((None, None, concept_uri)):
                if str(p).startswith(str(self.SANTIAGO)):
                    rel = str(p).split("/")[-1]
                    related.append((str(s).split("/")[-1], f"inverse_{rel}"))

        return related

    # Query methods
    def sparql_query(self, query: str) -> List[Dict]:
        """Execute a SPARQL query"""
        try:
            results = self.graph.query(query)
            return [dict(row) for row in results]
        except Exception as e:
            self.logger.error(f"SPARQL query error: {e}")
            return []

    def get_statistics(self) -> Dict:
        """Get knowledge graph statistics"""
        return {
            "total_triples": len(self.graph),
            "agents": len(list(self.graph.subjects(RDF.type, self.SANTIAGO.Agent))),
            "tasks": len(list(self.graph.subjects(RDF.type, self.SANTIAGO.Task))),
            "concepts": len(list(self.graph.subjects(RDF.type, self.SANTIAGO.Concept))),
            "learning_events": len(list(self.graph.subjects(RDF.type, self.SANTIAGO.Learning)))
        }