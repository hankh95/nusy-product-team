"""
Santiago Memory Coordinator

Orchestrates the layered memory architecture for Santiago-core.
Manages the flow between different memory layers and ensures proper data routing.

Memory Layers:
- Crew Member Brain: Personal agent knowledge
- Officer's Private Logbook: Private thoughts
- Bridge Talk: Live conversation memory
- Voyage Shared Memory: Collective project knowledge
- Captain's Intent & Orders: Mission directives
- Multimodal Ingest Officer: Input processing and routing
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from .personal_memory import SantiagoCrewMemberBrain
from .conversation_memory import SantiagoBridgeTalkMemory
from .knowledge_graph import SantiagoKnowledgeGraph
from .multimodal_ingest import SantiagoMultimodalIngestOfficer


class SantiagoMemoryCoordinator:
    """Coordinates all memory layers for Santiago agents"""

    def __init__(self, workspace_path: Path, voyage_id: str = "default_voyage"):
        self.workspace_path = workspace_path
        self.voyage_id = voyage_id
        self.logger = logging.getLogger("santiago-memory-coordinator")

        # Initialize memory layers
        self.shared_memory = SantiagoKnowledgeGraph(voyage_id, workspace_path)
        self.conversation_memory = SantiagoBridgeTalkMemory(workspace_path)
        self.multimodal_ingest = SantiagoMultimodalIngestOfficer(workspace_path)

        # Agent-specific memory layers (lazy-loaded)
        self.agent_brains: Dict[str, SantiagoCrewMemberBrain] = {}

        self.logger.info("Santiago Memory Coordinator initialized")

    def get_agent_brain(self, agent_name: str) -> SantiagoCrewMemberBrain:
        """Get or create personal brain for an agent"""
        if agent_name not in self.agent_brains:
            self.agent_brains[agent_name] = SantiagoCrewMemberBrain(agent_name, self.workspace_path)
        return self.agent_brains[agent_name]

    # Data Flow Methods (following the memory architecture)

    def process_human_input(self, input_type: str, content: Any, metadata: Dict[str, Any] = None) -> str:
        """Process human input through multimodal ingest officer"""
        content_id = self.multimodal_ingest.ingest_content(input_type, content, metadata)

        # Process the ingest queue
        processed_count = self.multimodal_ingest.process_ingest_queue()

        # Route the processed content
        routed_count = self.multimodal_ingest.route_content()

        self.logger.info(f"Processed human input: {content_id} ({processed_count} processed, {routed_count} routed)")
        return content_id

    def start_conversation(self, conversation_id: str, participants: List[str], topic: str = "") -> bool:
        """Start a new conversation in bridge talk memory"""
        return self.conversation_memory.start_conversation(conversation_id, participants, topic)

    def add_conversation_message(self, conversation_id: str, sender: str, content: str,
                                message_type: str = "text", metadata: Dict[str, Any] = None) -> bool:
        """Add message to active conversation"""
        return self.conversation_memory.add_message(conversation_id, sender, content, message_type, metadata)

    def archive_conversation(self, conversation_id: str) -> bool:
        """Archive conversation and move summary to shared memory"""
        # Generate summary
        summary = self.conversation_memory.generate_conversation_summary(conversation_id)
        if not summary:
            return False

        # Archive the conversation
        archived = self.conversation_memory.archive_conversation(conversation_id, summary)
        if not archived:
            return False

        # Add key insights to shared memory
        if summary.key_decisions:
            self.shared_memory.record_collective_decision(
                decision_id=f"conv_{conversation_id}_decisions",
                title=f"Decisions from conversation: {summary.topic}",
                description=f"Key decisions from conversation {conversation_id}",
                participants=list(summary.participants),
                outcome="Decisions recorded",
                rationale=f"From conversation summary: {summary.summary_text}"
            )

        if summary.action_items:
            self.shared_memory.record_shared_task(
                task_id=f"conv_{conversation_id}_actions",
                title=f"Action items from conversation: {summary.topic}",
                description=f"Follow-up actions from conversation {conversation_id}",
                assigned_crew=list(summary.participants),
                priority="normal"
            )

        self.logger.info(f"Archived conversation {conversation_id} to shared memory")
        return True

    def record_personal_learning(self, agent_name: str, concept: str, knowledge: str,
                               confidence: float = 1.0, source: str = "experience"):
        """Record personal knowledge in agent's brain"""
        agent_brain = self.get_agent_brain(agent_name)
        agent_brain.record_personal_knowledge(concept, knowledge, confidence, source)

    def record_shared_learning(self, concept: str, experience: str, outcome: str,
                             contributors: List[str]):
        """Record learning in shared voyage memory"""
        learning_id = f"shared_{datetime.now().timestamp()}"
        self.shared_memory.record_shared_learning(learning_id, concept, experience, outcome, contributors)

    def record_personal_experience(self, agent_name: str, experience_type: str, description: str,
                                 outcome: str, lessons_learned: List[str]):
        """Record personal experience with lessons"""
        agent_brain = self.get_agent_brain(agent_name)
        agent_brain.record_personal_experience(experience_type, description, outcome, lessons_learned)

    def set_personal_goal(self, agent_name: str, goal_id: str, description: str,
                         priority: str = "medium", deadline: Optional[str] = None):
        """Set personal development goal"""
        agent_brain = self.get_agent_brain(agent_name)
        agent_brain.set_personal_goal(goal_id, description, priority, deadline)

    def update_goal_progress(self, agent_name: str, goal_id: str, progress: float, notes: str = ""):
        """Update progress on personal goal"""
        agent_brain = self.get_agent_brain(agent_name)
        agent_brain.update_goal_progress(goal_id, progress, notes)

    # Query Methods

    def get_conversation_context(self, conversation_id: str, max_messages: int = 10) -> Dict[str, Any]:
        """Get conversation context for continuity"""
        return self.conversation_memory.get_conversation_context(conversation_id, max_messages)

    def get_personal_knowledge(self, agent_name: str, concept: Optional[str] = None,
                             limit: int = 10) -> List[Dict]:
        """Retrieve personal knowledge"""
        agent_brain = self.get_agent_brain(agent_name)
        return agent_brain.get_personal_knowledge(concept, limit)

    def get_shared_knowledge(self, concept: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """Retrieve shared voyage knowledge"""
        return self.shared_memory.get_shared_learnings(concept, limit)

    def get_voyage_status(self) -> Dict:
        """Get current voyage status"""
        return self.shared_memory.get_voyage_status()

    def get_personal_goals(self, agent_name: str, status: str = "active") -> List[Dict]:
        """Get personal goals for an agent"""
        agent_brain = self.get_agent_brain(agent_name)
        return agent_brain.get_personal_goals(status)

    def get_behavior_patterns(self, agent_name: str, min_success_rate: float = 0.0) -> List[Dict]:
        """Get learned behavior patterns"""
        agent_brain = self.get_agent_brain(agent_name)
        return agent_brain.get_behavior_patterns(min_success_rate)

    # Maintenance Methods

    def cleanup_old_data(self) -> Dict[str, int]:
        """Clean up old data across all memory layers"""
        results = {}

        # Clean up old conversations
        results['old_conversations'] = self.conversation_memory.cleanup_old_conversations()

        # Clean up old ingest files
        results['old_ingest_files'] = self.multimodal_ingest.cleanup_old_content()

        self.logger.info(f"Memory cleanup completed: {results}")
        return results

    def get_memory_statistics(self) -> Dict[str, Any]:
        """Get comprehensive memory statistics"""
        stats = {
            "voyage_id": self.voyage_id,
            "shared_memory": self.shared_memory.get_statistics(),
            "conversation_memory": self.conversation_memory.get_statistics(),
            "multimodal_ingest": self.multimodal_ingest.get_ingest_statistics(),
            "agent_brains": {}
        }

        # Add stats for each agent brain
        for agent_name, brain in self.agent_brains.items():
            stats["agent_brains"][agent_name] = brain.get_statistics()

        return stats

    # Integration Methods

    def save_all_memories(self):
        """Save all memory layers to persistent storage"""
        self.shared_memory.save_shared_memory()

        for agent_name, brain in self.agent_brains.items():
            brain.save_personal_brain()

        self.logger.info("All memories saved to persistent storage")

    def load_all_memories(self):
        """Load all memory layers from persistent storage"""
        # Shared memory loads automatically on init
        # Agent brains load lazily when accessed
        # Conversation memory loads on init

        self.logger.info("All memories loaded from persistent storage")

    # Search Methods

    def search_memories(self, query: str, agent_name: Optional[str] = None,
                       memory_types: List[str] = None) -> Dict[str, List]:
        """
        Search across memory layers

        Args:
            query: Search term
            agent_name: Optional agent to search personal memory
            memory_types: List of memory types to search ['personal', 'shared', 'conversations']
        """
        if memory_types is None:
            memory_types = ['personal', 'shared', 'conversations']

        results = {}

        # Search personal memory
        if 'personal' in memory_types and agent_name:
            agent_brain = self.get_agent_brain(agent_name)
            # Simple text search in personal knowledge
            personal_knowledge = agent_brain.get_personal_knowledge(limit=100)
            matching_knowledge = [
                k for k in personal_knowledge
                if query.lower() in k['knowledge'].lower()
            ]
            results['personal'] = matching_knowledge

        # Search shared memory
        if 'shared' in memory_types:
            shared_learnings = self.shared_memory.get_shared_learnings(limit=100)
            matching_shared = [
                l for l in shared_learnings
                if query.lower() in l['experience'].lower() or query.lower() in l['outcome'].lower()
            ]
            results['shared'] = matching_shared

        # Search conversations
        if 'conversations' in memory_types:
            conv_results = self.conversation_memory.search_conversations(keyword=query)
            results['conversations'] = conv_results

        return results