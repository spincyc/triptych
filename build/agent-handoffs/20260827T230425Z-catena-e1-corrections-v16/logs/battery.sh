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
# THE V13 CORRECTION, ONE: THE COMMIT IS COMPARED, NOT MERELY READ. V12 took
# `START_SHA=$(git rev-parse HEAD)` and never compared it to anything. The only
# preflight assertion was cleanliness, which proves the tree matches SOME
# commit and never THE commit — so a clean checkout sitting at the wrong commit
# passed preflight, passed postflight, and was labelled `side=parent` purely
# because `$3` said so. `EXPECT_SHA` is now required and is compared: a
# mismatch is terminal, through `discard()`, with its own reason.
#
# THE V13 CORRECTION, TWO: A DIRTY POSTFLIGHT FAILS THE BATTERY. V12 recorded
# `porcelain=DIRTY: ...` in the postflight and then keyed the failure branch
# only on SHA drift, so a battery that ended dirty still wrote
# `status=complete`. That is exactly what a failing `restore-parent-tree` step
# produces — `set -u` is on, `-e` is not, so a failed restore does not abort —
# and it leaves the next battery to start on a poisoned checkout. Only the
# POSTFLIGHT reading is required clean: the parent side deliberately dirties
# the tree mid-battery and puts it back, and every row records the tree it
# actually ran against.
#
# THE V13 CORRECTION, THREE: THE ORDINAL IS ALLOCATED BY ONE ALLOCATOR, FOR A
# NAMED LANE. V12 recomputed `max(attempt_no) + 1` over the CURRENT ledger
# file; the operator started a fresh file partway through the lane, so ordinals
# 03/04/05/06 were reissued as 03/04/05 while the package claimed "an ordinal
# is allocated once for the whole lane". This script no longer computes an
# ordinal at all. `checks.py --allocate-ordinal --lane $LANE` does, and it
# refuses an ordinal any row has ever carried, refuses a ledger belonging to
# another lane, and refuses to open a fresh ledger over an existing one. The
# lane rides on every row this script appends.
#
# THE ATTEMPT LEDGER. Every run appends machine-readable rows to
# `attempt-ledger.jsonl` beside `$LOGS` (or wherever `$ATTEMPTS` points):
# a `record=lane` row opening the lane's ledger, a `record=state
# status=started` row appended the moment an ordinal is allocated so the
# ordinal is spent before anything can allocate it twice, one row per step, and
# one terminal row per attempt carrying the disposition — `complete` or
# `failed`, with its single reason. A failed battery also drops
# `DISCARDED-<attempt>.txt` into its own `$LOGS`, and `checks.py` REFUSES to
# compose a package from a logs directory that contains one.
#
# NO EVIDENCE DISPOSITION IS WRITTEN HERE, and that is deliberate. What this
# script records is the EXECUTION disposition — how the run itself ended.
# Whether a completed cohort's measurements are the ones a package reports is
# a SEPARATE AXIS, it is not known while the battery runs, and it is therefore
# never this script's terminal disposition. The battery terminates `complete`;
# the operator later appends ONE `record=state` row, with its one non-empty
# reason, saying what became of the figures —
#
#   record=state side=<head|parent> status=set-aside      reason="<why>"
#   record=state side=<head|parent> status=authoritative  reason="<why>"
#
# — written by `checks.py --set-aside-attempt` and `--authoritative-evidence`
# respectively. Neither touches the `complete` terminal row: `checks.py`
# reports the two axes side by side and never collapses one into the other.
# A cohort with no such row is `unevidenced` until one is recorded.
#
# V12 had no word for a completed-but-unused cohort at all, so four of them
# were deleted from the record instead of being recorded in it; V16 found the
# opposite hole beside it, that "these are the figures this package reports"
# had no word either and lived only in prose.
#
# Usage:
#   EXPECT_SHA=<sha> LANE=<lane> battery.sh REPO LOGS head
#   EXPECT_SHA=<sha> LANE=<lane> battery.sh REPO LOGS parent HEAD_TEST_FILE
#
# Environment:
#   EXPECT_SHA  REQUIRED. The commit this battery claims to measure. The
#               checkout's HEAD is compared against it and a mismatch is
#               terminal. At least 7 hex characters; a prefix is accepted, so
#               the abbreviated SHA an operator has to hand works, and the full
#               one it stands for is what lands in the record.
#   LANE        REQUIRED. The lane whose attempt ledger this appends to. A
#               ledger declares its lane on its first row and every row repeats
#               it; appending on another lane's behalf is refused.
#   ATTEMPTS    the append-only attempt ledger; default `attempt-ledger.jsonl`
#               beside $LOGS. Point the batteries and assemble.sh at ONE path
#               for a single end-to-end ledger.
#   ATTEMPT_NO  propose the attempt ordinal (1-99). Refused if any row in the
#               lane's ledger has ever carried it. Default: one past the
#               highest the lane has ever allocated.
#
# The parent battery, after its own baselines, copies the HEAD's replay test
# file over the parent's and runs it against the parent's production files —
# same scenarios, same oracles, other code — which is the class decomposition
# the V7 review requires from isolated runs rather than assertion.
set -u

