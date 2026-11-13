# Six-group installation plan — scratch only

`install-plan.json` is the finite logical delta for queue sections 1–6. It is
not an installation, approval, or new source finding. `root-merit-inputs.json`
retains every complete old/new selected dictionary, full English body, Latin
body/hash, source grade, source file mapping, and independent review needed for
Root's decision. Earlier proposals remain immutable.

| Group | New proper English uses | Latin selections | Permitted source claim |
|---|---:|---:|---|
| Semen | 3 | 3 | Full governing OLM1981 words; independently old complete Latin; unchanged Bute human English |
| In spiritu | 0 | 1 Ordinary | The named prayer's words match a complete official quotation expressly citing Missal2008; existing historical English unchanged |
| OT21 | 1 | 1 | Complete declared historical assembly and new study English; modern target unresolved |
| All Saints | 1 | 1 | Complete1922 historical Latin and new study English; modern target unresolved |
| Easter Vigil and Easter3 Wednesday/Friday | 3 | 0 | Qualified study English; no Latin admission or2008 upgrade |
| Extended Pentecost | 2 | 0 | Two unchanged existing study English recipient uses; official referral/incipits plus secondary whole-body comparison |

The two Easter Vigil alternative nodes receive only the same neutral
`ordinary_disposition.basis` correction. Their bodies, kinds, options, and
mutual exclusion remain unchanged. Only the two extended-vigil rows of the
four-row temporal proposal are selected. Every other temporal candidate and
queue section 7 onward is excluded from the delta.

The plan has 105 explicit actual-scratch-to-durable mappings: 61 new source
files and 44 candidate, review, and manifest documents. Archival predecessors
and broader original candidate packets are evidence only; their unselected
rows are not authorized by inclusion. The three original Easter source
reviews map from these actual files, with exact hashes verified:

- `.scratch/modern-new-orations-review/easter-vigil/review.json`
- `.scratch/modern-new-orations-review/easter-3-wednesday/review.json`
- `.scratch/modern-new-orations-review/easter-3-friday/review.json`

Their destinations are the existing declared
`workflows/reviews/missal-english-completion-2026-11-12/postconciliar/easter-study-three/*-source-review.json`
paths, not assumed pre-existing canonical files. The independent temporal
note review is retained separately from the shared addendum which authored
those two notes. Frozen evidence retains its original historical scratch
strings; this explicit path map supplies their durable counterparts without
rewriting accepted bytes. No protected target PDF or image is copied into the
publication tree.

`apply_to_scratch.py` reads the current canonical documents, checks exact
finite preimages, and applies the logical changes to a fresh snapshot under
this scratch directory. It refuses the repository root and every output
outside this directory. It never takes an old whole inventory from a
candidate package, and all writes replace files atomically so shared hardlinks
cannot modify canonical bytes. Re-run with a fresh output path:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 .scratch/modern-next-cohort-plan/apply_to_scratch.py \
  --output-root .scratch/modern-next-cohort-plan/another-dry-run-root
```

`scratch-apply-receipt.json` records the actual live inputs, scratch outputs,
and preservation checks. The selected delta leaves all other positive
English entries and refusals unchanged, including the current Hildegard and
Newman gaps. It preserves every unselected proper node, Latin sidecar row,
and current Ordinary element. In spiritu's complete English source dictionary
and body remain unchanged.

`validate_merged.py` checks the full merged source graph, exact body/artifact
joins, actual Latin publication owners and decisions on six surfaces,
English overlays and qualification in both consumers, and the complete
Ordinary before/after projection. `merged-validation.json` is the resulting
receipt. This is author integration validation using the pinned independent
source reviews; it is not a new independent merits decision or a final
browser/source-epoch adoption check.

The inherited `d85c36fb` Lasance derivative metadata record is unchanged and
pinned separately. Root owns its truthful digitizer-notice correction as a
separate action; no body, binary, permission, or metadata repair is hidden in
this plan. Any later correction needs its own successor pin.

Root can review the finite complete-expression decisions and then implement
the logical delta against the still-matching live preimages. The only
executable supplied here is intentionally restricted to scratch. Durable
candidate/review retention and source additions belong in the same eventual
adoption as their receiving entries. No canonical files were changed by this
lane.
