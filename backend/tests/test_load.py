"""
Load testing script for performance benchmarking.
Demonstrates scalability testing for the report (K24).

Run with: python -m pytest backend/tests/test_load.py -v -s
"""

import time
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def single_health_request():
    """Make a single health check request and return response time in ms."""
    start = time.perf_counter()
    response = client.get("/health")
    elapsed = (time.perf_counter() - start) * 1000  # Convert to ms
    assert response.status_code == 200
    return elapsed


def test_health_latency_single():
    """Benchmark: Single request latency for /health endpoint."""
    times = [single_health_request() for _ in range(100)]
    avg = statistics.mean(times)
    p95 = sorted(times)[94]
    p99 = sorted(times)[98]
    print(f"\n{'='*60}")
    print("PERFORMANCE BENCHMARK: /health (100 sequential requests)")
    print(f"{'='*60}")
    print(f"  Average latency:  {avg:.2f} ms")
    print(f"  P95 latency:      {p95:.2f} ms")
    print(f"  P99 latency:      {p99:.2f} ms")
    print(f"  Min latency:      {min(times):.2f} ms")
    print(f"  Max latency:      {max(times):.2f} ms")
    print(f"{'='*60}")
    # NFR2: API response latency < 2000ms
    assert avg < 100, f"Average latency {avg:.2f}ms exceeds 100ms threshold"


def test_health_concurrent_load():
    """Benchmark: Concurrent request handling (simulates NFR1 - 50+ users)."""
    num_requests = 50
    results = []

    start_total = time.perf_counter()
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(single_health_request) for _ in range(num_requests)]
        for future in as_completed(futures):
            results.append(future.result())
    total_time = (time.perf_counter() - start_total) * 1000

    avg = statistics.mean(results)
    p95 = sorted(results)[int(0.95 * len(results))]
    throughput = num_requests / (total_time / 1000)

    print(f"\n{'='*60}")
    print(f"LOAD TEST: /health ({num_requests} concurrent requests)")
    print(f"{'='*60}")
    print(f"  Total time:       {total_time:.2f} ms")
    print(f"  Average latency:  {avg:.2f} ms")
    print(f"  P95 latency:      {p95:.2f} ms")
    print(f"  Throughput:       {throughput:.0f} requests/second")
    print(f"  All succeeded:    {len(results)}/{num_requests}")
    print(f"{'='*60}")
    # All requests should complete successfully
    assert len(results) == num_requests
    # Throughput should be reasonable
    assert throughput > 100, f"Throughput {throughput:.0f} rps below 100 rps threshold"
