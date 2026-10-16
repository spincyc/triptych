"""A printable review preview of the existing browser's act-history geometry.

This is not the accepted LOOM production plate. The canonical DOT owns graph
facts and monochrome styles; the structure projection owns station evidence;
history.js owns layout and connector geometry. No layout is copied here.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import textwrap
import xml.etree.ElementTree as ET


class PreviewError(ValueError):
    """The preview cannot preserve or render the canonical inputs."""


NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)
ATTR = re.compile(r'(\w+)=("(?:[^"\\]|\\.)*")')
ROW = re.compile(r'^  ("(?:[^"\\]|\\.)*")(?: -- ("(?:[^"\\]|\\.)*"))? \[(.*)\];$')
BROWSER_GEOMETRY = r"""
const fs = require('node:fs');
const vm = require('node:vm');
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
const source = input.source;
function section(start, end, throughEnd = true) {
  const at = source.indexOf(start);
  if (at < 0 || source.indexOf(start, at + start.length) >= 0)
    throw Error('Browser geometry extraction contract changed: ' + start);
  const stop = source.indexOf(end, at + start.length);
  if (stop < 0) throw Error('Browser geometry extraction has no end: ' + start);
  return source.slice(at, stop + (throughEnd ? end.length : 0));
}
const model = section('  const M = (function () {', '  }());');
const connector = section('  function connector(from, to) {', '\n  }');
const sizes = section('  const COL = ', '\n\n', false);
if (!sizes.includes('const ROW = ') || !sizes.includes('const PAD = '))
  throw Error('Browser geometry constants contract changed');
const context = vm.createContext({T:{stationKind:{}}});
vm.runInContext(model + '\n' + sizes + '\n' + connector +
  '\nglobalThis.layout=M.layout; globalThis.extent=M.extent;' +
  'globalThis.connector=connector; globalThis.sizes={COL,ROW,PAD};', context);
const positions = context.layout(input.stations);
const {COL,ROW,PAD} = context.sizes;
const nodes = input.stations.map(s => {
  const at = positions.get(s.id);
  return {id:s.id,...at,x:PAD+at.col*COL,y:PAD+at.row*ROW};
});
const edges = input.stations.flatMap(s => (s.parents || []).map(p => ({
  from:p,to:s.id,path:context.connector(positions.get(p),positions.get(s.id))
})));
process.stdout.write(JSON.stringify({nodes,edges,extent:context.extent(positions),sizes:context.sizes}));
"""


def executable(name: str) -> str:
    found = shutil.which(name)
    local = Path.home() / ".local/bin" / name
    if found:
        return found
    if local.is_file() and local.stat().st_mode & 0o111:
        return str(local)
    raise PreviewError(f"print preview requires {name} on PATH or in ~/.local/bin")


def run(args: list[str], **kwargs) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(args, check=True, capture_output=True, text=True,
                              timeout=120, **kwargs)
    except (OSError, subprocess.SubprocessError) as error:
        detail = getattr(error, "stderr", None) or str(error)
        raise PreviewError(f"print preview command failed: {args[0]}: {detail}") from error


def plate_records(source: str) -> tuple[list[dict], list[dict]]:
    """Read only our generator's quoted node/edge records, not arbitrary DOT."""
    nodes, edges = [], []
    for row in source.splitlines():
        if not row.startswith('  "'):
            continue
        match = ROW.fullmatch(row)
        if not match:
            raise PreviewError("canonical plate record format changed")
        first, second, fields = match.groups()
        values = {key: json.loads(value) for key, value in ATTR.findall(fields)}
        if second:
            edges.append({"from": json.loads(first), "to": json.loads(second), **values})
        else:
            nodes.append({"id": json.loads(first), "number": len(nodes) + 1, **values})
    if not nodes:
        raise PreviewError("canonical plate contains no stations")
    return nodes, edges


def browser_geometry(spine: dict, browser_source: Path) -> dict:
    source = browser_source.read_text(encoding="utf-8")
    result = run([executable("node"), "-e", BROWSER_GEOMETRY],
                 input=json.dumps({"source": source, "stations": spine["stations"]}))
    geometry = json.loads(result.stdout)
    geometry["browser_sha256"] = hashlib.sha256(source.encode()).hexdigest()
    return geometry


def element(parent, name, value=None, **attrs):
    node = ET.SubElement(parent, "{" + NS + "}" + name,
                         {k.replace("_", "-"): str(v) for k, v in attrs.items()})
    if value is not None:
        node.text = value
    return node


