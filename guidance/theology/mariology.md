# Mariological Reference Works

This profile governs repeatable theological reference works beneath `src/gpt/theology/mariology/`, including the Rosary exposition and studies of ecclesial judgments concerning alleged Marian apparitions. These works may be discursive, historical, devotional, doctrinal, or juridically status-conscious, but they do not inherit the Mass-propers template, the Ordinary-exposition sequence, the sacramental-reference architecture, or the general article path.

Publishable documents live at `src/gpt/theology/mariology/<document>/`; transient and installed PDFs mirror them at `build/gpt/theology/mariology/<document>.pdf` and `doc/gpt/theology/mariology/<document>.pdf`. Reusable Mariological source fragments, if genuinely shared, live at `src/gpt/theology/mariology/shared/`, have no independent PDF, and must be imported rather than copied. Rebuild and inspect every consumer after a shared change.

## Governing doctrinal hierarchy

Public Revelation is complete in Jesus Christ. A private revelation cannot improve, complete, correct, or replace the apostolic deposit, and the faithful are never required to give a private revelation divine and Catholic faith (DV 2--4; CCC 65--67). Scripture, Tradition, dogma, authoritative non-definitive teaching, liturgical reception, administrative judgment, theological opinion, devotional tradition, historical reconstruction, typology, and project synthesis must remain visibly distinct.

Christ alone is Redeemer and the one mediator between God and humanity. Mary's cooperation is created, graced, maternal, subordinate, participated, and wholly dependent upon Christ; it neither adds to his merits nor compensates for deficient divine mercy (LG 56, 60--62; CCC 970). Apply the current doctrinal safeguards in the Dicastery for the Doctrine of the Faith's *Mater Populi Fidelis* when Marian titles or mediation formulas matter. Do not depict Mary as an independent source of grace, a rival advocate against Christ, or a restraint upon an otherwise merciless Father.

Authentic Marian devotion leads to the Trinity through Christ and into Scripture, liturgy, sacraments, conversion, charity, mission, and communion with the Church. It does not define doctrine through alleged messages, authenticate political programs, supply an inevitable future chronology, promise mechanical salvation, or displace ordinary pastoral, medical, legal, or safeguarding action.

## Required records and source classes

Every document leaf keeps one structured `generation-metadata.tex` record, imports it once in a terminal `Generation Metadata` section, and keeps:

- `research/scope.md`, stating question, reader, thesis, included and excluded corpus, authority classes, currentness needs, material uncertainties, and review state; and
- `research/source-audit.md`, mapping consequential claims to exact sources and loci, source class, translation or OCR status, quotation limits, rejected leads, and unresolved disagreements.

An apparition-judgment study also keeps `research/corpus-status.md` as its controlling inventory. Narrative prose may explain but never silently broaden or upgrade that inventory. Update the inventory first when a competent authority changes a status.

Prefer Scripture, conciliar and papal teaching, DDF acts, competent diocesan or eparchial decrees, official shrine or episcopal records, and critical primary editions. Papal addresses, liturgical feasts, shrine status, canonizations, coronations, visits, indulgences, imprimaturs, and popular reception can prove ecclesial reception within their proper scope; none by itself proves that an alleged event is supernatural. Secondary scholarship may reconstruct history but must not be assigned magisterial or juridic force.

When a historical or status claim lacks its expected primary or competent-authority record, search the reasonably accessible official indices, diocesan or eparchial archives and publications, DDF and Holy See records, critical editions, contemporary press or documentary witnesses, and professional scholarship before treating the gap as final. Record the source families checked and consequential negative result in the source audit; do not turn an untested absence into a historical or juridic conclusion.

## Reader-facing order

After the title and table of contents, begin the work's usable or substantive object: the Rosary's prayer and contemplative form, the scriptural and doctrinal economy of the Marian dogmas, the history or judgment actually under study, or the first event dossier. Do not put a question-and-method chapter, corpus boundary, evidence key, status taxonomy, date-range survey, currentness block, terminology guide, or review disclaimer between the reader and that content.

