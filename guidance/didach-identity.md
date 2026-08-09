# didach.ai public identity

## Status and authority

This document owns the candidate public identity and whole-site identity layer
for the corpus whose governing future public origin is `https://didach.ai/`.
The origin decision is binding. The visible name, wordmark, hierarchy, copy,
asset, and transition decisions below are a coordinated design candidate until
independent review accepts or changes them.

The candidate was prepared on `ux/didach-identity` from
`origin/main@fc3092de98fee56ab09c406ade257e84e7633e45`. It selectively inspected:

- `origin/ux/foundation@3b5938a0dba88831763ec09c762ae1572007a27e`;
- `origin/ux/corpus-wave-1@e42b9287485a5a6d18ad8a528ab0f0f3f0024ff9`;
- `origin/ux/corpus-wave-1-review-fixes@c66c143643ff75a6cd54afdbe1fcd6eac0aca1b6`.

It does not merge those branches wholesale. C0 Home, C1 Publications, D0
Reader, and E0 Catena are accepted evidence. F0 Sources and the shared-shell
correction at the review-fix head remain candidate work awaiting their own
independent acceptance. This identity lane may demonstrate a consequence on an
accepted surface, but it does not reopen that surface's composition.

This document does not authorize DNS, a `CNAME`, GitHub Pages configuration,
production URL changes, redirects, deployment, a merge to `main`, canonical PDF
changes, publication-prose changes, or a public release. Those operations have
separate owners and require separate authority.

Research and precedent evidence lives in
`guidance/didach-identity-research.md`. Execution state, open review decisions,
and evidence live in `guidance/didach-identity-roadmap.md`. The isolated
real-data candidate lives in `src/web/browser/prototypes/didach-identity/`.

## Product premise

The corpus is the product. didach.ai should feel like the permanent public home
of a serious scholarly library and a family of research instruments, not a
technology company placed in front of Catholic content.

The first encounter must answer, in this order:

1. what this is;
2. what a reader or researcher can do;
3. how its evidence, editions, rights, absences, and provenance can be judged;
4. where the major corpus domains and instruments belong;
5. what role AI has, without making AI the offer or the authority.

Identity earns trust through truthful objects and records. It must never replace
an edition, citation, rights basis, absence reason, review fact, or limitation
with a badge or claim of authority.

## Recommended public name

The sole ordinary public name is **`didach.ai`**.

- Render the exact lowercase ASCII string, including U+002E FULL STOP.
- Keep it uninterrupted and unbroken. Do not insert a space, raised dot, middle
  dot, slash, line break, or separately styled suffix.
- Keep `.ai` the same face, size, weight, and color as `didach`. Context changes
  the size and prominence of the whole wordmark, not the suffix alone.
- Use the full name at ownership points: Home, masthead, browser-title suffix,
  OpenGraph site name and card footer, favicon description, global footer,
  About, citations, and transition notices.
- In sustained reading, make the whole mark quiet and subordinate to the object.
- In prose, use `didach.ai` on first reference and then “the corpus” or “the
  library.” Avoid the awkward possessive `didach.ai’s`.
- When spelling the address aloud, say “didach dot A I.” Do not define “Didach
  AI” as the spoken product name.

Do not use **Didach AI**. It turns the suffix into a product category and is
especially confusable with nearby teaching-and-AI products. Do not establish
**Didach** as a second ordinary UI name: it looks clipped, loses the exact
address, and increases confusion with *Didache*. `Didachai` may appear once in
an About-page etymology, but is not a second brand.

The name alludes to Greek `διδαχή`, teaching or instruction, and the continuous
string can be read as `didachai`, the plural “teachings.” The project must not
claim that the dotted hostname is a normal transliteration or that the corpus
has teaching-office or ecclesiastical authority.

### Naming risk

`didache.ai` is a live enterprise-AI training product, one letter away. Other
Didache books, curricula, journals, and the ancient church order also occupy the
semantic field. The exact dotted spelling and the descriptor below mitigate
confusion but do not constitute trademark clearance. Legal/name clearance and a
pre-launch collision check remain blocking launch work.

## Naming and information hierarchy

1. **`didach.ai`** — public origin, Home link, and public site identity.
2. **A source-first corpus for Catholic faith, worship, and law** — descriptor,
   not part of the proper name.
3. **Publications, Sources, Scripture, Liturgy, History, Law, Commentary** —
   durable public domains.
4. **Catena Omnia, The Source Library, Today’s Missal, The Propers of the Mass, The
   Story of Salvation, How the Missal Changed, The Code, Canon by Canon** —
   purpose-built instruments, not subsidiary brands.
