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
#                            declared, and written by the next phase. Then the
#                            two protocol audits -- the attempt-log audit and
#                            the authority audit -- and the LAST write inside
#                            the package: logs/attempts.json, carrying this
#                            attempt's own terminal row, which says `sealed`
#                            and NOT `authoritative` (see the V13 correction
#                            below), because a ledger member written at P1
#                            cannot state a disposition reached at P8 and a
#                            member written at P5 cannot state one either.
#                            Neither audit writes a member; the invocation log
#                            is their transcript.
#   P6  manifest         -- re-hash every frozen row, refuse on drift, write
#                            MANIFEST.sha256 once. Nothing writes inside the
#                            package directory after this line.
#   P7  archive          -- the ZIP, single top-level root, sorted paths,
#                            DETERMINISTIC ENTRY METADATA; then the sidecar
#                            carrying the ZIP's sha256 AND its byte size; then
#                            `sanitize-and-seal.py --verify`, which recomputes
#                            every manifest digest and cross-proves the ZIP
#                            against the manifest. V12 shipped that mode and
#                            never invoked it.
#   P8  final verification -- verify-final-package.py, READ-ONLY, from the
#                            ZIP alone, run from the out-of-package trust
#                            anchor and pointed at it with --tools, so no
#                            byte the archive carries is ever executed and
#                            the anchor is named in the transcript rather
#                            than inherited; its transcript lands OUTSIDE the
#                            package, beside the archive, because a file
#                            created after the seal is not in the manifest
#                            that seal produced. Run it twice and it is the
#                            same run twice. It is handed the contemporaneous
#                            executed-tool record (--executed) and writes its
#                            own machine-readable table (--table-out).
#   P9  FINAL AUTHORITY  -- and not one instant earlier. The ZIP's size and
#                            digest are RECOMPUTED here, from the archive's
#                            own bytes, never carried forward from P7; the P8
#                            transcript's verdict line and its post-verification
#                            rehash line are read back out of the transcript;
#                            and only if both say PASS/UNCHANGED does this
#                            phase write `<package>.authority.json`, append the
#                            external `authoritative` row, and derive the
#                            per-package append-only ledger
#                            `<package>.attempts.jsonl` beside the archive.
#                            If P8 failed, none of that happens and the attempt
#                            stays non-authoritative.
#   P10 the gates        -- authority-coherence.py and handoff-inventory.py,
#                            which V12 ran BY HAND after sealing, which is why
#                            two of its attempts had to be superseded. They run
#                            here, automatically, each to its own outer log,
#                            and either one refusing fails the run.
#   P11 outer sanitization -- the tracked files BESIDE the package -- the
#                            invocation log, the P8 transcript, the digest
#                            sidecar, the authority record, the executed-tool
#                            record, the tool-bytes table, the per-package
#                            ledger and the two gate logs -- through
#                            `sanitize-and-seal.py --sanitize-files`, then
#                            `--scan-files` over the same set, and residue
#                            fails the run. THIS PHASE RUNS IN THE OUTER STAGE,
#                            after `tee` has closed the invocation log; see
#                            THE V13 CORRECTION, THREE.
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
# THE V12 CORRECTION, ONE: EVERY ATTEMPT OWNS A LOG ROOT. V11 gave the battery
# logs an attempt ordinal and gave the package-phase transcripts nothing, so
# `logs/gate-comparison.log`, `logs/sealer-tests.log`, `logs/seal.log`,
# `logs/seal-check.log`, `logs/derive-claims.log` and `logs/head-consistency.log`
# were fixed paths every attempt opened. In the reviewed package the gate
# comparison log was claimed by six attempts and the sealer-tests log by five:
# a failed attempt's transcript did not stay with that attempt, the next
# attempt overwrote it. Every transcript now lives under
# `logs/attempt-<ordinal>/`, with the SAME ordinal the attempt ledger
# allocated, batteries and package phases alike, and a target that already
# exists is still refused rather than opened. `logs/checks.py --audit-logs`
# runs at P5 and refuses the seal if any log breaks the rule.
#
# THE V12 CORRECTION, TWO: `authoritative` NAMES A PACKAGE, NOT A RUN, AND THE
# LEDGER MEMBER IS WRITTEN LATE.
#
# The reviewed package shipped `logs/attempts.json` marking THREE attempts
# `authoritative` -- the head battery, the parent battery and a superseded
# package attempt -- while the package that actually shipped carried
# "unresolved: the ledger carries no terminal row for this attempt", because
# `checks.py` wrote that member at P1 and this script wrote its own terminal
# row at the end of P8. Only prose repaired it. Two defects, both fixed here:
#
#   * ONE WORD FOR TWO FACTS. A battery terminates `complete` or `failed`.
#     `authoritative` is reserved for a package attempt and at most one package
#     attempt in a ledger may hold it.
#   * THE MEMBER WAS WRITTEN BEFORE THE FACT IT REPORTS. `logs/attempts.json`
#     is now written at P5, after the consistency audit and immediately before
#     P6, which is as late as the freeze line allows; it is a DECLARED DERIVED
#     MEMBER, deferred exactly like `claims.json`, and this script appends its
#     own terminal row just before that write so the shipped ledger carries it.
#
# THE ATTEMPT STATE MACHINE. This is the one statement of it; `battery.sh` and
# `logs/checks.py --audit-authority` refer here rather than restating it.
#
#   BATTERY ATTEMPT   (side=head, side=parent)
#       started -> complete
#       started -> failed
#     `started` is optional -- a battery that runs to its terminal row in one
#     go writes only that row. A battery attempt may NEVER be `authoritative`,
#     `sealing` or `superseded`: those are package words.
#
#   PACKAGE ATTEMPT   (side=package)
#       started -> sealing -> sealed -> authoritative -> superseded
#       started -> sealing -> sealed -> superseded
#       started -> sealing -> discarded
#     `started` and `sealing` are optional prefixes; `discarded` keeps its
#     meaning and its exactly-one-reason rule. `sealed` is the TERMINAL
#     disposition and the most a row INSIDE the package may ever claim.
#     `authoritative` is a POST-TERMINAL state, carried by a `record=state`
#     row that exists only OUTSIDE the package, appended at P9 -- see THE V13
#     CORRECTION, ONE. AT MOST ONE package attempt in a ledger may resolve to
#     `authoritative` -- an attempt's resolved state is its LAST state row, so
#     superseding an attempt is what makes room for the next one, and a
#     package attempt that ends `superseded` is not counted. THIS SCRIPT NEVER
#     SUPERSEDES ANOTHER ATTEMPT. Sealing a replacement while a previous
#     package still holds authority is refused, by name, at P5: demoting a
#     package that is already out for review is a judgement about which package
#     a reader should be holding, and the operator appends that supersession --
#     one row, one reason -- rather than an assembly script making it as a side
#     effect of running again.
#
#   Exactly one `record=attempt` row per attempt carries the TERMINAL
#   disposition (`complete`/`failed`/`sealed`/`discarded`). The non-terminal
#   states and the post-terminal `authoritative`/`superseded` are `record=state`
#   rows, so nothing can be described as authoritative and discarded at once
#   and superseding does not overwrite the disposition it supersedes.
#
# THE V13 CORRECTION, ONE: NO SEALED BYTE CLAIMS FINAL AUTHORITY BEFORE P8.
#
# V12 wrote `status=authoritative` at P5 -- before the manifest, before the ZIP
# existed, before P7 and P8 had proved anything -- and froze that row into the
# shipped `logs/attempts.json`. The package and the archive therefore carried a
# permanent claim of final authority that a later P7/P8 failure could only
# answer with a best-effort sibling marker and an external supersession. A
# record that must be repaired afterwards has settled nothing.
#
# The required progression, and this pipeline's shape is now exactly it:
#
#     attempt started -> package sealed -> P7/P8 verification
#                     -> post-P8 ZIP size/hash confirmed
#                     -> FINAL AUTHORITY ESTABLISHED
#
#   * the P5 terminal row -- the one that is frozen into the package -- says
#     `sealed`. That is a true statement about the package DIRECTORY at that
#     instant and it is the whole of what the package may claim about itself;
#   * FINAL AUTHORITY is established at P9, after P8 has passed, by exactly one
#     record: `<package>.authority.json` beside the archive, whose schema is
#     owned by `authority-coherence.py` and restated nowhere else. It names the
#     ZIP's basename, its RECOMPUTED byte size and RECOMPUTED sha256, the P8
#     transcript's own verdict line and its own post-verification rehash line.
#     The binding runs ONE WAY -- the record names the archive's digest, and the
#     archive carries no `*.authority.json` member -- because a record the
#     archive vouched for is a record the archive could have been sealed around;
#   * IF P8 FAILS, NO AUTHORITY RECORD IS WRITTEN and the attempt stays
#     non-authoritative. The failure supersedes or discards exactly as before.
#
# The claim is kept non-vacuous by the failure path: if P6, P7 or P8 fails, the
# attempt is SUPERSEDED -- one `record=state` row with its one reason -- and
# `DISCARDED.txt` plus `logs/DISCARDED-<attempt>.txt` are written into the
# package directory, the second under exactly the name `checks.py` already
# refuses to compose a package from.
#
# AND THE LEDGER A REVIEWER CAN REACH. V12's `$ATTEMPTS` default was a
# lane-wide `attempt-ledger.jsonl` that was neither beside the package nor
# shipped nor tracked, so the package deferred to records no reviewer could
# open. The lane ledger STAYS the append-only superset -- it is the allocator
# `checks.py --allocate-ordinal` spends ordinals out of, and splitting it per
# package is exactly how V12 reissued ordinals 03/04/05 -- and P9 DERIVES
# `<package>.attempts.jsonl` beside the archive by copying, in original order,
# every row of the lane ledger belonging to an attempt this package mentions.
# Copy, not point: one allocator, and a complete slice beside the artifact.
#
# THE V13 CORRECTION, TWO: EVERY EXECUTED TOOL IS HASHED AS IT IS EXECUTED.
#
# V12 digested four tools, at P8, from the archive -- which proves shipped
# against trusted and says nothing at all about what actually ran. `run_tool`
# below computes the sha256 of the exact file it is about to execute,
# IMMEDIATELY before executing it, records the logical identity, the phase, the
# transcript and the instant, and then runs it. Every tool invocation in this
# file goes through it. The rows are rendered to
# `<package>.executed-tools.json`, which P8 receives as `--executed` and
# cross-proves against the archive's own copies; P8's machine-readable table
# lands beside it as `<package>.tool-bytes.json`. Every tool the package ships
# under `logs/` appears in that record with a class, including the ones this
# attempt did not run, so "not executed" is a stated fact rather than an
# absence.
#
# THE V13 CORRECTION, THREE: THE OUTER LOGS ARE SANITIZED BEFORE THEY ARE
# COMMITTED, AND THE ORDERING PROBLEM IS SOLVED RATHER THAN NOTED.
#
# The sanitizer's walk root is the package. The tracked files BESIDE it are
# written after the manifest and never passed through it, so V12 committed the
# absolute workspace path, the account name and the lane anchor on twelve lines
# of `.assemble.log` and `.verify-final.log`.
#
# The ordering problem is real: `$RUN_LOG` is open, and still being appended
# to, by the `tee` this script re-executes itself under, so sanitizing it in
# place from the inner stage would rewrite a file that is about to be written
# to again -- the sanitized bytes would be overwritten by the tail of the run.
# THE SOLUTION IS THE STAGE, NOT A TRICK: P11 runs in the OUTER stage, after
# the `tee` pipeline has exited and the invocation log's final byte is written,
# where every outer sibling is a finished file. The cost is stated rather than
# hidden: the outer stage's own lines are not in the invocation log, so P11's
# transcripts are outer siblings of their own and the ledger carries its rows.
#
# THE V13 CORRECTION, FOUR: THE GATES THIS PIPELINE NEVER RAN, RUN.
# `authority-coherence.py` and `handoff-inventory.py` shipped in V12 and were
# invoked by hand afterwards, which is how two attempts came to be superseded
# after sealing. Both run at P10, automatically, routed through `run_tool`,
# each to its own outer transcript, and either one refusing fails the run.
# `handoff-inventory.py` distinguishes setup failure (exit 2) from findings
# (exit 1) and so does this.
#
# THE V13 CORRECTION, FIVE: ONE ALLOCATOR, AND EVERY ROW NAMES ITS LANE.
# V12's `next_attempt_no()` here took `max(attempt_no) + 1` over whatever file
# it was pointed at; the operator started a fresh ledger partway through the
# lane, so ordinals 03/04/05/06 were reissued as 03/04/05 while a shipped
# member claimed an ordinal is allocated once for the whole lane. That function
# is DELETED. `checks.py --allocate-ordinal` is the one allocator -- it refuses
# an ordinal any row has ever carried, however that attempt ended, and refuses
# a ledger belonging to another lane -- and `battery.sh` calls the same one.
# Nothing in this file computes a maximum. Every row `attempt_row` writes
# carries `lane`, prepended in the helper rather than typed at each call site,
# because a rule kept by remembering is a rule already broken somewhere.
#
# Environment:
#   REPO      the implementation clone. Required.
#   PARENT    the parent commit the package is a diff against.
#   REVIEW    the review commit the corrections answer.
#   STAMP     the package's UTC timestamp. Required.
#   SRC       the staged package directory. Required.
#   NAME      the package basename after the stamp.
#   LANE      the lane identity, as the ledger and the claims record it.
#   ATTEMPTS  the LANE-WIDE append-only attempt ledger; default
#             `attempt-ledger.jsonl` under build/agent-handoffs. Point the
#             batteries and this script at ONE path for a single end-to-end
#             ledger and one ordinal allocator: ordinal uniqueness is a
#             property of ONE FILE, and a per-package ledger would reissue 01
#             for every package. The per-package slice beside the archive is
#             DERIVED from this at P9 and is never this value.
#   ATTEMPT_NO / ATTEMPT
#             normally allocated and minted here and exported to the inner
#             stage. Set them only to re-enter an identity that already exists.
#   TOOLS     the P8 trust anchor: the out-of-package directory holding the
#             verifier and the trusted copies of the shared tools it runs.
#             Default: the directory this script was invoked from. Never the
#             package, and never the archive. It is named SYMBOLICALLY in
#             everything this script echoes; see EVIDENCE below.
set -euo pipefail