After the substantive synthesis, place a terminal `Scope, Status, and Qualifications` appendix containing the question and thesis boundary, included and excluded corpus, geographic and chronological range, as-of or checked-through date, status taxonomy, source hierarchy and method, terminology, global doctrinal and juridic limits, unresolved questions, rights boundary, and review state. A corpus index, global status map, orientation timeline, or inclusion-threshold account used chiefly to bound the work belongs in this appendix block. References follow, then terminal `Generation Metadata`.

The title may identify the devotion, dogma set, event, place, or competent act. Where reliance risk is immediate, a compact notice may state the completeness of public Revelation, the nonbinding character of private revelation, or the exact current controlling judgment and point to the appendix. The precise object and limit of an apparition judgment, a disputed historical witness, a doctrinal authority distinction, or a qualification affecting one message or event remains beside that claim; the appendix never licenses a globally cautious but locally overbroad narrative.

## Rosary expositions

A comprehensive Rosary exposition begins with the prayer and contemplative form rather than an identity-and-method essay. It records the provenance and function of each prayer component; distinguishes the historic fifteen-decade Rosary, the expanded twenty-mystery cycle, and an ordinary five-decade recitation; and analyzes both the complete cycle and every included mystery at biblical, Christological, Trinitarian, Marian, ecclesial, patristic, spiritual, and moral levels. Put the work-wide cycle boundary, historical range, method, and currentness in the terminal appendix while retaining a date or source qualification beside the historical claim it changes.

The source and publication must preserve these boundaries:

- the Rosary is a contemplative pious exercise distinct from the sacred liturgy and from sacramental anamnesis;
- the Luminous Mysteries are Saint John Paul II's freely proposed enrichment, not a test of obedience or a claim that the traditional cycle was defective;
- the St. Dominic attribution is a venerable devotional and papal tradition, while delivery of the complete modern form in one historically documented event is not asserted without contemporary evidence;
- Pius V stabilized an inherited developing form rather than inventing every component;
- Fatima commended an existing devotion and did not originate the Rosary or supplement the Gospel;
- typology is distinguished from literal exegesis, and disciplined imaginative meditation from recovered historical detail; and
- mutable indulgence discipline and current devotional norms are checked against official sources and date-qualified.

Apparitions, promises, exact wound counts, undocumented speeches, end-time schedules, or other private-revelation details may not be smuggled into mystery analysis as public Revelation or historical fact. Spiritual fruits are invitations to grace-enabled conversion, not automatic psychological effects or guarantees.

## Marian-dogma references

A comprehensive reference on Marian dogma treats the four truths commonly identified in Catholic theology as Marian dogmas: divine motherhood, perpetual virginity, the Immaculate Conception, and the bodily Assumption. It states the precise object and authority of each teaching before supplying biblical, patristic, liturgical, scholastic, conciliar, or papal evidence. It must not create additional dogmas by promoting every authoritative Marian doctrine, devotional title, theological conclusion, or proposed definition to the same rank.

For each dogma, keep distinct:

- the revealed reality and its Christological or ecclesial center;
- the exact solemn definition or other controlling magisterial formulation, with authority, date, and locus;
- Scripture read in its literary and canonical context, distinguishing direct assertion from typology;
- early witnesses to the substance of the belief, later terminological precision, liturgical reception, controversy, and final definition;
- genuinely checked patristic and Thomistic loci, including material difficulty or historical limitation rather than retrospective unanimity; and
- the dogma's theological consequences and the questions its definition deliberately leaves open.

When a repeated dogma or mystery panel is already set apart typographically and its internal fields name the proposition or scriptural loci, controlling authority or doctrinal center, and necessary limit or contemplative fruit, do not add a second generic wrapper title. Retain visible titles only when they supply substantive status, authority, or interpretive information not carried by those fields.

