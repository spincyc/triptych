## Claude propers 54–56 integrated and driven under proper-finish v5, 2026-09-09

<!-- draft; production results to be filled in per leaf -->

Three Claude branches (`feature/claude/propers/tlm/54`, `/55`, `/56`) had each
stopped short of a published leaf and left a handoff. Read together, the
handoffs named one structural cause and several owned gaps:

- **The absolute ceiling stopped converging runs.** Run `2bd4a1ab7521853d`
  (55) blocked at 8/8 with blocking counts 18, 17, 10, 5, 5, 3, 3, 3 and three
  leaf-local findings standing; run `e4aebcbd941b6b1a` (56) at 7 rounds with
  18, 12, 10, 8, 7, 5, 7; run `efff3a6f73c1f451` (54) at 8/8 with one finding
  standing and four of five lanes passing. In every case the repeat budget was
  barely charged: revisers repaired what they were given and evaluations kept
  finding new work, because five lanes over ~2,500 lines sample rather than
  enumerate, advisories re-filed as blocking to be heard (31% of 56's blocking
  findings), both editions were judged at once, and criterion 12 repairs
  deleted the bounds criteria 1 and 2 require.
- **Three classes had no owner**: false assertions about what an appointed
  text says (three stood through four evaluations of 55 as observations), the
  guide's statements about itself, and the brief in `proper-finish`, which no
  stage could correct.
- **Two host limits** ended the 54 and 56 second productions mid-flight, one
  lane short and mid-derivation respectively.

Branch 56 had already sequenced the editions (`proper` v26) and made
advisories travel; branch 54 had fixed the criterion-12 oscillation under the
same version number. Both are integrated, reconciled, and carried to `proper`
v27 / `proper-finish` v5 in `cbaa57659`, whose commit message and
`workflows/OPERATOR.md` list the changes. The source-identity reconciliation
the three merges needed is
[`claude-propers-54-56-identity-reconciliation-2026-09-09.md`](src/sources/inventories/claude-propers-54-56-identity-reconciliation-2026-09-09.md).

### Left standing for the maintainer

- `CON-CIT-012`/`CON-EVI-011` (55): the `pentecost-13/14/15` `[[untranslated]]`
  rows of `roman-1962-proper-translations-v1.toml` still type the Cummiskey
  1861 orations rights-withheld while verified passage records exist.
- `CON-EVI-008`/`CON-EVI-012` (55): the Cummiskey Secret and Postcommunion
  passage records state verification against the wrong marginal numbers (1571,
  1573 for 1589, 1591).
- `CON-EVI-007`/`CON-EVI-013` (55): every antiphonary datum rests on
  gregorien.info's index, which the AMS edition record calls a lead.
- `CON-EVI-018` (56): `roman-1962-proper-latin-provenance-v1.toml` collates a
  `j`/consonantal-`i` difference at the Sixteenth Sunday Postcommunion that
  neither book has.
- `CON-SYN-206` (54): the profile's synthesis-companion paragraph binds the
  companion to both an integrated commentary and a synthesis over one evidence
  set; the sequenced workflow now judges that under derivation fidelity, but
  the profile sentence itself is unchanged.
- Five stale tests pin the pre-revision Fourteenth Sunday specimen or a
  chronology fixture (`test_workflow_content_preflight` ×4,
  `test_workflow_chronology` ×1); three fail on `main` already.

### The Fifteenth Sunday under proper-finish v5, run 6fb5fba4867eb8cf

Seeded 2026-09-09 against the merged tree at `cbaa57659`. Blocking counts by
round: **11 → 6 → 8 → 14**, and **not one finding has repeated**: the repeat
budget stands at 1 of 4 (charged once, on the first failure of the streak)
while consecutive failures stand at 4 of 8. Rounds three and four each routed
through `brief-revision`, the stage `proper-finish` v5 added: nine `brief`
findings have now been corrected in place — a verb identity the Greek does not
bear, Bede's figure inverted, an unevidenced claim of Cassiodorus's
independence, the Catena's lemma frequencies, Ps. 94:3's place in the psalm,
the Guéranger volume's imprint (1909, not "Duffy 1900"), an editorial
paragraph heading quoted as Augustine's sentence, and two loci off by one.
Under v4 every one of those would have had no owner, and the next authoring
pass would have regenerated the leaf's side of them.

Three host interruptions were recovered rather than restarted: two session
rate limits (14:00 and 19:00 America/Chicago) and the exhaustion of the
weekly Fable allowance at 19:45, after which the maintainer switched the
session to `claude-opus-5[1m]`. Each time the run state was verified
unchanged and the killed agents were resumed in their own contexts; the run's
intervention ledger records all three, and the model change besides.
