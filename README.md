# Liturgical Year TLM Mass Preparation Guides

This project builds printable preparation guides for advanced lay readers of the traditional Roman Mass propers together with source documents that supply their sacramental theology. The present set covers Trinity Sunday and the Second through Seventh Sundays after Pentecost in the 1962 temporal cycle, the 1962 Nuptial Mass, and a full patristic and Thomistic reference work on the seven sacraments.

These are not homiletic sketches. They are layered study instruments for use before Mass: each guide places the appointed Scriptures in their human and salvation-historical settings, then helps a reader see how the chants, orations, Epistle, Gospel, altar texts, and sacramental conclusion form one symbolic and theological whole.

The guides are aids for liturgical study, prayerful preparation, and attentive participation. They are not critical editions, official liturgical texts, or substitutes for checking the cited primary sources and an edition-identified 1962 missal facsimile.

**Editorial status:** mixed-maturity working drafts. The linked patristic translations have been checked for the claims presently made, but the existing Latin has not uniformly received the public, line-by-line facsimile collation now required below or an external theological review. The guide-by-guide evidence state is recorded below.

## Guide Status and Canonical Sunday Order

The catalog uses the 52 Sunday identities of the 1962 Roman temporal cycle, rotated so that the First Sunday of Lent is `01`. This is a stable repository order, not the occurrence schedule of one civil year. Under the 1962 *Missale Romanum*, *Rubricae generales* 17–18, omitted Third through Sixth Sundays after Epiphany may be resumed after the Twenty-third Sunday after Pentecost, while the formulary printed as the Twenty-fourth and Last Sunday after Pentecost always remains last. Those resumed uses remain attached to their Epiphany identity below, but each requires a separately generated and evaluated variant because it uses the chants of the Twenty-third Sunday after Pentecost with its own Epiphany orations, Epistle, and Gospel. See the public [1962 missal facsimile](https://media.churchmusicassociation.org/pdf/missale62.pdf), especially the General Rubrics and printed pp. 418–424.

The status codes record evidence, not aspirational quality scores:

- **Generation:** `G0` not generated; `G1` legacy AI-assisted generation whose exact model, agent, and runtime were not recorded; `G2` `gpt-5.6-sol`, `reasoning=ultra`, OpenAI Codex agents, Codex CLI `0.144.1`, API workspace; `G3` substantial revision by OpenAI Codex agents on a GPT-5-based runtime, with the exact model identifier and reasoning profile unexposed, Codex CLI `0.144.1`, API workspace.
- **Text/source evaluation:** `S0` none; `S1` internal source check recorded in the guide, but repository propers and public-facsimile recollation remain pending; `S2` stored retrieval and verified propers, every appointed principal, seasonal, and ritual element facsimile-collated, with an internal source-and-claim audit.
- **Theological evaluation:** `T0` no independent theological review recorded; `T1` independent theological review completed against the identified revision. No present guide has reached `T1`.
- **Production evaluation:** `Q0` no artifact; `Q1` tracked PDF using the legacy architecture, without a durable specification-level QA attestation; `Q2` two-pass, warning-checked, visually inspected PDF under the source-audited macro-order that preceded `In Illo Tempore...`; `Q3` current macro-order including the one-page heterogeneous `In Illo Tempore...` table immediately after page 1, two-pass build, warning check, and visual page inspection. The `Q` prefix denotes production QA.

| ID | Temporal Sunday identity | Guide state | Generation | Text/source eval. | Theology | Production |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | First Sunday of Lent | Not started | G0 | S0 | --- | Q0 |
| 02 | Second Sunday of Lent | Not started | G0 | S0 | --- | Q0 |
| 03 | Third Sunday of Lent | Not started | G0 | S0 | --- | Q0 |
| 04 | Fourth Sunday of Lent | Not started | G0 | S0 | --- | Q0 |
| 05 | Passion Sunday | Not started | G0 | S0 | --- | Q0 |
| 06 | Palm Sunday | Not started | G0 | S0 | --- | Q0 |
| 07 | Easter Sunday | Not started | G0 | S0 | --- | Q0 |
| 08 | Low Sunday | Not started | G0 | S0 | --- | Q0 |
| 09 | Second Sunday after Easter | Not started | G0 | S0 | --- | Q0 |
| 10 | Third Sunday after Easter | Not started | G0 | S0 | --- | Q0 |
| 11 | Fourth Sunday after Easter | Not started | G0 | S0 | --- | Q0 |
| 12 | Fifth Sunday after Easter | Not started | G0 | S0 | --- | Q0 |
| 13 | Sunday after the Ascension | Not started | G0 | S0 | --- | Q0 |
| 14 | Pentecost Sunday | Not started | G0 | S0 | --- | Q0 |
| 15 | Trinity Sunday | Historically situated, source-audited working draft ([source](src/gpt/15-trinity-sunday/main.tex); [propers](src/gpt/15-trinity-sunday/propers/verified.md); [scope](src/gpt/15-trinity-sunday/research/scope.md); [PDF](doc/gpt/15-trinity-sunday.pdf)) | G3 | S2 | T0 | Q3 |
| 16 | Second Sunday after Pentecost | Historically situated, source-audited working draft ([source](src/gpt/16-second-after-pentecost/main.tex); [propers](src/gpt/16-second-after-pentecost/propers/verified.md); [scope](src/gpt/16-second-after-pentecost/research/scope.md); [PDF](doc/gpt/16-second-after-pentecost.pdf)) | G3 | S2 | T0 | Q3 |
| 17 | Third Sunday after Pentecost | Historically situated, source-audited working draft ([source](src/gpt/17-third-after-pentecost/main.tex); [propers](src/gpt/17-third-after-pentecost/propers/verified.md); [scope](src/gpt/17-third-after-pentecost/research/scope.md); [PDF](doc/gpt/17-third-after-pentecost.pdf)) | G3 | S2 | T0 | Q3 |
| 18 | Fourth Sunday after Pentecost | Historically situated, source-audited working draft ([source](src/gpt/18-fourth-after-pentecost/main.tex); [propers](src/gpt/18-fourth-after-pentecost/propers/verified.md); [scope](src/gpt/18-fourth-after-pentecost/research/scope.md); [PDF](doc/gpt/18-fourth-after-pentecost.pdf)) | G3 | S2 | T0 | Q3 |
| 19 | Fifth Sunday after Pentecost | Historically situated, source-audited working draft ([source](src/gpt/19-fifth-after-pentecost/main.tex); [propers](src/gpt/19-fifth-after-pentecost/propers/verified.md); [scope](src/gpt/19-fifth-after-pentecost/research/scope.md); [PDF](doc/gpt/19-fifth-after-pentecost.pdf)) | G3 | S2 | T0 | Q3 |
| 20 | Sixth Sunday after Pentecost | Historically situated, source-audited working draft ([source](src/gpt/20-sixth-after-pentecost/main.tex); [propers](src/gpt/20-sixth-after-pentecost/propers/verified.md); [scope](src/gpt/20-sixth-after-pentecost/research/scope.md); [PDF](doc/gpt/20-sixth-after-pentecost.pdf)) | G3 | S2 | T0 | Q3 |
| 21 | Seventh Sunday after Pentecost | Historically situated, source-audited working draft ([source](src/gpt/21-seventh-after-pentecost/main.tex); [propers](src/gpt/21-seventh-after-pentecost/propers/verified.md); [scope](src/gpt/21-seventh-after-pentecost/research/scope.md); [PDF](doc/gpt/21-seventh-after-pentecost.pdf)) | G3 | S2 | T0 | Q3 |
| 22 | Eighth Sunday after Pentecost | Not started | G0 | S0 | --- | Q0 |
| 23 | Ninth Sunday after Pentecost | Not started | G0 | S0 | --- | Q0 |
| 24 | Tenth Sunday after Pentecost | Not started | G0 | S0 | --- | Q0 |
| 25 | Eleventh Sunday after Pentecost | Not started | G0 | S0 | --- | Q0 |
| 26 | Twelfth Sunday after Pentecost | Not started | G0 | S0 | --- | Q0 |
| 27 | Thirteenth Sunday after Pentecost | Not started | G0 | S0 | --- | Q0 |
| 28 | Fourteenth Sunday after Pentecost | Not started | G0 | S0 | --- | Q0 |
| 29 | Fifteenth Sunday after Pentecost | Not started | G0 | S0 | --- | Q0 |
| 30 | Sixteenth Sunday after Pentecost | Not started | G0 | S0 | --- | Q0 |
| 31 | Seventeenth Sunday after Pentecost | Not started | G0 | S0 | --- | Q0 |
| 32 | Eighteenth Sunday after Pentecost | Not started | G0 | S0 | --- | Q0 |
| 33 | Nineteenth Sunday after Pentecost | Not started | G0 | S0 | --- | Q0 |
| 34 | Twentieth Sunday after Pentecost | Not started | G0 | S0 | --- | Q0 |
| 35 | Twenty-first Sunday after Pentecost | Not started | G0 | S0 | --- | Q0 |
| 36 | Twenty-second Sunday after Pentecost | Not started | G0 | S0 | --- | Q0 |
| 37 | Twenty-third Sunday after Pentecost | Not started | G0 | S0 | --- | Q0 |
| 38 | Twenty-fourth and Last Sunday after Pentecost | Not started | G0 | S0 | --- | Q0 |
| 39 | First Sunday of Advent | Not started | G0 | S0 | --- | Q0 |
| 40 | Second Sunday of Advent | Not started | G0 | S0 | --- | Q0 |
| 41 | Third Sunday of Advent | Not started | G0 | S0 | --- | Q0 |
| 42 | Fourth Sunday of Advent | Not started | G0 | S0 | --- | Q0 |
| 43 | Sunday within the Octave of Christmas | Not started | G0 | S0 | --- | Q0 |
| 44 | Holy Family / First Sunday after Epiphany | Not started | G0 | S0 | --- | Q0 |
| 45 | Second Sunday after Epiphany | Not started | G0 | S0 | --- | Q0 |
| 46 | Third Sunday after Epiphany — ordinary form | Not started | G0 | S0 | --- | Q0 |
| 46R | Third Sunday after Epiphany — resumed after Pentecost (conditional) | Not started | G0 | S0 | --- | Q0 |
| 47 | Fourth Sunday after Epiphany — ordinary form | Not started | G0 | S0 | --- | Q0 |
| 47R | Fourth Sunday after Epiphany — resumed after Pentecost (conditional) | Not started | G0 | S0 | --- | Q0 |
| 48 | Fifth Sunday after Epiphany — ordinary form | Not started | G0 | S0 | --- | Q0 |
| 48R | Fifth Sunday after Epiphany — resumed after Pentecost (conditional) | Not started | G0 | S0 | --- | Q0 |
| 49 | Sixth Sunday after Epiphany — ordinary form | Not started | G0 | S0 | --- | Q0 |
| 49R | Sixth Sunday after Epiphany — resumed after Pentecost (conditional) | Not started | G0 | S0 | --- | Q0 |
| 50 | Septuagesima Sunday | Not started | G0 | S0 | --- | Q0 |
| 51 | Sexagesima Sunday | Not started | G0 | S0 | --- | Q0 |
| 52 | Quinquagesima Sunday | Not started | G0 | S0 | --- | Q0 |

The catalog therefore contains 52 numbered Sunday identities and 56 complete formulary variants when all four resumed forms are counted. The `46R`--`49R` entries are variant-status rows, not additional top-level directory numbers; ordinary and resumed editions belong under their shared numbered Sunday directory but must keep separate source, generation, and evaluation records. General-calendar feasts assigned to a Sunday but lacking a stable temporal ordinal are tracked separately:

| ID | Sunday-assigned feast | Occurrence rule | Guide state | Generation | Text/source eval. | Theology | Production |
| --- | --- | --- | --- | --- | --- | --- | --- |
| F01 | Most Holy Name of Jesus | Sunday occurring January 2–5; otherwise January 2 | Not started | G0 | S0 | --- | Q0 |
| F02 | Christ the King | Last Sunday of October; its post-Pentecost ordinal varies | Not started | G0 | S0 | --- | Q0 |

Fixed-date and local feasts that may supersede a second-class Sunday are outside this temporal catalog and require a calendar- and place-specific layer rather than fictitious permanent Sunday numbers.

## Masses Other Than Sunday Masses

This catalog is separate from the temporal Sunday rotation. `M` identifies a ritual, votive, or other non-Sunday guide; it does not assign a liturgical rank or imply that the formulary can replace an occurring Sunday. The occurrence column is part of the source question: a sacramental rite may require the occurring Mass on some days, its own votive formulary on others, or ritual texts inserted into another Mass.

| ID | Formulary or ritual context | 1962 occurrence / use to research | Guide state | Generation | Text/source eval. | Theology | Production |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M01 | Nuptial Mass — *Missa votiva pro sponsis* | II-class votive when permitted; when the blessing is permitted on a Sunday or I-class day, use the occurring Mass with the Nuptial collect and blessings; All Souls and the Sacred Triduum prohibit both | Historically situated, source-audited working draft ([source](src/gpt/m01-nuptial-mass/main.tex); [propers](src/gpt/m01-nuptial-mass/propers/verified.md); [scope](src/gpt/m01-nuptial-mass/research/scope.md); [PDF](doc/gpt/m01-nuptial-mass.pdf)) | G3 | S2 | T0 | Q3 |
| M02 | Mass in the 25th or 50th anniversary of marriage | Votive Mass or permitted commemoration under the printed anniversary rubrics | Not started | G0 | S0 | --- | Q0 |
| M03 | Mass with priestly or diaconal ordination | Occurring or appointed Mass with the ordination rite; Pontifical and Missal must be collated together | Not started | G0 | S0 | --- | Q0 |
| M04 | Mass of episcopal consecration | Pontifical rite and appointed Mass; mandate, consecrators, and proper ritual texts require their own source record | Not started | G0 | S0 | --- | Q0 |
| M05 | Paschal Vigil with adult Christian initiation | Holy Saturday liturgy with Baptism, Confirmation where conferred, and first Eucharist | Not started | G0 | S0 | --- | Q0 |
| M06 | Pentecost Vigil with Baptism | Reduced 1962 Pentecost Vigil formulary; any Baptism associated with it must be sourced separately from the competent Ritual rather than importing the suppressed older extended vigil | Not started | G0 | S0 | --- | Q0 |
| M07 | Mass associated with Confirmation | Occurring Mass or permitted votive context together with the Pontifical / Ritual rite | Not started | G0 | S0 | --- | Q0 |
| M08 | Votive Mass for the Sick | Missal formulary; when Anointing is actually celebrated, the sacramental rite is separately sourced | Not started | G0 | S0 | --- | Q0 |
| M09 | Requiem Mass for burial | Funeral formulary and burial rites; not itself a sacrament, but a major non-Sunday liturgical guide | Not started | G0 | S0 | --- | Q0 |
| M10 | Mass at religious profession | Votive / occurring Mass and the distinct profession rite; profession is not an eighth sacrament | Not started | G0 | S0 | --- | Q0 |

## Sacramental Reference Document

The [full sacramental treatise](src/gpt/sacraments/main.tex) ([research scope](src/gpt/sacraments/research/scope.md); [PDF](doc/gpt/sacraments.pdf)) begins with the formal definition and a seven-sacrament matter–form–minister matrix, defines its metaphysical vocabulary, treats each sacrament through Scripture, patristic reception, and Thomistic synthesis, distinguishes sacramental from substantial form and states what each sign changes, separates outward operation, intermediate sacramental reality, proper grace, primary and secondary ends, and the common ultimate order to God's glory and beatitude, catalogs initiation practice across all twenty-four Catholic Churches *sui iuris*, and gives one reusable one-page summary for every sacrament. Its summary fragments live in `src/gpt/sacraments/summaries/`; ritual-Mass guides import those fragments rather than keeping independent condensed accounts.

The compact [Sacraments at a Glance](src/gpt/sacraments-at-a-glance/main.tex) ([PDF](doc/gpt/sacraments-at-a-glance.pdf)) collects, in order, the same canonical master matrix, metaphysical lexicon, seven one-page sacrament summaries, and twenty-four-Church initiation table. It is a retrieval companion rather than an independent doctrinal authority or research ceiling: its contents are composed directly from the full treatise's shared fragments and must never be maintained as duplicate theological copies.

## Reader and Use

The assumed reader already knows the basic order of Mass and can follow biblical, doctrinal, sacramental, and patristic connections. The guides therefore emphasize relationships that are easy to miss when the propers are read separately:

- repeated words, images, and grammatical forms;
- authors, first audiences, composition places and moments, and the passages' place in Israel's and salvation history;
- the movement from entrance through proclamation, offering, Communion, and continuing effect;
- distinctions among literal context, patristic exegesis, canonical typology, and editorial synthesis;
- doctrinal guardrails that prevent an attractive symbol from being pressed too far;
- questions and visual cues that can be carried into Mass without turning preparation into a script.

The guide is a companion to an open hand missal, not a replacement for it. Research and repository records retain the complete appointed texts, but the PDF normally uses an incipit, reference, or decisive clause rather than reproducing a complete proper. `In Illo Tempore...` identifies every distinct directly appointed biblical passage by citation only and does not reproduce its wording; composed orations remain selective throughout. Translate or parse a quoted fragment elsewhere when its wording carries the argument or when common hand-missal renderings may obscure the point.

The intended rhythm is **survey, historical situation, authoritative synthesis, authoritative depth, proposed synthesis, verification**: survey the Propers map and four senses, place the directly quoted Scriptures in their authors' lives or recoverable compositional horizons, first audiences, geography, and salvation-historical moment, read the two-page authoritative condensation, enter the expansive sourced analysis, consider the separately labeled speculative exposition, and verify the witnesses in the final references.

## Required Weekly Document Order

Every new or substantially revised guide follows one fixed macro-order. The content and internal teaching forms remain adaptive to the Sunday, but the section sequence does not. Immediately after page 1, use the exact major headings `In Illo Tempore...`, `Condensed Authoritative Exposition`, `Expansive Authoritative Exposition`, `Speculative Exposition`, `References`, and `Generation Metadata`; insert `Notable Quotables` after speculation when verified examples exist, followed by any required sacramental appendix and then `References`.

### Sacramental appendix rule for ritual Masses

When a Mass is celebrated with or specifically for Baptism, Confirmation, Penance, Anointing of the Sick, Holy Orders, or Matrimony, its guide includes the relevant one-page sacrament summary as a clearly labeled `Sacramental Appendix`. Import the canonical fragment from `src/gpt/sacraments/summaries/` after `Speculative Exposition` and any `Notable Quotables`, but before `References`; `Generation Metadata` remains terminal. If more than one non-Eucharistic sacrament is actually conferred, include each relevant summary. The Eucharist needs no routine appendix because every Mass guide already treats the Eucharistic sacrifice and reception as the liturgy's intrinsic center; a Mass specifically focused upon Eucharistic doctrine may include its summary when that adds real value.

The one-page appendix is a retrieval aid, not the research ceiling. In generating or substantially revising the exposition, use the complete [sacramental treatise](src/gpt/sacraments/main.tex), its [research record](src/gpt/sacraments/research/scope.md), and the primary and scholarly documents to which they point as additional source material. The verified Mass formulary still governs what is appointed and what can be claimed about its compositional unity; the sacramental sources govern doctrinal context, distinctions, inherited interpretations, and cross-sacramental connections. Do not infer that a general sacramental theme was the historical reason a particular chant or oration entered the formulary unless a source establishes that claim.

When the sacrament has a received hierarchy of ends, the ritual-Mass exposition states it explicitly and shows how the appointed texts disclose, order, or qualify those ends. Distinguish the primary proper end, intrinsic secondary ends, contingent effects, and the common ultimate end; do not confuse objective finality with empirical outcome or make a secondary end either a rival to the primary end or a disposable good.

Non-Sunday ritual and votive guides otherwise retain the macro-order below, adapted to every text actually appointed. Seasonal chant substitutions, blessings inserted within Mass, Pontifical or Ritual prayers, and post-Mass rites receive explicit map entries and source records when they materially govern the liturgical action; they must not be hidden merely to preserve a ten-row Sunday template.

### Page 1: Propers map and four senses

The four-column table presents all ten principal texts in liturgical order:

1. Introit, including its psalm verse
2. Collect
3. Epistle
4. Gradual
5. Alleluia
6. Gospel
7. Offertory
8. Secret
9. Communion
10. Postcommunion

These ten elements are the fixed list for the present Trinity and post-Pentecost set. If the project is extended to a formulary with a Tract or Sequence, substitute the Tract for the Alleluia and add the Sequence where appointed; adjust the row count rather than omitting a proper to preserve the number ten.

The page-one table names every proper in full and uses no numeric badges. Later proper-focused subsection headings and speculative-unit leads end with a parenthetical, comma-separated list of italic abbreviations keyed directly to those names—for example, `Acclaim and ask` (*Int., Coll.*). The standard vocabulary is *Int.*, *Coll.*, *Ep.*, *Grad.*, *All.*, *Gosp.*, *Off.*, *Sec.*, *Comm.*, and *Postcomm.* Use only the entries actually governing that unit and retain their liturgical order. A Tract uses *Tr.* in place of *All.*; an added Sequence uses *Seq.* A ritual guide defines any additional cues it needs: M01 uses *Nupt. I*, *Nupt. II*, and *Final* for the first prayer after the Pater, the long nuptial blessing, and the final blessing.

These cues are quiet navigation, not a second numbering system: use ordinary parentheses and italic text, with no boxes, arrows, dots, icons, or explanatory sentence. Apply them to each substantive unit governed by a definite set of propers, but omit them from macro-order headings such as `References` and from generic sections with no useful hand-missal target. The table's columns identify the proper, incipit or reference, scriptural axis, and connection. The `Connection` cell may state only a relation directly demonstrable from the appointed wording or context, or one explicitly supported by an identified inherited interpretation; every inferential AI bridge belongs later in `Speculative Exposition`. The Secret receives its own row because it normally discloses the relation between the offered gifts, the offerers, and sacramental reception; the later exposition should then unfold rather than merely repeat that relation.

Immediately below the Propers map, without a separate section heading, a compact table labeled `Sense` and `Synthesis` presents exactly four rows:

- **Literal:** the appointed passages in their narrative, grammatical, and canonical setting.
- **Allegorical:** Christ, the Church, salvation history, and sacramental fulfillment.
- **Moral:** the kind of conversion, virtue, or rightly ordered action disclosed by the texts.
- **Anagogical:** judgment, resurrection, heavenly worship, or final communion.

The four syntheses must remain grounded in the appointed texts or documented inherited interpretation. They are not a loophole for placing an unlabeled AI proposal on page 1.

Both tables must fit together on page 1.

### Page 2: In Illo Tempore...

`In Illo Tempore...` occupies exactly one page immediately after page 1 and ends with a forced page break. It is an authoritative historical orientation to the biblical words appointed for the day, not a speculative reconstruction.

Present every distinct directly appointed biblical passage in one heterogeneous table. Sort the dossiers by the books' canonical order in the Catholic Bible, then by ascending chapter and verse within a book; do not use liturgical order. Consolidate a repeated passage into one dossier while naming every proper in which it occurs. Do not treat loose biblical echoes in composed orations as direct quotations.

Each dossier ordinarily consists of a composition-metadata row and a full-width explanatory row. A Gospel dossier inserts one additional narrated-event row between them.

- Use exactly the four column headings `Proper`, `Citation`, `Location`, and `Date`. The composition row contains the full name of the proper or propers, the biblical citation, the traditional composition location, and the approximate traditional year or date range. Its citation cell contains no scriptural text; use `c.` or a range rather than false precision. Because the short headings are neutral, the one-sentence interpretive key must state that a proper row's `Location` and `Date` are traditional composition metadata. Place a horizontal rule immediately after every row containing a name and citation.
- Immediately after the Gospel's composition row, add a four-field row whose first cell is `Narrated event`, whose second contains the locating narrative citations without scriptural text, and whose last two cells give the narrated location and approximate event date. Follow it with the same horizontal rule. This row distinguishes where and when Jesus speaks from where and when the Evangelist writes.
- The explanatory row spans the full table width and begins directly with its prose; do not prefix it with `Description.` In compact prose, identify the traditional author, the addressee or first audience, the relevant point in the author's life or the communal compositional horizon, the narrated setting when it is not already supplied in the Gospel event row, and the passage's place in Israel's history and the larger story of salvation. Distinguish traditional placement from historical judgment and state material uncertainty or responsible alternatives.

Where Psalm numbering differs, give the missal's Vulgate/Septuagint number first and the common modern number in parentheses. Give secure ancient places with present-day geographic equivalents in the description when useful. Use edition-identified biblical introductions, commentaries, historical studies, and geographic references, with exact citations sufficient to verify the claims. Record materially competing judgments and unresolved questions in `research/scope.md`, cite every source actually used in `References`, and avoid duplicating this background later unless the expansive argument requires a particular detail.

The table must remain readable at ordinary print size while fitting with the section heading and any one-sentence interpretive key on page 2. Do not add a second table, biblical quotations, a concluding recap box, or prose outside the table that forces a spill page.

### Next two pages: Condensed Authoritative Exposition

The two pages immediately following `In Illo Tempore...` form exactly two pages of source-grounded, scan-first synthesis, not a miniature continuous essay. A reader scanning only the governing thesis, orienting form, relationship-titled units, and callout titles must be able to recover the Sunday's central claim, direction of movement, decisive witnesses, and interpretive limits. Begin with a one- or two-sentence thesis and one compact sequence, paired track, relationship map, or comparison containing no more than four primary stages.

Organize the remaining material into three to five short synthesis units keyed to that same architecture. Name every appointed proper within the staged movement or units, grouping texts by theological or liturgical function rather than reproducing ten isolated summaries. End each unit heading with the parenthetical italic abbreviations of its governing propers. Make the decisive evidence and essential guardrails visibly locatable through information-bearing headings, tables, matrices, short labeled lists, or restrained callouts.

Each unit must make a complete claim in full sentences, join evidence to interpretation, and show how it advances the whole movement; scanability must not reduce the argument to disconnected fragments. No prose paragraph may exceed 120 words, and no unit may contain more than two consecutive prose paragraphs without an information-bearing structured form. The section contains no AI speculation and must fill two genuinely readable pages without decorative repetition, padding, oversized headings, or artificial whitespace.

### Thereafter: Expansive Authoritative Exposition

The expansive section begins on a new page immediately after the two-page condensed section. It supplies the detailed scriptural exegesis, patristic and saintly comparisons, lexical work, doctrinal distinctions, sacramental development, genuine disagreements, and source qualifications behind the condensed account. It deepens and demonstrates the first treatment rather than repeating it paragraph for paragraph.

### Speculative Exposition

After the authoritative exposition, place every original AI-generated analogy, cross-proper proposal, symbolic extension, or theological inference not established by the sources in a clearly titled `Speculative Exposition` section. One compact opening notice establishes that the section contains exploratory AI-generated syntheses, attributes none of them to cited authorities, and makes no claim about historical compositional intent. Once that boundary is set, write in a natural exploratory voice rather than repeating formulaic hedges.

The section has no fixed number of proposals or prescribed length. It may offer competing models, surprising symbolic trajectories, canonical or sacramental analogies, unresolved questions, or hypotheses for future research. Each substantial unit should make its textual launch points visible with the same parenthetical italic abbreviations, develop the proposal freely, and state a brief limit or serious alternative where needed. Do not substitute an all-propers listening checklist, a recap of the authoritative exposition, or a `source boundaries to retain` inventory for actual proposals; the opening notice supplies the attribution boundary, while source roles belong beside the authoritative claim or in `References`. Evaluate speculation for textual anchoring, novelty, coherence, theological plausibility, interpretive or prayerful fruitfulness, and awareness of alternatives—not for whether an inherited source already said it. Speculation may not invent facts or quotations, attribute itself to a source, disguise a research lead as a discovery, or contradict established text or doctrine. If no responsible speculation is warranted, retain the heading and state that none is offered.

### Notable Quotables

When verified examples exist, place a section titled exactly `Notable Quotables` after `Speculative Exposition` and before any required sacramental appendix and `References`. Treat it as a light cultural interlude, not another scholarly exposition. Survey whether wording from any appointed proper or its underlying biblical passage appears in literature, poetry, drama, film, television, music, advertising, comedy, memes, or other popular culture. Give particular prominence to quotations that are incorrect, humorously displaced, or used with an ironic force different from their scriptural or liturgical setting.

Aim for two to four examples, preferably drawn from different works or media. One strong example is acceptable only when no second candidate survives verification; never pad the section with a weak connection. Present each example as one compact list item of no more than two sentences and normally 25–60 words. Its information-bearing lead must identify the proper or wording, the classification (`Exact quotation`, `Adaptation`, `Recognized allusion`, `Sampled`, or `Misquotation`), the work, creator, date, and a sufficiently precise scene, chapter, page, episode, track, or other location. Follow with only the short payoff: the joke, irony, displacement, or memorable use. Do not supply a full theological justification or an extended comparison with the passage's original context; mention that context only when the humor or irony would otherwise be unclear.

Verify the wording and context in the primary cultural work or a reliable edition, transcript, or recording; quotation websites and memory are only leads. Do not turn a coincidental phrase or uncertain AI-proposed allusion into a factual example: uncertain connections remain in `Speculative Exposition`. Keep excerpts brief, quote song lyrics especially sparingly, and never reproduce substantial copyrighted text. Cite every cultural work or verification source in `References`. If no verified example is found after a reasonable search, omit `Notable Quotables` rather than inventing an entry or retaining an empty section, and preserve the attempted cultural-reception search in `research/scope.md`; mention the negative result in the PDF only when it materially limits an argument.

### References

`References` is the final scholarly section and immediately precedes `Generation Metadata`. Its bibliographic entries contain only sources actually used, with sufficiently exact works, books, homilies, chapters, or sections to permit verification; distinguish primary sources from any secondary work actually relied upon. Every historical dossier cites the sources governing its authorship, date, place, audience, and chronology, distinguishing traditional attribution from historical judgment when both are reported. End with a compact, labeled `Search Scope and Limitations` panel giving only the text-verification status, the principal direct and illuminating source scope, material limitations that affect the argument, and pointers to `propers/verified.md` for the text audit and `research/scope.md` for the research survey. Retrieval mechanics, checksums, query logs, discarded leads, and repeated verification explanations belong in those repository records rather than the reader-facing PDF. A limitation that changes a particular claim remains beside that claim. No conclusion, listening guide, or other expository prose follows `References`.

### Generation Metadata

`Generation Metadata` is always the terminal section of the document. Keep it compact—normally three short labeled lines with semicolon-separated key-value fragments rather than six repetitive fields or explanatory sentences:

```text
Generated: YYYY-MM-DD
Model: exact full runtime identifier; qualifier=value; every other exposed qualifier
Agent/runtime: product and role(s); client/build kind and exact version; interface; unexposed: specific unavailable components
```

Use the ISO date on which the final document was generated or last substantially regenerated. Preserve the complete model label exposed by the runtime verbatim; do not shorten it to a family name or drop a numbered version, named variant, preview status, modality, reasoning mode, reasoning profile or tier, deployment channel, or similar qualifier. For example, a runtime label such as `GPT-5.6 Sol Ultra` must be recorded in full, not reduced to `GPT-5`. If the runtime exposes qualifiers separately, list each once in compact `key=value` form; do not repeat a derived combined designation when the exact identifier and its qualifiers already supply the same information.

Identify the acting product or agent and its role, such as primary drafting agent, research subagent, or review agent. Record every exposed agent, client, build, or revision version and label what the number describes; do not present an installed client version as a server-side model or agent version. Group contributors that share a model, qualifier set, runtime, and environment instead of repeating identical fields for each. Separate a contributor only when one of those values differs. If a component is unavailable, name it once after `unexposed:` rather than guessing, silently omitting it, or repeating a full explanatory sentence.

Describe the AI environment at the product/interface level, for example `OpenAI Codex CLI`, `ChatGPT with a Codex workspace`, or another comparably specific interface. Prefer terse labels whose meaning is self-evident (`CLI 1.2.3`, `API workspace`) and omit prose that merely restates a label. The compact form must remove redundancy, never version or qualifier detail.

Do not include machine-specific or identifying operational details such as hostname, username, absolute filesystem paths, IP or MAC addresses, container or session identifiers, hardware identifiers, credentials, or access tokens. Refresh this metadata whenever the guide is substantially revised or its final PDF is regenerated by a different model or environment.

All sections after page 1, beginning with `In Illo Tempore...`, are scoped inside the `deepstudy` environment. Their ordinary prose, lists, and box bodies use the document's 10-point `small` size, while the opening survey page remains unchanged and tables retain their own explicit sizes. This keeps sustained historical and patristic analysis readable without letting normal body type dominate the page.

## Required Weekly Research and Writing Workflow for AI

### 1. Extract and verify the complete formulary

Before interpreting anything, create or locate the Sunday's repository-owned source record under `Stored Propers and Repository Layout`, then locate the formulary with the public witnesses under `Public Missal Sources and Editorial Status`. Identify it by its printed liturgical heading, rank, and place in the 1962 temporal cycle rather than by a civil date or an unverified filename. OCR and searchable transcriptions are finding aids only: use them to locate and provisionally transcribe the texts, then visually collate every Latin form, rubric, reference, and formulary boundary against the facsimile page image.

Extract every one of the ten propers listed under `Page 1` above, together with any seasonal substitution or addition. Store the unedited Sunday-specific retrieval in `propers/retrieved.txt` and the visually checked text and provenance in `propers/verified.md`; both files are required, tracked project sources rather than disposable build products. Record the full appointed Latin or exact reference, the source of every chant verse, the immediate biblical context, the text's liturgical function, the facsimile's printed page number, its stable public URL and access date, and any unresolved textual issue. Read the complete literary contexts of every directly appointed biblical passage, not only the printed Epistle and Gospel pericopes. Check an unclear reading against the secondary public image witness and report any disagreement; do not silently blend witnesses.

Study every oration and chant in full during research. Publication remains selective because the reader is expected to have a hand missal open: `In Illo Tempore...` gives citations without biblical wording, and the later analysis uses the incipit or smallest clause it needs, while the complete verified wording remains in `propers/verified.md`.

No proper may disappear from the later interpretation because it is brief, difficult, or not itself a biblical pericope. Do not merge separate formularies. A displaced Sunday or ferial Mass may be mentioned in a clearly marked source note, but its texts do not become part of the appointed feast's synthesis.

### 2. Establish the historical coordinates of every direct scriptural passage

Inventory every distinct directly appointed biblical passage before drafting. Read its complete literary context and research its traditional authorship, date and composition place; its first audience and biographical or communal horizon; its narrated setting; the strongest historical judgments and alternatives; and its place in Israel's and salvation history. Distinguish the traditional metadata requested by the table from historical judgment, and distinguish the writer's location from the events narrated and the recipients' location.

Use identified, edition-specific scholarship and preserve calibrated uncertainty. Anonymous or composite texts receive no invented authorial biography; disputed places and dates are reported as ranges or alternatives in the explanatory row even when the composition row supplies a traditional placement. Record the governing sources, materially competing judgments, geographic identifications, and unresolved questions in `research/scope.md`. Draft the dossiers in canonical order, add the Gospel narrated-event row, and fit the complete `In Illo Tempore...` table to one page before producing the condensed exposition.

### 3. Conduct a deep patristic and saintly source study

Research every appointed biblical passage and the theological substance of every oration. Search as broadly as the accessible corpus permits for:

- direct patristic or saintly commentary on the appointed passage;
- homilies, tractates, letters, and catecheses treating its immediate question;
- doctrinal, moral, mystical, or sacramental works that illuminate an oration or chant;
- inherited liturgical interpretations relevant to the proper;
- later Doctors and saints where they substantially deepen the earlier reception.

For every source retained, record author, work, exact locus, edition or stable link, whether it comments directly on the appointed text or supplies doctrinal illumination, and whether the guide quotes or paraphrases it. A catena, anthology, search result, or secondary citation is only a lead until the underlying source and attribution have been checked. Prefer direct exegesis to thematic resemblance; compare genuine disagreements and do not invent patristic consensus.

Source selection is claim-driven, not quota-driven. No fixed number or category of ancient, modern, lexical, historical, liturgical, or musical sources is required. A source earns space by establishing text or context, directly explaining an appointed passage, supplying a necessary doctrinal boundary, preserving a genuine alternative, or materially changing how a proper is heard. Search broadly enough to test the governing claims, publish selectively, and stop accumulating when additional sources merely repeat rather than refine, qualify, or challenge the argument. If one author dominates, test whether the material warrants it or the search was narrow.

The instruction to seek “all” patristic and saintly exegesis means the broadest feasible survey relevant to the claims, not a false assertion of universal exhaustiveness. Preserve corpora, language, search, and negative-result details in `research/scope.md`. In the PDF, identify a missing direct witness when that absence affects the argument or when doctrinal illumination first takes its place; do not repeat the same provenance caveat throughout the exposition. Summarize only material boundaries in the compact `Search Scope and Limitations` panel.

### 4. Trace the symbolic unity of the entire formulary

After studying the texts individually, identify the week's governing relationship and the deepest connections among the propers and commentaries. Examine repeated words, grammatical forms, speakers, actions, images, biblical types, sacramental movements, moral transformations, eschatological ends, and convergences or tensions among the witnesses. Ask what an attentive, well-catechized reader most needs help seeing; the answer should be a relationship rather than a generic topic.

Account for every appointed principal element as one ordered action:

```text
entrance condition
  -> petition for grace
  -> apostolic disclosure
  -> chanted response and Gospel preparation
  -> Gospel manifestation or command
  -> self-offering and Secret
  -> sacramental reception
  -> continuing effect
```

The analysis need not repeat ten prose rows. It may encode the sequence in a diagram, paired track, timeline, matrix, or annotated map, provided no proper disappears from the interpretation. Make the Gradual, Alleluia, Secret, and Postcommunion do real interpretive work. A cross-passage connection may enter the authoritative exposition only when it is demonstrable from the texts or responsibly grounded in cited tradition.

### 5. Maintain a strict boundary around AI speculation

“Authoritative” in this project means traceable to Scripture, the verified missal text, identified and checked biblical-historical scholarship, or an identified and checked patristic, saintly, doctrinal, or liturgical witness. It does not make the guide a magisterial document or every cited judgment equally binding. Classify every substantial claim before drafting:

- **Textual observation:** directly verifiable in the appointed texts and their contexts.
- **Documented historical orientation:** an authorship, date, place, audience, biographical, geographic, or salvation-historical judgment supported by identified scholarship, with material uncertainty preserved.
- **Documented reception:** explicitly taught by a cited Father, Doctor, saint, or liturgical source.
- **Source-grounded synthesis:** a restrained conclusion demonstrably supported by the appointed texts, documented historical orientation, or documented reception.
- **Speculative exposition:** a new analogy, symbolic proposal, typological extension, compositional inference, pastoral application, or theological conclusion not explicitly established by the evidence.

The first four classes may appear in the authoritative sections. The fifth appears only in `Speculative Exposition`. A canonical or liturgical analogy supported by cited tradition may be authoritative; an AI-generated analogy without that support is speculative. An unverified study lead supports no final claim. Never place an AI-generated connection in a Father's mouth, imply consensus by proximity, or hide speculation in the four-senses table.

This boundary is intended to license responsible invention rather than suppress it. After the authoritative case is secure, generate multiple possible syntheses, including serious alternatives, and retain those that are textually anchored, coherent, theologically plausible, and capable of changing attention to the Mass. Their value lies in disclosed exploration, not borrowed authority.

### 6. Produce condensed and expansive authoritative treatments

Develop the source-grounded analysis fully, then condense its governing results into exactly two pages.

The two-page treatment must:

- open with a one- or two-sentence governing thesis and a compact orienting form of no more than four primary stages;
- develop three to five relationship-titled units that follow the same vocabulary and order as the orienting form;
- include the decisive evidence actually needed for the claims made;
- account for every appointed proper in functional groups without becoming another catalogue;
- make necessary disagreements and doctrinal guardrails findable at a glance;
- keep each prose paragraph within 120 words and break up every run of more than two paragraphs with an information-bearing structure;
- use concise, source-governed, syntactically complete claims with no speculative material or telegraphic fragments.

The expansive treatment supplies the detailed exegesis, source comparisons, lexical work, distinctions, and sacramental development behind that synthesis. The condensed section states the architecture and leading conclusions; the expansive section demonstrates, complicates, and qualifies them. A witness may be named compactly in the two-page synthesis and treated fully later, but quotation, extended paraphrase, evidence, and caveat receive one fullest home rather than being duplicated.

### 7. Assemble the guide in the required order

Assemble the guide according to `Required Weekly Document Order`. Fit the complete `In Illo Tempore...` table to page 2 and force a boundary after it, then force another after the second condensed page so that the expansive exposition begins on a fresh page. Edit to make the historical table and both condensed pages genuinely full, readable, and scan-first. The condensed section requires one compact orienting form; its internal headings, tables, matrices, source cards, short lists, and diagrams may otherwise vary with the Sunday, but the macro-order may not.

### 8. Perform a final depth-and-clarity edit

Read the entire guide linearly and make a claim-by-claim pass before the final build:

- remove repeated quotations, diagrams, examples, conclusions, protocols, and paraphrases;
- ensure the condensed section summarizes while the expansive section proves and qualifies;
- replace several weak analogies with the strongest defensible connection;
- merge thin subsections and delete links stretched beyond their textual or sourced support;
- replace repeated provenance narration with the compact source classification and final scope panel while retaining the full repository audit;
- give every paragraph one necessary task: evidence, interpretation, connection, or guardrail;
- scan only the condensed thesis, visual labels, unit titles, and callout titles; together they must recover the central claim, direction of movement, decisive witnesses, and interpretive limits;
- sharpen transitions, define difficult distinctions, and preserve genuine disagreement;
- verify every attribution, locus, quotation, Latin form, biblical reference, and authority label;
- confirm that every proper contributes and that the Secret and Postcommunion are treated substantially;
- prefer profundity through precision, source depth, and integration rather than through length.

Finally, compile twice and visually inspect every page. Confirm the exact section order and page boundaries, readable density, intact tables and callouts, any `Notable Quotables` section before the sacramental appendix (when required) and `References`, `References` as the penultimate section, `Generation Metadata` as the terminal section, and the absence of overflow, split headings, sparse spill pages, and layout warnings.

## Analytical and Visual Forms

Use visual and analytical forms selectively. The condensed exposition is the exception in requiring one compact orienting form, but its type must be chosen for the actual Sunday rather than copied mechanically:

| Representation | Best use |
| --- | --- |
| Sequence or timeline | Showing development through the order of Mass or salvation history |
| Parallel tracks | Comparing divine initiative with human or ecclesial response |
| Comparison table | Holding two images, passages, or patristic readings beside one another |
| Diagnostic matrix | Separating questions that are often confused or testing combinations of factors |
| Concept or coordinate map | Showing several symbolic axes meeting at a theological center |
| Lexical study | Explaining a repeated word, grammatical subject, verbal contrast, or Latin bridge |
| Layered reading | Distinguishing literal, patristic, canonical, liturgical, and eschatological senses of one sign |
| Calibration panel | Stating what a symbol means and what it does not establish |
| Proper cue | Sending the reader back to the relevant hand-missal rows with parenthetical italic abbreviations |
| Source card | Placing one short quotation or paraphrase beside the claim it governs |
| Listening or examination card | Converting sourced findings into attention; any new AI application belongs in `Speculative Exposition` |

A representation earns its place only when it makes a relationship easier to grasp than another paragraph would. Do not create decorative diagrams or repeat the same claim in multiple forms. A single diagram should normally contain no more than four primary stages; when the material requires more, divide it into separate views or use a table with explicit headings.

### Monochrome print standard

The guides are designed for ordinary black-and-white printers. All text, rules, arrows, borders, and links use pure black; page and box interiors use pure white. Visual distinctions must rely on line weight, border style, labels, position, and whitespace rather than color or gray shading. A diagram that becomes ambiguous when hue is removed must be redesigned.

### Callout hierarchy

Callouts use an editorial rather than a dashboard-like visual language. Conceptual notes receive a single left rule; preparation or listening panels receive a restrained square hairline frame; primary-source cards receive a lighter framed treatment with the attribution integrated into the title. Filled title bars, rounded cards, and decorative badges are avoided. Two short source cards may share a row when their texts are genuinely parallel and remain readable at print size; otherwise the callout stays full-width.

## Week-Specific Content Architectures in the Present Set

These examples show how the internal teaching forms may respond to a Sunday's material. They do not override the required macro-order above.

| Sunday | Governing learning problem | Principal teaching forms |
| --- | --- | --- |
| Trinity | How mercy, salvation-historical wonder, the one baptismal Name, self-offering, and universal mission belong together | One-page canonical historical table, blessing-before-mastery route, Chrysostom's Romans dossier, Psalm-and-Daniel chant study, three-Father baptismal rule, Secret syntax, Augustinian charity guardrails |
| Second | How a prepared gift tests desire, widens the house, forms charity, and transfers the guest toward heavenly conduct | One-page canonical historical table, four-Father role comparison, Augustinian excuse and charity dossiers, `compelle intrare` guardrail, five-psalm voice study, Secret syntax |
| Third | How Christ's search re-educates the gaze without cancelling repentance, vigilance, sanctification, or joy | One-page canonical historical table, five-gaze matrix, Cyril--Gregory controversy dossier, Shepherd-and-coin reception comparison, Peter/Gradual bridge, Secret grammar, sacramental completion |
| Fourth | How Christ's word orders creation, the apostolic Church, bodily hope, perception, and resistant willing | One-page canonical historical table, three-scale matrix, Chrysostom--Irenaeus Romans dossier, Cyril--Ambrose catch exegesis, Augustine's two catches, Psalm 12 eye study, and two-petition Secret grammar |
| Fifth | How infused charity orders desire, peace, reconciliation, individual offering, and the common ecclesial good | One-page canonical historical table, Augustinian order-of-love dossier, Psalm 26 envelope, Bede's Petrine peace reading, Chrysostom--Augustine Gospel comparison, `singuli`--`cunctis` Secret study |
| Sixth | How baptismal newness remains dependent pilgrimage sustained by opened Scripture, faithful prayer, and Eucharistic gift | One-page canonical historical table, font--desert--road--altar itinerary, Chrysostom's Romans dossier, Cyril--Ambrose mystagogy, Bede--Augustine feeding comparison, Secret prayer guardrail, Psalm 26 completion |
| Seventh | How voice and works, doctrine and life, freedom and service, individual offering and ecclesial sacrifice, judgment and healing are distinguished and reunited | One-page canonical historical table, Psalm 46 concordance, focused Gospel-reception comparison, Pauline fruit-and-gift anatomy, Secret grammar, and an integrated hearing-and-cure sequence |
| Nuptial Mass | How God's principal agency, free consent, created one flesh, Christ's Paschal covenant, household fruitfulness, Eucharistic oblation, and lasting peace belong together | One-page canonical historical table, four-stage covenant route, divine-causality lexical study, Matthew--Ephesians comparison, full nuptial-blessing exegesis, seasonal chant map, and canonical Matrimony appendix |

The Sunday sequence moves from divine gift to embodied discernment: the Trinity is adored, charity answers invitation, mercy finds the lost, Christ's word orders mission, reconciliation makes sacrifice truthful, baptismal life is fed, and sacramental medicine produces holy fruit. The first non-Sunday guide then applies the same method to a ritual Mass, where created covenant is elevated, offered, nourished, and ordered toward the Lamb's wedding.

## Stored Propers and Repository Layout

Every proper guide has its own directory, and its guide and source record live together. Sundays use the canonical number; non-Sunday Masses use their `mNN` catalog identifier. Never place multiple formularies' propers in one shared source file:

```text
src/gpt/
  NN-sunday-name/
    main.tex
    propers/
      retrieved.txt
      verified.md
    research/
      scope.md
```

The parallel non-Sunday pattern is `src/gpt/mNN-formulary-name/` with the same `main.tex`, `propers/`, and `research/` structure. The doctrinal reference work instead uses `src/gpt/sacraments/fragments/` for shared front matter, `src/gpt/sacraments/sections/` for long treatments, `src/gpt/sacraments/summaries/` for the canonical reusable one-page appendices, and `src/gpt/sacraments/research/scope.md` for its authority and qualification audit. `src/gpt/sacraments-at-a-glance/main.tex` composes those canonical fragments and contains no independent doctrinal copy. Installed PDFs follow the same provider branch under `doc/gpt/`.

`retrieved.txt` preserves the formulary-specific text exactly as pulled from the public machine-readable finding aid, including OCR errors and enough heading or boundary text to identify the formulary. Do not silently clean this file. Do not commit an entire third-party missal, bulk OCR dump, or page-image cache in place of the focused extract.

`verified.md` is the repository's reviewed proper record. It contains the ten propers in liturgical order, any seasonal substitution or addition, and a provenance block with at least:

```text
Missal edition:
Printed formulary heading and rank:
Retrieval URL and source identifier:
Retrieval date:
Printed pages and digital pages or leaves:
Retrieved source-file checksum, when available:
Facsimile verification URL:
Verification status and date:
Unresolved discrepancies:
```

`research/scope.md` preserves the operational scholarship audit displaced from the PDF: biblical authorship, dating, composition-place, audience, geographic, and chronology research; materially competing judgments and unresolved historical identifications; corpora and languages searched; materially relevant negative results; unverified leads that were rejected or left open; and any source-role or attribution issue too detailed for the compact reader-facing panel. It is not a diary or chain-of-thought record and need not reproduce obvious searches; it records enough scope and disposition to make research limits honest.

All three files must be added to Git with a new or substantially revised proper guide. Corrections, refreshed retrievals, source substitutions, and newly resolved discrepancies are normal reviewed changes: update the appropriate record, explain the reason in the commit, and preserve the earlier state in Git history. The `propers/` and `research/` directories must never be ignored, regenerated only at build time, or treated as optional personal caches.

## Public Missal Sources and Editorial Status

This repository has no required sibling corpus, private checkout, or fixed local source path. Use this public-first source hierarchy:

1. **Facsimile baseline:** the Church Music Association of America's [complete resource list](https://churchmusicassociation.org/resources/resource-list-complete/) links a public [scan of the 1962 *Missale Romanum*](https://media.churchmusicassociation.org/pdf/missale62.pdf). Use the printed page images as the baseline for Latin text, rubrics, rank, references, and formulary boundaries. Cite the printed missal page number, not only the PDF page index.
2. **Machine-readable finding aid:** the Internet Archive item [*Missale Romanum* (1962)](https://archive.org/details/MissaleRomanum1962RomanMissalColorLatin) provides [downloadable full-text OCR](https://archive.org/download/MissaleRomanum1962RomanMissalColorLatin/Missale-Romanum-1962-Roman-Missal-color-latin_djvu.txt). It is suitable for searching headings, sequence, incipits, and references, but not as publication text.
3. **Secondary image witness:** the same Internet Archive item provides a color scan in its browser reader and download options. Consult those page images when the baseline scan is unclear. Its OCR and its page images are derivatives of the same item, so comparing those two alone is not an independent collation.

A browser is sufficient; no private or machine-specific corpus is required. Fetch the public witnesses on demand and commit only the focused proper records described above; do not vendor the complete scans or bulk OCR in this repository, and observe the source sites' terms governing redistribution. Contributors may keep a larger offline cache wherever convenient, but it is not the project source record. If a link becomes unavailable, substitute another complete, edition-identified public facsimile of the 1962 missal, update the guide's provenance, disclose the substitution in the PDF when it materially affects the published text or argument, and preserve unresolved differences instead of silently harmonizing them.

Guides created before this workflow may retain historical source notes. Those notes record provenance, not a dependency future contributors must reproduce. When such a guide is substantially revised, re-collate its Latin against the public facsimile workflow and replace machine-specific source references.

Psalm citations follow the Vulgate/Septuagint numbering printed in the missal. Bibles based on the Hebrew/Masoretic numbering normally number Psalms 10--148 one higher; the missal's Psalm 17, for example, is Psalm 18 in most modern English Bibles.

The authority classes in the workflow above govern what may be published in each section. Research notes additionally use four evidence statuses:

- **Checked direct quotation:** wording verified in the identified edition and quoted only as much as necessary.
- **Checked paraphrase:** an identified argument verified and restated without quotation marks.
- **Unverified study lead:** a work proposed for investigation; it is research-only, cannot support a final claim, and never appears in `References`. After verification and actual use, reclassify it as a checked quotation or paraphrase.
- **Editorial or AI proposal:** the project's own relationship among texts; it appears only in `Speculative Exposition`, even when plausible.

Public-domain translations linked in `References` are working study editions, not claims that a particular English rendering is definitive.

## Quality Gates

Before a guide is complete, verify that:

- a ritual Mass connected with a non-Eucharistic sacrament imports the canonical one-page summary from `src/gpt/sacraments/summaries/` as a `Sacramental Appendix` before `References`, while its research uses the full sacramental treatise, its audit, and the sources they identify rather than relying on the appendix alone;
- the sacramental reference document keeps the requested formal definition and complete matter–form–subject–minister–effect matrix together on page 1, the metaphysical lexicon alone on page 2, the three initiation sacraments under the first overall section, all twenty-four Catholic Churches *sui iuris* on the single initiation-practice page, and exactly one consistently structured summary page after every sacrament; every full treatment and summary explicitly distinguishes primary proper, intrinsic secondary, contingent, and ultimate ends where those distinctions apply;
- the at-a-glance companion contains exactly the shared master matrix, lexicon, seven canonical summaries in sacramental order, and the single twenty-four-Church initiation page; the summaries remain one page each, and no copied theological text can drift from the full treatise;
- every sacrament defines its matter or quasi-matter and sacramental form, identifies the intermediate reality and proper grace, and states what formal, relational, or substantial change occurs; Eucharistic transubstantiation is never confused with the determining sacramental words or with a change of accidents;
- the proper guide has its own cataloged directory containing Git-tracked `propers/retrieved.txt`, `propers/verified.md`, and `research/scope.md`; the first preserves the focused pull without silent cleanup, the second contains the text provenance and verification fields, and the third retains material research scope displaced from the PDF;
- the missal witnesses are public and edition-identified, every published Latin form has been visually checked against a facsimile page, and `References` records printed pages, stable URLs, access dates, substitutions, and unresolved discrepancies without machine-specific paths;
- all appointed principal propers (ten in the present set, with any seasonal substitutions or additions where applicable) have been extracted, verified, and made to contribute to the guide;
- the generator studied every complete appointed text, while the hand-missal companion PDF gives citation-only historical metadata in `In Illo Tempore...` and otherwise only the incipits, references, and clauses needed for its analysis;
- page 1 contains only the title, any necessary source note, the complete Propers map (ten rows in the present set), and the four-row `Sense` / `Synthesis` table;
- proper-focused subsection headings and speculative-unit leads end with ordinary parentheses containing the standard italic abbreviations in liturgical order; the page-one table retains full proper names, and the guide uses no numeric badges, boxes, arrows, dots, or icons for this navigation;
- both opening tables share the same horizontal extents and first-column width and fit entirely on page 1;
- `In Illo Tempore...` occupies exactly page 2, ends at a forced page boundary, and contains no unsupported reconstruction;
- one heterogeneous table contains every distinct directly appointed biblical passage exactly once in canonical Bible order and then ascending chapter-and-verse order; repeated passages are consolidated, while loose scriptural echoes in composed orations are not mislabeled as direct quotations;
- the table headings are exactly `Proper`, `Citation`, `Location`, and `Date`; each dossier begins with a four-field composition row naming the proper or propers and citation without scriptural text, followed immediately by a horizontal rule;
- the Gospel composition row is followed by a four-field `Narrated event` row giving locating citations without scriptural text, the event location, and its approximate date, followed by another horizontal rule before the explanatory prose;
- every explanatory row begins without a `Description.` label and, together with any Gospel event row, distinguishes narrated setting, traditional and historical authorship status, composition date and place, first audience, authorial life stage or compositional horizon, and the passage's location in Israel's and salvation history;
- writer, event, and recipient locations remain distinct, secure ancient locations receive present-day equivalents, and disputed or unknown claims remain explicitly uncertain;
- every historical claim is supported by an identified source, with competing judgments and unresolved matters retained in `research/scope.md`;
- the two pages immediately following `In Illo Tempore...` contain exactly two full, readable pages of condensed authoritative exposition and no AI speculation;
- the condensed section begins with a one- or two-sentence thesis and a compact orienting form of no more than four primary stages, then uses three to five relationship-titled units keyed to the same argumentative spine;
- every proper appears in a functional grouping, decisive witnesses and guardrails are visibly labeled, no prose paragraph exceeds 120 words, and no unstructured prose run exceeds two paragraphs;
- a signpost-only scan of the condensed section recovers its central claim, direction of movement, decisive witnesses, and interpretive limits, while the full text remains a continuous argument rather than disconnected fragments;
- the expansive authoritative exposition begins on the fresh page after the two-page condensed section, gives the evidence and qualifications behind the condensation, and does not duplicate either the historical orientation or the condensation paragraph for paragraph;
- every original AI analogy, typological extension, compositional inference, or unsourced cross-proper connection appears only in `Speculative Exposition`;
- `Speculative Exposition` begins with one global boundary notice, then gives exploratory proposals room to develop without repetitive hedging; substantial proposals expose their proper anchors, while material limits or serious alternatives appear where needed rather than as a repeated formula; the section remains free of invented facts, quotations, attributions, or doctrinal contradiction;
- speculative material is selected for anchoring, novelty, coherence, theological plausibility, fruitfulness, and awareness of alternatives rather than by a prescribed number, length, or source precedent;
- `Notable Quotables`, when included, appears after speculation and before any required sacramental appendix and `References`, normally contains two to four verified examples from varied works or media, and never adds a weak item merely to reach that range;
- every cultural entry is one compact list item of no more than two sentences and normally 25–60 words; its lead identifies the proper or wording, classification, work, creator, date, and precise location, while its remainder gives only the brief joke, irony, displacement, or memorable use rather than a full justification;
- uncertain cultural parallels remain in `Speculative Exposition`, copyrighted excerpts remain brief, and an empty `Notable Quotables` section is not retained when no verified example exists; unsuccessful leads remain in `research/scope.md` rather than padding the PDF;
- `References` is the penultimate section, contains every source actually cited, contains no unused study leads, and ends with a compact labeled `Search Scope and Limitations` panel rather than operational provenance prose; `propers/verified.md` and `research/scope.md` retain the full text and research audits;
- `Generation Metadata` is the terminal section, normally uses three compact labeled lines, and unambiguously gives the final generation date in `YYYY-MM-DD` form, the full verbatim AI model label, every exposed model qualifier, the AI agent and its role, every exposed and accurately labeled agent/client/build version, and the product/interface-level AI environment;
- the metadata records shared model/runtime facts once, separates materially contributing agents only when their values differ, groups specifically named unavailable components after `unexposed:`, and never removes detail by collapsing a qualified model label to a generic family name;
- the metadata is refreshed for the final generation event and excludes hostnames, usernames, paths, network addresses, container or session IDs, hardware identifiers, credentials, and tokens;
- the internal teaching forms are fitted to this formulary rather than copied mechanically from another guide;
- the retained sources are sufficient for the actual claims rather than selected by numerical or categorical quota, and the compact PDF scope note does not claim universal exhaustiveness;
- named scriptural, patristic, saintly, doctrinal, and liturgical claims have exact works and loci and are accurately labeled as direct exegesis or doctrinal illumination;
- quotation, paraphrase, source-grounded synthesis, and speculation remain distinguishable;
- each substantial claim has one fullest home, with repeated quotations, recap diagrams, duplicate conclusions, thin subsections, and stretched links removed;
- every diagram has an explicit reading order and adds information;
- no visual block asks the reader to decode more than four primary stages or two simultaneous paths without a strong reason;
- every visual remains intelligible in pure black and white, with no color-dependent distinction or gray fill;
- callouts use the lightest treatment that preserves hierarchy and are not stacked or paired merely for decoration;
- the PDF builds twice without fatal errors or layout warnings;
- every page is visually checked for overflow, split headings, unreadable cells, excessive density, artificial padding, and sparse spill pages;
- all sections after page 1, beginning with `In Illo Tempore...`, use the scoped `deepstudy` size; page 1 is not globally reduced.

## Build

```sh
make
make install
```

`make` compiles PDFs and all LaTeX intermediates under the transient, ignored `build/gpt/` tree. `make install` publishes those PDFs under the tracked `doc/gpt/` tree, preserving each document basename. Unique job names make parallel builds safe. Both `make clean` and the backward-compatible `make distclean` remove only `build/`; installed documents remain in `doc/`.

## Future AI Operating Rule

Treat the required document order, eight-step workflow, sacramental appendix rule, and quality gates above as acceptance criteria, not suggestions. Research and classify the evidence before drafting. If direct patristic commentary cannot be found, record the gap and use clearly labeled doctrinal illumination rather than pretending that a saint commented on the proper itself. Do not fill source categories or numerical targets that the material does not require.

Do not preserve weak material merely to maintain length, and do not pad the two-page condensation. Within the fixed macro-order, allow the appointed formulary's actual texts and witnesses to determine the internal architecture. Prefer fewer strong authoritative axes, then give clearly bounded speculation freedom to test unfamiliar patterns, competing models, and questions. Refresh `Generation Metadata` for the final generation event, build and inspect the PDF, run `make clean`, and commit each proper-guide creation or substantial revision together with its stored `propers/` source record as one coherent change in this repository.
