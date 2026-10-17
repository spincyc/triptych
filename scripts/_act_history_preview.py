"""Printable review previews of the shared history browser models.

This is not the accepted LOOM production plate. The canonical DOT owns graph
facts and monochrome styles for legacy act routes. Source projections own
station and chronological stage evidence; history.js owns year positions and
connector geometry. No layout is copied here.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import textwrap
import xml.etree.ElementTree as ET
from urllib.parse import quote, urlsplit, urlunsplit


class PreviewError(ValueError):
    """The preview cannot preserve or render the canonical inputs."""


NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)
ATTR = re.compile(r'(\w+)=("(?:[^"\\]|\\.)*")')
ROW = re.compile(r'^  ("(?:[^"\\]|\\.)*")(?: -- ("(?:[^"\\]|\\.)*"))? \[(.*)\];$')
RTL_RUN = re.compile(r'[\u0590-\u08ff][\u0590-\u08ff\s0-9–—,:;./-]*')
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
  'globalThis.connector=connector; globalThis.sizes={COL,ROW,PAD};' +
  'globalThis.panels=M.panelLayout; globalThis.overview=M.overviewModel; globalThis.network=M.networkLayout; globalThis.networkStyle=M.networkStyle;' +
  'globalThis.stageLayout=M.stageLayout; globalThis.stageStyle=M.stageStyle;', context);
const positions = context.layout(input.stations);
const {COL,ROW,PAD} = context.sizes;
const nodes = input.stations.map(s => {
  const at = positions.get(s.id);
  return {id:s.id,...at,x:PAD+at.col*COL,y:PAD+at.row*ROW};
});
const edges = input.stations.flatMap(s => (s.parents || []).map(p => ({
  from:p,to:s.id,path:context.connector(positions.get(p),positions.get(s.id))
})));
if (typeof context.panels !== 'function') throw Error('Browser panel layout extraction contract changed');
const panels = context.panels(input.stations, input.lines || []);
const overview = input.catalogue ? context.overview(input.catalogue) : {groups:[],relations:[]};
if (input.catalogue && typeof context.network !== 'function') throw Error('Browser network layout extraction contract changed');
const network = input.catalogue ? context.network(input.catalogue) : [];
const network_styles = Object.fromEntries(overview.relations.map(r => [r.kind,context.networkStyle(r.kind)]));
const history = input.catalogue && input.catalogue.stage_history;
if (history && typeof context.stageLayout !== 'function') throw Error('Browser stage layout extraction contract changed');
const chronology = history ? (input.stage_options || [{}]).map(options => context.stageLayout(history, options)) : [];
process.stdout.write(JSON.stringify({nodes,edges,panels,overview,network,network_styles,chronology,extent:context.extent(positions),sizes:context.sizes}));
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


def browser_geometry(spine: dict, browser_source: Path, catalogue: dict | None = None,
                     stage_options: list[dict] | None = None) -> dict:
    source = browser_source.read_text(encoding="utf-8")
    result = run([executable("node"), "-e", BROWSER_GEOMETRY],
                 input=json.dumps({"source": source, "stations": spine["stations"], "lines": spine.get("lines", []),
                                   "catalogue": catalogue, "stage_options": stage_options}))
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
    # Isolate a source-language title from adjacent English date punctuation.
    # Numeric ranges remain left-to-right inside an otherwise RTL quotation.
    def isolate(match):
        run = match.group(0)
        body = run.rstrip(" \t\n–—,:;./-")
        tail = run[len(body):]
        body = re.sub(r'[0-9]+(?:[–—/-][0-9]+)*', lambda number: '\u2066' + number.group(0) + '\u2069', body)
        return '\u2067' + body + '\u2069' + tail
    display = RTL_RUN.sub(isolate, value)
    return element(parent, "text", display, x=x, y=y, font_size=size,
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
                   browser_source: Path, catalogue: dict | None = None, view: str = "auto") -> dict:
    """Render accepted routes and a separately labelled research overview.

    Catalogue relationships never become act parents or station identities.
    The browser owns panel topology; this helper only paginates and labels it.
    """
    if view not in ("auto", "chronology", "legacy"):
        raise PreviewError("preview view must be auto, chronology or legacy")
    history = (catalogue or {}).get("stage_history") if view != "legacy" else None
    if view == "chronology" and history is None:
        raise PreviewError("chronological preview needs stage_history")
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
    stage_requests = _stage_requests(history) if history else None
    geometry = browser_geometry(spine, browser_source, catalogue, stage_requests)
    if history:
        dense = {lane["id"] for model in geometry["chronology"] for lane in model["lanes"]
                 if lane["height"] > 860
                 or len(lane["nodes"]) >= 4 and model["end"] - model["start"] > 500}
        if dense:
            stage_requests = _stage_requests(history, dense)
            geometry = browser_geometry(spine, browser_source, catalogue, stage_requests)
        page_requests = _stage_page_requests(history, geometry["chronology"], stage_requests)
        if page_requests != stage_requests:
            geometry = browser_geometry(spine, browser_source, catalogue, page_requests)
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
    panels = geometry["panels"]
    panel_nodes = [node for panel in panels for node in panel["nodes"]]
    panel_edges = [edge for panel in panels for edge in panel["edges"]]
    if ({node["id"] for node in panel_nodes} != set(stations)
            or len(panel_nodes) != len(stations)
            or {(edge["from"], edge["to"]) for edge in panel_edges} != expected
            or len(panel_edges) != len(expected)):
        raise PreviewError("browser panels lost or invented graph records")
    for panel in panels:
        if len({(n["x"], n["y"]) for n in panel["nodes"]}) != len(panel["nodes"]):
            raise PreviewError("browser panel overlaps station positions")
    plate_hash = hashlib.sha256(plate_bytes).hexdigest()
    graph_row = next((row for row in plate_bytes.decode().splitlines() if row.startswith("  graph [")), "")
    graph_fields = {key: json.loads(value) for key, value in ATTR.findall(graph_row)}
    twin = urlsplit(graph_fields.get("url", "").split(" ")[0])
    catalogue_url = urlunsplit((twin.scheme, twin.netloc, twin.path, "view=catalogue", ""))
    if history is not None:
        return _render_chronology(history, geometry, spine, catalogue, out_dir, parts, plate_hash,
                                  catalogue_url, renderer, joiner, isolated_count)
    detail_pages, station_sheets, panel_sheets = _detail_pages(panels, stations, numbers, edges, styles, slice_id)
    overview_pages = _overview_pages(geometry["overview"], panels, panel_sheets, styles, slice_id,
                                     len(stations), len(edges), isolated_count, reception_count, plate_hash, catalogue_url)
    guide_key = next(page.find("{" + NS + "}title").text.rsplit(" — ", 1)[-1]
                     for page in overview_pages
                     if page.find("{" + NS + "}title").text.startswith("Guide to the dated route sheets"))
    for page in detail_pages:
        _route_legend(page, guide_key)
    network_pages = _network_pages(geometry["network"], geometry["overview"], geometry["network_styles"], slice_id)
    map_pages = network_pages + overview_pages + detail_pages
    map_paths = []
    for i, page in enumerate(map_pages, 1):
        path = parts / f"map-{i:02d}.svg"
        write_svg(page, path)
        map_paths.append(path)
    dimensions = [tuple(float(value) for value in page.get("viewBox").split()) for page in map_pages]
    master_width = max(row[2] for row in dimensions)
    master_height = sum(row[3] for row in dimensions)
    master = sheet(master_width, master_height, f"{master_width * 210 / 794:g}mm", f"{master_height * 297 / 1123:g}mm",
                   title + " — overview and dated route sheets")
    element(master, "desc", "Review preview: research relationships and accepted stations are separate. "
            "All canonical station identities and parent links are preserved. Text coverage is partial.")
    top = 0
    for i, page in enumerate(map_pages):
        group = element(master, "g", transform=f"translate({(master_width - dimensions[i][2]) / 2:g},{top:g})", data_sheet=i + 1)
        top += dimensions[i][3]
        for child in page:
            group.append(copy.deepcopy(child))
    map_path = out_dir / f"{slice_id}-preview.svg"
    write_svg(master, map_path)
    map_pdfs = []
    for path in map_paths:
        pdf = path.with_suffix(".pdf")
        run([renderer, "--format", "pdf", "-o", str(pdf), str(path)])
        map_pdfs.append(str(pdf))
    run([joiner, *map_pdfs, str(map_path.with_suffix(".pdf"))])
    run([renderer, "--background-color", "white", "-w", "1200", "-o",
         str(map_path.with_suffix(".png")), str(map_paths[0])])
    station_url = urlunsplit((twin.scheme, twin.netloc, twin.path, "view=map&slice=" + quote(slice_id), ""))
    pages = _catalogue(spine, numbers, edges, parts, title, station_sheets, station_url)
    pages += _relationship_evidence(geometry["overview"], parts, slice_id, catalogue_url)
    pdfs = []
    for page in pages:
        pdf = page.with_suffix(".pdf")
        run([renderer, "--format", "pdf", "-o", str(pdf), str(page)])
        pdfs.append(str(pdf))
    catalogue_path = out_dir / f"{slice_id}-catalogue.pdf"
    run([joiner, *pdfs, str(catalogue_path)])
    (parts / "browser-geometry.json").write_text(json.dumps(geometry, indent=2) + "\n")
    audit = dict(schema="triptych-act-preview/v1", status="review-preview",
                 renderer="existing-browser-geometry", presentation="dated-line-panels",
                 station_count=len(stations), edge_count=len(edges),
                 line_count=len(styles), track_count=sum(panel["tracks"] for panel in panels),
                 panel_count=len(panels), isolated_count=isolated_count,
                 reception_count=reception_count, catalogue_pages=len(pages), map_pages=len(map_pages),
                 overview_pages=len(network_pages) + len(overview_pages), network_pages=len(network_pages), detail_pages=len(detail_pages),
                 research_relationship_count=len((catalogue or {}).get("relationships", [])),
                 canonical_station_ids_preserved=True, canonical_parent_pairs_preserved=True,
                 plate_sha256=plate_hash, browser_sha256=geometry["browser_sha256"],
                 structure_sha256=hashlib.sha256(json.dumps(spine, sort_keys=True).encode()).hexdigest(),
                 catalogue_sha256=hashlib.sha256(json.dumps(catalogue, sort_keys=True).encode()).hexdigest(),
                 station_sheets=station_sheets,
                 artifacts=[map_path.name, map_path.with_suffix(".pdf").name,
                            map_path.with_suffix(".png").name, catalogue_path.name])
    (out_dir / f"{slice_id}-preview-audit.json").write_text(json.dumps(audit, indent=2) + "\n")
    return audit


def wrapped(parent, x, y, value, *, width=92, size=13, leading=18, weight="normal"):
    lines = textwrap.wrap(" ".join(str(value).split()), width=width, break_on_hyphens=False) or [""]
    for line in lines:
        text(parent, x, y, line, size, weight)
        y += leading
    return y


def _page(title, key, slice_id, subtitle):
    page = sheet(794, 1123, "210mm", "297mm", title + " — " + key)
    text(page, 45, 45, title, 24, "bold")
    wrapped(page, 45, 73, subtitle, width=108, size=11, leading=15)
    element(page, "line", x1=45, y1=1048, x2=749, y2=1048, stroke="#b3b7bb")
    text(page, 45, 1073, "REVIEW PREVIEW · " + slice_id + " · " + key, 11, "bold")
    text(page, 45, 1094, "Read each source's scope and limitations before treating a connection as established.", 10)
    return page


def _detail_pages(panels, stations, numbers, edges, styles, slice_id):
    """Paginate browser coordinates without rebuilding the graph or routing it."""
    scale = .70
    placements, station_sheets, panel_sheets = [], {}, {}
    sheet_index, cursor = 0, 110
    for panel in panels:
        chunks = [panel["nodes"][i:i + 8] for i in range(0, len(panel["nodes"]), 8)]
        for part, members in enumerate(chunks):
            height = 84 + (members[-1]["y"] - members[0]["y"] + 104) * scale
            if cursor + height > 965:
                sheet_index += 1
                cursor = 110
            key = f"D{sheet_index + 1:02d}"
            placements.append((sheet_index, cursor, panel, members, part, len(chunks)))
            panel_sheets.setdefault(panel["line"], [])
            if key not in panel_sheets[panel["line"]]:
                panel_sheets[panel["line"]].append(key)
            for node in members:
                station_sheets[node["id"]] = key
            cursor += height + 14
    pages = [_page("Recorded station routes", f"D{i + 1:02d}", slice_id,
                   "Read each line downward by its printed dates. Separate panels have no shared time axis.")
             for i in range(sheet_index + 1)]
    for page_index, top, panel, members, part, count in placements:
        page = pages[page_index]
        color = styles[panel["line"]]["color"]
        label = f"P{panel['number']:02d} · {panel['label']}"
        if count > 1:
            label += f" · part {part + 1}/{count}"
        element(page, "line", x1=45, y1=top, x2=749, y2=top, stroke=color, stroke_width=4)
        heading_end = wrapped(page, 45, top + 26, label, width=78, size=17, leading=21, weight="bold")
        text(page, 45, heading_end + 2,
             f"{members[0]['date']} to {members[-1]['date']} · {len(members)} of {len(panel['nodes'])} stations on this line", 11)
        origin = heading_end + 26
        offset = members[0]["y"] - 38
        local_ids = {node["id"] for node in members}
        clip_id = f"panel-{panel['number']}-{part}"
        defs = element(page, "defs")
        clip = element(defs, "clipPath", id=clip_id)
        element(clip, "rect", x=0, y=offset, width=1000,
                height=members[-1]["y"] - offset + 54)
        graph = element(page, "g", transform=f"translate(45,{origin - offset * scale:g}) scale({scale})",
                        clip_path=f"url(#{clip_id})")
        for edge in panel["edges"]:
            if edge["to"] not in local_ids:
                continue
            spec = edges[(edge["from"], edge["to"])]
            attrs = dict(d=edge["path"], fill="none", stroke=spec["color"],
                         stroke_width=9 if edge["reception"] else float(spec["penwidth"]) * 2,
                         data_from=edge["from"], data_to=edge["to"],
                         data_reception=str(edge["reception"]).lower())
            if spec.get("dasharray") and not edge["reception"]:
                attrs["stroke_dasharray"] = " ".join(str(float(n) * 2) for n in spec["dasharray"].split())
            path = element(graph, "path", **attrs)
            element(path, "title", f"{edge['fromTitle']} → {edge['toTitle']}: {spec['descent']}")
            if edge["reception"]:
                element(graph, "path", d=edge["path"], fill="none", stroke="white", stroke_width=3,
                        data_reception_core="true")
        for node in members:
            station = stations[node["id"]]
            mark = element(graph, "g", data_station=node["id"])
            if station.get("receptions"):
                element(mark, "circle", cx=node["x"], cy=node["y"], r=14,
                        fill="white", stroke="#171717", stroke_width=2, data_interchange="true")
            element(mark, "circle", cx=node["x"], cy=node["y"], r=8,
                    fill="white" if station["station_kind"] == "printed" else "#171717",
                    stroke="#171717", stroke_width=2)
            label_x = 45 + panel.get("textX", 130) * scale
            label_y = origin + (node["y"] - offset) * scale
            title_end = label_y - 3
            # Print's fixed page margin is narrower than the browser's flowing
            # text column. Rewrap labels only; retain the shared station geometry.
            for line in textwrap.wrap(node["title"], 72, break_on_hyphens=False):
                label = text(page, label_x, title_end, line, 14, "bold")
                label.set("data-label-for", node["id"])
                title_end += 17
            date = ("~" if station.get("date_precision") != "day" else "") + station["date"]
            kind = "surviving printing; no act claimed" if station["station_kind"] == "printed" else "recorded act"
            text(page, label_x, title_end + 2, f"{date} · {kind} · evidence {numbers[node['id']]:02d}", 12)
            refs = [e for e in panel["edges"] if e["to"] == node["id"]
                    and (e["external"] or e["from"] not in local_ids)]
            if refs:
                reference = "; ".join(f"From {e['fromTitle']} [{station_sheets[e['from']]}]" for e in refs)
                wrapped(page, label_x, title_end + 20, reference, width=95, size=10, leading=12)
            elif station.get("via_unrepresented"):
                wrapped(page, label_x, title_end + 20,
                        "Intervening acts not plotted: " + "; ".join(station["via_unrepresented"]),
                        width=95, size=10, leading=12)
        if part + 1 < count:
            next_id = panel["nodes"][(part + 1) * 8]["id"]
            text(page, 45, origin + (members[-1]["y"] - offset + 70) * scale,
                 "Line continues on " + station_sheets[next_id] + " →", 11, "bold")
    return pages, station_sheets, panel_sheets


def _route_legend(page, guide_key):
    for x, fill, label in ((52, "#171717", "Recorded act"), (210, "white", "Printing; no act claimed")):
        element(page, "circle", cx=x, cy=989, r=5, fill=fill, stroke="#171717", stroke_width=1.5)
        text(page, x + 13, 993, label, 10)
    element(page, "circle", cx=443, cy=989, r=8, fill="white", stroke="#171717", stroke_width=1.5)
    element(page, "circle", cx=443, cy=989, r=4, fill="#171717")
    text(page, 459, 993, "Documented cross-line reception", 10)
    text(page, 45, 1024, f"Connected overview: N01 · route index: {guide_key} · evidence numbers: companion catalogue", 10)


def _network_pages(network, overview, styles, slice_id):
    """Render the browser's connected-component geometry at readable sheet sizes."""
    if not network:
        return []
    by_number = {row["number"]: row for row in overview["relations"]}
    represented = [identifier for panel in network for edge in panel["edges"] for identifier in edge["ids"]]
    represented += [by_number[number]["id"] for panel in network for node in panel["nodes"] for number in node["within"]]
    expected = [row["id"] for row in overview["relations"]]
    if sorted(represented) != sorted(expected):
        raise PreviewError("connected overview lost, duplicated or invented research relationships")
    pages, bundles, number = [], [], 0

    def render_panel(page, panel, x, y, scale):
        nonlocal number
        graph = element(page, "g", transform=f"translate({x:g},{y:g}) scale({scale:g})",
                        data_network_component=panel["number"])
        defs = element(graph, "defs")
        for kind, style in styles.items():
            marker = element(defs, "marker", id=f"network-arrow-{panel['number']}-{kind}",
                             viewBox="0 0 10 10", refX=9, refY=5, markerWidth=5, markerHeight=5,
                             orient="auto-start-reverse")
            element(marker, "path", d="M 0 0 L 10 5 L 0 10 Z", fill=style["color"])
        for node in panel["nodes"]:
            if node.get("leader"):
                element(graph, "path", d=node["leader"], fill="none", stroke="#a3acb5", stroke_width=1.5)
        for edge in panel["edges"]:
            number += 1
            key = f"B{number:02d}"
            style = styles[edge["kind"]]
            attrs = dict(d=edge["path"], fill="none", stroke=style["color"], stroke_width=style["width"],
                         data_network_bundle=key, data_relationship_ids=" ".join(edge["ids"]),
                         data_kind=edge["kind"], data_certainty=edge["certainty"])
            if style["dash"]:
                attrs["stroke_dasharray"] = style["dash"]
            if edge["directed"]:
                attrs["marker_end"] = f"url(#network-arrow-{panel['number']}-{edge['kind']})"
            path = element(graph, "path", **attrs)
            element(path, "title", edge["label"])
            bundles.append((key, edge))
        # Place lookup keys on their shared curve, clear of the full group labels.
        occupied = []
        for node in panel["nodes"]:
            width = min(max([len(line) * 14 for line in node["labelLines"]] + [290]) + 16, 355)
            left = node["labelX"] - (width if node["anchor"] == "end" else width / 2 if node["anchor"] == "middle" else 0)
            occupied.append((left-10, node["labelY"]-31, left+width+10,
                             node["labelY"]+len(node["labelLines"])*31+17))
        for key, edge in bundles[-len(panel["edges"]):] if panel["edges"] else []:
            coordinates = [float(value) for value in re.findall(r"-?\d+(?:\.\d+)?", edge["path"])]
            if len(coordinates) != 6:
                raise PreviewError("shared network path format changed")
            ax, ay, mx, my, bx, by = coordinates
            for t in (.5, .4, .6, .3, .7, .2, .8, .1, .9):
                px = (1-t)**2*ax + 2*(1-t)*t*mx + t*t*bx
                py = (1-t)**2*ay + 2*(1-t)*t*my + t*t*by
                bounds = (px-23, py-16, px+23, py+10)
                if not any(bounds[0] < b[2] and bounds[2] > b[0] and bounds[1] < b[3] and bounds[3] > b[1] for b in occupied):
                    break
            occupied.append(bounds)
            element(graph, "rect", x=px-20, y=py-13, width=40, height=20, rx=3, fill="white", fill_opacity=.94)
            text(graph, px, py+2, key, 16, "bold", "middle")
        for node in panel["nodes"]:
            marker = element(graph, "g", data_network_group=node["id"],
                             data_within_relationships=" ".join(by_number[n]["id"] for n in node["within"]))
            element(marker, "circle", cx=node["x"], cy=node["y"], r=13,
                    fill="#263b4d", stroke="white", stroke_width=3)
            lines = node["labelLines"]
            width = max([len(line) * 14 for line in lines] + [290]) + 16
            width = min(width, 355)
            left = node["labelX"] - (width if node["anchor"] == "end" else width / 2 if node["anchor"] == "middle" else 0)
            height = len(lines) * 31 + 26
            element(marker, "rect", x=left-5, y=node["labelY"]-26, width=width+10, height=height+12,
                    fill="white", fill_opacity=.94, rx=4)
            ly = node["labelY"]
            for line in lines:
                text(marker, node["labelX"], ly, line, 26, "bold", node["anchor"])
                ly += 31
            metadata = node["caption"]
            text(marker, node["labelX"], ly, metadata, 20, anchor=node["anchor"])

    large = [panel for panel in network if panel["width"] > 1000]
    small = [panel for panel in network if panel["width"] <= 1000]
    for panel in large:
        key = f"N{len(pages) + 1:02d}"
        page = sheet(2245, 1588, "594mm", "420mm", "Connected research overview — " + key)
        pages.append(page)
        text(page, 55, 62, "EUCHARISTIC BOOKS · CONNECTED RESEARCH OVERVIEW", 40, "bold")
        text(page, 55, 107, f"{len(overview['relations'])} source relationships across {sum(len(p['nodes']) for p in network)} connected groups. "
             "Groups organize sources; they are not acts or editions.", 24)
        text(page, 55, 144, "Conventional radial arrangement, with no time axis. A shared prayer is not proof of whole-book descent or reception.", 22)
        scale = min(2135 / panel["width"], 1220 / panel["height"])
        render_panel(page, panel, (2245 - panel["width"] * scale) / 2, 185, scale)
        x = 55
        for kind, style in sorted(styles.items()):
            element(page, "line", x1=x, y1=1465, x2=x+55, y2=1465, stroke=style["color"],
                    stroke_width=style["width"], stroke_dasharray=style["dash"] or "none")
            text(page, x+65, 1472, style["label"], 21)
            x += 410
        text(page, 55, 1520, "Arrow = directed claim. B keys identify bundles in the following connection key; R keys identify full cited assertions in the detailed views.", 20)
        text(page, 55, 1558, f"{key} · REVIEW PREVIEW · Other connected components follow. Groups without established links remain in the coverage directory.", 20)
    for start in range(0, len(small), 2):
        key = f"N{len(pages) + 1:02d}"
        page = sheet(1123, 1588, "297mm", "420mm", "Further connected components — " + key)
        pages.append(page)
        text(page, 45, 57, "Further connected components", 31, "bold")
        wrapped(page, 45, 94, "These groups have established links within this record. No link to the preceding component is asserted. "
                "An absent connection remains uninvestigated or unestablished here.", width=100, size=17, leading=23)
        for i, panel in enumerate(small[start:start+2]):
            y = 210 + i * 585
            relation_count = len(panel['relations'])
            text(page, 45, y - 20, f"Component {panel['number']} · {relation_count} source relationship{'s' if relation_count != 1 else ''}", 22, "bold")
            render_panel(page, panel, 61, y, 1)
        text(page, 45, 1518, "Kinds and arrow directions use the same key as N01. Within-group references name exact assertions.", 16)
        text(page, 45, 1550, key + " · REVIEW PREVIEW · Relationship details: O sheets; station routes: D sheets.", 16, "bold")
    key_page, y = None, 120
    for key, edge in bundles:
        description = edge["label"]
        lines = textwrap.wrap(description, 95, break_on_hyphens=False)
        if key_page is None or y + len(lines) * 18 + 45 > 1015:
            key_page = _page("Connected overview: connection key", f"N{len(pages) + 1:02d}", slice_id,
                             "Each B label maps a visible network connection to its exact research assertions. These are not act-parent links.")
            pages.append(key_page)
            y = 120
        style = styles[edge["kind"]]
        element(key_page, "line", x1=45, y1=y-4, x2=76, y2=y-4, stroke=style["color"],
                stroke_width=style["width"], stroke_dasharray=style["dash"] or "none")
        text(key_page, 90, y, key + f" · {len(edge['ids'])} assertion(s)", 14, "bold")
        y = wrapped(key_page, 45, y+23, description, width=95, size=12, leading=18) + 22
    for panel in network:
        for node in panel["nodes"]:
            if not node["within"]:
                continue
            descriptions = [f"R{n:02d} · {by_number[n]['kind']} · {by_number[n]['label']}" for n in node["within"]]
            for index, description in enumerate(descriptions):
                lines = textwrap.wrap(description, 95, break_on_hyphens=False)
                if key_page is None or y + len(lines) * 18 + 45 > 1015:
                    key_page = _page("Connected overview: within-group references", f"N{len(pages) + 1:02d}", slice_id,
                                     "These assertions connect distinct source records in one presentation group; they are not self-parent acts.")
                    pages.append(key_page)
                    y = 120
                text(key_page, 45, y, node["label"] + " · within-group assertion", 14, "bold")
                y = wrapped(key_page, 45, y+23, description, width=95, size=12, leading=18) + 22
    return pages


