"""
Santiago Expert CLI - Human Q&A Interface
==========================================
Command-line interface for querying santiago-pm domain knowledge.

Uses the same validated neurosymbolic reasoner as BDD test executor,
providing human-friendly answers with provenance and confidence.

Usage:
    santiago-expert "What are the PM tools?"
    santiago-expert "How do I track task progress?"
    santiago-expert "What is the artifact-driven workflow?"

Architecture:
- Same reasoner as BDD executor (100% validated)
- Returns: answer + provenance + confidence
- Sources: KG + document fallback
- Interactive mode: Ask follow-up questions
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional
import argparse

# Add src to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from domain.src.nusy_pm_core.adapters.kg_store import KGStore
from domain.src.nusy_pm_core.santiago_core_bdd_executor import SantiagoCoreNeurosymbolicReasoner


class SantiagoExpert:
    """
    Santiago domain expert Q&A interface.
    Uses validated neurosymbolic reasoner for PM domain questions.
    """
    
    def __init__(self, workspace_path: Optional[Path] = None):
        """Initialize Santiago expert with KG and reasoner."""
        self.workspace_path = workspace_path or project_root
        
        # Load KG
        print("🔄 Loading santiago-pm knowledge graph...")
        self.kg_store = KGStore(workspace_path=str(self.workspace_path))
        stats = self.kg_store.get_statistics()
        print(f"✅ Loaded {stats.total_triples:,} triples")
        
        # Initialize reasoner (same as BDD executor - 100% validated)
        self.reasoner = SantiagoCoreNeurosymbolicReasoner(
            workspace_path=self.workspace_path
        )
        print(f"✅ Santiago domain expert ready\n")
    
    def ask(self, question: str, confidence_threshold: float = 0.5) -> Dict[str, Any]:
        """
        Ask Santiago a question about PM domain.
        
        Args:
            question: Natural language question
            confidence_threshold: Minimum confidence (0.0-1.0)
            
        Returns:
            Dictionary with answer, confidence, sources, evidence
        """
        result = self.reasoner.query_graph(
            question=question,
            kg_store=self.kg_store,
            confidence_threshold=confidence_threshold
        )
        
        # Handle None result
        if result is None:
            return {
                'confidence': 0.0,
                'passed': False,
                'triples': 0,
                'doc_matches': 0,
                'knowledge_sources': [],
                'keywords_used': [],
                'entities': []
            }
        
        return result
    
    def format_answer(self, question: str, result: Dict[str, Any]) -> str:
        """Format answer for human-friendly display."""
        lines = []
        
        # Question
        lines.append(f"❓ Question: {question}")
        lines.append("")
        
        # Confidence & Status
        confidence = result.get('confidence', 0.0)
        passed = result.get('passed', False)
        status = "✅ HIGH CONFIDENCE" if passed else "⚠️  LOW CONFIDENCE"
        lines.append(f"{status}")
        lines.append(f"Confidence: {confidence:.1%}")
        lines.append("")
        
        # Evidence
        kg_triples = result.get('triples', 0)
        doc_matches = result.get('doc_matches', 0)
        
        if kg_triples > 0 or doc_matches > 0:
            lines.append("📊 Evidence Found:")
            if kg_triples > 0:
                lines.append(f"  • {kg_triples} knowledge graph triples")
            if doc_matches > 0:
                lines.append(f"  • {doc_matches} document matches")
            lines.append("")
        
        # Sources (Provenance)
        sources = result.get('knowledge_sources', [])
        if sources:
            lines.append("📚 Sources:")
            for source in sources[:5]:  # Top 5 sources
                lines.append(f"  • {source}")
            if len(sources) > 5:
                lines.append(f"  • ... and {len(sources) - 5} more")
            lines.append("")
        
        # Keywords Used
        keywords = result.get('keywords_used', [])
        if keywords:
            lines.append(f"🔑 Keywords: {', '.join(keywords[:10])}")
            lines.append("")
        
        # Answer interpretation
        if not passed:
            lines.append("💡 Answer: Insufficient evidence found.")
            lines.append("   Try rephrasing your question or asking about a different topic.")
        else:
            lines.append("💡 Answer: Found strong evidence in knowledge base.")
            entities = result.get('entities', [])
            if entities:
                lines.append(f"   Related concepts: {len(entities)} entities discovered")
        
        return "\n".join(lines)
    
    def interactive(self):
        """Run interactive Q&A session."""
        print("🤖 Santiago Expert - Interactive Mode")
        print("=" * 70)
        print("Ask questions about santiago-pm domain.")
        print("Type 'exit' or 'quit' to end session.")
        print("=" * 70)
        print()
        
        while True:
            try:
                question = input("❓ Your question: ").strip()
                
                if not question:
                    continue
                
                if question.lower() in ['exit', 'quit', 'q']:
                    print("\n👋 Goodbye!")
                    break
                
                print()
                result = self.ask(question)
                formatted = self.format_answer(question, result)
                print(formatted)
                print()
                print("-" * 70)
                print()
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Santiago Expert - Domain Q&A Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  santiago-expert "What are the PM tools?"
  santiago-expert "How do I track task progress?"
  santiago-expert --interactive
        """
    )
    
    parser.add_argument(
        'question',
        nargs='?',
        help='Question to ask (omit for interactive mode)'
    )
    
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Start interactive Q&A session'
    )
    
    parser.add_argument(
        '-c', '--confidence',
        type=float,
        default=0.5,
        help='Minimum confidence threshold (0.0-1.0, default: 0.5)'
    )
    
    parser.add_argument(
        '-w', '--workspace',
        type=Path,
        help='Workspace path (default: current directory parent)'
    )
    
    args = parser.parse_args()
    
    # Initialize expert
    try:
        expert = SantiagoExpert(workspace_path=args.workspace)
    except Exception as e:
        print(f"❌ Failed to initialize Santiago: {e}")
        return 1
    
    # Interactive mode
    if args.interactive or not args.question:
        expert.interactive()
        return 0
    
    # Single question mode
    try:
        result = expert.ask(args.question, confidence_threshold=args.confidence)
        formatted = expert.format_answer(args.question, result)
        print(formatted)
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
