# Third-Party Material

Triptych is a source-based collection. Its sources and PDFs quote, transcribe,
or incorporate material that the project does not own. The project's CC BY
4.0 license applies only to project-created contributions and does not apply
to the third-party or public-domain material described below.

## Retained Reusable Source Artifacts

The reusable source library under `src/sources/` may retain exact source bytes
when an artifact manifest records an affirmative distribution basis. Those
bytes keep their own status and are not offered under Triptych's CC BY 4.0
license merely because they are committed beside project-created metadata.

The retained 1871 English *City of God* texts are normalized derivatives of
Project Gutenberg eBooks 45304 and 45305. Marcus Dods edited the edition and is
the named translator; George Wilson translated Books IV, XVII, and XVIII, and
J. J. Smith translated Books V--VIII. Douglas L. Alley III, Charlene Taylor,
Joe C, and the Online Distributed Proofreading Team produced the Gutenberg
transcriptions from Internet Archive and Canadian Libraries images. The
retained derivatives remove the Gutenberg wrapper, license, trademark
references, and marker lines; normalize line endings; and otherwise preserve
the transcription between the markers. The transcriber notes disclose
punctuation and spelling corrections, so these files are neither facsimiles
nor diplomatic transcriptions. The 1871 text is recorded as public domain in
the United States; users must determine its status in other jurisdictions.

