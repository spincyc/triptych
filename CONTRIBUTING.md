# How to Contribute

You do not need to know Git, edit source files, or rewrite a paragraph. A useful contribution can be one sentence.

Feedback starts an investigation; every proposed change is still checked against the governing sources and editorial rules.

## Easiest: Send a Short Note

Ask the person who shared the PDF to pass your note to the project team, or open an issue on the project’s hosting page. The team can turn ordinary feedback into a prompt—a plain-language request—for an AI agent.

Useful notes can be short:

- “The treatment of this doctrine feels ambiguous. Check it against the cited magisterial sources.”
- “This section seems to confuse doctrine, discipline, and theological opinion. Revise it.”
- “A priest should be able to find the pastoral answer more quickly. Keep the sources, but make the structure clearer.”
- “The document is missing an important objection or authority. Investigate it throughout, not only here.”

Name the document and page or section if you can, but a high-level concern is enough. Review the proposed revision and send another note; several short rounds can substantially improve a document.

## More Advanced: Run an Agent Yourself

Git keeps the project’s files and history. An AI coding agent can edit, check, and rebuild them.

1. Clone the repository using the address shown by its hosting site. If you already have a copy, run `git pull` to update it.
2. From the repository’s top-level folder, start Codex with `make codex` (or use `scripts/triptych-codex` when passing supported agent options). You may start several sessions; each receives an isolated task checkout automatically. Do not create, move, delete, or reuse those task directories yourself.
3. Give the agent an ordinary request, including any sources, concerns, emphases, or limits that matter.
4. Ask it to show the changes and verification results before authorizing a commit or integration. A local commit or merge does not authorize a push.
5. Read the revised PDF as well as the line-by-line view of what changed.
6. After reviewing the committed result, expressly authorize its integration and any resulting update to its recorded local target, including local `main` when `main` was the dispatch branch. Return to that target’s clean primary checkout and run `make integrate <run-id>` (or `scripts/triptych-codex --triptych-integrate <run-id>` directly). A result already contained by the target is confirmed and cleaned; one already based on the current target is landed without rewriting its commits. If target and worker both advanced, the launcher rebases the audited linear worker commits onto the captured target. A conflict-free rebase remains a one-step integration. Landing uses an exact expected-old ref transaction rather than a merge commit, never rewrites existing target history, and leaves a raced unrelated checked-out ref unchanged.

   If that launcher-owned rebase reaches a genuine conflict, it remains active as a managed conflict instead of being aborted. Open the fixed staging-only resolver with `make resolve <run-id>`, reconcile and stage the source-aware result, and then run `make continue <run-id>`; repeat if a later commit conflicts. The resolver never administers the rebase. Successful continuation stops at a clean review-pending candidate without updating the target. Review its complete object-to-object patch with `make final-diff <run-id>`, then give fresh integration authorization and run `make integrate <run-id>` again. That later landing accepts only the exact candidate while its captured target is unchanged; target movement retains the candidate for review without reset, silent rebase, merge, or cleanup. To abandon a provable managed conflict, a clean review-pending candidate, or a clean manually resolved candidate retained after a pre-landing verification failure with no recorded landing result or checkpoint, explicitly run `make abort <run-id>`; the launcher proves the retained rebase or candidate and the private source anchor, restores the exact audited source, and leaves the live target unchanged.

   These Make targets are convenience wrappers for an exact run ID emitted by the launcher. GNU Make interprets options and command-line variable assignments before the project Makefile can validate goals, so automation must not forward arbitrary or external input to them; use the corresponding direct launcher form, such as `scripts/triptych-codex --triptych-resolve <run-id>`, whose lifecycle parser requires one syntactically valid run ID without GNU Make's option or assignment reinterpretation. The launcher refuses uncommitted or unaudited worker state and a fresh integration from a dirty or wrong primary checkout. Durable landing and cleanup checkpoints remain safely retryable. All launcher-owned Git operations disable hooks, signing, and editors as applicable; no target-side merge hook runs because landing does not invoke a merge. After exact landing verification, the launcher attempts to remove the retained task checkout, worker branch, and private source anchor. It never invokes `git push`.
