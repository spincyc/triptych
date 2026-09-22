# Claude postconciliar web candidate: bounded cold review

## Disposition

**PASS.** No blocker was found in the exact candidate. No browser was launched during this review, and no tracked file was edited.

- Candidate: `build/web/claude/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s51-twenty-fifth-sunday-in-ordinary-time-year-a.md`
- Candidate SHA-256: `b00ee2b37eac785eb0f616f7ef99b685ca8ea5b276c891c9e1b94467af8e3ea6`
- Fresh regeneration SHA-256: `b00ee2b37eac785eb0f616f7ef99b685ca8ea5b276c891c9e1b94467af8e3ea6`; `cmp` exited 0.
- `research/web-artifact.json` records the same candidate path and SHA-256.

## Findings

- **Exact old/new delta:** the prior browser-reviewed Markdown is SHA-256 `121204cc47d0b09dcfe45953184eb52bd064c64e1feb9ab591560b89645bf036`, 123,476 bytes. The candidate is 123,480 bytes. A unified diff has exactly two changed lines: two Markdown hard breaks expressed as two trailing spaces were replaced by semantic `<br>` elements in the displayed title/subtitle. There is no other content, order, anchor, table, chronology, or navigation change. Both forms render to the same two `<br>` nodes; the retained old and current rendered HTML bodies confirm that semantic identity.
- **Receipt identity:** `.scratch/claude-no-web-review-final/render-receipt.json` names the exact candidate hash and its current renderer, layout, CSS, and icon hashes. Recomputed hashes match every receipt input and proof asset. The current rendered HTML is SHA-256 `b847bea38a4ba7010bd8e969879ddf6f54f069225e14d874e3acc8f07eff00b8`.
- **Graph and component isolation:** schema-2 `proper-components.toml` declares the research study as the only web output. Fresh generation, `check-web-edition`, both research component phases, and full research content preflight pass. The source graph resolves 94 valid bindings and the three research interpretive lanes. No `-synthesis.md` or `-homily.md` companion leaf exists in either `build/web/claude` or tracked `web/claude`.
- **Rite isolation:** the candidate has no match for `1962`, `trident`, `extraordinary form`, `traditional latin mass`, `missale romanum.*1962`, or `preconciliar`. Its title, breadcrumb, liturgical-resolution appendix, edition statement, and scope consistently identify the postconciliar Roman Missal, Third Edition, United States 2011 context.
- **Whitespace and title:** there are no trailing spaces or tabs. The current HTML has one correct H1 and document title, with the site suffix only in `<title>`. The two semantic breaks occur only in the secondary displayed title/subtitle and introduce no extra paragraph or heading.
- **TOC, anchors, and navigation:** the candidate retains 11 TOC entries and their stable explicit targets. The current HTML has 11 TOC fragment links, no duplicate IDs, the `main-content` skip target, primary navigation, and `Library › Postconciliar Missal` breadcrumb. The prior exact-content browser audit resolved all 11 TOC targets.
- **Tables and chronology:** the current HTML contains all four tables: appointed elements, interpretive comparison, Scriptural Date and Location, and liturgical branches. The chronology remains 20 rows in the retained browser evidence. Current preflight passes the eight-element chronology record, generated annotations, and claim-support checks. The old-byte browser audit proved page-level reflow and table-local horizontal scrolling at 1440×900, 393×852, and 320×852; the only Markdown delta renders identically and occurs before the TOC.
- **Four senses:** all three interpretive lanes remain present, each with Literal, Allegorical, Moral, and Anagogical in order. The current HTML contains 12 corresponding definition terms; prior browser evidence confirmed three complete four-sense definition lists.
- **Visual inspection:** the supplied exact-candidate 1440×900 and 393×852 top screenshots are legible, calm, single-column renderings. The full title, edition identity, breadcrumb, primary navigation, subtitle, and beginning of document content are visible without clipping or horizontal overflow. The prior deep desktop/mobile chronology captures remain applicable because the candidate changes only the two semantically identical title breaks.
- **Static publication check:** scoped `public-alpha check` passes for this publication and recognizes the canonical, synthesis, and homily PDFs while preserving the canonical research study as the sole web edition. This is a candidate review, not deployment verification.

## Evidence boundary

The prior retained browser audit (`.scratch/claude-no-web-review-retry/browser-audit.json`) reports PASS at 1440×900, 393×852, and 320×852, with 11/11 live TOC targets, four tables, three complete four-senses lists, visible rights/revision matter, and no document-level horizontal overflow. This review independently checked that the candidate differs from those reviewed Markdown bytes only by the two semantic `<br>` spellings and inspected the supplied current-candidate desktop/mobile screenshots. No claim is made about deployment.
