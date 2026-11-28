# Source Audit: Against the Instrumentalists

- **Audit Date:** 2026-11-28
- **Publication Leaf:** `src/gemini/articles/faith/against-the-instrumentalists`
- **Provider Independence:** Independent Gemini authoring; zero inspection or reuse of sibling provider drafts.

## 1. Locally Verified Public-Domain Primary Sources (Verbatim Quotations Checked)

Every verbatim quotation printed in `sections/*.tex` was read directly from a tracked public-domain file under `src/sources/works/` and verified at its exact locus on 2026-11-28:

| Source | Artifact / Segment ID | Exact Loci Verified | Verification Notes |
| --- | --- | --- | --- |
| Challoner Douay-Rheims Bible (Wisdom) | `artifact.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581.verse-text-25-wisdom-2fe4073b` | Wis 11:21; 13:1–9 | Read directly in tracked `25-wisdom.tsv`; quoted verbatim in Sections 1 and 6. |
| Challoner Douay-Rheims Bible (Romans) | `artifact.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581.verse-text-52-romans-4d45c497` | Rom 1:18–25 | Read directly in tracked `52-romans.tsv`; quoted verbatim in Section 6. |
| Clementine Vulgate (Wisdom) | `artifact.catholic-church.vulgata-clementina.ebible-latvuc.verse-text-25-wisdom-bfeace21` | Wis 11:21; 13:1–9 | Checked directly in tracked Latin corpus for key terms (`in mensura, et numero et pondere`; `cognoscibiliter`; `aestimare saeculum`). Standard typographic normalization expands Vulgate `æ` ligatures to `ae`. |
| Clementine Vulgate (Romans) | `artifact.catholic-church.vulgata-clementina.ebible-latvuc.verse-text-52-romans-b5092f0e` | Rom 1:18–22 | Checked directly in tracked Latin corpus for Rom 1:19–20 (`Invisibilia enim ipsius ... intellecta, conspiciuntur`). Standard typographic normalization expands Vulgate `æ` ligatures to `ae`. |
| G. K. Chesterton, *Orthodoxy* (1908) | `artifact.g-k-chesterton.orthodoxy.gutenberg-ebook-16769.gutenberg-pg16769-body-lf` | Ch. 2 ("The Maniac"), Ch. 3 ("The Suicide of Thought") | Read directly in tracked `orthodoxy.txt` (lines 40–95); verbatim quotations in Section 2 checked word-for-word (with `[t]here` bracketed for sentence-initial case shift). |
| St. Thomas Aquinas, *Summa Theologiae*, Prima Pars | `artifact.thomas-aquinas.summa-theologiae.2006-english-dominicans-gutenberg-prima.pg17611-body-9c99a67a` | I, q. 1, a. 8; q. 2, aa. 1–3; q. 3, a. 1; q. 12, aa. 12–13; q. 79, a. 3; q. 84, aa. 6–7; q. 85, a. 1 | Read directly in tracked `source.txt`; verbatim quotations in Section 5 verified word-for-word against English Dominican text (Project Gutenberg eBook 17611, with disclosed electronic-editor revisions by Sandra K. Perry and David McClamrock). |
| St. Augustine, *Confessions* | `segment.augustine-of-hippo.confessiones.ccel-web-2026-10-13.complete-work` | Book X, ch. 6, §§9–10 | Read directly in tracked CCEL NPNF1-1 text (lines 13610–13715); Pilkington translation quoted verbatim in Section 5. |
| St. Augustine, *On the Trinity* (*De Trinitate*) | `artifact.augustine.de-trinitate.1887-haddan-english-web-2026-09-29.complete-page-text-07b2f4f0` | Book III, ch. 3 | Read directly in tracked `source.txt` (line 31); Haddan 1873 translation revised by W. G. T. Shedd in NPNF1-3 (1887), New Advent web transcription (uncollated against print), quoted verbatim in Section 5 with `[O]ne` bracketed and full concluding clause retained. Tracked artifact covers Book III only. |
| St. John Henry Newman, *Parochial and Plain Sermons*, Vol. 1 (1869) | `artifact.john-henry-newman.parochial-and-plain-sermons.rivingtons-1869-volume-1.ia-ocr-9947fafd` | Sermon XV (pp. 191–195); Sermon XVII (p. 225) | Read directly in tracked `source.txt` (lines 7030–7490, 7920–8350). Quoted passages in Sections 2 (pp. 191–192) and 5 (p. 225) verified free of OCR defects; OCR-noisy island-testimony paragraph (pp. 194–195, `tlicn`) paraphrased rather than quoted verbatim. Historical provenance (preached in Newman's Anglican ministry, 1825–1843, and republished unaltered by W. J. Copeland at Rivingtons in 1868/1869 with Copeland's preface disclaiming Catholic-era re-assertion of every passage) documented in endnote, Scope appendix, and References. |
| First Vatican Council, *Dei Filius* (1870) — Latin | `artifact.first-vatican-council.dei-filius.latin-vatican-web-2026-07-24.historical-latin-text-1577b504` | Chs. 1, 2, 4; Canons I.2, II.1 | Read directly in tracked `source.txt` (lines 1–121); Latin phrasing verified verbatim in Section 6 endnotes. |
| First Vatican Council, *Dei Filius* (1870) — English | `segment.first-vatican-council.dei-filius.1912-devin-adair-manning-english.complete-english-ocr` | Chs. 1, 2, 4; Canons I.2, II.1 (pp. 220–221, 228–234) | Read directly in tracked container `text.txt` (lines 6603–7402); Cardinal Manning translation quoted verbatim in Section 6, checked against Latin original; exact pages verified (`mutual aid` p. 231, `Nor does the Church forbid...` p. 232). |
| Pope Leo XIII, *Aeterni Patris* (1879) — Latin | `artifact.papal.leo-xiii.hf-l-xiii-enc-04081879-aeterni-patris.2026-10-26-vatican-la.latin-text-1a714f0fff76` | Unnumbered Latin `text.txt` (Wis 13 paragraph and physical-sciences paragraphs) | Read directly in tracked `text.txt` (lines 1–69); Latin control checked beside Benziger English. |
| Pope Leo XIII, *Aeterni Patris* (1879) — English | `segment.papal.leo-xiii.hf-l-xiii-enc-04081879-aeterni-patris.1903-benziger-english.benziger-english-transcription` | pp. 38, 55 (whole encyclical pp. 34–57; reading-text lines 139, 187–189) | Read directly in tracked container `great-encyclical-letters-reading-text.txt` and cross-checked for exact Benziger 1903 pagination against sibling tracked Wikisource HTML artifacts (`ws-chapter-03-13bb0856` and `ws-chapter-04-934b7793`, preserving `data-page-number` markers); quoted verbatim in Section 6. |
| Pope St. Pius X, *Pascendi Dominici Gregis* (1907) — Latin | `artifact.papal.pius-x.hf-p-x-enc-19070908-pascendi-dominici-gregis.2026-10-26-vatican-la.latin-text-cc267546aed0` | Unnumbered Latin `text.txt`, lines 13–15 (corresponding to standard nn. 6–7) | Read directly in tracked `text.txt`; Latin control checked beside 1908 English. |
| Pope St. Pius X, *Pascendi Dominici Gregis* (1907) — English | `segment.papal.pius-x.hf-p-x-enc-19070908-pascendi-dominici-gregis.1908-programme-modernism-english.complete-english-reading` | pp. 181, 183, 185 (lines 45–63) | Read directly in tracked container `text.txt` and cross-checked for exact pagination against sibling `raw-ocr-24bb7557577b/text.txt`; quoted verbatim in Section 6 (preserving original British spelling `recognising` while normalizing OCR line-break splits and pre-colon/semicolon spaces in `atheistic:` and `phenomena;` consistently with Newman and *Dei Filius*). |

