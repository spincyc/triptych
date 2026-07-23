# Leonine *Summa theologiae* Passage Reuse Review

Reviewed on 2026-07-23.

This record documents the first bounded canonicalization and reuse proof for
`family.thomas-aquinas.summa-theologiae`. It supplements the family ledger and
does not itself create a source identity, evidence state, or publication
binding.

## Exact edition and artifacts

The checked witness is the 1888 Leonine *Opera omnia*, volume 4, containing
*Prima Pars* questions 1–49 with Cajetan's commentary. Its title leaf prints
MDCCCLXXXVIII. Internet Archive's item metadata says 1882, so that metadata
value is retained only as a known catalog error and does not control the
edition date.

The exact 532-page Internet Archive Text PDF is 50,128,370 bytes with SHA-256
`13c5497631563814f3573fe81b63f17470b5e06ff669a48607125951cbaf85ce`.
It was acquired and inspected but remains a remote artifact: the 1888 volume
is public domain in the United States, while the item metadata gives no
artifact-level rights statement for this exact digitization.

A separate 185-byte, one-line checked transcription is tracked as a
public-domain derivative. It contains only the complete opening sentence of
I, q. 1, a. 1, *corpus*, not the complete article, volume, or work. Its
SHA-256 is
`03457a82a37e2f5ac58541579c4c04bcc3eb4cd6cfc18b1813847c038f017fb3`.
The derivative preserves the Leonine comma after *salutem* and depends on the
exact remote PDF, so changes to either ancestor invalidate its consumers.

## Passage and normalization

The passage is I, q. 1, a. 1, *corpus* opening, printed p. 6 / artifact PDF
p. 24. The article heading, complete sentence, and beginning of its surrounding
response were visually inspected.

The Ecclesiastical Latin course macro reproduces every word but omits the
source comma after *salutem* under the owner's declared pedagogical punctuation
normalization. Its text is therefore a normalized received passage, not a
diplomatic reproduction of the page image. EL-M21's instruction to copy
“diplomatically from the course text” remains bounded to the printed course
text and does not assert diplomatic identity with the Leonine witness.

## Reviewed consumers

Exactly four publications bind the shared passage:

1. EL-M19, for the sentence in its register comparison;
2. EL-M21, for the scholastic reader, collation, translation, and response
   architecture;
3. EL-M22, for the compact source anthology and bounded source study; and
4. EL-REVIEW-IV, which receives the same course-owned sentence through M19,
   M21, and M22 in its reader set.

M20 does not print the Thomas sentence. The nonpublication course owner owns
the source decision but is not treated as a publication consumer. Other
Triptych citations of Aquinas or the *Summa* are not promoted to this exact
Leonine passage without their own edition-and-locus review. No Corpus
Thomisticum artifact, translation, work-wide search, critical-edition claim,
manuscript collation, author-wide style claim, or repository corpus is implied.

## Acceptance proof

Reverse-use lookup must return exactly the four publications above. Impact
from the remote PDF must reach the checked transcription, passage, and all
four. A run-local mirror of the actual source graph must validate before a
valid passage-metadata mutation and then report exactly four stale consumer
fingerprints with one common replacement value.

No rendered source or installed PDF changes in this migration.
