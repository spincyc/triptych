# Independent source-retention review — 2026-09-17

**PASS after correction. No remaining blocking source-retention finding.** This verdict covers source identity, retained bytes, bounds, derivation, rights records, the Cummiskey verification delta, and the new third-party notice. It does not accept either liturgical publication, its research, appointment claims, interpretation, or source sufficiency.

Reviewed branch: `feature/codex/propers/homily`; HEAD: `af9b2d10a98a6aac2ce44cc84d6358ede8e630e8`. Reviewed state includes uncommitted additions. Completed at 2026-09-17T19:52Z.

The scope is all 124 new files under `src/sources/works/`, plus the changed Cummiskey `post-pentecosten-17.toml` and `THIRD_PARTY.md`: 109 manifests, 16 payloads, and one notice. The manifests comprise 16 works, 24 editions, 24 artifacts, 12 segments, and 33 passages including the changed existing passage. The companion `final-path-hashes.json` lists every exact path and SHA-256. Its file hash is `29662e4fdee83c8dbc78bc45b7723e14cffb5e4f0f5b76ad567edfd5b93d770b`; the equivalent `final-snapshot.sha256` file hash is `f5c59e4c7bfe05769fe414b3260d9933dd2bd9744c2ee0b1e0ca816a4185f7bd`.

## Finding and disposition

**P2, closed:** All 16 new `work.toml` records initially omitted `composed` and `composed_basis`, contrary to the composition/edition distinction and explicit-unknown rule in `guidance/sources.md`. Root added `composed = "unknown"` and scoped bases distinguishing original composition, compilation, and institutional-calendar inception. Re-review confirmed that these are cataloguing limits, not claims that historical dating is impossible, and that no printing or acquisition date was substituted. These 16 files are the only changes between initial and final review snapshots. All payload and other manifest hashes stayed unchanged. Exact affected paths are enumerated by the companion JSON's `record_type = "work"` entries.

No new duplicate work was found in the bounded alias searches. The expressly disclosed, pre-existing two identities for Aquinas's Ephesians commentary remain outside this change's scope.

## Evidence checked

| Source group | Independent checks and disposition |
| --- | --- |
| CCEL NPNF 1.2, 1.5, 1.6, 1.7, 1.10, 1.11 | Six complete offered deliveries match their hashes and sizes. Front matter, terminal material, rights headers, constituent titles, and every new line-range boundary were inspected. Container ownership stays distinct from constituent works. Digital dates do not pretend to authenticate the undated reprint imprints. Each file expressly declares public-domain rights; the retained credits and historical editorial matter remain. A bounded notice search found no additional modern copyright notice in these files. |
| Gregory | EPUB has 42 content spine members: index, preface, and 40 homilies. Text extraction replays exactly. EPUB metadata and About page expressly supply CC BY-SA 3.0 and contributor Mizardellorsa; the manifest and `THIRD_PARTY.md` preserve attribution, source/history route, license, and change notice. The three facsimile pages match parent pages 40–42, including all six image XObjects. Visual review confirms PL columns 1153–1158, complete sections 1–6, incidental surrounding material, and incomplete section 7. Exact historical impression remains unidentified as stated. |
| Aquinas 1857 Pauline volume | Title image confirms Tomus II, H. Dessain, Leodii, MDCCCLVII. All 456 derivative pages match parent pages 2–457 in media boxes, rotations, content streams and 459 compressed XObject streams. Only the opening Google wrapper is excluded. OCR is exactly the parent bytes from offset 3010. Printed pages 312, 315 and 317 establish the chapter/lecture boundaries at derivative pages 316, 319 and 321. |
| Aquinas Parma 1863 | Title image reads MDCCCLXIII; the catalog's 1852 date is correctly rejected. Three derivative pages match parent pages 11, 576, 577, with six XObject streams. Visual review confirms all chapter 55 on printed pages 556–557, including its continuation beneath the CAPUT LVI running header. The measured 118,531,843-byte whole scan is remote; full OCR and bounded images are retained. |
| Jerome and Gutenberg Summa III | Jerome revision 263922 and its Migne 1845 attribution are supported by the exact XML input. Existing extractor replay matches the retained Latin. Generated locators, surviving numeric furniture, and absence of image collation are disclosed. Gutenberg marker extraction also replays exactly, retaining the electronic editor's revision notice and producer credits. Questions 1–90 and the specified III.79 answer/reply boundaries are present. |
| Pustet and Cummiskey | Pustet leaf n427 is printed page 342 and visibly continues the Sunday before Ember Wednesday; the page's running header is correctly qualified. Cummiskey's three orations were visually compared with PDF pages 440–442 and the TSV: wording, historical spelling and abbreviated conclusions agree. Existing scan hashes match the new note. The 1962 Latin correspondence is visible at PDF pages 480–481. Leaf/PDF numbering and historical-translation limits are correctly stated. |
| Modern Ordos | Both full local HTML responses match recorded hashes/sizes. Source-local dated entries support the factual metadata; no HTML payload is registered for distribution. Institutional scope and offline limitations remain explicit. No publication appointment decision was made in this review. |

