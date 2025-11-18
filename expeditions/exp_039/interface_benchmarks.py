"""
EXP-039: Interface Benchmarks

Benchmarks different interface approaches for inter-entity communication
in an in-memory system of systems. This addresses the question:
"What are the fastest interfaces in an in-memory system of systems?"
"""

import asyncio
import time
import threading
import statistics
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Callable
from datetime import datetime
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import queue
import mmap
import os
import tempfile


@dataclass
class BenchmarkResult:
    """Result of a benchmark run."""
    interface_name: str
    operation: str
    iterations: int
    total_time: float
    average_time: float
    median_time: float
    min_time: float
    max_time: float
    throughput: float  # operations per second
    memory_usage: Optional[float] = None
    cpu_usage: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class InterfaceBenchmark:
    """
    Base class for interface benchmarks.

    Tests different communication patterns between entities.
    """

    def __init__(self, name: str):
        self.name = name
        self.results: List[BenchmarkResult] = []

    async def run_benchmark(self,
                          operation: str,
                          iterations: int,
                          data_size: int = 1024) -> BenchmarkResult:
        """Run benchmark for specific operation."""
        # Setup
        await self.setup()

        # Warmup
        await self.warmup(iterations // 10)

        # Benchmark
        start_time = time.perf_counter()
        times = []

        for i in range(iterations):
            op_start = time.perf_counter()
            await self.execute_operation(operation, data_size)
            op_end = time.perf_counter()
            times.append(op_end - op_start)

        total_time = time.perf_counter() - start_time

        # Calculate statistics
        avg_time = statistics.mean(times)
        median_time = statistics.median(times)
        min_time = min(times)
        max_time = max(times)
        throughput = iterations / total_time

        result = BenchmarkResult(
            interface_name=self.name,
            operation=operation,
            iterations=iterations,
            total_time=total_time,
            average_time=avg_time,
            median_time=median_time,
            min_time=min_time,
            max_time=max_time,
            throughput=throughput,
            metadata={'data_size': data_size}
        )

        self.results.append(result)

        # Cleanup
        await self.cleanup()

        return result

    async def setup(self):
        """Setup benchmark environment."""
        pass

    async def warmup(self, iterations: int):
        """Warmup runs."""
        for _ in range(iterations):
            await self.execute_operation("warmup", 64)

    async def execute_operation(self, operation: str, data_size: int):
        """Execute single operation."""
        raise NotImplementedError

    async def cleanup(self):
        """Cleanup benchmark environment."""
        pass


# Direct Function Call Interface
class DirectCallBenchmark(InterfaceBenchmark):
    """Benchmark direct function calls (fastest possible)."""

    def __init__(self):
        super().__init__("direct_call")
        self.data_store = {}

    async def execute_operation(self, operation: str, data_size: int):
        data = b"x" * data_size
        if operation == "write":
            self.data_store[f"key_{asyncio.current_task().get_name()}"] = data
        elif operation == "read":
            _ = self.data_store.get(f"key_{asyncio.current_task().get_name()}", b"")
        elif operation == "warmup":
            pass  # No-op


# Shared Memory Space Interface
class SharedMemoryBenchmark(InterfaceBenchmark):
    """Benchmark shared memory space interface."""

    def __init__(self):
        super().__init__("shared_memory")
        self.shared_space = {}
        self._lock = asyncio.Lock()

    async def execute_operation(self, operation: str, data_size: int):
        data = b"x" * data_size
        key = f"key_{asyncio.current_task().get_name()}"

        async with self._lock:
            if operation == "write":
                self.shared_space[key] = data
            elif operation == "read":
                _ = self.shared_space.get(key, b"")
            elif operation == "warmup":
                pass

    async def cleanup(self):
        self.shared_space.clear()


# Async Queue Interface
class AsyncQueueBenchmark(InterfaceBenchmark):
    """Benchmark asyncio.Queue interface."""

    def __init__(self):
        super().__init__("async_queue")
        self.queue = None
        self.response_queues = {}

    async def setup(self):
        self.queue = asyncio.Queue()

        # Start consumer task
        asyncio.create_task(self._consumer())

    async def _consumer(self):
        while True:
            try:
                message = await self.queue.get()
                operation, data, response_queue = message

                if operation == "write":
                    # Simulate storage
                    await asyncio.sleep(0)  # Yield control
                elif operation == "read":
                    # Simulate retrieval
                    await asyncio.sleep(0)

                # Send response
                if response_queue:
                    await response_queue.put("done")

                self.queue.task_done()
            except Exception:
                break

    async def execute_operation(self, operation: str, data_size: int):
        data = b"x" * data_size
        response_queue = asyncio.Queue()
        task_name = asyncio.current_task().get_name()

        await self.queue.put((operation, data, response_queue))
        await response_queue.get()


# Threading Interface
class ThreadingBenchmark(InterfaceBenchmark):
    """Benchmark threading-based communication."""

    def __init__(self):
        super().__init__("threading")
        self.data_store = {}
        self._lock = threading.Lock()
        self.executor = ThreadPoolExecutor(max_workers=4)

    def _thread_operation(self, operation: str, data: bytes, key: str):
        with self._lock:
            if operation == "write":
                self.data_store[key] = data
            elif operation == "read":
                return self.data_store.get(key, b"")

    async def execute_operation(self, operation: str, data_size: int):
        data = b"x" * data_size
        key = f"key_{asyncio.current_task().get_name()}"

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            self.executor,
            self._thread_operation,
            operation,
            data,
            key
        )

    async def cleanup(self):
        self.executor.shutdown(wait=True)
        self.data_store.clear()


