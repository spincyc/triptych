# Web data: fragments, structure, and why nothing is pre-rendered

The published pages are assemblers. The repository carries structured data; a
page fetches the structure it needs, fetches only the fragments that structure
names, and puts them together in the browser.

Pre-rendering is the thing to avoid, and it is worth being explicit about why.
A propers browser offers a mass and a translation. Rendering those combinations
ahead of time is 596 masses times however many translations, and adding a
translation would rewrite every page. The same trap sits one level down: a
fragment set keyed by mass and translation would be just as combinatorial. So
the rule is that **file counts must be additive, never multiplicative**. Adding
a translation adds that translation's fragments and changes nothing else.

## The four layers

Each layer is generated from the one above it and is checked against it, so a
consumer never has to trust that two representations agree.

### 1. Verse text — canonical

Per-book TSVs under `src/sources/works/<publisher>/<work>/editions/<edition>/`,
each with an artifact record carrying its hash, rights basis, and the exact
transformation that produced it. This is the only layer with provenance, and it
is the only layer a rights question is ever answered from.

### 2. Chapter fragments — what a reader fetches

`<bible-root>/<edition>/chapters/<BookToken>/<chapter>.json`, written by
`index-bible build`:

```json
{"book":"Ps","chapter":24,"verses":{"1":"Unto the end, a psalm for David...","2":"..."}}
```

A chapter is the unit that is small enough to send for a three-verse antiphon
and large enough to serve a reading that runs to the end of one — around 3 KB
in the middle of the distribution, 15 KB at the worst. The passage range does
the cutting, so a fragment never needs regenerating when a citation changes,
and the same fragments serve the propers browser and the reading plan.

`index-bible check` verifies every fragment against a fresh derivation and
fails on three things: a fragment that differs, a fragment that is missing, and
a fragment left behind after the chapter that produced it stopped being
derived. The third matters most — an orphan is the failure that looks like
success.

Fragments follow `--bible-root`, so a licensed edition's fragments are written
outside the repository along with its index and cannot reach the public tree.

### 3. Structure — citations resolved

`<out>/propers/<calendar>.json`, written by `mass-propers structure`:

```json
{"ref":"Psalm 24:1-3","book":"Psalms","token":"Ps",
 "loci":{"vulgate":[{"chapter":24,"first":1,"last":3}],
         "hebrew":[{"chapter":25,"first":1,"last":3}]},
 "unresolved":null}
```

Every citation is resolved here, in both numbering systems, so that **no
numbering logic ships to the browser**. A page reads its chosen translation's
`numbering` and takes the loci already computed for it. Two variants, not one
per translation: numbering is a property of the system, not of the edition.

A citation that cannot be converted carries the reason in `unresolved` and no
loci at all. This is the load-bearing rule of the whole design. The eleven
postconciliar antiphons that carry Vulgate numbers inside a Hebrew-declared
file would otherwise resolve to real, wrong verses, and a page would render
them confidently. A page that explains itself beats one that is quietly wrong.

Cycle-varying propers keep each year's citations apart under `cycles`, because
a merged list is one the browser cannot tell apart — and because merging them
silently dropped 43% of the postconciliar citations when it was first written.

### 4. Manifest — what may be offered

`<out>/bibles.json`, written by `index-bible manifest`, lists exactly the
editions whose records say `publishable: true`. A licensed text is excluded
when the file is generated rather than filtered in the page, so a browser
cannot offer what the project has no right to serve even if its fragments were
somehow present beside it.

## The calendar layer

`structure/calendar/<calendar>/<civil-year>.json`, written by `calendar-days
structure`, answers the one question the four layers above cannot: which mass
does a given date point at. It sits beside the structure files rather than
above them, because it is derived from the calendar's mass index and the
arithmetic in [calendar computation](liturgy/calendar-computation.md), not from
verse text.

One file per civil year per calendar is additive in both directions: a year
adds one file per calendar and a calendar adds one file per year. A file per
date would be neither, and it is the trap the propers browser already avoids.
`structure/calendar/index.json` names the calendars, the span, and the path
template, so a page discovers the set with one fetch and then fetches the year
it wants.

The layer is a **finding aid and never an authority**, which is a constraint on
the data and not only on the page. A date carries every candidate the rules
reach — a temporal day and a fixed-date feast both stand, unranked, because no
general table of precedence is stated. A celebration whose transfer to a Sunday
belongs to the competent authority carries both forms, each tagged with the
option it holds under, so nothing in the file resolves a territorial decision by
arithmetic. Where the rules run out — a year with no Sunday in the Christmas
octave, a 1962 year with twenty-three Sundays after Pentecost — the year records
the refusal in `unresolved` instead of choosing. Each file carries the advisory
that says so, so the caution cannot be separated from the data.

