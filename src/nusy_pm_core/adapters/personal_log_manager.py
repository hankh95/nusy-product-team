"""
Personal Log Manager - MCP Tools for F-027 Phase 1 MVP
========================================================
Implements 3 core MCP tools for personal log context restoration:
1. save_chat_history: Save agent conversation with metadata
2. restore_context_from_log: Load context from previous session
3. create_human_log_entry: Template for human journal entries

Design:
- Minimal transformation (preserve original format)
- Auto-extract semantic links (files mentioned, decisions made)
- YAML frontmatter for queryability
- Markdown body for readability

Success Criteria:
- Context restoration time < 30 seconds (target: < 2 minutes)
- New agent understands context without re-explanation
- Full provenance chain (session → log → artifacts)
"""

from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
import yaml
import re


class PersonalLogManager:
    """
    Manages personal log operations for agents and humans.
    
    Core capabilities:
    - Save agent chat histories with metadata extraction
    - Restore context from previous sessions
    - Create human journal entries with templates
    - Semantic link extraction (artifacts, decisions, patterns)
    """
    
    def __init__(self, workspace_path: Path):
        """Initialize personal log manager with workspace path."""
        self.workspace_path = Path(workspace_path)
        self.personal_logs_dir = self.workspace_path / "santiago-pm" / "personal-logs"
        self.agents_dir = self.personal_logs_dir / "agents"
        self.humans_dir = self.personal_logs_dir / "humans"
        
        # Ensure directories exist
        self.agents_dir.mkdir(parents=True, exist_ok=True)
        self.humans_dir.mkdir(parents=True, exist_ok=True)
    
    
    def save_chat_history(
        self,
        conversation: str,
        agent_name: str,
        session_date: Optional[str] = None,
        topic: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Path:
        """
        Save agent conversation as personal log.
        
        Args:
            conversation: Full conversation transcript
            agent_name: Name of agent (e.g., "copilot-claude", "santiago-pm")
            session_date: Date (YYYY-MM-DD), defaults to today
            topic: Brief topic description for filename
            metadata: Additional metadata to include
        
        Returns:
            Path to created log file
        
        Example:
            log_path = manager.save_chat_history(
                conversation="User: ...\nAgent: ...",
                agent_name="copilot-claude",
                topic="feature-prioritization"
            )
        """
        # Default values
        if session_date is None:
            session_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        
        if topic is None:
            topic = "session"
        
        # Generate filename: YYYY-MM-DD-{agent-name}-{topic}.md
        filename = f"{session_date}-{agent_name}-{topic}.md"
        filepath = self.agents_dir / filename
        
        # Extract metadata from conversation
        extracted_metadata = self._extract_metadata_from_conversation(conversation)
        
        # Merge with provided metadata
        if metadata:
            extracted_metadata.update(metadata)
        
        # Build YAML frontmatter
        frontmatter = self._build_frontmatter(
            artifact_type="personal-log",
            log_type="agent-chat-history",
            agent_name=agent_name,
            session_date=session_date,
            metadata=extracted_metadata
        )
        
        # Build complete log file
        log_content = f"---\n{frontmatter}\n---\n\n{conversation}"
        
        # Write to file
        filepath.write_text(log_content, encoding="utf-8")
        
        print(f"✅ Saved chat history: {filepath.relative_to(self.workspace_path)}")
        return filepath
    
    
    def restore_context_from_log(
        self,
        log_id: Optional[str] = None,
        log_date: Optional[str] = None,
        topic: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Restore context from previous session log.
        
        Args:
            log_id: Specific log ID (filename without .md)
            log_date: Date to search (YYYY-MM-DD)
            topic: Topic keyword to search for
        
        Returns:
            Dict with:
                - summary: Brief context summary
                - decisions: Key decisions made
                - artifacts: Artifacts worked on
                - blockers: Outstanding blockers
                - next_steps: What to do next
                - full_content: Complete log content
                - metadata: All YAML frontmatter
        
        Example:
            context = manager.restore_context_from_log(
                log_date="2025-11-17",
                topic="prioritization"
            )
            print(context["summary"])
            print(context["next_steps"])
        """
        # Find matching log file
        log_file = self._find_log_file(log_id, log_date, topic)
        
        if not log_file:
            return {
                "error": "No matching log found",
                "search_criteria": {
                    "log_id": log_id,
                    "log_date": log_date,
                    "topic": topic
                }
            }
        
        # Parse log file
        content = log_file.read_text(encoding="utf-8")
        
        # Extract YAML frontmatter and body
        frontmatter, body = self._parse_log_file(content)
        
        # Build context object
        context = {
            "log_file": str(log_file.relative_to(self.workspace_path)),
            "summary": frontmatter.get("context_summary", "No summary available"),
            "decisions": frontmatter.get("key_decisions", []),
            "artifacts": {
                "worked_on": frontmatter.get("worked_on", []),
                "created": frontmatter.get("created", []),
                "modified": frontmatter.get("modified", []),
                "mentioned": frontmatter.get("mentioned", [])
            },
            "blockers": frontmatter.get("blockers", []),
            "questions": frontmatter.get("questions", []),
            "next_steps": frontmatter.get("next_steps", "No next steps specified"),
            "learning": frontmatter.get("learning", []),
            "metadata": frontmatter,
            "full_content": body
        }
        
        print(f"✅ Restored context from: {log_file.name}")
        print(f"📝 Summary: {context['summary'][:100]}...")
        
        return context
    
    
    def create_human_log_entry(
        self,
        author: str,
        session_date: Optional[str] = None,
        topic: Optional[str] = None,
        template_only: bool = False
    ) -> Path:
        """
        Create human personal log entry (journal-style).
        
        Args:
            author: Human's name (e.g., "hank")
            session_date: Date (YYYY-MM-DD), defaults to today
            topic: Brief topic for filename
            template_only: If True, just return template path (don't create file)
        
        Returns:
            Path to created log file or template
        
        Example:
            log_path = manager.create_human_log_entry(
                author="hank",
                topic="workflow-discovery"
            )
            # Opens editor with template, user fills in
        """
        # Default values
        if session_date is None:
            session_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        
        if topic is None:
            topic = "work-session"
        
        # Template path
        template_path = self.personal_logs_dir / "personal-log-template.md"
        
        if template_only:
            return template_path
        
        # Generate filename: YYYY-MM-DD-{author}-{topic}.md
        filename = f"{session_date}-{author}-{topic}.md"
        filepath = self.humans_dir / filename
        
        # Load template
        template_content = template_path.read_text(encoding="utf-8")
        
        # Customize template with author and date
        customized_content = template_content.replace(
            "author: [your-name]", f"author: {author}"
        ).replace(
            "session_date: YYYY-MM-DD", f"session_date: {session_date}"
        )
        
        # Write to file
        filepath.write_text(customized_content, encoding="utf-8")
        
        print(f"✅ Created human log entry: {filepath.relative_to(self.workspace_path)}")
        print(f"📝 Edit file to add session details")
        
        return filepath
    
    
    # ========================================================================
    # HELPER METHODS (Internal)
    # ========================================================================
    
    def _extract_metadata_from_conversation(self, conversation: str) -> Dict[str, Any]:
        """
        Extract metadata from conversation content.
        
        Extracts:
        - Files mentioned (*.md, *.py, *.feature)
        - Decisions (phrases like "decided to", "chose", "selected")
        - Features mentioned (F-XXX format)
        - Artifacts created/modified
        """
        metadata = {
            "worked_on": [],
            "created": [],
            "modified": [],
            "mentioned": [],
            "key_decisions": []
        }
        
        # Extract file mentions
        file_pattern = r'\b[\w/-]+\.(md|py|feature|yaml|yml|json|txt)\b'
        files = re.findall(file_pattern, conversation, re.IGNORECASE)
        metadata["mentioned"].extend(list(set(files)))
        
        # Extract feature IDs (F-XXX format)
        feature_pattern = r'F-\d{3}'
        features = re.findall(feature_pattern, conversation)
        metadata["mentioned"].extend(list(set(features)))
        
        # Extract decisions (simple heuristic)
        decision_markers = [
            "decided to", "chose to", "selected", "decision:",
            "we will", "plan to", "going with"
        ]
        lines = conversation.split('\n')
        for line in lines:
            if any(marker in line.lower() for marker in decision_markers):
                metadata["key_decisions"].append(line.strip())
        
        return metadata
    
    
    def _build_frontmatter(
        self,
        artifact_type: str,
        log_type: str,
        agent_name: str,
        session_date: str,
        metadata: Dict[str, Any]
    ) -> str:
        """Build YAML frontmatter for log file."""
        frontmatter_dict = {
            "artifact_type": artifact_type,
            "log_type": log_type,
            "agent_name": agent_name,
            "session_date": session_date,
            "session_start": datetime.now(timezone.utc).isoformat(),
            "session_end": None,  # Will be filled manually or by editor
            "session_duration": None,
            "conversation_id": metadata.get("conversation_id", None),
            "context_summary": metadata.get("context_summary", ""),
            "worked_on": metadata.get("worked_on", []),
            "created": metadata.get("created", []),
            "modified": metadata.get("modified", []),
            "mentioned": metadata.get("mentioned", []),
            "key_decisions": metadata.get("key_decisions", []),
            "blockers": metadata.get("blockers", []),
            "questions": metadata.get("questions", []),
            "next_steps": metadata.get("next_steps", []),
            "related_to": metadata.get("related_to", []),
            "importance": metadata.get("importance", "medium"),
            "tags": metadata.get("tags", [])
        }
        
        return yaml.dump(frontmatter_dict, default_flow_style=False, sort_keys=False)
    
    
    def _find_log_file(
        self,
        log_id: Optional[str],
        log_date: Optional[str],
        topic: Optional[str]
    ) -> Optional[Path]:
        """
        Find log file matching criteria.
        
        Search strategy:
        1. If log_id provided: exact match
        2. If log_date + topic: find matching filename
        3. If only log_date: most recent on that date
        4. If only topic: most recent with that topic
        5. If nothing: most recent overall
        """
        all_logs = sorted(
            self.agents_dir.glob("*.md"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        
        # Exact log_id match
        if log_id:
            log_file = self.agents_dir / f"{log_id}.md"
            if log_file.exists():
                return log_file
        
        # Date + topic match
        if log_date and topic:
            pattern = f"{log_date}-*-{topic}.md"
            matches = list(self.agents_dir.glob(pattern))
            if matches:
                return matches[0]
        
        # Date only
        if log_date:
            pattern = f"{log_date}-*.md"
            matches = list(self.agents_dir.glob(pattern))
            if matches:
                return matches[0]
        
        # Topic only
        if topic:
            matches = [log for log in all_logs if topic in log.name]
            if matches:
                return matches[0]
        
        # Most recent
        if all_logs:
            return all_logs[0]
        
        return None
    
    
    def _parse_log_file(self, content: str) -> tuple[Dict[str, Any], str]:
        """
        Parse log file into frontmatter and body.
        
        Returns:
            (frontmatter_dict, body_content)
        """
        # Split on --- markers
        parts = content.split('---', 2)
        
        if len(parts) < 3:
            # No frontmatter
            return {}, content
        
        # Parse YAML frontmatter
        try:
            frontmatter = yaml.safe_load(parts[1])
        except yaml.YAMLError:
            frontmatter = {}
        
        # Body is everything after second ---
        body = parts[2].strip()
        
        return frontmatter, body


# ============================================================================
# CLI INTERFACE (for testing)
# ============================================================================

def main():
    """CLI interface for personal log management."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Personal Log Manager - Save and restore session context"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # save-chat command
    save_parser = subparsers.add_parser("save-chat", help="Save chat history")
    save_parser.add_argument("--agent", required=True, help="Agent name")
    save_parser.add_argument("--topic", help="Session topic")
    save_parser.add_argument("--input", help="Input file (conversation transcript)")
    
    # restore command
    restore_parser = subparsers.add_parser("restore", help="Restore context from log")
    restore_parser.add_argument("--log-id", help="Log ID (filename without .md)")
    restore_parser.add_argument("--date", help="Log date (YYYY-MM-DD)")
    restore_parser.add_argument("--topic", help="Topic keyword")
    
    # create-human command
    human_parser = subparsers.add_parser("create-human", help="Create human log entry")
    human_parser.add_argument("--author", required=True, help="Author name")
    human_parser.add_argument("--topic", help="Session topic")
    
    args = parser.parse_args()
    
    # Initialize manager
    workspace_path = Path.cwd()
    manager = PersonalLogManager(workspace_path)
    
    # Execute command
    if args.command == "save-chat":
        if args.input:
            conversation = Path(args.input).read_text()
        else:
            print("Enter conversation (Ctrl+D when done):")
            conversation = sys.stdin.read()
        
        log_path = manager.save_chat_history(
            conversation=conversation,
            agent_name=args.agent,
            topic=args.topic
        )
        print(f"Saved to: {log_path}")
    
    elif args.command == "restore":
        context = manager.restore_context_from_log(
            log_id=args.log_id,
            log_date=args.date,
            topic=args.topic
        )
        
        if "error" in context:
            print(f"❌ {context['error']}")
            print(f"Search criteria: {context['search_criteria']}")
        else:
            print(f"\n📝 Context Summary:\n{context['summary']}\n")
            print(f"🔧 Artifacts Worked On: {', '.join(context['artifacts']['worked_on']) if context['artifacts']['worked_on'] else 'None'}\n")
            print(f"✅ Next Steps:\n{context['next_steps']}\n")
            
            if context['decisions']:
                print(f"🎯 Key Decisions:")
                for decision in context['decisions']:
                    print(f"  - {decision}")
    
    elif args.command == "create-human":
        log_path = manager.create_human_log_entry(
            author=args.author,
            topic=args.topic
        )
        print(f"Created: {log_path}")
        print("Open this file in your editor to fill in session details.")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    import sys
    main()
