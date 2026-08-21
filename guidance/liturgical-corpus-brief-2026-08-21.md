# Liturgical corpus brief, 21 August 2026

## Status and authority

This is the maintainer's own brief, written by him and confirmed in session as
the project's governing instruction. It is kept because it is the WARRANT for
`guidance/liturgical-text-publication-policy.md`: that page states the policy,
and this one is where the policy came from and who asked for it.

**Read the policy, not this, for what the rules are.** Two halves of this brief
have different fates and a reader who confuses them will act on a spent
instruction:

- **Standing policy** — its sections 1 to 6, 10, 11, 14, 19 and 20 — is
  implemented in `guidance/liturgical-text-publication-policy.md`, which is the
  authority. Where the two differ, the policy governs, because the policy was
  written against sources verified at execution time and this brief was written
  before that verification. Section 26 of this brief asks for exactly that
  re-verification and expects it to correct the brief.
- **A work order** — its sections 12, 13, 23 and 28 to 32, the repository sweep,
  the completeness audit, the phase sequence, the stop conditions and the report
  format — was addressed to the agents executing it in August 2026. It is spent.
  Do not read "Execute in this order" or "At completion, report" as an
  instruction to you.

Its sections 7 to 9, the corpus targets for the 1955, 1962 and postconciliar
states, are absorbed into the files that own that data:
`guidance/propers-for-agents.md` and `guidance/recensions.md`.

What this brief settled, and what nothing since has disturbed: publish unless a
rightsholder has affirmatively reserved the particular use, or no defensible
basis exists; analyse the actual work, rightsholder, use and licence rather than
treating every copyright notice as ownership of all underlying words; and never
fill a corpus hole with generated text.

Three of its factual premises were corrected in execution, and the corrections
are recorded in the policy's own superseded register rather than edited into the
text below. The brief is preserved as written.

---

# Claude Execution Brief: Reestablish Liturgical Text Publication Policy and Complete the Mystagogy Missal Corpus

## Mission

Perform a repository-wide policy reset and corpus completion sweep for Mystagogy's Roman Mass data.

The objective is to make the 1955, 1962, and postconciliar missal corpora as complete, textually faithful, provenance-rich, and publicly usable as reasonably possible, while adopting a **permission-maximizing publication policy** rather than a reflexively restrictive copyright policy.

This is an implementation task, not merely a legal or editorial review.

You are to:

1. reestablish the project's liturgical-text publication policy from first principles and authoritative current sources;
2. audit every relevant corpus, parser, metadata record, provenance field, availability state, and UI assumption in the repository;
3. identify incomplete, missing, suppressed, or unnecessarily withheld liturgical texts;
4. enrich and complete the 1955, 1962, and postconciliar Roman Mass corpora;
5. distinguish underlying public-domain liturgical works from later copyrighted editions;
6. use express permissions aggressively where they exist;
7. prefer publication where the legal basis is genuinely ambiguous but defensible;
8. preserve typed provenance and rights metadata so every published text can be audited;
9. isolate only material that is actually blocked by an affirmative restriction or lacks a defensible publication basis;
10. leave the repository with tests, records, and documentation sufficient for another agent to verify every material decision.

Do not stop at producing recommendations. Make the changes that can safely and defensibly be made.

---

# 1. Governing Policy

The operating presumption is:

> **Publish unless a copyright holder has affirmatively reserved the particular use at issue, or the text lacks a defensible permission or public-domain basis.**

Do **not** use this older, excessively conservative presumption:

> Do not publish unless someone has affirmatively granted permission.

The project exists to present the public prayer of the Church faithfully. Copyright and publication restrictions must be obeyed where applicable, but they must not be allowed to erase texts merely because a modern printed edition bears a copyright notice when the underlying liturgical work is ancient, public domain, independently available, expressly licensed for noncommercial web reproduction, or otherwise defensibly publishable.

Use this priority order:

1. **Public-domain underlying text** -> publish.
2. **Express general web permission** -> publish under its stated conditions.
3. **Ancient/public-domain underlying work reproduced in a modern copyrighted edition** -> source independently from a public-domain witness and publish the underlying work.
4. **Authorized syndication mechanism** -> display through that mechanism.
5. **Specific written permission already held by the project** -> publish within its scope.
6. **Ambiguous but defensible publication basis** -> prefer publication, document the argument, and mark the basis explicitly.
7. **Affirmative restriction or no defensible basis** -> do not locally republish; retain metadata and, where useful, expose a typed unavailable/externally-sourced state.

The burden is on a restriction to be specific enough to defeat an otherwise defensible publication basis.

