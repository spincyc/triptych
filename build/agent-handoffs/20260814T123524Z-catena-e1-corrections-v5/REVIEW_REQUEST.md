# Review request — Catena E1 V5

Exact head `19982ab433dd25704ed60b1ac6ddb678bc3a98f9`, **four commits** above
`f93757854b54c19e50bdcb97ca0fed9b48d22bb7`: three implementation commits and
one records commit. Every measurement, probe and capture in this package was
taken at the last implementation commit, `d0218bae2f7db75e181a0a97937264933c35c09f`, whose
build-sensitive tree is byte-identical to the head; `commits.txt` proves it
with the exact `git diff` invocations and their output.

*(That sentence is the correction of a V4.1 package error the review named:
`REVIEW_REQUEST.md` there said the candidate was one commit above its base
when it was two, and stated the capture-commit qualification only in sibling
records.)*

## Blockers

### 1. Is one record boundary in the unbudgeted model the right shape?

The review asked for "one strict record boundary for every file and collection
member". V5 put it in `catena-model.js` and left `catena.js` calling it,
because the page had thirty gzipped bytes of margin and a boundary bought out
of thirty bytes would have been another list of one-off guards. The page is
371 stripped bytes smaller as a result, and `catena-model.js` grew by roughly
that plus its explanations.

This continues a direction V4 began and the V4.1 review did not object to. But
it does mean the model file — which is also executed under node by
`scripts/_catena.py` during emit, and whose digest is a release binding — now
carries page-shaped derivations (`chapterLines`, `absenceSummary`) alongside
the chapter-membership rule it was created for. `absenceSummary` in particular
returns **visible prose**, placed beside `voicePhrase`, `voiceLabel` and
`joinNames`, which already do.

**A reviewer should decide** whether that is the right home for prose, or
whether the model should return only the typed counts and the page should
compose the sentence at a cost of roughly 200 gzipped bytes it does not have.

### 2. Is `chapterPath`'s three-valued answer the right way to refuse a manufactured absence?

`chapterPath` returns a path, `''` for a chapter the index truthfully records
nothing on, or `null` where the record cannot establish either. The third
answer is new, and it is what stops an unreadable `present` list from becoming
"Nothing held here". The page routes `null` into its existing broken-record
notice, which reads *"its record (the index record) could not be read"*.

That phrasing changed one word of accepted V4.1 copy — "fetched" to "read" —
because a malformed index record fetches perfectly well. **A reviewer should
decide** whether that one-word change is inside the bounded correction or
whether it reopens refusal copy the V4.1 review accepted.

### 3. The malformed-data evidence is fabricated, and had to be

`capture-catena.mjs`, carried forward, reaches only real corpus addresses and
says so proudly. The corpus holds no malformed data, so it cannot evidence
this correction at all. `probe-catena.mjs` therefore injects fixtures in its
own server's response path and reads the live DOM in the same browser.

`LIMITATIONS.md` §1 states plainly that every fixture is fabricated and
represents no holding. **A reviewer should decide** whether that disclosure is
sufficient, or whether adversarial evidence of this kind belongs outside an
evidence package altogether.

### 4. Three defects were corrected that the review did not name

The reflecting-`lang` gap in the harness, `sound()` admitting
`"not a language code"` into visible language prose, and the silent early
return in `render()`. Each was found by writing a regression the review
required, and each is inside the same class the review defined.

**A reviewer should decide** whether correcting unnamed defects found this way
is inside a bounded correction, or whether V5 should have stopped at the five
named classes and reported the other three for a successor.

## Optional feedback

### 5. The absence vocabulary this page may speak

V5 added two clauses: *"has not been surveyed for English"* and *"has a
finding this page cannot read"*. Neither is a new finding — the generator's
four are unchanged — but both are new sentences on a page whose copy the V4.1
review scrutinised. The second is a statement about the page rather than about
the corpus, which is unusual for this surface.

### 6. `MALFORMED_ABSENCES` was rebuilt, not re-asserted

The review named this fixture as the one manufacturing four closed negatives.
Not one of its rows carried a `finding`. Correcting the fixture rather than
the assertion is the right repair in this lane's judgement, but it does mean
the old fixture's exact shape is no longer under test.

### 7. Lane-local tooling, again

`probe-catena.mjs` is new and shipped in `logs/` following the precedent V4
set with `sanitize-and-seal.py` and V4.1 continued with `capture-catena.mjs`.
V4.1's own review request asked whether that tooling should be promoted to
`tools/`; if that question was answered, the answer should govern this one
too. `probe-catena.mjs` has a stronger claim than most: it reads DOM
attributes and the resource log, which the shared browser gate cannot do for
hash-addressed Catena states, and it is the only instrument in the repository
that can evidence malformed-data behaviour at all.

### 8. The sealer was hardened

`PRIVACY-AUDIT.md` records six named additions to `sanitize-and-seal.py`.
They close gaps found by auditing it against the maintainer record of what its
V3 predecessor leaked. None weakens an existing rule.
