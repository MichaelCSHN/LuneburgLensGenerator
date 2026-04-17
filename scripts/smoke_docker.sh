#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
docker run --rm -v "$(pwd)":/app -w /app luneburg-gen python3 -u Luneburg.py \
  --resolution 2 --step 5.0 --k 10 -o output/smoke.stl
test -s output/smoke.stl
test -s output/smoke.json
python3 -c "import json; d=json.load(open('output/smoke.json')); assert 'pipeline' in d"
echo "Smoke OK: output/smoke.stl, output/smoke.json"
