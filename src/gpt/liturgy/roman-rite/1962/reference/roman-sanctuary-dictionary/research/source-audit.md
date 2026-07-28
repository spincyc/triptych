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
