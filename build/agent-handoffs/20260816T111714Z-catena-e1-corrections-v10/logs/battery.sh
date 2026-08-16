#!/usr/bin/env bash
# Run one validation battery — head or parent — writing one log per step and
# the ordering ledger `logs/checks.py` composes `checks.txt` from.
#
# The ledger records what actually ran: the exact command string handed to the
# shell, its numeric exit, a timestamp either side, and THE LOG IT WROTE. The
# V7 review found a head ledger that recorded start, end and exit without the
# command itself; the V9 review found two commands sharing one log path, the
# second overwriting the first's transcript. Every entry therefore writes a
# unique log under a monotonic per-battery index (`NN-slug-side.log`), records
# that path in its own ledger row, and REFUSES — nonzero, nothing written —
# if the target already exists. A discarded run keeps its own log and its own
# rows; nothing is ever overwritten into silence.
#
# PROVENANCE IS EMITTED DURING EXECUTION, never reconstructed. The V9 review
# found the exact SHA, clean state and cwd asserted only in PROVENANCE.md,
# after the fact. The ledger now opens with a preflight — the exact commit,
# the `git status --porcelain` result, and the working directory as the $REPO
# token, NEVER the real path — and closes with a postflight that re-reads the
# commit, so drift during a battery is visible in the record the battery
# itself wrote, and is a failure.
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
# A battery never overwrites a previous run's record. The old truncate-first
# behaviour destroyed the prior ledger before the first step could refuse.
if [ -e "$LEDGER" ]; then
  echo "REFUSING: ledger already exists: $LEDGER" >&2
  echo "A battery never reuses a record; run against a fresh LOGS directory." >&2
  exit 1
fi
: > "$LEDGER"

INDEX=0

run() {
  local slug=$1
  local cmd=$2
  local name=${3:-$slug-$SIDE.log}
  INDEX=$((INDEX + 1))
  local log
  log=$(printf '%s/%02d-%s' "$LOGS" "$INDEX" "$name")
  if [ -e "$log" ]; then
    echo "REFUSING: log target already exists: $log" >&2
    printf 'REFUSED %s: log target exists: logs/%02d-%s\n' \
      "$slug" "$INDEX" "$name" >> "$LEDGER"
    exit 1
  fi
  date -Is >> "$LEDGER"
  echo "START $slug" >> "$LEDGER"
  printf 'LOG: logs/%02d-%s\n' "$INDEX" "$name" >> "$LEDGER"
  echo "CMD: $cmd" >> "$LEDGER"
  ( cd "$REPO" && eval "$cmd" ) > "$log" 2>&1
  echo "exit=$?" >> "$LEDGER"
  date -Is >> "$LEDGER"
  echo "END $slug" >> "$LEDGER"
}

HERE=$(cd "$(dirname "$0")" && pwd)

# THE PREFLIGHT: commit, clean-tree proof and cwd identity, written into the
# ledger AT RUN TIME, before the first step. `cwd=$REPO` is emitted as the
# literal token — the real path is a private value, and the sanitizer is a
# backstop for accidents, not a license to record one on purpose.
START_SHA=$(git -C "$REPO" rev-parse HEAD) || exit 1
PORCELAIN=$(git -C "$REPO" status --porcelain)
{
  echo "PREFLIGHT battery=$SIDE"
  date -Is
  echo "sha=$START_SHA"
  if [ -z "$PORCELAIN" ]; then
    echo "porcelain=clean"
  else
    echo "porcelain=${#PORCELAIN} bytes; NOT CLEAN"
  fi
  echo 'cwd=$REPO'
} >> "$LEDGER"

run focused-catena "python3 -m unittest discover -s tools/tests -p 'test_catena*.py' -v"
run catena-check "python3 scripts/_catena.py check"
run promised "tools/tpt check-promised-deliverables"
run full-discovery "python3 -m unittest discover -s tools/tests"
run make-check "make -k check"
run release-bindings "make check-release-bindings"
run public-site "make public-site"
# The gate's stdout IS its JSON report; capturing both shipped two
# byte-identical ~590KB members in V9. The `--json-out` file is the one
# artifact; stdout is discarded AS THE RECORDED COMMAND SAYS, and the log is
# the short real transcript: the note below plus anything the gate put on
# stderr.
run browser-gate "node tools/tests/corpus_browser_gate.mjs --json-out '$LOGS/browser-gate-$SIDE.json' > /dev/null && echo 'report written: browser-gate-$SIDE.json (the gate prints the same JSON to stdout; discarded so the report ships once)'"
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
  run head-tests-against-parent \
    "cp '$HEAD_TEST' tools/tests/test_catena_wave_1.py && python3 -m unittest discover -s tools/tests -p 'test_catena_wave_1.py' -v" \
    "head-tests-against-parent.log"
  run request-journals "python3 '$HERE/journal-dump.py' tools/tests/test_catena_wave_1.py"
fi

# THE POSTFLIGHT: the commit re-read after the last step. A battery that
# drifted mid-run is a battery whose figures describe two different trees,
# and the record says so before anything downstream can average over it.
END_SHA=$(git -C "$REPO" rev-parse HEAD)
{
  echo "POSTFLIGHT battery=$SIDE"
  date -Is
  echo "sha=$END_SHA"
  if [ "$END_SHA" = "$START_SHA" ]; then
    echo "sha-drift=none"
  else
    echo "sha-drift=DRIFTED from $START_SHA"
  fi
} >> "$LEDGER"
if [ "$END_SHA" != "$START_SHA" ]; then
  echo "BATTERY $SIDE FAILED: HEAD drifted during the battery" >&2
  exit 1
fi

echo "battery $SIDE complete"
