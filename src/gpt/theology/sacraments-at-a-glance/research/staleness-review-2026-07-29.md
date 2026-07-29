# Staleness review — 2026-07-29

## Edition, inheritance, and trigger

Edition reviewed: `gpt theology/sacraments-at-a-glance`. No Claude edition
exists.

This companion is mechanically inherited from
`src/gpt/theology/sacraments/`. It owns no theological prose: the treatise owns
the master matrix, lexicon, seven summaries, initiation table, and inherited
generation provenance. A substantive theological correction would therefore
begin in the treatise, not in this leaf.

`scripts/research-staleness explain` reports new CCC passage records at 270,
277, 391–395, 550, 1667–1673, 1700–1706, 1734–1735, 1857–1859, 2111,
2116–2117, and 2846–2854, plus *Lumen gentium* 12.

Both ignored candidates preserve mechanical inheritance:

- `modified/` is the unchanged current wrapper and its direct imports.
- `rewritten/` reconstructs the wrapper from the profile's required retrieval
  order without consulting or creating independent theological prose. It still
  imports the canonical treatise files directly.

## Per-claim three-way comparison

| Consequential inherited claim or invariant | Changed-input result | Old / modified / rewritten comparison | Effect and verdict |
| --- | --- | --- | --- |
| The master matrix distinguishes matter or quasi-matter, form, subject, minister, sacramental reality, grace/effect, change, and repetition for all seven sacraments. | None of the new passages corrects a matrix field. CCC 1667–1673 concerns sacramentals, a distinct subject outside the seven-sacrament matrix. | Modified imports the old matrix unchanged; rewrite independently selects the same canonical import. | No addition, removal, strengthening, weakening, or contradiction. |
| The lexicon distinguishes sacramental form, quasi-matter, grace, character, and *ex opere operato* from recipient disposition. | CCC 2111 on superstition is consonant with rejecting mechanical efficacy, but it neither changes the lexicon nor replaces Trent/CCC 1128 as its mapped control. | All three render the same treatise-owned lexicon. | No material strengthening is required. |
| Baptism's summary states subject, washing and Trinitarian form, minister, character, grace, and incorporation. | CCC 391–395 and 550 concern demons and Christ's exorcisms; CCC 1667–1673 distinguishes sacramentals and exorcism. They do not alter Baptism's sacramental fields. | All three import the same Baptism summary. | No change. |
| Confirmation's summary states anointing/laying on of hands, form, ministerial distinctions, character, and strengthening grace. | LG 12 concerns the faithful's prophetic office and charisms generally, not Confirmation's matter, form, minister, character, or proper grace. | All three import the same Confirmation summary. | No change. |
| Eucharist's summary distinguishes determining words, transubstantiation, accidents, sacrifice, presence, communion, and proper effects. | CCC 1857–1859 concerns mortal sin and is consistent with the existing warning about impenitent mortal sin, but supplies no change to Eucharistic ontology or discipline. | All three import the same Eucharist summary. | Merely consonant; no consequential change. |
| Penance's summary distinguishes contrition, confession, satisfaction, absolution, ministerial faculty, reconciliation, and mercy. | CCC 270 and 277 concern divine mercy; CCC 1700–1706 and 1734–1735 concern freedom and responsibility. These general loci do not correct the summary's sacrament-specific fields. | All three import the same Penance summary. | No strengthening, weakening, or contradiction. |
| Anointing, Orders, and Matrimony retain their sacrament-specific matter/form, subject, minister, grace/effects, and qualifications. | CCC 2846–2854 on temptation, LG 12 on charisms, and the general freedom passages do not amend those sacramental claims. | All three import the same three summaries. | No change. |
| The initiation table covers all twenty-four Catholic Churches *sui iuris* while preserving jurisdictional and pastoral limits. | No new Eastern-law, liturgical-book, ecclesial-status, or particular-law input. | All three import the same table. | No change. |
| The companion contains exactly matrix, lexicon, seven summaries, and initiation table in retrieval order, with one inherited provenance display and no independent theology. | The changed research supplies no reason to break mechanical inheritance. | Old and modified are identical. Rewritten uses a newly drafted wrapper but the same required import order and provenance mechanism. | Wrapper wording differs only in nonprinting implementation comments and metadata subject; rendered theology is substantively identical. |
| Translation, jurisdiction, currentness, and rights boundaries remain inherited from the canonical sources and terminal material. | No translation, law, rights, or authority record changed. | All three agree. | No change. |

## Verdict

The changed records add no correction to an inherited sacramental claim and no
reason to create independent companion prose. The rewritten wrapper differs
only in non-theological composition details. **Verdict: no material change.**
No canonical treatise fragment, companion source, installed PDF, or baseline
is changed.
