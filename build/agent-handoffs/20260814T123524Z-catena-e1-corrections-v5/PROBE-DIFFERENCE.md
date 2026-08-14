# Probe difference — V4.1 base against V5 head, real Chromium, identical fixtures

Base is `f93757854b54c19e50bdcb97ca0fed9b48d22bb7`; head is this candidate's
implementation commit. Both were served from their own `make public-site`
build by `logs/probe-catena.mjs`, which injects the same fabricated fixtures
into each. Only the fields that DIFFER are shown; every other field of every
probe is identical, which is itself part of the evidence.

**Every fixture is fabricated adversarial data and represents no holding of
this project.** See `LIMITATIONS.md` section 1.

## malformed-language-everything-held

_blocker 1 — a DOM lang attribute composed from a record_

Address `#book=Gen&chapter=1&bible=douay-rheims`

### `langAttributes`

```
base: ["passage=en", "fragment-text=la", "fragment-text=[object Object]", "fragment-text=la", "fragment-text=42", "fragment-text=true", "fragment-text=   ", "fragment-text=not a language code"]
head: ["passage=en", "fragment-text=la", "fragment-text=en", "fragment-text=en", "fragment-text=en", "fragment-text=en", "fragment-text=en", "fragment-text=en"]
```

### `languageChips`

```
base: ["Latin — the author’s own", "NOT A LANGUAGE CODE — the author’s own"]
head: ["Latin — the author’s own"]
```

## mixed-collection-members

_blocker 2 — counts, refusals and surviving siblings_

Address `#book=Gen&chapter=1&bible=douay-rheims`

### `asideNotes`

```
base: []
head: ["3 unreconciled lead entries on the acquisition record for this chapter, which omits its confidence. An entry establishes no distinct work, no possession and nothing renderable, and the list is not checked against the commentary above."]
```

### `blocked`

```
base: []
head: ["Blocked One — Blocked Work Onerights", "", "Blocked Two — Blocked Work Tworights"]
```

### `dataStates`

```
base: []
head: ["blocked", "held", "lead"]
```

### `extents`

```
base: []
head: ["Genesis 1:1", "Genesis 1:2", "Genesis 1:5"]
```

### `fragmentCount`

```
base: 0
head: 3
```

### `langAttributes`

```
base: []
head: ["passage=en", "fragment-text=la", "fragment-text=la", "fragment-text=la"]
```

### `languageChips`

```
base: []
head: ["Latin — the author’s own", "Latin — the author’s own", "Latin — the author’s own"]
```

### `leads`

```
base: []
head: ["Lead One — Lead Work One (500)", "", "Lead Two — Lead Work Two (600)"]
```

### `status`

```
base: "This chapter could not be loaded: Cannot read properties of null (reading 'source')"
head: "Genesis 1, Douay-Rheims (Challoner), 3 fragments held, 3 works held, not renderable yet, 3 lead entries on the acquisition list."
```

### `tally`

```
base: ""
head: "3 fragments held · 3 works held, not renderable yet · 3 lead entries on the acquisition list"
```

### `wordChips`

```
base: []
head: ["4 words", "4 words", "4 words"]
```

## typed-absence-findings

_blocker 3 — what each typed finding licenses the page to say_

Address `#book=Gen&chapter=1&bible=douay-rheims&voice=translation:en`

### `absenceSummary`

```
base: "4 works standing here have no English this project may publish; 1 has only a partly public domain English, not yet taken"
head: "2 works standing here have no English this project may publish; 1 has only a partly public domain English, not yet taken; 1 has not been surveyed for English; 1 has a finding this page cannot read"
```

## malformed-word-tallies

_blocker 4 — a tally is a number the record wrote_

Address `#book=Gen&chapter=1&bible=douay-rheims`

### `wordChips`

```
base: ["1,200 words", "1,200 words", "1 words", "12.5 words"]
head: ["1,200 words"]
```

## malformed-held-path

_blocker 4 — a path that is not text is not fetched_

Address `#book=Gen&chapter=1&bible=douay-rheims`

### `requested`

```
base: ["browse/[object%20Object]001.json", "browse/bibles.json", "browse/douay-rheims/chapters/Gen/1.json", "browse/structure/catena/index.json", "browse/structure/paragraphs/douay-rheims/01-gen/001.json", "browse/structure/paragraphs/index.json"]
head: ["browse/bibles.json", "browse/douay-rheims/chapters/Gen/1.json", "browse/structure/catena/index.json", "browse/structure/paragraphs/douay-rheims/01-gen/001.json", "browse/structure/paragraphs/index.json"]
```

## malformed-canon-bootstrap

_blocker 4 — the bootstrap record, and the terminal state it owes_

Address `(no address)`

### `ariaBusy`

```
base: null
head: "false"
```

### `bookOptions`

```
base: ["Loading…"]
head: ["Unavailable"]
```

### `reference`

```
base: "Loading…"
head: "Unavailable"
```

### `status`

```
base: null
head: "The catena index could not be read."
```
