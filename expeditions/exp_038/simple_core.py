"""
Simple Santiago Core for EXP-038 - In-Memory Implementation
"""

import asyncio
from typing import Dict, List, Any
from enum import Enum
import time

class KnowledgeDomain(Enum):
    PRODUCT_MANAGEMENT = "product_management"
    SOFTWARE_ENGINEERING = "software_engineering" 
    SYSTEM_ARCHITECTURE = "system_architecture"
    TEAM_DYNAMICS = "team_dynamics"
    TECHNICAL_DEBT = "technical_debt"
    RISK_MANAGEMENT = "risk_management"
    KNOWLEDGE_MANAGEMENT = "knowledge_management"

class SantiagoCore:
    def __init__(self):
        self.knowledge: Dict[str, Dict[str, Any]] = {}
        self.domains: Dict[KnowledgeDomain, List[str]] = {
            domain: [] for domain in KnowledgeDomain
        }
        
    async def initialize_core(self) -> bool:
        """Initialize the core with basic knowledge."""
        # Add some core principles
        self.knowledge["core_1"] = {
            "domain": KnowledgeDomain.SYSTEM_ARCHITECTURE,
            "content": "Santiago Core is the central nervous system for autonomous development",
            "confidence": 1.0
        }
        self.domains[KnowledgeDomain.SYSTEM_ARCHITECTURE].append("core_1")
        
        self.knowledge["core_2"] = {
            "domain": KnowledgeDomain.SYSTEM_ARCHITECTURE, 
            "content": "The core unifies reasoning across all domains",
            "confidence": 1.0
        }
        self.domains[KnowledgeDomain.SYSTEM_ARCHITECTURE].append("core_2")
        
        return True
    
    async def load_domain_knowledge(self, domain: KnowledgeDomain, knowledge_data: Dict[str, Any]) -> int:
        """Load knowledge for a specific domain."""
        loaded = 0
        if "nodes" in knowledge_data:
            for node in knowledge_data["nodes"]:
                node_id = f"{domain.value}_{len(self.knowledge)}"
                self.knowledge[node_id] = {
                    "domain": domain,
                    "content": node.get("content", ""),
                    "confidence": node.get("confidence", 0.8)
                }
                self.domains[domain].append(node_id)
                loaded += 1
        return loaded
    
    async def reason(self, query: str, domain: KnowledgeDomain) -> Dict[str, Any]:
        """Perform reasoning on a query."""
        start_time = time.time()
        
        # Simple keyword matching
        relevant_knowledge = []
        query_words = set(query.lower().split())
        
        for node_id in self.domains[domain]:
            node = self.knowledge[node_id]
            content_words = set(node["content"].lower().split())
            overlap = len(query_words & content_words)
            if overlap > 0:
                relevant_knowledge.append((overlap, node))
        
        # Sort by relevance
        relevant_knowledge.sort(key=lambda x: x[0], reverse=True)
        
        # Generate answer
        if relevant_knowledge:
            top_knowledge = [node for _, node in relevant_knowledge[:3]]
            combined_content = " ".join([k["content"] for k in top_knowledge])
            answer = f"Based on knowledge: {combined_content[:200]}..."
            confidence = min(1.0, len(relevant_knowledge) * 0.2)
        else:
            answer = "No relevant knowledge found for this query"
            confidence = 0.0
        
        return {
            "answer": answer,
            "confidence": confidence,
            "execution_time": time.time() - start_time,
            "knowledge_used": len(relevant_knowledge)
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get core status."""
        return {
            "knowledge_nodes": len(self.knowledge),
            "domains": {d.value: len(nodes) for d, nodes in self.domains.items()},
            "health": "healthy" if len(self.knowledge) > 0 else "empty"
        }
