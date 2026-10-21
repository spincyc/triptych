# chant-page-proof

Read-only mechanical checks for two existing bounded chant proof layouts.
The tool emits a mechanical-only JSON result with `--json`, or a short summary.
Exit0 means the requested mechanical checks passed; exit1 means a packet failed
or its format is unsupported; exit2 is an invalid CLI invocation.

```text
chant-page-proof PACKET (--manifest REL | --sha256sums REL)
  [--proof source-proof.json] [--record-root DIR]
  [--render-receipt REL ...] [--json]
```

The manifest is a JSON object whose nonempty `files` list contains
`{path,size_bytes,sha256}` records. The alternative inventory accepts only
lowercase SHA256, two spaces, and a packet-relative path on each line. GNU
escaped filenames and binary-marker variants are not supported. Inventory paths
may not be absolute, traverse parents, duplicate a file, or escape through a
symlink. The selected proof and explicit render receipt files must be covered
by the inventory. Image bytes are always checked against the proof's own image
hash and size, whether or not the outer inventory also lists them.

Supported proof layouts are explicit:

- `packet_type: bounded-source-proof-only`: each row has nested source and
  target `checked_text`/`checked_text_sha256` pairs, plus
  `normalized_target_proposal`/`normalized_target_proposal_sha256`; image records
  use `size_bytes` and `dimensions_pixels`.
- `schema: triptych.scratch.checked-chant-word-proof/v1`: each row has exact
  `source_body`, `target_control_body`, and `target_proposal` strings and their
  corresponding `_sha256` fields; image records use `bytes`, `width`, `height`,
  and explicit renderer records.

Body hashes use the existing `_proper_latin.text_sha256` owner over the exact
Unicode string encoded as UTF8. The tool trims no final LF, folds no accents,
and supplies no normalization. File hashes/sizes use the existing
`source-library._hash_and_size`; canonical fingerprints still belong to
`source-library fingerprint` and are not computed here.

Image paths normally resolve relative to PACKET. The second existing layout
stores repository-relative paths, so pass `--record-root .` from that repository.
Every resolved image or render output must still lie inside PACKET. This path
base selects data only and never changes the code used for owner functions.

PNG checking reads the signature and first IHDR dimensions, not pixel content
or the complete PNG structure. Explicit render receipts are JSON lists. Their
exit status must be zero and their page, DPI, crop, output, and recorded
`pdftoppm` arguments must agree; external receipts must agree with the proof
image records and cover every proof image once. Commands are never executed.
External PDF inputs, their identity, and their page content are not verified by
this checker. Crop commands that rely on clipping beyond the page dimensions
are not supported by this bounded exact-size contract.

The result does not certify OCR, source readings, lexical equivalence,
normalization, `actually_viewed`, review attestations, rights, publication
permission, source-to-body relevance, or a canonical source-library fingerprint.
It does not generate rasters, transcribe bodies, update packets, or execute any
source-specific proof writer.

The two help examples were run on the actual held packets. Their scratch inputs
are not public fixtures. The example replay records their local-input
preconditions: present packets are checked, and absent packets are reported as
not run. The durable Python tests use only synthetic words and IHDR header
streams, not copied source bodies or scanned images.
