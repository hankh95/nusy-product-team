"""
EXP-040: Entity Specialization

Creates specialized Santiago entities: Santiago-PM, Santiago-Dev, and Santiago-Architect
with domain-specific knowledge, capabilities, and collaboration patterns.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
import asyncio
import uuid
from datetime import datetime

# Add EXP paths
exp_039_path = Path(__file__).parent.parent / "exp_039"
exp_040_path = Path(__file__).parent
sys.path.insert(0, str(exp_039_path))
sys.path.insert(0, str(exp_040_path))

try:
    from entity_architecture import SantiagoEntity, EntityIdentity, KnowledgeItem, Capability
    from capability_interfaces import CapabilityHub, KnowledgeQueryCapability, CollaborationCapability
    from mcp_service_integration import IntegratedServiceRegistry
except ImportError as e:
    print(f"Warning: Could not import required components: {e}")
    # Create minimal mocks for development
    class SantiagoEntity:
        def __init__(self, identity): self.identity = identity
        async def reason_and_act(self, goal): return {"result": "mock"}

    class CapabilityHub:
        def __init__(self): pass


class SantiagoPMEntity(SantiagoEntity):
    """
    Product Management Santiago Entity

    Focus: Feature prioritization, roadmap planning, stakeholder management
    Domain: Product strategy, user needs, business requirements
    """

    def __init__(self, service_registry: IntegratedServiceRegistry):
        identity = EntityIdentity(
            entity_id=f"santiago-pm-{uuid.uuid4().hex[:8]}",
            name="Santiago-PM",
            role="product_manager",
            expertise_domains=["product_management", "roadmap_planning", "stakeholder_management"],
            personality_traits={
                "strategic": 0.9,
                "user_focused": 0.8,
                "business_oriented": 0.9,
                "collaborative": 0.8
            },
            created_at=datetime.now(),
            reputation={
                "feature_prioritization": 0.9,
                "roadmap_planning": 0.8,
                "stakeholder_communication": 0.9
            }
        )

        super().__init__(identity)
        self.service_registry = service_registry
        self._initialize_knowledge()
        self._initialize_capabilities()

    def _initialize_knowledge(self):
        """Initialize product management domain knowledge."""

        pm_knowledge = [
            KnowledgeItem(
                id=f"pm_knowledge_{uuid.uuid4().hex[:8]}",
                domain="product_management",
                content={
                    "principles": [
                        "User-centered design",
                        "Data-driven decisions",
                        "MVP and iterative development",
                        "Feature prioritization frameworks (RICE, Kano, etc.)"
                    ],
                    "methodologies": ["Agile", "Scrum", "Kanban", "Lean Startup"],
                    "metrics": ["User engagement", "Conversion rates", "Feature adoption", "Customer satisfaction"]
                },
                confidence=0.9,
                source="product_management_best_practices",
                timestamp=datetime.now(),
                tags=["product", "strategy", "prioritization"]
            ),
            KnowledgeItem(
                id=f"pm_knowledge_{uuid.uuid4().hex[:8]}",
                domain="stakeholder_management",
                content={
                    "stakeholder_types": ["Users", "Developers", "Business stakeholders", "Executives"],
                    "communication_patterns": {
                        "users": "User research, feedback collection, usability testing",
                        "developers": "Requirements clarity, technical constraints, implementation feedback",
                        "business": "ROI analysis, market positioning, competitive analysis",
                        "executives": "Strategic alignment, high-level metrics, risk assessment"
                    }
                },
                confidence=0.8,
                source="stakeholder_management_guide",
                timestamp=datetime.now(),
                tags=["stakeholders", "communication", "management"]
            )
        ]

        for item in pm_knowledge:
            self.knowledge_base.add_knowledge(item)

    def _initialize_capabilities(self):
        """Initialize product management capabilities."""

        async def prioritize_features(goal):
            """Prioritize features using product management frameworks."""
            # Mock implementation for now
            return {
                "prioritized_features": [
                    {"feature": "User authentication", "priority": "High", "effort": "Medium"},
                    {"feature": "Dependency analysis", "priority": "High", "effort": "High"},
                    {"feature": "Security scanning", "priority": "Medium", "effort": "Medium"}
                ]
            }

        async def create_roadmap(goal):
            """Create product roadmap based on prioritized features."""
            # Mock implementation for now
            return {
                "roadmap": "Q1: User authentication and basic dependency analysis\nQ2: Advanced security scanning and reporting\nQ3: Performance optimizations and scalability"
            }

        async def analyze_requirements(goal):
            """Analyze and refine feature requirements."""
            # Mock implementation for now
            return {
                "analysis": {
                    "functional_requirements": ["User login", "Dependency scanning", "Report generation"],
                    "non_functional_requirements": ["Performance", "Security", "Usability"],
                    "risks": ["Complex dependency graphs", "Security vulnerabilities"],
                    "recommendations": ["Start with MVP", "Use established libraries"]
                }
            }

        async def ask_question(goal):
            """Ask questions to gather information and clarify requirements."""
            # Mock implementation for now - would use LLM service
            question_context = goal.description
            
            # Extract question from goal description
            if "question:" in question_context.lower():
                question = question_context.split("question:", 1)[1].strip()
            else:
                question = question_context
            
            return {
                "question": question,
                "answer": f"This is a mock answer to: {question}. In a real implementation, this would use the LLM service to provide detailed, contextual answers.",
                "confidence": 0.8,
                "sources": ["domain knowledge", "best practices", "similar projects"],
                "follow_up_questions": ["What are the specific constraints?", "Are there existing patterns to follow?"]
            }

        async def create_pr(goal):
            """Create a pull request for implemented features."""
            # Mock implementation for now - would integrate with PR workflow manager
            pr_details = goal.description
            
            return {
                "pr_created": True,
                "pr_number": f"PR-{uuid.uuid4().hex[:6]}",
                "title": f"Feature: {pr_details[:50]}...",
                "description": f"Implementation of: {pr_details}",
                "branch": f"feature/{uuid.uuid4().hex[:8]}",
                "status": "draft"
            }

        async def review_code(goal):
            """Review code changes and provide feedback."""
            # Mock implementation for now - would use LLM for code review
            return {
                "review_complete": True,
                "issues_found": 2,
                "comments": [
                    "Consider adding error handling for edge cases",
                    "Code follows good practices, minor style improvements suggested"
                ],
                "approval_recommended": True,
                "confidence": 0.85
            }

        async def manage_workflow(goal):
            """Manage PR workflows and track progress."""
            # Mock implementation for now - would integrate with PR workflow manager
            return {
                "workflow_active": True,
                "current_stage": "code_review",
                "progress": 75.0,
                "next_steps": ["Address review comments", "Run integration tests", "Merge PR"],
                "blockers": [],
                "estimated_completion": "2 days"
            }

        pm_capabilities = [
            Capability(
                name="feature_prioritization",
                description="Prioritize features using product management frameworks",
                interface=prioritize_features,
                execution_cost=0.3
            ),
            Capability(
                name="roadmap_planning",
                description="Create and maintain product roadmaps",
                interface=create_roadmap,
                execution_cost=0.4
            ),
            Capability(
                name="requirements_analysis",
                description="Analyze and refine feature requirements",
                interface=analyze_requirements,
                execution_cost=0.2
            ),
            Capability(
                name="question_asking",
                description="Ask questions to gather information and clarify requirements",
                interface=ask_question,
                execution_cost=0.1
            ),
            Capability(
                name="pr_creation",
                description="Create pull requests for feature implementations",
                interface=create_pr,
                execution_cost=0.3
            ),
            Capability(
                name="code_review",
                description="Review code changes and provide feedback",
                interface=review_code,
                execution_cost=0.4
            ),
            Capability(
                name="workflow_management",
                description="Manage PR workflows and track development progress",
                interface=manage_workflow,
                execution_cost=0.2
            )
        ]

        for cap in pm_capabilities:
            self.capability_registry.register_capability(cap, ["product", "planning"])


class SantiagoDevEntity(SantiagoEntity):
    """
    Development Santiago Entity

    Focus: Code implementation, testing, debugging, refactoring
    Domain: Programming languages, frameworks, development best practices
    """

    def __init__(self, service_registry: IntegratedServiceRegistry):
        identity = EntityIdentity(
            entity_id=f"santiago-dev-{uuid.uuid4().hex[:8]}",
            name="Santiago-Dev",
            role="developer",
            expertise_domains=["software_development", "coding", "testing", "debugging"],
            personality_traits={
                "technical": 0.9,
                "detail_oriented": 0.8,
                "problem_solving": 0.9,
                "quality_focused": 0.8
            },
            created_at=datetime.now(),
            reputation={
                "code_quality": 0.9,
                "testing": 0.8,
                "debugging": 0.9,
                "refactoring": 0.7
            }
        )

        super().__init__(identity)
        self.service_registry = service_registry
        self._initialize_knowledge()
        self._initialize_capabilities()

    def _initialize_knowledge(self):
        """Initialize development domain knowledge."""

        dev_knowledge = [
            KnowledgeItem(
                id=f"dev_knowledge_{uuid.uuid4().hex[:8]}",
                domain="software_development",
                content={
                    "languages": ["Python", "JavaScript", "TypeScript", "Rust", "Go"],
                    "paradigms": ["Object-oriented", "Functional", "Reactive", "Event-driven"],
                    "patterns": ["MVC", "MVVM", "Observer", "Factory", "Singleton", "Strategy"],
                    "best_practices": [
                        "Clean Code principles",
                        "SOLID principles",
                        "DRY (Don't Repeat Yourself)",
                        "Test-driven development",
                        "Continuous integration/deployment"
                    ]
                },
                confidence=0.9,
                source="software_engineering_best_practices",
                timestamp=datetime.now(),
                tags=["development", "patterns", "best_practices"]
            ),
            KnowledgeItem(
                id=f"dev_knowledge_{uuid.uuid4().hex[:8]}",
                domain="testing",
                content={
                    "test_types": ["Unit tests", "Integration tests", "System tests", "Acceptance tests"],
                    "testing_frameworks": {
                        "python": ["pytest", "unittest"],
                        "javascript": ["Jest", "Mocha"],
                        "rust": ["cargo test"]
                    },
                    "coverage_goals": "80-90% code coverage",
                    "test_driven_development": "Red-Green-Refactor cycle"
                },
                confidence=0.8,
                source="testing_best_practices",
                timestamp=datetime.now(),
                tags=["testing", "quality", "tdd"]
            )
        ]

        for item in dev_knowledge:
            self.knowledge_base.add_knowledge(item)

    def _initialize_capabilities(self):
        """Initialize development capabilities."""

        async def implement_feature(goal):
            """Implement a software feature."""
            # Mock implementation for now
            return {
                "implementation": f"""
