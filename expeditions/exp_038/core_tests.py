"""
EXP-038: Santiago Core Tests

Integration tests for the Santiago Core in-memory implementation.
Tests knowledge loading, reasoning capabilities, and integration.
"""

import asyncio
import unittest
import tempfile
import json
from pathlib import Path

from .santiago_core import SantiagoCore, KnowledgeDomain, ReasoningContext, ReasoningMode
from .knowledge_loader import KnowledgeLoader, initialize_knowledge_base


class TestSantiagoCore(unittest.TestCase):
    """Test the Santiago Core functionality."""

    def setUp(self):
        """Set up test environment."""
        self.core = SantiagoCore(max_memory_mb=64)  # Small memory for testing

    def tearDown(self):
        """Clean up test resources."""
        # Reset global instance if it exists
        import expeditions.exp_038.santiago_core as core_module
        core_module._santiago_core = None

    async def asyncSetUp(self):
        """Async setup for tests requiring initialization."""
        success = await self.core.initialize_core()
        self.assertTrue(success, "Core initialization should succeed")

    def test_core_initialization(self):
        """Test that the core initializes correctly."""
        async def run_test():
            success = await self.core.initialize_core()
            self.assertTrue(success)

            status = self.core.get_core_status()
            self.assertEqual(status["health"], "healthy")
            self.assertGreater(status["knowledge_nodes"], 0)

        asyncio.run(run_test())

    def test_knowledge_loading(self):
        """Test loading knowledge into different domains."""
        async def run_test():
            await self.core.initialize_core()

            # Test loading product management knowledge
            pm_knowledge = {
                "nodes": [
                    {
                        "id": "pm_1",
                        "content": "Product management focuses on delivering value to users",
                        "confidence": 0.9
                    },
                    {
                        "id": "pm_2",
                        "content": "Successful products solve real user problems",
                        "confidence": 0.8
                    }
                ]
            }

            nodes_loaded = await self.core.load_domain_knowledge(
                KnowledgeDomain.PRODUCT_MANAGEMENT, pm_knowledge
            )
            self.assertEqual(nodes_loaded, 2)

            # Test loading software engineering knowledge
            eng_knowledge = {
                "nodes": [
                    {
                        "id": "eng_1",
                        "content": "Clean code is maintainable and readable",
                        "confidence": 0.95
                    }
                ]
            }

            nodes_loaded = await self.core.load_domain_knowledge(
                KnowledgeDomain.SOFTWARE_ENGINEERING, eng_knowledge
            )
            self.assertEqual(nodes_loaded, 1)

            # Check status
            status = self.core.get_core_status()
            self.assertGreaterEqual(status["knowledge_nodes"], 5)  # Core + loaded nodes

        asyncio.run(run_test())

    def test_reasoning_basic(self):
        """Test basic reasoning capabilities."""
        async def run_test():
            await self.core.initialize_core()

            # Load some test knowledge
            test_knowledge = {
                "nodes": [
                    {
                        "id": "test_1",
                        "content": "Testing is essential for software quality",
                        "confidence": 0.9
                    },
                    {
                        "id": "test_2",
                        "content": "Automated tests provide fast feedback",
                        "confidence": 0.8
                    }
                ]
            }

            await self.core.load_domain_knowledge(
                KnowledgeDomain.SOFTWARE_ENGINEERING, test_knowledge
            )

            # Test reasoning
            context = ReasoningContext(
                query="Why is testing important?",
                domain=KnowledgeDomain.SOFTWARE_ENGINEERING,
                mode=ReasoningMode.SYMBOLIC
            )

            result = await self.core.reason(context)

            self.assertIsInstance(result, object)
            self.assertGreater(result.confidence, 0.0)
            self.assertIsInstance(result.answer, str)
            self.assertGreater(len(result.answer), 0)
            self.assertEqual(result.mode_used, ReasoningMode.SYMBOLIC)

        asyncio.run(run_test())

    def test_reasoning_cache(self):
        """Test that reasoning results are cached."""
        async def run_test():
            await self.core.initialize_core()

            context = ReasoningContext(
                query="What is the purpose of Santiago Core?",
                domain=KnowledgeDomain.SYSTEM_ARCHITECTURE,
                mode=ReasoningMode.SYMBOLIC
            )

            # First reasoning call
            result1 = await self.core.reason(context)

            # Second reasoning call with same query
            result2 = await self.core.reason(context)

            # Results should be identical (from cache)
            self.assertEqual(result1.answer, result2.answer)
            self.assertEqual(result1.confidence, result2.confidence)

            # Check cache size
            status = self.core.get_core_status()
            self.assertGreaterEqual(status["cache_size"], 1)

        asyncio.run(run_test())

    def test_memory_limits(self):
        """Test memory usage stays within limits."""
        async def run_test():
            await self.core.initialize_core()

            # Load a lot of knowledge to test memory limits
            large_knowledge = {
                "nodes": []
            }

            for i in range(100):
                large_knowledge["nodes"].append({
                    "id": f"large_{i}",
                    "content": f"This is test knowledge node number {i} with some additional content to make it larger and test memory usage patterns in the system.",
                    "confidence": 0.7
                })

            nodes_loaded = await self.core.load_domain_knowledge(
                KnowledgeDomain.SYSTEM_ARCHITECTURE, large_knowledge
            )
            self.assertEqual(nodes_loaded, 100)

            # Check memory usage
            status = self.core.get_core_status()
            self.assertLess(status["memory_usage_mb"], 64)  # Should stay under limit

        asyncio.run(run_test())


