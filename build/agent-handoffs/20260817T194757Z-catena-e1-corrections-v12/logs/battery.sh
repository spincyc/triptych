#!/usr/bin/env bash
# Run one validation battery — head or parent — writing one log per step and
# the ordering ledger `logs/checks.py` composes `checks.txt` from.
#
# The ledger records what actually ran: the exact command string handed to the
# shell, its numeric exit, a timestamp either side, THE LOG IT WROTE, and the
# working tree's state read either side of that command. The V7 review found a
# head ledger that recorded start, end and exit without the command itself;
# the V9 review found two commands sharing one log path, the second
# overwriting the first's transcript. Every entry therefore writes a unique
# log, records that path in its own ledger row, and REFUSES — nonzero,
# nothing written — if the target already exists.
#
# THE V11 CORRECTION, ONE: A LOG NAME IDENTIFIES AN ATTEMPT, NOT A POSITION.
# V10 named logs `NN-slug-side.log` where NN was a positional counter reset to
# zero on every run. Two runs produced byte-identical filenames — the ledger
# guard's own advice, "run against a fresh LOGS directory", reproduced them
# exactly — and the same NN meant different commands on the head and the
# parent side. NN is now the ATTEMPT ORDINAL: it is allocated from the attempt
# ledger, which lives OUTSIDE `$LOGS` and is append-only, so a rerun against a
# fresh `$LOGS` still receives a new ordinal and a new identity. Within one
# attempt a log is keyed by its SLUG, so a step means the same thing on both
# sides; between attempts the ordinal differs, so no filename is ever reused.
# The ledger states this in as many words, at run time, in `log-prefix=`.
#
# THE V12 CORRECTION, ONE: THE ORDINAL IS THE DIRECTORY, NOT THE PREFIX. V11
# put the ordinal in the battery FILENAME and left every package-phase
# transcript `assemble.sh` writes — the gate comparison, the sealer tests, the
# seal passes, the derivation, the consistency audit — with no ordinal at all.
# In the reviewed package `logs/gate-comparison.log` was claimed by six
# different attempts and `logs/sealer-tests.log` by five: a failed attempt's
# transcript did not stay with that attempt, the next attempt opened the same
# path and overwrote it. An attempt now owns a log ROOT,
# `logs/attempt-<ordinal>/`, and everything it writes goes inside it —
# battery logs, the gate's JSON report, and every package-phase transcript
# alike — so there is no path two attempts can both name. The filename inside
# the root keeps the slug and side and drops the now-redundant ordinal prefix.
# The ledger states the convention at run time in `log-root=` and
# `log-naming=`, and `logs/checks.py --audit-logs` refuses a package that
# breaks it.
#
# THE V12 CORRECTION, TWO: A BATTERY IS NEVER `authoritative`. A battery's
# terminal row said `status=authoritative`, and so did an assembly's, so the
# ledger of a lane that ran two batteries and one assembly reported THREE
# authoritative attempts and no way to tell which of them was the package to
# review. "This battery ran to completion" and "this is the package attempt to
# review" are different facts and now carry different words: a battery
# terminates `complete` or `failed` and the word `authoritative` is reserved
# for a package attempt. THE STATE MACHINE, both sides of it, is written out
# once in the header of `assemble.sh`; it is not restated here, and
# `logs/checks.py --audit-authority` is what enforces it.
#
# THE V11 CORRECTION, TWO: TREE STATE IS READ PER COMMAND. V10 read
# `git status --porcelain` once, in the preflight, and `checks.py` stamped
# that one answer onto every row. It was provably false: the parent battery's
# last two steps run after `cp` has overwritten a TRACKED test file, and both
# printed `clean`. Each entry now reads the tree immediately before and
# immediately after its own command, and records both — `TREE-BEFORE:` and
# `TREE-AFTER:` — so a row says what was true when that row ran. The
# preflight and postflight readings are kept as well, at battery scope.
#
# PROVENANCE IS EMITTED DURING EXECUTION, never reconstructed. The V9 review
# found the exact SHA, clean state and cwd asserted only in PROVENANCE.md,
# after the fact. The ledger opens with a preflight — the exact commit, the
# attempt identity, the `git status --porcelain` result, and the working
# directory as the $REPO token, NEVER the real path — and closes with a
# postflight that re-reads the commit AND the tree, so drift during a battery
# is visible in the record the battery itself wrote, and is a failure.
#
# THE ATTEMPT LEDGER. Every run appends machine-readable rows to
# `attempt-ledger.jsonl` beside `$LOGS` (or wherever `$ATTEMPTS` points):
# one row per step, and one terminal row per attempt carrying the disposition
# — `complete` or `failed`, with its single reason. A failed battery also
# drops `DISCARDED-<attempt>.txt` into its own `$LOGS`, and `checks.py`
# REFUSES to compose a package from a logs directory that contains one.
#
# Usage:
#   battery.sh REPO LOGS head
#   battery.sh REPO LOGS parent HEAD_TEST_FILE
#
# Environment:
#   ATTEMPTS    the append-only attempt ledger; default `attempt-ledger.jsonl`
#               beside $LOGS. Point the batteries and assemble.sh at ONE path
#               for a single end-to-end ledger.
#   ATTEMPT_NO  force the attempt ordinal (00-99). Default: one past the
#               highest the ledger has ever recorded.
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

