# Supplemental controls review against current main

**Disposition: preserve upstream homily-coverage semantics.** The selective
manifest change previously approved against `a53e262d00d2658ac079801b07b26deeffb05a6d`
must not be carried unchanged onto `origin/main` at `b373dd5db`. The earlier
approval remains bounded to its recorded snapshot and does not approve this
integration.

Commit `6f3a3567c99e47dacd7370775451432b66389f3f`, including its explicit
commit rationale, settles the ambiguity. Current-main
`guidance/liturgy/propers-three-documents.md:508–517` says homily
`element_keys` declares the elements whose research informs the speech; the
checker requires all of them. This does not claim that the spoken body recites
each element. The same profile expressly permits selective preaching. On this
baseline the complete manifest and selective speech are compatible, so the
proposed subset gate changes a settled field's meaning rather than repairing
an unresolved checker/profile contradiction.

Recommended integration:

- Restore the upstream checker and omit the three tests introduced solely for
  its proposed selective-homily contract.
- Remove the added profile sentence declaring a nonempty homily subset and
  its continuation, and remove `derive-homily.md`'s instruction to declare only
  elements actually used in the spoken component. Preserve the existing
  researched-coverage definition in the mechanical-gates section.
- Retain the corrected question/inference controls, consequential-textual-
  difficulty judgments, and text-driven homily movement. The prior P2 repair
  permitting distinct answers to the same question remains appropriate.
  `homily-review.md`'s refusal to require enumeration of every minor proper is
  compatible with upstream and may stay.
- Explain the changed disposition in the durable controls review/operator
  record. Preserve the historical observation that the pc-s53 writer expanded
  the sermon, but do not present it as proof that current main requires spoken
  enumeration or still has a contradictory gate.
- Bump the editorial workflow to **v9**. Upstream commit
  `a0ced2ce22775a65d7ffc13a95263a1fe871b684` already introduced v8 with
  `proper-study-v4` research seals, automatic chronology computation/source
  dependency discovery, and the clarified old-quota sentence. Preserve all of
  those changes. Resolve research.md using upstream's “Inspect” instruction;
  the added Psalm questions do not justify restoring redundant manual
  chronology dependency declarations.

This review read the current-main profile, both controlling commit rationales
and diffs, and the attempted controls diff against current main. The worktree
was still in conflict resolution when inspected; this report recommends the
resolution and does not certify a completed merged tree or new workflow digest.
No tests were rerun and no tracked files were changed. A final bounded diff
check should confirm that these resolutions are present before seeding.
