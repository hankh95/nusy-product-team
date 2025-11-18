"""
Question Answering Service for Santiago-PM

Provides intelligent question answering capabilities for the team using:
- Questionnaire system for structured data collection
- Santiago Core neurosymbolic reasoning for prioritization
- Knowledge graph integration for context-aware responses
"""

import os
import sys
import json
import asyncio
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import re

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "expeditions" / "exp_040"))
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "expeditions" / "exp_038"))

try:
    from mcp_service_integration import IntegratedServiceRegistry, SantiagoCoreMCPService
    from simple_core import SantiagoCore, KnowledgeDomain
    print("✅ Imported EXP-040 integrated services")
except ImportError as e:
    print(f"Warning: Could not import EXP-040 services: {e}")
    # Mock implementations for development
    class SantiagoCore:
        async def reason(self, query, domain): return {"answer": "Mock answer", "confidence": 0.5}
        async def load_domain_knowledge(self, domain, data): return 0

class QuestionAnsweringService:
    """
    Service that provides intelligent question answering for the Santiago-PM team.

    Features:
    - Context-aware question routing using knowledge domains
    - Questionnaire generation for complex questions
    - Santiago Core reasoning for prioritization decisions
    - Knowledge graph integration for comprehensive answers
    """

    def __init__(self, registry: Optional[IntegratedServiceRegistry] = None, workspace_path: Optional[str] = None):
        self.workspace_path = workspace_path
        self.registry = registry or IntegratedServiceRegistry(workspace_path=self.workspace_path)
        # Use the Santiago Core from the registry instead of creating a new one
        core_service = self.registry.get_service('santiago_core')
        if core_service:
            # Get the actual SantiagoCore instance from the MCP wrapper
            self.santiago_core = core_service.capability.santiago_core
        else:
            # Fallback to direct instantiation
            self.santiago_core = SantiagoCore()
        self.questionnaire_templates = self._load_questionnaire_templates()
        self.knowledge_domains = self._get_knowledge_domains()

    def _load_questionnaire_templates(self) -> Dict[str, Dict]:
        """Load available questionnaire templates."""
        templates_dir = Path(__file__).parent.parent / "questionnaires"
        templates = {}

        if templates_dir.exists():
            for template_file in templates_dir.glob("*.md"):
                if template_file.name != "README.md":
                    try:
                        content = template_file.read_text()
                        # Extract metadata from YAML frontmatter
                        metadata = self._extract_metadata(content)
                        templates[template_file.stem] = {
                            "path": template_file,
                            "content": content,
                            "metadata": metadata
                        }
                    except Exception as e:
                        print(f"Warning: Could not load template {template_file}: {e}")

        return templates

    def _extract_metadata(self, content: str) -> Dict[str, Any]:
        """Extract YAML frontmatter metadata from markdown content."""
        metadata = {}
        lines = content.split('\n')

        if lines and lines[0].strip() == '---':
            # Find end of frontmatter
            end_idx = -1
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == '---':
                    end_idx = i
                    break

            if end_idx > 0:
                frontmatter = '\n'.join(lines[1:end_idx])
                # Simple YAML parsing (could be enhanced)
                for line in frontmatter.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        metadata[key.strip()] = value.strip()

        return metadata

    def _get_knowledge_domains(self) -> Dict[str, str]:
        """Map question topics to Santiago Core knowledge domains."""
        return {
            "product_management": "product_management",
            "software_engineering": "software_engineering",
            "system_architecture": "system_architecture",
            "team_dynamics": "team_dynamics",
            "technical_debt": "technical_debt",
            "risk_management": "risk_management",
            "prioritization": "product_management",
            "requirements": "product_management",
            "architecture": "system_architecture",
            "code_quality": "software_engineering",
            "collaboration": "team_dynamics"
        }

    async def answer_question(self, question: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Answer a question using appropriate reasoning and tools.

        Args:
            question: The question to answer
            context: Additional context (user role, current task, etc.)

        Returns:
            Dict containing answer, confidence, reasoning, and any generated artifacts
        """
        context = context or {}

        # Step 1: Analyze question to determine domain and complexity
        domain, complexity = await self._analyze_question(question, context)

        # Step 2: Route to appropriate answering strategy
        if complexity == "simple":
            return await self._answer_simple_question(question, domain)
        elif complexity == "complex":
            return await self._answer_complex_question(question, domain, context)
        else:  # requires_research
            return await self._answer_research_question(question, domain, context)

    async def _analyze_question(self, question: str, context: Dict[str, Any]) -> Tuple[str, str]:
        """Analyze question to determine knowledge domain and complexity level."""
        # Extract keywords to determine domain
        question_lower = question.lower()
        domain = "product_management"  # default

        for keyword, domain_name in self.knowledge_domains.items():
            if keyword in question_lower:
                domain = domain_name
                break

        # Determine complexity based on question structure
        if any(word in question_lower for word in ["how to", "what is", "explain", "simple"]):
            complexity = "simple"
        elif any(word in question_lower for word in ["why", "should", "best", "recommend", "prioritize"]):
            complexity = "complex"
        else:
            complexity = "requires_research"

        return domain, complexity

    async def _answer_simple_question(self, question: str, domain: str) -> Dict[str, Any]:
        """Answer simple questions using direct reasoning."""
        # Use Santiago Core for reasoning
        result = await self.santiago_core.reason(question, getattr(KnowledgeDomain, domain.upper(), KnowledgeDomain.PRODUCT_MANAGEMENT))

        return {
            "answer": result.get("answer", "I need more information to answer this question."),
            "confidence": result.get("confidence", 0.5),
            "reasoning": f"Answered using {domain} knowledge domain",
            "method": "direct_reasoning",
            "artifacts_generated": []
        }

    async def _answer_complex_question(self, question: str, domain: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Answer complex questions that may require prioritization or recommendations."""
        # For prioritization questions, use workflow service
        if "prioritize" in question.lower() or "priority" in question.lower():
            return await self._handle_prioritization_question(question, domain, context)

        # For recommendation questions, use combined reasoning
        result = await self.santiago_core.reason(question, getattr(KnowledgeDomain, domain.upper(), KnowledgeDomain.PRODUCT_MANAGEMENT))

        # Generate questionnaire if answer needs validation
        questionnaire = None
        if result.get("confidence", 0) < 0.7:
            questionnaire = await self._generate_validation_questionnaire(question, domain)

        return {
            "answer": result.get("answer", "Based on analysis, here's my recommendation..."),
            "confidence": result.get("confidence", 0.6),
            "reasoning": f"Complex analysis using {domain} domain with neurosymbolic reasoning",
            "method": "complex_reasoning",
            "questionnaire": questionnaire,
            "artifacts_generated": ["recommendation"]
        }

    async def _answer_research_question(self, question: str, domain: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Answer questions that require research and may generate new artifacts."""
        # Generate a questionnaire to gather more information
        questionnaire = await self._generate_research_questionnaire(question, domain)

        # Use Santiago Core for initial analysis
        result = await self.santiago_core.reason(question, getattr(KnowledgeDomain, domain.upper(), KnowledgeDomain.PRODUCT_MANAGEMENT))

        return {
            "answer": "This question requires more research. I've generated a questionnaire to gather the necessary information.",
            "confidence": 0.3,
            "reasoning": f"Question requires research in {domain} domain",
            "method": "research_required",
            "questionnaire": questionnaire,
            "artifacts_generated": ["questionnaire"]
        }

    async def _handle_prioritization_question(self, question: str, domain: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle questions about prioritization using workflow service and Santiago Core."""
        # Extract items to prioritize from the question
        items_to_prioritize = self._extract_prioritization_items(question)

        if not items_to_prioritize:
            return await self._answer_simple_question(question, domain)

        # Use workflow service for prioritization
        workflow_service = self.registry.get_service("workflow")
        if workflow_service:
            from mcp_service_layer import MCPRequest
            request = MCPRequest(
                id=str(uuid.uuid4()),
                method="execute",
                params={
                    "operation": "prioritize",
                    "params": {"tasks": items_to_prioritize}
                },
                timestamp=datetime.now(),
                client_id="question_answering_service"
            )

            response = await workflow_service.invoke(request)
            prioritized_tasks = response.result.get("prioritized_tasks", [])

            # Use Santiago Core to explain the prioritization
            explanation_query = f"Explain why this prioritization makes sense: {prioritized_tasks}"
            explanation = await self.santiago_core.reason(explanation_query, KnowledgeDomain.PRODUCT_MANAGEMENT)

            return {
                "answer": f"Based on neurosymbolic reasoning, here's the recommended prioritization:\n\n" +
                         "\n".join([f"{i+1}. {task.get('description', task.get('id', 'Unknown'))}"
                                   for i, task in enumerate(prioritized_tasks)]),
                "confidence": 0.8,
                "reasoning": explanation.get("answer", "Prioritization based on workflow analysis and domain knowledge"),
                "method": "prioritization_analysis",
                "prioritized_items": prioritized_tasks,
                "artifacts_generated": ["prioritization_recommendation"]
            }
        else:
            # Fallback to Santiago Core only
            result = await self.santiago_core.reason(question, KnowledgeDomain.PRODUCT_MANAGEMENT)
            return {
                "answer": result.get("answer", "I need more information to provide prioritization recommendations."),
                "confidence": result.get("confidence", 0.5),
                "reasoning": "Prioritization analysis using neurosymbolic reasoning",
                "method": "reasoning_only_prioritization",
                "artifacts_generated": []
            }

    def _extract_prioritization_items(self, question: str) -> List[Dict[str, Any]]:
        """Extract items that need to be prioritized from the question."""
        # Simple extraction - could be enhanced with NLP
        items = []

        # Look for lists in the question
        lines = question.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith(('- ', '* ', '• ')) or re.match(r'^\d+\.', line):
                # Extract the item text
                item_text = re.sub(r'^[-*•]\s*|\d+\.\s*', '', line)
                if item_text:
                    items.append({
                        "id": f"item_{len(items) + 1}",
                        "description": item_text,
                        "priority": 1  # Will be determined by prioritization algorithm
                    })

        return items

    async def _generate_validation_questionnaire(self, question: str, domain: str) -> Dict[str, Any]:
        """Generate a questionnaire to validate an answer."""
        template = self.questionnaire_templates.get("questionnaire-template", {})

        if not template:
            return None

        # Customize template for validation
        content = template["content"]
        content = content.replace("{{QUESTION}}", question)
        content = content.replace("{{DOMAIN}}", domain)
        content = content.replace("{{PURPOSE}}", "Validate the reasoning and recommendations provided")

        return {
            "title": f"Validation Questionnaire: {question[:50]}...",
            "content": content,
            "purpose": "validation",
            "domain": domain
        }

    async def _generate_research_questionnaire(self, question: str, domain: str) -> Dict[str, Any]:
        """Generate a questionnaire to gather research information."""
        template = self.questionnaire_templates.get("questionnaire-template", {})

        if not template:
            return None

        # Customize template for research
        content = template["content"]
        content = content.replace("{{QUESTION}}", question)
        content = content.replace("{{DOMAIN}}", domain)
        content = content.replace("{{PURPOSE}}", "Gather information to properly answer this question")

        return {
            "title": f"Research Questionnaire: {question[:50]}...",
            "content": content,
            "purpose": "research",
            "domain": domain
        }

    async def generate_questionnaire_for_topic(self, topic: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate a questionnaire for a specific topic.

        Args:
            topic: The topic to create a questionnaire for
            context: Additional context for questionnaire generation

        Returns:
            Dict containing questionnaire content and metadata
        """
        context = context or {}

        # Determine the most appropriate template
        template_name = "questionnaire-template"  # Default
        if "personal" in topic.lower():
            template_name = "personal-log-discovery-questionnaire"

        template = self.questionnaire_templates.get(template_name, self.questionnaire_templates.get("questionnaire-template"))

        if not template:
            return {"error": "No questionnaire template available"}

        # Customize the template
        content = template["content"]

        # Replace placeholders
        content = content.replace("{{TOPIC}}", topic)
        content = content.replace("{{CONTEXT}}", context.get("description", "General inquiry"))
        content = content.replace("{{DATE}}", datetime.now().strftime("%Y-%m-%d"))

        return {
            "title": f"Questionnaire: {topic}",
            "content": content,
            "template_used": template_name,
            "generated_at": datetime.now().isoformat(),
            "topic": topic
        }

    async def analyze_questionnaire_response(self, response_content: str) -> Dict[str, Any]:
        """
        Analyze a completed questionnaire response and extract insights.

        Args:
            response_content: The completed questionnaire markdown content

        Returns:
            Dict containing analysis, insights, and recommended actions
        """
        # Use Santiago Core to analyze the response
        analysis_query = f"Analyze this questionnaire response and extract key insights, recommendations, and potential artifacts to create: {response_content[:1000]}..."

        result = await self.santiago_core.reason(analysis_query, KnowledgeDomain.PRODUCT_MANAGEMENT)

        # Extract potential artifacts from the analysis
        artifacts = self._extract_artifacts_from_analysis(result.get("answer", ""))

        return {
            "analysis": result.get("answer", "Analysis not available"),
            "confidence": result.get("confidence", 0.5),
            "insights": self._extract_insights(response_content),
            "recommended_actions": artifacts.get("actions", []),
            "potential_artifacts": artifacts.get("artifacts", []),
            "follow_up_questions": artifacts.get("questions", [])
        }

    def _extract_insights(self, response_content: str) -> List[str]:
        """Extract key insights from questionnaire response."""
        insights = []

        # Look for response sections
        lines = response_content.split('\n')
        in_response = False

        for line in lines:
            if "Response:" in line:
                in_response = True
                continue
            elif in_response and line.strip() and not line.startswith('   ') and len(line.strip()) > 10:
                # Extract meaningful response lines
                insights.append(line.strip())
                if len(insights) >= 5:  # Limit to top 5 insights
                    break

        return insights

    def _extract_artifacts_from_analysis(self, analysis: str) -> Dict[str, List[str]]:
        """Extract potential artifacts and actions from analysis text."""
        artifacts = {"artifacts": [], "actions": [], "questions": []}

        analysis_lower = analysis.lower()

        # Look for artifact types
        if "feature" in analysis_lower:
            artifacts["artifacts"].append("cargo-manifest")
        if "issue" in analysis_lower or "bug" in analysis_lower:
            artifacts["artifacts"].append("ships-log")
        if "experiment" in analysis_lower:
            artifacts["artifacts"].append("voyage-trial")
        if "note" in analysis_lower or "knowledge" in analysis_lower:
            artifacts["artifacts"].append("captains-journal")

        # Look for actions
        if "create" in analysis_lower or "build" in analysis_lower:
            artifacts["actions"].append("create_artifact")
        if "prioritize" in analysis_lower:
            artifacts["actions"].append("prioritization_analysis")
        if "research" in analysis_lower:
            artifacts["actions"].append("further_research")

        return artifacts


# CLI Interface for the Question Answering Service
def main():
    """CLI interface for question answering."""
    import argparse

    parser = argparse.ArgumentParser(description="Santiago-PM Question Answering Service")
    parser.add_argument("question", help="The question to answer")
    parser.add_argument("--context", help="Additional context as JSON string")
    parser.add_argument("--generate-questionnaire", action="store_true", help="Generate a questionnaire instead of answering")

    args = parser.parse_args()

    async def run():
        service = QuestionAnsweringService()

        if args.generate_questionnaire:
            # Generate questionnaire
            result = await service.generate_questionnaire_for_topic(args.question)
            print(json.dumps(result, indent=2))
        else:
            # Answer question
            context = json.loads(args.context) if args.context else {}
            result = await service.answer_question(args.question, context)
            print(json.dumps(result, indent=2))

    asyncio.run(run())


if __name__ == "__main__":
    main()