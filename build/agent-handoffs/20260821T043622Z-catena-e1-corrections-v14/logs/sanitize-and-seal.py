#!/usr/bin/env python3
"""Sanitize a handoff package, prove it clean, and only then seal it.

WHAT IT DOES
============

Given a package directory, the tool runs one ordered pipeline:

  self-check -> clear manifest -> normalize -> scan -> index-check
             -> screenshot-pair audit -> HARD GATE -> write MANIFEST.sha256

* SELF-CHECK. This file is a package member and is scanned by its own checks,
  so a private value written into it as a literal would make it blind to that
  value exactly the way a shipped denylist is blind to itself. Every private
  value is derived at run time, and `own_source_literals()` asserts that
  property before anything is written.
* NORMALIZE rewrites private tokens in every text member to placeholders.
* SCAN re-derives the private values and asks, independently of whether any
  rule fired, whether any of them survives. Rules and checks for a class are
  built from ONE shared pattern constant, so a rule that cannot repair what its
  check flags is unrepresentable.
* INDEX-CHECK resolves every artifact a Markdown member names against the
  package root, and reports members no document references.
* SCREENSHOT-PAIR AUDIT digests every `before--`/`after--` pair and reports
  whether the two bytes are identical.
* HARD GATE. A single private-token hit, a missing referenced artifact, or a
  byte-identical pair that a document claims shows a difference, and no
  manifest is written at all.

Identities come from the environment and can be overridden with
`SANITIZE_USER`, `SANITIZE_HOST`, `SANITIZE_UID` and `SANITIZE_HOME`, so a
reviewer can re-run the scan with the operator's values and reproduce the
zero-hit result.

Usage:
    sanitize-and-seal.py PACKAGE_DIR                  normalize, scan, seal
    sanitize-and-seal.py PACKAGE_DIR --normalize-only normalize and scan; never
                                                      writes a manifest
    sanitize-and-seal.py PACKAGE_DIR --check-only     scan only; never seals
    sanitize-and-seal.py PACKAGE_DIR --manifest-only  audit the frozen rows and
                          [--claims claims.json]      seal; never rewrites
    sanitize-and-seal.py PACKAGE_DIR --verify         verify an existing seal;
                                                      writes nothing

    sanitize-and-seal.py --sanitize-files PATH [PATH ...]
                                                      normalize and scan files
                                                      that are NOT package
                                                      members; no package
                                                      directory is taken
    sanitize-and-seal.py --scan-files PATH [PATH ...] scan those files only;
                                                      never rewrites one

    --defer PATH  (repeatable, normalize/check modes) a document may reference
                  PATH while it is absent: a later pipeline phase writes it.
                  The deferral is printed, and the final gates run without it.
    --repo PATH   the repository root that reduces to `$REPO`. Without it the
                  root is probed with `git rev-parse --show-toplevel` in the
                  CALLER'S CWD, so two consumers of one rewrite table can
                  resolve two different values -- or none.

`--verify` recomputes every digest in `MANIFEST.sha256`, reports members that
are missing, altered or unlisted, and -- when a sibling `<package>.zip` and
`<package>.zip.sha256` exist -- recomputes the archive digest and compares it
against the recorded sidecar value. Any mismatch exits non-zero.

CHANGED IN V13
==============

Four defects, and three of them share one shape: a leak class that no rule and
no check covered, so the transcript reported zero hits over a real disclosure.

1. THE SCRATCH RULE REQUIRED A HARNESS MARKER IN THE DIRECTORY NAME. A plain
   `mktemp -d` root has none, so it passed through verbatim into the sealed
   archive at three sites -- and since rule and check are one constant, the
   check was blind in the same place. `SCRATCH_DIR` is now the CLASS: any
   absolute path under a temporary root. See `TEMP_ROOT`.

2. THE DASH-FLATTENED WORKSPACE SLUG SURVIVED. A harness names a per-workspace
   scratch directory by flattening the workspace path, and `WORKSPACE_PATH` is
   built from `/`-separated segments, so it cannot match that spelling by
   construction. Prefix, account and session id were all replaced around it
   while the flattened tail -- the whole worktree topology -- stood, three
   times. `WORKSPACE_FLAT` is the new class, and `_scratch()` no longer
   re-emits a tail it has not examined.

3. NOTHING COULD SANITIZE A FILE OUTSIDE THE PACKAGE. Every mode took a package
   directory and `members()` walks it, so the transcripts the pipeline writes
   AROUND the package -- after the manifest, outside the root, and tracked --
   were never sanitized at all. Twelve committed lines carried the absolute
   workspace path, the account name and the tool-anchor path.
   `--sanitize-files` and `--scan-files` apply the SAME table and the SAME gate
   to an explicit file list. See `sanitize_outside()`.

4. `$REPO` DEPENDED ON THE CALLER'S CWD. `repo_root()` probed git where the
   process started, so one rewrite table resolved differently for different
   consumers -- and from the tool anchor, which is not inside a repository, the
   `$REPO` rule was silently not installed at all. `--repo` makes it explicit;
   the probe remains the default. See `repo_root()`.

CHANGED IN V11
==============

1. THE WORKSPACE AND THE LANE SURVIVED SANITIZATION. Evidence is produced
   inside an agent workspace, whose path is `<root>/<project>/<slug>` -- two
   segments that together name the line of work -- and whose lane evidence
   lives under an agent directory named for that lane. The V10 home rules
   rewrote the `/home/<account>` PREFIX only, because the account-name class
   stops at a separator, so everything after it stood: the review counted the
   workspace pair surviving 89 times and the lane directory 88 times under a
   scan that reported ZERO hits, because `forbidden()` had no rule for either.
   Both halves were blind at once. There are now shared patterns for both --
   `workspace-path` and `evidence-dir` -- so each backs a rule AND a check, and
   the workspace rule accepts the prefix RAW or ALREADY TOKENIZED, since the
   home rule runs first and a `$HOME`-prefixed path is the same disclosure.

2. THE BUILDER'S UTC OFFSET LEAKED IN PLAINTEXT. The `utc-offset` rule replaced
   the offset MARKER and kept the local wall clock, so a package carrying
   `<local time><tz>` beside an archive name stamped in UTC disclosed the zone
   by subtraction, with the archive never opened. Redaction was the obvious
   alternative and is the wrong one: the members that carry these stamps are
   provenance ledgers whose whole value is start/end ORDER and ELAPSED time,
   and a ledger of placeholders proves nothing. THE STAMP IS NOW SHIFTED TO ITS
   UTC EQUIVALENT and marked `Z` -- see `_to_utc()`. Ordering and every
   duration survive to the second, and there is no offset left to subtract. A
   stamp already reduced to `<local time><tz>` by the previous version cannot
   be recovered -- that repair threw the offset away -- so the residue shape
   has its own rule and check, `local-time-tokenized`, and is dropped whole.

CHANGED IN V9
=============

THE SEAL IS NOW TWO MODES, BECAUSE THE MANIFEST WAS WRITTEN TOO OFTEN. The V8
pipeline ran the whole normalize-and-seal pass twice, so a manifest existed
while later steps were still rewriting members, and `claims.json`'s inventory
was captured mid-pipeline -- five members moved after it was sized, and the
package's own audit called that residue informational. The V9 pipeline
separates the two writes this file used to make in one breath:

* `--normalize-only` is the V8 default path WITHOUT the manifest: it rewrites,
  scans, and gates, and the pipeline loops it until a `--check-only` pass
  reports zero hits AND zero would-be substitutions over the whole tree,
  transcripts included. `--check-only` therefore now runs the substitution
  table dry and reports what it WOULD change; a nonzero count fails the check,
  because a tree that a rewrite pass would still touch is not at a fixpoint
  and nothing derived from it can be final.
* `--manifest-only` is the manifest WITHOUT the rewrite: given `--claims`, it
  re-hashes every frozen inventory row and REFUSES on any drift, re-scans for
  private tokens, and only then writes `MANIFEST.sha256` once. Nothing may
  write inside the package after it.
* `--defer` replaces the V8 placeholder logs. V8 pre-created four empty logs
  so the index check would find them; an inventory then sized the
  placeholders. Now the pipeline DECLARES the late members instead, absence
  is tolerated only where declared, and nothing is ever sized before it is
  written.

CHANGED IN V6
=============

1. TIMEZONE MATCHING WAS INCOMPLETE. The area list omitted most of the IANA
   set, the city part could not contain a digit (so the legacy signed-offset
   zones in the `Etc` area never matched), and the `posix` and `right` path
   prefixes were unhandled. The area list is now complete, the city class
   accepts digits, both prefixes are recognised, and the legacy single-word
   zones -- including the factory zone and the local-time symlink name --
   are matched in a widened set of timezone contexts. The `utc-offset` RULE
   and CHECK were also asymmetric: the rule rewrote a bare `[+-]HH:MM`
   anywhere, the check only flagged one attached to a full time. Both are now
   built from the same two constants, and both require a timestamp.

2. A FAILURE PATH LEFT A STALE MANIFEST. `normalize()` rewrites member bytes;
   if the scan or the index check then failed, the run returned 1 without ever
   reaching `manifest()`, whose `unlink` was the only thing that removed the
   previous run's file. The package was left carrying digests that described
   its pre-normalization bytes. The manifest is now removed BEFORE the first
   member is rewritten, and a failing `--check-only` run removes it too: a
   package can never carry a manifest that does not describe it.

3. FALSE POSITIVES HARD-BLOCKED ORDINARY DATA. `:<digits>.<digits>` was read as
   a D-Bus name, so minified JSON coordinates, a CSS-style width and the
   fractional part of a timestamp all blocked sealing; the RFC1918 rule matched
   any three-component `10.x.y`, so a version triple became an IP; the
   utc-offset rule rewrote a time range; and 32 unbroken hex digits were read
   as a machine id, so any MD5 digest blocked sealing. Each pattern is now
   shaped to the token it is looking for -- a bus name is not preceded by a
   word character, a quote or a dot; a private address has all four octets; a
   compact 128-bit id is matched only after a label that says it is one -- and
   every one of those negatives is a regression test.

4. MISSING REFERENCED ARTIFACTS WERE NOT RELIABLY DETECTED. The index check
   only considered backticked names CONTAINING a slash, which exempted every
   top-level package member, and it accepted a reference that resolved under
   EITHER the package root or the referring file's directory, so a
   wrong-directory reference passed. Bare artifact names are now checked and
   every reference resolves against the package root only. Referenced-but-
   absent artifacts are reported as such, and members no document references
   are reported as data.

5. THE PACKAGE HASH WAS NEVER VERIFIED. `--verify` is new; see Usage above.

6. SCREENSHOT PAIRS WERE NEVER AUDITED. A package claimed five before/after
   pairs showed visible differences; all five were byte-identical. Every
   `before--`/`after--` pair is now digested and reported as identical or
   differing, and an identical pair described by a Markdown member in
   difference-claiming language FAILS the gate. See `CLAIM_WORDS`.

7. ROBUSTNESS. `is_text()` sniffs only the head of a file, so a member that is
   clean at the head and binary later raised `UnicodeDecodeError` mid-run,
   after earlier members had already been rewritten. Decoding failures are now
   caught, the member is treated as binary, and the skip is reported. Hit lists
   were truncated to 50 while a full count was printed; the truncation is now
   stated in the output.

TWO CONSTRAINTS SHAPE WHAT IS EXPRESSIBLE HERE
==============================================

* NO PRIVATE VALUE MAY BE A LITERAL IN THIS FILE. `own_source_literals()`
  asserts this at startup instead of trusting the author to remember it.
* THIS FILE IS SCANNED BY ITS OWN CHECKS, so a check that flags a bare word
  flags this file for containing that word in its own pattern. That is why
  bare zone names are matched only in a zone context, why no area-plus-city
  sequence is written anywhere in this source, and why the examples in the
  comments carry `N` where a real leak would carry a digit.
"""