This policy is not an instruction to ignore copyright. It is an instruction to analyze the actual copyrightable work, actual rightsholder, actual use, and actual license instead of treating every copyright statement as ownership of all underlying words.

---

# 2. Legal / Publication Posture to Encode

This brief is not legal advice. Treat it as the project's editorial and engineering policy, subject to correction if stronger authority is discovered.

When authority conflicts, prefer:

1. statute / controlling law;
2. official Holy See or bishops' conference decree;
3. current rightsholder publication or permissions policy;
4. official publisher or commission guidance;
5. scholarly / historical evidence;
6. secondary commentary.

Do not let a generic permissions page silently override a more specific express permission from the actual rightsholder without establishing that the latter has been rescinded or superseded.

Record dates and retrieval URLs for all controlling policy sources.

---

# 3. ICEL English Roman Missal Texts: Default to Publish

ICEL currently provides an express Internet reproduction permission for approved/promulgated ICEL texts and translations on a **non-commercial website**, without obtaining individual written or oral permission, subject to stated conditions.

Authoritative source:

https://www.icelweb.org/PubPolicy.PDF

Current ICEL copyright-policy summary:

https://www.icelweb.org/copyright.htm

Relevant conditions include, at minimum:

- no fee may be charged to access the website or the ICEL translations/texts;
- the appropriate ICEL copyright acknowledgment must appear as required;
- ICEL translations and texts must be followed exactly;
- no implication of affiliation, sponsorship, or endorsement by ICEL;
- the permission does not extend automatically to every other form of publication;
- ICEL reserves the right to modify or terminate the permission.

Therefore:

## 3.1 Presumption

For an ICEL text that has:

- been approved by the relevant conference(s),
- received the required Holy See confirmation/recognition as applicable,
- been promulgated for use,

and is displayed on Mystagogy as a free noncommercial website:

> **Treat the text as publishable unless a more specific current ICEL policy excludes it.**

This includes, where actually owned by ICEL and covered by the permission:

- Order of Mass;
- collects;
- prayers over the offerings;
- prayers after Communion;
- prefaces;
- Eucharistic Prayers;
- antiphons;
- commons;
- ritual Mass texts;
- Masses and prayers for various needs and occasions;
- votive Masses;
- Masses for the dead;
- approved rubrical translations where ICEL owns the English text;
- other promulgated Roman Missal material.

Do not ask ICEL for individual permission when its standing policy already grants the relevant permission.

## 3.2 Exactness

ICEL's permission requires exact reproduction.

Accordingly:

- preserve canonical wording exactly;
- do not normalize punctuation or capitalization merely for style;
- do not silently modernize spellings;
- do not interpolate explanatory text into the liturgical text;
- keep annotations, provenance, commentary, structural labels, and UI chrome structurally separate from the reproduced text;
- test corpus output against authoritative exemplars.

If the repository currently contains paraphrased, normalized, inferred, reconstructed, or generated ICEL text, replace it with exact authorized text or mark it unavailable until exact text is established.

## 3.3 Attribution

Create a centralized attribution mechanism rather than duplicating fragile free-text notices.

At minimum, support the appropriate notice equivalent to:

> The English translation of The Roman Missal © 2010, International Commission on English in the Liturgy Corporation. All rights reserved.

For excerpts/multiple works, follow ICEL's current prescribed wording rather than inventing our own.

Attribution must be generated from typed metadata where possible.

---

# 4. USCCB-Specific English Material: Separate It from ICEL

Do not treat "English Roman Missal text" as a single copyright bucket.

Some text belongs to ICEL; some national adaptations, proper texts, calendars, explanatory material, or other material may be controlled by the USCCB or another entity.

Current USCCB publication guidance:

https://www.usccb.org/committees/divine-worship/policies/guidelines-for-the-publication-of-liturgical-books

2025 guidelines resource page:

https://www.usccb.org/resources/guidelines-publication-liturgical-books

The 2025 guidelines enter into force on **November 29, 2026**.

Participation-aid / digital-platform section:

https://www.usccb.org/committees/divine-worship/policies/guidelines-for-the-publication-of-liturgical-books/participation-aids

The new guidelines state that digital production platforms/subscriptions must have licenses for copyrighted texts and undergo review when they are participation aids.

## 4.1 Do not overgeneralize

This does **not automatically mean** that ICEL's own express noncommercial Internet permission disappears.

For every English text, determine:

- actual copyright owner;
- actual governing license;
- whether it is ICEL universal text;
- whether it is a USCCB national adaptation/proper;
- whether it is CCD Scripture;
- whether another party owns it.

Do not classify text merely by the book in which it appears.

## 4.2 Product characterization

