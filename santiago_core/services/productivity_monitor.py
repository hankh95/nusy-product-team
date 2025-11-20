#!/usr/bin/env python3
"""
Productivity Monitor Service

This service monitors active work items and detects when tasks have been stuck
for too long without progress. It helps ensure team productivity by identifying
stalled work and triggering appropriate actions.

Key features:
- Monitors active kanban cards (in_progress state)
- Tracks time spent on each task
- Detects tasks stuck for more than configurable threshold (default: 5 minutes)
- Triggers alerts and potential escalation actions
- Integrates with kanban workflow for automatic task reassignment
- Provides productivity metrics and reports
"""

import asyncio
import signal
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging
import json

from santiago_core.services.kanban_service import SantiagoKanbanService


class ProductivityMonitor:
    """Service that monitors task progress and detects stalled work"""

    def __init__(self, workspace_path: Path, config: Optional[Dict[str, Any]] = None):
        self.workspace_path = workspace_path
        self.config = config or self._get_default_config()
        self.kanban_service = SantiagoKanbanService(workspace_path)

        # Service state
        self.running = False
        self.last_check_time = None
        self.task_timers: Dict[str, Dict[str, Any]] = {}  # card_id -> timer data
        self.alerted_tasks: set = set()  # Tasks we've already alerted about

        # Setup logging
        self.logger = logging.getLogger('ProductivityMonitor')
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            'check_interval_seconds': 60,  # Check every minute
            'stuck_threshold_minutes': 5,  # Alert after 5 minutes
            'escalation_threshold_minutes': 15,  # Escalate after 15 minutes
            'auto_reassign_stuck_tasks': False,  # Whether to auto-reassign stuck tasks
            'target_boards': [],  # Empty means monitor all boards
            'alert_channels': ['log'],  # Where to send alerts: log, email, slack, etc.
            'productivity_report_interval_hours': 24,  # Daily productivity reports
            'log_level': 'INFO'
        }

    async def start(self):
        """Start the productivity monitoring service"""
        self.logger.info("📊 Starting Productivity Monitor Service")
        self.running = True

        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        try:
            # Initial discovery and baseline
            await self._initialize_monitoring()

            # Main monitoring loop
            while self.running:
                try:
                    await self._check_productivity()
                    await asyncio.sleep(self.config['check_interval_seconds'])
                except Exception as e:
                    self.logger.error(f"❌ Error in monitoring loop: {e}")
                    await asyncio.sleep(self.config['check_interval_seconds'])

        except Exception as e:
            self.logger.error(f"❌ Fatal error in productivity monitor: {e}")
        finally:
            self.logger.info("🛑 Productivity Monitor Service stopped")

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.logger.info(f"📡 Received signal {signum}, shutting down gracefully...")
        self.running = False

    async def _initialize_monitoring(self):
        """Initialize monitoring by discovering current active tasks"""
        self.logger.info("🔍 Initializing productivity monitoring...")

        # Discover boards
        boards_result = await self.kanban_service.handle_tool_call('kanban_list_boards', {})
        if boards_result.error:
            self.logger.error(f"❌ Failed to list boards: {boards_result.error}")
            return

        boards = boards_result.result.get('boards', [])
        if not boards:
            self.logger.warning("⚠️  No kanban boards found")
            return

        if self.config['target_boards']:
            available_board_ids = [b['board_id'] for b in boards]
            self.config['target_boards'] = [b for b in self.config['target_boards'] if b in available_board_ids]
        else:
            self.config['target_boards'] = [b['board_id'] for b in boards]

        self.logger.info(f"✅ Monitoring {len(self.config['target_boards'])} board(s): {', '.join(self.config['target_boards'])}")

        # Initialize timers for currently active tasks
        await self._scan_active_tasks()

    async def _scan_active_tasks(self):
        """Scan all boards for currently active (in_progress) tasks"""
        self.logger.info("📋 Scanning for active tasks...")

        for board_id in self.config['target_boards']:
            try:
                # Get board summary to find active tasks
                summary_result = await self.kanban_service.handle_tool_call('kanban_get_board_summary', {
                    'board_id': board_id
                })

                if summary_result.error:
                    self.logger.error(f"❌ Failed to get summary for board {board_id}: {summary_result.error}")
                    continue

                items = summary_result.result.get('items', [])
                active_items = [item for item in items if item.get('column') == 'in_progress']

                for item in active_items:
                    card_id = item['card_id']
                    if card_id not in self.task_timers:
                        # Initialize timer for this task
                        self.task_timers[card_id] = {
                            'board_id': board_id,
                            'card_id': card_id,
                            'title': item['title'],
                            'assignee': item.get('assignee', 'unassigned'),
                            'start_time': datetime.now(),
                            'last_activity': datetime.now(),
                            'status': 'active',
                            'alerts_sent': 0,
                            'escalated': False
                        }
                        self.logger.info(f"⏱️  Started monitoring: {item['title']} (assigned to {item.get('assignee', 'unassigned')})")

            except Exception as e:
                self.logger.error(f"❌ Error scanning board {board_id}: {e}")

        self.logger.info(f"✅ Now monitoring {len(self.task_timers)} active task(s)")

    async def _check_productivity(self):
        """Check productivity by examining active tasks"""
        self.last_check_time = datetime.now()
        current_time = datetime.now()

        # Check for stuck tasks
        stuck_tasks = []
        for card_id, timer in self.task_timers.items():
            time_since_activity = current_time - timer['last_activity']
            minutes_stuck = time_since_activity.total_seconds() / 60

            # Update timer status
            if minutes_stuck >= self.config['stuck_threshold_minutes']:
                stuck_tasks.append((card_id, timer, minutes_stuck))

        # Process stuck tasks
        for card_id, timer, minutes_stuck in stuck_tasks:
            await self._handle_stuck_task(card_id, timer, minutes_stuck)

        # Clean up completed tasks (this would be enhanced with actual completion detection)
        await self._cleanup_completed_tasks()

        # Periodic productivity report
        await self._generate_productivity_report()

    async def _handle_stuck_task(self, card_id: str, timer: Dict[str, Any], minutes_stuck: float):
        """Handle a task that appears to be stuck"""
        if card_id in self.alerted_tasks:
            # Already alerted, check if escalation is needed
            if (minutes_stuck >= self.config['escalation_threshold_minutes'] and
                not timer.get('escalated', False)):
                await self._escalate_stuck_task(card_id, timer, minutes_stuck)
            return

        # First time detecting this stuck task
        self.alerted_tasks.add(card_id)
        timer['alerts_sent'] += 1

        self.logger.warning(f"⚠️  STUCK TASK ALERT: '{timer['title']}' has been active for {minutes_stuck:.1f} minutes")
        self.logger.warning(f"   Assigned to: {timer['assignee']}")
        self.logger.warning(f"   Board: {timer['board_id']}")
        self.logger.warning(f"   Started: {timer['start_time'].strftime('%Y-%m-%d %H:%M:%S')}")

        # Send alerts
        await self._send_alerts(timer, minutes_stuck, "stuck_task")

        # Consider auto-reassignment if enabled
        if self.config.get('auto_reassign_stuck_tasks', False):
            await self._consider_reassignment(card_id, timer)

    async def _escalate_stuck_task(self, card_id: str, timer: Dict[str, Any], minutes_stuck: float):
        """Escalate a severely stuck task"""
        timer['escalated'] = True

        self.logger.error(f"🚨 STUCK TASK ESCALATION: '{timer['title']}' has been stuck for {minutes_stuck:.1f} minutes!")
        self.logger.error(f"   This task requires immediate attention")

        # Send escalation alerts
        await self._send_alerts(timer, minutes_stuck, "escalation")

        # Add urgent comment to the task
        try:
            comment_result = await self.kanban_service.handle_tool_call('kanban_add_comment', {
                'board_id': timer['board_id'],
                'card_id': card_id,
                'comment': f"🚨 URGENT: This task has been stuck for {minutes_stuck:.1f} minutes and requires immediate attention!",
                'author': 'productivity-monitor'
            })

            if comment_result.error:
                self.logger.error(f"❌ Failed to add escalation comment: {comment_result.error}")

        except Exception as e:
            self.logger.error(f"❌ Error adding escalation comment: {e}")

    async def _send_alerts(self, timer: Dict[str, Any], minutes_stuck: float, alert_type: str):
        """Send alerts through configured channels"""
        alert_channels = self.config.get('alert_channels', ['log'])

        alert_message = {
            'type': alert_type,
            'task_title': timer['title'],
            'assignee': timer['assignee'],
            'board_id': timer['board_id'],
            'minutes_stuck': minutes_stuck,
            'start_time': timer['start_time'].isoformat(),
            'timestamp': datetime.now().isoformat()
        }

        for channel in alert_channels:
            try:
                if channel == 'log':
                    # Already logged above
                    pass
                elif channel == 'file':
                    await self._write_alert_to_file(alert_message)
                elif channel == 'email':
                    await self._send_email_alert(alert_message)
                elif channel == 'slack':
                    await self._send_slack_alert(alert_message)
                else:
                    self.logger.warning(f"⚠️  Unknown alert channel: {channel}")
            except Exception as e:
                self.logger.error(f"❌ Error sending alert via {channel}: {e}")

    async def _write_alert_to_file(self, alert_message: Dict[str, Any]):
        """Write alert to a log file"""
        alerts_dir = self.workspace_path / "logs" / "alerts"
        alerts_dir.mkdir(parents=True, exist_ok=True)

        alert_file = alerts_dir / f"productivity_alerts_{datetime.now().strftime('%Y%m%d')}.jsonl"

        with open(alert_file, 'a') as f:
            f.write(json.dumps(alert_message) + '\n')

    async def _send_email_alert(self, alert_message: Dict[str, Any]):
        """Send email alert (placeholder for actual email implementation)"""
        self.logger.info(f"📧 Would send email alert: {alert_message['task_title']} stuck for {alert_message['minutes_stuck']:.1f} minutes")

    async def _send_slack_alert(self, alert_message: Dict[str, Any]):
        """Send Slack alert (placeholder for actual Slack integration)"""
        self.logger.info(f"💬 Would send Slack alert: {alert_message['task_title']} stuck for {alert_message['minutes_stuck']:.1f} minutes")

    async def _consider_reassignment(self, card_id: str, timer: Dict[str, Any]):
        """Consider reassigning a stuck task to another team member"""
        self.logger.info(f"🤔 Considering reassignment for stuck task: {timer['title']}")

        # Get team workload to find best reassignment candidate
        try:
            workload_result = await self.kanban_service.handle_tool_call('kanban_get_team_workload', {
                'board_id': timer['board_id']
            })

            if not workload_result.error:
                team_workload = workload_result.result.get('team_workload', {})

                # Find team member with lowest workload
                best_candidate = None
                lowest_load = float('inf')

                for member, workload in team_workload.items():
                    if member != timer['assignee']:  # Don't reassign to current assignee
                        total_tasks = workload['total']
                        if total_tasks < lowest_load:
                            lowest_load = total_tasks
                            best_candidate = member

                if best_candidate:
                    self.logger.info(f"💡 Suggesting reassignment from {timer['assignee']} to {best_candidate}")
                    # In a real implementation, you might automatically reassign here
                    # For now, just log the suggestion
                else:
                    self.logger.warning("⚠️  No suitable reassignment candidate found")

        except Exception as e:
            self.logger.error(f"❌ Error considering reassignment: {e}")

    async def _cleanup_completed_tasks(self):
        """Clean up timers for completed tasks"""
        # This is a simplified version - in practice, you'd want to detect
        # when tasks actually move out of in_progress status
        current_time = datetime.now()

        # Remove tasks that have been monitored for more than 24 hours
        # (assuming they're either completed or genuinely stuck)
        to_remove = []
        for card_id, timer in self.task_timers.items():
            if current_time - timer['start_time'] > timedelta(hours=24):
                to_remove.append(card_id)

        for card_id in to_remove:
            timer = self.task_timers[card_id]
            self.logger.info(f"🧹 Cleaning up old task timer: {timer['title']} (monitored for {(current_time - timer['start_time']).total_seconds() / 3600:.1f} hours)")
            del self.task_timers[card_id]

    async def _generate_productivity_report(self):
        """Generate periodic productivity reports"""
        # Generate daily reports
        current_time = datetime.now()
        report_interval = self.config.get('productivity_report_interval_hours', 24)

        # Simple time-based reporting (could be enhanced with persistent storage)
        if (not hasattr(self, '_last_report_time') or
            current_time - self._last_report_time > timedelta(hours=report_interval)):

            self._last_report_time = current_time
            await self._create_productivity_report()

    async def _create_productivity_report(self):
        """Create a productivity report"""
        current_time = datetime.now()
        report_date = current_time.strftime('%Y-%m-%d')

        # Calculate metrics
        total_active_tasks = len(self.task_timers)
        alerted_tasks = len(self.alerted_tasks)
        escalated_tasks = sum(1 for t in self.task_timers.values() if t.get('escalated', False))

        # Average task duration for completed tasks (simplified)
        avg_duration_hours = 0  # Would need completion tracking to calculate properly

        report = {
            'date': report_date,
            'total_active_tasks': total_active_tasks,
            'alerted_tasks': alerted_tasks,
            'escalated_tasks': escalated_tasks,
            'avg_task_duration_hours': avg_duration_hours,
            'productivity_score': self._calculate_productivity_score(),
            'generated_at': current_time.isoformat()
        }

        # Write report to file
        reports_dir = self.workspace_path / "reports" / "productivity"
        reports_dir.mkdir(parents=True, exist_ok=True)

        report_file = reports_dir / f"productivity_report_{report_date}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        self.logger.info(f"📊 Generated productivity report: {report_file}")
        self.logger.info(f"   Active tasks: {total_active_tasks}, Alerts: {alerted_tasks}, Escalations: {escalated_tasks}")

    def _calculate_productivity_score(self) -> float:
        """Calculate a simple productivity score"""
        if not self.task_timers:
            return 100.0  # No active tasks = perfectly productive

        alerted_ratio = len(self.alerted_tasks) / len(self.task_timers)
        escalated_ratio = sum(1 for t in self.task_timers.values() if t.get('escalated', False)) / len(self.task_timers)

        # Simple scoring: lower alerts/escalations = higher score
        score = 100.0 - (alerted_ratio * 30) - (escalated_ratio * 50)
        return max(0.0, min(100.0, score))

    async def get_status(self) -> Dict[str, Any]:
        """Get current status of the productivity monitor"""
        current_time = datetime.now()

        # Calculate some metrics
        active_tasks = len(self.task_timers)
        stuck_tasks = len(self.alerted_tasks)
        escalated_tasks = sum(1 for t in self.task_timers.values() if t.get('escalated', False))

        # Get details of currently stuck tasks
        stuck_task_details = []
        for card_id, timer in self.task_timers.items():
            if card_id in self.alerted_tasks:
                time_stuck = current_time - timer['last_activity']
                stuck_task_details.append({
                    'card_id': card_id,
                    'title': timer['title'],
                    'assignee': timer['assignee'],
                    'minutes_stuck': time_stuck.total_seconds() / 60,
                    'escalated': timer.get('escalated', False)
                })

        return {
            'running': self.running,
            'last_check_time': self.last_check_time.isoformat() if self.last_check_time else None,
            'active_tasks': active_tasks,
            'stuck_tasks': stuck_tasks,
            'escalated_tasks': escalated_tasks,
            'stuck_task_details': stuck_task_details,
            'config': self.config
        }

    def stop(self):
        """Stop the productivity monitoring service"""
        self.logger.info("🛑 Stopping Productivity Monitor Service...")
        self.running = False