from __future__ import annotations

import argparse
# V11: the utc-offset rule shifts a local stamp to UTC instead of blanking the
# offset, so it needs real calendar arithmetic -- a `-05:00` stamp near
# midnight moves the DATE, and a hand-rolled hour subtraction would not.
import datetime as _datetime
import getpass
import hashlib
# V9: the manifest-only mode reads the frozen inventory out of claims.json.
import json
import os
import re
import socket
import subprocess
import sys
# V7: the ZIP is opened and its members proved against the manifest. V6 never
# imported this, which is the whole of why the archive's contents went
# unchecked while its bytes were checked twice.
import zipfile
from pathlib import Path

MANIFEST_NAME = "MANIFEST.sha256"

PLACEHOLDER_USER = "<user>"
PLACEHOLDER_HOST = "<host>"
PLACEHOLDER_UID = "<uid>"
PLACEHOLDER_PID = "<pid>"
PLACEHOLDER_DBUS = "<dbus-name>"
PLACEHOLDER_UUID = "<uuid>"
PLACEHOLDER_TZ = "<tz>"
PLACEHOLDER_EMAIL = "<email>"
# V11. Path-shaped placeholders, spelled like `$HOME`/`$REPO`/`$SCRATCH` so a
# normalized path still reads as a path.
PLACEHOLDER_WORKSPACE = "$WORKSPACE"
PLACEHOLDER_EVIDENCE = "$EVIDENCE"

HIT_LIMIT = 50

# ---------------------------------------------------------------------------
# SHARED PATTERNS. Every class below is covered by BOTH a normalize rule and a
# scan check, and both are built from the SAME string -- see SHARED_BEFORE_IDS
# and SHARED_AFTER_IDS, which the rule table and the check table both consume.
# A rule that cannot repair what its check flags is therefore unrepresentable.
# Patterns that need a runtime identity value (the uid) cannot be constants, so
# for those the shared part -- the risky part, the boundary -- is the constant
# and only the value is spliced in at call time.
# ---------------------------------------------------------------------------

# A process id is identifiable ONLY by the label in front of it. A bare integer
# is indistinguishable from a byte count, a duration or a line number, so no
# value-keyed rule could be safe. Covers `pid=N`, `Pid:<tab>N`, `PID N`,
# `--pid N` and `ppid=N`; the label is captured so the replacement keeps it.
PID_LABELLED = r"\b(p?pid\b[ \t:=]+)\d+"
PROC_PID = r"/proc/\d+\b"

# uid/gid/euid/egid/ruid/rgid/suid/sgid, plus the word labels; the optional
# `--` covers command-line flags. The `\b` sits after the dashes because there
# is no word boundary before one.
UID_LABEL = r"(?:--)?\b(?:[ers]?[ug]id|user|group|owner)\b[ \t:=]+"

# Private workspace and home paths, value-free forms.
HOME_PATH = r"/(?:home|Users)/[A-Za-z0-9._-]+"

# V13 CORRECTION 1. ANY absolute temporary-directory path, not only one whose
# name happens to carry an agent-harness marker.
#
# V12 required a harness marker substring inside the first segment. A plain
# `mktemp -d` name has no such substring, so a scratch root of the shape the
# temporary root plus `tmp` plus a dot plus ten random letters passed through
# VERBATIM into the sealed archive at three sites -- the example is spelled out
# in words here for the reason the header gives: writing it as a path would
# make THIS FILE a hit under the very rule below.
#
# Because the rule and the check are built from this ONE constant, the check
# was blind in exactly the same place: the seal transcript reported zero
# private-token hits over a package that named the operator's scratch root
# three times. A marker-keyed pattern cannot be a class; the CLASS is "an
# absolute path under a temporary root", and that is what is matched now.
#
# The roots are enumerated rather than guessed: the FHS pair, the macOS
# `/private` aliases of the same pair, the macOS per-session TMPDIR tree, and
# the environment-variable spelling a script writes when it has not expanded
# it. At least ONE segment under the root is required, so bare prose about a
# temporary directory is not a hit and `$SCRATCH` -- the placeholder this rule
# writes -- cannot match it either. Written in fragments for the reason the
# header gives: this file is scanned by this pattern.
TEMP_SEGMENT = r"[A-Za-z0-9._-]+"
TEMP_ROOT = (r"(?:\$TMPDIR"
             r"|(?:/private)?/(?:var/)?" + r"tmp"
             # The macOS per-session tree carries TWO opaque segments derived
             # from the account before the temporary directory itself, so the
             # root has to swallow both; stopping after the first would leave
             # half an account-derived identifier standing, which is the
             # prefix-only repair this whole file exists to reject.
             r"|(?:/private)?/var/" + r"folders/" + TEMP_SEGMENT
             + r"/" + TEMP_SEGMENT + r"(?:/T)?"
             + r")")
SCRATCH_DIR = TEMP_ROOT + r"/" + TEMP_SEGMENT + r"(/[^\s\"'>)\],]*)?"

# V11 CORRECTION 1, FIRST HALF. An agent workspace path. What is matched is the
# CONVENTION and never one name: a worktrees root, then exactly the two
# segments -- project and slug -- that together identify one line of work.
#
# HOME_PATH above rewrites the `/home/<account>` PREFIX and nothing else, since
# its account class stops at a separator. That left the two segments standing
# in every path the package carried, and no check looked for them, so the seal
# transcript reported zero hits over a package that named the workspace 89
# times. Prefix repair is not identity repair.
#
# The prefix is accepted BOTH raw and already tokenized. Ordering forces it:
# the home rules run first, so by the time this rule sees a path it usually
# reads `$HOME/git/worktrees/<project>/<slug>` -- which is exactly the same
# disclosure as the raw form, and is the form that survived V10. A short run of
# segments may sit between the home and the worktrees directory, because the
# root is configurable; it is anchored at a home so that an ordinary RELATIVE
# path containing the same directory name is never touched.
WORKSPACE_SEGMENT = r"[A-Za-z0-9._-]+"
WORKSPACE_ROOT = (r"(?:\$HOME|/(?:home|Users)/" + WORKSPACE_SEGMENT + r")"
                  + r"(?:/" + WORKSPACE_SEGMENT + r"){0,3}?"
                  + r"/worktrees")
WORKSPACE_PATH = (WORKSPACE_ROOT
                  + r"/" + WORKSPACE_SEGMENT
                  + r"/" + WORKSPACE_SEGMENT
                  + r"(?![A-Za-z0-9._-])")

# V13 CORRECTION 2, FIRST HALF. The DASH-FLATTENED spelling of the same
# workspace path, which is a different string and therefore was a different
# leak class -- and there was no rule and no check for it at all.
#
# An agent harness names a per-workspace scratch directory by flattening the
# workspace path: every separator becomes a dash. `WORKSPACE_PATH` above is
# built from `/`-separated segments and cannot match that form by
# construction, so the V12 package shipped, at three sites, a scratch path
# whose prefix, account and session id had all been replaced while the
# flattened tail stood intact -- and the tail is the whole topology: the
# worktrees root, the project and the slug, in order, joined by dashes.
# Replacing three of four components is not repair.
#
# The convention is matched, never one name: a flattened home root, any run of
# flattened segments, the flattened worktrees root, then the remainder. The
# remainder is taken whole because a project or slug may itself contain dashes
# and nothing in the flattened form distinguishes a separator dash from a name
# dash -- which is exactly why the flattened form must collapse ENTIRELY
# rather than be parsed.
#
# THE REMAINDER MUST CARRY AT LEAST ONE DASH, which is what keeps ordinary
# hyphenated prose out. `WORKSPACE_PATH` requires exactly TWO segments after
# the worktrees root -- the project and the slug -- and flattening joins those
# two with a dash, so a remainder with no dash at all cannot be a flattened
# workspace and is far more likely to be an English compound.
#
# An intermediate segment is accepted as a PLACEHOLDER as well as raw, for the
# reason `WORKSPACE_ROOT` accepts `$HOME`: the account-name rule runs after
# this one, but a re-scan of an artifact an EARLIER version repaired meets the
# half-tokenized form, and that is the same disclosure.
FLAT_SEGMENT = r"(?:[A-Za-z0-9._]+|<[A-Za-z][A-Za-z0-9-]*>)"
WORKSPACE_FLAT = (r"(?<![A-Za-z0-9._-])"
                  + r"-?(?:home|" + r"Users)-"
                  + r"(?:" + FLAT_SEGMENT + r"-)*"
                  + r"work" + r"trees-"
                  + FLAT_SEGMENT + r"(?:-" + FLAT_SEGMENT + r")+"
                  + r"(?![A-Za-z0-9._-])")