The historical page derivatives contain no added modern editorial wrapper; PDF metadata is empty or identifies pypdf only. The retained Gregory EPUB is separately licensed. Successful downloads were not treated as a rights grant. The revised `THIRD_PARTY.md` preserves the boundary from Triptych's CC BY 4.0 license.

Primary rights references checked during review: [CCEL's copyright policy](https://www.ccel.org/about/copyright.html), [Gutenberg's item 19950 record](https://www.gutenberg.org/ebooks/19950), [CC BY-SA 3.0 terms](https://creativecommons.org/licenses/by-sa/3.0/legalcode), and [Princeton's record for the Parma volume](https://commons.ptsem.edu/id/sanctithomaeaqui14thom). CCEL's general warning about special copyrighted contents was considered alongside these exact files' rights headers and inspected contents; it was not generalized into permission for unrelated CCEL material.

## Checks and separate consumer drift

Commands were run from the repository root. Review-only scripts, logs, and rasters are under `.scratch/source-retention-cold-review/`.

| Exact validation command | Exit | Result |
| --- | --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.scratch/tlm-source-retention/pylib python3 .scratch/source-retention-cold-review/check.py` | 0 | 126 final snapshot hashes; 16 payload sizes/hashes; 10 acquired evidence inputs; four text derivations; three complete PDF derivative comparisons; composition corrections. |
| `python3 scripts/migne_transcribe.py .scratch/tlm-source-retention/jerome-daniel-export.xml --unit page --out .scratch/source-retention-cold-review/jerome-replay.txt` | 0 | 81 lines, revision 263922. |
| `cmp .scratch/source-retention-cold-review/jerome-replay.txt src/sources/works/jerome/commentaria-in-danielem/editions/1845-migne-pl-25-wikisource/artifacts/latin-text-3fe4ba4f/source.txt` | 0 | Byte-identical. |
| `sha256sum -c .scratch/source-retention-cold-review/final-snapshot.sha256` | 0 | All 126 reviewed files unchanged at final check. |
| `tools/tpt source-library validate` | 1 | After composition correction: 19 stale consumer fingerprints only; no source-record errors. |

The earlier, pre-correction validator reported valid counts of 2726 artifacts, 987 editions, 5159 passages, 89 segments, 722 works and 2665 bindings. The **final exit 1 is not a source-retention failure**. The changed source ancestors require independent consumer review and refreshed pins:

- `src/gpt/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost/research/source-bindings.toml`: entries 12, 13, 14, 15, 16, 21, 22, 24, 25.
- `src/gpt/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s51-twenty-fifth-sunday-in-ordinary-time-year-a/research/source-bindings.toml`: entries 8, 13, 17, 18, 19, 20, 21, 22, 23, 24.

Those counts describe this validation instant; the active publication lanes own their resolution. No publication interpretation or authored research was read or combined. This review inspected source-local boundaries and material identity/locus images, not every page of every acquired work, and does not promote OCR or transcriptions to whole-work collation. No source, publication, inventory, staging, or commit mutation was performed by the reviewer.
