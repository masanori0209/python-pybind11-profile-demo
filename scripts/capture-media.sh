#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORK="${ROOT}/.media-build"
IMG_DIR="${ZENN_IMAGES_DIR:?Set ZENN_IMAGES_DIR to the Zenn images directory}"
PYTHON="${ZENN_MEDIA_PYTHON:-python3}"

if ! "$PYTHON" -c "from PIL import Image" 2>/dev/null; then
  VENV="${ROOT}/.media-venv"
  if [[ ! -x "${VENV}/bin/python" ]]; then
    python3 -m venv "$VENV"
    "${VENV}/bin/pip" install -q pillow
  fi
  PYTHON="${VENV}/bin/python"
fi

DEMO_VENV="${ROOT}/.venv"
if [[ ! -x "${DEMO_VENV}/bin/python" ]]; then
  python3 -m venv "$DEMO_VENV"
  "${DEMO_VENV}/bin/pip" install -U pip scikit-build-core pybind11 cmake ninja -q
  "${DEMO_VENV}/bin/pip" install -e "$ROOT" -q
fi
PY="${DEMO_VENV}/bin/python"

mkdir -p "$WORK" "$IMG_DIR"

sanitize_paths() {
  sed -e "s|${ROOT}|.|g" -e "s|${HOME}|~|g"
}

render_png() {
  local textfile="$1"
  local outfile="$2"
  "$PYTHON" "${ROOT}/scripts/render_terminal_png.py" "$textfile" "$outfile"
}

capture_cprofile() {
  local f="${WORK}/cprofile.txt"
  {
    echo "\$ python scripts/run_cprofile.py --chunks 3000 --top 8"
    "$PY" "${ROOT}/scripts/run_cprofile.py" --chunks 3000 --top 8 --output "${WORK}/profile-python-3000.txt" | sanitize_paths
    echo
    echo "\$ head -n 12 reports/profile-python-3000.txt"
    head -n 12 "${WORK}/profile-python-3000.txt" | sanitize_paths
  } > "$f"
  render_png "$f" "${IMG_DIR}/python-pybind11-demo-cprofile.png"
}

capture_benchmark() {
  local f="${WORK}/benchmark.txt"
  {
    echo "\$ python scripts/benchmark.py --chunks 10000 --rounds 5"
    "$PY" "${ROOT}/scripts/benchmark.py" --chunks 10000 --rounds 5 --output "${WORK}/benchmark-10000.txt"
  } > "$f"
  render_png "$f" "${IMG_DIR}/python-pybind11-demo-benchmark.png"
}

cd "$ROOT"
capture_cprofile
capture_benchmark

echo "created:"
echo "  ${IMG_DIR}/python-pybind11-demo-cprofile.png"
echo "  ${IMG_DIR}/python-pybind11-demo-benchmark.png"
