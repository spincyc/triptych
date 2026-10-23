# lectern — the terminal reader

`tools/lectern` reads what the site publishes, in a terminal: the same files
under `src/web/data/`, the same derivations, a different screen. It is a
consumer of the published structure exactly as a browser page is, and it holds
itself to the page's rules.

## The one rule

**Nothing is derived here.** A view is either read from a published file or
asked of the code that already owns its derivation:

| Owner | How the reader reaches it |
| --- | --- |
| a browser model (`src/web/browser/**/*.js`) | `bridge.js`, one long-lived node process set up as a page's realm |
| a page's own renderer (`Triptych.renderProper`, …) | the same realm, against `dom.js`, read back as blocks of styled runs |
| a published data file | `bridge.js`, through `read()` or the realm's `siteFetch` |

Where a page keeps its logic or its sentences inside its own closure — the
Day page's "Why this Mass", the history model, the law page's glossaries —
`adapters/page-slice.js` slices them out of the page source and runs them
here, as `scripts/_act_history_preview.py` already does; a slice whose marker
moves throws rather than falls back. What even a slice cannot reach is
repeated with its source line: a sentence as `// page: catena.js:571`, a few
lines of page logic as `// PORT: law.js:581-608`. A `PORT:` is the last resort,
and `tools/tests/test_lectern.py` pins what each one yields, so that a page
that changes fails a test rather than drifting from its reader.

A choice the data leaves open — a Mass the rubrics permit either way, a form,
a territorial branch, a lectionary cycle, a translation witness — is shown as
open and made only by the reader. Nothing is chosen by order, and nothing
missing is filled from elsewhere: an absence is stated where the text would
have been, with the reason the data gives.

## Layout

| File | What it is |
| --- | --- |
| `app.py` | the shell: top bar, surfaces by digit, help, themes |
| `surface.py` | the base every surface extends: built on first open, `follow(**intent)`, `where()` |
| `__init__.py` | dependency-free surface digits, labels, and module names shared by the CLI and runtime |
| `surfaces/<name>.py` | one surface per page of the site; `surfaces/__init__.py` loads them in the shared order |
| `adapters/<name>.js` | the node side of a surface: calls the page's model in the page's order |
| `bridge.js`, `bridge.py` | the node realm and its Python client; `bridge.call(adapter, fn, *args)` |
| `dom.js` | the document the page renderers write to, and `read()` back to blocks |
| `widgets.py` | `Panel`, `ScrollPanel` (rounded, titled boxes), `Ink` (theme-aware text), meters |
| `strip.py`, `month.py` | the chapter strip and the month grid |
| `timeline.py` | the scrolling box-drawn timeline and route map, and `Doc` (prose with hanging indents) |
| `missal.py` | how a reading of the Missal is set: runs by class, the Ordinary by kind |
| `dialogs.py` | `Ask` (a line of input), `Pick` (one of several), `Reading` (a long text) |
| `webedition.py` | a web edition set for a terminal: the site's locked Markdown renderer (`scripts/_markdown_render.py`), then pandoc's `ansi` writer; refuses rather than falls back |
| `theme.py` | palettes; one accent per surface (`$day-color`, `$catena-color`, …) |
| `snapshot.py` | the reader drawn headlessly, for `lectern snapshot` and the tests |

## Writing a surface

A surface subclasses `Surface`, sets `key` (its digit) and `label`, mounts its
panes in `build()`, and loads in a `@work(thread=True)` worker that calls the
bridge and hands the result back with `self.deliver(...)`, which drops the
answer of a request a newer one has superseded. Text is built
with `Ink`, whose styles may name theme variables (`"bold $catena-color"`), so
it follows a change of theme. Colour is never the only carrier of a meaning:
every state it marks is also written in words or a glyph with a legend.

`tools/lectern snapshot --surface <name> --size 140x40 [--keys a,b]` draws it
without a terminal; `--format svg` gives a picture to look at.
