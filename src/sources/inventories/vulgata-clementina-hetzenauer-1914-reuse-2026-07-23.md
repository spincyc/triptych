# Hetzenauer 1914 Clementine Vulgate Reuse Review

Reviewed on 2026-07-23.

This record documents the bounded canonicalization and reuse proof for
`family.scripture.vulgata-clementina-hetzenauer-1914`, split from the broader
`family.scripture.vulgate-editions` migration cluster. It supplements the
family ledger and does not itself create a source identity, evidence state, or
publication binding. The generic family remains unresolved; these records
identify only the Hetzenauer 1914 Clementine slice.

## Exact edition and retained artifacts

The title leaf identifies Michael Hetzenauer's *Biblia Sacra Vulgatae
Editionis, Sixti V Pont. Max. iussu recognita et Clementis VIII auctoritate
edita*, published by Friedrich Pustet in 1914. The canonical edition is not a
generic “Vulgate”: it remains distinct from other Clementine printings, the
Oxford and Benedictine projects, Weber--Gryson, the Nova Vulgata,
translations, manuscripts, and mutable delivery pages.

SacredBible's technical record, retrieved 2026-07-23, expressly permits
downloading and distributing the image, HTML, and associated files and places
the electronic work in the public domain. Triptych therefore retains:

- the exact 476,635-byte title-page JPEG, SHA-256
  `39fa403aea5ba39fedd793866d86ae990061a69022770f9ef4f168d044740f70`;
- the exact 762,641-byte scan-page 0960 JPEG, SHA-256
  `a40b10652d9d949052bba93a5d11a5134ebf03211be91ddcf95ca0babbcca4ef`;
  and
- a 509-byte, five-line checked transcription of Matthew 8:23--27, SHA-256
  `771cbab22a56479d14d01f5f683b229add77eeccb90aa10f195fcf2c08c923d3`.

The checked text is derived directly from scan page 0960. It preserves the
source wording, capitalization, ligature, and punctuation while omitting
superscript verse numbers, apparatus letters, marginal matter, cross
references, apparatus, and surrounding verses. SacredBible's separate Matthew
HTML is not an evidence ancestor: although the target five verses agree, that
transcription contains at least one nearby error, *patream* for the scan's
*patrem* at Matthew 8:21, and remains only a finding aid.

## Passage and publication normalization

The verified passage is the complete storm narrative, Matthew 8:23--27, from
Jesus entering the boat through the witnesses' final question. Its boundary
was checked with Matthew 8:22 and 8:28, the marginal summary, and the bottom
apparatus visible on the same scan.

The course rendering keeps every word while omitting printed accents,
regularizing consonantal *j/i*, expanding the ligature, and normalizing
capitalization and display punctuation under the curriculum owner's declared
rules. The canonical checked transcription retains the page's source features;
publication bindings describe their received normalized use.

## Reviewed consumers

Two publications consume the complete passage:

1. EL-M22, which prints it as the reader model for guided narrative; and
2. EL-REVIEW-IV, which imports that reader through M22 in its M19--M22 set.

EL-M08 consumes only the bounded Matthew 8:23 phrase *secuti sunt eum discipuli
eius*. It binds the checked artifact at Matthew 8:23, not the five-verse
passage. The nonpublication course owner owns the source decision but is not a
publication consumer. M19, generic packet notices, Vulgate histories, and other
scriptural references are not promoted to this exact passage without their own
edition-and-locus review.

## Acceptance proof

Reverse-use lookup for the passage must return exactly M22 and EL-REVIEW-IV.
Reverse-use lookup for the checked artifact must additionally return M08.
Impact from scan page 0960 must reach the checked text, passage, and all three
publications. A run-local mirror of the actual source graph must validate
before mutation; changing passage metadata must stale exactly the two complete
passage consumers, while changing checked-artifact metadata must stale all
three consumers.

No rendered source or installed PDF changes in this migration.