def _overview_pages(overview, panels, panel_sheets, styles, slice_id,
                    station_count, edge_count, isolated_count, reception_count, plate_hash, catalogue_url):
    pages = []
    relations = overview["relations"]
    groups = overview["groups"]
    page = _page("Research relationships: detailed views", "O01", slice_id,
                 "Research relationships are shown separately from recorded acts. Inclusion does not assert current authorization.")
    pages.append(page)
    y = wrapped(page, 45, 120,
                f"{sum(len(group['entries']) for group in groups)} source records in {len(groups)} named record groups; "
                f"{len(relations)} documented research relationships. The dated route sheets carry {station_count} accepted stations, "
                f"{len(panels)} recorded lines and {edge_count} parent links in the {slice_id} slice.", width=91, size=14, leading=20)
    y = wrapped(page, 45, y + 8,
                "Text coverage is partial. Missing connections have not yet been investigated or established in this record. "
                "An undated textual tradition is not a dated edition or a fabricated ancestor station.",
                width=100, size=12, leading=18) + 8
    y = wrapped(page, 45, y, "Source catalogue: " + catalogue_url, width=112, size=10, leading=15) + 18
    for relation in relations:
        left, right, record = relation["from"], relation["to"], relation["record"]
        if not left or not right:
            raise PreviewError("research relationship endpoint is unresolved")
        endpoint_lines = []
        for endpoint in (left, right):
            status = ("Textual reference; shown without a date axis" if endpoint["entity"] else
                      "Recorded edition or reform" if endpoint["record"].get("act_ref") else
                      "Source record; text " + str(endpoint["record"].get("text_status") or "not assessed").replace("-", " "))
            endpoint_lines.append((textwrap.wrap(endpoint["group"], 32),
                                   textwrap.wrap(endpoint["title"], 26 if re.search("[\u0400-\u058f]", endpoint["title"]) else 32),
                                   textwrap.wrap(str(endpoint.get("date") or "Date not established"), 32),
                                   textwrap.wrap(status, 36)))
        box_height = max(sum(len(lines) for lines in column) for column in endpoint_lines) * 16 + 43
        scope = textwrap.wrap(record["scope"], 100)
        height = box_height + 78 + len(scope) * 16
        if y + height > 1015:
            page = _page("Research connections", f"O{len(pages) + 1:02d}", slice_id,
                         "Named source relationships; these connectors do not create act parents or transmit text.")
            pages.append(page)
            y = 120
        text(page, 45, y, f"R{relation['number']:02d} · {relation['label']}", 15, "bold")
        text(page, 45, y + 20, record["kind"].replace("-", " ") + " · " + record["certainty"], 11)
        box_y = y + 34
        midpoint = box_y + box_height / 2
        stroke = "#436a82" if record["certainty"] == "sourced" else "#796248"
        element(page, "path", d=f"M 327 {midpoint:g} L 467 {midpoint:g}",
                fill="none", stroke=stroke, stroke_width=3, stroke_dasharray="5 4",
                data_relationship=relation["id"])
        if record.get("directed"):
            element(page, "path", d=f"M 456 {midpoint - 7:g} L 467 {midpoint:g} L 456 {midpoint + 7:g}",
                    fill="none", stroke=stroke, stroke_width=3)
        else:
            text(page, 397, midpoint - 9, "shared", 10, anchor="middle")
        for x, endpoint, column in zip((45, 467), (left, right), endpoint_lines):
            element(page, "rect", x=x, y=box_y, width=282, height=box_height, rx=5,
                    fill="#f5f8fa", stroke=stroke, stroke_width=1.5,
                    stroke_dasharray="3 3" if endpoint["entity"] else "none")
            ty = box_y + 20
            for index, lines in enumerate(column):
                for line in lines:
                    text(page, x + 12, ty, line, 12 if index != 1 else 13,
                         "bold" if index == 1 else "normal")
                    ty += 16
                ty += 5
        ty = box_y + box_height + 21
        for line in scope:
            text(page, 45, ty, line, 12)
            ty += 16
        text(page, 45, ty + 3, f"Citations, inspection status and limits: companion catalogue, R{relation['number']:02d}.", 10)
        y += height + 20
    if not relations:
        wrapped(page, 45, y, "No research relationships have yet been supplied to this preview. "
                "The route sheets below preserve the accepted act graph without filling those gaps.", width=95, size=13)
    if groups:
        page = _page("Research coverage by named group", f"O{len(pages) + 1:02d}", slice_id,
                     "These source-owned groups organize records; their count is not a census of rites or distinct versions.")
        pages.append(page)
        y = 120
        for group in groups:
            connections = [f"R{r['number']:02d}" for r in relations
                           if group["id"] in (r["from"]["groupId"], r["to"]["groupId"])]
            admitted = sum(bool(row.get("act_ref")) for row in group["entries"])
            summaries = []
            dated = [row["chronology"] for row in group["entries"] if row.get("chronology")]
            if dated:
                summaries.append(f"Dated source bounds: {min(row['start'] for row in dated)}–{max(row['end'] for row in dated)}; "
                                 f"{len(group['entries']) - len(dated)} records unpositioned. Not the lifespan of the tradition.")
            else:
                summaries.append("No source-record dates positioned here; undated traditions acquire no invented date.")
            for field, label in (("acquisition_status", "Acquisition"), ("text_status", "Text")):
                counts = {}
                for row in group["entries"]:
                    value = str(row.get(field) or "unassessed").replace("-", " ")
                    counts[value] = counts.get(value, 0) + 1
                summaries.append(label + ": " + ("; ".join(f"{value} {count}" for value, count in sorted(counts.items()))
                                                  if counts else "not applicable; this group contains no book record"))
            height = 78 + len(textwrap.wrap(group["label"], 77)) * 18 + sum(len(textwrap.wrap(s, 105)) * 15 for s in summaries)
            if y + height > 1020:
                page = _page("Research coverage by named group", f"O{len(pages) + 1:02d}", slice_id,
                             "Records are evidence holdings and research leads, not automatic admissions to the act graph.")
                pages.append(page)
                y = 120
            y = wrapped(page, 45, y, group["label"], width=77, size=15, leading=18, weight="bold")
            text(page, 45, y + 2,
                 f"{admitted} admitted stations · {len(group['entries']) - admitted} other research records · "
                 f"{len(group['entities'])} undated textual traditions", 11)
            y += 21
            for summary in summaries:
                y = wrapped(page, 45, y, summary, width=105, size=11, leading=15)
            y = wrapped(page, 45, y, "Connections: " + (", ".join(connections) if connections else
                        "not yet investigated or established in this record"), width=105, size=11, leading=15)
            group_url = catalogue_url + "#family=" + quote("group:" + group["id"], safe="")
            link = element(page, "a", href=group_url)
            y = wrapped(link, 45, y + 2, group_url, width=115, size=9, leading=13) + 20
    page = _page("Guide to the dated route sheets", f"O{len(pages) + 1:02d}", slice_id,
                 "Every accepted station appears once, with its full title and date. P identifies a line; D identifies its sheets.")
    pages.append(page)
    y = 120
    for panel in panels:
        label = f"P{panel['number']:02d} · {panel['label']}"
        if y > 850:
            page = _page("Guide to the dated route sheets", f"O{len(pages) + 1:02d}", slice_id,
                         "Single-station lines remain visible. A root means that this record has not established its parent.")
            pages.append(page)
            y = 120
        element(page, "line", x1=45, y1=y - 4, x2=74, y2=y - 4,
                stroke=styles[panel["line"]]["color"], stroke_width=4)
        y = wrapped(page, 86, y, label, width=72, size=14, leading=17, weight="bold")
        text(page, 86, y + 1,
             f"{panel['nodes'][0]['date']} – {panel['nodes'][-1]['date']} · {len(panel['nodes'])} stations · "
             + ", ".join(panel_sheets[panel["line"]]), 11)
        y += 31
    if y > 730:
        page = _page("Reading the route notation", f"O{len(pages) + 1:02d}", slice_id,
                     "The map presents the recorded evidence, including its limits.")
        pages.append(page)
        y = 120
    for paragraph in (
        "Filled circle: a recorded act. Open circle: a surviving printing; no act is claimed. "
        "The evidence number points to the companion catalogue; full titles remain on the map.",
        "Spacing counts graph steps, not years. Dates carry time; ~ marks a year or month without a known day. "
        "Panel position never aligns unrelated roots to one historical date.",
        "Band texture identifies a recorded line. Width records parent-link evidence: stated 3, attributed 2, sequence alone 1. "
        "A use-continuity connection records the order of printings of one use, not proof of textual descent.",
        f"{reception_count} structured cross-line receptions: only these receive a hollow band and double-ring station. "
        f"{isolated_count} isolated stations are retained. A crossing without a ring creates no reception.",
        "Branch tracks belong to the same named line. References to another sheet name the source station explicitly; "
        "no unseen ancestor or intervening act is invented.",
    ):
        y = wrapped(page, 45, y, paragraph, width=100, size=12, leading=18) + 13
    wrapped(page, 45, y + 5, "Canonical plate SHA-256: " + plate_hash, width=97, size=10, leading=15)
    return pages


