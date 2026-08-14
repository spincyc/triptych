# How the V5 evidence was produced

## The instrument, and why it is a new one

`logs/probe-catena.mjs`. Hand-written DevTools-Protocol client over
`--headless=new`, no Playwright, no Puppeteer, no `node_modules` — the same
shape as the gate and the V4.1 capture tools this package carries forward.

It exists because **the tools carried forward cannot evidence this
correction.** `capture-catena.mjs` visits only real corpus addresses and its
header says so: *"Every address below is real repository data … Nothing is
fabricated for the picture."* The corpus holds no malformed data, so no real
address can exhibit the behaviour under review. The shared browser gate cannot
help either: its `--routes` flag takes paths, not hash addresses, so it cannot
reach a Catena route state at all.

And four of the five blocking classes turn on facts **a picture cannot carry**:

| Class | The fact | Visible in a raster? |
| --- | --- | --- |
| 1 | a DOM `lang` attribute | no |
| 2 | which collection members survived | partly — the crash is visible |
| 3 | the absence summary sentence | yes |
| 4 | which URL the page requested | no |
| 4 | `aria-busy` after a malformed bootstrap | no |

So the probe **reads the live DOM and the live resource log** in the same
browser, at the base and at the head, and the JSON reports are the evidence.
Screenshots are added only where rendering visibly differs.

## Exact invocation

```
make public-site                       # at each head, into build/public-alpha/site

node logs/probe-catena.mjs build/public-alpha/site \
     logs/probe-head.json "V5 head" screenshots/ "after--"

node logs/probe-catena.mjs <v4.1 build>/public-alpha/site \
     logs/probe-base.json "V4.1 base f93757854" screenshots/ "before--"
```

Chromium is found at `$TRIPTYCH_CHROME` or `/usr/bin/chromium`. No display
server is needed. The debug port is derived from the process id; the static
server binds an ephemeral `127.0.0.1` port.

## How the fixtures are injected — and what is NOT modified

The probe runs its own static server over the built site. A fixture is
substituted **in the response path**, keyed by the request path. Nothing on
disk is written: `build/public-alpha/site` is byte-identical before and after
a run, and the two runs read two different, unmodified builds.

Every fixture is **fabricated adversarial data**. It represents no holding of
this project. See `LIMITATIONS.md` §1.

## Settling

Fixed 1,400 ms, then up to 40 × 100 ms polling until
`#reading[aria-busy] !== 'true'`. The bootstrap probe deliberately reaches a
state where the base never sets `aria-busy` at all — that is the finding — so
the poll falls through and the report records `ariaBusy: null` for the base and
`"false"` for the head.

## Screenshots

Five states, two viewports each, `before--` and `after--`: **20 PNGs**.
Filenames follow the repository grammar,
`<before--|after-->catena--<state>--<WxH>.png`. Viewports are 1440×900 and
393×852. Media is `screen`; no print or forced-colors variant is offered,
because `catena.css` is byte-identical and nothing in this correction bears on
those media — V4.1's accepted 53-image matrix already covers them and is
neither superseded nor re-issued.

Captures are `Page.captureScreenshot {format:'png', captureBeyondViewport:false}`
written straight to disk. Chromium's CDP encoder writes no `tEXt`, `iTXt`,
`zTXt`, `eXIf`, `pHYs` or `tIME` chunks, so the PNGs carry no metadata and none
had to be stripped. They are page-content captures, not desktop grabs: no
browser chrome, title bar, path, user name or host name appears in any of them.

`screenshots/after--probe-index.json` and `before--probe-index.json` inventory
them machine-readably: file, state, address, viewport, variant, media, what the
image shows, and byte length.
