# Cummiskey Preface note: source-impact review, 13 October 2026

The new Twenty-first Sunday research found an unsupported comparison in the
1861 Cummiskey English-prefaces transcription. Row 6's project-authored note
said the facing Latin reads *Quam* where the Roman text reads *Quem*. The
researcher inspected the Cummiskey printed p. xxix, PDF p. 40, and the 1962
Vatican Missal printed p. 293, PDF p. 374. The coordinator independently
inspected those same full-page facsimile rasters: both plainly read *Quam
laudant*. This supports the specific edition comparison, not a claim about
all Roman Missal editions.

The repair removes the false contrast and records the checked 1962 agreement.
The registered source is
`artifact.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861.praefationes-en`.
Against foundation commit `9c4d5e5eb`, a parsed comparison of every TSV row and
field found exactly one changed cell: row 6, `notes`. Every English text,
incipit, heading, locator and other field is unchanged. The artifact manifest
changes only the payload SHA-256 and byte size. The payload changes from
`c3d14547a313e50ba297204cc6ee1f6abc8efbbbbef9110dd922bd8a5c32b957`
to `67400ec1b528854f45e1ab8a1b0598235d9471072b1e26e261db1ea5d1871441`.

The existing binding consumers were reviewed individually, as required by
`guidance/sources.md`; this is not a permission to copy changed fingerprints
without assessing their use.

| Consumer | Existing use and inspected evidence | Impact disposition |
| --- | --- | --- |
| Claude `57-seventeenth-after-pentecost` | Its `research/source-bindings.toml` uses rows 5–6 as historical-English translation control, with `inspected` status. Its `propers/verified.md` already records that the 1861 and 1962 Latin wording agrees, distinguishing punctuation, capitals and *quotidie/cotidie*. The reader sources do not assert the removed *Quam/Quem* contrast. | The used English and its identified bounds are unchanged; update this artifact's binding fingerprint with a context reference to this review. Preserve its evidence states and historical reviews. |
| GPT `60-twentieth-after-pentecost` | Its binding uses the common opening and Trinity continuation as textual control, verified on 2026-10-05. Its `propers/verified.md` expressly records “Latin Quam, not Quem”; both its retrieved text and `sections/10-appointed-text.tex` print *Quam*. | The used English, printed Latin and existing collation conclusion are unchanged; update this artifact's binding fingerprint with a context reference to this review. Preserve its states and original verification date. |

The new artifact fingerprint is
`sha256:228733d9248988b0eb27e84b159ee4053384eb72863134056c1c9ed115f753b5`.
The two source bindings are updated only after the impact assessment above.
No publication prose, PDF, generation timestamp, archived packet, review seal
or historical acceptance is renewed by this repair. The research and source
gates for the new Sunday must still run on the resulting source graph.

The complete source check later exposed two stale reader projections of this
same comparison note: `src/web/data/structure/ordinary/roman-1962.json` and
`src/web/data/structure/ordinary/roman-pre-1955.json`. They were regenerated
through `mass-ordinary structure`. Independent parsed comparisons with the
previous committed files find exactly one changed value in each:
`sections[2].elements[5].note`. Every other parsed value is identical, including
the prayer texts, dates and rights fields. This carries the already checked
source correction into its existing reader consumers; it supplies no new
collation or renewed approval.
