"""
Santiago Bridge Talk (Conversation Memory Service)

Implements the "Bridge Talk" layer from the Santiago Fleet Memory Architecture.
This handles live conversation memory - the transcript and summary of current
conversations only, staying private to participants until explicitly committed.

Conversations are stored temporarily and archived to shared memory when complete.

Part of the layered memory system:
- Crew Member Brain: Personal agent knowledge (personal_memory.py)
- Officer's Private Logbook: Private thoughts (personal_logs.py)
- Bridge Talk: This file - live conversation memory
- Voyage Shared Memory: Collective knowledge (knowledge_graph.py)
- Captain's Intent & Orders: Mission directives (captains_memory.py)
- Multimodal Ingest Officer: Input processing (multimodal_ingest.py)
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, field
import hashlib


@dataclass
class ConversationMessage:
    """A single message in a conversation"""
    message_id: str
    sender: str
    content: str
    timestamp: datetime
    message_type: str = "text"  # text, action, system
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConversationSummary:
    """Summary of a conversation for archival"""
    conversation_id: str
    participants: Set[str]
    start_time: datetime
    end_time: datetime
    topic: str
    key_decisions: List[str]
    action_items: List[str]
    summary_text: str
    sentiment: str = "neutral"  # positive, negative, neutral
    archived: bool = False


class SantiagoBridgeTalkMemory:
    """Manages live conversation memory for Santiago agents"""

    def __init__(self, workspace_path: Path, max_conversation_age_hours: int = 24):
        self.workspace_path = workspace_path
        self.max_age = timedelta(hours=max_conversation_age_hours)
        self.logger = logging.getLogger("santiago-bridge-talk")

        # Active conversations: conversation_id -> list of messages
        self.active_conversations: Dict[str, List[ConversationMessage]] = {}

        # Conversation summaries: conversation_id -> summary
        self.conversation_summaries: Dict[str, ConversationSummary] = {}

        # Conversation storage directory
        self.conversations_dir = workspace_path / "conversations"
        self.conversations_dir.mkdir(parents=True, exist_ok=True)

        # Load existing conversations
        self._load_active_conversations()

    def _load_active_conversations(self):
        """Load active conversations from disk"""
        for conv_file in self.conversations_dir.glob("active_*.json"):
            try:
                with open(conv_file, 'r') as f:
                    data = json.load(f)

                conv_id = data['conversation_id']
                messages = []
                for msg_data in data['messages']:
                    msg = ConversationMessage(
                        message_id=msg_data['message_id'],
                        sender=msg_data['sender'],
                        content=msg_data['content'],
                        timestamp=datetime.fromisoformat(msg_data['timestamp']),
                        message_type=msg_data.get('message_type', 'text'),
                        metadata=msg_data.get('metadata', {})
                    )
                    messages.append(msg)

                self.active_conversations[conv_id] = messages
                self.logger.info(f"Loaded active conversation: {conv_id}")

            except Exception as e:
                self.logger.error(f"Error loading conversation {conv_file}: {e}")

    def _save_conversation(self, conversation_id: str):
        """Save a conversation to disk"""
        if conversation_id not in self.active_conversations:
            return

        messages = self.active_conversations[conversation_id]
        data = {
            'conversation_id': conversation_id,
            'messages': [
                {
                    'message_id': msg.message_id,
                    'sender': msg.sender,
                    'content': msg.content,
                    'timestamp': msg.timestamp.isoformat(),
                    'message_type': msg.message_type,
                    'metadata': msg.metadata
                }
                for msg in messages
            ],
            'last_updated': datetime.now().isoformat()
        }

        conv_file = self.conversations_dir / f"active_{conversation_id}.json"
        try:
            with open(conv_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving conversation {conversation_id}: {e}")

    def start_conversation(self, conversation_id: str, participants: List[str],
                          initial_topic: str = "") -> bool:
        """Start a new conversation"""
        if conversation_id in self.active_conversations:
            self.logger.warning(f"Conversation {conversation_id} already exists")
            return False

        self.active_conversations[conversation_id] = []

        # Add system message
        system_msg = ConversationMessage(
            message_id=f"system_{conversation_id}_{datetime.now().timestamp()}",
            sender="system",
            content=f"Conversation started. Topic: {initial_topic}",
            timestamp=datetime.now(),
            message_type="system",
            metadata={"participants": participants, "topic": initial_topic}
        )

        self.active_conversations[conversation_id].append(system_msg)
        self._save_conversation(conversation_id)

        self.logger.info(f"Started conversation: {conversation_id} with participants: {participants}")
        return True

    def add_message(self, conversation_id: str, sender: str, content: str,
                   message_type: str = "text", metadata: Dict[str, Any] = None) -> bool:
        """Add a message to an active conversation"""
        if conversation_id not in self.active_conversations:
            self.logger.warning(f"Conversation {conversation_id} not found")
            return False

        message_id = f"{sender}_{conversation_id}_{datetime.now().timestamp()}"
        message = ConversationMessage(
            message_id=message_id,
            sender=sender,
            content=content,
            timestamp=datetime.now(),
            message_type=message_type,
            metadata=metadata or {}
        )

        self.active_conversations[conversation_id].append(message)
        self._save_conversation(conversation_id)

        self.logger.debug(f"Added message to {conversation_id} from {sender}")
        return True

    def get_conversation_history(self, conversation_id: str, participant: str = None) -> List[Dict]:
        """Get conversation history, filtered by participant if specified"""
        if conversation_id not in self.active_conversations:
            return []

        messages = self.active_conversations[conversation_id]

        # Filter by participant if specified
        if participant:
            messages = [msg for msg in messages if msg.sender == participant or msg.sender == "system"]

        return [
            {
                "message_id": msg.message_id,
                "sender": msg.sender,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat(),
                "message_type": msg.message_type,
                "metadata": msg.metadata
            }
            for msg in messages
        ]

    def get_active_conversations_for_participant(self, participant: str) -> List[str]:
        """Get all active conversation IDs where participant is involved"""
        active_convs = []

        for conv_id, messages in self.active_conversations.items():
            participants = set()
            for msg in messages:
                if msg.sender != "system":
                    participants.add(msg.sender)
                elif "participants" in msg.metadata:
                    participants.update(msg.metadata["participants"])

            if participant in participants:
                active_convs.append(conv_id)

        return active_convs

    def generate_conversation_summary(self, conversation_id: str) -> Optional[ConversationSummary]:
        """Generate a summary of the conversation for archival"""
        if conversation_id not in self.active_conversations:
            return None

        messages = self.active_conversations[conversation_id]

        if not messages:
            return None

        # Extract participants
        participants = set()
        start_time = messages[0].timestamp
        end_time = messages[-1].timestamp

        for msg in messages:
            if msg.sender != "system":
                participants.add(msg.sender)
            elif "participants" in msg.metadata:
                participants.update(msg.metadata["participants"])

        # Extract topic from first system message
        topic = ""
        for msg in messages:
            if msg.message_type == "system" and "topic" in msg.metadata:
                topic = msg.metadata["topic"]
                break

        # Simple summary generation (in practice, use LLM)
        total_messages = len([m for m in messages if m.message_type != "system"])
        summary_text = f"Conversation with {len(participants)} participants, {total_messages} messages"

        # Placeholder for key decisions and action items (would need NLP)
        key_decisions = []
        action_items = []

        summary = ConversationSummary(
            conversation_id=conversation_id,
            participants=participants,
            start_time=start_time,
            end_time=end_time,
            topic=topic,
            key_decisions=key_decisions,
            action_items=action_items,
            summary_text=summary_text
        )

        self.conversation_summaries[conversation_id] = summary
        return summary

    def archive_conversation(self, conversation_id: str, summary: ConversationSummary = None) -> bool:
        """Archive a conversation to shared memory and clean up active storage"""
        if conversation_id not in self.active_conversations:
            return False

        # Generate summary if not provided
        if not summary:
            summary = self.generate_conversation_summary(conversation_id)

        if summary:
            summary.archived = True

            # Save summary to archive
            archive_file = self.conversations_dir / f"archived_{conversation_id}.json"
            archive_data = {
                'conversation_id': summary.conversation_id,
                'participants': list(summary.participants),
                'start_time': summary.start_time.isoformat(),
                'end_time': summary.end_time.isoformat(),
                'topic': summary.topic,
                'key_decisions': summary.key_decisions,
                'action_items': summary.action_items,
                'summary_text': summary.summary_text,
                'sentiment': summary.sentiment,
                'archived_at': datetime.now().isoformat(),
                'message_count': len(self.active_conversations[conversation_id])
            }

            try:
                with open(archive_file, 'w') as f:
                    json.dump(archive_data, f, indent=2)
            except Exception as e:
                self.logger.error(f"Error archiving conversation {conversation_id}: {e}")
                return False

        # Remove from active conversations
        del self.active_conversations[conversation_id]

        # Remove active file
        active_file = self.conversations_dir / f"active_{conversation_id}.json"
        if active_file.exists():
            active_file.unlink()

        self.logger.info(f"Archived conversation: {conversation_id}")
        return True

    def cleanup_old_conversations(self) -> int:
        """Clean up conversations older than max_age"""
        cutoff_time = datetime.now() - self.max_age
        cleaned_count = 0

        conversations_to_remove = []

        for conv_id, messages in self.active_conversations.items():
            if messages and messages[-1].timestamp < cutoff_time:
                # Auto-archive old conversations
                self.archive_conversation(conv_id)
                conversations_to_remove.append(conv_id)
                cleaned_count += 1

        # Remove from memory
        for conv_id in conversations_to_remove:
            if conv_id in self.active_conversations:
                del self.active_conversations[conv_id]

        if cleaned_count > 0:
            self.logger.info(f"Cleaned up {cleaned_count} old conversations")

        return cleaned_count

    def get_conversation_context(self, conversation_id: str, max_messages: int = 10) -> Dict[str, Any]:
        """Get conversation context for an agent to maintain continuity"""
        if conversation_id not in self.active_conversations:
            return {"error": "Conversation not found"}

        messages = self.active_conversations[conversation_id]
        recent_messages = messages[-max_messages:] if len(messages) > max_messages else messages

        participants = set()
        for msg in messages:
            if msg.sender != "system":
                participants.add(msg.sender)

        return {
            "conversation_id": conversation_id,
            "participants": list(participants),
            "message_count": len(messages),
            "recent_messages": [
                {
                    "sender": msg.sender,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat(),
                    "type": msg.message_type
                }
                for msg in recent_messages
            ],
            "last_activity": messages[-1].timestamp.isoformat() if messages else None
        }

    def search_conversations(self, participant: str = None, keyword: str = None,
                           since: Optional[datetime] = None) -> List[Dict]:
        """Search through active conversations"""
        results = []

        for conv_id, messages in self.active_conversations.items():
            matches = True

            # Filter by participant
            if participant:
                conv_participants = set()
                for msg in messages:
                    if msg.sender != "system":
                        conv_participants.add(msg.sender)
                if participant not in conv_participants:
                    matches = False

            # Filter by keyword
            if keyword and matches:
                found = False
                for msg in messages:
                    if keyword.lower() in msg.content.lower():
                        found = True
                        break
                if not found:
                    matches = False

            # Filter by time
            if since and matches:
                if not messages or messages[-1].timestamp < since:
                    matches = False

            if matches:
                results.append({
                    "conversation_id": conv_id,
                    "participant_count": len(set(msg.sender for msg in messages if msg.sender != "system")),
                    "message_count": len(messages),
                    "last_activity": messages[-1].timestamp.isoformat() if messages else None
                })

        return results

    def get_statistics(self) -> Dict:
        """Get conversation memory statistics"""
        total_messages = sum(len(messages) for messages in self.active_conversations.values())
        total_conversations = len(self.active_conversations)
        archived_conversations = len(list(self.conversations_dir.glob("archived_*.json")))

        return {
            "active_conversations": total_conversations,
            "total_messages": total_messages,
            "archived_conversations": archived_conversations,
            "max_age_hours": self.max_age.total_seconds() / 3600
        }