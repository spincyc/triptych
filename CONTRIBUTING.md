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
2. Open the repository’s top-level folder in your AI agent.
3. Give the agent an ordinary request, including any sources, concerns, emphases, or limits that matter.
4. Ask it to show the changes and verification results before committing them.
5. Read the revised PDF as well as the line-by-line view of what changed. Submit the change for review through the hosting site when ready.

A useful starting prompt is:

```text
Read AGENTS.md and the applicable guidance completely. Revise [document] to [describe the concern or desired result]. Check the governing sources, preserve material uncertainty, update the research records, and rebuild and inspect every affected PDF. Do not commit until I have reviewed the result.
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
- [Current library and supporting records](LIBRARY.md)

`AGENTS.md` routes each kind of document to its detailed profile.
