#!/usr/bin/env python3
"""
save-chat-log.py - Automated GitHub Copilot Chat Transcript Saver

IMPORTANT: Run with the project's venv Python to ensure dependencies are available:
    .venv/bin/python save-chat-log.py --paste --with-summary --topic "your-topic"
    
Or use the convenience wrapper:
    python save-chat-log.py --paste --with-summary --topic "your-topic"
    (if .venv is activated)


This script creates timestamped chat log files integrated with Santiago-PM personal logs.
It provides a template for pasting Copilot chat transcripts.

Integration with F-027 Personal Log Manager:
- Raw transcripts saved to: santiago-pm/personal-logs/agents/raw-transcripts/
- Can optionally create summary log via personal_log_manager.py
- Linked via metadata for full provenance

Usage:
    python save-chat-log.py [--paste] [--auto] [--with-summary]

Options:
    --paste: Interactively prompt for transcript paste
    --auto: Attempt automatic transcript retrieval (if available)
    --with-summary: Also create summary log via F-027 tool (recommended)
"""

import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

def get_current_user():
    """Get the current git user name"""
    try:
        import subprocess
        result = subprocess.run(['git', 'config', 'user.name'],
                              capture_output=True, text=True, cwd='.')
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except:
        pass
    return "unknown"

def get_model_name():
    """Get the Copilot model name (hardcoded for now)"""
    return "Grok_Code_Fast_1"

def create_chat_log_directory():
    """Create the raw transcripts directory integrated with personal logs"""
    log_dir = Path("santiago-pm/personal-logs/agents/raw-transcripts")
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir

def generate_filename():
    """Generate timestamped filename with user and model info"""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    username = get_current_user()
    model = get_model_name()
    filename = f"{timestamp}-{username}-copilot-{model}-raw.md"
    return filename

def create_transcript_template(log_dir, filename):
    """Create a template file for the chat transcript"""
    filepath = log_dir / filename

    template_content = f"""# GitHub Copilot Chat Transcript
**Session:** {datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}
**User:** {get_current_user()}
**Copilot Model:** {get_model_name()}
**Status:** Template - Ready for transcript paste

## Instructions for Use

1. In VS Code, use the command: **GitHub Copilot: Chat Transcript**
2. This opens a readonly transcript of the current session
3. Copy the entire transcript content
4. Paste it below this instruction block
5. Save the file

## Raw Chat Transcript

[PASTE COPILOT CHAT TRANSCRIPT HERE]

---

*Note: If the session resets, the transcript resets too. This is the closest thing to "save raw history."*
"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(template_content)

    return filepath

def interactive_paste_mode(log_dir, filename):
    """Interactive mode for pasting transcript content"""
    filepath = log_dir / filename

    print("🔄 GitHub Copilot Chat Transcript Saver")
    print("=" * 50)
    print(f"📁 Creating file: {filepath}")
    print()
    print("📋 Instructions:")
    print("1. In VS Code, run: GitHub Copilot: Chat Transcript")
    print("2. Copy the entire transcript")
    print("3. Paste it below (press Ctrl+D when done):")
    print()
    print("-" * 50)

    try:
        # Read multiline input from user
        # Check if stdin is being piped (non-interactive)
        if not sys.stdin.isatty():
            # Non-interactive: read all stdin at once
            transcript_content = sys.stdin.read()
        else:
            # Interactive: read line by line until EOF
            lines = []
            while True:
                try:
                    line = input()
                    lines.append(line)
                except EOFError:
                    break
            transcript_content = '\n'.join(lines)

        # Create the full content
        full_content = f"""# GitHub Copilot Chat Transcript
**Session:** {datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}
**User:** {get_current_user()}
**Copilot Model:** {get_model_name()}
**Status:** Saved - Transcript included

## Raw Chat Transcript

{transcript_content}

---

*Note: If the session resets, the transcript resets too. This is the closest thing to "save raw history."*
"""

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_content)

        print(f"\n✅ Transcript saved to: {filepath}")
        print(f"📊 File size: {os.path.getsize(filepath)} bytes")

    except KeyboardInterrupt:
        print("\n❌ Operation cancelled")
        return False

    return True

def auto_retrieval_mode(log_dir, filename):
    """Attempt automatic transcript retrieval (placeholder for future API access)"""
    filepath = log_dir / filename

    print("🔄 Attempting automatic transcript retrieval...")
    print("⚠️  Note: Automatic retrieval not currently implemented")
    print("   This would require API access to Copilot chat history")
    print()

    # For now, just create the template
    template_filepath = create_transcript_template(log_dir, filename)

    print(f"📝 Template created: {template_filepath}")
    print("📋 Please manually paste the transcript using:")
    print("   python save-chat-log.py --paste")

    return template_filepath

def main():
    parser = argparse.ArgumentParser(
        description="Save GitHub Copilot chat transcripts to timestamped files"
    )
    parser.add_argument(
        '--paste',
        action='store_true',
        help='Interactively prompt for transcript paste'
    )
    parser.add_argument(
        '--auto',
        action='store_true',
        help='Attempt automatic transcript retrieval (not implemented)'
    )
    parser.add_argument(
        '--with-summary',
        action='store_true',
        help='Also create summary log via F-027 personal_log_manager (recommended)'
    )
    parser.add_argument(
        '--topic',
        type=str,
        default='session',
        help='Session topic for filename (e.g., "feature-prioritization")'
    )

    args = parser.parse_args()

    # Create directory
    log_dir = create_chat_log_directory()

    # Generate filename
    filename = generate_filename()

    print(f"📁 Log directory: {log_dir.absolute()}")
    print(f"📄 Filename: {filename}")

    if args.paste:
        # Interactive paste mode
        success = interactive_paste_mode(log_dir, filename)
        if success:
            print("\n🎉 Raw chat log saved successfully!")
            
            # Optionally create summary log
            if args.with_summary:
                print("\n🔄 Creating summary log via F-027...")
                try:
                    from src.nusy_pm_core.adapters.personal_log_manager import PersonalLogManager
                    manager = PersonalLogManager(Path.cwd())
                    
                    # Read the raw transcript we just saved
                    raw_transcript = (log_dir / filename).read_text()
                    
                    # Extract agent name and date from filename
                    # Format: YYYY-MM-DD_HH-MM-SS-{username}-copilot-{model}-raw.md
                    parts = filename.split('-')
                    session_date = parts[0]  # YYYY-MM-DD
                    agent_name = f"{parts[4]}-{parts[5]}"  # copilot-{model}
                    
                    # Create summary log
                    summary_path = manager.save_chat_history(
                        conversation=raw_transcript,
                        agent_name=agent_name,
                        session_date=session_date,
                        topic=args.topic
                    )
                    
                    print(f"✅ Summary log created: {summary_path}")
                    print(f"   Raw transcript linked in metadata")
                except Exception as e:
                    print(f"⚠️  Could not create summary log: {e}")
                    print("   Raw transcript still saved successfully")
        else:
            print("\n❌ Failed to save chat log")
            sys.exit(1)
    elif args.auto:
        # Auto retrieval mode (placeholder)
        filepath = auto_retrieval_mode(log_dir, filename)
        print(f"\n📋 Template ready: {filepath}")
    else:
        # Default: create template
        filepath = create_transcript_template(log_dir, filename)
        print(f"📝 Template created: {filepath}")
        print("\n💡 To paste transcript interactively, run:")
        print("   python save-chat-log.py --paste")
        print("\n💡 To attempt auto-retrieval (future feature), run:")
        print("   python save-chat-log.py --auto")

if __name__ == "__main__":
    main()