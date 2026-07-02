from __future__ import annotations

from collections.abc import Callable
from typing import Iterable


def rank_chunks_with(
    query: str,
    chunks: Iterable[str],
    scorer: Callable[[str, str, int], float],
    n: int = 3,
) -> list[tuple[int, float]]:
    chunk_list = list(chunks)
    ranked = [(index, scorer(query, chunk, n)) for index, chunk in enumerate(chunk_list)]
    ranked.sort(key=lambda item: item[1], reverse=True)
    return ranked
