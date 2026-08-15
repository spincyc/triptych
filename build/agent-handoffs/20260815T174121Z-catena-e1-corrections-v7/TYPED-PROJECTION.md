# The typed projection — what crosses the boundary, and what does not

The V6 independent review's central finding, in its own words:

> The typed boundary is not complete. `chapterFragments()` copies every raw
> fragment property and clears `text_path` only when both normalized
> identities are valid. A malformed fragment can therefore retain an injected
> `text_path`, which `openFragment()` passes to the real request sink.

This is the account of what V7 did about that, and about the six other
blocking classes the review named beside it. Every claim below is driven at a
production sink by a test named in `EVIDENCE-INDEX.md`; none is asserted from
reading the source.

---

## 1. The shape that was wrong

V6 joined a fragment to its shared source record like this:

```js
const joined = {};
for (const name in shared) if (Object.hasOwn(shared, name)) joined[name] = shared[name];
for (const name in fragment) if (Object.hasOwn(fragment, name)) joined[name] = fragment[name];
const id = ident(fragment.id);
joined.id = id;
if (id && prefix) joined.text_path = prefix + id + '.json';
```

Read the last line as a condition rather than as an assignment and the defect
is plain: **`text_path` is overwritten only when a valid composed form
exists.** Where the fragment's id or the file's `text_prefix` could not be
read, the record's own `text_path` — whatever it was — survived the copy
intact, and the page requested it when a reader opened the fragment.

The wider fault is the loop above it. A shallow copy carries **whatever the
data happens to hold**, so the set of fields flowing downstream is not a set
the page has ever agreed to. A boundary of that shape has to be re-established
at every later sink, and the record shows exactly that: V4 found one such sink,
V5 found more, V6 found more, and the review found this one.

## 2. The shape V7 uses

`fragmentRow` builds a record of **known fields only**. There is no
`joined[name] = raw[name]` anywhere in it. Each field is validated for the use
the page actually puts it to:

| projected field | gate | why that gate |
| --- | --- | --- |
| `id` | `ident` | becomes a fetched path and a Source Library href |
| `text_path` | composed, never carried (§3) | the request sink |
| `author`, `work`, `locator`, `edition`, `edition_published`, `rights`, `attribution`, `rights_basis`, `review` | `sound` | visible prose |
| `date` | `say` | legitimately a number or text |
| `language` | `tongue` | reaches a DOM `lang`, which a screen reader reads |
| `voice` | `original`/`translation` only | there is no third, and an unrecognised one answers no selection |
| `text_words` | `whole` | a tally is a number the record wrote |
| `extent.*` | `bookToken` / `whole` | the locus is printed and the chapter membership decided from the same four numbers |
| `translators` | `list` + `sound` per member | a scalar is not a one-item list |
| `acknowledgement` / `acknowledgement_broken` | `sound`, and a separate "something was recorded and is not text" | collapsing them printed nothing where the record said something unreadable |

A field this page does not name is a field this page does not carry.
Everything downstream — the rows, the tally, the voice filter, the chips, the
provenance line, the Source Library link and the one request a fragment can
cause — reads this record and never the raw one.

**The minimum a fragment must state.** A row is the page saying this project
holds this commentary here. A record that can name neither an identity of this
corpus, nor an author, nor a work states no part of that, so it is not a thin
fragment — it is not a fragment. `{}` used to render an `<li>` with an empty
author, an empty work, a perpetual "Loading…" and no locator, and was counted
into "3 fragments held here": possession claimed by an empty object.

## 3. `text_path`, and the two ways it can be arrived at

**Composed.** Where the spine states a `text_prefix`, the path is
`trail(prefix) + ident(id) + '.json'` and nothing else. Both parts are
validated grammars of this data root; the result cannot leave it.

**Carried.** The sample corpus under `src/web/browser/fixture/` — which
`?data=fixture` serves, and which the page's own inline notice offers to a
reader with no data root — states no `text_prefix` and carries a literal
`text_path` per fragment. Discarding it outright would have told a reader that
47 fragments carry no text file, which is false. So a carried value may stand
in, under two conditions together:

1. it satisfies `leaf` — a relative JSON file of this data root's grammar:
   lowercase alphanumeric segments joined by `.` or `-`, each closed by one
   slash, and a `.json` suffix. No leading slash, no `..`, no percent-encoding,
   no scheme, no query, no space; and
2. **its stem is this fragment's own validated `id`.**

