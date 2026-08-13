# Evidence index

Start at `HANDOFF.md`; the open questions are in `REVIEW_REQUEST.md`.

## Documents

| file | what it carries |
| --- | --- |
| `HANDOFF.md` | identities, what the review found, what was done, all measurements |
| `REVIEW_REQUEST.md` | the five questions this lane cannot answer about itself, and where to press |
| `VOICE-KEY-PROJECTION.md` | the classifier defect, the four source pairs, the three route keys, why the index is the only possible home, before/after per address |
| `BASELINE-COMPARISON.md` | base vs head, identity **and** detail, every difference classified |
| `PRIVACY-AUDIT.md` | what the V3 package leaked, the five reasons its sealer reported zero, and proof the new sealer catches it |
| `AT-LIMITATION.md` | what was demonstrated, scoped to the inspected session; no transcript reproduced |
| `STRANGER-KEYS.md` | per-path behaviour, and the three prose corrections the review asked for |
| `UNRESOLVED-BLOCKERS.md` | separately owned prerequisites, all still open |
| `LIMITATIONS.md` | the two known gaps against the review, and the limits of every measurement |
| `checks.txt` | every command with its exit status, including the ownership-boundary audit |
| `changed-files.txt`, `changes.patch` | the exact diff from the reviewed head |
| `commits.txt` | the three commits, with identities |
| `MANIFEST.sha256` | content digest of every file here |

## Logs

| file | what it proves |
| --- | --- |
| `logs/focused-catena-suite.log` | 266 tests, OK |
| `logs/all-tests-base.log` | base `f2c9bc49`: 1,600 tests, 15 F, 13 E, 11 S |
| `logs/all-tests-head.log` | head: 1,617 tests, 14 F, 13 E, 11 S |
| `logs/browser-gate-base.json`, `logs/browser-gate-head.json` | the two full gate reports |
| `logs/gate-comparison.log` | assertion set equal, 0 status changes, 0 detail changes |
| `logs/make-k-check-head.log` | exit 2, the same three failing targets as base |
| `logs/budgets-head.log` | the four exact gzip-9 measurements |
| `logs/release-bindings-head.log` | four stale bindings, none re-signed |
| `logs/public-site.log` | the build the gate read |
| `logs/sanitize-and-seal.py` | the sealer, with the five V3 defects recorded at the point of fix |
| `logs/SANITIZATION-AND-INDEX-CHECK.log` | the seal run: zero hits, gate passed before the manifest was written |

## The regressions added, by what they pin

**`ExactVoiceKeyTest`** — `translation:grc` fails closed; the refusal names no
Greek and claims no holding; `translation:la` is honoured; an empty language
and a second delimiter are malformed rather than unsupported; the
supported → unsupported → supported round trip keeps the reader's voice and
leaves the region unbusy; and the published projection matches the four source
pairs actually present in the corpus.

**`TypedStructureBoundaryTest`** — the region never stays busy; malformed
extent members state no locus; no false chapter crossing; a scalar translator
container attributes nobody while a valid list survives beside it; a malformed
language reaches no label and no URL; unnamed authors get no shared filter
key; valid siblings survive every malformed neighbour; absence counts and
words are one typed value; non-list containers count nothing; and nothing
malformed reaches the page as words.

**Corrected oracles** — the V3 `voice-not-held` scenario asserted `Greek
translation — none here`; the support test pinned the literal source of the
language-membership check. Both encoded the defect and both now assert the
correction.

### Negative control

The seventeen new tests were run against the V3 implementation at
`f2c9bc49`. They fail there — and `TypedStructureBoundaryTest` does not merely
fail, it aborts with `TypeError: blocked is not iterable`, because the V3
render tail throws on a container that is not a list. A reviewer should
reproduce this rather than trust it: check out the parent's
`catena.js` and `catena-model.js`, keep this test file, and run the two
classes.