def text(parent, x, y, value, size=27, weight="normal", anchor="start",
         family="DejaVu Sans"):
    return element(parent, "text", value, x=x, y=y, font_size=size,
                   font_family=family, font_weight=weight, text_anchor=anchor, fill="#171717")


def sheet(width, height, physical_width, physical_height, title):
    svg = ET.Element("{" + NS + "}svg", {"viewBox": f"0 0 {width} {height}",
                     "width": physical_width, "height": physical_height, "role": "img"})
    element(svg, "title", title)
    element(svg, "rect", x=0, y=0, width=width, height=height, fill="white")
    return svg


def write_svg(svg, path):
    ET.ElementTree(svg).write(path, encoding="utf-8", xml_declaration=True)


def render_preview(*, plate_path: Path, spine: dict, out_dir: Path,
                   browser_source: Path, catalogue: dict | None = None) -> dict:
    """Render only accepted stations; research-catalogue candidates add none.

    ``catalogue`` is accepted for the owner's combined dispatch, but cannot
    supply stations or evidence to this act-keyed map. The source spine does.
    """
    del catalogue
    renderer, joiner = executable("rsvg-convert"), executable("pdfunite")
    slice_id = str(spine.get("slice", ""))
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", slice_id):
        raise PreviewError("preview needs a stable slice identifier")
    plate_bytes = plate_path.read_bytes()
    nodes, edge_rows = plate_records(plate_bytes.decode())
    stations = {s["id"]: s for s in spine["stations"]}
    numbers = {n["id"]: n["number"] for n in nodes}
    styles = {n["line"]: n for n in nodes}
    edges = {(e["from"], e["to"]): e for e in edge_rows}
    expected = {(p, s["id"]) for s in stations.values() for p in s.get("parents", [])}
    if len(stations) != len(spine["stations"]) or len(numbers) != len(nodes):
        raise PreviewError("duplicate station identifiers")
    if set(stations) != set(numbers) or expected != set(edges) or len(edges) != len(edge_rows):
        raise PreviewError("plate and structure do not carry the same stations and parent links")
    for node in nodes:
        station = stations[node["id"]]
        if any(str(node.get(key) or "") != str(station.get(key) or "")
               for key in ("date", "date_precision", "line", "title", "station_kind")):
            raise PreviewError("plate and structure station metadata disagree")
    for station in stations.values():
        for reception in station.get("receptions", []):
            if reception.get("from") not in station.get("parents", []):
                raise PreviewError("reception does not name a recorded parent")
    geometry = browser_geometry(spine, browser_source)
    position = {n["id"]: n for n in geometry["nodes"]}
    actual = {(e["from"], e["to"]) for e in geometry["edges"]}
    if (set(position) != set(stations) or len(position) != len(geometry["nodes"])
            or actual != expected or len(actual) != len(geometry["edges"])):
        raise PreviewError("browser geometry lost or invented graph records")
    if len({(n["x"], n["y"]) for n in position.values()}) != len(stations):
        raise PreviewError("browser geometry overlaps station positions")
    if not all(position[a]["x"] < position[b]["x"] for a, b in edges):
        raise PreviewError("browser parent links no longer progress rightward")
    out_dir.mkdir(parents=True, exist_ok=True)
    parts = out_dir / f"{slice_id}-preview-parts"
    parts.mkdir(exist_ok=True)
    title = slice_id.upper().replace("-", " ")
    connected = {key for pair in edges for key in pair}
    isolated_count = len(set(stations) - connected)
    reception_count = sum(len(s.get("receptions", [])) for s in stations.values())
    rows = {}
    for node in geometry["nodes"]:
        rows.setdefault(node["row"], stations[node["id"]]["line"])
    width = max(4200, max(n["x"] for n in position.values()) + 712)
    footer = max(2290, max(n["y"] for n in position.values()) + 454)
    height = footer + 680
    svg = sheet(width, height, f"{width * 594 / 4200:g}mm", f"{height * 420 / 2970:g}mm",
                title + " — printable review preview")
    element(svg, "desc", f"All {len(stations)} stations and {len(edges)} parent links from the canonical plate. "
            "Existing browser layout; review preview, not the LOOM production plate. "
            "Numbers refer to the companion station catalogue. No research candidates are plotted.")
    text(svg, 90, 100, title + " · A MAP OF RECORDED ACTS", 55, "bold")
    text(svg, 90, 160, "PRINTABLE REVIEW PREVIEW / Existing browser layout / " + slice_id, 29, "bold")
    text(svg, 90, 210, f"{len(stations)} stations · {len(styles)} recorded lines · {len(edges)} parent links. "
         "Parallel lines stay separate; crossing alone is no connection.", 28)
    text(svg, 90, 253, "Text coverage is partial. This map carries only the recorded slice, not a complete book or a complete history.", 28)
    group = element(svg, "g", transform="translate(550,320)")
    for edge in geometry["edges"]:
        spec = edges[(edge["from"], edge["to"])]
        received = any(r["from"] == edge["from"] for r in stations[edge["to"]].get("receptions", []))
        attrs = dict(d=edge["path"], fill="none", stroke=spec["color"],
                     stroke_width=12 if received else float(spec["penwidth"]) * 2.5,
                     stroke_linecap="butt", data_from=edge["from"], data_to=edge["to"],
                     data_reception=str(received).lower())
        if spec.get("dasharray") and not received:
            attrs["stroke_dasharray"] = " ".join(str(float(n) * 2.5) for n in spec["dasharray"].split())
        path = element(group, "path", **attrs)
        element(path, "title", f"{numbers[edge['from']]:02d} → {numbers[edge['to']]:02d}: {spec['descent']} ({spec['strength']})")
        if received:
            element(group, "path", d=edge["path"], fill="none", stroke="white", stroke_width=5,
                    aria_hidden="true", data_reception_core="true")
    for node in geometry["nodes"]:
        station = stations[node["id"]]
        mark = element(group, "g", data_station=node["id"])
        element(mark, "title", f"{numbers[node['id']]:02d}. {station['date']}. {station['title']}. {station['station_kind']}")
        if station.get("receptions"):
            element(mark, "circle", cx=node["x"], cy=node["y"], r=17, fill="white",
                    stroke="#171717", stroke_width=3, data_interchange="true")
        element(mark, "circle", cx=node["x"], cy=node["y"], r=10,
                fill="white" if station["station_kind"] == "printed" else "#171717", stroke="#171717", stroke_width=3)
        text(mark, node["x"], node["y"] - 23, f"{numbers[node['id']]:02d}", 28, "bold", "middle")
        date = ("~" if station.get("date_precision") != "day" else "") + station["date"]
        if station.get("via_unrepresented"):
            date += " *"
        text(mark, node["x"], node["y"] + 38, date, 23, anchor="middle")
    for row, line in rows.items():
        text(group, -45, geometry["sizes"]["PAD"] + row * geometry["sizes"]["ROW"] + 8, line, 24, anchor="end")
    element(svg, "line", x1=90, y1=footer, x2=width-90, y2=footer, stroke="#888", stroke_width=2)
    text(svg, 90, footer+60, "READING THE MAP", 31, "bold")
    gaps = "; ".join(f"station {numbers[s['id']]}: " + ", ".join(s["via_unrepresented"])
                     for s in stations.values() if s.get("via_unrepresented"))
    legend = [
        "Filled station: an act is claimed. Open station: a surviving printing; no act is claimed. Each number has evidence in the catalogue.",
        "Horizontal position counts graph steps, not years. Dates carry time; ~ marks a date known only to year or month.",
        "Band texture and grey identify a recorded line. Width records parent-link evidence: stated 3, attributed 2, sequence alone 1 (relative units).",
        f"A parent link is not proof of reception. {reception_count} structured receptions: a hollow band and double-ring receiving station mark only those.",
        ("* Intervening unrepresented acts — " + gaps + ". No intervening station is invented.") if gaps else "This slice records no intervening unrepresented acts.",
        f"{isolated_count} isolated stations remain visible. {len(rows)} drawing tracks accommodate {len(styles)} recorded lines and branches; no roots are joined.",
    ]
    for i, paragraph in enumerate(legend):
        wrapped = textwrap.wrap(paragraph, 145)
        if len(wrapped) > 2:
            raise PreviewError("map legend exceeds preview space; use a larger apparatus design")
        for j, line in enumerate(wrapped):
            text(svg, 90, footer+115+i*66+j*28, line, 25)
    text(svg, 90, footer+545, f"Source: canonical plate and structure projection. Station evidence: {slice_id}-catalogue.pdf.", 25, "bold")
    plate_hash = hashlib.sha256(plate_bytes).hexdigest()
    text(svg, 90, footer+595, "Plate SHA-256: " + plate_hash, 21)
    text(svg, 90, footer+640, "Review artifact only. Geometry comes from the existing browser; this is not an accepted LOOM production rendering.", 23)
    map_path = out_dir / f"{slice_id}-preview.svg"
    write_svg(svg, map_path)
    pages = _catalogue(spine, numbers, edges, parts, title)
    run([renderer, "--format", "pdf", "-o", str(map_path.with_suffix(".pdf")), str(map_path)])
    run([renderer, "--background-color", "white", "-w", "2100", "-o", str(map_path.with_suffix(".png")), str(map_path)])
    pdfs = []
    for page in pages:
        pdf = page.with_suffix(".pdf")
        run([renderer, "--format", "pdf", "-o", str(pdf), str(page)])
        pdfs.append(str(pdf))
    catalogue_path = out_dir / f"{slice_id}-catalogue.pdf"
    run([joiner, *pdfs, str(catalogue_path)])
    (parts / "browser-geometry.json").write_text(json.dumps(geometry, indent=2) + "\n")
    audit = dict(schema="triptych-act-preview/v1", status="review-preview",
                 renderer="existing-browser-geometry", station_count=len(stations), edge_count=len(edges),
                 line_count=len(styles), track_count=len(rows), isolated_count=isolated_count,
                 reception_count=reception_count, catalogue_pages=len(pages),
                 canonical_station_ids_preserved=True, canonical_parent_pairs_preserved=True,
                 plate_sha256=plate_hash, browser_sha256=geometry["browser_sha256"],
                 structure_sha256=hashlib.sha256(json.dumps(spine, sort_keys=True).encode()).hexdigest(),
                 artifacts=[map_path.name, map_path.with_suffix(".pdf").name,
                            map_path.with_suffix(".png").name, catalogue_path.name])
    (out_dir / f"{slice_id}-preview-audit.json").write_text(json.dumps(audit, indent=2) + "\n")
    return audit