Mystagogy should not falsely describe itself as:

- an official ritual edition;
- an approved altar Missal;
- an authenticated liturgical book;
- an ICEL-sponsored or USCCB-sponsored service.

Where accurate, characterize it as a free liturgical reader for prayer, study, reference, and participation, with precise source attribution.

Do not use that characterization as a pretext to evade a clearly applicable rule. It is simply important not to volunteer a more heavily regulated product category that does not accurately describe the site.

## 4.3 Effective-date sweep

Because the new USCCB guidelines take effect November 29, 2026:

- encode this date in the policy documentation;
- identify any present behavior that will become noncompliant under a plausible reading of the new policy;
- distinguish present requirements from future requirements;
- do not prematurely suppress otherwise permitted material merely because future review/licensing rules may apply;
- create an explicit issue/record for any matter requiring action before November 29, 2026.

---

# 5. Scripture and the U.S. Lectionary

CCD/NAB/Lectionary rights are not the same as ICEL rights.

Current permissions page:

https://www.usccb.org/offices/new-american-bible/permissions

USCCB RSS policy:

https://www.usccb.org/subscribe/rss

The USCCB states that no permission or fee is needed to display the daily readings through its RSS feed on a website that does not condition access on the user providing anything of value.

It also states that digital applications, including free-distribution applications, generally require a license and fee, and the Lectionary pages carry restrictive reproduction notices.

## 5.1 Architecture

Separate:

- **lectionary assignment**: which passage is appointed for a given Mass;
- **scriptural text**: the actual words of a Bible translation;
- **liturgical rendering**: incipits, refrains, acclamations, lectionary-specific adaptations;
- **source mechanism**: local corpus vs authorized syndication.

This separation should be explicit in both schema and code.

## 5.2 USCCB daily-readings RSS

Where the site can lawfully and technically display the official U.S. daily readings via the authorized RSS mechanism:

- preserve that path;
- implement it cleanly if missing;
- cache only to the extent consistent with the authorization and ordinary technical necessity;
- do not convert RSS permission into an asserted right to build a permanent local NAB/Lectionary corpus;
- preserve attribution and source metadata.

If the RSS route cannot support historical/arbitrary-date browsing or all required Mass variants, represent that limitation honestly.

## 5.3 Public-domain Scripture

Prefer local public-domain Scripture for a fully enrichable corpus where appropriate.

For traditional Roman Mass use, the Douay-Rheims is an obvious candidate, but confirm the rights/provenance of the exact digital transcription used.

Public-domain Scripture may be:

- stored locally;
- indexed;
- searched;
- verse-aligned;
- annotated;
- cross-referenced;
- used for Catena links;
- compared across missals.

Never assume a particular modern digital edition is public domain merely because the underlying translation is. Establish provenance for the transcription/data source as well.

---

# 6. Latin: Distinguish the Ancient Work from the Modern Edition

This is central to the corpus-completion strategy.

A modern copyrighted edition of the Missale Romanum does not automatically create a new copyright in an ancient Latin collect, antiphon, canon, ordinary, or other underlying work that was already public domain.

The Holy See claims copyright in its typical editions and controls publication of liturgical books. Respect that claim.

But do not conflate:

- a copyrighted modern *edition*;
- its editorial apparatus, arrangement, typography, newly authored material, and edition-specific changes;

with:

- underlying ancient or otherwise public-domain liturgical texts.

## 6.1 Preferred sourcing strategy

For a Latin item present in 1955, 1962, or the postconciliar Missal:

1. identify whether the underlying text predates modern copyright;
2. find the earliest reliable public-domain witness available to the project;
3. transcribe/verify from that public-domain witness;
4. compare against the target missal edition;
5. record whether the target reading is identical, orthographically normalized, rubrically changed, or substantively changed;
6. publish the public-domain underlying text when it establishes the target wording;
7. avoid copying protected editorial apparatus from a modern commercial or Vatican edition;
8. separately assess genuinely modern additions or revisions.

The goal is to establish text independently, not to pretend a modern source was not used when it was.

## 6.2 Provenance example

Prefer structured provenance like:

```yaml
text_identity: collect.example
language: la
target_missal: roman-1962

textual_basis:
  kind: public_domain_witness
  witness:
    title: Missale Romanum
    year: 1920
    locator: ...
  transcription_source: ...
  verification:
    - witness: roman-1962
      relationship: textually_identical

rights:
  basis: public_domain_underlying_work
  modern_edition_copied: false
  confidence: high
```

over:

```yaml
source: "1962 Missal"
copyright: "unknown"
```

## 6.3 Modern Latin additions

