# Historical and Hagiographic Biographies

This profile governs the repeatable biography collection beneath
`src/gpt/biographies/`.  It applies to source-first studies of saints and other
figures in the history of the Church whose lives must be read both historically
and through their ecclesial reception.  These works are neither devotional
legendaries, critical editions, canonization dossiers, nor general discursive
articles.  They follow this profile together with `guidance/editorial.md` and
`guidance/repository.md`.

Publishable leaves live at `src/gpt/biographies/<subject>/`; transient and
installed PDFs mirror them at `build/gpt/biographies/<subject>.pdf` and
`doc/gpt/biographies/<subject>.pdf`.  The provider-relative path
`biographies/<subject>` is the stable, namespaced publication identifier.  Use
an unnumbered lowercase kebab-case subject slug: the collection is not a rank of
sanctity or a closed chronological sequence.  A `biographies/shared/` directory
may own non-publishable typesetting primitives or genuinely common source
fragments; it has no PDF mirror, must be imported rather than copied, and every
consumer must be rebuilt after it changes.

## One life per publication

Give each person an independent publication, source record, chronology, and
tradition audit.  A shared feast, mission, controversy, friendship, or martyrdom
tradition does not merge two lives when their evidence and reception differ.
Cross-link the related biographies and explain the shared history from each
person's own evidentiary horizon.  A collective biography is appropriate only
when the group, rather than its individual members, is the actual historical
subject and the research scope proves that one record can represent it without
flattening distinct evidence.

Saint Peter and Saint Paul therefore receive separate biographies.  Their
common Roman memory and joint solemnity belong in both works, with the overlap
stated rather than copied as one drifting shared narrative.

## Governing aim and reader

A biography should let a serious general reader follow a life through time,
understand its historical world, locate the strongest evidence, encounter the
person's sanctity and ecclesial reception, and see exactly where later
hagiography exceeds recoverable history.  It may be spiritually attentive, but
its prose must not turn devotional usefulness into proof or historical
uncertainty into disbelief.

The opening scope states:

- the subject, ordinary forms of the name, dates or responsible date range,
  places, Church or ecclesial setting, and principal offices or states of life;
- the intended reader and depth;
- the historical and hagiographic question, governing thesis, and source
  boundary;
- whether the work treats an apostle, martyr, Father, Doctor, founder, ruler,
  visionary, missionary, or another kind of subject;
- the geographic, linguistic, ritual, and jurisdictional limits that materially
  affect the evidence; and
- any mutable recognition, relic, shrine, institutional, or liturgical claim
  checked through a stated date.

## Required source records

Every leaf keeps and imports one `generation-metadata.tex` record and keeps the
following reader-facing audit records:

- `research/scope.md`: document identity, question, reader, thesis, included
  and excluded material, source corpus, evidence classes, material
  uncertainties, rights boundary, and completed and outstanding review;
- `research/source-audit.md`: consequential claims mapped to exact sources and
  loci, witness date and genre, edition or translation status, evidentiary use,
  and necessary limit;
- `research/chronology.md`: a claim-by-claim chronology that distinguishes
  dated events, approximate reconstructions, relative sequence, competing
  chronologies, and dates supplied only by later tradition; and
- `research/tradition-audit.md`: traditions about death, burial, relics,
  miracles, appearance, patronage, iconography, sayings, foundations, and other
  memorable episodes, recording the earliest located witness, later reception,
  historical status, and what the tradition may responsibly signify.

The records may cite the same source for different functions, but they must not
be four copies of one bibliography.  Focused retrieval extracts are optional
and remain non-publishable evidence; complete scans, bulk OCR, and copyrighted
editions are not vendored.

## Evidence architecture

Classify evidence by both date and genre.  Sustained publication prose uses
plain language; research records and compact evidence keys or tables may use
these codes when each one is visibly explained:

- **A — autobiographical or subject-authored:** a work, letter, sermon, preface,
  inscription, or other source by the subject, read according to its genre and
  transmission;
- **N — near-contemporary external witness:** evidence from a contemporary or
  near contemporary who is not simply repeating the subject;
- **E — early received tradition:** an ancient witness removed from the event
  but early enough to establish reception, memory, cult, or an otherwise lost
  report;
- **L — later hagiographic or devotional tradition:** a later life, legend,
  sermon, liturgical text, iconographic convention, or local memory whose value
  may be theological, devotional, cultural, or reception-historical without
  supplying contemporary fact;
