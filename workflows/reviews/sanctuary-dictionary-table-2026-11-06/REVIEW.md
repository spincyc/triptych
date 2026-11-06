# Sanctuary dictionary table — independent cold review

Accept the exact candidate identified below for integration. No unresolved correctness, preservation, interaction, or visual blocker remains. This review concerns the website table requested on 6 November 2026; it does not claim that the candidate has reached main or the live site.

The reviewer worked independently of the renderer, frontend and test owners, read the changed renderer, stylesheet, enhancement script and website profile, and ran a separate Chromium/CDP harness against the generated preview. The preview used the actual gallery renderer, canonical artwork, stylesheet and script; its assembly stubbed unrelated native-reader traversal. No tracked files, publication sources or native PDFs were edited by this reviewer.

The final presentation is one semantic four-column table: Picture, Object, Grouping, and Identification / use. Its ten functional groups keep related objects together, starting with the altar and sanctuary, then vessels and cloths, books, service objects, incense, vestments and ministers, and related rites. Optional name sorting does not replace that default order. Small drawings and consistent headwords make the rows easy to scan. Shared compositions are placed with an explanatory entry and linked from other entries; they do not repeat the definitions. Expanded pictures have enough space to inspect details, with substantive qualifications visible and longer source apparatus behind native disclosures. The restrained separators, type hierarchy and consistent Details actions form a coherent table. Repetitive generic view labels and per-picture scale labels are absent.

Independent canonical-to-HTML comparison verified 64 primary rows, two contextual anchors and all 66 definitions exactly once. The book marker and Communion rail remain contextual. All 70 logical artwork assets appear once in ownership; thumbnail and expanded-image elements deliberately reuse each URL. All 70 preview PNGs match their canonical SHA-256 values. Every canonical use statement, source citation, qualification and warning is retained in its owning panel. The check covered 185 immediate-note occurrences across depicted objects and 35 image-credit statements. Each nonempty credit remains unchanged in its own adjacent native Image credit disclosure. No rights statement was generalized, removed or reclassified.

The independent browser run passed 43 assertions at 1440, 1024, 768, 390 and 320 pixels, with a normal desktop scrollbar retained at narrow widths. It checked unique anchors, resolving internal links, all loaded artwork, functional order, name sorting and row/detail pairing, Latin and contextual-name search, filtering and empty results, fragment navigation through filters, Enter/Space activation, Escape and native-summary closing with restored focus, and no-JavaScript details, credits and direct PNG fallback. No print calls or workers were activated. The enhanced gallery had no HTTP, JavaScript or console errors. After direct PNG navigation, Chromium's optional favicon request returned 404 in the minimal preview; the requested artwork loaded correctly.

All 64 rows were personally inspected through ten complete group captures. Six expanded compositions were inspected: prepared chalice, pontifical layers, historical chapel, Missal on its stand, worn cassock and surplice, and paired cruets. The visual set also covers the table's left and right positions and expanded clothing at all five widths, plus native no-JavaScript details and credits. Final coverage comprises 35 screenshots: 25 are byte-identical to already inspected captures; the ten changed or new final captures were opened and inspected directly. At 320 pixels the first three columns remain available on the left; horizontal scrolling exposes the complete prose column. That column is now 271 pixels wide within a 273-pixel visible region. Whole lines remain readable with JavaScript disabled as well. The page itself does not overflow horizontally, and expanded panels stay within the visible region.

Findings raised during this review were resolved before acceptance:

- An undefined `body_extra` reference in native print-page rendering was removed; the new argument belongs only to ordinary page rendering.
- Shared-image panels now retain qualifications and warnings for the other pictured objects, including the prepared-chalice components and surplice.
- The cruet's Details action now occupies its own line, consistent with entries that include Latin.
- The 320-pixel prose column now fits the table viewport; the former cropped line beginnings were directly rechecked in enhanced and native HTML modes.
- The baseline introduction no longer promises a second click to close when JavaScript is disabled.

The site can proceed through its normal integration gates with these bytes. The dictionary's canonical records, artwork and native print products were outside this presentation change. This review supplies interface and preservation evidence, not a new editorial, liturgical, rights, physical-print or publication approval.

| Candidate input | SHA-256 |
| --- | --- |
| `tools/public-alpha` | `8a9c657046ce8ab499c481dc10c52c9678c1c7ac6ca82b63b299af7ca5bdd1ef` |
| `release/public-alpha/assets/site.css` | `21c45816c86cc53cadba8b9236cdd063111976d1a59c30420ba670df818dde63` |
| `release/public-alpha/assets/sanctuary-dictionary.js` | `a462c6bb39146673a5e25d1e6359cc469e236bc32396cd79a0f0b079f0501ddb` |
| `library/sanctuary-picture-dictionary.html` | `d6a3b3ff6b80acb6190f9aaf93c07bc0b696c8392b8b251e3c1ac4eff2fad81c` |

Portable evidence accompanies this review in `review-summary.json` and `screenshots.json`. The raw browser report, harness, source projection and screenshots remain disposable scratch evidence under `.scratch/dictionary-table-cold-review/`. Screenshot filenames and their exact hashes are recorded in the manifest; the summary records every supporting report hash.

- `review-summary.json`: `d575855139501b12285381ea5b1472c8530dde1572fa554ab03842fc508edb05`
- `screenshots.json`: `6f0bfacfe9d3a5cd00c17bcc1249323b13e34e846602a68dbf0fd18e215c8936`
- Raw final browser report: `643517a75628c37ef9aaad78dfab8098ede7dcde055d5a07f814c71ab4a86f65`
- Canonical projection verification: `869ea133dd5244e5b479e80a9096efd1ac4ba552fb3939a212f689f9badd577b`
