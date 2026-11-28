# Cold Review Log: At the End of Every Why

- **Date:** 2026-11-28
- **Document:** `articles/faith/at-the-end-of-every-why` (`gemini`, *The Creature Before God*, Part III)
- **Scope:** Independent read-only review covering verbatim quotation and negative-claim verification, theological and pastoral accuracy, editorial voice, source-binding and preflight hygiene, web-edition conversion, and full 27-page print visual inspection.

## Summary of Findings and Remediations

### Critical
1. **C-1 — False negative claim regarding *Deus caritas est* and imprecise Trent phrasing:**
   - *Finding:* Appendix B, `research/source-audit.md`, and `research/scope.md` wrongly stated that Pope Benedict XVI's *Deus caritas est* (2005) was unregistered in `src/sources/works/` (it is registered under `src/sources/works/papal-documents/` as `work.papal.benedict-xvi.hf-ben-xvi-enc-20051225-deus-caritas-est`), and `scope.md` called Trent Sessions VI and XIII "unacquired decrees" despite uncollated historical OCR texts existing in the library.
   - *Remediation:* Corrected Appendix B, `research/source-audit.md`, and `research/scope.md` to record accurately that only St. John of the Cross and *Salvifici doloris* are absent from the source library, that *Deus caritas est* is registered as a restricted Vatican catalog entry outside the sources cited here, and that Trent Sessions VI and XIII are bound at the catalog level and paraphrased rather than quoting uncollated OCR.
2. **C-2 — Misquoted 1832 French Francis de Sales and unbound artifact:**
   - *Finding:* The endnote in Section 5 printed `employez les remèdes` where the tracked 1832 Périsse Frères French text reads `Quand il vous arrivera du mal, apportez-y les remèdes` (lines 4150–4152), and the 1832 French artifact was omitted from `research/source-bindings.toml`.
   - *Remediation:* Restored the exact tracked 1832 French wording in Section 5, added a verified `textual-control` binding for `artifact.francis-de-sales.introduction-a-la-vie-devote.perisse-freres-french-gutenberg.gutenberg-53540-text-c2d4183f` with its canonical SHA-256 fingerprint in `research/source-bindings.toml`, and added its own row in `research/source-audit.md`.

### Major
3. **M-1 — `house-voice` preflight failure:**
   - *Finding:* `sections/90-scope-method-qualifications.tex` contained `"logged in the leaf's source audit"`, failing `tools/check-content-preflight --check house-voice`.
   - *Remediation:* Rewrote to `"recorded in the accompanying source audit"` and re-ran `--check house-voice` individually (exit 0).
4. **M-2 — Non-Douay-Rheims Scripture wording under a blanket DR guarantee:**
   - *Finding:* Four phrases (`James 1:25`, `1 Cor 4:7`, `Gen 3:5`, `1 John 4:8/16`) diverged from tracked Challoner Douay-Rheims wording while Appendix B and Section 2 stated all Scripture quotes were Douay-Rheims.
   - *Remediation:* Corrected direct quotations to exact Douay-Rheims wording (`"the perfect law of liberty"`, `"what hast thou that thou hast not received"`, `"you shall be as Gods"` [Gen 3:5], and `"God is charity"` [1 John 4:8, 16] in Appendix A), and clarified in Section 2 and Appendix B that scriptural verses embedded inside quoted translations of Aquinas, Augustine, or Bernard retain the quoted translator's wording.
5. **M-3 — St. Thérèse printed page offsets and internal OCR line numbers in reader endnotes:**
   - *Finding:* Taylor fifteenth-thousand edition citations were shifted by +1 (`p. 136` for `p. 135`, `p. 163` for `p. 162`, `pp. 117–118` for `p. 117`), and internal OCR line ranges appeared in reader endnotes.
   - *Remediation:* Verified exact top-of-page headers directly in the tracked OCR text and replaced all reader endnotes with exact printed pages (`ch. VIII, p. 117`; `ch. IX, p. 135`; `ch. IX, pp. 138, 140`; `ch. X, p. 162`; `ch. XI, p. 182`), retaining physical line indices solely in `research/source-audit.md`.
