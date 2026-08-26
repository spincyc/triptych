#!/usr/bin/env python3
"""Dump the replay harness's request and ownership journals.

The V7 review's standard is the ACTUAL REQUEST SINK: the proof is the journal
of paths that reached the stubbed `fetch`, not a helper's return value. This
runs the replay harness exactly as the test suite does — the production
`browser-core.js`, `catena-model.js` and `catena.js` under node, every
scenario driven to its labelled snapshots — and prints, for each scenario, the
complete fetched journal, the owned journal, and the terminal sinks the
directions require: status writes, `aria-busy`, the visible per-fragment text,
history writes, and the failure paragraph.

Run at the head, the V8 scenarios show zero wrong-namespace requests and the
preserved valid ones, and the V9 scenarios show zero requests after a refused
prefix — cold, prewarmed and late. Run at the parent with the head's test file
copied in, the same scenarios show the defect's own journal, which is the
demonstration, not the assumption. Every labelled snapshot of each scenario is
dumped, not the terminal one alone, so prewarmed, walked and late phases are
readable in order.

V11, THE V10 REVIEW: the live harness captured request OWNERSHIP and this dump
threw it away. `FIELDS` was a fourteen-name whitelist that kept the flat
`fetched` list and dropped `requests`, `fragmentIds`, `historyState` and
`replacedStates` — so the packaged log could not reproduce the ownership claim
the package made, and a reader had to rerun the harness to check it. The
whitelist now carries all four, and a name the harness no longer emits is a
hard failure that names itself rather than a silent `null`.

V13, THE V12 REVIEW: the SAME omission recurred one lane later, through the
other whitelist. `NAMES` was a hand-maintained list of scenarios that stopped
at `v11-renderer-order-control`, so the head and parent packaged journals were
byte-identical, carried no V12 scenario at all, and supported none of the
closures the package claimed — while `EVIDENCE-INDEX.md` said they did. A
hand-maintained enumeration of what to prove will fall behind whatever is
proved next, so there is no longer one: **every scenario the test file
declares is dumped, in the order it declares them.** A lane that adds a
scenario cannot forget to add it here, because there is nowhere to add it.
`--only PREFIX` narrows a dump for reading; it never narrows what the package
ships, because the package ships the unfiltered run.

V13 also carries the ownership axes the V12 review required a reviewer to be
able to check without rerunning the harness: the projection that owns each
request, the route as it stood WHEN THE REQUEST WAS MADE, the cache
disposition, and the body it was answered with. A journalled request is by
definition a cache MISS — the page's cache answers before `fetch` is reached —
so a body shown with no row here is the hit, and that absence is the claim.

Usage: journal-dump.py PATH/TO/test_catena_wave_1.py [--only PREFIX]
"""
import importlib.util
import json
import sys

# The sinks the directions require, plus the four the V10 review found
# missing, plus the V13 ownership axes. `requests` is the flat owned journal;
# `ownership` is the same rows carrying the projection, route, cache and body;
# `projectionIds` and `projectionPasses` are the page-level projection census;
# `spineReads` is how many times the raw chapter's own members were asked.
FIELDS = (
    "fetched", "requests", "ownership", "projectionIds", "projectionPasses",
    "spineReads", "fragmentCount", "fragmentIds", "fragmentTexts",
    "sourceLines", "refusal", "refusalCount", "dataStates", "tallyText",
    "statusWrites", "statusText", "busy", "activeElement", "released",
    "errorSections", "hash", "hashWrites", "replaced", "replacedStates",
    "historyState", "failureText",
)

# The facts one ownership row states. Named here so the table below and any
# reader of the JSON agree on what a row is.
ROW_FIELDS = ("seq", "scenario", "route", "projection", "path", "kind",
              "step", "outcome", "cache", "body")

# The narrower shape the harness's flat request journal has carried since V11,
# used when a run predates the ownership rows.
FLAT_FIELDS = ("seq", "path", "kind", "phase", "outcome")

