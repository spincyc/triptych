# Cassock and surplice — source and artwork audit

Audit date: 2026-11-05. Provider: GPT. Roman Rite, 1962 horizon; English
headwords with Latin names. This slice supplies two canonical records,
`obj-cassock` and `obj-surplice`, for ordinary server clothing and basic choir
recognition. It does not close the servers, ministers and choir category.

## Admission boundary

The 1962 Missal names the minister's surplice. The checked 1943 ceremonial
describes the common cassock-and-surplice arrangement and explicitly records
a recognized custom of serving Low Mass in lay dress. The objects therefore
belong to the ordinary Roman corpus, while the black cassock, white linen
surplice and pictured cuts are not prescribed for every wearer or every local
branch by these records. `ceremonies` is bounded to Low Mass; the records do
not encode rank-specific choir dress or separate Holy Week, pontifical,
processional or related-ceremony branches.

The existing `vestments-ministers-audit.md` treated cassock, surplice and
cotta as research leads and rejected its generated mixed clothing study. The
two new records and three new figures supersede those leads only within this
slice. The rejected study receives no new approval.

## Checked evidence

All three sources already have canonical remote artifact identities. No new
source payload, source record or duplicate bibliographic identity was added.
The complete available PDFs were used; optical text located passages and page
images controlled the claims. Existing local Missal and Fortescue bytes were
rehashed against their records. The complete Hirten PDF was freshly retrieved
from its public download and matched its registered hash.

| Exact witness and inspected locus | Claim supported | Claim ceiling |
| --- | --- | --- |
| Vatican *Missale Romanum* (1962), *Ritus servandus* II.1, opening Ritus page without visible printed folio, PDF p. 56 | The minister precedes the priest to the altar wearing a surplice; Latin headword *superpelliceum* | The clause supplies no illustrated cut, textile, neckline, ornament or dimensions. |
| Adrian Fortescue, revised by J. O'Connell, *The Ceremonies of the Roman Rite Described*, seventh revised edition (London, 1943), title PDF p. 6; printed p. 10, PDF p. 31, opening paragraph and note 1 | Common server and choir dress: black cassock, *vestis talaris*, with white linen surplice, *superpelliceum*; *cotta* is supplied as its Italian name | This is the checked contemporary ceremonial's description. Prelatial exceptions mentioned nearby are outside the new records. |
| Same 1943 edition, printed p. 70, PDF p. 91, Preparation and note 4 | The server puts on cassock and surplice before Low Mass; the source also records a recognized lay-dress custom in several countries, including England | The cited Sacred Congregation of Rites decrees were not separately inspected. The record attributes the custom to the ceremonial and does not independently adjudicate the decrees or current law. |
| William J. Hirten Co., *Hirten* (1952), cover PDF p. 1; printed p. 125, PDF p. 127: altar-boy ensemble, No. 3893 utility cassock, No. 9607 boys' lawn surplice | Dated frontal morphology: a full-length, long-sleeved cassock; a short gathered surplice with broad open sleeves and no girdle; surplice worn over cassock | Catalog exemplars establish visible forms, not Roman prescription. Rear construction, exact folds, button count, collar or neckline design, sizes, textile requirements and universal color rules are not established. |

Public delivery routes and exact identities:

- [1962 Missal facsimile](https://media.churchmusicassociation.org/pdf/missale62.pdf),
  SHA-256 `648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a`.
- [Fortescue–O'Connell facsimile](https://archive.org/download/in.ernet.dli.2015.56750/2015.56750.Ceremonies-Of-The-Roman-Rite-Described_text.pdf),
  SHA-256 `10acb8de9b161ed2c08be7ce767515418bca5d1ed7ddfff2de902179e1b62c7a`.
  The public item's catalog date says 1917; the inspected title page identifies
  the actual seventh revised printing as 1943 and controls this audit.
- [Hirten 1952 facsimile](https://archive.org/download/hirten-religious-goods-1952/Hirten_Religious_Goods_1952_text.pdf),
  SHA-256 `ccd22db7a72a5b3e38a9e4bb9ff8fec03ebc31966d883edcfaf5e5be6d66dcb3`.
  The download was publicly reachable on the audit date; failure of the
  browser's separate item-page fetch did not prevent whole-file retrieval.

The canonical object source tables own the stable artifact IDs, source roles,
claim links and exact loci. These facts are original checked paraphrases;
the entry contains no extended quotation or prayer text.

## Terminology and variant decision

`obj-surplice` carries **Cotta** as an alias. Fortescue–O'Connell's p. 10
note 1 expressly calls it the Italian name for the surplice. This is positive
evidence for the alias, not an inference from two similar images. It does not
assert that every regional or later use of *cotta* is identical. No separate
`obj-cotta` is created and no different shape is invented to justify one.

A second terminology pass consulted Joseph Braun's 1912
[Catholic Encyclopedia article on the surplice](https://www.newadvent.org/cathen/14343d.htm)
through its New Advent delivery. Its historical discussion treats the earlier
names' precise distinction as uncertain. That web transcription was a
corroborating research lead, not a separately collated edition or a source for
printed claims in these records. The decision rests on the exact 1943 page.
The adjacent Hirten No. 9608 lace surplice remains decorative variation in this
slice; no separate object or substantive variant is claimed. Rochet, biretta,
religious-community habits and rank-specific dress remain open work.

## Rights and generation

The three source artifacts remain remote. Public download, historical date
and a host's public-domain metadata do not authorize reproducing the scan.
Neither scan pixels nor complete source text enter the new publication
material. Existing artifact-level rights ceilings remain unchanged.

Three original drawings were generated with the built-in image-generation
tool on 2026-11-05. No source image or other reference image was supplied to
generation. The prompts express only the checked general forms. The exact
prompts, selected original-output hashes, normalized hashes, dimensions,
byte counts, source controls and transformations have one owner in
`research/artwork-manifest.toml`; they are not reconstructed from the images.
The exact image model/version and runtime were not exposed.

| Artwork ID | Depicts | Teaching role |
| --- | --- | --- |
| `art-cassock-front` | `obj-cassock` | One complete unworn frontal cassock, with no surplice or wearer. |
| `art-surplice-front` | `obj-surplice` | One complete unworn frontal surplice, with no cassock or wearer. |
| `art-cassock-surplice-worn` | Both objects; canonical render owner `obj-cassock` | One representative figure shows the paired layer relationship. TeX must name both garments beside this figure. |

The selected images were converted to stripped 8-bit grayscale-alpha using
ImageMagick's `-colorspace Gray -depth 8 -strip -define png:color-type=4`.
Dimensions were retained. Alpha-channel absolute error against each original
was **0**, so the generated transparency was preserved exactly. The registered
`artwork-library normalize` command removes alpha and was therefore not used
for these transparent outputs. Each normalized raster is below one MiB and
two megapixels. The maximum placement envelopes are 3 by 4.5 inches for the
cassock and wearer, and 4.5 by 3 inches for the surplice, giving 341.33 pixels
per inch. This is an artwork envelope, not evidence of a completed print.

## Figure review and remaining integration

The producing agent inspected each normalized figure at full size on white.
The coordinating agent independently inspected the same three white-ground
figures against Hirten p. 125 on 2026-11-05 and accepted their bounded
morphology. Both checks found complete silhouettes, distinct garment
identities, the correct upper/lower layer relation, plausible construction
and anatomy, no clipping, no words or semantic marks, and no added insignia
or unrelated objects. The figure's hands are empty and relaxed; it teaches
no handling action or ceremonial gesture. Collar shape, buttons, proportions
and folds remain illustrative. White translucent fringe disappears on the
intended white page ground; dark-background use has not been approved.

The planned section is `plt-server-clothing`, with all six dictionary editions
as intended consumers. Both records set general-reader relevance to `required`:
recognizing the ordinary server-clothing pair and distinguishing its short
surplice from the alb belongs to that edition's basic visual survey. Its
existing required-only selection rule is unchanged. Every displayed view needs its English and Latin
identity, a representative-form qualification, and a not-to-common-scale
notice; the combined view must identify both garments. The shared worn
artwork is rendered once through its canonical owner.

At the initial source-and-figure checkpoint the objects were `art-reviewed`,
manifest artwork rows were `visual-review-passed`, and asset custody was
`held` pending the renderer's actual consumer check. The later proof review
and narrow promotion below supersede that checkpoint. The coordinator owns
final all-six-edition review and release. No completeness or external
ecclesiastical approval is asserted.

Validation at this checkpoint: the canonical inventory validator passed with
82 object records; `tools/check-roman-sanctuary-artwork` passed with zero held
object-link notices; and `tools/artwork-library check` passed for the complete
artwork manifest. These checks establish structural and technical integrity,
not consumer or print approval.

## Consumer proof check and promotion

The renderer agent built a two-page proof through the actual shared paired
layout and exact source-note machinery, selecting only these two records in
scratch. The source-producing agent independently inspected both page rasters
and collated the extracted PDF text against the object records and checked
loci. The final proof is
`.scratch/dictionary-cold-review/clothing-preview/clothing-preview.pdf`,
SHA-256 `5d9a0bf6cd790a2c841206cf4915eb5171e227c9d0da3c7f1ea6c82897f49557`.
Its first page contains the two isolated garments and exactly one worn
ensemble, with “Cassock with surplice” identifying both garments. English
and Latin names, garment layering, ordinary-dress attribution, recorded
lay-dress custom, black-color ceiling, representative tailoring and
not-to-common-scale notice are visible. The second page identifies all
three exact editions and each object's checked loci, including the 1943
title identity and 1962 Missal Ritus II.1. No content loss, clipped figure,
overlap, source-note mismatch, missing character or overfull-box warning was
found. The captions remain readable at the intended page layout. The proof
uses the altar-server reader notes; the shared renderer emits each record's
canonical care/limits warning in every audience edition.

Earlier proof checks caught and corrected an antecedent-free “same
ceremonial” caption, a worn-view label that did not name both garments,
and missing canonical care/limits text. No figures were changed. Temporary
duplicate tailoring sentences in audience notes were removed once the full
canonical warnings were rendered.

On this evidence, only the two clothing records were promoted to
`publication-ready`, their four artwork links to `approved`, the three new
asset custody rows to `canonical-alpha-eligible`, and their three artwork
rows to `consumer-review-passed`. Their factual, visual, rights, print and
consumer checks pass; **print means the inspected PDF screen proof**, not a
physical print test. Release stays `pending` for the coordinator's complete
six-edition production and release check. The intended six consumers remain
an integration scope, not a claim that this isolated proof is six complete
publications. No dark-ground use or physical-print result is asserted.

## Six candidate consumer checks

The source-producing agent inspected the clothing page in each complete
second-round candidate PDF below on 2026-11-05, including its audience note, canonical
limits, three figure placements and keyed source-note entries. All six
clothing pages pass. Each retains both garment identities, the single worn
ensemble, explicit paired label, representative form/color ceilings and
not-to-common-scale notice. The exact clothing source notes in every PDF
were text-collated against the checked loci above. PDF page numbers include
the cover. These are pre-release candidate receipts; a later production
receipt may supersede their layout or revision stamp.

| Edition | Candidate PDF basename | Clothing PDF page | SHA-256 |
| --- | --- | --- | --- |
| altar-server | `altar-server--8d6ef9ee7792363f.pdf` | 10 | `ad43188c4b948a6d375107bda4a8993eaefa75924aabbc7fda08ec4f8b950a5b` |
| comprehensive | `comprehensive--8d7a3290a3baac13.pdf` | 17 | `8aa0df6a21a877c77e4a963faa075db40a279d0cac325674e1daba04ed1ba94e` |
| general-reader | `general-reader--b3d3775d79dfdc4e.pdf` | 12 | `ec0c7d20f19a9b39e8c00bf4c1ca68a4b51d621efc27bf0f18900f1ab2fe29e3` |
| mc-trainer | `mc-trainer--8bbc52076ee3ca6f.pdf` | 11 | `585af8814875aa73942277f95177a97ae5b15e81336745cc262a3e0e0de6e5e8` |
| pontifical-ceremonies | `pontifical-ceremonies--8a620eda7508c98c.pdf` | 11 | `cc0841674cd61a3b68a730442a0364003fac8b222b3830ded09940d449e259f3` |
| sacristan | `sacristan--730c028c11eb6146.pdf` | 12 | `87e10e32e70988561341adea3033fa5c1ad8856d7163ceea1382c74f0f09e503` |

PDFs were under `.scratch/dictionary-cold-review/print-v2/<edition>/`; review
rasters and extracted notes are under
`.scratch/dictionary-corpus/consumer-review-v2/`. The first candidate
review found an MC/trainer working-set overlap outside the clothing page;
the second-round inspection confirms the corrected layout clears it. All
six clothing layouts remain intact. Source-note reference numbers changed
when the bibliography gained an edition, so each new number was also
checked against its listed edition; the clothing and ombrellino loci are
unchanged. Release remains pending the complete publication review and
committed revision-stamp pass.

## Final source admission

The three figures' release reviews passed after the final six-edition screen
review recorded in `../cold-review-2026-11-05.md`. Their image bytes are
unchanged from the inspected v2 clothing plates. The final proofs contain
100 pages across the six editions; this approval concerns those figures and
consumers, not full corpus closure, physical printing or live deployment.
Committed-stamp and served-bundle checks are recorded separately in the
current production manifest and project work register.