# THE ATTEMPT LEDGER, OUTSIDE $LOGS. It has to outlive `$LOGS` or it cannot
# tell one run from the next, which was the whole defect: appending here is
# what makes a rerun a NEW attempt rather than a second run wearing the first
# run's filenames.
ATTEMPTS=${ATTEMPTS:-$(cd "$(dirname "$LOGS")" && pwd)/attempt-ledger.jsonl}

# One row, JSON, from key=value pairs. Written through python3 rather than
# printf because a recorded command carries quotes and newlines and a
# hand-rolled escape is how a machine-readable record stops being one.
attempt_row() {
  python3 - "$@" <<'PY' >> "$ATTEMPTS"
import json, sys
print(json.dumps(dict(one.split("=", 1) for one in sys.argv[1:]),
                 sort_keys=True))
PY
}

# The next ordinal is one past the highest the ledger HAS EVER carried, so a
# fresh $LOGS cannot recycle a number an earlier attempt already used.
next_attempt_no() {
  python3 - "$ATTEMPTS" <<'PY'
import json, pathlib, sys
top = 0
path = pathlib.Path(sys.argv[1])
if path.is_file():
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
            top = max(top, int(row.get("attempt_no", 0)))
        except (ValueError, TypeError):
            continue
print(top + 1)
PY
}

