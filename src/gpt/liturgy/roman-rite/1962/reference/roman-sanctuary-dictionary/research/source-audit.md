# Source audit

Status: **initial gap audit with one narrow sacristy-furnishings pass**
Audit date: 2026-07-27

## What was audited

The initial pass audited the project contract, the pictorial-dictionary
profile, the new schema and selection declarations, and the current
publication scaffolding. A focused second pass on 2026-07-27 acquired and
inspected the publicly hosted introduction to the 2008 Vatican facsimile of
the *Pontificale Romanum* 1961--1962, and inspected two catalog records. It did
not acquire or inspect the three full liturgical volumes.

## Findings

- The declared corpus is far broader than the existing altar-server-guide
  evidence and cannot inherit verification from those guides.
- No owner `source-bindings.toml` or canonical source-library bindings yet
  support the dictionary inventory.
- No official corpus closure exists for pontifical functions, Holy Week,
  ritual Masses, or related ceremonies.
- No material-culture corpus establishes morphology, dimensions, substantive
  variants, or historical chronology.
- No lexical audit supports Latin headwords, aliases, or pronunciation.
- No claim-level source record supports symbolism.
- The schema correctly prevents `lead` and `held` records from appearing in
  derived editions, but no populated canonical records or validator presently
  demonstrate enforcement.

## Candle-tool material-culture control, 2026-07-28

The exact two-page facsimile of United States Letters Patent No. 717,186
(1902) was acquired, hashed, and checked at Figure 1 and the specification.
It establishes one dated combined family: a long supporting rod, taper tube,
and separate branch ending in an extinguisher bell. It is secular
material-culture evidence, not Catholic evidence or a ritual source. The
canonical record therefore makes no claim for Catholic prevalence, Roman
prescription, universal combined form, official terminology, dimensions,
ornament, handler, or operating method; the patented pneumatic mechanism is
excluded from the generic graphite synthesis.

## Focused Pontificale audit, 2026-07-27

Source inspected: Manlio Sodi and Alessandro Toniolo, introduction to
*Pontificale Romanum: Editio typica 1961--1962*, Monumenta Liturgica Piana 3
(Libreria Editrice Vaticana, 2008), pp. V--XIV, publicly hosted PDF. Exact
acquired identity and storage disposition are recorded in
`edition-manifest.md`.

Findings:

- The applicable Pontifical is a coordinated three-part 1961--1962 typical
  edition, not a single undifferentiated “1962 Pontifical.”
- Pars secunda is the 1961 *editio typica emendata*; Pars prima and Pars
  tertia et Appendix are the 1962 parts.
- The introduction's comparative contents directly identifies object-bearing
  rites and blessings for the pallium; church and altar consecration; portable
  altar; bell; chalice and paten; antimension; tabernacle, pyx, ostensorium,
  and *theca*; altar cloths, corporal, pall, purificator, and priestly
  vestments; crosses; images; reliquary cases; Holy Thursday oils and chrism;
  and several ceremony families.
- Those headings are now recorded as focused discovery evidence in
  `object-inventory.md`.

Evidence limits:

- The introduction is a scholarly finding aid, not the complete
  liturgical witness.
- No full rubric or prayer was checked. Therefore no presence, construction,
  handling, dimensions, required material, marking, symbolism, or complete-use
  claim has been verified from the Pontifical.
- The 1961 and 1962 decrees and the 2 January 1962 declaration are reported by
  the introduction but have not been collated with their complete official
  witnesses.
- Open Library and BeWeB corroborate the edition identity and library
  holdings; neither supplies a full-text witness.

## Evidence ceiling

Every proposed object remains an unverified lead unless a later record says
otherwise. The Pontifical's three-part edition identity and the existence of
the named rites in its comparative contents are inspected findings at the
bounded loci above; this does not promote any object record. Familiar terms,
current practice, retailer pages, museum captions, OCR, source snippets, and
generated images may guide search but may not support publication claims
without the required direct check.

## Research passes required

1. Resolve and bind exact official editions and promulgating acts.
2. Inventory named and presupposed objects by exact locus and ceremony.
3. Run a second terminology pass across Latin aliases, reforms, branches, and
   likely omissions before narrowing any category.
4. Add competent contemporary ceremonial sources for practical details,
   preserving disagreements and jurisdiction.
5. Build a provenanced material-culture corpus for construction and
   morphology.
6. Audit historical periods independently; do not infer ancestry or
   discontinuation from resemblance.
7. Bind every reader-facing claim and every artwork reference at its actual
   evidence ceiling.

## Consequential unresolved questions

- Exact boundaries among universal provision, condition, privilege, regional
  permission, religious-community practice, and local furnishing.
- Whether common English labels map one-to-one to Latin terms in the governing
  editions.
- Which forms are substantive variants rather than decoration.
- Exact transition evidence for items placed in the historical section.
- When an object belongs to Mass, an adjoining ceremony, or both.
- Which handling and safety claims are liturgical, practical, or local.

## Second Pontificale acquisition sweep, 2026-07-27

