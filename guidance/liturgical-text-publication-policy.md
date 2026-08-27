# Liturgical text publication policy

The rule for deciding whether a liturgical text may appear on this site, whose
right it is, and under what basis. Adopted 2026-08-20 on the maintainer's
written direction, replacing a presumption against publication with a
presumption for it.

**This document owns one rule and one procedure.** The rule is §1's presumption
and priority order. The procedure is §13 and §14. Everything else here is the
evidence those rest on, stated once so that the question is not reopened a
fourth time. `sources.md` still governs retrieval, aliases, storage disposition
and the rights-record genre; `missals.md` still reports what the missal
acquisition audit found; `the-shape.md` §4 still governs how an absence is
written. Where this page and a rights record under `src/sources/inventories/`
differ on a fact, the record is right; where they differ on the **presumption**,
this page is right and §15 says which sentences it displaces.

**It is not legal advice and it binds nobody outside this repository.** The
jurisdiction throughout is the United States unless a section says otherwise.

## Evidence conventions

- **[verified]** — read on the stated date from bytes fetched to this machine.
- **[sourced]** — read from an external document cited by URL, not re-derived.
- **[recorded]** — taken from a record already in this repository, cited by path.

Retrieval dates and URLs for every controlling source are in §16. A permission
whose policy cannot be re-opened cannot be re-verified, which is why the URL and
the date travel together everywhere in this file.

---

## 0. Where this came from

The maintainer wrote `guidance/liturgical-corpus-brief-2026-08-21.md` and
confirmed it as the project's governing instruction. This page is that brief's
standing policy, implemented and verified against sources opened at execution
time; the brief itself asks for exactly that verification, and where the two
differ this page governs. The brief's work-order half — its repository sweep,
completeness audit, phase sequence, Definition of Done and report format — has
been partly addressed but remains open. This page implements the standing
rights policy; it does not certify completion of that work order.

## 1. The presumption, and the priority order

> **Publish unless a copyright holder has affirmatively reserved the particular
> use at issue, or the text lacks a defensible permission or public-domain
> basis.**

The superseded presumption — *do not publish unless someone has affirmatively
granted permission* — is no longer this project's rule. §15 lists where it is
still written down.

Apply these bases in order, and record which one a text stands on:

1. **public-domain underlying text** → publish;
2. **express general web permission** → publish under its stated conditions;
3. **ancient or public-domain underlying work reproduced in a modern
   copyrighted edition** → source independently from a public-domain witness
   and publish the underlying work;
4. **authorized syndication mechanism** → display through that mechanism;
5. **specific written permission the project already holds** → publish within
   its scope;
6. **ambiguous but defensible basis** → prefer publication, document the
   argument, mark the basis explicitly;
7. **affirmative restriction, or no defensible basis** → do not locally
   republish; keep the metadata and expose a typed unavailable state.

The burden is on a restriction to be specific enough to defeat an otherwise
defensible basis. This is not a licence to ignore copyright. It is an
instruction to analyse the actual work, the actual rightsholder, the actual use
and the actual licence, instead of reading every copyright notice as ownership
of all the words beneath it.

**Two limits on the presumption, and they do most of the work in practice.**

- A basis is a permission to *use*, not a supply of *text*. §4.
- A basis is decided per text **and per surface**. §3.4.

---

## 2. When authority conflicts

Prefer, in order: statute or controlling law; an official Holy See or bishops'
conference decree; the current rightsholder's own publication or permissions
policy; official publisher or commission guidance; scholarly or historical
evidence; secondary commentary.

**A generic permissions page does not silently override a more specific express
permission from the actual rightsholder.** To displace such a permission,
establish that it was rescinded or superseded — not merely that some other body
says it would not grant the same thing. §6 is the live instance of this rule and
the one place this policy meets real resistance.

Where two sources conflict and neither is displaced, state both, say which
governs and why, and record the disagreement rather than resolving it silently.

---

## 3. ICEL's standing web permission

### 3.1 The grant

*Publication Policies of the International Commission on English in the Liturgy,
Inc.*, effective December 1995, amended 2008, 2010, 2013, appendix p. 25
[verified 2026-08-20]. Quoted entire, because every one of its conditions binds:

> **Use of ICEL Materials on Global Computer Networks**
>
> ICEL texts and translations that have been approved by the Conferences of
> Bishops, have received the recognition of the Holy See, and have subsequently
> been promulgated for use on the date established by the Conferences of Bishops
> may be reproduced in a non-commercial site ("Site") on the global computer
> network commonly known as the Internet without obtaining written or oral
> permission, subject to the following conditions:
>
> (1) there must be no fee charged to access the Site or any of the ICEL
> translations, texts, or music, thereon;
>
> (2) The appropriate ICEL copyright acknowledgment must appear on the first
> and last pages and/or frames within the Site displaying the ICEL translation
> or text (see www.icelweb.org and click on "copyright policies");
>
> (3) The ICEL translations and texts must be followed exactly;
>
> (4) These policies do not grant a license to publish texts in any other form
> or any other right in ICEL's name and marks, and the Site may not display the
> ICEL translations or texts or otherwise use the ICEL name in any way that
> implies affiliation with, or sponsorship or endorsement by, ICEL;
>
> (5) ICEL reserves the right to terminate or modify its permission to use its
> translations and texts;
>
> (6) ICEL reserves the right to take action against any party that fails to
> conform to these policies, infringes any of its intellectual property rights,
> or otherwise violates applicable law.

### 3.2 The page that does not carry it, recorded so nobody re-derives the wrong answer

**`icelweb.org/copyright.htm` alone does NOT carry this permission.** Fetched
2026-08-20 [verified], it says only that "All requests for permission should be
directed to the ICEL Secretariat", and gives the acknowledgment form. A reader
who checks that page and stops will conclude that no web permission exists and
that a written request is the only route. That conclusion is wrong, it was
reached in this repository, and §15.1 shows the record where it hardened.

Both pages are needed and neither substitutes for the other: **the PDF is the
grant; `copyright.htm` is the acknowledgment wording condition (2) points to.**
Cite the PDF for the permission. Cite `copyright.htm` only for the notice.

### 3.3 What the grant reaches: four facts, established per text

The clause reaches a text that is (a) ICEL's own, (b) approved by the
Conferences of Bishops, (c) recognised by the Holy See, and (d) promulgated for
use. Each is a fact about that text, never an inference from the book it is
printed in — §5.

(a) is settled for the Mass texts by ICEL's own published inventory: §5.2.
(b), (c) and (d) remain per-text facts, though for the 2011 U.S. *Roman Missal*
as a whole they are matters of public record rather than open questions. A
provisional or draft section text is **not** promulgated text and is outside the
grant; the inventory at §5.2 is an ownership record and not a promulgation
record, and it must not be read as one.

The narrow proposition this policy supports, and no broader one:

> This English text is ICEL-owned and falls within ICEL's standing permission
> for approved, recognised and promulgated ICEL texts on a non-commercial
> website, subject to the six stated conditions.

### 3.4 Condition (4): the basis is per surface, not per text

