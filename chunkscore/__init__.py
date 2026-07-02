from chunkscore.textscore_py import char_ngram_jaccard as char_ngram_jaccard_py
from chunkscore.textscore_py import rank_chunks as rank_chunks_py

try:
    from chunkscore._textscore_cpp import char_ngram_jaccard as char_ngram_jaccard_cpp
    from chunkscore._textscore_cpp import rank_chunks as rank_chunks_cpp
except ImportError:  # pragma: no cover - editable install without build
    char_ngram_jaccard_cpp = None
    rank_chunks_cpp = None

__all__ = [
    "char_ngram_jaccard_py",
    "rank_chunks_py",
    "char_ngram_jaccard_cpp",
    "rank_chunks_cpp",
]
