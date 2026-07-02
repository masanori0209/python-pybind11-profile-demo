"""Pure Python reference implementation — intentionally kept simple and slow."""

from __future__ import annotations

from typing import Iterable


def normalize(text: str) -> str:
    lowered = text.lower()
    cleaned = []
    for ch in lowered:
        if ch.isalnum():
            cleaned.append(ch)
        elif ch.isspace():
            if cleaned and cleaned[-1] != " ":
                cleaned.append(" ")
    return "".join(cleaned).strip()


def char_ngrams(text: str, n: int) -> set[str]:
    if n <= 0 or n > len(text):
        return set()
    return {text[i : i + n] for i in range(len(text) - n + 1)}


def char_ngram_jaccard(left: str, right: str, n: int = 3) -> float:
    left_norm = normalize(left)
    right_norm = normalize(right)
    left_grams = char_ngrams(left_norm, n)
    right_grams = char_ngrams(right_norm, n)

    if not left_grams and not right_grams:
        return 1.0
    if not left_grams or not right_grams:
        return 0.0

    intersection = len(left_grams & right_grams)
    union = len(left_grams | right_grams)
    return intersection / union if union else 0.0


def rank_chunks(query: str, chunks: Iterable[str], n: int = 3) -> list[tuple[int, float]]:
    ranked = [(index, char_ngram_jaccard(query, chunk, n)) for index, chunk in enumerate(chunks)]
    ranked.sort(key=lambda item: item[1], reverse=True)
    return ranked