# V11 CORRECTION 1, SECOND HALF. The lane evidence directory: the agent
# directory segment plus the lane name under it, which is a SESSION identity --
# it says which round of which correction built the package. Matched wherever
# it appears, absolute or relative, because that segment is the same
# disclosure either way. Written in fragments for the reason the header gives:
# this file is scanned by this pattern, and the examples in the comments carry
# `<...>` where a real leak would carry a name.
EVIDENCE_DIR = (r"(?<![A-Za-z0-9._-])" + r"\." + r"agents"
                + r"/" + WORKSPACE_SEGMENT
                + r"(?![A-Za-z0-9._-])")

# A unique bus name as it really appears: standing in a `busctl` column, after
# an `=`, inside parentheses -- that is, NEVER flush against a word character,
# a dot or a quote.
#
# V5 matched `:N.N` after a word boundary as well, which made every one of
# these ordinary data shapes a hard blocker:
#     minified JSON      {"x":12.5,"y":34.0}     -- quote before the colon
#     a style-ish datum  width:1440.0            -- word char before the colon
#     a wall-clock time  HH:MM:SS.mmm           -- digit before the colon
# The lookbehind rejects all three and still accepts every position a bus name
# is actually printed in. A bus name written flush against a word character --
# no separator at all -- is deliberately NOT matched: nothing prints it that
# way, and the false-positive cost of allowing it was total.
DBUS_NAME = r"(?<![\w.'\"]):\d{1,5}\.\d{1,10}(?![\w.])"

# Both spellings of a 128-bit id. The word boundaries keep the hyphenated form
# from biting a chunk out of a 40-hex git object name or a 64-hex digest.
UUID_HYPHENATED = (r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}"
                   r"-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b")
# The compact form -- what the machine id and CDP target ids use -- is SHAPE-
# IDENTICAL to an MD5 digest and to any other 32-hex datum, so shape alone
# cannot decide it. V5 matched on shape and blocked sealing on every MD5 in the
# package. It is matched here only after a label that says what it is; the
# label is captured so the replacement keeps it.
UUID_LABEL = (r"(?i:\b(?:machine[ _-]?id|boot[ _-]?id|uuid|guid"
              r"|(?:target|session|frame|loader|request|node|device|instance"
              r"|browser[ _-]?context|execution[ _-]?context)[ _-]?id"
              r"|id)\b[\"' \t:=]{0,4})")
UUID_COMPACT = r"(" + UUID_LABEL + r")([0-9a-fA-F]{32})\b"

# An address, with the public forms this repository legitimately carries held
# out by name: the no-reply trailer addresses are published identities, not
# machine-private ones, and flagging them would fire the hard gate on every
# commit trailer in the package. The systemd instance suffixes are held out for
# a different reason -- `user@N.service` is not an address at all.
EMAIL_EXEMPT = (r"(?:noreply@anthropic\.com"
                r"|[A-Za-z0-9._%+-]+@users\.noreply\.github\.com"
                r"|noreply@github\.com"
                r"|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.(?:service|socket|scope"
                r"|slice|target|timer|mount|device|path))"
                r"(?![A-Za-z0-9._%+-])")
# The lookbehind is load-bearing: without it the engine simply restarts one
# character into an exempt address and matches its tail.
EMAIL = (r"(?<![A-Za-z0-9._%+-])(?!" + EMAIL_EXEMPT + r")"
         r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")

LOOPBACK = r"\b(?:127\.0\.0\.1|localhost):\d+\b"

# A private address has ALL FOUR octets. V5 accepted three components after
# `10`, so a version triple and a coordinate triple were both rewritten as
# addresses. Each octet is range-checked, and the lookarounds keep the match
# from starting or ending inside a longer dotted run.
OCTET = r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
RFC1918 = (r"(?<![\w.])(?:10(?:\." + OCTET + r"){3}"
           r"|192\.168(?:\." + OCTET + r"){2}"
           r"|172\.(?:1[6-9]|2\d|3[01])(?:\." + OCTET + r"){2})(?![\w.])")

# A UTC offset is only a UTC offset when it is attached to a timestamp. V5's
# RULE rewrote a bare signed `HH:MM` anywhere -- which ate a time RANGE such as
# `10:00` minus `11:30` -- while its CHECK required a full time in front. Both
# forms below now drive BOTH the rule and the check; the timestamp is captured
# so only the offset is replaced.
UTC_OFFSET_DATED = (r"(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}(?::\d{2})?"
                    r"(?:[.,]\d+)?)([+-]\d{2}:?\d{2})(?![\d:])")
UTC_OFFSET_TIMED = (r"(\b\d{2}:\d{2}:\d{2}(?:[.,]\d+)?)"
                    r"([+-]\d{2}:?\d{2})(?![\d:])")

# V11 CORRECTION 2, THE RESIDUE SHAPE. A stamp the PREVIOUS version repaired --
# local wall clock, offset replaced by the placeholder -- is still a
# disclosure: the package name carries a UTC stamp, and the difference between
# the two is the offset. It cannot be repaired into an instant, because the
# earlier repair threw away the only thing that would let it be: the offset
# itself. So this class is dropped whole rather than shifted, and it is the one
# place in this file where evidence is lost rather than moved. Nothing a V11
# pipeline writes reaches this rule -- the two rules above run first and leave
# a `Z` behind, not a placeholder.
LOCAL_TIME_TOKENIZED = (r"(?:\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}(?::\d{2})?"
                        r"|\b\d{2}:\d{2}:\d{2})(?:[.,]\d+)?"
                        + re.escape(PLACEHOLDER_TZ))

# The IANA area set in full, plus the legacy areas and the two path prefixes a
# zoneinfo tree carries. Written as separate fragments so that no area-plus-
# city sequence exists in this file's own source -- see the header: this file
# is scanned by this pattern. The city class accepts DIGITS, without which the
# legacy signed-offset zones could not match.
TZ_PREFIX = r"(?:(?:posix|right)/)?"
TZ_AREA_NAME = (r"Africa|America|Antarctica|Arctic|Asia|Atlantic|Australia"
                r"|Brazil|Canada|Chile|Cuba|Egypt|Eire|Etc|Europe|Indian"
                r"|Iran|Israel|Jamaica|Japan|Libya|Mexico|Mideast|Navajo"
                r"|Pacific|Poland|Portugal|Singapore|SystemV|Turkey|US")
TZ_CITY = r"[A-Za-z0-9_+-]+"
TZ_AREA = (TZ_PREFIX + r"\b(?:" + TZ_AREA_NAME + r")"
           + r"/" + TZ_CITY + r"(?:/" + TZ_CITY + r")?")

# The bare zone names -- the ones with no area prefix -- are matched ONLY after
# something that establishes they are a zone. Two reasons, and both are hard:
# several of them are ordinary English words and a package is free to discuss
# them in prose, and a check listing them as bare words would flag THIS FILE
# for containing that list. V5 recognised three contexts; these are the shapes
# a zone is actually written in. The context is captured so the replacement
# keeps it.
TZ_BARE_NAMED = (r"(?:UTC|GMT|Japan|Israel|Egypt|Cuba|Poland|Turkey|Iceland"
                 r"|Iran|Jamaica|Libya|Portugal|Singapore|Hongkong|Eire|Navajo"
                 r"|Greenwich|Universal|Zulu|Kwajalein|Factory|localtime"
                 r"|PRC|ROK|ROC|GB|GB-Eire|NZ|NZ-CHAT|W-SU|CTT|PST"
                 r"|EST5EDT|CST6CDT|MST7MDT|PST8PDT|EST|MST|HST|CET|EET|MET|WET)")
TZ_CONTEXT_PREFIX = (r"(?:TZ|TZID)[ \t]*[:=][ \t]*[\"']?"
                     r"|zoneinfo/"
                     r"|(?i:time[ _-]?zone)[ \t]*[:=]?[ \t]*[\"']?"
                     r"|(?i:tz(?:name|id|info)?)[ \t]*[:=][ \t]*[\"']?"
                     r"|(?i:zoneinfo\([\"']?)"
                     r"|(?i:localtime[ \t]*(?:->|=>)[ \t]*)")
TZ_CONTEXT = r"(" + TZ_CONTEXT_PREFIX + r")" + TZ_BARE_NAMED + r"\b"


def _keep_first(replacement: str):
    """Replace only the match's second group, keeping the captured context."""
    def apply(match: re.Match[str]) -> str:
        return match.group(1) + replacement
    return apply


# Sub-parsers for _to_utc(). Both anchor on the WHOLE captured group, so a
# shape the offset rules can match but these cannot is a redaction rather than
# a silent pass-through.
_OFFSET_PARTS = re.compile(r"^([+-])(\d{2}):?(\d{2})$")
_STAMP_DATED_PARTS = re.compile(
    r"^(\d{4})-(\d{2})-(\d{2})([T ])(\d{2}):(\d{2})(?::(\d{2}))?([.,]\d+)?$")
_STAMP_TIMED_PARTS = re.compile(r"^(\d{2}):(\d{2}):(\d{2})([.,]\d+)?$")

MINUTES_PER_DAY = 24 * 60


def _to_utc(match: re.Match[str]) -> str:
    """Rewrite a local-offset timestamp to its UTC equivalent, marked `Z`.

    THE V11 CORRECTION, AND THE CHOICE IS THE POINT. V10 replaced group 2 --
    the offset -- and kept group 1, the local wall clock. The package name
    carries a UTC stamp, so the two differed by exactly the builder's offset
    and the archive never had to be opened to recover it.

    Redaction closes that and costs too much: the members carrying these stamps
    are provenance ledgers, and their whole purpose is the ORDER of the entries
    and the ELAPSED time between them. A ledger of `<tz>` proves nothing, and
    sanitizing must not cost evidence -- the same principle `_scratch()` above
    is built on.

    Shifting the instant to UTC costs nothing instead. Ordering is preserved
    exactly, because a single monotone shift is order-preserving; every
    duration is preserved to the second, because both ends move by the same
    amount; and the offset is gone, because the value written IS the UTC
    instant, not a local one with a marker beside it.

    A time with NO DATE wraps modulo the day. Ordering and elapsed time within
    one run survive that exactly -- every entry in one ledger carries one
    offset -- and a run that straddles the UTC date line is the only case where
    the wrapped clock reads out of order, which is why the dated form is
    shifted with real calendar arithmetic instead.

    A stamp that will not parse is REDACTED rather than trusted: emitting a
    value this function could not understand is how a leak survives a rule that
    appears to have fired.
    """
    stamp, marker = match.group(1), match.group(2)
    parts = _OFFSET_PARTS.match(marker)
    if not parts:
        return PLACEHOLDER_TZ
    sign, hours, minutes = parts.groups()
    shift = int(hours) * 60 + int(minutes)
    if sign == "-":
        shift = -shift

    dated = _STAMP_DATED_PARTS.match(stamp)
    if dated:
        year, month, day, sep, hour, minute, second, fraction = dated.groups()
        try:
            moved = (_datetime.datetime(int(year), int(month), int(day),
                                        int(hour), int(minute),
                                        int(second or 0))
                     - _datetime.timedelta(minutes=shift))
        except ValueError:
            return PLACEHOLDER_TZ
        text = (f"{moved.year:04d}-{moved.month:02d}-{moved.day:02d}{sep}"
                f"{moved.hour:02d}:{moved.minute:02d}")
        if second is not None:
            text += f":{moved.second:02d}"
        return text + (fraction or "") + "Z"

    timed = _STAMP_TIMED_PARTS.match(stamp)
    if timed:
        hour, minute, second, fraction = timed.groups()
        total = (int(hour) * 60 + int(minute) - shift) % MINUTES_PER_DAY
        return (f"{total // 60:02d}:{total % 60:02d}:{second}"
                + (fraction or "") + "Z")
    return PLACEHOLDER_TZ


# V13 CORRECTION 2, SECOND HALF. The identity-bearing path classes, compiled
# once, applied to the tail `_scratch()` re-emits. See `_scratch()`.
_SCRATCH_TAIL_REPAIRS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(WORKSPACE_FLAT), PLACEHOLDER_WORKSPACE),
    (re.compile(WORKSPACE_PATH), PLACEHOLDER_WORKSPACE),
    (re.compile(EVIDENCE_DIR), PLACEHOLDER_EVIDENCE),
]


