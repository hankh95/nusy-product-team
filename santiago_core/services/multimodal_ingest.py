"""
Santiago Multimodal Ingest Officer (First Mate Service)

Implements the "Multimodal Ingest Officer" layer from the Santiago Fleet Memory Architecture.
This is the First Mate - responsible for ingesting voice, video, screen, PDFs, and Grok chats,
transcribing/processing them, and routing the rich summaries to appropriate memory layers.

The First Mate is always watching/listening and routes content to personal or shared memory.

Part of the layered memory system:
- Crew Member Brain: Personal agent knowledge (personal_memory.py)
- Officer's Private Logbook: Private thoughts (personal_logs.py)
- Bridge Talk: Live conversation memory (conversation_memory.py)
- Voyage Shared Memory: Collective knowledge (knowledge_graph.py)
- Captain's Intent & Orders: Mission directives (captains_memory.py)
- Multimodal Ingest Officer: This file - input processing and routing
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import json
import base64


@dataclass
class IngestedContent:
    """Processed content from multimodal input"""
    content_id: str
    source_type: str  # voice, video, screen, pdf, chat, text
    raw_content: Any  # Original content (file path, text, etc.)
    processed_content: str  # Transcribed/processed text
    metadata: Dict[str, Any]  # Source info, timestamps, etc.
    embeddings: Optional[List[float]] = None  # Optional vector representation
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class ContentRoutingDecision:
    """Decision on where to route ingested content"""
    content_id: str
    primary_destination: str  # personal_brain, shared_memory, conversation, captains_log
    secondary_destinations: List[str]  # Additional routing
    urgency: str  # immediate, high, normal, low
    requires_human_attention: bool = False
    reasoning: str = ""


class SantiagoMultimodalIngestOfficer:
    """First Mate - handles multimodal input processing and routing"""

    SUPPORTED_TYPES = {
        'voice': ['wav', 'mp3', 'm4a', 'flac'],
        'video': ['mp4', 'avi', 'mov', 'mkv'],
        'screen': ['png', 'jpg', 'jpeg', 'gif', 'mp4'],
        'pdf': ['pdf'],
        'chat': ['json', 'txt', 'md'],
        'text': ['txt', 'md', 'json']
    }

    def __init__(self, workspace_path: Path):
        self.workspace_path = workspace_path
        self.logger = logging.getLogger("santiago-first-mate")

        # Processing queues
        self.ingest_queue: List[IngestedContent] = []
        self.routing_queue: List[Tuple[IngestedContent, ContentRoutingDecision]] = []

        # Ingest storage
        self.ingest_dir = workspace_path / "multimodal_ingest"
        self.ingest_dir.mkdir(parents=True, exist_ok=True)

        # Load any pending ingests
        self._load_pending_ingests()

    def _load_pending_ingests(self):
        """Load any pending ingests from disk"""
        pending_file = self.ingest_dir / "pending_ingests.json"
        if pending_file.exists():
            try:
                with open(pending_file, 'r') as f:
                    data = json.load(f)

                for item in data.get('pending', []):
                    content = IngestedContent(
                        content_id=item['content_id'],
                        source_type=item['source_type'],
                        raw_content=item['raw_content'],
                        processed_content=item['processed_content'],
                        metadata=item['metadata'],
                        timestamp=datetime.fromisoformat(item['timestamp'])
                    )
                    self.ingest_queue.append(content)

                self.logger.info(f"Loaded {len(self.ingest_queue)} pending ingests")

            except Exception as e:
                self.logger.error(f"Error loading pending ingests: {e}")

    def _save_pending_ingests(self):
        """Save pending ingests to disk"""
        data = {
            'pending': [
                {
                    'content_id': item.content_id,
                    'source_type': item.source_type,
                    'raw_content': item.raw_content,
                    'processed_content': item.processed_content,
                    'metadata': item.metadata,
                    'timestamp': item.timestamp.isoformat()
                }
                for item in self.ingest_queue
            ],
            'last_updated': datetime.now().isoformat()
        }

        pending_file = self.ingest_dir / "pending_ingests.json"
        try:
            with open(pending_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving pending ingests: {e}")

    def ingest_content(self, source_type: str, content: Any, metadata: Dict[str, Any] = None) -> str:
        """Ingest multimodal content and queue for processing"""
        content_id = f"{source_type}_{datetime.now().timestamp()}_{hash(str(content))}"

        ingested = IngestedContent(
            content_id=content_id,
            source_type=source_type,
            raw_content=content,
            processed_content="",  # Will be filled by processing
            metadata=metadata or {}
        )

        self.ingest_queue.append(ingested)
        self._save_pending_ingests()

        self.logger.info(f"Ingested {source_type} content: {content_id}")
        return content_id

    def process_ingest_queue(self) -> int:
        """Process all items in the ingest queue"""
        processed_count = 0

        while self.ingest_queue:
            content = self.ingest_queue.pop(0)

            try:
                # Process based on type
                processed_content = self._process_content(content)

                if processed_content:
                    content.processed_content = processed_content

                    # Make routing decision
                    routing_decision = self._decide_routing(content)

                    # Queue for routing
                    self.routing_queue.append((content, routing_decision))

                    processed_count += 1
                    self.logger.info(f"Processed content: {content.content_id}")

                else:
                    self.logger.warning(f"Failed to process content: {content.content_id}")

            except Exception as e:
                self.logger.error(f"Error processing content {content.content_id}: {e}")

        self._save_pending_ingests()
        return processed_count

    def _process_content(self, content: IngestedContent) -> Optional[str]:
        """Process content based on its type"""
        if content.source_type == 'text':
            return self._process_text(content)
        elif content.source_type == 'pdf':
            return self._process_pdf(content)
        elif content.source_type == 'voice':
            return self._process_voice(content)
        elif content.source_type == 'video':
            return self._process_video(content)
        elif content.source_type == 'screen':
            return self._process_screen(content)
        elif content.source_type == 'chat':
            return self._process_chat(content)
        else:
            self.logger.warning(f"Unsupported content type: {content.source_type}")
            return None

    def _process_text(self, content: IngestedContent) -> str:
        """Process text content (usually already text)"""
        if isinstance(content.raw_content, str):
            return content.raw_content
        elif isinstance(content.raw_content, Path):
            try:
                with open(content.raw_content, 'r') as f:
                    return f.read()
            except Exception as e:
                self.logger.error(f"Error reading text file: {e}")
                return ""
        else:
            return str(content.raw_content)

    def _process_pdf(self, content: IngestedContent) -> str:
        """Extract text from PDF"""
        # Placeholder - would use PyPDF2 or similar
        if isinstance(content.raw_content, Path):
            try:
                # Simulate PDF processing
                return f"[PDF Content from {content.raw_content.name}] Extracted text would go here."
            except Exception as e:
                self.logger.error(f"Error processing PDF: {e}")
                return ""
        return ""

    def _process_voice(self, content: IngestedContent) -> str:
        """Transcribe voice audio"""
        # Placeholder - would use Whisper or similar
        if isinstance(content.raw_content, Path):
            try:
                # Simulate voice transcription
                return f"[Voice Transcript from {content.raw_content.name}] Transcribed speech would go here."
            except Exception as e:
                self.logger.error(f"Error transcribing voice: {e}")
                return ""
        return ""

    def _process_video(self, content: IngestedContent) -> str:
        """Process video (extract audio and transcribe, plus visual summary)"""
        # Placeholder - would combine video processing with voice transcription
        if isinstance(content.raw_content, Path):
            try:
                # Simulate video processing
                return f"[Video Content from {content.raw_content.name}] Audio transcript and visual summary would go here."
            except Exception as e:
                self.logger.error(f"Error processing video: {e}")
                return ""
        return ""

    def _process_screen(self, content: IngestedContent) -> str:
        """Process screen capture (OCR + context)"""
        # Placeholder - would use OCR and screen understanding
        if isinstance(content.raw_content, Path):
            try:
                # Simulate screen processing
                return f"[Screen Content from {content.raw_content.name}] OCR text and screen context would go here."
            except Exception as e:
                self.logger.error(f"Error processing screen: {e}")
                return ""
        return ""

    def _process_chat(self, content: IngestedContent) -> str:
        """Process chat logs (Grok chats, etc.)"""
        if isinstance(content.raw_content, str):
            return content.raw_content
        elif isinstance(content.raw_content, Path):
            try:
                with open(content.raw_content, 'r') as f:
                    if content.raw_content.suffix == '.json':
                        data = json.load(f)
                        # Extract conversation text
                        return json.dumps(data, indent=2)
                    else:
                        return f.read()
            except Exception as e:
                self.logger.error(f"Error processing chat: {e}")
                return ""
        return ""

    def _decide_routing(self, content: IngestedContent) -> ContentRoutingDecision:
        """Decide where to route the processed content"""
        decision = ContentRoutingDecision(
            content_id=content.content_id,
            primary_destination="shared_memory",  # Default
            secondary_destinations=[],
            urgency="normal",
            requires_human_attention=False,
            reasoning="Default routing to shared memory"
        )

        # Analyze content for routing decisions
        processed_text = content.processed_content.lower()

        # Check for personal/private content
        if any(keyword in processed_text for keyword in ['private', 'personal', 'confidential', 'my notes']):
            decision.primary_destination = "personal_brain"
            decision.reasoning = "Content appears to be personal/private"

        # Check for urgent/important content
        elif any(keyword in processed_text for keyword in ['urgent', 'critical', 'emergency', 'asap']):
            decision.urgency = "high"
            decision.requires_human_attention = True
            decision.reasoning = "Content flagged as urgent"

        # Check for captain-level decisions
        elif any(keyword in processed_text for keyword in ['mission', 'strategy', 'captain', 'leadership']):
            decision.primary_destination = "captains_log"
            decision.secondary_destinations = ["shared_memory"]
            decision.reasoning = "Strategic/mission content for captain"

        # Check for conversation content
        elif content.source_type == 'chat' or 'conversation' in processed_text:
            decision.primary_destination = "conversation"
            decision.secondary_destinations = ["shared_memory"]
            decision.reasoning = "Chat/conversation content"

        # Check for learning/research content
        elif any(keyword in processed_text for keyword in ['research', 'study', 'analysis', 'findings']):
            decision.secondary_destinations = ["personal_brain"]
            decision.reasoning = "Research content with personal learning value"

        return decision

    def route_content(self) -> int:
        """Route processed content to appropriate memory layers"""
        routed_count = 0

        while self.routing_queue:
            content, decision = self.routing_queue.pop(0)

            try:
                # Route to primary destination
                self._route_to_destination(content, decision.primary_destination, decision)

                # Route to secondary destinations
                for secondary_dest in decision.secondary_destinations:
                    self._route_to_destination(content, secondary_dest, decision)

                # Handle human attention if needed
                if decision.requires_human_attention:
                    self._notify_human_attention(content, decision)

                routed_count += 1
                self.logger.info(f"Routed content {content.content_id} to {decision.primary_destination}")

            except Exception as e:
                self.logger.error(f"Error routing content {content.content_id}: {e}")

        return routed_count

    def _route_to_destination(self, content: IngestedContent, destination: str, decision: ContentRoutingDecision):
        """Route content to a specific memory destination"""
        # This would integrate with the actual memory services
        # For now, just log the routing

        routing_record = {
            'content_id': content.content_id,
            'destination': destination,
            'processed_content': content.processed_content,
            'metadata': content.metadata,
            'routing_decision': {
                'urgency': decision.urgency,
                'reasoning': decision.reasoning,
                'requires_human_attention': decision.requires_human_attention
            },
            'timestamp': datetime.now().isoformat()
        }

        # Save routing record
        routing_file = self.ingest_dir / f"routing_{content.content_id}.json"
        try:
            with open(routing_file, 'w') as f:
                json.dump(routing_record, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving routing record: {e}")

    def _notify_human_attention(self, content: IngestedContent, decision: ContentRoutingDecision):
        """Notify human (captain) of content requiring attention"""
        # This would integrate with notification system
        # For now, create a notification file

        notification = {
            'type': 'human_attention_required',
            'content_id': content.content_id,
            'urgency': decision.urgency,
            'reasoning': decision.reasoning,
            'preview': content.processed_content[:200] + "..." if len(content.processed_content) > 200 else content.processed_content,
            'timestamp': datetime.now().isoformat()
        }

        notification_file = self.workspace_path / "captains_attention" / f"attention_{content.content_id}.json"
        notification_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(notification_file, 'w') as f:
                json.dump(notification, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error creating human attention notification: {e}")

    def get_ingest_statistics(self) -> Dict:
        """Get statistics about ingested content"""
        total_ingested = len(self.ingest_queue) + len(self.routing_queue)

        type_counts = {}
        for content in self.ingest_queue:
            type_counts[content.source_type] = type_counts.get(content.source_type, 0) + 1

        for content, _ in self.routing_queue:
            type_counts[content.source_type] = type_counts.get(content.source_type, 0) + 1

        return {
            "total_pending": total_ingested,
            "in_ingest_queue": len(self.ingest_queue),
            "in_routing_queue": len(self.routing_queue),
            "by_type": type_counts
        }

    def cleanup_old_content(self, days_old: int = 30) -> int:
        """Clean up old ingested content files"""
        import os
        from datetime import timedelta

        cutoff_date = datetime.now() - timedelta(days=days_old)
        cleaned_count = 0

        # Clean up old routing files
        for routing_file in self.ingest_dir.glob("routing_*.json"):
            try:
                # Check file modification time
                if datetime.fromtimestamp(routing_file.stat().st_mtime) < cutoff_date:
                    routing_file.unlink()
                    cleaned_count += 1
            except Exception as e:
                self.logger.error(f"Error cleaning up {routing_file}: {e}")

        if cleaned_count > 0:
            self.logger.info(f"Cleaned up {cleaned_count} old ingest files")

        return cleaned_count