# Workflow repair, authorized 2026-09-10 by the maintainer

Sequence (a workflow edit is digest-bound and kills any live run):
1. Finish run 05f2d2fd7c2cf8b3 (leaf 55) to ACCEPTED and commit.
2. Apply the workflow change + whatever the cold review finds. Version bump.
3. Drive 56, then 54, under the new version.

## The defect that prompted it
`proper-finish` has `content-preflight` (program gate, 13 checks) between
`author-proper` and `content-evaluation`, but NOTHING between
`derive-synthesis` and `synthesis-evaluation`. The companion is never
screened by a program, so a class grep could settle costs a full two-lane
AI evaluation round and drains one subset at a time.

Evidence from run 05f2d2fd7c2cf8b3, synthesis loop:
  SYN-CON-005  2 sites in 99-references.tex   (iteration 0)
  SYN-CON-006  3 sites, same file, same shape (iteration 1)
  SYN-CON-008  1 site,  same file, same shape (iteration 2)
Three rounds, one file, one shape. Only a driver-instructed class sweep in
the third revision found the last two sites (Schuster, Gueranger).

This is the same pathology OPERATOR.md records for house-voice, which was
answered by moving the class into a program gate.
