# Scope: The City of Unseen Spirits

## Recorded Deliverable (2026-11-25)

An authoritative, original Gemini Catholic angelology reference work at `src/gemini/theology/angelology/` (kind `angelology`, document type `theology-reference-v1`), governed by `guidance/editorial.md`, `guidance/the-shape.md`, `guidance/document-schemas.md`, and `guidance/theology/angelology.md`. It follows St. Thomas Aquinas's *Summa theologiae* I, qq. 50–64 and 106–114 as its systematic spine, expounds all fifteen chapters of Pseudo-Dionysius's *Celestial Hierarchy* in order, treats the pre-Christian writings received and corrected by the Fathers alongside expansive patristic exposition, engages later Catholic schools and the Byzantine trajectory, documents the Roman and Byzantine liturgical calendars and Church regulation of angelic names, presents saints' devotion as pious tradition, and supplies complete synchronized research records and terminal reference appendices.

## Question, Reader, and Organizing Thesis

**Governing question:** What does Catholic faith, rooted in Sacred Scripture, unfolded by the Fathers and the *Celestial Hierarchy*, and ordered by St. Thomas Aquinas, teach about the nature, knowledge, freedom, grace, fall, hierarchy, ministry, and worship of the holy angels?

**Intended reader:** Serious Catholic lay readers, seminarians, catechists, and students of theology who wish to understand and pray within the Church's tradition, willing to engage precise philosophical and patristic distinctions supported by verified primary references.

**Organizing thesis:** Angelic greatness is altogether creaturely and Christ-centered: pure immateriality is not divinity, natural intellectual brilliance is not the beatific vision, hierarchical governance does not rival God's sovereignty, and all good angels belong with redeemed humanity to the one City of God under Jesus Christ, their Head.

## Corpus and Completeness Rule

- **Systematic spine:** *Summa theologiae* I, qq. 50–64 (72 articles) and I, qq. 106–114 (46 articles) — all **118 articles** — supplemented by *ST* III, q. 8, a. 4 and III, q. 30, aa. 1–4, plus directly inspected parallels in *De malo* q. 16 (aa. 1–12), *De veritate* qq. 8–9, *De ente et essentia* chs. 4–5, and *Super Ephesios* / *Super Colossenses* (Dessain 1857 OCR finding aid). Completeness means every one of the 118 articles appears exactly once in `research/question-inventory.md` and `appendices/03-article-census.tex`, verified for 100% 1-to-1 parity by `.scratch/lanes/lane-3/check_census.py`.
- **Celestial Hierarchy:** All fifteen chapters of Pseudo-Dionysius's *De caelesti hierarchia* expounded in exact order with Parker (1899) chapter titles, Migne PG 3 column bounds (verified against tracked PG 3 OCR), focused checked quotations, and exact *Summa* reception loci.
- **Pre-Christian, Patristic, Magisterial, Scholastic, Byzantine, Liturgical, and Saintly witnesses:** Grounded strictly in verified local artifacts under `src/sources/` (121 bound artifacts/segments/passages in `research/source-bindings.toml`). Where a relevant work is cataloged or restricted in the source library without local text bytes (e.g., *1 Enoch*, Philo, Hesiod, Scotus's *Ordinatio*, Suárez's *De angelis*, Gregory Palamas, modern Vatican documents), no verbatim quotation is invented; the boundary is disclosed honestly in `research/source-audit.md` and Appendix J.
- **Exclusions:** This is not a manual of exorcism, deliverance instruction, case discernment, or catalogue of extra-biblical angel names. Liturgical rites, canonical discipline, and pastoral practice concerning demonic affliction belong to the separate study of Catholic exorcism (`history/catholic-exorcism/`).

## Authority Grading Rule

Proposition grades describe the doctrinal standing of a specific claim, never the authority of an author as a whole, following `guidance/theology/angelology.md`:

- **Defined** — taught by an ecumenical council definition or solemn profession of faith (e.g., Nicene Creed, Lateran IV *Firmiter credimus*, Florence, Vatican I *Dei Filius*, Constantinople 543/553).
- **Church teaching** — taught by the ordinary magisterium, universal catechisms (*Roman Catechism*, *Catechism of the Catholic Church*), papal acts, or universal liturgical confession without a solemn definition.
- **Common teaching** — commonly held by the Church Fathers and Catholic theologians.
- **Thomist position** — St. Thomas Aquinas's distinctive systematic determination within Catholic orthodoxy (naming contrary Catholic schools where verified).
- **Disputed** — an actual open disagreement among identified Fathers or Catholic schools without a prevailing common resolution (I q. 61 a. 3; I q. 62 a. 3; I q. 108 a. 6; I q. 113 a. 5).
- **Pious tradition** — Catholic devotional practice, hagiography, and saintly accounts received in the spiritual life of the Church.
- **Apocryphal** — extra-canonical Second Temple Jewish writings (*1 Enoch*, *Jubilees*, *Testaments of the Twelve Patriarchs*).

Grade assignments represent source-grounded editorial synthesis; compact question dossiers and the terminal census carry the grades while body prose states each teaching affirmatively at its proper degree in the verb.

## Translation, Rights, and Received-Prayer Policy

- English Scripture quotations reproduce the public-domain Douay-Rheims (Challoner) text tracked in `src/sources/bibles/douay-rheims/`, citing Vulgate numbering with Hebrew or modern Greek numbering in brackets where different.
- Septuagint English quotations reproduce Sir Lancelot Brenton's public-domain 1851 translation; Greek Psalms are checked against H. B. Swete (CC-BY-SA-4.0 First1KGreek digitisation).
- Patristic and medieval English quotations come from unrevised public-domain printings tracked in `src/sources/works/` (ANF/NPNF CCEL, Dods 1871, Library of the Fathers, Parker 1899, 1920 English Dominican *Summa*). The two tracked witnesses derived from New Advent modernized web revisions (Origen *In Matt.* XIII.26–29; Augustine *De Trinitate* III.4–9) are paraphrased cleanly rather than presented as unrevised nineteenth-century printings.
- Received vocal prayers printed for recitation (*Angele Dei* from the 1910 *Raccolta* No. 296; Leo XIII's St. Michael prayer from 1945 Lasance p. 797) reproduce verified public-domain witnesses verbatim without composition or adaptation.
- Restricted modern Vatican and ICEL liturgical texts are paraphrased rather than reproduced. Project-authored prose is licensed under CC BY 4.0; incorporated external texts retain their own public-domain or third-party status.

## Limits and Review Facts

- **Provider & Leaf:** `gemini`, `src/gemini/theology/angelology/`, profile `guidance/theology/angelology.md`, document type `theology-reference-v1`.
- **Verification completed:** 118-article census 1-to-1 parity check (`check_census.py`), 121-binding library fingerprint validation (`bindings-valid`), `document-schema check`, `check-generation-metadata`, `check-web-edition`, `house-voice` preflight, and compiled PDF visual inspection.
- **Review boundary:** This reference work is an AI-assisted study aid; it carries no independent human theological review, ecclesiastical *imprimatur*, or magisterial authority, and does not substitute for official liturgical books, catechisms, or competent pastoral counsel.
