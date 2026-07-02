#!/usr/bin/env python3
from __future__ import annotations

import argparse
import cProfile
import io
import pstats
from pathlib import Path

from chunkscore.pipeline import rank_chunks_with
from chunkscore.textscore_py import char_ngram_jaccard
from chunkscore.dataset import generate_chunks


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Profile pure-Python chunk ranking")
    parser.add_argument("--chunks", type=int, default=3000, help="Number of chunks to rank")
    parser.add_argument("--top", type=int, default=20, help="Print top N functions")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/profile-python.txt"),
        help="pstats text output path",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    chunks = generate_chunks(args.chunks)
    query = chunks[0]

    profiler = cProfile.Profile()
    profiler.enable()
    ranked = rank_chunks_with(query, chunks, char_ngram_jaccard, n=3)
    profiler.disable()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stream).sort_stats("cumulative")
    stats.print_stats(args.top)
    args.output.write_text(stream.getvalue(), encoding="utf-8")

    print(f"wrote profile report: {args.output}")
    print(f"top result score: {ranked[0][1]:.4f} (chunk {ranked[0][0]})")


if __name__ == "__main__":
    main()
