# Production manifest

Status: **scaffold only; not approved for full publication**
Audit date: 2026-07-27

## Leaves

| Leaf | Source exists | Canonical records rendered | PDF built/reviewed/installed | Web edition reviewed | Release state |
| --- | --- | --- | --- | --- | --- |
| Comprehensive | Yes, prototype | No | No recorded completed gate | No | Hold |
| Altar server | Yes, prototype | No | No recorded completed gate | No | Hold |
| Sacristan | Yes, prototype | No | No recorded completed gate | No | Hold |
| MC/trainer | Yes, prototype | No | No recorded completed gate | No | Hold |
| General reader | Yes, prototype | No | No recorded completed gate | No | Hold |
| Pontifical ceremonies | Yes, prototype | No | No recorded completed gate | No | Hold |

Each leaf still requires its own `research/guide-map.md` and any required
source bindings. Presence of `main.tex`, generation metadata, or
`web-edition.toml` is not publication approval.

## Required pipeline

1. Close the official and material-culture corpus.
2. Populate and validate canonical object, variant, source, artwork, and plate
   records.
3. Implement strict generation from TOML to ignored `build/` TeX; reject
   unknown fields, dangling IDs, unverified required claims, and unapproved
   artwork.
4. Prove edition selections and explicit exclusions from canonical data.
5. Build enough passes to settle contents, references, and indexes.
6. Reject fatal errors, undefined references, overflows, unresolved layout
   warnings, automatic PDF dates, and nondeterministic trailer IDs.
7. Use only the repository review helpers for rasters/contact sheets; inspect
   every page and every ambiguous figure at full size.
8. Print and monochrome-photocopy representative dense, linen, vestment, and
   composition plates.
9. Verify PDF structure, embedded fonts, metadata, extracted text, web reading
   order, and reviewed-build/installed byte identity.
10. Record independent source, factual-artwork, production, and distribution
    approvals separately.

## Artifact ledger

No dictionary PDF identity, page count, installed byte hash, raster
normalization result, print-test result, or approved web snapshot is recorded
as complete in this manifest.

## Full-publish readiness

**Not ready.** The present source tree is a structural prototype prepared for
future production. It must not be described as complete, source-audited,
independently reviewed, ecclesiastically approved, or distribution-approved.
