"""Benchmark orchestration and CSV reporting."""

import csv
import multiprocessing
from queue import Empty
import time
from dataclasses import dataclass
from typing import Callable, Dict, Iterable, List, Optional

from sorting_algorithms import ALGORITHMS, RecordKey
from student_records import StudentRecord

TIME_LIMIT_SECONDS = 300.0


@dataclass(frozen=True)
class BenchmarkResult:
    dataset_size: int
    algorithm: str
    execution_time: Optional[float]
    status: str


def is_sorted(records: List[StudentRecord], key: RecordKey) -> bool:
    """Return True when records are in non-decreasing key order."""
    for index in range(1, len(records)):
        if key(records[index - 1]) > key(records[index]):
            return False
    return True


def _same_input_order(first: List[StudentRecord], second: List[StudentRecord]) -> bool:
    """Check that two algorithm inputs contain the same records in the same order."""
    if len(first) != len(second):
        return False
    for first_record, second_record in zip(first, second):
        if first_record != second_record:
            return False
    return True


def _sorting_worker(
    records: List[StudentRecord],
    algorithm_name: str,
    result_queue: multiprocessing.Queue,
) -> None:
    """Sort and verify one copy in a child process.

    The worker uses the fixed benchmark key directly because a lambda key is
    not reliably picklable when multiprocessing uses Windows ``spawn``.
    """
    key = lambda student: student.marks
    start = time.perf_counter()
    output = ALGORITHMS[algorithm_name](records, key)
    elapsed = time.perf_counter() - start
    status = "PASS" if is_sorted(output, key) else "FAILED - incorrect order"
    result_queue.put((elapsed, status))


def _run_with_timeout(
    records: List[StudentRecord],
    algorithm_name: str,
    time_limit: float,
) -> tuple[Optional[float], str]:
    """Run one sort in a Windows-compatible process with a hard deadline."""
    context = multiprocessing.get_context("spawn")
    result_queue = context.Queue()
    process = context.Process(
        target=_sorting_worker,
        args=(records, algorithm_name, result_queue),
    )
    process.start()
    try:
        try:
            elapsed, status = result_queue.get(timeout=time_limit)
        except Empty:
            if process.is_alive():
                process.terminate()
            process.join()
            return None, "TIMEOUT"
        return elapsed, status
    finally:
        if process.is_alive():
            process.terminate()
        process.join()
        result_queue.close()
        result_queue.join_thread()


def benchmark_dataset(
    records: List[StudentRecord],
    key: RecordKey,
    algorithm_names: Iterable[str] = ALGORITHMS.keys(),
) -> List[BenchmarkResult]:
    """Run selected algorithms with a separate 300-second process limit."""
    results: List[BenchmarkResult] = []
    baseline = list(records)

    for algorithm_name in algorithm_names:
        if algorithm_name not in ALGORITHMS:
            raise ValueError(f"Unknown algorithm: {algorithm_name}")

        algorithm_input = list(records)
        if not _same_input_order(baseline, algorithm_input):
            results.append(BenchmarkResult(len(records), algorithm_name, None, "FAILED - unfair input"))
            continue

        elapsed, status = _run_with_timeout(
            algorithm_input,
            algorithm_name,
            TIME_LIMIT_SECONDS,
        )
        results.append(BenchmarkResult(len(records), algorithm_name, elapsed, status))

    return results


def write_results_csv(results: Iterable[BenchmarkResult], output_path: str) -> None:
    """Write an Excel-friendly CSV report."""
    with open(output_path, "w", newline="", encoding="utf-8") as output_file:
        writer = csv.writer(output_file)
        writer.writerow(["dataset size", "algorithm", "execution time", "status"])
        for result in results:
            execution_time = "" if result.execution_time is None else f"{result.execution_time:.6f}"
            writer.writerow([result.dataset_size, result.algorithm, execution_time, result.status])


def print_results(results: Iterable[BenchmarkResult]) -> None:
    """Print the same information in a readable comparison table."""
    print(f"{'Dataset size':>14} | {'Algorithm':<16} | {'Time (seconds)':>15} | Status")
    print("-" * 70)
    for result in results:
        time_text = "N/A" if result.execution_time is None else f"{result.execution_time:.6f}"
        print(f"{result.dataset_size:>14,} | {result.algorithm:<16} | {time_text:>15} | {result.status}")