def _catalogue(spine, numbers, edges, parts, title):
    pages, page, y = [], None, 0

    def new_page():
        nonlocal page, y
        page = sheet(794, 1123, "210mm", "297mm", title + " — station catalogue")
        pages.append(page)
        text(page, 45, 45, title + " · STATION CATALOGUE", 19, "bold")
        text(page, 45, 70, "Companion to the numbered review map · source evidence reproduced as recorded", 10)
        text(page, 45, 1090, f"Review preview · page {len(pages)} · {spine['slice']} slice", 10)
        y = 105

    def block(value, bold=False):
        nonlocal y
        for line in textwrap.wrap(" ".join(value.split()), width=92, break_on_hyphens=False) or [""]:
            if y > 1045:
                new_page()
            text(page, 45, y, line, 12, "bold" if bold else "normal", family="DejaVu Sans Mono")
            y += 17

    new_page()
    block(f"The numbers identify all {len(numbers)} recorded stations, including printed stations for which no act is claimed. "
          "The graph is not a complete history or a complete text corpus. Evidence status is reproduced, not independently upgraded.")
    y += 20
    for station in spine["stations"]:
        if y > 925:
            new_page()
        block(f"{numbers[station['id']]:02d} | {station['date']} | {station['title']}", True)
        block(f"ID: {station['id']}. Recorded line: {station['line']}. Station kind: {station['station_kind']}. "
              f"Date precision: {station.get('date_precision', 'unstated')}.")
        for label, key in [("Authority", "authority"), ("Instrument", "instrument"), ("Printing", "printing"),
                           ("Act citation status", "act_citation"), ("Citation", "citation")]:
            if station.get(key):
                block(label + ": " + str(station[key]))
        for parent in station.get("parents", []):
            edge = edges[(parent, station["id"])]
            block(f"Parent: {numbers[parent]:02d} ({parent}). Recorded relationship: {edge['descent']}; evidence strength: {edge['strength']}.")
        for reception in station.get("receptions", []):
            block("Documented reception from " + reception["from"] + ": " + reception["kind"])
            for key in ("instrument", "citation", "basis"):
                if reception.get(key):
                    block(key.title() + ": " + reception[key])
        if not station.get("parents"):
            block("Root: no parent is recorded; no common ancestor is invented.")
        if station.get("via_unrepresented"):
            block("Intervening unrepresented acts: " + "; ".join(station["via_unrepresented"]))
        if "effect_established" in station:
            block("Effect established in this record: " + str(station["effect_established"]).lower() + ".")
        y += 20
    paths = []
    for i, page in enumerate(pages, 1):
        path = parts / f"catalogue-{i:02d}.svg"
        write_svg(page, path)
        paths.append(path)
    return paths
