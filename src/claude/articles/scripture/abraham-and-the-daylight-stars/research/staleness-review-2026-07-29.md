# Research staleness review — 2026-07-29

## Trigger and method

`scripts/research-staleness explain claude
articles/scripture/abraham-and-the-daylight-stars` reported changed research
after the edition's recorded baseline. The research-first rewrite was drafted
before the current prose was consulted. It was then compared with the current
edition and a minimal-modification candidate under:

- `build/staleness/claude/articles/scripture/abraham-and-the-daylight-stars/rewritten/`;
- `build/staleness/claude/articles/scripture/abraham-and-the-daylight-stars/modified/`;
- `build/staleness/claude/articles/scripture/abraham-and-the-daylight-stars/comparison.md`.

Those paths are ignored working artifacts, not publication or audit inputs.

## Inputs named by `explain`

The edition-local and cross-provider inputs were:

- new `current-guidance-audit-2026-07-27.md` records in both provider editions;
- changed GPT `evidence-map.md`, `scope.md`, `source-audit.md`, and
  `source-bindings.toml`;
- new GPT Hebraic/versional, Hebrew-edition, Jewish-witness, patristic,
  rabbinic/patristic-resolution, independent editorial, independent
  exact-snapshot, independent rabbinic/patristic, final-production, and
  versional-second-pass reviews dated 2026-07-27.

The newly reachable reusable-source inputs named by `explain` were:

- Augustine, *De civitate Dei* 9.2;
- Hetzenauer 1914 Clementine Vulgate retained-page and focused 1 Kings and
  Tobias records, plus the Latin SacredBible and Douay–Rheims 1 Corinthians
  6:9–11 records;
- Swete 1909 retained-page and focused 1 Kingdoms 16 and Exodus 16 records;
- Josephus work, editions, artifacts, and focused *Antiquities* I.10.3 and
  VIII.2.5 records.

Unlike the GPT deterministic set, the Claude `explain` result did not name the
new Kittel–Beer or Syriac Peshitta reusable records because the current Claude
binding file does not bind them. Their findings nevertheless enter this
edition's re-evaluation through the changed cross-provider GPT research
records. The non-Genesis records above are named because they lie under bound
reusable source records; their presence in the input set does not make them
evidence for this article.

## Consequential-claim comparison

| Claim | Effect of changed research | Current / minimal / rewrite |
| --- | --- | --- |
| Verse 5 precedes the narrated sunset if the scene is continuous | Strengthens the textual basis without removing the continuity condition | All three retain the conditional conclusion |
| Genesis 15:17 uses a completed Hebrew form | Contradicted: the verified form is a feminine singular Qal active participle and does not alone prove completed sunset | Current is wrong; both candidates correct it |
| Swete's Greek form explains patristic silence or represents the text used by the Fathers generally | Weakened and unsupported: the evidence permits only a claim about Swete's identified printing, with Augustine's contrary Old Latin at verse 18 | Current overstates; both candidates narrow it |
| The Fathers did not ask the question | Contradicted as a broad formulation and materially narrowed by newly checked loci | Current heading and repeated generalizations overstate; both candidates report Ambrose's visionary reading, Chrysostom's and Ephrem's night–day–sunset sequences, Theodoret's local non-treatment, and Jerome as unchecked |
| Peshitta and *Jubilees* were not reached | Removed: the dated Syriac delivery supplies bounded comparison evidence and *Jubilees* is inspected as rewritten reception, not a textual version | Current records are stale; both candidates reconcile them |
| The Hebrew remained only an uncollated digital text | Removed: Kittel–Beer 1909 pages and exact Genesis loci were directly verified | Current provenance statement is stale; both candidates identify the verified printing and retain its limits |
| Abarbanel states the dilemma | Retained and bounded; no priority claim follows | All three agree |
| Five incompatible answer families exist | Strengthened by the new loci without collapsing their distinctions | All three retain the classification |
| Paul or Hebrews teaches the daylight hour | Not added | All three deny it |
| Daylight makes the sign a demand of faith | Remains conditional project synthesis, not ancient or apostolic exegesis | All three agree |
| Specialist or ecclesiastical approval has been obtained | Not added | All three deny it |

The minimal and rewritten candidates agree on every substantive correction.
They differ principally in compression and architecture.

## Verdict

**Material change is required for the Claude edition.** Its central
conditional daylight conclusion survives, but its Hebrew morphology, Greek
transmission scope, patristic negative claims, witness-status statements, and
Hebrew provenance are materially stale.

Per the staleness policy, replacement requires explicit confirmation followed
by the ordinary editorial, build, page-review, installation, catalog, release,
and rebaseline pipeline. This review performs none of those steps. No ledger
entry was changed and no rebaseline was performed.
