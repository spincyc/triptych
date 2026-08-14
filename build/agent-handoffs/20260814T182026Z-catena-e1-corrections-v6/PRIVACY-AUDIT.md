# Privacy and sanitization audit

## The instrument

`logs/sanitize-and-seal.py` is the reusable sealer, carried forward and
corrected for V6. It runs in one fixed order — self-check, normalize, scan,
index-check, screenshot-pair audit, hard gate, manifest — so that a package
cannot be sealed while any check is unsatisfied.

- **Self-check first.** Before any file is written, the tool greps its own
  source for the operator's account name, host name and uid, and for the home
  path as a substring. A hit means the tool cannot see its own leak, and it
  refuses rather than sealing.
- **Normalize.** Every text member is rewritten through one ordered
  substitution table: repository root, home path, scratch directory, account
  name on word boundaries, host name, uid in each of its shapes, pid, D-Bus
  session name, uuid, loopback and private addresses, email, timezone.
- **Scan.** An INDEPENDENT verification pass over the file names and every line
  of every text member, using checks derived from the SAME shared pattern
  constants as the rules — so a rule and its check cannot drift apart.
- **Index-check.** Every backticked reference in every Markdown member is
  resolved against the package root, and every member no document references is
  reported.
- **Screenshot-pair audit.** Every `before--`/`after--` pair is hashed and
  classified, and sealing FAILS if a byte-identical pair is described anywhere
  in the package as showing a difference.
- **Hard gate.** Any scan hit, any missing reference, or any false visual claim
  refuses the seal and no manifest is written.

## What V6 corrected in the sealer, and the test that pins each

The V5 review found five defects. Each is fixed and regressed;
`logs/test-sanitize-and-seal.py` is 45 focused tests and
`logs/sealer-tests.log` is its run.

| Defect the review found | Correction | Pinning test |
| --- | --- | --- |
| Timezone matching incomplete: whole IANA areas absent, `posix/` and `right/` prefixes unmatched, the signed-offset zone under Etc normalized to `<tz>5`, leaving the offset behind, and bare zone names gated behind only three contexts | The area, prefix and city patterns are completed and the context list widened; rule and check are both derived from the shared constants | `TimezoneAreas`, `TimezoneBareNames` |
| The utc-offset RULE was broader than its CHECK, the exact drift the tool's own header claims is unrepresentable | Both are generated from one shared pattern | `UtcOffsetSymmetry` |
| A failing run left the PREVIOUS run's manifest on disk, describing pre-normalization digests | Any existing manifest is removed before any member is rewritten; a failing `--check-only` clears it too | `StaleManifest` (3 tests) |
| Ordinary screenshot coordinates, version triples, timestamps and MD5 digests were HARD-BLOCKING the seal as D-Bus names, private IPs, timezone offsets and uuids | The D-Bus pattern requires a real left boundary, the private-IP pattern range-checks all four octets, the offset pattern requires a timestamp, and 32-hex requires an id label | `FalsePositives` (3), with `PreservedDetections` (22 cases) proving nothing real was lost |
| Missing referenced artifacts undetectable: only `*.md` inspected, only names containing a slash checked — so every top-level member was exempt — and a reference accepted if it resolved under either of two roots | Bare names are checked against the package root; one root only; unreferenced members reported as data | `IndexCheck` (4 tests) |

Added beyond the review's list, because the brief required them:

| Addition | Why | Pinning test |
| --- | --- | --- |
| `--verify` mode | The brief requires the sealer to verify the exact package hash. It recomputes every manifest member and, where a sibling ZIP and its digest sidecar exist, the archive digest; it writes nothing and exits non-zero on any mismatch | `VerifyMode` (7 tests) |
| Screenshot-pair audit and its hard gate | This is the instrument that would have caught the V5 package's five byte-identical pairs described as visibly different | `ScreenshotPairs` (5 tests) |
| Decode robustness and honest truncation | A member clean in its first 8 KiB and binary later raised mid-run, after some members had been rewritten; and hit lists were silently truncated to 50 under a full count | `Robustness` (4 tests) |

**Nothing was weakened.** No detection was removed, no whitelist added, no
filename special-cased. `PreservedDetections` re-asserts the account name, host
name, home path, uid in each shape, pid, D-Bus name, email and both uuid
spellings, and `SelfBlindness.test_a_private_value_written_as_a_literal_is_refused`
proves the tool still refuses a package that leaks.

## The test module is itself a sealable package member

V5's equivalent could not have shipped: a test module for a privacy scanner
naturally contains private-token-shaped literals, and the scanner would
correctly refuse it. `logs/test-sanitize-and-seal.py` composes every
adversarial fixture at runtime from fragments, so no literal line of its source
matches a forbidden pattern while every value fed to the scanner is unchanged.
`SelfBlindness.test_the_test_module_is_itself_sealable` and
`SelfBlindness.test_the_shipped_pair_seals_together` pin that permanently, so a
future edit that reintroduces a raw literal fails in the suite rather than at
seal time.

Fixtures that must NOT match — benign coordinates, exempt no-reply addresses,
time ranges — are deliberately left as raw literals, so the shipped file is a
second, independent demonstration that they do not.

## What the seal reported for this package

The sealer was run over the assembled package. The first pass normalizes; the
second is the check that nothing was still being rewritten when the digests
were taken, and it is the pass whose manifest ships.

**First pass**, over the package as assembled:

    normalized 14 file(s), 378 substitution(s)
    sanitization scan: 0 private-token hit(s)
    evidence-index check: 0 missing reference(s), 0 unreferenced member(s)
    screenshot pair audit: 16 before/after pair(s), 0 byte-identical, 16 differing
    MANIFEST.sha256 written: 85 file(s) covered

The 378 substitutions are the repository root, the home path and the scratch
directory in the raw run logs, rewritten to `$REPO`, `$HOME` and `$SCRATCH`.
They are why the logs ship readable rather than redacted.

**Second pass**, over the result, is quoted in `checks.txt` with its exit. It
makes **zero** substitutions — nothing was still being rewritten — and the scan,
index check and pair audit all report the same figures as above. Every one of
the 16 before/after pairs is genuinely different; none is byte-identical, so
no claim of a visible change in this package is unsupported by its own files.

The evidence index resolves completely in both directions: no document names an
artifact the package does not contain, and no member goes unmentioned by any
document.

## What the tool still cannot do

An absolute path outside the home directory, the repository root and the
scratch directory is not recognisable as private by any pattern. It is handled
by policy — this package contains no such path — and not by the tool.

The account-name and host-name checks match the operator's runtime identity on
word boundaries. A reviewer whose account name is an ordinary English word may
see a false hit on ordinary prose; the documented answer is to set
`SANITIZE_USER` and `SANITIZE_HOST`, which is the reproduction path the tool
already advertises.

## How a reviewer re-checks this package

    cd <package> && sha256sum -c MANIFEST.sha256
    python3 logs/sanitize-and-seal.py <package> --verify
    python3 logs/sanitize-and-seal.py <package> --check-only
    python3 logs/test-sanitize-and-seal.py

The first two are content proofs, the third re-runs the privacy scan and the
pair audit without writing, and the fourth re-runs the sealer's own tests.