Development is neither invention nor a license to project nineteenth- or twentieth-century formulas word for word into the Fathers. Apocryphal or legendary material may document reception, imagination, or feast development without becoming apostolic eyewitness evidence. A saint or Doctor's incomplete, disputed, or materially different formulation must be acknowledged. In particular, do not make Thomas Aquinas teach the 1854 definition in its final form, and do not invent a dedicated Thomistic proof of the 1950 definition where his surviving treatment supplies only broader theological principles.

A comprehensive four-dogma reference enters the scriptural and doctrinal economy or the first dogma immediately after the contents rather than beginning with method and boundary apparatus. It ends its substantive synthesis with one genuinely page-bounded appendix synopsis for each dogma. Each sheet keeps together the exact object, mode and authority of proposal, biblical center, principal patristic witnesses, Thomistic support or limitation, development hinge, doctrinal fruit, required assent, and exclusions or open questions. The synopsis condenses the audited argument; it may not erase a historical difficulty, promote typology into direct assertion, or turn a theological opinion into defined content.

A section on Mary's cooperation in salvation must apply *Lumen gentium* 56 and 60--62 together with the current DDF doctrinal note *Mater Populi Fidelis*. “Co-redemptrix” is not a fifth Marian dogma and must not be recommended as a definition of Mary's cooperation; “Mediatrix” and “Advocate” require the conciliar and DDF safeguards of Christ's unique mediation and Mary's wholly received, maternal, subordinate intercession. Historical papal or devotional uses are reported with their date and authority, not treated as if repetition by itself created a solemn definition.

## Apparition judgments and authority-qualified corpora

Avoid an unqualified title or assertion of “all approved apparitions.” The Church publishes no identified universal master registry, and “approved” can collapse unlike acts: a positive judgment on an event, witness credibility, permission of cult, approval of a devotion or text, papal or liturgical reception, and a current pastoral `Nihil obstat`. A comprehensive study must define its taxonomy, search boundary, as-of date, inclusion and exclusion rules, and meaning of every status term.

The DDF's *Norms for Proceeding in the Discernment of Alleged Supernatural Phenomena* took effect on 19 May 2024. Under the current ordinary process the diocesan bishop investigates and proposes a determination in dialogue with the DDF, and the DDF gives final approval. The six possible prudential conclusions are:

1. `Nihil obstat`;
2. `Prae oculis habeatur`;
3. `Curatur`;
4. `Sub mandato`;
5. `Prohibetur et obstruatur`; and
6. `Declaratio de non supernaturalitate`.

A `Nihil obstat` permits positive pastoral reception and may recognize signs of the Spirit's action amid an experience; it does not certify the event's supernatural origin or oblige belief. As a rule, current authorities do not declare supernatural origin, although the Pope may exceptionally authorize such a procedure. Legacy decisions retain their exact historical formulas and scopes---including `constat de supernaturalitate`, `constat de non supernaturalitate`, “worthy of belief,” permission of cult, or a commission's credibility finding---unless a competent later act supersedes or reclassifies them. Do not retroactively force them into a 2024 category.

### Controlling dossier fields

For each included event or received tradition, record as applicable:

- stable title or invocation; place, country, diocese or eparchy, Church `sui iuris`, and jurisdiction;
- claimed event type and dates; named recipients, seers, or witness corpus;
- competent authority and office; act title, protocol when public, date, effective or publication date, official language, exact locus, and stable source;
- procedural regime and exact operative formula or tightly checked paraphrase;
- precise object judged: event, testimony, message corpus, cult, devotion, shrine, miracle, pastoral fruit, or another object;
- included and excluded dates, persons, messages, secrets, translations, later accretions, and geographic reach;
- later acts, reversals, restrictions, clarifications, supersession, and Holy See involvement;
- current controlling status and an express statement of what that status does **not** establish;
- verified reported-message themes, doctrinal cautions, symbolic qualifications, historical context, and ecclesial reception; and
- source class, translation or OCR status, copyright boundary, disagreements, unresolved leads, and review maturity.

