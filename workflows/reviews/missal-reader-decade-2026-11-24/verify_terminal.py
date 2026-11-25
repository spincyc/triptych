"""Compare the actual terminal Day documents with the calendar's independent appointment plan."""

import argparse
from collections import Counter
from datetime import date
import json
from pathlib import Path
import statistics
import subprocess
import sys
from time import perf_counter

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from lectern.reader_navigation import ReadingNavigation
from lectern.surfaces.day import Day


PLAN = """
const fs = require('node:fs');
const model = require('./src/web/browser/liturgy/assembly-model.js');
const [directory, calendar, first, last] = process.argv.slice(1);
const load = name => JSON.parse(fs.readFileSync(directory + '/structure/' + name + '.json', 'utf8'));
const rubrics = load('rubrics/' + calendar);
const masses = new Map(load('propers/reader/' + calendar).masses.map(mass => [mass.key, mass]));
const years = new Map(), plan = {};
for (let time = Date.parse(first); time <= Date.parse(last); time += 86400000) {
  const date = new Date(time).toISOString().slice(0, 10);
  const year = date.slice(0, 4);
  if (!years.has(year)) years.set(year, load('calendar/' + calendar + '/' + year));
  const branches = model.derive({date, year: years.get(year), rubrics}).options;
  plan[date] = branches.flatMap(branch => branch.readable.flatMap(reading => {
    const mass = masses.get(reading.key);
    if (!mass) throw Error(date + ': unknown formulary ' + reading.key);
    return (mass.forms?.length ? mass.forms : [{id: 'main'}])
      .map(form => [branch.option || null, mass.key, form.id]);
  }));
}
process.stdout.write(JSON.stringify(plan));
"""


class Panel:
    """Capture Textual Content without running the compositor for each document."""
    scroll_y = 0

    def update(self, content):
        self.content = content

    def retitle(self, *_):
        pass

    def scroll_to(self, **_):
        pass


class Capture:
    rubrics = True
    opening = {}

    def __init__(self, calendar):
        self.navigation = ReadingNavigation()
        self.panel = Panel()
        self.calendars = [{"id": calendar, "short": calendar}]

    def query_one(self, *_):
        return self.panel

    def call_after_refresh(self, callback):
        callback()


def open_day(process, calendar, day, options):
    request = {"id": 1, "adapter": "liturgy", "fn": "day", "args": [calendar, day, options]}
    process.stdin.write(json.dumps(request) + "\n")
    process.stdin.flush()
    reply = json.loads(process.stdout.readline())
    if not reply["ok"]:
        raise ValueError(reply["error"])
    return reply["value"]


def significant_runs(event, missal):
    members = [event]
    if event["kind"] == "proper-choice":
        selected = (event.get("selection") or {}).get("option")
        members = [member for option in event["options"] if not missal or option["id"] == selected
                   for member in option["members"]]
    for member in members:
        if member.get("problem") or member.get("placeholder"):
            raise ValueError(f"{event['id']}: {member.get('problem') or 'unrendered placeholder'}")
        for block in member.get("blocks", []):
            if "translation-apparatus-closed" in block.get("classes", []):
                continue
            for run in block["runs"]:
                if {"verse-num", "composed-label"}.isdisjoint(run.get("classes", [])):
                    words = " ".join(run["text"].split())
                    if len(words) >= 30:
                        yield words


def check_roman_creed(events, totals):
    keys = ("credo-in-unum-deum", "et-in-unum-dominum", "et-in-spiritum-sanctum")
    ids = {event["id"] for event in events if event["kind"] == "ordinary-element"}
    if not ids:
        totals["no_ordinary_frame"] += 1
        return
    admitted = ["ordinary-element/oblatio/" + key in ids for key in keys]
    if len(set(admitted)) != 1:
        raise ValueError(f"1962 Creed continuation disagrees with the principal text: {dict(zip(keys, admitted))}")
    totals["creed_included" if admitted[0] else "creed_omitted"] += 1


