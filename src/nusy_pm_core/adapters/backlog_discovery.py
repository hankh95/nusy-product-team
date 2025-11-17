"""
Continuous Backlog Discovery (F-029 Phase 1)

Automated scanning of personal logs, ships logs, and cargo manifests
for new work items. Implements semantic extraction, duplicate detection,
and continuous grooming workflow.

Author: Copilot Claude (Autonomous Execution)
Created: 2025-11-17
Feature ID: F-029
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import re
import yaml


@dataclass
class DiscoveredItem:
    """
    Represents a work item discovered from source documents.
    
    Attributes:
        id: Unique identifier (generated)
        title: Short description of the work
        description: Full context from source
        source_file: Path to file where discovered
        source_type: Type of source (personal_log, ships_log, cargo_manifest)
        discovered_at: Timestamp of discovery
        confidence: How confident we are this is a real work item (0.0-1.0)
        category: Type of work (feature, bug, improvement, research, etc.)
        related_items: IDs of similar/related items
        metadata: Additional context (author, tags, links, etc.)
    """
    id: str
    title: str
    description: str
    source_file: Path
    source_type: str
    discovered_at: datetime
    confidence: float
    category: str
    related_items: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'source_file': str(self.source_file),
            'source_type': self.source_type,
            'discovered_at': self.discovered_at.isoformat(),
            'confidence': self.confidence,
            'category': self.category,
            'related_items': self.related_items,
            'metadata': self.metadata
        }


@dataclass
class ScanResult:
    """
    Results from scanning a source for work items.
    
    Attributes:
        source: Path to scanned file/directory
        items_found: Number of new items discovered
        items: List of discovered items
        scan_duration_seconds: How long the scan took
        errors: Any errors encountered during scanning
    """
    source: Path
    items_found: int
    items: List[DiscoveredItem]
    scan_duration_seconds: float
    errors: List[str] = field(default_factory=list)


class PersonalLogScanner:
    """
    Scans personal logs (human and agent) for work items.
    
    Detects patterns like:
    - "NEW FEATURE: ..."
    - "need to build ..."
    - "should implement ..."
    - "discovered that ..."
    - "pain point: ..."
    """
    
    WORK_PATTERNS = [
        # Explicit feature markers
        (r'(?i)NEW FEATURE:?\s*(.+?)(?:\n|$)', 'feature', 0.95),
        (r'(?i)FEATURE IDEA:?\s*(.+?)(?:\n|$)', 'feature', 0.90),
        (r'(?i)DISCOVERED FEATURE:?\s*(.+?)(?:\n|$)', 'feature', 0.90),
        
        # Intent markers
        (r'(?i)(?:we|I|should)\s+(?:need to|should|could)\s+build\s+(.+?)(?:\n|\.)', 'feature', 0.80),
        (r'(?i)(?:we|I|should)\s+(?:need to|should|could)\s+implement\s+(.+?)(?:\n|\.)', 'feature', 0.80),
        (r'(?i)(?:we|I|should)\s+(?:need to|should|could)\s+create\s+(.+?)(?:\n|\.)', 'feature', 0.80),
        
        # Pain points
        (r'(?i)PAIN POINT:?\s*(.+?)(?:\n|$)', 'improvement', 0.85),
        (r'(?i)struggling with\s+(.+?)(?:\n|\.)', 'improvement', 0.75),
        (r'(?i)(?:it|this)\s+(?:is|was)\s+(?:hard|difficult|painful)\s+to\s+(.+?)(?:\n|\.)', 'improvement', 0.70),
        
        # Discoveries
        (r'(?i)DISCOVERED:?\s*(.+?)(?:\n|$)', 'research', 0.80),
        (r'(?i)learned that\s+(.+?)(?:\n|\.)', 'research', 0.75),
        (r'(?i)found out\s+(.+?)(?:\n|\.)', 'research', 0.75),
        
        # Questions (often indicate missing capabilities)
        (r'(?i)(?:how|what|why|when|where)\s+(?:can|do|should)\s+(?:we|I)\s+(.+?)\?', 'research', 0.65),
    ]
    
    def __init__(self, logs_directory: Path):
        """
        Initialize scanner with personal logs directory.
        
        Args:
            logs_directory: Path to santiago-pm/personal-logs/
        """
        self.logs_dir = logs_directory
        self.agent_logs_dir = logs_directory / "agents"
        self.human_logs_dir = logs_directory / "humans"
    
    def scan_all_logs(self) -> ScanResult:
        """
        Scan all personal logs (agents + humans) for work items.
        
        Returns:
            ScanResult with all discovered items
        """
        start_time = datetime.now()
        all_items = []
        errors = []
        
        # Scan agent logs
        if self.agent_logs_dir.exists():
            for log_file in self.agent_logs_dir.glob("*.md"):
                try:
                    items = self._scan_log_file(log_file, "personal_log_agent")
                    all_items.extend(items)
                except Exception as e:
                    errors.append(f"Error scanning {log_file}: {e}")
        
        # Scan human logs
        if self.human_logs_dir.exists():
            for log_file in self.human_logs_dir.glob("*.md"):
                try:
                    items = self._scan_log_file(log_file, "personal_log_human")
                    all_items.extend(items)
                except Exception as e:
                    errors.append(f"Error scanning {log_file}: {e}")
        
        duration = (datetime.now() - start_time).total_seconds()
        
        return ScanResult(
            source=self.logs_dir,
            items_found=len(all_items),
            items=all_items,
            scan_duration_seconds=duration,
            errors=errors
        )
    
    def _scan_log_file(self, log_path: Path, source_type: str) -> List[DiscoveredItem]:
        """
        Scan a single log file for work items.
        
        Args:
            log_path: Path to log file
            source_type: Type (personal_log_agent or personal_log_human)
        
        Returns:
            List of discovered items
        """
        content = log_path.read_text(encoding='utf-8')
        items = []
        
        # Extract metadata from YAML frontmatter (if present)
        metadata = self._extract_yaml_frontmatter(content)
        
        # Apply each pattern
        for pattern, category, confidence in self.WORK_PATTERNS:
            matches = re.finditer(pattern, content, re.MULTILINE)
            for match in matches:
                title = match.group(1).strip()
                
                # Skip if too short or too long
                if len(title) < 10 or len(title) > 200:
                    continue
                
                # Generate unique ID
                item_id = self._generate_item_id(title, log_path)
                
                # Extract surrounding context (3 lines before/after)
                context = self._extract_context(content, match.start(), match.end())
                
                item = DiscoveredItem(
                    id=item_id,
                    title=title,
                    description=context,
                    source_file=log_path,
                    source_type=source_type,
                    discovered_at=datetime.now(),
                    confidence=confidence,
                    category=category,
                    metadata={
                        **metadata,
                        'pattern_matched': pattern,
                        'match_position': match.start()
                    }
                )
                items.append(item)
        
        return items
    
    def _extract_yaml_frontmatter(self, content: str) -> Dict[str, Any]:
        """
        Extract YAML frontmatter from markdown content.
        
        Args:
            content: Full file content
        
        Returns:
            Dictionary of metadata fields (JSON-serializable)
        """
        # Match YAML frontmatter (between --- delimiters)
        pattern = r'^---\s*\n(.*?)\n---\s*\n'
        match = re.search(pattern, content, re.DOTALL | re.MULTILINE)
        
        if match:
            try:
                metadata = yaml.safe_load(match.group(1)) or {}
                # Convert dates to ISO strings for JSON serialization
                return self._sanitize_metadata(metadata)
            except yaml.YAMLError:
                return {}
        
        return {}
    
    def _sanitize_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert metadata to JSON-serializable format.
        
        Args:
            metadata: Raw metadata dictionary
        
        Returns:
            Sanitized metadata (all values JSON-serializable)
        """
        sanitized = {}
        for key, value in metadata.items():
            if isinstance(value, (datetime, )):
                sanitized[key] = value.isoformat()
            elif hasattr(value, 'isoformat'):  # date, time objects
                sanitized[key] = value.isoformat()
            elif isinstance(value, dict):
                sanitized[key] = self._sanitize_metadata(value)
            elif isinstance(value, list):
                sanitized[key] = [self._sanitize_metadata(v) if isinstance(v, dict) else v for v in value]
            else:
                sanitized[key] = value
        return sanitized
    
    def _extract_context(self, content: str, start: int, end: int, lines: int = 3) -> str:
        """
        Extract surrounding context for a match.
        
        Args:
            content: Full file content
            start: Start position of match
            end: End position of match
            lines: Number of lines before/after to include
        
        Returns:
            Context string with match and surrounding lines
        """
        # Split content into lines
        all_lines = content.split('\n')
        
        # Find line number of match
        chars_before = content[:start]
        match_line = chars_before.count('\n')
        
        # Extract context lines
        start_line = max(0, match_line - lines)
        end_line = min(len(all_lines), match_line + lines + 1)
        
        context_lines = all_lines[start_line:end_line]
        return '\n'.join(context_lines)
    
    def _generate_item_id(self, title: str, source_file: Path) -> str:
        """
        Generate a unique ID for a discovered item.
        
        Format: DI-<source>-<hash>
        Example: DI-agent-a3f9c2
        
        Args:
            title: Item title
            source_file: Path to source file
        
        Returns:
            Unique item ID
        """
        # Create hash from title + filename
        import hashlib
        content = f"{title}{source_file.name}"
        hash_hex = hashlib.sha256(content.encode()).hexdigest()[:6]
        
        # Determine source prefix
        if 'agents' in str(source_file):
            prefix = 'agent'
        elif 'humans' in str(source_file):
            prefix = 'human'
        else:
            prefix = 'log'
        
        return f"DI-{prefix}-{hash_hex}"


