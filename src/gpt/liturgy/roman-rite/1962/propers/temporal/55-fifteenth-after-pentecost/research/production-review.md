# Production review


## Post-acceptance revision answering every standing finding, 2026-10-01

### Findings and dispositions

The standing findings register has no undisposed advisory, observation or
escalation. The generated chronology was refreshed for the shared display
repair: the Gospel's A.D. 27 and Communion's A.D. 28 now say `(derived)`, and
approximation markers remain visible. These figures are generated from the
corpus's source-bound conversion, not independent biblical dates supplied by
this revision. The traditional attribution, composition and event relations
remain separate. Earlier source-lane statements in `scope.md` describe their
inspection state; the dated chronology revisions record later additions.

### Layout repairs

No layout adjustment was needed. The existing page counts and declared page
contracts hold. All page contact sheets were inspected; full-size inspection
covered both page-2 date dossiers. No clipping,
overlap or displaced date content was found in those inspected pages.
The generation timestamp is `2026-10-01T22:25:03Z`; the new contribution
records GPT-6, requested high effort, and explicitly unexposed runtime details.
Prior contributors and the original workflow provenance are preserved.

### Artifacts

These are the completed build artifacts, not installation claims. Paths are
relative to the repository root.

| Artifact | Pages | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| `build/gpt/liturgy/roman-rite/1962/propers/temporal/55-fifteenth-after-pentecost-synthesis.pdf` | 12 | 412014 | `781d6296394c38f58a49ea536462ece957f99ba3f7cfe536c7bd00178175a5d0` |
| `build/gpt/liturgy/roman-rite/1962/propers/temporal/55-fifteenth-after-pentecost.pdf` | 16 | 459060 | `a02a5ab3821cf20d311d110a92db1fc645970954e17598a7322d167cb1b90017` |
| `build/web/gpt/liturgy/roman-rite/1962/propers/temporal/55-fifteenth-after-pentecost.md` | — | 73989 | `9c38cf85aab687b96e4d3a2636be56ff8a44e00743d1e7b7723cf641d89281d1` |

This legacy schema-1 leaf has only the full and concise outputs. Its artifact
identities are recorded above; no schema-2 homily or receipt was invented.

### Checks run

- `proper-chronology record` and `annotations`, each `--write` and `--check`: passed.
- Normal `make doc` for every declared edition: passed, including the anchor
  and generation-metadata gates. Settled logs have no warning, undefined
  reference, overfull/underfull box or rerun request.
- Edition-specific content checks: passed. All default
  `check-content-preflight` checks and the separate `provenance-matches-run`
  check against the original recorded run identity: passed.
- Artifact checks through `check-proper-components` for both editions: passed.
- `source-library validate`: passed.
- Web generation with the pinned Markdown 3.10.3 environment and
  `check-web-edition`: passed.
- `pdfinfo`, full text extraction and font inspection: succeeded; every font
  is embedded. The bounded `pdf-review` helper rendered every page.
- Scoped `git diff --check`: passed.

The exact command/exit records and build, preflight, artifact, web and raster
logs are retained under `.scratch/recovery-leaf-gpt/`. The raster set is under
`build/gpt/liturgy/roman-rite/1962/propers/temporal/55-fifteenth-after-pentecost-recovery-review/rasters/`.

### Review boundary

This entry records the recovery author’s checks and visual inspection. The
coordinator has dispatched an independent content, visual and web review of
the exact hashes above; that review is pending at this entry. Earlier accepted
workflow seals remain historical and were not restamped as current acceptance.
Installation, publication projections, release bindings and deployment remain
with the coordinator. No source, rights, appointment or local-calendar
limitation was broadened by this repair.
