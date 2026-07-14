# Novena Pious Exercises

This profile governs the numbered novena collection beneath `src/gpt/devotions/novenas/`. A novena is a sustained pious exercise ordered to persevering Christian prayer over nine days or another historically identified ninefold observance. It is not automatically a liturgical celebration, an approved public text, a sacrament, a sacramental, a private revelation, or a mechanism that compels a requested result. Novena documents must lead toward Scripture, the sacred liturgy, the sacraments, conversion, ecclesial communion, and concrete charity while preserving the superiority and proper integrity of the liturgy.

Publishable leaves use `src/gpt/devotions/novenas/<numbered-document>/`; build and installed PDFs mirror them beneath `build/gpt/` and `doc/gpt/`. Internal ordering keys use `N00`, `N10`, `N20`, and so forth so later additions can be inserted without renumbering source leaves; `N00` is reserved for the Ascension-to-Pentecost archetype. These keys govern repository ordering, internal research references, and catalog order only. They are not publication identities: do not print them on a title page, heading, appendix, running element, PDF metadata field, or other reader-facing prose. On the public Prayer page, list each full guide and its condensed companion in one table row, put the companion link in the `Short form` column, and omit the internal identifier. Internal scope, audit, and control records may retain the key needed to identify their source leaf. A shared source beneath `src/gpt/devotions/novenas/shared/` is non-publishable and must have one textual owner, explicit consumers, and build dependencies that rebuild every novena after a shared change.

## Condensed recitation companions

A full novena may have one parallel condensed companion at the sibling leaf `<numbered-document>-daily-prayer/`. The companion is a prayer-book view of the canonical full guide, not a second edition with its own prayer text or theological synthesis. Its reader has already read the full guide or uses both publications together.

The full guide remains the sole textual owner. Put every common prayer, proper collect, hymn, sequence, or other recited text used by both publications in a canonical fragment beneath the full guide, and import that same fragment into both consumers. Do not copy a prayer into the companion, silently shorten it, modernize its translation, or let the two publications drift. Register the cross-document dependencies in the build so a canonical prayer change rebuilds the full guide and its companion.

A condensed companion contains only:

- a title and explicit companion relationship;
- a concise recitation sequence and the minimum rubrics needed to execute it safely;
- every common vocal prayer appointed by the full guide, printed once;
- the nine proper prayers under clearly navigable day headings;
- any prayer appointed only on a particular day, in full; and
- a compact status notice that sends calendar, Scripture, meditation, examination, concrete act, history, doctrine, approval, and translation questions back to the canonical full guide.

It does not reproduce the full guide's exposition, meditation, examination, pastoral applications, historical claims, source notes, calendar essay, or references. Omitting these materials for a reader who already knows them does not make the vocal order a substitute for the source guide's Scripture, silence, conversion, sacramental, liturgical, or charitable orientation.

Because the companion is mechanically assembled from canonical prayer fragments and fixed navigation or status rubrics, it imports one `\AIInheritedGenerationMetadata` declaration naming the full guide and displays no second provenance block. It keeps `research/derivation.md`, mapping every rendered prayer and rubric to its canonical owner and recording comparison, build, and review results. It does not duplicate the full guide's scope, prayer inventory, or source audit; the public catalog must link the companion to those controlling records and state the inherited relationship explicitly.

## Doctrinal and liturgical boundaries

Every novena must identify its addressee correctly. Prayer is offered to the triune God, to a divine Person, or through Christ; Mary, angels, and saints are invoked for subordinate intercession, never treated as independent divinities, sources of grace, or powers that override divine wisdom. A promise attached to a devotion cannot guarantee salvation, healing, a particular temporal outcome, or exemption from repentance and the ordinary means of grace.

The document must distinguish:

- the one saving mystery and its liturgical celebration;
- a public or private pious exercise ordered toward that celebration;
- a prayer text approved for a specified use;
- a historically received but non-liturgical prayer;
- a project-composed meditation or other non-vocal editorial material; and
- any private-revelation tradition, whose exact judgment and nonbinding scope must be stated.

