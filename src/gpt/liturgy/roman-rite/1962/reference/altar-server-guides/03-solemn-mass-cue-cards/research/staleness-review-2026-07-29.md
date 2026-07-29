# Staleness review — 2026-07-29

## Exact stale-provider explanation

The repository contains only a GPT edition of
`liturgy/roman-rite/1962/reference/altar-server-guides/03-solemn-mass-cue-cards`;
there is no Claude edition of this leaf to evaluate. Immediately before this
review,

```text
scripts/research-staleness explain gpt \
  liturgy/roman-rite/1962/reference/altar-server-guides/03-solemn-mass-cue-cards
```

reported exactly one changed input:

```text
src/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/03-solemn-mass-cue-cards/research/guide-map.md
```

The ledger's reviewed copy of that map had SHA-256
`2068027d4d129968fb873a485d4640d036e5c64e566172c23472fd1d1b577f2e`.
The current map has SHA-256
`32fb08d4c4d6ae64f2a2d88a68fe714abec62985d203a3be4e9471b5257c03c1`.
Across that interval the map:

- changed the twelve-page predecessor/candidate account into installed
  twelve-page and later source-built thirteen-page accounts;
- replaced pending-review language with the active Alpha checks;
- recorded the installed twelve-page artifact identity and the later
  response-frame repair;
- added a thirteenth, uncut adult-facing terminal apparatus page; and
- recorded the later thirteen-page, thirty-six-card Alpha snapshot.

No response, pronunciation, ceremonial, action-card, shared-source, or sibling
provider record is reported by the exact explanation.

## Candidates

Both required candidates are retained in the ignored build tree:

- `build/staleness/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/03-solemn-mass-cue-cards/modified/`
  is the minimal in-place treatment. It keeps the current thirteen-page source
  and incorporates the changed guide map literally.
- `build/staleness/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/03-solemn-mass-cue-cards/rewritten/`
  is the research-first treatment. It derives the selected card run from the
  shared data and governing records, retains the allowed notice below the
  final grid, and omits the forbidden terminal apparatus.

Neither candidate is an installed replacement, and neither has passed the
ordinary build, physical-duplex, actual-size, visual, or release gates.

## Consequential-claim comparison

| Claim family | Old/current publication | Modified candidate | Rewritten candidate | Effect of changed research |
|---|---|---|---|---|
| Form and selection | Solemn Mass; R01--R07, R08A--R08C, R09--R22, and SO-A01--SO-A12 | Same | Same | No addition, removal, strengthening, weakening, or contradiction. |
| Response-card content | Complete cues with canonical replies and the audited sung-form learning layers | Same | Same | No substantive effect; no response or pronunciation record changed. |
| Action-card authority | Twelve editorial cross-views of the controlling SO chronology, including the separately identified recovery policy for SO-A12 | Same | Same | No substantive effect; no ceremonial record changed. |
| Duplex order and parity | Response fronts on 1, 3, 5, 7; action fronts on 9, 11; mirrored backs follow each front | Same | Same | Strengthened documentation only; the map records the settled sequence and frame review. |
| Allowed final notice | Compact revision and rights notice after the final back grid | Same | Same | No substantive effect. |
| Cards-only boundary | Adds an uncut adult-facing terminal apparatus after all card faces | Retains that page | Omits it | The changed map adds and strengthens the terminal-page claim, but that claim contradicts the profile rule that the leaf reproduce only selected card faces, have no terminal apparatus, and add no page. |
| Physical page count | Thirteen pages, of which pages 1--12 are card faces and page 13 is apparatus | Thirteen | Twelve | Substantive disagreement caused by the boundary conflict, not wording. |
| Training and qualification prose | Adult Alpha, safety, textual, and rights explanation appears in the leaf's terminal apparatus | Same | Leaves those work-wide controls to the paired full guide and series records; face-local conditions remain on cards | The rewrite removes prose that the changed map newly documents inside a cards-only leaf. |
| Alpha evidence | Map distinguishes screen review from uncompleted actual-size and physical-duplex checks | Same | Same limitation; candidate itself makes no new review claim | The changed record strengthens qualification and does not justify inferring omitted checks. |
| Artifact identity and frame repair | Records the installed twelve-page hash, later inset repair, and the thirteen-page Alpha snapshot | Same | Treats these as historical/current audit facts, not authority to add apparatus | Stronger audit history, but no change to card text, order, or ceremonial claims. |

The modified candidate differs from the old/current publication only in its
explicit audit annotation. The rewritten candidate agrees with it on every
response, action, source-boundary, duplex, rights, and Alpha limitation claim,
but disagrees substantively on the terminal apparatus and therefore on page
count and ownership of adult-facing qualification prose.

## Verdict

**Material change requiring user confirmation.** The changed edition-local
map does not reveal a liturgical, ceremonial, Latin, pronunciation, or
action-card error. It does, however, document a publication-structure change
that contradicts the governing cards-only contract in
`guidance/liturgy/roman-1962-server-training.md`. The research-first candidate
restores the twelve-page cards-only boundary; the minimally modified candidate
preserves the thirteen-page treatment. Because those candidates disagree in
substance, this review does not replace the source or installed PDF and does
not rebaseline the edition.

## User disposition and implementation

The user approved the rewritten candidate on 29 July 2026. The canonical
source now omits the terminal-apparatus invocation and retains the compact
revision and rights notice below the final back grid. The resulting installed
companion has twelve physical pages and thirty-six cards; its exact build,
validation, visual-review, and installed identity are recorded in the series
production manifest. This disposition resolves the material
publication-boundary question without changing any response, pronunciation,
action-card, ceremonial, or duplex-order claim.
