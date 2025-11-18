#!/usr/bin/env python3
"""
QA Integration Service for Santiago-Dev

Provides local-first QA capabilities with knowledge graph and git analysis.
"""

import os
import json
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime


class QAIntegrationService:
    """
    QA Integration Service with local-first approach.
    """

    def __init__(self, workspace_path: Path):
        self.workspace_path = Path(workspace_path)
        self.features_path = workspace_path / "cargo-manifests"  # Santiago-PM uses cargo-manifests
        self.knowledge_graph = self._load_knowledge_graph()

    def _load_knowledge_graph(self) -> Dict[str, Any]:
        """Load or create knowledge graph of local artifacts."""
        kg_file = self.workspace_path / "knowledge_graph.json"
        if kg_file.exists():
            try:
                with open(kg_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass

        # Create initial knowledge graph
        return {
            'artifacts': {},
            'features': {},
            'last_updated': datetime.now().isoformat()
        }

    def _save_knowledge_graph(self):
        """Save knowledge graph to file."""
        kg_file = self.workspace_path / "knowledge_graph.json"
        try:
            with open(kg_file, 'w') as f:
                json.dump(self.knowledge_graph, f, indent=2, default=str)
        except Exception as e:
            print(f"⚠️ Failed to save knowledge graph: {e}")

    def index_workspace_artifacts(self):
        """Index all workspace artifacts for local QA."""
        print("🔍 Indexing workspace artifacts...")

        artifacts = {}

        # Index feature files
        if self.features_path.exists():
            for feature_file in self.features_path.glob("*.feature"):
                try:
                    with open(feature_file, 'r') as f:
                        content = f.read()
                        artifacts[str(feature_file)] = {
                            'type': 'feature',
                            'content': content,
                            'indexed_at': datetime.now().isoformat()
                        }
                except Exception as e:
                    print(f"⚠️ Failed to index {feature_file}: {e}")

        # Index Python files
        for py_file in self.workspace_path.rglob("*.py"):
            try:
                with open(py_file, 'r') as f:
                    content = f.read()
                    artifacts[str(py_file)] = {
                        'type': 'python_code',
                        'content': content,
                        'indexed_at': datetime.now().isoformat()
                    }
            except Exception as e:
                print(f"⚠️ Failed to index {py_file}: {e}")

        self.knowledge_graph['artifacts'] = artifacts
        self.knowledge_graph['last_updated'] = datetime.now().isoformat()
        self._save_knowledge_graph()

        print(f"✅ Indexed {len(artifacts)} artifacts")

    def get_next_prioritized_feature(self) -> Optional[Dict[str, Any]]:
        """Get the next highest priority feature to work on."""
        features = self._discover_features()

        if not features:
            return None

        # Sort by priority (critical > high > medium > low)
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}

        sorted_features = sorted(
            features,
            key=lambda f: priority_order.get(f.get('priority', 'medium'), 2)
        )

        return sorted_features[0] if sorted_features else None

    async def discover_features(self, topic: str) -> List[Dict[str, Any]]:
        """Discover features related to a specific topic."""
        # For now, return existing features - in future could generate new ones
        features = self._discover_features()
        
        # Filter by topic if possible
        if topic:
            topic_lower = topic.lower()
            filtered_features = []
            for feature in features:
                content = feature.get('content', '').lower()
                name = feature.get('name', '').lower()
                if topic_lower in content or topic_lower in name:
                    filtered_features.append(feature)
            return filtered_features
        
        return features

    def _discover_features(self) -> List[Dict[str, Any]]:
        """Discover all available features from workspace."""
        features = []

        if not self.features_path.exists():
            return features

        for feature_file in self.features_path.glob("*.feature"):
            try:
                feature_data = self._parse_feature_file(feature_file)
                if feature_data:
                    features.append(feature_data)
            except Exception as e:
                print(f"⚠️ Failed to parse feature {feature_file}: {e}")

        return features

    def _parse_feature_file(self, feature_file: Path) -> Optional[Dict[str, Any]]:
        """Parse a Gherkin feature file."""
        try:
            with open(feature_file, 'r') as f:
                content = f.read()

            # Skip completed features
            if '@completed' in content:
                return None

            lines = content.split('\n')
            feature_name = ""
            priority = "medium"
            scenarios = []

            i = 0
            while i < len(lines):
                line = lines[i].strip()

                if line.startswith('Feature:'):
                    feature_name = line.replace('Feature:', '').strip()
                elif 'priority:' in line.lower():
                    # Extract priority from comments or tags
                    if 'critical' in line.lower():
                        priority = 'critical'
                    elif 'high' in line.lower():
                        priority = 'high'
                    elif 'low' in line.lower():
                        priority = 'low'
                elif line.startswith('Scenario:'):
                    scenario_name = line.replace('Scenario:', '').strip()
                    scenario_steps = []

                    # Collect scenario steps
                    i += 1
                    while i < len(lines) and not lines[i].strip().startswith('Scenario:'):
                        step_line = lines[i].strip()
                        if step_line.startswith(('Given', 'When', 'Then', 'And', 'But')):
                            scenario_steps.append(step_line)
                        i += 1
                    i -= 1  # Adjust for outer loop

                    scenarios.append({
                        'name': scenario_name,
                        'steps': scenario_steps
                    })

                i += 1

            if feature_name:
                return {
                    'name': feature_name,
                    'file': str(feature_file),
                    'priority': priority,
                    'scenarios': scenarios,
                    'content': content
                }

        except Exception as e:
            print(f"⚠️ Error parsing feature file {feature_file}: {e}")

        return None

    async def get_qa_guidance(self, question: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Get QA guidance for a question, using local knowledge first."""
        # Check local knowledge graph first
        local_answer = self._search_local_knowledge(question)
        if local_answer:
            return f"Local knowledge: {local_answer}"

        # If no local answer, provide general guidance
        return f"General guidance: {question} - Consider reviewing existing patterns and best practices."

    def _search_local_knowledge(self, question: str) -> Optional[str]:
        """Search local knowledge graph for relevant information."""
        question_lower = question.lower()

        # Search through indexed artifacts
        for artifact_path, artifact_data in self.knowledge_graph.get('artifacts', {}).items():
            content = artifact_data.get('content', '').lower()

            # Simple keyword matching
            if any(keyword in content for keyword in question_lower.split()):
                return f"Found relevant information in {Path(artifact_path).name}"

        return None

    def analyze_git_history(self) -> Dict[str, Any]:
        """Analyze git history for development patterns."""
        try:
            import subprocess

            # Get recent commits
            result = subprocess.run(
                ['git', 'log', '--oneline', '-10'],
                cwd=self.workspace_path,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                commits = result.stdout.strip().split('\n')
                return {
                    'recent_commits': len(commits),
                    'commit_messages': commits,
                    'patterns': self._analyze_commit_patterns(commits)
                }

        except Exception as e:
            print(f"⚠️ Git analysis failed: {e}")

        return {'error': 'Git analysis unavailable'}

    def _analyze_commit_patterns(self, commits: List[str]) -> Dict[str, Any]:
        """Analyze patterns in commit messages."""
        patterns = {
            'feature_additions': 0,
            'bug_fixes': 0,
            'refactoring': 0,
            'documentation': 0
        }

        for commit in commits:
            msg = commit.lower()
            if 'feat' in msg or 'add' in msg:
                patterns['feature_additions'] += 1
            elif 'fix' in msg or 'bug' in msg:
                patterns['bug_fixes'] += 1
            elif 'refactor' in msg:
                patterns['refactoring'] += 1
            elif 'doc' in msg:
                patterns['documentation'] += 1

        return patterns