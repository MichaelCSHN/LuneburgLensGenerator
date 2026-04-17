#!/usr/bin/env bash
# 多方法/多配置批处理占位：逐条用 --from-config 跑，输出到 output/batch_*.stl
# 后续可在宿主机聚合各 JSON 调用 luneburg.compare.build_comparison_placeholder
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
shopt -s nullglob
for f in "$ROOT/examples/"*.json; do
  rel="examples/$(basename "$f")"
  echo "==> $rel"
  docker run --rm -v "$ROOT":/app -w /app luneburg-gen \
    python3 -u Luneburg.py --from-config "$rel"
done
echo "Batch stub done. Inspect output/*.stl and output/*.json"
