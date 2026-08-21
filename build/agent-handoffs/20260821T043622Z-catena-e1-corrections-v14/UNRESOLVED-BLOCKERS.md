# Unresolved blockers — E1 Catena

This lane closed six findings of the V13 independent review and touched
nothing else. Everything below is recorded open and untouched, and none of it
is authorized by this lane's disposition.

| Blocker | Owner | State after V14 |
| --- | --- | --- |
| The V13 independent review is unpublished | The V13 reviewer | Open. No branch or commit on `origin`; this lane records the gap and cannot fill it. |
| Full sole-source semantic projection beyond the chapter | E1 continuation | Open. The chapter is projected once; the index, the bible roots, the paragraph layer and the absence sources are not. |
| Orphan raw sources | E1 continuation | Open. A source with no fragment standing under it still contributes an edition. |
| Source-only fragments counting | E1 continuation | Open. `{source: "0"}` still borrows its edition's author and work and is counted. |
| Scalar and nested translator coercion | E1 continuation | Partly narrowed, not closed. Each edition's translator list is normalized once and frozen; a fragment's own list is still coerced per row. |
| Malformed and padded absence rows | E1 continuation | Open. |
| Broader selection and ordering defects | E1 continuation | Open. |
| Refusal verse typing | E1 continuation | Open. Refusals carry `kind`, `chapter` and `note`; verses are not typed. |
| Unreadable roots and the `src/web/data/bibles.json` prose | E1 continuation | Open. |
| Broader terminal and corrected-oracle proofs | E1 continuation | Open outside this lane's vectors. |
| CLI/web duplicated semantic model | Separate owner | Open. `scripts/_catena.py` and `src/web/browser/catena/catena-model.js` still state the corpus twice. |
| Model and combined route budget governance | Budget owner | Open. Disclosed by four lanes; no ceiling raised, none proposed here. |
| Historical data seam | Separate owner | Open. `src/web/data/` has zero changes in this lane. |
| Four stale release bindings | Release owner | Open, fail-closed and unsigned. None re-signed. |
| Common browser gate failures | Gate owner | Open. 226 inherited failures, identical at both endpoints and to V10–V13. |
| B0 / shared shell | Shell owner | Open and untouched. |
| Real-device and assistive-technology evidence | Separate owner | Open. Not produced by this lane. |
| Protected Liturgy and PDFs | Protected owners | Untouched. |
| E1 integration | Master-plan owner | Not integrated. No merge, re-sign, deploy or cutover. |
