#!/usr/bin/env bash
# Run one validation battery — head or parent — writing one log per step and
# the ordering ledger `logs/checks.py` composes `checks.txt` from.
#
# The ledger records what actually ran: the exact command string handed to the
# shell, its numeric exit, and a timestamp either side. The V7 review found a
# head ledger that recorded start, end and exit without the command itself,
# and the superseding package's whole claim is that nobody types these rows.
#
# Usage:
#   battery.sh REPO LOGS head
#   battery.sh REPO LOGS parent HEAD_TEST_FILE
#
# The parent battery, after its own baselines, copies the HEAD's replay test
# file over the parent's and runs it against the parent's production files —
# same scenarios, same oracles, other code — which is the class decomposition
# the V7 review requires from isolated runs rather than assertion.
set -u

REPO=$1
LOGS=$2
SIDE=$3
HEAD_TEST=${4:-}

mkdir -p "$LOGS"
LEDGER="$LOGS/order-$SIDE.txt"
: > "$LEDGER"

run() {
  local slug=$1
  local cmd=$2
  local log=${3:-$LOGS/$slug-$SIDE.log}
  date -Is >> "$LEDGER"
  echo "START $slug" >> "$LEDGER"
  echo "CMD: $cmd" >> "$LEDGER"
  ( cd "$REPO" && eval "$cmd" ) > "$log" 2>&1
  echo "exit=$?" >> "$LEDGER"
  date -Is >> "$LEDGER"
  echo "END $slug" >> "$LEDGER"
}

HERE=$(cd "$(dirname "$0")" && pwd)

run focused-catena "python3 -m unittest discover -s tools/tests -p 'test_catena*.py' -v"
run catena-check "python3 scripts/_catena.py check"
run promised "tools/tpt check-promised-deliverables"
run full-discovery "python3 -m unittest discover -s tools/tests"
run make-check "make -k check"
run release-bindings "make check-release-bindings"
run public-site "make public-site"
run browser-gate "node tools/tests/corpus_browser_gate.mjs --json-out '$LOGS/browser-gate-$SIDE.json'"
if [ "$SIDE" = head ]; then
  run browser-static "python3 -m unittest discover -s tools/tests -p 'test_browser_static.py'"
fi
run gzip-sizes "python3 '$HERE/gzip-sizes.py' src/web/browser/catena"

if [ "$SIDE" = head ]; then
  run request-journals "python3 '$HERE/journal-dump.py' tools/tests/test_catena_wave_1.py"
fi

if [ "$SIDE" = parent ] && [ -n "$HEAD_TEST" ]; then
  # The head's test file, run against the parent's production files. The copy
  # is part of the recorded command: the ledger says what ran, including the
  # substitution that makes the run mean what it means.
  run v8-tests-against-parent \
    "cp '$HEAD_TEST' tools/tests/test_catena_wave_1.py && python3 -m unittest discover -s tools/tests -p 'test_catena_wave_1.py' -v" \
    "$LOGS/v8-tests-against-parent.log"
  run request-journals "python3 '$HERE/journal-dump.py' tools/tests/test_catena_wave_1.py"
fi

echo "battery $SIDE complete"
