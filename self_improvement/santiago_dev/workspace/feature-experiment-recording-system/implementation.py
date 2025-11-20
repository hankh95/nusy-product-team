#!/usr/bin/env python3
"""
Experiment Recording System - Complete Session Capture for Learning

This system captures complete chat sessions, file states, and time-based changes
to enable pattern analysis and learning optimization for autonomous development.
"""

import os
import json
import hashlib
import tempfile
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, asdict, field
from enum import Enum
import yaml
import re

from pydantic import BaseModel, Field


class InteractionType(Enum):
    """Types of interactions that can be recorded"""
    CHAT_MESSAGE = "chat_message"
    FILE_EDIT = "file_edit"
    COMMAND_EXECUTION = "command_execution"
    DECISION_POINT = "decision_point"
    ERROR_EVENT = "error_event"
    SUCCESS_EVENT = "success_event"


class PrivacyLevel(Enum):
    """Privacy classification levels for recorded data"""
    PUBLIC = "public"
    INTERNAL = "internal"
    SENSITIVE = "sensitive"
    RESTRICTED = "restricted"


@dataclass
class Interaction:
    """Individual interaction within an experiment session"""
    timestamp: datetime
    interaction_type: InteractionType
    actor: str  # "user", "agent", "system"
    content: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)
    privacy_level: PrivacyLevel = PrivacyLevel.INTERNAL


@dataclass
class FileState:
    """Snapshot of file state at a point in time"""
    file_path: str
    timestamp: datetime
    content_hash: str
    size_bytes: int
    line_count: int = 0
    modification_type: str = "unknown"  # "created", "modified", "deleted"


@dataclass
class ExperimentSession:
    """Complete experiment session with all interactions and states"""
    session_id: str
    experiment_name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status: str = "active"  # "active", "completed", "failed", "cancelled"
    goal: str = ""
    tags: List[str] = field(default_factory=list)
    interactions: List[Interaction] = field(default_factory=list)
    file_states: List[FileState] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    privacy_classification: PrivacyLevel = PrivacyLevel.INTERNAL


@dataclass
class PatternAnalysis:
    """Analysis results from pattern recognition"""
    pattern_id: str
    pattern_type: str  # "success_sequence", "failure_pattern", "efficiency_optimization"
    confidence_score: float
    description: str
    occurrences: List[str]  # Session IDs where pattern was found
    recommendations: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)


