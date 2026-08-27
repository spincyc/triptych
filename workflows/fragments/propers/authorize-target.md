# Authorize the Production Target

## Your task

Record the maintainer's decision to open the closed propers boundary for one
provider and one permanent identity, and for nothing else.

The 1962 propers collections are **closed**. `guidance/liturgy/propers-production-plan.md`
is the maintainer's record of that decision, and it is the only place a target
becomes authorized. A permanent identity in the registry is not authorization:
the registry says an identity exists and may never be reassigned, and an
identity with no guide is the normal state of the collection. Authorization is
a separate, dated, per-provider decision, and this stage writes it down.

You are recording a decision, not making one. If the packet's target was not
in fact authorized by the maintainer, say so and stop.

## What an entry authorizes

One entry authorizes **one provider** and **one identity**. It does not
authorize:

- the other provider for the same identity — each provider is a separate
  decision, and each gets its own entry;
- a neighbouring identity, however adjacent in the calendar;
- the series, the band, or the season the identity belongs to;
- any later revision of the same guide beyond the target this entry names.

Never write one entry covering two providers, a range of identities, or a
plural target. An entry that names more than one provider-and-identity pair
is not an authorization record, it is a reopened boundary.

## Steps

1. Read `guidance/liturgy/propers-production-plan.md` completely, and the
   `## Scope boundary` section closely. It states when the collections were
   closed and which targets have since been reopened.
2. Confirm the identity is a registered permanent identity:
   ```
   tools/check-proper-identity --document {proper}
   ```
   A non-zero exit means the leaf id names no identity the 1962 calendar
   registers. Do not write an entry for it; return `BLOCKED`.
3. Confirm the provider is `{provider}` and that it is one this repository
   publishes for: `claude` or `gpt`.
4. Look for an existing authorization line for exactly this provider and this
   identity. Match an entry in the list, not a mention anywhere in the file, so
   that prose discussing a target — or a line revoking one — never reads as an
   authorization:
   ```
   awk -v p='{provider}' -v d='{proper}' \
       'index($0, "- Authorized ") == 1 &&
        index($0, "provider `" p "`, identity `" d "`.") > 0 { found = 1 }
        END { exit !found }' \
       guidance/liturgy/propers-production-plan.md
   ```
   If it is already there, **write nothing**. The target is authorized and
   this stage is done; say so in your summary. Reauthorizing an authorized
   target must not add a second entry, reorder the entries, reword an
   existing one, or restamp its date.
5. If it is not there, append exactly one entry to the `### Authorized
   targets` list inside `## Scope boundary`. The entry is one line, in this
   exact form:
   ```
   - Authorized <YYYY-MM-DD>: provider `{provider}`, identity `{proper}`.
   ```
   `<YYYY-MM-DD>` is today's UTC date (`date -u +%F`). Add the entry at the
   end of the list, so the list reads in the order the decisions were taken.
6. If the `### Authorized targets` subsection does not exist yet, create it
   at the end of `## Scope boundary`, after the paragraph about permanent
   identities, with this heading and this standing text before the first
   entry:
   ```
   ### Authorized targets

   Each line below records one maintainer decision to open the boundary for
   one provider and one permanent identity. A line is the whole
   authorization: it opens that provider's target and nothing else — not the
   other provider, not a neighbouring identity, not the series it belongs
   to. A permanent identity in the registry is not itself an authorization,
   and an identity with no line here is closed.
   ```
7. Change nothing else in the file. Do not restore a status table, a target
   enumeration, or a count the registry or a profile already states; the
   plan's own Maintenance section forbids it. Do not touch the prose
   recording the 2026-07-25 closure or the earlier reopenings.
8. Re-read the file and confirm that it now contains exactly one entry for
   this provider and this identity, that no other provider's or identity's
   line changed, and that the boundary is otherwise still closed.

## Result

Return a worker result with `disposition: "PASS"`, `artifact_path` set to
`guidance/liturgy/propers-production-plan.md`, and a summary saying whether
you added an entry or found one already present, and naming the exact
provider and identity authorized.

Return `disposition: "BLOCKED"` instead when the target may not be
authorized from here: the identity is not registered, the provider is not one
this repository publishes for, or the packet's target is not the target the
maintainer decided on. Name what you found. The scope gate that follows will
refuse the run anyway; blocking here says why in one place.