Create an explicit inventory of texts that are genuinely modern enough that public-domain antecedent sourcing does not establish the target wording.

Examples may include:

- newly composed postconciliar collects;
- newly composed prefaces;
- new Eucharistic Prayers;
- new proper texts for recently canonized saints;
- post-1955/post-1962 revisions that are not merely restorations of old text;
- new rubrics or explanatory material.

These require a separate rights basis.

Do not let this minority force the entire Latin corpus into an unavailable state.

---

# 7. 1955 Corpus Target

Treat "1955" precisely.

The repository may use "1955" colloquially for a Holy Week / rubrical state around the reforms of Pius XII. Determine the exact intended liturgical snapshot.

Establish and document:

- calendar/rubrical baseline;
- Holy Week reform state;
- vigil structure;
- octaves;
- commemorations;
- ranks;
- propers;
- ordinary;
- prefaces;
- readings;
- chant/antiphon references where represented;
- local or project-specific conventions.

Do not silently blend pre-1955 and post-1955 states.

## 7.1 Required sweep

For 1955, inventory at least:

- Temporal cycle;
- Sanctoral cycle;
- Commons;
- Votive Masses;
- Masses for the Dead;
- Ritual Masses where in project scope;
- Orations;
- Secreta;
- Postcommunions;
- Introits;
- Graduals;
- Alleluias;
- Tracts;
- Sequences;
- Offertories;
- Communions;
- Epistles;
- Gospels;
- additional lessons where applicable;
- prefaces;
- Ordinary;
- Canon;
- proper Last Gospels where the model supports them;
- commemorations and alternative/additional prayers;
- Holy Week;
- Easter Vigil;
- ember days;
- rogation/litanic days where within Mass scope;
- vigils and octaves;
- feast rank and precedence metadata.

For every missing item, determine whether it is:

- truly absent in the rite;
- omitted from the current corpus;
- derivable by reference to a common;
- suppressed by prior copyright policy;
- unavailable because the source pipeline is incomplete;
- malformed/unparsed;
- present but unreachable because calendar/rubric dispatch is wrong.

Do not manufacture "Unavailable" when the rite specifies a cross-reference to another Mass/common. Model the reference.

---

# 8. 1962 Corpus Target

The 1962 corpus should become independently complete, not merely a patch layer on 1955 unless the data model explicitly and safely represents inheritance.

Audit:

- Temporal;
- Sanctoral;
- Commons;
- Votive Masses;
- Dead;
- Ritual Masses in scope;
- Holy Week;
- Easter Vigil;
- Ember Days;
- Rogations;
- vigils;
- commemorations;
- ranks/classes;
- orations;
- propers;
- lessons;
- Ordinary;
- Canon;
- prefaces;
- calendar reforms;
- removal/addition/alteration relative to 1955.

## 8.1 Differential validation

Generate a machine-readable 1955 -> 1962 delta.

Classify every difference as one of:

```text
added
removed
moved
renamed
rank_changed
calendar_changed
rubric_changed
text_changed
reading_changed
common_changed
reference_changed
identical
unknown
```

Unknown should approach zero.

Do not infer historical differences from memory. Establish them from sources.

---

# 9. Postconciliar Corpus Target

Use a precise target instead of "Novus Ordo" as an undifferentiated blob.

At minimum distinguish:

- Latin typical edition lineage;
- current U.S. English Roman Missal;
- current U.S. calendar adaptations;
- U.S. Lectionary assignment layer;
- Scripture text source;
- ICEL universal English;
- USCCB-specific English;
- optional/alternative forms.

Where the project supports more than one postconciliar historical state, model those explicitly rather than overwriting older promulgated forms.

## 9.1 Required structural coverage

Inventory:

- Proper of Time;
- Proper of Saints;
- Commons;
- Ritual Masses;
- Masses and Prayers for Various Needs and Occasions;
- Votive Masses;
- Masses for the Dead;
- Order of Mass;
- Eucharistic Prayers;
- prefaces;
- antiphons;
- collects;
- prayers over offerings;
- prayers after Communion;
- solemn blessings;
- prayers over the people;
- optional memorial logic;
- memorial/feast/solemnity precedence;
- vigil Masses;
- evening Mass variants;
- proper readings vs common readings;
- lectionary-number metadata where lawful to store;
- U.S. proper celebrations;
- recently-added universal celebrations;
- newly promulgated texts/supplements already in force.

Do not import unpromulgated Gray Book / draft text as though it were approved liturgical text.

---

# 10. Corpus Rights Schema

Implement or normalize typed rights metadata.

A suggested vocabulary:

