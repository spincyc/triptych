# Research Staleness and Re-evaluation

This policy governs every provider branch. Its deterministic half is
implemented by `scripts/research-staleness` and the tracked ledger
`src/sources/inventories/research-staleness-v1.toml`; the evaluative half
is provider work that this profile defines.

## Staleness

A paper's research inputs are:

1. its own `research/` records;
2. the `research/` records of every other provider's edition of the same
   leaf; and
3. the reusable source records under `src/sources/works/` that its
   `source-bindings.toml` binds.

When any input changes — by any provider — every provider's edition of
that leaf is stale. `make check-staleness` reports stale editions;
`scripts/research-staleness explain <provider> <leaf>` names the exact
changed inputs. Staleness is a flag for re-evaluation, not a judgment
that the paper is wrong, and it never blocks builds or release checks on
its own.

Staleness is also diagnostic only: it grants no authority to edit,
rebaseline, rebuild, install, or otherwise change an edition. A
cross-provider input may make another provider's edition stale, but that
dependency edge authorizes inspection only. Perform the re-evaluation
steps below solely for providers that the current request expressly places
in material-edit scope. Leave every other provider's flag open and its
tracked and generated publication files unchanged until authority for that
provider is explicit.

## Re-evaluation

Each authorized provider re-evaluates its own stale editions independently;
one provider's re-evaluation neither clears nor substitutes for another's.
For each stale edition within the expressly authorized provider scope:

1. reads the changed inputs (`explain`) and the current paper;
2. produces **both** candidate treatments under the ignored build tree
   (`build/staleness/<provider>/<leaf>/modified/` and `.../rewritten/`):
   an in-place modification of the current source that incorporates the
   changed research minimally, and a complete rewrite drafted from the
   changed research without consulting the current prose;
3. performs an honest three-way comparison of old, modified, and
   rewritten: for every consequential claim, note whether the changed
   research adds, removes, strengthens, weakens, or contradicts it, and
   whether the two candidates disagree with the old paper in substance
   rather than wording; and
4. records the comparison and its verdict in the edition's
   `research/` records (a dated staleness-review note in `scope.md`'s
   review state or a dedicated record the profile requires).

**No material change:** clear the flag with
`make rebaseline-doc PROVIDER=<p> DOC=<leaf>` and discard the
candidates. Do not install either candidate merely because it exists.

**Material change:** raise the comparison to the user — old, modified,
and rewritten, with the per-claim differences — and wait for explicit
confirmation before replacing the installed edition. Replacement then
follows the ordinary editorial pipeline (build, gates, page review,
install, catalog, release accounting) and ends with a rebaseline.

## Baselines

`rebaseline` records the current fingerprints as reviewed state; run it
only after the re-evaluation above, after installing a replacement, or
when creating a new edition (whose first baseline is its authoring
state). `bootstrap` initializes the ledger once for every discovered
edition. The ledger is tracked; commit baseline changes with the work
that justified them.