Do not splice devotional material into Mass or the Liturgy of the Hours, call a booklet “the Church's official novena” without a controlling act, or imply that private recitation reproduces a liturgical office. Where the Directory on Popular Piety recommends Vespers, another office, Mass, Scripture, or sacramental participation, the guide must say so plainly and present its own order as a subordinate option.

## Required records

Each novena leaf imports exactly one `generation-metadata.tex` record and keeps:

- `research/scope.md`, identifying provider, collection, stable ID, reader, thesis, included and excluded material, doctrinal and liturgical boundaries, calendar or jurisdiction variables, currentness, consequential uncertainties, and review state;
- `research/source-audit.md`, mapping material historical, doctrinal, liturgical, hagiographical, private-revelation, indulgence, and pastoral claims to exact sources and loci; and
- `research/prayer-inventory.md`, listing every vocal prayer printed for recitation, its Latin or Greek witness, textual status and date where known, exact English witness and ownership, approval or liturgical status, source locus, rights basis, and any mechanical expansion of an explicit source abbreviation.

The mechanically derived condensed-companion exception uses the inherited metadata and derivation record defined above; its canonical full guide owns and supplies the three substantive research records.

If a novena depends on a claimed apparition, promise, vision, or locution, add a controlling status record or link to the repository-owned Mariological dossier that defines the exact competent act and object judged. Approval of a saint, title, feast, shrine, scapular, confraternity, or prayer does not authenticate every origin narrative or promise.

## Prayer and translation standard

Every vocal prayer printed for recitation in English must appear with its complete Latin or Greek source text adjacent to it. This includes common prayers, daily collects, hymns, litanic responses, acts of offering, and concluding prayers. Prose instructions, historical exposition, scriptural citations, examination questions, and non-vocal meditation are not prayers and need not be duplicated in Latin or Greek.

Use only identified historical, approved, liturgical, or otherwise received prayer texts. Neither the project nor an AI contributor may compose, translate, paraphrase, modernize, conflate, or materially adapt a vocal prayer. Reproduce each source-language prayer and exact identified human translation without verbal alteration; if no suitable translation can be verified and lawfully reproduced, omit the English recited text until one can. Expand an explicit abbreviation only with the exact full formula printed by the same identified witness or by a governing liturgical edition that the source explicitly incorporates; record both loci and the basis of the connection.

Select an exact received English witness whose status and rights permit the intended use. Record whether it is official, historically approved, public domain, licensed, or reproduced under another identified basis. Do not silently modernize even a public-domain translation, and do not alter poetry, biblical allusion, Trinitarian grammar, a collect's conclusion, or distinctions among worship, intercession, petition, praise, thanksgiving, and reparation.

Print a recurring common prayer once and direct the reader to it; do not multiply identical texts merely to fill nine daily sections. Typography may distinguish Latin witness, English translation, rubric, source note, and editorial meditation without repeating a prose “boundary” label on every page.

A recurring bilingual prayer card uses the prayer's name as its content-bearing title and gives each internal field a stable visible identifier: `Text and status`, the actual source language (`Latin` or `Greek`), and `English`. The first field states textual provenance, approval or liturgical status, and translation ownership as applicable; do not leave it as an unlabeled italic line. If a card adds another genuinely distinct field, label that field too rather than relying on position or type style.

## Historical and calendar discipline

A document explains why its observance is ninefold, when the particular devotion arose, how its text developed, what authority commended or approved it, and which origin claims remain late, legendary, disputed, or unverified. Biblical ninefold patterns may ground a theology of persevering prayer without proving that a later fixed booklet existed in apostolic times.

Give a reproducible calendar rule:

- name the feast or event to which the novena is ordered;
- state whether day one begins nine calendar days before the feast, on the day after an initiating feast, or by another received reckoning;
- give at least one dated worked example;
- account for a transferred feast, impeded celebration, local calendar, Eastern calendar, or other material jurisdictional difference; and
- distinguish a devotional choice from a liturgical transfer or canonical obligation.

