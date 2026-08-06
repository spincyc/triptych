# Liturgical Instrument production-integration handoff

- Integration implementation commit: `3cd46072b164ff39b00639bb67ad6b8943a255dc`
- Exact successfully deployed production commit: `5444d89fc9b379a1babef5b2220323fe1508b2b3`
- Final pushed continuity boundary: `0059e501dc535f4546f3966143c8af21e1e119c8`
- Selected direction: Liturgical Instrument — accepted production foundation
- Review state: candidate; independent production-integration review open
- Public navigation: unauthorized and unchanged
- Public cutover: unauthorized
- Pages disposition: run `31125898045` succeeded at 2026-08-06T18:29:55Z
- Day candidate: `https://spincyc.github.io/triptych/liturgy/day-reader.html`
- Propers candidate: `https://spincyc.github.io/triptych/liturgy/propers-reader.html`

## Outcome

The accepted Instrument presentation now runs on the existing unlinked Day and
Propers production-reader candidates through one scoped, last-loaded stylesheet.
Production retains the established state, adapter, renderer, Ordinary seating,
semantic-location, focus, modal, and race owners. The accepted visual-reset
prototype remains unchanged as the oracle.

The extended Chromium run passes 19/19 governed assertions across 100 captures,
including 23 exact accepted-prototype/production pairs. All 23 production
originals were inspected at full size. The 768×1024 Read measure remains 636
pixels/about 75 characters; the 393×852 production Missal begins principal text
3.43 pixels earlier than the oracle while retaining the same reading plane;
1024 and 200% shell geometry match the accepted system. Propers Browse retains
the existing production selector because search remains out of scope.

## Validation and deployment

Focused Python, Propers browser, shared-shell browser, governed visual,
JavaScript syntax, release bindings, promised-deliverables, tool registry,
public-alpha site/preview build and verify, and diff checks pass. Day remains
33/34 solely because of its unchanged date-dependent first-visit expectation.
The governed full gate remains non-green only at unrelated stored example
transcript divergence; no transcript was recaptured or blessed.

Pages run `31125898045` succeeded for exact intended production commit
`5444d89fc9b379a1babef5b2220323fe1508b2b3`, with every repository verify,
build, compatibility, upload, and deploy step passing. Direct verification
returned HTTP 200 for Day, Propers, and both accepted oracle routes. Deployed
Instrument CSS, Day/Propers JavaScript, and oracle CSS/JavaScript byte-match
source; hashes are in `checks.txt` and `logs/pages-and-parity.txt`.

## Integrity

- `INSTRUCTIONS.md`: `aac369494856665f3c7dd69c2371680a2b25453d54716e34f1352a65b91b0ef4`
- canonical instruction: same; byte-identical by `cmp`
- `PLAN-AND-CONTINUITY.md`: `d466dc57d125d8893020f1918076323488122b9f0e1fbba9197fc2460033a6bb`
- canonical continuity: same; byte-identical by `cmp`
- candidate/source Instrument CSS: `64a566758f20df72f53f0f1dfc90ba82fe4ad28cf0ed55a346066f6c1ed5ee02`; byte-identical by `cmp`

`MANIFEST.sha256` covers every directory file except itself and is generated
last. Its verification, ZIP test, one-top-level-directory proof, and ZIP hash
are recorded in `checks.txt`.

## Review gate

No known implementation, evidence, deployment, asset-parity, accessibility,
or isolation blocker remains. Independent production-integration review is the
only integration gate. A later accepted integration may authorize a separately
scoped cutover plan, but this package does not change or authorize public
navigation or public cutover. No independent integration acceptance is claimed.