5. **The current object** — publication, passage, source work or edition,
   formulary, civil date, historical act, or canon. It dominates a Reader or
   Instrument.
6. **Treatment and evidence identity** — provider, edition, revision, rights,
   source, witness, and status. These qualify the object; they do not become
   site branding.
7. **Triptych** — project, repository, legal, internal, and historical lineage.

The seven subject portals remain Faith, Scripture, Liturgy, History, Formation,
Mary, and Law in their established order and color roles. They orient the root
catalogue; they are not the same layer as the seven durable browser domains.

## Relationship to Triptych

Triptych becomes lineage, not a co-brand.

Recommended transition sentence:

> didach.ai is the public home of the Triptych corpus.

Triptych remains where removing it would make history or attribution false:

- the repository and project history;
- existing canonical PDFs, publication colophons, and citations;
- the current licence and project-identity boundary;
- stable source paths, schema IDs, storage keys, JavaScript namespaces, and
  implementation identifiers;
- detailed production provenance where naming the producing project matters.

Triptych leaves ordinary public mastheads, browser-title suffixes, generic
OpenGraph identity, routine navigation, result rows, empty states, and 404
branding after an accepted migration. Do not globally replace the string.
Changing existing PDFs or their mirrored web-edition colophons is a separate
publication/legal migration, not identity cleanup.

If the public identity is accepted, `LICENSE` must deliberately add the new
name to its project-identity reservation without weakening existing Triptych
attribution. No prototype is legal clearance.

## Wordmark and typographic system

The primary logo is the live-text wordmark `didach.ai`. It uses the editorial
serif role, weight 700, normal kerning, zero letter spacing, one color, one text
node, and no companion symbol. It must remain legible without a webfont, in
monochrome, with CSS disabled, and in forced colors.

Recommended semantic stacks are:

```css
--font-editorial: Charter, "Bitstream Charter", "Iowan Old Style", Baskerville,
  "Palatino Linotype", Palatino, Cambria, "Noto Serif", "DejaVu Serif",
  Georgia, "Times New Roman", serif;
--font-ui: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
  "Segoe UI", "Noto Sans", "DejaVu Sans", sans-serif;
--font-id: ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace;
--font-greek-serif: Cambria, "Noto Serif", "DejaVu Serif", Georgia,
  "Times New Roman", serif;
--font-hebrew-serif: "Noto Serif Hebrew", "Times New Roman", "DejaVu Serif",
  serif;
```

Use the editorial role for wordmark, headings, and sustained prose; UI for
navigation, controls, metadata, and state labels; monospace only for literal
IDs. Mark Ancient or Koine Greek `lang="grc"`, Modern Greek `lang="el"`, and
Latin `lang="la"`. Mark Hebrew `lang="he"` and preserve an explicit `dir="rtl"`
boundary around right-to-left runs rather than relying on surrounding Latin or
Greek context. Never line-clamp a scholarly title. Allow IDs to wrap anywhere;
ordinary titles wrap at words.

Reject custom webfonts in the first identity implementation. A later frozen SVG
wordmark would require font rights, optical review, fallback parity, and a
separate asset decision.

## Small-space icon

The domain wordmark remains the logo wherever space permits. The candidate
favicon/app mark is a repository-original, optically strengthened lowercase
`d`, cropped from the wordmark rather than established as a second logo.

- At 16 pixels, omit the dot; a one-pixel punctuation mark is unstable and
  must not be the only identity cue.
- At larger sizes, review a plain `d` against a `d.` variant, but do not make
  the dot an AI accent.
- Use one-color-capable geometry. Test 16, 32, 180, 192, and 512 pixels,
  grayscale, forced colors, light and dark browser chrome, and common circular
  or rounded crops.
- Do not use the three Triptych panels, a cross, fish, seal, manuscript glyph,
  Greek letter, sparkle, chat bubble, circuit, neural node, or `AI` monogram.

The current generator admits one 180-pixel PNG as favicon and Apple icon. A
multi-size favicon or manifest package is a later generator/file-set/release-
binding work unit. The identity lane supplies a direction, not production
assets.

## Color and visual roles

Preserve the accepted warm editorial foundation across the identity layer:

- warm paper canvas and quiet raised surfaces;
- near-black primary text with a distinct muted-text role;
- restrained oxblood for identity emphasis and ordinary links;
- blue outline focus that remains distinguishable from selection and error;
- quiet and strong rule roles rather than shadow-heavy containers; and
- the seven established portal colors only where those subjects carry meaning.

Identity components consume these semantic roles. They do not introduce a
second raw brand palette, gradient, glow, or dark shell. Positive, caution,
negative, selection, link, and provenance colors remain state roles, not
decoration.

