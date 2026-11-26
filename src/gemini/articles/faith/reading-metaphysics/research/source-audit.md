# Source Audit: Reading Metaphysics

**Audited:** 2026-11-26  
**Scope:** Every primary quotation, Latin text, English rendering, Bekker pagination, historical attribution, and scholarly reference appearing in `src/gemini/articles/faith/reading-metaphysics/`.

## 1. Tracked Local Repository Artifacts Directly Inspected (`states = ["cataloged", "inspected"]`)

| Source ID (Artifact) | Canonical `source_fingerprint` | Loci Verified | Rights Status |
|---|---|---|---|
| `artifact.thomas-aquinas.summa-theologiae.2006-english-dominicans-gutenberg-prima.pg17611-body-9c99a67a` | `sha256:c17b98dc58cabd0086fc556359882738be070d90f21f2dbaebe7f8676128b3e7` | *ST* I, q. 1 aa. 2, 8; q. 2 aa. 1–3; q. 3 aa. 1–4; q. 4 a. 1; q. 8 a. 1 (Phase 1 transfer); q. 9 a. 1 (final pencil test); q. 13 aa. 3, 5; q. 14 a. 1; q. 44 aa. 1–2; q. 46 aa. 1–2 | Public domain (Benziger / Project Gutenberg eBook 17611) |
| `artifact.thomas-aquinas.de-ente-et-essentia.1933-latin-corpus-thomisticum-2026-09-29.oee-historical-latin-aa6b1de0` | `sha256:abc4c485ce30b7b7ffa6d89b54f682f54383016890362e88c3e95aee6ce11ac6` | *De ente et essentia* c. 1, c. 4 (verbatim Latin verified) | Public-domain medieval Latin text (Baur 1933 / Koch / Corpus Thomisticum) |

## 2. Cataloged Contextual Repository Witnesses (`states = ["cataloged"]`)

These registered repository editions and works are bound strictly at catalog level (`role = "context"`, `states = ["cataloged"]`) to match `research/source-bindings.toml`:

| Source ID | Bound Loci | Contextual Role |
|---|---|---|
| `edition.john-of-damascus.de-fide-orthodoxa.1899-salmond-english-web-2026-09-29` | `I.1`, `I.3` | Background witness for the patristic maxim quoted inside *ST* I, q. 2, a. 1, Obj. 1 and qualified in Reply 1 (Lesson 2, Worked Passage 2). |
| `edition.aristotle.ethica-nicomachea.english-ross-1925-mit-web-2026-07-27` | `VI.3, 1139b18-1139b22`, `VI.6, 1140b31-1141a8` | Background witness for Aristotle's *episteme* and *nous* cited in Lessons 0, 6, and Appendix A. |
| `work.thomas-aquinas.summa-contra-gentiles` | `I.13` | Parallel ordered-movers and ordered-efficient-causes discussions (*SCG* I, c. 13, nn. 14, 15, 33) noted in Lessons 4, 7, 8, and Appendix A. |

## 3. Primary Texts Verified via Critical Editions and Governing Specifications

- **Aquinas, *Summa Theologiae*, Prima Pars (Leonine Vol. IV, Rome 1888, via Corpus Thomisticum):** Verbatim Latin verified for *ST* I, q. 2, a. 1 (arg. 2, corp., ad 2); q. 2, a. 2 (corp., ad 1, ad 2); q. 2, a. 3 (First Way & Second Way, normalized to Leonine punctuation); q. 13, a. 5 (*inter puram aequivocationem et simplicem univocationem*); q. 46, a. 2 (title, arg. 7, corp. opening, and complete ad 7 including *martellis* and *a corpore elementari, et a sole*).
- **Aquinas, *Summa contra Gentiles* I (Leonine, Turin 1961):** Verified *SCG* I, c. 3 (*duplex veritatis modus*), cc. 10–11, c. 13 **nn. 14, 15, and 33** (n. 14 ordered movers, n. 15 instrumental movers, n. 33 ordered efficient causes), and cc. 14–28.
- **Aquinas, *In PA* (I, lect. 2; II, lect. 1, 7, 9) and *Super Boetium De Trinitate* (q. 5, a. 3; q. 6, a. 4, ad 2):** Verified against `DOCUMENT-SPEC.md` Appendix A §A.3; unused *In Metaph.* Prooemium and uncited *De Trin.* sub-loci removed from reader-facing References and Appendix A.
- **Aristotle, *Posterior Analytics* (Mure Oxford 1928), *Prior Analytics* (Jenkinson Oxford 1928), *Topics* (Pickard-Cambridge Oxford 1928), *Metaphysics* (Ross Oxford 1924):** Verbatim Mure quotation of I.2 (71b17–25) and I.13 (78a30–38) verified; Bekker pagination strictly governs and was audited during cold review (`Post. An.` I.30 corrected to `87b19–27`; `Prior An.` corrected to `I.1, 24b18–20`; `Metaph.` Gamma 4 capped at `1009a5`; `Post. An.` II.16 `98b4–10` used cleanly in Exercise 6.2).
- **Bl. John Duns Scotus, *Ordinatio* I, d. 3, p. 1, qq. 1–2, n. 26 (Vatican ed.):** Verbatim Latin verified for Lesson 7 comparative burden analysis.
- **David Hume, *Dialogues Concerning Natural Religion*, Part IX (1779, public domain):** Verbatim text of Cleanthes on the twenty particles of matter verified for Lesson 7 comparative burden analysis.

## 4. Material Corrections Applied During Audits

1. ***ST* I, q. 2, a. 1 — Damascene's location:** Confirmed in **Objection 1** (answered in Reply 1), not *sed contra* (which cites Aristotle *Metaph.* IV and Ps. 52:1).
2. ***SCG* I, c. 13 — n. 14 vs. n. 15:** Confirmed n. 14 = ordered movers, n. 15 = instrumental movers, n. 33 = ordered efficient causes.
3. ***ST* I, qq. 3–11 vs. q. 14:** Divine entitative attributes = qq. 3–11; divine knowledge = q. 14.
4. **Aristotle Bekker pagination fixes (cold review B2):** *Post. An.* I.30 = `87b19–27` (not `88a5–17`, which is I.31); *Prior An.* `24b18–20` = **I.1** (not I.2); *Metaph.* Gamma 4 ends at `1009a5` (not `1011a5`, which runs into Gamma 5–6).
5. **All Appendix A §A.5 correction notes enforced:** Deciduousness in Book II (`98b4–10`, never I.13); twofold prior knowledge in I.1; *separatio* distinct from manuals' "three degrees of abstraction"; *quinque viae* kept as *viae*; *subalterna* not attributed to *ST* I q. 1 a. 2; Anselm noted as unnamed in *ST* I q. 2 a. 1; analogical four-term problem attributed to Cajetan (1498).

## 5. Excluded Unverified Leads

Per `DOCUMENT-SPEC.md` Appendix A §A.6, the following unchecked items are excluded from all reader-facing prose and references:
- Aquinas, *In Phys.* VIII; *SCG* II, c. 38; *De ver.* q. 10, a. 12; unverified composition dates of *In PA* or *ST* I.
- Aristotle, *Topics* VIII.5, 159b4ff.
- Unchecked manual pages or page-level citations to Garrigou-Lagrange, Maritain, Boyer, Gredt, and unchecked page-level arguments of secondary scholars.
