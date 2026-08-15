#!/usr/bin/env bash
# Assemble, derive, audit and seal the V7 handoff package.
#
# One command, so the package is a function of the head rather than of the
# order somebody happened to do things in, and every transcript inside it is
# the honest one for the state it describes.
#
# THE ORDER IS THE ARGUMENT. Three things constrain it:
#
#   - the sealer NORMALIZES paths, so a `--check-only` run before it would
#     ship a log full of hits the seal then fixed, and a reader would have to
#     know that to read it. It runs after.
#   - `claims.json` inventories the package, so it must be derived after every
#     log exists. `head-consistency.py` reports what was written after that
#     derivation, so the residue is visible rather than hidden.
#   - a transcript of a sealing run cannot be inside the set that run seals:
#     the manifest is written while the run is still writing the log. So the
#     seal runs twice, and `logs/seal.log` is the first pass. The second pass
#     normalizes the logs written between the two; a third makes no change at
#     all, which is the idempotence a reviewer can check by running it again.
set -euo pipefail

REPO=${REPO:?set REPO to the implementation clone}
PARENT=${PARENT:?set PARENT to the parent sha}
REVIEW=${REVIEW:?set REVIEW to the review sha}
STAMP=${STAMP:?set STAMP to the package timestamp}
SRC=${SRC:?set SRC to the staged package directory}

PKG="$REPO/build/agent-handoffs/$STAMP-catena-e1-corrections-v7"
HEAD_SHA=$(git -C "$REPO" rev-parse HEAD)
SEAL_ONE=$(mktemp)
trap 'rm -f "$SEAL_ONE"' EXIT

echo "== assembling $PKG at $HEAD_SHA"
rm -rf "$PKG"
mkdir -p "$PKG/logs"
( cd "$SRC" && find . -type f ! -path '*/__pycache__/*' -print0 ) \
  | ( cd "$SRC" && xargs -0 -I{} cp --parents {} "$PKG" )
chmod +x "$PKG"/logs/*.py "$PKG"/logs/*.sh 2>/dev/null || true

echo "== git-derived members"
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

echo "== composing checks.txt from the batteries' own ledgers"
python3 "$SRC/logs/checks.py" --package "$PKG" --head "$HEAD_SHA" \
  --parent "$PARENT" ${MEASURED:+--measured "$MEASURED"}

echo "== the sealer's own tests"
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

# Four members are referenced by documents and are written by steps that run
# after the index check which reads those references. They are created empty
# and replaced in place; nothing depends on the placeholder content, and the
# manifest is written last, over the real thing.
: > "$PKG/logs/seal.log"
: > "$PKG/logs/seal-check.log"
: > "$PKG/logs/derive-claims.log"
: > "$PKG/logs/head-consistency.log"

echo "== deriving claims, so the derived record exists to be sealed"
python3 "$PKG/logs/derive-claims.py" --repo "$REPO" --parent "$PARENT" \
  --head "$HEAD_SHA" --review "$REVIEW" --package "$PKG" \
  --out "$PKG/claims.json" > /dev/null

echo "== seal, first pass — normalizes, scans, and becomes logs/seal.log"
set +e
python3 "$PKG/logs/sanitize-and-seal.py" "$PKG" > "$SEAL_ONE" 2>&1
SEAL=$?
set -e
echo "EXIT=$SEAL" >> "$SEAL_ONE"
cat "$SEAL_ONE"
[ "$SEAL" -eq 0 ] || { echo "SEAL FAILED"; exit 1; }
cp "$SEAL_ONE" "$PKG/logs/seal.log"

echo "== check-only over the normalized package (writes nothing)"
set +e
python3 "$PKG/logs/sanitize-and-seal.py" "$PKG" --check-only \
  > "$PKG/logs/seal-check.log" 2>&1
CHECK=$?
set -e
echo "EXIT=$CHECK" >> "$PKG/logs/seal-check.log"
cat "$PKG/logs/seal-check.log"
[ "$CHECK" -eq 0 ] || { echo "CHECK-ONLY FAILED"; exit 1; }

# Again, now that every log exists and the tree is normalized. This is the
# derivation the package ships; the first was only to give the seal something
# to seal.
echo "== deriving claims over the complete, normalized package"
python3 "$PKG/logs/derive-claims.py" --repo "$REPO" --parent "$PARENT" \
  --head "$HEAD_SHA" --review "$REVIEW" --package "$PKG" \
  --out "$PKG/claims.json" | tee "$PKG/logs/derive-claims.log"

echo "== head consistency"
set +e
python3 "$PKG/logs/head-consistency.py" --package "$PKG" \
  > "$PKG/logs/head-consistency.log" 2>&1
CONSISTENT=$?
set -e
echo "EXIT=$CONSISTENT" >> "$PKG/logs/head-consistency.log"
cat "$PKG/logs/head-consistency.log"
[ "$CONSISTENT" -eq 0 ] || { echo "HEAD CONSISTENCY FAILED"; exit 1; }

echo "== seal, second pass — this writes the manifest you hold"
python3 "$PKG/logs/sanitize-and-seal.py" "$PKG"

echo "== archive"
( cd "$REPO/build/agent-handoffs" \
  && python3 - "$STAMP-catena-e1-corrections-v7" <<'PY'
import sys, zipfile, pathlib
name = sys.argv[1]
root = pathlib.Path(name)
archive = pathlib.Path(name + ".zip")
# The package directory is the single top-level entry, which is what
# `guidance/external-review-handoffs.md` requires and what `--verify` now
# proves rather than assumes.
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as handle:
    for path in sorted(root.rglob("*")):
        if path.is_file():
            handle.write(path, path.as_posix())
print(f"archive: {archive} ({archive.stat().st_size} bytes)")
PY
)
( cd "$REPO/build/agent-handoffs" \
  && sha256sum "$STAMP-catena-e1-corrections-v7.zip" \
     > "$STAMP-catena-e1-corrections-v7.zip.sha256" \
  && cat "$STAMP-catena-e1-corrections-v7.zip.sha256" )

echo "== verify — proves every ZIP member against the manifest"
# Deliberately not written into the package: a file created after the seal is
# not in the manifest that seal produced.
python3 "$PKG/logs/sanitize-and-seal.py" "$PKG" --verify
