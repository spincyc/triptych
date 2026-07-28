# Linen and textile inventory audit

Audit date: 2026-07-27
Scope owner: altar linens and the visually confusable Mass textiles
State: **bounded source and artwork pass; not a completeness or publication approval**

## Controlling checks

The page images of the registered 1962 Vatican typical Missal facsimile were
checked directly, not merely through OCR:

- *Rubricae generales Missalis romani* 526 and 528, artifact PDF p. 34
  (printed p. XXXVI): the altar is covered with three clean blessed cloths; at
  the Epistle side a prepared table holds the wine and water cruets, basin,
  `manutergium`, bell, and Communion plate.
- *Ritus servandus in celebratione Missae* I.1--II.2, artifact PDF p. 56
  (printed p. LIV): the prepared chalice has a clean `purificatorium`, paten
  and host, small linen `palla`, silk veil, and burse containing the folded
  `corporale`; the corporal must be wholly white linen and is spread in the
  middle of the altar.
- *Ritus servandus* VII.2--11 and X.5, artifact PDF pp. 60--64 (printed
  pp. LVIII--LXII): the corporal, purificator, pall, burse, chalice veil,
  handwashing and post-Communion disposition are named in use.

The source identity is
`artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf`,
SHA-256
`648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a`.
The remote PDF was downloaded only below the run-owned temporary directory and
its tracked artifact record was not altered.

For morphology and historical distinctions, A. J. Schulte, “Altar Linens,”
*Catholic Encyclopedia* 1 (New York: Robert Appleton, 1907), and the
encyclopedia articles “Chalice,” “Humeral Veil,” “Altar Cloths,” and “Amice”
were inspected as specialist secondary leads. They support the visual
distinction between corporal, purificator, stiff and soft linen palls,
finger-towel, altar cloths, cere-cloth, amice, burse, chalice veil, and humeral
veil. They do not by themselves establish a universal 1962 prescription.

## Canonical candidate families

The IDs below are reserved for later TOML records. A term is
`source-audited-core` only where the checked Missal page establishes its
presence and liturgical relationship; morphology remains at the lower
specialist-secondary ceiling unless otherwise stated.

| ID | English headword | Latin headword / searched aliases | Distinguishing visual fact | Evidence ceiling |
| --- | --- | --- | --- | --- |
| `obj-corporal` | corporal | *corporale* | square white linen; unfolded beneath the chalice, folded in the burse | source-audited core |
| `obj-purificator` | purificator | *purificatorium*; historical *emunctorium* | narrow rectangular white linen used at chalice and fingers | source-audited core |
| `obj-chalice-pall` | chalice pall | *palla*; *parva palla linea* | small square chalice cover | source-audited core |
| `obj-lavabo-towel` | lavabo or finger towel | *manutergium* | small towel presented with basin at the Epistle side | source-audited core |
| `obj-altar-cloths` | altar cloths | *tobaleae*; *mappae* | three clean blessed cloth layers over the altar | source-audited core |
| `obj-chalice-veil` | chalice veil | *velum sericum*; *velum calicis* | silk square draped over the prepared chalice | source-audited core |
| `obj-burse` | burse | *bursa* | stiff square case containing the folded corporal | source-audited core |
| `obj-communion-cloth` | Communion cloth | *mappa Communionis* (lexical form still to verify) | long white cloth at rail or held before communicants | identified lead |
| `obj-credence-cloth` | credence cloth | *mappa credentiae* (lexical form still to verify) | cloth covering the credence top | identified lead |
| `obj-cere-cloth` | cere-cloth | *chrismale*; cere-cloth | waxed protective cloth beneath altar linens | specialist-secondary lead |
| `obj-amice` | amice | *amictus* | plain oblong linen with two tapes; no neck opening | source-audited as vestment; retained here as a confusable |
| `obj-humeral-veil` | humeral veil | *velum humerale* | one long rectangular silk veil worn over shoulders | identified; ceremony claims need corpus closure |
| `obj-gremial` | gremial | *gremiale* | broad lap cloth used by a seated bishop | identified pontifical lead |
| `obj-vimpa` | vimpa | *vimpa*; plural *vimpae* | one of a pair of narrow shoulder veils for insignia bearers | identified pontifical lead |

### Substantive candidate variants

- `var-chalice-pall-rigid`: linen-faced stiff square, commonly with a removable
  washable underside.
- `var-chalice-pall-soft`: a single or folded piece of linen without a board.
- `var-corporal-carthusian-large`: older large corporal form reported as
  retained by the Carthusians; religious-order source verification is still
  required before selection.
- Humeral veils used by the subdeacon at Solemn Mass and for Blessed-Sacrament
  functions differ materially in color rule and use; they should be separate
  contextual views of the same object family unless later official-source
  audit establishes separate canonical identities.
- Vimpae are a paired article; ornament alone does not create a variant.

## Artwork assets and personal review

All four assets were generated with the built-in image tool, without reference
images, normalized to 8-bit grayscale/256 colors, and inspected at full
resolution:

| Asset | Contents | Review result |
| --- | --- | --- |
| `shared/artwork/pencil/RSD-ART-001-white-linens.png` | corporal folded/unfolded and in use; purificator; rigid and soft pall; finger towel | identity-checked; compact and legible; some folded specimens remain dependent on labels for certainty |
| `shared/artwork/pencil/RSD-ART-002-altar-textiles.png` | three altar-cloth relationship, cere-cloth, Communion cloth, credence cloth, corrected rectangular amice | held multi-object research plate; the cutaway is unsuitable for altar-server publication because its explanatory layers can read as construction courses or cloths inserted between altar elements |
| `shared/artwork/pencil/RPD-FIG-linens-0006-three-altar-cloths.png` | exactly three plain cloth sheets above one neutral thin altar-top silhouette | source-minimal altar-server successor; extents, hanging edges, folds, spacing, and support silhouette are illustrative; no masonry, frontal, dust cover, corporal, marks, dimensions, person, action, or ritual object |
| `shared/artwork/pencil/RSD-ART-003-veils-burse-gremial.png` | chalice veil, burse, humeral uses, gremial, vimpae | partially identity-checked; chalice veil, burse, and gremial are usable studies; its flat humeral-veil silhouettes are rejected in favor of the next asset |
| `shared/artwork/pencil/RSD-ART-004-humeral-veils-vimpae.png` | long rectangular subdeacon and Benediction humeral veils, paired vimpae, context insets | identity-checked; long rectangular geometry corrected; inset hands and vesture still require competent ceremonial review |

No asset is marked liturgically approved or print-approved. Generated
ornament, fold direction, relative dimensions, hand placement, and every
pontifical context remain review obligations. Typeset labels, not generated
lettering, must identify every figure.

## Holds before publication

1. Close the official corpus for Communion cloth, humeral veil, gremial, and
   vimpae; verify their exact Latin headwords at source loci.
2. Register the inspected specialist reference as a canonical reusable source
   or bind an equivalent retained source before using morphology claims.
3. Obtain competent ceremonial review of all in-use insets.
4. Print-test the plates at intended column width and add labels/callouts from
   canonical records.
5. Keep the amice under vestments and use its linen-plate appearance only as a
   confusable cross-reference.
