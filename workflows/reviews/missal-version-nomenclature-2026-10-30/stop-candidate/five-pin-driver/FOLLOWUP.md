# Prepared Names phase-5 code-currentness addition

Status: scratch proposal only. No Names application, source-epoch candidate,
acceptance, canonical snapshot or production generation has occurred.

The old 47-control metadata preparation remains byte-exact at
`naming-metadata-successor/`. This directory is an additive copy for current
source epoch fixture3bcf / manifestea29 / receipt4d35. Its fresh parent commit
is still pending.

`phase5-calendars-currentness.patch` changes test9414 to c52f. It inserts one
dedicated `_calendars.py` branch. The existing PRESERVED_FILES literal54f370
checks a byte-exact pre-Names historical snapshot; a separate fixed checksum
checks the independently reviewed current Names codeca1388. The literal table,
body/oracle assertions, proper-L852 and coverage10db branches are unchanged.
Deleting the inserted branch restores the whole original test byte-for-byte.

The exact test/snapshot postimages and `PROPOSAL.json` received independent
review1d0bdfb6, including nine positive/negative branch controls. The historical
snapshot is evidence only and is not imported as current code. It must not be
resampled from the Names code after application.

The copied driver has five exact existing source-pin changes: the four original
Names metadata paths plus this separately reviewed test. It rebuilds exactly
two original inverse specifications (PC Proper YAML and phase5 test), preserves
the other15 specifications and every semantic fixture oracle, and checks all17
actual original Git streams. Forty-three owner controls pass. There is no
generic source or runtime grant.

Before root runs the prepared driver, root applies the reviewed Names files,
the exact test patch and snapshot, retains the independent test receipt, and
completes `ROOT-APPLICATION.template.json`. The actual record must have status
`applied-exact-reviewed-test-and-snapshot`, exact test/snapshot/Named-code hashes,
the current receipt4d35 and the separately sealed test review1d0bdfb6. Root
supplies its exact path/hash to both prepared commands:

```sh
python -B names_metadata.py --parent <fresh-pre-Names-commit> \
  --test-root-binding <repo-relative-actual-Root-record> \
  --test-root-binding-sha256 <exact-record-sha> --out <fresh-own-scratch-path>
python -B verify_producers.py --parent <same-commit> \
  --test-root-binding <same-record> \
  --test-root-binding-sha256 <same-sha> --out <fresh-own-scratch-path>
```

Run from the repository root with the pinned Python interpreter and full script
paths in this directory. The actual source-root verifier, independent final
accounting review and root acceptance remain required.

Catalog boundary: this copy still binds original53 catalogecbd under READY0bd.
The independently reviewed Joseph addendum2e416 / reviewfec3 is separate. If
root adopts it, bind that exact actual catalog successor and review before any
final source-epoch run; the old53 receipt does not cover it. No extra source
path is implied by that same-file addendum.
