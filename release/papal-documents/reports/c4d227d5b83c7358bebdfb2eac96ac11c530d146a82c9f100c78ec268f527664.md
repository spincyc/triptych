# Independent cold review: E supremi, French

**PASS** — exact candidate `acta.ass.036.ass-036-l005778` / `fr`, six pages. All six reader pages and native artifact pages 151–163 were individually viewed. All twelve historical page-foot note groups have explicit paragraph block boundaries on both sides. No clipping, overlap, missing-glyph boxes, body-note fusion, sustained nonsense or materially unreadable passage was observed.

Source-readonly review of the exact OCR-derived candidate only. Native geometry is not original-print glyph, full lexical or translation collation. No historical authentication, lexical correction, installation, publication or deployment is claimed. No producer or previous visual judgment was inherited; the Latin sibling review was consulted only for JSON format.

## Exact evidence

| Item | SHA-256 |
| --- | --- |
| Scope pins | `01c23a6fc4456089f7bd00f5956c937963d32914b7aa4b4dd5ca0fdce49128d6` |
| Producer manifest and frozen snapshot | `ca12f96e8dbec6dc938a69d1b92c02b469c70b7225e4d810c719beacd8fcf488` |
| Producer receipt | `fce1af199380be667fbc94f0cecedc094f27f2c211098fc36ee193096d639302` |
| Six-page candidate PDF | `fbc767396bb1738328b8e04f028b4294d05d14c43a7cdc282fcf5500921007eb` |
| LF-only source derivative | `d424eba6825acd5874b21832a04910de33bd4b5e74635b5fe87c421a1954a8b6` |
| Partition spec | `35ea77e60c748dd146485b969eeea169ef2a7f586687aa73d463e1ccdb6e0b2d` |
| Unchanged text parent | `2e2ac41b82e92ef6a68a6bd1d4c768933ebadf42a8c74f3103755ac13fd762cb` |
| Whole native ASS 36 OCR PDF | `4d5577b47b26023818a4219fc9e089c3425a066056638aa2c16013990fd87d27` |
| Native excerpt: artifact pages 151–163 | `e228971dc3097f3c97afd2ef4d009ea6afa9991fb274b0e2c5f1f0b88bd6f67f` |
| Tracked `scripts/_papal_source_notes.py` | `a0b31d45f498bec3a12a29cdff28da38f3e01cc02c50e5de8a9a65e4a82a9d57` |
| Tracked `scripts/_typeset_papal.py` | `1c14411ed430d51605af66a37ddcb6d758d0eb67c9e8d56a1d4d875e9a0ba146` |

The complete producer manifest and frozen snapshot are byte-identical, including the whole candidate document row. Receipt identity, language, source/artifact/segment, physical ranges, render revision, six-page extent and PDF hash agree. Independent `read_manifest`/source validation checks current on-disk artifact and segment controllers, exact payload, rights basis and French edition. Current acta/classic manifests remain intentional predecessor rows; their original source ranges match the partition spec. `controller-checks.json` records those intended deltas; its false whole-row comparisons are the expected pre-install state, not candidate/frozen inequality. The installed row retains its prior source keys and PDF `6349fbbb40e2aa0342b0ffb92574ad65d2f1f0a803915477aa5d254305c62435`, which differs from both this candidate and the supersession receipt's prior typography PDF `6a66e045bd3be689d2e34ea7be5f1725cd9ee24cb43ad9c83ad284673c74b79c`. No installed bytes were accepted or changed here.

## Actual visual coverage

| Reader page | Direct observation |
| --- | --- |
| 1 | Pius X / 1903-10-04 / French identification; source parenthetical, address, PIE X PAPE, salutation and incipit retained. Anselm note separately interrupts `igno-` / `rer`. |
| 2 | Three citation groups remain separate from body, including `en-` / `core`. Both columns continue normally. |
| 3 | Chrysostom-related and Apocalypse note groups stay separate. Isolated OCR forms `Chinisi` and `eieue` appear within readable sentences. |
| 4 | Six-reference and Tim/Rom/Thren groups remain separate; body resumes around notes and across columns. |
| 5 | Is/Cor/Ibid/Eccli/Acts notes span the column break with intact membership and a separate boundary before `l'approbation`. Romans note separately interrupts `il sera` / `manifeste`. |
| 6 | Substantial source body, Rome / S. Pierre / 4 octobre 1903 dating, PIE X PAPE and five closing notes precede source/rights apparatus. Final project-license continuation appears in the right column on this same source-bearing page. |

