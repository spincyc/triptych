# Linen Cloths — GPT Held Source Audit

The canonical Greek and registered Douay–Rheims artifacts were inspected for
the governing sequence. Existing provider-neutral passage records identify the
Vulgate, Chrysostom, Augustine, Cyril, Aquinas, Westcott, and lexical evidence.
Their existence does not transfer the Claude edition's verification judgment.

Before release, this GPT edition must:

1. inspect every exact central passage and record a GPT publication-local
   binding and fingerprint;
2. replay the Mishnah/Talmud, patristic, Lightfoot, Roman dining, and modern
   provenance searches underlying the folded-napkin negative;
3. distinguish OCR inspection from page-image or critical-text verification;
4. audit every quotation against its identified public-domain translation;
5. record contrary readings and the unresolved content of John 20:8 belief.

No independent review event from the Claude edition applies to this edition.

`source-bindings.toml` records the first independently framed GPT
bindings for the governing Greek and English artifacts, the lexical controls,
Chrysostom, Augustine, the directly relevant rabbinic passages, Roman material
culture, and the earliest located online claim/refutation pair. The source
library validator accepted this active binding file on 2026-07-26. It does not
satisfy the complete binding gate: several patristic, medieval, textual-critical,
material-culture, and modern-provenance claims still require exact artifact
inspection and publication-local binding.

## Live corpus replay blocker — 2026-07-26

The GPT pass attempted a fresh bounded retrieval of Sefaria's text-search page
for `napkin`, directing any response only to the run-owned temporary directory.
The sandboxed request failed at DNS resolution with `Could not resolve host:
www.sefaria.org`. A requested escalated retry remained pending and was
user-aborted without producing a response. After network access was reported
enabled, a new request bounded by a ten-second connection timeout and
thirty-second total timeout failed with the same DNS error. No response bytes,
result list, or receipt were created.

Accordingly the prior edition's forty-nine-hit count is retained only as a lead,
not as a GPT finding. The exact Berakhot and Sanhedrin controls were
independently inspected and bound; the whole-corpus count remains an external
replay gate.
