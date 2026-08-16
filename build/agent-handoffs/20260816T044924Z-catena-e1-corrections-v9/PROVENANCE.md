# Parent-run provenance — retained and discarded

The exact parent and head SHAs, and every derived figure of both batteries,
are in `claims.json`; this file records where the runs happened and which
runs are authoritative, which the V8 review found the V8 package never
stated explicitly.

## The retained runs — authoritative

Both batteries ran in dedicated workspace clones, each on the exact
checked-out SHA it claims, with a clean working tree at battery start:

- **Head battery** — the implementation clone, checked out at the exact V9
  head, working tree clean beyond the head's own committed content. Ledger:
  `logs/order-head.txt`; every command, exit and timestamp is there.
- **Parent battery** — a separate parent-side clone, checked out at
  this lane's exact parent `7e4df42a21bc2be2d28ff14943f63af3e7e3a6f8` — the
  reviewed V8 candidate — working tree clean at battery start. Ledger:
  `logs/order-parent.txt`. Its final steps overlay the head's test file
  over the parent's — the overlay is part of the recorded command, which is
  what makes the run mean what it means — and the clone was restored to the
  exact parent state afterwards.

Both clones' absolute path prefixes are normalized by the sealer and the
sanitization scan proves no operator identity survived; the ledgers record
what ran, in order, with nothing typed from memory.

## The discarded run — recorded, used nowhere

During the V8 lane, an initial parent-baseline battery was run in a
temporary directory under `/tmp`. It produced an unrelated
`pdf-review.test` failure caused by the repository's location — an
environment artifact, not a product regression. That run was discarded from
authoritative evidence at the time; the V8 review accepted the discard as
non-authoritative but found it never explicitly ledgered. It is ledgered
here: the `/tmp` run happened, it was discarded for its environment-caused
failure, and **no comparison, figure or claim in this package or its
predecessors derives from it**. The V9 lane itself ran no battery in `/tmp`
and discarded nothing: every V9 run above is retained and its ledger is in
the package.
