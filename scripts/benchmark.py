#!/usr/bin/env python3
from __future__ import annotations

import argparse
import statistics
import time
from pathlib import Path

from chunkscore import rank_chunks_cpp
from chunkscore.textscore_py import rank_chunks
from chunkscore.dataset import generate_chunks


def bench(fn, *args, rounds: int = 5) -> list[float]:
    timings: list[float] = []
    for _ in range(rounds):
        start = time.perf_counter()
        fn(*args)
        timings.append(time.perf_counter() - start)
    return timings


def summarize(label: str, timings: list[float]) -> str:
    return (
        f"{label}: "
        f"median={statistics.median(timings):.4f}s "
        f"min={min(timings):.4f}s max={max(timings):.4f}s"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Benchmark Python vs pybind11 chunk ranking")
    parser.add_argument("--chunks", type=int, default=3000)
    parser.add_argument("--rounds", type=int, default=5)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/benchmark.txt"),
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    chunks = generate_chunks(args.chunks)
    query = chunks[0]

    py_timings = bench(lambda: rank_chunks(query, chunks, n=3), rounds=args.rounds)

    lines = [
        f"chunks={args.chunks} rounds={args.rounds}",
        summarize("python", py_timings),
    ]

    if rank_chunks_cpp is None:
        lines.append("cpp: skipped (_textscore_cpp is not built)")
    else:
        cpp_timings = bench(lambda: rank_chunks_cpp(query, chunks, n=3), rounds=args.rounds)
        lines.append(summarize("cpp", cpp_timings))
        ratio = statistics.median(py_timings) / statistics.median(cpp_timings)
        lines.append(f"median_speedup={ratio:.2f}x")

    report = "\n".join(lines) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print(report, end="")


if __name__ == "__main__":
    main()
