Verdict: **PASS** for the final five-file metadata-scope repair. No unresolved actionable finding remains in this bounded review. This verdict permits resuming the requested single-document build; it does not approve the liturgical content, rendered pages, publication, or deployment.

Reviewed against base `53fbb228615420f45446f6c8a6eb457da2ce115d`. HEAD at the final capture was `c98e396a1bd2b1a21a2686fb2af216fbc78765c5`; that intervening commit did not change these review subjects. Exact final SHA-256 values are in `final-hashes.json`. The reviewer made no subject edits or live TLM/NO builds.

One P2 finding was reproduced and repaired during review. In the first submitted Makefile, source-only validation ran inside the canonical PDF recipe. After a successful build, deleting that document's `generation-metadata.tex` removed the file from the dynamically discovered dependency list. Both cached `make doc DOC=demo-a` and direct `make build/gpt/demo-a.pdf` then exited 0 without any metadata checker or TeX invocation. The same isolated reproduction against the stated base exited 2, so this was a concrete regression. The final Makefile's phony per-document source audit, registered at `Makefile:115` and implemented at `Makefile:1420`, is an order-only prerequisite of all three PDF recipes, the verification target, and the individual installation target (`Makefile:1424`, `Makefile:1439`, `Makefile:1454`, `Makefile:1524`, `Makefile:1646`). The final replay rejects the deletion with exit 2 and no TeX execution for both build entry points. Initial Makefile bytes, hashes, and paired baseline/initial/final probe results remain in the review scratch directory.

The final behavior satisfies the reviewed scope:

- `tools/check-generation-metadata:580` makes `--document` and `--pdf` mutually exclusive. The selected source uses the same provenance audit as the global and rendered paths. Resolution validates provider-relative IDs, preserves canonical and declared companion ownership plus legacy synthesis fallback, and rejects source/metadata symlink escapes from the provider or owner (`tools/check-generation-metadata:458`, `tools/check-generation-metadata:534`).
- `make doc` targets the existing `.metadata/DOC.verify` graph (`Makefile:770`). Cached builds audit source provenance and retain current PDF/checker hash verification without unnecessary TeX. Synthesis and homily use the same source audit on fresh and cached invocations.
- `install-doc` and a direct individual installed-PDF target use the selected source audit and existing exact PDF verification. A deficient unrelated draft does not block them. Own missing or invalid provenance, or altered cached build PDF bytes, prevent installation; the fixture's previously installed bytes remain unchanged after rejection. The separate altar-server series routing remains intact and its existing test passes.
- Bulk `pdf`, `install`, `check`, and `check-metadata` retain the global metadata audit. Scoped CLI selection changes neither source provenance requirements nor release authorization.
- The entire Makefile delta was reviewed. The parent's Week 25 verified-propers dependency remains attached to the canonical, synthesis, and homily PDFs at `Makefile:1620`–`Makefile:1623`. `tmt.json` accurately advertises the mutually exclusive selection modes.

Independent verification, with all fixtures and raw review logs confined to `.scratch/implementation-cold-review/scoped-metadata/`:

| Check | Result |
| --- | --- |
| Focused parser/provenance/source-selection and complete Makefile fixture suite | **55 tests passed; 0 failures, 0 errors, 0 skipped** |
| Published-source identity compatibility, using the current checker's own `audit_document(..., pdf=None)` over tracked `main.tex` identities | **192 passed: 140 GPT, 52 Claude; 0 failures** |
| Original cached metadata-deletion regression | Base rejected both targets; first submission accepted both; final submission rejects both, with no TeX |
| Independent individual-install matrix | **6 scenarios passed**: both entry points × unrelated-draft success, own metadata deletion, preserved-mtime build-PDF tampering; exact installed bytes checked |
| Independent bulk-gate matrix | **4 targets passed**: `pdf`, `install`, `check`, `check-metadata` reject the failing global audit before TeX in the serial fixture |
| Focused `git diff --check` | Passed |
| Workflow compatibility | No diff against the base in `workflows/pipelines`, `workflows/fragments`, `workflows/schema`, or `scripts/_workflow.py` |

The final test suite also checks changed-validator revalidation, old-mtime invalid source metadata, legacy stamp migration, cached PDF tampering, bounded parallel build behavior, and the existing seven-document altar-server install route. The 192-document compatibility audit explicitly excludes the two untracked, actively authored liturgical drafts; their incomplete state is not evidence about legacy compatibility. The metadata checker hash was unchanged between that compatibility audit and final capture.

Limits: build-graph and installation probes use isolated renderer/checker doubles to test command selection, dependency ordering, hashes, and copied bytes. Real source validation is separately exercised by the CLI fixtures and the 192-source audit. No live PDFs were built, installed, rendered, or reviewed, and no whole-corpus deployment claim is made. The previously reported whole-corpus test affected by an actively authored NO web-edition declaration was deliberately not counted as a repair pass. No workflow, fragment, schema, or engine change is part of this repair; existing workflow digest compatibility is retained.

Archive scope: this public-safe review, `final-hashes.json`, and `command-outcomes.json` are the durable review records. Raw fixture logs, scripts, initial/final patches, and reproduction output remain disposable scratch evidence; this report does not imply that those raw files are included in a later archive.