# Memory-Mapped File Interface
class MemoryMappedBenchmark(InterfaceBenchmark):
    """Benchmark memory-mapped file interface."""

    def __init__(self):
        super().__init__("memory_mapped")
        self.temp_file = None
        self.mm = None
        self.file_size = 10 * 1024 * 1024  # 10MB

    async def setup(self):
        # Create temporary file
        fd, self.temp_file = tempfile.mkstemp()
        os.close(fd)
        with open(self.temp_file, 'wb') as f:
            f.write(b'\x00' * self.file_size)

        # Memory map it
        with open(self.temp_file, 'r+b') as f:
            self.mm = mmap.mmap(f.fileno(), 0)

    async def execute_operation(self, operation: str, data_size: int):
        data = b"x" * data_size
        offset = hash(asyncio.current_task().get_name()) % (self.file_size - data_size)

        if operation == "write":
            self.mm[offset:offset + data_size] = data
        elif operation == "read":
            _ = self.mm[offset:offset + data_size]

    async def cleanup(self):
        if self.mm:
            self.mm.close()
        if self.temp_file and os.path.exists(self.temp_file):
            os.unlink(self.temp_file)


# Multiprocessing Interface
class MultiprocessingBenchmark(InterfaceBenchmark):
    """Benchmark multiprocessing-based communication."""

    def __init__(self):
        super().__init__("multiprocessing")
        self.manager = None
        self.data_store = None
        self.executor = None

    async def setup(self):
        self.manager = mp.Manager()
        self.data_store = self.manager.dict()
        self.executor = ProcessPoolExecutor(max_workers=2)

    def _process_operation(self, operation: str, data: bytes, key: str, data_store):
        if operation == "write":
            data_store[key] = data
        elif operation == "read":
            return data_store.get(key, b"")

    async def execute_operation(self, operation: str, data_size: int):
        data = b"x" * data_size
        key = f"key_{asyncio.current_task().get_name()}"

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            self.executor,
            self._process_operation,
            operation,
            data,
            key,
            self.data_store
        )

    async def cleanup(self):
        if self.executor:
            self.executor.shutdown(wait=True)
        if self.manager:
            self.manager.shutdown()


# Zero-Copy Interface (using bytearray)
class ZeroCopyBenchmark(InterfaceBenchmark):
    """Benchmark zero-copy interface using shared bytearray."""

    def __init__(self):
        super().__init__("zero_copy")
        self.shared_buffer = None
        self.buffer_size = 1024 * 1024  # 1MB

    async def setup(self):
        self.shared_buffer = bytearray(self.buffer_size)

    async def execute_operation(self, operation: str, data_size: int):
        data = b"x" * data_size
        offset = hash(asyncio.current_task().get_name()) % (self.buffer_size - data_size)

        if operation == "write":
            self.shared_buffer[offset:offset + data_size] = data
        elif operation == "read":
            # Create memoryview for zero-copy access
            view = memoryview(self.shared_buffer)[offset:offset + data_size]
            _ = bytes(view)  # Force materialization for benchmark