Condition (1) is about fees. Condition (4) is about **forms**, and they are
separate conditions. mystago.gy satisfies condition (1): no fee, no
registration, no advertising, no third-party call, nothing of value asked of the
reader [verified 2026-08-20, from the release records and site sources; the
deployed origin's own configuration is outside what any file here proves and
should be confirmed there].

Two existing routes fall outside condition (4), and this is not qualified:

- **Downloadable files.** `pdf/` holds installed PDFs, the browser builds
  explicit `download` links to them, and the release authorization's
  `authority_scope` includes `public-web-hosting-and-download`. A file handed to
  a reader is a publication in another form. Free does not cure it.
- **The corpus as data, and the public Git repository.** `src/web/data/` is
  fetched from stable public URLs, and the repository is public by design. A
  clonable copy is a distribution of copies, which is a different act from
  displaying a site.

There is a mechanical hazard behind the second. `LICENSE` offers project-created
content under CC BY 4.0 and carves out third-party material only where a file or
`THIRD_PARTY.md` says otherwise — a real mechanism, but a manual one. **ICEL
text entering the corpus without a `THIRD_PARTY.md` entry and a file-level
marker would be swept into an outbound CC BY 4.0 offer**, purporting to
sublicense ICEL's translation to the world. That is worse than not publishing,
and it would happen by omission rather than by decision.

**Therefore: no ICEL payload belongs in a propers corpus, public static-data
bundle, Git distribution, or PDF merely because a free live site could display
it.** Text-free source, provenance, rights, and acknowledgement metadata may be
tracked; the payload remains quarantined unless a separate non-bundled display
route can enforce the per-text and per-surface decision. `mass-ordinary` and
`mass-propers` can require an acknowledgement for a permission-bearing witness,
but that validation does not expand the permission or make the generated JSON
an eligible surface. The public-artifact boundary must refuse the payload as
well.

The acknowledgement is also surface-specific. ICEL's current copyright page
prescribes `Excerpts from the English translation ...` for excerpts and a
different form for an entire work. A selected proper or Ordinary element uses
the excerpt form. Retaining the entire-work form copied from a source PDF, or
replacing `©` with `(c)`, does not satisfy the current prescribed wording.

**Current-tree quarantine does not clean Git history.** Earlier commits tracked
ICEL payloads, including strings sourced through unofficial intermediaries; the
commit graph retains those blobs after the served files stop carrying them.
Whether the public repository needs a history rewrite, replacement, access
change, or another remedy is a release-policy and counsel decision for the
maintainer. This policy records the residual and does not treat a clean current
artifact as retroactive clearance of historical distribution.

---

## 4. Permission is not availability

**This is the single most important distinction in this document.**

ICEL's grant is established. That does not make a stored copy publishable, and
it does not establish that any candidate string is exact, approved, recognized,
promulgated, current for the relevant territory, or ICEL-owned rather than a
USCCB/CCD or other rightsholder's text.

Condition (3) requires the texts be followed exactly. Brief §14.3 and §15, and
`sources.md`, forbid sourcing them from blogs, unofficial missal sites, scraped
parish PDFs, unverified OCR, or generation.

**A first survey on 2026-08-20 got this substantially wrong, and the correction
is instructive enough to keep as an audit snapshot rather than overwrite.** It
claimed that most ledgered slots lacked an authoritative source and that "ICEL
grants the permission and publishes no exemplar: its own site has seven pages,
catalogues the books it has translated, and offers no text and no download".
The second claim is false. Re-scored the same day against files actually opened
at the bytes, the survey found multiple official, free, whole, reachable sources.
Its old slot counts are intentionally not restated here: later corpus work
changed the inventory, and source reachability is not a publication decision.

What that survey missed, and what any later one should look for first:

| Source | What it publishes | Reaches |
| --- | --- | ---: |
| ICEL's own open music folder, linked from its News page | publisher PDFs of the Missal's chanted texts; the inventory distinguishes publisher artifacts, restricted derivatives, and its index rather than treating every manifest as one free PDF | the bulk of the Holy Week ritual slots |
| The ICEL Antiphonary, hosted by the CBCEW Liturgy Office | 265 pp: the English of ALL Entrance and Communion Antiphons of the Missale Romanum 2002/2008, Proper of Time, Saints, Commons, Ritual, Various Needs, Votive and Dead | every antiphon slot |
| CBCEW Liturgy Office | the whole Order of Mass and all four Eucharistic Prayers, free and entire | the Order of Mass |
| USCCB, `/resources/` PDFs | the Committee on Divine Worship Newsletter archive and the post-2011 Mass formularies, several carrying the full English formulary with both Roman decrees | new celebrations |

Two facts about the Antiphonary matter beyond its coverage: its hosting page
states that **a Word version is available on request**, which is close to the
machine-readable reference copy the narrow ask below describes; and its own
copyright block names Psalms 23(24), 46(47) and 115(116) as Revised Grail,
which is GIA's and not ICEL's — see §5.1.

The gaps in that dated survey had a structural pattern: conference sites tended
to publish the Order of Mass, GIRM, new celebrations, and Holy Week, but not the
whole Proper of Time. That observation is a search lead, not proof that no
official source exists; later harvests must report their own measured coverage.

The England-and-Wales text must be verified element by element against the U.S.
state before it lands: the universal ICEL text is common to ICEL territories,
national adaptations are not. And an authoritative publisher establishes WHO
says so, not AS OF WHEN: ICEL's own presidential-tones file prints the Advent 1
Collect with the ending superseded after Cardinal Sarah's letter of May 2020,
which each conference implemented on its own date.

So the reason a slot is empty must be recorded truly. It is not enough to say
*"nobody may publish"* or *"ICEL owns it"*. Name the actual blocker: no exact
authoritative copy, a territory/version mismatch, a different rightsholder, or
the fact that the only recorded permission is for a live web display while the
current route would bundle a downloadable copy.

Anything that closes such a slot without naming an exemplar is a
reconstruction, and §12 forbids it absolutely.

An authoritative **reference copy** can solve the exactness problem. It cannot
solve the surface problem by itself. A request to a rightsholder is a
representation about who is asking and what they will do; **only the maintainer
may send one, and no agent may.** Any request must name the unresolved text and
surface narrowly rather than ask for a blanket license already partly addressed
by a standing policy.

---

## 5. "English Roman Missal text" is not one copyright bucket

Do not classify a text by the book it appears in.

### 5.1 The 2011 book's own copyright block divides itself six ways

Read from the book's front matter and recorded `[verified]` at
`src/sources/inventories/lt-hist-rights-audit-v1.toml`, `[[notices]]`, version
`2011-roman-missal-third-edition-english-source-located`. Six claimants over one
volume:

| What | Claimant |
| --- | --- |
| the Latin | Libreria Editrice Vaticana, 2008 |
| **the English translation and chants** | **International Commission on English in the Liturgy Corporation, © 2010** |
| the *Lectionary for Mass* | Confraternity of Christian Doctrine, with its own express prohibition on reproduction |
| three psalms (23[24], 46[47], 116[115]) | Revised Grail Psalms, Conception Abbey / The Grail, admin. GIA |
| **particular adaptations and proper texts for the Dioceses of the United States** | **United States Conference of Catholic Bishops, © 2010**, with its own express prohibition |
| one musical setting | Robert Snow |