REPO=${REPO:?set REPO to the implementation clone}
PARENT=${PARENT:-d312786dd2b23926aa88e29ea15647dfcc7e7e6e}
REVIEW=${REVIEW-}
STAMP=${STAMP:?set STAMP to the package timestamp}
SRC=${SRC:?set SRC to the staged package directory}
NAME=${NAME:-catena-e1-corrections-v13}
LANE=${LANE:-V13}

PKG="$REPO/build/agent-handoffs/$STAMP-$NAME"
ZIP="$PKG.zip"
# OUTSIDE THE PACKAGE, every one of them: a file created after the seal is not
# in the manifest that seal produced, and the invocation log is being written
# while the package is still being built.
VERIFY_LOG="$REPO/build/agent-handoffs/$STAMP-$NAME.verify-final.log"
RUN_LOG="$REPO/build/agent-handoffs/$STAMP-$NAME.assemble.log"
# THE POST-P8 RECORDS. Each is allocated on the same never-reuse terms as the
# package and the archive, and each is sanitized at P11 before it can be
# committed. `authority-coherence.py` derives every one of these names from the
# package basename, so the names are a contract and not a convention.
AUTHORITY="$REPO/build/agent-handoffs/$STAMP-$NAME.authority.json"
PKG_LEDGER="$REPO/build/agent-handoffs/$STAMP-$NAME.attempts.jsonl"
EXECUTED="$REPO/build/agent-handoffs/$STAMP-$NAME.executed-tools.json"
TOOL_BYTES="$REPO/build/agent-handoffs/$STAMP-$NAME.tool-bytes.json"
COHERENCE_LOG="$REPO/build/agent-handoffs/$STAMP-$NAME.authority-coherence.log"
INVENTORY_LOG="$REPO/build/agent-handoffs/$STAMP-$NAME.handoff-inventory.log"
SANITIZE_LOG="$REPO/build/agent-handoffs/$STAMP-$NAME.outer-sanitize.log"
SCAN_LOG="$REPO/build/agent-handoffs/$STAMP-$NAME.outer-scan.log"

# THE OUTER SIBLINGS, AS ONE LIST, DECLARED ONCE. P0 refuses to reuse any of
# them, P11 sanitizes and then rescans exactly this set, and a name that is in
# one list and not the other is the defect that let V12 commit two unsanitized
# transcripts. `$SANITIZE_LOG` and `$SCAN_LOG` are not in it: they are written
# BY P11, they cannot be inputs to the pass that writes them, and on a clean
# pass the sanitizer names no path at all -- `$SCAN_LOG` covers `$SANITIZE_LOG`
# and a finding in either fails the run, so neither can be committed dirty and
# silent.
OUTER_SIBLINGS=("$RUN_LOG" "$VERIFY_LOG" "$ZIP.sha256" "$AUTHORITY"
                "$EXECUTED" "$TOOL_BYTES" "$PKG_LEDGER" "$COHERENCE_LOG"
                "$INVENTORY_LOG")

