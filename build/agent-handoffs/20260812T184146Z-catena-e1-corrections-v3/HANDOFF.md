# HANDOFF — E1 Catena route-owned correction, V3

## 1. Task and intended outcome

Answer the 2026-08-12 independent review of E1 Catena correction V2 with the
smallest bounded correction from the exact reviewed head, and return that head
for fresh independent review.

The review dispositioned reviewed head `17f031b37840d8320c664a128d72b502108fe075`
**CHANGES REQUIRED** and named exactly four things for this lane:

1. a syntactically well-formed but **unsupported voice** rendered as an
   invented held-language absence (findings 5 and 8);
2. **malformed displayed provenance** reaching visible text through implicit
   JavaScript coercion (finding 4);
3. an inaccurate, unqualified **stranger-key** preservation statement
   (findings 5 and 11);
4. a false **AT-SPI bus launcher** absence claim (finding 11).

Nothing else was in scope. Every other review finding stays with the owner the
review assigned it to, and this lane repaired none of them, including the
deliberately unsigned Catena release binding.

This package supersedes `20260811T212656Z-catena-e1-corrections-v2`, the
reviewed V2 package. **That package and its ZIP are unchanged**: nothing in
this lane read-modified, replaced, refreshed or deleted it, and it remains as
historical evidence in the lane that produced it. This is a new immutable
package with a new timestamp. Where a V2 statement was found inaccurate, this
package states the correct fact and names the V2 file and line it corrects; it
does not edit the sealed package.

## 2. Current branch

`impl/catena-wave-1-e1-corrections-v3`

## 3. Current commit SHA and task base commit

| Identity | SHA |
| --- | --- |
| Packaged head (reviewed state) | `f2c9bc49dd29499734193b264ba9da21304b27f1` |
| Task base = exact reviewed V2 head | `17f031b37840d8320c664a128d72b502108fe075` |
| Independent review addressed | `4c30d86f7118d69eb27d12dc9b63568e531918eb` |
| Merge base with `main` | `9b9ff74a77d1bcd7d454d2a7fc448b8a6c8f1fd4` |

The base is the exact reviewed head, not `main`, so the reviewable delta is the
correction alone rather than the whole V2 lane.

## 4. Does the reviewed state include uncommitted changes?

No. `git status --short` is empty at the packaged head. This package is written
under `build/`, which is git-ignored, and is not part of the reviewed tree.

## 5. Focused files changed

Two production/test paths, plus four durable authority records:

| Path | Role |
| --- | --- |
| `src/web/browser/catena/catena.js` | the whole implementation correction |
| `tools/tests/test_catena_wave_1.py` | the regressions that pin it |
| `PROJECT-WORK.md` | durable lane record |
| `guidance/corpus-browser-roadmap.md` | durable disposition and corrected prose |
| `guidance/corpus-browser-master-plan.md` | E1 status row |
| `promised-deliverables.toml` | the V3 deliverable |

**Byte-identical at this head**, and verified as such in `checks.txt`:
`src/web/browser/catena/catena.css`, `src/web/browser/catena/index.html`,
`src/web/browser/catena/catena-model.js`. No generator, generated Catena data,
release record, common browser gate, B0/shared shell, protected Liturgy path,
or PDF changed.

## 6. Exact startup commands, including required route state

    $ python3 -m unittest discover -s tools/tests -p 'test_catena*.py'
    $ make public-site && make check-browser-gate
    $ make -k check

To see the corrected behaviour in a browser, serve the built site and open:

    /catena/index.html#book=Gen&chapter=1&bible=douay-rheims&voice=translation:zz
      -> refused: "voice=translation:zz is not a voice this corpus holds"
    /catena/index.html#book=Gen&chapter=1&bible=douay-rheims&voice=translation:grc
      -> honoured and named "Greek translation — none here" (supported, unheld)
    /catena/index.html#book=Gen&chapter=1&bible=douay-rheims&voice=translation:en
      -> honoured, 14 fragments

The malformed-provenance states are fixture-driven and are exercised by the
`untyped-provenance` replay scenario; the corpus itself carries no malformed
provenance, which is why a labelled fixture is the only way to show it.

## 7. Implementation summary

### 7.1 Unsupported voice — shape is not support

`hashProblems` validated `voice` against a grammar alone
(`original`, or `translation:` plus two or three lowercase letters) while
`book`, `chapter` and `bible` were each validated against runtime data. So
`translation:zz` passed, was seeded into the control, and was then named by
`voicePhrase` in three places — the option label, the tally clause, and the
chain's aside — producing `none in ZZ translation`: an assertion about what the
corpus holds, derived from nothing but the reader's own URL.

The correction adds one branch. After the shape test passes, a translation
voice must also name a language the corpus actually holds:

    } else if (parsed.language &&
               !(index.held || []).some((one) =>
                 (one.languages || []).includes(parsed.language))) {
      flag('voice', voice, 'is not a voice this corpus holds');
    }

`index.held[].languages` is Catena-owned runtime truth already in memory: the
route awaits `src/web/data/structure/catena/index.json` in `start()` before any arrival is
resolved, so **no request is added** and the pinned six-request first load is
unchanged. Its union over the corpus is `en`, `grc`, `la`; over the fixture
root, `en`, `la`.

An unsupported voice now fails closed through the **existing** invalid-address
state, which is the same disposition `bible=nope` already receives — the
address is left exactly as written, the specific value is named, recovery is
offered without the key that could not be honoured, and `fillVoices(null, true)`
suppresses any "none here" label. No new state, no new markup, no new CSS.

Three states now exist where two did:

