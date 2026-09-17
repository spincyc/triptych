# Independent font-notice supplement

**PASS. No finding in the six-line URW Palladio L addition to `THIRD_PARTY.md`.** This is a separate 2026-09-17 supplement; it does not replace the 58-file integration snapshot or accept a publication's content or appearance.

Reviewed `THIRD_PARTY.md`: SHA-256 `518e37e1dac872463377e98da05084f5b6a3238464066a3e09dfad36acf150b9` (22,819 bytes). The rest of this file was outside the supplementary change. The prior source-retention snapshot and its already-reviewed source notice remain separate evidence.

The inspected proof was `.scratch/tlm-production/author-study-0000/author-proof.pdf`, SHA-256 `e4cc786b57ab10ec4ba835d0bf12b487a5da7127fe760d3a1a980e64b64825b3` (193,334 bytes). Independent `pdffonts` reports embedded subsets of `URWPalladioL-Roma`, `URWPalladioL-Bold` and `URWPalladioL-Ital`, alongside two Latin Modern Mono fonts. This supports the notice's statement that the proper-study production uses URW Palladio L.

I resolved and read the unencrypted ASCII header of each of these installed Type 1 font programs, each identifying version 1.05:

| Program | Font name | Exact SHA-256 |
| --- | --- | --- |
| `uplr8a.pfb` | `URWPalladioL-Roma` | `1fa269c3d9f9cce83a3d032dc58122a7d514a79e6027c86858d8f1761d47d1f4` |
| `uplri8a.pfb` | `URWPalladioL-Ital` | `47495953f98b3c05f123d4dfdd331e2db6884e61df76b05a5e085ac3910951cb` |
| `uplb8a.pfb` | `URWPalladioL-Bold` | `763886de629c882c76e3b5f26702664984ca4219067a6edd60b1d098c53d01f3` |

All three headers identify URW++ Design & Development's 1999 copyright, refer to the GNU General Public License, and expressly allow inclusion in a PostScript or PDF text document irrespective of the document's own licensing conditions. The notice accurately paraphrases that exception and keeps the font programs outside Triptych's CC BY 4.0 offer. It does not invent a GPL version or extend the document-embedding exception into a general relicensing of the fonts.

The [CTAN URW Base 35 record](https://ctan.org/tex-archive/fonts/urw/base35), checked on 2026-09-17, independently lists URW Palladio L as part of the package and identifies GPL licensing. The exact installed headers, rather than that general package label, are the evidence for the embedding exception. The complete fetched HTML is retained as `ctan-urw-base35.html`, SHA-256 `73ca715c7213fda19bb3c729582b865aeb73ba2a1fd0adc88b4b7b9ad0f36887`.

Commands and evidence:

- `pdffonts .scratch/tlm-production/author-study-0000/author-proof.pdf` — exit 0; independently saved as `font-proof-pdffonts.log`.
- `kpsewhich uplr8a.pfb uplri8a.pfb uplb8a.pfb` — exit 0; all resolve under the installed `fonts/type1/urw/palatino/` directory.
- Python read each resolved PFB as bytes, verified the opening PFB ASCII-segment marker, decoded the complete first segment using its encoded length and hashed the complete program — exit 0. Exact headers are preserved in the three `*.pfb.header.txt` files; all input hashes and resolved files are recorded in `font-notice-evidence.json`.
- `curl -fLsS https://ctan.org/tex-archive/fonts/urw/base35 -o .scratch/source-integration-review/ctan-urw-base35.html` — exit 0; complete page acquired after checking the official CTAN page.

The notice makes no claim that Pazo Math is embedded, and this proof's `pdffonts` output does not list it. This review identifies the sampled proof's font names and the matching installed font programs; it does not inspect every final TLM or NO artifact, reconstruct subset font byte provenance, judge authoring quality, or grant visual/final-PDF acceptance. No subject was changed; all reviewer writes remained in the assigned scratch directory.