```text
copyright_authority:
    public_domain
    icel
    holy_see
    usccb
    ccd
    episcopal_conference_other
    third_party
    unknown
```

and:

```text
publication_basis:
    public_domain
    public_domain_underlying_work
    express_web_license
    authorized_syndication
    written_permission
    statutory_exception
    defensible_ambiguous
    restricted
    pending_analysis
```

Add, where useful:

```text
permission_scope
permission_conditions
source_url
policy_url
policy_retrieved_at
copyright_notice
attribution_required
exact_text_required
commercial_use_allowed
local_storage_allowed
redistribution_allowed
syndication_only
liturgical_use_restriction
effective_from
effective_until
analysis_notes
confidence
```

Avoid free-text-only rights records.

A renderer or publication pipeline should be able to answer:

> Why is this text allowed to appear here?

without requiring a human to reconstruct the answer from git history.

---

# 11. Provenance Schema

Every substantive text should have recoverable provenance.

At minimum:

```text
work identity
language
rite / missal edition
liturgical location
source witness
source date
source locator
transcription source
verification witness(es)
editorial transformations
rights basis
authority
confidence
```

If text is inherited from a Common or another Mass, encode inheritance/reference explicitly.

If the same ancient text occurs in multiple missals, prefer stable text identity plus edition-specific placement/usage metadata rather than duplicating opaque strings where the repository architecture permits it.

Never collapse:

- text identity;
- liturgical assignment;
- rights status;
- translation identity;
- witness identity.

---

# 12. Repository-Wide Sweep

Before editing, inspect the entire repository for:

- missal source files;
- generated corpora;
- importers;
- scrapers;
- parsers;
- normalizers;
- schema validators;
- calendar engines;
- liturgical selectors;
- UI rendering;
- "unavailable" states;
- copyright guards;
- hard-coded suppression lists;
- tests;
- build scripts;
- documentation;
- prior legal-policy notes;
- TODOs;
- dead code;
- generated artifacts that have drifted from source;
- provenance metadata;
- source URLs;
- corpus statistics.

Search for terms such as:

```text
copyright
permission
rights
licensed
license
ICEL
USCCB
CCD
NAB
NABRE
Lectionary
Missale
1962
1955
Novus
postconciliar
unavailable
held
withheld
restricted
provenance
source
public domain
public_domain
attribution
```

Also identify code paths where "unknown rights" currently becomes "hide the text."

That behavior should be replaced with the policy in this brief.

---

# 13. Completeness Audit

Produce machine-verifiable corpus completeness reports for all three missal families.

A useful record should include:

```text
expected celebrations
represented celebrations
missing celebrations
expected text slots
filled text slots
inherited/reference slots
lawfully external/syndicated slots
truly unavailable slots
malformed slots
unknown slots
duplicate identities
orphan texts
unreachable texts
source-less texts
rights-pending texts
```

Separate structural completeness from textual completeness.

A celebration that exists in metadata but has half its propers missing is not complete.

A prayer that exists in storage but cannot be reached through calendar/dispatch logic is not complete.

A text whose source is unknown is not provenance-complete even if rendered.

---

# 14. Source Strategy

Prefer high-authority and legally useful sources.

## 14.1 Traditional Latin

Prioritize public-domain printed witnesses, scans, or trustworthy transcriptions whose publication date and edition can be established.

Where a modern web transcription is used as an aid:

- do not assume its own transcription is unencumbered;
- verify the text against a public-domain witness;
- preserve the public-domain witness as the publication basis.

## 14.2 Postconciliar Latin

Distinguish:

- ancient inherited text;
- restored ancient text;
- newly composed modern text;
- modern editorial/rubrical material.

Source public-domain antecedents wherever they establish the exact target wording.

## 14.3 English

For current approved ICEL text, use an authoritative exact source.

Do not silently source current English from:

- blogs;
- scraped parish PDFs;
- unofficial missal sites;
- OCR without verification;
- AI-generated reconstructions.

For USCCB-specific English, establish separate permission.

## 14.4 Scripture

For public-domain translations, verify both underlying translation rights and the digital transcription provenance.

For the official U.S. readings, prefer the authorized USCCB mechanism where its scope fits.

---

# 15. No Hallucinated Liturgical Text

Under no circumstances fill corpus holes by asking an LLM to "translate" or reconstruct official liturgical text.

An LLM may assist with:

- locating candidate witnesses;
- comparing strings;
- identifying likely duplicate texts;
- generating audit tooling;
- explaining differences.

It may not be treated as a textual authority.

Every published liturgical text must resolve to a source/witness chain.

---

# 16. Normalization Rules

Be extremely cautious with normalization.

Safe structural normalization may include:

