# Bullarium reading-order visual review 06 — batch bullarium-ro-0003

CHANGES_REQUIRED for 3 of 16 assigned PDFs; 13 PASS. All 45 pages were individually opened at full size, with zero reused pages. The blocking defect is the same in all three: a page-foot note run into a body paragraph (addendum item b). There are five such fusions on four pages. No marginal-into-body fusion was found; one locus is recorded as uncertain (see `unit-0033` below). This report covers only lane 6 of batch `bullarium-ro-0003`: 16 complete printed acts of Clement VIII from Bullarium Romanum volume 11 (1867 Turin printing), all coordinate-reconstructed reading-order readers.

## Scope and method

Each page PNG listed in the lane assignment was opened as its own full-size image with the Read tool (1700x2200 rasters, displayed at 1545x2000). No contact sheet, thumbnail or new raster pass was used. One ledger line per page was appended to `observations.jsonl` after each one to three pages.

Checked on every page: displayed title, responsible issuer, Latin label and the omission of the unresolved date against the frozen metadata; headings, two-column flow, gutters, margins and glyphs; natural source closing; modern provider signatures; running heads and furniture; raw placeholders. Per the Bullarium reading-order addendum, every marginal summary was checked to be its own separate block, every printed page-foot note its own block at the page break, and two-column order natural. No document is a fragment.

Where a page raised a question about a block's role, the volume's tracked reading-order derivative was read to confirm TAB-led (marginal) versus body role and paragraph membership. That derivative is `src/sources/works/bullarium-romanum/volume-11/editions/1867-turin-latin/artifacts/reading-order-e3cb674fd723/hybrid.txt`, SHA-256 `e3cb674fd723d9f16c10562dd15e3f565aac2a19586d6f0c5664374f365b2db0`. `pdftotext` output of each PDF was used only to confirm literal characters. Two read-only helper scans over each document's selected LF ranges cross-checked the visual findings:

- **Mixed paragraphs (`margscan.py`):** zero paragraphs mix TAB-led and body lines, out of 166 all-marginal paragraphs.
- **Notes sharing body paragraphs (`notescan3.py`):** this flagged exactly the five fusions confirmed visually. Its other hits were all note-only paragraphs, not defects: a note carrying a printer signature mark (`unit-0016`), a long note (`unit-0030`) and a `(I)` note (`unit-0047`).

No word geometry was available locally (the volume XML is remote), so no locus was decided by coordinates.

Counts: 164 marginal-summary blocks were counted in the ledger. Two further single-glyph TAB-led speck blocks in `unit-0016` (pages 2 and 3) were recorded but not counted, which gives 166 marginal-role blocks; that equals the derivative's count. Of these, 7 are single-glyph speck blocks. 101 separate note blocks and 45 separate running-head blocks were seen. **Five page-foot note-into-body fusions** were found (below). **Zero marginal-into-body fusions** were found, with one locus left uncertain. No recognizable modern provider signature ("Digitized by Google" or variants), no raw `None` placeholder, no clipping, no overlap and no tofu or missing-glyph boxes were found. The black square `■` in some OCR noise strings is a literal extracted character (U+25A0, confirmed in `pdftotext` output), not a missing-glyph box.

No document carried a `prior_finding`.

## Evidence verification

All 64 pinned files (receipt, frozen manifest, raster-run record, 16 PDFs and 45 page PNGs) were hashed before inspection and again after. Every digest matched its assignment pin both times (`verification-before.json` all_match=true, `verification-after.json` all_match=true; the two records are byte-identical).

