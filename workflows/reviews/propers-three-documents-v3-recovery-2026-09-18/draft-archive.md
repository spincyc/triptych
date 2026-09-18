# Unfinished pagination drafts: exact-byte archive

Archive-only recovery, 18 September 2026. Both proposals remain **unrendered and
unreviewed; no new acceptance**. The revised pagination requirement remains
**OPEN**. No v3 run, content adoption, new source verification, build, installation
or publication approval was performed. Historical v1 records were not rewritten.

## Scope and integrity

- Preserved **63 unchanged payloads, 520,334 bytes**: 1962, 12 files / 96,807 bytes;
  U.S. 2011 postconciliar, 51 files / 423,527 bytes, including its own adapter candidate.
- Every payload gained only a terminal `.draft` filename suffix; byte-for-byte
  comparisons and SHA-256 checks passed. All original draft labels and contents remain.
- Each owner has three new wrappers: `README.md`, `manifest.json`, `SHA256SUMS`.
  The manifests identify source roots, original relative names, archived names, sizes,
  hashes, unreviewed status, exclusions and scratch-only restoration instructions.
  Checksums distinguish original payloads from new wrappers and do not hash themselves.
- Inventoried 66 input files. Excluded only three transient postconciliar scripts:
  `count-drafts.py`, `expand-commentary.py`, `query-chronology.py` (8,388 bytes).
  No scripts were executed from the input drafts, and no source files were deleted.
- Privacy screening found no machine-private absolute/runtime paths, current machine
  or user identifiers, credential markers, session UUIDs, numeric network addresses
  or credential-bearing URLs in retained payloads or archival wrappers. No symlinks
  were retained. Repository-relative scratch paths and public source locators remain
  unchanged. This is a bounded identifier screen, not a new scholarly/rights approval.
- All **297 preexisting owner files and installed publication artifacts** in the
  before/after snapshot remained byte-identical. All original draft inputs also
  remained unchanged. Each family retains only its own proposal and research inputs.

## Seal-discovery boundary

Inspected `scripts/_proper_study.py` and `scripts/_proper_components.py` before
copying. The default historical research seal scans `research/`, `propers/`,
`instance/` and declared/bound source owners; none includes these evaluation archives.
Content seals follow the unchanged literal include graph and declared component
references. Visual discovery recursively admits only `.tex`, `.sty`, `.cls` and
`.bib`, plus the unchanged component manifest and actual recorder inputs. `.draft`
does not match those suffixes. The new `.md`, `.json` and extensionless wrappers
are not selected either. Web seals hash the existing built canonical Markdown.
No import, dependency declaration, scanner or sealed field was changed.

## Historical comparisons

For each row, ran the actual historical-default command before and after copying:

```sh
python3 scripts/_proper_study.py seal --provider gpt --document <owner-id> --review <scope>
```

No `--review-contract proper-study-v3` was supplied. Compared the complete parsed
output, without dropping fields, with `review_inputs` in the historical engine
result. All **12/12 comparisons passed before and after**; all twelve result files
also matched their live `build/tpt-runs/<run>/results/` copies byte-for-byte.
The result paths below are relative to each owning leaf's
`evaluations/proper-study-results/<run>/`. These are identity checks, not re-reviews.

| Owner / historical run | Engine result | Before | After |
| --- | --- | --- | --- |
| 1962 / `80a724fb8410dc3d` | `research-review-0000.json` | MATCH | MATCH |
| 1962 / `80a724fb8410dc3d` | `study-review-0002.json` | MATCH | MATCH |
| 1962 / `80a724fb8410dc3d` | `synthesis-review-0002.json` | MATCH | MATCH |
| 1962 / `80a724fb8410dc3d` | `homily-review-0002.json` | MATCH | MATCH |
| 1962 / `80a724fb8410dc3d` | `visual-review-0002.json` | MATCH | MATCH |
| 1962 / `80a724fb8410dc3d` | `web-review-0003.json` | MATCH | MATCH |
| postconciliar / `8f4e6454c021280a` | `research-review-0002.json` | MATCH | MATCH |
| postconciliar / `8f4e6454c021280a` | `study-review-0002.json` | MATCH | MATCH |
| postconciliar / `8f4e6454c021280a` | `synthesis-review-0001.json` | MATCH | MATCH |
| postconciliar / `8f4e6454c021280a` | `homily-review-0001.json` | MATCH | MATCH |
| postconciliar / `8f4e6454c021280a` | `visual-review-0001.json` | MATCH | MATCH |
| postconciliar / `8f4e6454c021280a` | `web-review-0001.json` | MATCH | MATCH |

For reproducibility, these are SHA-256 values of each complete seal serialized
with Python `json.dumps(value, sort_keys=True, separators=(",", ":"))`.
They are comparison fingerprints, not newly issued engine approval seals.

