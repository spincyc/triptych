# Liturgical Year TLM Proper Connections

This project builds weekly LaTeX/PDF study sheets for the traditional Roman Mass propers. The present set covers Trinity Sunday and the Second through Seventh Sundays after Pentecost: the first seven weeks of the 1962 post-Pentecost temporal cycle.

The sheets are aids for preaching, meditation, and liturgical study. They are not critical editions, official liturgical texts, or substitutes for checking a printed missal and the cited primary sources.

**Editorial status:** source-audited working drafts. The local missal OCR and linked patristic translations have been checked for the claims now made, but the Latin has not yet received a line-by-line printed-missal collation or an external theological review.

## Build

```sh
make
```

PDFs are written to `build/`. Use `make clean` to remove LaTeX intermediates and `make distclean` to remove generated PDFs too.

## Source Corpus and Editorial Status

The Mass proper references are keyed to the local corpus at:

- `../liturgy-history/versions/1962-missale-romanum-latin/sections/proper/011-proprium-de-tempore-after-ordinary.md`
- `../liturgy-history/versions/1962-missale-romanum-latin/metadata.json`

That Latin source is OCR. It is useful for locating a Mass, identifying its sequence, and checking incipits and biblical references, but OCR spellings and punctuation are not treated as publication-ready text. Full Latin must be checked against a reliable printed 1962 missal before publication.

Scriptural references control the literal reading. Patristic interpretation is taken, where possible, from an identified primary work. Public-domain translations linked in `Primary References` are working study editions, not claims that a particular English rendering is definitive.

Psalm citations follow the Vulgate/Septuagint numbering printed in the missal. Readers using Bibles based on the Hebrew/Masoretic numbering will normally find Psalms 10–148 numbered one higher; for example, the missal's Psalm 17 is Psalm 18 in most modern English Bibles.

Each kind of source material has a distinct status:

- **Direct quotation:** wording checked in the edition linked or fully identified in `Primary References`; quotation marks are used.
- **Paraphrase:** an identified author's argument restated in the editor's words; no quotation marks are used and the row says that it is a paraphrase.
- **Study lead:** a relevant author or work proposed for further research; it must not be presented as though a particular claim or wording has already been verified there.
- **Editorial synthesis:** the project's account of how the appointed texts illuminate one another. It may be strong, but it is not silently attributed to a Father.

Within sourced reception, the sheets also distinguish direct exegesis of an appointed passage from a related doctrinal witness or a later analogical application. Only the first should be described as a Father's reading of that particular text.

## Evaluation of the First Pass

The first pass established a useful and unusually consistent foundation:

- The page-one table keeps the TLM propers, rather than a generic seasonal theme, in view.
- The four senses are generally applied with restraint and give each homily doctrinal, moral, and eschatological depth.
- The symbol tables extract concrete biblical images instead of merely renaming abstract topics.
- The strongest passages trace a real liturgical movement from entrance, through proclamation, to offering and Communion.
- The applications are brief and concrete enough to help a preacher.

The review of all seven sheets also exposed recurring weaknesses:

- Several sections restated the same thesis in slightly different tables, making the documents feel templated rather than cumulative.
- The Gradual, Alleluia, and Secret were often absent from the synthesis even though they are important hinges in the Mass's movement.
- Some patristic rows named an author without an exact work or blurred paraphrase and quotation.
- In several weeks the final quotation dossier did not match the Fathers or claims used in the body of the sheet.
- The witness and final synthesis tables lacked section headings, which weakened navigation in the PDFs.
- A few confident symbolic conclusions needed clearer separation between a Father's documented reading and the editor's inference.

The current method responds by assigning one job to each section, accounting for the complete liturgical sequence, labeling source status, matching the quotation dossier to the body, and ending with an ordered homiletic architecture rather than a third thematic recap.

The week-by-week audit produced these specific judgments and revisions:

| Week | Strongest feature retained | Main weakness corrected |
| --- | --- | --- |
| Trinity Sunday | The one Name, intellectual humility, doxology, and mission form a strong doctrinal arc | The distinct ferial formulary had been blended into the feast; it is now an explicitly separate comparison, and the feast's Secret supplies its own moral hinge |
| Second Sunday | The wide place, open house, and practical test of charity make the banquet concrete | `Domine, convertere` had been misread as the soul being turned; it addresses the Lord, while the Secret's `transferat` carries the transformation theme |
| Third Sunday | The lion/Shepherd contrast and angelic joy give repentance emotional and ascetical range | The draft overstated passivity and called the murmurers righteous; grace's initiative is now joined to repentance and resistance, with matched Luke 15 witnesses |
| Fourth Sunday | Romans 8 gives apostolic frustration a bodily and cosmic horizon | The strongest hinge had been omitted: the Secret now places the rebellious will under Christ's efficacious word |
| Fifth Sunday | Altar, brother, tongue, and reconciliation form the set's tightest pastoral synthesis | The Collect had incorrectly been described as asking for fear; infused love and the Secret's common-good offering now govern the sequence |
| Sixth Sunday | Baptismal burial followed by wilderness feeding is a clear mystagogical arc | Eucharistic and doctrinal bread readings were blurred, and the Cyril quotations did not support burial; the claims and primary loci are now separated and matched |
| Seventh Sunday | Fire and sacramental medicine hold judgment and healing together | “Cannot” had been weakened and moral fruit confused with doctrinal truth; conversion, moral evidence, and the apostolic norm of doctrine are now distinguished |