## Global masthead

The wordmark is the Home link. Its accessible name begins with the visible
string: `didach.ai, home`. Never substitute a pronunciation-only accessible
name.

Wide composition:

- `didach.ai`;
- Publications as a stable high-frequency destination;
- the current durable domain when it differs and is not already present;
- Browse for the complete seven-domain list;
- Jump for context-specific instrument or document destinations.

Exactly one visible wide link has `aria-current="page"`, except an unowned 404
where no destination is falsely marked current. Do not repeat an adjacent
current-domain chip next to the wordmark.

Compact composition:

- `didach.ai` remains intact;
- a short current-domain label may appear when wide navigation collapses;
- Menu and Jump remain distinct actions;
- at 320 pixels the actions may recompose below the wordmark before any label
  shrinks, clips, or wraps.

Menu lists durable corpus destinations. Jump lists context-relevant instruments
or document headings; it is not a duplicate Menu. Use ordinary navigation and
buttons, not ARIA menu roles. A future production shell must retain a real
browse path with JavaScript disabled.

The proposed non-Liturgy shell correction is still awaiting independent
acceptance. Identity evidence may use it as a candidate adapter, never describe
it as accepted.

## Root Home

Recommended first-view copy:

> **A source-first corpus for Catholic faith, worship, and law.**
>
> Read publications and Scripture; trace claims to editions and passages;
> follow commentary, liturgy, historical change, and canon law.

The Home page then presents six task entrances in the accepted order: Read
today; Find a publication; Trace a source; Follow commentary; See what changed;
Look up a canon. Reader-facing and research-facing purposes remain legible from
the ordinary-language verbs and descriptions; do not split them into personas
or application modes.

The Story of Salvation and the Propers remain quiet secondary entrances. The
seven subject portals follow in their established order. Do not add a dashboard,
metric tiles, activity feeds, news carousel, chat prompt, feature-card wall, or
hero art. Generated corpus counts may appear in a quiet evidence sentence only
when derived from the current release; never hard-code mutable totals.

Trust copy belongs after the task entrances:

> AI assists the work; it does not supply authority. Claims stand or fall by
> the identified sources and editions; citations, rights, and stated limits
> make that basis inspectable.

## Surface adapters

Identity supplies shared name, tokens, masthead/footer grammar, browser titles,
and metadata. Reader, Catalogue, and Instrument retain different compositions.

The candidate consequences on previously reviewed work are explicit:

| Surface | Current reviewed identity | Proposed identity-only consequence | Composition preserved | Status and decision owner |
| --- | --- | --- | --- | --- |
| C0 Home | Triptych name and AI-forward shared shell | exact `didach.ai` wordmark, corpus-first title, trust sentence, title/footer metadata grammar | six task entrances, seven portals, order, responsive flow | C0 body accepted; identity consequence open to identity/product reviewer |
| C1 Publications | Triptych shell around list-first Catalogue | exact wordmark, Publications current location, title/footer grammar | filters, list-first results, provider/treatment truth, detail states | C1 body accepted; identity consequence open to identity/product reviewer |
| D0 Reader | Triptych shell around publication Reader | quiet wordmark, provider-qualified browser title, identity footer after publication colophon | title dominance, canonical PDF, Contents, revision, rights, reading measure | D0 body accepted; identity consequence open to identity/accessibility reviewer |
| E0 Catena | Triptych shell around Catena Omnia | quiet wordmark, Commentary location, route/object title, identity footer outside local epistemic footer | Scripture primacy, chronological chain, typed evidence states, hash grammar | E0 body accepted; identity consequence open to identity/product reviewer |
| F0 Sources | review-fix candidate shell and corrected evidence hierarchy | exact wordmark, Sources location, title/footer grammar | Work/Edition ownership, passage/artifact truth, withholding states | F0 and its identity consequence remain candidate; source-product reviewer owns disposition |
| Shared non-Liturgy shell | review-fix candidate | one wordmark, one current place, distinct Browse/Menu and context-specific Jump | stable routes, ordinary navigation, bounded dialogs, compact reflow | candidate; identity/product/accessibility reviewers own disposition |
| Protected Liturgy | separately accepted reader shell | only the atomic adapter described below, in a later authorized unit | all accepted reader composition and behavior | excluded here; liturgy coordinator owns separate approval |

### Publications and Reader

- Keep the list-first Catalogue and the publication title dominant.
- Use `Independent treatment`, `Provider · GPT` or `Provider · Claude`, exact
  revision, browser/PDF availability, and `Parallel treatment` only when the
  relationship exists.
