# Independent typography review

## Final recheck: ACCEPTED

The P1 finding below is closed at renderer SHA-256 `1c14411ed430d51605af66a37ddcb6d758d0eb67c9e8d56a1d4d875e9a0ba146`. Both original quote repros now compile with source-body and displayed-title quotation marks intact. Global Babel shorthands are off and the receipt records that setting. The new FreeSerif symbol fallback retains `■ ― ♦ ►` in source body and title with embedded ToUnicode fonts. The opt-in `\\S{48,}|_{24,}` wrapping rule only inserts break opportunities between unchanged source character clusters.

An independently compiled composite proof retains all 35 original underscores, quotes, symbols, original source hyphens and two added layout hyphens; its extracted body fidelity passes. Its single page was rasterized through `tools/tpt pdf-review` and inspected full size: the long underscore run wraps visibly, with one underfull warning and no clipping, overflow or missing glyphs. `fix-composite-result.json` records exact PDF hash and evidence. All 254 damaged-text cases were again rejected; all 62 valid layout-hyphen cases were again accepted. The coordinator's completed `final-renderer-tests.txt` reports 43 tests OK; no duplicate suite was launched. Focused `git diff --check` passes. No remaining renderer finding; earlier mass-render and clean-host limits still apply.

Reviewed HEAD `28030e50c61106ef16950a48afce22ba0d2511ca` plus the uncommitted renderer, tests and papal typography guidance. Renderer SHA-256 at review: `764f66d3789d2e20918d4962269c5a66bd0a4b3cf216106acc3f751f8e7767aa`.

## Blocking finding

**P1 — Latin Babel shorthands consume literal source quotation marks.** `scripts/_typeset_papal.py:567` loads `babel[latin]` with its default active double-quote shorthands. Body `Dicit: "Verba integra" et "aequitas" servantur.` loses quotes and neighboring spaces. Current renderer refuses source fidelity; HEAD renderer passes the same fixture. Latin title `De "Verba"` visibly loses its opening quote while the unchanged body still passes fidelity. Actual canonical Latin Octobri mense contains the exposed source sequence `"De Mariae Virginis Rosario"`.

Reproduce from repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 .scratch/cold-typography/repro_quotes.py
```

The minimal scratch-only remedy `\\usepackage[shorthands=off,latin]{babel}` passes the same quote fixture while still yielding an automatic layout hyphen. Disable shorthands for both loaded languages and add a rendered Latin regression covering body and displayed-title literal quotes. Existing Latin test at `tools/tests/test_typeset_papal.py:491` covers only unquoted text.

## Evidence and limits

- Independent focused suite: 41 tests PASS; no failures/errors/skips. Test scratch redirected exclusively beneath this review directory. `tests.log` retains results.
- `adversarial-fidelity.json`: all 254 deletion, replacement and internal-insertion damages rejected, including lost original hyphens combined with valid layout hyphens; all 62 valid inserted line-hyphen positions accepted with correct counts.
- Rechecked all four sample PDFs against validated complete source inputs and exact receipt hashes: PASS. `sample-evidence.json` records full PDF metadata and embedded subset Latin Modern font checks; all fonts have ToUnicode mappings.
- Inspected all 33 pages at contact-sheet scale, and nine full-size pages: Qui nuper 1; In amplissimo 1–2; English Rerum novarum 1, 3, 11, 16; Latin Rerum novarum 1, 14. No clipping, overlap or apparatus-only page found. Layout meets the requested classic two-column design. Literal OCR word fractures in Qui nuper remain markedly less readable under justification, as already disclosed; that is not grounds for changing source wording.
- Dependency requirements are documented, including Latin patterns/format rebuild and fallbacks. Review used the configured existing toolchain; a fresh clean-host dependency installation was not performed.
- This review does not authorize installation or cover every page of the later mass render. No repository implementation files were edited; all writes were confined to `.scratch/cold-typography/`.
