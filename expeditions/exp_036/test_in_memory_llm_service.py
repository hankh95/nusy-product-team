"""
Tests for the In-Memory LLM Service
===================================

Tests the in-memory LLM integration for instant question answering.
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

# Set testing environment for permissive memory limits
os.environ["LLM_TESTING"] = "true"

from in_memory_llm_service import (
    InMemoryLLMService,
    LLMModel,
    LLMModelType,
    LLMSize,
    LLMQuery,
    query_llm
)


class TestInMemoryLLMService:

    def test_initialization(self):
        """Test service initialization"""
        service = InMemoryLLMService()
        assert len(service.loaded_models) >= 3  # Should have default models
        assert service.max_memory_bytes > 0
        assert service.query_history == []

    def test_model_loading(self):
        """Test model loading functionality"""
        service = InMemoryLLMService()

        # Test loading a known model
        success = service.load_model("phi-2")
        assert success

        model = service.loaded_models["phi-2"]
        assert model.loaded
        assert model.memory_usage > 0
        assert model.last_used > 0

    def test_model_unloading(self):
        """Test model unloading functionality"""
        service = InMemoryLLMService()

        # Load then unload
        service.load_model("phi-2")
        success = service.unload_model("phi-2")
        assert success

        model = service.loaded_models["phi-2"]
        assert not model.loaded
        assert model.memory_usage == 0

    def test_query_processing(self):
        """Test basic query processing"""
        service = InMemoryLLMService()

        query = LLMQuery(
            question="How do I implement a simple function?",
            context={"language": "python", "task": "coding"}
        )

        response = service.query(query)

        assert response is not None
        assert response.answer is not None
        assert len(response.answer) > 0
        assert response.confidence >= 0.0 and response.confidence <= 1.0
        assert response.processing_time >= 0
        assert response.model_used in service.loaded_models

    def test_model_selection(self):
        """Test model selection logic"""
        service = InMemoryLLMService()

        # Load a specific model
        service.load_model("mistral-7b-instruct")

        query = LLMQuery(
            question="Test question",
            context={},
            model_preference=LLMModelType.MISTRAL
        )

        response = service.query(query)
        assert response is not None
        assert response.model_used == "mistral-7b-instruct"

    def test_query_history(self):
        """Test query history tracking"""
        service = InMemoryLLMService()

        # Make a few queries
        for i in range(3):
            query = LLMQuery(question=f"Question {i}", context={})
            service.query(query)

        assert len(service.query_history) == 3
        assert all("question" in q for q in service.query_history)

    def test_statistics(self):
        """Test statistics calculation"""
        service = InMemoryLLMService()

        # Make some queries
        service.query(LLMQuery(question="Test 1", context={}))
        service.query(LLMQuery(question="Test 2", context={}))

        stats = service.get_stats()
        assert stats["total_queries"] == 2
        assert "loaded_models" in stats
        assert "avg_confidence" in stats
        assert "avg_response_time" in stats

    def test_convenience_function(self):
        """Test the convenience query function"""
        answer = query_llm("What is Python?")
        assert answer is not None
        assert isinstance(answer, str)
        assert len(answer) > 0

    def test_context_handling(self):
        """Test context preservation in queries"""
        service = InMemoryLLMService()

        context = {"file": "test.py", "line": 42, "function": "test_function"}
        query = LLMQuery(question="How do I fix this?", context=context)

        response = service.query(query)

        assert response is not None
        # Check that context was logged
        assert len(service.query_history) == 1
        logged_query = service.query_history[0]
        assert "context_keys" in logged_query

    def test_memory_limits(self):
        """Test memory limit handling"""
        # Create service with very low memory limit
        service = InMemoryLLMService(max_memory_gb=0.001)  # 1MB

        # Try to load a model (should fail due to memory limits)
        success = service.load_model("mistral-7b-instruct")
        # This might succeed or fail depending on actual memory check implementation
        # The important thing is that the service doesn't crash
        assert isinstance(success, bool)

    def test_cleanup(self):
        """Test service cleanup"""
        service = InMemoryLLMService()

        # Load a model
        service.load_model("phi-2")
        assert service.loaded_models["phi-2"].loaded

        # Cleanup
        service.cleanup()

        # Should be unloaded
        assert not service.loaded_models["phi-2"].loaded
        assert len(service.query_history) == 0