| Evidence | Path | SHA-256 | Verification |
| --- | --- | --- | --- |
| Render receipt | `.scratch/typeset_pipeline/claude/bullarium-ro-0003/receipt.json` | `4630fab56b8bbfa1f62db653aba468655fe661502c4d542023eee3dcad929b3e` | Before and after |
| Frozen manifest | `.scratch/typeset_pipeline/claude/bullarium-ro-0003/frozen-manifest.json` | `5ae108677f3bc8075c77de79fb694c8871fc01898aa3af28b575fddffe6f9294` | Before and after |
| Raster run | `.scratch/claude-review/rasters-bullarium-ro-0003/review-run.json` | `6849911614a92c10885f9d9977d01a37f5ad78137723500b4ad9d831eaf671ef` | Before and after |
| Lane assignment | `.scratch/claude-review/bullarium-ro-0003/lane-06/assignment.json` | `08f183b4d57d3381d0e26304ebe6e688768da94b3d5a65f94376d00160399301` | Scope binding |
| Before verification record | `.scratch/claude-review/bullarium-ro-0003/lane-06/verification-before.json` | `824509a567a8ba3efb50765b64c57835f4086cd07e3eaa72c2d0a1ceb6b92eea` | PASS |
| After verification record | `.scratch/claude-review/bullarium-ro-0003/lane-06/verification-after.json` | `824509a567a8ba3efb50765b64c57835f4086cd07e3eaa72c2d0a1ceb6b92eea` | PASS; identical input hashes |
| Inspection ledger | `.scratch/claude-review/bullarium-ro-0003/lane-06/observations.jsonl` | `07f882d6f8ed5be84dbeaf1264264b0061bba60fafc3d1060079232471716e5e` | 45 unique observations |

## PDF outcomes

All 16 are printed acts in Latin, with the act date unresolved and omitted from the title line.

| Source ID | Kind | Language | Pages | Pages inspected | Marginal / note blocks (ledger) | PDF SHA-256 | Outcome |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `bullarium.volume-11.unit-0012.reading-order` | printed-act | `la` | 1 | 1 | 3 / 1 | `dc2158454037a9485a7eb01d176613d9d6ed577483716c6c674f21fed99a1e32` | PASS |
| `bullarium.volume-11.unit-0013.reading-order` | printed-act | `la` | 2 | 1, 2 | 8 / 1 | `86160245b20ec66c59f5f143e1f63b5da0e96ccd82892edf1064087d7a3e2b34` | PASS |
| `bullarium.volume-11.unit-0014.reading-order` | printed-act | `la` | 1 | 1 | 4 / 1 | `741276271dfad73c19135aad4909d2e39649e4825046ddf2da045371ce1dd274` | PASS |
| `bullarium.volume-11.unit-0016.reading-order` | printed-act | `la` | 6 | 1, 2, 3, 4, 5, 6 | 26 / 8 | `a1ed4c04e3e7c60a67db16436be956c40da2b4519b6dae33fb288be7db97e15f` | PASS |
| `bullarium.volume-11.unit-0017.reading-order` | printed-act | `la` | 2 | 1, 2 | 12 / 4 | `32900247e95a541f1b3faed7386ca9fcb75f3cc0ca6f64bb2e102b376cf05298` | PASS |
| `bullarium.volume-11.unit-0018.reading-order` | printed-act | `la` | 2 | 1, 2 | 7 / 2 | `33529ff679ebb2aa38eb7c39f87e5104cfbae9952cba13baf3eed78dc377fe93` | PASS |
| `bullarium.volume-11.unit-0019.reading-order` | printed-act | `la` | 2 | 1, 2 | 6 / 5 | `8672f7a3b685037a1dbcbeba23592411e92cd2cb8fea8e694d752288e8a4f4d9` | PASS |
| `bullarium.volume-11.unit-0028.reading-order` | printed-act | `la` | 2 | 1, 2 | 5 / 1 | `ca0b68aa8483d61ff439a9c02ec53999f31e048c6a415c6abb15415980dcbfcd` | PASS |
| `bullarium.volume-11.unit-0030.reading-order` | printed-act | `la` | 5 | 1, 2, 3, 4, 5 | 17 / 32 | `a0cd8f883107eb2c9f6192f9e812d8cb3ae7f1418898e35d7d8952a272837c19` | CHANGES_REQUIRED |
| `bullarium.volume-11.unit-0033.reading-order` | printed-act | `la` | 3 | 1, 2, 3 | 11 / 10 | `d39fd419f81318b5d8d79862574473e404ee0c0c61d48039ebdf4d30fc502ab8` | PASS (one uncertain locus) |
| `bullarium.volume-11.unit-0037.reading-order` | printed-act | `la` | 3 | 1, 2, 3 | 7 / 10 | `7cb2d929bc54d93758f89839dcd40e59097d51b542978e51e091e8cfa5ebc0f9` | CHANGES_REQUIRED |
| `bullarium.volume-11.unit-0038.reading-order` | printed-act | `la` | 4 | 1, 2, 3, 4 | 11 / 11 | `dbec35bdb2bbabb31effb57a9bb1919e2d8bd1132c5f50ca686b691dc4e0acf2` | CHANGES_REQUIRED |
| `bullarium.volume-11.unit-0039.reading-order` | printed-act | `la` | 5 | 1, 2, 3, 4, 5 | 20 / 4 | `0a3f398e4be9344411c34d6d73c2537d2a93800ae42cf40a1dd45c9f6982752e` | PASS |
| `bullarium.volume-11.unit-0042.reading-order` | printed-act | `la` | 2 | 1, 2 | 8 / 2 | `cb34b7c798abf7ce6864f26a90fce0bb7b5c91b36be8df8a73648d78599dc2a3` | PASS |
| `bullarium.volume-11.unit-0043.reading-order` | printed-act | `la` | 2 | 1, 2 | 7 / 2 | `68271aa2f19a0fb682ce2b0a3617c97f4391a9d11ea890daf9df998056800a5a` | PASS |
| `bullarium.volume-11.unit-0047.reading-order` | printed-act | `la` | 3 | 1, 2, 3 | 12 / 7 | `a110a638c96fe5a424d7bd977dbadc1f4211e2e3b3b63a4eb325f0a5d92bee0c` | PASS |

