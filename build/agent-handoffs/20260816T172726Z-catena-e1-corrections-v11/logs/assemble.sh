#!/usr/bin/env bash
# Assemble, freeze, derive, audit and seal the handoff package.
#
# One command, so the package is a function of the head rather than of the
# order somebody happened to do things in, and every transcript inside it is
# the honest one for the state it describes.
#
# THE ORDER IS THE ARGUMENT, and the V9 correction is the order. The V8
# pipeline derived its inventory at step 9 of 14 and then rewrote five of the
# members that inventory had already sized -- claims.json itself among them --
# so the shipped rows understated the final bytes by 1,822 and the audit could
# only wave at the drift as residue. The cure is a freeze line nothing crosses:
#
#   P1  evidence staging  -- everything whose bytes already exist. NO
#                            placeholder logs: a member is created by the
#                            phase that writes it, or it does not exist yet
#                            and is declared deferred. The gate comparison
#                            and the log index are produced HERE, as recorded
#                            steps, so both are frozen like any other member.
#   P2  normalize to a fixpoint -- seal/normalize passes until a check-only
#                            run reports zero hits AND zero would-be
#                            substitutions over the whole tree, the seal
#                            transcripts included, with a transcript that is
#                            byte-identical to the one already in the tree.
#                            No manifest is written here.
#   P3  THE FREEZE       -- (path, bytes, sha256) of every member, snapshot
#                            outside the package. The only inventory input
#                            the derivation accepts.
#   P4  derive once      -- claims.json + DERIVED-CLAIMS.md from the P3
#                            snapshot, written PRE-NORMALIZED so no later
#                            pass touches them; everything written at or
#                            after this instant is NAMED in derived_members,
#                            never sized.
#   P5  consistency audit -- a member outside derived_members whose bytes
#                            differ from the freeze is a HARD FAILURE, not
#                            printed residue. MANIFEST.sha256 is --pending:
#                            declared, and written by the next phase.
#   P6  manifest         -- re-hash every frozen row, refuse on drift, write
#                            MANIFEST.sha256 once. Nothing writes inside the
#                            package directory after this line.
#   P7  archive          -- the ZIP, single top-level root, sorted paths,
#                            DETERMINISTIC ENTRY METADATA; then the sidecar
#                            carrying the ZIP's sha256 AND its byte size.
#   P8  final verification -- verify-final-package.py, READ-ONLY, from the
#                            ZIP alone, run from the out-of-package trust
#                            anchor and pointed at it with --tools, so no
#                            byte the archive carries is ever executed and
#                            the anchor is named in the transcript rather
#                            than inherited; its transcript lands OUTSIDE the
#                            package, beside the archive, because a file
#                            created after the seal is not in the manifest
#                            that seal produced. Run it twice and it is the
#                            same run twice.
#
# The package-total and final-byte authority is MANIFEST.sha256 plus the ZIP
# and its sidecar. claims.json sizes only what was frozen before it was
# written, and says so.
#
# THE V11 CORRECTION, ONE: THE INVOCATION ITSELF IS LOGGED. V10 tee'd two
# transcripts and let everything else -- every phase banner, the fixpoint pass
# count, the archive's own byte line, the sidecar echo -- go to whatever
# terminal happened to be attached, so the pipeline's own run left no record.
# The run now re-invokes itself once through `tee`, into an invocation log
# beside the archive and OUTSIDE the package, added to the P0 never-reuse
# target list so it is allocated exactly like the package and the ZIP.
#
# THE V11 CORRECTION, TWO: A FAILED ATTEMPT SAYS SO, ON DISK. V10 left a
# half-built package directory behind on every failure path, unmarked and
# indistinguishable by inspection from a finished package that merely lacked
# its ZIP. Every failure path now writes DISCARDED.txt into the abandoned
# directory -- the attempt id, the phase it died in, the exact reason, and the
# statement that it is not evidence -- and appends one terminal row to the
# attempt ledger. One attempt is one id, one disposition and one reason: the
# first discard wins and every later one is a no-op, so nothing can be
# described as authoritative and discarded at once.
#
# THE V11 CORRECTION, THREE: THE GATE COMPARISON IS A STEP. compare-gate.py
# shipped in V10 and NOTHING in the pipeline invoked it, so the comparison had
# no ledger row, no exit and no log. It runs at P1 now, with its exit
# recorded; a difference is reported, never judged, exactly as checks.txt
# reports rather than judges.
#
# THE V11 CORRECTION, FOUR: ZIP ENTRY METADATA IS A CONSTANT. See P7.
#
# Environment:
#   ATTEMPTS  the append-only attempt ledger; default `attempt-ledger.jsonl`
#             under build/agent-handoffs. Point the batteries and this script
#             at ONE path for a single end-to-end ledger.
#   TOOLS     the P8 trust anchor: the out-of-package directory holding the
#             verifier and the trusted copies of the shared tools it runs.
#             Default: the directory this script was invoked from. Never the
#             package, and never the archive.
set -euo pipefail

