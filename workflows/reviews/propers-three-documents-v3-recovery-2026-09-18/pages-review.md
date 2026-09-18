# Independent Pages recovery-selection review — 2026-09-18

**Disposition: accept the scoped deployment-selection fix; no blocking or
actionable findings.** Both blockers in `REVIEW_REQUEST.md` are answered below.
This is not approval of quota-blocked v3 document production, its pagination,
or any other uncommitted work.

## Identity and integrity

Reviewed `build/agent-handoffs/20260918T123800Z-sunday-recovery-pages/` and its
sibling ZIP against base `6f552cc63729bfa2a6970c13bdf92bf1257651db`, on
`feature/codex/propers/homily`. Scope: `.github/workflows/pages.yml`,
`tools/tests/test_pages_publication_selection.py`, and only the deployment
paragraph in `guidance/repository.md`.

Before review, `sha256sum -c SHA256SUMS` inside the handoff returned **0:
8/8 OK**. `python3 -m zipfile -t
build/agent-handoffs/20260918T123800Z-sunday-recovery-pages.zip` returned **0**;
an independent byte comparison confirmed **9/9 archive files** exactly match
the directory, with no missing/extra files, and **3/3 subjects** exactly match
the working files. Initial `unzip -t` was unavailable (exit 127); Python's
successful verification replaced it. Final manifest verification again passed
8/8. Existing handoff/archive were verified, not created or modified.

## Blocking questions

1. **Renderer ownership and fail-closed inventory: pass.** The workflow calls
   the renderer's provider discovery, normalized publication map (including
   local overrides), source discovery and non-preview inclusion function.
   Unknown/missing statuses and source/manifest/Make mismatches stop planning;
   only explicit `hold` records may be excluded. Actual inventory is **218:
   216 included, 2 held**. The selected set is **58 Claude + 158 GPT**, including
   **7 Claude + 16 GPT synthesis/homily companions**. The only excluded outputs
   are Claude's
   `liturgy/roman-rite/1962/propers/temporal/54-fourteenth-after-pentecost`
   and its `-synthesis`. Actual Make install edges match all 216 selected PDFs
   exactly; neither held output is an install edge.
2. **Same cold/full-hit set without bypassing validation: pass.** Cache keys,
   restoration, cold installation and cache-only installation use the same
   planned per-provider identities. Both install loops pass the complete
   quoted `DOCUMENTS` value to ordinary `make install`; the container receives
   the same plan read-only. Make's source metadata gate, per-PDF validation
   chain, validation-stamp checks and hash-checked install remain intact.
   Missing selected cached output invokes the refusal guard, not a silent skip.
   The unchanged downstream deployment-source, public-site and Pages
   verification gates still run before upload. Renderer build/verification
   independently enforce the same included set and the separately bound six
   reading-plan PDFs. Guidance accurately describes this boundary; ordinary
   local Make defaults are unchanged.

## Independently executed checks

Commands below ran from the repository root with `PYTHONDONTWRITEBYTECODE=1`
for Python. Logs and review-only scripts are under
`.scratch/recovery-pages-review/`.

| Command | Exit | Result |
| --- | ---: | --- |
| `python3 -m unittest tools.tests.test_pages_publication_selection -v` | 0 | 17 tests passed; `focused-tests.log` |
| `python3 -m unittest tools.tests.test_pages_publication_selection tools.tests.test_public_alpha tools.tests.test_makefile -q` | 0 | 154 tests passed, including the same 17; `core-regressions.log` |
| `python3 .scratch/recovery-pages-review/adversarial.py` | 0 | 10 independent tests / 22 fixture cases passed; `adversarial.log` |
| `python3 .scratch/recovery-pages-review/real_selection.py` | 0 | Exact workflow inventory prefix against real sources; both real `make -p -n install PROVIDER=… DOCUMENTS=…` graphs matched; 13 workflow shell blocks plus inner container script passed `bash -n`; `real-selection.log` |
| `python3 tools/public-alpha check` | 0 | 218 publications: 216 alpha, 2 hold; `public-alpha-check.log` |
| `git diff --check -- .github/workflows/pages.yml guidance/repository.md tools/tests/test_pages_publication_selection.py` | 0 | No scoped tracked whitespace errors |
| `tmt check` | 0 | `ok` |

Independent adverse cases: previously published cache entries becoming held
are neither restored nor retained; canonical and companion statuses remain
independent on both install paths; missing canonical/companion TeX stops
planning; malformed legacy states (`null`, boolean, number, list, object,
`alpha`, `HOLD`) fail closed; duplicate/extra Make identities fail;
component-only undeclared providers fail; all-held providers install nothing
and clear obsolete cache entries; a corrupt restored PDF still fails on the
cold/mixed-hit path; duplicate providers or an omitted primary provider fail.
Fixtures use actual workflow scripts and the renderer, real GNU Make, and fake
PDF/typesetter bytes—not a real container deployment.

### Expanded-suite qualification

Also ran
`python3 -m unittest tools.tests.test_pages_publication_selection tools.tests.test_public_alpha tools.tests.test_makefile tools.tests.test_generation_metadata -q`:
**exit 1, 195 tests**, with **187 assertion failures confined to one test**,
`InstallCommitDerivationTests.test_every_recorded_install_commit_is_that_pdf_s_latest_install`
(`combined-tests.log`). It reports 186 absent historical PDF installs and
`186 != 187`. That test and `scripts/_corpus.py` are byte-identical to the
handoff base; that base has no provider-PDF/old-doc install history. This is
not a selection regression or permission to call the expanded suite green.
The handoff's separate “29 untouched smoke/help failures” claim was not
baseline-compared here and is not relied upon for acceptance.

## Final SHA-256

```text
6ac0f5383e03e3003da0d93f1f59a27d8725bb5cc312b199c71c331e9bda8150  .github/workflows/pages.yml
08ba8bc4934bfe681b5a42bbe5de0c1bb0b293076e62e32dda4d34a5b83f4990  tools/tests/test_pages_publication_selection.py
d916ecbcf81c44a3a4167b113b57968ca756d21d10e15bf353fb216c9082970e  guidance/repository.md
7ae0ec190dbde28aa61731fb508c0afd84a0ee3ff01dd311653d80bc30763401  build/agent-handoffs/20260918T123800Z-sunday-recovery-pages.zip
ac4d7145e7b9886042db03c1a4a38923386bf002956602f06186f0674d860251  tools/public-alpha
d463dccba07d9d57a757cf2ca510eb1a02bd54a01c6c3527d991f1bec6ee21ba  Makefile
9e7d61df749af69aee2d37b7aacfbc2e8269e48d05a2a87d753446cf53666098  .scratch/recovery-pages-review/adversarial.py
cfc9c62f29f4289e7b14bb8cff9c9274de1b1cb09e52d6947ae5b773aa1fed51  .scratch/recovery-pages-review/real_selection.py
```

No author/source edits, staging, commits, pushes or deployment were performed.
The parent's completed 210-PDF rebuild and source checks were not repeated;
this review does not claim independent content/pagination approval. Actual
GitHub/container execution remains unattempted. Follow-up: parent coordinates
integration and a real deployment attempt, then verifies its result.