Two consequences. First, the sentence *"no portion of this text may be
reproduced by any means without permission in writing"* is **not** a global
reservation over the book; it is the tail of the CCD's lectionary notice and
governs the readings. Second, neither express prohibition printed in that book
reaches an ICEL oration: the CCD's governs the readings, the USCCB's governs the
U.S. adaptations and U.S. propers, and the ICEL line carries "All rights
reserved" with its terms stated in ICEL's own published policy — which is §3.

**A third consequence, withdrawn.** This page argued on 2026-08-20 that the
Grail line made the unit of rights smaller than a proper slot, because on Palm
Sunday an ICEL antiphon and a Grail psalm verse appear together, and that no
antiphon could land until the model could express it. **That was wrong, and the
schema already had the answer.** An antiphon slot is `source: mixed`: it carries
the antiphon's own words as `text` and its scriptural constituents as `verses`,
which are CITATIONS resolved at render time against whichever bible the reader
has selected. The 1962 calendar has done this all along — its First Antiphon at
the Distribution of Palms carries the antiphon's Latin beside `Matthew 21:9` and
`Psalm 23:1-2, 7-10`, and the psalm's words come from the reader's own edition.

So a Grail rendering is never needed and never wanted. What this project carries
from ICEL is the antiphon; what it carries for the psalm is the reference. The
psalms are the psalms, and they are served from the public-domain editions this
repository already indexes. No slot is blocked by the Grail line, and the three
psalms it names require nothing of us but that we do not transcribe ICEL's
particular rendering of them, which we have no reason to.

### 5.2 What ICEL says it owns

`icelweb.org/copyrightICEL.htm` and its child `RomanMissal.htm`, both retrieved
2026-08-20 [verified]. ICEL's own inventory names as its property, now carried
by the single 2010 *Roman Missal* acknowledgment that supersedes the
provisional section copyrights: the **Order of Mass**, the **Proper of Seasons**,
the **Proper of Saints**, the **Commons**, **Ritual Masses**, **Masses and
Prayers for Various Needs and Intentions**, the **Antiphons**, **Votive
Masses**, **Masses for the Dead**, the **Eucharistic Prayers** including those
for Masses with Children and for Reconciliation, the **GIRM**, and the
**Appendix** and **Supplement**. Also ICEL's: *The Roman Missal*, 1973, and both
1998 *Sacramentary* volumes — which is why age is not a route to the 1973 text
and will not be in any reader's lifetime.

This establishes fact (a) of §3.3 for the Mass texts and nothing more. It is an
ownership record. It says nothing about which English is the **approved**
English, and `RomanMissal.htm` describes provisional texts issued during the
translation of the *Missale Romanum* 2002. A provisional Green or Gray Book text
must never be imported as approved liturgical text.

### 5.3 USCCB and CCD material: classify it separately and do not import it

Absent from ICEL's inventory of its own property, and owned elsewhere: the *New
American Bible*; the *Lectionary for Mass for Use in the Dioceses of the United
States* (the CCD book — distinct from ICEL's own "Lectionary for Mass, 1969,
1981, 1997", which was never the U.S. lectionary); *The Abbey Psalms and
Canticles*, which is **USCCB-owned, not ICEL-owned**, and is the place a corpus
most easily mistakes one bucket for another; and the U.S. proper calendar and
national adaptations.

The USCCB's 2025 guidelines print the mandated notices for these, and they are
affirmative restrictions in the sense of §1 item 7 [sourced 2026-08-20]:

> No portion of this text may be reproduced by any means without permission in
> writing from the copyright owner. *(Lectionary for Mass)*

> No part of the New American Bible may be reproduced in any form without
> permission in writing from the copyright owner.

> No part of this work may be reproduced or transmitted in any form or by any
> means … without permission in writing from the copyright holder. *(The Abbey
> Psalms and Canticles)*

For this material there is no competing ICEL standing grant, the holder's own
statement is the governing source, and **§1 item 7 applies to this repository's
local corpus and public bundle: do not locally republish.** No lane should treat
ICEL ownership of neighboring material as a basis for these texts.

The CCD/NAB permissions page appeared through the official site's indexed web
view on 2026-08-26 but still returned HTTP 403 to the required whole-document
retrieval path. Treat that as corroboration, not a verified source-text fetch.
Nothing turns on the gap: the verified authorized RSS route at §9 does not
authorize building a permanent local NAB, NABRE, or Lectionary corpus, and it
does not apply to ICEL Missal text.

---

## 6. The adverse finding, recorded because a policy that omits it is not honest

The USCCB's *Copyright Permission Requirements for the Use of Liturgical Texts*,
excerpted from the July–August 2021 Newsletter of the Committee on Divine
Worship, © 2021 USCCB, retrieved 2026-08-20 [verified], under the heading
"Posting Text, Audio, or Video Online (Apart from Digital Worship Aids or
Livestreamed Liturgies)":

> **Typically, permission is not granted to post the liturgical texts online.**
> However, no permission or fee is needed to display the daily readings using
> the USCCB RSS feed, but only on a website which does not condition access by
> users on the users giving anything of value to the website operator.
> Permission is not granted to podcast or offer videos of the Sunday or daily
> readings.

A second and older statement points the same way. The USCCB's *Policy on
Electronic Copyrights* [sourced,
`https://www.usccb.org/committees/divine-worship/policies`, re-read at source
2026-08-20]:

> With the exception of publication permission for single daily collects from
> the Roman Missal, no permission will be given for the publication of
> liturgical texts on the Internet at this time.

**These are the most adverse things in this whole analysis and they are not to
be minimised.** Four features narrow the first, and one does not.

1. **It describes what the Secretariat grants, not what a different rightsholder
   has already granted.** The sentence is in the indicative about a permissions
   practice — "permission is not granted." Where ICEL has granted in advance and
   in writing the permission this office would otherwise be asked for, there is
   nothing here to withhold. This is a permissions FAQ, one heading of a
   newsletter; §2's rule applies squarely.
2. **Its declared subject is narrow.** It addresses "parishes, schools, and
   other entities" asking about "typical uses" of the English and Spanish
   liturgical texts. It does not mention, and is not addressed to, comparative
   or scholarly publication of historical rites.
3. **It is a 2021 document.** The 2025 guidelines are the later and fuller
   statement of the same Committee, they cover digital publication at ¶52 and
   open the ¶69 subcategory, and they do not repeat this sentence.
4. **Its own carve-out independently re-verifies the RSS grant** from a second
   USCCB page, in nearly the words of `/subscribe/rss`. §9.

**What none of that reaches.** For text the USCCB or the CCD actually owns —
the NAB, the LFM, *The Abbey Psalms and Canticles*, U.S. propers and national
adaptations — this page is the holder's own statement, there is no competing
grant, and the answer is no. §5.3.

**What the evidence supports about ICEL.** Nothing located establishes that
ICEL's Internet clause has been rescinded or superseded, and a different body's
generic permissions FAQ is not evidence of rescission by the rightsholder. That
supports recording ICEL's grant for ICEL-owned text. It does not settle whether
another approval, authentication, or territorial requirement attaches to a
particular U.S. publication.