## Blocking findings

Each fusion was confirmed in the rendered page and in the derivative, where the note lines and body lines share one paragraph with no blank-line break.

1. `bullarium.volume-11.unit-0030.reading-order` page 1, column 2, lower half. Page-foot note `1 Bull. Ord. cil. legit de Clavasio (R. t.).` runs directly after the body words `cuius ullimodicti, et illis forsan annexo-` in the same paragraph (derivative LF 16766-16767).
2. `bullarium.volume-11.unit-0030.reading-order` page 1, column 2, foot. The body continuation `rum respeclive etiam quinquaginta* duca- lorum'auri de Camera ...` runs on inside the paragraph of note `3 Edil. Mail). Iiahet dioeces. brevialum, ... siciit paulo post (R. T.).` (derivative LF 16774-16775). The fused paragraph continues at the top of page 2 (`fruclus, redditus ... dux as-`).
3. `bullarium.volume-11.unit-0030.reading-order` page 3, column 1, upper third. The tail of note 3, `de qua unione vide supra Conslit. cccxxvil eiusdem Clem. Vili pag. 30 (r. t.).`, runs directly after the body words `simul vel successive (eliam in`. The note's head, `3 Nescio annon forel legendiiin: ...`, is a separate block just below (derivative LF 16950-16952).
4. `bullarium.volume-11.unit-0037.reading-order` page 1, column 2, lower third. The continuation of note 2 runs between the body halves `episcopi JIer])ipo-` and `lensis coUationi et disposilioni`. The continuation reads `len. ecdesiarum praedictarum; ideoque Iler- hipolensium furcl legendum ; sed salius nobis visiim fiiil addere liane vooern civi/ulis (R. t.).` Its head, `2 Edit. Main. habet extra muros Herhipo-`, is a separate block at the top of column 2 (derivative LF 20015-20019).
5. `bullarium.volume-11.unit-0038.reading-order` page 3, column 2, middle. The continuation of note 1 runs directly after the §5 body words `et aliarum regalium pcrsonaium defuncla-`. The continuation reads `una Cìemeiitis Vili Conslitutio ad ipsum riiilip- pum II spectans, sed isla de qua Iiìc agilm- non liabetnr (R. t.).` The body resumes in the next paragraph, `rum, applicavit quosdam annuos reddilus`. The note's head, `1 Sub liac dalà liabelur quidein in BuUario`, is a separate block higher in column 2 (derivative LF 20668-20678).