if [ $# -lt 3 ]; then
  echo "usage: EXPECT_SHA=<sha> LANE=<lane> battery.sh REPO LOGS head" >&2
  echo "       EXPECT_SHA=<sha> LANE=<lane> battery.sh REPO LOGS parent \
HEAD_TEST_FILE" >&2
  exit 1
fi

REPO=$1
LOGS=$2
SIDE=$3
HEAD_TEST=${4:-}

# THE TOOLS BESIDE THIS SCRIPT, resolved before anything else needs them: the
# ordinal allocator is `checks.py`, and it is one of them.
HERE=$(cd "$(dirname "$0")" && pwd)

# ---- THE ROOT VARIABLES, DISTINCT AND DEFINED ONCE EACH --------------------
#
# THE V15 DEFECT, NAMED. V15 composed its command strings by interpolating
# REAL ABSOLUTE PATHS inside SINGLE QUOTES -- correct at the instant of
# execution -- and the sanitizer then rewrote those paths into `$WORKSPACE/`
# and `$REPO/` tokens IN PLACE, inside quotes whose entire purpose is to stop
# expansion. Seven rows shipped labelled "the exact string handed to the
# shell; re-runnable" naming paths that no shell can produce. Worse, `$REPO`
# came to mean TWO THINGS in one row: `cwd : $REPO` was the parent checkout
# and `cp '$REPO/tools/tests/...'` was the candidate checkout, because the
# sanitizer's `--repo` root was the candidate. Unquoting alone could not have
# recovered that execution.
#
# THE FIX IS HERE, NOT IN THE SANITIZER. The recorded string never contains a
# real path at all. It contains a root variable, DOUBLE QUOTED so it expands,
# and `run()` exports the real value into the subshell that evaluates it -- so
# the string the ledger records is BYTE-IDENTICAL to the string the shell was
# handed, and running it elsewhere needs only the same five bindings. The
# sanitizer becomes what it was always supposed to be: a backstop for
# accidents, with nothing left for it to rewrite here.
#
# EACH NAME MEANS ONE DIRECTORY, ON BOTH SIDES.
#
#   $CANDIDATE_REPO  the implementation checkout under review -- the head side
#   $PARENT_REPO     the comparison checkout -- the parent side
#   $TOOLS_ANCHOR    this script's own directory, the handoff-tools checkout
#   $EVIDENCE_ROOT   the staged package source directory transcripts land in
#
# `$REPO`, `$WORKSPACE`, `$EVIDENCE` and `$SCRATCH` are RESERVED and never
# defined: `catena_command.py` refuses a record that binds any of them,
# precisely so a V16 record cannot repeat V15's overloading under V15's
# spelling.
#
# DERIVED, NOT DECLARED. The candidate root on the PARENT side is read out of
# the head test file's own checkout, so an operator cannot point the two at
# each other by mistyping one of them.
TOOLS_ANCHOR=$HERE
EVIDENCE_ROOT=$(cd "$LOGS/.." 2>/dev/null && pwd || echo "$LOGS")
# The logs directory's name RELATIVE TO `$EVIDENCE_ROOT`, read rather than
# assumed: a row that hardcoded `logs` would name the wrong path the first
# time an operator staged into a directory called anything else.
LOGS_REL=$(basename "$LOGS")
if [ "$SIDE" = head ]; then
  CANDIDATE_REPO=$(cd "$REPO" && pwd)
  PARENT_REPO=""
  SIDE_CWD='$CANDIDATE_REPO'
else
  PARENT_REPO=$(cd "$REPO" && pwd)
  CANDIDATE_REPO=""
  if [ -n "$HEAD_TEST" ]; then
    CANDIDATE_REPO=$(git -C "$(dirname "$HEAD_TEST")" rev-parse --show-toplevel \
                     2>/dev/null || echo "")
  fi
  SIDE_CWD='$PARENT_REPO'
fi
export TOOLS_ANCHOR EVIDENCE_ROOT CANDIDATE_REPO PARENT_REPO

# THE COMMIT THIS BATTERY CLAIMS TO MEASURE, STATED BY THE CALLER. V12 read
# HEAD and compared it to nothing, so `side=parent` was true because the third
# argument said so and for no other reason. Required, and it is not a
# formality: the whole package is a comparison of two commits.
EXPECT_SHA=${EXPECT_SHA:-}
if [ -z "$EXPECT_SHA" ]; then
  echo "REFUSING: EXPECT_SHA is required." >&2
  echo "A battery measures a NAMED commit. Reading HEAD and believing it is" >&2
  echo "how a clean checkout at the wrong commit gets labelled side=$SIDE." >&2
  echo "usage: EXPECT_SHA=<sha> LANE=<lane> battery.sh REPO LOGS \
$SIDE${HEAD_TEST:+ HEAD_TEST_FILE}" >&2
  exit 1
fi
case "$EXPECT_SHA" in
  *[!0-9a-fA-F]*|"")
    echo "REFUSING: EXPECT_SHA is not hexadecimal: $EXPECT_SHA" >&2
    exit 1 ;;
