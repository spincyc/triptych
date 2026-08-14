# Limitations — what this package does not prove

### 1. The fixtures are fabricated, and deliberately so

`logs/probe-catena.mjs` serves a **fixture site root**: it injects malformed
JSON in the response path of its own static server, over a real built site.
Those fixtures are adversarial test data. **They represent no holding of this
project, no corpus record, and no real state of the published site.**

This is a departure from the V4.1 capture tool carried forward beside it,
whose header says of its own addresses: *"Every address below is real
repository data … Nothing is fabricated for the picture."* That claim is right
for evidencing real holdings and useless for evidencing malformed-data
behaviour, because the corpus holds no malformed data. A reviewer should read
every image and every probe row in this package as **behaviour under
deliberately corrupted input**, never as a picture of the corpus.

The built site itself is never modified: the injection is in the server's
response path, so `build/public-alpha/site` on disk is byte-identical before
and after a probe run.

### 2. Screenshots are offered for five states only, and cannot carry the rest

Four of the five blocking classes turn on facts a picture cannot show. A DOM
`lang` attribute is invisible in a raster. A request the page did or did not
make is invisible. `aria-busy` is invisible. For those, the evidence is
`logs/probe-base.json` and `logs/probe-head.json` — the live DOM and the live
resource log, read in the same browser, at the base and at the head.

Screenshots accompany only the five states whose *rendering* visibly differs,
at two viewports each. They are supporting evidence, not the proof.

### 3. This is rendering evidence, not announcement evidence

As in V4 and V4.1, no AT bus or screen reader was available. The probe reads
`aria-busy`, the status region's text and the focused element; it does not
prove what a screen reader says. **The real-device-or-AT prerequisite remains
open with its owner and is not superseded by anything here.**

### 4. No print or forced-colors evidence is added

V4.1's accepted 53-image matrix already covers print and forced-colors
emulation for the real corpus states, and V5 changed no CSS — `catena.css` is
byte-identical. Nothing in this correction bears on those media, so no
successor capture was made. The V4.1 matrix is neither superseded nor
re-issued here.

### 5. The browser-gate identity claim is narrower than it sounds

`logs/compare-gate.py` reports the whole report deep-equal — but it excludes
four volatile keys, not one: `generatedAt`, `root`, `durationMs` and
`browser`. The V4.1 record's wording named only `generatedAt`. The correct
statement is: **every non-volatile key of the report is deep-equal across
both runs, with those four excluded.**

### 6. The full-suite comparison is a name-set comparison

The head runs more tests than the base, because V5 adds regressions. No
literal baseline identity is claimed. What is compared is the set of FAIL and
ERROR test names, and that comparison is recorded in `checks.txt` with the
exact `diff` invocation that produced it.

### 7. The package digest is a transport digest

The `.zip.sha256` proves the archive received is the archive sent. It does
**not** prove reproducible construction: the ZIP entry timestamps are local
mtimes. `MANIFEST.sha256` is the content proof, and it survives repacking.

### 8. The sealer was hardened, and still cannot solve one class by pattern

`logs/sanitize-and-seal.py` is carried forward from V4.1 with named additions
recorded in `PRIVACY-AUDIT.md`. One class is not solvable by pattern: an
absolute path outside `$HOME`, the repository root and the scratch directory
is unrecognisable as private. It is handled by policy — this package contains
no such path — not by the tool.

### 9. Inherited state this lane did not repair, and could not

- Four stale Catena release bindings, including the new `catena-model.js`
  digest. Correctly fail-closed, none re-signed. The release owner's.
- The `src/web/data/` test contradiction, preserved untouched. The Day-reader
  owner's.
- The common-gate failure population. The shared shell's.
- `check-tool-registry` and `check-examples`. Their own owners'.

Every one of these is recorded with its owner in `UNRESOLVED-BLOCKERS.md`.
None was worked around, whitelisted, weakened or expect-marked.