- Do not call provider treatments bibliographic editions or claim every work
  has parallel providers.
- In the Reader, canonical PDF, revision, rights colophon, notes, and long-form
  measure remain publication-owned. The global identity footer follows the
  publication colophon; it does not replace it.

### Catena

- Hierarchy: didach.ai → Commentary → Catena Omnia → Scripture locus and named
  Bible edition → Scripture anchor → chronological held commentary.
- Keep author, work, edition, translator, licence, and passage identity attached
  to fragments. The site brand never becomes source authority.
- Evidence known without held commentary remains visibly different from held
  commentary.

### Sources

- Hierarchy: didach.ai → Sources → The Source Library → external Work → Edition,
  with Artifact, Segment, and Passage as edition-owned siblings where the data
  says so.
- Preserve record, readable-text, withholding, acquisition, and rights states.
  The site does not author or own the external source.
- The review-fix prototype is correction evidence, not accepted F0 design.

### Protected Liturgy

Canonical Day and Propers remain the quality benchmark and are excluded from
the identity overlay. This lane must prove their generated bytes are unchanged.

The eventual visible consequence requiring separate coordinator and liturgy-
specific approval is narrow and atomic:

| Current | Proposed consequence |
| --- | --- |
| three-bar mark plus `Triptych` in the existing reader masthead slot | live-text `didach.ai` in that same slot |
| `Day / Read` or `Propers / Read` | unchanged |
| exactly four actions | unchanged |
| accepted first viewport, reading measure, modal ownership, and print | unchanged |

Site-level title, `og:site_name`, favicon, and route-level social card can later
change through the global metadata owner. Do not add the global shell, a fifth
action, breadcrumb, second modal owner, search, sticky chrome, or branded print.

## Footer and provenance

The global footer begins with:

> **didach.ai** — a source-first corpus for Catholic faith, worship, and law.
> Independent study material; not an official publication of the Catholic
> Church.
> AI assists the work. Claims stand or fall by the identified sources and
> editions; citations, rights, and stated limits make that basis inspectable.

Links: About · Method and AI use · Sources · Contributing · Licensing ·
Third-party material · Feedback · Source code.

During transition, one quiet line may say “didach.ai is the public home of the
Triptych corpus.” Do not make it a permanent dual-brand lockup. Do not put a
blanket CC BY statement in the global footer: external material retains its own
status. Reader rights colophons and Catena/Sources point-of-use licence and
rights statements remain separate and take precedence.

## Browser titles and metadata

Object first, public name last. Use at most object, surface, and site:

- Home: `didach.ai — A source-first Catholic corpus`;
- domain: `Publications · didach.ai`;
- deep object: `John 6 · Catena Omnia · didach.ai`;
- provider-qualified Reader: `{Title} — {Provider} treatment · didach.ai`;
- error: `Page not found · didach.ai`.

Use `og:site_name = didach.ai`. `og:title` carries the bare page or object title
without repeating the site name. Descriptions come from an explicit route or
document summary, not incidental opening prose. Provider qualification prevents
same-title GPT and Claude Readers from colliding.

Every social image has deterministic `og:image:alt` derived from its object
type, visible title, and `didach.ai`; the alt does not repeat qualifiers already
present in adjacent metadata unless needed to distinguish the object. The
ordinary title and description remain complete when the raster abbreviates.

Hash and client-selected query state is not independently available to social
crawlers on static GitHub Pages. Catena chapters, Source passages, law canons,
history stations, Scripture readings, and liturgical selections keep truthful
route-level OpenGraph metadata until generated static object routes exist.

The future didach.ai cutover must atomically align visible identity, canonical
URL, `og:url`, structured-data URL, sitemap, internal links, and one-to-one old-
host redirects. This design lane changes none of them. Do not emit a dead future
canonical or claim the new origin is live.

## Social-card system

The review candidate is a deterministic, repository-original “scholarly folio”
at 1200×630:

- warm field, near-black text, one quiet oxblood or portal-role rule;
- small `didach.ai` identity and written object type;
- exact fixed-route title, at most three measured lines;
- only the edition, provider, revision, locus, or availability qualifier needed
  to identify the object;
- no generated imagery, manuscript texture, photography, saint art, AI art,
  gradients, sparkles, circuits, bots, or copied external assets.

For very long or multilingual titles, preserve the full title in metadata and
use a deterministic size-and-wrap algorithm; fail on missing glyphs or required
identity rather than silently substituting a generic card. A generic site card
is permitted only for genuinely generic routes. Static hash instruments use
route-level cards.

