# Install the Publication

## Your task

Make the reviewed work reachable: confirm the evaluated web edition is what
the site will build, create the per-publication release records, wire this
provider's catalog cell, and refresh the release bindings. Everything this
stage installs has already been accepted or evaluated. Nothing here judges
the work again, and nothing here rewrites it.

## Steps

### 1. Confirm the web edition

No web edition is installed or tracked: the site converts this proper and its
companions from their canonical TeX when it is built (`guidance/web-editions.md`).
Confirm that the file the evaluator read, `build/web/{provider}/{proper}.md`, is
still what current sources convert to, and that
`tools/tpt web-edition check --leaf {provider}/{proper}` passes. Record the
evaluation in the leaf's `web-edition.toml` as its inspection (`inspected`,
`inspected_by`, `inspection`).

### 2. Create the release records

Each publication has its own record. The canonical leaf and its synthesis
companion are published in their own right, so each gets one:

```
make add-publication ID={proper} \
    CATALOG=library/traditional-latin-mass.md \
    PROVIDER={provider} STATUS=alpha
make add-publication ID={proper}-synthesis \
    CATALOG=library/traditional-latin-mass.md \
    PROVIDER={provider} STATUS=alpha
```

These write `release/publications/{provider}/{proper}.json` and
`release/publications/{provider}/{proper}-synthesis.json`. The command
refuses to overwrite an existing record: if one is already there, read it,
confirm it names this catalog, and leave it alone.

### 3. Wire the catalog cell

`library/traditional-latin-mass.md` already carries a row for every permanent
temporal identity. Find this identity's row and fill in **this provider's
cell only**. A componentized proper's provider cell links all three published
artifacts, in this order, joined by ` · `:

```
[Full PDF](../pdf/{provider}/{proper}.pdf) · [Synthesis PDF](../pdf/{provider}/{proper}-synthesis.pdf) · [Read](../web/{provider}/{proper}.html)
```

The rule is owned by `guidance/repository.md`; read it there rather than
copying the shape of a neighbouring row, several of which predate the
convention. A provider with nothing installed shows the bare word `Planned`,
so leave the other provider's cell exactly as you found it.

Add the identity marker for this publication in the marker block, using the
grammar `guidance/repository.md` states: the bare leaf id for the primary
provider, and the `{provider}:` prefixed form for a secondary one.

**Do not write the row itself.** The Sunday's name and the identity's place
in the table are the maintainer's, not this workflow's. If this identity has
no row, return `BLOCKED` naming the missing row rather than inventing one.

### 4. Refresh the release bindings

The catalog is a reader-facing source, so its hash and the site source list
must be brought up to date:

```
make refresh-release-bindings ADOPT=1
```

`ADOPT=1` is what admits a newly recognized source, such as the leaf's
sources, into the site source list.

Do not run the site checks yourself and report that they passed. Since
version 13 the publication gates run `check-release-bindings`,
`check-public-alpha`, `check-document-catalogue` and
`web-edition check` as gate checks of their own, judged by exit
code. A stale binding or an unrecorded source is a wiring defect for those
gates to catch and for `publication-revision` to repair, and a worker's
account of a check it ran is not the evidence acceptance rests on.

## Result

Return a worker result with `disposition: "PASS"`, `artifact_path` set to
`release/publications/{provider}/{proper}.json`, and a summary naming: the
recorded web inspection, both release records and whether each was created or
already present, the catalog row and cell you filled, and the marker you added.

Return `disposition: "BLOCKED"` when the publication cannot be wired from
here: no catalog row for this identity is the standing case, because writing
one is a maintainer's decision and not a step this stage may take.