# CLI interface
async def main():
    """CLI entry point for the Productivity Monitor"""
    import argparse

    parser = argparse.ArgumentParser(description='Productivity Monitor Service')
    parser.add_argument('--workspace', '-w', type=str, default='.',
                       help='Workspace path (default: current directory)')
    parser.add_argument('--check-interval', '-i', type=int, default=60,
                       help='Check interval in seconds (default: 60)')
    parser.add_argument('--stuck-threshold', '-t', type=int, default=5,
                       help='Stuck threshold in minutes (default: 5)')
    parser.add_argument('--escalation-threshold', '-e', type=int, default=15,
                       help='Escalation threshold in minutes (default: 15)')
    parser.add_argument('--boards', '-b', nargs='*',
                       help='Target board IDs (default: all boards)')
    parser.add_argument('--auto-reassign', action='store_true',
                       help='Automatically reassign stuck tasks')
    parser.add_argument('--alert-channels', nargs='*', default=['log'],
                       help='Alert channels: log, file, email, slack (default: log)')
    parser.add_argument('--status', action='store_true',
                       help='Show service status and exit')

    args = parser.parse_args()

    workspace_path = Path(args.workspace).resolve()

    # Configuration
    config = {
        'check_interval_seconds': args.check_interval,
        'stuck_threshold_minutes': args.stuck_threshold,
        'escalation_threshold_minutes': args.escalation_threshold,
        'auto_reassign_stuck_tasks': args.auto_reassign,
        'target_boards': args.boards or [],
        'alert_channels': args.alert_channels,
        'log_level': 'INFO'
    }

    # Create and configure monitor
    monitor = ProductivityMonitor(workspace_path, config)

    if args.status:
        # Just show status
        status = await monitor.get_status()
        print("📊 Productivity Monitor Status:")
        print(f"  Running: {status['running']}")
        print(f"  Last Check: {status['last_check_time'] or 'Never'}")
        print(f"  Active Tasks: {status['active_tasks']}")
        print(f"  Stuck Tasks: {status['stuck_tasks']}")
        print(f"  Escalated Tasks: {status['escalated_tasks']}")

        if status['stuck_task_details']:
            print("\n🚨 Currently Stuck Tasks:")
            for task in status['stuck_task_details']:
                escalated = " (ESCALATED)" if task['escalated'] else ""
                print(f"  • {task['title']} - {task['assignee']} - {task['minutes_stuck']:.1f} min stuck{escalated}")
        return

    # Start the service
    try:
        await monitor.start()
    except KeyboardInterrupt:
        monitor.stop()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())