# EVIDENCE-INDEX — every artifact in this package

Every path below resolves to a file in this package; the index check in
`logs/sanitize-and-seal.py` fails the seal if one does not.

## Mechanism vocabulary, stated once and applied per row

- **REAL** — the command really ran here, at the packaged head, and this is its
  output.
- **DERIVED** — a comparison computed from two REAL outputs; the script that
  computes it is shipped or the method is stated in the row.
- **SYNTHETIC fixture** — a labelled test fixture stood in for data the corpus
  does not contain. Used only for the malformed-provenance evidence, because
  the tracked corpus types every provenance field it carries.
- **STATEMENT** — prose asserting a fact about behaviour or environment, with
  its supporting evidence named in the row.

There is no EMULATED or AT-SUPPLEMENT class in this package, because it carries
no capture set. See `HANDOFF.md` §10 and `LIMITATIONS.md` §6.

## 1. Package records

| Path | Mechanism | What it is, and what it establishes |
| --- | --- | --- |
| `HANDOFF.md` | STATEMENT | The ten protocol sections: task, branch, exact head/base/review SHAs, tree cleanliness, changed files, startup commands, implementation summary, limitations, open decisions, inventory. |
| `REVIEW_REQUEST.md` | STATEMENT | Questions only. Seven blockers, each naming the acceptance decision it blocks and the artifact to look at; six optional items. |
| `LIMITATIONS.md` | STATEMENT | Eight things this package does not establish, including the two the reviewer is most likely to test: the untested stranger-key discard, and the prose cost of the one-byte code ceiling. |
| `STRANGER-KEYS.md` | STATEMENT | **Evidence correction 1.** The exact unrecognized-hash-key behaviour, per address path, with proven cases separated from cases read from the code. Quotes the V2 sentence it corrects, with file and line. |
| `AT-LIMITATION.md` | STATEMENT + REAL | **Evidence correction 2.** Quotes the false V2 line with file and line, gives the real command output showing the launcher exists and the bus was running, tabulates what is genuinely absent, and states the corrected limitation. |
| `UNRESOLVED-BLOCKERS.md` | STATEMENT | Twelve outside-owner rows, every one open, plus three this lane's own audit added and deliberately did not fix. Nothing is marked complete. |
| `BASELINE-COMPARISON.md` | DERIVED | Reviewed head versus packaged head across seven classes, kept apart so no single "no regressions" claim hides a class. |
| `changed-files.txt` | REAL | `git diff --numstat -M`, the boundary audit, and the byte-identical list. |
| `changes.patch` | REAL | `git diff -M 17f031b37..f2c9bc49d`. The complete reviewable delta, 801 lines. |
| `commits.txt` | REAL | `git log` for the range, with full messages. |
| `checks.txt` | REAL | Every command with its exact exit status and result, in sections A–E plus S (skipped, and why). |
| `EVIDENCE-INDEX.md` | — | this file |
| `MANIFEST.sha256` | REAL | SHA-256 of every file in this package except itself. |
| `SANITIZATION-AND-INDEX-CHECK.log` | REAL | The seal's own output: normalization, private-token scan, index completeness, manifest coverage. |

## 2. Logs

| Path | Mechanism | What it establishes |
| --- | --- | --- |
| `logs/focused-catena-suite.log` | REAL | The focused suite at the packaged head: 249 tests, OK. Verbose, so every new test name is visible. |
| `logs/all-tests-head.log` | REAL | `unittest discover` over all of `tools/tests` at the packaged head: 1600 tests, 14 failures / 13 errors. |
| `logs/all-tests-base.log` | REAL | The same discovery at `17f031b37`, run in a separate clean clone: 1582 tests, 15 failures / 13 errors. |
| `logs/all-tests-comparison.log` | DERIVED | The per-name set difference of the two. **No new failure at head.** The one name absent at head is disclosed as an environment artifact of the baseline clone's path, not a fix. |
| `logs/budgets-head.log` | REAL | All four gzip-9 measures at the packaged head, computed with the repository's own function. |
| `logs/make-k-check-head.log` | REAL | `make -k check`, exit 2, three failing targets — the same three as baseline. |
| `logs/release-bindings-head.log` | REAL | The three stale Catena bindings and `stale: 3 stale binding(s)`, unrepaired. |
| `logs/examples-comparison.log` | DERIVED | 28 divergences at head versus 30 at baseline, and the set difference in both directions. The "new divergence" side is **empty**. |
| `logs/browser-gate-head.json` | REAL | The full gate report at the packaged head. |
| `logs/browser-gate-base.json` | REAL | The full gate report at the baseline. |
| `logs/gate-comparison.log` | DERIVED | The two reports compared as complete assertion objects: identity set equal, 0 status changes, 0 detail changes, 14 Catena failing rows on both sides with their names. |
| `logs/public-site.log` | REAL | `make public-site`, exit 0, the site the gate then read. |
| `logs/sanitize-and-seal.py` | — | The sealing script, carried forward from the V2 package with its private-path table extended for this checkout, so the seal is reproducible. |

## 3. Evidence for the two implementation defects

