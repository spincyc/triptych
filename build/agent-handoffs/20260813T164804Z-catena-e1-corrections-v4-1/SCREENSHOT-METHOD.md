# Screenshot evidence: method, and the correction of V4's stated reason

## V4's reason did not hold

V4 recorded, in `LIMITATIONS.md` and `REVIEW_REQUEST.md`:

> The review asked for a capture of the visible refusal change. **No display was
> available to this session**, so the refusal change is evidenced structurally
> — replayed DOM projections, roles, labels, status writes — and not visually.

That reason is **incorrect**, and this lane records the correction plainly:
headless Chromium requires no display server. The capability was not tested; it
was inferred from the absence of a desktop session, which is a different fact.
The screenshots the review asked for were producible in the same environment.

This is stated as a factual correction of the record, not as a criticism of the
structural evidence V4 produced, which stands on its own.

## What is actually available here

Probed, not assumed:

```
$ command -v chromium
/usr/bin/chromium
$ /usr/bin/chromium --version
Chromium 151.0.7922.108 Arch Linux
$ command -v node
/usr/bin/node          (v26.7.0)
$ fc-list | wc -l
1981
```

Playwright, Puppeteer and Selenium are all absent — and irrelevant. The
repository does not use them: `tools/tests/corpus_browser_gate.mjs` drives
`/usr/bin/chromium` directly over the DevTools Protocol with no third-party
dependency, and it discovers that binary automatically. The gate is a **real
browser harness**, not a DOM simulator; its own header says "driven by real
Chromium", and it spawns

    --headless=new --no-sandbox --disable-dev-shm-usage --disable-gpu
    --remote-debugging-port=<port>

The gate already supports screenshots: `--capture-dir <dir>` writes one PNG per
route per state as `<route-slug>--<state>--<WxH>.png`.

## Why this lane did not simply run `--capture-dir`

The shared gate's route list carries exactly one Catena address, the ordinary
populated one (`corpus_browser_gate.mjs:128`). It carries **none** of the
fail-closed or refusal addresses this review is about. Adding them would mean
editing the common browser gate, which is another owner's surface and outside
this lane's authority.

So the capture is done with the **same engine and the same flags**, by a
lane-local script that adds only the missing Catena addresses:
`logs/capture-catena.mjs` and `logs/capture-provenance.mjs`, both shipped in
this package as evidence artifacts rather than added to repository tooling.
This follows the precedent V4 set with `logs/sanitize-and-seal.py`.

## Exact commands

Built artifact (the set published to GitHub Pages):

    make public-site                    # -> build/public-alpha/site

`before--` images, from the parent commit's artifact:

    git switch --detach e40720d5d622e8b0528b8c714cc5caee0b21cee3
    make public-site
    node <package>/logs/capture-catena.mjs build/public-alpha/site <out> "before--"

`after--` images, from the V4.1 head's artifact:

    git switch impl/catena-wave-1-e1-corrections-v4-1
    make public-site
    node <package>/logs/capture-catena.mjs build/public-alpha/site <out> "after--"
    node <package>/logs/capture-provenance.mjs build/public-alpha/site <out>

Both scripts serve `build/public-alpha/site` over a loopback `node:http` server
on an ephemeral port, exactly as the gate does, and honour `TRIPTYCH_CHROME`.

## What was captured

53 PNGs. Nine route states x three viewports (1440x900, 393x852, 320x852), plus
a `forced-colors: active` variant at 393x852 and a print-emulation variant at
1440x900 for each state, plus two focused-region provenance captures, plus six
`before--` images for the two states whose copy changed.

`VISUAL-STATE-INDEX.md` names, for every image: the exact head, the route/state,
the viewport, the browser mode, and the requirement it demonstrates.

## Honest limits of this evidence

- **Print** is CSS print-media emulation, captured deterministically. It is not
  a PDF export. The repository has no deterministic print-to-PDF harness and
  this lane did not invent one.
- **Forced colors** is `Emulation.setEmulatedMedia` with `forced-colors: active`.
  It is the browser's forced-colors mode, not a Windows High Contrast system
  theme on real hardware.
- **These are screenshots, not assistive-technology validation.** V4's
  `AT-LIMITATION.md` remains accurate and is not superseded: no screen reader,
  AT bus, or real assistive-technology run happened here. A picture proves
  rendering, not announcement.
- Text scaling at 200% and page zoom at 400%, which the shared gate exercises as
  assertions, were **not** captured as images; the gate covers them structurally
  across all 19 routes and this lane did not duplicate that.
