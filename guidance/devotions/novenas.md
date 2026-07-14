# Novena Pious Exercises

This profile governs the numbered novena collection beneath `src/gpt/devotions/novenas/`. A novena is a sustained pious exercise ordered to persevering Christian prayer over nine days or another historically identified ninefold observance. It is not automatically a liturgical celebration, an approved public text, a sacrament, a sacramental, a private revelation, or a mechanism that compels a requested result. Novena documents must lead toward Scripture, the sacred liturgy, the sacraments, conversion, ecclesial communion, and concrete charity while preserving the superiority and proper integrity of the liturgy.

Publishable leaves use `src/gpt/devotions/novenas/<numbered-document>/`; build and installed PDFs mirror them beneath `build/gpt/` and `doc/gpt/`. Internal ordering keys use `N00`, `N10`, `N20`, and so forth so later additions can be inserted without renumbering source leaves; `N00` is reserved for the Ascension-to-Pentecost archetype. These keys govern repository ordering, internal research references, and catalog row order only. They are not publication identities: do not print them on a title page, heading, appendix, running element, PDF metadata field, or other reader-facing prose, and list novenas in the public README without an identifier column. Internal scope, audit, and control records may retain the key needed to identify their source leaf. A shared source beneath `src/gpt/devotions/novenas/shared/` is non-publishable and must have one textual owner, explicit consumers, and build dependencies that rebuild every novena after a shared change.

## Doctrinal and liturgical boundaries

Every novena must identify its addressee correctly. Prayer is offered to the triune God, to a divine Person, or through Christ; Mary, angels, and saints are invoked for subordinate intercession, never treated as independent divinities, sources of grace, or powers that override divine wisdom. A promise attached to a devotion cannot guarantee salvation, healing, a particular temporal outcome, or exemption from repentance and the ordinary means of grace.

The document must distinguish:

- the one saving mystery and its liturgical celebration;
- a public or private pious exercise ordered toward that celebration;
- a prayer text approved for a specified use;
- a historically received but non-liturgical prayer;
- a project-composed prayer or meditation; and
- any private-revelation tradition, whose exact judgment and nonbinding scope must be stated.

Do not splice devotional material into Mass or the Liturgy of the Hours, call a booklet “the Church's official novena” without a controlling act, or imply that private recitation reproduces a liturgical office. Where the Directory on Popular Piety recommends Vespers, another office, Mass, Scripture, or sacramental participation, the guide must say so plainly and present its own order as a subordinate option.

## Required records

Each novena leaf imports exactly one `generation-metadata.tex` record and keeps:

- `research/scope.md`, identifying provider, collection, stable ID, reader, thesis, included and excluded material, doctrinal and liturgical boundaries, calendar or jurisdiction variables, currentness, consequential uncertainties, and review state;
- `research/source-audit.md`, mapping material historical, doctrinal, liturgical, hagiographical, private-revelation, indulgence, and pastoral claims to exact sources and loci; and
- `research/prayer-inventory.md`, listing every vocal prayer printed for recitation, its Latin or Greek witness, textual status and date where known, English translation ownership, approval or liturgical status, source locus, and any editorial adaptation.

If a novena depends on a claimed apparition, promise, vision, or locution, add a controlling status record or link to the repository-owned Mariological dossier that defines the exact competent act and object judged. Approval of a saint, title, feast, shrine, scapular, confraternity, or prayer does not authenticate every origin narrative or promise.

## Prayer and translation standard

Every vocal prayer printed for recitation in English must appear with its complete Latin or Greek source text adjacent to it. This includes common prayers, daily collects, hymns, litanic responses, acts of offering, and concluding prayers. Prose instructions, historical exposition, scriptural citations, examination questions, and non-vocal meditation are not prayers and need not be duplicated in Latin or Greek.

Use an identified historic, liturgical, or otherwise received Latin or Greek witness wherever one is fit for the devotion. If the project composes or materially adapts a prayer, its Latin or Greek form is the canonical project text, the English is labeled a project translation, and neither may be represented as ancient, liturgical, indulgenced, or ecclesiastically approved. Obtain specialist review before calling an original Latin or Greek composition idiomatic or publication-final.

English prayer should be faithful, speakable, and literary: concrete images, balanced cadence, and dignified vocabulary are preferred to bureaucratic paraphrase. Poetry must not add a promise, title, causal claim, or doctrinal content absent from the source. Preserve biblical allusion, Trinitarian grammar, the conclusion of a collect, and distinctions among worship, intercession, petition, praise, thanksgiving, and reparation. Identify whether an English rendering is official, public domain, licensed, or a project translation; do not silently modernize a copyrighted translation.

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
5. nine visibly distinct days, each with a scriptural center, source-grounded meditation, concrete examination or act, proper intention, and unique bilingual prayer;
6. the principal received hymns, antiphons, litanies, or feast prayers used by the guide, in their complete bilingual form; and
7. references and an appendix or one-page annual-use table when it materially improves practice.

Daily meditations must develop rather than paraphrase one another. They should connect doctrine to repentance, virtue, vocation, works of mercy, ecclesial unity, or mission. They may invite prudent fasting, almsgiving, confession, spiritual reading, or service, but they may not impose obligations, discourage medical or psychological care, substitute private counsel for safeguarding or justice, or use suffering to keep a reader in danger.

A repeated daily orientation panel whose internal fields already name the scriptural center, grace sought, and concrete act uses an untitled frame. Do not add a generic wrapper such as `The day's axis`; the day heading, typography, and field labels already establish the relationship. Titles for examinations, prayers, approval notices, or other materially different functions remain visible when they aid use or prevent confusion.

## Current discipline, approval, and indulgences

Approval claims must name the competent authority, act, date, exact object, and jurisdiction. An imprimatur concerns freedom from doctrinal error in the submitted text; it is not proof of an origin legend or guarantee of spiritual efficacy. A repository-authored novena without ecclesiastical review must say so.

Indulgence claims are mutable. Identify the edition of the `Enchiridion Indulgentiarum`, concession and general norms, public or private condition, required approved text where applicable, and as-of date. Do not perpetuate superseded day-and-quarantine measures, apply an indulgence attached to another text or circumstance, or imply that completing the repository's booklet automatically fulfills every condition.

## Completion gate

A novena is ready to install only when:

- its object, status, historical development, ninefold rationale, calendar rule, and principal annual placement are exact;
- liturgy, pious exercise, approved prayer, received tradition, private revelation, and project composition remain distinct;
- every recited English prayer has the complete adjacent Latin or Greek source and a recorded translation status;
- every day contains a genuinely distinct biblical center, meditation, intention, act, and proper prayer;
- claims about approval, promises, scapulars, apparitions, healings, and indulgences are authority-bounded and current;
- the common prayer order is complete, practical, and not needlessly duplicated;
- all shared-source consumers have been rebuilt and reviewed after a shared change;
- source scope, prayer inventory, source audit, copyright review, and AI metadata are complete;
- multi-pass build, log scan, every-page visual inspection, PDF metadata and font checks, and installed/build identity checks pass; and
- the catalog states source and production maturity separately from independent theological, liturgical, linguistic, historical, or ecclesiastical review.