## The rubrics layer

`structure/rubrics/<calendar>.json`, written by `calendar-rubrics structure`,
supplies the one thing the calendar layer deliberately withholds: the ranking.
It is a separate layer rather than a field on the day files, because it is a
separate kind of claim. A day file says *this date carries these masses*, which
is arithmetic. A rubrics file says *this one takes the day, under this numbered
rubric*, which is a reading of a code — and a reading has to be citable,
arguable, and correctable in one place.

The layer is **one file per calendar and none per year**. That is the whole of
its storage design and it is not an optimisation: an assembly precomputed per
date per calendar would be some seventy-four thousand objects over the span the
day files cover, and correcting a single rubric would invalidate every one of
them at once. So the page fetches the rules once, the year it wants once, and
derives the day in the browser. Adding a year adds nothing here; adding a
calendar adds one file.

The source is `src/sources/calendars/<calendar>/rubrics.yaml`, beside the mass
index it classifies. It carries the precedence table with its locus, the bases
that assign each mass to a row, the rules that constitute a day the index has no
formulary for, the commemoration ceilings, the oration rules, and — as much as
the rest — what it does not decide. Every rule names the rubric number behind
it, and every rule is transcribed from a collated in-repository publication
rather than read afresh. Where the file departs from that publication it says so
in `divergences` and does not silently choose.

Two consequences are worth stating because they are easy to erode:

- **`calendar-days` is not changed by this.** Its refusal to rank was correct
  and stands; `precedence.stated` is still `false` in the day files. The
  authority arrives as a separate tracked artifact that can be checked and
  disagreed with on its own.
- **A calendar directory now holds more than one kind of file.** Discovery under
  `src/sources/calendars` is therefore by declared `schema`, in
  `scripts/_calendars.py`, shared by every tool that reads the directory. A file
  whose schema nothing claims is a hard failure: silently skipping it would let
  a mass index with a mistyped schema stop being checked.

The derivation itself lives in `src/web/browser/liturgy/assembly-model.js` and
exists once. `calendar-rubrics check` runs that same file under node against the
solved cases each source carries, so the page and the check cannot drift; where
node is absent the check says which verification it did not perform instead of
passing quietly.

## Assembling the site

Five of the pieces are generated straight into the data root:

```sh
tools/tpt mass-propers  structure --out src/web/data  # structure/propers/*.json
tools/tpt reading-plan  structure --out src/web/data  # structure/readings/*.json
tools/tpt calendar-days structure --out src/web/data  # structure/calendar/**/*.json
tools/tpt calendar-rubrics structure --out src/web/data  # structure/rubrics/*.json
tools/tpt index-bible   manifest  --out src/web/data  # bibles.json
```

The fragments are the exception, and deliberately so. They live beside the
edition that owns them, at `src/sources/bibles/<edition>/chapters/`, because
that is where `index-bible` checks them for staleness and orphans. Copying them
into the data root as well would put the same verse text in the tree twice.

So the deploy copies, for each edition named in `bibles.json` and no other:

    src/sources/bibles/<edition>/chapters/  ->  <site>/<edition>/chapters/

Driving the copy from `bibles.json` rather than from the directory listing is
what keeps a licensed edition out of the site: an unpublishable edition is
absent from the manifest, so it is never copied, even if its fragments were
sitting in the tree. A deploy that walked `src/sources/bibles/` instead would
publish whatever it found.

`tools/public-alpha build` performs that assembly, into `data/` inside the
artifact, so the browser reaches the whole root through one `?data=` setting.
`tools/public-alpha verify` re-derives the same map and refuses the artifact if
it carries an edition the served `bibles.json` does not offer, or if a chapter
the structure files cite has no fragment beside it in the edition's own
numbering.

## Rights

Only the verse text is rights-bearing. The propers definitions, the reading
plan, and the structure files are the project's own work or are bare
references, and a reference is a fact. That is why a licensed translation
changes nothing structural: it ships fragments or it does not.

Permission to *use* a text is not permission to *republish* it, and an
ecclesiastical imprimatur is not a copyright licence — it attests that a work
is free of doctrinal error and says nothing about who may copy it. An edition
becomes `publishable: true` on the strength of a licence from whoever holds the
copyright, recorded with the acknowledgement wording that licence requires.

## Adding a translation

1. Register the edition and its verse text in the source library, with rights.
2. Add it to `EDITIONS` in `tools/index-bible`, declaring `language`,
   `numbering`, `psalter`, `rights`, and `publishable`.
3. `index-bible build` for its index and fragments; `index-bible manifest` to
   refresh the offered list.

Nothing else changes. No page is rewritten, no structure file is regenerated,
and no existing fragment is touched.
