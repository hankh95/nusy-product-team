#!/usr/bin/env python3
"""
Knowledge Loading Script for Santiago-PM Domain

Loads PM knowledge from the Santiago-PM repository into Santiago Core
via the MCP service integration layer.
"""

import asyncio
import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
import json
import re
from datetime import datetime

# Add project paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "expeditions" / "exp_040"))
sys.path.insert(0, str(project_root / "expeditions" / "exp_038"))

from mcp_service_integration import IntegratedServiceRegistry, KnowledgeDomain, SantiagoCore
from mcp_service_layer import MCPRequest
import uuid


class PMKnowledgeLoader:
    """Loads PM knowledge from Santiago-PM repository into Santiago Core."""

    def __init__(self):
        # Create a shared SantiagoCore instance for loading and registry
        self.shared_santiago_core = SantiagoCore()
        self.registry = IntegratedServiceRegistry(santiago_core=self.shared_santiago_core)
        self.core_service = self.registry.get_service('santiago_core')
        self.santiago_pm_path = project_root / "santiago-pm"

        # Domain mapping based on directory structure
        self.domain_mapping = {
            'cargo-manifests': KnowledgeDomain.PRODUCT_MANAGEMENT,
            'ships-logs': KnowledgeDomain.PRODUCT_MANAGEMENT,
            'captains-journals': KnowledgeDomain.TEAM_DYNAMICS,
            'crew-manifests': KnowledgeDomain.TEAM_DYNAMICS,
            'issues': KnowledgeDomain.RISK_MANAGEMENT,
            'tasks': KnowledgeDomain.PRODUCT_MANAGEMENT,
            'research-logs': KnowledgeDomain.KNOWLEDGE_MANAGEMENT,
            'quality-assessments': KnowledgeDomain.RISK_MANAGEMENT,
            'strategic-charts': KnowledgeDomain.PRODUCT_MANAGEMENT,
            'prioritization-validation.json': KnowledgeDomain.PRODUCT_MANAGEMENT,
            'discovery-results.json': KnowledgeDomain.KNOWLEDGE_MANAGEMENT,
        }

    async def load_all_knowledge(self) -> Dict[str, int]:
        """Load all PM knowledge from the repository."""
        print("🚀 Starting PM knowledge loading into Santiago Core...")

        total_loaded = {}

        # Load knowledge from each domain directory
        for dir_name, domain in self.domain_mapping.items():
            dir_path = self.santiago_pm_path / dir_name
            if dir_path.exists() and dir_path.is_dir():
                print(f"📁 Loading from {dir_name} → {domain.value}")
                loaded = await self.load_directory_knowledge(dir_path, domain)
                total_loaded[dir_name] = loaded
                print(f"✅ Loaded {loaded} nodes from {dir_name}")
            elif dir_name.endswith('.json') and (self.santiago_pm_path / dir_name).exists():
                # Handle JSON files
                json_file = self.santiago_pm_path / dir_name
                print(f"📄 Loading JSON file {dir_name} → {domain.value}")
                loaded = await self.load_json_file(json_file, domain)
                total_loaded[dir_name] = loaded
                print(f"✅ Loaded {loaded} nodes from {dir_name}")

        # Load additional knowledge sources
        print("🔍 Loading additional knowledge sources...")

        # Load from issues directory
        issues_path = self.santiago_pm_path / "issues"
        if issues_path.exists():
            loaded = await self.load_directory_knowledge(issues_path, KnowledgeDomain.RISK_MANAGEMENT)
            total_loaded['issues'] = loaded
            print(f"✅ Loaded {loaded} nodes from issues")

        # Load from tasks directory
        tasks_path = self.santiago_pm_path / "tasks"
        if tasks_path.exists():
            loaded = await self.load_directory_knowledge(tasks_path, KnowledgeDomain.PRODUCT_MANAGEMENT)
            total_loaded['tasks'] = loaded
            print(f"✅ Loaded {loaded} nodes from tasks")

        print("🎉 Knowledge loading complete!")
        print(f"📊 Total loaded: {sum(total_loaded.values())} nodes across {len(total_loaded)} sources")

        return total_loaded

    async def load_directory_knowledge(self, dir_path: Path, domain: KnowledgeDomain) -> int:
        """Load knowledge from all files in a directory."""
        total_loaded = 0

        for file_path in dir_path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in ['.md', '.txt', '.json']:
                try:
                    loaded = await self.load_file_knowledge(file_path, domain)
                    total_loaded += loaded
                except Exception as e:
                    print(f"⚠️ Error loading {file_path}: {e}")

        return total_loaded

    async def load_file_knowledge(self, file_path: Path, domain: KnowledgeDomain) -> int:
        """Load knowledge from a single file."""
        try:
            if file_path.suffix.lower() == '.json':
                return await self.load_json_file(file_path, domain)
            else:
                return await self.load_text_file(file_path, domain)
        except Exception as e:
            print(f"⚠️ Error processing {file_path}: {e}")
            return 0

    async def load_text_file(self, file_path: Path, domain: KnowledgeDomain) -> int:
        """Load knowledge from a text/markdown file."""
        try:
            content = file_path.read_text(encoding='utf-8')

            # Extract meaningful content chunks
            chunks = self.extract_content_chunks(content, str(file_path))

            # Load each chunk as a knowledge node
            loaded = 0
            for chunk in chunks:
                if chunk['content'].strip():
                    await self.load_knowledge_node(domain, chunk)
                    loaded += 1

            return loaded

        except Exception as e:
            print(f"⚠️ Error reading {file_path}: {e}")
            return 0

    async def load_json_file(self, file_path: Path, domain: KnowledgeDomain) -> int:
        """Load knowledge from a JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Handle different JSON structures
            if isinstance(data, dict):
                return await self.load_json_object(data, domain, str(file_path))
            elif isinstance(data, list):
                loaded = 0
                for item in data:
                    if isinstance(item, dict):
                        loaded += await self.load_json_object(item, domain, str(file_path))
                return loaded

            return 0

        except Exception as e:
            print(f"⚠️ Error reading JSON {file_path}: {e}")
            return 0

    async def load_json_object(self, data: Dict[str, Any], domain: KnowledgeDomain, source: str) -> int:
        """Load a JSON object as knowledge."""
        # Convert JSON to knowledge nodes
        content = json.dumps(data, indent=2)
        chunk = {
            'content': content,
            'confidence': 0.8,
            'source': source,
            'metadata': {'type': 'json_data'}
        }

        await self.load_knowledge_node(domain, chunk)
        return 1

    def extract_content_chunks(self, content: str, source: str) -> List[Dict[str, Any]]:
        """Extract meaningful content chunks from text."""
        chunks = []

        # Split by headers for markdown files
        if content.startswith('#'):
            sections = re.split(r'^#+\s+', content, flags=re.MULTILINE)
            for section in sections:
                if section.strip():
                    chunks.append({
                        'content': section.strip(),
                        'confidence': 0.7,
                        'source': source,
                        'metadata': {'type': 'markdown_section'}
                    })
        else:
            # For non-markdown, split by paragraphs or fixed size
            paragraphs = content.split('\n\n')
            for para in paragraphs:
                if len(para.strip()) > 50:  # Only meaningful paragraphs
                    chunks.append({
                        'content': para.strip(),
                        'confidence': 0.6,
                        'source': source,
                        'metadata': {'type': 'text_paragraph'}
                    })

        return chunks

    async def load_knowledge_node(self, domain: KnowledgeDomain, node_data: Dict[str, Any]):
        """Load a single knowledge node via MCP service."""
        request = MCPRequest(
            id=str(uuid.uuid4()),
            method='execute',
            params={
                'operation': 'load_knowledge',
                'params': {
                    'domain': domain.value,
                    'knowledge_data': {
                        'nodes': [node_data]
                    }
                }
            },
            timestamp=datetime.now(),
            client_id='knowledge_loader'
        )

        response = await self.core_service.invoke(request)

        if response.error:
            print(f"❌ Error loading knowledge: {response.error}")
        elif not response.result.get('success', False):
            print(f"⚠️ Failed to load knowledge node: {response.result}")

    async def verify_loading(self) -> Dict[str, Any]:
        """Verify that knowledge was loaded successfully."""
        print("🔍 Verifying knowledge loading...")

        request = MCPRequest(
            id=str(uuid.uuid4()),
            method='execute',
            params={'operation': 'get_status', 'params': {}},
            timestamp=datetime.now(),
            client_id='verifier'
        )

        response = await self.core_service.invoke(request)

        if response.result and response.result.get('success'):
            status = response.result.get('status', {})
            print(f"📊 Core status: {status}")
            return status
        else:
            print(f"❌ Failed to get status: {response.error}")
            return {}


async def main():
    """Main knowledge loading execution."""
    print("🧠 Santiago-PM Knowledge Loading System")
    print("=" * 50)

    loader = PMKnowledgeLoader()

    try:
        # Load all knowledge
        results = await loader.load_all_knowledge()

        print("\n📈 Loading Results:")
        for source, count in results.items():
            print(f"  {source}: {count} nodes")

        # Verify loading
        print("\n" + "=" * 50)
        status = await loader.verify_loading()

        print("\n✅ Knowledge loading completed successfully!")
        print(f"🎯 Total knowledge nodes: {status.get('knowledge_nodes', 0)}")
        print(f"🗂️ Domains populated: {list(status.get('domains', {}).keys())}")

    except Exception as e:
        print(f"❌ Error during knowledge loading: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())