- Unicode normalization;
- normalized internal identifiers;
- whitespace normalization outside semantically significant content;
- line-structure metadata;
- parser-level markup cleanup.

Do not silently normalize liturgical content in ways that defeat exactness:

- punctuation;
- capitalization;
- spelling;
- diacritics;
- sacred names;
- versicle/response markers;
- paragraph boundaries where liturgically meaningful;
- rubric wording;
- optional text brackets;
- chant punctuation.

If multiple witnesses differ only orthographically, preserve a canonical target transcription and record the normalization decision.

---

# 17. Edition Differences Must Remain Differences

The purpose is not to harmonize 1955, 1962, and postconciliar texts into one synthetic Roman Missal.

Preserve real differences.

Examples:

- changed collects;
- altered feast names;
- rank/class changes;
- removed octaves;
- changed Holy Week texts;
- changed lectionary assignments;
- different offertories/communions;
- different calendars;
- different ordinary/rubrical forms;
- different prefaces;
- additional postconciliar alternatives.

Shared text identity is useful; false equivalence is not.

---

# 18. Cross-Edition Data Model

Where practical, model:

```text
Text
Witness
Translation
LiturgicalAssignment
CalendarRule
RightsRecord
SourceRecord
```

as conceptually distinct entities, even if the existing repository cannot fully normalize them yet.

A text can be:

- public domain as a Latin work;
- represented by multiple witnesses;
- assigned differently in 1955 and 1962;
- translated by ICEL in a copyrighted but web-permitted English form;
- paired with a public-domain Douay-Rheims reading in one UI mode;
- paired with an externally syndicated official U.S. reading in another.

Do not let one "copyright" flag on a celebration obscure these distinctions.

---

# 19. UI / User-Facing Availability

The reader should prefer presenting a useful lawful text over an opaque "Unavailable."

Availability states should distinguish:

```text
available_local
available_public_domain
available_under_license
available_via_syndication
available_with_attribution
unavailable_rights_restricted
unavailable_source_missing
unavailable_not_in_rite
unavailable_not_yet_transcribed
unavailable_not_yet_verified
unavailable_technical_error
```

Never turn malformed data into a theological/liturgical claim of absence.

Never describe a text as absent from the rite merely because the corpus has not acquired it.

---

# 20. Attribution UX

Attribution should be:

- correct;
- visible enough to satisfy the license;
- not intrusive enough to destroy the reader;
- generated from the underlying rights/source records.

Consider a compact per-page/per-section legal/provenance footer plus detailed provenance expansion.

Do not bury required ICEL attribution if the policy requires it at particular display boundaries.

Do not imply ICEL/USCCB/Vatican endorsement.

---

# 21. Tests

Add or expand tests for:

## Rights

- ICEL-covered text renders on a free-web target.
- Required ICEL attribution renders.
- Text is byte/textually exact against canonical fixture after permitted structural transformations.
- A restricted text cannot accidentally enter a locally redistributable bundle.
- RSS/syndication-only material remains segregated from local permanent corpus generation.
- Unknown rights does not automatically mean "absent from rite."

## Provenance

- every published text has a source;
- every published text has a rights basis;
- public-domain-underlying-work claims identify a witness;
- edition-specific differences identify verification witnesses;
- no malformed provenance objects render as `[object Object]` or equivalent.

## Completeness

- every expected celebration has a modeled disposition;
- every expected text slot is filled, inherited, external, truly absent, or explicitly pending;
- zero unexplained/unknown holes at release gate;
- no duplicate verse/text identity caused by parser errors;
- no unreachable corpus members.

## Historical correctness

- 1955 vs 1962 delta fixtures;
- 1962 vs postconciliar structural distinctions;
- Holy Week fixtures;
- major calendar/rank fixtures;
- Ember/Rogation/Vigil fixtures;
- sample feasts with changed propers;
- sample shared texts proving stable identity across editions.

---

# 22. Generated Corpus / Build Discipline

Determine which files are authoritative sources and which are generated outputs.

Do not hand-edit generated corpora unless the repository explicitly treats them as authority.

When importers or generators are defective:

- fix the generator;
- regenerate;
- verify deterministic output;
- record corpus deltas.

Any large corpus enrichment must have a reproducible source path.

Do not land opaque mass data dumps without provenance.

---

# 23. Metrics Before and After

Before modification, capture a baseline.

After modification, report at least:

```text
1955:
  celebrations
  filled slots
  missing slots
  rights-blocked
  source-missing
  malformed
  provenance-complete %

1962:
  ...

postconciliar:
  ...

cross-edition:
  stable shared-text identities
  verified deltas
  unresolved deltas
```

