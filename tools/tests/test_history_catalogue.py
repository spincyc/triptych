"""Replay the real catalogue controller without opening a sandbox socket.

The small DOM records behavior, not geometry. Real Chromium verification of
keyboard focus, narrow reflow, forced colors, and built-route parity remains a
separate gate; these tests never claim visual acceptance.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
NODE = shutil.which("node")
PAGE = ROOT / "src/web/browser/history/index.html"
SCRIPT = ROOT / "src/web/browser/history/history.js"

HARNESS = r"""
const fs = require('node:fs');
const vm = require('node:vm');
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
const nodes = new Map();
class Element {
  constructor(tag, text = '') {
    this.tagName = tag; this.children = []; this.attrs = {}; this.events = {};
    this._text = text; this.hidden = false; this.disabled = true; this.value = '';
    this.classList = {add: name => { this.className = (this.className || '') + ' ' + name; }};
  }
  set id(id) { this._id = id; nodes.set(id, this); }
  get id() { return this._id; }
  set textContent(text) { this._text = String(text); this.children = []; }
  get textContent() { return this._text + this.children.map(n => n.textContent).join(''); }
  get childNodes() { return this.children; }
  appendChild(child) { child.parent = this; this.children.push(child); return child; }
  setAttribute(k, v) { this.attrs[k] = String(v); }
  removeAttribute(k) { delete this.attrs[k]; }
  addEventListener(k, fn) { this.events[k] = fn; }
  remove() { this.parent.children = this.parent.children.filter(n => n !== this); nodes.delete(this.id); }
  focus() { document.activeElement = this; }
  querySelectorAll(selector) {
    const all = this.children.flatMap(n => [n, ...n.querySelectorAll(selector)]);
    return all.filter(n => selector === '[aria-current]' && n.attrs['aria-current']);
  }
}
const html = fs.readFileSync(input.page, 'utf8');
for (const id of html.matchAll(/id="([^"]+)"/g)) { const e = new Element('div'); e.id = id[1]; }
const document = {getElementById: id => nodes.get(id), createElementNS: (_,tag) => new Element(tag), activeElement: null};
const location = {search: input.search || '?view=catalogue&data=../../../data', hash: input.hash || ''};
const calls = [];
let hashHandler;
const Triptych = {
  stationKind: {}, dataRoot: '../../../data',
  el(tag, cls, text) { const e = new Element(tag, text || ''); e.className = cls; return e; },
  clear(node) { node.textContent = ''; },
  loadJSON: async path => {
    calls.push(path);
    if (input.missing) throw Error('HTTP 404');
    if (path === 'structure/act-history/catalogue.json') return input.data;
    if (input.fragments && Object.hasOwn(input.fragments, path)) return input.fragments[path];
    throw Error('HTTP 404');
  },
  setInlineNotice() {}, doneBootstrapping() {},
  readHash: () => new URLSearchParams(location.hash.replace(/^#/, '')),
  writeHash(pairs) { location.hash = '#' + new URLSearchParams(pairs.filter(p => p[1])).toString(); },
  onHashChange(fn) { hashHandler = fn; }
};
vm.runInNewContext(fs.readFileSync(input.script, 'utf8'), {
  window: {Triptych, location}, document, URL, URLSearchParams, console
});
function all(node) { return [node, ...node.children.flatMap(all)]; }
setImmediate(async () => {
  for (const action of input.actions || []) {
    if (action.do === 'filter') {
      nodes.get('catalogue-family').value = action.family || '';
      nodes.get('catalogue-query').value = action.q || '';
      nodes.get('catalogue-filter').events.submit({preventDefault() {}});
    } else if (action.do === 'hash') {
      location.hash = action.value;
      hashHandler(Triptych.readHash());
    } else if (action.do === 'open') {
      const link = all(nodes.get('catalogue-results')).find(n => n.className === 'catalogue-title');
      link.events.click({preventDefault() {}});
    } else if (action.do === 'back') {
      const button = all(nodes.get('catalogue-detail')).find(n => n.tagName === 'button');
      button.events.click();
    } else if (action.do === 'comparison' || action.do === 'relationship-comparison') {
      const fold = all(nodes.get(action.do === 'comparison' ? 'catalogue-comparison-list' : 'overview-connections')).find(n => (n.className || '').includes('comparison-fold'));
      fold.open = true;
      fold.events.toggle();
      await new Promise(resolve => setImmediate(resolve));
    }
  }
  const result = {};
  for (const id of ['catalogue-results', 'catalogue-status', 'catalogue-detail', 'tally', 'catalogue-limits', 'catalogue-comparison-list', 'history-overview', 'overview-network', 'overview-connections', 'overview-groups']) {
    const node = nodes.get(id);
    result[id] = {text: node.textContent, hidden: node.hidden, attrs: node.attrs,
      links: all(node).filter(n => n.tagName === 'a').map(n => ({text: n.textContent, href: n.href, attrs: n.attrs})),
      tags: all(node).map(n => n.tagName)};
    result[id].texts = all(node).filter(n => n.className === 'held-text comparison-text').map(n => n.textContent);
    result[id].ids = all(node).map(n => n.id).filter(Boolean);
  }
  result.calls = calls;
  result.hash = location.hash;
  result.focus = document.activeElement && document.activeElement.id;
  result.mapHidden = nodes.get('historical-map').hidden;
  result.catalogueHidden = nodes.get('catalogue').hidden;
  result.family = nodes.get('catalogue-family').value;
  result.navigation = nodes.get('history-map-link').href;
  result.overviewNavigation = nodes.get('history-overview-link').href;
  console.log(JSON.stringify(result));
});
"""


MAP_HARNESS = r"""
const fs = require('node:fs'), vm = require('node:vm');
const input = JSON.parse(fs.readFileSync(0,'utf8'));
const source = fs.readFileSync(input.script,'utf8');
class E {
 constructor(tag) { this.tagName=tag; this.children=[]; this.attrs={}; this.style={}; this.events={}; this._text=''; }
 appendChild(n) { this.children.push(n); return n; }
 setAttribute(k,v) { this.attrs[k]=String(v); }
 getAttribute(k) { return this.attrs[k]; }
 addEventListener(k,fn) { this.events[k]=fn; }
 getBoundingClientRect() { return {height:input.expanded ? 190 : 104}; }
 set textContent(v) { this._text=String(v); this.children=[]; }
 get textContent() { return this._text+this.children.map(n=>n.textContent).join(''); }
}
const all = n => [n,...n.children.flatMap(all)];
const map = new E('div');
const T = {stationKind:{PROMULGATED:'promulgated',PRINTED:'printed',UNSTATED:'unstated',
 stated:ss=>ss.every(s=>s.station_kind),of:s=>s.station_kind||'unstated'},
 el:(tag,cls,text)=>{const e=new E(tag); e.className=cls; if(text)e.textContent=text;return e;},
 clear:n=>{n.textContent='';}};
const document = {createElementNS:(_,tag)=>new E(tag),getElementById:()=>new E('div')};
const opened=[];
const context={T,document,map,spine:input.spine,byId:new Map(input.spine.stations.map(s=>[s.id,s])),
 kindsStated:true,changeSummary:()=>'recorded summary',NS:'http://www.w3.org/2000/svg',open:id=>opened.push(id),revealDetail:()=>{},console};
vm.createContext(context);
const mStart=source.indexOf('  const M = (function () {');
const mEnd=source.indexOf('\n  }());',mStart)+'\n  }());'.length;
vm.runInContext(source.slice(mStart,mEnd),context);
function fn(start,end) { vm.runInContext(source.slice(source.indexOf(start),source.indexOf(end,source.indexOf(start))),context); }
fn('  function svg(name, attrs) {','  function nameOf(');
fn('  function receptionsOf(station) {','  const RECEPTION_WORDS');
fn('  function magnitude(station) {','  function draw() {');
fn('  function draw() {','  /* What the count under a station');
vm.runInContext('draw()',context);
const nodes=all(map);
const buttons=nodes.filter(n=>n.tagName==='button' && n.attrs['data-station']);
buttons[0].events.click();
console.log(JSON.stringify({
 labels:buttons.map(n=>({id:n.attrs['data-station'],title:n.children.find(c=>c.className==='route-title-text').textContent,accessible:n.attrs['aria-label']})),
 panels:nodes.filter(n=>n.className==='route-panel').map(n=>n.id),
 edges:nodes.filter(n=>n.tagName==='path' && n.attrs['data-from']).map(n=>n.attrs),
 words:map.textContent,opened,geometry:vm.runInContext('M.panelLayout(spine.stations,spine.lines)',context)
}));
"""


@unittest.skipIf(NODE is None, "node is unavailable")
class RoutePanelControllerTests(unittest.TestCase):
    def drive(self, expanded=False):
        spine = json.loads((ROOT / "src/web/data/structure/act-history/latin-missal.json").read_text())
        request = {"script": str(SCRIPT), "spine": spine, "expanded": expanded}
        run = subprocess.run([NODE, "-e", MAP_HARNESS], input=json.dumps(request), text=True,
                             capture_output=True, cwd=ROOT, timeout=20)
        self.assertEqual(run.returncode, 0, run.stderr)
        return spine, json.loads(run.stdout)

    def test_actual_draw_preserves_full_names_all_parent_pairs_and_one_panel_per_line(self):
        spine, got = self.drive()
        self.assertEqual({r["id"]:r["title"] for r in got["labels"]},
                         {r["id"]:r["title"] for r in spine["stations"]})
        self.assertEqual(set(got["panels"]), {"line-"+r["line"] for r in spine["stations"]})
        self.assertEqual(len(got["panels"]), len(set(got["panels"])))
        self.assertEqual({(e["data-from"],e["data-to"]) for e in got["edges"]},
                         {(p,r["id"]) for r in spine["stations"] for p in r["parents"]})
        self.assertIn("Read dates downward", got["words"])
        self.assertIn("not independent historical origins", got["words"])
        roman_panel = list(dict.fromkeys(row["line"] for row in spine["stations"])).index("typica") + 1
        self.assertIn("· line " + str(roman_panel), got["words"], "cross-panel parents need their derived line locator")
        self.assertEqual(got["opened"], [got["labels"][0]["id"]])

    def test_a_branch_never_passes_through_an_unrelated_station(self):
        _, got = self.drive()
        for panel in got["geometry"]:
            for edge in panel["edges"]:
                coordinates = edge["path"].replace("M", "").replace("L", "").split()
                points = list(zip(map(float, coordinates[::2]), map(float, coordinates[1::2])))
                for node in panel["nodes"]:
                    if node["id"] in (edge["from"], edge["to"]):
                        continue
                    for (x1,y1),(x2,y2) in zip(points,points[1:]):
                        x,y = node["x"],node["y"]
                        within = min(x1,x2) <= x <= max(x1,x2) and min(y1,y2) <= y <= max(y1,y2)
                        on_line = abs((x-x1)*(y2-y1)-(y-y1)*(x2-x1)) < 0.001
                        self.assertFalse(within and on_line,
                          f"{edge['from']} -> {edge['to']} falsely crosses station {node['id']}")

    def test_reflow_expands_station_spacing_without_dropping_labels_or_changing_edges(self):
        _, normal = self.drive()
        _, expanded = self.drive(expanded=True)
        self.assertEqual(normal["labels"], expanded["labels"])
        self.assertEqual([(e["data-from"],e["data-to"]) for e in normal["edges"]],
                         [(e["data-from"],e["data-to"]) for e in expanded["edges"]])
        self.assertNotEqual([e["d"] for e in normal["edges"]], [e["d"] for e in expanded["edges"]])


def entry(identifier="example", **changes):
    row = dict(
        id=identifier, family="Example / use", title="A recorded book", date_label="circa 1500",
        chronology={"start": 1490, "end": 1510, "kind": "witness", "certainty": "approximate"},
        record_kind="printed-witness", evidence_status="candidate", text_status="not-transcribed",
        acquisition_status="scan-held", substantive_status="unestablished",
        origin={"inventory": "example.toml", "table": "candidates", "id": identifier},
        sources=[{"id": "source", "url": "https://example.org/book", "label": "Catalogue", "inspection": "metadata only"}],
        links=[], source_record={"qualification": "No substantive change established", "language": "Latin"},
        act_ref=None,
    )
    row.update(changes)
    return row


def catalogue():
    return dict(schema="triptych-eucharistic-history/v1", entries=[entry(), entry("undated", title="Undated book", chronology=None)],
                text_sets=[{"id": "example-set", "adapter": "example", "status": "configured-not-generated"}],
                limitations=["The record is incomplete."])


def network_geometry(data):
    script = r"""
const fs=require('node:fs'),vm=require('node:vm');
const input=JSON.parse(fs.readFileSync(0,'utf8')),source=fs.readFileSync(input.script,'utf8');
const start=source.indexOf('  const M = (function () {');
const end=source.indexOf('\n  }());',start)+'\n  }());'.length;
const context={T:{stationKind:{}},data:input.data}; vm.createContext(context);
vm.runInContext(source.slice(start,end),context);
process.stdout.write(JSON.stringify(vm.runInContext('M.networkLayout(data)',context)));
"""
    run = subprocess.run([NODE, "-e", script], input=json.dumps({"script": str(SCRIPT), "data": data}),
                         text=True, capture_output=True, check=True)
    return json.loads(run.stdout)


def comparison_fixture():
    """Constructed wording tests presentation, never historical evidence."""
    declared = {"id": "constructed-witness-pair", "projection_path": "comparisons/constructed-witness-pair.json",
                "apparatus_caveat": "The apparatus attests another reading; this comparison does not date its introduction.",
                "left": {"text_set": "left", "unit_ids": ["left-1"]},
                "right": {"text_set": "right", "unit_ids": ["right-1", "right-2"]}}
    payload = {"schema": "triptych-eucharistic-witness-comparison/v1", "id": declared["id"],
               "kind": "same-prayer-witness-comparison", "membership_status": "established",
               "basis": "Explicitly aligned source members.", "apparatus_caveat": declared["apparatus_caveat"],
               "historical_ancestry_claimed": False, "historical_act_claimed": False, "introduction_date_inferred": False,
               "sources": [], "limitations": ["Constructed comparison, not history."],
               "unified_diff": "--- left\n+++ right\n-First wording.\n+Second wording.\n"}
    for name, text in (("left", "First wording."), ("right", "Second wording.")):
        payload[name] = {"text_set": name, "title": name + " witness", "target_date": "1915" if name == "left" else "1861",
                         "witness_date": "ninth century" if name == "left" else "1861",
                         "join_rule": "insert-one-space-between-exact-source-bodies", "joined_source_text": text,
                         "members": [{"unit_id": identifier, "source_id": "source." + identifier,
                                      "source_artifact_id": "artifact." + name, "text_edition_id": "edition." + name,
                                      "source_text": text, "language": "la", "publication": {"status": "permitted", "basis": "public-domain"}}
                                     for identifier in declared[name]["unit_ids"]]}
    data = catalogue()
    data["comparisons"] = [declared]
    return data, {"structure/act-history/" + declared["projection_path"]: payload}


@unittest.skipIf(NODE is None, "node is unavailable")
class CatalogueControllerTests(unittest.TestCase):
    def drive(self, data=None, **options):
        request = {"data": catalogue() if data is None else data, "page": str(PAGE), "script": str(SCRIPT), **options}
        run = subprocess.run([NODE, "-e", HARNESS], input=json.dumps(request), text=True,
                             capture_output=True, cwd=ROOT, timeout=20)
        self.assertEqual(run.returncode, 0, run.stderr)
        return json.loads(run.stdout)

    def test_catalogue_fetches_only_its_projection_and_preserves_date_uncertainty(self):
        got = self.drive()
        self.assertEqual(got["calls"], ["structure/act-history/catalogue.json"])
        self.assertTrue(got["mapHidden"])
        self.assertFalse(got["catalogueHidden"])
        self.assertIn("Undated or unresolved (1)", got["catalogue-results"]["text"])
        self.assertIn("circa 1500", got["catalogue-results"]["text"])
        self.assertNotIn("svg", got["catalogue-results"]["tags"])
        self.assertIn("not a count of complete books", got["tally"]["text"])
        self.assertIn("configured-not-generated", got["catalogue-limits"]["text"])

    def test_filters_search_and_back_restore_shareable_selection(self):
        got = self.drive(actions=[{"do": "filter", "family": "Example / use", "q": "undated"}, {"do": "open"}])
        self.assertIn("1 of 2", got["catalogue-status"]["text"])
        self.assertIn("record=undated", got["hash"])
        self.assertEqual(got["focus"], "catalogue-detail")
        self.assertIn("No accepted act-history station", got["catalogue-detail"]["text"])
        got = self.drive(actions=[{"do": "filter", "q": "absent"}, {"do": "hash", "value": "#record=example"}])
        self.assertIn("2 of 2", got["catalogue-status"]["text"])
        self.assertIn("A recorded book", got["catalogue-detail"]["text"])
        got = self.drive(actions=[{"do": "open"}, {"do": "back"}])
        self.assertEqual(got["focus"], "catalogue-entry-example")

    def test_source_metadata_acquisition_and_station_link_remain_distinct(self):
        data = catalogue()
        data["entries"][0]["act_ref"] = {"slice": "latin-missal", "station_id": "example-1500"}
        got = self.drive(data, hash="#record=example")
        text = got["catalogue-detail"]["text"]
        for term in ["scan-held", "not-transcribed", "unestablished", "metadata only", "No substantive change established", "example.toml"]:
            self.assertIn(term, text)
        target = next(link["href"] for link in got["catalogue-detail"]["links"] if "station" in link["text"])
        self.assertIn("view=map", target)
        self.assertIn("slice=latin-missal#station=example-1500", target)
        self.assertIn("data=", target)

    def test_unknown_filters_and_records_are_explicit_and_do_not_broaden(self):
        got = self.drive(hash="#family=Unknown&record=missing")
        self.assertIn("0 of 2", got["catalogue-status"]["text"])
        self.assertEqual(got["family"], "Unknown")
        self.assertIn("not in the catalogue: missing", got["catalogue-detail"]["text"])
        got = self.drive(hash="#q=undated&record=example")
        self.assertIn("outside the current filters", got["catalogue-detail"]["text"])

    def test_missing_and_malformed_projection_fail_closed(self):
        for options in ({"missing": True}, {"data": {}}, {"data": {**catalogue(), "entries": [None]}}):
            with self.subTest(options=options):
                got = self.drive(**options)
                self.assertIn("unavailable", got["catalogue-status"]["text"])
                self.assertEqual(got["catalogue-results"]["attrs"]["aria-busy"], "false")
                self.assertIn("Reload", got["catalogue-results"]["text"])
        for invalid in [{"start": "1500", "end": 1501}, {"start": 1600, "end": 1500}]:
            data = catalogue()
            data["entries"][0]["chronology"] = invalid
            self.assertIn("unavailable", self.drive(data)["catalogue-status"]["text"])

    def test_untrusted_text_and_source_urls_never_become_markup_or_executable_links(self):
        data = catalogue()
        data["entries"][0]["title"] = '<img src=x onerror="alert(1)">'
        data["entries"][0]["sources"][0]["url"] = "javascript:alert(1)"
        data["entries"][0]["links"] = [{"label": "private", "url": "https://user:secret@example.org"},
                                       {"label": "local", "url": "file:///etc/passwd"}]
        got = self.drive(data, hash="#record=example")
        self.assertIn("<img", got["catalogue-detail"]["text"])
        self.assertNotIn("img", got["catalogue-detail"]["tags"])
        self.assertEqual(got["catalogue-detail"]["links"], [])

    def relationship_fixture(self):
        data, fragments = comparison_fixture()
        group = {"id": "example-group", "label": "Example tradition and historical uses"}
        data["presentation_groups"] = [group]
        data["entries"][0]["presentation_group"] = group
        data["entries"][1]["presentation_group"] = group
        data["entries"][1]["family"] = "source-alias"
        evidence = [{"source_id": "example-source", "locus": "Book I, chapter 2",
                     "source": {"id": "example-source", "title": "An identified primary source",
                                "url": "https://example.org/evidence", "inspection_status": "inspected",
                                "inspection": "Constructed fixture; no historical assertion."}}]
        data["relationship_entities"] = [{"id": "fixture:entity:donor", "label": "An undated textual tradition",
          "kind": "textual-tradition", "family": "Example / use", "chronology": None,
          "presentation_group": group, "evidence": evidence}]
        data["relationships"] = [{"id": "fixture:borrowing", "kind": "borrowing", "label": "A bounded borrowing claim",
          "from": "fixture:entity:donor", "to": "example", "directed": True, "certainty": "sourced",
          "scope": "Only the named prayer.", "basis": "The cited account states this borrowing.",
          "limitations": "The donor edition is not established.", "evidence": evidence,
          "git_ancestry": False, "text_inheritance": False,
          "comparison_links": [{"id": data["comparisons"][0]["id"],
                                "projection_path": data["comparisons"][0]["projection_path"]}]}]
        return data, fragments

    def test_overview_shows_typed_connection_evidence_and_undated_donor_without_admitting_station(self):
        data, fragments = self.relationship_fixture()
        got = self.drive(data, search="?view=overview&data=fixture", fragments=fragments)
        self.assertEqual(got["calls"], ["structure/act-history/catalogue.json"])
        self.assertFalse(got["history-overview"]["hidden"])
        text = got["overview-connections"]["text"]
        for term in ["Borrowing", "sourced", "Only the named prayer", "donor edition is not established",
                     "Book I, chapter 2", "Source inspection: inspected", "no dated witness plotted",
                     "does not create a historical station", "linked text comparison"]:
            self.assertIn(term, text)
        links = got["overview-connections"]["links"]
        self.assertTrue(any("record=example" in link["href"] for link in links))
        self.assertFalse(any("station=" in link["href"] for link in links))
        self.assertIn("2 catalogue records", got["overview-groups"]["text"])
        self.assertIn("1 undated textual-tradition references", got["overview-groups"]["text"])
        self.assertIn("not a census of rites", got["tally"]["text"])
        loaded = self.drive(data, search="?view=overview", fragments=fragments,
                            actions=[{"do": "relationship-comparison"}])
        self.assertEqual(loaded["calls"], ["structure/act-history/catalogue.json", *fragments])
        self.assertIn("First wording.", loaded["overview-connections"]["text"])

    def test_connected_network_retains_triangle_local_links_direction_and_uncertainty(self):
        data, _ = self.relationship_fixture()
        groups = [{"id": name, "label": "Full name of " + name} for name in ["second", "third", "unassessed"]]
        data["presentation_groups"].extend(groups)
        data["entries"].extend(entry(g["id"], presentation_group=g) for g in groups)
        original = data["relationships"][0]
        data["relationships"].extend([
            {**original, "id": "fixture:a-b", "to": "second", "certainty": "attributed"},
            {**original, "id": "fixture:b-c", "from": "second", "to": "third"},
            {**original, "id": "fixture:c-a", "from": "third", "to": "example", "kind": "shared-text", "directed": False},
        ])
        panels = network_geometry(data)
        self.assertEqual(len(panels), 1)
        self.assertEqual({n["id"] for n in panels[0]["nodes"]}, {"example-group", "second", "third"})
        self.assertEqual({identifier for e in panels[0]["edges"] for identifier in e["ids"]},
                         {"fixture:a-b", "fixture:b-c", "fixture:c-a"})
        self.assertEqual([n for node in panels[0]["nodes"] for n in node["within"]], [1])
        self.assertEqual(panels[0]["relations"], [1, 2, 3, 4])
        self.assertTrue(all(e["path"].startswith("M ") for e in panels[0]["edges"]))
        attributed = next(e for e in panels[0]["edges"] if e["ids"] == ["fixture:a-b"])
        self.assertEqual(attributed["certainty"], "attributed")
        self.assertTrue(attributed["directed"])
        self.assertFalse(next(e for e in panels[0]["edges"] if e["kind"] == "shared-text")["directed"])
        got = self.drive(data, search="?view=overview")
        self.assertIn("svg", got["overview-network"]["tags"])
        self.assertIn("Full name of second", got["overview-network"]["text"])
        self.assertIn("Positions show connections, not dates", got["overview-network"]["text"])
        self.assertIn("R03", got["overview-network"]["text"])
        self.assertIn("Full name of unassessed", got["overview-groups"]["text"])

    def test_network_group_link_opens_all_candidates_in_qualified_date_order(self):
        data, _ = self.relationship_fixture()
        group = data["presentation_groups"][0]
        data["entries"].append(entry("earlier", title="Earlier candidate", date_label="perhaps 1200–1250",
            presentation_group=group, chronology={"start":1200,"end":1250,"kind":"witness","certainty":"uncertain"}))
        overview = self.drive(data, search="?view=overview&data=fixture")
        link = next(link for link in overview["overview-network"]["links"] if "family=group" in link["attrs"].get("href", ""))
        url = link["attrs"]["href"]
        self.assertIn("view=catalogue",url)
        self.assertIn("data=fixture",url)
        got = self.drive(data, hash="#"+url.split("#",1)[1])
        titles = [link["text"] for link in got["catalogue-results"]["links"]]
        self.assertEqual(titles,["Earlier candidate","A recorded book","Undated book"])
        for term in ["Historical book candidate","perhaps 1200–1250","uncertain","scan-held","not-transcribed","do not imply descent"]:
            self.assertIn(term,got["catalogue-results"]["text"])

    def test_opening_record_from_overview_does_not_duplicate_relationship_anchors(self):
        data, _ = self.relationship_fixture()
        got = self.drive(data, search="?view=overview", actions=[{"do":"open"}])
        self.assertIn("research-R01",got["overview-connections"]["ids"])
        self.assertNotIn("research-R01",got["catalogue-detail"]["ids"])

    def test_declared_group_filter_collects_aliases_and_preserves_legacy_family_filter(self):
        data, _ = self.relationship_fixture()
        grouped = self.drive(data, hash="#family=group%3Aexample-group")
        self.assertIn("2 of 2", grouped["catalogue-status"]["text"])
        data["entries"][1]["family"] = "example-group"
        collided = self.drive(data, hash="#family=example-group")
        self.assertIn("1 of 2", collided["catalogue-status"]["text"])
        data["entries"][1]["family"] = "source-alias"
        legacy = self.drive(data, hash="#family=source-alias")
        self.assertIn("1 of 2", legacy["catalogue-status"]["text"])
        self.assertIn("Undated book", legacy["catalogue-results"]["text"])
        searched = self.drive(data, hash="#q=historical+uses")
        self.assertIn("2 of 2", searched["catalogue-status"]["text"])
        record = self.drive(data, hash="#record=example")
        self.assertIn("Recorded research connections", record["catalogue-detail"]["text"])
        self.assertIn("Book I, chapter 2", record["catalogue-detail"]["text"])

    def test_missing_connection_does_not_claim_historical_isolation(self):
        got = self.drive(search="?view=overview", hash="#record=example")
        self.assertIn("not yet been investigated or established", got["overview-connections"]["text"])
        self.assertIn("not yet investigated or established", got["overview-groups"]["text"])
        self.assertIn("does not establish historical isolation", got["catalogue-detail"]["text"])

    def test_relationship_endpoint_or_ancestry_mismatch_fails_closed(self):
        for change in [{"from": "missing"}, {"kind": "guess"}, {"git_ancestry": True},
                       {"text_inheritance": True}, {"directed": False}, {"certainty": "certain"}, {"evidence": []},
                       {"comparison_links": [{"id": "x", "projection_path": "../../private.json"}]}]:
            data, _ = self.relationship_fixture()
            data["relationships"][0].update(change)
            with self.subTest(change=change):
                got = self.drive(data, search="?view=overview")
                self.assertIn("unavailable", got["catalogue-status"]["text"])
                self.assertEqual(got["overview-connections"]["text"], "")

    def test_generated_catalogue_obeys_the_browser_contract_when_present(self):
        path = ROOT / "src/web/data/structure/act-history/catalogue.json"
        if not path.exists():
            self.skipTest("catalogue projection has not been generated")
        data = json.loads(path.read_text())
        got = self.drive(data)
        self.assertIn(f'{len(data["entries"])} of {len(data["entries"])}', got["catalogue-status"]["text"])

    def test_comparison_fetch_is_lazy_and_displays_exact_text_and_owning_diff(self):
        data, fragments = comparison_fixture()
        unopened = self.drive(data, fragments=fragments)
        self.assertEqual(unopened["calls"], ["structure/act-history/catalogue.json"])
        self.assertIn("does not date its introduction", unopened["catalogue-comparison-list"]["text"])
        got = self.drive(data, fragments=fragments, actions=[{"do": "comparison"}, {"do": "comparison"}])
        self.assertEqual(got["calls"], ["structure/act-history/catalogue.json", *fragments])
        self.assertEqual(got["catalogue-comparison-list"]["texts"], ["First wording.", "Second wording."])
        for term in ["--- left\n+++ right", "ninth century", "1915", "1861", "source.left-1", "source.right-2",
                     "2 source units", "Publication basis", "does not date its introduction"]:
            self.assertIn(term, got["catalogue-comparison-list"]["text"])
        self.assertNotIn("svg", got["catalogue-comparison-list"]["tags"])

    def test_parallel_function_comparison_does_not_claim_same_composition(self):
        data, fragments = comparison_fixture()
        payload = next(iter(fragments.values()))
        payload["kind"] = "parallel-liturgical-unit-comparison"
        payload["identity_claim"] = "parallel-function-not-same-composition"
        data["comparisons"][0]["kind"] = payload["kind"]
        got = self.drive(data, fragments=fragments, actions=[{"do": "comparison"}])
        self.assertIn("Parallel liturgical function; different compositions", got["catalogue-comparison-list"]["text"])
        self.assertIn("not a same-prayer revision", got["catalogue-comparison-list"]["text"])
        payload["identity_claim"] = "same-prayer-witnesses"
        refused = self.drive(data, fragments=fragments, actions=[{"do": "comparison"}])
        self.assertEqual(refused["catalogue-comparison-list"]["texts"], [])

    def test_comparison_errors_do_not_replace_catalogue_or_leak_mismatched_text(self):
        data, fragments = comparison_fixture()
        missing = self.drive(data, actions=[{"do": "comparison"}])
        self.assertIn("HTTP 404", missing["catalogue-comparison-list"]["text"])
        self.assertIn("2 of 2", missing["catalogue-status"]["text"])
        payload = next(iter(fragments.values()))
        payload["right"]["members"].reverse()
        got = self.drive(data, fragments=fragments, actions=[{"do": "comparison"}])
        self.assertIn("does not match", got["catalogue-comparison-list"]["text"])
        self.assertEqual(got["catalogue-comparison-list"]["texts"], [])
        data["comparisons"][0]["projection_path"] = "../../private.json"
        got = self.drive(data, fragments=fragments)
        self.assertEqual(got["calls"], ["structure/act-history/catalogue.json"])
        self.assertIn("invalid metadata", got["catalogue-comparison-list"]["text"])

    def test_comparison_text_and_diff_are_text_nodes(self):
        data, fragments = comparison_fixture()
        payload = next(iter(fragments.values()))
        payload["left"]["joined_source_text"] = "<img onerror=alert(1)>"
        payload["unified_diff"] = "<script>alert(1)</script>"
        got = self.drive(data, fragments=fragments, actions=[{"do": "comparison"}])
        self.assertIn("<script>", got["catalogue-comparison-list"]["text"])
        self.assertNotIn("script", got["catalogue-comparison-list"]["tags"])
        self.assertNotIn("img", got["catalogue-comparison-list"]["tags"])

    def test_generated_comparisons_match_declared_members_and_display_exact_bodies(self):
        path = ROOT / "src/web/data/structure/act-history/catalogue.json"
        if not path.exists():
            self.skipTest("catalogue projection has not been generated")
        data = json.loads(path.read_text())
        if not data.get("comparisons"):
            self.skipTest("no comparisons have been generated")
        for row in data["comparisons"]:
            with self.subTest(comparison=row["id"]):
                payload = json.loads((path.parent / row["projection_path"]).read_text())
                isolated = {**data, "comparisons": [row]}
                got = self.drive(isolated, fragments={"structure/act-history/" + row["projection_path"]: payload},
                                 actions=[{"do": "comparison"}])
                self.assertEqual(got["catalogue-comparison-list"]["texts"],
                                 [payload["left"]["joined_source_text"], payload["right"]["joined_source_text"]])
                self.assertIn(payload["unified_diff"], got["catalogue-comparison-list"]["text"])


@unittest.skipUnless(os.environ.get("TRIPTYCH_HISTORY_CATALOGUE_BROWSER") == "1",
                     "real browser pending: run with TRIPTYCH_HISTORY_CATALOGUE_BROWSER=1 on a host that permits sockets")
class CatalogueBrowserTests(unittest.TestCase):
    def test_narrow_keyboard_selection_and_forced_colors(self):
        from tools.tests import test_browser_truthfulness as browser

        self.assertTrue((ROOT / "src/web/data/structure/act-history/catalogue.json").exists(),
                        "generate the catalogue before running real-browser acceptance")
        marker = "      } else {\n        throw new Error('unknown act: ' + act.do);"
        self.assertEqual(browser.HARNESS.count(marker), 1)
        harness = browser.HARNESS.replace(marker, """      } else if (act.do === 'cdp') {
        await cdp.send(act.method, act.params || {});
""" + marker)
        plan = {"acts": [
            {"do": "navigate", "url": browser.page("history", "view=catalogue")},
            {"do": "wait", "until": "document.querySelector('.catalogue-title')"},
            {"do": "cdp", "method": "Emulation.setDeviceMetricsOverride", "params": {
                "width": 320, "height": 852, "deviceScaleFactor": 1, "mobile": False}},
            {"do": "eval", "expression": "document.querySelector('.catalogue-title').focus()"},
            {"do": "cdp", "method": "Input.dispatchKeyEvent", "params": {
                "type": "keyDown", "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13}},
            {"do": "wait", "until": "!document.getElementById('catalogue-detail').hidden"},
            {"do": "eval", "name": "selected", "expression": """({
                focus: document.activeElement.id,
                hash: location.hash,
                overflow: document.documentElement.scrollWidth > innerWidth,
                main: document.querySelectorAll('main').length,
                mapHidden: document.getElementById('historical-map').hidden,
                facts: document.querySelector('.catalogue-facts').textContent
            })"""},
            {"do": "cdp", "method": "Emulation.setEmulatedMedia", "params": {
                "features": [{"name": "forced-colors", "value": "active"}]}},
            {"do": "eval", "expression": "document.querySelector('#catalogue-detail button').focus()"},
            {"do": "cdp", "method": "Input.dispatchKeyEvent", "params": {
                "type": "keyDown", "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13}},
            {"do": "eval", "name": "returned", "expression": """({
                focus: document.activeElement.className,
                forced: matchMedia('(forced-colors: active)').matches,
                overflow: document.documentElement.scrollWidth > innerWidth
            })"""},
            {"do": "eval", "expression": "document.querySelector('.comparison-fold summary').focus()"},
            {"do": "cdp", "method": "Input.dispatchKeyEvent", "params": {
                "type": "keyDown", "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13}},
            {"do": "wait", "until": "document.querySelectorAll('.comparison-text').length === 2"},
            {"do": "eval", "name": "comparison", "expression": """({
                texts: [...document.querySelectorAll('.comparison-text')].map(n => n.textContent),
                caveat: document.querySelector('.comparison-caveat').textContent,
                overflow: document.documentElement.scrollWidth > innerWidth,
                labels: [...document.querySelectorAll('.comparison-witness')].map(n => n.getAttribute('aria-labelledby'))
            })"""},
        ]}
        scratch = ROOT / ".scratch/history-catalogue-ui"
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as temporary:
            script = Path(temporary) / "browser.mjs"
            script.write_text(harness)
            result = subprocess.run([NODE or "node", str(script), str(ROOT), json.dumps(plan), browser.browser()],
                                    capture_output=True, text=True, timeout=120,
                                    env={**os.environ, "TMPDIR": temporary})
        self.assertEqual(result.returncode, 0, result.stderr)
        got = json.loads(result.stdout)
        self.assertEqual(got["selected"]["focus"], "catalogue-detail")
        self.assertIn("record=", got["selected"]["hash"])
        self.assertEqual(got["selected"]["main"], 1)
        self.assertTrue(got["selected"]["mapHidden"])
        self.assertIn("Source acquisition", got["selected"]["facts"])
        self.assertIn("Text status", got["selected"]["facts"])
        self.assertFalse(got["selected"]["overflow"])
        self.assertEqual(got["returned"]["focus"], "catalogue-title")
        self.assertTrue(got["returned"]["forced"])
        self.assertFalse(got["returned"]["overflow"])
        catalogue_path = ROOT / "src/web/data/structure/act-history/catalogue.json"
        declaration = json.loads(catalogue_path.read_text())["comparisons"][0]
        payload = json.loads((catalogue_path.parent / declaration["projection_path"]).read_text())
        self.assertEqual(got["comparison"]["texts"], [payload["left"]["joined_source_text"], payload["right"]["joined_source_text"]])
        self.assertEqual(got["comparison"]["caveat"], payload["apparatus_caveat"])
        self.assertFalse(got["comparison"]["overflow"])
        self.assertTrue(all(got["comparison"]["labels"]))


if __name__ == "__main__":
    unittest.main()