Neither defect has a screenshot, because neither introduces a visual state; both
are pinned by executable assertions instead. The replay harness drives the real
`src/web/browser/shared/browser-core.js`, `src/web/browser/catena/catena-model.js` and `src/web/browser/catena/catena.js` under node against the real
corpus, so these are behavioural evidence, not source inspection.

### 3a. Unsupported voice — `UnsupportedVoiceTest`

| Assertion | Mechanism | What it proves |
| --- | --- | --- |
| `test_an_unsupported_voice_fails_closed` | REAL replay | `translation:zz` produces the error state, names `voice=translation:zz is not a voice this corpus holds`, keeps the address as written, offers recovery, renders no fragment, and fetches no chapter. |
| `test_a_real_but_unheld_language_code_fails_closed_the_same_way` | REAL replay | `translation:de` — a nameable ISO code the corpus has never held — is refused identically, so the fix is not a special case for nonsense codes. |
| `test_an_upper_case_code_is_malformed_rather_than_unsupported` | REAL replay | `translation:EN` fails the *grammar*, not the set: the two refusals do not collapse into one. |
| `test_the_refusal_is_distinct_from_the_malformed_one` | REAL replay | The malformed note and the unsupported note are mutually exclusive in the rendered detail text. Three states, not two. |
| `test_no_unsupported_voice_ever_claims_a_holding` | REAL replay | **The review's contradiction assertion.** Over the whole rendered projection, for both unsupported scenarios: no `none in ZZ translation`, no `ZZ translation`, no German equivalent, no `none here`; the tally is empty and the voice control offers only `Everything held`. |
| `test_the_unsupported_voice_is_dropped_from_the_recovery_route` | REAL replay | Recovery offers `#book=Gen&chapter=1&bible=douay-rheims` — the sound part of the address kept, the unhonourable key dropped. |
| `test_a_supported_voice_survives_a_pass_through_an_unsupported_one` | REAL replay | supported → unsupported → supported over one live document: 14 fragments, then the error state, then 14 fragments again with the address intact. History is not stranded. |
| `test_the_supported_set_is_read_from_the_index_not_from_the_key` | REAL replay + source pin | The set comes from `index.held[].languages`, and the refusal fetches only the three bootstrap files — **no request was added**. |
| `test_a_voice_the_chapter_lacks_is_kept_and_named_rather_than_widened` | REAL replay | The preserved case: `translation:grc` is supported, so it is kept, named `Greek translation — none here`, and the address is not rewritten. |

### 3b. Untyped provenance — `UntypedProvenanceTest`, over `UNTYPED_PROVENANCE_FIXTURE`

| Assertion | Mechanism | What it proves |
| --- | --- | --- |
| `test_nothing_untyped_reaches_the_page_as_words` | SYNTHETIC fixture, REAL replay | No `[object Object]`, `undefined`, `NaN`, comma-joined array, or fixture marker anywhere in the rendered projection; and no `true`/`false`/`null` in any displayed source line. |
| `test_the_sound_record_beside_them_is_untouched` | SYNTHETIC fixture | The control row keeps its edition, printing and rights: withholding garbage costs no valid fact. |
| `test_a_malformed_edition_and_printing_are_withheld_not_coerced` | SYNTHETIC fixture | The review's two named scalar fields, object and array, withheld — and the sound sibling on the same row still renders. |
| `test_a_mixed_translator_list_keeps_every_valid_hand_and_no_other` | SYNTHETIC fixture | **The review's exact requirement.** `["Good Name", {…}, 42, "   ", "Other Name"]` renders exactly `tr. Good Name, Other Name`. |
| `test_a_translator_container_that_is_not_a_list_kills_nothing` | SYNTHETIC fixture | The page-kill is gone: all five fragments render, the tally and the announcement both exist, so the render completed past the point the exception used to escape from. |
| `test_an_untyped_locator_and_review_state_say_nothing` | SYNTHETIC fixture | Two fields the review did not name, closed: no coercion, and no `not collated` claim from an untyped review state. |
| `test_untyped_identity_fields_are_withheld_from_every_chip` | SYNTHETIC fixture | `authors`, `works`, `dates`, `languages`, `extents`, the author heading and the filter label all clean. These four projections were **added to the harness** by this lane, because the existing global sweep could not see those nodes. |
| `test_the_remaining_adversarial_scalars_render_nothing` | SYNTHETIC fixture | boolean, null, empty and whitespace values render nothing, and the one sound fact among them still stands. |
| `test_an_untyped_refusal_note_is_not_coerced_into_the_sentence` | SYNTHETIC fixture | The numbering-refusal sentence, a third field the review did not name. |
| `test_no_replayed_page_ever_coerces_a_value_into_words` (pre-existing) | REAL replay | The repository's own global sweep, now covering four more node classes and the new scenarios. |

## 4. Coverage, and what is not met

Met and evidenced here: both implementation defects, both evidence corrections,
the ownership boundary, the unraised budgets, the frozen model, the gate
comparison, the full-check comparison, and the no-regression claim.

**Not met, and not claimed:** a real assistive-technology session
(`AT-LIMITATION.md`); a genuine system forced-colors palette; and a signed
release binding, which is the release owner's. No capture set is included; the
V2 package remains the visual evidence of record for the states it covers, and
remains accurate for them because `src/web/browser/catena/catena.css` and `src/web/browser/catena/index.html` are
byte-identical at this head.