def _relationship_evidence(overview, parts, slice_id, catalogue_url):
    pages, page, y = [], None, 120
    entities = sorted((row for group in overview["groups"] for row in group["entities"]), key=lambda row: row["id"])
    entity_keys = {row["id"]: f"E{index:02d}" for index, row in enumerate(entities, 1)}

    def new_page():
        nonlocal page, y
        page = _page("Research relationship evidence", f"A{len(pages) + 1:02d}", slice_id,
                     "These assertions are research evidence; they create neither act ancestry nor automatic text inheritance.")
        pages.append(page)
        y = 120

    def lines(value):
        return textwrap.wrap(" ".join(str(value).split()), 100, break_on_hyphens=False)

    def record(heading, blocks):
        nonlocal y
        rows = [(line, index == 0) for index, value in enumerate([heading, *blocks]) for line in lines(value)]
        if page is None or (y > 120 and y + len(rows) * 17 > 1020):
            new_page()
        for line, bold in rows:
            if y > 1020:
                new_page()
                for continuation in lines(heading + " — continued"):
                    text(page, 45, y, continuation, 12, "bold")
                    y += 17
                y += 8
            text(page, 45, y, line, 12, "bold" if bold else "normal")
            y += 17
        y += 24

    def citations(evidence_rows):
        result = []
        for evidence in evidence_rows:
            source = evidence["source"]
            result.append("Citation: " + source["title"] + "; " + evidence["locus"])
            result.append("Inspection: " + source["inspection_status"] + ". " + source["inspection"])
            if source.get("url"):
                result.append("Source: " + source["url"])
        return result

    for relation in overview["relations"]:
        row = relation["record"]
        blocks = ["From: " + relation["from"]["title"] + ". To: " + relation["to"]["title"] + ".",
                  "Kind: " + row["kind"] + ". Certainty: " + row["certainty"] + "."]
        for endpoint in (relation["from"], relation["to"]):
            if endpoint["entity"]:
                blocks.append("Context record: " + endpoint["id"] + ". Not admitted here as a dated edition or act. "
                              "Its own evidence and limits appear below at " + entity_keys[endpoint["id"]] + ".")
            else:
                blocks.append("Source catalogue: " + catalogue_url + "#record=" + quote(endpoint["id"], safe=""))
        blocks += [key.title() + ": " + row[key] for key in ("scope", "basis", "limitations")]
        blocks += citations(row["evidence"])
        blocks.append("Record: " + relation["id"])
        record(f"R{relation['number']:02d} · {relation['label']}", blocks)
    for entity in entities:
        blocks = ["Context entity not admitted here as a dated edition or act; dates in its title do not establish a plotted witness."]
        blocks += [key.title() + ": " + entity.get(key, "Not supplied in this record.")
                   for key in ("scope", "basis", "limitations")]
        blocks += citations(entity.get("evidence", []))
        blocks.append("Record: " + entity["id"])
        record(entity_keys[entity["id"]] + " · " + entity["label"], blocks)
    paths = []
    for index, page in enumerate(pages, 1):
        path = parts / f"relationships-{index:02d}.svg"
        write_svg(page, path)
        paths.append(path)
    return paths