## 2. Cataloged Restricted / Copyrighted Magisterial Sources (Zero Verbatim Quotation)

The following official texts carry restricted Vatican copyright and are bound strictly at the edition level (`role = "bibliographic"`, `states = ["cataloged"]`), engaged solely in original doctrinal paraphrase with zero verbatim reproduction:

- Second Vatican Council, *Gaudium et spes* (nos. 36, 57) — `edition.second-vatican-council.gaudium-et-spes.english-vatican-web-2026-07-23`
- *Catechism of the Catholic Church* (nos. 31–39) — `edition.catholic-church.catechism.english-vatican-archive-2003`
- Pope St. John Paul II, *Fides et ratio* (nos. 55, 67, 83, 88) — `edition.papal.john-paul-ii.hf-jp-ii-enc-14091998-fides-et-ratio.2026-10-26-vatican-en`

## 3. Untracked Modern Philosophical, Metrological, and Scientific Works (Historical-Analysis Boundary)

The following works are not held as tracked text artifacts under `src/sources/works/` and are therefore engaged exclusively in accurate analytical prose with standard bibliographic citations and **zero verbatim quotation**:

- David Hume, *An Enquiry Concerning Human Understanding* (1748), Sections IV and XII
- Auguste Comte, *Cours de philosophie positive* (1830–1842), Lessons 1 and 19
- Pierre Duhem, *La théorie physique* (1906)
- Hans Hahn, Otto Neurath, and Rudolf Carnap, *Wissenschaftliche Weltauffassung: Der Wiener Kreis* (1929)
- Karl R. Popper, *Logik der Forschung* (1934) / *The Logic of Scientific Discovery* (1959) and *Conjectures and Refutations* (1963)
- A. J. Ayer, *Language, Truth and Logic* (1936; 2nd ed., 1946)
- Alonzo Church, review of Ayer (2nd ed.), *Journal of Symbolic Logic* 14 (1949): 52–53 (formal proof independently verified in propositional logic)
- Carl G. Hempel, "Problems and Changes in the Empiricist Criterion of Meaning," *Revue Internationale de Philosophie* 4 (1950): 41–63
- W. V. O. Quine, "Two Dogmas of Empiricism," *Philosophical Review* 60 (1951): 20–43
- Bas C. van Fraassen, *The Scientific Image* (1980)
- Joint Committee for Guides in Metrology (JCGM), VIM and GUM (conceptual metrological vocabulary)
- Stephen Hawking and Leonard Mlodinow, *The Grand Design* (2010), ch. 1
- Lawrence M. Krauss, *A Universe from Nothing* (2012)

## 4. Negative Results and Open Limitations

- The tracked Latin witness of St. Thomas Aquinas's *Summa Theologiae* Prima Pars (`sth1050-historical-latin-3e44340c`) covers only qq. 50–64, leaving qq. 1–49 (beyond the opening of q. 1, a. 1) and qq. 79, 84, and 85 absent locally in Latin; therefore all Prima Pars citations rely on the verified public-domain English Dominican Gutenberg text (`pg17611-body-9c99a67a`), while standard Latin technical phrases (*demonstratio quia*, *praeambula fidei*, *intellectus agens*, *conversio ad phantasmata*) are used in ordinary philosophical exposition rather than quoted as a collated Leonine witness.
- The tracked public-domain witness of St. Augustine's *De Trinitate* (`complete-page-text-07b2f4f0`) covers Book III only; accordingly, only Book III, ch. 3 is cited verbatim.
- All bibliographic entries in `sections/99-references.tex` correspond directly to works cited in the body or endnotes.
