# Scope: The Seven Sacraments

## Recorded Deliverable (2026-11-27)

Two linked Catholic theological reference publications under the `gemini` provider branch, governed by `guidance/editorial.md`, `guidance/the-shape.md`, `guidance/document-schemas.md`, `guidance/web-editions.md`, and `guidance/theology/sacramental-reference.md`:

1. **Canonical Treatise:** `src/gemini/theology/sacraments/` (kind `sacraments`, document type `theology-reference-v1`, generated `main.tex`), owning all shared fragments (`format.tex`, `summary-preamble.tex`, `fragments/full-matrix.tex`, `fragments/lexicon.tex`, `sections/14-churches-initiation.tex`, and the seven one-page summaries under `summaries/*.tex`).
2. **Mechanically Derived At-a-Glance Companion:** `src/gemini/theology/sacraments-at-a-glance/` (kind `sacraments-summary`, hand-written `main.tex` with `\AIInheritedGenerationMetadata{theology/sacraments}`), importing strictly the master matrix, metaphysical lexicon, seven canonical one-page summaries, and twenty-four-Church initiation table in retrieval order with zero independent theological prose.

## Question, Reader, and Organizing Thesis

**Governing question:** What does Catholic faith—rooted in Sacred Scripture, unfolded by the Church Fathers, ordered systematically by St. Thomas Aquinas, defined by the ecumenical councils, and regulated by Latin and Eastern canon law—teach concerning the nature, constitution, causality, grace, ends, and liturgical celebration of the seven sacraments of the New Law?

**Intended reader:** Serious Catholic lay readers, catechists, seminarians, and students of theology seeking a clear, source-disciplined, tradition-inhabiting reference spanning both Western scholastic rigor and the liturgical patrimony of all twenty-four Catholic Churches *sui iuris*.

**Organizing thesis:** Every sacrament of the New Law proceeds from Christ's pierced side as an efficacious sensible instrument of His glorified humanity, commemorating His Passion, conferring proper sanctifying grace and ecclesial configuration in the present, and pledging future glory. Across the sevenfold organism—Initiation, Healing, and Service of Communion—Baptism opens the gate and the Eucharist stands as the substantial center and summit.

## Corpus, Required Structure, and Completeness Rules

- **Continuous body order:**
  1. Sacraments of Christian Initiation (`sections/10-initiation-introduction.tex`, `11-baptism.tex`, `12-confirmation.tex`, `13-eucharist.tex`)
  2. Sacraments of Healing (`sections/20-healing-introduction.tex`, `21-penance.tex`, `22-anointing.tex`)
  3. Sacraments at the Service of Communion (`sections/30-communion-introduction.tex`, `31-orders.tex`, `32-matrimony.tex`)
  4. Concluding Theological Synthesis (`sections/40-synthesis.tex`)
  5. Complete Bibliography (`sections/90-references.tex`), immediately preceding the terminal appendices.
- **Terminal appendices (exact required order per `guidance/theology/sacramental-reference.md`):**
  1. `Scope, Terms, and Qualifications` (`sections/91-scope-terms-qualifications.tex`), importing the single authoritative `fragments/lexicon.tex`.
  2. Seven-Sacrament Comparative Matrix (`fragments/full-matrix.tex`).
  3. Twenty-Four Catholic Churches *sui iuris* Initiation Table (`sections/14-churches-initiation.tex`), covering the Latin Church plus all 23 Eastern Catholic Churches across the five traditions of CCEO c. 28 §2 (`1 + 3 + 3 + 1 + 2 + 14 = 24`; post-2015 census including the Eritrean Metropolitan Church *sui iuris* and the elevated Hungarian Greek Catholic Metropolitan Church *sui iuris*).
  4. Seven structurally uniform **strictly one-page** summaries (`summaries/{baptism,confirmation,eucharist,penance,anointing,orders,matrimony}.tex`) in canonical order.
  5. Generation metadata (`generation-metadata.tex`) and universal rights colophon (`\TriptychRightsNotice`) last.
- **Per-sacrament analytical completeness:** Every full chapter, comparative matrix row, and one-page summary explicitly identifies matter or quasi-matter, form, capable subject, ordinary and extraordinary minister (with ecclesial intention and jurisdiction where applicable), intermediate reality (*res et sacramentum*), proper grace (*res tantum*), principal effects, the exact formal/relational/substantial change involved, and primary proper, intrinsic secondary, contingent, and ultimate ends. Eucharistic transubstantiation is kept strictly distinct from both the determining words of consecration and any change of sensible accidents.

## Source Hierarchy, Rights, and As-Of Bounds

- **Scripture:** Douay-Rheims (Challoner) public-domain text tracked in `src/sources/bibles/douay-rheims/` with Clementine Vulgate (`src/sources/bibles/clementine-vulgate/`) as Latin control; Vulgate vs. Greek/Hebrew verse divergences (such as John 6:54 vs. 6:53 and Acts 14:22 vs. 14:23) are disclosed locally.
- **Patristic, Medieval, and Historical Magisterium:** Direct block quotations come strictly from verified public-domain printings tracked locally under `src/sources/works/` (ANF1 CCEL, NPNF1/2 CCEL unrevised printings, Dods 1871 & CSEL 40 *De civitate Dei*, Oxford 1842 *Catena Aurea*, 1920 English Dominicans *Summa theologiae* III, Lateran IV *Firmiter* Latin, Council of Trent Tauchnitz 1887 Latin verified passages, the collated *Roman Catechism* Donovan 1829 satisfaction passage, and Leo XIII *Arcanum Divinae* and *Apostolicae Curae* in the 1903 Benziger edition). Uncollated OCR finding aids and New Advent modernized web revisions of the Fathers are never presented as verified verbatim block quotations.
- **Modern Magisterium & Canon Law:** Vatican II, *Catechism of the Catholic Church*, CIC 1983, CCEO 1990, and papal acts after Leo XIII are `restricted` in `src/sources/` and are paraphrased accurately rather than reproduced in block quotation; copyrighted ICEL English liturgical translations (2010/2011 Roman Missal consecration words; 1983 Pastoral Care of the Sick) and CCC 1524 prose are excluded in favor of official Latin *editio typica* formulas and descriptive prose, while short essential Latin/Catechism formulas carry explicit Vatican web vs. USCCB edition caveats where wording diverges (CCC 1300, 1449). Where a cited historical document (such as Trent Session VII canons, *Ordinatio Sacerdotalis* standalone, the 1996 Eastern Liturgical *Instruction*, or individual Eastern particular-law initiation codes) lacks locally tracked text or passage records in `src/sources/`, that evidence boundary is stated explicitly in `research/source-audit.md` without fabricated quotations.
- **As-of date & Jurisdiction:** Canonical and twenty-four-Church census statements reflect universal Latin (CIC 1983) and Eastern (CCEO 1990) law and subsequent papal amendments verified through November 2026. Particular diocesan, eparchial, and synodal norms govern local celebration.

## Review Boundary

This treatise and its at-a-glance companion are AI-assisted study aids verified mechanically across schema, metadata, source-library bindings, house voice, reference usage, web conversion, PDF anchor alignment, and native `wasmtex` print rendering (including visual inspection of every one-page summary and landscape matrix). They carry no independent human theological review, ecclesiastical *imprimatur*, or canonical authority.