class TestKnowledgeLoader(unittest.TestCase):
    """Test the KnowledgeLoader functionality."""

    def setUp(self):
        """Set up test environment."""
        self.core = SantiagoCore(max_memory_mb=64)
        self.loader = KnowledgeLoader(self.core)

    async def asyncSetUp(self):
        """Async setup."""
        await self.core.initialize_core()

    def test_json_knowledge_loading(self):
        """Test loading knowledge from JSON files."""
        async def run_test():
            await self.core.initialize_core()

            # Create temporary JSON file
            test_data = {
                "nodes": [
                    {
                        "id": "json_test_1",
                        "content": "This is test knowledge from JSON",
                        "confidence": 0.85
                    }
                ]
            }

            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(test_data, f)
                temp_file = f.name

            try:
                nodes_loaded = await self.loader.load_json_knowledge_base(
                    temp_file, KnowledgeDomain.PRODUCT_MANAGEMENT
                )
                self.assertEqual(nodes_loaded, 1)

                # Check loader status
                status = self.loader.get_loading_status()
                self.assertIn("json_test", status["loaded_sources"][0])

            finally:
                Path(temp_file).unlink()

        asyncio.run(run_test())

    def test_text_document_loading(self):
        """Test loading knowledge from text documents."""
        async def run_test():
            await self.core.initialize_core()

            documents = [
                {
                    "content": "Agile development emphasizes iterative progress and customer collaboration.",
                    "metadata": {"source": "agile_manifesto"}
                },
                {
                    "content": "Test-driven development ensures code quality through comprehensive testing.",
                    "metadata": {"source": "tdd_principles"}
                }
            ]

            nodes_loaded = await self.loader.load_text_documents(
                documents, KnowledgeDomain.SOFTWARE_ENGINEERING
            )
            self.assertEqual(nodes_loaded, 2)

        asyncio.run(run_test())

    def test_knowledge_synthesis(self):
        """Test knowledge synthesis across domains."""
        async def run_test():
            await self.core.initialize_core()

            # Load knowledge in different domains with some overlap
            pm_knowledge = {
                "nodes": [
                    {
                        "id": "pm_quality",
                        "content": "Quality is essential for product success",
                        "confidence": 0.9
                    }
                ]
            }

            eng_knowledge = {
                "nodes": [
                    {
                        "id": "eng_quality",
                        "content": "Code quality ensures maintainable software",
                        "confidence": 0.9
                    }
                ]
            }

            await self.core.load_domain_knowledge(KnowledgeDomain.PRODUCT_MANAGEMENT, pm_knowledge)
            await self.core.load_domain_knowledge(KnowledgeDomain.SOFTWARE_ENGINEERING, eng_knowledge)

            # Synthesize knowledge
            synthesized = await self.loader.synthesize_knowledge()
            self.assertGreaterEqual(synthesized, 0)  # May or may not create synthetic nodes

        asyncio.run(run_test())

    def test_knowledge_validation(self):
        """Test knowledge validation after loading."""
        async def run_test():
            await self.core.initialize_core()

            # Load some test knowledge
            test_knowledge = {
                "nodes": [
                    {
                        "id": "validate_1",
                        "content": "Validation testing ensures knowledge is working",
                        "confidence": 0.8
                    }
                ]
            }

            await self.core.load_domain_knowledge(KnowledgeDomain.SYSTEM_ARCHITECTURE, test_knowledge)

            # Validate loaded knowledge
            validation = await self.loader.validate_loaded_knowledge()

            self.assertGreater(validation["total_nodes"], 0)
            self.assertGreater(validation["domains_loaded"], 0)
            self.assertGreater(len(validation["reasoning_tests"]), 0)

        asyncio.run(run_test())


class TestIntegration(unittest.TestCase):
    """Integration tests combining core and loader."""

    def setUp(self):
        """Set up integration test environment."""
        self.core = SantiagoCore(max_memory_mb=128)

    def test_full_initialization(self):
        """Test full initialization with knowledge loading."""
        async def run_test():
            # Initialize knowledge base
            loader = await initialize_knowledge_base(self.core)

            # Should have loaded some knowledge (at least basic fallback)
            status = self.core.get_core_status()
            self.assertGreater(status["knowledge_nodes"], 0)

            # Test reasoning works
            context = ReasoningContext(
                query="What is Santiago?",
                domain=KnowledgeDomain.SYSTEM_ARCHITECTURE,
                mode=ReasoningMode.SYMBOLIC
            )

            result = await self.core.reason(context)
            self.assertGreater(result.confidence, 0.0)

        asyncio.run(run_test())

    def test_reasoning_modes(self):
        """Test different reasoning modes work."""
        async def run_test():
            await self.core.initialize_core()

            # Load test knowledge
            test_knowledge = {
                "nodes": [
                    {
                        "id": "mode_test",
                        "content": "Different reasoning modes provide different perspectives",
                        "confidence": 0.8
                    }
                ]
            }

            await self.core.load_domain_knowledge(KnowledgeDomain.SYSTEM_ARCHITECTURE, test_knowledge)

            modes_to_test = [ReasoningMode.SYMBOLIC, ReasoningMode.NEURAL, ReasoningMode.NEUROSYMBOLIC]

            for mode in modes_to_test:
                context = ReasoningContext(
                    query="How should I approach system design?",
                    domain=KnowledgeDomain.SYSTEM_ARCHITECTURE,
                    mode=mode
                )

                result = await self.core.reason(context)
                self.assertEqual(result.mode_used, mode)
                self.assertGreater(result.confidence, 0.0)

        asyncio.run(run_test())


if __name__ == "__main__":
    unittest.main()</content>
<parameter name="filePath">/Users/hankhead/Projects/Personal/nusy-product-team/expeditions/exp_038/core_tests.py