REPO=${REPO:?set REPO to the implementation clone}
PARENT=${PARENT:-3c5b78249193df065c4e1c2ee5a98e5989c6e582}
REVIEW=${REVIEW:-55df5c236a1dfda12bb974efdbb9f46d0aeb3436}
STAMP=${STAMP:?set STAMP to the package timestamp}
SRC=${SRC:?set SRC to the staged package directory}
NAME=${NAME:-catena-e1-corrections-v10}
LANE=${LANE:-V10}

PKG="$REPO/build/agent-handoffs/$STAMP-$NAME"
ZIP="$PKG.zip"
# OUTSIDE THE PACKAGE, both of them: a file created after the seal is not in
# the manifest that seal produced, and the invocation log is being written
# while the package is still being built.
VERIFY_LOG="$REPO/build/agent-handoffs/$STAMP-$NAME.verify-final.log"
RUN_LOG="$REPO/build/agent-handoffs/$STAMP-$NAME.assemble.log"

# THE P8 TRUST ANCHOR. The verifier no longer imports or executes anything out
# of the reviewed ZIP: it runs trusted copies of the shared tools and hashes
# each against the copy the archive ships. That is only worth anything if the
# trusted copies come from somewhere this pipeline can name. Left to its
# default the anchor would be whatever directory the verifier itself sits in,
# and V10 ran it out of `$PKG/logs` -- the package staging tree the ZIP was
# built from. Outside the archive, never archive bytes, and still not an
# independent anchor; the verifier says so, verbatim, in the transcript.
#
# So the anchor is stated: the directory this script was invoked from, which
# is the tools' own source, overridable with TOOLS. Both the verifier that
# RUNS and the copies it trusts are taken from there, so the transcript's
# `verifier` line and its `tools` line name the same out-of-package source,
# and §19's "record its exact source/version/commit" is answered by the path,
# the per-tool sha256 the verifier prints, and the checkout commit where the
# anchor is a checkout.
HERE=$(cd "$(dirname "$0")" && pwd)
TOOLS=${TOOLS:-$HERE}

# THE ATTEMPT LEDGER. Append-only, outside the package, so it spans attempts:
# a discarded assembly and the one that replaced it are both in it, each with
# its own id, and neither can be mistaken for the other.
ATTEMPTS=${ATTEMPTS:-$REPO/build/agent-handoffs/attempt-ledger.jsonl}
mkdir -p "$(dirname "$ATTEMPTS")"

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