def _catalogue(spine, numbers, edges, parts, title, station_sheets=None, station_url=""):
    pages, page, y = [], None, 0

    def new_page():
        nonlocal page, y
        page = sheet(794, 1123, "210mm", "297mm", title + " — station catalogue")
        pages.append(page)
        text(page, 45, 45, title + " · STATION CATALOGUE", 19, "bold")
        text(page, 45, 70, "Companion to the dated route sheets · source evidence reproduced as recorded", 10)
        text(page, 45, 1090, f"Review preview · page {len(pages)} · {spine['slice']} slice", 10)
        y = 105

    def lines(value):
        return textwrap.wrap(" ".join(str(value).split()), width=92, break_on_hyphens=False) or [""]

    def block(value, bold=False, continued=None):
        nonlocal y
        for line in lines(value):
            if y > 1045:
                new_page()
                if continued:
                    text(page, 45, y, continued + " — continued", 12, "bold")
                    y += 24
            text(page, 45, y, line, 12, "bold" if bold else "normal", family="DejaVu Sans Mono")
            y += 17

    new_page()
    block(f"The numbers identify all {len(numbers)} recorded stations, including printed stations for which no act is claimed. "
          "The graph is not a complete history or a complete text corpus. Evidence status is reproduced, not independently upgraded.")
    y += 20
    relation_meaning = {
        "act-states-it": "the cited instrument names the relationship",
        "book-states-it": "the book names the relationship",
        "attributed": "a cited scholarly attribution",
        "use-continuity": "successive printings declaring one use; no textual descent is asserted",
        "line-order": "acts recorded in this order; neither is claimed to name the other",
    }
    for station in spine["stations"]:
        record = []
        def add(value, bold=False):
            record.append((value, bold))
        label = f"{numbers[station['id']]:02d} | {station['date']} | {station['title']}"
        add(label, True)
        add(f"Route sheet: {(station_sheets or {}).get(station['id'], 'unspecified')}. ID: {station['id']}. "
            f"Recorded line: {station['line']}. Station kind: {station['station_kind']}. "
            f"Date precision: {station.get('date_precision', 'unstated')}.")
        if station_url:
            add("Browser station and witness evidence: " + station_url + "#station=" + quote(station["id"], safe=""))
        for field_label, key in [("Authority", "authority"), ("Instrument", "instrument"), ("Printing", "printing"),
                                 ("Act citation status", "act_citation"), ("Citation", "citation")]:
            if station.get(key):
                add(field_label + ": " + str(station[key]))
        for parent in station.get("parents", []):
            edge = edges[(parent, station["id"])]
            meaning = relation_meaning.get(edge["descent"], edge["descent"])
            add(f"Parent: {numbers[parent]:02d} ({parent}). Relationship: {meaning}. "
                f"Source kind: {edge['descent']}; evidence strength: {edge['strength']}.")
        for reception in station.get("receptions", []):
            add("Documented reception from " + reception["from"] + ": " + reception["kind"])
            for key in ("instrument", "citation", "basis"):
                if reception.get(key):
                    add(key.title() + ": " + reception[key])
        if not station.get("parents"):
            add("Root: a parent has not yet been established in this record; no common ancestor is invented.")
        if station.get("via_unrepresented"):
            add("Intervening unrepresented acts: " + "; ".join(station["via_unrepresented"]))
        if "effect_established" in station:
            add("Recorded effect: " + ("this record establishes an effect within its encoded scope."
                if station["effect_established"] else "the effect is not established in the encoded scope; this does not mean the act changed nothing."))
        required_height = sum(len(lines(value)) * 17 for value, _ in record)
        if y > 105 and y + required_height > 1045:
            new_page()
        for value, bold in record:
            block(value, bold, f"Evidence {numbers[station['id']]:02d}")
        y += 20
    paths = []
    for i, page in enumerate(pages, 1):
        path = parts / f"catalogue-{i:02d}.svg"
        write_svg(page, path)
        paths.append(path)
    return paths


