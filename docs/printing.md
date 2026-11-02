# Printing Triptych

Read in the existing browser readers. Use the browser's Print or Save as PDF
for a flowing copy of the current page. That copy follows the page's content
and rights limits; its line and page breaks depend on the browser, paper and
printer settings.

For a publication's designed print layout, generate one selected edition from
the canonical source. PDFs are optional local outputs. The repository and
normal site deployment do not keep or rebuild a PDF corpus.

Where an edition offers **Archived PDF**, that link preserves a verified
historical fixed layout in the external archive. It is distinct from browser
reflow and from a newly generated print edition. The exact public snapshot,
PDF hashes and delivery are recorded in `release/print-archive.json`.

## Generate one edition

Run these commands from the repository root:

```sh
tools/print-document list --family publication --provider gpt
tools/print-document check --document publication:gpt/theology/angelology
tools/print-document build --document publication:gpt/theology/angelology --out .scratch/print/angelology
```

`--out` is an output directory. The command reports the selected recipe,
dependencies, generated files and receipt. The default destination is under
`.scratch/print-document/`. It does not install files into a tracked tree,
publish a download, or build other documents.

For a proper with declared companions, select its canonical leaf and edition:

```sh
tools/print-document build --document publication:gpt/liturgy/roman-rite/1962/propers/temporal/f02-all-saints --edition synthesis --out .scratch/print/all-saints-synthesis
```

`--edition main` selects the canonical publication; `research` and `full`
are aliases for it. `synthesis` and `homily` are available only where the
source owner declares them. List the actual recipes before choosing an edition.

Provider-neutral source editions use their own identities:

| Identity | Selects |
| --- | --- |
| `publication:gpt/<leaf>` or `publication:claude/<leaf>` | One provider publication and its selected edition. |
| `bible:<id>` | One publishable Bible edition under its own rights. |
| `reading-plan:<volume>` | One declared reading-plan volume. |
| `papal:<id>/<language>` | One admitted papal source reading selection. |

Use `tools/print-document list --family bible`, `--family reading-plan`, or
`--family papal` to obtain exact available IDs. Bibles and reading-plan
recipes can also emit standalone TeX with `--output-format tex`; this prepares
the source without compiling a PDF. Check `tools/print-document build --help`
for supported formats and options.

## Dependencies and review

The print command validates the selected canonical inputs and uses the owning
typesetter. A PDF build needs that recipe's TeX engine, packages and fonts;
the command reports a missing dependency instead of generating a substitute.
Existing authored typography, artwork, content selection and source notices
remain part of the recipe. A browser printout does not reproduce duplex cards,
paired course pages or other fixed-page contracts.

Source and evidence review, print-template review, and inspection of one
rendering are separate facts. A successful build is not a new visual review
or publication approval. When issuing a reviewed print edition, follow the
owning profile and [repository print-review contract](../guidance/repository.md#build-and-review-contract),
including exact page/duplex requirements and a receipt for the actual output
and pages inspected. Keep generated files and review rasters outside Git.

Exact binary source evidence is optional local data, resolved through
`src/sources/artifact-delivery.json`. To inspect it offline, obtain the
relevant verified archive and explicitly hydrate it as described in
[the source-library contract](../guidance/sources.md#exact-binary-delivery-and-offline-access).
A normal site build does not fetch that archive. Access and redistribution
remain governed by each source's rights, even when a print recipe exists.

Old PDF links may now open an identified reader or a page explaining the
print options. A historical binary download is offered only when its exact
archive delivery is verified; the current print recipe need not reproduce
its old bytes. Source removal does not erase PDF objects from Git history or
shrink a full-history clone.