Also report:

```text
ICEL texts exposed under express web permission
public-domain Latin texts newly restored
texts moved from "unknown/restricted" to defensibly publishable
USCCB/CCD texts kept external/syndicated
remaining genuine permission requests
```

The desired outcome is that the final list of actual permission requests is small and specific.

---

# 24. Permission Requests: Narrow Them

Do not send a broad request such as:

> May we reproduce the Roman Missal?

That needlessly invites a broad denial.

If permission is truly needed, isolate the exact material:

```text
rightsholder
work
specific text set
language
edition
planned use
noncommercial/free status
web-only status
whether downloadable
whether for liturgical celebration vs study/reference
requested scope
```

Before recommending a permission request, establish why each of these alternatives fails:

- public-domain underlying work;
- existing express license;
- existing project permission;
- authorized syndication;
- independently sourced earlier witness;
- another clearly lawful text option.

---

# 25. Do Not Delete Historical Corpus Merely Because It Is Not Currently Authorized for Liturgical Celebration

A historical liturgical reader may display historical rites/texts as historical/liturgical-study material even when they are no longer the ordinary currently authorized form.

Do not confuse:

- ecclesiastical authorization to celebrate a rite;
- copyright permission to reproduce a text;
- historical accuracy;
- website publication.

Track these separately.

---

# 26. Current Authoritative Policy Sources to Verify

At execution time, re-open and verify all of these in case policy changed.

ICEL publication policies:

https://www.icelweb.org/PubPolicy.PDF

ICEL copyright summary:

https://www.icelweb.org/copyright.htm

ICEL copyrighted-material inventory:

https://www.icelweb.org/copyrightICEL.htm

USCCB current liturgical publication guidance:

https://www.usccb.org/committees/divine-worship/policies/guidelines-for-the-publication-of-liturgical-books

USCCB 2025 guideline resource / effective date:

https://www.usccb.org/resources/guidelines-publication-liturgical-books

USCCB participation-aid / digital-platform section:

https://www.usccb.org/committees/divine-worship/policies/guidelines-for-the-publication-of-liturgical-books/participation-aids

USCCB copyright-permissions requirements:

https://www.usccb.org/committees/divine-worship/policies/copyright-permissions-requirements

CCD/NAB permissions:

https://www.usccb.org/offices/new-american-bible/permissions

USCCB authorized RSS feeds:

https://www.usccb.org/subscribe/rss

Also locate and preserve the current Holy See decree/policy governing copyright/publication of Latin typical liturgical books and cite the authoritative Vatican source in the repository policy document.

If any of these sources have changed, use the current source and document the change rather than blindly following this brief.

---

# 27. Required Repository Documentation

Create or replace a durable policy document, suggested path:

```text
guidance/liturgical-text-publication-policy.md
```

It must contain:

- governing permission-maximizing presumption;
- rights hierarchy;
- ICEL web permission;
- USCCB/CCD distinctions;
- Latin underlying-work distinction;
- public-domain witness strategy;
- Scripture/RSS architecture;
- November 29, 2026 USCCB effective-date note;
- provenance requirements;
- attribution requirements;
- prohibited shortcuts;
- procedure for new corpus imports;
- procedure for unresolved rights;
- source URLs and retrieval dates.

Also add a corpus audit record, suggested path:

```text
build/agent-continuity/liturgical-corpus-rights-and-completeness.md
```

This should be a factual execution ledger, not aspirational prose.

---

# 28. Work Sequence

Execute in this order unless repository evidence demands a better sequence.

## Phase A — Baseline

1. identify branch/head;
2. inventory corpus architecture;
3. capture tests/build status;
4. capture completeness metrics;
5. inventory existing policy/docs;
6. inventory rights suppressions;
7. inventory source/provenance quality.

Commit/record the baseline if repository workflow expects durable checkpoints.

## Phase B — Policy reset

1. install the permission-maximizing policy;
2. implement typed rights/provenance schema or migrate the existing equivalent;
3. update render/publication logic so unknown does not automatically mean forbidden;
4. centralize attribution.

## Phase C — 1955

1. establish exact target edition/state;
2. fill structural holes;
3. fill Latin text from defensible public-domain witnesses;
4. validate calendar/rubrics;
5. establish Scripture mapping/text strategy;
6. generate completeness/delta reports.

## Phase D — 1962

1. complete the corpus;
2. establish public-domain witnesses;
3. validate 1955 -> 1962 deltas;
4. eliminate unexplained holes.

## Phase E — Postconciliar