The second pass tested exact 1961/1962 and broad-title searches in Internet
Archive; Open Library and ecclesiastical library holdings; Google Books
catalog/preview routes; the 1999 CLV reprint; contemporary liturgical
periodicals; and official Vatican backward citations.

Two exact remote artifacts were acquired and inspected:

1. Pierre Jounel, “La nouvelle édition du Pontifical romain,” *La
   Maison-Dieu* 75 (1963), pp. 155--158. It is a near-contemporary,
   part-by-part survey of the newly issued book and directly distinguishes the
   portable altar from the simple altar stone or *tabula*.
2. Paul VI, *Inter eximia* (1978), official Vatican Latin HTML. Its opening
   paragraph identifies the pallium among episcopal-office insignia and cites
   Pars prima (1962), p. 92.

Their exact hashes, byte counts, URLs, storage dispositions, and evidence
ceilings are recorded in `edition-manifest.md`. No full typical-edition scan
was found. The bounded negative result is repository- and access-route
specific: it does not establish that no scan exists or that institutional
digital access is unavailable.

What the second pass changed:

- confirmed a defensible substantial contemporary overview beyond the 2008
  facsimile introduction;
- added an exact official backward citation for the pallium;
- added the portable-altar versus altar-stone distinction as a focused
  confusable-object lead;
- documented concrete full-volume access routes for future onsite or licensed
  consultation; and
- retained, rather than narrowed, the full Pontifical source gap because
  object-level rubrics remain uninspected.

## Publication state

Source-audited, independently reviewed, complete, approved, and release-ready
labels are prohibited at this stage.

## Initial vessel and cruet pass — 2026-07-27

Three canonical records now bind limited claims to evidence:

- `obj-chalice` and `obj-paten` use the 1962 *Missale Romanum*, *Ritus
  servandus* VII–XII, for their identity and ceremonial use. The existing
  checked passage record and altar-server source audit distinguish the
  priest's paten from the Communion plate.
- `obj-altar-cruet` combines the Missal's wine-and-water Offertory and
  ablution requirements with the checked altar-server-guide synthesis for the
  practical two-cruet service.

This pass does **not** verify a universal ornamental form, precise dimensions,
materials, or the cruet's proposed Latin aliases. Those remain explicit
morphology and lexical holds. The associated pencil figures are therefore
identity-checked candidates rather than factual-, print-, consumer-, or
release-approved publication assets.

## Bounded pontifical discovery pass

On 2026-07-27 the 1948 Marietti third edition after the typical of the
*Caeremoniale Episcoporum* was acquired, hashed, and inspected at book I,
chapters XI--XII and XXI. The exact retrieval, hash, inspected findings, and
limits are recorded in `pontifical-ceremony-candidate-audit.md`.

That bounded pass raises the named equipment only from memory-based search
terms to directly witnessed 1948 candidates. It does not close the operative
1962 edition and amendment question, does not establish material forms, and
does not authorize any candidate for rendering.

## Narrow pass: sacristy and preparation furnishings

This pass does not close the church-and-sanctuary category. The 2026-07-28
correction admits the cross-or-suitable-image and local signal bell as bounded
publication records, retains the preparatory handwashing place as a
source-audited text-only record, and leaves the other sacristy candidates held.

| Binding ID | Witness and exact locus | Claim use and limit |
| --- | --- | --- |
| `passage.catholic-church.missale-romanum.vatican-typica-1962.ritus-servandus-sacristy-preparation-and-reverence` | *Missale Romanum*, Vatican typical edition (1962), *Ritus servandus* I.1 and II.1, printed pp. LII and LIV / artifact PDF pp. 56 and 58 | Governing evidence for the pre-Mass handwashing action and departure bow toward the sacristy cross or image. It prescribes neither lavatory morphology nor a crucifix-only form. |
| `passage.adrian-fortescue.ceremonies-of-the-roman-rite-described.seventh-revised-1943.p-37-40` and `.p-59` | Fortescue, revised by J. B. O'Connell, *The Ceremonies of the Roman Rite Described*, seventh ed. (1943), printed pp. 37--40 and 59 | Contemporary ceremonial witness for the return bow and for a departure bell as practice in many churches. It does not make the bell universal or prescribe its mechanism, placement, operator, or morphology. |
| `passage.catholic-encyclopedia.volume-13.new-york-1912.sacristy` | Andrew Meehan, “Sacristy,” *Catholic Encyclopedia* 13 (1912), exact New Advent HTML artifact, furnishing paragraph | Dated specialist evidence for the room's function, cross-or-suitable-image focus, lavatory, and customary bell. It is not an official 1962 furnishing code. |
| `rsd-catholic-encyclopedia-piscina` | Francis Mershman, “Piscina,” *Catholic Encyclopedia* 12 (1911), New Advent transcription, lines 12--14, <https://www.newadvent.org/cathen/12115a.htm>, inspected 2026-07-27 | Specialist historical synthesis for names, disposal function, variable location, and materially different forms. It does not prove that every 1962 sacristy had one. |

