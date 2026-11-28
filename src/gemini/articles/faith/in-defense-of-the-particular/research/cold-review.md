# Cold Review Record: In Defense of the Particular

- **Publication:** `gemini/articles/faith/in-defense-of-the-particular`
- **Review date:** 2026-11-28
- **Review scope:** Independent adversarial read-only audit of all canonical TeX sections, research records, web Markdown conversion, and 29-page print PDF against `guidance/editorial.md`, `guidance/articles.md`, `guidance/bibles-for-agents.md`, and tracked primary sources in `src/sources/`, including character-level collation of all 143 extracted quotation items against 33 locally tracked artifacts and rights/metadata verification across 41 bindings.
- **Initial verdict:** REVISE BEFORE RELEASE (4 Critical, 8 Major, 7 Minor, 4 Editorial Polish clusters, plus 4 cross-series harmonization items).
- **Post-remediation status:** All findings resolved and re-verified across schema, metadata, web-edition, preflight, and print-document checks on 2026-11-28.

## Findings and Dispositions

### Critical (C1–C4)
- **C1 (Acts 17:27 misquote):** Corrected `sections/02-universal-cause.tex` to match `challoner-gutenberg-1581` verbatim (`God is ``not far from every one of us. For in him we live and move and are''`).
- **C2 (Fabricated Feltoe apparatus attribution for Leo's Latin):** Restricted endnote on Leo *Sermon 74* § 2 (`sections/05-water-bread-neighbor.tex`) strictly to what Feltoe's footnote `[1131]` actually prints (`in sacramenta transivit`), removing the untracked preceding Latin clause.
- **C3 (Silent unmarked omissions in Aquinas blockquotes):** Restored the omitted internal cross-references in *ST* I, q. 14, a. 11 (`sections/02-universal-cause.tex`, with bracketed `[S]ince`) and *ST* III, q. 75, a. 1 (`sections/05-water-bread-neighbor.tex`, with exact `(Ethic. ix)` and explicit ellipsis).
- **C4 (Verbatim/near-verbatim overlap with restricted Vatican English *LG* 16, *GS* 22, *NA* 2):** Recast all three paragraphs in `sections/04-whole-in-the-part.tex` into fully independent analytical prose while preserving *quodammodo* reserve, invincible ignorance, grace-moved conscience, and Douay-Rheims `John 14:6`.

### Major (M1–M8)
- **M1 (Wrong Bible control edition):** Replaced all 17 `american-1899-ebible` TSV bindings with the single tracked reading witness `artifact.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581.gutenberg-text-7d10da78`, re-collating every Scripture quote character-for-character against `pg1581.txt` and removing obsolete OCR disclaimers.
- **M2 (Ps 8:5–6 grammatical person mismatch):** Quoted Ps 8:4–6 verbatim in its own intact second-person voice from `pg1581.txt` (`sections/06-limits-scale-name.tex`).
- **M3 (Authority-grade misclassification of *CCC* and Vatican II):** Separated ecumenical dogmatic definitions (Chalcedon 451), Second Vatican Council documents by exact genre, and authoritative papal/curial teaching (including the *Catechism*) in `sections/90-scope-method-qualifications.tex`.
- **M4 (Unbound `John 4:24` and missing/ghost loci):** Bound all 43 cited Scripture loci (including `John.4.24`, `John.14.6`, `1Tim.2.4-5`, `Isa.2.2-3`, `Rom.11.17-18`, `Acts.4.12`), added Athanasius `44.7-8`, updated `04` to `"chapters 41 through 44"`, and removed ghost loci (`Matt 16:16`, `Acts 17:26`, Athanasius `8.2-3`, `45`) across sections, references, bindings, audit, and scope.
- **M5 (Mis-anchored *ST* III and *De ente* citations):** Split `ST` III, q. 75, a. 1, obj. 3 (multiple altars) from `ST` III, q. 76, a. 3, obj. 3 (parts of species) in `sections/05-water-bread-neighbor.tex` and bound both; added *De ente*, c. 5 to Appendix A Row 1 (`sections/80-objections-synopsis.tex`).
- **M6 (*De ente* translations in quotes & untracked Latin in Augustine X.32):** Removed English quotation marks around inline translations of Baur–Koch *De ente* (rendering `ab omni esse` literally as `distinct from all being`) and disclosed the inline translation convention in `90` and endnotes; removed the uncollated Latin parenthetical beside Dods's Augustine X.32.
- **M7 (Unverified Hebrew/LXX/Vulgate claim on Gen 12:3):** Replaced the unchecked morphological claim in `sections/03-chosen-for-all.tex` with the bound Challoner text and Catholic canonical reception.
- **M8 (Bibliographic dates/imprints contradicting `edition.toml`):** Aligned `sections/99-references.tex` and all endnotes strictly with `edition.toml` records for Gutenberg *Summa*, CCEL ANF-1/NPNF1-7/NPNF1-10/NPNF2-7/NPNF2-12, NPNF2-4 (1892), Dods (1871), and Gutenberg eBook 1581.

### Minor (m1–m7) & Editorial Polish (E1–E4)
- **m1–m6:** Restricted `\latin{}` strictly to Latin (using `\textit{}` for English concepts and transliterated Greek); standardized Pilate's title to `Roman prefect`; fixed Gen 12:3, Heb 1:1–2, and Augustine *Tractate 123* § 5 quotation punctuation/capitalization; added `ST` I, q. 22, a. 4 (`I.22.4.corpus`, `reply-1`, `reply-3`) for contingency under providence and tightened paraphrases of Aquinas q. 22 ad 2, Scotus *haecceitas*, Irenaeus III.22.2 (`weariness from a journey`), Athanasius § 44.7 (`stubble`), and Celsus (`worms in mud or a cluster of bats`); tightened Appendix A and Reference verse ranges; synced `scope.md` and `source-audit.md`.
- **E1–E4:** Replaced prohibited metaphor (`grammar of love`) and ledger/text-agency verbs (`holds... together`, `double movement... carry... governs`, `supplies`); removed self-narration and section-end heading previews; cut restating closing maxims so Fathers and Scripture keep the last word; removed significance-announcing formulas and AI praise adjectives.

### Cross-Series Harmonization
1. Unified all non-quoted divine pronouns to lowercase (`he`, `him`, `his`, `himself`) while preserving exact source capitalization inside verbatim quotations.
2. De-duplicated St. John Chrysostom *Homily 50 on Matthew* § 4 against Part II (*The Due Return*), replacing the overlapping block quotation in `sections/05-water-bread-neighbor.tex` with concise prose exposition and the distinct verified sentences from §§ 4–5 (`cup of gold` vs. `cup of cold water`, distressed brother as temple).
3. Replaced all `\term{...}` and `\work{...}` calls with `\textit{...}` and deleted `format.tex`, eliminating `\providecommand{\term}` and keeping italic rendering uniform across PDF and web Markdown.
4. Recorded this tracked `research/cold-review.md` audit record.