def _stage_keys(history):
    """Keys are source-order references, never chronological ranks."""
    return {table: {row["id"]: f"{prefix}{i:03d}" for i, row in enumerate(history.get(table, []), 1)}
            for table, prefix in (("stages", "S"), ("transitions", "T"), ("sources", "C"), ("gaps", "G"))}


def _stage_requests(history, dense_traditions=None):
    """Use explicit dated windows, split only between disjoint date bounds."""
    requests = []
    traditions = history.get("traditions", [])
    default_id = history.get("default_tradition_id")
    default_family = next((row.get("family") for row in traditions if row["id"] == default_id), None)
    if default_family is not None:
        traditions = ([row for row in traditions if row.get("family") == default_family]
                      + [row for row in traditions if row.get("family") != default_family])
    for tradition in traditions:
        dated = sorted((row for row in history.get("stages", []) if row["tradition_id"] == tradition["id"]
                        and row.get("start_year") is not None and row.get("end_year") is not None),
                       key=lambda row: (row["start_year"], row["end_year"]))
        options = {"tradition": tradition["id"], "includeProvisional": True, "width": 1600, "compact": True}
        if not dated:
            requests.append(options)
            continue
        if tradition["id"] not in (dense_traditions or set()):
            start, end = min(row["start_year"] for row in dated), max(row["end_year"] for row in dated)
            padding = max(5, round((end - start) * .04))
            requests.append({**options, "start": start - padding, "end": end + padding})
            continue
        # Overlapping uncertainty intervals cannot be split across sheets as
        # though they were known dates. Connected intervals stay together.
        blocks = []
        for row in dated:
            if not blocks or row["start_year"] > blocks[-1]["end"]:
                blocks.append({"start": row["start_year"], "end": row["end_year"], "count": 1})
            else:
                blocks[-1]["end"] = max(blocks[-1]["end"], row["end_year"])
                blocks[-1]["count"] += 1
        windows = []
        for block in blocks:
            if (not windows or block["end"] - windows[-1]["start"] > 500
                    or windows[-1]["start"] < 1800 <= block["start"]
                    or windows[-1]["start"] >= 1800 and block["end"] - windows[-1]["start"] > 200
                    or windows[-1]["count"] >= 6):
                windows.append(dict(block))
            else:
                windows[-1]["end"] = block["end"]
                windows[-1]["count"] += block["count"]
        for index, window in enumerate(windows):
            padding = max(5, round((window["end"] - window["start"]) * .04))
            start = max(window["start"] - padding, windows[index - 1]["end"] + 1) if index else window["start"] - padding
            end = min(window["end"] + padding, windows[index + 1]["start"] - 1) if index + 1 < len(windows) else window["end"] + padding
            requests.append({**options, "start": start, "end": end})
    return requests or [{"width": 1600, "includeProvisional": True, "compact": True}]


def _stage_outgoing_references(history, stage_id, member_ids, stage_sheets):
    """Expose recorded onward connections even when their arrow is on another sheet."""
    keys = _stage_keys(history)
    return [f"Outgoing: {keys['transitions'][row['id']]} → {keys['stages'][row['to_stage']]} on "
            + "/".join(stage_sheets.get(row["to_stage"], ["undated register"]))
            + f" · {row['kind'].replace('-', ' ')} · {row['evidence_level'].replace('-', ' ')} · {row['status']}."
            for row in history.get("transitions", [])
            if row["from_stage"] == stage_id and row["to_stage"] not in member_ids]


def _stage_detail_blocks(history, members, edges, stage_sheets=None):
    """Same-page source-derived explanations, independent of chart geometry."""
    keys = _stage_keys(history)
    stages = {row["id"]: row for row in history.get("stages", [])}
    member_ids = {node["id"] for node in members}
    blocks = []

    def refs(evidence):
        return "; ".join(dict.fromkeys(keys["sources"][row["source_id"]] + " · " + row["locus"] for row in evidence))

    def block(identifier, heading, values, kind):
        rows = [(line, 16, "bold", 21) for line in textwrap.wrap(heading, 155, break_on_hyphens=False)]
        rows += [(line, 14, "normal", 19) for value in values
                 for line in textwrap.wrap(value, 180, break_on_hyphens=False)]
        blocks.append({"id": identifier, "kind": kind, "rows": rows,
                       "height": sum(row[3] for row in rows) + 15})

    for node in sorted(members, key=lambda node: (node["stage"]["start_year"], node["stage"]["end_year"], node["key"])):
        row = node["stage"]
        block(row["id"], node["key"] + " · " + ", ".join(row.get("components", [])),
              ["Scope: " + row["scope"], "State evidence: " + refs(row.get("evidence", []))]
              + _stage_outgoing_references(history, row["id"], member_ids, stage_sheets or {}), "stage-scope")
    for edge in edges:
        owner = edge["to"] if stages[edge["to"]].get("start_year") is not None else edge["from"]
        if owner not in member_ids:
            continue
        row = edge["transition"]
        heading = (edge["key"] + " · " + edge["fromKey"] + " → " + edge["toKey"] + " · "
                   + row["kind"].replace("-", " ") + " · " + row["evidence_level"].replace("-", " ")
                   + (" · provisional" if row["status"] == "provisional" else ""))
        values = [edge["fromKey"] + " · " + stages[edge["from"]]["date_label"] + " · " + stages[edge["from"]]["label"]
                  + " → " + edge["toKey"] + " · " + stages[edge["to"]]["date_label"] + " · " + stages[edge["to"]]["label"],
                  row["summary"]]
        change = next(iter(row.get("changes", [])), None)
        if change:
            values += ["Before: " + change["before"], "After: " + change["after"]]
            values.append("Compared loci: " + change["locus_before"] + " → " + change["locus_after"])
        if len(row.get("changes", [])) > 1:
            values.append("First component shown; further recorded changes appear under " + edge["key"] + " in the companion.")
        values.append("Evidence: " + refs(row.get("evidence", []) + (change.get("evidence", []) if change else [])))
        if row.get("limitations"):
            values.append("Limits: " + row["limitations"])
        block(row["id"], heading, values, "change-detail")
    return blocks