esac
if [ ${#EXPECT_SHA} -lt 7 ]; then
  echo "REFUSING: EXPECT_SHA needs at least 7 hex characters; \
$EXPECT_SHA is ${#EXPECT_SHA}" >&2
  exit 1
fi
# `git rev-parse` prints lowercase. A pasted uppercase SHA is the same commit
# and refusing it would be a refusal about typography, not about the checkout.
EXPECT_SHA=$(printf '%s' "$EXPECT_SHA" | tr 'A-F' 'a-f')

# THE LANE THIS LEDGER BELONGS TO. Not decoration: it is what lets the
# allocator refuse to append to another lane's record, and what makes an
# operator who starts the lane's ledger over do it out loud.
LANE=${LANE:-}
if [ -z "$LANE" ]; then
  echo "REFUSING: LANE is required." >&2
  echo "An attempt ordinal is allocated once for a LANE. A ledger that does" >&2
  echo "not name its lane cannot say whose allocation it carries, which is" >&2
  echo "how V12 reissued ordinals 03/04/05 over a fresh file." >&2
  exit 1
fi

mkdir -p "$LOGS"
LEDGER="$LOGS/order-$SIDE.txt"

# THE ATTEMPT LEDGER, OUTSIDE $LOGS. It has to outlive `$LOGS` or it cannot
# tell one run from the next, which was the whole defect: appending here is
# what makes a rerun a NEW attempt rather than a second run wearing the first
# run's filenames.
ATTEMPTS=${ATTEMPTS:-$(cd "$(dirname "$LOGS")" && pwd)/attempt-ledger.jsonl}

# THE BATTERY'S CONTEMPORANEOUS TOOL DIGESTS, beside the attempt ledger and on
# the same terms: outside `$LOGS`, append-only, spanning attempts.
#
# V15, THE V14 REVIEW. `gate-summary.py`, `gzip-sizes.py` and `journal-dump.py`
# shipped classed `shipped-not-executed` in a package that also ships their
# transcripts. That was not an `assemble.sh` bug -- `assemble.sh` never
# invokes them; THIS script does, in a different attempt, and it recorded the
# command in the ledger while recording nothing about the BYTES it handed the
# interpreter. So the assembler had nothing to classify them from and fell
# back, correctly given what it knew, to "this attempt did not run it".
#
# The fix is the same rule `assemble.sh`'s `run_tool` follows: hash the exact
# file on the line before it runs. Which files those are is DERIVED from the
# command string about to be evaluated, not from a list maintained by hand --
# a list is a thing that goes stale the first time a step is added.
TOOLRUNS=${TOOLRUNS:-$(cd "$(dirname "$ATTEMPTS")" && pwd)/executed-tools.jsonl}

# One row, JSON, from key=value pairs. Written through python3 rather than
# printf because a recorded command carries quotes and newlines and a
# hand-rolled escape is how a machine-readable record stops being one.
#
# EVERY ROW CARRIES THE LANE. Prepended here rather than at each call site, so
# there is no row this script can write without one, and two lanes' ledgers
# cannot be concatenated in silence.
attempt_row() {
  python3 - "lane=$LANE" "$@" <<'PY' >> "$ATTEMPTS"
import json, sys
print(json.dumps(dict(one.split("=", 1) for one in sys.argv[1:]),
                 sort_keys=True))
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

# THE ORDINAL COMES FROM THE ONE ALLOCATOR, NOT FROM A MAXIMUM COMPUTED HERE.
# `checks.py --allocate-ordinal` opens the lane's ledger if it does not exist,
# refuses one belonging to another lane, and refuses any ordinal a row of this
# lane has EVER carried — including a discarded attempt's, which is precisely
# the case V12's `max(attempt_no) + 1` could not see once the ledger file had
# been started again. A refusal here is nonzero and this script stops: there is
# no ordinal, so there is no attempt to record a disposition for.
ATTEMPT_NO=$(python3 "$HERE/checks.py" --allocate-ordinal \
  --attempts "$ATTEMPTS" --lane "$LANE" \
  ${ATTEMPT_NO:+--propose "$ATTEMPT_NO"}) || {
  echo "BATTERY $SIDE REFUSING: no attempt ordinal was allocated." >&2
  exit 1
}
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
# THE INSTANT THE ID CLAIMS, AND THE INSTANT THE FIRST ROW CLAIMS, TAKEN
# TOGETHER. `checks.py --verify-ledger` compares the timestamp embedded in the
# id above against the attempt's first row, because V12's final attempt carried
# an id stamped 2m25s LATER than its own last row. Reading the clock here, one
# line apart, is what makes that comparison mean something.
BATTERY_START=$(date -Is)
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
    side="$SIDE" sha=unknown cwd="$SIDE_CWD" phase=preflight-ledger order=0 \
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
    side="$SIDE" sha=unknown cwd="$SIDE_CWD" phase=preflight-log-root order=0 \
    start="$(date -Is)" end="$(date -Is)" exit=1 result=refused \
    status=failed reason="logs/$ROOT_NAME already exists; the attempt ordinal \
$PREFIX has been used before, nothing was run and nothing was overwritten" \
    log="(none: refused before writing)"
  exit 1
fi
: > "$LEDGER"
mkdir "$LOG_ROOT"

# THE ORDINAL IS SPENT THE MOMENT IT IS ALLOCATED. Without this row the ledger
# carries no trace of the ordinal until the first step finishes, and two
# batteries starting together would both be handed the same number by an
# allocator reading a file neither had written to yet. `started` is a legal
# opening state on the battery side and needs no reason; the disposition, and
# the one reason it may carry, arrive on the terminal row.
attempt_row attempt="$ATTEMPT" attempt_no="$ATTEMPT_NO" record=state \
  side="$SIDE" status=started reason="" phase=preflight order=0 \
  start="$BATTERY_START" end="$BATTERY_START" cwd="$SIDE_CWD" \
  expect="$EXPECT_SHA" log="(none: the ordinal is allocated and the log root \
logs/$ROOT_NAME opened; no transcript is written yet)"

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
    echo "lane    : $LANE"
    echo "battery : $SIDE"
    echo "state   : failed"
    echo "phase   : $phase"
    echo "reason  : $reason"
    echo "expected: $EXPECT_SHA"
    echo "sha     : ${START_SHA:-(not read)}"
    echo "when    : $(date -Is)"
    echo "cwd     : $SIDE_CWD"
    echo ""
    echo "This battery FAILED. Its rows and its logs are a record of an"
    echo "attempt, not evidence of a result. Do not stage this directory"
    echo "into a package: logs/checks.py refuses a package whose logs carry"
    echo "this marker. The attempt ledger beside this directory carries the"
    echo "same disposition in machine-readable form."
  } > "$marker"
  # THROUGH THE SANITIZER, BEST-EFFORT. V16, the V15 review: retained
  # discard markers "preserve builder-local offsets or absolute paths" and
  # nothing ever pointed the sanitizer at one. The marker carries a
  # `date -Is` with a LOCAL OFFSET and a free-text reason composed at the
  # failure site; the sanitizer has a rule for both. The exit is ignored on
  # purpose: a discard path must not fail harder than the failure that
  # reached it, and a marker that exists and says what happened is worth
  # more than a marker that was refused for being unsanitized.
  python3 "$HERE/sanitize-and-seal.py" --repo "$REPO" \
    --sanitize-files "$marker" > /dev/null 2>&1 || true
  {
    echo "DISCARDED attempt=$ATTEMPT phase=$phase"
    echo "discard-reason=$reason"
    echo "discard-marker=logs/DISCARDED-$ATTEMPT.txt"
  } >> "$LEDGER"
  attempt_row attempt="$ATTEMPT" attempt_no="$ATTEMPT_NO" record=attempt \
    side="$SIDE" sha="${START_SHA:-unknown}" cwd="$SIDE_CWD" phase="$phase" \
    order="$INDEX" start="${BATTERY_START:-$(date -Is)}" end="$(date -Is)" \
    exit=1 result=failed status=failed reason="$reason" \
    expect="$EXPECT_SHA" head="${START_SHA:-unknown}" \
    log="logs/DISCARDED-$ATTEMPT.txt"
}

# EVERY TOOL OF OURS THIS COMMAND NAMES, HASHED BEFORE IT RUNS.
#
# WHICH tools is derived, not declared: the command strings this script
# composes reach our own helpers exactly one way, as `$HERE/<name>`, so the
# set is "the files in `$HERE` whose absolute path appears in the string".
# Add a step tomorrow that runs a fourth helper and it is recorded with no
# edit here; that is the point. A step that runs none of ours -- `make check`,
# `node tools/tests/...` -- writes no row, which is correct: those are the
# repository's own tools and this record is about the ones the package ships.
#
# The row names the transcript the invocation is about to write, PACKAGE-
# RELATIVE, because that is what lets `assemble.sh` merge it without knowing
# anything about this attempt: it ships the transcript or it does not.
#
# Best-effort by design. A failure to write this record must never take down a
# battery step -- the step's own ledger row and transcript are the primary
# evidence and they are written either way -- so the write is guarded and the
# function always succeeds.
record_tool_digests() {  # command package-relative-log slug
  local cmd=$1 log=$2 slug=$3 one base sha
  [ -n "${TOOLRUNS:-}" ] || return 0
  mkdir -p "$(dirname "$TOOLRUNS")" 2>/dev/null || return 0
  for one in "$HERE"/*.py "$HERE"/*.sh; do
    [ -f "$one" ] || continue
    base=$(basename "$one")
    # MATCHED ON THE RECORDED TOKEN, NOT THE REAL PATH. The command strings
    # this script composes now name our helpers as `$TOOLS_ANCHOR/<name>` --
    # that is the whole V16 correction -- so the real absolute path no longer
    # appears in them and the old `*"$HERE/$base"*` test matched nothing. The
    # set is still DERIVED from the command rather than declared: add a step
    # tomorrow that runs a fourth helper and it is recorded with no edit here.
    case $cmd in
      *"\$TOOLS_ANCHOR/$base"*|*"$HERE/$base"*) ;;
      *) continue ;;
    esac
    sha=$(sha256sum "$one" | cut -d' ' -f1) || continue
    python3 - "$base" "$sha" "$(date -Is)" "$slug" "$log" "$ATTEMPT" \
        battery <<'PY' >> "$TOOLRUNS" || true
import json, sys
keys = ("tool", "sha256", "at", "phase", "log", "attempt", "kind")
print(json.dumps(dict(zip(keys, sys.argv[1:])), sort_keys=True))
PY
  done
  return 0
}

# THE EXEC RECORD, BUILT FROM WHAT IS ABOUT TO RUN.
#
# `catena_command.py` owns the schema and the validation; this composes the
# fields the shell already holds at the instant of execution and hands them
# over. Nothing here writes JSON by hand and nothing invents a string: the
# `shell` field is the EXACT text `eval` receives, and an `argv` row's
# elements are the exact words the interpreter receives.
#
# IT VALIDATES BEFORE IT RUNS. A step whose record cannot be replayed is a
# step whose evidence would ship mislabelled, and V15 shipped seven of them.
# Refusing here costs one battery step; refusing at review costs a package.
# Prints TWO lines: the record as one line of JSON, then the shell rendering
# derived from it. The rendering is what a reader sees on the `command :` row
# and what `eval` is handed, so the two can never describe different things.
exec_record() {  # cwd-token form(shell|argv) env-json -- command-or-argv...
  local cwd=$1 form=$2 envjson=$3
  shift 3
  [ "${1:-}" = "--" ] && shift
  python3 - "$HERE" "$cwd" "$form" "$envjson" "$@" <<'PY'
import json, sys
sys.path.insert(0, sys.argv[1])
import catena_command as CC
cwd, form, envjson = sys.argv[2:5]
rest = sys.argv[5:]
env = json.loads(envjson or "{}")
if form == "argv":
    record = CC.make_record(cwd, argv=rest, env=env)
else:
    record = CC.make_record(cwd, shell=rest[0], env=env)
print(json.dumps(record, sort_keys=True))
print(CC.render_shell(record))
PY
}

# THE ARGV FORM. A step that is one command with its arguments is recorded as
# a LIST, which has no quoting at all and therefore cannot carry V15's defect
# in any form: there is no quote for a `$` to hide inside. The shell form
# below stays for the steps that really are shell composites -- a saved exit
# status, a command substitution -- and those are validated for expandability
# instead.
RUN_RECORD=""
run_argv() {  # slug -- command args...
  local slug=$1
  shift
  [ "${1:-}" = "--" ] && shift
  local both
  both=$(exec_record "$SIDE_CWD" argv '{}' -- "$@") || {
    echo "REFUSING: $slug does not produce a replayable exec record" >&2
    discard "$slug" "the step's exec record failed validation before the step \
ran; a step whose recorded command cannot be replayed would ship mislabelled"
    exit 1
  }
  RUN_RECORD=${both%%$'\n'*}
  run "$slug" "${both#*$'\n'}"
}

run() {
  local slug=$1
  local cmd=$2
  local base=${3:-$slug-$SIDE.log}
  # THE RECORD FOR A SHELL-FORM STEP, composed here so a caller that already
  # built one (`run_argv`) is not made to build it twice.
  local record=$RUN_RECORD both
  if [ -z "$record" ]; then
    # `{}` PLAINLY, not `\{\}`: the escaped form is what the shell hands on,
    # and it is not JSON. The first shell-form step of the first battery
    # refused on it, which is the guard working and the default being wrong.
    local envj=${RUN_ENV_JSON:-}
    [ -n "$envj" ] || envj='{}'
    both=$(exec_record "$SIDE_CWD" shell "$envj" -- "$cmd") || {
      echo "REFUSING: $slug does not produce a replayable exec record" >&2
      echo "  command: $cmd" >&2
      discard "$slug" "the step's exec record failed validation before the \
step ran; V15 shipped seven rows whose recorded command could not expand, and \
this is the check that refuses one rather than shipping it"
      exit 1
    }
    record=${both%%$'\n'*}
  fi
  RUN_RECORD=""
  RUN_ENV_JSON=""
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
    # THE MACHINE-READABLE FORM, BESIDE THE HUMAN ONE, ON THE SAME LINE PAIR.
    # `CMD:` is a rendering for a reader; `CMDJSON:` is the record a replay
    # executes. V15 had only the first and called it the second.
    echo "CMDJSON: $record"
  } >> "$LEDGER"
  # IMMEDIATELY BEFORE. Every tool of ours this command names is hashed on the
  # line before the command is evaluated, and the row says which transcript
  # the invocation wrote, so the assembler can merge it against the package it
  # is about to seal. Derived from the command string; nothing is listed here.
  record_tool_digests "$cmd" "logs/$name" "$slug"
  # THE ROOTS ARE IN THE SUBSHELL'S ENVIRONMENT, so the recorded string and
  # the executed string are ONE string. V15 interpolated real paths into the
  # string and let the sanitizer rewrite them afterwards, which is how a
  # single-quoted `'$WORKSPACE/...'` came to be shipped as "re-runnable".
  # Nothing is interpolated now; the shell expands the same tokens a replay
  # expands, from the same bindings.
  ( cd "$REPO" \
    && export CANDIDATE_REPO PARENT_REPO TOOLS_ANCHOR EVIDENCE_ROOT \
    && eval "$cmd" ) > "$log" 2>&1
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
    side="$SIDE" sha="$START_SHA" cwd="$SIDE_CWD" phase="$slug" \
    order="$INDEX" \
    start="$start" end="$end" exit="$status" result="exit $status" \
    tree_before="$before" tree_after="$after" log="logs/$name" command="$cmd" \
    exec_record="$record"
}

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
# THE COMMIT, COMPARED. A clean tree proves the checkout matches SOME commit;
# it has never proved it matches THE commit, and V12 asserted nothing else. A
# clean checkout parked at the head therefore passed every preflight this
# script had and was written into the record as `side=parent` because the third
# argument said so. `EXPECT_SHA` is the caller's claim about which commit this
# battery is measuring, and this is where the claim meets the checkout.
case "$START_SHA" in
  "$EXPECT_SHA"*) ;;
  *)
    echo "BATTERY $SIDE REFUSING: the clone under test is not at the commit \
this battery claims to measure." >&2
    echo "expected : $EXPECT_SHA" >&2
    echo "found    : $START_SHA" >&2
    echo "A clean tree proves the checkout matches SOME commit. It has never \
proved it matches THIS one." >&2
    discard preflight "the clone under test is at $START_SHA, not at the \
commit this battery was told it measures ($EXPECT_SHA); every figure it would \
have produced would have been labelled side=$SIDE on the strength of an \
argument rather than of the checkout"
    exit 1 ;;
esac
{
  echo "PREFLIGHT battery=$SIDE"
  echo "$BATTERY_START"
  echo "attempt=$ATTEMPT"
  echo "attempt-no=$ATTEMPT_NO"
  echo "lane=$LANE"
  echo "expect-sha=$EXPECT_SHA"
  echo "sha=$START_SHA"
  echo "sha-matches-expected=yes"
  echo "porcelain=$(tree_state)"
  echo "cwd=$SIDE_CWD"
  # THE ROOT VARIABLES THIS ATTEMPT'S ROWS REFERENCE, DEFINED HERE, ONCE EACH.
  # `checks.py` reads these lines to build `commands.json`'s `variables`
  # block, so the definitions a reviewer replays against are the ones the
  # battery actually exported into the subshell that ran each step. V15 had no
  # such block at all: seven rows named `$WORKSPACE` and `$REPO` and nothing
  # anywhere in the package said what either was.
  echo "root=CANDIDATE_REPO the implementation checkout under review -- the head side"
  echo "root=PARENT_REPO the comparison checkout -- the parent side"
  echo "root=TOOLS_ANCHOR the out-of-package handoff-tools checkout this lane ran from"
  echo "root=EVIDENCE_ROOT the staged package source directory the batteries wrote into"
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

# ---- THE DRIVER RECORDS ITSELF ---------------------------------------------
#
# V16, THE V15 REVIEW: "both `assemble.sh` and `battery.sh` are marked not
# executed although they drove the build". They were, and the reason is that
# the executed-tool record only ever carried rows written BY a driver ABOUT
# something else. A driver that hashes every tool it invokes and never itself
# is a record with a hole exactly the shape of the thing that produced it.
#
# This row is contemporaneous on the same terms as every other: the sha256 of
# the exact file bash is executing, taken here, before the first step. Its
# `kind` is `driver`, which is the class `emit_executed_tools` uses to say
# "this ran, and these transcripts are the steps it drove".
if [ -n "${TOOLRUNS:-}" ]; then
  mkdir -p "$(dirname "$TOOLRUNS")" 2>/dev/null || true
  BATTERY_SHA=$(sha256sum "$0" | cut -d' ' -f1) || BATTERY_SHA=""
  if [ -n "$BATTERY_SHA" ]; then
    python3 - battery.sh "$BATTERY_SHA" "$(date -Is)" "battery-$SIDE" \
        "logs/order-$SIDE.txt" "$ATTEMPT" driver <<'PY' >> "$TOOLRUNS" || true
import json, sys
keys = ("tool", "sha256", "at", "phase", "log", "attempt", "kind")
print(json.dumps(dict(zip(keys, sys.argv[1:])), sort_keys=True))
PY
  fi
fi

run_argv focused-catena -- python3 -m unittest discover -s tools/tests -p 'test_catena*.py' -v
run_argv catena-check -- python3 scripts/_catena.py check
run_argv promised -- tools/tpt check-promised-deliverables
run_argv full-discovery -- python3 -m unittest discover -s tools/tests
# ---- THE COLD-BUILD PRECONDITION, CHECKED RATHER THAN WRITTEN DOWN --------
#
# V16, MEASURED. `make -k check` runs `check-examples`, and that target's
# divergence count is BUILD-STATE SENSITIVE: 30 divergent rows on a cold
# `build/`, 28 on a warm one. The whole delta is two captures of
# `tools/mass-ordinary check --out build/example-ordinary`, which diverges
# against a directory a LATER capture in the same target writes -- so the
# second run of the target in one tree reports fewer divergences than the
# first, and both are honest reports of the run that produced them.
#
# A battery that runs the target twice therefore produces two different true
# figures for one head, and a durable record quoting either has no way to say
# which. V15's package shipped a WARM transcript (28) beside a durable claim
# of 30 taken from a cold run, and the mismatch was read as an arithmetic
# error when it was a state error.
#
# So the state is READ, here, before the step, and recorded. A warning rather
# than a refusal: the figures are still true of the run that produced them,
# and a battery that stopped here would lose a whole cohort over a
# reproducibility caveat. What must not happen is that nobody says so.
if [ -d "$REPO/build/example-ordinary" ]; then
  echo "WARNING: $LOGS_REL build/example-ordinary already exists in the" >&2
  echo "clone under test. check-examples is build-state sensitive: a warm" >&2
  echo "build/ reports FEWER divergent rows than a cold one, because a" >&2
  echo "capture that writes that directory makes an earlier capture in the" >&2
  echo "same target match. Run the battery exactly once per fresh clone, or" >&2
  echo "the figure this attempt records will not reproduce from the head." >&2
  {
    echo "build-state=WARM: build/example-ordinary existed before make-check;"
    echo "build-state-note=check-examples reports fewer divergent rows on a \
warm build/ than on a cold one, so the divergence figure this attempt records \
is the WARM figure and a cold run of the same head reports more"
  } >> "$LEDGER"
else
  echo "build-state=COLD: build/example-ordinary did not exist before \
make-check; the divergence figure this attempt records is the cold figure" \
    >> "$LEDGER"
fi
run_argv make-check -- make -k check
run_argv release-bindings -- make check-release-bindings
run_argv public-site -- make public-site
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
# V15, the V14 review: this row shipped classified ELIDED, "the capitalised
# token(s) JSON stand in for values this lane held". Nothing was elided. The
# command string is recorded verbatim and re-runs as written; the only
# capital word in it was the English word JSON inside this note. `checks.py`
# reads a standalone capitalised token as a placeholder for a value the lane
# held -- correctly, since that is exactly how `assemble.sh` writes PKG,
# FREEZE and ZIP -- and it cannot tell an acronym in prose from an elision.
# The classifier is right to be conservative, so the fix belongs HERE: the
# note says "json report" in lower case, and the recorded command classifies
# LITERAL, which is what it is. KEEP THIS WORD LOWER CASE, and keep any word
# added to this note lower case, or the row goes back to claiming the lane
# elided something it did not.
# THE ENVIRONMENT THE COMMAND NEEDS, INSIDE THE COMMAND THAT NEEDS IT.
#
# `run()` evaluates its string with `( cd "$REPO" && eval "$cmd" )`, so the
# invocation inherits this shell's environment while the RECORDED string
# carries none of it. Where the gate needs a variable to run at all, a
# reviewer handed the recorded string alone cannot reproduce the row -- which
# is the same class of defect as an elided token, and the lane directive is
# explicit: where environment variables are needed, the exact sanitized
# assignments to reproduce the command are recorded.
#
# `TRIPTYCH_CHROME` names the browser binary the gate drives. Hosts differ --
# `google-chrome-stable` on one, `/usr/bin/chromium` on another -- so the
# value is READ FROM THE ENVIRONMENT at compose time and never hardcoded: this
# script stays host-neutral and the row states the host it actually ran on.
# The prefix is EMPTY when the variable is unset, so a host whose gate needs
# nothing records nothing, rather than an assignment to an empty string that
# a reader would have to interpret.
#
# A binary path is not a private identity -- no account name, no home
# directory, no hostname -- so it survives the sanitizer unchanged. If a host
# ever needs a value that IS private, the sanitizer rewrites it here like
# anywhere else and the row says so; it does not belong hidden in an
# inherited environment either way.
# V16, THE V15 REVIEW: THE ENVIRONMENT IS A FIELD, NOT A PREFIX. V15 glued
# `TRIPTYCH_CHROME='...' ` onto the front of the command string, which is a
# correct shell prefix and an unreadable record: nothing downstream could
# separate "the environment this needed" from "the command this ran", and the
# assignment's own quoting is one more thing to get wrong. The exec record
# carries `env` as its own object; `render_shell()` puts the prefix back for
# a reader, from the field, so the two cannot drift.
GATE_ENV_JSON='{}'
if [ -n "${TRIPTYCH_CHROME:-}" ]; then
  GATE_ENV_JSON=$(python3 -c 'import json,sys;print(json.dumps({"TRIPTYCH_CHROME":sys.argv[1]}))' "$TRIPTYCH_CHROME")
fi
# THE JSON REPORT PATH IS A ROOT REFERENCE IN DOUBLE QUOTES, so it expands in
# the battery and expands identically in a replay. V15 wrote the real absolute
# path inside SINGLE quotes here and let the sanitizer turn it into
# `'$WORKSPACE/spincyc/v15-package-src/logs/attempt-01/browser-gate-parent.json'`
# -- a string naming a file no shell can ever produce, shipped under the label
# "the exact string handed to the shell; re-runnable". That row and its head
# twin are two of the seven the V15 review found.
RUN_ENV_JSON=$GATE_ENV_JSON
run browser-gate "node tools/tests/corpus_browser_gate.mjs --json-out \"\$EVIDENCE_ROOT/$LOGS_REL/$ROOT_NAME/browser-gate-$SIDE.json\" > /dev/null; gate=\$?; python3 \"\$TOOLS_ANCHOR/gate-summary.py\" \"\$EVIDENCE_ROOT/$LOGS_REL/$ROOT_NAME/browser-gate-$SIDE.json\"; echo 'report written: browser-gate-$SIDE.json beside this log, under this attempt root (the gate prints the same json report to stdout; discarded so the report ships once)'; exit \$gate"
if [ "$SIDE" = head ]; then
  run_argv browser-static -- python3 -m unittest discover -s tools/tests -p 'test_browser_static.py'
fi
run_argv gzip-sizes -- python3 '$TOOLS_ANCHOR/gzip-sizes.py' src/web/browser/catena

if [ "$SIDE" = head ]; then
  run_argv request-journals -- python3 '$TOOLS_ANCHOR/journal-dump.py' tools/tests/test_catena_wave_1.py
fi

if [ "$SIDE" = parent ] && [ -n "$HEAD_TEST" ]; then
  # The head's test file, run against the parent's production files. The copy
  # is part of the recorded command: the ledger says what ran, including the
  # substitution that makes the run mean what it means. IT ALSO DIRTIES A
  # TRACKED FILE, which is why the tree is read per command: this row and
  # every row after it record the tree they actually ran against.
  # V16, THE V15 REVIEW: `$REPO` MEANT TWO DIRECTORIES IN THIS ONE ROW.
  # V15 recorded `cp '$REPO/tools/tests/test_catena_wave_1.py' ...` with
  # `cwd : $REPO`, where the cwd `$REPO` was the PARENT checkout and the
  # quoted `$REPO` was the CANDIDATE checkout -- the sanitizer's `--repo` root
  # was the candidate, and the cwd token was written by hand. One name, two
  # roots, in one row: unquoting alone could not have recovered the execution.
  # The two roots now have two names, each defined exactly once, and
  # `catena_command.py` refuses a record that defines `REPO` at all.
  run head-tests-against-parent \
    "cp \"\$CANDIDATE_REPO/tools/tests/test_catena_wave_1.py\" tools/tests/test_catena_wave_1.py && python3 -m unittest discover -s tools/tests -p 'test_catena_wave_1.py' -v" \
    "head-tests-against-parent.log"
  run_argv request-journals -- python3 '$TOOLS_ANCHOR/journal-dump.py' tools/tests/test_catena_wave_1.py
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
END_TREE=$(tree_state)
BATTERY_END=$(date -Is)
{
  echo "POSTFLIGHT battery=$SIDE"
  echo "$BATTERY_END"
  echo "sha=$END_SHA"
  echo "porcelain=$END_TREE"
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
# A DIRTY POSTFLIGHT IS A FAILURE, NOT A NOTE. V12 recorded the reading and
# then keyed the failure branch only on SHA drift, so a battery that ended
# dirty wrote `status=complete` with an empty reason. The parent side's
# `restore-parent-tree` step is exactly what fails into this state — `set -u`
# is on and `-e` is not, so a failing restore does not abort — and the tree it
# leaves behind poisons the NEXT battery, which is how V12's second parent
# battery reported the head's 544 focused and 1,895 discovered as the parent's.
# ONLY THE POSTFLIGHT READING IS REQUIRED CLEAN: the parent side dirties the
# tree mid-battery on purpose, by design and on the record, and every row
# carries the tree it actually ran against.
if [ "$END_TREE" != clean ]; then
  echo "BATTERY $SIDE FAILED: the clone under test is dirty at postflight" >&2
  git -C "$REPO" status --porcelain >&2
  discard postflight "the clone under test was dirty when the battery \
finished ($END_TREE); a battery that ends dirty has left a checkout no commit \
names, and the next battery run against it would report this one's figures"
  exit 1
fi

# THE TERMINAL ROW: this attempt, and its disposition, once. `complete`, NOT
# `authoritative` -- see the state machine in assemble.sh's header. A battery
# that ran to completion has said everything it is entitled to say; which
# package a reviewer should read is a fact about a package attempt, and a lane
# whose ledger called three attempts authoritative could not state it.
attempt_row attempt="$ATTEMPT" attempt_no="$ATTEMPT_NO" record=attempt \
  side="$SIDE" sha="$END_SHA" cwd="$SIDE_CWD" phase=battery order="$INDEX" \
  start="$BATTERY_START" end="$BATTERY_END" exit=0 result="complete" \
  status=complete reason="" expect="$EXPECT_SHA" head="$END_SHA" \
  log="logs/order-$SIDE.txt"
echo "battery $SIDE complete: attempt $ATTEMPT, logs under logs/$ROOT_NAME/"