def _scratch(match: re.Match[str]) -> str:
    """Replace the temporary ROOT, and repair what the tail still discloses.

    THE TAIL SURVIVES, AND THAT IS DELIBERATE: a rule that consumed the
    remainder reduced 64 baseline tracebacks to `File "$SCRATCH"` and destroyed
    the identity of the test that raised. Sanitizing must not cost evidence.

    THE V13 CORRECTION IS THAT SURVIVING IS NOT THE SAME AS PASSING THROUGH.
    V12 returned `"$SCRATCH" + group(1)` unexamined, and a harness that names
    its scratch directory after the flattened workspace path puts the whole
    topology in that tail. Prefix, account and session id were all replaced
    around it; the tail stood, and disclosed the worktrees root, the project
    and the slug.

    So the tail is REPAIRED rather than truncated. The three classes applied
    here are the identity-bearing path classes, taken from the same constants
    the rule table and `forbidden()` are built from, so this cannot repair
    something the check does not flag or miss something it does. Every
    replacement is a fixed placeholder, so the result is stable across runs and
    the normalize/check fixpoint still converges. What is left is the artifact
    path -- which is the evidence -- and nothing that names who produced it.
    """
    tail = match.group(1) or ""
    for pattern, replacement in _SCRATCH_TAIL_REPAIRS:
        tail = pattern.sub(replacement, tail)
    return "$SCRATCH" + tail


# (label, pattern, replacement, flags). Consumed by BOTH rules() and
# forbidden(). Split in two only because the account-name and hostname rules
# have to run between them: an address must be placeheld as one token before
# the account-name rule can mangle it into `<user>@domain`, and a home path
# must be collapsed before the account name inside it is rewritten.
SHARED_BEFORE_IDS: list[tuple[str, str, object, int]] = [
    ("scratch-dir", SCRATCH_DIR, _scratch, 0),
    ("home-path", HOME_PATH, "$HOME", 0),
    # V11: AFTER the home rules, deliberately. By here the prefix is usually
    # `$HOME` already, and the workspace pair is precisely what a prefix-only
    # repair leaves behind. The pattern accepts both spellings, so the order is
    # a preference and not a dependency.
    ("workspace-path", WORKSPACE_PATH, PLACEHOLDER_WORKSPACE, 0),
    # V13: the dash-flattened spelling of the line above. A separate class
    # because it is a separate STRING -- `WORKSPACE_PATH` cannot match it -- and
    # therefore needs its own check, which is what it had none of.
    ("workspace-flat", WORKSPACE_FLAT, PLACEHOLDER_WORKSPACE, 0),
    ("evidence-dir", EVIDENCE_DIR, PLACEHOLDER_EVIDENCE, 0),
    ("proc-pid", PROC_PID, "/proc/" + PLACEHOLDER_PID, 0),
    ("pid", PID_LABELLED, _keep_first(PLACEHOLDER_PID), re.IGNORECASE),
    ("email", EMAIL, PLACEHOLDER_EMAIL, 0),
]

SHARED_AFTER_IDS: list[tuple[str, str, object, int]] = [
    ("dbus-name", DBUS_NAME, PLACEHOLDER_DBUS, 0),
    ("uuid", UUID_HYPHENATED, PLACEHOLDER_UUID, 0),
    ("uuid-compact", UUID_COMPACT, _keep_first(PLACEHOLDER_UUID), 0),
    ("loopback", LOOPBACK, PLACEHOLDER_HOST + ":<port>", 0),
    ("private-ip", RFC1918, "<ip>", 0),
    # V11: `_to_utc` replaces the WHOLE match -- the stamp moves, it is not
    # kept beside a marker. `_keep_first` here was the leak: it preserved the
    # local wall clock, which differenced against the package's UTC name
    # recovers the offset the marker was there to hide.
    ("utc-offset", UTC_OFFSET_DATED, _to_utc, 0),
    ("utc-offset", UTC_OFFSET_TIMED, _to_utc, 0),
    ("local-time-tokenized", LOCAL_TIME_TOKENIZED, PLACEHOLDER_TZ, 0),
    ("iana-timezone", TZ_AREA, PLACEHOLDER_TZ, 0),
    ("timezone-name", TZ_CONTEXT, _keep_first(PLACEHOLDER_TZ), 0),
]

# Difference-claiming vocabulary for the screenshot-pair audit. Deliberately
# small, literal and lowercased: a substring test over the Markdown block that
# names the pair. NO_CLAIM_WORDS is consulted FIRST and wins, so a block that
# accurately says the two frames are identical is never treated as a claim --
# a false negative is acceptable, silently sealing a false visual claim is not.
NO_CLAIM_WORDS = (
    "no visual difference", "no visible difference", "no observable difference",
    "no perceptible difference", "no difference", "not different", "unchanged",
    "no change", "byte-identical", "byte identical", "identical",
    "indistinguishable", "same image", "same bytes", "pixel-identical",
)
CLAIM_WORDS = (
    "visible difference", "visibly different", "visual difference",
    "clearly different", "differs", "different", "difference",
    "change is visible", "changed", "now shows", "no longer shows",
    "improvement", "improved", "demonstrates the change", "shows the fix",
    "before/after difference", "side-by-side difference",
)


def identities() -> dict[str, str]:
    """The private values, read from the environment rather than guessed.

    Overridable so a reviewer can re-run this against the sealed package with
    the operator's values and reproduce the zero-hit result themselves.
    """
    user = os.environ.get("SANITIZE_USER") or getpass.getuser()
    host = os.environ.get("SANITIZE_HOST") or socket.gethostname()
    uid = os.environ.get("SANITIZE_UID") or str(os.getuid())
    home = os.environ.get("SANITIZE_HOME") or str(Path.home())
    return {"user": user, "host": host, "uid": uid, "home": home}


def repo_root(override: "Path | str | None" = None) -> str:
    """The path that reduces to `$REPO`.

    V13 CORRECTION 4. This probed `git rev-parse --show-toplevel` IN THE
    CALLER'S CWD and nothing else, so the value was a property of where the
    process happened to start rather than of the work being sanitized. Two
    consumers of one rewrite table then resolved two different `$REPO` values:
    run from the checkout the evidence describes it returned that checkout, and
    run from the tool anchor directory -- which is not itself inside a
    repository -- the same probe returned the empty string and the `$REPO` rule
    was simply not installed. A rewrite table whose contents depend on the
    caller's cwd cannot be reasoned about, and the class it silently dropped is
    the one that names the operator's filesystem.

    An explicit override makes it deterministic. Passing nothing keeps the
    probe exactly as it was, so every existing caller is unaffected.
    """
    if override is not None:
        return str(Path(override).resolve())
    try:
        out = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, check=True)
        return out.stdout.strip()
    except Exception:
        return ""