def _stage_map_pages(history, models, slice_id):
    """Paginate shared label rows; neither dates nor transition paths are rerouted."""
    keys = _stage_keys(history)
    stages = {row["id"]: row for row in history.get("stages", [])}
    traditions = {row["id"]: row for row in history.get("traditions", [])}
    placements, stage_sheets, pages = [], {}, []
    for model in models:
        nodes = [node for lane in model["lanes"] for node in lane["nodes"]]
        rows = []
        for y in sorted({node["y"] for node in nodes}):
            members = [node for node in nodes if node["y"] == y]
            rows.append({"top": y - 80, "bottom": max(node["y"] + 20 + node["cardHeight"] for node in members),
                         "nodes": members})
        bands = []
        for row in rows:
            if not bands:
                bands.append([])
            bands[-1].append(row)
        for part, band in enumerate(bands, 1):
            key = f"H{len(placements) + 1:03d}"
            members = [node for row in band for node in row["nodes"]]
            placements.append({"key": key, "model": model, "nodes": members, "top": band[0]["top"],
                               "bottom": band[-1]["bottom"], "part": part, "parts": len(bands)})
            for node in members:
                stage_sheets.setdefault(node["id"], []).append(key)
    windows = {}
    for place in placements:
        model = place["model"]
        window = (tuple(lane["id"] for lane in model["lanes"]), model["start"], model["end"])
        windows.setdefault(window, []).append(place)
    for window in windows.values():
        for index, place in enumerate(window, 1):
            place.update(part=index, parts=len(window))
    for place in placements:
        model, members, key = place["model"], place["nodes"], place["key"]
        member_ids = {node["id"] for node in members}
        continued = []
        for edge in model["edges"]:
            owner = edge["to"] if stages[edge["to"]].get("start_year") is not None else edge["from"]
            if owner not in member_ids:
                continue
            for endpoint in (edge["from"], edge["to"]):
                if endpoint not in member_ids:
                    continued.append(f"{edge['key']}: {keys['stages'][endpoint]} on "
                                     + "/".join(stage_sheets.get(endpoint, ["undated register"])))
        continuation_lines = textwrap.wrap("Off-sheet endpoints — " + "; ".join(continued), 180) if continued else []
        extra_footer = max(0, len(continuation_lines) - 1) * 18
        detail_blocks = _stage_detail_blocks(history, members, model["edges"], stage_sheets)
        chart_height = max(300, place["bottom"] - place["top"])
        detail_top = 175 + chart_height + 35
        required_height = detail_top + sum(block["height"] for block in detail_blocks) + 175 + extra_footer
        height = (297 if required_height <= 297 * 1600 / 420 else 594) * 1600 / 420
        if required_height > height:
            raise PreviewError("chronology panel exceeds native A2 page; split its shared label rows")
        page = sheet(1600, height, "420mm", f"{height * 420 / 1600:g}mm", "Book states through time — " + key)
        pages.append(page)
        text(page, 42, 48, "Book states through time", 30, "bold")
        text(page, 42, 82, f"{key} · {model['start']}–{model['end']} · years increase left to right · local year scale", 17)
        text(page, 42, 111, "Labels use extra rows for space. Only recorded transitions connect states; empty space asserts no ancestry.", 15)
        lane = next(lane for lane in model["lanes"] if lane["nodes"])
        title_y = wrapped(page, 42, 193, lane["label"], width=18, size=22, leading=28, weight="bold")
        title_y = wrapped(page, 42, title_y + 12, f"Panel {place['part']} of {place['parts']} in this dated window.",
                          width=27, size=14, leading=20)
        gaps = [row for row in history.get("gaps", []) if row["tradition_id"] == lane["id"]]
        if gaps:
            title_y = wrapped(page, 42, title_y + 20,
                              "Recorded gaps: " + ", ".join(keys["gaps"][row["id"]] for row in gaps)
                              + ". Full coverage and missing witnesses: evidence companion.",
                              width=27, size=13, leading=19)
        axis_y, top, bottom = 153, 175, 175 + chart_height
        for tick in model["axis"]["ticks"]:
            element(page, "line", x1=tick["x"], y1=axis_y + 8, x2=tick["x"], y2=bottom,
                    stroke="#dfe5e9", stroke_width=1)
            text(page, tick["x"], axis_y, str(tick["year"]), 16, anchor="middle")
        element(page, "line", x1=model["axis"]["x0"], y1=axis_y + 8,
                x2=model["axis"]["x1"], y2=axis_y + 8, stroke="#596571", stroke_width=1)
        defs = element(page, "defs")
        clip = element(defs, "clipPath", id="stage-band-" + key)
        element(clip, "rect", x=225, y=top, width=1365, height=bottom - top)
        marker = element(defs, "marker", id="stage-arrow-" + key, markerWidth=12, markerHeight=12,
                         viewBox="0 0 12 12", refX=21, refY=6, orient="auto", markerUnits="userSpaceOnUse")
        element(marker, "path", d="M 0 0 L 12 6 L 0 12 Z", fill="#3a5266")
        clip_group = element(page, "g", clip_path="url(#stage-band-" + key + ")")
        chart = element(clip_group, "g", transform=f"translate(0,{top - place['top']:g})")
        edge_key_labels = []
        for edge in model["edges"]:
            # Each transition is drawn on its target sheet, or its dated source
            # sheet if the target itself cannot be positioned.
            target = stages[edge["to"]]
            owner = edge["to"] if target.get("start_year") is not None else edge["from"]
            if owner not in member_ids:
                continue
            style = edge["style"]
            path = element(chart, "path", d=edge["path"], fill="none", stroke="#3a5266",
                           stroke_width=style["width"], marker_end="url(#stage-arrow-" + key + ")",
                           data_transition=edge["id"], data_from_stage=edge["from"], data_to_stage=edge["to"],
                           data_evidence_level=edge["transition"]["evidence_level"],
                           data_transition_kind=edge["transition"]["kind"])
            if style["dash"]:
                path.set("stroke-dasharray", style["dash"])
            if edge.get("keyLabel"):
                edge_key_labels.append((edge["keyLabel"], edge["key"]))
            for endpoint, outside, point in (("from", "fromOutside", "fromPoint"), ("to", "toOutside", "toPoint")):
                if not edge[outside] or not edge.get(point):
                    continue
                at, stage_id = edge[point], edge[endpoint]
                element(chart, "circle", cx=at["x"], cy=at["y"], r=4, fill="white", stroke="#3a5266", stroke_width=1)
                source_stage = stages[stage_id]
                bounds = ("unpositioned" if source_stage.get("start_year") is None else
                          str(source_stage["start_year"]) if source_stage["start_year"] == source_stage["end_year"] else
                          f"{source_stage['start_year']}–{source_stage['end_year']} date bounds")
                if source_stage.get("start_year") is not None and (source_stage["end_year"] < model["start"] or source_stage["start_year"] > model["end"]):
                    bounds += " outside window"
                label = keys["stages"][stage_id] + " · " + bounds
                label += " · " + "/".join(stage_sheets.get(stage_id, ["undated register"]))
                lines = textwrap.wrap(label, 45)
                label_x = at["x"]
                anchor = "middle" if 500 < label_x < 1400 else "start" if label_x <= 500 else "end"
                label_width = max(map(len, lines)) * 6
                label_top, label_bottom = at["y"] - 35 - (len(lines) - 1) * 15, at["y"] - 22
                for other in model["edges"]:
                    key_at = other.get("keyLabel")
                    if not key_at or key_at["y"] < label_top or key_at["y"] - 13 > label_bottom:
                        continue
                    left = label_x - (label_width if anchor == "end" else label_width / 2 if anchor == "middle" else 0)
                    if left <= key_at["x"] + 3 and left + label_width >= key_at["x"] - 43:
                        if anchor == "end":
                            label_x = min(label_x, key_at["x"] - 55)
                        else:
                            anchor, label_x = "start", max(label_x, key_at["x"] + 12)
                for line_index, line in enumerate(lines):
                    text(chart, label_x, at["y"] - 24 - (len(lines) - line_index - 1) * 15,
                         line, 11, "normal", anchor)
        for label, transition_key in edge_key_labels:
            element(chart, "rect", x=label["x"] - 43, y=label["y"] - 13,
                    width=46, height=16, fill="white")
            text(chart, label["x"], label["y"], transition_key, 12, "bold", "end")
        for node in members:
            stage = node["stage"]
            group = element(chart, "g", data_stage=node["id"], data_stage_key=node["key"],
                            data_start_year=stage["start_year"], data_end_year=stage["end_year"],
                            data_status=stage["status"])
            if node["xStart"] != node["xEnd"]:
                element(group, "path", d=f"M {node['xStart']} {node['y']-7} V {node['y']+7} M {node['xStart']} {node['y']} H {node['xEnd']} M {node['xEnd']} {node['y']-7} V {node['y']+7}",
                        fill="none", stroke="#253d50", stroke_width=2, data_date_bounds="uncertainty-not-duration")
            mark = element(group, "circle", cx=node["x"], cy=node["y"], r=7,
                           fill="white" if stage["status"] == "provisional" else "#253d50",
                           stroke="#253d50", stroke_width=2)
            if stage["status"] == "provisional":
                mark.set("stroke-dasharray", "2 2")
            key_on_left = node["x"] > 1500
            text(group, node["x"] + (-14 if key_on_left else 14), node["y"] - 10,
                 node["key"], 14, "bold", "end" if key_on_left else "start")
            element(group, "rect", x=node["labelX"] - 5, y=node["labelY"] - 17,
                    width=node["cardWidth"] + 10, height=node["cardHeight"], fill="white", fill_opacity=".96")
            y = node["labelY"]
            for field, weight, size in (("labelLines", "bold", 16), ("dateLines", "normal", 14),
                                       ("scopeLines", "normal", 14), ("coverageLines", "normal", 14),
                                       ("changeLines", "normal", 14)):
                for line in node.get(field, []):
                    label = text(group, node["labelX"], y, line, size, weight)
                    label.set("data-stage-label", node["id"])
                    y += node["leading"]
        y = detail_top
        element(page, "line", x1=42, y1=y - 20, x2=1558, y2=y - 20, stroke="#a9b5be")
        for block in detail_blocks:
            group = element(page, "g", **{"data_" + block["kind"].replace("-", "_"): block["id"]})
            for line, size, weight, leading in block["rows"]:
                text(group, 42, y, line, size, weight)
                y += leading
            y += 15
        legend_y = height - 115
        for index, line in enumerate(continuation_lines):
            text(page, 42, legend_y - 42 - extra_footer + index * 18, line, 13, "bold")
        element(page, "line", x1=42, y1=legend_y - 20, x2=1558, y2=legend_y - 20, stroke="#9ca6af")
        text(page, 42, legend_y, "● Documented state     ○ Provisional lead     |—●—| Date bounds = uncertainty, not duration of use", 15)
        text(page, 42, legend_y + 26,
             "Transition evidence: solid thick = text collated; solid thin = primary description; dashed = scholarly; dotted = bibliographic or provisional.", 14)
        text(page, 42, legend_y + 52,
             "Arrowheads point to recorded targets. Witness succession proves no revision or continuous use. Full evidence: S/T keys in the companion.", 14)
        text(page, 42, height - 24, f"{key} · REVIEW PREVIEW · Contents at front · Print at native A3/A2 size · No transition grants Git ancestry or text inheritance.", 12)

    # Undated material is readable without inventing a horizontal position.
    unpositioned = [row for row in history.get("stages", []) if row.get("start_year") is None or row.get("end_year") is None]
    page, y = None, 120
    for row in unpositioned:
        blocks = [f"{keys['stages'][row['id']]} · {row['label']}",
                  f"{traditions[row['tradition_id']]['label']} · {row['status']} · text: {row['text_coverage']}",
                  "Date: " + row["date_label"] + ". No dated position asserted.", row["summary"], row["limitations"]]
        blocks += _stage_outgoing_references(history, row["id"], {row["id"]}, stage_sheets)
        rows = [textwrap.wrap(" ".join(value.split()), 92) or [""] for value in blocks]
        required = sum(len(lines) * 17 for lines in rows) + 24
        if page is None or y + required > 1015:
            key = f"H{len(pages) + 1:03d}"
            page = _page("States without a dated position", key, slice_id,
                         "These records have no invented year. Their absence from the year axis is not an assertion of historical isolation.")
            pages.append(page)
            y = 120
        group = element(page, "g", data_unpositioned_stage=row["id"])
        for index, lines in enumerate(rows):
            for line in lines:
                text(group, 45, y, line, 12, "bold" if index == 0 else "normal")
                y += 17
        y += 24
        stage_sheets[row["id"]] = [key]
    if not pages:
        pages.append(_page("Book states through time", "H001", slice_id,
                           "No stage records are positioned by this dataset. This is a research gap, not a claim that no historical states existed."))
    index_pages, index_page, y = [], None, 120
    indexed_traditions = sorted(history.get("traditions", []), key=lambda tradition: min(
        (key for row in history.get("stages", []) if row["tradition_id"] == tradition["id"]
         for key in stage_sheets.get(row["id"], [])), default="ZZZ"))
    for tradition in indexed_traditions:
        members = [row for row in history.get("stages", []) if row["tradition_id"] == tradition["id"]]
        sheets = list(dict.fromkeys(key for row in members for key in stage_sheets.get(row["id"], [])))
        blocks = [tradition["label"], "Sheets: " + (", ".join(sheets) or "No recorded stage"),
                  f"States: {sum(row['status'] == 'documented' for row in members)} documented; "
                  f"{sum(row['status'] == 'provisional' for row in members)} provisional leads."]
        height_needed = sum(len(textwrap.wrap(value, 90)) * 17 for value in blocks) + 24
        if index_page is None or y + height_needed > 1020:
            index_page = _page("Traditions and dated sheets", f"I{len(index_pages) + 1:03d}", slice_id,
                               "Map sheets use native A3 landscape or A2 portrait; do not shrink them to A4. Each window has its own true-year scale. S/T keys locate full evidence in the A4 companion. Counts describe scoped attestations, not complete reconstructed books.")
            index_pages.append(index_page)
            y = 120
        for index, value in enumerate(blocks):
            y = wrapped(index_page, 45, y, value, width=90, size=12, leading=17,
                        weight="bold" if index == 0 else "normal")
        y += 24
    return index_pages + pages, stage_sheets


