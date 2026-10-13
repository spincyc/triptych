# Research acceptance checkpoint

This archive records the actual `proper-study` v10 run `a72731c5491066a3`
after `research-review-0001` returned `PASS` and the engine advanced to
`author-study-0000`. The run is still active; this is not terminal publication
acceptance. The author-study packet is compiled but no author was dispatched
before this checkpoint.

The manifest identifies every native engine record and auxiliary item by
source path, archive path, size, and SHA-256. Native manifest, bootstrap,
state, events, packets, results, gates, and embedded input seals are copied
byte-exact. No source snapshot or facsimile payload is included.

Auxiliary evidence is under `evidence/`. All retained auxiliary files are
byte-exact except `research-review-0001/review-checks.public.json`, explicitly
a public derivative. That file replaces only its numeric native exec session
identifier with an omission marker. The manifest records the untouched local
original's hash and this exact transformation. The native review result and
packet are unaffected. Auxiliary checks and driver integrity receipts do not
substitute for the actual reviewer verdict or engine transitions.

The accepted research seal remained current after the engine cleared its
standing research findings and publication inventories were refreshed:
1,738 sealed files and 13 chronology computation inputs matched. Source
inventory, source-family migration, publication-inventory validation, and
whitespace checks passed. The previously recorded aggregate `check-sources`
limitation remains the absent downstream publication declaration; no final
publication verification is claimed at this checkpoint.
