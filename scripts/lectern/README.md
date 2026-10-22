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
| a repository tool | `repo.run_tool`, through the tool's own shebang |

Where a page's *prose* lives only in page code (a sentence `catena.js`
writes, a heading `day.js` groups under), the adapter repeats it and cites the
line it came from (`// page: catena.js:571`). That is the only restatement
allowed, and it is of words, never of a rule.

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
| `surfaces/<name>.py` | one surface per page of the site; `surfaces/__init__.py` orders them |
| `adapters/<name>.js` | the node side of a surface: calls the page's model in the page's order |
| `bridge.js`, `bridge.py` | the node realm and its Python client; `bridge.call(adapter, fn, *args)` |
| `dom.js` | the document the page renderers write to, and `read()` back to blocks |
| `widgets.py` | `Panel`, `ScrollPanel` (rounded, titled boxes), `Ink` (theme-aware text), meters |
| `strip.py`, `month.py` | the chapter strip and the month grid |
| `missal.py` | how a reading of the Missal is set: runs by class, the Ordinary by kind |
| `dialogs.py` | `Ask` (a line of input), `Pick` (one of several), `Reading` (a long text) |
| `theme.py` | palettes; one accent per surface (`$day-color`, `$catena-color`, …) |
| `snapshot.py` | the reader drawn headlessly, for `lectern snapshot` and the tests |

## Writing a surface

A surface subclasses `Surface`, sets `key` (its digit) and `label`, mounts its
panes in `build()`, and loads in a `@work(thread=True)` worker that calls the
bridge and hands the result back with `app.call_from_thread`. Text is built
with `Ink`, whose styles may name theme variables (`"bold $catena-color"`), so
it follows a change of theme. Colour is never the only carrier of a meaning:
every state it marks is also written in words or a glyph with a legend.

`tools/lectern snapshot --surface <name> --size 140x40 [--keys a,b]` draws it
without a terminal; `--format svg` gives a picture to look at.