class DuplicateDetector:
    """
    Detects duplicate or similar work items.
    
    Uses simple text similarity for Phase 1. Phase 2 will add
    embedding-based semantic similarity.
    """
    
    def __init__(self, similarity_threshold: float = 0.85):
        """
        Initialize detector with similarity threshold.
        
        Args:
            similarity_threshold: Minimum similarity to consider duplicate (0.0-1.0)
        """
        self.threshold = similarity_threshold
    
    def find_duplicates(self, items: List[DiscoveredItem]) -> Dict[str, List[str]]:
        """
        Find duplicate items in a list.
        
        Args:
            items: List of discovered items to check
        
        Returns:
            Dictionary mapping item IDs to lists of duplicate IDs
        """
        duplicates = {}
        
        for i, item1 in enumerate(items):
            similar_items = []
            
            for j, item2 in enumerate(items):
                if i >= j:  # Skip self and already compared pairs
                    continue
                
                similarity = self._calculate_similarity(item1.title, item2.title)
                
                if similarity >= self.threshold:
                    similar_items.append(item2.id)
            
            if similar_items:
                duplicates[item1.id] = similar_items
        
        return duplicates
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate text similarity between two strings.
        
        Uses Jaccard similarity on word sets for Phase 1.
        Phase 2 will use embeddings.
        
        Args:
            text1: First text
            text2: Second text
        
        Returns:
            Similarity score (0.0-1.0)
        """
        # Normalize texts
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        # Jaccard similarity
        intersection = words1 & words2
        union = words1 | words2
        
        if not union:
            return 0.0
        
        return len(intersection) / len(union)


class BacklogDiscoveryManager:
    """
    Main interface for continuous backlog discovery workflow.
    
    Coordinates scanning, duplicate detection, and integration
    with prioritization system.
    """
    
    def __init__(self, workspace_root: Path):
        """
        Initialize manager with workspace root.
        
        Args:
            workspace_root: Root directory of the workspace
        """
        self.workspace_root = workspace_root
        self.logs_dir = workspace_root / "santiago-pm" / "personal-logs"
        
        # Initialize components
        self.scanner = PersonalLogScanner(self.logs_dir)
        self.duplicate_detector = DuplicateDetector(similarity_threshold=0.85)
    
    def discover_new_items(self) -> Dict[str, Any]:
        """
        Run full discovery workflow:
        1. Scan all sources
        2. Detect duplicates
        3. Return results for prioritization
        
        Returns:
            Dictionary with scan results, duplicates, and next actions
        """
        # Scan for new items
        scan_result = self.scanner.scan_all_logs()
        
        # Detect duplicates
        duplicates = self.duplicate_detector.find_duplicates(scan_result.items)
        
        # Organize results
        results = {
            'scan': {
                'sources_scanned': str(scan_result.source),
                'items_found': scan_result.items_found,
                'duration_seconds': scan_result.scan_duration_seconds,
                'errors': scan_result.errors
            },
            'items': [item.to_dict() for item in scan_result.items],
            'duplicates': duplicates,
            'summary': {
                'total_items': len(scan_result.items),
                'duplicate_clusters': len(duplicates),
                'unique_items': len(scan_result.items) - sum(len(dups) for dups in duplicates.values()),
                'by_category': self._count_by_category(scan_result.items),
                'by_source': self._count_by_source(scan_result.items)
            }
        }
        
        return results
    
    def _count_by_category(self, items: List[DiscoveredItem]) -> Dict[str, int]:
        """Count items by category."""
        counts = {}
        for item in items:
            counts[item.category] = counts.get(item.category, 0) + 1
        return counts
    
    def _count_by_source(self, items: List[DiscoveredItem]) -> Dict[str, int]:
        """Count items by source type."""
        counts = {}
        for item in items:
            counts[item.source_type] = counts.get(item.source_type, 0) + 1
        return counts


def main():
    """CLI interface for testing discovery workflow."""
    import sys
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python backlog_discovery.py <workspace_root>")
        sys.exit(1)
    
    workspace_root = Path(sys.argv[1])
    
    print(f"🔍 Starting backlog discovery in: {workspace_root}\n")
    
    # Initialize manager
    manager = BacklogDiscoveryManager(workspace_root)
    
    # Run discovery
    results = manager.discover_new_items()
    
    # Display results
    print("📊 Discovery Results:")
    print(f"  Sources scanned: {results['scan']['sources_scanned']}")
    print(f"  Items found: {results['scan']['items_found']}")
    print(f"  Duration: {results['scan']['duration_seconds']:.2f}s")
    
    if results['scan']['errors']:
        print(f"\n⚠️  Errors:")
        for error in results['scan']['errors']:
            print(f"    {error}")
    
    print(f"\n📦 Summary:")
    print(f"  Total items: {results['summary']['total_items']}")
    print(f"  Unique items: {results['summary']['unique_items']}")
    print(f"  Duplicate clusters: {results['summary']['duplicate_clusters']}")
    
    print(f"\n📂 By Category:")
    for category, count in results['summary']['by_category'].items():
        print(f"    {category}: {count}")
    
    print(f"\n📁 By Source:")
    for source, count in results['summary']['by_source'].items():
        print(f"    {source}: {count}")
    
    if results['duplicates']:
        print(f"\n🔗 Duplicates Detected:")
        for item_id, duplicates in results['duplicates'].items():
            print(f"    {item_id} → {', '.join(duplicates)}")
    
    # Show first 3 items
    if results['items']:
        print(f"\n💡 Sample Items (first 3):")
        for i, item in enumerate(results['items'][:3], 1):
            print(f"\n  {i}. [{item['category']}] {item['title']}")
            print(f"     Confidence: {item['confidence']:.2f}")
            print(f"     Source: {Path(item['source_file']).name}")
            print(f"     ID: {item['id']}")
    
    # Save full results to JSON
    output_file = workspace_root / "santiago-pm" / "discovery-results.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(results, indent=2))
    print(f"\n✅ Full results saved to: {output_file}")


if __name__ == "__main__":
    main()