This direction deliberately accepts some large text in the raster, in tension
with platform advice to avoid image text. Review must judge whether large,
redundant, high-contrast type and complete metadata are sufficient, or whether
the production family should be graphical and text-free.

## Empty, error, refusal, and 404 identity

Use the sequence **verdict → basis → recovery**. Brand the containing page;
keep the instrument's epistemic state language.

- 404: `Page not found` — “This address is not part of the published corpus.”
  Actions: `Go to didach.ai`; `Browse publications`; optionally `Report a
  broken citation`.
- Catalogue zero: `No publications match these filters.` Recovery: clear
  filters or browse all publications.
- Rights: `Record available · text withheld.` Keep the recorded reason at the
  point of use.
- Acquisition: `Text not acquired.` Do not imply rights withholding.
- Unsupported numbering: `No verified correspondence.` Preserve the selected
  edition and locus.
- Invalid identity: display the submitted value and fail closed; do not silently
  open a different passage, canon, Mass, or edition.
- Partial: name exactly what is present and missing.
- Load failure: name the unavailable instrument/data and offer a retry or stable
  parent route without inventing content.

Routine empty results may use a polite status. Blocking errors may alert. Never
use a mascot, joke, chatbot apology, or generic “Something went wrong.”

## Responsive, accessibility, color, motion, and print

- WCAG 2.2 AA is the baseline; preserve the project's stronger 44×44 primary
  target rule.
- Test 1440×900, 1024×768, 768×1024, 393×852, and 320×852; 200% text; exact
  320-CSS-pixel reflow; actual native-browser 400% zoom; and the WCAG
  text-spacing override. The automated candidate matrix proves the viewport,
  text-size, text-spacing, and 320-CSS-pixel reflow cases. Its CDP page-scale
  evidence is diagnostic only: native-browser 400% zoom remains an external,
  cross-platform production-acceptance check and is not claimed by this
  candidate.
- Keep the wordmark real text. Its accessible link name begins with the exact
  visible label. Decorative marks are `aria-hidden` when adjacent.
- Preserve skip link → wordmark Home → navigation/Menu/Jump → main order.
- Dialogs contain focus, close with Escape and a visible Close button, restore
  focus and scroll, and make the background inert while modal.
- The identity is static. Reduced-motion mode removes nonessential transitions
  and smooth scrolling.
- Phase one remains intentionally light with `color-scheme: only light`. Forced
  colors uses system colors, real borders/underlines, and outline focus. Do not
  use broad `forced-color-adjust: none`.
- Dark preference is deferred until every Reader, Catalogue, Instrument, state,
  and asset is tokenized and verified together. Do not ship an identity-only
  dark masthead over light content.
- No-JavaScript HTML must retain wordmark, H1, browse path, footer/legal truth,
  source/rights truth, and canonical-PDF access. Buttons that require script may
  not remain dead.
- Browser print is a non-canonical fallback. Hide navigation, dialogs, controls,
  decorative identity, and backgrounds; retain document title, treatment,
  revision, rights, and a compact origin if useful. Canonical PDFs remain the
  printable authority.

## Rejected directions

Reject any candidate that becomes:

- `Didach AI`, `Didach.AI`, `DIDACH.AI`, or a differently colored, weighted,
  glowing, boxed, superscript, animated, or removable `.ai`;
- an AI startup, assistant, chatbot, generic SaaS landing page, dashboard, or
  feature grid;
- a seal, crest, cross, Greek-letter emblem, triptych-panel logo, manuscript
  texture, faux colophon, uncial, blackletter, apologetics-blog, or
  pseudo-medieval identity;
- a permanent `didach.ai × Triptych` lockup;
- a global hero or shell that subordinates a publication, source, Scripture
  locus, canon, Mass, or historical act;
- a visual “verified,” “authoritative,” “trusted,” “complete,” or AI-confidence
  claim unsupported by reachable evidence;
- a uniform layout imposed on Reader, Catalogue, and Instrument;
- a global string replacement of Triptych, internal identifiers, URLs, PDFs, or
  legal attribution;
- object-specific OpenGraph claims for hash-only states;
- a production URL, DNS, redirect, canonical, release-binding, or deployment
  change disguised as design work.

## Change control

Before altering this identity after acceptance, update the durable decision here
and the execution/review state in `guidance/didach-identity-roadmap.md`. Record
new precedent evidence in `guidance/didach-identity-research.md`. A production
implementation must separately update and test every actual owner, including
the global layout, metadata generator, 404, public assets, authorization
bindings, About, licensing consequences, and any approved protected-surface
adapter. It must not infer implementation authority from acceptance of this
design candidate.
