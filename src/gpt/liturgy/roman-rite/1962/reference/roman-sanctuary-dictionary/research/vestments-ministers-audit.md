# Vestments, servers, and ministers: inventory and artwork audit

Audit date: 2026-07-27

Status: **inventory leads established; three study plates generated; no plate
approved for publication**

This pass owns the vesture slice for priests, deacons, subdeacons, servers,
other ministers, and choir in Roman ceremonies at the 1962 horizon. It does
not include episcopal and prelatial vesture or insignia, which require the
separate pontifical corpus. The records below are deliberate inventory leads,
not claim-level verified object records. They must not be selected by the
publication generator until exact source loci, object records, and corrected
artwork satisfy the schema gates.

## Canonical object queue

| Proposed object ID | English headword | Latin lead | Category | Required views | State and source work |
| --- | --- | --- | --- | --- | --- |
| `obj-amice` | Amice | *amictus* | priestly vestments; linens and textiles | flat, tied, worn | Identified lead; verify terminology, dimensions, apparelled form, and vesting use |
| `obj-alb` | Alb | *alba* | priestly vestments | front, back, apparelled detail, worn | Identified lead; verify construction and ministerial use |
| `obj-cincture` | Cincture | *cingulum* | priestly vestments | coiled, tied, worn | Identified lead; verify terminology, material, and use |
| `obj-maniple` | Maniple | *manipulus* | priestly vestments; deacon and subdeacon | isolated, worn on left arm | Identified lead; verify use by order and ceremony at the 1962 horizon |
| `obj-priest-stole` | Priest's stole | *stola* | priestly vestments | isolated, worn crossed/uncrossed where applicable | Identified lead; verify arrangement by wearer and ceremony |
| `obj-deacon-stole` | Deacon's stole | *stola* | deacon and subdeacon | isolated, diagonal worn view, fastening detail | Identified lead; verify exact ceremonial arrangement |
| `obj-chasuble` | Chasuble | *casula; planeta* | priestly vestments | Roman and Gothic front/back/worn comparisons | Identified lead; lexical and substantive-variant audit required |
| `obj-cope` | Cope | *pluviale* | priestly vestments; related ceremonies | front, back, open, clasp and hood details | Identified lead; verify Mass-adjacent and processional uses |
| `obj-biretta` | Biretta | *biretum* | priestly vestments; servers, ministers, and choir | front, top, worn | Identified lead; rank, region, tuft, and peak variants require audit |
| `obj-dalmatic` | Dalmatic | *dalmatica* | deacon and subdeacon | front, back, worn | Identified lead; distinguish stable construction from ornament |
| `obj-tunicle` | Tunicle | *tunicella* | deacon and subdeacon | front, back, worn | Identified lead; direct comparison with dalmatic required |
| `obj-folded-chasuble` | Folded chasuble | *planeta plicata* | deacon and subdeacon; historical | front, back, worn | Held pending exact 1962 reform-horizon chronology and ceremonial loci |
| `obj-broad-stole` | Broad stole | *stola latior* | deacon and subdeacon; historical | isolated, worn | Held pending the same chronology audit |
| `obj-cassock` | Cassock | *vestis talaris* | servers, ministers, and choir | front, back, worn | Identified lead; distinguish clerical and server use without universalizing local color |
| `obj-surplice` | Surplice | *superpelliceum* | servers, ministers, and choir | front, back, worn | Identified lead; construction and jurisdictional variation audit required |
| `obj-cotta` | Cotta | *cotta* | servers, ministers, and choir | front, back, worn comparison | Identified lead; determine whether it is a stable object distinction or regional terminology/form |
| `obj-rochet` | Rochet | *rochettum* | servers, ministers, and choir; pontifical and prelatial | front, back, worn | Identified lead; rank, sleeve, and jurisdiction claims require exact sources |

The queue deliberately excludes vague umbrella records such as “priestly
vestment set.” Each material item must become its own TOML object record so
derived editions can select, cross-reference, and describe it without copied
facts. Decorative motifs, lace depth, and individual embroidery are not
separate variants. Roman/Gothic chasuble construction, dalmatic/tunicle
construction, and surplice/cotta/rochet distinctions may be substantive only
after the variant audit proves them.

## Source ceiling

The existing repository binding for the Vatican 1962 *Missale Romanum*
facsimile can support exact ceremonial-presence and vesting claims only after
the relevant page image is inspected for each claim. The repository record for
Fortescue--O'Connell, twelfth revised edition (1962), is presently a catalog
lead: no relevant page payload or page image has been inspected here. Neither
record presently supports dimensions, textile construction, regional forms,
or symbolism.

Required next checks:

1. inspect the 1962 Missal's *Ritus servandus*, Mass formularies, and Holy Week
   rubrics wherever they name or presuppose these items;
2. inspect exact pages in a competent 1962 ceremonial manual for sacred
   ministers, server dress, and handling relationships;
3. bind a provenanced textile/museum corpus for morphology, backs, openings,
   fastening, and materially different forms;
4. treat folded chasubles and the broad stole as held until their reform
   chronology is established directly;
5. source any brief symbolism separately rather than inferring it from
   appearance.

## Generated study assets

All three images were generated with the built-in image-generation path on
2026-07-27. No external reference image was supplied. They are study assets,
not source evidence.

| Artwork lead | Asset | Prompt summary | Dimensions / SHA-256 | Personal review and disposition |
| --- | --- | --- | --- | --- |
| `art-vest-priest-study` | `shared/artwork/pencil/RSD-ART-VEST-001-priestly-vestments-study.png` | Dense portrait graphite comparison of amice, alb, cincture, maniple, stole, Roman and Gothic chasubles, cope, and biretta; isolated and front/back views; no text | 997 x 1577 px; `f7cccf657ca717249a35af01e67ed38627d714c0b7aa1b5a3041d5572e01ea84` | Monochrome/no-text and gross identity checked. **Rejected for publication:** amice morphology is questionable, the maniple/stole grouping is ambiguous, and variants were generated without source references. |
| `art-vest-sacred-ministers-study` | `shared/artwork/pencil/RSD-ART-VEST-002-sacred-ministers-study.png` | Dense portrait graphite comparison requested for deacon, subdeacon, dalmatic, tunicle, diagonal stole, maniple, folded chasuble, and broad stole | 1024 x 1536 px; `da9e94695202c586995b5cc82446baaaea8b4088603796dce7a76f7639a83d13` | Monochrome/no-text and figure count checked. **Rejected for publication:** the first figure shows a stole over the alb rather than the requested complete dalmatic ensemble, worn identities are not self-evident, and folded-chasuble/broad-stole chronology is unsourced. |
| `art-vest-server-choir-study` | `shared/artwork/pencil/RSD-ART-VEST-003-server-choir-study.png` | Dense portrait graphite comparison of cassock, surplice, cotta, rochet, apparelled details, and worn cassock/surplice ensembles; no text | 1024 x 1536 px; `fb7f509db2ab1c43bcbbd582f66452a79746b0aee0692c98a7ceaa063694b8bd` | Monochrome/no-text, gross garment identity, front/back arrangement, and obvious anatomy checked. **Rejected for publication:** the apparelled details are not reliably rendered, surplice/cotta distinctions are inconsistent, and rochet/rank morphology needs source-led redrawing. |

No factual, liturgical, print, rights, or release approval is claimed. A future
generation pass must use directly inspected visual references with known reuse
status, issue one tightly bounded object/variant family per asset, and retain
typeset labels outside the pixels.
