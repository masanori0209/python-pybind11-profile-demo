from __future__ import annotations

import random

PREFIXES = [
    "顧客から問い合わせがあり",
    "障害対応中に確認した",
    "次フェーズで対応予定の",
    "社内レビューで指摘された",
    "引き継ぎメモに残っていた",
]

SUFFIXES = [
    "ため、API 連携は見送り CSV 対応とした。",
    "点について、CS から説明済み。",
    "件は、来週の定例で再確認する。",
    "内容は、監査ログにも記録されている。",
    "手順は、Runbook 第3章を参照。",
]

DETAILS = [
    "初回リリースのみの暫定対応",
    "本番環境では feature flag を OFF",
    "staging では再現しない",
    "rollback 手順は別紙",
    "担当チームは Platform",
]


def make_chunk(rng: random.Random, index: int) -> str:
    prefix = PREFIXES[index % len(PREFIXES)]
    suffix = SUFFIXES[(index // len(PREFIXES)) % len(SUFFIXES)]
    detail = DETAILS[(index // (len(PREFIXES) * len(SUFFIXES))) % len(DETAILS)]
    noise = "".join(rng.choice("abcdefghijklmnopqrstuvwxyz0123456789") for _ in range(12))
    return f"[chunk-{index:04d}] {prefix}、{detail}。{suffix} trace={noise}"


def generate_chunks(count: int, seed: int = 42) -> list[str]:
    rng = random.Random(seed)
    return [make_chunk(rng, index) for index in range(count)]
