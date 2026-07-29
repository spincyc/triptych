# Staleness review — 2026-07-29

## Edition and trigger

- Provider edition: `gpt`
- Leaf: `liturgy/roman-rite/1962/reference/altar-server-guides/02-missa-cantata-cue-cards`
- Deterministic explanation:
  `src/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/02-missa-cantata-cue-cards/research/guide-map.md`
- Baseline guide-map fingerprint:
  `21f0f24aca4ca9a52823c585b75cd28589001f154f7ecbda17bac1a44b842804`
- Candidate locations:
  `build/staleness/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/02-missa-cantata-cue-cards/modified/`
  and
  `build/staleness/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/02-missa-cantata-cue-cards/rewritten/`

Only the GPT edition exists, so no second provider edition requires a separate
verdict. The modified candidate preserves the current mechanical source
exactly. The rewritten candidate was freshly assembled from the changed guide
map and the shared render contract; it retains the same card selections and
terminal apparatus while independently restating the PDF subject and removing
the non-rendering `deepstudy` wrapper.

## Old / modified / rewritten comparison

| Consequential claim | Effect of changed research | Old installed source | Modified candidate | Rewritten candidate | Substantive disagreement |
|---|---|---|---|---|---|
| The companion is a cards-only rendering of the paired guide's integrated responses and `MC-A01`–`MC-A12` actions. | Unchanged; the guide map continues to bind the same selections and shared owners. | Renders `response-reference` and `missa-cantata-action-cards` with the Missa Cantata and cards-only switches set. | Same source and result. | Independently retains the same switches and shared inputs. | None. |
| The deck includes an uncut adult-facing terminal apparatus after the cut cards. | Adds this boundary and removes the former exclusion of a terminal-reference page. | Already invokes `\CardCompanionTerminalApparatus` in the end hook. | Same invocation. | Independently retains the terminal-apparatus invocation. | None; the changed record documents behavior already present in the current paper. |
| The physical sequence is twelve duplex card pages plus page 13 as apparatus, not part of the cut grid. | Adds page 13 and changes the documented count from twelve to thirteen. | Current installed PDF has thirteen pages; the source appends apparatus only after the shared card renders. | Same sequence. | Same sequence. | None. |
| Revision and rights material remains below the final cut grid, with the full guide owning printing, actor, roster, branch, and safety keys. | Strengthens the boundary by distinguishing the compact final-back notice from the separate adult-facing apparatus. | End hook retains generation metadata and the compact rights notice before the apparatus; no ownership key is moved into the card faces. | Same treatment. | Same treatment. | None. |
| The edition remains an Alpha training aid whose physical actual-size, duplex, photocopy, and cut review is pending. | Adds an Alpha-apparatus snapshot and explicitly refuses to infer physical review from screen review. | Terminal apparatus supplies the Alpha/training/safety/textual/rights qualifications; nothing in the card source claims physical approval. | Same qualifications. | Same qualifications. | None. |
| Exact artifact identity and review state are audit-record facts, not card-face teaching claims. | Replaces an old uninstalled-candidate note with historical installed-snapshot and later Alpha-snapshot records. | Does not print a PDF hash or assert release completion on a card face. The currently installed PDF is thirteen pages with SHA-256 `ce0dfad27e008e3583baa8d0937fdb62688f584e2fd90f7f69f71f201fe6314e`, matching the latest production-manifest row. | Same. | Same. | None. The changed guide map's earlier `172ead…` value identifies its dated 2026-07-27 snapshot, not the later installed Alpha artifact. |

The rewritten candidate differs from the old paper in wording of PDF metadata
and in non-rendering source structure only. It does not differ in card
selection, actor or condition handling, terminal apparatus, page sequence,
rights treatment, or training status. The modified candidate has no source or
rendering difference from the old paper because every changed research claim
that bears on the publication is already represented.

## Edition-local verdict

**No material publication change.** The changed guide map adds and strengthens
the audit description of the already-installed thirteen-page Alpha apparatus
state; it neither adds a new card claim nor removes, weakens, or contradicts
any consequential claim made by the current edition. Neither candidate should
replace the installed source. This review deliberately does not rebaseline the
edition; baseline disposition remains with the coordinating task.
