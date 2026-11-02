# Bounded source successor compiler review

Disposition: accept the compiler for preparing a pending candidate at SHA-256
`d6623dd274dd4d83e7f0e59d3e6eb627fa10648fd050c0b96e11f692b9205a2f`.
Support SHA-256 is
`3622fc1bcbf6e21e09e65be3cff50786930564de6be8640edd72b5be279d95ae`.
Final source/admission and exact candidate acceptance remain open because source
lanes are still changing the epoch.

Reviewed `compile_successor.py` and `support.py` completely, the V4 receipt,
strict runtime helper and its synthetic controls, relevant current/historical
consumer contracts, and the lane validation plan. The accepted compiler has no
scratch-library dependency and preserves the bounded V4 domain.

## Findings and disposition

| Finding in initial scratch compiler | Final disposition |
| --- | --- |
| Source additions were auto-adopted from Git changes without an enforced declared path/hash set. | `derive` now requires a separately supplied exact delta SHA and compares the complete observed path/before/after rows with it. Extra dependencies must be explicit source paths. |
| Semantic delta omitted body-state/hash changes, effective pre-1955 proofs, complete pre-1955 English/exclusions, and Ordinary inventory dictionaries. | Those complete before/after partitions are included in the transition contract. |
| Early candidate manufactured a projection artifact and edition despite unchanged current Latin proofs/bodies. | New projection oracles now derive from changes against accepted V4; the historical oracles are preserved. The early candidate remains diagnostic. |
| Source namespace completeness was deferred to consumers. | Exact English/projection namespace equality with historical complement plus final manifest is checked before output. |
| Compiler proof could hash a later on-disk compiler revision. | Startup-selected compiler bytes, support, explicit delta, and epoch are rechecked before output. |
| Final-file symlink rejection permitted files below symlinked ancestors outside the root. | Demonstrated independently, then corrected with root-resolution and ancestor-symlink checks plus regression coverage. |

## Evidence

- Independent immutable parent verification: 5,615 pins, all 12 original
  historical fields, and all 17 raw byte inverses. The tracked fixture and
  manifest still matched V4 at the base check; strict helper remains exact
  `f60498c9c9f28f72d69d729b1d086044fa3877803327bb4e16d779c479ad55b1`.
- Historical English namespace: 1,452 paths; projection namespace: 1,430 paths.
  Every historical namespace path is already in the V4 domain.
- Strict runtime synthetic corruption controls: 14/14 pass, exit 0.
- Portable compiler synthetic controls: 10/10 pass, exit 0. The test copy changes
  only the subject path and scratch destination to keep this lane's writes in
  its own directory.
- Independent portable parent check and adversarial controls verify escaped
  ancestor rejection and rejection after deletion of a pinned source namespace.
- Evidence files: `parent-check.json`, `portable-compiler-check.json`,
  `ancestor-symlink-control.json`, `strict-consumer-controls.log`, and
  `compiler-controls.log`.

## Final candidate review still required

Freeze source inputs, include unchanged newly used dependencies outside V4 as
`extra_inputs`, select the exact declared delta and reviewed compiler hashes,
and derive into a new scratch output. Review that exact fixture, manifest,
transition contract, and data proof against the independent source admissions.
Confirm all V4 paths plus the exact declared additions, truthful derived maps,
unchanged original fields/inverses, and `pending` state. Root acceptance must
allocate a fresh unused receipt identity, bind the exact candidate, then run the
required guard consumers and owning checks after installation.

Changes made by this review: owned scratch evidence only. No subject, tracked,
commit, or push mutation.