Additional finding for `unit-0030` (metadata, recorded alongside the blocking fusions): the displayed title `Ordiiies Alili lilaros prò de-` matches the frozen metadata. However, it is a hyphen-truncated marginal-summary fragment; the same words appear as the TAB-led marginal block `Ordiiies Alili ; lilaros prò de- '` in column 1. It is not the act's printed heading, `Suppressio nonnullarum ecclesiarum , ca- pcllarum ci prioratuum ... Ss. Mauritìi et Lazari '.`. The title/incipit is therefore not displayed unambiguously; the upstream title should be corrected when the reader is rebuilt.

## Per-document qualifications (non-blocking)

- **Running heads and signature marks.** Running heads (for example `An. C. 1604 CLEMENS Vili PP. 113 An.C. 1604`) appear on most multi-page source spans as separate blocks at the source page break, often mid-sentence or between the halves of a hyphenated word. Printer signature marks appear four times:
  - carried at the end of a note block: `Bull. Rom. — Voi. XI. 6` in `unit-0016` page 3, and `Bull. lìom. - Yo\. XI. 7` in `unit-0018` page 1;
  - as their own block: `Bull. Hom. — Voi. A7. 15` in `unit-0037` page 3, before the dating;
  - inline at the end of a body paragraph inside hyphenated `con- BuU. Rom. - Voi. XI. 10 / sanguineorum`, in `unit-0039` page 2, column 2.

  All are non-blocking qualifications under addendum item d.
- **Stray characters.** Stray one-character body-role blocks sit at page feet near notes or running heads:
  - `1` in `unit-0018` page 1;
  - `1`, `'`, `j`, `i`, `'` in `unit-0033` page 2;
  - `i` in `unit-0030` page 3;
  - `|` in `unit-0030` page 4;
  - `1.1` in `unit-0039` page 1;
  - `i`, `j` in `unit-0047` page 3.

  Single-glyph TAB-led speck blocks appear in `unit-0016` (pages 2, 3), `unit-0030` page 1, `unit-0033` page 1 (two) and `unit-0039` page 1 (two). All are recorded as literal OCR without inferred content.
- **Marginal placement.** Some marginal blocks are placed between the halves of a hyphenated word or mid-sentence, a little early or late; this is a qualification under addendum item d. Examples:
  - `unit-0016` page 2, `earum exequa* ...`;
  - `unit-0017` page 2, `poenas decer- na ...`;
  - `unit-0030` page 1, `Bcneìcu ec- clesiaslica ...`; page 2, `cumprimum ...` and `Kt benttGcia ...`; page 3, five blocks;
  - `unit-0037` page 2, `cum ini.ibi. ...`;
  - `unit-0038` page 2, `Addii.s am- ...`; page 3, `11.1 i.mion ...`;
  - `unit-0039` page 3, four blocks;
  - `unit-0047` page 2, `sexcnnii tempii! ...`.
- **Note-to-note merges.** Two such merges involve no body text: `unit-0037` page 2 (`1 Turbatissime ...` and `"2 l'aiticulani ...` share one note block) and `unit-0038` page 4 (`1 Vide super hoc ...` and `'i Praedicla duo ...`). They are qualifications, not item b defects.
- **Issuer lines.** Every issuer line matches the frozen metadata and names Clement VIII. Variants:
  - `Glemens Papa Vili.` (`unit-0019`);
  - `Clemens episcopus` (`unit-0030`);
  - perpetuity clause included: `Clemens Papa Vili, ad perpetuam rei memoriam.` (`unit-0028`) and `Clemens Papa Vili, ad futuram rei memoriam.` (`unit-0043`);
  - in `unit-0047`, the entire address protocol, `Gharissimo in Christo fillio nostro Philippe Hìspaniarum regi catholico Clemens Papa Vili. diarissime in Christo fili noster, salutem et apostolicam benedictiouem.` That is the metadata extraction carrying addressee and salutation into the issuer field. It is recorded as a qualification under the standing issuer ruling and flagged for the coordinator.