**What this policy does not assert.** It does not assert that the USCCB is wrong,
that no USCCB requirement can attach to a publication in the United States, or
that the two statements have been reconciled by anyone but this project. The
2025 guidelines describe a route in which "ICEL … issues licenses for
publications after receiving the authentication of the Secretariat." They are
scheduled to enter force on 29 November 2026, cover digital publications, and
do not mention ICEL's Internet clause. This repository does not resolve that
silence into either a revocation or an exemption. Its current public-data route
quarantines the ICEL payload. Any future non-bundled display in the United
States must recheck both bodies' then-current requirements before release.

Also carry across the preamble's exactness demand, which is materially ICEL
condition (3) plus one more requirement:

> In all cases, the excerpts must be verbatim from the official text, including
> capitalization and punctuation. The poetic structure of those texts provided
> in sense lines must generally be preserved.

**A corpus schema must be able to represent sense lines before it stores a
single oration.**

---

## 7. The 2025 USCCB guidelines and 29 November 2026

*Guidelines for the Publication of Liturgical Books*, approved 15 June 2025 by
the Committee on Divine Worship, first printing July 2025, 51 pp. Its title page
and its HTML landing page both carry, verbatim [verified 2026-08-20 from two
independent renderings of the same act]:

> Enters into Force on November 29, 2026, First Sunday of Advent

### 7.1 What the date does and does not change

**Encode the date.** It is confirmed. Present requirements and future
requirements are different things and must be kept apart.

- **Do not** infer from the effective date that ICEL ownership or ICEL's present
  published policy has changed. Do quarantine any payload whose actual release
  surface has not been cleared under the complete applicable requirements.
- **Do** create an explicit record for any present behaviour that becomes
  noncompliant under a plausible reading of the new rules, with an action date
  before 29 November 2026.
- **Do not** populate `effective_from` on a rights record with this date for
  anything but the guidelines themselves. It is the date a publication rule
  binds, not the date a permission begins or ends.

The guidelines define "publisher" and "publications" widely enough to catch a
free digital publication by a lay individual — "for-profit or not-for-profit,
ecclesiastical, religious, or lay", "print or non-print (e.g., digital), whether
for sale or for distribution without charge". A reading that says *we are not a
publisher because we are not a firm and sell nothing* is not available on those
words. What the document then does with that width is answered by **category**,
not by the definition.

The one categorical rule the brief names is ¶52, and it is narrower than a
paraphrase suggests:

> Digital production platforms and subscriptions must have a license for use of
> copyrighted texts, and their products must undergo review by the Secretariat.
> … Digital platforms must follow all requirements for participation aids, and
> licensing and royalty fees should be reviewed annually and adjusted based on
> subscription numbers.

¶52 sits inside Section C, and its last sentence presupposes that the platform
in question **is** a participation aid; its fee mechanism describes a
subscription product. It does not reach a free non-subscription reader in the
¶69 class. **It would reach one the day that reader became a digital
participation aid.**

### 7.2 ¶69 is a possible study category, not a classification of the day reader

