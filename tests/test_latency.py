"""Latency measurement tests (NFR-01 / AC-08 / TS-08).

Measures local sequential search latency over a 1,000 customer dataset,
validating p95 <= 50 ms and p99 <= 100 ms.
"""

import statistics
import time
from customer_search.repository import CustomerRepository
from customer_search.search_service import SearchService


def test_search_latency_nfr01(capsys):
    """Verify search latency on 1,000 customers meets p95 <= 50 ms and p99 <= 100 ms."""
    repo = CustomerRepository()
    customers = repo.find_all()
    assert len(customers) == 1000, f"Expected 1,000 customers for NFR-01, found {len(customers)}"

    service = SearchService(repository=repo)

    # Diverse set of representative queries (exact, prefix, substring, diacritics, domain, no-results)
    queries = [
        "José",
        "ana",
        "García",
        "example.com",
        "special",
        "bel",
        "Leonardo",
        "Hélène",
        "nonexistent_query_term",
        "carlos",
    ]

    # Warm-up run
    for q in queries:
        service.search(q)

    # Measurement runs: 10 repetitions of 10 queries = 100 sequential measurements
    latencies_ms: list[float] = []
    for q in queries * 10:
        start_time = time.perf_counter()
        service.search(q)
        duration_ms = (time.perf_counter() - start_time) * 1000.0
        latencies_ms.append(duration_ms)

    latencies_ms.sort()
    n = len(latencies_ms)
    p50 = statistics.median(latencies_ms)
    p95 = latencies_ms[int(n * 0.95)]
    p99 = latencies_ms[int(n * 0.99)]

    # Print report for traceability and verification
    report = (
        f"\n--- Latency Benchmark (NFR-01 / AC-08 / TS-08) ---\n"
        f"Catalog size: {len(customers)} customers\n"
        f"Total queries executed: {n}\n"
        f"Observed p50: {p50:.2f} ms\n"
        f"Observed p95: {p95:.2f} ms (Threshold: <= 50.0 ms)\n"
        f"Observed p99: {p99:.2f} ms (Threshold: <= 100.0 ms)\n"
        f"---------------------------------------------------\n"
    )
    print(report)

    # Verify thresholds per AC-08
    assert p95 <= 50.0, f"p95 latency {p95:.2f} ms exceeded threshold 50.0 ms"
    assert p99 <= 100.0, f"p99 latency {p99:.2f} ms exceeded threshold 100.0 ms"
