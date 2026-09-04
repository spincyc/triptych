# Source Registration

## Your task

The research lanes retrieved sources and kept the bytes. You are the one stage
of this workflow that may write `src/sources/`, and your whole job is to turn
those retrievals into records the library holds, before `author-proper` runs
and needs them.

Read `guidance/sources.md` first, completely. It owns identity, rights, storage
disposition, extent and the states a record may claim; this fragment tells you
when to apply it and what this run has waiting, not what the rules are.

## Where the receipts are

Every research lane returned its findings with a `retrievals` list, and `tpt`
recorded each lane result verbatim. Your packet header names the run. Read:

```
build/tpt-runs/{RUN_ID}/results/research-*-lane-*.json
```

taking the highest iteration present for each lane, and collect every
`retrievals` entry from every finding. Each names a URL, a digest, a size, a
media type, a path in that lane's scratch directory, a retrieval date, and the
extent the lane measured.

Verify before you trust: `sha256sum` the file at `path` and require it to equal
the recorded `sha256`. A receipt whose bytes have moved or vanished is not a
registration you may complete from memory — record it as unregistered in your
summary and say why. **Never reconstruct a `source_url` you cannot read off a
receipt.** A guessed source URL is a record that resolves successfully and
wrongly, which `guidance/sources.md` calls this library's governing failure.

## Look before you create

Two failures pull in opposite directions and both have happened here.

**A false duplicate.** Resolve a work's aliases before minting an id: a Latin
title, a vernacular one, an incipit standing in for a title, the author in
Latin and in the vernacular and by see or epithet, a Migne volume, a modern
editor's short form. `tools/source-reader list --find <term>` prints the
registered works and editions that match. Four Sundays' orations were once held
twice under two names and the copies had silently diverged in five ways before
anything noticed.

**A superseded record read as a missing one.** Before you register an artifact
whose id the library lacks, check whether the library holds a *corrected
derivation of the same edition*. An id absent from `src/sources/` looks exactly
like a gap from every angle a comparison can see — a complete, well-formed
record, asserting its rights, byte-identical across every checkout that still
carries it. Only the replacement's `transformation` and `provenance` say it was
deliberately replaced.

This is not hypothetical. `artifact.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.new-roman-missal-text-deb5d167`
still sits in dozens of branches, asserting `public-domain` over an OCR text
built by one deletion. The library holds `new-roman-missal-text-80b34759`,
re-derived later by *two* deletions, because the first pass left the lettered
inserts at printed pp. 1302a-1302d in bytes whose rights basis does not cover
them. Registering the older id would reintroduce a rights defect that was
already found and fixed. When a work already has editions here, read their
artifacts' `transformation` and `provenance` before adding a sibling.

## Both languages, and the whole of each

`guidance/sources.md` requires the fullest view a source offers. This stage
adds the pairing rule that the propers line needs:

- **Register the work in the language it was written in.** A patristic homily,
  a conciliar canon, an oration, a medieval commentary — the original is the
  witness, and a translation is testimony about it. A work held only in English
  cannot settle a question about its own wording.
- **Register an English translation as well, wherever one is lawfully
  available.** It is a separate edition of the same work, never a substitute
  for the original, and it carries its own translator, date and rights.
- **Where one of the pair cannot be had, say so in the edition record**: what
  was sought, under which aliases, where, and what the bound was. An absence
  recorded is data; an absence unrecorded is indistinguishable from never
  having looked.

The library today holds 55 works with both and 169 whose composition language
is not English and which are held *only* in translation — Ambrose's *De
mysteriis*, Irenaeus' *Adversus Haereses*, Plato's *Symposium*. That backlog is
not yours to clear. Do not add to it.

## Rights decide retention, never registration

Register the identity of every source a lane actually read. Then let the rights
record choose the disposition, per `guidance/sources.md`: `tracked` for lawful,
reasonably sized, reusable bytes — the project-wide default; `remote` only when
the record itself earns it in plain words; `restricted` where lawful access
does not extend to redistribution; `unavailable` where the bytes cannot
presently be obtained or authenticated.

A restricted source is registered, not skipped. The library already holds 344
such records — identity, digest and rights kept, bytes held elsewhere — and
that is how a rights-encumbered witness becomes citable without being
republished. Declining to register it instead loses the identity and the
rights finding together.

## What you write

For each source that survives the checks above, create or extend, under
`src/sources/works/<namespace>/<work>/`:

- `work.toml` — the abstract work: title, responsible party, `languages`, and
  `composed` with `composed_basis` where the composition date is known. A
  work's date is when it was **written**, never when this printing appeared.
- `editions/<edition>/edition.toml` — the printing, translation, recension or
  dated web state, with its own `date`, editors or translators, and language.
- `editions/<edition>/artifacts/<artifact>/artifact.toml` — the exact bytes:
  `sha256`, `byte_size`, `media_type`, `source_url`, `retrieved`, `provenance`,
  `storage`, `rights_status`, `rights_basis`, and the measured extent in
  `notes`. Retain the file beside its record when `storage = "tracked"`.

Use the language codes the library already uses — `la`, `grc`, `en`, `he`,
`arc` — and not their alternates. The vocabulary is mixed today (`la` 242
against `lat` 8, `de` 12 against `deu` 2, `grc` 61 against `el` 3) and nothing
validates it, so a pairing check reads `languages = ["lat"]` beside a `la`
edition as an original that is missing. Do not add a variant.

## Verify before you return

```
tools/source-library validate
make check-sources
```

Both must pass over what you wrote. `make check-sources` is the ordinary
non-completion gate: it validates the canonical source graph and bindings and
replays the inventory. A record that does not validate is not registered, and
returning `PASS` over one hands `author-proper` a fingerprint that will refuse.

## What you may not do

You write `src/sources/` and nothing else. Not the canonical leaf, not
`research/scope.md`, not `propers/verified.md`, not guidance, not `tools/`. You
do not retrieve: the lanes did that, and a source you fetch here is evidence no
research lane swept, no coverage audit saw, and no rights check cleared. Where
a receipt is unusable, say so and move on — the run continues, and the author
is separately told that a witness the library does not register is cited in the
ordinary way rather than blocked on.

## Result

Return a worker result with `disposition: "PASS"` and a summary naming, in
numbers and then by id: how many receipts you read, how many sources you
registered, how many you declined and on what ground (already held, superseded,
digest mismatch, rights, unmeasurable extent), and which works you registered
in one language only and why the other could not be had. Return
`disposition: "BLOCKED"` only if you could not read the recorded lane results
at all; a receipt you could not use is a line in the summary, not a blocked
run.
