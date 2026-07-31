# How to Contribute

You do not need to know Git, edit source files, or rewrite a paragraph. A useful contribution can be one sentence.

Feedback starts an investigation; every proposed change is still checked against the governing sources and editorial rules.

## Easiest: Send a Short Note

Open an issue at [github.com/spincyc/triptych/issues](https://github.com/spincyc/triptych/issues), or write to <71109625+spincyc@users.noreply.github.com>. If you were given a PDF by someone else, passing your note back to them works just as well. The team can turn ordinary feedback into a prompt—a plain-language request—for an AI agent.

Useful notes can be short:

- “The treatment of this doctrine feels ambiguous. Check it against the cited magisterial sources.”
- “This section seems to confuse doctrine, discipline, and theological opinion. Revise it.”
- “A priest should be able to find the pastoral answer more quickly. Keep the sources, but make the structure clearer.”
- “The document is missing an important objection or authority. Investigate it throughout, not only here.”

Name the document and page or section if you can, but a high-level concern is enough. Review the proposed revision and send another note; several short rounds can substantially improve a document.

## More Advanced: Run an Agent Yourself

Git keeps the project’s files and history. An AI coding agent can edit, check, and rebuild them.

1. Clone the repository using the address shown by its hosting site. If you already have a copy, update it and begin from a clean `main`.
2. From the repository’s top-level folder, start Codex directly. The current checkout is the ordinary workspace; do not create, move, delete, or administer worktrees yourself.
3. Give the agent an ordinary request, including any sources, concerns, emphases, or limits that matter.
   The agent must first read `PROJECT-WORK.md` and
   `promised-deliverables.toml`, record any new promised outcome there, and
   reconcile both records before reporting completion.
4. Review the changes and verification results. Direct Codex sessions have
   standing authority to make coherent ordinary commits and regularly push
   validated checkpoints to `origin/main`.
5. Read the revised PDF as well as the line-by-line view of what changed.
6. Before each push, the agent must inspect the exact outgoing range, confirm
   that every newly reachable object is intended for public disclosure, and
   run the checks required by the affected guidance. Pushing `origin/main`
   starts the GitHub Pages workflow and authorizes that automatic deployment
   attempt; it does not authorize force-pushing, rewriting history, changing
   remotes, or deploying elsewhere.
7. Continue with another coherent work unit rather than accumulating a large,
   unpushed session branch.

A useful starting prompt is:

```text
Read AGENTS.md and the applicable guidance completely. Revise [document] to [describe the concern or desired result]. Check the governing sources, preserve material uncertainty, update the research records, and rebuild and inspect every affected PDF. Commit coherent validated checkpoints and push them regularly to origin/main under the standing authority.
```

The agent should do the technical work. The contributor remains responsible for judging whether the result is faithful, clear, and worth proposing.

### Contributing reusable research

When several publications use the same external work, identify the work,
edition, exact artifact, and checked locus once under `src/sources/` and give
each publication its own `research/source-bindings.toml`. When the relevant
work is a bounded constituent of an anthology or other separately owned
container, register a segment under the constituent's edition and point it to
the one exact container artifact; do not duplicate or falsely reassign the
container bytes. Reuse the canonical identity and evidence; do not copy a
consumer's interpretation or sufficiency judgment into the other
publications. Record the retrieval route, artifact hash when bytes were
acquired, and the rights basis for anything proposed for tracking. A whole
searchable source or bounded searchable segment may be retained when it is
lawful and reasonably sized, but possessing or searching it does not mean
every passage was inspected or verified.

After changing a publication or source record, refresh the structural source
inventory, review any new classification or source-family presence, refresh
the family ledger, and run `make check-sources`. The detailed order and the
separate family-screening completion audit are in
[`guidance/sources.md`](guidance/sources.md).

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
- [Durable project work register](PROJECT-WORK.md)
- [Promised-deliverable contract](guidance/promised-deliverables.md)
- [Editorial and evidence standard](guidance/editorial.md)
- [Repository and publication contract](guidance/repository.md)
- [Reusable source library contract](guidance/sources.md)
- [Reusable source library](src/sources/README.md)
- [Library index](LIBRARY.md)

`AGENTS.md` routes each kind of document to its detailed profile.