## Methodology

### 1. Establish the textual base

1. Locate the Sunday or feast in the local 1962 temporal corpus.
2. Record the Introit, Collect, Epistle, Gradual, Alleluia, Gospel, Offertory, Secret, Communion, and Postcommunion. Record a displaced Sunday or exceptional rubric when it materially affects the week.
3. Check incipits, biblical references, and the sequence against the corpus. Treat suspicious OCR forms as unresolved rather than silently repairing them.
4. Read the Epistle and Gospel in context, then read the psalm or biblical contexts from which the chants are excerpted.

Do not merge texts from separate formularies and then call them the Church's grouped instruction. A displaced or ferial Mass may be compared in a clearly labeled note, but the synthesis of a feast must first be built from the texts actually heard at that feast.

The first-page summary has nine rows in liturgical order: Introit, Collect, Epistle, Gradual, Alleluia, Gospel, Offertory, Communion, and Postcommunion. Its four columns identify the proper, text or reference, scriptural axis, and connection. Source status belongs in the later exegetical and witness sections rather than in this compact overview. The Secret, although omitted from page 1 for space, must be treated explicitly in `Patristic Exegesis of the Grouped Propers` as the hinge between offered gifts and sacramental reception.

### 2. Derive the controlling question

Before consulting secondary themes, ask four textual questions:

1. What condition does the Introit place the worshipper in: praise, poverty, danger, desire, confidence, or repentance?
2. What grace does the Collect ask God to supply?
3. What diagnosis and promise emerge when the Epistle and Gospel are read together?
4. How do the Offertory and Secret turn that teaching into sacrifice, and how do the Communion and Postcommunion turn it into received grace and a continuing way of life?

The answer becomes the week's controlling liturgical thesis. It must explain movement, not merely list themes.

### 3. Test the thesis with the four senses

Use the four senses as controls on interpretation:

- **Literal:** state what the appointed text says in its narrative, grammatical, and canonical setting.
- **Allegorical:** identify Christ, the Church, salvation history, or sacramental fulfillment without erasing the literal sense.
- **Moral:** name the conversion, virtue, renunciation, or action demanded of the hearer.
- **Anagogical:** identify the final judgment, resurrection, heavenly worship, or eternal communion toward which the text tends.

If a proposed synthesis cannot be stated coherently in all four registers, it is probably too thin or too detached from the appointed texts.

### 4. Extract the symbolic grammar

Select concrete images that actually occur in the readings or propers: name, depth, banquet, sheep, coin, boat, net, altar, brother, burial, bread, tree, fruit, wolf, fire, medicine, and similar images.

For each symbol:

1. Locate it in the appointed text.
2. Place it within its broader scriptural field.
3. Identify a documented patristic use when one is available.
4. State what it reveals about Christ, the Church, the sacraments, the soul, or the last things.
5. Explain how it advances this Mass's instruction.

Shared Christian symbolism is not automatically the exegesis of a named Father. When the final connection is editorial, say so by writing in the project's voice rather than attributing it.

### 5. Read the propers as a liturgical argument

This is the exegetical center of each sheet. Follow the texts in the order in which the Church gives them:

```text
entrance condition
  -> petition for grace
  -> apostolic diagnosis
  -> chanted response and preparation
  -> Gospel disclosure or command
  -> self-offering and Secret
  -> sacramental reception
  -> postcommunion effect
```

The first table in `Patristic Exegesis of the Grouped Propers` must account for every stage. Each row should distinguish:

- the primary text and its function;
- the documented patristic reading or an explicitly editorial reading;
- the spiritual diagnosis;
- the reason the text stands at that point in the Mass.

End the section with one concise statement of the Church's grouped instruction. Do not add another table that merely repeats the same pairings.

### 6. Build the patristic dossier

Prefer witnesses who comment on an appointed passage or its immediate theological question. A famous saying is not enough merely because it fits the theme.

For each witness:

1. Identify author, work, and section or homily where available.
2. Decide whether the body will quote, paraphrase, or list the work only as a study lead.
3. Explain what interpretive claim the witness controls.
4. Put every selected direct quotation in the final `Full Patristic and Saintly Texts` section.
5. Confirm that every quotation in that final section is used or clearly relevant earlier in the sheet.

Short excerpts are preferred. Ellipses must not alter the argument. If wording has not been verified, convert it to a labeled paraphrase.

### 7. Resynthesize for preaching

After exegesis, produce a `Homiletic Synthesis` with five distinct elements:

