"""
EXP-038: Knowledge Loader

Loads and synthesizes domain knowledge from Santiago-PM and NuSy prototypes
into the Santiago Core knowledge graph.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
import asyncio
from datetime import datetime

from .santiago_core import SantiagoCore, KnowledgeDomain, KnowledgeNode


class KnowledgeLoader:
    """
    Loads domain knowledge from various sources into Santiago Core.

    Supports loading from:
    - Santiago-PM domain knowledge
    - NuSy prototype knowledge structures
    - JSON knowledge bases
    - Text documents with metadata
    """

    def __init__(self, core: SantiagoCore):
        self.core = core
        self.loaded_sources: Dict[str, datetime] = {}

    async def load_santiago_pm_knowledge(self, knowledge_path: str) -> int:
        """
        Load knowledge from Santiago-PM domain.

        Args:
            knowledge_path: Path to Santiago-PM knowledge files

        Returns:
            Number of knowledge nodes loaded
        """
        total_loaded = 0

        try:
            pm_path = Path(knowledge_path)

            # Load product management principles
            pm_principles_file = pm_path / "product_management_principles.json"
            if pm_principles_file.exists():
                with open(pm_principles_file, 'r') as f:
                    principles_data = json.load(f)
                nodes_loaded = await self.core.load_domain_knowledge(
                    KnowledgeDomain.PRODUCT_MANAGEMENT, principles_data
                )
                total_loaded += nodes_loaded
                self.loaded_sources["santiago_pm_principles"] = datetime.now()

            # Load development workflow knowledge
            workflow_file = pm_path / "development_workflows.json"
            if workflow_file.exists():
                with open(workflow_file, 'r') as f:
                    workflow_data = json.load(f)
                nodes_loaded = await self.core.load_domain_knowledge(
                    KnowledgeDomain.SOFTWARE_ENGINEERING, workflow_data
                )
                total_loaded += nodes_loaded
                self.loaded_sources["santiago_pm_workflows"] = datetime.now()

            # Load risk management knowledge
            risk_file = pm_path / "risk_management.json"
            if risk_file.exists():
                with open(risk_file, 'r') as f:
                    risk_data = json.load(f)
                nodes_loaded = await self.core.load_domain_knowledge(
                    KnowledgeDomain.RISK_MANAGEMENT, risk_data
                )
                total_loaded += nodes_loaded
                self.loaded_sources["santiago_pm_risks"] = datetime.now()

            print(f"Loaded {total_loaded} nodes from Santiago-PM knowledge")

        except Exception as e:
            print(f"Failed to load Santiago-PM knowledge: {e}")

        return total_loaded

    async def load_nusy_prototype_knowledge(self, prototype_path: str) -> int:
        """
        Load knowledge from NuSy prototype structures.

        Args:
            prototype_path: Path to NuSy prototype knowledge

        Returns:
            Number of knowledge nodes loaded
        """
        total_loaded = 0

        try:
            nusy_path = Path(prototype_path)

            # Load neurosymbolic reasoning patterns
            reasoning_file = nusy_path / "neurosymbolic_patterns.json"
            if reasoning_file.exists():
                with open(reasoning_file, 'r') as f:
                    reasoning_data = json.load(f)
                nodes_loaded = await self.core.load_domain_knowledge(
                    KnowledgeDomain.SYSTEM_ARCHITECTURE, reasoning_data
                )
                total_loaded += nodes_loaded
                self.loaded_sources["nusy_reasoning_patterns"] = datetime.now()

            # Load knowledge representation schemas
            schema_file = nusy_path / "knowledge_schemas.json"
            if schema_file.exists():
                with open(schema_file, 'r') as f:
                    schema_data = json.load(f)
                nodes_loaded = await self.core.load_domain_knowledge(
                    KnowledgeDomain.SYSTEM_ARCHITECTURE, schema_data
                )
                total_loaded += nodes_loaded
                self.loaded_sources["nusy_knowledge_schemas"] = datetime.now()

            # Load learning mechanisms
            learning_file = nusy_path / "learning_mechanisms.json"
            if learning_file.exists():
                with open(learning_file, 'r') as f:
                    learning_data = json.load(f)
                nodes_loaded = await self.core.load_domain_knowledge(
                    KnowledgeDomain.SYSTEM_ARCHITECTURE, learning_data
                )
                total_loaded += nodes_loaded
                self.loaded_sources["nusy_learning_mechanisms"] = datetime.now()

            print(f"Loaded {total_loaded} nodes from NuSy prototype knowledge")

        except Exception as e:
            print(f"Failed to load NuSy prototype knowledge: {e}")

        return total_loaded

    async def load_json_knowledge_base(self, file_path: str,
                                     domain: KnowledgeDomain) -> int:
        """
        Load knowledge from a JSON knowledge base file.

        Args:
            file_path: Path to JSON knowledge file
            domain: Knowledge domain for the content

        Returns:
            Number of knowledge nodes loaded
        """
        try:
            with open(file_path, 'r') as f:
                knowledge_data = json.load(f)

            nodes_loaded = await self.core.load_domain_knowledge(domain, knowledge_data)
            self.loaded_sources[f"json_{Path(file_path).stem}"] = datetime.now()

            print(f"Loaded {nodes_loaded} nodes from {file_path}")
            return nodes_loaded

        except Exception as e:
            print(f"Failed to load JSON knowledge from {file_path}: {e}")
            return 0

    async def load_text_documents(self, documents: List[Dict[str, Any]],
                                domain: KnowledgeDomain) -> int:
        """
        Load knowledge from text documents with metadata.

        Args:
            documents: List of document dicts with 'content' and optional 'metadata'
            domain: Knowledge domain for the documents

        Returns:
            Number of knowledge nodes loaded
        """
        knowledge_data = {"documents": documents}
        nodes_loaded = await self.core.load_domain_knowledge(domain, knowledge_data)

        self.loaded_sources[f"text_docs_{domain.value}"] = datetime.now()
        print(f"Loaded {nodes_loaded} text documents for domain {domain.value}")

        return nodes_loaded

    async def synthesize_knowledge(self) -> int:
        """
        Synthesize knowledge across domains to create new insights.

        Returns:
            Number of new synthesized knowledge nodes
        """
        synthesized_nodes = 0

        try:
            # Find connections between domains
            cross_domain_connections = await self._find_cross_domain_connections()

            # Generate synthetic knowledge
            for connection in cross_domain_connections:
                synthetic_node = await self._create_synthetic_knowledge(connection)
                if synthetic_node:
                    self.core.knowledge_graph[synthetic_node.id] = synthetic_node
                    self.core.domain_indices[synthetic_node.domain].add(synthetic_node.id)
                    synthesized_nodes += 1

            print(f"Created {synthesized_nodes} synthetic knowledge nodes")

        except Exception as e:
            print(f"Knowledge synthesis failed: {e}")

        return synthesized_nodes

    def get_loading_status(self) -> Dict[str, Any]:
        """Get status of knowledge loading operations."""
        return {
            "loaded_sources": list(self.loaded_sources.keys()),
            "last_loaded": {k: v.isoformat() for k, v in self.loaded_sources.items()},
            "total_sources": len(self.loaded_sources),
            "core_status": self.core.get_core_status()
        }

    async def validate_loaded_knowledge(self) -> Dict[str, Any]:
        """Validate that loaded knowledge is accessible and usable."""
        validation_results = {
            "total_nodes": len(self.core.knowledge_graph),
            "domains_loaded": len(self.core.metrics.knowledge_domains),
            "reasoning_tests": []
        }

        # Test reasoning in each loaded domain
        for domain in self.core.metrics.knowledge_domains:
            try:
                from .santiago_core import ReasoningContext, ReasoningMode

                test_query = f"What are the key principles of {domain.value.replace('_', ' ')}?"
                context = ReasoningContext(
                    query=test_query,
                    domain=domain,
                    mode=ReasoningMode.SYMBOLIC
                )

                result = await self.core.reason(context)
                validation_results["reasoning_tests"].append({
                    "domain": domain.value,
                    "query": test_query,
                    "success": result.confidence > 0.5,
                    "confidence": result.confidence,
                    "nodes_used": len(result.reasoning_path)
                })
            except Exception as e:
                validation_results["reasoning_tests"].append({
                    "domain": domain.value,
                    "error": str(e)
                })

        return validation_results

    # Private helper methods

    async def _find_cross_domain_connections(self) -> List[Dict[str, Any]]:
        """Find connections between knowledge in different domains."""
        connections = []

        # Simple implementation - find nodes with similar content across domains
        all_nodes = list(self.core.knowledge_graph.values())

        for i, node1 in enumerate(all_nodes):
            for j, node2 in enumerate(all_nodes):
                if (i != j and node1.domain != node2.domain and
                    self.core._content_similarity(node1.content, node2.content) > 0.6):
                    connections.append({
                        "node1": node1,
                        "node2": node2,
                        "similarity": self.core._content_similarity(node1.content, node2.content)
                    })

        return connections[:10]  # Limit to top 10 connections

    async def _create_synthetic_knowledge(self, connection: Dict[str, Any]) -> Optional[KnowledgeNode]:
        """Create a synthetic knowledge node from a cross-domain connection."""
        node1 = connection["node1"]
        node2 = connection["node2"]

        # Create synthetic content combining both domains
        synthetic_content = f"Synthesis of {node1.domain.value} and {node2.domain.value}: {node1.content[:100]}... combined with {node2.content[:100]}..."

        synthetic_node = KnowledgeNode(
            id=f"synthetic_{node1.id}_{node2.id}",
            domain=KnowledgeDomain.SYSTEM_ARCHITECTURE,  # Synthetic knowledge goes to architecture
            content=synthetic_content,
            confidence=min(node1.confidence, node2.confidence) * 0.8,  # Slightly lower confidence
            metadata={
                "synthetic": True,
                "sources": [node1.id, node2.id],
                "domains": [node1.domain.value, node2.domain.value]
            }
        )

        return synthetic_node


async def initialize_knowledge_base(core: SantiagoCore,
                                  santiago_pm_path: Optional[str] = None,
                                  nusy_path: Optional[str] = None) -> KnowledgeLoader:
    """
    Initialize the knowledge base by loading from available sources.

    Args:
        core: The Santiago Core instance
        santiago_pm_path: Path to Santiago-PM knowledge (optional)
        nusy_path: Path to NuSy prototype knowledge (optional)

    Returns:
        Configured KnowledgeLoader instance
    """
    loader = KnowledgeLoader(core)

    # Load Santiago-PM knowledge if available
    if santiago_pm_path and os.path.exists(santiago_pm_path):
        await loader.load_santiago_pm_knowledge(santiago_pm_path)

    # Load NuSy prototype knowledge if available
    if nusy_path and os.path.exists(nusy_path):
        await loader.load_nusy_prototype_knowledge(nusy_path)

    # Create some basic fallback knowledge if nothing was loaded
    if len(core.knowledge_graph) == 0:
        print("No external knowledge sources found, loading basic fallback knowledge...")
        basic_knowledge = {
            "nodes": [
                {
                    "id": "basic_pm_1",
                    "content": "Product management involves balancing user needs, business goals, and technical feasibility",
                    "domain": "product_management"
                },
                {
                    "id": "basic_eng_1",
                    "content": "Software engineering requires careful planning, testing, and iterative improvement",
                    "domain": "software_engineering"
                },
                {
                    "id": "basic_arch_1",
                    "content": "System architecture should be modular, scalable, and maintainable",
                    "domain": "system_architecture"
                }
            ]
        }

        # Load basic knowledge into appropriate domains
        for node_data in basic_knowledge["nodes"]:
            domain_map = {
                "product_management": KnowledgeDomain.PRODUCT_MANAGEMENT,
                "software_engineering": KnowledgeDomain.SOFTWARE_ENGINEERING,
                "system_architecture": KnowledgeDomain.SYSTEM_ARCHITECTURE
            }
            domain = domain_map.get(node_data["domain"])
            if domain:
                await core.load_domain_knowledge(domain, {"nodes": [node_data]})

    # Synthesize knowledge across domains
    await loader.synthesize_knowledge()

    return loader</content>
<parameter name="filePath">/Users/hankhead/Projects/Personal/nusy-product-team/expeditions/exp_038/knowledge_loader.py