- **Uncertain locus (`unit-0033` page 1, column 1, §2).** The body line `canoni- riTA I r\ 1- • • . • • corum` carries the four-letter token `riTA` beside the §2 marginal. That marginal is rendered as its own block, `Causao Slip- si"rir°iVr"iK'fn- di meo collciiii.`, ending in a full stop, and `riTA` is not a recognizable word. However, the marginal's middle line is itself OCR-garbled and no word geometry was available, so I cannot rule out `riTA` as marginal residue. It is not counted as a fusion; it is flagged for coordinator decision, not guessed.
- **Literal OCR noise.** Short non-word runs inside body lines appear throughout, with the adjacent marginal summary complete as its own block (addendum item f). Examples:
  - `Sigismundus «, • ^,. >,. . , r, , • n ■ -.1 • ■ •` (`unit-0012`);
  - `^ ^" ^*'^ P*"*^ "°^""" pastoralis` (`unit-0014`);
  - `sancii t\ ... .p. n i- • r< Dommici` (`unit-0017`);
  - `_ ^ o r I 3. Nos igitur` (`unit-0019`);
  - `gra- ^ i i i- :i o` (`unit-0039`).
- **Selection gaps.** Several selections skip short LF spans, as disclosed by their source-note line ranges. For example, `unit-0028` skips LF 16382-16383, a note `I Haec verba praescntes Utteras omisit Miiin. (a. T.).` that appears to attach to the preceding act. These are upstream selection decisions and were not adjudicated here. On `unit-0030` page 2, the first note run is numbered 1, 2, 4-9, with no 3 visible; this was recorded and not adjudicated.
- **Sparse final pages.** The sparse final pages of `unit-0013`, `unit-0018`, `unit-0028`, `unit-0030`, `unit-0037`, `unit-0039`, `unit-0042` and `unit-0043` each open with genuine source text and close with the literal dating clause and `Dat.` line, sometimes followed by the source's own notes, before the project apparatus. None is a colophon-only page.
- **Literal dates.** Literal source dates are retained without repair, for example `Dat. die 31 iulii 1601` against `mdciv` in `unit-0037`. No calendar date was inferred.

## Limitations

These are literal uncorrected, uncollated historical OCR reading editions rebuilt from native OCR word order. This review is a hash-bound layout and visual review only. It does not collate words against the printing or a facsimile, authenticate historical wording, adjudicate provenance or rights, normalize dates, or verify automated printed-page labels. Block roles were confirmed against the tracked reading-order derivative, but no word coordinates were consulted. One marginal-versus-noise locus therefore remains uncertain, as stated above. Upstream canonical admission, source-fidelity and font checks were accepted within the assigned contract. No publication, installation or deployment is claimed or authorized by this report.

## Individual page evidence

Every row is an actual full-size inspection; all PNG hashes were verified before and after viewing. Ledger lines hold the full per-page observations, with the PDF hash and block counts.

