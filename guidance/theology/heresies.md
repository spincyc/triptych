# Historical Heresy Reference Works

This profile governs repeatable historical and theological reference works beneath `src/gpt/theology/heresies/`. These works study condemned propositions, persons, schools, movements, and ecclesial responses across Catholic history. They are neither general discursive articles nor juridical determinations of a living person's culpability. Publishable leaves mirror to `build/gpt/theology/heresies/<document>.pdf` and `doc/gpt/theology/heresies/<document>.pdf`.

## Comprehensive claims and the controlling census

No title, ancient heresiology, conciliar collection, or modern handbook supplies a self-authenticating universal list of every heresy. A work may call itself comprehensive only when it defines a reproducible corpus and accounts for every item in that corpus as one of:

- a full dossier;
- an alias, subgroup, or proposition assigned to a named dossier;
- a compact source-limited notice when a catalogue preserves a distinct attributed error but the evidence does not support a full dossier;
- a contextual controversy treated without the formal label of heresy; or
- a reasoned exclusion whose basis is recorded.

The document keeps `research/corpus-inventory.md` as the controlling census. The inventory records a stable namespaced dossier key, normalized name and aliases, dates and places, historical object type, baseline witnesses, formal response when one exists, treatment class, evidence grade, document location, and unresolved classification issues. Narrative prose and timelines may explain this inventory but may not silently broaden it. “All,” “complete,” or “comprehensive” is always qualified by the named census rule; the work must not imply that the Catholic Church maintains a universal retrospective register of culpable persons.

The minimum census for an all-history survey reconciles the principal ancient Greek and Latin heresiologies; groups and propositions named in the dogmatic acts of the ecumenical councils received by the Catholic Church; consequential papal, Roman, regional-synodal, and medieval canonical condemnations; the Reformation-era propositions answered by papal acts and Trent; and the principal modern Roman doctrinal censures through the stated as-of date. Private compendia and modern critical editions are indexes and textual witnesses, not promulgating authorities.

## Terms, objects, and censures

Current Latin canon law defines heresy, apostasy, and schism in canon 751. That definition supplies a present conceptual boundary; it is not retroactively imposed as a penal finding on every ancient or medieval subject. Keep at least these axes distinct:

1. **Historical object:** proposition or formula; person; school or tendency; organized movement; ecclesial communion; schism; disciplinary practice; or allegation and historiographical construction.
2. **Doctrinal relation:** materially incompatible proposition; formally condemned proposition; dogmatic counter-definition; theological dispute not settled as heresy; or anachronistic, disputed, or merely polemical label.
3. **Recorded censure:** preserve the act's own grade and scope, including `heretical`, `erroneous`, `rash`, `scandalous`, `seditious`, `offensive to pious ears`, anathematized, prohibited, excommunicated, or deposed. A list condemned with several grades may not be rewritten as a list of heresies.
4. **Personal status:** distinguish what a text says, whether a person authored or accepted it, the evidence of obstinacy, recantation or reconciliation, and any penalty. Never infer the internal forum or present culpability of descendants.
5. **Mechanism and jurisdiction:** patristic refutation, episcopal act, local or regional synod, papal letter or constitution, ecumenical council, profession of faith, inquisitorial judgment, or civil act. Name the promulgating or adjudicating authority, date, locus, territory, confirmation, and force actually established.

An anathema, deposition, excommunication, prohibition, or civil penalty does not by itself prove that every disputed proposition was solemnly defined as heresy. Conversely, a council may positively define doctrine without producing a complete sociological description of the movement it answered.

## Required records

Every document leaf keeps one `generation-metadata.tex` record, imports it once in the terminal metadata section, and keeps:

- `research/scope.md`, stating question, reader, thesis, corpus rule, period and geography, authority classes, included and excluded objects, currentness needs, uncertainties, quotation and rights limits, and review state;
- `research/source-audit.md`, mapping consequential claims to exact acts, texts, editions, loci, source classes, translation status, and unresolved discrepancies;
- `research/corpus-inventory.md`, the controlling normalized census and alias/exclusion ledger; and
- `research/timeline-audit.md` when the publication contains a timeline, mapping every timeline row to its source and qualification.

If a later volume shares a canonical inventory or source fragment, place that source at the narrowest common ancestor and import it. Do not copy a census into several publications. Rebuild and inspect every consumer after a shared source changes.

## Source hierarchy and evidence grades

Prefer, in order:

1. the extant act itself: conciliar creed, definition, canon, sentence, acts, papal letter or constitution, doctrinal decree, local synodal record, profession, or judgment;
2. the target's extant writing or a critically identified fragment;
3. a critical edition, official translation, or scholarly documentary collection that identifies the underlying witness;
4. near-contemporary historical reports and patristic or medieval refutations; and
5. later heresiologies, handbooks, inquisitorial summaries, aggregations, or modern secondary reconstruction.

Assign the controlling evidence one of these grades:

- **A:** extant formal act and extant target text;
- **B:** extant act, but the target survives only in extracts, judicial propositions, or summary;
- **C:** near-contemporary report without an extant formal act; or
- **D:** late, hostile, legendary, or substantially disputed reconstruction.

The grade measures documentary access, not theological gravity. Heresiologists and inquisitorial records are interested witnesses. State when the proposition is a refuter's formulation, a judicial extract, a recantation formula, or the target's own words. Do not quote a modern translation as though it were the original act or a critical edition. Keep quotations only as long as necessary to identify the doctrinal object, and record the rights status of official texts, translations, and editions.

