# python-pybind11-profile-demo

RAG のチャンク再ランキングを想定した、**cProfile → pybind11 で 1 関数 C++ 化** の最小デモです。

解説記事（Zenn）: （公開後に URL を追記）

> **Note:** 本番 RAG の精度比較ではありません。合成チャンクに対する文字 n-gram Jaccard の再ランキングで、計測と C++ 化の手順を再現するためのローカル実験用です。

## できること

- 純 Python 実装で `rank_chunks()` を実行
- `cProfile` で `char_ngram_jaccard()` がボトルネックだと確認
- 同じ API を pybind11 で C++ 化
- `scripts/benchmark.py` で before / after を計測

## 前提

- Python 3.10+
- C++ コンパイラ（macOS なら Xcode CLT、Linux なら g++ など）
- CMake / Ninja（`pip install cmake ninja` でも可）

## セットアップ

```bash
git clone https://github.com/masanori0209/python-pybind11-profile-demo.git
cd python-pybind11-profile-demo

python3 -m venv .venv
source .venv/bin/activate
pip install -U pip scikit-build-core pybind11 cmake ninja
pip install -e .
```

## プロファイル

```bash
python scripts/run_cprofile.py --chunks 3000 --top 12
```

## ベンチマーク

```bash
python scripts/benchmark.py --chunks 10000 --rounds 5
```

## 構成

```text
python-pybind11-profile-demo/
├── chunkscore/
│   ├── textscore_py.py      # 純 Python（計測対象）
│   └── pipeline.py
├── src/textscore_cpp.cpp    # pybind11 実装
├── scripts/
│   ├── run_cprofile.py
│   └── benchmark.py
└── reports/                 # 計測ログ（git 管理外）
```