| Source ID | Page | PNG SHA-256 | Status | Observation |
| --- | --- | --- | --- | --- |
| `bullarium.volume-11.unit-0012.reading-order` | 1 | `ac91a3e94e9e68a0b139032dbfd83151bd589aa5fb065d8bf0a47bf9cbdff71b` | PASS | Title/issuer/Latin match; 3 marginal blocks and 1 note separate; running head own block; dated closing and apparatus. |
| `bullarium.volume-11.unit-0013.reading-order` | 1 | `8afa28e29ad3406fe55bc0a844af029a34faea19c161f369d164fd06b9c2ba1f` | PASS | Title/issuer/Latin match; 6 marginal blocks, note and running head separate; non-word noise only. |
| `bullarium.volume-11.unit-0013.reading-order` | 2 | `e0b2682b9ff7861c0f4e0a21cbb79af5072f09b29111f88bdd5576fc93fd4fad` | PASS | Sparse source-bearing final page; 2 marginal blocks; dated closing before apparatus. |
| `bullarium.volume-11.unit-0014.reading-order` | 1 | `56199250e128e91fd9a6f2e97b1ae575b5ff38b8e2b166e43d286128bc9b28db` | PASS | Title/issuer/Latin match; 4 marginal blocks; dated closing; note after closing; apparatus col 2. |
| `bullarium.volume-11.unit-0016.reading-order` | 1 | `27df38be23e26a1748371b6630ec37e3b139a9b9b244b4fd6772e04aad1b40e4` | PASS | Four-line title/issuer/Latin match; 8 marginal blocks, note and running head separate. |
| `bullarium.volume-11.unit-0016.reading-order` | 2 | `c97fea0b9b9d76fd06200bea958d44b231de989acc2702dadcd6f3d6bf0b6d9a` | PASS | 7 marginal blocks (one mid-sentence), 2 notes, running head; constitution headings clear. |
| `bullarium.volume-11.unit-0016.reading-order` | 3 | `16799d392e8a6b112a2414315f44e6254fad385899ff8d62cb3072c78b8c95aa` | PASS | Chapters II-IV; 3 notes and 2 running heads separate; signature mark at end of note 2. |
| `bullarium.volume-11.unit-0016.reading-order` | 4 | `fe11bbabf33e14f795d11f122853067ed666bc05b37b84a766b8357bf073d390` | PASS | Chapters V-IX; running head own block at page break; no blocker. |
| `bullarium.volume-11.unit-0016.reading-order` | 5 | `5aba82081dfd0ccbb942253d82ca3d59d520a45c9d3c03e567bb011f796e638e` | PASS | 7 marginal blocks, 2 notes, 2 running heads all separate; body noise only. |
| `bullarium.volume-11.unit-0016.reading-order` | 6 | `df07e2fa8d78bf2e4388d87d47df3d48dec4a46f08b4bc2831c6cb10019327d8` | PASS | Source-bearing final page; 4 marginal blocks; dated closing before apparatus. |
| `bullarium.volume-11.unit-0017.reading-order` | 1 | `b456e2b120a06c5ec2c45924663d4e6265d59bae16869dc63bb4c234204c33a6` | PASS | Title/issuer/Latin match; 6 marginal blocks, 3 notes, 2 running heads separate; non-word noise. |
| `bullarium.volume-11.unit-0017.reading-order` | 2 | `6273655c84aa48543d9fe8ec057ee592a85ac109620596edae558b551abd9f7a` | PASS | 6 marginal blocks, note, running head separate; dated closing and apparatus. |
| `bullarium.volume-11.unit-0018.reading-order` | 1 | `3b8701c3a066b88172487f87944e244938784bec3667346d2bb049152d32954d` | PASS | Title/issuer/Latin match; 5 marginal blocks, 2 notes (signature mark in note), stray `1`, running head. |
| `bullarium.volume-11.unit-0018.reading-order` | 2 | `c9972a17978b407959b245e3b03f10330e6f790aac53216b0c0e7ea5d948c11d` | PASS | Sparse source-bearing final page; 2 marginal blocks; dated closing. |
| `bullarium.volume-11.unit-0019.reading-order` | 1 | `7a26169b89bf0bcc6b4f83ff5c82c1242f88ed57ea46af883233ff6b2a30f095` | PASS | `Glemens Papa Vili.` matches metadata; 2 marginal blocks, 2 notes, 2 running heads separate. |
| `bullarium.volume-11.unit-0019.reading-order` | 2 | `b53b0656a2d5cd62105a4b8231edf048909cde4648d77c51ad56bbab5a592852` | PASS | 4 marginal blocks, 3 notes, running head separate; dated closing and apparatus. |
| `bullarium.volume-11.unit-0028.reading-order` | 1 | `bfbe8ef00a05e109bf2b287e52c043f8aa0d5c9021481d88d7a9797c09fb3fdb` | PASS | Issuer with perpetuity clause matches metadata; 5 marginal blocks, note, running head separate. |
| `bullarium.volume-11.unit-0028.reading-order` | 2 | `a7c3b5e924a6e30be669ac0c57dc7f7595783d69ca0db92a0d835bc7cb75f8ba` | PASS | Sparse source-bearing final page; dated closing before apparatus. |
| `bullarium.volume-11.unit-0030.reading-order` | 1 | `b0058c1401df5407071b7099202df183f5241fde6439c6b21097a0f6f52b1f12` | CHANGES_REQUIRED | Col 2: note 1 fused after body `annexo-`; body continuation fused into note 3 paragraph. Title is a truncated marginal fragment. |
| `bullarium.volume-11.unit-0030.reading-order` | 2 | `86750cfc179d24d154627c5187999515b7a157c2392289304677e24c7c561fc4` | PASS | 4 marginal blocks, 11 separate notes, running head; opening lines are tail of page-1 fused paragraph. |
| `bullarium.volume-11.unit-0030.reading-order` | 3 | `9f574336f3d21f077c4e3a665745260f794f961449d104ef218af247d853c65d` | CHANGES_REQUIRED | Col 1: note 3 tail `de qua unione vide supra ... (r. t.).` fused after body `(eliam in`. |
| `bullarium.volume-11.unit-0030.reading-order` | 4 | `6b5b0370cf23c9ada116f5fd8b7a2599304921b75a3b88c1637a32a00223c8d6` | PASS | 2 marginal blocks, 3 notes, stray `|`, running head separate; no fusion. |
| `bullarium.volume-11.unit-0030.reading-order` | 5 | `8f8c4eff1cd3bd3708fdae594ce50938549a965d5f0bea86ddaec839f7811bbb` | PASS | Sparse source-bearing final page; sanctio, dated closing, 3 separate notes, apparatus. |
| `bullarium.volume-11.unit-0033.reading-order` | 1 | `7105647d26196a9b5c1db8740a0262aafeba5090e5a7716e679d1c48d2c4e54d` | PASS | Title/issuer/Latin match; 6 marginal blocks, 4 notes, running head separate; `riTA` in §2 body line uncertain. |
| `bullarium.volume-11.unit-0033.reading-order` | 2 | `60e48b7be331ba20fde6d0d1e9259600c4d62f5226e263dfcb2d2dcfb2de4461` | PASS | 4 marginal blocks, 2 notes, five one-character specks, running head separate. |
| `bullarium.volume-11.unit-0033.reading-order` | 3 | `59ef73be95024cf92c2918c3f0ad9207e13b4859268bb72a4d960acbe36e54dc` | PASS | Source-bearing final page; dated closing, 4 separate notes, apparatus. |
| `bullarium.volume-11.unit-0037.reading-order` | 1 | `5722337c0ccf2924f37f95ca7eca2bbebd38333e47ec72f0a2029b788c491eb1` | CHANGES_REQUIRED | Col 2: note 2 continuation fused between body `JIer])ipo-` and `lensis coUationi`. |
| `bullarium.volume-11.unit-0037.reading-order` | 2 | `66b681cf4f53784166ed5f58341eb34ee8933abec842b22447b707209687ed39` | PASS | 3 marginal blocks, 7 notes (one note-to-note merge), 2 running heads; no body fusion. |
| `bullarium.volume-11.unit-0037.reading-order` | 3 | `a11b9b78ee07b442c284c6b55e236062094058d61cb3336cbe21942b8543303d` | PASS | Sparse source-bearing final page; 2 marginal blocks; signature mark own block; dated closing. |
| `bullarium.volume-11.unit-0038.reading-order` | 1 | `04309ebfa2a8afa085dddcbbdc9c6e26c1a3e7b45248e1d877eda441e365264a` | PASS | Four-line title/issuer/Latin match; 2 marginal blocks, 2 notes, running head separate. |
| `bullarium.volume-11.unit-0038.reading-order` | 2 | `cecbda585524e8eff131bac2259515553b79143fe5e7d4d647372830afd85779` | PASS | 4 notes, 3 marginal blocks, 2 running heads separate; body noise only. |
| `bullarium.volume-11.unit-0038.reading-order` | 3 | `c2f97fcf4d60e716a1573a4ec99924730e582000e5a371eb35f1c7cd57c18a0d` | CHANGES_REQUIRED | Col 2: note 1 continuation fused after §5 body `defuncla-`. |
| `bullarium.volume-11.unit-0038.reading-order` | 4 | `8232650e731962f64ee9ad8ba36cf5f7888d05991c70ec49a9ddde772f0ea89a` | PASS | Source-bearing final page; 3 marginal blocks, notes separate (one note-to-note merge); dated closing. |
| `bullarium.volume-11.unit-0039.reading-order` | 1 | `f4641be56af13b1d6ec7e6127b721db5c34d90eceaa09bcc30995804b88047d1` | PASS | Title/issuer/Latin match; 6 marginal blocks (2 specks), 2 notes, 2 running heads separate. |
| `bullarium.volume-11.unit-0039.reading-order` | 2 | `4db63cf9ed70a60bdd1af43a08dc3baa0e01ec45c591ef31b0c41c4085efb1cc` | PASS | Marginal, note, running head separate; inline signature mark in body (qualification). |
| `bullarium.volume-11.unit-0039.reading-order` | 3 | `1ca44ed8d630a6fda4811c461ee447c6c601a98025c0c7e16c41b8c80433156a` | PASS | 7 marginal blocks separate (four placed mid-sentence); running head; noise only. |
| `bullarium.volume-11.unit-0039.reading-order` | 4 | `85815da2f10215539fa9e87f9860a986aafa709c6168c22dd3d3b3da5f713d8c` | PASS | 5 marginal blocks, 2 running heads separate; garbled §11 body OCR. |
| `bullarium.volume-11.unit-0039.reading-order` | 5 | `eb159985d9542ad542cc6b9d5693a145a5ebaa9b7b658c077a914691d4e8a817` | PASS | Sparse source-bearing final page; marginal, dated closing, note, apparatus. |
| `bullarium.volume-11.unit-0042.reading-order` | 1 | `c67f346ae7ca01b3232147182a30310381cf0719952c3814926a99a2dfaa1890` | PASS | Four-line title/issuer/Latin match; 8 marginal blocks, 2 notes, running head separate. |
| `bullarium.volume-11.unit-0042.reading-order` | 2 | `d1f142293bf9a27a21708345c5f410a673b3c71f06584c5c2a69b3a6e649a414` | PASS | Sparse source-bearing final page; §7 and dated closing before apparatus. |
| `bullarium.volume-11.unit-0043.reading-order` | 1 | `45ab6198c573f76f00343f920bc228df369e487059071e49c2b9f8ae0552125a` | PASS | Issuer with perpetuity clause matches metadata; 7 marginal blocks, note, running head separate. |
| `bullarium.volume-11.unit-0043.reading-order` | 2 | `6c1817adc9a1c0447292fb60067796033cd5fe97ba65da8917aa73be0c22c6a4` | PASS | Sparse final page: dated closing and source note before apparatus. |
| `bullarium.volume-11.unit-0047.reading-order` | 1 | `160d8ba8178a4859ddefc72b39319598d163137093c5767fd6b28cf73f46eae2` | PASS | Seven-line title matches; issuer field is full address protocol (qualification); 4 marginal blocks, 2 notes, running head. |
| `bullarium.volume-11.unit-0047.reading-order` | 2 | `d902ef1967c8eac19fb0d3a0e77341809b91b696c775bccca21331e4b1ca9dfc` | PASS | 5 marginal blocks, 2 notes, running head separate; body noise only. |
| `bullarium.volume-11.unit-0047.reading-order` | 3 | `d7d7019c3e06f76a7d4e4cccb9926626d5e50c4f3d261c7a995037457eebe3f1` | PASS | Source-bearing final page; 3 marginal blocks, notes separate; dated closing, note, apparatus. |