| Address | Disposition | Note shown |
| --- | --- | --- |
| `voice=klingon`, `translation:`, `original:x`, `translation:en:extra`, `translation:EN` | malformed shape | `is not a voice — "original", or "translation:" plus a language` |
| `voice=translation:zz`, `translation:de` | well formed, unsupported | `is not a voice this corpus holds` |
| `voice=translation:en`, `translation:grc`, `original` | supported | honoured; "— none here" only where the chapter really lacks it |

The distinction the review asked for is exact: a voice the **chapter** lacks is
untouched, still kept in the URL and still named rather than widened, because
the corpus does hold that language.

### 7.2 Untyped displayed provenance — one gate, applied once

The route already had the right predicate — `sound(value)`, "a fact only as
nonempty text" — and applied it to five values out of roughly twenty. The
correction moves the check into the one funnel every provenance fact already
passed through, so the per-field guards disappear rather than multiply:

    const fact = (said) => {
      if (!sound(said)) return;
      source.appendChild(T.el('span', 'sep'));
      source.appendChild(textNode(said));
    };

Every displayed value is now typed: `locator`, `edition`, `edition_published`,
`translators` (container **and** each item), `rights`, `attribution`,
`rights_basis`, `review`, `id`, and, in the fragment head and the chain, the
`author`, `work`, `date` and `language` chips, the author heading, the
author-filter label, and the numbering-refusal note.

Translator entries are judged one at a time, so a malformed entry is dropped
while its valid siblings still render:

    const hands = [].concat(fragment.translators).filter(sound).join(', ');
    if (hands) fact('tr. ' + hands);

`["Good Name", {"broken": true}, 42, "   ", "Other Name"]` renders exactly
`tr. Good Name, Other Name`.

The author name is typed **once**, where the chronological groups are built, so
the group heading, the filter checkbox label and the persisted exclusion set are
all the same already-typed name and cannot disagree.

**A defect worse than coercion, found by this lane's own audit and fixed here:**
`translators` carrying a `length` and no `join` — for example `{"length": 2}` —
satisfied the old `.length` guard and then threw `TypeError` from inside
`renderFragment`. Because `render()` is `async`, that escaped as an unhandled
rejection *after* `T.clear(reading)` and after the chapter was appended, so the
chain column, the tally, the status announcement, focus recovery and the route
write never ran, and the reading region kept `aria-busy="true"` for ever. The
review did not name this; it is the same defect one type further along.

### 7.3 What was deleted to pay for it

Both JavaScript ceilings were effectively exhausted at the reviewed head (4 and
5 bytes). Nothing was waived; the corrections were funded by removal:

- a **provably dead** voice lookup repeated four times.
  `M.chapterVoices(file).find((one) => one.key === wanted) || M.parseVoiceKey(wanted)`
  is exactly `M.parseVoiceKey(wanted)`: `chapterVoices` builds each entry's
  `key` from its own `voice` and `language`, so a found entry and the parsed key
  are equal by construction, and at the one site inside `fillVoices` the guard
  immediately above had already excluded a match, so `.find` could only ever
  return `undefined`;
- six per-field `if (…)` guards, folded into the one typed `fact` gate;
- `joinNames`, `.filter(Number.isFinite)`, and the refusal-note construction,
  each tightened — the last of which also closed a coercion hole.

## 8. Known limitations

See `LIMITATIONS.md`. The three that most affect judgement of this package:

1. **No real assistive-technology evidence** — unchanged from V2, and the
   reason is corrected in `AT-LIMITATION.md`.
2. **Stranger-key discard is proven by reading, not by test.** See
   `STRANGER-KEYS.md`. Only the value-identical preservation case has a test.
3. **The code-only budget stands one byte clear**, and the explanatory prose
   this file's house style would ordinarily carry could not be afforded. One
   precondition (`joinNames` consumes its argument) is pinned by a test instead
   of a comment.

## 9. Unresolved decisions

See `REVIEW_REQUEST.md`. The two this lane most wants judged are the choice to
fail closed rather than add a distinct unsupported-voice surface, and the
`[].concat` container rule for `translators`.

## 10. Artifact inventory

| Entry | What it is |
| --- | --- |
| `HANDOFF.md` | this file |
| `REVIEW_REQUEST.md` | the questions only |
| `LIMITATIONS.md` | what this package does not establish |
| `STRANGER-KEYS.md` | the corrected stranger-key statement, and its proof state |
| `AT-LIMITATION.md` | the corrected AT-SPI statement |
| `UNRESOLVED-BLOCKERS.md` | outside-owner ledger; every row still open |
| `BASELINE-COMPARISON.md` | reviewed V2 head versus this head |
| `changed-files.txt` | the changed-path inventory and the boundary audit |
| `changes.patch` | `git diff` from the reviewed head to this head |
| `commits.txt` | the commits in that range, with full messages |
| `checks.txt` | every command, its exit status and its result |
| `EVIDENCE-INDEX.md` | every artifact here, and what it proves |
| `logs/` | the raw outputs the above records summarise |
| `MANIFEST.sha256` | SHA-256 of every file here except itself |

The ZIP's own SHA-256 cannot live inside the ZIP: it is written to a sibling
transport digest beside the archive — the archive's name with a `.sha256`
suffix — and printed in this lane's final report.

**Where this package is, and what it is not.** It is written under `build/`,
which is git-ignored, exactly as the V2 package was; it is not part of the
reviewed tree and is not acceptance by itself. This package carries no
screenshot or capture set: the four corrections are a URL-validation branch, a
rendering-type discipline and two prose corrections, all of which are pinned by
the focused suite, and no new visual state was introduced to photograph.