def inspect_day(process, calendar, day, missal, totals, timings):
    base = {"ordinary": missal, "ordinaryLang": "en", "orations": "en",
            "textDisplay": "latin-and-selected", "bible": "douay-rheims"}
    pending, visited, displayed = [{}], set(), set()
    while pending:
        request = pending.pop()
        identity = tuple(sorted(request.items()))
        if identity in visited:
            continue
        visited.add(identity)
        start = perf_counter()
        view = open_day(process, calendar, day, base | request)
        timings["adapter"].append(1000 * (perf_counter() - start))
        capture = Capture(calendar)
        start = perf_counter()
        Day.show_reading(capture, "#panel", "#text", view, calendar)
        timings["content"].append(1000 * (perf_counter() - start))
        text = " ".join(capture.panel.content.plain.split())
        expected_ids = [(row.get("prefix") or "") + event["id"] for row in view["rows"]
                        for event in row.get("events", [])]
        if expected_ids != [entry[0] for entry in capture.navigation.entries] or view["longDate"] not in text:
            raise ValueError("Contents order or rendered date disagrees with the resolved reading")
        totals["documents"] += 1
        for row in view["rows"]:
            if row.get("failed"):
                raise ValueError(row["failed"])
            territory = {"territory": row["option"]} if row.get("option") else {}
            key = Day.resolved_key(row)
            form = (row.get("resolved") or {}).get("form") or "main"
            chooser = row.get("primaryDayChoice")
            if not request:
                for reading in row["branch"]["readable"]:
                    if reading.get("key") and (reading["key"] != key or chooser):
                        pending.append(territory | {"mass": reading["key"]})
                for choice in row.get("unresolvedChoices", []):
                    if choice["id"] == chooser and not chooser.startswith("proper-form:"):
                        pending.extend(territory | {"mass": option["id"]} for option in choice["options"])
            for named in (row.get("mass") or {}).get("forms", []):
                if key and not request.get("form") and (named["id"] != form or chooser):
                    pending.append(territory | {"mass": key, "form": named["id"]})
            if chooser:
                totals["choice_rows"] += 1
                continue
            appointment = (row.get("option"), key, form)
            if not key or appointment in displayed:
                continue
            displayed.add(appointment)
            standing = (row.get("resolved") or {}).get("standing")
            if standing and standing != "said" and "Standing: " + standing not in text:
                raise ValueError(f"{key}: selected calendar standing is missing")
            if not row["events"] or key != row["mass"]["key"]:
                raise ValueError(f"{key}: missing reading or conflicting source owner")
            if calendar == "roman-1962" and missal:
                check_roman_creed(row["events"], totals)
            for event in row["events"]:
                totals[event["kind"]] += 1
                if any(words not in text for words in significant_runs(event, missal)):
                    raise ValueError(f"{event['id']}: spoken text is absent from the terminal document")
    return displayed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("product_root", type=Path, help="Generated browser data directory containing structure/")
    parser.add_argument("--calendar", choices=("roman-1962", "postconciliar"), required=True)
    parser.add_argument("--mode", choices=("read", "missal"), required=True)
    parser.add_argument("--first", type=date.fromisoformat, default=date(2026, 11, 24))
    parser.add_argument("--last", type=date.fromisoformat, default=date(2036, 11, 23))
    parser.add_argument("--timings", type=Path, help="Optional JSON file for individual adapter and formatter timings in milliseconds")
    args = parser.parse_args()
    if args.first > args.last:
        parser.error("--last must be on or after --first")
    directory = str(args.product_root.resolve())
    plan = json.loads(subprocess.check_output(
        ["node", "-e", PLAN, directory, args.calendar, str(args.first), str(args.last)], cwd=ROOT, text=True))
    counts = Counter()
    timings = {"adapter": [], "content": []}
    missing, extra, errors = [], [], []
    with subprocess.Popen(["node", "scripts/lectern/bridge.js", directory], cwd=ROOT,
                          stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True) as process:
        try:
            for day, expected in plan.items():
                wanted = set(map(tuple, expected))
                try:
                    seen = inspect_day(process, args.calendar, day, args.mode == "missal", counts, timings)
                except (ValueError, KeyError) as error:
                    errors.append({"date": day, "error": str(error)})
                    seen = set()
                counts["expected"] += len(wanted)
                counts["displayed"] += len(seen)
                missing.extend((day, *item) for item in sorted(wanted - seen, key=str))
                extra.extend((day, *item) for item in sorted(seen - wanted, key=str))
        finally:
            process.stdin.close()
    if args.timings:
        args.timings.write_text(json.dumps(timings) + "\n", encoding="utf-8")
    performance = {}
    for name, values in timings.items():
        if values:
            p95 = statistics.quantiles(values, n=100, method="inclusive")[94] if len(values) > 1 else values[0]
            performance[name] = {"median": round(statistics.median(values), 1), "p95": round(p95, 1)}
    print(json.dumps({"calendar": args.calendar, "mode": args.mode, "dates": len(plan), "counts": counts,
                      "missing": missing, "extra": extra, "errors": errors, "milliseconds": performance}, indent=2))
    return bool(missing or extra or errors)


if __name__ == "__main__":
    sys.exit(main())