def rules(who: dict[str, str], root: str) -> list[tuple[re.Pattern[str], object]]:
    """Ordered substitutions. Longest, most specific paths first."""
    user = re.escape(who["user"])
    host = re.escape(who["host"])
    uid = re.escape(who["uid"])
    home = re.escape(who["home"])
    made: list[tuple[re.Pattern[str], object]] = []
    if root:
        made.append((re.compile(re.escape(root)), "$REPO"))
    made.append((re.compile(home), "$HOME"))
    made.append((re.compile(r"/run/user/" + uid), "/run/user/" + PLACEHOLDER_UID))
    made.append((re.compile(r"\buser@" + uid + r"\.service\b"),
                 "user@" + PLACEHOLDER_UID + ".service"))
    made.append((re.compile(r"\buid=" + uid + r"\b"), "uid=" + PLACEHOLDER_UID))
    # The pair form goes first -- `--user N:N` -- because the labelled rule
    # below would otherwise stop at the colon and leave the second half
    # standing. The labelled rule takes a RUN of values, not one, because
    # `/proc/status` prints four uid columns on a line and repairing only the
    # first would leave three behind for the check to block on.
    made.append((re.compile(r"\b" + uid + r":" + uid + r"\b"),
                 PLACEHOLDER_UID + ":" + PLACEHOLDER_UID))
    made.append((re.compile(UID_LABEL + r"(?:" + uid + r"[ \t,]*)+",
                            re.IGNORECASE),
                 lambda m: re.sub(r"\b" + uid + r"\b", PLACEHOLDER_UID,
                                  m.group(0))))
    for _label, pattern, replacement, flags in SHARED_BEFORE_IDS:
        made.append((re.compile(pattern, flags), replacement))
    # The account name as a free-standing token: it is matched as a VALUE on
    # word boundaries, not as a path component, because a bare column in a
    # process listing is where it actually leaks.
    made.append((re.compile(r"\b" + user + r"\b", re.IGNORECASE), PLACEHOLDER_USER))
    made.append((re.compile(r"\b" + host + r"(\.local)?\b", re.IGNORECASE),
                 PLACEHOLDER_HOST))
    for _label, pattern, replacement, flags in SHARED_AFTER_IDS:
        made.append((re.compile(pattern, flags), replacement))
    return made


def forbidden(who: dict[str, str], root: str) -> list[tuple[str, re.Pattern[str]]]:
    """The verification pass. Independent of the rules above by construction:
    these ask "is any private VALUE still present", not "did a rule fire".

    The value-free classes come from the SAME constants the rules do, so no
    check can flag a shape no rule can repair.
    """
    user = re.escape(who["user"])
    host = re.escape(who["host"])
    uid = re.escape(who["uid"])
    home = re.escape(who["home"])
    made: list[tuple[str, re.Pattern[str]]] = [
        ("account-name", re.compile(r"\b" + user + r"\b", re.IGNORECASE)),
        ("hostname", re.compile(r"\b" + host + r"\b", re.IGNORECASE)),
        ("home-literal", re.compile(home)),
        ("session-bus", re.compile(r"/run/user/" + uid)),
        ("user-slice", re.compile(r"user@" + uid + r"\.service")),
        # The optional run of already-substituted placeholders is what lets
        # this catch a column that a partial repair left behind:
        # `Uid:<tab><uid><tab>N`.
        ("uid-pair", re.compile(r"\b" + uid + r":" + uid + r"\b")),
        ("uid-labelled", re.compile(UID_LABEL
                                    + r"(?:" + re.escape(PLACEHOLDER_UID)
                                    + r"[ \t,]*)*" + uid + r"\b",
                                    re.IGNORECASE)),
    ]
    for label, pattern, _replacement, flags in SHARED_BEFORE_IDS + SHARED_AFTER_IDS:
        made.append((label, re.compile(pattern, flags)))
    if root:
        made.append(("repo-path", re.compile(re.escape(root))))
    return made


def own_source_literals(who: dict[str, str]) -> list[str]:
    """Assert that no private value is written into this file as a literal.

    The defect this guards is not a bad denylist; it is a denylist that is a
    REGEX, because a pattern's own metacharacters hide it from a scan for the
    thing it describes. Deriving every private value at run time fixes that --
    but nothing stops the next editor from pasting a real value into a pattern,
    and if they do, this file goes blind to that value silently, with a clean
    report.

    So the property is checked instead of assumed. This is not a substitute for
    the scan: the scan covers this file's CONTENT like any other member's, and
    would catch a plain literal. What it cannot catch is a literal buried in a
    character class or an alternation, which is precisely the dangerous shape.
    This runs before anything is written.
    """
    try:
        source = Path(__file__).read_text(encoding="utf-8")
    except (OSError, NameError, UnicodeDecodeError):
        # Not readable (frozen, stdin, deleted): report it rather than passing
        # a check that was never performed.
        return ["<source unreadable>"]
    found: list[str] = []
    for label in ("user", "host", "uid"):
        if re.search(r"\b" + re.escape(who[label]) + r"\b", source, re.IGNORECASE):
            found.append(label)
    # The home path is matched as a substring: it carries separators, so word
    # boundaries would be the wrong instrument.
    if who["home"] in source:
        found.append("home")
    return found


def is_text(path: Path) -> bool:
    """Sniffed, not guessed from the suffix: a suffix allowlist skips
    `MANIFEST.sha256` and every extensionless file.

    Only the head is sniffed, so this is a fast filter and NOT a promise that
    the whole file decodes -- see read_text_or_none(), which is what every
    caller actually reads through.
    """
    try:
        with path.open("rb") as handle:
            head = handle.read(8192)
    except OSError:
        return False
    if b"\x00" in head:
        return False
    try:
        head.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return True


def read_text_or_none(path: Path) -> str | None:
    """Decode a whole member, or report that it cannot be decoded.

    is_text() sniffs 8192 bytes; a file that is clean at the head and binary
    later used to raise mid-run, AFTER earlier members had been rewritten. A
    member that cannot be decoded is treated as binary and reported.
    """
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError, ValueError):
        return None


def members(root: Path):
    for path in sorted(root.rglob("*")):
        if path.is_file():
            yield path


def digest(path: Path) -> str:
    accumulator = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            accumulator.update(block)
    return accumulator.hexdigest()


def clear_manifest(root: Path) -> bool:
    """Remove any existing manifest. Returns True if one was there.

    This is the fix for the stale-seal defect: the manifest is destroyed BEFORE
    the first member is rewritten, so an aborted or failing run can never leave
    a manifest describing bytes the package no longer has.
    """
    target = root / MANIFEST_NAME
    if target.exists():
        target.unlink()
        return True
    return False


def _rewrite_one(path: Path, table, *,
                 dry_run: bool) -> tuple[bool, int, bool]:
    """Rewrite ONE file through the table. (changed, substitutions, undecodable).

    Extracted in V13 so that `normalize()` (package members) and
    `normalize_files()` (files that are NOT package members) cannot drift
    apart. There is one rewrite here, and both modes call it.
    """
    if not is_text(path):
        return False, 0, False
    original = read_text_or_none(path)
    if original is None:
        return False, 0, True
    text = original
    applied = 0
    for pattern, replacement in table:
        text, count = pattern.subn(replacement, text)
        applied += count
    if text == original:
        return False, applied, False
    if not dry_run:
        path.write_text(text, encoding="utf-8")
    return True, applied, False


def _scan_one(path: Path, name: str, checks) -> tuple[list[str], bool]:
    """Scan ONE file's NAME and contents. (hits, undecodable).

    Extracted in V13 for the reason `_rewrite_one()` is: the outside-file mode
    has to be the SAME gate, not a second implementation of it.
    """
    hits: list[str] = []
    for label, pattern in checks:
        # THE NAME IS SCANNED TOO; contents alone are not enough.
        if pattern.search(name):
            hits.append(f"{name}: [name/{label}]")
    if not is_text(path):
        return hits, False
    text = read_text_or_none(path)
    if text is None:
        return hits, True
    for number, line in enumerate(text.splitlines(), start=1):
        for label, pattern in checks:
            found = pattern.search(line)
            if found:
                hits.append(f"{name}:{number}: [{label}] {found.group(0)!r}")
    return hits, False


def normalize(root: Path, table, *, dry_run: bool = False) -> tuple[int, int, list[str]]:
    """Apply the substitution table; with dry_run, only COUNT what it would do.

    The dry pass is the V9 fixpoint instrument: `--check-only` runs it so a
    tree that a rewrite would still touch fails the check instead of drifting
    under a later pass. Same table, same order, no write.
    """
    touched = 0
    applied = 0
    undecodable: list[str] = []
    for path in members(root):
        if path.name == MANIFEST_NAME:
            continue
        changed, count, bad = _rewrite_one(path, table, dry_run=dry_run)
        applied += count
        if bad:
            undecodable.append(path.relative_to(root).as_posix())
        elif changed:
            touched += 1
    return touched, applied, undecodable


def normalize_files(paths, table, *,
                    dry_run: bool = False) -> tuple[int, int, list[str]]:
    """`normalize()` over an EXPLICIT list of files instead of a package tree.

    V13 CORRECTION 3. `normalize()` walks `root.rglob("*")`, so the only files
    it could ever reach were package members. The logs the pipeline writes
    AROUND the package -- the assemble transcript, the final-verify transcript
    and their siblings -- are written after the manifest, live outside the
    root, and were therefore never passed through the sanitizer at all. In V12
    those tracked files leaked the absolute workspace path, the account name
    and the tool-anchor path on twelve lines, and the twelve lines were
    committed. Same table, same order; only the member set differs.
    """
    touched = 0
    applied = 0
    undecodable: list[str] = []
    for path in paths:
        changed, count, bad = _rewrite_one(path, table, dry_run=dry_run)
        applied += count
        if bad:
            undecodable.append(path.name)
        elif changed:
            touched += 1
    return touched, applied, undecodable


def scan(root: Path, checks) -> tuple[list[str], list[str]]:
    hits: list[str] = []
    undecodable: list[str] = []
    for path in members(root):
        relative = path.relative_to(root).as_posix()
        found, bad = _scan_one(path, relative, checks)
        hits.extend(found)
        if bad:
            undecodable.append(relative)
    return hits, undecodable


def scan_files(paths, checks) -> tuple[list[str], list[str]]:
    """`scan()` over an EXPLICIT list of files. The SAME `forbidden()` gate.

    THE BASENAME IS SCANNED, NOT THE PATH. For a package member the name that
    travels with the bytes is the path relative to the package root, and that
    is what `scan()` checks. An outside file has no package root: its directory
    is the operator's filesystem, which is private BY DEFINITION and is not
    part of what gets published, while its basename is what a reader sees. So
    checking the absolute path here would fail every run on the location of the
    file rather than on its content, which is a gate that says nothing.
    """
    hits: list[str] = []
    undecodable: list[str] = []
    for path in paths:
        found, bad = _scan_one(path, path.name, checks)
        hits.extend(found)
        if bad:
            undecodable.append(path.name)
    return hits, undecodable


