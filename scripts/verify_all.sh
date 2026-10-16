#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

sha256sum -c certificates/constructions/packing_12.sha256
python3 verify/verify_packing.py certificates/constructions/packing_12.json
python3 lean/verification/check_model_independently.py
python3 lean/verification/verify_source_structure.py

BINARY="$(mktemp -t p2632-checker-XXXXXXXX)"
trap 'rm -f "$BINARY"' EXIT
g++ -O2 -std=c++17 verify/independent_checker.cpp -o "$BINARY"
"$BINARY" certificates/constructions/packing_12.txt

echo 'All locally runnable mathematical certificate checks: PASS'
echo 'Lean compilation is separate: cd lean && lake build'
