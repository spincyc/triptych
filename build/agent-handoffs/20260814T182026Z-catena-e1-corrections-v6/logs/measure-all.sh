#!/bin/sh
# ONE process. Every step waits for the one before it because they are lines in
# a script, not jobs coordinated by a watcher. `make check`, the full suite, the
# site build and the gate all write under build/, and two of them running at
# once is a measurement of neither.
set -u
cd $REPO
S=$SCRATCH/-home-<user>-git-worktrees-triptych-e1-catena-v3/<uuid>/scratchpad/v6/runs
SHA=$(git rev-parse HEAD)
say() { printf '\n>>> %s\n' "$1"; }

say "0/6 focused Catena suite"
{ echo "COMMAND: python3 -m unittest discover -s tools/tests -p 'test_catena*.py' -v"; echo "SHA: $SHA"
  echo "TREE: clean at this SHA."; } > "$S/focused-catena-head.log"
python3 -m unittest discover -s tools/tests -p 'test_catena*.py' -v >> "$S/focused-catena-head.log" 2>&1
echo "EXIT=$?" >> "$S/focused-catena-head.log"

say "1/6 full discovery"
{ echo "COMMAND: python3 -m unittest discover -s tools/tests"; echo "SHA: $SHA"
  echo "TREE: clean at this SHA; this was the only job running in this checkout."; } > "$S/all-tests-head.log"
python3 -m unittest discover -s tools/tests >> "$S/all-tests-head.log" 2>&1
echo "EXIT=$?" >> "$S/all-tests-head.log"

say "2/6 make -k check"
{ echo "COMMAND: make -k check"; echo "SHA: $SHA"
  echo "TREE: clean at this SHA; run after the full suite finished, not beside it."; } > "$S/make-k-check-head.log"
make -k check >> "$S/make-k-check-head.log" 2>&1
echo "EXIT=$?" >> "$S/make-k-check-head.log"

say "3/6 public-site"
{ echo "COMMAND: make public-site"; echo "SHA: $SHA"; } > "$S/public-site-head.log"
make public-site >> "$S/public-site-head.log" 2>&1
echo "EXIT=$?" >> "$S/public-site-head.log"

say "4/6 browser gate"
{ echo "COMMAND: TRIPTYCH_CHROME=/usr/bin/chromium node tools/tests/corpus_browser_gate.mjs --json-out logs/gate-head.json"
  echo "PREREQUISITE: make public-site (see logs/public-site-head.log)"; echo "SHA: $SHA"; } > "$S/gate-head.log"
TRIPTYCH_CHROME=/usr/bin/chromium node tools/tests/corpus_browser_gate.mjs --json-out "$S/gate-head.json" > /dev/null 2>> "$S/gate-head.log"
echo "EXIT=$?" >> "$S/gate-head.log"
python3 -c "import json;print('counts',json.load(open('$S/gate-head.json'))['counts'])" >> "$S/gate-head.log" 2>&1

say "5/6 gate comparison"
{ echo "COMMAND: python3 logs/compare-gate.py logs/gate-parent.json logs/gate-head.json"
  echo "PARENT SHA: 19982ab433dd25704ed60b1ac6ddb678bc3a98f9"; echo "HEAD SHA: $SHA"; } > "$S/gate-comparison.log"
python3 "$S/compare-gate.py" "$S/gate-parent.json" "$S/gate-head.json" >> "$S/gate-comparison.log" 2>&1
echo "EXIT=$?" >> "$S/gate-comparison.log"

say "6/6 misc checks"
sh "$S/misc.sh" > "$S/misc-checks-head.log" 2>&1

printf '\n===== RESULTS =====\n'
grep -E "^Ran |^OK|^FAILED|^EXIT=" "$S/focused-catena-head.log" | tail -3
grep -E "^Ran |^FAILED|^OK|^EXIT=" "$S/all-tests-head.log"
grep -E "^make.*Error|^EXIT=" "$S/make-k-check-head.log"
grep -E "^EXIT=|counts" "$S/gate-head.log"
grep -E "whole report identical|^EXIT=" "$S/gate-comparison.log"
