# Native reader browser zoom regression

`tools/tests/test_reader_native_zoom.py` registers an opt-in built-artifact
check. Its default run checks fixture syntax and artifact identity binding, and
skips Chromium. The browser run requires a released artifact and quiet timing
work to have finished. It uses Python's standard library, Node for syntax checks,
Git, a matching Chrome/Chromium and ChromeDriver, and POSIX process groups.
It installs no packages. Set `TRIPTYCH_CHROME` and `TRIPTYCH_CHROMEDRIVER` when
the executables cannot be found on `PATH`.
After a `PATH` miss, bare command names also check `$HOME/.local/bin` and are
invoked by validated absolute path. This includes configured browser/driver
names; an explicit configured path must itself be executable.

## Release and run

Create a fresh JSON record under repository `.scratch`, naming the exact artifact
reviewed for this run. Use a repository-relative `artifact_root`, the SHA-256 of
its `SHA256SUMS` file, and the SHA-256 of its `PUBLICATION-MANIFEST.json` file.
Both commits must be complete 40-character commit IDs. `source_commit` is the
actual reviewed checkout HEAD. `runtime_source_commit` identifies the source
that produced the artifact. `source_qualification` must describe any difference,
including a reviewed assertion of byte equality when later commits only change
documentation or test apparatus. The runner records this qualification; the
statement's review remains the release owner's responsibility.

Required fields:

```json
{
  "released_by_coordinator": false,
  "artifact_root": "build/public-alpha/preview",
  "sha256sums_sha256": "<64 lowercase hexadecimal characters>",
  "publication_manifest_sha256": "<64 lowercase hexadecimal characters>",
  "source_commit": "<40 lowercase hexadecimal characters>",
  "runtime_source_commit": "<40 lowercase hexadecimal characters>",
  "source_qualification": "Describe the reviewed artifact and source relationship."
}
```

Set `released_by_coordinator` to `true` only for the specifically authorized
eight-case run. A prior capability smoke release is insufficient. There is no
smoke option, retry loop, source-server fallback, or build operation in this test.
After release, run from the repository root:

```sh
TRIPTYCH_NATIVE_ZOOM_CHROMIUM=1 \
TRIPTYCH_NATIVE_ZOOM_CONFIG=.scratch/reader-native-zoom-release.json \
python3 -m unittest discover -s tools/tests -p test_reader_native_zoom.py -v
```

All profiles, screenshots, logs and receipts stay beneath repository `.scratch`.
`TRIPTYCH_BROWSER_SCRATCH` may select a child of that directory. The runner prints
the receipt path and helper PID when it starts. It binds the artifact by checking
every manifest-listed file before and after the run. It records actual HEAD,
worktree status, browser capabilities, browser arguments, native API values,
window/viewport geometry, request diagnostics and owned process handles. Its
780-second run deadline, interrupt handling, and wrapper timeout allow browser,
profile and local-server cleanup; a remaining process or profile fails the run.

## What the check establishes

Eight cases cover Day and Propers entrances in Read, Missal, Study and Compare.
Day uses 2026-11-22 and its canonical resolved formulary. Propers uses Roman 1962
Pentecost 10. Day Compare uses the postconciliar recension peer; Propers Compare
uses English/Latin oration language pairing. All start in fresh reader tabs.

The small MV3 extension controls the browser's native tab zoom through
`chrome.tabs.setZoom`, with `automatic`/`per-tab` zoom settings. It first requests
1.0, then exactly 4.0. Raw API and event values are retained. Only native API/event
round trips permit absolute error of `1e-9`, accounting for factor/level numeric
conversion. No values are rounded to create a pass.

Each case keeps the 1280×1000 browser window and screenshot pixel dimensions
unchanged, checks the fourfold DPR change and quarter CSS width, and checks
`visualViewport.scale === 1`, unchanged CSS zoom and root font size, no horizontal
overflow, and stacked Compare pairs. No Emulation command is issued; the saved
command trace is also checked. CSS zoom, pinch scaling, device scale overrides
and narrow-window emulation do not satisfy this check.

Native WebDriver clicks open Contents, choose a semantic destination and wait
for observed scroll stability: at least 150 ms and six consecutive animation
frames within 0.1 CSS pixel, bounded at three seconds. The test checks semantic
focus, positive scroll, no horizontal overflow, and at least 12 CSS pixels of the
target heading exposed between fixed masthead and action dock. Opening Mode and
pressing Escape must restore the same semantic place and scroll, and return
visible focus to the Mode action. API, geometry and partial case receipts are
saved before assertions so a failure retains its observations.

Six screenshots per successful case capture 100%, 400%, Contents, the landed
destination, Mode, and restored focus. A machine pass still requires a human to
inspect every screenshot against the named artifact. This check does not replace
actual assistive-technology use, manual touch checks, an independent review, or
a WCAG conformance evaluation.

## Primary API references

- [Chrome tabs zoom API](https://developer.chrome.com/docs/extensions/reference/api/tabs?hl=en)
- [ChromeDriver extensions](https://developer.chrome.com/docs/chromedriver/extensions)
- [ChromeDriver capabilities](https://developer.chrome.com/docs/chromedriver/capabilities)
- [Unified headless Chrome](https://developer.chrome.com/docs/automation-and-testing/headless)
- [Chromium zoom-factor conversion guidance](https://chromium.googlesource.com/chromium/src/+/HEAD/third_party/blink/public/common/page/page_zoom.h)
