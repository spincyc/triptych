# Unresolved blockers — E1 Catena

This lane closed the semantic defect the V14 independent review required, and
the evidence defects that review named in the pipeline, and touched nothing
else. Everything below is recorded open and untouched, and none of it is
authorized by this lane's disposition.

| Blocker | Owner | State after V15 |
| --- | --- | --- |
| The V13 independent review is unpublished | The V13 reviewer | Open, and now historical. The V14 review **is** published, at `0d11766ec232b2b4e46a7d1b0ada56ef22370004` on `review/catena-wave-1-e1-corrections-v14-independent`, so this lane can name the review it answers where V14 could not; every lane from V5 to V12 could, and V13's is the one link missing. The V13 link stays empty; this lane does not fill it with a SHA it does not have. |
| Full sole-source semantic projection beyond the chapter | E1 continuation | Open. The chapter is projected once; the index, the bible roots, the paragraph layer and the absence sources are not. |
| Orphan raw sources | E1 continuation | Open. A source with no fragment standing under it still contributes an edition. |
| Source-only fragments counting | E1 continuation | Open. `{source: "0"}` still borrows its edition's author and work and is counted. |
| Scalar and nested translator coercion | E1 continuation | Open beyond the edition list the previous lane normalized. Unchanged here. |
| Malformed and padded absence rows | E1 continuation | Open. |
| Broader selection and ordering defects | E1 continuation | Open. |
| Refusal verse typing | E1 continuation | Open. |
| Unreadable roots and the `src/web/data/bibles.json` prose | E1 continuation | Open. |
| Broader terminal and corrected-oracle proofs | E1 continuation | Open outside this lane's transport vectors. Inside them the late-answer oracle is corrected and now fails at the exact parent; that correction is scoped to those vectors and proves nothing about the others. |
| CLI/web duplicated semantic model | Separate owner | Open. `scripts/_catena.py` and `src/web/browser/catena/catena-model.js` still state the corpus twice. |
| Model and combined route budget governance | Budget owner | Open, and larger. The model grew again and carries no ceiling; this lane also relocated three paragraphs of page prose into it to stay under the page ceiling. No ceiling was raised and none is proposed here. |
| Historical data seam | Separate owner | Open. `src/web/data/` has zero changes in this lane. |
| Four stale release bindings | Release owner | Open, fail-closed and unsigned. None re-signed. `make -k check` fails closed on them, correctly. |
| Common browser gate failures | Gate owner | Open. 226 inherited failures in three classes — 117 nested `main`, 82 target size, 27 skip link — out of 2,290 assertions over 171 pages and 19 routes, and the two endpoints' reports are identical under the named volatile exclusions, so nothing here moved. Nothing in this lane touches their causes. |
| B0 / shared shell | Shell owner | Open and untouched. |
| Real-device and assistive-technology evidence | Separate owner | Open. Not produced by this lane. |
| Protected Liturgy and PDFs | Protected owners | Untouched. |
| Packaged parent-only PDF error | Separate owner | Open and unrelated. The previous review established `test_pdf_review.PdfReviewCommandTests.test_repeated_signals_do_not_interrupt_child_cleanup` as a signal-timing flake. It did not reproduce at either endpoint in this lane's fresh full-discovery runs, whose failure identity sets are equal. This lane does not fix PDF and claims nothing about it. |
| E1 integration | Master-plan owner | Not integrated. `origin/main` stands at `e4085889fc1b3d2e6721b21166394fe5ea2dea9b`; this lane is not merged into it, and no merge, re-sign, deploy or cutover was attempted. |