- **M — magisterial or official ecclesial reception:** a conciliar, papal,
  dicasterial, episcopal, liturgical, canonization, shrine, or institutional act,
  limited to what that act actually establishes;
- **K — modern critical reconstruction:** a conclusion of identified modern
  scholarship, including its premises, alternatives, and degree of confidence;
  and
- **S — source-grounded project synthesis:** an editorial connection supported
  by named evidence and not attributed verbatim to any source.

“Primary” does not mean “contemporary,” “eyewitness,” “neutral,” or
“historically certain.”  A late ancient saint's life can be a primary source for
the age that produced it while remaining late evidence for the life it narrates.
An autobiography gives privileged access to remembered experience and
self-presentation, not an unmediated transcript.  A hostile source may preserve
facts while distorting motive; a panegyric may preserve memory while arranging
it for praise.  State those genre effects where they matter.

## Historical and hagiographic discipline

Build the historical account from the earliest and best-controlled evidence,
then trace reception forward.  Do not write a seamless omniscient narrative by
silently combining sources composed in different decades or centuries.  When
accounts differ, name the witnesses, distinguish contradiction from different
selection or viewpoint, and explain whether a synthesis is secure, plausible,
or unresolved.

Hagiography is evidence of Christian memory, sanctity, imitation, cult, and
theological interpretation.  It is not a synonym for falsehood, and historical
criticism is not permission for contempt.  At the same time:

- do not backdate the first located witness;
- do not turn a motif shared with other saints into independent corroboration;
- do not use canonization, a feast, a basilica, patronage, or an approved cult to
  authenticate every narrated episode;
- do not make an archaeological possibility prove the personal identity of a
  tomb, relic, house, prison, or artifact;
- do not convert silence into disproof when the record is merely incomplete;
  and
- do not keep a vivid story in the historical narrative after its source has
  been found to be late, transferred, anachronistic, or unsupported.  Place it
  in the tradition history with its actual status.

Miracle reports are narrated according to their sources.  Scripture's inspired
testimony, a contemporary report, a canonization inquiry, a later saint's life,
and a popular legend do not carry the same historical or theological function.
The project neither invents a natural explanation nor certifies a supernatural
event on its own authority.  It may state what the Church receives or a
competent act judges, but only within that act's object and scope.

## Scripture and apostolic subjects

For a biblical person, inventory every material passage before drafting.  Read
each book as a distinct literary and theological witness; identify authorship,
date, audience, and historicity questions only to the degree needed for the
biography.  Parallel Gospel scenes, Acts, letters, and later ecclesial testimony
must not be collapsed into one quotation-free harmony that hides their sources.

Distinguish:

- the narrated event from the date and purpose of the surviving narrative;
- the subject's words as reported by a source from a modern verbatim transcript;
- undisputed subject-authored letters from disputed or pseudonymous writings,
  without pretending that a disputed attribution has been settled by assertion;
- an inspired theological portrait from a complete modern biography; and
- apostolic or Roman reception from the exact circumstances of a martyrdom that
  no contemporary narrative describes in full.

The canonical text governs its theological claims.  Modern historical
reconstruction may analyze sequence, social world, travel, language, conflict,
and probable date; it may not demote the text's ecclesial status by rhetorical
sleight of hand or claim more historical precision than the evidence permits.

## Authors, Fathers, Doctors, and disputed works

For a prolific subject, treat writings as biographical evidence and as works
with their own chronology, genre, audience, revision history, and transmission.
Use exact book, section, letter, sermon, preface, or retraction loci.  Do not
construct a personality from isolated maxims or assign every work transmitted
under a famous name to that author.

Explain major controversies in their historical sequence and quote opponents
through surviving sources fairly.  Distinguish what the subject held at a
particular date, later correction or development, the Church's subsequent
reception, and modern debate.  Sainthood or the title Doctor of the Church does
not make every historical judgment, exegetical opinion, polemical tactic, or
disciplinary proposal irreformable.  Candidly address consequential failures,
hard texts, and contested legacies without reducing a life to them.

## Chronology, geography, and social world

Dates are claims, not decorative labels.  State the calendar and conversion
assumptions when they matter.  Use ranges, `before`, `after`, `by`, relative
sequence, or competing columns instead of false precision.  A later feast day
does not by itself establish a death date.

