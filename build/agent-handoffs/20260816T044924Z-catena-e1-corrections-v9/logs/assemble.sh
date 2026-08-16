#!/usr/bin/env bash
# Assemble, freeze, derive, audit and seal the V9 handoff package.
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
#                            and is declared deferred.
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
#   P7  archive          -- the ZIP, single top-level root, sorted paths;
#                            then the sidecar carrying the ZIP's sha256 AND
#                            its byte size.
#   P8  final verification -- verify-final-package.py, READ-ONLY, from the
#                            ZIP alone; its transcript lands OUTSIDE the
#                            package, beside the archive, because a file
#                            created after the seal is not in the manifest
#                            that seal produced. Run it twice and it is the
#                            same run twice.
#
# The package-total and final-byte authority is MANIFEST.sha256 plus the ZIP
# and its sidecar. claims.json sizes only what was frozen before it was
# written, and says so.
set -euo pipefail

REPO=${REPO:?set REPO to the implementation clone}
PARENT=${PARENT:-7e4df42a21bc2be2d28ff14943f63af3e7e3a6f8}
REVIEW=${REVIEW:-611b5eed8128ad5f84f6bf73ac9f9ead5959ab7f}
STAMP=${STAMP:?set STAMP to the package timestamp}
SRC=${SRC:?set SRC to the staged package directory}
NAME=${NAME:-catena-e1-corrections-v9}

PKG="$REPO/build/agent-handoffs/$STAMP-$NAME"
HEAD_SHA=$(git -C "$REPO" rev-parse HEAD)
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

# The members later phases write, declared instead of pre-created. A document
# may name one while it is absent; the deferral is printed on every pass, and
# the P8 re-check over the extraction runs with no deferrals at all.
DEFER=(--defer claims.json --defer DERIVED-CLAIMS.md
       --defer logs/derive-claims.log --defer logs/head-consistency.log
       --defer logs/seal.log --defer logs/seal-check.log)

echo "== P1 evidence staging: $PKG at $HEAD_SHA"
rm -rf "$PKG"
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

echo "== P1 composing checks.txt from the batteries' own ledgers"
python3 "$SRC/logs/checks.py" --package "$PKG" --head "$HEAD_SHA" \
  --parent "$PARENT" ${MEASURED:+--measured "$MEASURED"}

echo "== P1 the sealer's own tests"
set +e
python3 "$PKG/logs/test-sanitize-and-seal.py" > "$PKG/logs/sealer-tests.log" 2>&1
TESTS=$?
set -e
echo "EXIT=$TESTS" >> "$PKG/logs/sealer-tests.log"
# Running them inside the package leaves bytecode behind, and a build artifact
# is not evidence.
rm -rf "$PKG/logs/__pycache__"
tail -3 "$PKG/logs/sealer-tests.log"
[ "$TESTS" -eq 0 ] || { echo "SEALER TESTS FAILED"; exit 1; }

echo "== P2 normalize to a fixpoint (no manifest is written here)"
# Each pass appends its transcript to logs/seal.log, then a check-only pass
# writes its transcript beside it. The loop ends only when a check-only run
# exits clean AND its transcript is byte-identical to the one already in the
# tree -- which means the final check really did run over a tree that already
# contained its own transcript. That is the idempotence a reviewer can replay.
PASS=0
while :; do
  PASS=$((PASS + 1))
  [ "$PASS" -le 6 ] || { echo "P2 FAILED: no fixpoint within 6 passes"; exit 1; }
  set +e
  ( cd "$REPO" && python3 "$PKG/logs/sanitize-and-seal.py" "$PKG" \
      --normalize-only "${DEFER[@]}" ) > "$WORK/seal-pass" 2>&1
  SEAL=$?
  set -e
  echo "EXIT=$SEAL" >> "$WORK/seal-pass"
  { echo "== normalize pass $PASS"; cat "$WORK/seal-pass"; } >> "$PKG/logs/seal.log"
  [ "$SEAL" -eq 0 ] || { cat "$WORK/seal-pass"; echo "P2 FAILED"; exit 1; }
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
    cat "$WORK/check-pass"; echo "P2 FAILED: check-only still failing"; exit 1
  fi
done

echo "== P3 THE FREEZE: the snapshot that IS the inventory"
python3 "$PKG/logs/derive-claims.py" --package "$PKG" \
  --write-freeze "$WORK/freeze.json"

echo "== P4 derive once, from the freeze, pre-normalized"
( cd "$REPO" && python3 "$PKG/logs/derive-claims.py" --repo "$REPO" \
    --parent "$PARENT" --head "$HEAD_SHA" --review "$REVIEW" \
    --package "$PKG" --freeze "$WORK/freeze.json" \
    --out "$PKG/claims.json" ) | tee "$PKG/logs/derive-claims.log"

echo "== P5 consistency audit: undeclared drift is a hard failure"
set +e
python3 "$PKG/logs/head-consistency.py" --package "$PKG" \
  --pending MANIFEST.sha256 > "$PKG/logs/head-consistency.log" 2>&1
CONSISTENT=$?
set -e
echo "EXIT=$CONSISTENT" >> "$PKG/logs/head-consistency.log"
cat "$PKG/logs/head-consistency.log"
[ "$CONSISTENT" -eq 0 ] || { echo "HEAD CONSISTENCY FAILED"; exit 1; }

echo "== P6 manifest: prove the freeze held, then write the seal once"
( cd "$REPO" && python3 "$PKG/logs/sanitize-and-seal.py" "$PKG" \
    --manifest-only --claims "$PKG/claims.json" )
# Nothing writes inside $PKG below this line.

echo "== P7 archive"
( cd "$REPO/build/agent-handoffs" \
  && python3 - "$STAMP-$NAME" <<'PY'
import sys, zipfile, pathlib
name = sys.argv[1]
root = pathlib.Path(name)
archive = pathlib.Path(name + ".zip")
# The package directory is the single top-level entry, which is what
# `guidance/external-review-handoffs.md` requires and what P8 proves rather
# than assumes.
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as handle:
    for path in sorted(root.rglob("*")):
        if path.is_file():
            handle.write(path, path.as_posix())
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

echo "== P8 final verification, from the ZIP alone, read-only"
# The transcript lands OUTSIDE the package, beside the archive: a file created
# after the seal is not in the manifest that seal produced.
python3 "$PKG/logs/verify-final-package.py" \
  --zip "$REPO/build/agent-handoffs/$STAMP-$NAME.zip" \
  --sidecar "$REPO/build/agent-handoffs/$STAMP-$NAME.zip.sha256" \
  --name "$STAMP-$NAME" \
  | tee "$REPO/build/agent-handoffs/$STAMP-$NAME.verify-final.log"
