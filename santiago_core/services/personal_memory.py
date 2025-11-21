"""
Santiago Crew Member Brain (Personal Memory Service)

Implements the "Crew Member Brain" layer from the Santiago Fleet Memory Architecture.
This is the private, persistent knowledge of individual agents - their lifetime learnings,
personal notes, and autonomous memory that never gets deleted.

Each crew member has their own personal tupugit (brain) that's private to them,
containing their unique knowledge, patterns, and experiences.

Part of the layered memory system:
- Crew Member Brain: This file - personal agent knowledge
- Officer's Private Logbook: Private thoughts (personal_logs.py)
- Bridge Talk: Live conversation memory (conversation_memory.py)
- Voyage Shared Memory: Collective knowledge (knowledge_graph.py)
- Captain's Intent & Orders: Mission directives (captains_memory.py)
- Multimodal Ingest Officer: Input processing (multimodal_ingest.py)
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import hashlib

from rdflib import Graph, Literal, Namespace, RDF, RDFS, URIRef, BNode
from rdflib.namespace import FOAF, XSD


class SantiagoCrewMemberBrain:
    """Personal knowledge graph for individual Santiago agents"""

    # Define namespaces for personal knowledge
    SANTIAGO = Namespace("https://santiago.ai/ontology/")
    PERSONAL = Namespace("https://santiago.ai/personal/")
    AGENT = Namespace("https://santiago.ai/agent/")
    CONCEPT = Namespace("https://santiago.ai/concept/")
    EXPERIENCE = Namespace("https://santiago.ai/experience/")

    def __init__(self, agent_name: str, workspace_path: Path):
        self.agent_name = agent_name
        self.workspace_path = workspace_path
        self.logger = logging.getLogger(f"santiago-brain-{agent_name}")

        # Initialize personal RDF graph
        self.graph = Graph()
        self._bind_namespaces()

        # Personal brain file - private to this agent
        self.brain_file = workspace_path / "crew" / agent_name / "brain.ttl"
        self.brain_file.parent.mkdir(parents=True, exist_ok=True)

        # Load existing personal knowledge
        self._load_personal_brain()

    def _bind_namespaces(self):
        """Bind RDF namespaces for personal brain"""
        self.graph.bind("santiago", self.SANTIAGO)
        self.graph.bind("personal", self.PERSONAL)
        self.graph.bind("agent", self.AGENT)
        self.graph.bind("concept", self.CONCEPT)
        self.graph.bind("experience", self.EXPERIENCE)
        self.graph.bind("foaf", FOAF)
        self.graph.bind("rdf", RDF)
        self.graph.bind("rdfs", RDFS)

    def _load_personal_brain(self):
        """Load existing personal brain knowledge"""
        if self.brain_file.exists():
            try:
                self.graph.parse(str(self.brain_file), format="turtle")
                self.logger.info(f"Loaded {len(self.graph)} triples from personal brain")
            except Exception as e:
                self.logger.error(f"Error loading personal brain: {e}")
        else:
            self.logger.info("No existing personal brain found, starting fresh")
            # Initialize agent metadata
            self._initialize_personal_brain()

    def _initialize_personal_brain(self):
        """Initialize basic agent metadata in personal brain"""
        agent_uri = self.AGENT[self.agent_name]

        self.graph.add((agent_uri, RDF.type, self.SANTIAGO.Agent))
        self.graph.add((agent_uri, self.SANTIAGO.name, Literal(self.agent_name)))
        self.graph.add((agent_uri, self.SANTIAGO.brainCreated, Literal(datetime.now().isoformat(), datatype=XSD.dateTime)))
        self.graph.add((agent_uri, self.SANTIAGO.brainStatus, Literal("active")))

        self.save_personal_brain()

    def save_personal_brain(self):
        """Save personal brain to file"""
        try:
            self.graph.serialize(destination=str(self.brain_file), format="turtle")
            self.logger.info(f"Saved {len(self.graph)} triples to personal brain")
        except Exception as e:
            self.logger.error(f"Error saving personal brain: {e}")

    # Personal Knowledge Recording
    def record_personal_knowledge(self, concept: str, knowledge: str, confidence: float = 1.0,
                                source: str = "experience", tags: List[str] = None):
        """Record personal knowledge that this agent has learned"""
        knowledge_uri = BNode()
        concept_uri = self.CONCEPT[concept]
        agent_uri = self.AGENT[self.agent_name]

        # Create knowledge hash for deduplication
        knowledge_hash = hashlib.md5(knowledge.encode()).hexdigest()

        self.graph.add((knowledge_uri, RDF.type, self.SANTIAGO.PersonalKnowledge))
        self.graph.add((knowledge_uri, self.SANTIAGO.agent, agent_uri))
        self.graph.add((knowledge_uri, self.SANTIAGO.concept, concept_uri))
        self.graph.add((knowledge_uri, self.SANTIAGO.knowledge, Literal(knowledge)))
        self.graph.add((knowledge_uri, self.SANTIAGO.confidence, Literal(confidence, datatype=XSD.float)))
        self.graph.add((knowledge_uri, self.SANTIAGO.source, Literal(source)))
        self.graph.add((knowledge_uri, self.SANTIAGO.knowledgeHash, Literal(knowledge_hash)))
        self.graph.add((knowledge_uri, self.SANTIAGO.timestamp, Literal(datetime.now().isoformat(), datatype=XSD.dateTime)))

        if tags:
            for tag in tags:
                self.graph.add((knowledge_uri, self.SANTIAGO.tag, Literal(tag)))

        self.save_personal_brain()
        self.logger.info(f"Recorded personal knowledge for concept: {concept}")

    def get_personal_knowledge(self, concept: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """Retrieve personal knowledge, optionally filtered by concept"""
        knowledge_list = []

        agent_uri = self.AGENT[self.agent_name]
        query = f"""
        SELECT ?knowledge ?concept ?confidence ?source ?timestamp
        WHERE {{
            ?k rdf:type santiago:PersonalKnowledge .
            ?k santiago:agent <{agent_uri}> .
            ?k santiago:knowledge ?knowledge .
            ?k santiago:concept ?concept .
            ?k santiago:confidence ?confidence .
            ?k santiago:source ?source .
            ?k santiago:timestamp ?timestamp .
        }}
        """

        if concept:
            concept_uri = self.CONCEPT[concept]
            query = query.replace("}", f" FILTER (?concept = <{concept_uri}>) }}")

        query += f" ORDER BY DESC(?confidence) DESC(?timestamp) LIMIT {limit}"

        results = self.graph.query(query)

        for row in results:
            knowledge_list.append({
                "knowledge": str(row[0]),
                "concept": str(row[1]).split("/")[-1],
                "confidence": float(row[2]),
                "source": str(row[3]),
                "timestamp": str(row[4])
            })

        return knowledge_list

    # Personal Pattern Recognition
    def record_behavior_pattern(self, pattern_name: str, description: str,
                              triggers: List[str], actions: List[str], success_rate: float):
        """Record a behavioral pattern this agent has learned"""
        pattern_uri = BNode()
        agent_uri = self.AGENT[self.agent_name]

        self.graph.add((pattern_uri, RDF.type, self.SANTIAGO.BehaviorPattern))
        self.graph.add((pattern_uri, self.SANTIAGO.agent, agent_uri))
        self.graph.add((pattern_uri, self.SANTIAGO.patternName, Literal(pattern_name)))
        self.graph.add((pattern_uri, self.SANTIAGO.description, Literal(description)))
        self.graph.add((pattern_uri, self.SANTIAGO.successRate, Literal(success_rate, datatype=XSD.float)))
        self.graph.add((pattern_uri, self.SANTIAGO.discoveredTime, Literal(datetime.now().isoformat(), datatype=XSD.dateTime)))

        # Record triggers and actions
        for trigger in triggers:
            self.graph.add((pattern_uri, self.SANTIAGO.trigger, Literal(trigger)))

        for action in actions:
            self.graph.add((pattern_uri, self.SANTIAGO.action, Literal(action)))

        self.save_personal_brain()
        self.logger.info(f"Recorded behavior pattern: {pattern_name}")

    def get_behavior_patterns(self, min_success_rate: float = 0.0) -> List[Dict]:
        """Get learned behavior patterns"""
        patterns = []

        agent_uri = self.AGENT[self.agent_name]
        query = f"""
        SELECT ?pattern ?name ?description ?successRate
        WHERE {{
            ?pattern rdf:type santiago:BehaviorPattern .
            ?pattern santiago:agent <{agent_uri}> .
            ?pattern santiago:patternName ?name .
            ?pattern santiago:description ?description .
            ?pattern santiago:successRate ?successRate .
            FILTER (?successRate >= {min_success_rate})
        }}
        ORDER BY DESC(?successRate)
        """

        results = self.graph.query(query)

        for row in results:
            pattern_uri = row[0]
            # Get triggers and actions
            triggers = [str(o) for s, p, o in self.graph.triples((pattern_uri, self.SANTIAGO.trigger, None))]
            actions = [str(o) for s, p, o in self.graph.triples((pattern_uri, self.SANTIAGO.action, None))]

            patterns.append({
                "pattern_name": str(row[1]),
                "description": str(row[2]),
                "success_rate": float(row[3]),
                "triggers": triggers,
                "actions": actions
            })

        return patterns

    # Personal Experience Logging
    def record_personal_experience(self, experience_type: str, description: str,
                                 outcome: str, lessons_learned: List[str]):
        """Record a personal experience with lessons learned"""
        experience_uri = BNode()
        agent_uri = self.AGENT[self.agent_name]

        self.graph.add((experience_uri, RDF.type, self.SANTIAGO.PersonalExperience))
        self.graph.add((experience_uri, self.SANTIAGO.agent, agent_uri))
        self.graph.add((experience_uri, self.SANTIAGO.experienceType, Literal(experience_type)))
        self.graph.add((experience_uri, self.SANTIAGO.description, Literal(description)))
        self.graph.add((experience_uri, self.SANTIAGO.outcome, Literal(outcome)))
        self.graph.add((experience_uri, self.SANTIAGO.timestamp, Literal(datetime.now().isoformat(), datatype=XSD.dateTime)))

        # Record lessons learned
        for lesson in lessons_learned:
            self.graph.add((experience_uri, self.SANTIAGO.lessonLearned, Literal(lesson)))

        self.save_personal_brain()
        self.logger.info(f"Recorded personal experience: {experience_type}")

    def get_personal_experiences(self, experience_type: Optional[str] = None) -> List[Dict]:
        """Get personal experiences, optionally filtered by type"""
        experiences = []

        agent_uri = self.AGENT[self.agent_name]
        query = f"""
        SELECT ?experience ?type ?description ?outcome ?timestamp
        WHERE {{
            ?experience rdf:type santiago:PersonalExperience .
            ?experience santiago:agent <{agent_uri}> .
            ?experience santiago:experienceType ?type .
            ?experience santiago:description ?description .
            ?experience santiago:outcome ?outcome .
            ?experience santiago:timestamp ?timestamp .
        }}
        """

        if experience_type:
            query = query.replace("}", f" FILTER (?type = '{experience_type}') }}")

        query += " ORDER BY DESC(?timestamp)"

        results = self.graph.query(query)

        for row in results:
            experience_uri = row[0]
            # Get lessons learned
            lessons = [str(o) for s, p, o in self.graph.triples((experience_uri, self.SANTIAGO.lessonLearned, None))]

            experiences.append({
                "experience_type": str(row[1]),
                "description": str(row[2]),
                "outcome": str(row[3]),
                "timestamp": str(row[4]),
                "lessons_learned": lessons
            })

        return experiences

    # Personal Goal Tracking
    def set_personal_goal(self, goal_id: str, description: str, priority: str = "medium",
                         deadline: Optional[str] = None):
        """Set a personal development goal"""
        goal_uri = BNode()
        agent_uri = self.AGENT[self.agent_name]

        self.graph.add((goal_uri, RDF.type, self.SANTIAGO.PersonalGoal))
        self.graph.add((goal_uri, self.SANTIAGO.agent, agent_uri))
        self.graph.add((goal_uri, self.SANTIAGO.goalId, Literal(goal_id)))
        self.graph.add((goal_uri, self.SANTIAGO.description, Literal(description)))
        self.graph.add((goal_uri, self.SANTIAGO.priority, Literal(priority)))
        self.graph.add((goal_uri, self.SANTIAGO.status, Literal("active")))
        self.graph.add((goal_uri, self.SANTIAGO.createdTime, Literal(datetime.now().isoformat(), datatype=XSD.dateTime)))

        if deadline:
            self.graph.add((goal_uri, self.SANTIAGO.deadline, Literal(deadline, datatype=XSD.date)))

        self.save_personal_brain()
        self.logger.info(f"Set personal goal: {goal_id}")

    def update_goal_progress(self, goal_id: str, progress: float, notes: str = ""):
        """Update progress on a personal goal"""
        # Find the goal
        agent_uri = self.AGENT[self.agent_name]
        query = f"""
        SELECT ?goal
        WHERE {{
            ?goal rdf:type santiago:PersonalGoal .
            ?goal santiago:agent <{agent_uri}> .
            ?goal santiago:goalId "{goal_id}" .
        }}
        """

        results = self.graph.query(query)
        if not results:
            self.logger.warning(f"Goal not found: {goal_id}")
            return

        goal_uri = results.bindings[0]['goal']

        # Update progress
        self.graph.remove((goal_uri, self.SANTIAGO.progress, None))
        self.graph.add((goal_uri, self.SANTIAGO.progress, Literal(progress, datatype=XSD.float)))
        self.graph.add((goal_uri, self.SANTIAGO.lastUpdated, Literal(datetime.now().isoformat(), datatype=XSD.dateTime)))

        if notes:
            self.graph.add((goal_uri, self.SANTIAGO.progressNotes, Literal(notes)))

        self.save_personal_brain()
        self.logger.info(f"Updated goal progress: {goal_id} - {progress:.1%}")

    def get_personal_goals(self, status: str = "active") -> List[Dict]:
        """Get personal goals by status"""
        goals = []

        agent_uri = self.AGENT[self.agent_name]
        query = f"""
        SELECT ?goal ?id ?description ?priority ?progress ?deadline
        WHERE {{
            ?goal rdf:type santiago:PersonalGoal .
            ?goal santiago:agent <{agent_uri}> .
            ?goal santiago:goalId ?id .
            ?goal santiago:description ?description .
            ?goal santiago:priority ?priority .
            ?goal santiago:status "{status}" .
            OPTIONAL {{ ?goal santiago:progress ?progress }}
            OPTIONAL {{ ?goal santiago:deadline ?deadline }}
        }}
        ORDER BY ?priority DESC(?deadline)
        """

        results = self.graph.query(query)

        for row in results:
            goals.append({
                "goal_id": str(row[1]),
                "description": str(row[2]),
                "priority": str(row[3]),
                "progress": float(row[4]) if row[4] else 0.0,
                "deadline": str(row[5]) if row[5] else None
            })

        return goals

    # Query methods
    def sparql_query(self, query: str) -> List[Dict]:
        """Execute a SPARQL query on personal brain"""
        try:
            results = self.graph.query(query)
            return [dict(row) for row in results]
        except Exception as e:
            self.logger.error(f"SPARQL query error: {e}")
            return []

    def get_statistics(self) -> Dict:
        """Get personal brain statistics"""
        return {
            "total_triples": len(self.graph),
            "personal_knowledge": len(list(self.graph.subjects(RDF.type, self.SANTIAGO.PersonalKnowledge))),
            "behavior_patterns": len(list(self.graph.subjects(RDF.type, self.SANTIAGO.BehaviorPattern))),
            "personal_experiences": len(list(self.graph.subjects(RDF.type, self.SANTIAGO.PersonalExperience))),
            "personal_goals": len(list(self.graph.subjects(RDF.type, self.SANTIAGO.PersonalGoal))),
            "agent_name": self.agent_name
        }