def _stage_page_requests(history, models, requests):
    """Ask the shared model to retain true-year ports on paginated panels."""
    result = []
    for model, request in zip(models, requests):
        nodes = [node for lane in model["lanes"] for node in lane["nodes"]]
        bands = []
        for y in sorted({node["y"] for node in nodes}):
            members = [node for node in nodes if node["y"] == y]
            bottom = max(node["y"] + 20 + node["cardHeight"] for node in members)
            candidate = (bands[-1]["nodes"] if bands else []) + members
            details = _stage_detail_blocks(history, candidate, model["edges"])
            combined_height = max(300, bottom - (bands[-1]["top"] if bands else y - 80)) + sum(block["height"] for block in details)
            if not bands or combined_height > 1835:
                bands.append({"top": y - 80, "ids": [], "nodes": []})
            bands[-1]["ids"].extend(node["id"] for node in members)
            bands[-1]["nodes"].extend(members)
        if len(bands) > 1:
            result.extend({**request, "stageIds": band["ids"]} for band in bands)
        else:
            result.append(request)
    return result


def _render_chronology(history, geometry, spine, catalogue, out_dir, parts, plate_hash,
                       catalogue_url, renderer, joiner, isolated_count):
    slice_id = spine["slice"]
    map_pages, stage_sheets = _stage_map_pages(history, geometry["chronology"], "eucharistic book states")
    expected = {row["id"] for row in history.get("stages", [])}
    visible = [node.get("data-stage") or node.get("data-unpositioned-stage") for page in map_pages
               for node in page.iter() if node.get("data-stage") or node.get("data-unpositioned-stage")]
    if set(visible) != expected or len(visible) != len(expected):
        raise PreviewError("chronological sheets lost or duplicated stage records")
    expected_transitions = {row["id"] for row in history.get("transitions", [])
                            if any(stage["id"] in (row["from_stage"], row["to_stage"])
                                   and stage.get("start_year") is not None for stage in history.get("stages", []))}
    drawn_transitions = [node.get("data-transition") for page in map_pages for node in page.iter() if node.get("data-transition")]
    if set(drawn_transitions) != expected_transitions or len(drawn_transitions) != len(expected_transitions):
        raise PreviewError("chronological sheets lost or duplicated positioned transition records")
    dimensions = [tuple(float(value) for value in page.get("viewBox").split()) for page in map_pages]
    width, height = max(size[2] for size in dimensions), sum(size[3] for size in dimensions)
    master = sheet(width, height, f"{width * 420 / 1600:g}mm", f"{height * 420 / 1600:g}mm", "Book states through time")
    top, pdfs = 0, []
    for index, page in enumerate(map_pages, 1):
        path = parts / f"chronology-{index:03d}.svg"
        write_svg(page, path)
        run([renderer, "--format", "pdf", "-o", str(path.with_suffix('.pdf')), str(path)])
        pdfs.append(str(path.with_suffix(".pdf")))
        group = element(master, "g", transform=f"translate(0,{top:g})", data_sheet=index)
        for child in page:
            group.append(copy.deepcopy(child))
        top += dimensions[index - 1][3]
    master_path = out_dir / f"{slice_id}-preview.svg"
    write_svg(master, master_path)
    run([joiner, *pdfs, str(master_path.with_suffix(".pdf"))])
    run([renderer, "--background-color", "white", "-w", "1600", "-o", str(master_path.with_suffix(".png")),
         str(parts / "chronology-001.svg")])
    evidence = _stage_evidence(history, parts, "eucharistic book states", stage_sheets, catalogue_url)
    evidence_pdfs = []
    for path in evidence:
        pdf = path.with_suffix(".pdf")
        run([renderer, "--format", "pdf", "-o", str(pdf), str(path)])
        evidence_pdfs.append(str(pdf))
    catalogue_path = out_dir / f"{slice_id}-catalogue.pdf"
    run([joiner, *evidence_pdfs, str(catalogue_path)])
    (parts / "browser-geometry.json").write_text(json.dumps(geometry, indent=2) + "\n")
    audit = {"schema": "triptych-act-preview/v1", "status": "review-preview", "renderer": "existing-browser-geometry",
             "presentation": "chronological-book-stages", "map_pages": len(map_pages), "catalogue_pages": len(evidence),
             "paper_sizes": sorted({page.get("width") + " × " + page.get("height") for page in map_pages}),
             "printing": "Native A3 landscape/A2 portrait map sheets; A4 index and evidence. Do not shrink map sheets to A4.",
             "main_change_text_points": round(14 * 420 / 1600 * 72 / 25.4, 2),
             "stage_count": len(expected), "transition_count": len(history.get("transitions", [])),
             "drawn_transition_count": len(drawn_transitions), "tradition_count": len(history.get("traditions", [])),
             "documented_stages": sum(row["status"] == "documented" for row in history.get("stages", [])),
             "provisional_stages": sum(row["status"] == "provisional" for row in history.get("stages", [])),
             "unpositioned_stages": sum(row.get("start_year") is None for row in history.get("stages", [])),
             "stage_sheets": stage_sheets, "stage_ids_preserved": True, "explicit_transitions_preserved": True,
             "canonical_station_ids_preserved": True, "canonical_parent_pairs_preserved": True,
             "legacy_routes": "Available separately with render_preview(view='legacy'); not stage ancestry.",
             "station_count": len(spine["stations"]), "edge_count": sum(len(s.get("parents", [])) for s in spine["stations"]),
             "isolated_count": isolated_count, "plate_sha256": plate_hash, "browser_sha256": geometry["browser_sha256"],
             "structure_sha256": hashlib.sha256(json.dumps(spine, sort_keys=True).encode()).hexdigest(),
             "catalogue_sha256": hashlib.sha256(json.dumps(catalogue, sort_keys=True).encode()).hexdigest(),
             "stage_history_sha256": hashlib.sha256(json.dumps(history, sort_keys=True).encode()).hexdigest(),
             "artifacts": [master_path.name, master_path.with_suffix(".pdf").name, master_path.with_suffix(".png").name, catalogue_path.name]}
    (out_dir / f"{slice_id}-preview-audit.json").write_text(json.dumps(audit, indent=2) + "\n")
    return audit