# THE SYMBOLIC NAME OF THE TRUST ANCHOR, and eleven of V12's twelve leaking
# lines. `TOOLS` is an absolute path under the account's home and the lane's
# evidence directory; the `trust anchor:`, `verifier` and `tools` lines this
# pipeline echoed printed it verbatim into a tracked log. Where the value is
# only informational the SYMBOL is echoed instead -- spelled exactly as the
# sanitizer's `evidence-dir` rule spells it, so the echoed line is already at
# the fixpoint P11 checks for and the two can never drift apart. The real path
# is still what is EXECUTED; it is simply not what is printed.
EVIDENCE='$EVIDENCE'

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
#
# V13: EVERY ROW NAMES ITS LANE, and it is prepended here rather than typed at
# thirty call sites, because a rule enforced by remembering is a rule that has
# already been broken somewhere. `checks.py --seal-ledger` refuses a ledger
# with an unlaned row, and it is right to: two lanes' ledgers concatenated in
# silence is how one lane's ordinals come to describe another's attempts.
# `battery.sh` does the same on its side.
attempt_row() {
  python3 - lane="$LANE" "$@" <<'PY' >> "$ATTEMPTS"
import json, sys
print(json.dumps(dict(one.split("=", 1) for one in sys.argv[1:]),
                 sort_keys=True))
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

# ---- the contemporaneous executed-tool record ------------------------------
#
# THE V13 CORRECTION, TWO. The review's requirement, in its own order: capture
# the SHA-256 of the exact bytes contemporaneously AT EXECUTION, record the
# logical identity, execute, link the execution to that digest, ship a copy,
# compare shipped to executed. V12 did none of it. It digested four tools at
# P8, out of the archive, which proves the shipped copy against the trusted
# copy and is silent about what actually ran -- and "what actually ran" is the
# only question a reader of a transcript is asking.
#
# `run_tool` is the whole answer, and below this line it is the ONLY way a tool
# is invoked in this file. It hashes the exact file it is about to execute,
# IMMEDIATELY before executing it, appends one run row, and then runs it.
#
# IT LIVES ABOVE THE FORK because the FIRST tool this pipeline runs is
# `checks.py --allocate-ordinal`, at P0, before the package exists and before
# this attempt even has an id. The rows therefore carry neither: the attempt id
# and each tool's shipped path and class are resolved at RENDER time, when the
# package is there to answer. A row records what only the moment of execution
# knows -- which bytes, when, in which phase, into which transcript -- and
# nothing it would have to guess.
RUNS=${RUNS:-$(mktemp -t assemble-runs.XXXXXXXX)}

run_tool() {  # logical-name executed-path phase log -- command...
  local name=$1 executed=$2 phase=$3 log=$4
  shift 4
  if [ "${1:-}" != "--" ]; then
    echo "run_tool: expected -- between the identity and the command" >&2
    return 2
  fi
  shift
  local digest
  # IMMEDIATELY BEFORE. Not at the top of the phase, not at P8, not out of the
  # archive: from the file that is about to be handed to the interpreter, on
  # the line before it is.
  digest=$(sha256sum "$executed" | cut -d' ' -f1)
  python3 - "$name" "$digest" "$(date -Is)" "$phase" "$log" shipped \
      <<'PY' >> "$RUNS"
import json, sys
keys = ("tool", "sha256", "at", "phase", "log", "kind")
print(json.dumps(dict(zip(keys, sys.argv[1:])), sort_keys=True))
PY
  "$@"
}

# THE INTERPRETER AND git ARE RECORDED ONCE, BY IDENTITY AND DIGEST. They are
# not this lane's bytes, they are not shipped, and routing every one of the
# dozens of `git` reads through `run_tool` would bury the tools the review is
# actually asking about under repetition of two constants. They are named,
# hashed and classed `external-system-tool`, which is the class the vocabulary
# has for exactly this, and the row says which phase first used them.
record_external_tool() {  # logical-name absolute-path phase
  local name=$1 path=$2 phase=$3 digest
  [ -x "$path" ] || return 0
  digest=$(sha256sum "$path" | cut -d' ' -f1)
  python3 - "$name" "$digest" "$(date -Is)" "$phase" \
      "$(basename "$RUN_LOG")" system <<'PY' >> "$RUNS"
import json, sys
keys = ("tool", "sha256", "at", "phase", "log", "kind")
print(json.dumps(dict(zip(keys, sys.argv[1:])), sort_keys=True))
PY
}

# THE RECORD ITSELF: the accumulated run rows, resolved against the package,
# plus a row for EVERY tool the package ships that this attempt did NOT
# execute.
#
# "Every tool shipped under logs/ appears with some class" is the requirement,
# and the not-executed ones are the half that matters: a record listing only
# what ran cannot be distinguished, by a reader, from a record that forgot
# something. `shipped-not-executed` says the shipped copy exists, states its
# digest, and states that THIS attempt did not run it -- which is true of the
# tools `battery.sh` runs in a different attempt, and of the reviewer-facing
# helpers nothing in this pipeline calls.
#
# It refuses on ONE condition of its own: two different digests for one logical
# tool. Several rows per tool are expected -- `sanitize-and-seal.py` runs a
# dozen times -- and every one of them must have hashed the same bytes, or
# "the tool that ran" is not a single thing and the record cannot say which
# copy any claim is about.
emit_executed_tools() {  # phase
  python3 - "$RUNS" "$EXECUTED" "$ATTEMPT" "$EVIDENCE" "$PKG" "$1" \
      "$(basename "$RUN_LOG")" <<'PY'
import datetime, hashlib, json, pathlib, sys

runs_path, out, attempt, anchor, package, phase, outer = sys.argv[1:8]
logs = pathlib.Path(package) / "logs"

rows = []
executed = set()
digests = {}
problems = []
for line in pathlib.Path(runs_path).read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue
    row = json.loads(line)
    name = row["tool"]
    first = digests.setdefault(name, row["sha256"])
    if first != row["sha256"]:
        problems.append(f"{name}: executed as {first} and as "
                        f"{row['sha256']}; one logical tool, two sets of bytes")
    # RESOLVED HERE, NOT AT EXECUTION. A tool the package ships under `logs/`
    # is named by that path whichever copy of it was executed -- the P8 trust
    # anchor deliberately executes the out-of-package copy -- because "shipped
    # path plus executed digest" is exactly the pair a reader needs to compare
    # the two. At P0 the package does not exist yet, so a run-time answer
    # would have been wrong for the first tool this pipeline runs.
    if row.get("kind") == "system":
        path = f"(external: {name} is a system tool, not a package member)"
        klass = "external-system-tool"
    elif (logs / name).is_file():
        path = f"logs/{name}"
        klass = "shipped-executed"
        executed.add(name)
    else:
        path = f"{anchor}/{name}"
        klass = "external-system-tool"
    rows.append({"tool": name, "path": path, "attempt": attempt,
                 "sha256": row["sha256"], "at": row["at"],
                 "phase": row["phase"], "log": row["log"], "class": klass})

if problems:
    for one in sorted(set(problems)):
        print(f"REFUSING: {one}", file=sys.stderr)
    raise SystemExit(1)

now = (datetime.datetime.now(datetime.timezone.utc)
       .replace(microsecond=0).isoformat().replace("+00:00", "Z"))
if logs.is_dir():
    for one in sorted(logs.iterdir()):
        if not one.is_file() or one.suffix not in (".py", ".sh"):
            continue
        if one.name in executed:
            continue
        rows.append({
            "tool": one.name,
            "path": f"logs/{one.name}",
            "attempt": attempt,
            "sha256": hashlib.sha256(one.read_bytes()).hexdigest(),
            "at": now,
            "phase": phase,
            "log": outer,
            "class": "shipped-not-executed",
        })

record = {
    "schema": "catena-executed-tools/1",
    "attempt": attempt,
    # THE SYMBOLIC ANCHOR, NEVER AN ABSOLUTE PATH. This file is tracked and
    # committed; the anchor's absolute path is the account name and the
    # workspace topology, and the symbol is what identifies it.
    "anchor": anchor,
    "runs": rows,
}
pathlib.Path(out).write_text(
    json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
counts = {}
for row in rows:
    counts[row["class"]] = counts.get(row["class"], 0) + 1
print("executed-tools: " + ", ".join(
    f"{number} {kind}" for kind, number in sorted(counts.items())))
PY
}

# ---- the attempt identity --------------------------------------------------
#
# THE ORDINAL IS ALLOCATED, NOT COMPUTED. V12's `next_attempt_no()` took
# `max(attempt_no) + 1` over whatever file it was handed; the operator started
# a fresh ledger partway through the lane and 03/04/05/06 were reissued as
# 03/04/05, while a shipped member claimed "an ordinal is allocated once for
# the whole lane". `checks.py --allocate-ordinal` is now the ONE allocator --
# `battery.sh` calls it too, and its own local maximum has been deleted -- and
# it refuses an ordinal any row has ever carried, however that attempt ended,
# and refuses a ledger belonging to another lane. This script does not compute
# a maximum anywhere.
#
# It is the first `run_tool` call of the run, which is why the machinery above
# it is above the fork.
allocate_ordinal() {
  run_tool checks.py "$TOOLS/checks.py" "P0 preflight" \
    "(the allocation writes no transcript; the ordinal is its whole output)" \
    -- python3 "$TOOLS/checks.py" --allocate-ordinal --attempts "$ATTEMPTS" \
    --lane "$LANE"
}

# The outer invocation allocates the identity and exports it; the inner,
# logged invocation inherits it, so one run is one attempt with one id.
#
# A REFUSED ALLOCATION IS A REFUSED RUN, and it leaves no ledger row because
# there is no identity to write one under: the allocator refused to give this
# run a name. Its own message on stderr is the whole record, which is the
# honest amount for a run in which nothing was created, nothing was reused and
# no package was begun.
if [ -z "${ATTEMPT_NO:-}" ]; then
  if ! ATTEMPT_NO=$(allocate_ordinal); then
    echo "REFUSING: the lane ledger would not allocate an attempt ordinal" >&2
    echo "for lane $LANE; nothing was created and no package was begun." >&2
    exit 1
  fi
fi
ATTEMPT=${ATTEMPT:-package-$STAMP-$(printf '%02d' "$ATTEMPT_NO")$(nonce)}
# THIS ATTEMPT'S LOG ROOT, from the SAME ordinal the ledger allocated. Every
# transcript this run writes inside the package goes under it; no other
# attempt can name it, so no other attempt can overwrite what is in it.
LOG_PREFIX=$(printf '%02d' "$ATTEMPT_NO")
LOG_ROOT="logs/attempt-$LOG_PREFIX"
PKG_LOG_ROOT="$PKG/$LOG_ROOT"
ORDER=0
PHASE="P0 preflight"
DISCARDED=""
DISCARD_WHEN=""
DISCARD_REASON=""
# Set once the terminal `sealed` row has been appended at P5. After that
# instant a failure supersedes this attempt rather than discarding it: the
# disposition row is already written and one attempt gets exactly one.
SEALED=""
# Set once the P9 final-authority record exists and the external
# `authoritative` row has been appended. It is a SEPARATE flag from `SEALED`
# because the two facts are separate -- V12 conflated them by writing one row
# for both -- and because the marker a late failure writes has to say which of
# them the attempt had actually reached.
AUTHORITATIVE=""

step_row() {  # phase command exit start end log
  ORDER=$((ORDER + 1))
  attempt_row attempt="$ATTEMPT" attempt_no="$ATTEMPT_NO" record=step \
    side=package sha="${HEAD_SHA:-unknown}" cwd='$REPO' phase="$1" \
    order="$ORDER" command="$2" exit="$3" result="exit $3" start="$4" \
    end="$5" log="$6"
}

if [ -z "${ASSEMBLE_INNER:-}" ]; then
  # The run rows are scratch: they are the SOURCE of the executed-tool record,
  # not the record, and the record is rendered beside the package before this
  # stage ends. The outer stage owns them because the outer stage outlives the
  # inner one.
  trap 'rm -f "$RUNS"' EXIT
  echo "== P0 preflight: a handoff target is never reused"
  # The protocol allocates a NEW timestamped directory after proving neither
  # target exists. Never reuse, merge into, replace or overwrite an existing
  # handoff directory or archive; never update an existing ZIP in place. The
  # cure for a stale target is a fresh UTC STAMP, not a deletion. The
  # invocation log is allocated on the same terms as the package it describes,
  # and so is every post-P8 record: an authority record, an executed-tool
  # record or a gate transcript left over from an earlier stamp would be a
  # record of another attempt sitting beside this one under this one's name.
  #
  # THE NAME IS PRINTED, NOT THE PATH. The refusal is about the stamp, and the
  # basename is the whole of what a reader needs to allocate a fresh one; the
  # absolute path adds nothing but the account and the workspace topology.
  for TARGET in "$PKG" "$ZIP" "$RUN_LOG" "${OUTER_SIBLINGS[@]}" \
                "$SANITIZE_LOG" "$SCAN_LOG"; do
    if [ -e "$TARGET" ]; then
      echo "REFUSING: handoff target already exists: $(basename "$TARGET")" >&2
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
    echo "REFUSING: cannot allocate the invocation log: $(basename "$RUN_LOG")" >&2
    exit 1
  fi
  set +C
  export ASSEMBLE_INNER="$RUN_LOG"
  export REPO PARENT REVIEW STAMP SRC NAME LANE ATTEMPTS ATTEMPT ATTEMPT_NO
  export TOOLS
  # THE RUN ROWS SPAN BOTH STAGES. The ordinal allocation is a tool invocation
  # and it happened up here, before the fork; every other one happens below it.
  # One file, so the record is one record.
  export RUNS
  [ -z "${MEASURED+x}" ] || export MEASURED
  set +e
  bash "$0" ${1+"$@"} 2>&1 | tee -a "$RUN_LOG"
  STATUS=${PIPESTATUS[0]}
  set -e

  # ---- P11 outer sanitization ----------------------------------------------
  #
  # THE V13 CORRECTION, THREE, AND THE PLACE IT HAD TO GO. The tracked files
  # beside the package are written after the manifest and the sanitizer's walk
  # root is the package, so nothing ever passed them through it: V12 committed
  # `$WORKSPACE`, the account name and the lane anchor on twelve lines of the
  # two outer transcripts.
  #
  # THE ORDERING PROBLEM, STATED AND SOLVED. `$RUN_LOG` is held open by the
  # `tee` above and is appended to for the whole of the inner run. Sanitizing
  # it from the inner stage would rewrite bytes that `tee` is still about to
  # write past -- the repair would be undone by the tail of the same run, and a
  # scan run before the last line was written would prove nothing about the
  # file that is finally committed. So the pass runs HERE, in the outer stage,
  # after the pipeline above has exited and `$RUN_LOG`'s final byte exists.
  # Every one of `${OUTER_SIBLINGS[@]}` is a finished file at this instant.
  #
  # WHAT THAT COSTS, SAID OUT LOUD: these lines are not in the invocation log,
  # because nothing tees them there any more. The pass therefore writes its own
  # two transcripts beside the package, and its outcome is a ledger row, so the
  # record of it is machine-readable even though the narrative log ends above.
  #
  # A run that already failed is not sanitized: it is not going to be committed
  # as evidence, its markers are already written, and rewriting the transcript
  # of a failure is how a failure stops being legible.
  if [ "$STATUS" -eq 0 ]; then
    P11_START=$(date -Is)
    # THE ONE INVOCATION THAT IS NOT IN `$EXECUTED`, AND ITS DIGEST IS STILL
    # CONTEMPORANEOUS. This pass REWRITES `$EXECUTED`'s bytes, so a row added
    # to that file after the pass would ship unsanitized, and a row added
    # before it would name a digest for a run that had not happened. The
    # requirement is answered where it can be: the sha256 of the exact file
    # about to run is taken here, on the line before it runs, and carried on
    # this phase's ledger row -- which is in the lane ledger and in the
    # per-package slice beside the archive, both of which a reviewer reaches.
    P11_SHA=$(sha256sum "$TOOLS/sanitize-and-seal.py" | cut -d' ' -f1)
    set +e
    python3 "$TOOLS/sanitize-and-seal.py" --repo "$REPO" \
      --sanitize-files "${OUTER_SIBLINGS[@]}" > "$SANITIZE_LOG" 2>&1
    SANITIZED=$?
    python3 "$TOOLS/sanitize-and-seal.py" --repo "$REPO" \
      --scan-files "${OUTER_SIBLINGS[@]}" "$SANITIZE_LOG" \
      > "$SCAN_LOG" 2>&1
    SCANNED=$?
    set -e
    ORDER=$((ORDER + 1))
    attempt_row attempt="$ATTEMPT" attempt_no="$ATTEMPT_NO" record=step \
      side=package sha="${HEAD_SHA:-unknown}" cwd='$REPO' \
      phase="P11 outer sanitization" order="$ORDER" \
      tool=sanitize-and-seal.py tool_sha256="$P11_SHA" \
      command="sanitize-and-seal.py --repo REPO --sanitize-files OUTER \
then --scan-files OUTER (${#OUTER_SIBLINGS[@]} sibling(s), from the outer \
stage, after tee closed the invocation log; the tool's sha256 at execution is \
on this row because this pass rewrites the executed-tool record itself)" \
      exit="$SANITIZED/$SCANNED" result="sanitize $SANITIZED, scan $SCANNED" \
      start="$P11_START" end="$(date -Is)" \
      log="$(basename "$SANITIZE_LOG"), $(basename "$SCAN_LOG")"
    # AND INTO THE SLICE. The step row is part of the record a reviewer holding
    # this package reads; leaving it only in the lane-wide file would put P11
    # in the same position P11 exists to fix.
    #
    # IT ARRIVES AFTER THE SCAN, SO IT IS SCANNED AGAIN. Appending a line to a
    # file that has already been proved clean leaves one line nothing proved.
    # The row is symbolic by construction -- basenames, `$REPO`, digests,
    # instants, exit codes -- but "by construction" is an argument, not a
    # check, and the whole of this phase exists because a file nobody scanned
    # was committed. So the slice is rescanned, and its exit joins the other
    # two in the decision below.
    RESCANNED=0
    if [ -f "$PKG_LEDGER" ]; then
      tail -1 "$ATTEMPTS" >> "$PKG_LEDGER" || true
      set +e
      # SANITIZED, THEN SCANNED -- IN THAT ORDER. The row just appended was
      # written by `date -Is`, which prints a LOCAL offset, and the sanitizer
      # normalizes an offset instant to UTC. Scanning it without sanitizing it
      # first therefore reports the one line that was never put through the
      # pass, which is true and is the pass's own fault rather than the row's.
      # Every other line of this file went through the sanitize pass above;
      # this one arrives after it, so it gets the same two steps.
      python3 "$TOOLS/sanitize-and-seal.py" --repo "$REPO" \
        --sanitize-files "$PKG_LEDGER" >> "$SCAN_LOG" 2>&1
      python3 "$TOOLS/sanitize-and-seal.py" --repo "$REPO" \
        --scan-files "$PKG_LEDGER" >> "$SCAN_LOG" 2>&1
      RESCANNED=$?
      set -e
    fi
    if [ "$SANITIZED" -ne 0 ] || [ "$SCANNED" -ne 0 ] \
       || [ "$RESCANNED" -ne 0 ]; then
      echo "P11 FAILED: the outer siblings are not clean" >&2
      tail -20 "$SCAN_LOG" >&2 || true
      # THE ATTEMPT HAD ALREADY REACHED FINAL AUTHORITY -- P9 wrote the record
      # and P10's gates passed -- so this is a SUPERSESSION, not a discard, and
      # the marker goes beside the package where `authority-coherence.py`
      # already looks for exactly this file. The authority record is NOT
      # deleted: nothing in this lane deletes evidence. It is contradicted, in
      # the two places a reader reaches -- the sibling marker and the ledger's
      # last row for this attempt -- so the gate that passed a minute ago
      # refuses now.
      {
        echo "SUPERSEDED ATTEMPT -- NOT THE PACKAGE TO REVIEW"
        echo "state   : superseded"
        echo "attempt : $ATTEMPT"
        echo "stamp   : $STAMP"
        echo "phase   : P11 outer sanitization"
        echo "reason  : a tracked file beside this package still carries a"
        echo "          private token, or is not at the sanitizer's fixpoint;"
        echo "          sanitize $SANITIZED, scan $SCANNED, ledger rescan $RESCANNED"
        echo ""
        echo "The package directory sealed, P8 passed and P9 established final"
        echo "authority. P11 then found that a file BESIDE the package -- one"
        echo "of the transcripts and records committed alongside it -- could"
        echo "not be brought to a clean fixpoint. A package whose siblings"
        echo "disclose the workspace is not shippable evidence, so the attempt"
        echo "is superseded rather than shipped, and the correction is a fresh"
        echo "UTC stamp. Nothing was deleted, the authority record still sits"
        echo "beside the package, and this marker plus the ledger's last row"
        echo "for this attempt are what contradict it."
      } > "$REPO/build/agent-handoffs/$STAMP-$NAME.SUPERSEDED.txt" || true
      attempt_row attempt="$ATTEMPT" attempt_no="$ATTEMPT_NO" record=state \
        side=package sha="${HEAD_SHA:-unknown}" cwd='$REPO' \
        phase="P11 outer sanitization" order="$ORDER" \
        start="$P11_START" end="$(date -Is)" exit=1 result=superseded \
        status=superseded package="$STAMP-$NAME" \
        head="${HEAD_SHA:-unknown}" log="$(basename "$SCAN_LOG")" \
        reason="the outer siblings did not reach a clean sanitizer fixpoint \
(sanitize exit $SANITIZED, scan exit $SCANNED, ledger rescan exit \
$RESCANNED); a tracked file beside the package still discloses a private \
token, or would still be rewritten by the sanitizer" || true
      # AND INTO THE SLICE BESIDE THE PACKAGE. P9 derived `$PKG_LEDGER` from
      # the lane ledger before this row existed; a supersession that reached
      # only the lane-wide file is a supersession the reviewer holding this
      # package cannot see, which is the V12 defect this whole record exists to
      # answer. The row is copied, not recomposed, so the two files carry the
      # same bytes for the same fact.
      [ ! -f "$PKG_LEDGER" ] || tail -1 "$ATTEMPTS" >> "$PKG_LEDGER" || true
      STATUS=1
    else
      echo "P11: ${#OUTER_SIBLINGS[@]} outer sibling(s) sanitized and rescanned clean"
    fi
  fi

  echo "invocation log: $(basename "$RUN_LOG")"
  exit "$STATUS"
fi

# ---- from here on this is the inner, logged invocation ---------------------

# The refusal is re-asserted for every target this run is about to create.
# Only the invocation log is exempt, because the outer run created it after
# proving it absent -- the guard is not weakened, it has already fired.
for TARGET in "$PKG" "$ZIP" "${OUTER_SIBLINGS[@]}" "$SANITIZE_LOG" "$SCAN_LOG"; do
  if [ "$TARGET" = "$RUN_LOG" ]; then
    continue
  fi
  if [ -e "$TARGET" ]; then
    echo "REFUSING: handoff target already exists: $(basename "$TARGET")" >&2
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

# The two system tools, once each, at the phase that first uses them. See
# `record_external_tool` above for why they are not routed per invocation.
record_external_tool python3 "$(command -v python3)" "$PHASE"
record_external_tool git "$(command -v git)" "$PHASE"

# `started`, said once, at the instant this attempt begins doing work. The
# state machine in the header allows an attempt to go straight to its terminal
# row, but a run that dies before P5 would then leave no trace of itself in the
# ledger except its step rows, and "which attempts have ever begun" is the
# question the ordinal is allocated from.
attempt_row attempt="$ATTEMPT" attempt_no="$ATTEMPT_NO" record=state \
  side=package sha="$HEAD_SHA" cwd='$REPO' phase="$PHASE" order=0 \
  start="$STARTED" end="$STARTED" exit=0 result=started status=started \
  reason="" package="$STAMP-$NAME" head="$HEAD_SHA" \
  log="$(basename "$RUN_LOG")"

# ONE ATTEMPT, ONE DISPOSITION, ONE REASON. The first call wins; every later
# call is a no-op. The marker is written INTO the abandoned directory, which
# is the only place an inspector is guaranteed to look, and beside the archive
# as well if one had already been produced -- an archive is never rewritten in
# place, so the marker goes next to it rather than into it.
#
# AFTER THE TERMINAL ROW, A FAILURE SUPERSEDES RATHER THAN DISCARDS. The
# terminal `sealed` row is appended at P5, before P6 writes the manifest and
# before P7 and P8 run, so a failure in those phases meets an attempt that has
# already spent its one disposition. Writing a second one would put the pair
# the ledger exists to prevent -- sealed and discarded, one attempt -- into the
# record. The attempt is SUPERSEDED instead: one `record=state` row carrying
# the phase and the one reason, which is the transition the header's machine
# names, and which drops this attempt out of the authoritative count.
#
# THE V13 SHAPE OF THAT RULE. `SEALED` and `AUTHORITATIVE` are two flags
# because they are two facts. A failure between P5 and P9 supersedes an attempt
# that had SEALED and never claimed final authority -- nothing anywhere says
# `authoritative`, so there is nothing to contradict, and the marker says so.
# A failure at P10 supersedes an attempt whose authority record exists; the
# record is not deleted -- nothing here deletes evidence -- and the
# supersession row plus this marker are what contradict it. A P8 failure
# reaches neither: no authority record is written and the attempt simply stays
# non-authoritative, which is the required progression's whole point.
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
  # AND UNDER THE NAME `checks.py` ALREADY REFUSES. A half-built package whose
  # logs directory carries `DISCARDED-<attempt>.txt` cannot be staged into a
  # later package by the tool that composes checks.txt, which is the one path
  # by which this directory's bytes could otherwise be published as evidence.
  if [ -d "$PKG/logs" ] && [ ! -e "$PKG/logs/DISCARDED-$ATTEMPT.txt" ]; then
    mark_discarded "$phase" "$PKG/logs/DISCARDED-$ATTEMPT.txt"
  fi
  if [ -e "$ZIP" ] && [ ! -e "$ZIP.DISCARDED.txt" ]; then
    mark_discarded "$phase" "$ZIP.DISCARDED.txt"
  fi
  if [ -n "$SEALED" ]; then
    attempt_row attempt="$ATTEMPT" attempt_no="$ATTEMPT_NO" record=state \
      side=package sha="${HEAD_SHA:-unknown}" cwd='$REPO' phase="$phase" \
      order="$ORDER" start="${STARTED:-$when}" end="$when" exit=1 \
      result=superseded status=superseded reason="$reason" \
      package="$STAMP-$NAME" head="${HEAD_SHA:-unknown}" \
      log="$(basename "$RUN_LOG")" || true
    # If P9 had already derived the slice beside the package, the supersession
    # goes into it too. A reviewer holding this package reads that file, not
    # the lane-wide one, and V12's whole defect was deferring to records the
    # reviewer could not reach.
    [ ! -f "$PKG_LEDGER" ] || tail -1 "$ATTEMPTS" >> "$PKG_LEDGER" || true
    return 0
  fi
  attempt_row attempt="$ATTEMPT" attempt_no="$ATTEMPT_NO" record=attempt \
    side=package sha="${HEAD_SHA:-unknown}" cwd='$REPO' phase="$phase" \
    order="$ORDER" start="${STARTED:-$when}" end="$when" exit=1 \
    result=discarded status=discarded reason="$reason" \
    package="$STAMP-$NAME" head="${HEAD_SHA:-unknown}" \
    log="$(basename "$RUN_LOG")" || true
}

mark_discarded() {
  local phase=$1
  local marker=$2
  {
    if [ -n "$SEALED" ]; then
      echo "SUPERSEDED ATTEMPT -- NOT THE PACKAGE TO REVIEW"
      echo "state   : superseded"
    else
      echo "DISCARDED ATTEMPT -- NON-AUTHORITATIVE"
      echo "state   : discarded"
    fi
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
    echo "FAILED at the phase named above. It is not a handoff package. It is"
    echo "kept, unaltered apart from this marker, so the attempt can be"
    echo "inspected; it is never repaired and never reused. The correction"
    echo "for a failed assembly is a fresh UTC stamp, never a deletion."
    echo ""
    if [ -n "$AUTHORITATIVE" ]; then
      # The latest failure there is. P8 passed, P9 wrote the record, and
      # something after that refused. Saying "nothing was ever claimed" here
      # would be false.
      echo "This attempt had SEALED, had passed P8, and had established final"
      echo "authority: the record beside this package names the archive's own"
      echo "bytes. It failed afterwards, at or after the post-P8 gates. The"
      echo "record is NOT deleted -- nothing in this lane deletes evidence --"
      echo "and it is contradicted instead, in the two places a reader"
      echo "reaches: this marker, and the last row for this attempt in the"
      echo "ledger beside the handoff directory, which is a supersession"
      echo "carrying this phase and this one reason. The attempt is therefore"
      echo "no longer the authoritative package attempt of that ledger, and"
      echo "the gate that reads both refuses it."
    elif [ -n "$SEALED" ]; then
      # The honest version of the mid-late failure. The directory HAD reached
      # its terminal row -- saying "it was not sealed" here would be false, and
      # a marker that lies about which half of the pipeline ran is worse than
      # no marker at all.
      echo "This attempt had already recorded its terminal SEALED row for the"
      echo "sealed package DIRECTORY. It failed afterwards, at or after the"
      echo "manifest, so nothing about the archive or the final verification"
      echo "was ever claimed, and NO FINAL-AUTHORITY RECORD WAS EVER WRITTEN:"
      echo "under the V13 order that record is written at P9, after P8 passes,"
      echo "and this attempt did not get there. The attempt is SUPERSEDED in"
      echo "the ledger beside the handoff directory -- one state row, this"
      echo "phase, this one reason -- and is therefore not the authoritative"
      echo "package attempt of that ledger and never was."
    else
      echo "It was not sealed, its manifest is absent or does not describe it,"
      echo "and no figure, digest or claim anywhere derives from it."
      echo ""
      echo "The same disposition, with this one reason, is the terminal row"
      echo "of this attempt in the ledger beside the handoff directory."
    fi
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
       --defer logs/attempts.json
       --defer "$LOG_ROOT/derive-claims.log"
       --defer "$LOG_ROOT/head-consistency.log"
       --defer "$LOG_ROOT/seal.log" --defer "$LOG_ROOT/seal-check.log")

PHASE="P1 evidence staging"
# THE BASENAME, NOT THE PATH. The package's identity is its name; the absolute
# path adds the account, the worktrees root and the lane directory to a
# tracked line and adds nothing a reader of this log needs.
echo "== P1 evidence staging: $STAMP-$NAME at $HEAD_SHA"
mkdir -p "$PKG/logs"
( cd "$SRC" && find . -type f ! -path '*/__pycache__/*' -print0 ) \
  | ( cd "$SRC" && xargs -0 -I{} cp --parents {} "$PKG" )
chmod +x "$PKG"/logs/*.py "$PKG"/logs/*.sh 2>/dev/null || true
# THIS ATTEMPT'S LOG ROOT IS ALLOCATED, NOT ENTERED. The staged tree carries
# the batteries' roots, each under their own ordinal; a root already bearing
# THIS attempt's ordinal means the ordinal was reused, which is the one thing
# the ordinal exists to make impossible.
if [ -e "$PKG_LOG_ROOT" ]; then
  echo "REFUSING: the staged tree already carries $LOG_ROOT" >&2
  discard "$PHASE" "the staged tree already carries $LOG_ROOT; the attempt \
ordinal $LOG_PREFIX has been used before and no transcript was overwritten"
  exit 1
fi
mkdir "$PKG_LOG_ROOT"

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
GATE_LOG="$PKG_LOG_ROOT/gate-comparison.log"
# THE REPORTS ARE FOUND, NOT ASSUMED. Each battery wrote its report into ITS
# OWN attempt root, whose ordinal this script never allocated and cannot
# predict, so the two paths are discovered and the recorded command names what
# actually ran. Two roots offering the same side's report is a refusal: the
# staged tree would carry two batteries claiming to be the same side, and
# picking one silently is how a comparison comes to describe the wrong run.
gate_report() {  # side -> package-relative report path, or nothing
  local side=$1 one found=""
  for one in "$PKG"/logs/attempt-*/browser-gate-"$side".json; do
    if [ -f "$one" ]; then
      if [ -n "$found" ]; then
        echo "REFUSING: two attempt roots carry a browser-gate-$side.json" >&2
        return 1
      fi
      found="${one#"$PKG"/}"
    fi
  done
  printf '%s' "$found"
}
GATE_PARENT=$(gate_report parent)
GATE_HEAD=$(gate_report head)
GATE_CMD="python3 logs/compare-gate.py ${GATE_PARENT:-(absent)} ${GATE_HEAD:-(absent)}"
GATE_START=$(date -Is)
if [ -e "$GATE_LOG" ]; then
  echo "REFUSING: a gate-comparison log was staged into the package:" \
       "$LOG_ROOT/gate-comparison.log" >&2
  discard "$PHASE" "$LOG_ROOT/gate-comparison.log was already present in the \
staged tree; this pipeline's own comparison is the one this attempt records \
and a transcript is never overwritten"
  exit 1
fi
if [ -n "$GATE_PARENT" ] && [ -n "$GATE_HEAD" ]; then
  set +e
  # V13: THROUGH `run_tool`, LIKE EVERY OTHER TOOL. The comparison runs the
  # package's own copy, from inside the package, exactly as before -- what is
  # new is that the digest of the bytes that ran is recorded on the line before
  # they run. `eval` is gone with it: the command is now spelled once, as
  # arguments, so the string in the ledger and the argv handed to the
  # interpreter cannot differ.
  ( cd "$PKG" && run_tool compare-gate.py "$PKG/logs/compare-gate.py" \
      "$PHASE" "$LOG_ROOT/gate-comparison.log" \
      -- python3 logs/compare-gate.py "$GATE_PARENT" "$GATE_HEAD" \
  ) > "$GATE_LOG" 2>&1
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
  "$LOG_ROOT/gate-comparison.log"

PHASE="P1 checks.txt, the log index and the packaged attempt rows"
echo "== P1 composing checks.txt from the batteries' own ledgers"
# THE STEP THAT COMPOSES THE STEP LIST HAD NO STEP ROW. V12 ran this
# invocation and recorded nothing for it, so the one command that reads every
# other command's record was itself outside the record. It has a row now, like
# everything else, and the row is appended AFTER the composition -- which is
# also the exact reason `checks.txt` cannot contain it. See the epilogue note
# at P5.
#
# The SOURCE copy runs, not the staged one: importing the package's own copy
# writes bytecode into a tree that is about to be frozen. The digest recorded
# is of the bytes that ran, and the shipped copy is the same bytes -- if they
# ever diverge, `emit_executed_tools` refuses, because two digests for one
# logical tool is exactly the ambiguity this record exists to remove.
COMPOSE_START=$(date -Is)
run_tool checks.py "$SRC/logs/checks.py" "$PHASE" \
  "(this step writes checks.txt and logs/LOG-INDEX.md, not a transcript; the \
invocation log is the transcript)" \
  -- python3 "$SRC/logs/checks.py" --package "$PKG" --head "$HEAD_SHA" \
  --parent "$PARENT" --attempts "$ATTEMPTS" --attempt "$ATTEMPT" \
  --attempt-no "$ATTEMPT_NO" ${MEASURED:+--measured "$MEASURED"}
step_row "$PHASE" "logs/checks.py --package PKG --head HEAD --parent PARENT \
--attempts LEDGER --attempt ATTEMPT --attempt-no $ATTEMPT_NO" 0 \
  "$COMPOSE_START" "$(date -Is)" \
  "(this step writes checks.txt and logs/LOG-INDEX.md, not a transcript; the \
invocation log is the transcript)"

PHASE="P1 the sealer's own tests"
echo "== P1 the sealer's own tests"
TESTS_START=$(date -Is)
set +e
run_tool test-sanitize-and-seal.py "$PKG/logs/test-sanitize-and-seal.py" \
  "$PHASE" "$LOG_ROOT/sealer-tests.log" \
  -- python3 "$PKG/logs/test-sanitize-and-seal.py" \
  > "$PKG_LOG_ROOT/sealer-tests.log" 2>&1
TESTS=$?
set -e
echo "EXIT=$TESTS" >> "$PKG_LOG_ROOT/sealer-tests.log"
# Running them inside the package leaves bytecode behind, and a build artifact
# is not evidence.
rm -rf "$PKG/logs/__pycache__"
tail -3 "$PKG_LOG_ROOT/sealer-tests.log"
step_row "$PHASE" "python3 logs/test-sanitize-and-seal.py" "$TESTS" \
  "$TESTS_START" "$(date -Is)" "$LOG_ROOT/sealer-tests.log"
[ "$TESTS" -eq 0 ] || {
  echo "SEALER TESTS FAILED"
  discard "$PHASE" "the sealer's own test suite failed with exit $TESTS; a \
package sealed by an unproven sealer is not evidence of privacy"
  exit 1
}

PHASE="P2 normalize to a fixpoint"
echo "== P2 normalize to a fixpoint (no manifest is written here)"
# Each pass appends its transcript to this attempt's seal.log, then a
# check-only pass
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
  ( cd "$REPO" && run_tool sanitize-and-seal.py \
      "$PKG/logs/sanitize-and-seal.py" "$PHASE (normalize pass $PASS)" \
      "$LOG_ROOT/seal.log" \
      -- python3 "$PKG/logs/sanitize-and-seal.py" "$PKG" --repo "$REPO" \
      --normalize-only "${DEFER[@]}" ) > "$WORK/seal-pass" 2>&1
  SEAL=$?
  set -e
  echo "EXIT=$SEAL" >> "$WORK/seal-pass"
  { echo "== normalize pass $PASS"; cat "$WORK/seal-pass"; } \
    >> "$PKG_LOG_ROOT/seal.log"
  [ "$SEAL" -eq 0 ] || {
    cat "$WORK/seal-pass"
    echo "P2 FAILED"
    discard "$PHASE" "normalize pass $PASS failed with exit $SEAL"
    exit 1
  }
  set +e
  ( cd "$REPO" && run_tool sanitize-and-seal.py \
      "$PKG/logs/sanitize-and-seal.py" "$PHASE (check pass $PASS)" \
      "$LOG_ROOT/seal-check.log" \
      -- python3 "$PKG/logs/sanitize-and-seal.py" "$PKG" --repo "$REPO" \
      --check-only "${DEFER[@]}" ) > "$WORK/check-pass" 2>&1
  CHECK=$?
  set -e
  echo "EXIT=$CHECK" >> "$WORK/check-pass"
  if [ "$CHECK" -eq 0 ] \
     && cmp -s "$WORK/check-pass" "$PKG_LOG_ROOT/seal-check.log" 2>/dev/null; then
    echo "   fixpoint reached at pass $PASS"
    break
  fi
  cp "$WORK/check-pass" "$PKG_LOG_ROOT/seal-check.log"
  if [ "$CHECK" -ne 0 ] && [ "$PASS" -ge 3 ]; then
    cat "$WORK/check-pass"
    echo "P2 FAILED: check-only still failing"
    discard "$PHASE" "the check-only pass was still failing at pass $PASS \
with exit $CHECK"
    exit 1
  fi
done
step_row "$PHASE" "logs/sanitize-and-seal.py PKG --repo REPO --normalize-only, to a fixpoint \
($PASS pass(es))" 0 "$P2_START" "$(date -Is)" "$LOG_ROOT/seal.log"
# TWO TRANSCRIPTS, TWO ROWS. V11 recorded one row for this phase and named
# only seal.log on it, so seal-check.log -- the transcript that actually closes
# the fixpoint -- was a member of the package no ledger row claimed. The
# attempt-log audit below refuses exactly that, and it is right to: an
# unclaimed transcript is a transcript no attempt is answerable for.
step_row "$PHASE" "logs/sanitize-and-seal.py PKG --repo REPO --check-only, the pass that \
closed the fixpoint" 0 "$P2_START" "$(date -Is)" "$LOG_ROOT/seal-check.log"

PHASE="P3 the freeze"
echo "== P3 THE FREEZE: the snapshot that IS the inventory"
P3_START=$(date -Is)
run_tool derive-claims.py "$PKG/logs/derive-claims.py" "$PHASE" \
  "(the freeze is taken outside the package; the invocation log is the \
transcript)" \
  -- python3 "$PKG/logs/derive-claims.py" --package "$PKG" \
  --write-freeze "$WORK/freeze.json"
step_row "$PHASE" "logs/derive-claims.py --package PKG --write-freeze \
FREEZE (outside the package)" 0 "$P3_START" "$(date -Is)" \
  "(the freeze is taken outside the package; the invocation log is the \
transcript)"

PHASE="P4 derive once"
echo "== P4 derive once, from the freeze, pre-normalized"
P4_START=$(date -Is)
( cd "$REPO" && run_tool derive-claims.py "$PKG/logs/derive-claims.py" \
    "$PHASE" "$LOG_ROOT/derive-claims.log" \
    -- python3 "$PKG/logs/derive-claims.py" --repo "$REPO" \
    --parent "$PARENT" --head "$HEAD_SHA" --review "$REVIEW" \
    --package "$PKG" --freeze "$WORK/freeze.json" --lane "$LANE" \
    --attempt-no "$ATTEMPT_NO" \
    --out "$PKG/claims.json" ) | tee "$PKG_LOG_ROOT/derive-claims.log"
step_row "$PHASE" "logs/derive-claims.py --repo REPO --parent PARENT --head \
HEAD --review REVIEW --package PKG --freeze FREEZE --lane $LANE --attempt-no \
$ATTEMPT_NO --out claims.json" 0 "$P4_START" "$(date -Is)" \
  "$LOG_ROOT/derive-claims.log"

PHASE="P5 consistency audit"
echo "== P5 consistency audit: undeclared drift is a hard failure"
P5_START=$(date -Is)
set +e
run_tool head-consistency.py "$PKG/logs/head-consistency.py" "$PHASE" \
  "$LOG_ROOT/head-consistency.log" \
  -- python3 "$PKG/logs/head-consistency.py" --package "$PKG" \
  --pending MANIFEST.sha256 --pending logs/attempts.json \
  > "$PKG_LOG_ROOT/head-consistency.log" 2>&1
CONSISTENT=$?
set -e
echo "EXIT=$CONSISTENT" >> "$PKG_LOG_ROOT/head-consistency.log"
cat "$PKG_LOG_ROOT/head-consistency.log"
step_row "$PHASE" "logs/head-consistency.py --package PKG --pending \
MANIFEST.sha256 --pending logs/attempts.json" "$CONSISTENT" "$P5_START" \
  "$(date -Is)" "$LOG_ROOT/head-consistency.log"
[ "$CONSISTENT" -eq 0 ] || {
  echo "HEAD CONSISTENCY FAILED"
  discard "$PHASE" "the consistency audit failed with exit $CONSISTENT; a \
member disagreed with the frozen inventory or with the claims derived from it"
  exit 1
}

PHASE="P5 attempt-log audit"
echo "== P5 attempt-log audit: every transcript under the attempt that wrote it"
# THE RULE THE V11 PACKAGE BROKE, ENFORCED. Six attempts claimed one
# gate-comparison log there and five claimed one sealer-tests log, and nothing
# in the pipeline could see it, because no phase ever compared the ledger's
# `log=` values against the transcripts on disk. This does, both ways: a row
# whose log escapes its own attempt root, two rows claiming one path, an empty
# transcript nobody explained, and a transcript no row claims are each a
# refusal. It writes NOTHING into the package -- the invocation log is its
# transcript -- so it can run after the freeze without becoming residue.
LOGAUDIT_START=$(date -Is)
set +e
run_tool checks.py "$PKG/logs/checks.py" "$PHASE" \
  "(the audit writes no member; the invocation log is the transcript)" \
  -- python3 "$PKG/logs/checks.py" --audit-logs --package "$PKG" \
  --attempts "$ATTEMPTS" --attempt "$ATTEMPT" --attempt-no "$ATTEMPT_NO"
LOGAUDIT=$?
set -e
step_row "$PHASE" "logs/checks.py --audit-logs --package PKG --attempts \
LEDGER --attempt ATTEMPT --attempt-no $ATTEMPT_NO" "$LOGAUDIT" \
  "$LOGAUDIT_START" "$(date -Is)" \
  "(the audit writes no member; the invocation log is the transcript)"
[ "$LOGAUDIT" -eq 0 ] || {
  echo "ATTEMPT-LOG AUDIT FAILED"
  discard "$PHASE" "the attempt-log audit failed with exit $LOGAUDIT; a \
transcript in this package is not accounted for by exactly one row of exactly \
one attempt, which is the defect that let one attempt overwrite another's logs"
  exit 1
}

PHASE="P5 the sealed row and the shipped ledger"
echo "== P5 the SEALED terminal row, then the ledger member, then nothing"
# THE LAST WRITE INSIDE THE PACKAGE, AND THE REASON IT IS HERE. V11 wrote
# logs/attempts.json at P1 and this attempt's terminal row at the end of P8, so
# the shipped ledger described the package it shipped in as unresolved and
# every earlier package attempt as authoritative. The order is inverted now:
# the terminal row is appended FIRST, then the member is composed from a ledger
# that already contains it, and both happen after the consistency audit and
# before the manifest, which is as late as the freeze line allows.
#
# AND THE ROW SAYS `sealed`, NOT `authoritative`. THIS IS THE V13 CORRECTION,
# ONE, at the one line where it bites. V12 wrote `status=authoritative` here
# and `checks.py --seal-ledger` froze it into the shipped member, so the
# package bytes and the archive built from them carried a claim of FINAL
# authority made before the manifest existed, before the ZIP existed and
# before P8 had a verdict. No sealed package byte may claim final authority
# before P8; `sealed` is the most this row is entitled to, and it is exactly
# true: the package DIRECTORY is complete and about to be manifested.
#
# What is claimed here, precisely: the directory is sealed. NOT the archive --
# the sidecar carries its identity. NOT the P8 verdict -- the outer transcript
# carries that. NOT final authority -- the P9 record carries that, and only
# after P8 has passed over the archive's own bytes. If P6, P7 or P8 fails,
# `discard` supersedes this attempt and marks the directory, and no authority
# record is ever written, so the claim cannot outlive the run that made it and
# there is no later claim to retract.
LEDGER_START=$(date -Is)
SEALED=yes
attempt_row attempt="$ATTEMPT" attempt_no="$ATTEMPT_NO" record=attempt \
  side=package sha="$HEAD_SHA" cwd='$REPO' phase="$PHASE" order="$ORDER" \
  start="$STARTED" end="$(date -Is)" exit=0 \
  result="sealed $STAMP-$NAME" status=sealed reason="" \
  package="$STAMP-$NAME" head="$HEAD_SHA" log="$(basename "$RUN_LOG")"
set +e
run_tool checks.py "$PKG/logs/checks.py" "$PHASE" \
  "(this step writes the member logs/attempts.json, not a transcript; the \
invocation log is the transcript)" \
  -- python3 "$PKG/logs/checks.py" --seal-ledger --package "$PKG" \
  --attempts "$ATTEMPTS" --attempt "$ATTEMPT" --attempt-no "$ATTEMPT_NO" \
  --package-name "$STAMP-$NAME" --head "$HEAD_SHA" --lane "$LANE"
LEDGER_WRITE=$?
set -e
step_row "$PHASE" "logs/checks.py --seal-ledger --package PKG --attempts \
LEDGER --attempt ATTEMPT --attempt-no $ATTEMPT_NO --package-name $STAMP-$NAME \
--head HEAD --lane $LANE" "$LEDGER_WRITE" "$LEDGER_START" "$(date -Is)" \
  "(this step writes the member logs/attempts.json, not a transcript; the \
invocation log is the transcript)"
[ "$LEDGER_WRITE" -eq 0 ] || {
  echo "LEDGER AUDIT FAILED"
  discard "$PHASE" "the ledger audit failed with exit $LEDGER_WRITE; the \
attempt ledger does not resolve this attempt to sealed with a legal state \
history, or another attempt still holds a disposition that leaves this one \
unable to say which package it is"
  exit 1
}

PHASE="P6 manifest"
echo "== P6 manifest: prove the freeze held, then write the seal once"
P6_START=$(date -Is)
( cd "$REPO" && run_tool sanitize-and-seal.py \
    "$PKG/logs/sanitize-and-seal.py" "$PHASE" "MANIFEST.sha256" \
    -- python3 "$PKG/logs/sanitize-and-seal.py" "$PKG" --repo "$REPO" \
    --manifest-only --claims "$PKG/claims.json" )
step_row "$PHASE" "logs/sanitize-and-seal.py PKG --repo REPO --manifest-only --claims \
claims.json" 0 "$P6_START" "$(date -Is)" "MANIFEST.sha256"
# Nothing writes inside $PKG below this line. The single exception is the
# discard marker -- at the package root and, under the name checks.py already
# refuses, in logs/ -- which is written only when this attempt has already
# failed and is therefore not a package at all.

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

# THE SEAL VERIFICATION V12 SHIPPED AND NEVER RAN. `sanitize-and-seal.py
# --verify` has been implemented since V8: it recomputes every digest in
# MANIFEST.sha256 against the tree and cross-proves the sibling ZIP against
# the sidecar. Nothing in the pipeline invoked it, so the one mode that can
# catch "the manifest and the tree disagree" between the seal and the archive
# was dead code beside the package it was written to check. It runs here,
# after the archive and its sidecar exist, so both halves of what it proves
# are present. It writes nothing.
P7V_START=$(date -Is)
set +e
run_tool sanitize-and-seal.py "$PKG/logs/sanitize-and-seal.py" \
  "$PHASE (seal verification)" \
  "(--verify writes nothing; the invocation log is the transcript)" \
  -- python3 "$PKG/logs/sanitize-and-seal.py" "$PKG" --repo "$REPO" --verify
SEALVERIFY=$?
set -e
step_row "$PHASE" "logs/sanitize-and-seal.py PKG --repo REPO --verify (recompute every \
manifest digest, and cross-prove the sibling archive against its sidecar)" \
  "$SEALVERIFY" "$P7V_START" "$(date -Is)" \
  "(--verify writes nothing; the invocation log is the transcript)"
[ "$SEALVERIFY" -eq 0 ] || {
  echo "SEAL VERIFICATION FAILED"
  discard "$PHASE" "logs/sanitize-and-seal.py --verify failed with exit \
$SEALVERIFY; a manifest digest does not describe the member beside it, or the \
archive does not match the sidecar written from it"
  exit 1
}

PHASE="P8 final verification"
echo "== P8 final verification, from the ZIP alone, read-only"
# SYMBOLICALLY, NOT ABSOLUTELY. This line and the verifier's own `verifier`
# and `tools` lines were eleven of the twelve leaking lines the review found
# in V12's tracked transcripts. The anchor's IDENTITY is what a reader needs;
# its absolute path is the account name and the workspace topology. What runs
# is still `$TOOLS`; what is printed is the symbol P11 would have rewritten it
# to anyway.
echo "   trust anchor: $EVIDENCE (out-of-package, lane $LANE)"
# The transcript lands OUTSIDE the package, beside the archive: a file created
# after the seal is not in the manifest that seal produced.
#
# The verifier RUN is the trusted copy, not the staged one, and --tools names
# the same directory explicitly rather than letting the anchor fall out of
# wherever the verifier happened to be invoked from. Neither path is inside
# the package, so nothing here executes a byte the archive carries; the
# verifier hashes the archive's own copy of each tool against the trusted one
# and fails on divergence.
#
# V13: AND IT IS HANDED WHAT ACTUALLY RAN. `--executed` is the contemporaneous
# record every phase above has been appending to; the verifier compares the
# digest each tool carried AT EXECUTION against the archive's shipped copy,
# which is the executed-vs-shipped proposition V12's P8-only hashing could not
# state. `--table-out` puts its own table beside the package as data rather
# than only as prose in the transcript.
P8_START=$(date -Is)
set +e
emit_executed_tools "$PHASE"
EMITTED=$?
set -e
step_row "$PHASE" "render $(basename "$EXECUTED") from the run rows every \
phase above appended immediately before its own invocation, plus a row for \
every tool the package ships that this attempt did not execute" "$EMITTED" \
  "$P8_START" "$(date -Is)" "$(basename "$EXECUTED")"
[ "$EMITTED" -eq 0 ] || {
  echo "EXECUTED-TOOL RECORD REFUSED"
  discard "$PHASE" "the executed-tool record could not be rendered with exit \
$EMITTED; one logical tool was executed as two different sets of bytes, so \
the record cannot say which copy any claim in this package is about"
  exit 1
}
set +e
run_tool verify-final-package.py "$TOOLS/verify-final-package.py" "$PHASE" \
  "$(basename "$VERIFY_LOG")" \
  -- python3 "$TOOLS/verify-final-package.py" \
  --zip "$ZIP" \
  --sidecar "$ZIP.sha256" \
  --name "$STAMP-$NAME" \
  --tools "$TOOLS" \
  --executed "$EXECUTED" \
  --table-out "$TOOL_BYTES" \
  | tee "$VERIFY_LOG"
VERIFIED=${PIPESTATUS[0]}
set -e
step_row "$PHASE" "verify-final-package.py --zip ZIP --sidecar SIDECAR \
--name $STAMP-$NAME --tools TOOLS --executed EXECUTED --table-out TABLE (both \
the verifier and the trusted tools taken from the out-of-package anchor, never \
from the archive)" "$VERIFIED" "$P8_START" "$(date -Is)" \
  "$(basename "$VERIFY_LOG")"
[ "$VERIFIED" -eq 0 ] || {
  echo "P8 FINAL VERIFICATION FAILED"
  # AND THE ATTEMPT STAYS NON-AUTHORITATIVE. This is the path the whole V13
  # reordering exists for. No authority record is written, the external
  # `authoritative` row is never appended, and the only thing on disk about
  # this attempt's standing is the `sealed` row -- which is true, and which
  # says nothing about a verification that did not pass. Nothing has to be
  # retracted because nothing was claimed.
  discard "$PHASE" "the final verification failed with exit $VERIFIED; the \
archive does not answer for the claims the package makes about itself, so no \
final-authority record was written and this attempt is not authoritative"
  exit 1
}

PHASE="P9 final authority"
# THE BANNER DOES NOT SAY THE WORDS. `authority-coherence.py` scans this log
# for lines claiming authority and binds each to the nearest attempt id, and
# a banner carrying the phrase with no id on it puts a dangling claim into the
# record for the next id to answer. The claim is made ONCE, below, on a line
# that names the attempt AND the package it is authoritative for.
echo "== P9: the archive's own bytes, the P8 verdict, and the record they bind"
# THE REQUIRED PROGRESSION'S LAST STEP, AND NOT ONE INSTANT EARLIER.
#
#     attempt started -> package sealed -> P7/P8 verification
#                     -> post-P8 ZIP size/hash confirmed
#                     -> FINAL AUTHORITY ESTABLISHED
#
# Everything before this line has claimed at most `sealed`. This phase is the
# only place in the toolchain that establishes final authority, and it does it
# with one record whose every field is RECOMPUTED or READ BACK:
#
#   * the ZIP's size and sha256 come from the archive on disk, hashed here.
#     They are NOT carried forward from P7. A value carried forward proves the
#     variable, not the file, and the whole point of a post-verification rehash
#     is that the bytes were read again after everything else had finished;
#   * `p8_result` and `rehash_result` are parsed out of the P8 transcript's own
#     verdict and post-verification rehash lines, and this refuses if either
#     disagrees with the recompute. A record carrying a verdict that did not
#     exist until P8 completed cannot have been written before P8;
#   * the binding runs ONE WAY. The record names the archive's digest; the
#     archive names nothing about the record, and this refuses if the archive
#     carries any `*.authority.json` member. A mutual binding is
#     unconstructible, and a record the archive vouched for is a record the
#     archive could have been sealed around.
#
# The schema is owned by `authority-coherence.py`, which is the gate that reads
# it at P10; it is not restated here, it is written to.
P9_START=$(date -Is)
set +e
python3 - "$ZIP" "$VERIFY_LOG" "$AUTHORITY" "$ATTEMPT" "$STAMP-$NAME" \
    "$HEAD_SHA" <<'PY'
import datetime, hashlib, json, pathlib, re, sys, zipfile

zip_path, verify_log, out, attempt, package, head = sys.argv[1:7]
archive = pathlib.Path(zip_path)

# RECOMPUTED HERE, FROM THE ARCHIVE. Not read from the sidecar, not inherited
# from P7's variables.
hashed = hashlib.sha256()
with archive.open("rb") as handle:
    for block in iter(lambda: handle.read(1 << 20), b""):
        hashed.update(block)
zip_sha = hashed.hexdigest()
zip_bytes = archive.stat().st_size

problems = []

# THE ONE-WAY BINDING, ASSERTED FROM THIS SIDE TOO. The gate refuses an archive
# carrying the record; so does the phase that writes it, because discovering it
# here costs nothing and discovering it at the gate costs a stamp.
with zipfile.ZipFile(archive) as handle:
    for member in handle.namelist():
        if member.rsplit("/", 1)[-1].endswith(".authority.json"):
            problems.append(f"the archive carries {member!r}; the final "
                            f"authority record may not live inside the "
                            f"archive it binds")

said = pathlib.Path(verify_log).read_text(encoding="utf-8", errors="replace")
verdict = re.search(r"^P8 verification:\s*(PASS|FAIL)\b", said, re.MULTILINE)
p8_result = verdict.group(1) if verdict else ""

# The rehash block, read from the label onward so a `result:` line belonging to
# some earlier check cannot be mistaken for the one that closes the file.
rehash_result = ""
post_bytes = None
post_sha = ""
lines = said.splitlines()
start = 0
for number, line in enumerate(lines):
    if "post-verification rehash" in line.lower():
        start = number
        break
for line in lines[start:]:
    got = re.search(r"post-check bytes\s*:\s*(\d+)", line)
    if got:
        post_bytes = int(got.group(1))
    got = re.search(r"post-check sha256\s*:\s*([0-9a-fA-F]{64})", line)
    if got:
        post_sha = got.group(1).lower()
    got = re.search(r"^\s*result\s*:\s*(UNCHANGED|CHANGED)\b", line)
    if got:
        rehash_result = got.group(1)

if p8_result != "PASS":
    problems.append(f"the P8 transcript's verdict is "
                    f"{p8_result or '(unstated)'}, not PASS; if P8 fails the "
                    f"attempt remains non-authoritative")
if rehash_result != "UNCHANGED":
    problems.append(f"the P8 transcript's post-verification rehash is "
                    f"{rehash_result or '(unstated)'}, not UNCHANGED")
if post_sha and post_sha != zip_sha:
    problems.append(f"the P8 transcript rehashed {post_sha}, the archive's "
                    f"bytes hash to {zip_sha} now")
if post_bytes is not None and post_bytes != zip_bytes:
    problems.append(f"the P8 transcript rehashed {post_bytes} bytes, the "
                    f"archive is {zip_bytes} bytes now")

if problems:
    for one in problems:
        print(f"REFUSING: {one}", file=sys.stderr)
    raise SystemExit(1)

# `established` is stamped in UTC with an explicit designator, because an
# instant without an offset is a local wall clock and this record's whole job
# is to be checkable by somebody else.
established = (datetime.datetime.now(datetime.timezone.utc)
               .replace(microsecond=0).isoformat().replace("+00:00", "Z"))
record = {
    "schema": "catena-final-authority/1",
    "attempt": attempt,
    "package": package,
    "head": head,
    "zip_name": archive.name,
    "zip_bytes": zip_bytes,
    "zip_sha256": zip_sha,
    "p8_log": pathlib.Path(verify_log).name,
    "p8_result": p8_result,
    "rehash_result": rehash_result,
    "rehash_bytes": zip_bytes,
    "rehash_sha256": zip_sha,
    "status": "authoritative",
    "established": established,
}
pathlib.Path(out).write_text(
    json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(f"authority record: {archive.name} is {zip_bytes} bytes, {zip_sha}")
print(f"                 P8 {p8_result}, rehash {rehash_result}, "
      f"established {established}")
PY
AUTHORITY_WRITTEN=$?
set -e
step_row "$PHASE" "recompute the archive's size and sha256 from its own bytes, \
read back the P8 verdict and post-verification rehash, and write \
$(basename "$AUTHORITY")" "$AUTHORITY_WRITTEN" "$P9_START" "$(date -Is)" \
  "$(basename "$RUN_LOG")"
[ "$AUTHORITY_WRITTEN" -eq 0 ] || {
  # Worded without the trigger phrase on purpose: a reviewer running the
  # coherence gate over this failed attempt with --pre-p8 asks whether any
  # record claims final authority, and a REFUSAL that spells the phrase
  # would answer yes.
  echo "THE AUTHORITY RECORD WAS REFUSED"
  discard "$PHASE" "the final-authority record could not be written with \
exit $AUTHORITY_WRITTEN; the archive's bytes, the P8 verdict and the post-P8 \
rehash do not agree, so nothing establishes final authority and this attempt \
is not authoritative"
  exit 1
}

# THE EXTERNAL ROW, AND WHY IT IS `record=state`. `sealed` is this attempt's
# one disposition and it is already written; `authoritative` is POST-terminal,
# exactly as `superseded` is, so it arrives on a state row that does not
# overwrite the disposition it follows. It lives OUTSIDE the package by
# construction -- the manifest was taken at P6 and nothing writes inside the
# directory after it -- which is also why the record beside the archive, and
# not any member, is what establishes authority.
AUTHORITATIVE=yes
attempt_row attempt="$ATTEMPT" attempt_no="$ATTEMPT_NO" record=state \
  side=package sha="$HEAD_SHA" cwd='$REPO' phase="$PHASE" order="$ORDER" \
  start="$STARTED" end="$(date -Is)" exit=0 \
  result="authoritative $STAMP-$NAME" status=authoritative reason="" \
  package="$STAMP-$NAME" head="$HEAD_SHA" log="$(basename "$AUTHORITY")"

# THE COMPLETE LEDGER A REVIEWER CAN REACH, BESIDE THE PACKAGE.
#
# V12's `$ATTEMPTS` was a lane-wide file under build/agent-handoffs that was
# neither beside the package, nor tracked, nor shipped -- so the package's own
# records deferred, for every attempt they mentioned, to rows no reviewer could
# open. THE CHOICE MADE HERE, AND WHY: the lane ledger STAYS the append-only
# superset and stays the value of `$ATTEMPTS`, because it is the allocator
# `checks.py --allocate-ordinal` spends ordinals out of and a per-package
# ledger would reissue them -- which is precisely how V12 came to have two
# attempts numbered 03, 04 and 05. So the per-package file is DERIVED: every
# row of the lane ledger belonging to an attempt this package's own
# `logs/attempts.json` mentions, copied in the order the lane ledger recorded
# them, plus the lane declaration row. Copy, not point: one allocator, and a
# complete slice beside the artifact.
LEDGERCOPY_START=$(date -Is)
set +e
python3 - "$ATTEMPTS" "$PKG/logs/attempts.json" "$PKG_LEDGER" "$ATTEMPT" \
    <<'PY'
import json, pathlib, sys

lane_path, member_path, out, attempt = sys.argv[1:5]
wanted = {attempt}
member = json.loads(pathlib.Path(member_path).read_text(encoding="utf-8"))
for row in member.get("rows", []):
    one = str(row.get("attempt", ""))
    if one:
        wanted.add(one)
for one in member.get("attempts", []):
    named = str(one.get("attempt", ""))
    if named:
        wanted.add(named)

kept = []
seen = set()
for line in pathlib.Path(lane_path).read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue
    try:
        row = json.loads(line)
    except json.JSONDecodeError:
        # A row the lane ledger cannot parse is not silently dropped from the
        # slice: dropping it would make the slice look cleaner than the record
        # it is taken from.
        kept.append(line)
        continue
    if row.get("record") == "lane":
        kept.append(line)
        continue
    one = str(row.get("attempt", ""))
    if one in wanted:
        kept.append(line)
        seen.add(one)

missing = sorted(wanted - seen)
if missing:
    print("REFUSING: the package mentions attempts the lane ledger has no "
          "rows for: " + ", ".join(missing), file=sys.stderr)
    raise SystemExit(1)

pathlib.Path(out).write_text("\n".join(kept) + "\n", encoding="utf-8")
print(f"per-package ledger: {len(kept)} row(s) for {len(seen)} attempt(s), "
      f"copied from the lane ledger in its own order")
PY
LEDGER_COPY=$?
set -e
step_row "$PHASE" "derive the per-package append-only ledger beside the \
archive by copying every lane-ledger row for an attempt this package mentions \
(the lane ledger remains the append-only superset and the ordinal allocator)" \
  "$LEDGER_COPY" "$LEDGERCOPY_START" "$(date -Is)" \
  "$(basename "$PKG_LEDGER")"
[ "$LEDGER_COPY" -eq 0 ] || {
  echo "PER-PACKAGE LEDGER REFUSED"
  discard "$PHASE" "the per-package ledger could not be derived with exit \
$LEDGER_COPY; the package mentions an attempt the lane ledger carries no rows \
for, so the record beside the archive would be incomplete"
  exit 1
}
# The row appended a moment ago goes into the slice as well: it was written
# after the member was frozen at P5, so the filter above -- which reads that
# member -- keeps it only because the sealing attempt is in `wanted` by name.
# Stated because it is the one row whose presence is not obvious.

echo ""
echo "== FINAL AUTHORITY: attempt $ATTEMPT is the authoritative package \
attempt for $STAMP-$NAME"
echo "   established after P8 passed, bound to the archive's own bytes by"
echo "   $(basename "$AUTHORITY"); the shipped logs/attempts.json says"
echo "   sealed, which is all a member written before P8 may say."
echo ""

PHASE="P10 the post-seal gates"
echo "== P10 the gates V12 ran by hand, run here"
# WHY THIS PHASE EXISTS. `authority-coherence.py` and `handoff-inventory.py`
# both shipped in V12 and this pipeline invoked neither. They were run by hand,
# afterwards, and what they found is why two V12 attempts had to be superseded
# AFTER sealing -- which is the most expensive way to learn anything, because
# by then the stamp is spent. They run automatically, here, after the authority
# record exists (both read it), routed through `run_tool` like everything else,
# each to its own outer transcript, and either one refusing fails the run.
#
# THE INVOCATION LOG IS FLUSHED FIRST. `authority-coherence.py` reads
# `$RUN_LOG` and requires it to name this attempt on a line that claims
# authority -- the block echoed just above. That line reaches the file through
# the `tee` this script runs under, so the gate is not started until the write
# has had a moment to land; this is not a timing assumption about correctness,
# it is a refusal to race a gate against its own input.
sync || true
sleep 1

COHERENCE_START=$(date -Is)
set +e
run_tool authority-coherence.py "$TOOLS/authority-coherence.py" "$PHASE" \
  "$(basename "$COHERENCE_LOG")" \
  -- python3 "$TOOLS/authority-coherence.py" --package "$PKG" \
  --head "$HEAD_SHA" --name "$STAMP-$NAME" --outer "$RUN_LOG" \
  --zip "$ZIP" --sidecar "$ZIP.sha256" --verify-log "$VERIFY_LOG" \
  --authority "$AUTHORITY" --ledger "$PKG_LEDGER" \
  > "$COHERENCE_LOG" 2>&1
COHERENCE=$?
set -e
# THE TAIL IS NOT ECHOED. The gate's own success line contains the word this
# script's log is scanned for, and a summary line copied out of it would put a
# second authority claim into the transcript under whatever attempt id happened
# to be nearest. The exit and the transcript's name are the report.
echo "   authority coherence: exit $COHERENCE ($(basename "$COHERENCE_LOG"))"
step_row "$PHASE" "authority-coherence.py --package PKG --head HEAD --name \
$STAMP-$NAME --outer OUTER --zip ZIP --sidecar SIDECAR --verify-log VERIFY \
--authority AUTHORITY --ledger LEDGER" "$COHERENCE" "$COHERENCE_START" \
  "$(date -Is)" "$(basename "$COHERENCE_LOG")"
[ "$COHERENCE" -eq 0 ] || {
  echo "AUTHORITY COHERENCE FAILED"
  tail -20 "$COHERENCE_LOG" >&2 || true
  discard "$PHASE" "the authority-coherence gate refused with exit \
$COHERENCE; the records beside this package do not agree on which attempt is \
authoritative, or the record does not bind the archive's own bytes"
  exit 1
}

INVENTORY_START=$(date -Is)
set +e
run_tool handoff-inventory.py "$TOOLS/handoff-inventory.py" "$PHASE" \
  "$(basename "$INVENTORY_LOG")" \
  -- python3 "$TOOLS/handoff-inventory.py" --package "$PKG" \
  > "$INVENTORY_LOG" 2>&1
INVENTORY=$?
set -e
echo "   handoff inventory : exit $INVENTORY ($(basename "$INVENTORY_LOG"))"
step_row "$PHASE" "handoff-inventory.py --package PKG" "$INVENTORY" \
  "$INVENTORY_START" "$(date -Is)" "$(basename "$INVENTORY_LOG")"
# TWO EXITS, TWO MEANINGS, AND THEY ARE NOT THE SAME FINDING. Exit 2 is a
# SETUP failure -- the gate could not run, so nothing was inspected and the
# package is neither proved nor disproved. Exit 1 is FINDINGS -- the gate ran
# and HANDOFF.md cannot be reconciled with the bytes beside it. Collapsing them
# into "non-zero" would report a broken invocation as a defective package and
# send an operator to fix the wrong thing.
if [ "$INVENTORY" -eq 2 ]; then
  echo "HANDOFF INVENTORY COULD NOT RUN"
  tail -20 "$INVENTORY_LOG" >&2 || true
  discard "$PHASE" "the handoff-inventory gate failed to START (exit 2): a \
setup failure, so nothing was inspected and this package is neither proved nor \
disproved by it; the run is refused rather than shipped ungated"
  exit 1
fi
[ "$INVENTORY" -eq 0 ] || {
  echo "HANDOFF INVENTORY REFUSED"
  tail -20 "$INVENTORY_LOG" >&2 || true
  discard "$PHASE" "the handoff-inventory gate reported findings (exit \
$INVENTORY): HANDOFF.md cannot be reconciled with the package and the \
artifacts beside it"
  exit 1
}

# THE EXECUTED-TOOL RECORD, RE-RENDERED WITH THE GATES IN IT.
#
# It was rendered once before P8, because P8 receives it as `--executed` and a
# file cannot be an input to the run that produces it. P8, P9 and P10 have run
# since, and a record of executed tools that stops before the gates would be
# the same omission `checks.txt` is criticised for. The path is the same file
# and the earlier rows are byte-identical -- the digests are of the same bytes,
# taken at the same instants -- so this is an extension of the record, not a
# revision of it. Stated here rather than left for a reader to reconcile.
RERENDER_START=$(date -Is)
set +e
emit_executed_tools "$PHASE"
RERENDERED=$?
set -e
step_row "$PHASE" "re-render $(basename "$EXECUTED") with the P8, P9 and P10 \
rows appended; the pre-P8 rendering is what P8 itself received as --executed" \
  "$RERENDERED" "$RERENDER_START" "$(date -Is)" "$(basename "$EXECUTED")"
[ "$RERENDERED" -eq 0 ] || {
  echo "EXECUTED-TOOL RECORD REFUSED"
  discard "$PHASE" "the executed-tool record could not be re-rendered with \
exit $RERENDERED; one logical tool was executed as two different sets of bytes"
  exit 1
}

# THE COMPLETION ROW, NOT A SECOND DISPOSITION. The terminal `sealed` row was
# written at P5 and one attempt gets exactly one; the `authoritative` state row
# was written at P9 and one attempt gets exactly one of those too. Saying
# either again here is how a ledger comes to carry two.
step_row "P10 complete" "the archive was produced, verified, bound to a \
final-authority record and passed both post-seal gates; the terminal sealed \
row was written at P5 and the authoritative state row at P9, and neither is \
restated here" 0 "$STARTED" "$(date -Is)" "$(basename "$VERIFY_LOG")"
echo "== P10 complete. P11 sanitizes the outer siblings from the outer stage,"
echo "   after tee has closed this log; its transcripts are beside the package."