An item controlled only by grade C or D evidence triggers a targeted gap search before publication: look for the extant act, target text or fragment, critical edition, manuscript or archival description, near-contemporary witness, and current professional reconstruction reasonably accessible online or through cited catalogs. Record the search boundary and consequential negative result in the source audit. A late witness remains late after an unsuccessful search, but the gap must not survive merely because an inherited handbook was convenient.

## Dossier contract

Each full dossier is brief enough for comparison but specific enough to be checked. It uses a substantive heading and these visible fields in a stable order:

- `Object and setting` --- names and aliases, dates, places, proponents or communities, object type, and evidence limit;
- `Propositions at issue` --- exact wording when short and verified, otherwise a tightly checked paraphrase, with the source of the formulation identified;
- `Ecclesial response` --- authority, act, date, locus, jurisdiction, censure, positive doctrinal answer, and any later confirmation; and
- `Aftermath and qualification` --- recantation, deposition, alternative hierarchy, survival, diffusion, coercive action, doctrinal clarification, later agreement, and present terminology.

Civil exile, confiscation, imprisonment, torture, crusade, or execution is reported separately from the Church's doctrinal act. Do not make coercion invisible, attribute a civil sentence to a council, or assume that later similar ideas descend historically from an earlier group. A dossier known principally from opponents states that limitation locally.

## Historical and ecumenical discipline

Ancient catalogues often multiply aliases and derive groups from founders; medieval sources may impose scholastic language on vernacular testimony; Reformation and post-Reformation acts may condemn propositions with mixed censures; modern doctrinal notifications often judge a book or formulation without declaring a new named heresy. Preserve those differences.

When a controversy contributed to a lasting separation, distinguish the proposition historically condemned from the present teaching and members of a separated communion. Christians born into separated communities are not charged with the personal sin of the original separation. Modern common Christological declarations, agreed statements, reconciliations, and clarifications belong in the aftermath when they materially change the accuracy of inherited labels. Do not use “Nestorian,” “Monophysite,” “Lutheran,” “Calvinist,” “Anglican,” or another inherited label as a complete present-day adjudication.

Religious communities outside Christianity, ordinary sins, abuses, political programs, disputed schools permitted within Catholic theology, schisms without a defining doctrinal error, and accusations disproved or too uncertain to reconstruct belong in the contextual or exclusion ledger rather than being forced into the dossier count.

## Publication architecture

A comprehensive all-history volume:

- begins with a title page and table of contents, then proceeds directly to the apostolic or earliest historical boundary and chronologically through the dossiers while keeping related doctrinal complexes together;
- states the positive Catholic doctrine clarified by each major response rather than becoming only a catalogue of error;
- includes a conclusion identifying recurrent doctrinal fault lines without claiming genealogical descent where none is documented;
- includes a chronological appendix of response events with date, place, object, authority and act, immediate aftermath, longer reception, and evidence grade;
- includes an alias, contextual-controversy, and exclusion accounting appendix or an equally accessible summary of the controlling inventory; and
- includes a terminal `Scope, Terms, and Qualifications` appendix containing the reader warning, period and geographic bounds, census and completeness rule, definitions, current-law boundary, authority and evidence grades, source hierarchy, method, checked-through date, global uncertainties, rights limits, and review state;
- ends with references keyed to exact acts and source families, followed by terminal structured generation metadata.

Order the appendix block after the historical synthesis; the timeline and census accounting may precede or follow `Scope, Terms, and Qualifications` according to use, but none belongs before the first dossier. Use plain language in the body so a reader need not memorize the evidence key. Do not rely on the appendix to cure an overbroad title: remove or qualify `all`, `complete`, or `comprehensive` in the title itself when the named corpus cannot sustain it. Censure grade, disputed attribution, hostile-witness status, personal-status limit, and present ecumenical qualification remain in the dossier they govern.

The timeline uses one row per datable response, not one row per vague movement. It preserves circa dates, rival sessions, later confirmations, mixed censures, and uncertain provenance. It must not compress ecclesial judgment and civil enforcement into one unlabeled event.

## Currentness and review

Stable historical acts do not need artificial legal currentness. The terminal scope appendix nevertheless displays `checked through YYYY-MM-DD` for current canon law, current doctrinal documents, and modern ecumenical or ecclesial-status claims. Before installation, recheck the current Code, recent Dicastery for the Doctrine of the Faith acts material to the scope, and official common declarations cited as present qualifications.

Source audit is not independent historical, theological, canonical, ecumenical, or ecclesiastical review. Catalog and title-page maturity language must preserve that limitation. A broad survey must expressly warn that brevity can identify propositions and responses but cannot replace specialized histories or establish personal culpability.

## Completion gate

A historical heresy reference is ready to publish only when:

- every comprehensive claim agrees exactly with the controlling census and every baseline item is assigned or reasonedly excluded;
- each dossier distinguishes object, proposition, act, authority, censure, positive doctrine, aftermath, evidence, and present qualification;
- mixed censure grades, disputed attributions, hostile witnesses, aliases, and modern ecumenical agreements are not flattened;
- ecclesial definitions, disciplinary measures, and civil coercion remain distinct;
- the timeline agrees with the dossiers and every row is audited;
- the first dossier follows the title and contents without an intervening warning, method, terminology, census, evidence-grade, currentness, or limitation chapter, and those global controls appear once in the terminal appendix block;
- every grade C or D baseline item has received and recorded a targeted source-gap search;
- quotation, translation, official-text, and third-party rights boundaries are recorded;
- current law and present ecclesial claims are rechecked and date-qualified;
- independent specialist review is claimed only when actually recorded; and
- universal metadata validation, terminal provenance, settled multi-pass build, log inspection, every-page visual review, PDF structure checks, installed/build comparison, supporting records, catalog integration, and release-policy accounting are complete.