1. separate Latin / ICEL / USCCB / CCD ownership layers;
2. expose ICEL text allowed by express web permission;
3. source public-domain Latin antecedents where appropriate;
4. segregate modern Latin requiring separate analysis;
5. integrate authorized readings syndication where useful;
6. complete calendar/options/propers;
7. preserve national adaptations distinctly.

## Phase F — Cross-edition validation

1. stable text identities;
2. historical deltas;
3. provenance completeness;
4. rights completeness;
5. UI availability semantics;
6. full tests/build/browser gates.

---

# 29. Stop Conditions

Do **not** stop because:

- the corpus is large;
- a modern source bears a copyright notice;
- some texts require case-by-case analysis;
- one source is inconvenient to parse;
- public-domain witnesses require cross-comparison;
- an earlier policy marked content "held" or "unavailable";
- a broad USCCB page sounds restrictive.

Stop and report a blocker only when:

1. an authoritative source affirmatively forbids the intended use and no alternative lawful publication basis exists;
2. the exact target text cannot be established from reliable sources;
3. rights ownership is materially disputed and publication would require guessing;
4. implementing the change would require destructive scope outside this task;
5. repository tests reveal a pre-existing blocker that makes further corpus changes unsafe and cannot be repaired within scope.

Even then, continue all independent lanes.

One blocked text must not block an entire missal.

---

# 30. No Unsupported Claims

Do not write:

- "we own this";
- "this is public domain";
- "permission is not required";
- "this text is absent";
- "the Vatican cannot copyright this";
- "ICEL allows all liturgical text online";

unless the actual narrower proposition is established.

Prefer precise claims:

> The underlying Latin collect is attested identically in a public-domain 1920 witness; Mystagogy's transcription derives from that witness rather than the modern edition.

or:

> This English text is ICEL-owned and falls within ICEL's standing permission for promulgated ICEL texts on a noncommercial website, subject to the stated conditions.

Precision is more permissive than vague fear because it lets us publish what is actually allowed.

---

# 31. Definition of Done

This task is done only when:

- the permission-maximizing policy is durable and documented;
- 1955 has a measured, explained corpus state;
- 1962 has a measured, explained corpus state;
- the postconciliar corpus has a measured, explained corpus state;
- all three are substantially enriched/completed wherever reliable sources permit;
- rights ownership is typed rather than guessed from book-level labels;
- ICEL-covered English is no longer unnecessarily withheld;
- ancient/public-domain Latin is not unnecessarily withheld merely because a modern edition reproduces it;
- Scripture rights are architecturally separated from lectionary assignment;
- authorized RSS use is supported where advantageous;
- attribution is automatic and correct;
- every remaining unavailable item has an explicit reason;
- every remaining permission request is narrow and specific;
- tests prove historical distinctions rather than flattening the rites;
- the repository contains before/after corpus metrics;
- all relevant test/build/browser gates pass or failures are proven pre-existing and unchanged;
- a final continuity record tells the next agent exactly what changed, what remains, and why.

---

# 32. Final Report Format

At completion, report:

## Identity

- branch
- parent
- head
- commits
- changed production files
- changed corpus/source files
- generated files

## Policy

- previous effective policy
- new effective policy
- authoritative sources
- rights schema changes

## Corpus

### 1955
- completeness before
- completeness after
- major additions
- unresolved holes

### 1962
- completeness before
- completeness after
- major additions
- unresolved holes

### Postconciliar
- completeness before
- completeness after
- ICEL text enabled
- Latin text enabled
- USCCB/CCD external/restricted material
- unresolved holes

## Rights

- newly established public-domain bases
- express-license bases
- syndicated bases
- ambiguous-but-defensible bases
- genuinely restricted items
- actual permission requests still needed

## Validation

- focused tests
- full tests
- browser tests
- corpus validators
- generation reproducibility
- before/after failure comparison

## Risks

Only concrete remaining risks, each tied to a corpus item, source, rightsholder, or implementation defect.

---

# 33. Core Principle

The site's policy must reflect a distinction that is both editorially and legally important:

> **The Church's public liturgical text, the copyrightable features of a particular modern edition, a copyrighted translation, and ecclesiastical authorization to use a book in worship are not the same thing.**

Treat them separately.

The project should be aggressive about recovering, preserving, and publishing the Church's liturgical patrimony wherever a defensible basis exists, while being exact and transparent about the comparatively small set of texts whose modern authorship, translation rights, national adaptation, Scripture rights, or explicit publication restrictions genuinely require a license.

The desired result is not a corpus made artificially sparse by fear.

The desired result is a **complete, source-auditable, historically precise, rights-aware Roman Mass corpus for 1955, 1962, and the postconciliar rite, with the maximum amount of lawful text actually available to the reader.**