# Not a package reference: absolute system paths, repository-relative source
# paths, git refs, URLs, placeholders, and anything carrying an `=` or a
# `:line` suffix.
EXTERNAL_REFERENCE = re.compile(
    r"^(?:https?:|mailto:|ftp:|file:|#|/|\$REPO|\$HOME|\$SCRATCH|"
    r"\$WORKSPACE|\$EVIDENCE|src/|"
    r"tools/|scripts/|guidance/|build/|release/|web/|pdf/|"
    r"impl/|review/|evidence/|origin/|refs/)")
# A backticked token is a candidate package reference only if it has this
# shape. Prose backticks -- flags, commands, `re.sub`, `main()` -- do not.
REFERENCE_SHAPE = re.compile(r"^[A-Za-z0-9._+@-]+(?:/[A-Za-z0-9._+@-]+)*$")
# BARE names (no slash) are checked too -- their absence is what let every
# top-level member escape the check. To keep ordinary dotted identifiers out,
# a bare name qualifies only when its suffix is an artifact suffix. A
# backticked dotted identifier that happens to end in one of these will be
# reported as a missing artifact; that is a loud, trivially corrected false
# positive, and the alternative is the silent miss this replaces.
ARTIFACT_SUFFIXES = {
    "md", "txt", "json", "jsonl", "ndjson", "csv", "tsv", "log", "patch",
    "diff", "png", "jpg", "jpeg", "gif", "webp", "svg", "pdf", "py", "sh",
    "zip", "tar", "gz", "sha256", "html", "htm", "yaml", "yml", "toml", "ini",
    "cfg", "conf", "xml", "mp4", "webm", "har", "css", "js", "ts",
}


def _reference_candidates(text: str) -> set[str]:
    named = set(re.findall(r"\[[^\]]*\]\(([^)]+)\)", text))
    for one in re.findall(r"`([^`]+)`", text):
        if not REFERENCE_SHAPE.match(one) or one.endswith("/"):
            continue
        if "/" in one:
            named.add(one)
            continue
        suffix = one.rsplit(".", 1)[-1].lower() if "." in one else ""
        if suffix in ARTIFACT_SUFFIXES:
            named.add(one)
    return named


CHANGED_FILES = "changed-files.txt"


def repository_paths(root: Path) -> set[str]:
    """Every repository path the package's own changed-file record names.

    Read from `git diff --name-status` output: a status letter, a tab, a path.
    A rename carries two paths and both are repository paths. Anything the
    parse does not recognise is skipped rather than guessed at — a wrong entry
    here would silence a real dangling reference, which is the one thing this
    check exists to catch.
    """
    text = read_text_or_none(root / CHANGED_FILES)
    if text is None:
        return set()
    found: set[str] = set()
    for line in text.splitlines():
        if not re.match(r"^[A-Z]\d*\t", line):
            continue
        for one in line.split("\t")[1:]:
            one = one.strip()
            if one:
                found.add(one)
    return found


def index_check(root: Path,
                deferred: frozenset[str] = frozenset(),
                ) -> tuple[list[str], list[str], list[str]]:
    """Resolve every artifact a Markdown member names against the PACKAGE ROOT.

    Returns (missing, unreferenced, deferred_notes). `missing` is a hard
    failure: the document names an artifact the package does not contain.
    `unreferenced` is data: a member no document mentions, which is how a
    package acquires an orphan.

    `deferred` is the V9 replacement for pre-created placeholder logs: the
    pipeline DECLARES which members a later phase writes, a reference to a
    declared-but-absent member is reported as data rather than failed, and the
    final gates run with an empty deferral set so nothing stays forgiven.

    Resolution is against the package root only. Accepting a reference that
    resolved against the referring file's directory as well meant a
    wrong-directory reference passed.
    """
    missing: list[str] = []
    deferred_notes: list[str] = []
    referenced: set[str] = set()
    # PATHS OF THE REPOSITORY, NOT OF THE PACKAGE. `EXTERNAL_REFERENCE` knows
    # the directory prefixes a repository uses, and cannot know its ROOT-LEVEL
    # filenames — so a document naming a changed file that lives at the
    # repository root read as a dangling package reference.
    #
    # The package already records exactly that set, by construction: the
    # changed-file member is `git diff --name-status` against the parent. Every
    # path it names is a repository path and none is a package member. This is
    # not a filename special case for one correction — every package under this
    # protocol carries that record, and a package without one simply gets the
    # prefix heuristic it had before.
    outside = repository_paths(root)
    for path in sorted(root.rglob("*.md")):
        text = read_text_or_none(path)
        if text is None:
            continue
        for one in sorted(_reference_candidates(text)):
            if EXTERNAL_REFERENCE.match(one) or one.startswith("<") or "=" in one:
                continue
            if one in outside:
                continue
            # A SUFFIX IS NOT A FILENAME. V13: a document may have to describe
            # an artifact it cannot name as present — the outer-sanitization
            # pass writes its transcripts AFTER the gates that would check
            # them, precisely so it can rewrite and re-scan what those gates
            # produced. Naming such a file would be the claim the checks
            # exist to refuse, so the document names the SUFFIX instead. A
            # bare token beginning with a dot and carrying no separator is a
            # suffix: this package has no hidden member for it to be.
            if one.startswith(".") and "/" not in one:
                continue
            # THE SIBLINGS, WHICH ARE NOT MEMBERS AND MUST STILL BE NAMED.
            # V13, the V12 review: the handoff inventory must name every
            # artifact that lives BESIDE the package by its exact filename —
            # V12 omitted one and scored ten of ten — while this check reads
            # every backticked artifact name as a package member. The two
            # requirements are only in tension until the shape is noticed: a
            # sibling is `<this package's own directory name>.<something>`,
            # which no member can be, because a member lives INSIDE that
            # directory. So a reference of that shape is a sibling, and the
            # gate that owns siblings is the inventory, not this one.
            if one.startswith(root.name + "."):
                continue
            if re.search(r":\d+$", one):
                continue
            # THE MANIFEST IS WRITTEN BY THIS TOOL, AFTER THIS CHECK. A document
            # that names it names something the sealed package really contains,
            # and refusing the reference because the file does not exist YET is
            # an ordering bug in the checker rather than an incomplete index.
            if one == MANIFEST_NAME:
                referenced.add(one)
                continue
            if (root / one).exists():
                referenced.add(Path(one).as_posix())
                continue
            if one in deferred:
                deferred_notes.append(
                    f"{path.relative_to(root).as_posix()} -> {one} "
                    f"(absent, deferred: a later pipeline phase writes it)")
                referenced.add(Path(one).as_posix())
                continue
            missing.append(
                f"{path.relative_to(root).as_posix()} -> {one} "
                f"(referenced but absent from the package root)")
    unreferenced: list[str] = []
    for path in members(root):
        relative = path.relative_to(root).as_posix()
        if relative == MANIFEST_NAME:
            continue
        if relative in referenced:
            continue
        unreferenced.append(relative)
    return missing, unreferenced, deferred_notes


PAIR_PREFIXES = ("before--", "after--")


def screenshot_pairs(root: Path) -> list[tuple[str, str, str, bool]]:
    """Every pair of members whose names differ only by a before/after prefix.

    Returns (key, before-relative, after-relative, identical) rows, where `key`
    is the shared remainder -- the directory plus the name with the prefix
    stripped. Pairing is within one directory, which is what "the names differ
    only by the prefix" means.
    """
    seen: dict[str, dict[str, Path]] = {}
    for path in members(root):
        for prefix in PAIR_PREFIXES:
            if path.name.startswith(prefix) and len(path.name) > len(prefix):
                key = (path.parent / path.name[len(prefix):]) \
                    .relative_to(root).as_posix()
                seen.setdefault(key, {})[prefix] = path
    rows = []
    for key in sorted(seen):
        found = seen[key]
        if len(found) != 2:
            continue
        before = found["before--"]
        after = found["after--"]
        rows.append((key,
                     before.relative_to(root).as_posix(),
                     after.relative_to(root).as_posix(),
                     digest(before) == digest(after)))
    return rows


def _blocks(text: str) -> list[str]:
    return re.split(r"\n[ \t]*\n", text)


def pair_claims(root: Path, rows) -> list[str]:
    """Markdown blocks that claim a visible difference for an IDENTICAL pair.

    A block is a run of lines between blank lines. A block counts as a claim
    when it names one of the pair's files (or their shared remainder) AND
    contains one of CLAIM_WORDS AND contains none of NO_CLAIM_WORDS. The
    no-claim check runs first and wins: an accurate "the two frames are
    identical" description must not be punished.
    """
    violations: list[str] = []
    documents = []
    for path in sorted(root.rglob("*.md")):
        text = read_text_or_none(path)
        if text is not None:
            documents.append((path.relative_to(root).as_posix(), text))
    for key, before, after, identical in rows:
        if not identical:
            continue
        names = {before, after, key,
                 Path(before).name, Path(after).name, Path(key).name,
                 Path(key).stem}
        for name, text in documents:
            for number, block in enumerate(_blocks(text), start=1):
                lowered = block.lower()
                if not any(one.lower() in lowered for one in names if one):
                    continue
                if any(word in lowered for word in NO_CLAIM_WORDS):
                    continue
                claimed = [word for word in CLAIM_WORDS if word in lowered]
                if claimed:
                    violations.append(
                        f"{name} (block {number}) claims {claimed[0]!r} for "
                        f"{key}, but {before} and {after} are byte-identical")
    return violations


def manifest(root: Path) -> int:
    target = root / MANIFEST_NAME
    if target.exists():
        target.unlink()
    rows = []
    for path in members(root):
        rows.append(f"{digest(path)}  {path.relative_to(root).as_posix()}")
    target.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return len(rows)


