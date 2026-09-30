# The Angels — Production Plan and Status

Operational record for resuming the work. `PROJECT-WORK.md` (marker
`claude-angelology-2026-09-29`) and `promised-deliverables.toml` hold the
promise; this file holds the per-unit state. Update the status column in the
same commit that changes a unit.

Status values: `planned`, `drafting`, `drafted` (compiles, sourced, not yet
page-reviewed), `reviewed` (every page inspected in a review raster).

## Branch and commits

- Local branch `feature/angelology` (the workspace branch) is pushed to
  `origin/feature/droid/theology/angelology`:
  `git -c credential.helper='!gh auth git-credential' push -u origin feature/angelology:feature/droid/theology/angelology`.
- Commit with explicit paths, subject plus `AI summary:` body, and the
  co-author trailer of the agent doing the work (Factory Droid through
  2026-09-29; Claude Code from 2026-09-30).
- Every model contribution is Opus 5.5; do not switch models.

## Drafting rules for every unit

- Read `guidance/editorial.md` (voice: from within the tradition; state the
  finding, not the process; no meta-labels such as "Key takeaway") and
  `guidance/theology/angelology.md` (grades, dossier fields, and the
  2026-09-30 "Voice and determination" rules) first.
- The lane brief at `.scratch/lanes/BRIEF.md` expands these rules for
  subagent lanes; if `.scratch` has been tidied away, rebuild it from this
  section and the profile.
- Quote only what was read at its locus in an identified witness, and record
  the witness, URL, access date, and loci in `research/source-audit.md`
  under the unit's heading. English Summa quotations follow the English
  Dominican translation; the Latin of key terms follows Corpus Thomisticum.
- Each Summa question gets exposition plus one `\angeldossier` (or
  `\angeldossiersettled` when no contrary opinion is recorded).
- Every article treated is entered in `research/question-inventory.md`.
- Greek is given in italic transliteration through `\gk{}`.
- No TikZ or landscape outside an `\ifdefined\TriptychPrintEdition` print
  branch that has a full textual equivalent beside it.
- Received prayers: identified witness only, Latin and English each with
  its source; never compose or adapt.

## Drafting lanes

Units are drafted by parallel subagent lanes (all Opus 5.5). Each lane
writes only its own unit files plus a transient record (source audit
entries, question- and order-inventory rows, terminology, Scripture cited,
binding candidates, Aquinas parallels, Dionysius citations, open issues);
the orchestrator merges those records into the tracked `research/` files
(`.scratch/lanes/merge.py`, with `MERGE_LANES` naming the lanes) and
commits. Launching all thirteen lanes at once was rate-limited by the
model provider on 2026-09-29, so lanes run about five at a time.

On 2026-09-30 the patristic lanes were split to give each Father real
exposition, a saints lane was added, and a revision lane (`l-voice`)
brought the drafted units to the voice directive.

| Lane | Units |
| --- | --- |
| l1-substance | Angelic substance; Bodies, place, motion |
| l2-knowledge | Intellect and knowledge |
| l3-will-creation | Will and love; Creation, grace, glory |
| l4-fall | Fall and punishment |
| l5-hierarchies | Illumination and speech; Hierarchies and orders; Order of the universe |
| l6a-government-assaults | Government and mission; Assaults of demons; App. demons' powers |
| l6b-guardians | Guardian angels |
| l7-ch | Celestial Hierarchy; App. nine orders; App. Dionysius in the Summa |
| l8-scripture-faith | Scripture; Faith of the Church; App. magisterial chronology |
| l9a-greek-ante | Greek Fathers to Origen and Methodius |
| l9a-greek-nicene | Greek Fathers from Athanasius to Chrysostom |
| l9c-latin | Latin Fathers before Dionysius (Tertullian to Cassian) |
| l9d-augustine | Augustine |
| l9b1-gregory-isidore-bede | Gregory the Great, Isidore, Bede |
| l9b2-medieval-doctors | Medieval Doctors to Lombard; App. comparative orderings |
| l10a-christ-byzantine | Christ, Mary, angels; Byzantine line |
| l10b-disputed | Disputed questions; App. first sin |
| l11-liturgy | Liturgy; Devotion and regulation; App. calendar; App. names |
| l12-saints | The saints and the holy angels |
| l13a-israel | Before the Fathers: Israel's writings outside the canon, the Septuagint, Philo |
| l13b-philosophers | Before the Fathers: the Greek poets and philosophers; the Fathers' account of continuity |
| l-voice | Voice revision of drafted units; record for the fall |
| orchestrator | App. article census, parallels, Scripture index, terminology, witness register, scope, references |

