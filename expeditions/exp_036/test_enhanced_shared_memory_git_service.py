"""
Test Enhanced Shared Memory Git Service

Tests atomic operations, conflict detection, performance monitoring,
and multi-agent collaboration scenarios for the enhanced shared memory Git service.
"""

import asyncio
import tempfile
import time
import unittest
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from enhanced_shared_memory_git_service import (
    EnhancedSharedMemoryGitService,
    get_enhanced_shared_memory_git_service,
    Commit,
    Branch,
    AtomicOperation,
    PerformanceMetrics
)


class TestEnhancedSharedMemoryGitService(unittest.TestCase):
    """Test cases for the enhanced shared memory Git service."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.service = EnhancedSharedMemoryGitService(self.temp_dir, max_memory_mb=256)

    def tearDown(self):
        """Clean up test fixtures."""
        self.service.cleanup_memory()

    def test_initialization(self):
        """Test service initialization creates default structures."""
        self.assertIn("main", self.service.branches)
        self.assertEqual(len(self.service.commits), 1)
        self.assertEqual(len(self.service.branches), 1)

        main_branch = self.service.branches["main"]
        self.assertIsNotNone(main_branch.head_commit_id)
        self.assertIn(main_branch.head_commit_id, self.service.commits)

    def test_atomic_operation_creation(self):
        """Test creating atomic operations."""
        operations = [
            {
                "type": "create",
                "file_path": "test.txt",
                "content": "Hello World"
            }
        ]

        operation_id = asyncio.run(self.service.create_atomic_operation(operations))
        self.assertIn(operation_id, self.service.pending_operations)

        operation = self.service.pending_operations[operation_id]
        self.assertEqual(operation.status, "pending")
        self.assertEqual(len(operation.operations), 1)
        self.assertEqual(operation.operations[0]["file_path"], "test.txt")

    def test_atomic_operation_execution(self):
        """Test executing atomic operations successfully."""
        operations = [
            {
                "type": "create",
                "file_path": "test.txt",
                "content": "Hello World"
            }
        ]

        operation_id = asyncio.run(self.service.create_atomic_operation(operations))
        success = asyncio.run(self.service.execute_atomic_operation(operation_id))

        self.assertTrue(success)
        self.assertNotIn(operation_id, self.service.pending_operations)
        self.assertIn(operation_id, self.service.completed_operations)

        # Verify file was created
        content = self.service.get_file_content("test.txt")
        self.assertEqual(content, "Hello World")

    def test_atomic_operation_with_dependencies(self):
        """Test atomic operations with dependencies."""
        # Create first operation
        op1_operations = [
            {
                "type": "create",
                "file_path": "base.txt",
                "content": "Base content"
            }
        ]
        op1_id = asyncio.run(self.service.create_atomic_operation(op1_operations))

        # Create dependent operation
        op2_operations = [
            {
                "type": "update",
                "file_path": "base.txt",
                "content": "Updated content"
            }
        ]
        op2_id = asyncio.run(self.service.create_atomic_operation(op2_operations, {op1_id}))

        # Try to execute dependent operation before dependency - should fail
        success = asyncio.run(self.service.execute_atomic_operation(op2_id))
        self.assertFalse(success)

        # Execute dependency first
        success = asyncio.run(self.service.execute_atomic_operation(op1_id))
        self.assertTrue(success)

        # Now dependent operation should succeed
        success = asyncio.run(self.service.execute_atomic_operation(op2_id))
        self.assertTrue(success)

        # Verify final content
        content = self.service.get_file_content("base.txt")
        self.assertEqual(content, "Updated content")

    def test_conflict_detection(self):
        """Test conflict detection between operations."""
        # Create two operations that modify the same file
        op1_operations = [
            {
                "type": "create",
                "file_path": "conflict.txt",
                "content": "Version 1"
            }
        ]
        op1_id = asyncio.run(self.service.create_atomic_operation(op1_operations))

        op2_operations = [
            {
                "type": "create",
                "file_path": "conflict.txt",
                "content": "Version 2"
            }
        ]
        op2_id = asyncio.run(self.service.create_atomic_operation(op2_operations))

        # Both operations should detect conflict with each other
        conflicts1 = self.service.detect_conflicts(op1_id)
        conflicts2 = self.service.detect_conflicts(op2_id)

        self.assertIn(op2_id, conflicts1)
        self.assertIn(op1_id, conflicts2)

    def test_batch_operation_execution(self):
        """Test batch execution of multiple operations."""
        operations_data = [
            ([{"type": "create", "file_path": f"file{i}.txt", "content": f"Content {i}"}],
             set())
            for i in range(5)
        ]

        operation_ids = []
        for ops, deps in operations_data:
            op_id = asyncio.run(self.service.create_atomic_operation(ops, deps))
            operation_ids.append(op_id)

        # Execute all operations in batch
        results = asyncio.run(self.service.batch_execute_operations(operation_ids))

        # All should succeed
        for op_id in operation_ids:
            self.assertTrue(results[op_id])
            self.assertIn(op_id, self.service.completed_operations)

        # Verify all files were created
        for i in range(5):
            content = self.service.get_file_content(f"file{i}.txt")
            self.assertEqual(content, f"Content {i}")

    def test_file_operations(self):
        """Test various file operations (create, update, delete)."""
        # Create file
        create_ops = [{"type": "create", "file_path": "test.txt", "content": "Initial"}]
        op_id = asyncio.run(self.service.create_atomic_operation(create_ops))
        asyncio.run(self.service.execute_atomic_operation(op_id))

        content = self.service.get_file_content("test.txt")
        self.assertEqual(content, "Initial")

        # Update file
        update_ops = [{"type": "update", "file_path": "test.txt", "content": "Updated"}]
        op_id = asyncio.run(self.service.create_atomic_operation(update_ops))
        asyncio.run(self.service.execute_atomic_operation(op_id))

        content = self.service.get_file_content("test.txt")
        self.assertEqual(content, "Updated")

        # Delete file
        delete_ops = [{"type": "delete", "file_path": "test.txt"}]
        op_id = asyncio.run(self.service.create_atomic_operation(delete_ops))
        asyncio.run(self.service.execute_atomic_operation(op_id))

        content = self.service.get_file_content("test.txt")
        self.assertIsNone(content)

    def test_performance_metrics(self):
        """Test performance metrics collection."""
        initial_metrics = self.service.get_performance_metrics()

        # Create and execute some operations
        for i in range(10):
            ops = [{"type": "create", "file_path": f"perf{i}.txt", "content": f"Data {i}"}]
            op_id = asyncio.run(self.service.create_atomic_operation(ops))
            asyncio.run(self.service.execute_atomic_operation(op_id))

        final_metrics = self.service.get_performance_metrics()

        # Metrics should be updated
        self.assertGreater(final_metrics.total_commits, initial_metrics.total_commits)
        self.assertGreater(final_metrics.total_operations, initial_metrics.total_operations)
        self.assertGreaterEqual(final_metrics.memory_usage_mb, 0)

    def test_list_files(self):
        """Test listing files at different commits."""
        # Create some files
        files_to_create = ["a.txt", "b.txt", "c.txt"]
        for filename in files_to_create:
            ops = [{"type": "create", "file_path": filename, "content": f"Content of {filename}"}]
            op_id = asyncio.run(self.service.create_atomic_operation(ops))
            asyncio.run(self.service.execute_atomic_operation(op_id))

        files = self.service.list_files()
        self.assertEqual(set(files), set(files_to_create))

        # Delete one file
        ops = [{"type": "delete", "file_path": "b.txt"}]
        op_id = asyncio.run(self.service.create_atomic_operation(ops))
        asyncio.run(self.service.execute_atomic_operation(op_id))

        files = self.service.list_files()
        self.assertEqual(set(files), {"a.txt", "c.txt"})

    def test_concurrent_operations(self):
        """Test concurrent execution of operations."""
        def create_and_execute_file(index):
            ops = [{"type": "create", "file_path": f"concurrent{index}.txt", "content": f"Concurrent {index}"}]
            op_id = asyncio.run(self.service.create_atomic_operation(ops))
            return asyncio.run(self.service.execute_atomic_operation(op_id))

        # Execute operations concurrently
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(create_and_execute_file, i) for i in range(10)]
            results = [future.result() for future in as_completed(futures)]

        # All should succeed
        self.assertTrue(all(results))

        # All files should exist
        for i in range(10):
            content = self.service.get_file_content(f"concurrent{i}.txt")
            self.assertEqual(content, f"Concurrent {i}")

    def test_memory_cleanup(self):
        """Test memory cleanup functionality."""
        # Create many files
        for i in range(100):
            ops = [{"type": "create", "file_path": f"cleanup{i}.txt", "content": f"Content {i}" * 100}]
            op_id = asyncio.run(self.service.create_atomic_operation(ops))
            asyncio.run(self.service.execute_atomic_operation(op_id))

        initial_content_count = len(self.service.file_contents)

        # Delete half the files
        for i in range(0, 100, 2):
            ops = [{"type": "delete", "file_path": f"cleanup{i}.txt"}]
            op_id = asyncio.run(self.service.create_atomic_operation(ops))
            asyncio.run(self.service.execute_atomic_operation(op_id))

        # Run cleanup
        self.service.cleanup_memory()

        # Should have fewer content entries now
        final_content_count = len(self.service.file_contents)
        self.assertLess(final_content_count, initial_content_count)


class TestGlobalService(unittest.TestCase):
    """Test the global service instance management."""

    def test_get_service_instance(self):
        """Test getting the global service instance."""
        with tempfile.TemporaryDirectory() as temp_dir:
            service1 = get_enhanced_shared_memory_git_service(temp_dir)
            service2 = get_enhanced_shared_memory_git_service(temp_dir)

            # Should be the same instance
            self.assertIs(service1, service2)

            # Different directory should create new instance
            with tempfile.TemporaryDirectory() as temp_dir2:
                service3 = get_enhanced_shared_memory_git_service(temp_dir2)
if __name__ == "__main__":
    unittest.main()