def read_manifest(target: Path) -> tuple[dict[str, str], list[str]]:
    listed: dict[str, str] = {}
    malformed: list[str] = []
    text = read_text_or_none(target)
    if text is None:
        return listed, ["<manifest is not readable utf-8 text>"]
    for number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        found = re.match(r"^([0-9a-fA-F]{64})\s\s?(.+)$", line)
        if not found:
            malformed.append(f"line {number}: {line!r}")
            continue
        listed[found.group(2)] = found.group(1).lower()
    return listed, malformed


def archive_members(archive: Path, root: Path, listed: dict[str, str]) -> list[str]:
    """Prove every ZIP MEMBER against the manifest, and the manifest against it.

    V7 CORRECTION, and the V6 review's load-bearing evidence gap. `verify()`
    proved two things separately — the tree's bytes against the manifest's
    digests, and the archive's bytes against the sidecar's digest — and
    nothing joined them. Nothing opened the ZIP at all; `zipfile` was not
    imported. So a ZIP built from a different tree, or carrying an injected
    member, verified clean, because the sidecar is computed from the archive
    after the fact and therefore always agrees with it. THE ZIP IS WHAT A
    REVIEWER ACTUALLY RECEIVES, and it was the one artifact whose contents
    nothing checked.

    The archive is expected to carry the package directory as its single
    top-level entry, which is what `guidance/external-review-handoffs.md`
    requires of it; the prefix is derived from the directory's own name rather
    than assumed of the entries, so a mis-rooted archive is a finding here
    instead of a silent pass.
    """
    problems: list[str] = []
    prefix = root.name + "/"
    inside: dict[str, str] = {}
    try:
        with zipfile.ZipFile(archive) as handle:
            for entry in handle.infolist():
                if entry.is_dir():
                    continue
                name = entry.filename
                if not name.startswith(prefix):
                    problems.append(f"archive member outside {prefix}: {name}")
                    continue
                digester = hashlib.sha256()
                with handle.open(entry) as stream:
                    for block in iter(lambda: stream.read(1 << 20), b""):
                        digester.update(block)
                inside[name[len(prefix):]] = digester.hexdigest()
    except (zipfile.BadZipFile, OSError) as error:
        return [f"archive unreadable: {archive.name} ({error})"]

    # The manifest never lists itself, and the archive carries it.
    expected = dict(listed)
    seal = root / MANIFEST_NAME
    if seal.is_file():
        expected[MANIFEST_NAME] = digest(seal)
    for relative in sorted(set(expected) - set(inside)):
        problems.append(f"archive omits: {relative}")
    for relative in sorted(set(inside) - set(expected)):
        problems.append(f"archive carries an unlisted member: {relative}")
    for relative in sorted(set(inside) & set(expected)):
        if inside[relative] != expected[relative]:
            problems.append(
                f"archive member does not match the manifest: {relative} "
                f"(manifest {expected[relative]}, archive {inside[relative]})")
    print(f"archive members: {len(inside)} proved against the manifest, "
          f"{len(problems)} problem(s)")
    return problems


def verify(root: Path) -> int:
    """Verify an EXISTING seal. Writes nothing; non-zero on any mismatch."""
    target = root / MANIFEST_NAME
    if not target.is_file():
        print(f"VERIFY FAILED: no {MANIFEST_NAME} in {root}", file=sys.stderr)
        return 1
    listed, malformed = read_manifest(target)
    problems: list[str] = [f"malformed manifest {one}" for one in malformed]
    for relative in sorted(listed):
        path = root / relative
        if not path.is_file():
            problems.append(f"missing: {relative}")
            continue
        actual = digest(path)
        if actual != listed[relative]:
            problems.append(f"digest mismatch: {relative} "
                            f"(manifest {listed[relative]}, actual {actual})")
    present = {path.relative_to(root).as_posix() for path in members(root)}
    for relative in sorted(present - set(listed) - {MANIFEST_NAME}):
        problems.append(f"unlisted member: {relative}")
    print(f"manifest verify: {len(listed)} member(s) listed, "
          f"{len(problems)} problem(s)")

    archive = root.parent / (root.name + ".zip")
    sidecar = root.parent / (root.name + ".zip.sha256")
    if archive.is_file() and sidecar.is_file():
        recorded = ""
        text = read_text_or_none(sidecar)
        if text:
            found = re.search(r"\b([0-9a-fA-F]{64})\b", text)
            recorded = found.group(1).lower() if found else ""
        actual = digest(archive)
        if not recorded:
            problems.append(f"no sha256 recorded in {sidecar.name}")
            print(f"archive verify: {sidecar.name} carries no digest")
        elif recorded != actual:
            problems.append(f"archive digest mismatch: {archive.name} "
                            f"(sidecar {recorded}, actual {actual})")
            print(f"archive verify: {archive.name} DOES NOT match {sidecar.name}")
        else:
            print(f"archive verify: {archive.name} matches {sidecar.name}")
        problems.extend(archive_members(archive, root, listed))
    else:
        print("archive verify: no sibling .zip/.zip.sha256 pair; skipped")

    report(problems, "problem")
    if problems:
        print("VERIFY FAILED: the package does not match its seal.",
              file=sys.stderr)
        return 1
    return 0


def seal_frozen(root: Path, who: dict[str, str], where: str,
                claims_path: Path | None) -> int:
    """P6: the manifest write, alone. NEVER rewrites a member.

    THE V9 CORRECTION LIVES HERE. V8 wrote the manifest as the tail of a
    normalize pass, twice, so the manifest and the inventory each described a
    tree some later step went on to rewrite. This mode is what runs after the
    freeze: it re-hashes every row `claims.json` froze at P3 and refuses on
    any drift -- a frozen member whose bytes moved is a pipeline defect, not
    residue -- re-runs the private-token scan so a leaky package still cannot
    acquire a manifest, and then writes `MANIFEST.sha256` exactly once, over
    every member except itself. Nothing writes inside the package after it.
    """
    if clear_manifest(root):
        print(f"removed a pre-existing {MANIFEST_NAME}: the only manifest is "
              f"the one this run writes")

    hits, undecodable = scan(root, forbidden(who, where))
    print(f"sanitization scan: {len(hits)} private-token hit(s)")
    report(hits, "hit")
    if undecodable:
        print(f"  note: {len(undecodable)} file(s) sniffed as text but not "
              f"decodable as utf-8; contents not scanned")
        report(undecodable, "file")

    drifted: list[str] = []
    if claims_path is not None:
        text = read_text_or_none(claims_path)
        if text is None:
            print(f"cannot read claims: {claims_path}", file=sys.stderr)
            return 1
        rows = json.loads(text)["package"]["rows"]
        for one in rows:
            path = root / one["path"]
            if not path.is_file():
                drifted.append(f"{one['path']}: frozen member is gone")
            elif (path.stat().st_size != one["bytes"]
                  or digest(path) != one["sha256"]):
                drifted.append(f"{one['path']}: bytes drifted after the freeze")
        print(f"freeze audit: {len(rows)} frozen row(s) re-hashed, "
              f"{len(drifted)} drifted")
        report(drifted, "drift")
    else:
        print("freeze audit: no --claims given; no frozen inventory to prove")

    failures = []
    if hits:
        failures.append("REFUSING TO SEAL: private tokens are still present.")
    if drifted:
        failures.append("REFUSING TO SEAL: a frozen member drifted after "
                        "the freeze.")
    if failures:
        for one in failures:
            print(one, file=sys.stderr)
        return 1

    count = manifest(root)
    print(f"{MANIFEST_NAME} written: {count} file(s) covered")
    return 0


def outside_files(paths: list[Path]) -> tuple[list[Path], list[str]]:
    """Resolve the named files, and REPORT anything that is not one.

    A path that does not resolve to a file is a failure and not a skip: the
    caller named it because it believes that file needs sanitizing, and
    silently passing over a typo is how a leaky log ships under a clean
    transcript. Duplicates are collapsed so a file named twice is rewritten and
    counted once.
    """
    found: list[Path] = []
    problems: list[str] = []
    seen: set[Path] = set()
    for one in paths:
        resolved = Path(one).resolve()
        if not resolved.is_file():
            problems.append(f"{one}: not a file")
            continue
        if resolved in seen:
            continue
        seen.add(resolved)
        found.append(resolved)
    return found, problems


def sanitize_outside(paths: list[Path], who: dict[str, str], where: str,
                     *, write: bool) -> int:
    """V13 CORRECTION 3: sanitize (or scan) files that are NOT package members.

    Every other mode in this file takes a package DIRECTORY and can only ever
    reach what is inside it. The pipeline also writes tracked files AROUND the
    package -- `<package>.assemble.log`, `<package>.verify-final.log` and their
    siblings -- after the manifest is sealed, and nothing sanitized those. They
    are committed, so a leak there is as public as a leak inside the archive;
    in V12 twelve such lines carried the absolute workspace path, the account
    name and the tool-anchor path.

    This mode is deliberately NOT a second sanitizer. It applies `rules()` and
    `forbidden()` -- the same table and the same gate the package modes use,
    built from the same shared constants -- and exits non-zero on residue. What
    it does not do is anything package-shaped: there is no manifest, no index
    check, no pair audit and no seal, because these files are not a package and
    pretending otherwise would invent findings.

    `write=False` is the check-only twin: nothing is rewritten, and a file the
    table WOULD still touch fails, for the V9 reason -- a file that is not at a
    fixpoint is not final.
    """
    found, problems = outside_files(paths)
    verb = "sanitize-files" if write else "scan-files"
    print(f"{verb}: {len(found)} file(s) named, {len(problems)} unusable")
    report(problems, "problem")

    would_apply = 0
    if write:
        touched, applied, undecodable = normalize_files(
            found, rules(who, where))
        print(f"normalized {touched} file(s), {applied} substitution(s)")
        if touched == 0:
            print("  (no file changed: inputs were already normalized, or the "
                  "rules matched nothing -- the scan below is what decides)")
        # THE FIXPOINT, ASKED IN THE SAME BREATH. `--normalize-only` may skip
        # this because the P2 pipeline loops it against `--check-only` until
        # the tree stops moving. These files have no such loop around them --
        # one invocation is the whole treatment -- so the mode has to ask the
        # question itself or a file the table would still touch ships as final.
        _, would_apply, _ = normalize_files(found, rules(who, where),
                                            dry_run=True)
    else:
        would_touch, would_apply, undecodable = normalize_files(
            found, rules(who, where), dry_run=True)
        print(f"check-only: {would_touch} file(s) would change, "
              f"{would_apply} would-be substitution(s)")
    if undecodable:
        print(f"  ({len(undecodable)} file(s) sniffed as text but not "
              f"decodable as utf-8; treated as binary and not rewritten)")
        report(undecodable, "file")

    hits, unreadable = scan_files(found, forbidden(who, where))
    print(f"sanitization scan: {len(hits)} private-token hit(s)")
    report(hits, "hit")
    if unreadable:
        print(f"  note: {len(unreadable)} file(s) sniffed as text but not "
              f"decodable as utf-8; contents not scanned")
        report(unreadable, "file")

    failures = []
    if problems:
        failures.append("REFUSING: a named path is not a readable file.")
    if hits:
        failures.append("REFUSING: private tokens are still present.")
    if would_apply:
        failures.append(f"NOT AT A FIXPOINT: {would_apply} substitution(s) "
                        f"would still be applied.")
    if failures:
        for one in failures:
            print(one, file=sys.stderr)
        return 1
    print(f"{verb}: clean; no manifest is written for files outside a package")
    return 0