Primary texts are read from their public hosts (New Advent, Corpus
Thomisticum, tertullian.org, CCEL, the Holy See, Denzinger at
patristica.net, Project Gutenberg, archive.org); the source audit gives
each URL and reading date.

## Units

| Unit | File | Status | Principal sources |
| --- | --- | --- | --- |
| Scripture | `sections/00-scripture.tex` | drafted | Douay–Rheims; Vulgate; ST I q. 50 a. 1, q. 108 a. 5 |
| Faith of the Church | `sections/05-faith-of-the-church.tex` | drafted (voice revised 2026-09-30) | Lateran IV *Firmiter*; Vatican I *Dei Filius* 1; Braga I (561); Constantinople (543); *Humani generis* 26; Paul VI (15 Nov 1972); CDF *Christian Faith and Demonology* (1975); John Paul II audiences (July–Aug 1986); CCC 328–336, 391–395 |
| Before the Fathers: Israel | `sections/07-israel-before-christ.tex` | drafting | Septuagint; 1 Enoch; *Jubilees*; *Testaments of the Twelve Patriarchs*; Philo |
| Before the Fathers: philosophers | `sections/08-philosophers-before-christ.tex` | drafting | Hesiod; Plato; Aristotle; Plutarch; Apuleius; Plotinus; Porphyry; Proclus; Eusebius *Praep. ev.* |
| Greek Fathers to Origen | `sections/10-fathers-before-dionysius.tex` | drafting | 1 Clement; Ignatius; Hermas; Justin; Athenagoras; Irenaeus; Clement of Alexandria; Origen |
| Greek Fathers, Athanasius to Chrysostom | `sections/11-greek-fathers-nicene.tex` | drafting | Athanasius; Cyril of Jerusalem; Basil; Gregory Nazianzen; Gregory of Nyssa; Ephrem; Chrysostom |
| Latin Fathers before Dionysius | `sections/12-latin-fathers-before-dionysius.tex` | drafting | Tertullian; Cyprian; Lactantius; Hilary; Ambrose; Jerome; Cassian |
| Augustine | `sections/13-augustine.tex` | drafting | *De civ. Dei* VIII–XII, XV, XXII; *De Gen. ad litt.*; *De Trin.* III; *Enchiridion*; *Enarr. in Ps.* 103 |
| Celestial Hierarchy | `sections/15-celestial-hierarchy.tex` | drafted | CH 1–15 (Parker); PG 3; Aquinas's citations |
| Gregory, Isidore, Bede | `sections/20-fathers-after-dionysius.tex` | planned | Gregory *Hom. in Ev.* 34, *Moralia*, *Dialogues*; Isidore *Etym.* VII.5; Bede |
| Medieval Doctors to Lombard | `sections/21-medieval-doctors.tex` | planned | Anselm; Bernard *De consid.* V, *Qui habitat* 11–12; Hugh of St Victor; Hildegard; Lombard *Sent.* II dd. 2–11 |
| Angelic substance | `sections/30-angelic-substance.tex` | drafted | ST I q. 50; *De ente* 4; *De sub. sep.* |
| Bodies, place, motion | `sections/32-bodies-place-motion.tex` | drafted | ST I qq. 51–53 |
| Intellect and knowledge | `sections/34-intellect-and-knowledge.tex` | drafted | ST I qq. 54–58; *De ver.* 8 |
| Will and love | `sections/36-will-and-love.tex` | drafted | ST I qq. 59–60 |
| Creation, grace, glory | `sections/38-creation-grace-glory.tex` | drafted | ST I qq. 61–62 |
| Fall and punishment | `sections/40-fall-and-punishment.tex` | drafted | ST I qq. 63–64; *De malo* 16 |
| Illumination and speech | `sections/50-illumination-and-speech.tex` | drafting | ST I qq. 106–107; *De ver.* 9 |
| Hierarchies and orders | `sections/52-hierarchies-and-orders.tex` | drafting | ST I qq. 108–109 |
| Government and mission | `sections/54-government-and-mission.tex` | drafting | ST I qq. 110–112 |
| Guardian angels | `sections/56-guardian-angels.tex` | planned | ST I q. 113 |
| Assaults of demons | `sections/58-assaults-of-demons.tex` | drafting | ST I q. 114 |
| Christ, Mary, angels | `sections/60-christ-mary-and-the-angels.tex` | planned | ST III q. 8 a. 4; q. 30; I q. 108 a. 8 |
| Disputed questions | `sections/70-disputed-questions.tex` | drafted | Bonaventure *In II Sent.*; Scotus *Ord.* II dd. 2–6; Suárez *De angelis*; Tempier 1277 |
| Byzantine line | `sections/72-byzantine-line.tex` | planned | Damascene; Palamas *Capita 150*; Byzantine synaxis of 8 November |
| Liturgy | `sections/80-liturgy.tex` | planned | repository calendars; Missale Romanum 1962 and 2002; Roman Canon; Rituale |
| Devotion and regulation | `sections/82-devotion-and-its-regulation.tex` | planned | Laodicea c. 35; Rome 745; Leo XIII; Directory on Popular Piety 213–217 |
| Saints and the holy angels | `sections/84-the-saints-and-the-angels.tex` | planned | Francis and Bonaventure's *Legenda*; Gertrude; Frances of Rome; Ignatius; Teresa; Francis de Sales; Newman |
| Order of the universe | `sections/88-the-order-of-the-universe.tex` | drafting | ST I q. 47, q. 50 a. 1, q. 108 |
| App. nine orders | `appendices/01-the-nine-orders.tex` | drafted | order inventory |
| App. pre-Christian continuities | `appendices/02a-pre-christian-continuities.tex` | planned | continuity rows of l13a and l13b |
| App. comparative orderings | `appendices/02-comparative-orderings.tex` | planned | order inventory |
| App. article census | `appendices/03-article-census.tex` | planned | question inventory |
| App. parallels in Aquinas | `appendices/04-parallels-in-aquinas.tex` | planned | Corpus Thomisticum |
| App. Dionysius in the Summa | `appendices/05-dionysius-in-the-summa.tex` | drafted | ST citations of CH |
| App. magisterial chronology | `appendices/06-magisterial-chronology.tex` | drafted | acts above |
| App. calendar | `appendices/07-calendar.tex` | planned | repository calendars |
| App. Scripture index | `appendices/08-scripture-index.tex` | planned | body citations |
| App. names | `appendices/09-names.tex` | planned | Tobit, Daniel, Luke, Jude, Rev.; Rome 745; Directory 217 |
| App. demons' powers | `appendices/10-demons-powers-and-limits.tex` | drafting | ST I qq. 64, 109–114 |
| App. first sin | `appendices/11-the-first-sin.tex` | drafted | Aquinas, Scotus, Suárez, Fathers |
| App. terminology | `appendices/12-terminology.tex` | planned | terminology audit |
| App. witness register | `appendices/13-witness-register.tex` | planned | source audit; author-standing inventory |
| Scope appendix | `appendices/90-scope-corpus-qualifications.tex` | drafted | scope record |
| References | `appendices/99-references.tex` | planned | source audit |

## Pipeline steps after drafting

1. `make doc DOC=theology/angelology PROVIDER=claude`; clear warnings.
2. `make review-doc DOC=theology/angelology PROVIDER=claude`; inspect every page.
3. `make install-doc DOC=theology/angelology PROVIDER=claude`.
4. `make web-editions PROVIDER=claude`, review the generated Markdown against
   the PDF, then install it.
5. Catalog row in `library/faith.md`; `make add-publication
   ID=theology/angelology CATALOG=library/faith.md PROVIDER=claude
   STATUS=alpha`; `make document-catalogue`.
6. Register new source works; `research/source-bindings.toml`; source
   inventory refresh and Claude classification review; `make check-sources`.
7. `make check-metadata PROVIDER=claude`, `make check-web-editions
   PROVIDER=claude`, `make check-promised-deliverables`.
8. Reconcile `PROJECT-WORK.md` and the ledger; commit and push.