def analyze_dependencies(manifest_path):
    \"\"\"Analyze cargo manifest dependencies.\"\"\"
    import json
    import os
    
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    
    dependencies = manifest.get('dependencies', {{}})
    dev_dependencies = manifest.get('dev-dependencies', {{}})
    
    analysis = {{
        'total_dependencies': len(dependencies),
        'dev_dependencies': len(dev_dependencies),
        'outdated_check': 'Not implemented yet',
        'security_scan': 'Not implemented yet'
    }}
    
    return analysis
                """,
                "language": "python",
                "files_created": ["dependency_analyzer.py"]
            }

        async def write_tests(goal):
            """Write tests for implemented code."""
            # Mock implementation for now
            return {
                "tests": f"""
import pytest
from dependency_analyzer import analyze_dependencies

def test_analyze_dependencies():
    \"\"\"Test dependency analysis function.\"\"\"
    # Mock manifest data
    mock_manifest = {{
        "dependencies": {{"serde": "1.0", "tokio": "1.0"}},
        "dev-dependencies": {{"criterion": "0.3"}}
    }}
    
    # This would test the actual implementation
    assert True  # Placeholder test

def test_empty_manifest():
    \"\"\"Test with empty manifest.\"\"\"
    assert True  # Placeholder test
                """,
                "framework": "pytest",
                "coverage_target": "80%"
            }

        async def debug_issue(goal):
            """Debug and fix code issues."""
            # Mock implementation for now
            return {
                "debug_analysis": {
                    "issue_type": "AttributeError",
                    "root_cause": "Object doesn't have expected attribute",
                    "fix_suggestion": "Add proper error handling and attribute checks",
                    "code_changes": "Add try-except blocks and validation"
                },
                "confidence": 0.8
            }

        async def ask_question(goal):
            """Ask questions to gather information and clarify requirements."""
            # Mock implementation for now - would use LLM service
            question_context = goal.description
            
            # Extract question from goal description
            if "question:" in question_context.lower():
                question = question_context.split("question:", 1)[1].strip()
            else:
                question = question_context
            
            return {
                "question": question,
                "answer": f"This is a mock answer to: {question}. In a real implementation, this would use the LLM service to provide detailed, contextual answers.",
                "confidence": 0.8,
                "sources": ["domain knowledge", "best practices", "similar projects"],
                "follow_up_questions": ["What are the specific constraints?", "Are there existing patterns to follow?"]
            }

        async def run_tests(goal):
            """Run automated tests for implemented code."""
            # Mock implementation for now
            return {
                "tests_run": True,
                "total_tests": 15,
                "passed": 14,
                "failed": 1,
                "coverage": 87.5,
                "failed_tests": ["test_edge_case_handling"],
                "recommendations": ["Fix edge case handling", "Add more test cases"]
            }

        async def deploy_code(goal):
            """Deploy code changes to staging/production."""
            # Mock implementation for now
            return {
                "deployment_started": True,
                "environment": "staging",
                "status": "in_progress",
                "estimated_completion": "5 minutes",
                "rollback_available": True,
                "monitoring_enabled": True
            }

        dev_capabilities = [
            Capability(
                name="feature_implementation",
                description="Implement software features from specifications",
                interface=implement_feature,
                execution_cost=0.5
            ),
            Capability(
                name="test_writing",
                description="Write comprehensive tests for code",
                interface=write_tests,
                execution_cost=0.3
            ),
            Capability(
                name="debugging",
                description="Debug and fix code issues",
                interface=debug_issue,
                execution_cost=0.4
            ),
            Capability(
                name="question_asking",
                description="Ask questions to gather information and clarify requirements",
                interface=ask_question,
                execution_cost=0.1
            ),
            Capability(
                name="test_execution",
                description="Run automated tests and validate code quality",
                interface=run_tests,
                execution_cost=0.2
            ),
            Capability(
                name="deployment",
                description="Deploy code changes to target environments",
                interface=deploy_code,
                execution_cost=0.6
            )
        ]

        for cap in dev_capabilities:
            self.capability_registry.register_capability(cap, ["development", "coding"])


class SantiagoArchitectEntity(SantiagoEntity):
    """
    Architecture Santiago Entity

    Focus: System design, technical oversight, scalability analysis
    Domain: System architecture, design patterns, technology evaluation
    """

    def __init__(self, service_registry: IntegratedServiceRegistry):
        identity = EntityIdentity(
            entity_id=f"santiago-architect-{uuid.uuid4().hex[:8]}",
            name="Santiago-Architect",
            role="architect",
            expertise_domains=["system_architecture", "design_patterns", "scalability", "technology_evaluation"],
            personality_traits={
                "systemic": 0.9,
                "analytical": 0.8,
                "forward_thinking": 0.9,
                "risk_aware": 0.8
            },
            created_at=datetime.now(),
            reputation={
                "system_design": 0.9,
                "scalability_analysis": 0.8,
                "technology_evaluation": 0.9,
                "risk_assessment": 0.8
            }
        )

        super().__init__(identity)
        self.service_registry = service_registry
        self._initialize_knowledge()
        self._initialize_capabilities()

    def _initialize_knowledge(self):
        """Initialize architecture domain knowledge."""

        arch_knowledge = [
            KnowledgeItem(
                id=f"arch_knowledge_{uuid.uuid4().hex[:8]}",
                domain="system_architecture",
                content={
                    "architectural_styles": [
                        "Layered architecture",
                        "Microservices",
                        "Event-driven architecture",
                        "Serverless architecture",
                        "Hexagonal architecture"
                    ],
                    "quality_attributes": [
                        "Scalability", "Reliability", "Performance", "Security",
                        "Maintainability", "Testability", "Deployability"
                    ],
                    "trade_off_analysis": "Every architectural decision involves trade-offs between competing quality attributes"
                },
                confidence=0.9,
                source="software_architecture_principles",
                timestamp=datetime.now(),
                tags=["architecture", "design", "quality_attributes"]
            ),
            KnowledgeItem(
                id=f"arch_knowledge_{uuid.uuid4().hex[:8]}",
                domain="scalability",
                content={
                    "scaling_patterns": {
                        "horizontal_scaling": "Adding more instances",
                        "vertical_scaling": "Adding more resources to existing instances",
                        "auto_scaling": "Automatic scaling based on load"
                    },
                    "bottleneck_identification": [
                        "CPU-bound", "Memory-bound", "I/O-bound", "Network-bound"
                    ],
                    "caching_strategies": ["Write-through", "Write-behind", "Cache-aside"],
                    "database_scaling": ["Read replicas", "Sharding", "CQRS"]
                },
                confidence=0.8,
                source="scalability_patterns_guide",
                timestamp=datetime.now(),
                tags=["scalability", "performance", "patterns"]
            )
        ]

        for item in arch_knowledge:
            self.knowledge_base.add_knowledge(item)

    def _initialize_capabilities(self):
        """Initialize architecture capabilities."""

        async def design_system(goal):
            """Design system architecture for requirements."""
            # Mock implementation for now
            return {
                "architecture_design": {
                    "pattern": "Microservices",
                    "components": ["API Gateway", "Dependency Analyzer Service", "Report Generator", "Database"],
                    "data_flow": "Manifest -> Parser -> Analyzer -> Database -> Report Generator -> API",
                    "scalability": "Horizontal scaling for analyzer service",
                    "security": "Input validation, secure API endpoints"
                }
            }

        async def review_architecture(goal):
            """Review and analyze existing architecture."""
            # Mock implementation for now
            return {
                "architecture_review": {
                    "strengths": ["Modular design", "Clear separation of concerns"],
                    "weaknesses": ["Potential single points of failure", "Complex inter-service communication"],
                    "recommendations": ["Add circuit breakers", "Implement service mesh", "Add comprehensive monitoring"],
                    "risk_assessment": "Medium risk - good foundation but needs resilience improvements"
                }
            }

        async def analyze_scalability(goal):
            """Analyze scalability of system design."""
            # Mock implementation for now
            return {
                "scalability_analysis": {
                    "current_limitations": ["Single analyzer instance", "Memory-bound processing"],
                    "scaling_recommendations": ["Horizontal pod scaling", "Async processing queues", "Caching layer"],
                    "performance_targets": "100 manifests/minute, 10GB memory limit",
                    "bottlenecks": ["Dependency graph analysis", "File I/O operations"]
                }
            }

        async def ask_question(goal):
            """Ask questions to gather information and clarify requirements."""
            # Mock implementation for now - would use LLM service
            question_context = goal.description
            
            # Extract question from goal description
            if "question:" in question_context.lower():
                question = question_context.split("question:", 1)[1].strip()
            else:
                question = question_context
            
            return {
                "question": question,
                "answer": f"This is a mock answer to: {question}. In a real implementation, this would use the LLM service to provide detailed, contextual answers.",
                "confidence": 0.8,
                "sources": ["domain knowledge", "best practices", "similar projects"],
                "follow_up_questions": ["What are the specific constraints?", "Are there existing patterns to follow?"]
            }

        async def monitor_system(goal):
            """Monitor system performance and health."""
            # Mock implementation for now
            return {
                "monitoring_active": True,
                "metrics": {
                    "cpu_usage": 45.2,
                    "memory_usage": 67.8,
                    "response_time": 125.3,
                    "error_rate": 0.02
                },
                "alerts": ["High memory usage detected"],
                "recommendations": ["Consider memory optimization", "Scale up if needed"]
            }

        async def generate_docs(goal):
            """Generate documentation for system components."""
            # Mock implementation for now
            return {
                "documentation_generated": True,
                "files_created": ["api_docs.md", "architecture_diagram.png", "deployment_guide.md"],
                "coverage": 92.5,
                "format": "markdown",
                "auto_generated": True
            }

        arch_capabilities = [
            Capability(
                name="system_design",
                description="Design system architectures for requirements",
                interface=design_system,
                execution_cost=0.6
            ),
            Capability(
                name="architecture_review",
                description="Review and analyze system architectures",
                interface=review_architecture,
                execution_cost=0.4
            ),
            Capability(
                name="scalability_analysis",
                description="Analyze scalability of system designs",
                interface=analyze_scalability,
                execution_cost=0.5
            ),
            Capability(
                name="question_asking",
                description="Ask questions to gather information and clarify requirements",
                interface=ask_question,
                execution_cost=0.1
            ),
            Capability(
                name="system_monitoring",
                description="Monitor system performance and health metrics",
                interface=monitor_system,
                execution_cost=0.2
            ),
            Capability(
                name="documentation_generation",
                description="Generate comprehensive system documentation",
                interface=generate_docs,
                execution_cost=0.3
            )
        ]

        for cap in arch_capabilities:
            self.capability_registry.register_capability(cap, ["architecture", "design"])


class SantiagoEntityFactory:
    """
    Factory for creating specialized Santiago entities.
    """

    def __init__(self, service_registry: IntegratedServiceRegistry):
        self.service_registry = service_registry

    def create_pm_entity(self) -> SantiagoPMEntity:
        """Create a Product Management Santiago entity."""
        return SantiagoPMEntity(self.service_registry)

    def create_dev_entity(self) -> SantiagoDevEntity:
        """Create a Development Santiago entity."""
        return SantiagoDevEntity(self.service_registry)

    def create_architect_entity(self) -> SantiagoArchitectEntity:
        """Create an Architecture Santiago entity."""
        return SantiagoArchitectEntity(self.service_registry)

    def create_all_entities(self) -> Dict[str, SantiagoEntity]:
        """Create all three specialized entities."""
        return {
            "pm": self.create_pm_entity(),
            "dev": self.create_dev_entity(),
            "architect": self.create_architect_entity()
        }


# Test entity specialization
async def test_entity_specialization():
    """Test specialized entity creation and basic functionality."""

    print("Testing Entity Specialization...")

    # Create service registry
    registry = IntegratedServiceRegistry()

    # Create entity factory
    factory = SantiagoEntityFactory(registry)

    # Create all entities
    entities = factory.create_all_entities()

    print(f"Created entities: {list(entities.keys())}")

    # Test basic functionality
    for name, entity in entities.items():
        print(f"\n{name.upper()} Entity:")
        print(f"  ID: {entity.identity.entity_id}")
        print(f"  Role: {entity.identity.role}")
        print(f"  Domains: {entity.identity.expertise_domains}")
        print(f"  Knowledge items: {len(entity.knowledge_base.knowledge)}")
        print(f"  Capabilities: {len(entity.capability_registry.capabilities)}")

    print("\nEntity specialization test completed!")


if __name__ == "__main__":
    asyncio.run(test_entity_specialization())