The second condition is the one that matters. It means a carried path can
address exactly one thing — the text of the fragment that carried it — so an
injected path names some other file *by definition* and is refused. All 47
fixture paths satisfy it unchanged; `carried-other` in
`V7_TEXT_PATH_NO_PREFIX` is a sound, relative, correctly formed path inside
the text directory that names somebody else's file, and it is refused.

**Proved at the sink, not at the helper.** `V7TextPathRequestSinkTest` opens
*every* fragment of two chapters and pins the whole request journal. That
matters: a request is composed only when a fragment is opened, so a scenario
that opens one fragment proves nothing about the eleven beside it — which is
how "no unsafe path was requested" held at V6 while the path was reachable.

## 4. The other six classes, in one line each

- **Fragment members.** `V7HollowFragmentMemberTest` feeds `valid, {},
  malformed record, null, scalar, valid` in **both orders** and pins that only
  the two valid members render and are counted, that no blank row stands, and
  that no refusal, absence or emptiness is manufactured.

- **Absence members.** The source is validated *before* it claims a work's
  row, so a source naming neither author nor work no longer renders a blank
  entry and mask the valid sibling behind it. A member that names no language
  is not an absence record at all.

- **Refusal members.** "Boundary not established" is the strongest sentence
  this page says about a text it did not write, and it now needs the whole
  typed record the projection writes: the closed `kind`, the chapter **matched
  against the chapter being read**, and the note.

- **Contradictory findings.** Where no single recognised finding can be read,
  there are no carriers, so there is no prose. V6 blanked the finding and then
  printed one side's `reason`, chosen by ranking the two on length.

- **`partial`.** Prose or nothing, and only under `partial-public-domain`. The
  browser half was already right in V6; `scripts/_catena.py` was not —
  `str(row.get("partial") or "")` turned a mapping into `"{'a': 1}"`. Both
  prose fields are now refused at build time when they are not text, and a
  `partial` detached from its finding is refused with them.

- **Unreadable roots.** `chapterPath`, `paragraphPath`, `chapterReading`,
  `canonRoot`, `bibleRoot` and `voiceRoot` each distinguish *we read it and
  found nothing* from *we could not establish what is there*. Those are not
  interchangeable sentences and V6 was answering the first while meaning the
  second, for holdings, canon, voices, editions, the paragraph layer and the
  verses container alike.

## 5. Where the code went, and what it cost

`src/web/browser/catena/catena.js` finished V6 with **seven** gzipped bytes under its whole-file
ceiling. The projection is not payable out of seven bytes in any form, so it
lives in `src/web/browser/catena/catena-model.js`, which carries no ceiling — the same move V5 and V6
made, for the same arithmetic. The address judgment moved with it, because the
sentence "…is not a book of this canon" and the root that licenses it must not
be able to drift apart, and because that sentence was one of the defects.

The page came out **smaller in both measures**. The model grew, and the exact
figures for both — including the two files' combined payload, measured as one
stream and summed separately, because neither alone is the load a reader pays
— are in `DERIVED-CLAIMS.md`, computed at the sealed head.

The V5 review asked whether that much explanation belongs in an unbudgeted
model, and the V6 review asked again. Neither was answered.
`REVIEW_REQUEST.md` asks a third time, and this lane trimmed its own additions
by a measured amount first rather than treating the silence as consent.

---

## 6. The shape the three self-review passes had

Worth recording, because it is a fact about this correction rather than about
this lane, and a successor meets it again.

Every pass found real defects, and each round was mostly the same class one
level under the last:

| round | what was closed | what the next round found under it |
| --- | --- | --- |
| the correction | `text_path` carried forward | `paragraphPath` still fell back to a digit width of 1; `chapterPath` consulted its readability flag on one of two exits |
| second | the chapter PAYLOAD given a third answer | its CONTENTS had not been: `fragments` as a record, `sources` as a list, `refusals` as a string |
| second | `null` replaced as the 404 in one place | it was still the 404 in three others |
| third | the `sources` ROOT guarded | its MEMBERS were not, so the voice control still said "none here" of a chapter holding nine Latin fragments |
| third | a sentinel that `null` could not forge | one a PAYLOAD could: a key named `absent`, and one named `unfetched` whose string reached a reader |
| third | the layer ROOT's transport failure caught | the optional FILE's, one scope under it, still took the page down |

The generalisation, stated so the next lane can check it directly: **whenever
this page distinguishes "we read it and found nothing" from "we could not
establish what is there", ask the same question one level in.** Of the
container and then of its members; of the root and then of each record under
it; of the request and then of the payload it returned. Every one of the
nineteen defects the three passes found is an instance of not having asked it
one level deeper than the fix that preceded it.

That is also why `LIMITATIONS.md` does not claim the bottom was reached.
