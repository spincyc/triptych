# Catena E1 — V5 malformed-data and partial-arrival correction handoff

## 1. Task and intended outcome

Answer the fresh independent review of V4.1 —
`7f69575b982926e827974f2ed236b1c8bfd8aaad`, **CHANGES REQUIRED** at exact
candidate `f93757854b54c19e50bdcb97ca0fed9b48d22bb7` — with the smallest
bounded correction of its five proven malformed-data and partial-arrival
classes, behind one typed record boundary; prove route completion rather than
parse rejection; and stop for a fresh independent review.

The intended outcome is a reviewable head, not an accepted one. **This lane
records no acceptance of its own work, and does not review it.**

This package supersedes nothing. It names, and does not mutate,
`build/agent-handoffs/20260813T164804Z-catena-e1-corrections-v4-1`
(SHA-256 `781c9b7582c5d3dd22a9330291fa158b12b722a626ce0264dc3dfc95d54f1552`),
whose digest was re-verified byte-exact from its evidence commit
`8bd64e70f18892f52029f25817d2ca493ddb7467` before anything here was written.

## 2. Branch

`impl/catena-wave-1-e1-corrections-v5`, started by detaching at the exact
reviewed V4.1 head in a **fresh clone**, not a worktree.

## 3. Commits

| | |
| --- | --- |
| review addressed | `7f69575b982926e827974f2ed236b1c8bfd8aaad` |
| parent (V4.1 head) | `f93757854b54c19e50bdcb97ca0fed9b48d22bb7` |
| implementation (1 of 3) | `aba43989637989430dbaf8814c24960bf372cd9a` |
| implementation (2 of 3) | `3dbe298246cbeb9357cd3c787d6a2e6b66cc5893` |
| implementation (3 of 3) | `d0218bae2f7db75e181a0a97937264933c35c09f` |
| HEAD (final) | `19982ab433dd25704ed60b1ac6ddb678bc3a98f9` |

**Four** commits: three implementation, one records. `commits.txt` proves the
records commit touches no code, and names each implementation commit.

The second and third are small and were made rather than folded in, because
this repository does not amend: the second binds the gated language code once
instead of validating it and then indexing the language table with the raw
value beside it, and the third stops a note quoting a byte figure that a later
comment trim made stale. Both are in `changes.patch`.

## 4. Uncommitted changes in the reviewed state

None. `git status --porcelain` is empty at the reviewed head.

## 5. Focused files changed

| File | Change |
| --- | --- |
| `src/web/browser/catena/catena-model.js` | the typed record boundary and the derivations that moved into it — `whole`, `tongue`, `voiceLanguage`, `records`, `canonBook`/`canonBooks`/`bookOf`, `chapterPath`, `paragraphPath`, `chapterLines`, `absenceRows`/`absenceCount`/`absenceSummary`, plus stricter `touchesChapter`, `formatExtent`, `spansChapters`, `chapterFragments`, `voiceKey`, `chapterVoices`, `parseVoiceKey` |
| `src/web/browser/catena/catena.js` | calls them; two `lang` sinks gated; the visible language chip gated on shape; word tally, refusal members, lead and blocked members, `index.voices` and the canon typed; `onArrival` and `render`'s early return brought into the terminal funnel; one word of broken-record prose corrected from "fetched" to "read" |
| `tools/tests/test_catena_wave_1.py` | `lang` reflection in the replay shim, `langAttributes` in the projection, the rebuilt absence fixture, `MODEL_SHA256`, and 39 new regressions in five classes |
| `PROJECT-WORK.md`, `guidance/corpus-browser-roadmap.md`, `guidance/corpus-browser-master-plan.md`, `promised-deliverables.toml` | durable records |

**Byte-identical and untouched:** `src/web/browser/catena/catena.css`,
`src/web/browser/catena/index.html`, everything under `src/web/data/`, every
release record, the common gate, the shared shell, protected Liturgy, and all
PDFs.

## 6. Preview and exact startup commands

```
make public-site
node logs/probe-catena.mjs build/public-alpha/site logs/probe-head.json "V5 head"
python3 -m unittest discover -s tools/tests -p 'test_catena*.py'
```

All paths are repository-relative and run from the repository root.

## 7. Implementation summary

See `TYPED-PRESENTATION-BOUNDARY.md` for the full account. In brief: the review's
five classes are one class, so V5 answers it once, in `catena-model.js`, which
carries no byte ceiling. The page calls the boundary and is **371 stripped
gzipped bytes smaller** for it. No ceiling was raised.

Three defects the review did not name were found by writing the regressions it
required: the replay harness did not reflect `lang` into the content attribute,
which is why the proven sink was invisible to a green suite; `sound()` admitted
`"not a language code"` into visible language prose; and `render()` had a
silent early return that left the page unterminated after a malformed canon.

## 8. Known limitations

`LIMITATIONS.md`, nine numbered. The load-bearing ones: every fixture in this
package is **fabricated** and represents no holding; screenshots are offered
for five states only because four of the five classes turn on facts a picture
cannot carry; and this is rendering evidence, not announcement evidence.

## 9. Unresolved decisions

`REVIEW_REQUEST.md`, four blockers and four optional. The sharpest is whether
visible prose (`absenceSummary`) belongs in the model beside `voicePhrase` and
`joinNames`, or whether the page should compose it at a cost of roughly 200
gzipped bytes it does not have.

## 10. Artifact inventory

| Path | What it is |
| --- | --- |
| `HANDOFF.md` | this file |
| `REVIEW_REQUEST.md` | questions only — four blockers, four optional |
| `changes.patch` | the exact parent→head diff |
| `changed-files.txt` | `git diff --name-only` output, bare |
| `checks.txt` | every command, its numeric exit, its result and its qualification |
| `commits.txt` | ancestry, and the proof that the records commit touches no code |
| `TYPED-PRESENTATION-BOUNDARY.md` | what changed, where, and why the model |
| `BASELINE-COMPARISON.md` | base vs head for every suite and gate |
| `PROBE-DIFFERENCE.md` | the real-Chromium before/after, field by field |
| `REGRESSIONS-FAIL-ON-PARENT.md` | the new regressions replayed against the parent: 23 fail, and the two bootstrap scenarios kill the harness outright |
| `VISUAL-STATE-INDEX.md` | one row per PNG |
| `SCREENSHOT-METHOD.md` | how the evidence was produced, and what is fabricated |
| `DATA-TEST-CONTRADICTION.md` | status: unchanged, untouched |
| `UNRESOLVED-BLOCKERS.md` | seven, each with its owner |
| `PRIVACY-AUDIT.md` | method, result, what was removed, independent verification |
| `LIMITATIONS.md` | what this package does not prove |
| `EVIDENCE-INDEX.md` | every member and what it establishes |
| `MANIFEST.sha256` | SHA-256 of every member except itself |
| `logs/` | measurement logs, and the four tools shipped as evidence |
| `screenshots/` | 20 PNGs and their two index files |

**Conditional classes deliberately omitted, with reasons:**

- `sources.md` — no research, provenance, rights or source-history work was
  done; this is a defensive-boundary correction over existing records.
- print and forced-colors captures — `catena.css` is byte-identical and
  nothing here bears on those media; V4.1's accepted matrix stands.
- PDF artifacts — no PDF was touched.
- No empty directory was created to imply evidence that does not exist.
