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

This pass does not close the church-and-sanctuary category. It supports six
bounded records under `shared/records/sacristy/` and deliberately leaves their
art and publication gates open.

| Binding ID | Witness and exact locus | Claim use and limit |
| --- | --- | --- |
| `rsd-mr1962-rs-i-ii` | *Missale Romanum*, Vatican typical edition (1962), *Ritus servandus* I.1 and II.1; repository source record under `src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/` | Governing evidence that the priest washes at a place prepared for that purpose, vests, and bows to the sacristy cross or image. It does not prescribe furniture construction. |
| `rsd-fortescue-oconnell-reid-1962-sacristy` | Fortescue, O'Connell, and Reid, *The Ceremonies of the Roman Rite Described*, 12th ed. (1962), ch. VI, sec. 1, scan pp. 67--68 | Contemporary ceremonial witness for a vesting table, the washing place, cross, and customary door bell. Shapes and dimensions remain local. |
| `rsd-catholic-encyclopedia-sacristy` | J. F. G. Gilmartin, “Sacristy,” *Catholic Encyclopedia* 13 (1912), New Advent transcription, lines 68--71, <https://www.newadvent.org/cathen/13322b.htm>, inspected 2026-07-27 | Specialist synthesis for the room's function, labelled vestment cases, prominent cross or image, lavatory, and customary bell. It is not an official 1962 furnishing code. |
| `rsd-catholic-encyclopedia-piscina` | Francis Mershman, “Piscina,” *Catholic Encyclopedia* 12 (1911), New Advent transcription, lines 12--17, <https://www.newadvent.org/cathen/12115a.htm>, inspected 2026-07-27 | Specialist historical synthesis for names, disposal function, variable location, and materially different forms. It does not prove that every 1962 sacristy had one. |

The ordinary handwashing lavatory and the piscina or sacrarium remain separate
records. Torch racks, processional-object racks, hot-thurible stations,
generic sacristy kneelers, safes, and utility furniture remain practical/local
discovery leads until a material-culture source supports a representative
form. Generated resemblance is not evidence for them.
