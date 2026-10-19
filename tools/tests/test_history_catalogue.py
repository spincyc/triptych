"""Replay the real catalogue controller without opening a sandbox socket.

The small DOM records behavior, not geometry. Real Chromium verification of
keyboard focus, narrow reflow, forced colors, and built-route parity remains a
separate gate; these tests never claim visual acceptance.
"""

from __future__ import annotations

import json
import copy
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
  get isConnected() {
    let node=this;
    while(node.parent) {
      if (!node.parent.children.includes(node)) return false;
      node=node.parent;
    }
    return nodes.get(node.id)===node;
  }
  appendChild(child) { child.parent = this; this.children.push(child); return child; }
  setAttribute(k, v) { this.attrs[k] = String(v); }
  removeAttribute(k) { delete this.attrs[k]; }
  addEventListener(k, fn) { this.events[k] = fn; }
  remove() { this.parent.children = this.parent.children.filter(n => n !== this); nodes.delete(this.id); }
  focus() { document.activeElement = this; }
  scrollIntoView() {}
  querySelectorAll(selector) {
    const all = this.children.flatMap(n => [n, ...n.querySelectorAll(selector)]);
    return all.filter(n => selector === '[aria-current]' && n.attrs['aria-current']);
  }
}
const html = fs.readFileSync(input.page, 'utf8');
for (const id of html.matchAll(/id="([^"]+)"/g)) { const e = new Element('div'); e.id = id[1]; }
const document = {getElementById: id => nodes.get(id), createElementNS: (_,tag) => new Element(tag), activeElement: null};
const location = {search: input.search === undefined ? '?view=catalogue&data=../../../data' : input.search, hash: input.hash || ''};
const calls = [];
const pending = [];
let hashHandler;
const Triptych = {
  stationKind: {}, dataRoot: '../../../data',
  el(tag, cls, text) { const e = new Element(tag, text || ''); e.className = cls; return e; },
  clear(node) { node.textContent = ''; },
  loadJSON: async path => {
    calls.push(path);
    if (input.missing) throw Error('HTTP 404');
    if (path === 'structure/act-history/catalogue.json') return input.data;
    if (input.fragments && Object.hasOwn(input.fragments, path)) {
      if (input.defer_native && path.includes('/native-texts/')) return new Promise(resolve=>pending.push(()=>resolve(input.fragments[path])));
      return input.fragments[path];
    }
    throw Error('HTTP 404');
  },
  setInlineNotice() {}, doneBootstrapping() {},
  readHash: () => new URLSearchParams(location.hash.replace(/^#/, '')),
  writeHash(pairs) { location.hash = '#' + new URLSearchParams(pairs.filter(p => p[1])).toString(); },
  onHashChange(fn) { hashHandler = fn; }
};
vm.runInNewContext(fs.readFileSync(input.script, 'utf8'), {
  window: {Triptych, location, matchMedia: () => ({matches:!!input.mobile})}, document, URL, URLSearchParams, console
});
function all(node) { return [node, ...node.children.flatMap(all)]; }
setImmediate(async () => {
  for (const action of input.actions || []) {
    if (action.do === 'stage' || action.do === 'transition') {
      const attr='data-'+action.do;
      const element=[...all(nodes.get('timeline-chart')),...all(nodes.get('timeline-list')),...all(nodes.get('timeline-detail')),...all(nodes.get('timeline-unpositioned-list')),...all(nodes.get('timeline-provisional-list'))].find(n=>n.attrs[attr]===action.id && n.events.click);
      const target=element || all(nodes.get('timeline-chart')).find(n=>n.attrs[attr]===action.id).parent;
      target.events.click({preventDefault(){}});
    } else if (action.do === 'timeline-control') {
      const node=nodes.get(action.id);
      if (action.value !== undefined) node.value=action.value;
      if (action.checked !== undefined) node.checked=action.checked;
      node.events[action.event || 'click']({preventDefault(){}});
    } else if (action.do === 'years') {
      nodes.get('timeline-start').value=action.start;
      nodes.get('timeline-end').value=action.end;
      nodes.get('timeline-filter').events.submit({preventDefault(){}});
    } else if (action.do === 'filter') {
      nodes.get('catalogue-family').value = action.family || '';
      nodes.get('catalogue-query').value = action.q || '';
      nodes.get('catalogue-filter').events.submit({preventDefault() {}});
    } else if (action.do === 'hash') {
      location.hash = action.value;
      hashHandler(Triptych.readHash());
    } else if (action.do === 'open') {
      const link = all(nodes.get('catalogue-results')).find(n => n.className === 'catalogue-title');
      link.events.click({preventDefault() {}});
    } else if (action.do === 'timeline-back') {
      all(nodes.get('timeline-detail')).find(n => n.tagName === 'button').events.click();
    } else if (action.do === 'back') {
      const button = all(nodes.get('catalogue-detail')).find(n => n.tagName === 'button');
      button.events.click();
    } else if (action.do === 'native-text') {
      const fold=all(nodes.get('timeline-detail')).find(n=>(n.className || '').includes('native-text-fold'));
      fold.open=true; fold.events.toggle();
      await new Promise(resolve=>setImmediate(resolve));
    } else if (action.do === 'release-responses') {
      pending.forEach(resolve=>resolve());
      await new Promise(resolve=>setImmediate(resolve));
    } else if (action.do === 'comparison' || action.do === 'relationship-comparison' || action.do === 'stage-comparison') {
      const host=action.do === 'comparison' ? 'catalogue-comparison-list' : action.do === 'stage-comparison' ? 'timeline-detail' : 'overview-connections';
      const fold = all(nodes.get(host)).filter(n => (n.className || '').includes('comparison-fold'))[action.index || 0];
      fold.open = true;
      fold.events.toggle();
      await new Promise(resolve => setImmediate(resolve));
    }
  }
  const result = {};
  for (const id of ['catalogue-results', 'catalogue-status', 'catalogue-detail', 'tally', 'catalogue-limits', 'catalogue-comparison-list', 'history-overview', 'overview-network', 'overview-connections', 'overview-groups', 'timeline-chart', 'timeline-list', 'timeline-detail', 'timeline-status', 'timeline-unpositioned-list', 'timeline-provisional-list', 'timeline-gaps']) {
    const node = nodes.get(id);
    result[id] = {text: node.textContent, hidden: node.hidden, attrs: node.attrs,
      links: all(node).filter(n => n.tagName === 'a').map(n => ({text: n.textContent, href: n.href, attrs: n.attrs})),
      tags: all(node).map(n => n.tagName)};
    result[id].texts = all(node).filter(n => n.className === 'held-text comparison-text').map(n => n.textContent);
    result[id].nativeTexts = all(node).filter(n => n.className === 'held-text native-text-body').map(n => ({text:n.textContent,attrs:n.attrs}));
    result[id].elements = all(node).map(n=>({tag:n.tagName,attrs:n.attrs,text:n._text}));
    result[id].ids = all(node).map(n => n.id).filter(Boolean);
  }
  result.timelineHidden=nodes.get('timeline').hidden;
  result.timelineSelection={tradition:nodes.get('timeline-tradition').value,start:nodes.get('timeline-start').value,end:nodes.get('timeline-end').value};
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



def stage_fixture():
    """Constructed states exercise chronology, not historical claims."""
    evidence=[dict(source_id="fixture-source",locus="pp. 2–3",claim="The two actions are distinguished.")]
    def stage(identifier, year, **extra):
        result=dict(id=identifier,tradition_id="fixture-line",label="Book state "+identifier,
            date_label="Unresolved date" if year is None else str(year),start_year=year,end_year=year,
            date_kind="attestation",status="documented",scope="Ordinary rubrics only; not a whole book.",
            components=["rubrics"],witness_ids=["example"],witness_label="Identified example witness",
            summary="A bounded rubric state.",text_coverage="not-transcribed",evidence=evidence,
            limitations="No complete reconstruction.",reception="Community use is unestablished.")
        result.update(extra)
        return result
    transition=dict(id="change",from_stage="first",to_stage="second",kind="revision",status="documented",
        evidence_level="primary-description",summary="The standing rubric is replaced by kneeling.",
        components=["rubrics"],changes=[dict(component="rubrics",before="Stand during the prayer.",
        after="Kneel during the prayer.",locus_before="first p. 2",locus_after="second p. 3",evidence=evidence)],
        evidence=evidence,limitations="Source description; no full text collation.",comparison_ids=[],
        historical_parentage="attributed",git_ancestry=False,text_inheritance=False)
    return dict(schema="triptych-eucharistic-stages/v1",default_tradition_id="fixture-line",
        traditions=[dict(id="fixture-line",label="Constructed principal recension",scope="Only named rubric states",coverage_note="Incomplete."),
                    dict(id="parallel-line",label="Constructed parallel recension",scope="A contemporary book",coverage_note="Incomplete.")],
        sources=[dict(id="fixture-source",title="Constructed witness source",url="https://example.org/book",
                      kind="primary-book",inspection="Named pages inspected.",status="inspected",limitations="Excerpt only.")],
        stages=[stage("first",1200,end_year=1220,date_label="1200–1220"),
                stage("second",1210,end_year=1230,date_label="1210–1230",text_coverage="partial"),
                stage("companion",1250,components=["chants"],scope="Complementary chant volume."),
                stage("parallel",1210,end_year=1230,tradition_id="parallel-line"),
                stage("undated",None),stage("lead",1240,status="provisional")],
        transitions=[transition,dict(transition,id="succession",from_stage="second",to_stage="companion",
                    kind="witness-succession",evidence_level="bibliographic-only",changes=[],
                    historical_parentage="unestablished",summary="A later complementary witness is catalogued; no revision is established.")],
        gaps=[dict(id="gap",tradition_id="fixture-line",period="Before 1200",missing="Earlier rubric evidence missing.",
                   next_source="An earlier identified witness.",consequence="No earlier parent is inferred.")])


def stage_geometry(history, **options):
    script = r"""
const fs=require('node:fs'),vm=require('node:vm');
const input=JSON.parse(fs.readFileSync(0,'utf8')),source=fs.readFileSync(input.script,'utf8');
const start=source.indexOf('  const M = (function () {');
const end=source.indexOf('\n  }());',start)+'\n  }());'.length;
const context={T:{stationKind:{}},history:input.history,options:input.options}; vm.createContext(context);
vm.runInContext(source.slice(start,end),context);
process.stdout.write(JSON.stringify(vm.runInContext('M.stageLayout(history,options)',context)));
"""
    run=subprocess.run([NODE,"-e",script],input=json.dumps(dict(script=str(SCRIPT),history=history,options=options)),
                       text=True,capture_output=True,check=True)
    return json.loads(run.stdout)


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


def native_reading_fixture():
    """Literal fixture strings test display and refusal, never historical text."""
    history=stage_fixture()
    stage=history["stages"][1]
    stage.update(text_binding="native-book:fixture-text", text_projection_path="native-texts/fixture-text.json", text_binding_sha256="a"*64)
    payload=dict(schema="triptych-eucharistic-native-text/v1", id="fixture-text", adapter_id=stage["text_binding"],
        title="Constructed Arabic constituent", binding_sha256=stage["text_binding_sha256"], stage_ids=[stage["id"]], catalogue_witness_ids=stage["witness_ids"],
        scope=dict(extent_kind="constituent", whole_book_complete=False, complete_declared_extent=True,
                   description="Two constructed units only.", omitted_book_divisions=["The rest of the constructed book"], known_extent_units=2),
        counts=dict(units=2), witnesses=[dict(id="copy", edition_id="edition.fixture", artifact_id="artifact.scan")],
        sources=[dict(id="edition.fixture",record_type="edition",title="Constructed edition",date="1200"),
                 dict(id="artifact.scan",record_type="artifact",source_url="https://example.org/source"),
                 dict(id="artifact.text",record_type="artifact",edition_id="edition.fixture",rights_status="public-domain",rights_jurisdiction="United States",
                      rights_basis="Synthetic test rights statement; no historical source asserted.",transformation="No new paragraph divisions."),
                 dict(id="passage.first",record_type="passage",edition_id="edition.fixture",artifact_id="artifact.text"),
                 dict(id="passage.second",record_type="passage",edition_id="edition.fixture",artifact_id="artifact.text")], units=[])
    for index, body in enumerate(("ألف باء\n\nجيم <img src=x>", "دال هاء"),1):
        payload["units"].append(dict(unit_id="unit."+str(index),source_order=index,kind="rubric",native_path=["fixture",str(index)],
            text=body,language="ar",direction="rtl",source_locator="Constructed page "+str(index),
            source_id="passage.first" if index==1 else "passage.second",source_artifact_id="artifact.text",text_edition_id="edition.fixture",witness_id="copy",
            publication=dict(status="permitted",basis="public-domain",jurisdiction="United States",surfaces=["public-git","corpus-data"])))
    return history, {"structure/act-history/"+stage["text_projection_path"]:payload}


@unittest.skipIf(NODE is None, "node is unavailable")
class TimelineControllerTests(unittest.TestCase):
    def drive(self, history=None, **options):
        data=catalogue(); data["stage_history"]=stage_fixture() if history is None else history
        request=dict(data=data,page=str(PAGE),script=str(SCRIPT),search="?view=timeline&data=fixture"); request.update(options)
        run=subprocess.run([NODE,"-e",HARNESS],input=json.dumps(request),text=True,capture_output=True,cwd=ROOT,timeout=20)
        self.assertEqual(run.returncode,0,run.stderr)
        return json.loads(run.stdout)

    def test_default_entry_uses_timeline_and_keeps_optional_views_accessible(self):
        got=self.drive(search="")
        self.assertFalse(got["timelineHidden"])
        self.assertTrue(got["mapHidden"])
        self.assertEqual(got["calls"],["structure/act-history/catalogue.json"])
        self.assertEqual(got["timelineSelection"]["tradition"],"fixture-line")
        self.assertIn("standing rubric is replaced",got["timeline-chart"]["text"])
        self.assertIn("view=map",got["navigation"])
        self.assertIn("view=overview",got["overviewNavigation"])
        marker=next(e["attrs"] for e in got["timeline-chart"]["elements"] if e["tag"]=="marker")
        radius=max(float(e["attrs"]["r"]) for e in got["timeline-chart"]["elements"] if e["tag"]=="circle")
        self.assertEqual(marker["markerUnits"],"userSpaceOnUse")
        self.assertGreater(float(marker["refX"])-float(marker["viewBox"].split()[2]),radius)
        key=next(e["attrs"] for e in got["timeline-chart"]["elements"] if e["tag"]=="text" and e["text"]=="S001")
        point=next(e["attrs"] for e in got["timeline-chart"]["elements"] if e["tag"]=="circle" and e["attrs"]["r"]=="6")
        self.assertGreater(abs(float(key["x"])-float(point["cx"])),radius)

    def test_geometry_has_true_shared_year_axis_uncertainty_and_no_sorted_ancestry(self):
        model=stage_geometry(stage_fixture(),start=1200,end=1300)
        nodes={n["id"]:n for lane in model["lanes"] for n in lane["nodes"]}
        self.assertEqual(nodes["second"]["x"],nodes["parallel"]["x"])
        span=model["axis"]["x1"]-model["axis"]["x0"]
        self.assertAlmostEqual(nodes["first"]["xEnd"]-nodes["first"]["xStart"],span*.2)
        self.assertAlmostEqual(nodes["companion"]["x"]-nodes["second"]["x"],span*.3)
        self.assertEqual({e["id"] for e in model["edges"]},{"change","succession"})
        self.assertEqual([s["id"] for s in model["unpositioned"]],["undated"])
        self.assertNotIn("lead",nodes)
        self.assertNotEqual(nodes["first"]["row"],nodes["second"]["row"])
        self.assertEqual(model["edges"][0]["style"]["dash"],"")
        self.assertNotEqual(model["edges"][1]["style"]["dash"],"")
        self.assertNotEqual(model["edges"][0]["path"].split(" H ")[1],model["edges"][1]["path"].split(" H ")[1])

    def test_undated_external_arrows_follow_source_to_target_without_doubling_back(self):
        for source, target, upward in [("first", "undated", True), ("undated", "first", False)]:
            with self.subTest(source=source, target=target):
                history=stage_fixture()
                transition=dict(history["transitions"][0], from_stage=source, to_stage=target)
                history["transitions"]=[transition]
                model=stage_geometry(history, tradition="fixture-line", compact=True)
                edge=model["edges"][0]
                start,end=edge["fromPoint"],edge["toPoint"]
                self.assertTrue(edge["external"])
                self.assertEqual(start["x"],end["x"])
                self.assertEqual(edge["path"],f'M {start["x"]} {start["y"]} L {end["x"]} {end["y"]}')
                self.assertEqual(start["y"]>end["y"],upward)
                self.assertEqual(abs(start["y"]-end["y"]),30)
                self.assertEqual(edge["fromOutside"],source=="undated")
                self.assertEqual(edge["toOutside"],target=="undated")

    def test_same_row_transition_key_follows_own_arc_and_is_drawn_above_all_routes(self):
        history=stage_fixture()
        history["stages"]=history["stages"][:2]
        history["stages"][0].update(start_year=1200,end_year=1200)
        history["stages"][1].update(start_year=1300,end_year=1300)
        history["transitions"]=history["transitions"][:1]
        model=stage_geometry(history,tradition="fixture-line",compact=True,start=1200,end=1300)
        edge=model["edges"][0]
        self.assertEqual(edge["fromPoint"]["y"],edge["toPoint"]["y"])
        self.assertEqual(edge["keyLabel"]["y"],edge["fromPoint"]["y"]-3)
        self.assertEqual(edge["keyLabel"]["x"],(edge["fromPoint"]["x"]+edge["toPoint"]["x"])/2)
        got=self.drive()
        elements=got["timeline-chart"]["elements"]
        paths=[i for i,e in enumerate(elements) if e["attrs"].get("data-transition")]
        keys=[i for i,e in enumerate(elements) if e["attrs"].get("data-transition-key")]
        self.assertEqual(len(paths),len(keys))
        self.assertGreater(min(keys),max(paths))

    def test_parallel_same_row_transitions_keep_distinct_reachable_labels_and_paths(self):
        history=stage_fixture()
        history["stages"]=history["stages"][:2]
        history["stages"][0].update(start_year=1200,end_year=1200)
        history["stages"][1].update(start_year=1300,end_year=1300)
        history["transitions"]=[dict(history["transitions"][0],id="parallel-"+str(i)) for i in range(3)]
        model=stage_geometry(history,tradition="fixture-line",compact=True,start=1200,end=1300)
        self.assertEqual({edge["id"] for edge in model["edges"]},{row["id"] for row in history["transitions"]})
        self.assertEqual(len({edge["path"] for edge in model["edges"]}),3)
        for left,right in zip(model["edges"],model["edges"][1:]):
            self.assertEqual(left["fromPoint"],right["fromPoint"])
            self.assertEqual(left["toPoint"],right["toPoint"])
            self.assertGreaterEqual(abs(left["keyLabel"]["y"]-right["keyLabel"]["y"]),24)
        self.assertGreater(min(edge["keyLabel"]["y"] for edge in model["edges"]),model["lanes"][0]["top"])

    def test_parallel_undated_connections_have_distinct_curves_and_clear_labels(self):
        for from_stage,to_stage in (("first","undated"),("undated","first")):
            with self.subTest(from_stage=from_stage):
                history=stage_fixture()
                history["transitions"]=[dict(history["transitions"][0],id="parallel-"+str(i),from_stage=from_stage,to_stage=to_stage) for i in range(3)]
                model=stage_geometry(history,tradition="fixture-line",compact=True)
                self.assertEqual(len({edge["path"] for edge in model["edges"]}),3)
                for left,right in zip(model["edges"],model["edges"][1:]):
                    self.assertGreaterEqual(abs(left["keyLabel"]["x"]-right["keyLabel"]["x"]),38)
                for edge in model["edges"]:
                    self.assertGreater(edge["keyLabel"]["y"],model["lanes"][0]["top"])
                    self.assertGreaterEqual(edge["keyLabel"]["x"]-34,model["axis"]["x0"])
                    self.assertLessEqual(edge["keyLabel"]["x"]+4,model["axis"]["x1"])

    def test_native_text_is_lazy_literal_ordered_and_bounded_in_chart_and_list(self):
        history,fragments=native_reading_fixture()
        payload=next(iter(fragments.values()))
        for mobile in (False,True):
            with self.subTest(mobile=mobile):
                closed=self.drive(history,mobile=mobile,fragments=fragments,hash="#stage=second")
                self.assertEqual(closed["calls"],["structure/act-history/catalogue.json"])
                got=self.drive(history,mobile=mobile,fragments=fragments,hash="#stage=second",actions=[dict(do="native-text")])
                self.assertEqual(got["calls"],["structure/act-history/catalogue.json",*fragments])
                shown=got["timeline-detail"]
                self.assertEqual([row["text"] for row in shown["nativeTexts"]],[unit["text"] for unit in payload["units"]])
                self.assertEqual([row["attrs"] for row in shown["nativeTexts"]],
                                 [{"data-unit-id":unit["unit_id"],"lang":"ar","dir":"rtl"} for unit in payload["units"]])
                self.assertNotIn("img",shown["tags"])
                for value in ("Complete declared constituent", "Whole-book text coverage: partial", "The rest of the constructed book",
                              "Constructed edition", "Constructed page 1", "Public domain · United States", "Synthetic test rights statement"):
                    self.assertIn(value,shown["text"])
                self.assertTrue(any(e["attrs"].get("role")=="status" and e["text"]=="Source text loaded." for e in shown["elements"]))
                self.assertTrue(any(e["attrs"].get("aria-busy")=="false" for e in shown["elements"]))

    def test_native_text_refuses_wrong_binding_extent_rights_and_unit_order_before_display(self):
        history,fragments=native_reading_fixture()
        path=next(iter(fragments))
        for defect in ("binding","stale-binding","stage","extent","rights","unit-order","wrong-source-type","wrong-source-edition","wrong-witness-type"):
            with self.subTest(defect=defect):
                changed=copy.deepcopy(fragments)
                payload=changed[path]
                if defect=="binding": payload["adapter_id"]="native-book:different"
                elif defect=="stale-binding": payload["binding_sha256"]="b"*64
                elif defect=="stage": payload["stage_ids"]=["different"]
                elif defect=="extent": payload["scope"]["whole_book_complete"]=True
                elif defect=="rights": payload["sources"][2]["rights_status"]="unresolved"
                elif defect=="wrong-source-type": payload["units"][0]["source_id"]="artifact.scan"
                elif defect=="wrong-source-edition": payload["sources"][3]["edition_id"]="edition.different"
                elif defect=="wrong-witness-type": payload["witnesses"][0]["artifact_id"]="passage.first"
                else: payload["units"].reverse()
                got=self.drive(history,fragments=changed,hash="#stage=second",actions=[dict(do="native-text")])
                self.assertEqual(got["timeline-detail"]["nativeTexts"],[])
                self.assertIn("does not match this state",got["timeline-detail"]["text"])
                self.assertNotIn("ألف",got["timeline-detail"]["text"])
                self.assertTrue(any(e["attrs"].get("role")=="status" and e["text"]=="Source text could not be loaded." for e in got["timeline-detail"]["elements"]))

    def test_native_text_loading_announces_progress_without_making_literal_body_live(self):
        history,fragments=native_reading_fixture()
        got=self.drive(history,fragments=fragments,defer_native=True,hash="#stage=second",actions=[dict(do="native-text")])
        self.assertTrue(any(e["attrs"].get("role")=="status" and e["text"]=="Loading source text…" for e in got["timeline-detail"]["elements"]))
        self.assertTrue(any(e["attrs"].get("aria-busy")=="true" for e in got["timeline-detail"]["elements"]))
        self.assertEqual(got["timeline-detail"]["nativeTexts"],[])

    def test_native_text_late_response_cannot_replace_new_selection(self):
        history,fragments=native_reading_fixture()
        got=self.drive(history,fragments=fragments,defer_native=True,hash="#stage=second",
                       actions=[dict(do="native-text"),dict(do="stage",id="first"),dict(do="release-responses")])
        self.assertIn("Book state first",got["timeline-detail"]["text"])
        self.assertEqual(got["timeline-detail"]["nativeTexts"],[])
        self.assertNotIn("ألف",got["timeline-detail"]["text"])

    def test_native_text_routing_cannot_fetch_an_unowned_path(self):
        history,fragments=native_reading_fixture()
        history["stages"][1]["text_projection_path"]="../../unreviewed.json"
        got=self.drive(history,fragments=fragments,hash="#stage=second")
        self.assertEqual(got["calls"],["structure/act-history/catalogue.json"])
        self.assertIn("invalid routing metadata",got["timeline-detail"]["text"])

    def test_selecting_state_reveals_change_loci_witness_and_independent_text_status(self):
        got=self.drive(actions=[dict(do="stage",id="second")])
        detail=got["timeline-detail"]["text"]
        for text in ["Before: Stand during the prayer.","After: Kneel during the prayer.","first p. 2","second p. 3",
                     "primary description","parentage: attributed","Text coverage: partial","Ordinary rubrics only","pp. 2–3"]:
            self.assertIn(text,detail)
        self.assertEqual(got["focus"],"timeline-detail")
        self.assertIn("stage=second",got["hash"])
        self.assertTrue(any("view=catalogue" in link["href"] and "record=example" in link["href"] for link in got["timeline-detail"]["links"]))

    def test_presentation_is_restored_from_url_and_browser_history(self):
        got=self.drive(hash="#presentation=list")
        self.assertTrue(got["timeline-chart"]["hidden"])
        self.assertFalse(got["timeline-list"]["hidden"])
        got=self.drive(mobile=True,hash="#presentation=chart")
        self.assertFalse(got["timeline-chart"]["hidden"])
        got=self.drive(actions=[dict(do="timeline-control",id="timeline-presentation",event="change",value="list")])
        self.assertIn("presentation=list",got["hash"])
        got=self.drive(mobile=True,actions=[dict(do="hash",value="#presentation=chart")])
        self.assertFalse(got["timeline-chart"]["hidden"])

    def test_legacy_hash_restores_responsive_presentation_and_invalid_selection_name(self):
        got=self.drive(actions=[dict(do="timeline-control",id="timeline-presentation",event="change",value="list"),dict(do="hash",value="")])
        self.assertFalse(got["timeline-chart"]["hidden"])
        got=self.drive(hash="#stage=second",actions=[dict(do="hash",value="#stage=missing")])
        self.assertEqual(got["timeline-detail"]["attrs"]["aria-label"],"Selected state or transition evidence")

    def test_invalid_year_hash_clears_previous_selection_before_focus_restore(self):
        got=self.drive(hash="#stage=second",actions=[dict(do="hash",value="#stage=missing&start=2000&end=1900")])
        self.assertTrue(got["timeline-detail"]["hidden"])
        self.assertEqual(got["timeline-detail"]["text"],"")
        self.assertEqual(got["timeline-detail"]["attrs"]["aria-label"],"Selected state or transition evidence")
        self.assertEqual(got["focus"],"timeline-status")
        self.assertIn("Choose an ending year",got["timeline-status"]["text"])

    def test_supplementary_stage_controls_have_unique_ids_and_return_targets(self):
        got=self.drive(hash="#leads=1")
        ids=[identifier for host in ("timeline-list","timeline-provisional-list","timeline-unpositioned-list") for identifier in got[host]["ids"]]
        self.assertEqual(len(ids),len(set(ids)))
        got=self.drive(hash="#stage=undated",actions=[dict(do="timeline-back")])
        self.assertEqual(got["focus"],"timeline-unpositioned-list-stage-undated")

    def test_deep_links_and_browser_history_focus_selected_evidence(self):
        for address in ("#stage=second", "#transition=change"):
            with self.subTest(address=address):
                direct=self.drive(hash=address)
                back=self.drive(actions=[dict(do="hash",value=address)])
                for result in (direct,back):
                    self.assertEqual(result["focus"],"timeline-detail")
                    self.assertTrue(result["timeline-detail"]["attrs"]["aria-label"].startswith("Selected "))

    def test_return_restores_selected_marker_or_reading_list_item(self):
        for mobile in (False,True):
            for kind,identifier in (("stage","second"),("transition","change")):
                with self.subTest(mobile=mobile,kind=kind):
                    result=self.drive(mobile=mobile,actions=[dict(do=kind,id=identifier),dict(do="timeline-back")])
                    host="timeline-list" if mobile else "timeline-chart"
                    self.assertEqual(result["focus"],host+"-"+kind+"-"+identifier)

    def test_window_controls_keep_explicit_boundary_connection_and_shareable_state(self):
        got=self.drive(actions=[dict(do="years",start="1230",end="1260")])
        self.assertIn("start=1230&end=1260",got["hash"])
        self.assertIn("1 dated states outside",got["timeline-status"]["text"])
        model=stage_geometry(stage_fixture(),tradition="fixture-line",start=1230,end=1260)
        edge=next(e for e in model["edges"] if e["id"]=="change")
        self.assertTrue(edge["fromOutside"])
        self.assertEqual(edge["fromStage"]["date_label"],"1200–1220")
        self.assertIn("Bounds continue beyond this window",got["timeline-chart"]["text"])
        self.assertTrue(any("start" in e["attrs"].get("data-date-clipped","") for e in got["timeline-chart"]["elements"]))
        self.assertIn("From S001 · 1200–1220 · outside this view",got["timeline-chart"]["text"])
        self.assertTrue(any(e["attrs"].get("data-continuation")=="first" for e in got["timeline-chart"]["elements"]))
        got=self.drive(actions=[dict(do="years",start="1230",end="1260"),dict(do="timeline-control",id="timeline-local-years")])
        self.assertEqual(got["timelineSelection"]["start"],"1200")
        self.assertEqual(got["timelineSelection"]["end"],"1250")

    def test_mobile_list_and_provisional_controls_keep_evidence_visible(self):
        got=self.drive(mobile=True,actions=[dict(do="timeline-control",id="timeline-leads",event="change",checked=True)])
        self.assertTrue(got["timeline-chart"]["hidden"])
        self.assertFalse(got["timeline-list"]["hidden"])
        self.assertIn("Book state lead",got["timeline-list"]["text"])
        self.assertIn("provisional",got["timeline-list"]["text"])
        self.assertIn("standing rubric is replaced",got["timeline-list"]["text"])
        self.assertIn("Earlier rubric evidence missing",got["timeline-gaps"]["text"])
        self.assertIn("leads=1",got["hash"])

    def test_transition_selection_distinguishes_bibliographic_succession(self):
        got=self.drive(actions=[dict(do="transition",id="succession")])
        detail=got["timeline-detail"]["text"]
        self.assertIn("bibliographic only",detail)
        self.assertIn("parentage: unestablished",detail)
        self.assertIn("No component-level before/after collation",detail)
        self.assertIn("transition=succession",got["hash"])

    def test_undated_only_history_does_not_invent_axis_and_unknown_selection_does_not_broaden(self):
        history=stage_fixture(); history["stages"]=[history["stages"][4]]; history["transitions"]=[]
        got=self.drive(history)
        self.assertIn("No dated states",got["timeline-status"]["text"])
        self.assertIn("Book state undated",got["timeline-unpositioned-list"]["text"])
        self.assertEqual(stage_geometry(history)["axis"]["ticks"],[])
        got=self.drive(hash="#tradition=unknown&stage=missing")
        self.assertIn("not in the current stage record",got["timeline-status"]["text"])
        self.assertIn("not in the current record",got["timeline-detail"]["text"])

    def test_outgoing_cross_recension_navigation_moves_lane_and_window(self):
        history=stage_fixture()
        history["stages"][3].update(start_year=1500,end_year=1500,date_label="1500")
        history["transitions"].append(dict(history["transitions"][0],id="cross-recension",from_stage="companion",to_stage="parallel",kind="recension-branch"))
        got=self.drive(history,hash="#stage=companion",actions=[dict(do="stage",id="parallel")])
        self.assertEqual(got["timelineSelection"]["tradition"],"parallel-line")
        self.assertEqual(got["timelineSelection"]["start"],"1500")
        self.assertIn("stage=parallel",got["hash"])
        self.assertIn("Book state parallel",got["timeline-chart"]["text"])
        self.assertIn("Before: Stand",got["timeline-detail"]["text"])
        first=self.drive(history,hash="#stage=companion")
        self.assertIn("What follows from this state",first["timeline-detail"]["text"])
        self.assertIn("1500 · Book state parallel",first["timeline-detail"]["text"])

    def test_roman_1962_to_1970_source_transition_is_followable_across_named_recensions(self):
        dossier=json.loads((ROOT / "src/sources/inventories/eucharistic-stages/roman.json").read_text())
        # Retain source-owned rows; these two projection-only safety flags add
        # no historical claim. Backend tests validate the actual projection.
        history={key:dossier[key] for key in ("traditions","sources","stages","transitions","gaps")}
        history.update(schema="triptych-eucharistic-stages/v1",default_tradition_id="roman-stages-pian")
        history["transitions"]=[dict(t,git_ancestry=False,text_inheritance=False) for t in history["transitions"]]
        start="#tradition=roman-stages-pian&stage=roman-stages-1962-june"
        opened=self.drive(history,hash=start)
        target=next(s for s in history["stages"] if s["id"]=="roman-stages-1969-1970")
        self.assertIn(target["label"],opened["timeline-detail"]["text"])
        followed=self.drive(history,hash=start,actions=[dict(do="stage",id=target["id"])])
        self.assertEqual(followed["timelineSelection"]["tradition"],target["tradition_id"])
        self.assertTrue(any(target["label"] in e["attrs"].get("aria-label","") for e in followed["timeline-chart"]["elements"]))
        self.assertIn(target["label"],followed["timeline-detail"]["text"])

    def test_shared_origin_transition_keys_are_distinct_and_external_ports_clear_prior_cards(self):
        history=stage_fixture()
        history["transitions"][1]["from_stage"]="first"
        history["stages"][2].update(start_year=1231,end_year=1231,date_label="1231")
        model=stage_geometry(history,start=1200,end=1300,compact=True)
        self.assertNotEqual(model["edges"][0]["keyLabel"],model["edges"][1]["keyLabel"])
        paginated=stage_geometry(history,start=1200,end=1300,compact=True,stageIds=["second","companion"])
        nodes={n["id"]:n for lane in paginated["lanes"] for n in lane["nodes"]}
        edge=next(e for e in paginated["edges"] if e["to"]=="companion")
        self.assertLess(nodes["second"]["row"],nodes["companion"]["row"])
        prior_bottom=nodes["second"]["labelY"]-17+nodes["second"]["cardHeight"]
        self.assertGreater(edge["keyLabel"]["y"]-14,prior_bottom)

    def test_adjacent_corridors_have_nonoverlapping_transition_key_boxes(self):
        history=stage_fixture()
        history["stages"][2].update(start_year=1211,end_year=1229,date_label="1211–1229")
        history["transitions"][1].update(from_stage="parallel",to_stage="companion")
        history["transitions"].append(dict(history["transitions"][0],id="another",from_stage="first",to_stage="companion"))
        model=stage_geometry(history,start=1200,end=1300,compact=True)
        for i,first in enumerate(model["edges"]):
            for second in model["edges"][i+1:]:
                a,b=first["keyLabel"],second["keyLabel"]
                self.assertTrue(abs(a["x"]-b["x"])>=60 or abs(a["y"]-b["y"])>=24)

    def test_compact_model_reduces_cards_without_changing_dates_connections_or_evidence(self):
        full=stage_geometry(stage_fixture(),start=1200,end=1300)
        compact=stage_geometry(stage_fixture(),start=1200,end=1300,compact=True)
        self.assertLess(compact["height"],full["height"])
        self.assertEqual([(e["from"],e["to"],e["transition"]) for e in compact["edges"]],
                         [(e["from"],e["to"],e["transition"]) for e in full["edges"]])
        full_nodes={n["id"]:n for lane in full["lanes"] for n in lane["nodes"]}
        for lane in compact["lanes"]:
            for node in lane["nodes"]:
                original=full_nodes[node["id"]]
                self.assertEqual((node["x"],node["xStart"],node["xEnd"]),(original["x"],original["xStart"],original["xEnd"]))
                self.assertEqual(node["fullChangeLines"],original["changeLines"])
                self.assertEqual(node["stage"],original["stage"])
                self.assertEqual(node["changeLines"],[])

    def test_paginated_model_keeps_source_port_at_true_year_and_delta_citations_inline(self):
        model=stage_geometry(stage_fixture(),start=1200,end=1300,stageIds=["second"])
        edge=next(e for e in model["edges"] if e["id"]=="change")
        expected=model["axis"]["x0"]+.1*(model["axis"]["x1"]-model["axis"]["x0"])
        self.assertAlmostEqual(float(edge["path"].split()[1]),expected)
        self.assertTrue(edge["fromOutside"])
        self.assertEqual(model["counts"]["outsideWindow"],0)
        node=model["lanes"][0]["nodes"][0]
        self.assertIn("Before: Stand during the prayer."," ".join(node["changeLines"]))
        self.assertIn("After: Kneel during the prayer."," ".join(node["changeLines"]))
        self.assertIn("C001 · pp. 2–3"," ".join(node["changeLines"]))

    def test_projected_stage_comparisons_load_actual_source_payloads_only_when_opened(self):
        path=ROOT / "src/web/data/structure/act-history/catalogue.json"
        data=json.loads(path.read_text())
        history=data.get("stage_history")
        if not history:
            self.skipTest("stage projection has not been generated")
        comparisons={c["id"]:c for c in data["comparisons"]}
        exercised=[]
        for transition in history["transitions"]:
            for index,identifier in enumerate(transition["comparison_ids"]):
                with self.subTest(transition=transition["id"],comparison=identifier):
                    row=comparisons[identifier]
                    payload=json.loads((path.parent / row["projection_path"]).read_text())
                    fragment="structure/act-history/"+row["projection_path"]
                    options=dict(data=data,hash="#transition="+transition["id"],fragments={fragment:payload})
                    closed=self.drive(history,**options)
                    self.assertEqual(closed["calls"],["structure/act-history/catalogue.json"])
                    opened=self.drive(history,**options,actions=[dict(do="stage-comparison",index=index)])
                    self.assertEqual(opened["calls"],["structure/act-history/catalogue.json",fragment])
                    self.assertEqual(opened["timeline-detail"]["texts"],
                                     [payload["left"]["joined_source_text"],payload["right"]["joined_source_text"]])
                    self.assertIn(payload["unified_diff"],opened["timeline-detail"]["text"])
                    exercised.append(identifier)
        self.assertTrue(exercised,"final stage history must retain its declared source-text comparisons")

    def test_initial_timeline_transport_failure_claims_no_fallback(self):
        got=self.drive(missing=True)
        self.assertIn("Historical timeline unavailable",got["timeline-status"]["text"])
        self.assertNotIn("fallback",got["timeline-status"]["text"])
        self.assertEqual(got["timeline-chart"]["attrs"]["aria-busy"],"false")
        self.assertEqual(got["timeline-chart"]["text"],"")

    def test_malformed_evidence_and_dates_fail_closed(self):
        for mutation in (lambda h:h["stages"][0].update(end_year=1199),
                         lambda h:h["stages"][0]["evidence"][0].update(source_id="missing")):
            history=stage_fixture(); mutation(history)
            self.assertIn("unavailable",self.drive(history)["timeline-status"]["text"])


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