HEADER = """OWNED REQUEST JOURNAL

One line per request, in the order the page made it.

  seq         the request's sequence within the scenario
  route       the route as it stood WHEN THE REQUEST WAS MADE, not when this
              journal was read — a prewarmed body is fetched under one chapter
              and read under another
  projection  the normalized chapter projection whose row carried this
              address; blank where the address is not a fragment text
  kind        what the address holds, derived from the address alone
  step        the step that owned the request; `start` is the bootstrap,
              before any step ran
  outcome     completed, held (parked in flight), released (let go by a later
              step), or failed
  cache       `miss` on every row: a journalled request is one the cache did
              not answer. A body shown with no row here is the hit.
  body        the first bytes of the document the request was answered with,
              enough to name a planted marker
"""


def scenario_names(module, only=""):
    """Every scenario the test file declares, in declaration order."""
    plan = getattr(module, "SCENARIOS", None)
    if not isinstance(plan, list):
        raise SystemExit(
            "the test file declares no SCENARIOS list; this dump derives its "
            "roster from that list precisely so it cannot fall behind it")
    names = [one.get("name") for one in plan if isinstance(one, dict)]
    names = [name for name in names if isinstance(name, str) and name]
    if len(names) != len(plan):
        raise SystemExit(
            "%d of %d scenarios have no name; a nameless scenario cannot be "
            "journalled" % (len(plan) - len(names), len(plan)))
    if len(set(names)) != len(names):
        raise SystemExit("two scenarios share one name; the roster is not a set")
    return [name for name in names if name.startswith(only)]


def project(snapshot, where):
    """The named sinks of one snapshot. A missing name is a hard failure."""
    missing = [name for name in FIELDS if name not in snapshot]
    if missing:
        raise SystemExit(
            "%s: the harness no longer emits %s; this dump would have "
            "silently reported them as null, which is the V10 defect"
            % (where, ", ".join(missing)))
    return {name: snapshot[name] for name in FIELDS}


def rows_of(snapshot):
    """The ownership rows, or the flat journal where a run predates them."""
    owned = snapshot.get("ownership")
    if isinstance(owned, list) and owned:
        return ROW_FIELDS, owned
    return FLAT_FIELDS, snapshot.get("requests") or []


def table(pages, names):
    """The owned journal as text: one line per request, in sequence."""
    lines = HEADER.splitlines()
    lines.append("")
    for name in names:
        page = pages.get(name)
        lines.append("== " + name)
        if page is None:
            lines += ["   (scenario not present in this test file)", ""]
            continue
        if "error" in page:
            lines += ["   ERROR: " + str(page["error"]), ""]
            continue
        for label, snapshot in page.get("snapshots", {}).items():
            passes = snapshot.get("projectionPasses")
            lines.append(
                "   -- snapshot: %s%s" % (
                    label,
                    "" if passes is None
                    else "   (chapters normalized: %s)" % passes))
            fields, rows = rows_of(snapshot)
            if not rows:
                lines.append("      (no request recorded)")
            for row in rows:
                lines.append("      " + " | ".join(
                    str(row.get(field, "?")) for field in fields))
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    argv = sys.argv[1:]
    only = ""
    if "--only" in argv:
        at = argv.index("--only")
        if at + 1 >= len(argv):
            raise SystemExit("--only needs a prefix")
        only = argv[at + 1]
        argv = argv[:at] + argv[at + 2:]
    if len(argv) != 1:
        raise SystemExit(__doc__.strip().splitlines()[-1])
    spec = importlib.util.spec_from_file_location("catena_wave_1", argv[0])
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    names = scenario_names(module, only)
    if not names:
        raise SystemExit("no scenario matches %r" % only)
    pages = module.replayed()
    # EVERY DECLARED SCENARIO MUST HAVE REPLAYED. A roster derived from the
    # file and a run that skipped half of it would be the same omission in a
    # different place.
    absent = [name for name in names if name not in pages]
    if absent:
        raise SystemExit(
            "the harness declared but did not replay: %s" % ", ".join(absent))
    out = {}
    for name in names:
        page = pages[name]
        if "error" in page:
            out[name] = {"error": page["error"]}
        else:
            out[name] = {
                label: project(snapshot, name + "/" + label)
                for label, snapshot in page.get("snapshots", {}).items()}
    print(table(pages, names))
    print()
    print("scenarios journalled: %d" % len(names))
    print()
    print(json.dumps(out, indent=2, sort_keys=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
