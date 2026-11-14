# lectern — the terminal reader

`tools/lectern` reads the site's corpus in a terminal, using the same
source-owned derivations, publication filters and browser models. It loads
selected records through the shared thin index under `src/index/` instead of
building the complete set of browser products before opening a reading.

Both `open` and `snapshot` check index membership against Git and dirty paths,
then read the discovery metadata and canonical dependencies the selected view
needs. Actual input bytes are SHA-256 verified before use. Missing or stale
index data fails with maintenance instructions; startup never repairs it,
adopts changed hashes or starts a full site build. The complete contract is in
[Web data](../../guidance/web-data.md#tracked-discovery-and-ordinary-indexed-reading).

Interactive startup paints a loading screen while the index check and initial
chained loads finish. The screen reports preparation errors; `q` or `ctrl+c`
closes it. The check runs once, in a worker thread, and the first reading
session opens on that same checked membership; a restarted bridge checks
afresh. The check starts no producers, so cancelling simply discards it.
Snapshots check synchronously before their settling timer, report progress to
stderr, and emit only the completed drawing on stdout.

Install the pinned dependencies once with `python3 -m venv
.scratch/lectern-venv` and `.scratch/lectern-venv/bin/python -m pip install -r
requirements-tui.txt`. The ordinary command automatically selects that environment
in isolated Python mode and puts its executables on the child-process PATH.
Conflicting Python import-path and home settings are removed for those children.
An installed converter under `.scratch/web-edition-toolchain` is also found
automatically; `--help` documents its explicit installation. No shell activation
or cache/PATH exports are needed. Without a local environment the current Python
is used; a broken local environment is refused, with setup help still available.
Ordinary startup never installs packages or downloads tools.

The bridge holds one index membership view for its Node process lifetime and
passes immutable, verified bytes to the browser realm. It checks newly consumed
canonical bytes against that view; changing sources requires index maintenance
and a new reader session. Selected projections have a bounded memory cache and
a disposable disk cache under `.scratch/reader-data`, bound to code, history
and verified dependencies. Calendar-wide derivations that every selected Mass
needs are computed once per session and re-verified on reuse, as
[Web data](../../guidance/web-data.md#tracked-discovery-and-ordinary-indexed-reading)
states. `TRIPTYCH_BROWSER_DATA_ROOT` still controls full
publication builds; it is not the ordinary reading cache. Explicit verified
browser-product snapshot mode remains available for product audits.

Opening a publication can invoke its pinned converter for that edition. Other
views do not wait for unrelated publication conversions. Installation,
checkout and maintenance commands are in
[Reader setup and performance](../../docs/reader-performance.md).

## The one rule

**Every derivation keeps its existing owner.** A view reads a verified record
or asks the producer or browser code that already owns its derivation:

| Owner | How the reader reaches it |
| --- | --- |
| a browser model (`src/web/browser/**/*.js`) | `bridge.js`, one long-lived node process set up as a page's realm |
| a page's own renderer (`Triptych.renderProper`, …) | the same realm, against `dom.js`, read back as blocks of styled runs |
| a selected data record | `data.py` verifies dependencies; the existing producer supplies the logical browser payload through `bridge.js` |

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
open and made only by the reader. No coequal option is chosen by incidental
order; declared page and source defaults retain their stated basis. Nothing
missing is filled from elsewhere: an absence is stated where the text would
have been, with the reason the data gives.

## Day and Propers

Day (`1`) starts with a civil date and the browser's calendar resolution.
Propers (`2`) starts with a particular formulary, independently of a date;
without a selection it opens Browse. Both use the browser's semantic event
order, Proper and Ordinary renderers, source witnesses, rights qualifications
and coverage notices. Missal mode seats the Propers in the selected Ordinary.
Missing text and unresolved source conditions remain explicit.

| Key | Reading action |
| --- | --- |
| `c`, `o`, `b` | Next missal, oration language, or Bible edition |
| `m`, `r` | Toggle Missal mode; show or hide Ordinary rubrics |
| `L` | Choose the Ordinary language independently, in Missal mode |
| `B` | Pair Latin prayers with the selected language, or return to that language alone |
| `K` | Choose or remove a named Latin Bible companion; each Bible retains its own numbering and refusals |
| `w` | Choose an oration witness available within this Mass, including partial witnesses |
| `s` | Choose an offered Mass, form, cycle, Ordinary option, or source reading path |
| `i` | Open Contents at the actual semantic units; choose a destination without returning to the beginning |
| `d` | Open Study: calendar, coverage, placement, sources and full translation notes |
| `v`, `V` | Toggle Compare, or choose its peers |
| `u` | Copy and display the canonical website URL for this reading and semantic location |
| `g` | Enter a date or reader URL on Day; enter a reader URL on Propers |
| `f` | Show or hide navigation; on compact screens, swap navigation and reading |
| `?` | Show the current surface's full help and calendar-mark legend |

Day also provides previous/next day with the arrow keys, previous/next week
with `[` and `]`, previous/next month with `{` and `}`, and Today with `t`.
Its `p` opens the current formulary in Propers while preserving its material
reading choices. Propers provides `/` search and `[`/`]` movement within the
current browse or search result. The selected form stays highlighted; search
results show language availability before opening a reading.

Day Compare resolves the same date independently under two missals and an
explicit shared territorial context. Propers Compare keeps the formulary
independent of a date and offers supported pairs of oration languages,
lectionary cycles, source reading alternatives, translation witnesses or Bible
editions. Both use the production comparison builder, including its refusals;
neither resolves a coequal choice merely to make a comparison succeed.

Reader URLs use the browser's validation and canonical serializer and the
publisher's declared site origin. Import accepts canonical and retained Day
and Propers routes, preserves unknown and inert legacy hash fields, and
replaces prior semantic choices with the explicit URL state. A bare Propers
route opens Browse. Invalid locations and custom browser data roots are
refused: this reader consumes the published checkout data. Sharing also
reports when a narrowed territorial Read view has no equivalent browser URL.

Below 90 columns, Day and selected Propers readings start with the text;
an unselected Propers entrance starts with Browse. `f` swaps the two surfaces,
and `/` reveals Browse before focusing search. At wider sizes, `f` toggles the
side panes. Contents and ordinary reading changes preserve a corresponding
semantic location, including through bilingual reflow and mode changes.

The terminal uses keyboard navigation and scrolling, modal Study and choice
dialogs, and terminal clipboard support. Propers Compare stacks corresponding
units; Day can place their sides in columns. Browser print, touch controls and
font enlargement retain their native implementations. These presentation
differences do not create another liturgical model or substitute source text.

## Catena commentary

Where a held fragment declares reviewed passage excerpts, opening it shows the
excerpts matching the selected canonical chapter or verse range. The shared
browser model validates and slices the unchanged source text; each excerpt
keeps its own extent, locator and selection basis. Press `c` to read the complete
source passage and press it again to return to the excerpts. `s` still opens the
same passage in the Source Library; `n` and `p` walk the commentary chain.
Without an applicable excerpt the reader shows the complete natural fragment.
Required acknowledgements stay visible in both views.

## Source Library

The finder opens with compact metadata for the first page of works. Browsing
forward loads further discovery shards; a search, filter or different sort
loads the metadata needed to search the complete catalogue. A partial load is
never reported as a complete search. Edition details and passage text remain
separate selected reads. The browser and terminal share the finder model,
rights dispositions, exact edition identities and passage links.

## Layout

| File | What it is |
| --- | --- |
| `app.py` | the shell: top bar, surfaces by digit, help, themes |
| `surface.py` | the base every surface extends: built on first open, `follow(**intent)`, `where()` |
| `__init__.py` | dependency-free surface digits, labels, and module names shared by the CLI and runtime |
| `surfaces/<name>.py` | one surface per page of the site; `surfaces/__init__.py` loads them in the shared order |
| `adapters/<name>.js` | the node side of a surface: calls the page's model in the page's order |
| `bridge.js`, `bridge.py` | the node realm and its Python client; `bridge.call(adapter, fn, *args)` |
| `data.py` | the indexed reading session and disposable cache of selected projections |
| `dom.js` | the document the page renderers write to, and `read()` back to blocks |
| `widgets.py` | `Panel`, `ScrollPanel` (rounded, titled boxes), `Ink` (theme-aware text), meters |
| `strip.py`, `month.py` | the chapter strip and the month grid |
| `timeline.py` | the scrolling box-drawn timeline and route map, and `Doc` (prose with hanging indents) |
| `missal.py` | styles the browser-rendered Proper and Ordinary blocks, cues and explicit absences |
| `reader_navigation.py` | Contents and scroll positions over stable event IDs; canonical link display through the publisher's URL owner |
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
