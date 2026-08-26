# Generate the Web Edition

## Your task

Generate the reader-facing web edition of the canonical leaf into the build
tree, so the next stage can judge whether the conversion is faithful before
anything is installed. Generation is tier one and installs nothing: the
tracked artifact under `web/{provider}/` is written later, by
`install-publication`, and only from an edition that passed evaluation.

The web edition is generated from the **canonical** leaf. The synthesis is a
derived companion of that leaf and has no web edition of its own; do not
create a `-synthesis` web leaf, a `-synthesis` declaration, or a second
prose authority of any kind.

## Steps

1. Read `src/{provider}/{proper}/web-edition.toml`. It declares the leaf's
   eligibility and any blocking constructs. Nothing defaults to eligible: a
   leaf with no declaration cannot be generated, and a leaf declared
   eligible while using a blocking construct is an error, not a warning.
2. Validate the declaration:
   ```
   tools/tpt check-web-edition --provider {provider} --document {proper}
   ```
3. Confirm the leaf is listed as eligible:
   ```
   tools/tpt check-web-edition --provider {provider} --list-eligible
   ```
4. Generate the edition into the build tree:
   ```
   tools/tpt web-edition --provider {provider} {proper}
   ```
   The output is `build/web/{provider}/{proper}.md`.
5. Read the converter's own output and record every warning it emitted,
   verbatim, in your summary. A warning the converter printed and a loss it
   printed nothing about are two different problems, and the evaluator that
   follows needs to know which it is looking at.
6. Confirm the generated file exists and is non-empty, and that no
   `build/web/{provider}/{proper}-synthesis.md` was produced.

## Note

The web-edition evaluator that follows reads this generated edition against
the canonical leaf and the accepted PDFs. Your job here is to generate,
report the converter's own output, and change nothing about the accepted
material. If the generation fails, report the failure in your summary rather
than editing the leaf to make the converter happy — that is the reviser's
work, and only against a finding that names it.

## Result

Return a worker result with `disposition: "PASS"`, `artifact_path` set to
`build/web/{provider}/{proper}.md`, and a summary naming the generated path
and every converter warning.

Return `disposition: "BLOCKED"` when the edition cannot be generated at all:
a missing or invalid `web-edition.toml`, a leaf declared ineligible, or a
converter that cannot run are the standing cases.
