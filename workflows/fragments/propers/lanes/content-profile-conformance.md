# Lane: Profile Conformance

## Your lane

You own criteria **9 (Pagination)**, **10 (Provenance)** and **12
(Declarative discipline)** of the shared criteria list above, and nothing
else. Another lane owns each of the remaining criteria; do not report on
them, and do not judge the work as a whole.

Read the leaf's structure and its source records against the profile in
`guidance/liturgy/roman-1962-propers.md`, and answer only:

9. Does the content structure match the required reader order and page
   assignments from the profile?
10. Do the source records — `propers/verified.md`, `propers/retrieved.txt`,
    and `research/scope.md` — exist and follow the profile's format?
12. Does the reader-facing prose state its findings, or does it repeatedly
    narrate how the editors reasoned, what principles guided inclusion, why
    caution was necessary, what methodology governs the section, or why an
    interpretation is being presented at all? Weigh recurrence rather than a
    single sentence: a claim-local qualification that keeps a claim accurate
    is required by the profile, and so is the terminal apparatus. `Appendix:
    Scope and Qualifications`, `References`, and the exploratory notice and
    `Strongest limit` field of `The Propers: Interpretive Possibilities` are
    qualification by design and out of scope. In scope is their register
    leaking into the substantive body — the four senses, `Themes and
    Movement`, `Detailed Commentary`, the integrated commentary, and the
    source-grounded synthesis. A criterion 12 finding is `authoring`, and it
    is repaired by rewriting the sentence, never by deleting what it was
    about.

Judge the source structure only. The mechanical gates measure the rendered
pages; do not rediscover what they check.

## Result

Return an evaluator result for this lane. `PASS` when none of the three is
violated, `CHANGES_REQUIRED` with blocking findings when any is, `BLOCKED`
when a finding cannot be resolved by revision.

Finding IDs must use the `CON-PRO-` prefix and be stable across iterations.