- **Proposition:** one sentence the homily is trying to establish.
- **Movement I -- gift:** what God reveals, initiates, or gives.
- **Movement II -- resistance:** the sin, fear, illusion, or disorder exposed by the texts.
- **Movement III -- sacramental conversion:** how the altar enacts the passage from diagnosis to grace.
- **Final horizon:** the concrete practice and eternal end toward which the hearer is directed.

This is not a summary of every section. It is a preach-able order that preserves the logic discovered in the propers.

### 8. Apply quality gates

Before a week is complete, check that:

- all ten principal proper elements are accounted for at least once;
- separate formularies are not blended without an explicit comparison label;
- page 1 contains only the title, any necessary rubric note, and the summary table;
- the page-one table includes distinct Gradual and Alleluia rows and has no source-status column;
- `Four Senses of Scripture` begins on page 2;
- literal claims can be traced to the appointed text;
- named patristic claims have an identified source or are labeled as study leads;
- quotation marks occur only around checked wording;
- the final quotations match the body and include work/section attribution;
- applications arise from the liturgical argument rather than from a generic seasonal theme;
- no later table merely repeats an earlier table;
- the PDFs build twice without fatal errors and are visually checked for overflow, split headings, and unreadable cells.

## Series-Level Synthesis

Read together, the first seven weeks form a coherent post-Pentecost pedagogy. This is an editorial observation about the sequence, not a claim that the temporal cycle was historically composed as a seven-part treatise.

| Week | Governing gift | Disorder exposed | Liturgical formation |
| --- | --- | --- | --- |
| Trinity Sunday | The one divine Name and the mercy of Father, Son, and Holy Ghost | Pride that tries to master mystery or confess it without charity | Adoration becomes baptismal identity, praise, mercy, and mission |
| Second Sunday | The gratuitous supper and the breadth of divine invitation | Lawful goods hardened into excuses; love confined to words | The invited beggar is turned, fed, and made capable of charity in deed |
| Third Sunday | The Shepherd's initiative and heaven's joy | Pride, isolation, vigilance without hope, and resentment at another's return | The endangered sinner consents to be found, carried, restored, and celebrated |
| Fourth Sunday | Christ's efficacious word in a groaning creation | Activism, discouragement, and a rebellious will after fruitless labor | The Church hears, launches, offers even the will, and receives strength for mission |
| Fifth Sunday | Charity that makes sacrifice truthful | Anger, contempt, retaliation, and ritual used to evade the brother | Prayer and offering pass through reconciliation into ecclesial Communion |
| Sixth Sunday | Baptismal participation in Christ and bread for the journey | The old servitude and the fantasy of self-sustained new life | The old man is buried, the new man is fed, steadied, cleansed, and fortified |
| Seventh Sunday | Sanctification bearing fruit under Christ the King | False appearance, neutral accounts of freedom, and judgment without self-judgment | Doctrine and life are tested humbly while sacramental medicine heals the root |

The cumulative movement is from divine gift to embodied fruit: the Trinity is adored, charity accepts the banquet, mercy seeks the lost, obedience launches the Church, reconciliation purifies sacrifice, baptismal life is fed, and sanctification becomes discernible in works.

## Weekly Document Structure

Each weekly `main.tex` follows this order:

1. `\weektitle`, with the English week, Latin liturgical title, and TLM context.
2. An optional factual source/rubric note.
3. A four-column page-one `properstable` summarizing the Introit, Collect, Epistle, Gradual, Alleluia, Gospel, Offertory, Communion, and Postcommunion; attribution and source status are reserved for later sections.
4. `Four Senses of Scripture`, beginning on page 2 with exactly four rows.
5. `Core Scriptural Symbols`, treating developed biblical images rather than generic themes.
6. `Patristic Exegesis of the Grouped Propers`, the longest interpretive section and the complete liturgical argument.
7. `Exegetical Notes`, limited to close textual observations useful for preaching.
8. `Patristic and Saintly Witnesses`, with quotation/paraphrase status clear in every row.
9. `Homiletic Synthesis`, ordered as proposition, gift, resistance, sacramental conversion, and final horizon.
10. `Preaching Applications`, short and concrete.
11. `Primary References`, including the missal corpus and the primary works actually used.
12. `Full Patristic and Saintly Texts`, containing two to four checked, short quotations used by the sheet.

## Future Codex/GPT Notes

When extending the project:

- Preserve the method and sequence above unless the user asks for a structural change.
- Keep the TLM proper texts central; a topical devotional built around the Gospel alone does not belong in this series.
- Make the Gradual, Alleluia, Secret, and Postcommunion do interpretive work.
- Prefer exact primary works over lists of impressive names.
- Distinguish quotation, paraphrase, study lead, and editorial inference.
- Do not invent a patristic consensus where witnesses differ or where no source has been checked.
- Regenerate PDFs with `make`, visually inspect them, then run `make clean` before committing.
- Commit meaningful changes in the nested `liturgical-year` repository.