class ExperimentRecordingService:
    """
    Comprehensive experiment recording system for capturing and analyzing
    complete development sessions to enable learning and optimization.
    """

    def __init__(self, storage_path: str = ".experiment_records", auto_init: bool = True):
        """
        Initialize the experiment recording service.

        Args:
            storage_path: Path to store experiment records
            auto_init: Automatically create storage directory if needed
        """
        self.storage_path = Path(storage_path)
        self.active_sessions: Dict[str, ExperimentSession] = {}
        self.patterns: Dict[str, PatternAnalysis] = {}

        if auto_init and not self.storage_path.exists():
            self.storage_path.mkdir(parents=True, exist_ok=True)

        self._load_existing_sessions()
        self._load_patterns()

    def _load_existing_sessions(self):
        """Load existing experiment sessions from storage"""
        sessions_file = self.storage_path / "sessions.json"
        if sessions_file.exists():
            try:
                with open(sessions_file, 'r') as f:
                    data = json.load(f)
                    for session_data in data.values():
                        # Convert timestamps
                        session_data['start_time'] = datetime.fromisoformat(session_data['start_time'])
                        if session_data.get('end_time'):
                            session_data['end_time'] = datetime.fromisoformat(session_data['end_time'])

                        # Convert interactions
                        for interaction in session_data.get('interactions', []):
                            interaction['timestamp'] = datetime.fromisoformat(interaction['timestamp'])
                            interaction['interaction_type'] = InteractionType(interaction['interaction_type'])
                            interaction['privacy_level'] = PrivacyLevel(interaction['privacy_level'])

                        # Convert file states
                        for file_state in session_data.get('file_states', []):
                            file_state['timestamp'] = datetime.fromisoformat(file_state['timestamp'])

                        session = ExperimentSession(**session_data)
                        if session.status == "active":
                            self.active_sessions[session.session_id] = session
            except Exception as e:
                print(f"Warning: Could not load existing sessions: {e}")

    def _load_patterns(self):
        """Load existing pattern analysis results"""
        patterns_file = self.storage_path / "patterns.json"
        if patterns_file.exists():
            try:
                with open(patterns_file, 'r') as f:
                    data = json.load(f)
                    for pattern_data in data.values():
                        pattern = PatternAnalysis(**pattern_data)
                        self.patterns[pattern.pattern_id] = pattern
            except Exception as e:
                print(f"Warning: Could not load patterns: {e}")

    def _save_sessions(self):
        """Save all sessions to storage"""
        sessions_file = self.storage_path / "sessions.json"
        try:
            # Convert datetime objects for JSON serialization
            data = {}
            for session_id, session in self.active_sessions.items():
                session_dict = asdict(session)
                session_dict['start_time'] = session.start_time.isoformat()
                if session.end_time:
                    session_dict['end_time'] = session.end_time.isoformat()

                # Convert session-level enums
                session_dict['privacy_classification'] = session_dict['privacy_classification'].value

                # Convert interactions
                for interaction in session_dict.get('interactions', []):
                    interaction['timestamp'] = interaction['timestamp'].isoformat()
                    interaction['interaction_type'] = interaction['interaction_type'].value
                    interaction['privacy_level'] = interaction['privacy_level'].value

                # Convert file states
                for file_state in session_dict.get('file_states', []):
                    file_state['timestamp'] = file_state['timestamp'].isoformat()

                data[session_id] = session_dict

            with open(sessions_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save sessions: {e}")

    def _save_patterns(self):
        """Save pattern analysis results"""
        patterns_file = self.storage_path / "patterns.json"
        try:
            data = {pid: asdict(pattern) for pid, pattern in self.patterns.items()}
            with open(patterns_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save patterns: {e}")

    def start_experiment(self,
                        experiment_name: str,
                        goal: str = "",
                        tags: List[str] = None,
                        metadata: Dict[str, Any] = None) -> str:
        """
        Start a new experiment session.

        Args:
            experiment_name: Name of the experiment
            goal: Goal or objective of the experiment
            tags: Tags for categorization
            metadata: Additional metadata

        Returns:
            Session ID for the started experiment
        """
        session_id = f"exp_{experiment_name.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        session = ExperimentSession(
            session_id=session_id,
            experiment_name=experiment_name,
            start_time=datetime.now(),
            goal=goal,
            tags=tags or [],
            metadata=metadata or {}
        )

        self.active_sessions[session_id] = session
        self._save_sessions()

        # Record the experiment start
        self.record_interaction(
            session_id,
            InteractionType.SUCCESS_EVENT,
            "system",
            {"event": "experiment_started", "goal": goal},
            {"experiment_name": experiment_name}
        )

        return session_id

    def end_experiment(self, session_id: str, final_status: str = "completed"):
        """
        End an experiment session.

        Args:
            session_id: Session ID to end
            final_status: Final status ("completed", "failed", "cancelled")
        """
        if session_id not in self.active_sessions:
            print(f"Warning: Session {session_id} not found")
            return

        session = self.active_sessions[session_id]
        session.end_time = datetime.now()
        session.status = final_status

        # Record the experiment end
        self.record_interaction(
            session_id,
            InteractionType.SUCCESS_EVENT if final_status == "completed" else InteractionType.ERROR_EVENT,
            "system",
            {"event": "experiment_ended", "final_status": final_status},
            {"duration_seconds": (session.end_time - session.start_time).total_seconds()}
        )

        self._save_sessions()

    def record_interaction(self,
                          session_id: str,
                          interaction_type: InteractionType,
                          actor: str,
                          content: Dict[str, Any],
                          metadata: Dict[str, Any] = None,
                          privacy_level: PrivacyLevel = PrivacyLevel.INTERNAL):
        """
        Record an interaction within an experiment session.

        Args:
            session_id: Session ID to record in
            interaction_type: Type of interaction
            actor: Who performed the interaction
            content: Content of the interaction
            metadata: Additional metadata
            privacy_level: Privacy classification
        """
        if session_id not in self.active_sessions:
            print(f"Warning: Session {session_id} not active")
            return

        interaction = Interaction(
            timestamp=datetime.now(),
            interaction_type=interaction_type,
            actor=actor,
            content=content,
            metadata=metadata or {},
            privacy_level=privacy_level
        )

        self.active_sessions[session_id].interactions.append(interaction)
        self._save_sessions()

    def record_file_state(self,
                         session_id: str,
                         file_path: str,
                         modification_type: str = "modified"):
        """
        Record the current state of a file.

        Args:
            session_id: Session ID to record in
            file_path: Path to the file
            modification_type: Type of modification
        """
        if session_id not in self.active_sessions:
            return

        file_path_obj = Path(file_path)
        if not file_path_obj.exists():
            return

        try:
            content = file_path_obj.read_text()
            content_hash = hashlib.sha256(content.encode()).hexdigest()
            size_bytes = len(content.encode())
            line_count = len(content.splitlines())

            file_state = FileState(
                file_path=file_path,
                timestamp=datetime.now(),
                content_hash=content_hash,
                size_bytes=size_bytes,
                line_count=line_count,
                modification_type=modification_type
            )

            self.active_sessions[session_id].file_states.append(file_state)
            self._save_sessions()
        except Exception as e:
            print(f"Warning: Could not record file state for {file_path}: {e}")

    def record_chat_message(self,
                           session_id: str,
                           sender: str,
                           message: str,
                           context: Dict[str, Any] = None):
        """
        Record a chat message interaction.

        Args:
            session_id: Session ID to record in
            sender: Who sent the message
            message: Message content
            context: Additional context
        """
        # Apply privacy filtering
        privacy_level = self._assess_message_privacy(message)

        content = {
            "message": message,
            "sender": sender
        }

        if context:
            content.update(context)

        self.record_interaction(
            session_id,
            InteractionType.CHAT_MESSAGE,
            sender,
            content,
            {"word_count": len(message.split())},
            privacy_level
        )

    def record_command_execution(self,
                                session_id: str,
                                command: str,
                                exit_code: int,
                                output: str = "",
                                duration: float = 0.0):
        """
        Record a command execution.

        Args:
            session_id: Session ID to record in
            command: Command that was executed
            exit_code: Exit code from execution
            output: Command output (truncated for privacy)
            duration: Execution duration in seconds
        """
        # Privacy filtering for commands and output
        privacy_level = self._assess_command_privacy(command)

        content = {
            "command": self._sanitize_command(command),
            "exit_code": exit_code,
            "duration": duration
        }

        if output and privacy_level != PrivacyLevel.RESTRICTED:
            content["output_preview"] = output[:500] + "..." if len(output) > 500 else output

        self.record_interaction(
            session_id,
            InteractionType.COMMAND_EXECUTION,
            "system",
            content,
            {"has_output": bool(output)},
            privacy_level
        )

    def _assess_message_privacy(self, message: str) -> PrivacyLevel:
        """Assess privacy level of a chat message"""
        sensitive_patterns = [
            r'password', r'key', r'token', r'secret', r'private',
            r'api[_-]?key', r'auth', r'credential'
        ]

        message_lower = message.lower()
        for pattern in sensitive_patterns:
            if re.search(pattern, message_lower):
                return PrivacyLevel.RESTRICTED

        if any(word in message_lower for word in ['error', 'debug', 'internal']):
            return PrivacyLevel.SENSITIVE

        return PrivacyLevel.INTERNAL

    def _assess_command_privacy(self, command: str) -> PrivacyLevel:
        """Assess privacy level of a command"""
        sensitive_commands = [
            'ssh', 'scp', 'rsync', 'curl.*password', 'wget.*auth',
            'git.*push.*password', 'docker.*login'
        ]

        command_lower = command.lower()
        for sensitive in sensitive_commands:
            if re.search(sensitive, command_lower):
                return PrivacyLevel.RESTRICTED

        return PrivacyLevel.INTERNAL

    def _sanitize_command(self, command: str) -> str:
        """Sanitize command for privacy"""
        # Remove or mask sensitive information
        sanitized = re.sub(r'(--?password[=\s]\S+)', ' --password=***', command)
        sanitized = re.sub(r'(--?token[=\s]\S+)', ' --token=***', sanitized)
        sanitized = re.sub(r'(--?key[=\s]\S+)', ' --key=***', sanitized)
        return sanitized

    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """Get a summary of an experiment session"""
        if session_id not in self.active_sessions:
            return {"error": "Session not found"}

        session = self.active_sessions[session_id]

        # Calculate statistics
        interaction_counts = {}
        for interaction in session.interactions:
            interaction_counts[interaction.interaction_type.value] = interaction_counts.get(interaction.interaction_type.value, 0) + 1

        duration = None
        if session.end_time:
            duration = (session.end_time - session.start_time).total_seconds()

        return {
            "session_id": session_id,
            "experiment_name": session.experiment_name,
            "status": session.status,
            "start_time": session.start_time.isoformat(),
            "end_time": session.end_time.isoformat() if session.end_time else None,
            "duration_seconds": duration,
            "total_interactions": len(session.interactions),
            "interaction_breakdown": interaction_counts,
            "files_tracked": len(session.file_states),
            "tags": session.tags,
            "goal": session.goal
        }

    def search_sessions(self,
                       query: str = "",
                       tags: List[str] = None,
                       status: str = None,
                       limit: int = 50) -> List[Dict[str, Any]]:
        """
        Search experiment sessions based on criteria.

        Args:
            query: Text search in experiment names and goals
            tags: Filter by tags
            status: Filter by status
            limit: Maximum results to return

        Returns:
            List of session summaries matching criteria
        """
        results = []

        for session_id, session in self.active_sessions.items():
            # Apply filters
            if status and session.status != status:
                continue

            if tags and not all(tag in session.tags for tag in tags):
                continue

            if query:
                search_text = f"{session.experiment_name} {session.goal}".lower()
                if query.lower() not in search_text:
                    continue

            results.append(self.get_session_summary(session_id))

        # Sort by start time (newest first)
        results.sort(key=lambda x: x['start_time'], reverse=True)

        return results[:limit]

    def analyze_patterns(self, session_ids: List[str] = None) -> List[PatternAnalysis]:
        """
        Analyze patterns across experiment sessions.

        Args:
            session_ids: Specific sessions to analyze (all active if None)

        Returns:
            List of identified patterns
        """
        if session_ids is None:
            sessions = list(self.active_sessions.values())
        else:
            sessions = [self.active_sessions[sid] for sid in session_ids if sid in self.active_sessions]

        patterns = []

        # Analyze success patterns
        success_sessions = [s for s in sessions if s.status == "completed"]
        if success_sessions:
            success_pattern = self._analyze_success_patterns(success_sessions)
            if success_pattern:
                patterns.append(success_pattern)

        # Analyze failure patterns
        failed_sessions = [s for s in sessions if s.status == "failed"]
        if failed_sessions:
            failure_pattern = self._analyze_failure_patterns(failed_sessions)
            if failure_pattern:
                patterns.append(failure_pattern)

        # Analyze efficiency patterns
        efficiency_pattern = self._analyze_efficiency_patterns(sessions)
        if efficiency_pattern:
            patterns.append(efficiency_pattern)

        # Save patterns
        for pattern in patterns:
            self.patterns[pattern.pattern_id] = pattern
        self._save_patterns()

        return patterns

    def _analyze_success_patterns(self, sessions: List[ExperimentSession]) -> Optional[PatternAnalysis]:
        """Analyze patterns in successful experiments"""
        if len(sessions) < 2:
            return None

        # Simple pattern: experiments with high interaction diversity tend to succeed
        interaction_types = []
        for session in sessions:
            types = set(i.interaction_type.value for i in session.interactions)
            interaction_types.append(len(types))

        avg_diversity = sum(interaction_types) / len(interaction_types)

        if avg_diversity > 2:  # More than 2 different interaction types
            return PatternAnalysis(
                pattern_id=f"success_diversity_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                pattern_type="success_sequence",
                confidence_score=0.75,
                description=f"Successful experiments show high interaction diversity (avg {avg_diversity:.1f} types)",
                occurrences=[s.session_id for s in sessions],
                recommendations=[
                    "Encourage diverse interaction types during experiments",
                    "Include chat, file edits, and command execution in experiments"
                ]
            )

        return None

    def _analyze_failure_patterns(self, sessions: List[ExperimentSession]) -> Optional[PatternAnalysis]:
        """Analyze patterns in failed experiments"""
        if len(sessions) < 2:
            return None

        # Look for error patterns
        error_counts = []
        for session in sessions:
            errors = sum(1 for i in session.interactions if i.interaction_type == InteractionType.ERROR_EVENT)
            error_counts.append(errors)

        avg_errors = sum(error_counts) / len(error_counts)

        if avg_errors > 1:
            return PatternAnalysis(
                pattern_id=f"failure_errors_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                pattern_type="failure_pattern",
                confidence_score=0.8,
                description=f"Failed experiments show high error rates (avg {avg_errors:.1f} errors)",
                occurrences=[s.session_id for s in sessions],
                recommendations=[
                    "Implement early error detection and correction",
                    "Add validation checkpoints during experiments",
                    "Monitor error rates and intervene when thresholds exceeded"
                ]
            )

        return None

    def _analyze_efficiency_patterns(self, sessions: List[ExperimentSession]) -> Optional[PatternAnalysis]:
        """Analyze efficiency patterns across experiments"""
        if len(sessions) < 3:
            return None

        # Calculate efficiency metrics
        efficiencies = []
        for session in sessions:
            if session.end_time:
                duration = (session.end_time - session.start_time).total_seconds()
                interactions = len(session.interactions)
                if duration > 0:
                    efficiency = interactions / duration  # interactions per second
                    efficiencies.append(efficiency)

        if efficiencies:
            avg_efficiency = sum(efficiencies) / len(efficiencies)
            return PatternAnalysis(
                pattern_id=f"efficiency_interaction_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                pattern_type="efficiency_optimization",
                confidence_score=0.7,
                description=f"Optimal interaction rate: {avg_efficiency:.2f} interactions/second",
                occurrences=[s.session_id for s in sessions],
                recommendations=[
                    f"Target {avg_efficiency:.2f} interactions per second for optimal efficiency",
                    "Monitor interaction pacing during experiments",
                    "Balance thoroughness with efficiency"
                ]
            )

        return None

    def get_system_stats(self) -> Dict[str, Any]:
        """Get system-wide statistics"""
        total_sessions = len(self.active_sessions)
        completed_sessions = sum(1 for s in self.active_sessions.values() if s.status == "completed")
        failed_sessions = sum(1 for s in self.active_sessions.values() if s.status == "failed")

        total_interactions = sum(len(s.interactions) for s in self.active_sessions.values())
        total_file_states = sum(len(s.file_states) for s in self.active_sessions.values())

        return {
            "total_sessions": total_sessions,
            "completed_sessions": completed_sessions,
            "failed_sessions": failed_sessions,
            "success_rate": completed_sessions / total_sessions if total_sessions > 0 else 0,
            "total_interactions": total_interactions,
            "total_file_states": total_file_states,
            "avg_interactions_per_session": total_interactions / total_sessions if total_sessions > 0 else 0,
            "patterns_identified": len(self.patterns)
        }


# Convenience functions for easy integration
def start_experiment_recording(experiment_name: str, **kwargs) -> Tuple[ExperimentRecordingService, str]:
    """
    Convenience function to start experiment recording.

    Args:
        experiment_name: Name of the experiment
        **kwargs: Additional arguments for start_experiment

    Returns:
        Tuple of (service, session_id)
    """
    service = ExperimentRecordingService()
    session_id = service.start_experiment(experiment_name, **kwargs)
    return service, session_id


def record_chat(service: ExperimentRecordingService, session_id: str, sender: str, message: str):
    """Convenience function to record a chat message"""
    service.record_chat_message(session_id, sender, message)


def record_command(service: ExperimentRecordingService, session_id: str, command: str, exit_code: int, **kwargs):
    """Convenience function to record a command execution"""
    service.record_command_execution(session_id, command, exit_code, **kwargs)


if __name__ == "__main__":
    # Demo usage
    print("Experiment Recording System Demo")
    print("=" * 40)

    # Initialize service
    service = ExperimentRecordingService()

    # Start an experiment
    service, session_id = start_experiment_recording(
        "Memory Architecture Implementation",
        goal="Implement comprehensive memory systems for Santiago ecosystem",
        tags=["memory", "architecture", "santiago-core"]
    )

    print(f"✓ Started experiment: {session_id}")

    # Record some interactions
    record_chat(service, session_id, "user", "Let's implement the memory snapshot service")
    record_chat(service, session_id, "agent", "I'll create the MemorySnapshotService class")

    # Simulate file creation
    service.record_file_state(session_id, "memory_snapshot_service.py", "created")

    # Record command execution
    record_command(service, session_id, "python3 implementation.py", 0, duration=2.5)

    record_chat(service, session_id, "agent", "Implementation completed successfully")

    # End experiment
    service.end_experiment(session_id, "completed")

    print("✓ Recorded experiment interactions")

    # Get summary
    summary = service.get_session_summary(session_id)
    print(f"✓ Session summary: {summary['total_interactions']} interactions, {summary['files_tracked']} files tracked")

    # Analyze patterns
    patterns = service.analyze_patterns([session_id])
    print(f"✓ Identified {len(patterns)} patterns")

    # Get system stats
    stats = service.get_system_stats()
    print(f"✓ System stats: {stats['total_sessions']} sessions, {stats['success_rate']:.1%} success rate")

    print("\n🎉 Experiment Recording System operational!")
    print("Ready to capture complete development sessions for learning and optimization.")