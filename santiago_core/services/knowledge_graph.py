"""
Santiago Voyage Shared Memory (Knowledge Graph Service)

Implements the "Voyage Shared Memory" layer from the Santiago Fleet Memory Architecture.
This is the collective knowledge graph where all crew members contribute and access
shared project knowledge, decisions, and learnings.

Part of the layered memory system:
- Crew Member Brain: Personal knowledge (personal_memory.py)
- Officer's Private Logbook: Private thoughts (personal_logs.py)
- Bridge Talk: Live conversation memory (conversation_memory.py)
- Voyage Shared Memory: This file - collective project knowledge
- Captain's Intent & Orders: Mission directives (captains_memory.py)
- Multimodal Ingest Officer: Input processing (multimodal_ingest.py)
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
    """RDF-based shared knowledge graph for Santiago voyage/project memory"""

    # Define namespaces
    SANTIAGO = Namespace("https://santiago.ai/ontology/")
    VOYAGE = Namespace("https://santiago.ai/voyage/")
    AGENT = Namespace("https://santiago.ai/agent/")
    TASK = Namespace("https://santiago.ai/task/")
    CONCEPT = Namespace("https://santiago.ai/concept/")
    DECISION = Namespace("https://santiago.ai/decision/")

    def __init__(self, voyage_id: str, workspace_path: Path):
        self.voyage_id = voyage_id
        self.workspace_path = workspace_path
        self.logger = logging.getLogger(f"santiago-voyage-memory-{voyage_id}")

        # Initialize RDF graph for shared memory
        self.graph = Graph()
        self._bind_namespaces()

        # Shared memory file - accessible to entire crew
        self.memory_file = workspace_path / "voyages" / voyage_id / "shared_memory.ttl"
        self.memory_file.parent.mkdir(parents=True, exist_ok=True)

        # Load existing shared knowledge
        self._load_shared_memory()

    def _bind_namespaces(self):
        """Bind RDF namespaces for voyage memory"""
        self.graph.bind("santiago", self.SANTIAGO)
        self.graph.bind("voyage", self.VOYAGE)
        self.graph.bind("agent", self.AGENT)
        self.graph.bind("task", self.TASK)
        self.graph.bind("concept", self.CONCEPT)
        self.graph.bind("decision", self.DECISION)
        self.graph.bind("foaf", FOAF)
        self.graph.bind("rdf", RDF)
        self.graph.bind("rdfs", RDFS)

    def _load_shared_memory(self):
        """Load existing shared voyage memory"""
        if self.memory_file.exists():
            try:
                self.graph.parse(str(self.memory_file), format="turtle")
                self.logger.info(f"Loaded {len(self.graph)} triples from voyage shared memory")
            except Exception as e:
                self.logger.error(f"Error loading voyage shared memory: {e}")
        else:
            self.logger.info("No existing voyage shared memory found, starting fresh")
            # Initialize voyage metadata
            self._initialize_voyage_metadata()

    def _initialize_voyage_metadata(self):
        """Initialize basic voyage metadata in shared memory"""
        voyage_uri = self.VOYAGE[self.voyage_id]

        self.graph.add((voyage_uri, RDF.type, self.SANTIAGO.Voyage))
        self.graph.add((voyage_uri, self.SANTIAGO.voyageId, Literal(self.voyage_id)))
        self.graph.add((voyage_uri, self.SANTIAGO.createdTime, Literal(datetime.now().isoformat(), datatype=XSD.dateTime)))
        self.graph.add((voyage_uri, self.SANTIAGO.status, Literal("active")))

        self.save_shared_memory()

    def save_shared_memory(self):
        """Save shared voyage memory to file"""
        try:
            self.graph.serialize(destination=str(self.memory_file), format="turtle")
            self.logger.info(f"Saved {len(self.graph)} triples to voyage shared memory")
        except Exception as e:
            self.logger.error(f"Error saving voyage shared memory: {e}")

    # Collective Decision Recording
    def record_collective_decision(self, decision_id: str, title: str, description: str,
                                 participants: List[str], outcome: str, rationale: str):
        """Record a decision made collectively by the crew"""
        decision_uri = self.DECISION[decision_id]

        self.graph.add((decision_uri, RDF.type, self.SANTIAGO.CollectiveDecision))
        self.graph.add((decision_uri, self.SANTIAGO.decisionId, Literal(decision_id)))
        self.graph.add((decision_uri, self.SANTIAGO.title, Literal(title)))
        self.graph.add((decision_uri, self.SANTIAGO.description, Literal(description)))
        self.graph.add((decision_uri, self.SANTIAGO.outcome, Literal(outcome)))
        self.graph.add((decision_uri, self.SANTIAGO.rationale, Literal(rationale)))
        self.graph.add((decision_uri, self.SANTIAGO.timestamp, Literal(datetime.now().isoformat(), datatype=XSD.dateTime)))

        # Link to voyage
        voyage_uri = self.VOYAGE[self.voyage_id]
        self.graph.add((decision_uri, self.SANTIAGO.partOfVoyage, voyage_uri))

        # Record participants
        for participant in participants:
            agent_uri = self.AGENT[participant]
            self.graph.add((decision_uri, self.SANTIAGO.participant, agent_uri))

        self.save_shared_memory()
        self.logger.info(f"Recorded collective decision: {decision_id}")

    def get_voyage_decisions(self) -> List[Dict]:
        """Get all decisions made during this voyage"""
        decisions = []

        voyage_uri = self.VOYAGE[self.voyage_id]
        query = f"""
        SELECT ?decision ?title ?outcome ?timestamp
        WHERE {{
            ?decision rdf:type santiago:CollectiveDecision .
            ?decision santiago:partOfVoyage <{voyage_uri}> .
            ?decision santiago:title ?title .
            ?decision santiago:outcome ?outcome .
            ?decision santiago:timestamp ?timestamp .
        }}
        ORDER BY DESC(?timestamp)
        """

        results = self.graph.query(query)

        for row in results:
            decisions.append({
                "decision_id": str(row[0]).split("/")[-1],
                "title": str(row[1]),
                "outcome": str(row[2]),
                "timestamp": str(row[3])
            })

        return decisions

    # Shared Task Management (building on existing)
    def record_shared_task(self, task_id: str, title: str, description: str,
                          assigned_crew: List[str], priority: str = "medium"):
        """Record a task that affects the entire crew/voyage"""
        task_uri = self.TASK[task_id]

        self.graph.add((task_uri, RDF.type, self.SANTIAGO.SharedTask))
        self.graph.add((task_uri, self.SANTIAGO.taskId, Literal(task_id)))
        self.graph.add((task_uri, self.SANTIAGO.title, Literal(title)))
        self.graph.add((task_uri, self.SANTIAGO.description, Literal(description)))
        self.graph.add((task_uri, self.SANTIAGO.priority, Literal(priority)))
        self.graph.add((task_uri, self.SANTIAGO.status, Literal("created")))
        self.graph.add((task_uri, self.SANTIAGO.createdTime, Literal(datetime.now().isoformat(), datatype=XSD.dateTime)))

        # Link to voyage
        voyage_uri = self.VOYAGE[self.voyage_id]
        self.graph.add((task_uri, self.SANTIAGO.partOfVoyage, voyage_uri))

        # Assign to crew members
        for crew_member in assigned_crew:
            agent_uri = self.AGENT[crew_member]
            self.graph.add((task_uri, self.SANTIAGO.assignedTo, agent_uri))

        self.save_shared_memory()

    def update_shared_task_status(self, task_id: str, status: str, updated_by: str, notes: str = ""):
        """Update shared task status with crew consensus"""
        task_uri = self.TASK[task_id]

        # Remove old status
        self.graph.remove((task_uri, self.SANTIAGO.status, None))

        # Add new status and update info
        self.graph.add((task_uri, self.SANTIAGO.status, Literal(status)))
        self.graph.add((task_uri, self.SANTIAGO.updatedTime, Literal(datetime.now().isoformat(), datatype=XSD.dateTime)))
        self.graph.add((task_uri, self.SANTIAGO.updatedBy, self.AGENT[updated_by]))

        if notes:
            self.graph.add((task_uri, self.SANTIAGO.updateNotes, Literal(notes)))

        self.save_shared_memory()

    # Shared Learning Repository
    def record_shared_learning(self, learning_id: str, concept: str, experience: str,
                             outcome: str, contributors: List[str]):
        """Record a learning that benefits the entire crew"""
        learning_uri = BNode()

        concept_uri = self.CONCEPT[concept]

        self.graph.add((learning_uri, RDF.type, self.SANTIAGO.SharedLearning))
        self.graph.add((learning_uri, self.SANTIAGO.learningId, Literal(learning_id)))
        self.graph.add((learning_uri, self.SANTIAGO.concept, concept_uri))
        self.graph.add((learning_uri, self.SANTIAGO.experience, Literal(experience)))
        self.graph.add((learning_uri, self.SANTIAGO.outcome, Literal(outcome)))
        self.graph.add((learning_uri, self.SANTIAGO.timestamp, Literal(datetime.now().isoformat(), datatype=XSD.dateTime)))

        # Link to voyage
        voyage_uri = self.VOYAGE[self.voyage_id]
        self.graph.add((learning_uri, self.SANTIAGO.partOfVoyage, voyage_uri))

        # Record contributors
        for contributor in contributors:
            agent_uri = self.AGENT[contributor]
            self.graph.add((learning_uri, self.SANTIAGO.contributor, agent_uri))

        self.save_shared_memory()

    def get_shared_learnings(self, concept: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """Get shared learnings, optionally filtered by concept"""
        learnings = []

        voyage_uri = self.VOYAGE[self.voyage_id]
        query = f"""
        SELECT ?learning ?concept ?experience ?outcome ?timestamp
        WHERE {{
            ?learning rdf:type santiago:SharedLearning .
            ?learning santiago:partOfVoyage <{voyage_uri}> .
            ?learning santiago:concept ?concept .
            ?learning santiago:experience ?experience .
            ?learning santiago:outcome ?outcome .
            ?learning santiago:timestamp ?timestamp .
        }}
        """

        if concept:
            concept_uri = self.CONCEPT[concept]
            query = query.replace("}", f" FILTER (?concept = <{concept_uri}>) }}")

        query += f" ORDER BY DESC(?timestamp) LIMIT {limit}"

        results = self.graph.query(query)

        for row in results:
            learnings.append({
                "learning_id": str(row[0]) if hasattr(row[0], '__str__') else "anonymous",
                "concept": str(row[1]).split("/")[-1],
                "experience": str(row[2]),
                "outcome": str(row[3]),
                "timestamp": str(row[4])
            })

        return learnings

    # Voyage Status and Metrics
    def get_voyage_status(self) -> Dict:
        """Get current voyage status and metrics"""
        voyage_uri = self.VOYAGE[self.voyage_id]

        query = f"""
        SELECT ?status ?created ?updated
        WHERE {{
            <{voyage_uri}> santiago:status ?status .
            <{voyage_uri}> santiago:createdTime ?created .
            OPTIONAL {{ <{voyage_uri}> santiago:updatedTime ?updated }}
        }}
        """

        result = self.graph.query(query).bindings[0] if self.graph.query(query).bindings else {}

        return {
            "voyage_id": self.voyage_id,
            "status": str(result.get('status', 'unknown')) if result else 'unknown',
            "created": str(result.get('created', '')) if result else '',
            "updated": str(result.get('updated', '')) if result else '',
            "decisions_count": len(self.get_voyage_decisions()),
            "shared_tasks_count": len(self.get_shared_tasks()),
            "shared_learnings_count": len(self.get_shared_learnings(limit=1000))
        }

    def get_shared_tasks(self) -> List[Dict]:
        """Get all shared tasks for this voyage"""
        tasks = []

        voyage_uri = self.VOYAGE[self.voyage_id]
        query = f"""
        SELECT ?task ?title ?status ?priority
        WHERE {{
            ?task rdf:type santiago:SharedTask .
            ?task santiago:partOfVoyage <{voyage_uri}> .
            ?task santiago:title ?title .
            ?task santiago:status ?status .
            ?task santiago:priority ?priority .
        }}
        ORDER BY ?priority DESC(?status)
        """

        results = self.graph.query(query)

        for row in results:
            tasks.append({
                "task_id": str(row[0]).split("/")[-1],
                "title": str(row[1]),
                "status": str(row[2]),
                "priority": str(row[3])
            })

        return tasks

    # Query methods (preserved from original)
    def sparql_query(self, query: str) -> List[Dict]:
        """Execute a SPARQL query on shared memory"""
        try:
            results = self.graph.query(query)
            return [dict(row) for row in results]
        except Exception as e:
            self.logger.error(f"SPARQL query error: {e}")
            return []

    def get_statistics(self) -> Dict:
        """Get voyage shared memory statistics"""
        return {
            "total_triples": len(self.graph),
            "decisions": len(list(self.graph.subjects(RDF.type, self.SANTIAGO.CollectiveDecision))),
            "shared_tasks": len(list(self.graph.subjects(RDF.type, self.SANTIAGO.SharedTask))),
            "shared_learnings": len(list(self.graph.subjects(RDF.type, self.SANTIAGO.SharedLearning))),
            "concepts": len(list(self.graph.subjects(RDF.type, self.SANTIAGO.Concept))),
            "voyage_id": self.voyage_id
        }