6. **M-4 — Production/audit vocabulary in reader-facing text and endnotes:**
   - *Finding:* Audit/production terms (`Audit`, `Witnesses`, `Notice`, `grammar of creaturehood`, `firewall`, bare `(p. 327)`, and repeated `"paraphrased from the cataloged record"` / `"CCEL tracked text"` labels) appeared in body prose, headings, and endnotes.
   - *Remediation:* Renamed headings to `"Aquinas's Examination of Created Goods"` and `"Three Doctors in the Dry Land"`, moved `p. 327` to an endnote, replaced production/IT metaphors with plain English, and stripped internal tracking/cataloging phrases from endnotes so endnotes cite like a book while Appendix B and `research/source-audit.md` state repository provenance once.
7. **M-5 — Restating closing maxims after block quotations and back-to-back duplications:**
   - *Finding:* Several blockquotes were followed by restating aphorisms, and *CCC* 1718 and Irenaeus IV.13.4 were duplicated across adjacent body text and endnotes.
   - *Remediation:* Cut the redundant closing maxims in Sections 1–4 and 6, removed duplicate *CCC* 1718 and Irenaeus IV.13.4 summaries from endnotes, and let primary quotations carry their own weight.
8. **M-6 — Binding, source-audit, and bibliography locus reconciliation gaps:**
   - *Finding:* `Matt 6:8`, `Gen 3:5`, `Lev 19:18`, `Rom 1:20`, `1 Cor 12–13`, eight DR verses, `ST I.12.2`, `I.19.7–8`, `I.22.2, 4`, `II-II.19.10–11`, several cited *ST* replies, *Spe salvi* nos. 36–37, and the 1832 French Francis de Sales text were missing from `source-bindings.toml` (and some from `source-audit.md` / `99-references.tex`).
   - *Remediation:* Reconciled every quoted and cited locus across `sections/`, `sections/99-references.tex`, `research/source-audit.md`, and `research/source-bindings.toml` (21 bindings total).

### Minor, Polish, and Series Harmonization
- **m-1:** Harmonized Section 5 suffering boundaries to `"Five boundaries"` with `"Fifth, no human being can ever merit the first grace"`.
- **m-2:** Added the clinical-depression and medical/pastoral-care safeguard directly inside Section 4's body (point of use) alongside Appendix B.
- **m-3:** Added Hebrew Psalm equivalents on first citation for `Ps 15:2 DR [Heb. 16:2]` and `Ps 102:5 DR [Heb. 103:5]`.
- **m-4:** Logged all remaining OCR normalizations in `research/source-audit.md` (`then-`->`then,`, `ir`->`in`, CSEL `u`->`v` throughout, line-break splits) and corrected mid-sentence quotation endings (`ST I-II.3.8`, `ST III.80.4`, `ST I-II.114.5 ad 2`, Bernard chs. VII/IX/XI, and `[S]uffice` in Augustine *City of God* XXII.30).
- **m-5:** Corrected `licence` -> `license` (Section 3) and harmonized `Isaiah` -> `Isaias` (Section 2).
- **m-6 & m-7:** Added `\Needspace{16\baselineskip}` before Section 4's `threestable` and `\Needspace{8\baselineskip}` before Appendix B's editions subheading; prose trims eliminated Section 6's sparse trailing spillover page (27 -> 26 pages total).
- **P-1, P-2, P-3:** Trimmed gratuitous `not X, but Y` contrasts, removed evaluative stage-direction adjectives (`razor-sharp`, `lapidary`, `unforgettable`, `crystalline`, `bracing`, `unflinching`, `clinical`, `luminous`, `unfalsifiable`) and full-sentence rhetorical italics, glossed *De Revelatione*, *De Spiritu et Littera*, and *sed contra* on first occurrence, and noted Patmore's 1884 volume title in the first Bernard endnote.
- **Series harmonization:** Confirmed uniform lowercase divine pronouns in body prose outside verbatim quotations, standardized all block quotations from `\begin{primaryquote}` to `\begin{quote}`, and removed the now-empty `format.tex`.

## Post-Remediation Verification
- All five `tools/check-content-preflight` checks run individually (`references-used`, `bindings-valid`, `house-voice`, `restricted-not-reproduced`, `structural-meta-labels`), plus `tools/document-types refresh`, `tools/document-schema check`, `tools/check-generation-metadata`, `tools/check-web-edition`, `tools/web-edition`, and `tools/print-document build`: **all exit 0**.
