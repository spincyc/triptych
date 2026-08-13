# Assistive-technology evidence — what was demonstrated, and what was not

The V3 independent review accepted this correction at its core and asked for
two things: that the negatives be scoped to the session that was actually
inspected, and that the identifiers the transcript carried be removed. Both
are done here, and the reason for the second is recorded in
`PRIVACY-AUDIT.md`: the V3 record pasted raw `busctl` and `ps` output, which
published an account name, a host PID, a uid, a systemd user unit and a D-Bus
session address. **No command transcript is reproduced in this file.** The
findings are stated as findings.

## What was demonstrated

- An AT-SPI bus launcher is present on this machine, and an accessibility bus
  was running under the session that ran these checks.
- No display server, accessibility bus client, or login session sufficient for
  real assistive-technology validation was available to the session that ran
  these checks.
- No screen-reader session was completed. **No spoken announcement was
  produced, captured, or verified.**
- No braille device was present, and no braille session was attempted.
- The accessibility evidence in this package is therefore **structural**: it
  is derived from the rendered DOM, its roles, names, states and the text the
  page writes to its status region. Structural evidence remains structural
  evidence, and is not a substitute for a real assistive-technology session.

## What is claimed about announcements

The V3 record described "one announcement". That overstated what was shown.
What is shown is that **the page performs one status-region write** per
render, carrying the same clauses in the same order as the visible tally.
Whether any assistive technology speaks that write, when, or how it interacts
with a live region's politeness, was not tested here and is not claimed.

## Scope of the negatives — read this before quoting them

Every negative above is **scoped to the session that ran these checks**. None
of them is a claim about the tool, the platform, or what is possible in
general.

Specifically, this package does **not** claim:

- that AT-SPI, a screen reader, speech, or braille is unavailable on this
  machine in general;
- that a usable accessibility session cannot be established here;
- that any of these capabilities do not exist, are broken, or are unsupported.

The correct reading is narrower and is the only one supported by the evidence:
**a usable display/AT-bus/session was not available to this session, so no
real assistive-technology validation was performed.** An environment's absence
in one session is not a universal negative, and the V3 record's phrasing
allowed that stronger reading. It should not have.

## What this means for review

Real-device or real-AT evidence remains a **separately owned pre-release
prerequisite**, unchanged and unclosed by this lane. It is recorded in
`UNRESOLVED-BLOCKERS.md`. Genuine system forced-colors likewise remains a
disclosed limitation: the forced-colors evidence here is emulated.

Nothing in this lane's diff touches the shared shell, its landmarks, its
target sizes, or its focus and history behaviour, so the shared-shell
accessibility findings the V3 review recorded are neither addressed nor
affected here.