7. Submit the change for review through the hosting site when ready.

Agent results remain local until deliberately integrated and pushed. Pushing any branch to the public repository exposes its tracked files and reachable history. Pushing `main` also starts the reader-site publication workflow. Do not ask an agent to push unless the remote and ref, public-exposure review, and publication consequences have been expressly approved.

### Exceptional rewritten-quarantine retirement

Retiring an explicitly superseded quarantine after its worker history was rewritten is a destructive maintenance operation, not an ordinary cleanup or integration step. It requires separate, explicit authorization to discard the exact worker head and must be run from the primary checkout with the direct launcher command:

```sh
scripts/triptych-codex --triptych-retire RUN_ID --discard-head FULL_OID --target-contains FULL_OID
```

There is deliberately no Make wrapper. `--discard-head` is the full commit ID of the exact clean worker head authorized for destruction. `--target-contains` is a full commit ID chosen by the operator as a reachability checkpoint that the recorded target must contain; it does not prove that the target semantically incorporates, supersedes, or is equivalent to the discarded work. The launcher verifies but never moves the target, durably records the initial eligibility proof once, and anchors the discarded head. Before worktree removal and again before the atomic ref transaction, it freshly requires the current target to contain the selected checkpoint and records that exact target for a compare-and-swap verification. The transaction creates a per-run receipt at the discarded head and exact-deletes the worker branch and anchor. If the target races, those refs remain and an exact retry may use a newer containing descendant; if containment is lost, deletion is refused until it is restored. Only after recording the observed transaction does the launcher exact-delete the receipt and record its absence. Post-transaction recovery uses the durable record and strict phase refs, so it remains retryable after completed objects are pruned. Active, dirty, changed, conflicting, partial, or tampered state is refused. Changing either object argument is rejected. `make clean-run <run-id>` still refuses an untouched quarantine and may only resume retirement after the direct command has established its durable checkpoint.

A useful starting prompt is:

```text
Read AGENTS.md and the applicable guidance completely. Revise [document] to [describe the concern or desired result]. Check the governing sources, preserve material uncertainty, update the research records, and rebuild and inspect every affected PDF. Do not commit, integrate, or push until I have reviewed the result and expressly authorized that separate action.
```

The agent should do the technical work. The contributor remains responsible for judging whether the result is faithful, clear, and worth proposing.

## Most Sophisticated: Test Different Base Objectives

A Git branch is a separate line of work. It lets you change the project’s underlying editorial objectives without disturbing the main library.

Create an experimental branch, for example:

```sh
git switch -c experiment/my-objectives
```

Then revise the relevant files under `guidance/`: perhaps the universal evidence standard, a genre profile, the audience, the source hierarchy, or the boundary between source-grounded synthesis and editorial exploration. State the alternative objectives clearly, give the same task to an agent, and compare the results.

This tests the editorial method, not the truth or authority of Catholic teaching. Keep the experiment separate until its sources, methods, and consequences have been reviewed; persuasive prose does not make an alternative branch the current library.

## Licensing Contributions

By intentionally submitting text, code, or other material for inclusion, you agree to license it under the terms applicable to that part of the repository: CC BY 4.0 for project-created content and MIT for software and the listed reusable typesetting tools. You retain any copyright or similar rights you hold; no ownership is transferred.

Submit only material you created or have authority to provide. Identify quotations, translations, images, and other third-party material together with their source and rights status. Ordinary feedback is not licensed merely because it prompts a revision. See [Licensing](LICENSE) and [Third-Party Material](THIRD_PARTY.md).

## Technical Starting Points

- [Repository instructions](AGENTS.md)
- [Editorial and evidence standard](guidance/editorial.md)
- [Repository and publication contract](guidance/repository.md)
- [Library index](LIBRARY.md)

`AGENTS.md` routes each kind of document to its detailed profile.
