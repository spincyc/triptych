# Independent historical and liturgical review

Reviewed 2026-07-27 against `guidance/editorial.md`,
`guidance/history/historical-accounts.md`, the current rendered source, the
evidence map, the three focused audits, the publication bindings, and the
registered reusable-source records.

## Reviewer and scope

This is an independent agent review of historical method, chronology,
liturgical classification, edition control, and the fit between published
claims and recorded evidence. It is not a credentialed specialist,
ecclesiastical, canonical, clinical, safeguarding, pastoral, or rights review
and does not close those review lanes.

## Verdict

**Pass with reservations for the bounded historical and liturgical
narrative; reusable-source closure does not pass.**

The revised study no longer depends on named cases, an alleged unbroken ritual,
an unverified 1614 witness, or an expansive medieval synthesis. Its principal
historical argument is proportionate to its evidence: biblical narrative,
apologetic claim, baptismal preparation, clerical office, ritual-book witness,
codification, and the current major rite are related without being identified.
The distinction among manuscript, edition, official act, territorial
implementation, and present authorization is consistently maintained.

The exact Wilson scan and the 1614 princeps witness now support the two most
important liturgical transitions at the level claimed. The Gelasian discussion
is appropriately confined to Wilson's printed pp. 45--50 and does not infer a
manuscript stratum or frequency of use. The 1614 discussion distinguishes the
edition's architecture and cautions from later title numbering and present
authorization. The current Roman book's decree, 1999 issue, 2004 emended
reprint, and territorial translation are not collapsed into one event.

The disclosed gaps in the *Apostolic Tradition*, patristic editions, the
*Pontificale Romano-Germanicum*, a representative medieval ordinal, and
cross-genre medieval evidence are now used as ceilings rather than as positive
evidence. That treatment satisfies the historical-accounts evidence gate for
the narrower published claims. It does not satisfy the release manifest's
separate `complete-reusable-source-registration` gate.

## Required exact fixes

1. **Correct the PRG orientation sentence before release.** `sections/140-dated-orientation.tex`
   currently says that the *Pontificale Romano-Germanicum* “is consulted through”
   Vogel--Elze. The source record expressly says that no exact artifact, ordo,
   or page was acquired. Replace that phrase with: “is identified
   bibliographically through the Vogel--Elze 1963--1972 edition; no exact ordo
   or page supports a publication claim here.” This is a claim-state
   contradiction, not merely a desirable enhancement.

2. **Remove the unsupported possibilities attached to Cornelius's combined
   personnel total.** `sections/40-late-antique-medieval.tex` says that
   catechumenal preparation, care of afflicted persons, and other liturgical
   service “could all stand behind the title.” Eusebius 6.43.11 establishes the
   combined list and title, not those possible duties. Replace those two
   sentences with: “The list does not define the exorcists' duties, distinguish
   baptismal from extraordinary ministry, or establish the same arrangement in
   every church.”

3. **Clarify “public” in the opening.** Calling major exorcism a “public
   liturgical sacramental” correctly distinguishes an ecclesial act from private
   technique, but can be misread as describing an event open to spectators.
   Replace it with “an ecclesial liturgical sacramental, ordinarily celebrated
   with strict confidentiality.” Retain the canon 1172 qualification.

4. **Keep the current medieval ceiling.** Do not restore claims about PRG
   contents or circulation, regular duties of medieval officeholders,
   medicine replacing exorcism, demonological taxonomies, trials, magic,
   prevalence, or named cases until the exact primary loci and appropriate
   historical controls recorded in the audits are acquired and checked.

## Reusable-source closure

The source-library validator passes, but validation proves record consistency,
not completeness. The following remain open under the release manifest's
registration gate:

- a critical-edition control for the church-order complex conventionally
  called *Apostolic Tradition* 20--21;
- focused reusable passages for Justin, Tertullian, Origen, Cyril/Jerusalem,
  and other patristic claims presently supported at edition or local-audit
  level;
- an exact Vogel--Elze artifact, ordo, and page if the PRG is to establish
  content rather than bibliography;
- a representative Western ordinal if the delivery-of-the-book or office-duty
  history is to be stated positively;
- focused Aquinas III, q. 71 passage records if artifact-level binding is not
  accepted as final claim control; and
- the remaining passage normalization explicitly marked outstanding in
  `research/source-bindings.toml` and the focused audits.

These gaps do not require padding the narrative. They require either exact
registration or continued omission and an explicit release decision narrowing
what `complete-reusable-source-registration` means for this leaf. A manifest
gate must not be silently treated as closed merely because the prose now
discloses the gaps.

## Hold recommendation

Retain the release hold. After the three textual corrections above, the
historical and liturgical lane may be recorded as passed with the stated source
ceilings. Hold lift still requires closure of the manifest's reusable-source
gate, the other independent review lanes, a fresh final-source build and
every-page review, exact installed-snapshot verification, current web
generation, catalog insertion, and exact release binding.
