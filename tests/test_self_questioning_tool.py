"""
Tests for the Self-Questioning Tool
===================================

Tests the autonomous question answering capabilities.
"""

import pytest
from src.nusy_pm_core.tools.self_questioning_tool import (
    SelfQuestioningTool,
    QuestionSource,
    ConfidenceLevel,
    ask_self
)


class TestSelfQuestioningTool:

    def test_initialization(self):
        """Test tool initialization"""
        tool = SelfQuestioningTool()
        assert tool.question_history == []
        assert tool.knowledge_graph is None
        assert tool.local_llm is None

    def test_self_reflection_patterns(self):
        """Test pattern-based self-reflection answers"""
        tool = SelfQuestioningTool()

        # Test import error question
        question = "Why am I getting an import error?"
        result = tool.ask_question(question)

        assert result.question == question
        assert result.source == QuestionSource.SELF_REFLECTION
        assert result.confidence == ConfidenceLevel.MEDIUM
        assert "pip install" in result.answer

    def test_git_merge_question(self):
        """Test git merge conflict question"""
        tool = SelfQuestioningTool()

        question = "How do I resolve git merge conflicts?"
        result = tool.ask_question(question)

        assert result.source == QuestionSource.SELF_REFLECTION
        assert result.confidence == ConfidenceLevel.MEDIUM
        assert "git add" in result.answer

    def test_unknown_question_fallback(self):
        """Test that unknown questions fall back to external API"""
        tool = SelfQuestioningTool()

        question = "What is the meaning of life?"
        result = tool.ask_question(question)

        assert result.source == QuestionSource.EXTERNAL_API
        assert result.confidence == ConfidenceLevel.HIGH

    def test_convenience_function(self):
        """Test the ask_self convenience function"""
        question = "How do I run tests?"
        answer = ask_self(question)

        assert isinstance(answer, str)
        assert len(answer) > 0

    def test_question_history(self):
        """Test question history tracking"""
        tool = SelfQuestioningTool()

        tool.ask_question("Test question 1")
        tool.ask_question("Test question 2")

        history = tool.get_question_history()
        assert len(history) == 2
        assert history[0].question == "Test question 1"
        assert history[1].question == "Test question 2"

    def test_stats_calculation(self):
        """Test statistics calculation"""
        tool = SelfQuestioningTool()

        # Add some test questions
        tool.ask_question("import error")  # self-reflection
        tool.ask_question("unknown question")  # external API

        stats = tool.get_stats()
        assert stats["total_questions"] == 2
        assert QuestionSource.SELF_REFLECTION.value in stats["source_distribution"]
        assert QuestionSource.EXTERNAL_API.value in stats["source_distribution"]

    def test_context_preservation(self):
        """Test that context is preserved in answers"""
        tool = SelfQuestioningTool()
        context = {"file": "test.py", "line": 42}

        result = tool.ask_question("How do I fix this?", context)

        assert result.context == context
        assert result.timestamp > 0