def report(lines: list[str], noun: str) -> None:
    """Print at most HIT_LIMIT lines, and SAY SO when there are more.

    A truncated list under a full count reads as a complete list.
    """
    for one in lines[:HIT_LIMIT]:
        print(f"  {one}")
    if len(lines) > HIT_LIMIT:
        print(f"  ... {len(lines) - HIT_LIMIT} further {noun}(s) not shown "
              f"(showing the first {HIT_LIMIT} of {len(lines)})")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    # V13: OPTIONAL, because the two file modes below do not take a package.
    # Every other mode still requires it, and the check moved to a place that
    # can say which mode wanted it.
    parser.add_argument("package", type=Path, nargs="?", default=None,
                        help="the package directory (every mode except "
                             "--sanitize-files and --scan-files)")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check-only", action="store_true",
                      help="scan and report; never rewrite a member or seal")
    mode.add_argument("--normalize-only", action="store_true",
                      help="normalize, scan and gate; never write a manifest")
    mode.add_argument("--manifest-only", action="store_true",
                      help="audit the frozen inventory and write the manifest; "
                           "never rewrite a member")
    mode.add_argument("--verify", action="store_true",
                      help="verify an existing seal; writes nothing")
    mode.add_argument("--sanitize-files", nargs="+", type=Path, default=None,
                      metavar="PATH",
                      help="normalize and scan the named files IN PLACE; they "
                           "are not package members and no package directory "
                           "is taken")
    mode.add_argument("--scan-files", nargs="+", type=Path, default=None,
                      metavar="PATH",
                      help="scan the named files and report; never rewrite "
                           "one")
    parser.add_argument("--claims", type=Path, default=None,
                        help="claims.json carrying the frozen rows that "
                             "--manifest-only proves before sealing")
    parser.add_argument("--defer", action="append", default=[], metavar="PATH",
                        help="a reference to PATH may be absent: a later "
                             "pipeline phase writes it (repeatable)")
    parser.add_argument("--repo", type=Path, default=None, metavar="PATH",
                        help="the repository root that reduces to $REPO; "
                             "defaults to `git rev-parse --show-toplevel` in "
                             "the caller's cwd, which is not deterministic "
                             "across callers")
    args = parser.parse_args(argv)

    files = args.sanitize_files or args.scan_files
    if files is None:
        if args.package is None:
            parser.error("a package directory is required unless "
                         "--sanitize-files or --scan-files is given")
        root = args.package.resolve()
        if not root.is_dir():
            print(f"not a directory: {root}", file=sys.stderr)
            return 2
    elif args.package is not None:
        parser.error("--sanitize-files and --scan-files take files, not a "
                     "package directory")

    if args.verify:
        return verify(root)

    who = identities()
    where = repo_root(args.repo)

    # THE SELF-CHECK, BEFORE ANY WRITE. A private value hard-coded into this
    # file's patterns is the one defect that makes every number this tool
    # prints meaningless. Nothing is normalized, and no manifest is written,
    # while that is true. Silent on success.
    blind = own_source_literals(who)
    if blind:
        print("REFUSING TO SEAL: this file contains a private value as a "
              f"literal ({', '.join(blind)}); it cannot see its own leak.",
              file=sys.stderr)
        return 1

    if files is not None:
        # V13: the outside-file modes. Same identities, same self-check, same
        # rules() and forbidden() -- a different member set, and nothing
        # package-shaped after it.
        return sanitize_outside(files, who, where,
                                write=args.sanitize_files is not None)

    if args.manifest_only:
        # P6, alone. Everything before the manifest write in the V8 order --
        # the rewrite, the fixpoint, the derivation, the audit -- has already
        # happened by the time this mode is allowed to run.
        return seal_frozen(root, who, where, args.claims)

    would_apply = 0
    if not args.check_only:
        # BEFORE THE FIRST REWRITE: a manifest that survives a failing run
        # describes bytes the package no longer has.
        if clear_manifest(root):
            print(f"removed the previous {MANIFEST_NAME} before normalizing")
        touched, applied, undecodable = normalize(root, rules(who, where))
        # `normalized 0` is ambiguous between "already clean" and "patterns
        # broken", so both numbers are reported and the distinction is stated.
        print(f"normalized {touched} file(s), {applied} substitution(s)")
        if touched == 0:
            print("  (no file changed: inputs were already normalized, or the "
                  "rules matched nothing -- the scan below is what decides)")
        if undecodable:
            print(f"  ({len(undecodable)} file(s) sniffed as text but not "
                  f"decodable as utf-8; treated as binary and not rewritten)")
            report(undecodable, "file")
    else:
        # V9: the fixpoint question, asked without writing. A tree the table
        # would still touch is not final, whatever the token scan says.
        would_touch, would_apply, undecodable = normalize(
            root, rules(who, where), dry_run=True)
        print(f"check-only: {would_touch} file(s) would change, "
              f"{would_apply} would-be substitution(s)")
        if undecodable:
            print(f"  ({len(undecodable)} file(s) sniffed as text but not "
                  f"decodable as utf-8; treated as binary)")
            report(undecodable, "file")

    hits, undecodable = scan(root, forbidden(who, where))
    print(f"sanitization scan: {len(hits)} private-token hit(s)")
    report(hits, "hit")
    if undecodable:
        print(f"  note: {len(undecodable)} file(s) sniffed as text but not "
              f"decodable as utf-8; contents not scanned")
        report(undecodable, "file")

    missing, unreferenced, deferred_notes = index_check(
        root, frozenset(args.defer))
    print(f"evidence-index check: {len(missing)} missing reference(s), "
          f"{len(unreferenced)} unreferenced member(s), "
          f"{len(deferred_notes)} deferred reference(s)")
    report(missing, "missing reference")
    report(deferred_notes, "deferred reference")
    for one in unreferenced[:HIT_LIMIT]:
        print(f"  unreferenced: {one}")
    if len(unreferenced) > HIT_LIMIT:
        print(f"  ... {len(unreferenced) - HIT_LIMIT} further unreferenced "
              f"member(s) not shown (showing the first {HIT_LIMIT})")

    rows = screenshot_pairs(root)
    identical = [row for row in rows if row[3]]
    print(f"screenshot pair audit: {len(rows)} before/after pair(s), "
          f"{len(identical)} byte-identical, {len(rows) - len(identical)} differing")
    for key, before, after, same in rows:
        print(f"  {'identical' if same else 'differing'}  {key} "
              f"({before} vs {after})")
    claims = pair_claims(root, rows)
    report(claims, "claim")

    # THE HARD GATE.
    failures = []
    if hits:
        failures.append("REFUSING TO SEAL: private tokens are still present.")
    if missing:
        failures.append("REFUSING TO SEAL: the evidence index is incomplete.")
    if claims:
        failures.append("REFUSING TO SEAL: a byte-identical before/after pair "
                        "is described as showing a difference.")
    if args.check_only and would_apply:
        failures.append(f"NOT AT A FIXPOINT: {would_apply} substitution(s) "
                        f"would still be applied.")
    if failures:
        for one in failures:
            print(one, file=sys.stderr)
        # V7 CORRECTION. This removed MANIFEST.sha256 on a failing
        # `--check-only` run, in a mode whose own `--help` says "scan and
        # report; never rewrite a member". The V6 review found it, and the
        # consequence is not theoretical: `PRIVACY-AUDIT.md` instructs a
        # REVIEWER to run `--check-only` on a sealed package, and the same
        # document concedes the account-name pattern raises a false hit on an
        # operator whose username is an ordinary English word. A reviewer
        # named `will` or `mark`, following the package's own instructions,
        # destroyed the integrity proof and then met `sha256sum -c` failing
        # for a second, unrelated reason.
        #
        # The V5 defect this was meant to answer is real and is a different
        # one: `normalize()` REWRITES bytes, and a failing scan then returned
        # before `manifest()` ran, leaving a manifest that no longer described
        # the tree. That can only arise in a mode that writes. `--check-only`
        # never calls `normalize()`, so no staleness can arise there and there
        # is nothing to clear. The clearing moves to the writing path, where
        # the staleness it answers actually happens.
        if not (args.check_only or args.verify) and clear_manifest(root):
            print(f"removed {MANIFEST_NAME}: this package is not sealable")
        return 1

    if args.normalize_only:
        # V9: the rewrite ends here. The freeze, the derivation, the audit and
        # the manifest are later phases, and the manifest is `--manifest-only`.
        print("normalize-only: no manifest written; the freeze comes next")
        return 0
    if not args.check_only:
        count = manifest(root)
        print(f"{MANIFEST_NAME} written: {count} file(s) covered")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