Use “reported message” except when describing exactly what a competent act recognizes. A positive decision never automatically authenticates every sentence, translation, secret, miracle, later recipient, later appearance, interpretation, devotional promise, or internet compilation. Silent events must not be forced into a verbal-message template.

The recurring reader-facing dossier summary uses an untitled frame and three stable visible field identifiers: `Event or tradition`, `Ecclesial reception or judgment`, and `Limit of that reception`. Do not make the reader infer these materially different fields from their order, spacing, or type style, and do not add a generic title for the frame as a whole.

An appendix of renowned or frequently confused claims must define a reproducible inclusion threshold in the terminal apparatus and keep a repository-owned inclusion record. “Renowned,” “major,” and “moderately renowned” are editorial categories, not canonical statuses; do not promise a universal list from internet popularity or an unidentified aggregation. If typography marks “approved” cases, the legend must state exactly which competent acts trigger that mark. A strict event-level mark does not transfer from approval of a title, prayer, feast, sacramental, cult, shrine, pilgrimage, cure, witness credibility, or post-2024 `Nihil obstat`. Every indexed row still names the authority, date, object, formula, current qualification, and what the act does not establish.

Ancient and medieval apparition traditions require the same category discipline. Preserve an official source's attribution to “tradition,” dream, foundation memory, or late narrative; distinguish devotional or liturgical reception from contemporary evidence and from a modern event decree. Historical uncertainty does not nullify an approved devotion, and approved devotion does not retroactively supply missing event evidence.

## Currentness and status control

Apparition publications display “checked through YYYY-MM-DD” in the terminal scope and status appendix and, before every installation, recheck the DDF document index, current procedural norms, the competent diocese or eparchy, later Holy See interventions, reversals, and restrictions. Never infer unchanged status from silence. Preserve older acts under their original law and vocabulary while identifying any later controlling act separately. A current controlling act and its limit remain visible in the dossier it governs.

Rosary publications require an as-of date only where mutable discipline or current official judgments matter. Stable doctrine and historical claims still require exact verification, but should not be given artificial legal currentness language.

Negative, precautionary, unresolved, ambiguous, pastorally received without a fact judgment, and positively judged cases must remain distinct. Cross-case similarities in conversion, prayer, penance, peace, sacraments, or charity may be synthesized as editorial analysis; they neither prove supernatural origin nor create a new composite revelation.

## Completion gate

A Mariological reference work is ready to publish only when:

- Christ's unique mediation, the completeness of public Revelation, and the subordinate character of every Marian privilege and devotion remain explicit;
- dogma, doctrine, judgment, reception, history, typology, devotional tradition, and original synthesis are not blurred;
- substantive prayer, doctrine, history, or event treatment begins immediately after the title and contents, while corpus and search boundaries, global status taxonomy, date range, currentness, method, terminology, rights, and review qualifications occur only in the terminal appendix block;
- the Rosary's historical development, complete cycle, every included mystery, and private-revelation boundaries are documented where that is the work's scope;
- a Marian-dogma reference identifies the exact four-dogma corpus, documents every definition and historical development without anachronism, states the authority and limits of other Marian titles, and provides a one-page evidence-and-boundary synopsis for each dogma;
- an apparition corpus and its narrative agree exactly, every status claim has a competent-authority source and bounded object, and no claim of comprehensiveness implies a nonexistent official master list;
- negative, ambiguous, unresolved, legacy, received-tradition, and post-2024 categories are not flattened;
- message quotations and paraphrases are checked against the authority-bounded corpus and comply with copyright limits;
- mutable discipline and current judgments are rechecked and date-qualified;
- independent mariological, historical, canonical, linguistic, medical, or ecclesiastical review is claimed only when actually recorded; and
- expected primary or competent-authority source gaps have received and recorded targeted searches;
- universal metadata validation, terminal provenance, multi-pass build, log inspection, every-page visual review, PDF structure checks, installed/build comparison, source records, and catalog update are complete.
