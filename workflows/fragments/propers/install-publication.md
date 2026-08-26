# Install the Publication

## Your task

Make the reviewed work reachable: install the evaluated web edition as the
tracked artifact, create the per-publication release records, wire this
provider's catalog cell, and refresh the release bindings. Everything this
stage installs has already been accepted or evaluated. Nothing here judges
the work again, and nothing here rewrites it.

## Steps

### 1. Install the web edition

Install the reviewed Markdown as the tracked artifact:

```
install -m 0644 build/web/{provider}/{proper}.md \
    web/{provider}/{proper}.md
```

Create the destination directory first if it does not exist. Install exactly
the file the evaluator read; do not regenerate it here, because the reviewed
edition and the installed edition must be the same bytes.

Then confirm the tracked artifact matches what current sources produce:

```
make check-web-editions-current
```

Do not create `web/{provider}/{proper}-synthesis.md`. The synthesis is a
derived companion of the canonical leaf and has no web edition.

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

The catalog and the new web edition are reader-facing sources, so their
hashes and the site source list must be brought up to date:

```
make refresh-release-bindings ADOPT=1
make check-release-bindings
make check-public-alpha
make check-document-catalogue
```

`ADOPT=1` is what admits the newly tracked web edition as a site source. Read
each check's output; a failure here is a wiring defect for the publication
gates to catch and for `publication-revision` to repair.

## Result

Return a worker result with `disposition: "PASS"`, `artifact_path` set to
`web/{provider}/{proper}.md`, and a summary naming: the installed web
edition, both release records and whether each was created or already
present, the catalog row and cell you filled, the marker you added, and the
result of each check you ran.

Return `disposition: "BLOCKED"` when the publication cannot be wired from
here: no catalog row for this identity is the standing case, because writing
one is a maintainer's decision and not a step this stage may take.