Every native excerpt page was directly viewed as an original-size full-page PNG from `tools/pdf-review`, without using a contact sheet or OCR proxy for visual coverage. These images represent a text reconstruction. Artifact ordinal 152 has a corrupted visible page label; artifact ordinals are used here without inferring original printed pagination. Native page 151 shows the neighboring Italian closing before the separate French parenthetical/address/issuer/salutation/incipit. Native page 163 shows the French closing, dating, signature and final citations. The existing selected extent excludes the unrelated issue footer below the notes on native page 161; this derivative adds no new furniture exclusion.

| Native artifact page | Parent LF note bounds | Visibly separate page-foot material |
| --- | --- | --- |
| 152 | 5832 | Anselm citation |
| 153 | 5871–5874 | Four scriptural references |
| 154 | 5913–5916 | Four scriptural references |
| 155 | 5954–5960 | Seven scriptural references |
| 156 | 5998–6002 | Four scriptural references plus Chrysostom |
| 157 | 6043 | Apocalypse reference |
| 158 | 6080–6085 | Six references |
| 159 | 6125–6127 | Tim/Rom/Thren references |
| 160 | 6165–6170 | Six references |
| 161 | 6208–6214 | Is/Cor/Ibid/Eccli/Acts, internal blank lines preserved |
| 162 | 6257 | Romans reference |
| 163 | 6294–6298 | Five closing references after source subscription |

Notes interrupt some words or sentences in source order. Both outer LF paragraph boundaries are independently checked in the source bytes and confirmed visually in the PDF. The interruption alone is not fusion. Notes were not moved into invented modern footnotes. Literal OCR spellings, name/glyph/reference-number noise, punctuation and hard-line word divisions remain non-blocking limitations. No sustained nonsense or material unreadability was found.

## Checks

- `tools/typeset-papal check --manifest .scratch/encyclical-notes-05-finish/manifest.json --document acta.ass.036.ass-036-l005778 --json`: exit 0, one valid selection, cache disabled.
- `tools/papal-source-notes check` with exact scope spec and source paths: exit 0, twelve groups, 550 physical lines, 29,335 bytes. Separate direct LF reconstruction equals retained derivative. All selected non-LF bytes and order are preserved: SHA-256 `0ebabd9d89e278b26c0cf2f24a649e7af61ca0eac90b2b0a90b7b098505d4bc2`. All twelve groups pass both-side block assertions. Current tracked helper used without copying.
- `scripts/_typeset_papal.py:pdf_body_fidelity`: pass, `pdf-raw-source-aware-line-hyphen-nfkc-v3`, 28,497 source / 22,955 normalized characters, zero added layout hyphens, source on all pages 1–6.
- `pdfinfo`: exit 0, six unencrypted letter pages, edition title/Pius X/French metadata and tracked render timestamp match. `pdffonts`: exit 0, all four Latin Modern fonts embedded, subset and Unicode mapped.
- XeLaTeX log inspection found no fatal error, missing-character, overfull/underfull or warning match; receipt warnings empty. Visual inspection confirms ordinary left-then-right column flow.
- `tools/pdf-review --jobs 1`: exit 0, six reader and thirteen native page rasters generated in this lane. `raster-evidence.json` records paths, dimensions, actual PNG MIME and hashes. Review-run SHA-256 `d747b14af83654efed347460842dbc6b537fcec1785e2ba6382ebaebd8933f23`.
- Coordinator's uncached whole-library validation cited, not redundantly repeated: `.scratch/notes05-cold-recovery/source-graph-check-2.log`, SHA-256 `7d1df13bc67497cfc6da7d8158578371e75466d67d69f91ffd7ed0692f5f8ad0`, exit 0, valid source graph. This lane independently performed the narrower source/controller checks above.

Detailed evidence: `observations.md` contains incremental actual observations; `mechanical-checks.json` contains exact paths/hashes/commands/results and note boundaries; `controller-checks.json` records intentional predecessor deltas; `manifest-row.json`, `receipt-row.json`, `scope-row.json` and `raster-evidence.json` retain bounded evidence. No subject source, helper, release, inventory, shared manifest, installed PDF or Git state was written. Only this candidate acceptance gate is resolved; coordinator integration remains outside this lane.