def _stage_evidence(history, parts, slice_id, stage_sheets, catalogue_url):
    """Print full recorded claims, with shared citations rather than raw JSON."""
    keys = _stage_keys(history)
    stages = {row["id"]: row for row in history.get("stages", [])}
    traditions = {row["id"]: row for row in history.get("traditions", [])}
    sources = {row["id"]: row for row in history.get("sources", [])}
    pages, page, y = [], None, 120

    def lines(value, width=94):
        return textwrap.wrap(" ".join(str(value).split()), width, break_on_hyphens=False) or [""]

    def new_page():
        nonlocal page, y
        page = _page("Book states and changes: evidence", f"E{len(pages) + 1:03d}", slice_id,
                     "S = stage · T = transition · C = source · G = research gap. Source descriptions are not text collations.")
        pages.append(page)
        y = 120

    def record(heading, blocks):
        nonlocal y
        heading_rows = lines(heading, 83)
        rows = [(value, True) for value in heading_rows]
        rows += [(line, False) for value in blocks for line in lines(value)]
        if page is None or (y > 120 and y + len(rows) * 16 + 20 > 1025):
            new_page()
        # Keep a terminal record identifier with at least two preceding body lines.
        has_record_id = blocks and blocks[-1].startswith(("Tradition record: ", "Stage record: ",
                                                         "Transition record: ", "Source record: "))
        tail_size = min(len(rows) - len(heading_rows), len(lines(blocks[-1])) + 2) if has_record_id else 0
        for index, (line, bold) in enumerate(rows):
            if y > 1020 or (index == len(rows) - tail_size and y + (tail_size - 1) * 16 > 1020):
                new_page()
                for continuation in lines(heading + " — continued", 83):
                    text(page, 45, y, continuation, 12, "bold")
                    y += 16
                y += 8
            text(page, 45, y, line, 12 if bold else 11, "bold" if bold else "normal")
            y += 16
        y += 22

    def evidence(rows, seen=None):
        blocks = []
        seen = set() if seen is None else seen
        for row in rows:
            source_id = row["source_id"]
            if source_id not in sources:
                raise PreviewError("stage evidence refers to a missing source: " + source_id)
            identity = (source_id, row.get("locus", ""), row.get("claim", ""))
            if identity in seen:
                continue
            seen.add(identity)
            source = sources[source_id]
            blocks.append(f"Evidence {keys['sources'][source_id]}: {source['title']}; {row.get('locus', '')}.")
            if row.get("claim"):
                blocks.append("Claim supported: " + row["claim"])
        return blocks

    def field(row, name, label=None):
        value = row.get(name)
        if value is None or value == [] or value == "":
            return []
        return [(label or name.replace("_", " ").capitalize()) + ": "
                + (", ".join(str(item) for item in value) if isinstance(value, list) else str(value))]

    record("How to read this evidence companion", [
        "A stage records an identifiable state of a book or complementary book set. Documented does not mean fully transcribed. "
        "Provisional stages remain research leads and do not count as established states.",
        "Start and end years bound the stage's attestation, publication, approval, effective date or reconstruction. "
        "They never assert how long a rite or book remained in use. Unknown dates remain unpositioned.",
        "Only the transitions explicitly recorded below are drawn. Revision, recension branch, reception and witness succession "
        "are distinct. Witness succession alone does not establish revision, continuous use or historical parentage.",
        "Evidence level is recorded separately from historical parentage. No transition grants Git ancestry or inherits unchecked text.",
        *history.get("limitations", []),
    ])
    for tradition in history.get("traditions", []):
        blocks = field(tradition, "scope") + field(tradition, "coverage_note", "Coverage and limits")
        blocks += ["Stages: " + ", ".join(keys["stages"][row["id"]] for row in history.get("stages", [])
                                         if row["tradition_id"] == tradition["id"])]
        blocks.append("Tradition record: " + tradition["id"])
        record(tradition["label"], blocks)
    for row in history.get("stages", []):
        key = keys["stages"][row["id"]]
        tradition = traditions.get(row["tradition_id"], {})
        blocks = [f"Tradition: {tradition.get('label', row['tradition_id'])}. Chronology sheet: "
                  + ", ".join(stage_sheets.get(row["id"], ["unpositioned"])),
                  f"Date: {row['date_label']}. Date basis: {row['date_kind']}. "
                  + (f"Date bounds: {row['start_year']}–{row['end_year']} (not a duration of use)."
                     if row.get("start_year") is not None else "No dated position is asserted."),
                  f"Status: {row['status']}. Text coverage: {row['text_coverage']}."]
        for name in ("witness_label", "scope", "summary", "components", "reception", "limitations"):
            blocks += field(row, name)
        for witness_id in row.get("witness_ids", []):
            blocks.append("Catalogue witness: " + catalogue_url + "#record=" + quote(witness_id, safe=""))
        blocks += evidence(row.get("evidence", []))
        blocks.append("Stage record: " + row["id"])
        record(key + " · " + row["label"], blocks)
    for row in history.get("transitions", []):
        for endpoint in ("from_stage", "to_stage"):
            if row[endpoint] not in stages:
                raise PreviewError("transition refers to a missing stage: " + row[endpoint])
        from_id, to_id = row["from_stage"], row["to_stage"]
        blocks = [f"From {keys['stages'][from_id]}: {stages[from_id]['label']}. "
                  f"To {keys['stages'][to_id]}: {stages[to_id]['label']}.",
                  f"Kind: {row['kind']}. Status: {row['status']}. Evidence level: {row['evidence_level']}.",
                  "Historical parentage: " + row["historical_parentage"] + ". No Git ancestry or automatic text inheritance."]
        blocks += field(row, "summary", "What changed") + field(row, "components")
        component_evidence = set()
        for change in row.get("changes", []):
            blocks.append("Component: " + change["component"])
            blocks += field(change, "before") + field(change, "locus_before", "Before locus")
            blocks += field(change, "after") + field(change, "locus_after", "After locus")
            blocks += evidence(change.get("evidence", []))
            component_evidence.update((item["source_id"], item.get("locus", ""), item.get("claim", ""))
                                      for item in change.get("evidence", []))
        blocks += evidence(row.get("evidence", []), component_evidence)
        blocks += field(row, "limitations") + field(row, "comparison_ids", "Existing comparisons")
        blocks.append("Transition record: " + row["id"])
        record(keys["transitions"][row["id"]] + " · " + row["kind"].replace("-", " "), blocks)
    for row in history.get("gaps", []):
        blocks = field(row, "period") + field(row, "missing", "Missing evidence")
        blocks += field(row, "next_source", "Next source to inspect") + field(row, "consequence")
        record(keys["gaps"][row["id"]] + " · " + traditions.get(row["tradition_id"], {}).get("label", row["tradition_id"]), blocks)
    for row in history.get("sources", []):
        blocks = []
        for name in ("url", "kind", "status", "inspection", "checked_on", "limitations"):
            blocks += field(row, name)
        blocks.append("Source record: " + row["id"])
        record(keys["sources"][row["id"]] + " · " + row["title"], blocks)
    paths = []
    for index, page in enumerate(pages, 1):
        path = parts / f"stage-evidence-{index:03d}.svg"
        write_svg(page, path)
        paths.append(path)
    return paths