¶40 defines participation aids as publications "providing the necessary texts
and music to fulfill [the lay faithful's] active role in the celebration" —
hymnals, annual and quarterly pew aids. ¶69 opens the fourth subcategory,
**Non-Liturgical Publications That Quote Liturgical Texts**:

> This subcategory refers to texts that quote portions of liturgical texts.
> These texts are not complete ritual texts, not intended for liturgical use,
> nor are they able to be used liturgically. Examples include, but are not
> limited to catechetical materials, academic books, devotional materials, etc.

A comparative source-critical study that quotes only bounded portions may fit
¶69's description. That possibility does not classify every surface in this
repository. The day reader lays out a single day's Mass in celebration order,
offers prayer and Ordinary text, and is explicitly intended to be usable at
Mass; those facts place it near the participation-aid boundary rather than
establishing the academic-book category.

¶57 supplies the controlling caution: in ambiguity, follow the participation-
aid requirements, and a publisher may ask the Secretariat whether a work
qualifies as devotional. **The Secretariat decides; this project does not.**
Until a release surface is classified and all applicable rights are established,
do not use ¶69 as a publication basis. Keep ICEL payloads out of the clonable
public-data bundle and keep USCCB/CCD payloads out unless a separate license or
authorized syndication route actually covers them.

The dated action record
[`day-reader-participation-aid-review-v1.toml`](../src/sources/inventories/day-reader-participation-aid-review-v1.toml)
applies that caution to the present Day-reader surface. It records an internal,
non-legal fail-closed decision on 26 August 2026 and requires a fresh evidence
review to begin by 15 November and finish before the guidelines enter into force
on 29 November 2026. If that review is absent or incomplete, the gate stays
closed; the date supplies neither a classification nor blanket clearance.

Describe every released surface accurately. Never call it an official ritual
edition, an approved altar Missal, an authenticated liturgical book, or a work
carrying a *concordat cum originali*; never imply review, sponsorship, or
endorsement by ICEL, the USCCB, or the Holy See.

---

## 8. Latin: the ancient work and the modern edition

A modern copyrighted edition of the *Missale Romanum* does not create a new
copyright in an ancient collect, antiphon, canon or ordinary that was already
public domain. The Holy See's claim over its typical editions is real and is
respected. Do not conflate:

- a copyrighted modern **edition**, its editorial apparatus, arrangement,
  typography, newly authored material and edition-specific changes; with
- the **underlying ancient or otherwise public-domain liturgical text**.

### 8.1 *Postquam Summus Pontifex* (2021) is the current word, and this repository does not hold it

Decree of the Congregation for Divine Worship and the Discipline of the
Sacraments, 22 October 2021, giving effect to canon 838 CIC as modified by
*Magnum principium*; abbreviated `PSP` and cited at nn. 39–40 by the USCCB's own
2025 guidelines. Retrieved 2026-08-20 from the Holy See Press Office bulletin
[verified].

- **n. 2** — the Latin *editiones typicae* are promulgated by the Apostolic See,
  "which holds their copyright", and the same applies to subsequent editions.
- **n. 3** — a licence from the Congregation is required each time to print or
  reprint these Latin books **for liturgical use**, and: "**Similar permissions
  are also required for the distribution of liturgical books or parts thereof
  via the internet.**"
- **n. 3, footnote [8]** — "For editions of liturgical texts, even partial
  editions, for non-liturgical use (study editions, worship aids) the norms of
  the *Codex Iuris Canonici*, can. 826 § 3 apply." That is the imprimatur norm,
  the same canon the 2025 guidelines cite at ¶63 and ¶70.
- **n. 40** — the copyright of vernacular liturgical books and texts is held by
  the Bishops' Conference. This is the 2021 successor to *Liturgiam authenticam*
  n. 117.

**What footnote [8] gives, stated narrowly.** It is the strongest support any
source gives to §7.2: a study edition is expressly contemplated, expressly
distinguished from the licensed liturgical-use edition, and routed to a
canonical norm about doctrinal review rather than a proprietary one about
licensing. **What it does not say, and must not be inferred: it does not say a
study edition may reproduce the copyrighted Latin without permission.** It
allocates canonical competence; a footnote allocating canonical competence is
not a copyright licence, and n. 2's ownership claim stands over both cases.

Two open items follow, both real:

1. **PSP is not registered anywhere in this repository** — a search on
   2026-08-20 for "Postquam Summus", "postquam-summus" and `\bPSP\b` found no
   source record, passage or citation. The repository cites *Liturgiam
   authenticam* n. 111 (2001) in its place, and n. 111 speaks only of
   reprinting where PSP n. 3 speaks of the internet. **Registering PSP is the
   highest-value source acquisition this analysis identified.** Until it is
   registered, cite it as `[sourced]` from the URL in §16 and not from a
   repository record.
2. **The Holy See's own cited authority for its copyright has not been
   retrieved.** PSP n. 2 footnote [7] cites *Secretariat of State, Decree, 13
   May 2005: AAS 97 (2005) 798-799*. That, not LA n. 111, is the instrument the
   Holy See points to. Note also that `missals.md` §5 already cites a
   Secretariat of State decree of **31 May 2005** vesting rights in LEV; whether
   these are one act with a date discrepancy or two acts is unresolved here.
   **No policy document may claim to state the Holy See's current copyright
   position at first hand until the AAS text is acquired.**

A bounded negative, from a search and not from an exhaustive reading of the
*Acta*: no successor instrument later than PSP was found on 2026-08-20. Re-run
that search rather than trusting it indefinitely.

### 8.2 The public-domain witness strategy this repository already practises

For a Latin item in the 1955, 1962 or postconciliar Missal:

1. determine whether the underlying text predates modern copyright;
2. find the earliest reliable public-domain witness available to the project;
3. transcribe and verify from that witness;
4. compare against the target missal edition;
5. record whether the target reading is identical, orthographically normalized,
   rubrically changed, or substantively changed;
6. publish the underlying text where the witness establishes the target wording;
7. copy no protected editorial apparatus from a modern commercial or Vatican
   edition;
8. assess genuinely modern additions and revisions separately, on their own
   basis.

The goal is to establish the text independently — **not to pretend a modern
source was not used when it was.**

This is not new. Two routes already run here and both are recorded in
`postconciliar-proper-translations-v1.toml`: the **project-created** route,
which translates the ancient Latin afresh where the Missal prints an ancient
prayer unchanged; and the **antecedent** route, which carries a public-domain
book's English of the older oration where this calendar's own recorded Latin
reproduces it, one prayer at a time, on a shown identity of two Latin texts,
never as the Missal's English. Both stand. §15.3.

Their limits also stand, and are load-bearing. A similarity score is not an
identity. Nothing may carry a hand missal's English onto a postconciliar oration
on the strength of a coverage figure. Where the reform composed, recentonised or
rewrote, the alteration is the reform's and nothing is published.

**Do not let the genuinely modern minority force the whole Latin corpus into an
unavailable state.** Keep an explicit inventory of texts modern enough that
public-domain antecedent sourcing does not establish the target wording — newly
composed postconciliar collects and prefaces, new Eucharistic Prayers, propers
for recently canonized saints, post-1955 and post-1962 revisions that are not
restorations, new rubrics — and give those their own rights basis.

The current inventories still contain many substantive Latin bodies with no
per-text rights token or exact per-text target-edition witness. Their count is
mutable and must be derived from the inventories and validators rather than
copied into this policy. Their bases are not uniform, and assigning one basis to
all of them would assert a uniformity the record denies. The field must exist
and default to nothing, so that a text lacking a basis is visibly lacking one.

---

## 9. Scripture: assignment is not text

Keep four things separate, in schema and in code:

- **lectionary assignment** — which passage is appointed for a given Mass;
- **scriptural text** — the actual words of a Bible translation;
- **liturgical rendering** — incipits, refrains, acclamations, lectionary-
  specific adaptations;
- **source mechanism** — local corpus versus authorized syndication.

**This branch has implemented that separation for the postconciliar weekdays.**
287 weekday entries carry only the Lectionary *assignment*, as encoded
citations: no reading, no pericope title, no psalm response, no acclamation
text, no rubric, and structurally verified before landing — not one `text` field
across all 287. The citations were read from page images of the 1981 *Ordo
lectionum Missae* at 200 dpi, never from its optical text layer, and every entry
names its artifact page, printed page and marginal number. The scan itself stays
where its rights record puts it.

Which passage is appointed is a fact about the liturgy that this project records
and may keep recording. **The NAB text is not ours to store.** §5.3.

**The authorized syndication route.** `usccb.org/subscribe/rss`, retrieved
2026-08-20 [verified]:

> No permission or fee is needed to display the daily readings on an RSS feed
> only on a website which does not condition access by users on the users giving
> anything of value to the website operator.

and, the boundary in the same document:

> E-books and digital applications for sale or for free distribution require a
> license and a royalty payment or permissions fee.

mystago.gy meets the access condition on the evidence at §3.4. So where the site
can lawfully and technically display the official U.S. daily readings through
the feed, that path may be preserved or implemented; caching only so far as the
authorization and ordinary technical necessity allow; attribution and source
metadata preserved. **A permission to display through a feed is not a right to
build a permanent local NAB or Lectionary corpus, and it must never be converted
into one.** Where the feed cannot support historical or arbitrary-date browsing,
or all required Mass variants, say so plainly rather than papering over it.

**Public-domain Scripture** may be stored, indexed, searched, verse-aligned,
annotated, cross-referenced, used for Catena links, and compared across missals.
The Douay–Rheims (Challoner) already serves this role. Never assume a particular
modern digital edition is public domain because the underlying translation is:
establish the provenance of the transcription as well as of the translation.

---

## 10. Provenance

Every substantive text carries recoverable provenance: work identity; language;
rite and missal edition; liturgical location; source witness; source date;
source locator; transcription source; verification witnesses; editorial
transformations; rights basis; authority; confidence.

Never collapse **text identity**, **liturgical assignment**, **rights status**,
**translation identity** and **witness identity**. A text can be public domain as
a Latin work, represented by several witnesses, assigned differently in 1955 and
1962, translated by ICEL in a copyrighted but web-permitted English, paired with
a public-domain Douay–Rheims reading in one UI mode and an externally syndicated
official reading in another. One "copyright" flag on a celebration must not
obscure any of that.

Where text is inherited from a Common or another Mass, encode the reference
explicitly. Do not manufacture an absence where the rite specifies a
cross-reference; model the reference.

Prefer:

```yaml
textual_basis:
  kind: public_domain_witness
  witness: { title: Missale Romanum, year: 1920, locator: ... }
  verification:
    - witness: roman-1962
      relationship: textually_identical
rights:
  basis: public_domain_underlying_work
  modern_edition_copied: false
  confidence: high
```

over `source: "1962 Missal"` / `copyright: "unknown"`.

A renderer must be able to answer **"why is this text allowed to appear here?"**
without a human reconstructing it from git history — and must be unable to
assert that a text is publishable which nobody has established is publishable.
Every rights token defaults to absent, and **absent renders as absent.**

Reuse the vocabularies that exist rather than inventing parallel ones. The
source library's `rights_status` already carries an unused `permission` value —
the one the ICEL question needs. `mass-ordinary` already has the
notice-bearing publishable state and its enforcement. The reader already has a
two-axis availability model with a state-to-reason constraint table that is
finer than a flat list of labels, and it already forbids reaching an assertion of
liturgical absence from a data problem. Do not flatten it.

---

## 11. Attribution

Attribution is **generated from typed metadata**, not duplicated as free-text
notices that drift.

ICEL's current page distinguishes an entire work from excerpts. The entire-work
form is:

> The English translation of *The Roman Missal* © 2010, International Commission
> on English in the Liturgy Corporation. All rights reserved.

This corpus presents selected propers and Ordinary elements, not the entire
work. The required excerpt form for that use is:

> Excerpts from the English translation of *The Roman Missal* © 2010,
> International Commission on English in the Liturgy Corporation. All rights
> reserved.

For multiple works, follow ICEL's current prescribed wording at `copyright.htm`
rather than inventing our own. Do not substitute `(c)` for `©`, copy a stale
notice from an intermediary, or use the entire-work form for an excerpt.
**Condition (2) fixes the display boundary**: the acknowledgement must appear on
the first and last pages or frames within the site displaying the ICEL text.
Attribution required at a boundary must not be buried, and any acknowledgement
placed by generated metadata rather than in the page body must not inherit a
stale origin.

Attribution and text must not separate in transit. The renderer can emit an
acknowledgement beside every covered text, and the structure tools refuse a
notice-bearing witness without one. Those checks are necessary on an eligible
surface but do not clear an ineligible bundled corpus. While ICEL payloads are
quarantined, retain the corrected excerpt acknowledgement as text-free metadata
for a future non-bundled display route.

Attribution is an **obligation attached to a basis**, never an alternative to
one: a text can be public-domain *and* attributed. Do not model it as an
availability state.

Never imply ICEL, USCCB or Vatican endorsement. §7.2.

---

## 12. Prohibited shortcuts

- **No hallucinated liturgical text.** An LLM may locate candidate witnesses,
  compare strings, identify likely duplicates, generate audit tooling and
  explain differences. **It may never be treated as a textual authority.** Every
  published liturgical text resolves to a source and witness chain.
- **No model in the retrieval path.** `sources.md` governs and its reason is
  demonstrated in-tree: a model route returned a paraphrase of one father under
  another father's name, from the same host under the same instruction that
  returned an exact text. Use a fetcher that retains and hashes whole byte
  streams; use a model only to characterise a page, never to acquire text.
- **No unofficial sources for current English.** Not blogs, not unofficial
  missal sites, not scraped parish or seminary PDFs, not OCR without
  verification against page images, not AI reconstruction.
- **No unauthorised whole-book scans as an exemplar.** An Internet Archive
  upload of the 2011 Missal exists and is retrievable. It fails on the
  **authority of the copy**: uploaded by a private individual, no licence, a
  re-uploader supplying metadata for a scan they did not make of a book they do
  not own. "Authoritative" is a property of the publisher of the copy, not only
  of the text inside it. ICEL's permission to reproduce ICEL's text is not a
  warrant to source that text from an unauthorised reproduction of a whole book
  whose front matter carries two other bodies' express prohibitions. The
  repository has already ruled on this twice, in
  `missal-acquisition-audit-v1.toml` and `lt-hist-rights-audit-v1.toml`;
  reversing it is the maintainer's decision and belongs in a rights record.
- **No unpromulgated text.** Green Book, Gray Book, provisional section texts,
  and the 1998 *Sacramentary* the Holy See declined to confirm are outside
  ICEL's grant, which reaches promulgated texts only.
- **No silent normalization of liturgical content.** Unicode normalization,
  internal identifiers, whitespace outside significant content, line-structure
  metadata and parser markup cleanup are safe. Punctuation, capitalization,
  spelling, diacritics, sacred names, versicle and response markers,
  liturgically meaningful paragraph boundaries, rubric wording, optional-text
  brackets, chant punctuation and **sense lines** are not. Where witnesses
  differ only orthographically, keep a canonical transcription and record the
  decision.
- **No claim broader than the evidence.** Do not write "we own this", "this is
  public domain", "permission is not required", "this text is absent", "the
  Vatican cannot copyright this", or "ICEL allows all liturgical text online".
  Write the narrower true proposition instead. Precision is more permissive than
  vague fear, because it lets us publish what is actually allowed.
- **No paid or credentialed access.** `sources.md` governs. An exact,
  authoritative, complete printed Missal exists and costs about a hundred
  dollars; no agent may purchase one or ask the maintainer to. If the maintainer
  already owns a copy, declaring it as a witness is his to do.

---

## 13. Procedure: importing a new corpus

Before any text is written to a tracked file:

1. **Identify the work, the edition, the artifact and the language** without
   conflating them. `sources.md` governs.
2. **Retrieve the whole document**, never a fragment where the whole is
   pullable; hash it; declare the bound exactly if the whole genuinely cannot be
   had.
3. **Determine the actual copyright owner per text**, not per book. Is it ICEL
   universal text? a USCCB national adaptation or U.S. proper? CCD Scripture? a
   fourth party. **Scripture inside a proper is a citation, not a text to
   acquire**: an antiphon carries its own words and its scriptural constituents
   as references, and those resolve against the bible the reader selected. That
   is why the Revised Grail rendering of three psalms, named in the 2011 book
   and in ICEL's Antiphonary, blocks nothing — this project never wants a
   particular publisher's psalm wording, only the reference.
4. **Name the basis** from §1's seven, and record it as a token, not prose.
   Where the basis is a permission, record the policy URL and its retrieval date
   beside the artifact's own source URL: they are different URLs and condition
   (5) makes re-verification necessary.
5. **Decide the surface**, not just the text. Site display, corpus data, Git
   distribution and PDF are four different acts. §3.4. If the text may be
   displayed and not bundled, the model must be able to say so and the pipeline
   must enforce it, before the text lands.
6. **Check the outbound licence.** Anything not project-created needs its
   `THIRD_PARTY.md` entry and its file-level marker, or `LICENSE` will offer it
   under CC BY 4.0.
7. **Establish exactness.** Test the corpus output against an authoritative
   exemplar. Where a permission requires exact reproduction and sense lines, the
   schema must be able to carry them.
8. **Verify the publication path renders it**, with its acknowledgment, before
   declaring the import done. A text admitted under a basis no filter accepts
   lands and does not render, and nobody can tell that silence from a decision.
9. **Record the absence honestly** for every slot the import did not fill, with
   a typed reason. Never turn malformed data into a claim that the rite omits
   something.

---

## 14. Procedure: an unresolved rights question

1. **Do not stop the lane.** One blocked text does not block a missal. Continue
   every independent route.
2. **Record the state as unresolved**, distinct from restricted and distinct
   from absent. `unresolved` is a question addressed to the maintainer; writing
   it as a settled disposition would be answering it.
3. **Settle a recurring question once, in a rights record** under
   `src/sources/inventories/`, with its citations, the routes examined and
   refused, and what would overturn it. A position stated only in prose, in
   three places, in three wordings, is three positions.
4. **State both sides of a real conflict** and say which governs and why, per §2.
   Do not smooth it.
5. **Before recommending a permission request**, show why each of these fails:
   public-domain underlying work; an existing express licence; an existing
   project permission; authorized syndication; an independently sourced earlier
   witness; another lawful text option. §4 is the worked example, and its
   conclusion was that the request needed is not a licence at all.
6. **Narrow the request.** Never "may we reproduce the Roman Missal" — that
   invites a broad denial. Name the rightsholder, work, specific text set,
   language, edition, planned use, noncommercial and web-only status, whether
   downloadable, whether for celebration or study, and the exact requested scope.
7. **Only the maintainer sends it.** A request is a representation about who is
   asking and what they will do. No agent may make one.

---

## 15. What this supersedes, and what still stands

### 15.0 Claims this page itself made and had to withdraw

A guidance page is a set of assertions, and an assertion that was true when
written and is false now fails in the way this project's own `the-shape.md`
calls the governing defect: it resolves, plausibly and wrongly. Nothing detects
that mechanically. So the withdrawals are kept here with their dates, and the
wrong wording is quoted rather than quietly replaced, because a reader who finds
only the corrected claim learns nothing about how the error was reached.

| Withdrawn | This page had said | What is true | Corrected |
| --- | --- | --- | --- |
| ICEL publishes no exemplar | "its own site has seven pages, catalogues the books it has translated, and offers no text and no download" | ICEL's News page links an open music folder, and the ICEL Antiphonary is published free and entire. These are authoritative exemplar leads; coverage must be measured against the current corpus rather than copied from this dated audit. | 2026-08-21, §4 |
| The Grail makes the rights unit smaller than a slot | "the unit of rights is therefore smaller than the slot, and this repository types rights per proper, which cannot express it. Until it can, no Palm Sunday antiphon may land" | A psalm inside a proper is a CITATION, not a text to acquire. An antiphon is `source: mixed`: its own words as `text`, its scriptural constituents as `verses`, resolved at render time against the reader's chosen bible. The 1962 calendar has done this since before the objection was written. No slot is blocked. | 2026-08-21, §5.1 |
| The postconciliar Latin is refused entire | carried in the data rather than this page: one `editio-typica` absence asserted a rights refusal over all 48 elements of the Order of Mass | True of 12. The other 36 are twelve slots holding no words, eight modelled too coarsely to source, and sixteen ancient texts no rightsholder has refused. Now six typed keys. | 2026-08-21 |
| The postconciliar English is wholly this project's own | carried in `THIRD_PARTY.md` and `liturgical-english-rights-v1.toml` | Public-domain 1861 Cummiskey English is also carried for antecedent prayers; derive current coverage from the inventory. | 2026-08-20 |

**Who found them matters more than the list.** Three of the four were overturned
by the maintainer, not by a tool or a review: he said the text is online
everywhere, and he said the psalms are the psalms. A page like this one is
written from what its author could reach, and its most consequential errors will
usually be the ones only somebody who knows the subject can see. Contradiction
from such a reader is the intended failure path, not an interruption of it.

### 15.1 The root cause, in the repository's own record

The repository knew its evidence was incomplete and said so. The ICEL passage
record at
`src/sources/works/international-commission-on-english-in-the-liturgy/publication-policies/editions/web-2026-08-01/passages/permissions-and-royalties.toml`
reads:

> A summary page. It links a fuller booklet of Publication Policies **which this
> project has not retrieved**, so nothing here is a complete statement of ICEL's
> terms.

That un-retrieved booklet is the PDF whose p. 25 carries the grant at §3.1. The
gap was recorded honestly and then a downstream inventory hardened it into a
blanket absence reason. **No schema change fixes this
and no schema change caused it.** It was a sourcing gap, and it is why §13 step
2 is retrieve-the-whole and why §3.2 records the trap by name.

That prerequisite is now closed. The 2013-amended PDF edition, its artifact,
hash, and focused passages are registered under
`src/sources/works/international-commission-on-english-in-the-liturgy/publication-policies/`.

### 15.2 Statements this policy replaces

**Do not edit these as a side effect of reading this file.** They are listed for
the coordinator, and each needs its own owning lane.

| File | What it said before the owning correction | Disposition |
| --- | --- | --- |
| `src/sources/inventories/liturgical-english-rights-v1.toml` | `holding`: "The approved English of the postconciliar Roman Missal may not be published here". `[the_icel_translation]`: "May the approved English be reproduced? — Not without a licence, which this project does not have", reasoned from `copyright.htm` and `whatis.htm` and from the royalty schedule. `[seeking_a_licence]` written on the premise that a written grant is required. | **Superseded on the permission.** It never reaches the Global Computer Networks clause, because the document carrying that clause is the one the library did not retrieve. Rewrite the ICEL section against §3, and record exemplar and surface limits separately under §4. |
| `src/sources/inventories/postconciliar-ordo-missae-v1.toml` | `advisory`: "the approved English is the International Commission on English in the Liturgy's and this project has no licence to reproduce it"; a broad `absences.icel` classification. | **Superseded as a rights statement.** The absence of a licence is not a sufficient reason; classify exactness, provenance, rightsholder, and publication surface separately. The `editio-typica` absence key is a separate question and §8.1 governs it. |
| `src/sources/inventories/postconciliar-proper-translations-v1.toml` | Header: the Missale Romanum 2002 "is in copyright and not held here", and the file "publishes no English of the Missale Romanum 2002 by any route". | **Still true as written**, and its two routes stand (§15.3). What changes is that a third route is now permitted in principle and blocked in fact; the header should say which. |
| `guidance/the-shape.md` §4 | `absent: icel` glossed as "a postconciliar text two bodies have not agreed this project may publish", pointing at `missals.md`'s conflict finding. | **Superseded.** The gloss was already a correction of an earlier, falser one ("a text nobody may publish"). It is now wrong in the other direction: ICEL has granted a conditional live-web use. A current absence must name the actual blocker — exemplar/exactness, another rightsholder, territory/version, or a bundled surface outside that permission. Replace the example's reason, not the principle. |
| `guidance/missals.md` §5 and `src/sources/inventories/missal-acquisition-audit-v1.toml` correction `icel-internet-clause` | Quote the ICEL clause against the USCCB's *Policy on Electronic Copyrights* and record a conflict "recorded, not applied", reserving the resolution to the maintainer: "`absent: icel` remains the right operational default". | **Resolved, on the maintainer's direction.** §2 governs the conflict and §6 states the resolution and its limits. Mark the correction applied and cite this page. The audit's reservation was correct procedure at the time and should be recorded as having been answered, not as having been wrong. |
| `guidance/liturgy/postconciliar-propers.md` | "The ICEL English of the Roman Missal and the Lectionary text are under copyright and are never reproduced." | **Split.** The Lectionary half stands (§5.3). The ICEL half is superseded on the permission; current nonreproduction may still follow from an unverified exemplar or version and independently follows for a bundled/downloadable surface outside the standing permission. The profile's working rules remain correct for the published guides unless an eligible surface and exact text are both established. |
| `guidance/sources.md`, "Settle a recurring rights question once" | Cites `liturgical-english-rights-v1.toml` as the file that "settles whether the English of the postconciliar Roman Missal may be published here". | **Pointer only.** The rule stands unchanged; the file it names needs the rewrite above. Add this page beside it as the governing presumption. |
| the published Order of Mass exposition and comparative studies under `src/claude/…` and `web/claude/…` | Scope records stating the approved English is not reproduced. | **Unchanged for those documents.** A PDF is a publication in another form and outside ICEL condition (4). §3.4. Do not read this policy as opening the installed PDFs. |

### 15.3 What still stands, unchanged

- **The antecedent route and the project-created route** in
  `postconciliar-proper-translations-v1.toml`, and everything
  `liturgical-english-rights-v1.toml` says about them, `[the_latin]`,
  `[public_celebration]`, and `[the_1973_translation]`. Nothing found disturbs
  those findings. `[the_ellc_grant]` remains evidence of the grant and its
  notice conditions, not evidence that an ELLC payload is present or cleared
  for every surface: the current assembled and source-Git tree quarantines the
  text and asserts no current ELLC display. Apply the same text-versus-grant and
  surface analysis to `[other_freely_granted_corpora]` rather than inheriting a
  blanket conclusion.
- **The refusal of the mechanical similarity route.** Four of 215 postconciliar
  orations word-for-word identical to a 1962 formulary and ten more at 0.95 is
  not an identity, and no coverage figure licenses a transfer.
- **The CCD, NAB, LFM and *Abbey Psalms* restrictions.** §5.3.
- **`sources.md` in its entirety** — whole-document retrieval, alias
  resolution, no model in the retrieval path, per-artifact rights, the four
  storage dispositions, the publicly-reachable-only rule, the rights-record
  genre.
- **`the-shape.md` §4's principle** that absence is data and carries a reason.
- **The reader's two-axis availability model** and its state-to-reason
  constraint table, which are finer than a flat label list and must not be
  flattened into one.
- **`guidance/missals.md` §5's Latin rights findings** — the pre-1931 line, the
  1935 Berne date, the altar book's own APSA claim, Vatican Law N. CXCVII, and
  URAA restoration. §8.1 adds PSP above them; it displaces none of them.

---

## 16. Sources, with retrieval dates

Initial retrievals were 2026-08-20 unless stated. ICEL's grant and
acknowledgement page and the USCCB guidelines landing page were fetched again
whole on 2026-08-26; their hashes below are from those bytes.

**ICEL**

| Source | URL | State |
| --- | --- | --- |
| *Publication Policies*, p. 25 — the grant | `https://www.icelweb.org/PubPolicy.PDF` | registered; re-fetched 2026-08-26; sha256 `e2ec59f7d46f0673f40239a1185c7005f955959e0cb5eeb40e5daa55f2a254e7` |
| Copyright summary — the acknowledgement wording, **not** the grant | `https://www.icelweb.org/copyright.htm` | re-fetched 2026-08-26; sha256 `8327fb75a0aaa9740b51216b1162a1f32a98f3cd9c7c9a47ef951e1c692e08e8` |
| ICEL Copyrighted Materials — the ownership inventory | `https://www.icelweb.org/copyrightICEL.htm` | retrieved |
| Sections of *The Roman Missal* | `https://www.icelweb.org/RomanMissal.htm` | retrieved |

**USCCB**

| Source | URL | State |
| --- | --- | --- |
| *Guidelines for the Publication of Liturgical Books* (HTML) | `https://www.usccb.org/committees/divine-worship/policies/guidelines-for-the-publication-of-liturgical-books` | re-fetched 2026-08-26; sha256 `916a4e98994e7f0faba08a1a2dfc763ae9fa73e292fb219c9653aa0daa8c36e7` |
| The same, full text, 51 pp. | `https://www.usccb.org/resources/guidelines-publication-liturgical-books.pdf` | retrieved; sha256 `daab2999…` |
| 2025 guidelines resource page (HTML wrapper) | `https://www.usccb.org/resources/guidelines-publication-liturgical-books` | **HTTP 403**, six attempts; a bot interstitial, not a withdrawal. Nothing rests on it |
| *Copyright Permission Requirements for the Use of Liturgical Texts* (2021) | `https://www.usccb.org/committees/divine-worship/policies/copyright-permissions-requirements` | retrieved — §6 |
| *Policy on Electronic Copyrights* | `https://www.usccb.org/committees/divine-worship/policies` | re-read at source — §6 |
| Authorized RSS feeds | `https://www.usccb.org/subscribe/rss` | retrieved — §9 |
| CCD/NAB permissions | `https://www.usccb.org/offices/new-american-bible/permissions` | still **HTTP 403** to direct whole-document retrieval on 2026-08-26. **Unverified; do not quote.** §5.3 |

**An intermittent infrastructure problem, not a rights problem.** `usccb.org`
still returns a proof-of-work HTTP 403 on some paths, including the CCD/NAB
permissions page, while the guidelines landing page can now be fetched whole.
Treat reachability per URL and per retrieval; an indexed or model-rendered view
does not satisfy `sources.md`'s source-text retrieval rule.

**Holy See**

| Source | URL | State |
| --- | --- | --- |
| CDWDS, *Postquam Summus Pontifex*, 22 Oct 2021 | `https://press.vatican.va/content/salastampa/en/bollettino/pubblico/2021/10/22/211022b.pdf` | retrieved; sha256 `9fd22cb8…`; **not registered in this repository** — §8.1 |
| *Liturgiam authenticam* nn. 110, 111, 117 | `https://www.vatican.va/roman_curia/congregations/ccdds/documents/rc_con_ccdds_doc_20010507_il_en.html` | held as a verified passage record, verified 2026-08-01 |
| Secretariat of State, Decree, 13 May 2005: AAS 97 (2005) 798-799 | — | **not retrieved.** PSP's own cited authority — §8.1 |

**Candidate exemplar sources** (§4; reachability only, contents unopened)

| Source | URL | State |
| --- | --- | --- |
| CBCEW Liturgy Office — Order of Mass and Eucharistic Prayers, 20 free PDFs | `https://www.liturgyoffice.org.uk/Missal/Text/index.shtml` | HTTP 200 |
| CBCEW Liturgy Office — Holy Week and Triduum excerpts, 5 free PDFs | `https://www.liturgyoffice.org.uk/Missal/Text/Triduum.shtml` | HTTP 200 |

The CBCEW pages carry "© CBCEW" and a bounded grant for local parish reproduction
that does **not** cover a permanent website. That grant governs the PDFs as
CBCEW's typographical works; the ICEL text inside them is governed by §3. **Two
layers, two rights records; conflating them would be an error.**

---

## 17. In one paragraph

ICEL grants, in its own published policy, the reproduction of its approved,
recognised and promulgated texts on a free non-commercial website, subject to six
conditions — and its summary page does not say so, which is how this project came
to believe otherwise. The grant is established but supplies no text and does not
cover the public repository's bundled, downloadable corpus. Latin,
ICEL English, USCCB adaptations and CCD Scripture are four different properties
that happen to be bound between the same covers, and the last two are under
affirmative written-permission restrictions that this policy does not touch. The
ancient Latin underneath a modern edition is still ancient. Which passage is
appointed is a fact; the passage's words are somebody's property. And a
permission is decided per text and per surface: what might be displayed by a
future eligible route is not thereby a file a reader may download or a corpus
the world may clone. The current public route quarantines ICEL payloads and
retains only text-free rights, source, and acknowledgement metadata.