Identify ancient place names and responsible modern equivalents without
claiming uncertain borders.  Explain travel conditions, political authority,
language, family, education, class, patronage, slavery, gender, clerical office,
monastic form, and institutional structures only where sources make them
biographically consequential.  Maps are optional; if used, they require a
source and uncertainty statement and must remain legible in monochrome.

## Death, burial, relics, cult, and visual memory

Treat death and posthumous reception in separate evidentiary stages:

1. earliest evidence for death or martyrdom;
2. earliest located burial or cult witness;
3. translation, identification, opening, or scientific examination of remains;
4. liturgical and institutional reception;
5. later relic claims and competing local traditions; and
6. iconographic attributes, patronage, legends, and modern commemoration.

Name the authority, date, method, and published result for an archaeological or
scientific claim.  “Consistent with,” “traditionally identified,” and
“authenticated as the person” are not interchangeable.  Do not report a relic
or shrine's present status from an old source when a current official claim is
material; record the verification date.

Iconography is a history of reception, not a portrait photograph.  Explain
attributes such as keys, sword, book, lion, mitre, cardinal's dress, or a
particular physiognomy by their earliest controlled use and theological meaning
where possible.  Flag anachronistic dress or office without treating it as an
artist's historical claim.

## Publication architecture

Every full biography contains, in an order suited to the life:

- a title page with structured AI provenance and an explicit study limitation;
- a table of contents;
- a short method and evidence key;
- a one- or two-page chronological orientation;
- the subject's world, names, identity, and source problem;
- a sustained chronological life rather than a list of virtues;
- the person's writings, teaching, mission, office, relationships, and major
  controversies where applicable;
- death, burial, and the earliest cult or memory;
- later hagiography, liturgy, iconography, patronage, and institutional legacy;
- a dedicated `Tradition under review` section that reports memorable doubtful
  or late episodes without either credulity or ridicule;
- a final synthesis of sanctity, historical significance, and unresolved
  questions; and
- a detailed chronology and references.

The orientation may use tables, but the life itself should read as a coherent
biography.  Repeated evidence panels use stable visible fields such as `Claim`,
`Witness`, and `Limit`; do not force every paragraph into a box.  The references
identify editions and translations actually used, stable links and access dates
for material online evidence, and modern scholarship by full bibliographic
description.

## Rights, metadata, catalog, and maturity

Prefer paraphrase and short, necessary quotations.  Scripture, patristic and
official translations, liturgical texts, historical lives, modern scholarship,
images, and archival or archaeological reports retain their own rights status.
Record the translation and public-domain, licensed, permission, or quotation
basis in the source audit; do not assume that an ancient author makes a modern
translation public domain.  A biography does not need an image to be deep.

Display structured generation metadata once on the title page.  Catalog each
PDF only on `library/biographies.md`, followed by links to all four required
research records.  Catalog maturity distinguishes source audit, historical or
patristic specialist review, theological review, rights review, production
review, and ecclesiastical approval.  Use `source-audited working biography`
only after the source audit and publication checks are complete.  Never let
`saint`, `Doctor`, `apostle`, or `martyr` imply that the project has obtained an
imprimatur or independent review.

## Completion gate

A biography is ready to install only when:

- the historical core, early reception, later tradition, modern reconstruction,
  and project synthesis remain distinguishable;
- material chronology and geography are sourced and uncertainty is visible;
- every consequential vivid episode has an earliest located witness or is
  marked unresolved;
- subject-authored and disputed writings are classified responsibly;
- miracles, sanctity, canonization, cult, relics, archaeology, liturgy,
  patronage, and iconography are not made to prove more than their sources;
- difficult actions, disagreements, and contested legacies receive proportionate
  treatment rather than apologetic omission or presentist caricature;
- `scope.md`, `source-audit.md`, `chronology.md`, and `tradition-audit.md` agree
  with the publication and record rights and review limits;
- exact references, structured metadata, PDF title and subject, and the catalog
  entry are complete;
- compilation is settled, logs are clean of fatal, undefined-reference, and
  overflow errors, every page is visually inspected, PDF structure and fonts
  are checked, and the installed PDF is byte-identical to the reviewed build;
  and
- independent historical, theological, linguistic, archaeological, or
  ecclesiastical review is claimed only when actually recorded.
