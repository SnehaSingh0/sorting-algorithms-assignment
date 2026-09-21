"""Run the student sorting benchmark from the command line."""

import argparse
from typing import List

from benchmark import benchmark_dataset, print_results, write_results_csv
from sorting_algorithms import ALGORITHMS
from student_records import generate_students


DEFAULT_SIZES = [10_000]


def parse_arguments() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Compare five sorting algorithms on student records.")
	parser.add_argument(
		"--sizes",
		nargs="+",
		type=int,
		default=DEFAULT_SIZES,
		help="In-memory dataset sizes, for example 10000 100000.",
	)
	parser.add_argument(
		"--algorithms",
		nargs="+",
		choices=list(ALGORITHMS),
		default=list(ALGORITHMS),
		help="Algorithms to benchmark.",
	)
	parser.add_argument("--output", default="benchmark_results.csv", help="CSV output path.")
	parser.add_argument("--seed", type=int, default=42, help="Seed for repeatable data generation.")
	return parser.parse_args()


def run_benchmark(sizes: List[int], algorithm_names: List[str], output_path: str, seed: int) -> None:
	all_results = []
	for size in sizes:
		if size < 0:
			raise ValueError("Dataset sizes must be non-negative")
		print(f"Generating {size:,} student records...")
		students = generate_students(size, seed=seed)
		all_results.extend(benchmark_dataset(students, lambda student: student.marks, algorithm_names))

	print_results(all_results)
	write_results_csv(all_results, output_path)
	print(f"\nCSV report written to {output_path}")


if __name__ == "__main__":
	arguments = parse_arguments()
	run_benchmark(arguments.sizes, arguments.algorithms, arguments.output, arguments.seed)