When a novena may be prayed at any time, say so without erasing its principal annual placement. Missing a day does not make prayer worthless or authorize superstition; give a sober pastoral option for resuming or beginning again without inventing a legal rule.

## Daily architecture

A full nine-day guide normally contains:

1. a compact identity, status, and calendar guide;
2. biblical and historical provenance;
3. doctrinal exposition of the devotion's object;
4. one common order naming exactly what is prayed every day;
5. nine visibly distinct days, each with a scriptural center, source-grounded meditation, concrete examination or act, proper intention, and unique received prayer, with an exact identified human translation when it may lawfully be reproduced;
6. the principal received hymns, antiphons, litanies, or feast prayers used by the guide, complete in the source language and accompanied by exact identified human translations where they may lawfully be reproduced; and
7. references and an appendix or one-page annual-use table when it materially improves practice.

Its condensed companion instead gives one complete common vocal order, nine day headings with their canonical proper prayers, and any day-specific added or substituted prayer. Common texts remain printed once and are referenced by name from the daily sequence; “condensed” never authorizes an abridged prayer.

Daily meditations must develop rather than paraphrase one another. They should connect doctrine to repentance, virtue, vocation, works of mercy, ecclesial unity, or mission. They may invite prudent fasting, almsgiving, confession, spiritual reading, or service, but they may not impose obligations, discourage medical or psychological care, substitute private counsel for safeguarding or justice, or use suffering to keep a reader in danger.

A repeated daily orientation panel whose internal fields already name the scriptural center, grace sought, and concrete act uses an untitled frame. Do not add a generic wrapper such as `The day's axis`; the day heading, typography, and field labels already establish the relationship. Titles for examinations, prayers, approval notices, or other materially different functions remain visible when they aid use or prevent confusion.

## Current discipline, approval, and indulgences

Approval claims must name the competent authority, act, date, exact object, and jurisdiction. An imprimatur concerns freedom from doctrinal error in the submitted text; it is not proof of an origin legend or guarantee of spiritual efficacy. A repository-authored novena without ecclesiastical review must say so.

Indulgence claims are mutable. Identify the edition of the `Enchiridion Indulgentiarum`, concession and general norms, public or private condition, required approved text where applicable, and as-of date. Do not perpetuate superseded day-and-quarantine measures, apply an indulgence attached to another text or circumstance, or imply that completing the repository's booklet automatically fulfills every condition.

## Completion gate

A novena is ready to install only when:

- its object, status, historical development, ninefold rationale, calendar rule, and principal annual placement are exact;
- liturgy, pious exercise, approved prayer, received tradition, and private revelation remain distinct, with no project- or AI-authored prayer;
- every recited English prayer has the complete adjacent Latin or Greek source, an exact identified human translation witness, a recorded rights basis, and no editorial adaptation beyond a documented exact expansion of the source's explicit abbreviation from the same witness or an explicitly incorporated governing edition;
- every day contains a genuinely distinct biblical center, meditation, intention, act, and proper prayer;
- claims about approval, promises, scapulars, apparitions, healings, and indulgences are authority-bounded and current;
- the common prayer order is complete, practical, and not needlessly duplicated;
- all shared-source consumers have been rebuilt and reviewed after a shared change;
- source scope, prayer inventory, source audit, copyright review, and AI metadata are complete;
- multi-pass build, log scan, every-page visual inspection, PDF metadata and font checks, and installed/build identity checks pass; and
- the catalog states source and production maturity separately from independent theological, liturgical, linguistic, historical, or ecclesiastical review.

For a condensed companion, also require:

- a one-to-one derivation map from every rendered prayer to a canonical fragment owned by the full guide;
- a check that the companion introduces no independent prayer, doctrinal, historical, calendar, approval, indulgence, or translation claim;
- exact text comparison between each canonical prayer fragment as rendered in the full guide and companion, allowing only layout-driven line wrapping;
- inherited-provenance validation with no duplicate visible metadata block;
- explicit build dependencies from every canonical prayer fragment to both consumers; and
- catalog placement immediately after the full guide with the controlling source, inventory, scope, audit, and derivation links.