# Six characters from an alphabet with NO hex letter in it. The identity ends
# up in `checks.txt` and in the log index, both of which the consistency audit
# reads for commit SHAs; a random run of [0-9a-f] would be read as an
# abbreviated commit this package may not name.
nonce() {
  local pool='ghjkmnpqrstvwxyz23456789' out='' i pick
  for i in 1 2 3 4 5 6; do
    pick=$((RANDOM % ${#pool}))
    out="$out${pool:pick:1}"
  done
  printf '%s' "$out"
}

# THE TREE, READ NOW. Entries and bytes, never paths: a porcelain line carries
# a real workspace path and this record is shipped.
tree_state() {
  local out entries
  out=$(git -C "$REPO" status --porcelain 2>/dev/null)
  if [ -z "$out" ]; then
    printf 'clean'
  else
    entries=$(printf '%s\n' "$out" | wc -l | tr -d ' ')
    printf 'DIRTY: %s entries, %s bytes; NOT CLEAN' "$entries" "${#out}"
  fi
}

ATTEMPT_NO=${ATTEMPT_NO:-$(next_attempt_no)}
case "$ATTEMPT_NO" in
  ''|*[!0-9]*)
    echo "REFUSING: attempt ordinal is not a number: $ATTEMPT_NO" >&2
    exit 1 ;;
esac
if [ "$ATTEMPT_NO" -gt 99 ]; then
  echo "REFUSING: attempt ordinal $ATTEMPT_NO exceeds the two-digit prefix" >&2
  echo "the log names carry; start a new attempt ledger deliberately." >&2
  exit 1
fi
PREFIX=$(printf '%02d' "$ATTEMPT_NO")
# THE ATTEMPT'S OWN LOG ROOT. `$ROOT_NAME` is the only directory this battery
# writes transcripts into, and the ordinal in it is the attempt's, so the head
# battery and the parent battery -- two attempts, two ordinals -- cannot land
# in one directory even when they run the same slugs.
ROOT_NAME="attempt-$PREFIX"
LOG_ROOT="$LOGS/$ROOT_NAME"
ATTEMPT="$SIDE-$(date -u +%Y%m%dT%H%M%SZ)-$PREFIX$(nonce)"
INDEX=0
DISCARDED=""

# A battery never overwrites a previous run's record. The old truncate-first
# behaviour destroyed the prior ledger before the first step could refuse.
if [ -e "$LEDGER" ]; then
  echo "REFUSING: ledger already exists: $LEDGER" >&2
  echo "A battery never reuses a record. Run against a fresh LOGS directory:" >&2
  echo "the attempt ordinal comes from $ATTEMPTS, which outlives it, so the" >&2
  echo "new run gets new log names rather than the old run's." >&2
  attempt_row attempt="$ATTEMPT" attempt_no="$ATTEMPT_NO" record=attempt \
    side="$SIDE" sha=unknown cwd='$REPO' phase=preflight-ledger order=0 \
    start="$(date -Is)" end="$(date -Is)" exit=1 result=refused \
    status=failed reason="logs/order-$SIDE.txt already exists; nothing was \
run and nothing was overwritten" log="(none: refused before writing)"
  exit 1
fi
# THE LOG ROOT IS ALLOCATED, NEVER ENTERED. An existing `attempt-NN` directory
# means this ordinal has been used before, which is precisely what the ordinal
# exists to make impossible; a battery that wrote into it would put two
# attempts' transcripts in one place and lose the earlier one's.
if [ -e "$LOG_ROOT" ]; then
  echo "REFUSING: log root already exists: $LOG_ROOT" >&2
  echo "The attempt ordinal $PREFIX has been used before. The ordinal comes" >&2
  echo "from $ATTEMPTS, which outlives \$LOGS; allocate a new one." >&2
  attempt_row attempt="$ATTEMPT" attempt_no="$ATTEMPT_NO" record=attempt \
    side="$SIDE" sha=unknown cwd='$REPO' phase=preflight-log-root order=0 \
    start="$(date -Is)" end="$(date -Is)" exit=1 result=refused \
    status=failed reason="logs/$ROOT_NAME already exists; the attempt ordinal \
$PREFIX has been used before, nothing was run and nothing was overwritten" \
    log="(none: refused before writing)"
  exit 1
fi
: > "$LEDGER"
mkdir "$LOG_ROOT"

# ONE ATTEMPT, ONE DISPOSITION, ONE REASON. The first call wins and every
# later one is a no-op, so no attempt can be handed two reasons, and the
# terminal row is written exactly once.
discard() {
  local phase=$1
  local reason=$2
  [ -z "$DISCARDED" ] || return 0
  DISCARDED=$phase
  local marker="$LOGS/DISCARDED-$ATTEMPT.txt"
  {
    # NOT "NON-AUTHORITATIVE": a battery attempt is never authoritative in the
    # first place, and saying so here would imply the word was ever available
    # to it. The marker's filename is unchanged because `checks.py` refuses
    # this directory by that glob.
    echo "FAILED ATTEMPT -- NOT EVIDENCE"
    echo "attempt : $ATTEMPT"
    echo "battery : $SIDE"
    echo "state   : failed"
    echo "phase   : $phase"
    echo "reason  : $reason"
    echo "sha     : ${START_SHA:-(not read)}"
    echo "when    : $(date -Is)"
    echo 'cwd     : $REPO'
    echo ""
    echo "This battery FAILED. Its rows and its logs are a record of an"
    echo "attempt, not evidence of a result. Do not stage this directory"
    echo "into a package: logs/checks.py refuses a package whose logs carry"
    echo "this marker. The attempt ledger beside this directory carries the"
    echo "same disposition in machine-readable form."
  } > "$marker"
  {
    echo "DISCARDED attempt=$ATTEMPT phase=$phase"
    echo "discard-reason=$reason"
    echo "discard-marker=logs/DISCARDED-$ATTEMPT.txt"
  } >> "$LEDGER"
  attempt_row attempt="$ATTEMPT" attempt_no="$ATTEMPT_NO" record=attempt \
    side="$SIDE" sha="${START_SHA:-unknown}" cwd='$REPO' phase="$phase" \
    order="$INDEX" start="${BATTERY_START:-$(date -Is)}" end="$(date -Is)" \
    exit=1 result=failed status=failed reason="$reason" \
    head="${START_SHA:-unknown}" log="logs/DISCARDED-$ATTEMPT.txt"
}

run() {
  local slug=$1
  local cmd=$2
  local base=${3:-$slug-$SIDE.log}
  INDEX=$((INDEX + 1))
  # THE ATTEMPT ORDINAL, NOT THE STEP ORDINAL, AND IT IS THE DIRECTORY.
  # Slug-keyed within the attempt so `focused-catena` is `focused-catena` on
  # both sides; under the attempt's own root between attempts so no two
  # attempts can produce one path, whatever they name the file.
  local name="$ROOT_NAME/$base"
  local log="$LOGS/$name"
  if [ -e "$log" ]; then
    echo "REFUSING: log target already exists: $log" >&2
    printf 'REFUSED %s: log target exists: logs/%s\n' "$slug" "$name" \
      >> "$LEDGER"
    discard "$slug" "log target logs/$name already exists; a step of attempt \
ordinal $PREFIX has claimed that path before and nothing was overwritten"
    exit 1
  fi
  local before after start end status
  before=$(tree_state)
  start=$(date -Is)
  {
    echo "$start"
    echo "START $slug"
    echo "ORDER: $INDEX"
    echo "LOG: logs/$name"
    echo "TREE-BEFORE: $before"
    echo "CMD: $cmd"
  } >> "$LEDGER"
  ( cd "$REPO" && eval "$cmd" ) > "$log" 2>&1
  status=$?
  after=$(tree_state)
  end=$(date -Is)
  {
    echo "exit=$status"
    echo "TREE-AFTER: $after"
    echo "$end"
    echo "END $slug"
  } >> "$LEDGER"
  # `record=step`: a step row states what the step did. WHETHER THE ATTEMPT
  # STANDS is the terminal row's business, so nothing here can be read as
  # authoritative and discarded at once.
  attempt_row attempt="$ATTEMPT" attempt_no="$ATTEMPT_NO" record=step \
    side="$SIDE" sha="$START_SHA" cwd='$REPO' phase="$slug" order="$INDEX" \
    start="$start" end="$end" exit="$status" result="exit $status" \
    tree_before="$before" tree_after="$after" log="logs/$name" command="$cmd"
}

HERE=$(cd "$(dirname "$0")" && pwd)
BATTERY_START=$(date -Is)

# THE PREFLIGHT: commit, clean-tree proof, attempt identity and cwd identity,
# written into the ledger AT RUN TIME, before the first step. `cwd=$REPO` is
# emitted as the literal token — the real path is a private value, and the
# sanitizer is a backstop for accidents, not a license to record one on
# purpose.
START_SHA=$(git -C "$REPO" rev-parse HEAD)
if [ -z "$START_SHA" ]; then
  echo "BATTERY $SIDE FAILED: cannot read HEAD of the clone under test" >&2
  discard preflight "git rev-parse HEAD failed in the clone under test"
  exit 1
fi
# A BATTERY THAT STARTS DIRTY DESCRIBES A TREE NOBODY NAMED. V12: a second
# parent battery began on a checkout still carrying the head's test file,
# left there by the previous parent battery's own substitution step, and
# reported 544 focused and 1,895 discovered as the PARENT's counts. Every
# figure it produced was plausible and every one of them was the head's.
# Recording DIRTY was what caught it; recording is not enough, because a
# reader who trusts the figures never reaches the tree line. The commit a
# battery names is only its subject if the tree is that commit's.
if [ "$(tree_state)" != clean ]; then
  echo "BATTERY $SIDE REFUSING: the clone under test is not clean." >&2
  git -C "$REPO" status --porcelain >&2
  echo "A battery measures a commit. Restore the checkout, or point this at \
a clone that is at the commit it claims to be." >&2
  discard preflight "the clone under test was dirty before the first step; \
its figures would have described a tree no commit names"
  exit 1
fi
{
  echo "PREFLIGHT battery=$SIDE"
  echo "$BATTERY_START"
  echo "attempt=$ATTEMPT"
  echo "attempt-no=$ATTEMPT_NO"
  echo "sha=$START_SHA"
  echo "porcelain=$(tree_state)"
  echo 'cwd=$REPO'
  echo "log-prefix=$PREFIX"
  echo "log-root=logs/$ROOT_NAME"
  echo "log-naming=every transcript this attempt writes lives in its own root, \
logs/attempt-<ordinal>, and is named <slug>-<side>.log inside it; the ordinal \
names THE ATTEMPT and comes from the attempt ledger outside this directory, so \
a rerun never reuses a path, and the ordinal is the DIRECTORY rather than a \
filename prefix so the package-phase transcripts written later by assemble.sh \
are carried by the same rule instead of by none; the slug names the step, so a \
step means the same thing on both sides even though the two sides are two \
attempts with two ordinals"
  echo "tree-state=read before AND after every command, not once at preflight"
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
# the short real transcript: the counts, the note, and anything the gate put
# on stderr.
#
# V12, the V11 review: the two browser `.log` members shipped EMPTY. The note
# was joined with `&&`, so it printed only when the gate exited 0 -- and this
# route's inherited failures make it exit 1, so the transcript was empty
# exactly when there was something to explain. `;` and an explicit exit now,
# so the gate's own status still decides the row, and `gate-summary.py` puts
# the counts in the transcript rather than leaving a reader to open 590KB of
# JSON to learn whether anything ran.
run browser-gate "node tools/tests/corpus_browser_gate.mjs --json-out '$LOG_ROOT/browser-gate-$SIDE.json' > /dev/null; gate=\$?; python3 '$HERE/gate-summary.py' '$LOG_ROOT/browser-gate-$SIDE.json'; echo 'report written: browser-gate-$SIDE.json beside this log, under this attempt root (the gate prints the same JSON to stdout; discarded so the report ships once)'; exit \$gate"
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
  # substitution that makes the run mean what it means. IT ALSO DIRTIES A
  # TRACKED FILE, which is why the tree is read per command: this row and
  # every row after it record the tree they actually ran against.
  run head-tests-against-parent \
    "cp '$HEAD_TEST' tools/tests/test_catena_wave_1.py && python3 -m unittest discover -s tools/tests -p 'test_catena_wave_1.py' -v" \
    "head-tests-against-parent.log"
  run request-journals "python3 '$HERE/journal-dump.py' tools/tests/test_catena_wave_1.py"
  # AND PUT IT BACK, because a battery that leaves a tracked file substituted
  # poisons the NEXT battery silently. V12: it did. A second parent battery
  # ran against a checkout still carrying the head's test file and reported
  # the head's counts — 544 focused and 1,895 discovered — as the parent's.
  # The per-command tree reading caught it, recording DIRTY from the
  # preflight onward, which is the only reason it was caught at all; the
  # figures themselves looked entirely plausible. Restoring is its own
  # recorded step, so the ledger states that the substitution was undone
  # rather than leaving a reader to infer it from a clean postflight.
  # AND IT SAYS SO. `git status --porcelain` prints NOTHING when the tree is
  # clean, so the transcript of a successful restore is an empty file — and a
  # reader would have to know that emptiness means success. This lane exists
  # to refuse exactly that kind of implicit claim, and the attempt-log audit
  # refuses an unexplained empty log for the same reason. The step states its
  # outcome in words and counts what it found.
  run restore-parent-tree \
    "git checkout -- tools/tests/test_catena_wave_1.py; \
echo \"restored: tools/tests/test_catena_wave_1.py\"; \
git status --porcelain; \
echo \"porcelain entries after restore: \$(git status --porcelain | wc -l)\"" \
    "restore-parent-tree.log"
fi

# THE POSTFLIGHT: the commit and the tree re-read after the last step. A
# battery that drifted mid-run is a battery whose figures describe two
# different trees, and the record says so before anything downstream can
# average over it. The tree reading here is the battery's closing state, NOT
# the state any earlier row ran against; those are on the rows.
END_SHA=$(git -C "$REPO" rev-parse HEAD)
BATTERY_END=$(date -Is)
{
  echo "POSTFLIGHT battery=$SIDE"
  echo "$BATTERY_END"
  echo "sha=$END_SHA"
  echo "porcelain=$(tree_state)"
  if [ "$END_SHA" = "$START_SHA" ]; then
    echo "sha-drift=none"
  else
    echo "sha-drift=DRIFTED from $START_SHA"
  fi
} >> "$LEDGER"
if [ "$END_SHA" != "$START_SHA" ]; then
  echo "BATTERY $SIDE FAILED: HEAD drifted during the battery" >&2
  discard postflight "HEAD drifted during the battery; every figure it \
recorded describes two different trees"
  exit 1
fi

# THE TERMINAL ROW: this attempt, and its disposition, once. `complete`, NOT
# `authoritative` -- see the state machine in assemble.sh's header. A battery
# that ran to completion has said everything it is entitled to say; which
# package a reviewer should read is a fact about a package attempt, and a lane
# whose ledger called three attempts authoritative could not state it.
attempt_row attempt="$ATTEMPT" attempt_no="$ATTEMPT_NO" record=attempt \
  side="$SIDE" sha="$END_SHA" cwd='$REPO' phase=battery order="$INDEX" \
  start="$BATTERY_START" end="$BATTERY_END" exit=0 result="complete" \
  status=complete reason="" head="$END_SHA" log="logs/order-$SIDE.txt"
echo "battery $SIDE complete: attempt $ATTEMPT, logs under logs/$ROOT_NAME/"