The ordinary handwashing place and the piscina or sacrarium remain separate
records. No lavatory or piscina artwork is admitted: purpose, outlet, and
disposal practice must be learned locally and never inferred from appearance.
Torch racks, processional-object racks, hot-thurible stations,
generic sacristy kneelers, safes, and utility furniture remain practical/local
discovery leads until a material-culture source supports a representative
form. Generated resemblance is not evidence for them.
## Paired-cruet morphology and scale pass — 2026-07-27

The next bounded tranche closes a consumer-usable paired-cruet plate against
one dated manufacturer catalog and two exact Met Open Access object records.
The 1914 Gorham catalog leaves N36-N37 show and list multiple altar-cruet
models, materials, capacities, and heights. Met object 467483 supplies one
handled, footed exemplar at 16.7 cm; object 200141 supplies a cataloged pair,
each 14 cm high. Together they support a small paired altar-service identity
while disproving any claim that material, ornament, closure, handle, marking,
position, or silhouette is universal.

The generic plate is therefore narrower than any one witness. It teaches a
pair at common hand scale with stable bases, pouring lips, and graspable
handles. TeX owns the wine/water labels and local-variation statement. The
earlier single stoppered asset remains held because it can read as a household
decanter. Exact artifact identities, hashes, acquisition correction, rights,
and synthesis ceilings are recorded in
`cruet-pair-source-audit-2026-07-27.md`.

## Communion-plate morphology pass — 2026-07-28

The 1962 *Missale Romanum*, *Ritus servandus* X.7 continues to control the
distinct under-chin *patina* and fragment-catching function. One exact 1952
Hirten catalog page now supplies dated material-culture evidence for a round
one-wood-handle commercial exemplar and a separate two-handle variant. It
does not establish a universal Roman morphology, exact rim height or depth,
required material, color, ornament, server assignment, or ritual norm.

The comparison plate selects only the one-handle morphology, separates it
from the already controlled thin priest's paten, and carries an explicit
not-to-common-scale notice. The exact source identities, page-image check,
rights metadata, evidence ceilings, handling model, and artwork limits are
recorded in `communion-plate-source-audit-2026-07-28.md`.

## Thurible alpha reconciliation — 2026-07-28

The existing `obj-thurible` claims remain bounded to the exact 1962 Missal
loci and the inspected 1927 Benziger catalog pages recorded in
`thurible-source-audit-2026-07-27.md`. The Met object remains a variation
control only. Cross-edition promotion adds no new factual claim: it records
the existing project-generated graphite asset's provenance, rights, identity,
print, safety, and consumer checks and supplies audience notes derived from
the already checked identity and appearance claims.

The figure is one representative closed construction, not a universal
silhouette or material prescription. Reader-facing text does not provide
charcoal-lighting, loading, extinguishing, swinging, handoff, route, or hot
resting instructions. The bespoke altar-server leaf retains its stronger
existing full-page treatment and does not render a duplicate generated entry.

## Paired altar-cruets alpha reconciliation — 2026-07-28

The closed morphology tranche in
`cruet-pair-source-audit-2026-07-27.md` supports promotion of the paired
altar cruets through the five generic canonical-alpha editions. The exact
1962 Missal and checked server model control the wine-and-water service; the
1914 Gorham catalog and exact Met objects 467483 and 200141 control only the
small paired service identity, hand scale, stable bases, pouring edges, and
demonstrated variation. Promotion adds no fixed material, marking, closure,
handle, tray, left-right order, dimensions, ornament, or universal server
split.

The lexical question remains deliberately unresolved. Because the current
audit does not establish `ampulla` or `urceolus` as the preferred 1962
headword for this canonical record, the generic alpha pages print `Latin term
not asserted` rather than presenting either lead as verified. The bespoke
altar-server edition retains its stronger full-page paired treatment and is
not given a duplicate generated entry.

## Communion-plate alpha reconciliation — 2026-07-28

The exact Missal, 1952 Hirten catalog, Met catalog-exemplar comparison
control, and completed artwork audit recorded in
`communion-plate-source-audit-2026-07-28.md` support promotion of the
Communion plate through the five generic canonical-alpha editions. The
promotion adds no source claim. It preserves the Missal-controlled under-chin
function and fragment boundary while presenting the one-wood-handle form only
as one dated commercial exemplar.

The smaller priest's paten was comparison context at this checkpoint. Its
presence in this Communion-plate figure alone did not admit `obj-paten` or
establish a server handling claim. The later chalice-and-paten checkpoint
admits the canonical paten record through a different, separately controlled
plate and leaves this figure's not-to-common-scale boundary unchanged.

## Chalice-and-paten cross-edition reconciliation — 2026-07-28

The exact Missal and Met evidence chain recorded in
`paten-comparison-source-audit-2026-07-27.md` and the consumer reconciliation
in `chalice-paten-cross-edition-audit-2026-07-28.md` support canonical
admission of `obj-chalice` and `obj-paten` through the five generated
editions. The Met record controls one paired catalog exemplar and its
dimensions; the 1962 Missal independently controls identity, liturgical use,
the prepared relationship, and the distinction from the under-chin
Communion plate. Neither source supplies a universal vessel morphology or a
handling prescription. The bespoke altar-server leaf retains its stronger
combined treatment and is not regenerated.
