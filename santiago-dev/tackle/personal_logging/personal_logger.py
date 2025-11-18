#!/usr/bin/env python3
"""
Automated Personal Logger for Santiago-Dev

Creates Santiago-PM compliant personal logs with YAML metadata.
"""

import os
import yaml
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from uuid import uuid4


class AutomatedPersonalLogger:
    """
    Automated personal logger that creates Santiago-PM compliant logs.
    """

    def __init__(self, workspace_path: Path):
        self.workspace_path = Path(workspace_path)
        self.logs_path = workspace_path / "workspace" / "personal-logs"
        self.logs_path.mkdir(parents=True, exist_ok=True)

        self.current_session = None
        self.session_activities = []

    async def start_work_session(self, session_title: str):
        """Start a new work session."""
        session_id = str(uuid4())
        timestamp = datetime.now()

        self.current_session = {
            'id': session_id,
            'title': session_title,
            'start_time': timestamp.isoformat(),
            'activities': []
        }

        print(f"📝 Started work session: {session_title}")

    async def log_activity(self, activity: str, importance: str = "normal"):
        """Log an activity in the current session."""
        if not self.current_session:
            await self.start_work_session("Automated Session")

        timestamp = datetime.now()
        activity_entry = {
            'timestamp': timestamp.isoformat(),
            'activity': activity,
            'importance': importance
        }

        self.current_session['activities'].append(activity_entry)
        self.session_activities.append(activity_entry)

        print(f"📋 Logged activity: {activity}")

    async def end_work_session(self):
        """End the current work session and save the log."""
        if not self.current_session:
            return

        end_time = datetime.now()
        self.current_session['end_time'] = end_time.isoformat()

        # Calculate session duration
        start_time = datetime.fromisoformat(self.current_session['start_time'])
        duration = end_time - start_time
        self.current_session['duration_seconds'] = duration.total_seconds()

        # Save the log file
        await self._save_session_log()

        print(f"✅ Ended work session: {self.current_session['title']}")

        # Reset session
        self.current_session = None
        self.session_activities = []

    async def _save_session_log(self):
        """Save the session log in Santiago-PM compliant YAML format."""
        if not self.current_session:
            return

        # Create log filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_id = self.current_session['id'][:8]
        filename = f"personal_log_{timestamp}_{session_id}.yaml"

        log_file = self.logs_path / filename

        # Create Santiago-PM compliant YAML structure
        log_data = {
            'metadata': {
                'version': '1.0',
                'type': 'personal_log',
                'session_id': self.current_session['id'],
                'created_at': self.current_session['start_time'],
                'updated_at': datetime.now().isoformat()
            },
            'session': {
                'title': self.current_session['title'],
                'start_time': self.current_session['start_time'],
                'end_time': self.current_session.get('end_time'),
                'duration_seconds': self.current_session.get('duration_seconds'),
                'activities_count': len(self.current_session['activities'])
            },
            'activities': self.current_session['activities'],
            'context': {
                'workspace': str(self.workspace_path),
                'automation_level': 'autonomous',
                'agent_type': 'santiago-dev'
            }
        }

        try:
            with open(log_file, 'w') as f:
                yaml.dump(log_data, f, default_flow_style=False, sort_keys=False)

            print(f"💾 Saved personal log: {filename}")

        except Exception as e:
            print(f"❌ Failed to save personal log: {e}")

    def get_recent_logs(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get recent personal logs."""
        log_files = sorted(
            self.logs_path.glob("personal_log_*.yaml"),
            key=os.path.getmtime,
            reverse=True
        )

        recent_logs = []
        for log_file in log_files[:limit]:
            try:
                with open(log_file, 'r') as f:
                    log_data = yaml.safe_load(f)
                    recent_logs.append(log_data)
            except Exception as e:
                print(f"⚠️ Failed to load log {log_file}: {e}")

        return recent_logs

    def get_session_summary(self) -> Optional[Dict[str, Any]]:
        """Get summary of current session."""
        if not self.current_session:
            return None

        return {
            'title': self.current_session['title'],
            'start_time': self.current_session['start_time'],
            'activities_count': len(self.current_session['activities']),
            'active': True
        }