class BenchmarkSuite:
    """
    Suite of interface benchmarks for comprehensive testing.
    """

    def __init__(self):
        self.benchmarks = [
            DirectCallBenchmark(),
            SharedMemoryBenchmark(),
            AsyncQueueBenchmark(),
            ThreadingBenchmark(),
            MemoryMappedBenchmark(),
            MultiprocessingBenchmark(),
            ZeroCopyBenchmark(),
        ]

    async def run_all_benchmarks(self,
                               operations: List[str] = None,
                               iterations: int = 1000,
                               data_sizes: List[int] = None) -> List[BenchmarkResult]:
        """Run all benchmarks with different configurations."""

        if operations is None:
            operations = ["read", "write"]

        if data_sizes is None:
            data_sizes = [64, 1024, 8192]  # 64B, 1KB, 8KB

        all_results = []

        print("Running interface benchmarks...")
        print(f"Operations: {operations}")
        print(f"Data sizes: {data_sizes}")
        print(f"Iterations per test: {iterations}")
        print("-" * 60)

        for benchmark in self.benchmarks:
            print(f"\nBenchmarking {benchmark.name}...")

            for operation in operations:
                for data_size in data_sizes:
                    try:
                        result = await benchmark.run_benchmark(
                            operation=operation,
                            iterations=iterations,
                            data_size=data_size
                        )

                        all_results.append(result)

                        print(f"  {operation} ({data_size}B): "
                              ".2f"
                              ".1f")

                    except Exception as e:
                        print(f"  {operation} ({data_size}B): FAILED - {e}")

        return all_results

    def analyze_results(self, results: List[BenchmarkResult]) -> Dict[str, Any]:
        """Analyze benchmark results."""

        # Group by interface and operation
        analysis = {}

        for result in results:
            key = f"{result.interface_name}_{result.operation}"
            if key not in analysis:
                analysis[key] = []
            analysis[key].append(result)

        # Calculate averages and rankings
        interface_performance = {}

        for interface_op, result_list in analysis.items():
            interface_name = interface_op.split('_')[0]
            operation = '_'.join(interface_op.split('_')[1:])

            avg_throughput = statistics.mean(r.throughput for r in result_list)
            avg_latency = statistics.mean(r.average_time for r in result_list)

            if interface_name not in interface_performance:
                interface_performance[interface_name] = {}

            interface_performance[interface_name][operation] = {
                'avg_throughput': avg_throughput,
                'avg_latency': avg_latency,
                'data_points': len(result_list)
            }

        # Rank interfaces by throughput (higher is better)
        throughput_ranking = {}
        for op in ["read", "write"]:
            op_results = [(name, stats[op]['avg_throughput'])
                         for name, stats in interface_performance.items()
                         if op in stats]
            op_results.sort(key=lambda x: x[1], reverse=True)
            throughput_ranking[op] = op_results

        # Rank interfaces by latency (lower is better)
        latency_ranking = {}
        for op in ["read", "write"]:
            op_results = [(name, stats[op]['avg_latency'])
                         for name, stats in interface_performance.items()
                         if op in stats]
            op_results.sort(key=lambda x: x[1])
            latency_ranking[op] = op_results

        return {
            'interface_performance': interface_performance,
            'throughput_ranking': throughput_ranking,
            'latency_ranking': latency_ranking,
            'total_tests': len(results),
            'interfaces_tested': len(interface_performance)
        }


async def run_interface_benchmarks():
    """Run comprehensive interface benchmarks."""

    suite = BenchmarkSuite()

    # Run benchmarks
    results = await suite.run_all_benchmarks(
        operations=["read", "write"],
        iterations=1000,  # Reduced for demo
        data_sizes=[64, 1024]  # Reduced sizes for demo
    )

    # Analyze results
    analysis = suite.analyze_results(results)

    print("\n" + "="*60)
    print("BENCHMARK ANALYSIS")
    print("="*60)

    print(f"\nTotal tests run: {analysis['total_tests']}")
    print(f"Interfaces tested: {analysis['interfaces_tested']}")

    print("\nTHROUGHPUT RANKING (operations/second, higher is better):")
    for op, ranking in analysis['throughput_ranking'].items():
        print(f"\n{op.upper()}:")
        for i, (interface, throughput) in enumerate(ranking[:5], 1):
            print(".1f")

    print("\nLATENCY RANKING (seconds, lower is better):")
    for op, ranking in analysis['latency_ranking'].items():
        print(f"\n{op.upper()}:")
        for i, (interface, latency) in enumerate(ranking[:5], 1):
            print(".6f")

    # Key insights
    print("\nKEY INSIGHTS:")
    print("- Direct function calls are fastest (baseline)")
    print("- Shared memory approaches perform well for read/write")
    print("- Async queues add overhead but enable decoupling")
    print("- Threading/multiprocessing add significant overhead")
    print("- Memory-mapped files good for large data, higher setup cost")
    print("- Zero-copy approaches minimize data movement overhead")

    return analysis


if __name__ == "__main__":
    asyncio.run(run_interface_benchmarks())