The retained Patristic Text Archive transcriptions of Severian of Gabala's six
homilies *In cosmogoniam* are governed by their recorded [Creative Commons
Attribution-ShareAlike 4.0 International
License](https://creativecommons.org/licenses/by-sa/4.0/), not Triptych's CC BY
4.0 license. Each source file states that licence in its own header, and the
licence was read per file rather than inferred from the archive, whose README
records that its files carry different Creative Commons licences. Sever J. Voicu
transcribed the Greek from Migne's *Patrologia Graeca* 56, Paris 1862, and
corrected and standardised its spelling, accents, and punctuation to modern
editorial standards; Annette von Stockhausen converted the transcription to
CTS-compliant PTA TEI and added the biblical references and the annotation of
persons, groups, and places. The publisher is the Berlin-Brandenburgische
Akademie der Wissenschaften. Reusers must retain that attribution, indicate
changes, and satisfy ShareAlike where the licence requires it. The retained
derivatives carry the Greek alone: the TEI header, the editors' annotation, the
biblical pointers, the manuscript apparatus, and the source printing's page and
line breaks are removed, and the retained files are neither facsimiles nor
diplomatic transcriptions. Severian's fourth-century Greek and the modern
transcription and encoding of it remain distinct rights objects.

The retained Latin Wikisource transcriptions of Migne's *Patrologia Latina* --
Ambrose's *Hexameron* (PL 14), Jerome's *Liber quaestionum hebraicarum in
Genesim* (PL 23), Bede's *In principium Genesis* (PL 91), Alcuin's
*Interrogationes et responsiones in Genesim* (PL 100), Angelomus of Luxeuil's
and Remigius of Auxerre's *Commentarii in Genesim* (PL 115 and PL 131), and
Augustine's *De Genesi ad litteram* (PL 34) -- reproduce printings of 1841 to
1853 that are public domain in the United States. The wiki source of those pages
is licensed CC BY-SA 4.0, a condition on the contributors' markup rather than on
Migne's text beneath it; the exact wiki bytes are hashed and recorded but not
retained, and the retained derivatives carry the printed Latin alone, with every
template, link, heading, category, footnote, and column marker removed, together
with the University of Zurich Corpus Corporum encoding note that identifies the
encoder rather than the text. Those derivatives are transcriptions of a web
witness of the printing and not collations against the printed column.

The retained University of Leipzig/OpenGreekAndLatin CSEL 40.1--40.2 TEI files
are governed by their recorded [Creative Commons Attribution-ShareAlike 4.0
International License](https://creativecommons.org/licenses/by-sa/4.0/), not
Triptych's CC BY 4.0 license. The unmodified XML headers identify University of
Leipzig (2014), Emanuel Hoffmann's 1899--1900 edition, Jouve for OCR,
correction, and encoding, Gregory Crane as principal, and Greta Franzini,
Simona Stoyanova, Bruce Robertson, and Uvius Fonticola in the listed project
roles. Reusers must retain attribution, indicate changes, and satisfy
ShareAlike where the license requires it. The separately manifested figure
referenced by the first XML file reproduces a specimen from the 1899 volume and
is recorded as public domain in the United States. The underlying historical
edition, digital encoding, and support image remain distinct rights objects.

The retained Internet Archive OCR and automated page-number map for *The
Ante-Nicene Fathers*, volume 1, reproduce a Buffalo 1887 publication carrying
an 1885 copyright notice. The volume and notice are public domain in the United
States, and Internet Archive records the item as not in copyright in that
region. The exact uncorrected OCR and generated pagination data are retained as
locating and research derivatives; they are not facsimiles, corrected
transcriptions, or independent textual witnesses. The Roberts--Rambaut
translation and A. Cleveland Coxe's editorial prefaces and bracketed notes
retain their public-domain status and are not offered under Triptych's CC BY
4.0 license. OCR errors must not be attributed to the historical translators,
and Coxe's editorial matter must not be attributed to Irenaeus.

The retained Luke and Revelation running-text files from [Faithlife's SBLGNT
v1.2 repository](https://github.com/Faithlife/SBLGNT) reproduce *The Greek New
Testament: SBL Edition*, edited by Michael W. Holmes, copyright 2010 Society of
Biblical Literature and Logos Bible Software. They are distributed under the
[Creative Commons Attribution 4.0 International
License](https://creativecommons.org/licenses/by/4.0/), not Triptych's CC BY
4.0 license. The retained files are unchanged: each was extracted byte for byte
from the pinned upstream archive, without normalization or editorial
modification. Their artifact records identify the exact upstream commit,
source path, and hash.

The retained lemma-field projection from [*MorphGNT: SBLGNT
Edition*](https://github.com/morphgnt/sblgnt), by James Tauber and the MorphGNT
contributors, is distributed under the [Creative Commons
Attribution-ShareAlike 3.0 Unported
License](https://creativecommons.org/licenses/by-sa/3.0/). It is a modified,
project-created projection of the pinned MorphGNT 6.12 dataset: Triptych read
the 27 canonical-order `*-morphgnt.txt` files, emitted the final
whitespace-delimited lemma field from every nonblank token row in numeric book
order, and placed one lemma on each line. The projection omits the separately
licensed SBLGNT surface-text columns. Reusers must retain the MorphGNT
attribution, this change notice, the license link, and ShareAlike treatment
where the license requires them.

## Liturgical and Scriptural Texts

Scripture, Missal formularies, Orders of Mass, rubrics, chants, and texts from
other liturgical books retain the copyright, public-domain status, license, or
other legal status of their respective sources and editions.

In particular:

- `src/gpt/liturgy/roman-rite/1962/propers/**/propers/retrieved.txt` contains
  focused OCR source extracts and is not offered under CC BY 4.0; and
- the liturgical-text portions of the corresponding `propers/verified.md`
  files, document sources, and PDFs are not offered under CC BY 4.0; and
- English translations carried by the sidecar inventories under
  `src/sources/inventories/*-proper-translations-v1.toml` are overlaid onto the
  calendar mass indexes by `mass-propers` and recorded per proper with their own
  `rights` basis and, where licensed, the notice their licensor requires.
  A `rights` value is local provenance metadata, not an offer to relicense the
  words under this repository's CC BY 4.0 terms; and
- the English translation of *The Roman Missal*, third edition, is copyright
  the International Commission on English in the Liturgy Corporation (ICEL).
  ICEL's *Publication Policies* contain a standing, conditional permission for
  exact approved, recognized, and promulgated ICEL text on a no-fee,
  noncommercial Internet site. That permission is not public-domain status, is
  not a general license for a downloadable file, a clonable data corpus, an
  installed PDF, or another form of publication, and does not imply ICEL
  affiliation, sponsorship, or endorsement. The public repository and bundled
  static-web data therefore do not distribute ICEL text payloads on the
  strength of that web-only permission. Text-free source and rights metadata
  may record the source, permission, and required notice for a future display
  route whose surface satisfies the permission's conditions.

  The governing policy is
  `guidance/liturgical-text-publication-policy.md`; the factual rights records
  are
  `src/sources/inventories/icel-web-permission-rights-v1.toml` and
  `src/sources/inventories/liturgical-english-rights-v1.toml`. The controlling
  current external sources are ICEL's
  [Publication Policies](https://www.icelweb.org/PubPolicy.PDF) for the grant
  and its [copyright page](https://www.icelweb.org/copyright.htm) for the
  acknowledgement form. A display of excerpts from the 2010 translation must
  carry:

  > Excerpts from the English translation of The Roman Missal © 2010,
  > International Commission on English in the Liturgy Corporation. All rights
  > reserved.

  Preserve that wording with any covered excerpt; do not substitute the
  entire-work form, `(c)` for the copyright symbol, or an acknowledgement copied
  from an unofficial intermediary. The acknowledgement identifies the owner
  and satisfies a condition when the permission otherwise applies; it is not
  itself evidence that a payload is exact, approved, promulgated, or cleared
  for a particular surface. USCCB adaptations and proper texts, CCD/*Lectionary
  for Mass* text, NAB/NABRE text, and the Abbey Psalms and Canticles are
  separately controlled and are not covered by ICEL's permission.

  Quarantine of the current public bundle does not erase earlier Git objects.
  Repository history contains commits that tracked ICEL text payloads, Roman
  1962 Latin proper bodies, and a superseded Lasance OCR artifact containing the
  excluded lettered insert at printed pages 1302a--1302d. Whether a
  public-history rewrite, repository replacement, access change, or another
  remedial step is required is a release-policy and counsel decision for the
  maintainer; this notice neither clears those historical copies nor claims that
  current-tree removal makes them undistributed; and
- the English recorded in
  `src/sources/inventories/postconciliar-proper-translations-v1.toml` includes
  non-ICEL routes with different rights positions, and the file marks every
  translation with which basis and witness apply.

  One route is `project-created`: this project's own work, offered under
  CC BY 4.0 with the project's authorship identified at the point of use. They
  translate prayers of the ancient Roman sacramentaries — the Veronense, the
  Old Gelasian, the Hadrianum — which are out of copyright everywhere, and each
  entry names its ancient witness and states every difference between that
  witness and the Missal's own text.

  Other rows are `public-domain` and are not this project's work. Most carry,
  unaltered, the English of *The Roman Missal translated into the English
  language for the use of the laity*, first revised edition (Philadelphia:
  Eugene Cummiskey, 1861), made for the **antecedent** of the prayer — the older
  oration whose Latin this calendar's own recorded Latin reproduces. Each entry
  names that antecedent and enumerates every difference between the two Latin
  texts. The sequences use Edward Caswall's *Lyra Catholica* (London, 1849) and
  name that witness separately. These translations are in the public domain in
  the United States by publication date; Triptych claims no exclusive right in
  their wording and does not offer them under CC BY 4.0.

  Nothing on either non-ICEL route is an approved liturgical translation or is
  derived from ICEL's, and nothing in the file may be used for recitation; and
- the English recorded in
  `src/sources/inventories/roman-1962-proper-translations-v1.toml` comes from
  several public-domain historical witnesses. Sixty-one proper entries use *The
  Roman Missal translated into the English language for the use of the laity*,
  first revised edition (Philadelphia: Eugene Cummiskey, 1861), including three
  page-collated Palm Sunday procession antiphons and the St Augustine Collect
  at printed p. 652, Internet Archive leaf n660; six sequence
  entries use Edward Caswall's *Lyra Catholica* (London, 1849), with the
  *Hymns Ancient and Modern* printing attributed to William Josiah Irons
  (London, complete edition, catalogued 1890) retained as an alternative for
  one sequence; and thirty-two oration entries use Francis Xavier Lasance and
  Francis Augustine Walsh's *The New Roman Missal*, 1945 revised edition, in a
  printing of about 1955--56. Every Lasance entry is bound to an exact
  ordinary-numbered page-image passage. The only Common-of-a-Supreme-Pontiff
  row served from that witness is the Collect on ordinary printed p. 1302;
  none of the five candidate rows on inserted pp. 1302a--1302d is served.

  The Cummiskey book and its tracked public-domain transcription are registered
  under `src/sources/works/eugene-cummiskey/roman-missal-english-laity/`. Its
  unvendored Internet Archive text layer is a Google-produced derivative with
  separate unresolved artifact rights. The Lasance work is public domain in the
  United States by failure to renew registrations A 110108 and A 192159; that
  conclusion is jurisdiction-specific and does not cover the later lettered
  inserts at printed pages 1298a--1298n or 1302a--1302d. The tracked OCR
  derivative mechanically excludes both ranges. The exact source artifact and
  prior Git objects are not offered under CC BY 4.0 merely because the retained
  historical wording has a recorded U.S. public-domain basis.

  These are historical lay-book and hymn translations, not approved liturgical
  translations. Triptych claims no exclusive right in their wording, does not
  offer the wording under CC BY 4.0, and does not authorize any of it for
  recitation. The same 1861 Cummiskey book is also quoted, on the same
  public-domain basis, by antecedent entries in the postconciliar file described
  above; the rights position is identical and only the relation to the prayer
  differs.

Their inclusion as evidence or text for study is not a representation that
they may be extracted and redistributed independently. Their redistribution
status must be established from the governing source and jurisdiction.

## Ecclesiastical, Canonical, and Other Official Texts

Magisterial documents, canons, decrees, judgments, diocesan acts, official
translations, and other ecclesiastical or civil texts remain subject to their
own status. An official character, citation, or public web location does not
by itself place a text under the Triptych license.

## Received Prayers, Hymns, and Translations

Received prayers, antiphons, chants, collects, hymns, and translations not
created by this project are not relicensed. Some historical texts and
translations may be public domain in some jurisdictions; where that is so,
Triptych claims no exclusive right in the underlying wording. Project-created
prayers and translations are CC BY 4.0 only when their project authorship is
identified in the adjacent text or source record.

The repository's source records identify, among other examples, traditional
English prayer forms and Edward Caswall's 1849 hymn translations as public
domain. Users remain responsible for confirming the status applicable to
their jurisdiction and intended use.

## Quotations and Source Records

Quotations and closely transcribed material from books, articles, websites,
surveys, lyrics, prayer books, and other sources remain the property of their
respective rights holders where protected. A surrounding source audit,
annotation, translation, or synthesis may be project-created without changing
the status of the quoted wording.

## Received Project Manuscripts

The shared teaching, exercise, reference, and assessment sources under
`src/gpt/curriculums/ecclesiastical-latin/` derive from a separately supplied
Telos project. That donor tree contained no local license. Authorization to
integrate and edit the manuscript is not recorded as independent evidence of
authorship, ownership, or a general public-distribution license. The prior 52
installed working snapshots received an explicit exact-snapshot distribution
exception on 20 July 2026 under the repository's existing user-attested
authority. Later exact-current-snapshot exceptions bound corrected files from
that same superseded edition. Those bindings remain historical facts about the
prior bytes. The redesigned 37-PDF installed edition received a separate
exact-current-snapshot distribution exception on 23 July 2026. No exception
establishes donor authorship or ownership, supplies a general
public-distribution license, or authorizes extracted donor wording outside the
exact files it binds.
Their course-wide provenance and rights boundary are recorded in the adjacent
`research/edition-manifest.md`, `research/scope.md`, and
`research/source-audit.md`. No donor manuscript wording is offered under CC BY
4.0 unless a later work-specific rights record establishes that basis.

## Fonts and External Software

Published PDFs embed Latin Modern font programs. The altar-server guides and the
reading-plan tracks embed Libertinus Serif, Sans, and Mono font programs as used;
the tracks were reset in Libertinus on 1 August 2026, having been set in Latin
Modern before. Libertinus is supplied
by the Libertinus Project and is not relicensed under CC BY 4.0. The installed
font metadata identifies SIL Open Font License 1.1; the `libertinus` TeX
support files are supplied separately under the LaTeX Project Public License.
The PDFs embed subsetted font programs. TeX packages and other build
dependencies are external software governed by their own licenses; they are
not vendored merely because the build invokes them.

## Reuse and Contributions

Before reusing an excluded passage, consult its citation, the nearby research
record, and the original source. Inclusion, citation, or online availability
is not a promise of permission for independent reuse.

Contributors must identify third-party material and record its known author,
source, attribution, license, permission, public-domain basis, or applicable
legal exception. Do not submit material that Triptych is not permitted to
distribute.
