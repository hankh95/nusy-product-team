"""
Self-Questioning Tool for Santiago Autonomous Development
========================================================

This tool enables Santiago agents to ask questions internally or via external APIs
instead of blocking on human input. It implements the in-memory LLM integration
architecture described in the architecture commentary.
"""

import os
import json
import time
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QuestionSource(Enum):
    """Sources for answering questions"""
    SELF_REFLECTION = "self_reflection"
    LOCAL_LLM = "local_llm"
    EXTERNAL_API = "external_api"
    KNOWLEDGE_GRAPH = "knowledge_graph"


class ConfidenceLevel(Enum):
    """Confidence levels for answers"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"


@dataclass
class QuestionAnswer:
    """Structure for question-answer pairs"""
    question: str
    answer: str
    source: QuestionSource
    confidence: ConfidenceLevel
    timestamp: float
    context: Dict[str, Any]
    metadata: Dict[str, Any]


class SelfQuestioningTool:
    """
    Tool for autonomous question answering during development.

    This implements the "ask yourself first" principle to minimize blocking
    on human input and accelerate development velocity.
    """

    def __init__(self, knowledge_graph=None, local_llm=None):
        """
        Initialize the self-questioning tool.

        Args:
            knowledge_graph: Interface to the knowledge graph
            local_llm: Interface to local in-memory LLM service
        """
        self.knowledge_graph = knowledge_graph
        # Try to import and use the in-memory LLM service
        if local_llm is None:
            try:
                import os
                import sys
                # Add the current working directory to path
                cwd = os.getcwd()
                if cwd not in sys.path:
                    sys.path.insert(0, cwd)

                from expeditions.exp_036.in_memory_llm_service import InMemoryLLMService
                self.local_llm = InMemoryLLMService()
                logger.info("Initialized in-memory LLM service for self-questioning")
            except ImportError as e:
                self.local_llm = None
                logger.warning(f"In-memory LLM service not available ({e}), using external APIs only")
        else:
            self.local_llm = local_llm
        self.question_history: List[QuestionAnswer] = []
        self.confidence_threshold = {
            QuestionSource.SELF_REFLECTION: ConfidenceLevel.MEDIUM,
            QuestionSource.LOCAL_LLM: ConfidenceLevel.HIGH,
            QuestionSource.EXTERNAL_API: ConfidenceLevel.HIGH,
            QuestionSource.KNOWLEDGE_GRAPH: ConfidenceLevel.HIGH,
        }

    def ask_question(self, question: str, context: Dict[str, Any] = None) -> QuestionAnswer:
        """
        Ask a question and get an answer from the most appropriate source.

        Priority order:
        1. Self-reflection (internal reasoning)
        2. Local LLM (in-memory models)
        3. Knowledge graph lookup
        4. External API (xAI/OpenAI)

        Args:
            question: The question to answer
            context: Additional context for the question

        Returns:
            QuestionAnswer with the response
        """
        context = context or {}
        start_time = time.time()

        # Try self-reflection first
        answer = self._try_self_reflection(question, context)
        if answer and answer.confidence.value >= self.confidence_threshold[answer.source].value:
            self._log_question_answer(answer)
            return answer

        # Try local LLM
        answer = self._try_local_llm(question, context)
        if answer and answer.confidence.value >= self.confidence_threshold[answer.source].value:
            self._log_question_answer(answer)
            return answer

        # Try knowledge graph
        answer = self._try_knowledge_graph(question, context)
        if answer and answer.confidence.value >= self.confidence_threshold[answer.source].value:
            self._log_question_answer(answer)
            return answer

        # Fallback to external API
        answer = self._try_external_api(question, context)
        self._log_question_answer(answer)
        return answer

    def _try_self_reflection(self, question: str, context: Dict[str, Any]) -> Optional[QuestionAnswer]:
        """
        Attempt to answer using internal reasoning and patterns.
        """
        # This would contain logic for common development questions
        # For now, return low confidence for most questions
        confidence = ConfidenceLevel.LOW

        # Simple pattern matching for common questions
        if "import" in question.lower() and "error" in question.lower():
            answer = "Check if the module is installed and the import path is correct. Try: pip install <module> or python -c 'import <module>'"
            confidence = ConfidenceLevel.MEDIUM
        elif "test" in question.lower() and "fail" in question.lower():
            answer = "Run the test with verbose output: pytest -v -s <test_file>. Check for assertion errors, missing dependencies, or environment issues."
            confidence = ConfidenceLevel.MEDIUM
        elif "git" in question.lower() and "merge" in question.lower():
            answer = "Check for conflicts: git status. Resolve conflicts in conflicted files, then: git add <resolved_files> && git commit"
            confidence = ConfidenceLevel.MEDIUM

        if confidence == ConfidenceLevel.LOW:
            return None

        return QuestionAnswer(
            question=question,
            answer=answer,
            source=QuestionSource.SELF_REFLECTION,
            confidence=confidence,
            timestamp=time.time(),
            context=context,
            metadata={"reasoning": "pattern_matching"}
        )

    def _try_local_llm(self, question: str, context: Dict[str, Any]) -> Optional[QuestionAnswer]:
        """
        Attempt to answer using local in-memory LLM service.
        """
        if not self.local_llm:
            return None

        try:
            # Use the in-memory LLM service
            import os
            import sys
            # Add the current working directory to path
            cwd = os.getcwd()
            if cwd not in sys.path:
                sys.path.insert(0, cwd)

            from expeditions.exp_036.in_memory_llm_service import LLMQuery

            query = LLMQuery(
                question=question,
                context=context,
                max_tokens=256,  # Shorter responses for quick answers
                temperature=0.3  # Lower temperature for more focused answers
            )

            response = self.local_llm.query(query)

            if response:
                # Map the response to our QuestionAnswer format
                confidence = ConfidenceLevel.HIGH if response.confidence > 0.8 else ConfidenceLevel.MEDIUM

                return QuestionAnswer(
                    question=question,
                    answer=response.answer,
                    source=QuestionSource.LOCAL_LLM,
                    confidence=confidence,
                    timestamp=time.time(),
                    context=context,
                    metadata={
                        "model_used": response.model_used,
                        "processing_time": response.processing_time,
                        "tokens_used": response.tokens_used,
                        "llm_confidence": response.confidence
                    }
                )

            return None

        except Exception as e:
            logger.warning(f"Local LLM service query failed: {e}")
            return None

    def _try_knowledge_graph(self, question: str, context: Dict[str, Any]) -> Optional[QuestionAnswer]:
        """
        Attempt to answer using knowledge graph lookup.
        """
        if not self.knowledge_graph:
            return None

        try:
            # This would query the knowledge graph
            # For now, simulate with a placeholder
            answer = f"[Knowledge Graph] Found relevant information: {question[:50]}... matches existing patterns in the codebase."
            confidence = ConfidenceLevel.HIGH

            return QuestionAnswer(
                question=question,
                answer=answer,
                source=QuestionSource.KNOWLEDGE_GRAPH,
                confidence=confidence,
                timestamp=time.time(),
                context=context,
                metadata={"matches": 3, "confidence_score": 0.85}
            )
        except Exception as e:
            logger.warning(f"Knowledge graph query failed: {e}")
            return None

    def _try_external_api(self, question: str, context: Dict[str, Any]) -> QuestionAnswer:
        """
        Answer using external API (xAI/OpenAI) as last resort.
        """
        try:
            # This would call external APIs
            # For now, simulate with a placeholder
            answer = f"[External API] Comprehensive analysis: {question[:50]}... This requires expert knowledge. Based on best practices..."

            return QuestionAnswer(
                question=question,
                answer=answer,
                source=QuestionSource.EXTERNAL_API,
                confidence=ConfidenceLevel.HIGH,
                timestamp=time.time(),
                context=context,
                metadata={"api": "xai", "cost": 0.02, "model": "grok-1"}
            )
        except Exception as e:
            logger.error(f"External API call failed: {e}")
            # Return a fallback answer
            return QuestionAnswer(
                question=question,
                answer="Unable to determine answer automatically. This may require human expertise or additional context.",
                source=QuestionSource.EXTERNAL_API,
                confidence=ConfidenceLevel.UNKNOWN,
                timestamp=time.time(),
                context=context,
                metadata={"error": str(e)}
            )

    def _log_question_answer(self, qa: QuestionAnswer):
        """
        Log the question-answer interaction for learning and improvement.
        """
        self.question_history.append(qa)
        logger.info(f"Question answered via {qa.source.value} (confidence: {qa.confidence.value}): {qa.question[:50]}...")

    def get_question_history(self) -> List[QuestionAnswer]:
        """
        Get the history of questions asked and answered.
        """
        return self.question_history.copy()

    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about question answering performance.
        """
        if not self.question_history:
            return {"total_questions": 0}

        sources = {}
        confidences = {}

        for qa in self.question_history:
            sources[qa.source.value] = sources.get(qa.source.value, 0) + 1
            confidences[qa.confidence.value] = confidences.get(qa.confidence.value, 0) + 1

        return {
            "total_questions": len(self.question_history),
            "source_distribution": sources,
            "confidence_distribution": confidences,
            "self_sufficiency_rate": sources.get(QuestionSource.SELF_REFLECTION.value, 0) / len(self.question_history)
        }


# Convenience function for easy access
def ask_self(question: str, context: Dict[str, Any] = None) -> str:
    """
    Convenience function to ask a question and get just the answer string.

    This is the main interface for Santiago agents to use.
    """
    tool = SelfQuestioningTool()
    result = tool.ask_question(question, context)
    return result.answer