# No hex letter in the alphabet: the identity is rendered into checks.txt and
# the log index, and the consistency audit reads those for abbreviated commit
# SHAs.
nonce() {
  local pool='ghjkmnpqrstvwxyz23456789' out='' i pick
  for i in 1 2 3 4 5 6; do
    pick=$((RANDOM % ${#pool}))
    out="$out${pool:pick:1}"
  done
  printf '%s' "$out"
}

# The outer invocation allocates the identity and exports it; the inner,
# logged invocation inherits it, so one run is one attempt with one id.
ATTEMPT_NO=${ATTEMPT_NO:-$(next_attempt_no)}
ATTEMPT=${ATTEMPT:-package-$STAMP-$(printf '%02d' "$ATTEMPT_NO")$(nonce)}
ORDER=0
PHASE="P0 preflight"
DISCARDED=""
DISCARD_WHEN=""
DISCARD_REASON=""

step_row() {  # phase command exit start end log
  ORDER=$((ORDER + 1))
  attempt_row attempt="$ATTEMPT" attempt_no="$ATTEMPT_NO" record=step \
    side=package sha="${HEAD_SHA:-unknown}" cwd='$REPO' phase="$1" \
    order="$ORDER" command="$2" exit="$3" result="exit $3" start="$4" \
    end="$5" log="$6"
}

if [ -z "${ASSEMBLE_INNER:-}" ]; then
  echo "== P0 preflight: a handoff target is never reused"
  # The protocol allocates a NEW timestamped directory after proving neither
  # target exists. Never reuse, merge into, replace or overwrite an existing
  # handoff directory or archive; never update an existing ZIP in place. The
  # cure for a stale target is a fresh UTC STAMP, not a deletion. The
  # invocation log is allocated on the same terms as the package it describes.
  for TARGET in "$PKG" "$ZIP" "$ZIP.sha256" "$VERIFY_LOG" "$RUN_LOG"; do
    if [ -e "$TARGET" ]; then
      echo "REFUSING: handoff target already exists: $TARGET" >&2
      echo "Allocate a fresh UTC STAMP; an existing target is never reused." >&2
      # THE REFUSAL IS A LEDGER ROW, naming the timestamp that was attempted
      # and the outcome. Nothing was built and nothing was deleted, so this
      # attempt is discarded before it has a package to mark.
      attempt_row attempt="$ATTEMPT" attempt_no="$ATTEMPT_NO" record=attempt \
        side=package sha=unknown cwd='$REPO' phase="P0 preflight" order=0 \
        start="$(date -Is)" end="$(date -Is)" exit=1 result=refused \
        status=discarded log="(none: refused before anything was written)" \
        reason="the handoff target for stamp $STAMP already exists \
($(basename "$TARGET")); the stamp was refused, nothing was reused, merged, \
overwritten or deleted, and no package was created"
      exit 1
    fi
  done
  mkdir -p "$REPO/build/agent-handoffs"
  # noclobber: the log is CREATED, never opened over something that arrived
  # between the check above and this line.
  set -C
  if ! : > "$RUN_LOG"; then
    set +C
    echo "REFUSING: cannot allocate the invocation log: $RUN_LOG" >&2
    exit 1
  fi
  set +C
  export ASSEMBLE_INNER="$RUN_LOG"
  export REPO PARENT REVIEW STAMP SRC NAME LANE ATTEMPTS ATTEMPT ATTEMPT_NO
  export TOOLS
  [ -z "${MEASURED+x}" ] || export MEASURED
  set +e
  bash "$0" ${1+"$@"} 2>&1 | tee -a "$RUN_LOG"
  STATUS=${PIPESTATUS[0]}
  set -e
  echo "invocation log: $RUN_LOG"
  exit "$STATUS"
fi

# ---- from here on this is the inner, logged invocation ---------------------

# The refusal is re-asserted for every target this run is about to create.
# Only the invocation log is exempt, because the outer run created it after
# proving it absent -- the guard is not weakened, it has already fired.
for TARGET in "$PKG" "$ZIP" "$ZIP.sha256" "$VERIFY_LOG"; do
  if [ -e "$TARGET" ]; then
    echo "REFUSING: handoff target already exists: $TARGET" >&2
    # THE SAME REFUSAL, SAID THE SAME WAY. A guard that words itself
    # differently depending on how it was reached is two guards to read; and
    # the second line is the actionable half, so a reviewer who meets the
    # refusal here is owed it exactly as much as one who meets it above.
    echo "Allocate a fresh UTC STAMP; an existing target is never reused." >&2
    exit 1
  fi
done
echo "== P0 preflight passed: no handoff target for $STAMP existed, and the"
echo "   invocation log was allocated, not opened over anything"
echo "== attempt $ATTEMPT (invocation log: $(basename "$RUN_LOG"))"

HEAD_SHA=$(git -C "$REPO" rev-parse HEAD)
WORK=$(mktemp -d)
STARTED=$(date -Is)

# ONE ATTEMPT, ONE DISPOSITION, ONE REASON. The first call wins; every later
# call is a no-op. The marker is written INTO the abandoned directory, which
# is the only place an inspector is guaranteed to look, and beside the archive
# as well if one had already been produced -- an archive is never rewritten in
# place, so the marker goes next to it rather than into it.
discard() {
  local phase=$1
  local reason=$2
  [ -z "$DISCARDED" ] || return 0
  DISCARDED=$phase
  local when
  when=$(date -Is)
  DISCARD_WHEN=$when
  DISCARD_REASON=$reason
  if [ -d "$PKG" ] && [ ! -e "$PKG/DISCARDED.txt" ]; then
    mark_discarded "$phase" "$PKG/DISCARDED.txt"
  fi
  if [ -e "$ZIP" ] && [ ! -e "$ZIP.DISCARDED.txt" ]; then
    mark_discarded "$phase" "$ZIP.DISCARDED.txt"
  fi
  attempt_row attempt="$ATTEMPT" attempt_no="$ATTEMPT_NO" record=attempt \
    side=package sha="${HEAD_SHA:-unknown}" cwd='$REPO' phase="$phase" \
    order="$ORDER" start="${STARTED:-$when}" end="$when" exit=1 \
    result=discarded status=discarded reason="$reason" \
    log="$(basename "$RUN_LOG")" || true
}

mark_discarded() {
  local phase=$1
  local marker=$2
  {
    echo "DISCARDED ATTEMPT -- NON-AUTHORITATIVE"
    echo "attempt : $ATTEMPT"
    echo "stamp   : $STAMP"
    echo "phase   : $phase"
    echo "reason  : $DISCARD_REASON"
    echo "sha     : ${HEAD_SHA:-(not read)}"
    echo "started : ${STARTED:-(not recorded)}"
    echo "failed  : $DISCARD_WHEN"
    echo 'cwd     : $REPO'
    echo ""
    echo "This is a PARTIALLY BUILT package from an assembly attempt that"
    echo "FAILED at the phase named above. It is not a handoff package: it"
    echo "was not sealed, its manifest is absent or does not describe it,"
    echo "and no figure, digest or claim anywhere derives from it. It is"
    echo "kept, unaltered apart from this marker, so the attempt can be"
    echo "inspected; it is never repaired and never reused. The correction"
    echo "for a failed assembly is a fresh UTC stamp, never a deletion."
    echo ""
    echo "The same disposition, with this one reason, is the terminal row"
    echo "of this attempt in the ledger beside the handoff directory."
  } > "$marker" || true
}

# The backstop. An explicit failure path states its own reason and this does
# nothing; an unforeseen one still leaves the directory marked rather than
# silently half-built.
on_exit() {
  local status=$?
  [ -z "${WORK:-}" ] || rm -rf "$WORK"
  if [ "$status" -ne 0 ]; then
    discard "$PHASE" "the pipeline aborted in $PHASE with exit $status; no \
explicit reason was recorded, so this is the backstop marker and the \
invocation log is the transcript"
  fi
}
trap on_exit EXIT

# The members later phases write, declared instead of pre-created. A document
# may name one while it is absent; the deferral is printed on every pass, and
# the P8 re-check over the extraction runs with no deferrals at all.
DEFER=(--defer claims.json --defer DERIVED-CLAIMS.md
       --defer logs/derive-claims.log --defer logs/head-consistency.log
       --defer logs/seal.log --defer logs/seal-check.log)

PHASE="P1 evidence staging"
echo "== P1 evidence staging: $PKG at $HEAD_SHA"
mkdir -p "$PKG/logs"
( cd "$SRC" && find . -type f ! -path '*/__pycache__/*' -print0 ) \
  | ( cd "$SRC" && xargs -0 -I{} cp --parents {} "$PKG" )
chmod +x "$PKG"/logs/*.py "$PKG"/logs/*.sh 2>/dev/null || true

echo "== P1 git-derived members"
git -C "$REPO" log --format='%H%n  %aI%n  %s' "$PARENT..HEAD" > "$PKG/commits.txt"
{
  echo "# parent $PARENT"
  echo "# head   $HEAD_SHA"
  echo
  git -C "$REPO" diff --name-status "$PARENT..HEAD"
  echo
  git -C "$REPO" diff --stat "$PARENT..HEAD"
} > "$PKG/changed-files.txt"
git -C "$REPO" diff "$PARENT..HEAD" > "$PKG/changes.patch"

PHASE="P1 gate comparison"
echo "== P1 gate comparison: the two reports, object for object"
# V10 shipped compare-gate.py and invoked it from nothing, so the comparison
# a reader is told about had no row, no exit and no log. It is a step. Its
# exit is RECORDED, not judged: the two reports are two different code bases
# and a difference between them is the finding, not the failure.
GATE_LOG="$PKG/logs/gate-comparison.log"
GATE_CMD="python3 logs/compare-gate.py logs/browser-gate-parent.json logs/browser-gate-head.json"
GATE_START=$(date -Is)
if [ -e "$GATE_LOG" ]; then
  echo "REFUSING: a gate-comparison log was staged into the package: $GATE_LOG" >&2
  discard "$PHASE" "logs/gate-comparison.log was already present in the \
staged tree; this pipeline's own comparison is the authoritative one and a \
transcript is never overwritten"
  exit 1
fi
if [ -f "$PKG/logs/browser-gate-parent.json" ] \
   && [ -f "$PKG/logs/browser-gate-head.json" ]; then
  set +e
  ( cd "$PKG" && eval "$GATE_CMD" ) > "$GATE_LOG" 2>&1
  GATE=$?
  set -e
  echo "EXIT=$GATE" >> "$GATE_LOG"
  tail -2 "$GATE_LOG"
else
  {
    echo "the gate comparison did not run: one or both reports are absent"
    echo "from the staged package, so there was nothing to compare."
    echo "EXIT=(not run)"
  } > "$GATE_LOG"
  GATE="(not run)"
  cat "$GATE_LOG"
fi
step_row "$PHASE" "$GATE_CMD" "$GATE" "$GATE_START" "$(date -Is)" \
  "logs/gate-comparison.log"

PHASE="P1 checks.txt, the log index and the packaged attempt rows"
echo "== P1 composing checks.txt from the batteries' own ledgers"
python3 "$SRC/logs/checks.py" --package "$PKG" --head "$HEAD_SHA" \
  --parent "$PARENT" --attempts "$ATTEMPTS" --attempt "$ATTEMPT" \
  ${MEASURED:+--measured "$MEASURED"}

PHASE="P1 the sealer's own tests"
echo "== P1 the sealer's own tests"
TESTS_START=$(date -Is)
set +e
python3 "$PKG/logs/test-sanitize-and-seal.py" > "$PKG/logs/sealer-tests.log" 2>&1
TESTS=$?
set -e
echo "EXIT=$TESTS" >> "$PKG/logs/sealer-tests.log"
# Running them inside the package leaves bytecode behind, and a build artifact
# is not evidence.
rm -rf "$PKG/logs/__pycache__"
tail -3 "$PKG/logs/sealer-tests.log"
step_row "$PHASE" "python3 logs/test-sanitize-and-seal.py" "$TESTS" \
  "$TESTS_START" "$(date -Is)" "logs/sealer-tests.log"
[ "$TESTS" -eq 0 ] || {
  echo "SEALER TESTS FAILED"
  discard "$PHASE" "the sealer's own test suite failed with exit $TESTS; a \
package sealed by an unproven sealer is not evidence of privacy"
  exit 1
}

PHASE="P2 normalize to a fixpoint"
echo "== P2 normalize to a fixpoint (no manifest is written here)"
# Each pass appends its transcript to logs/seal.log, then a check-only pass
# writes its transcript beside it. The loop ends only when a check-only run
# exits clean AND its transcript is byte-identical to the one already in the
# tree -- which means the final check really did run over a tree that already
# contained its own transcript. That is the idempotence a reviewer can replay.
P2_START=$(date -Is)
PASS=0
while :; do
  PASS=$((PASS + 1))
  [ "$PASS" -le 6 ] || {
    echo "P2 FAILED: no fixpoint within 6 passes"
    discard "$PHASE" "the normalize/check loop reached no fixpoint within 6 \
passes; the tree never stopped changing under the sanitizer"
    exit 1
  }
  set +e
  ( cd "$REPO" && python3 "$PKG/logs/sanitize-and-seal.py" "$PKG" \
      --normalize-only "${DEFER[@]}" ) > "$WORK/seal-pass" 2>&1
  SEAL=$?
  set -e
  echo "EXIT=$SEAL" >> "$WORK/seal-pass"
  { echo "== normalize pass $PASS"; cat "$WORK/seal-pass"; } >> "$PKG/logs/seal.log"
  [ "$SEAL" -eq 0 ] || {
    cat "$WORK/seal-pass"
    echo "P2 FAILED"
    discard "$PHASE" "normalize pass $PASS failed with exit $SEAL"
    exit 1
  }
  set +e
  ( cd "$REPO" && python3 "$PKG/logs/sanitize-and-seal.py" "$PKG" \
      --check-only "${DEFER[@]}" ) > "$WORK/check-pass" 2>&1
  CHECK=$?
  set -e
  echo "EXIT=$CHECK" >> "$WORK/check-pass"
  if [ "$CHECK" -eq 0 ] \
     && cmp -s "$WORK/check-pass" "$PKG/logs/seal-check.log" 2>/dev/null; then
    echo "   fixpoint reached at pass $PASS"
    break
  fi
  cp "$WORK/check-pass" "$PKG/logs/seal-check.log"
  if [ "$CHECK" -ne 0 ] && [ "$PASS" -ge 3 ]; then
    cat "$WORK/check-pass"
    echo "P2 FAILED: check-only still failing"
    discard "$PHASE" "the check-only pass was still failing at pass $PASS \
with exit $CHECK"
    exit 1
  fi
done
step_row "$PHASE" "logs/sanitize-and-seal.py --normalize-only, then \
--check-only, to a fixpoint ($PASS pass(es))" 0 "$P2_START" "$(date -Is)" \
  "logs/seal.log"

PHASE="P3 the freeze"
echo "== P3 THE FREEZE: the snapshot that IS the inventory"
P3_START=$(date -Is)
python3 "$PKG/logs/derive-claims.py" --package "$PKG" \
  --write-freeze "$WORK/freeze.json"
step_row "$PHASE" "logs/derive-claims.py --package PKG --write-freeze \
FREEZE (outside the package)" 0 "$P3_START" "$(date -Is)" \
  "(the freeze is taken outside the package; the invocation log is the \
transcript)"

PHASE="P4 derive once"
echo "== P4 derive once, from the freeze, pre-normalized"
P4_START=$(date -Is)
( cd "$REPO" && python3 "$PKG/logs/derive-claims.py" --repo "$REPO" \
    --parent "$PARENT" --head "$HEAD_SHA" --review "$REVIEW" \
    --package "$PKG" --freeze "$WORK/freeze.json" --lane "$LANE" \
    --out "$PKG/claims.json" ) | tee "$PKG/logs/derive-claims.log"
step_row "$PHASE" "logs/derive-claims.py --repo REPO --parent PARENT --head \
HEAD --review REVIEW --package PKG --freeze FREEZE --lane $LANE --out \
claims.json" 0 "$P4_START" "$(date -Is)" "logs/derive-claims.log"

PHASE="P5 consistency audit"
echo "== P5 consistency audit: undeclared drift is a hard failure"
P5_START=$(date -Is)
set +e
python3 "$PKG/logs/head-consistency.py" --package "$PKG" \
  --pending MANIFEST.sha256 > "$PKG/logs/head-consistency.log" 2>&1
CONSISTENT=$?
set -e
echo "EXIT=$CONSISTENT" >> "$PKG/logs/head-consistency.log"
cat "$PKG/logs/head-consistency.log"
step_row "$PHASE" "logs/head-consistency.py --package PKG --pending \
MANIFEST.sha256" "$CONSISTENT" "$P5_START" "$(date -Is)" \
  "logs/head-consistency.log"
[ "$CONSISTENT" -eq 0 ] || {
  echo "HEAD CONSISTENCY FAILED"
  discard "$PHASE" "the consistency audit failed with exit $CONSISTENT; a \
member disagreed with the frozen inventory or with the claims derived from it"
  exit 1
}

PHASE="P6 manifest"
echo "== P6 manifest: prove the freeze held, then write the seal once"
P6_START=$(date -Is)
( cd "$REPO" && python3 "$PKG/logs/sanitize-and-seal.py" "$PKG" \
    --manifest-only --claims "$PKG/claims.json" )
step_row "$PHASE" "logs/sanitize-and-seal.py PKG --manifest-only --claims \
claims.json" 0 "$P6_START" "$(date -Is)" "MANIFEST.sha256"
# Nothing writes inside $PKG below this line. The single exception is the
# discard marker, which is written only when this attempt has already failed
# and is therefore not a package at all.

PHASE="P7 archive"
echo "== P7 archive"
P7_START=$(date -Is)
( cd "$REPO/build/agent-handoffs" \
  && python3 - "$STAMP-$NAME" <<'PY'
import sys, zipfile, pathlib
name = sys.argv[1]
root = pathlib.Path(name)
archive = pathlib.Path(name + ".zip")
# Never update an existing ZIP in place: the preflight proved absence at P0,
# and this refuses anything that arrived since rather than opening it for
# unconditional write.
if archive.exists():
    raise SystemExit(f"REFUSING: {archive} already exists; a handoff "
                     f"archive is never rewritten in place")

# THE V11 CORRECTION: EVERY ENTRY'S METADATA IS A CONSTANT.
#
# `ZipFile.write()` builds each entry through `ZipInfo.from_file()`, which
# sets `date_time = time.localtime(st.st_mtime)[0:6]`. The MS-DOS date and
# time fields carry NO timezone and store LOCAL wall clock, so differencing
# them against the UTC stamp in the archive's own name recovers the builder's
# UTC offset -- which is the V10 finding. The same call leaks the build host's
# mode and umask bits through `external_attr`, and its platform through
# `create_system`.
#
# So no entry is built from a stat. Each one is constructed:
#
#   date_time     1980-01-01 00:00:00, the DOS epoch floor -- ZIP cannot
#                 represent an earlier instant, and it is the conventional
#                 deterministic value, the ZIP analogue of the `mtime=0` this
#                 repository already uses for gzip. The package's real
#                 timestamps are inside it, in the ledgers, in UTC;
#   external_attr 0644, or 0755 for the tools the package ships to be run,
#                 decided by SUFFIX rather than by stat, so it is a function
#                 of the archive's own contents and of no host;
#   create_system 3, unconditionally, on every platform -- a constant that
#                 makes the Unix mode bits above meaningful, not a report of
#                 what this machine is;
#   compress_type deflate, stated on the entry as well as on the archive.
#
# The member BYTES are untouched: writestr writes the file's exact bytes, and
# MANIFEST.sha256 still describes them.
DOS_EPOCH = (1980, 1, 1, 0, 0, 0)
RUNNABLE = {".py", ".sh"}
# The package directory is the single top-level entry, which is what
# `guidance/external-review-handoffs.md` requires and what P8 proves rather
# than assumes.
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as handle:
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        info = zipfile.ZipInfo(path.as_posix(), date_time=DOS_EPOCH)
        info.compress_type = zipfile.ZIP_DEFLATED
        info.create_system = 3
        mode = 0o755 if path.suffix in RUNNABLE else 0o644
        info.external_attr = (0o100000 | mode) << 16
        handle.writestr(info, path.read_bytes())
print(f"archive: {archive} ({archive.stat().st_size} bytes)")
PY
)
( cd "$REPO/build/agent-handoffs" \
  && python3 - "$STAMP-$NAME" <<'PY'
import hashlib, pathlib, sys
name = sys.argv[1]
archive = pathlib.Path(name + ".zip")
hashed = hashlib.sha256()
with archive.open("rb") as handle:
    for block in iter(lambda: handle.read(1 << 20), b""):
        hashed.update(block)
# Digest AND size. The first line stays `sha256sum -c` compatible; the size
# line is the V9 addition, so a short download fails check 1 by arithmetic
# before it fails by digest.
sidecar = pathlib.Path(name + ".zip.sha256")
sidecar.write_text(f"{hashed.hexdigest()}  {archive.name}\n"
                   f"{archive.stat().st_size} bytes  {archive.name}\n",
                   encoding="utf-8")
sys.stdout.write(sidecar.read_text(encoding="utf-8"))
PY
)
step_row "$PHASE" "zip the package with constant entry metadata, then write \
the sidecar carrying its sha256 and its byte size" 0 "$P7_START" \
  "$(date -Is)" "$(basename "$RUN_LOG")"

PHASE="P8 final verification"
echo "== P8 final verification, from the ZIP alone, read-only"
echo "   trust anchor: $TOOLS"
# The transcript lands OUTSIDE the package, beside the archive: a file created
# after the seal is not in the manifest that seal produced.
#
# The verifier RUN is the trusted copy, not the staged one, and --tools names
# the same directory explicitly rather than letting the anchor fall out of
# wherever the verifier happened to be invoked from. Neither path is inside
# the package, so nothing here executes a byte the archive carries; the
# verifier hashes the archive's own copy of each tool against the trusted one
# and fails on divergence.
P8_START=$(date -Is)
python3 "$TOOLS/verify-final-package.py" \
  --zip "$REPO/build/agent-handoffs/$STAMP-$NAME.zip" \
  --sidecar "$REPO/build/agent-handoffs/$STAMP-$NAME.zip.sha256" \
  --name "$STAMP-$NAME" \
  --tools "$TOOLS" \
  | tee "$VERIFY_LOG"
step_row "$PHASE" "verify-final-package.py --zip ZIP --sidecar SIDECAR \
--name $STAMP-$NAME --tools TOOLS (both the verifier and the trusted tools \
taken from the out-of-package anchor, never from the archive)" 0 \
  "$P8_START" "$(date -Is)" "$(basename "$VERIFY_LOG")"

# THE TERMINAL ROW. This attempt is the authoritative one, named as such, with
# the archive it produced. Nothing else in the ledger carries this id.
attempt_row attempt="$ATTEMPT" attempt_no="$ATTEMPT_NO" record=attempt \
  side=package sha="$HEAD_SHA" cwd='$REPO' phase="P8 complete" \
  order="$ORDER" start="$STARTED" end="$(date -Is)" exit=0 \
  result="sealed $STAMP-$NAME.zip" status=authoritative reason="" \
  log="$(basename "$RUN_LOG")"
echo "== sealed: attempt $ATTEMPT is the authoritative one for $STAMP-$NAME"