| Owner | Scope | Unchanged comparison fingerprint |
| --- | --- | --- |
| 1962 | research | `e09590e975ba4d4c9bf764b4de68175256bc7f63cd72c03917b0d06d327810f0` |
| 1962 | study | `86a61b990cd73723e66e3aaeb91ff08c8568cf782443840ec7ba9688694a36cb` |
| 1962 | synthesis | `6373f5ade2314d4a109641a291bd5b41869bc51370b468ebde4e8e1220faabb8` |
| 1962 | homily | `6c98960ebd49927f7daa94e6b6cafa560958cb8026d043ae20b6fc348e46c406` |
| 1962 | visual | `0eb05d48b646b0f89bd566f562f3bf3eec485d27488db7856fd3f6bee14a51d2` |
| 1962 | web | `63ba53b0556b1e4f23aaccfb04d9055e8a5487c8a7b522926a42d003dbf38e26` |
| postconciliar | research | `4f55ca04949c1890ea7d0c041406b0818706cf137abf25eb3dafb8f29ed6d261` |
| postconciliar | study | `7dbe67ddaa0544c01e974b422ad34918ad23fb131301d49a1c8873578f08f52c` |
| postconciliar | synthesis | `0e6d26bacd1a50b00b135592dba8548a71c57c16de29e15efbbd2d52979b4c3f` |
| postconciliar | homily | `c1f06793ba0b824e31f5eb5cd75fe02240c5eb0e43319c930a076a3bcc8b8941` |
| postconciliar | visual | `f08ee5744571dc6087a5b55af96f1ebf6325ac9387f85477a6a4282fd9464ce8` |
| postconciliar | web | `d83ca884c7b2c03a344fad65081a066b4e83f153221817703b6174d107e7c7b9` |

## Exact archived files

### 1962

Archive root:
`src/gpt/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost/evaluations/pagination-revision-proposal/`

Source draft root:
`.scratch/tlm-production/pagination-revision/`

Exact files below this root:

```text
PLAN.md.draft
README.md
SHA256SUMS
chronology-annotations.tex.draft
chronology-source-ids.json.draft
chronology.toml.draft
components/00-inventory.tex.draft
components/01-overview.tex.draft
components/02-scriptural-date-location.tex.draft
components/20-themes-and-movement.tex.draft
components/30-interleaved-commentary.tex.draft
components/90-apparatus.tex.draft
draft-manifest.json.draft
manifest.json
synthesis-draft.tex.draft
```

Run `sha256sum -c SHA256SUMS` within this archive; both owner checks passed.

### postconciliar

Archive root:
`src/gpt/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s51-twenty-fifth-sunday-in-ordinary-time-year-a/evaluations/pagination-revision-proposal/`

Source draft root:
`.scratch/no-production/pagination-revision/`

The sole additional source is
`.scratch/postconciliar-chronology/chronology-inputs.toml`,
stored only as `adapter/chronology-inputs.toml.draft` in this owner.

Exact files below this root:

```text
PLAN.md.draft
README.md
SHA256SUMS
adapter/chronology-inputs.toml.draft
chronology-summary.txt.draft
chronology/Acts.16.14.json.draft
chronology/Is.55.6.json.draft
chronology/Is.55.7.json.draft
chronology/Is.55.8.json.draft
chronology/Is.55.9.json.draft
chronology/John.10.14.json.draft
chronology/Matt.20.1.json.draft
chronology/Matt.20.10.json.draft
chronology/Matt.20.11.json.draft
chronology/Matt.20.12.json.draft
chronology/Matt.20.13.json.draft
chronology/Matt.20.14.json.draft
chronology/Matt.20.15.json.draft
chronology/Matt.20.16.json.draft
chronology/Matt.20.2.json.draft
chronology/Matt.20.3.json.draft
chronology/Matt.20.4.json.draft
chronology/Matt.20.5.json.draft
chronology/Matt.20.6.json.draft
chronology/Matt.20.7.json.draft
chronology/Matt.20.8.json.draft
chronology/Matt.20.9.json.draft
chronology/Phil.1.20.json.draft
chronology/Phil.1.21.json.draft
chronology/Phil.1.22.json.draft
chronology/Phil.1.23.json.draft
chronology/Phil.1.24.json.draft
chronology/Phil.1.27.json.draft
chronology/Ps.118.4.json.draft
chronology/Ps.118.5.json.draft
chronology/Ps.144.17.json.draft
chronology/Ps.144.18.json.draft
chronology/Ps.144.2.json.draft
chronology/Ps.144.3.json.draft
chronology/Ps.144.8.json.draft
chronology/Ps.144.9.json.draft
chronology/Ps.36.39.json.draft
chronology/Ps.36.40.json.draft
chronology/manifest.json.draft
components/01-inventory.tex.draft
components/02-overview.tex.draft
components/03-chronology.tex.draft
components/04-themes.tex.draft
components/05-interleaved-commentary.tex.draft
handoff.json.draft
manifest.json
presentation-fragment.toml.draft
source-map.md.draft
word-counts.json.draft
```

Run `sha256sum -c SHA256SUMS` within this archive; both owner checks passed.

## Remaining boundary

These archives are not build-ready source trees. Their original scratch imports,
draft manifests, unresolved chronology and unproved page budgets remain intact.
Restoration goes to a new same-family scratch tree, never over accepted sources.
Fresh authorized research, authorship, requested-effort cold reviews and actual
v3 terminal acceptance remain required before adoption. No fresh worker or Codex
call occurred during archival recovery. No canonical prose, metadata, component
manifest, historical packet/result, installed PDF, canonical web file, release
record, shared inventory or ledger was edited by this archival task.

Shared source-inventory/release reconciliation and any staging, commit or push
remain the coordinator's work. This report and the owner archives were created
for tracking; this task did not stage, commit or publish them.
