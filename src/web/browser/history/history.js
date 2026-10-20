/* ===========================================================================
 * How the Missal changed — the map, and what each act did to the text
 * ===========================================================================
 *
 * WHAT A READER PAYS FOR. The map file is a SPINE: every station's act, date,
 * authority, instrument, line, parents, and a count of what it changed. It
 * carries no prayer text and no diff at all. Opening a station fetches that
 * station's change set; asking to read the missal as it stood fetches that
 * state; following one prayer fetches that prayer's history. A reader who only
 * looks at the map downloads the map.
 *
 * WHAT THIS FILE DOES NOT DO, AND MUST NOT START DOING:
 *
 *   It does not work out what an act changed. `act-history structure` derives
 *   that from the same state computation `emit` commits, and writes it. If this
 *   file ever diffed two states itself there would be two answers to "what
 *   changed in 1955" inside one artifact, and the wrong one would be the one on
 *   screen.
 *
 *   It does not decide whether a station is `promulgated` or `printed`. That is
 *   read from the file. Inferring it from whether an instrument string happens
 *   to be present would turn "nobody has read the decree yet" into "no decree
 *   is claimed", which are different statements about evidence.
 *
 *   It does not name a station, a line, or a count of either. The act data is
 *   being extended — earlier missals, further rites, parallel lines — and every
 *   loop below reads what the file gives.
 *
 * ABSENCE STAYS ON SCREEN. A connector crossing an edition this record does not
 * carry is drawn broken. A unit whose words the tracer never read says so where
 * the words would stand. A unit whose state an act left unestablished prints its
 * marker rather than falling back to the inherited text. A station that changed
 * nothing says that too: an authority acted and this slice did not move.
 * ======================================================================== */

(function () {
  'use strict';

  const T = window.Triptych;

  /* ========================================================================
   * THE MODEL — the drawing's arithmetic, and nothing else
   * ========================================================================
   *
   * Three things, and the rest of the file owns none of them:
   *
   *   lanes      where each station sits on the canvas, from the graph alone
   *   afterBase  which stations on a line stand below a given one
   *   kinds      whether a station is `promulgated` or `printed`
   *
   * IT DOES NOT WORK OUT WHAT TWO LINES SHARE. `act-history` derives the shared
   * base from the act graph, proves that derivation against `git merge-base` on
   * the repository it emits, and writes the answer into the map file. This
   * reads it. A second search for a merge base here is the two-tables defect
   * with extra steps, and the wrong table would be the one on screen.
   *
   * IT DOES NOT DERIVE WHAT AN ACT CHANGED. That is computed once, by
   * `act-history structure`, out of the same state computation `emit` commits,
   * and arrives as a fragment this page reads. A second derivation here is how
   * two answers to "what changed in 1955" ship inside one artifact, and
   * guidance/the-shape.md section 2 is about exactly that pair.
   *
   * THE GRAPH IS A FOREST, NOT A TREE. Before Trent there are missals whose
   * descent is genuinely uncertain, and inventing an edge there is forbidden,
   * so the honest graph has several origins with no parent at all. Everything
   * below is written against that: no root is privileged, no station id is
   * named, no count of lines or stations is assumed.
   * ===================================================================== */

  const M = (function () {
    /* ------------------------------------------------------------------------
     * Two kinds of station
     *
     * `promulgated` against `printed` is a statement about EVIDENCE, it is read
     * and never inferred, and the rule now lives in the shared machinery
     * because a second page reads it too. This page names it and keeps its own
     * copy of nothing.
     * --------------------------------------------------------------------- */

    const KIND = T.stationKind;
    const PROMULGATED = KIND.PROMULGATED;
    const PRINTED = KIND.PRINTED;
    const UNSTATED = KIND.UNSTATED;
    const kindsAreStated = KIND.stated;
    const kindOf = KIND.of;

    /* ------------------------------------------------------------------------
     * Lanes
     *
     * The same shape a git graph uses, with two rules and no more.
     *
     * ROW. A station continues the track of a parent that is still that track's
     * head and stands on its own line; among several it takes the lowest such
     * track, which is what pulls a rejoining branch back toward the trunk instead
     * of leaving the trunk stranded. Anything else opens a track: a fork, a merge
     * arriving from elsewhere, and every root. Rows are never re-used once a
     * track has ended, because dropping an unrelated station into a dead row
     * would draw it as that line continuing.
     *
     * COLUMN. One to the right of every parent, and one to the right of whatever
     * already stands in this row. Columns are therefore compact rather than one
     * per station, and a forest of roots all begins at the left edge. The column
     * is a position in the descent, not a date -- the year under each station is
     * what carries time, and two stations sharing a column are two stations at
     * the same remove from their origins, which is what a transit map says.
     * --------------------------------------------------------------------- */

    function layout(stations) {
      const rows = [];        // row -> id currently at the end of that track
      const ends = [];        // row -> rightmost column used in that track
      const lineOf = new Map();
      const at = new Map();
      (stations || []).forEach(function (station) { lineOf.set(station.id, station.line); });

      (stations || []).forEach(function (station) {
        const parents = station.parents || [];
        let row = -1;
        parents.forEach(function (parent) {
          const found = rows.indexOf(parent);
          if (found === -1) return;
          if (lineOf.get(parent) !== station.line) return;
          if (row === -1 || found < row) row = found;
        });
        if (row === -1) row = rows.length;

        let col = 0;
        parents.forEach(function (parent) {
          const placed = at.get(parent);
          if (placed && placed.col + 1 > col) col = placed.col + 1;
        });
        const end = ends[row];
        if (end !== undefined && end + 1 > col) col = end + 1;

        rows[row] = station.id;
        ends[row] = col;
        at.set(station.id, { col: col, row: row });
      });
      return at;
    }

    // A readable reflow of the existing graph tracks, not a second ancestry
    // computation. Dates order labels within each line; distance is not time.
    // Print consumes this exact model. Browser-measured label heights may expand
    // a row, but never change its identity, order, track, or parent links.
    function wrapLabel(value, width) {
      const result = [];
      String(value || '').split(/\s+/).forEach(function (word) {
        const last = result.length - 1;
        if (last < 0 || result[last].length + word.length + 1 > width) result.push(word);
        else result[last] += ' ' + word;
      });
      return result;
    }

    function panelLayout(stations, lines, heights) {
      const at = layout(stations);
      const index = new Map(stations.map(function (s, i) { return [s.id, i]; }));
      const stationById = new Map(stations.map(function (s) { return [s.id, s]; }));
      const order = Array.from(new Set(stations.map(function (s) { return s.line; })));
      const panels = order.map(function (line, i) {
        const definition = (lines || []).find(function (row) { return row.id === line; });
        const members = stations.filter(function (s) { return s.line === line; })
          .sort(function (a, b) { return a.date.localeCompare(b.date) || index.get(a.id) - index.get(b.id); });
        const tracks = Array.from(new Set(members.map(function (s) { return at.get(s.id).row; }))).sort(function (a,b) { return a-b; });
        let top = 12;
        const nodes = members.map(function (s) {
          const height = Math.max(104, (heights && heights[s.id]) || 104);
          const node = {id: s.id, x: 40 + tracks.indexOf(at.get(s.id).row) * 28,
            y: top + 52, top: top, height: height, date: s.date, title: s.title,
            titleLines: wrapLabel(s.title, 80), track: tracks.indexOf(at.get(s.id).row)};
          top += height;
          return node;
        });
        return {id: 'line-' + line, line: line, label: definition ? definition.label : line,
          number: i + 1, width: 1000, textX: Math.max(130, 68 + tracks.length * 28),
          height: top + 12, tracks: tracks.length, nodes: nodes, edges: []};
      });
      const panelByStation = new Map();
      panels.forEach(function (p) { p.nodes.forEach(function (n) { panelByStation.set(n.id, p); }); });
      panels.forEach(function (panel) {
        const local = new Map(panel.nodes.map(function (n) { return [n.id,n]; }));
        panel.nodes.forEach(function (to) {
          const station = stationById.get(to.id);
          (station.parents || []).forEach(function (parent) {
            const origin = panelByStation.get(parent);
            if (!origin) return;
            const external = origin !== panel;
            const from = external ? {x: to.x + 28, y: to.y - 32} : local.get(parent);
            const bend = Math.min(28, Math.abs(to.y - from.y) / 2);
            const path = from.x === to.x
              ? 'M ' + from.x + ' ' + from.y + ' L ' + to.x + ' ' + to.y
              : from.x < to.x
                ? 'M ' + from.x + ' ' + from.y + ' L ' + to.x + ' ' + (from.y + bend) +
                  ' L ' + to.x + ' ' + to.y
                : 'M ' + from.x + ' ' + from.y + ' L ' + from.x + ' ' + (to.y - bend) +
                  ' L ' + to.x + ' ' + to.y;
            panel.edges.push({from: parent, to: to.id, path: path, external: external,
              fromPanel: origin.number, toPanel: panel.number,
              fromTitle: stationById.get(parent).title, toTitle: station.title,
              reception: (station.receptions || []).some(function (r) { return r.from === parent; })});
          });
        });
      });
      return panels;
    }

    // Presentation groups are declared by the source owner. No UI alias table
    // turns similar names into a new historical claim or a census of rites.
    function overviewModel(data) {
      const groups = new Map();
      (data.presentation_groups || []).forEach(function (g) {
        groups.set(g.id, {id:g.id, label:g.label, note:g.note || '', entries:[], entities:[]});
      });
      const endpoints = new Map();
      (data.entries || []).concat(data.relationship_entities || []).forEach(function (row) {
        const declared = row.presentation_group;
        const group = declared || {id:'unmapped:' + row.family, label:row.family + ' (unmapped)'};
        if (!groups.has(group.id)) groups.set(group.id, {id:group.id, label:group.label, note:'', entries:[], entities:[]});
        const entity = row.kind === 'textual-tradition';
        groups.get(group.id)[entity ? 'entities' : 'entries'].push(row);
        endpoints.set(row.id, {id:row.id, title:row.title || row.label,
          group:group.label, groupId:group.id, entity:entity,
          date:entity ? 'Context entity; no dated witness plotted' : row.date_label,
          chronology:entity ? null : row.chronology, record:row});
      });
      const relations = (data.relationships || []).map(function (row, i) {
        return {id:row.id, number:i+1, label:row.label || row.kind, kind:row.kind,
          from:endpoints.get(row.from), to:endpoints.get(row.to), record:row};
      });
      return {groups:Array.from(groups.values()).filter(function (g) { return g.entries.length || g.entities.length; })
        .sort(function (a,b) { return a.label.localeCompare(b.label); }), relations:relations};
    }

    // A conventional radial network of declared presentation groups. Position
    // encodes connectivity only, never time, ancestry, or admission as an act.
    // Browser and print share this geometry and its complete relationship keys.
    function networkStyle(kind) {
      return {
        borrowing:{color:'#a4482d',dash:'',label:'Borrowing',width:6},
        reception:{color:'#176c79',dash:'16 5',label:'Reception',width:6},
        'shared-text':{color:'#715091',dash:'3 6',label:'Shared wording',width:6},
        'common-ancestry':{color:'#65742c',dash:'14 5 3 5',label:'Common ancestry',width:6},
        'edition-succession':{color:'#3c5f91',dash:'',label:'Edition succession',width:3}
      }[kind];
    }

    function networkLayout(data) {
      const model = overviewModel(data);
      const byGroup = new Map(model.groups.map(function (g) { return [g.id,g]; }));
      const adjacent = new Map();
      model.relations.forEach(function (r) {
        [r.from.groupId,r.to.groupId].forEach(function (id) { if (!adjacent.has(id)) adjacent.set(id,new Set()); });
        adjacent.get(r.from.groupId).add(r.to.groupId);
        adjacent.get(r.to.groupId).add(r.from.groupId);
      });
      const components = [], seen = new Set();
      Array.from(adjacent.keys()).sort().forEach(function (id) {
        if (seen.has(id)) return;
        const members = [], queue = [id]; seen.add(id);
        while (queue.length) {
          const next = queue.shift(); members.push(next);
          adjacent.get(next).forEach(function (other) { if (!seen.has(other)) { seen.add(other); queue.push(other); } });
        }
        components.push(members);
      });
      components.sort(function (a,b) { return b.length-a.length || a[0].localeCompare(b[0]); });
      return components.map(function (members, componentIndex) {
        members.sort(function (a,b) { return adjacent.get(b).size-adjacent.get(a).size || byGroup.get(a).label.localeCompare(byGroup.get(b).label); });
        const small = members.length <= 3;
        const width = small ? 1000 : 1800, height = small ? 480 : Math.max(1500,Math.ceil((members.length-1)/2)*126+180);
        const cx = width/2, cy = height/2, radius = Math.min(490,cy-180);
        const nodes = members.map(function (id,i) {
          const group = byGroup.get(id), angle = -Math.PI/2 + (i-1)*2*Math.PI/(members.length-1 || 1);
          const x = small ? members.length === 3 ? [500,220,780][i] : width*(i+1)/(members.length+1) : i === 0 ? cx : cx+radius*Math.cos(angle);
          const y = small ? members.length === 3 ? [70,290,290][i] : 170 : i === 0 ? cy : cy+radius*Math.sin(angle);
          return {id:id,label:group.label,x:x,y:y,labelX:x,labelY:y+50,anchor:'middle',
            labelLines:wrapLabel(group.label,small ? 20 : 25),hub:!small && i === 0,
            recordCount:group.entries.length,contextCount:group.entities.length,
            within:model.relations.filter(function (r) { return r.from.groupId === id && r.to.groupId === id; }).map(function (r) { return r.number; })};
        });
        nodes.forEach(function (node) {
          node.caption = node.recordCount ? node.recordCount+' record'+(node.recordCount === 1 ? '' : 's')
            : node.contextCount+' textual reference'+(node.contextCount === 1 ? '' : 's');
          if (node.within.length) node.caption += ' · '+node.within.length+' within-group link'+(node.within.length === 1 ? '' : 's');
        });
        if (!small) {
          [-1,1].forEach(function (side) {
            const sideNodes = nodes.slice(1).filter(function (n) { return (n.x < cx ? -1 : 1) === side; }).sort(function (a,b) { return a.y-b.y; });
            sideNodes.forEach(function (n,i) {
              n.labelX = side < 0 ? 30 : width-30;
              n.labelY = 80 + i*(height-280)/Math.max(1,sideNodes.length-1);
              n.anchor = side < 0 ? 'start' : 'end';
              const endX = side < 0 ? 365 : width-365;
              n.leader = 'M '+n.x+' '+n.y+' L '+endX+' '+n.labelY;
            });
          });
          nodes[0].labelY = cy-75;
        }
        const local = new Map(nodes.map(function (n) { return [n.id,n]; })), bundles = new Map();
        const relations = model.relations.filter(function (r) { return local.has(r.from.groupId); });
        relations.forEach(function (r) {
          if (r.from.groupId === r.to.groupId) return;
          let from = r.from.groupId, to = r.to.groupId;
          if (!r.record.directed && from > to) { const swap = from; from = to; to = swap; }
          const key = [from,to,r.kind,r.record.certainty].join('|');
          if (!bundles.has(key)) bundles.set(key,{from:from,to:to,kind:r.kind,certainty:r.record.certainty,directed:r.record.directed,numbers:[],ids:[]});
          bundles.get(key).numbers.push(r.number); bundles.get(key).ids.push(r.id);
        });
        const edges = Array.from(bundles.values());
        edges.forEach(function (e) {
          const a = local.get(e.from), b = local.get(e.to);
          const siblings = edges.filter(function (other) { return [other.from,other.to].sort().join('|') === [e.from,e.to].sort().join('|'); });
          const offset = (siblings.indexOf(e)-(siblings.length-1)/2)*34;
          const dx = b.x-a.x, dy = b.y-a.y, length = Math.hypot(dx,dy)||1;
          const ax = a.x+dx/length*16, ay = a.y+dy/length*16, bx = b.x-dx/length*20, by = b.y-dy/length*20;
          const orientation = e.from < e.to ? 1 : -1;
          let mx = (ax+bx)/2-dy/length*offset*orientation, my = (ay+by)/2+dx/length*offset*orientation;
          // Peripheral routes must not appear to stop at the central group.
          if (!small && !a.hub && !b.hub && Math.hypot(mx-cx,my-cy) < 180) {
            const distance = Math.hypot(mx-cx,my-cy);
            if (distance > 10) { mx += (mx-cx)/distance*300; my += (my-cy)/distance*300; }
            else { mx += -dy/length*300; my += dx/length*300; }
          }
          e.path = 'M '+ax+' '+ay+' Q '+mx+' '+my+' '+bx+' '+by;
          e.label = a.label+(e.directed ? ' → ' : ' ↔ ')+b.label+' · '+e.kind+' · '+e.certainty+' · '+e.numbers.map(function (n) { return 'R'+String(n).padStart(2,'0'); }).join(', ');
        });
        return {number:componentIndex+1,width:width,height:height,nodes:nodes,edges:edges,relations:relations.map(function (r) { return r.number; })};
      });
    }

    function stageStyle(level, status) {
      const styles = {
        'text-collated':{dash:'',width:3,label:'Text collated'},
        'primary-description':{dash:'',width:2,label:'Primary description'},
        'scholarly-description':{dash:'8 5',width:2,label:'Scholarly description'},
        'bibliographic-only':{dash:'2 5',width:2,label:'Bibliographic succession only'}
      };
      const style = styles[level] || styles['bibliographic-only'];
      return {dash:status === 'provisional' ? '2 7' : style.dash,width:style.width,
        label:style.label+(status === 'provisional' ? ' · provisional' : '')};
    }

    // A dated chart, not an ancestry layout: equal years share x coordinates.
    // Vertical subrows only prevent label collisions. Only source transitions
    // supply connecting paths; sorting never supplies a historical parent.
    function stageLayout(history, options) {
      options = options || {};
      const stages = history.stages || [], transitions = history.transitions || [];
      const stageKeys = new Map(stages.map(function (s,i) { return [s.id,'S'+String(i+1).padStart(3,'0')]; }));
      const transitionKeys = new Map(transitions.map(function (t,i) { return [t.id,'T'+String(i+1).padStart(3,'0')]; }));
      const byId = new Map(stages.map(function (s) { return [s.id,s]; }));
      const sourceKeys=new Map((history.sources || []).map(function (s,i) { return [s.id,'C'+String(i+1).padStart(3,'0')]; }));
      const selected = options.traditions || (options.tradition ? [options.tradition] : null);
      const traditions = (history.traditions || []).filter(function (t) { return !selected || selected.includes(t.id); });
      const traditionIds = new Set(traditions.map(function (t) { return t.id; }));
      const inLanes = stages.filter(function (s) { return traditionIds.has(s.tradition_id); });
      const eligible = inLanes.filter(function (s) { return options.includeProvisional || s.status === 'documented'; });
      const dated = eligible.filter(function (s) { return Number.isFinite(s.start_year) && Number.isFinite(s.end_year); });
      const allDated = stages.filter(function (s) { return Number.isFinite(s.start_year) && Number.isFinite(s.end_year) && (options.includeProvisional || s.status === 'documented'); });
      const min = allDated.length ? Math.min.apply(null,allDated.map(function (s) { return s.start_year; })) : null;
      const max = allDated.length ? Math.max.apply(null,allDated.map(function (s) { return s.end_year; })) : null;
      const start = Number.isFinite(options.start) ? options.start : min === null ? null : Math.floor(min/50)*50;
      let end = Number.isFinite(options.end) ? options.end : max === null ? null : Math.ceil(max/50)*50;
      if (end !== null && start !== null && end <= start) end = start+50;
      const width = Math.max(1000,options.width || 1600), x0 = 360, x1 = width-35;
      const x = function (year) { return x0+(year-start)/(end-start)*(x1-x0); };
      const clamp = function (value) { return Math.max(x0,Math.min(x1,value)); };
      const inWindow = start === null ? [] : dated.filter(function (s) { return s.end_year >= start && s.start_year <= end; });
      const visible = inWindow.filter(function (s) { return !options.stageIds || options.stageIds.includes(s.id); });
      const visibleIds=new Set(visible.map(function (s) { return s.id; }));
      const pairKey=function (a,b) { return JSON.stringify([a,b].sort()); };
      const pairCounts=new Map();
      transitions.forEach(function (t) {
        if ((!options.includeProvisional && t.status!=='documented') ||
            (!visibleIds.has(t.from_stage) && !visibleIds.has(t.to_stage))) return;
        const key=pairKey(t.from_stage,t.to_stage);
        pairCounts.set(key,(pairCounts.get(key) || 0)+1);
      });
      const nodeById = new Map(), cardWidth = 260, leading = 20;
      let top = 90;
      const lanes = traditions.map(function (tradition,laneIndex) {
        const rows = [];
        const nodes = visible.filter(function (s) { return s.tradition_id === tradition.id; })
          .sort(function (a,b) { return a.start_year-b.start_year || a.end_year-b.end_year || stages.indexOf(a)-stages.indexOf(b); })
          .map(function (stage) {
            const incoming = transitions.filter(function (t) { return t.to_stage === stage.id && (options.includeProvisional || t.status === 'documented'); })
              .map(function (t) { return {key:transitionKeys.get(t.id),transition:t}; });
            const year = (stage.start_year+stage.end_year)/2;
            const labelX = Math.max(x0,Math.min(x1-cardWidth,clamp(x(year))-20));
            const labelLines = wrapLabel(stage.label,26);
            const dateLines = wrapLabel(stage.date_label+' · '+stage.date_kind,34).concat(
              stage.start_year<start || stage.end_year>end ? ['Bounds continue beyond this window'] : []);
            const fullScopeLines = wrapLabel('Parts: '+(stage.components || []).join(', '),34);
            const scopeLines=options.compact && !options.inlineSummary ? [] : fullScopeLines;
            const coverageLines = wrapLabel((stage.status === 'provisional' ? 'Provisional lead' : 'Documented state')+' · text: '+stage.text_coverage,34);
            const fullChangeLines = incoming.flatMap(function (entry) {
              const transition=entry.transition;
              const origin=byId.get(transition.from_stage);
              const fromLines=origin ? wrapLabel('From '+stageKeys.get(origin.id)+' · '+
                (Number.isFinite(origin.start_year) ? origin.date_label : 'unpositioned')+' · '+origin.label,34) : [];
              const change=(transition.changes || [])[0];
              const excerpt=function (label,text) {
                const clipped=text.length>220;
                return wrapLabel(label+(clipped ? ' (excerpt)' : '')+': '+(clipped ? text.slice(0,217)+'…' : text),34);
              };
              const details=change ? excerpt('Before',change.before).concat(excerpt('After',change.after)) : [];
              if ((transition.changes || []).length>1) details.push('More components in transition detail.');
              const evidence=(transition.evidence || []).concat(change ? change.evidence || [] : []);
              const refs=Array.from(new Set(evidence.map(function (e) { return (sourceKeys.get(e.source_id) || e.source_id)+' · '+e.locus; })));
              return fromLines.concat(wrapLabel(entry.key+' · '+transition.kind.replace(/-/g,' ')+' · '+
                transition.evidence_level.replace(/-/g,' ')+(transition.status==='provisional' ? ' · provisional' : ''),34))
                .concat(wrapLabel(transition.summary,34),details,wrapLabel('Evidence: '+refs.join('; '),34));
            });
            const changeLines=options.compact
              ? (options.inlineSummary ? incoming.flatMap(function (entry) {
                const summary=entry.transition.summary;
                return wrapLabel(entry.key+' · '+(summary.length>180 ? summary.slice(0,177)+'… (excerpt)' : summary),34);
              }) : []) : fullChangeLines;
            const lineCount = labelLines.length+dateLines.length+scopeLines.length+coverageLines.length+changeLines.length;
            const cardHeight = 20+lineCount*leading+Math.max(0,incoming.length)*5;
            const left = Math.min(labelX,clamp(x(stage.start_year))), right = Math.max(labelX+cardWidth,clamp(x(stage.end_year)));
            let row = rows.findIndex(function (r) { return r.right+22 < left; });
            if (row < 0) { row=rows.length; rows.push({right:-Infinity,height:0,portClearance:0}); }
            rows[row].right=right; rows[row].height=Math.max(rows[row].height,cardHeight+55);
            const external=transitions.some(function (t) {
              return (options.includeProvisional || t.status==='documented') &&
                ((t.to_stage===stage.id && !visibleIds.has(t.from_stage)) || (t.from_stage===stage.id && !visibleIds.has(t.to_stage)));
            });
            if (external) rows[row].portClearance=45;
            transitions.forEach(function (t) {
              if (t.from_stage===stage.id || t.to_stage===stage.id) {
                const count=pairCounts.get(pairKey(t.from_stage,t.to_stage)) || 1;
                rows[row].portClearance=Math.max(rows[row].portClearance,(external ? 45 : 0)+(count-1)*32);
              }
            });
            return {id:stage.id,key:stageKeys.get(stage.id),stage:stage,row:row,x:clamp(x(year)),
              xStart:clamp(x(stage.start_year)),xEnd:clamp(x(stage.end_year)),
              clippedStart:stage.start_year<start,clippedEnd:stage.end_year>end,
              labelX:labelX,labelLines:labelLines,dateLines:dateLines,scopeLines:scopeLines,
              coverageLines:coverageLines,changeLines:changeLines,fullScopeLines:fullScopeLines,fullChangeLines:fullChangeLines,incoming:incoming,
              cardWidth:cardWidth,cardHeight:cardHeight,leading:leading};
          });
        const offsets=[]; let cursor=top+50;
        rows.forEach(function (r) { cursor+=r.portClearance; offsets.push(cursor); cursor+=r.height; });
        nodes.forEach(function (node) {
          node.y=offsets[node.row]; node.labelY=node.y+30; nodeById.set(node.id,node);
        });
        const height = Math.max(120,cursor-top+15);
        const lane = {id:tradition.id,label:tradition.label,tradition:tradition,index:(history.traditions || []).indexOf(tradition),
          top:top,height:height,nodes:nodes,labelLines:wrapLabel(tradition.label,27),
          visibleCount:nodes.length,totalCount:inLanes.filter(function (s) { return s.tradition_id===tradition.id; }).length};
        top+=height; return lane;
      });
      const edges = [], corridors=[], arcRows=new Map();
      transitions.forEach(function (transition) {
        if (!options.includeProvisional && transition.status !== 'documented') return;
        const fromNode=nodeById.get(transition.from_stage),toNode=nodeById.get(transition.to_stage);
        if (!fromNode && !toNode) return;
        const fromStage=byId.get(transition.from_stage),toStage=byId.get(transition.to_stage);
        if (!fromStage || !toStage) return;
        const port = function (stage,other) {
          const before = Number.isFinite(stage.end_year) && stage.end_year<start;
          const after = Number.isFinite(stage.start_year) && stage.start_year>end;
          const year=Number.isFinite(stage.start_year) && Number.isFinite(stage.end_year) ? (stage.start_year+stage.end_year)/2 : null;
          return {x:before ? x0 : after ? x1 : year===null ? other.x : clamp(x(year)),y:other.y-30};
        };
        const from=fromNode || port(fromStage,toNode),to=toNode || port(toStage,fromNode);
        const low=Math.min(from.y,to.y)-45,high=Math.max(from.y,to.y);
        let track=corridors.findIndex(function (ranges) { return ranges.every(function (r) { return high<r.low || low>r.high; }); });
        if (track<0) { track=corridors.length; corridors.push([]); }
        corridors[track].push({low:low,high:high});
        const gutter=x0-18-track*11;
        const clearance=22+(track%5)*5;
        const hasCorridor=fromNode && toNode && from.y!==to.y;
        const parallel=hasCorridor ? 0 : edges.filter(function (edge) {
          return pairKey(edge.from,edge.to)===pairKey(transition.from_stage,transition.to_stage);
        }).length;
        const sameRow=fromNode && toNode && from.y===to.y;
        let arcTrack=parallel;
        if (sameRow) {
          const tracks=arcRows.get(from.y) || [];
          const span={left:Math.min(from.x,to.x),right:Math.max(from.x,to.x)};
          let track=tracks.findIndex(function (ranges) {
            return ranges.every(function (r) { return span.right<r.left || span.left>r.right; });
          });
          if (track<0) { track=tracks.length; tracks.push([]); }
          tracks[track].push(span); arcRows.set(from.y,tracks); arcTrack=track;
        }
        const lift=Math.min(from.y,to.y)-28-arcTrack*32;
        const keyLabel=hasCorridor ? {x:gutter-5,y:(from.y+to.y)/2} : {x:(from.x+to.x)/2,y:sameRow ? from.y-3-arcTrack*24 : lift-5};
        const pairCount=pairCounts.get(pairKey(transition.from_stage,transition.to_stage)) || 1;
        const externalParallel=(!fromNode || !toNode) && from.x===to.x && pairCount>1;
        const side=from.x-x0>x1-from.x ? -1 : 1;
        const bend=from.x+side*(parallel+1)*60;
        if (externalParallel) {
          keyLabel.x=from.x+side*(parallel+1)*45+17;
          keyLabel.y=(from.y+to.y)/2+4;
        }
        if (hasCorridor) {
          const middle=keyLabel.y;
          const available=function (y) { return y>Math.min(from.y,to.y)+18 && y<Math.max(from.y,to.y)-18 &&
            edges.every(function (e) { return Math.abs(e.keyLabel.x-keyLabel.x)>=60 || Math.abs(e.keyLabel.y-y)>=24; }); };
          for (let offset=0;offset<Math.abs(from.y-to.y);offset+=24) {
            if (available(middle+offset)) { keyLabel.y=middle+offset; break; }
            if (available(middle-offset)) { keyLabel.y=middle-offset; break; }
          }
        }
        // Include the cubic extremum, key knockout and a four-unit paint margin.
        const arcBounds=sameRow ? {
          left:Math.min(from.x,to.x,keyLabel.x-43)-4,
          right:Math.max(from.x,to.x,keyLabel.x+3)+4,
          top:Math.min(from.y*.25+lift*.75-4,keyLabel.y-16),bottom:from.y+4
        } : null;
        // Three overlapping arcs fit the existing eighty-unit row band. Deeper
        // stacks need shared browser/print extent work; never silently clip them.
        if (arcBounds && arcBounds.top<from.y-80)
          throw Error('Chronology same-row arc tracks exceed the reserved row band: '+transitionKeys.get(transition.id));
        edges.push({id:transition.id,key:transitionKeys.get(transition.id),transition:transition,
          from:transition.from_stage,to:transition.to_stage,fromKey:stageKeys.get(transition.from_stage),toKey:stageKeys.get(transition.to_stage),
          fromStage:fromStage,toStage:toStage,fromPoint:{x:from.x,y:from.y},toPoint:{x:to.x,y:to.y},fromOutside:!fromNode,toOutside:!toNode,external:!fromNode || !toNode,
          keyLabel:keyLabel,arcTrack:sameRow ? arcTrack : null,arcBounds:arcBounds,
          path:fromNode && toNode && from.y!==to.y
            ? 'M '+from.x+' '+from.y+' V '+(from.y-clearance)+' H '+gutter+' V '+(to.y-clearance)+' H '+to.x+' V '+to.y
            : externalParallel
              ? 'M '+from.x+' '+from.y+' C '+bend+' '+from.y+' '+bend+' '+to.y+' '+to.x+' '+to.y
            : (!fromNode || !toNode) && from.x===to.x
              ? 'M '+from.x+' '+from.y+' L '+to.x+' '+to.y
              : 'M '+from.x+' '+from.y+' C '+from.x+' '+lift+' '+to.x+' '+lift+' '+to.x+' '+to.y,
          style:stageStyle(transition.evidence_level,transition.status)});
      });
      const ticks=[];
      if (start !== null) {
        const step=[1,5,10,25,50,100,200,500,1000,2000].find(function (s) { return (end-start)/s<=10; }) || 5000;
        for(let year=Math.ceil(start/step)*step;year<=end;year+=step) ticks.push({year:year,x:x(year)});
      }
      return {start:start,end:end,width:width,height:top+20,axis:{x0:x0,x1:x1,y:48,ticks:ticks},lanes:lanes,edges:edges,
        stageKeys:Object.fromEntries(stageKeys),transitionKeys:Object.fromEntries(transitionKeys),
        sourceKeys:Object.fromEntries((history.sources || []).map(function (s,i) { return [s.id,'C'+String(i+1).padStart(3,'0')]; })),
        unpositioned:eligible.filter(function (s) { return !Number.isFinite(s.start_year) || !Number.isFinite(s.end_year); }),
        provisional:inLanes.filter(function (s) { return s.status==='provisional'; }),
        counts:{visible:visible.length,dated:dated.length,outsideWindow:dated.length-inWindow.length,omittedFromPanel:inWindow.length-visible.length,
          documented:inLanes.filter(function (s) { return s.status==='documented'; }).length,
          provisional:inLanes.filter(function (s) { return s.status==='provisional'; }).length}};
    }

    function extent(at) {
      let cols = 0;
      let rows = 0;
      at.forEach(function (place) {
        if (place.col + 1 > cols) cols = place.col + 1;
        if (place.row + 1 > rows) rows = place.row + 1;
      });
      return { cols: cols, rows: rows };
    }

    /* ------------------------------------------------------------------------
     * Junctions — where two lines part, and what they parted from
     *
     * A fork's base needs no merge-base search: a station whose line differs from
     * its parent's line parted there, and the parent IS the shared base, by
     * construction. So this reads the same edges the map draws and computes no
     * table of its own. Where a MERGE's base is wanted -- the latest act two
     * differing parents both descend from -- that is `act-history commonality`'s
     * answer, taken from `git merge-base` against the emitted repository, and
     * this file does not compute a second one.
     * --------------------------------------------------------------------- */

    function childrenOf(stations) {
      const kids = new Map();
      (stations || []).forEach(function (station) {
        (station.parents || []).forEach(function (parent) {
          if (!kids.has(parent)) kids.set(parent, []);
          kids.get(parent).push(station.id);
        });
      });
      return kids;
    }

    /** Every station reachable downward from `from`, itself excluded. */
    function descendants(stations, from) {
      const kids = childrenOf(stations);
      const seen = new Set();
      const pending = (kids.get(from) || []).slice();
      while (pending.length) {
        const current = pending.pop();
        if (seen.has(current)) continue;
        seen.add(current);
        (kids.get(current) || []).forEach(function (child) { pending.push(child); });
      }
      return seen;
    }

    /**
     * What one line did after a given station, in the graph's own order.
     *
     * The BASE is not worked out here. `act-history` derives it from the act
     * graph and proves that derivation against `git merge-base` on the repository
     * it emits, and the map file carries the answer; a second search for it in
     * this file would be the two-tables defect with extra steps. This walks
     * downward from the base the file gives and reports which stations on a line
     * stand below it, which is reading the same edges the map draws.
     */
    function afterBase(stations, base, line) {
      const reach = descendants(stations, base);
      return (stations || [])
        .filter(function (station) { return station.line === line && reach.has(station.id); })
        .map(function (station) { return station.id; });
    }

    /* ------------------------------------------------------------------------
     * Names
     *
     * A station's short name is taken from its id rather than composed: the id is
     * the act's own slug, and the trailing year is already shown beneath it.
     * --------------------------------------------------------------------- */

    function shortName(id) {
      const parts = String(id).split('-');
      if (/^\d{4}$/.test(parts[parts.length - 1])) parts.pop();
      const words = parts.join(' ');
      return words.charAt(0).toUpperCase() + words.slice(1);
    }

    function year(date) {
      return String(date || '').slice(0, 4);
    }

    return {
        PROMULGATED: PROMULGATED,
        PRINTED: PRINTED,
        UNSTATED: UNSTATED,
        kindsAreStated: kindsAreStated,
        kindOf: kindOf,
        layout: layout,
        panelLayout: panelLayout,
        overviewModel: overviewModel,
        networkLayout: networkLayout,
        networkStyle: networkStyle,
        stageLayout: stageLayout,
        stageStyle: stageStyle,
        wrapLabel: wrapLabel,
        extent: extent,
        afterBase: afterBase,
        shortName: shortName,
        year: year
      };
  }());

  /* ------------------------------------------------------------------------
   * Where the map and its fragments live
   * --------------------------------------------------------------------- */

  /* One slice is drawn at a time, and which one is a parameter rather than a
   * fact about this file. The record is meant to grow past Holy Week, and a
   * second slice should be reachable by asking for it rather than by editing a
   * page. Everything below reads the file the slice names; nothing here knows
   * what is in it. */
  const MANIFEST = 'structure/act-history/index.json';
  const ASKED = new URLSearchParams(window.location.search).get('slice');
  let SLICE = '';
  let ROOT = '';
  const NS = 'http://www.w3.org/2000/svg';

  const COL = 190;   // horizontal distance between stations
  const ROW = 104;   // vertical distance between tracks
  const PAD = 68;

  const map = document.getElementById('map');
  const tally = document.getElementById('tally');
  const legend = document.getElementById('legend');
  const detail = document.getElementById('detail');
  const follow = document.getElementById('follow');
  const unitSelect = document.getElementById('unit-select');
  const indexButton = document.getElementById('unit-index-button');
  const unitView = document.getElementById('unit-view');
  const linesPanel = document.getElementById('lines');
  const linesView = document.getElementById('lines-view');

  // The whole history in this session: one promise per fragment, so a reader
  // who walks back and forth across the map pays for each station once.
  const fragments = new Map();

  function fragment(path) {
    if (!fragments.has(path)) fragments.set(path, T.loadJSON(path));
    return fragments.get(path);
  }

  let spine = null;
  let byId = new Map();
  let kindsStated = false;
  let selected = null;
  let openedUnit = null;
  const unitIndex = new Map();

  function svg(name, attrs) {
    const node = document.createElementNS(NS, name);
    for (const key of Object.keys(attrs || {})) node.setAttribute(key, String(attrs[key]));
    return node;
  }

  function nameOf(station) {
    return (station && (station.title || M.shortName(station.id))) || '';
  }

  function lineLabel(id) {
    const line = ((spine && spine.lines) || []).find(function (row) { return row.id === id; });
    return (line && line.label) || id;
  }

  // Only a declared reception changes the edge's meaning. A crossing or a
  // parent on another line alone is not evidence of reception.
  function receptionsOf(station) {
    return (station.receptions || []).filter(function (row) {
      return (station.parents || []).indexOf(row.from) !== -1;
    });
  }

  const RECEPTION_WORDS = {
    'translates-typical-edition': 'Translation of a typical edition',
    'receives-into-wider-use': 'Reception into wider use'
  };

  /* ------------------------------------------------------------------------
   * What this slice calls things
   *
   * The spine declares its base unit's word, its container's word, and the key
   * its containers arrive under. Nothing here invents any of the three. A page
   * that read `masses` and said "liturgies" regardless counted a Code's
   * divisions under a key its files do not carry — printing `undefined` for a
   * number it held, listing none of the 83 it was handed — and offered a reader
   * "follow this prayer" over a canon of the Code. The missal's words stay as
   * the fallback because a slice written before the vocabulary existed carries
   * none of them, and that slice is a missal.
   *
   * A SLICE THAT DECLARES THE GENERIC NOUN HAS DECLARED NOTHING. `unit` is the
   * word this page reaches for when it has NOT been told what a thing is, so
   * reading it back out of a file says no more than silence. A reader follows
   * a prayer through the Missal; a state fold shows recorded units, because
   * the record does not carry a complete missal. Neither label implies that
   * an indexed unit has been transcribed in full.
   * --------------------------------------------------------------------- */

  const DEFAULT_WORDS = { unit_word: 'unit', group_word: 'mass', group_key: 'masses' };
  // Nouns that name a category rather than a thing. A slice offering one of
  // these has told a reader nothing they did not have without it.
  const GENERIC_WORDS = ['unit', 'units', 'group', 'groups', 'item', 'items'];
  let words = { unit_named: '', group_named: '', group_key: DEFAULT_WORDS.group_key };

  /** What the slice SAID a thing is called, or '' where it said nothing. */
  function declaredWord(value) {
    const word = String(value || '').trim();
    return GENERIC_WORDS.indexOf(word.toLowerCase()) === -1 ? word : '';
  }

  function readVocabulary(data) {
    words = {
      unit_named: declaredWord(data && data.unit_word),
      group_named: declaredWord(data && data.group_word),
      group_key: (data && data.group_key) || DEFAULT_WORDS.group_key
    };
    return words;
  }

  /** The word for a base unit where counting it needs one either way. */
  function unitWord() {
    return words.unit_named || DEFAULT_WORDS.unit_word;
  }

  function groupWord() {
    return words.group_named || DEFAULT_WORDS.group_word;
  }

  /* What a reader follows through the record. Where the slice named its base
   * unit, that is the word; where it offered the generic, this page's own is
   * kept, because "follow this prayer" is what the Missal's reader is doing and
   * "follow this unit" would be a placeholder standing where a word had been. */
  function followWord() {
    return words.unit_named || 'prayer';
  }

  function plural(word) {
    if (/(?:s|x|z|ch|sh)$/.test(word)) return word + 'es';
    if (/[^aeiou]y$/.test(word)) return word.slice(0, -1) + 'ies';
    return word + 's';
  }

  /** A count and the word for what is counted, in the number the count needs. */
  function tallyOf(count, word) {
    return count + ' ' + (count === 1 ? word : plural(word));
  }

  /** The containers a fragment carries, under whichever key it keeps them. */
  function groupsIn(payload) {
    const held = payload && payload[words.group_key];
    return Array.isArray(held) ? held : [];
  }

  /** How many containers an act touched, under whichever key it counted them. */
  function groupsTouched(changed) {
    return (changed && changed[words.group_key + '_touched']) || 0;
  }

  /* ------------------------------------------------------------------------
   * The drawing
   * --------------------------------------------------------------------- */

  /* One bend at the octilinear 45°, covering the whole vertical change, with a
   * straight run into each end. A curve would suggest a gradual change where
   * the record has a single act; a diagonal that covered only part of the drop
   * would leave a kink that reads as a station nobody drew. Where the columns
   * are too close for 45°, the diagonal simply runs steeper — that is honest
   * about the crowding rather than overshooting into the next track. */
  function connector(from, to) {
    const x1 = PAD + from.col * COL;
    const y1 = PAD + from.row * ROW;
    const x2 = PAD + to.col * COL;
    const y2 = PAD + to.row * ROW;
    if (y1 === y2) return 'M ' + x1 + ' ' + y1 + ' L ' + x2 + ' ' + y2;
    const drop = Math.abs(y2 - y1);
    const run = Math.min(drop, Math.abs(x2 - x1));
    const a = x1 + (x2 - x1 - run) / 2;
    const b = a + run;
    return 'M ' + x1 + ' ' + y1 + ' L ' + a + ' ' + y1 + ' L ' + b + ' ' + y2 + ' L ' + x2 + ' ' + y2;
  }

  /* How many BASE UNITS an act moved. The containers it touched are not added
   * in: a liturgy is not a unit, and one unit entering a liturgy touches both,
   * so summing the two counted the same act twice and printed a number under
   * the station that answered to nothing — "42 changed" over a station whose
   * own summary said "38 entered, 4 liturgies touched". The containers are
   * counted, and said, separately. */
  function magnitude(station) {
    const changed = station.changed || {};
    return (changed.units_entered || 0) + (changed.units_gone || 0) +
      (changed.units_changed || 0) + (changed.unestablished || 0);
  }

  function draw() {
    const stations = spine.stations || [];
    T.clear(map);
    if (!stations.length) {
      map.appendChild(T.el('p', 'placeholder', 'This slice records no stations.'));
      map.setAttribute('aria-busy', 'false');
      return;
    }
    const panels = M.panelLayout(stations, spine.lines);
    map.setAttribute('aria-label', 'The acts this record carries: ' + stations.length + ' stations in dated line panels');
    map.appendChild(T.el('h2', null, 'Recorded historical lines'));
    map.appendChild(T.el('p', 'panel-note',
      'Read dates downward within each line. Spacing separates recorded stations, not elapsed years. ' +
      'Separate starting points mark the limits of this record, not independent historical origins. ' +
      'An ending here does not establish suppression or extinction.'));
    const contents = T.el('nav', 'line-index');
    contents.setAttribute('aria-label', 'Recorded line index');
    panels.forEach(function (panel) {
      const link = T.el('a', null, panel.number + '. ' + panel.label);
      link.href = '#' + panel.id;
      link.addEventListener('click', function (event) {
        event.preventDefault();
        document.getElementById(panel.id).scrollIntoView({block:'start'});
        document.getElementById(panel.id).focus();
      });
      contents.appendChild(link);
    });
    map.appendChild(contents);
    panels.forEach(function (panel) {
      const section = T.el('section', 'route-panel');
      section.id = panel.id;
      section.tabIndex = -1;
      section.appendChild(T.el('h3', null, panel.number + '. ' + panel.label));
      section.appendChild(T.el('p', 'panel-note', panel.nodes.length + ' recorded stations · ' +
        panel.nodes[0].date + ' – ' + panel.nodes[panel.nodes.length-1].date + ' · dates increase ↓'));
      const body = T.el('div', 'route-body');
      const canvas = svg('svg', {class:'route-geometry', width:panel.textX, height:panel.height,
        viewBox:'0 0 ' + panel.textX + ' ' + panel.height, 'aria-hidden':'true',
        'aria-label':'The acts this record carries: ' + stations.length + ' stations across the map; this panel is ' + panel.label});
      const labels = T.el('ol', 'route-labels');
      labels.style.marginLeft = panel.textX + 'px';
      panel.nodes.forEach(function (node) {
        const station = byId.get(node.id);
        const item = T.el('li', 'route-stop');
        item.setAttribute('data-label-for', node.id);
        item.appendChild(T.el('p', 'route-date', station.date + ' · ' + M.kindOf(station, kindsStated)));
        const button = T.el('button', 'station route-title' +
          (receptionsOf(station).length ? ' station-interchange' : ''));
        button.appendChild(T.el('span', 'route-title-text', station.title));
        const moved = magnitude(station);
        const count = M.kindOf(station, kindsStated) === M.PROMULGATED
          ? (moved ? moved + ' changed' : 'nothing changed')
          : (moved ? moved + ' differ' : 'nothing differs');
        const caption = T.el('span', 'route-count-caption', 'Recorded units: ');
        caption.appendChild(T.el('span', 'station-count', count));
        button.appendChild(caption);
        button.type = 'button';
        button.setAttribute('data-station', node.id);
        button.setAttribute('aria-label', station.title + ', ' + station.date + ', ' +
          M.kindOf(station, kindsStated) + ', ' + changeSummary(station) +
          (receptionsOf(station).length ? ', documented reception from ' +
          receptionsOf(station).map(function (r) { return byId.get(r.from).title; }).join('; ') : ''));
        button.addEventListener('click', function () { open(node.id); revealDetail(); });
        item.appendChild(button);
        const incoming = panel.edges.filter(function (edge) { return edge.to === node.id && edge.external; });
        incoming.forEach(function (edge) {
          const ref = T.el('a', 'route-reference',
            (edge.reception ? 'Reception from ' : 'Parent link from ') + edge.fromTitle + ' · line ' + edge.fromPanel);
          ref.href = '#station=' + encodeURIComponent(edge.from);
          ref.addEventListener('click', function (event) { event.preventDefault(); open(edge.from); revealDetail(); });
          item.appendChild(ref);
        });
        panels.forEach(function (other) {
          other.edges.filter(function (edge) { return edge.external && edge.from === node.id; }).forEach(function (edge) {
            const ref = T.el('a', 'route-reference', 'Linked to ' + edge.toTitle + ' · line ' + edge.toPanel);
            ref.href = '#station=' + encodeURIComponent(edge.to);
            ref.addEventListener('click', function (event) { event.preventDefault(); open(edge.to); revealDetail(); });
            item.appendChild(ref);
          });
        });
        if (station.parent_kind === 'use-continuity' || station.parent_kind === 'line-order') item.appendChild(
          T.el('p', 'route-reference', 'Sequence in this record; textual descent is not established by this link.'));
        if ((station.via_unrepresented || []).length) item.appendChild(T.el('p', 'route-reference',
          'Broken link: intervening edition or act not represented here.'));
        labels.appendChild(item);
      });
      body.appendChild(canvas);
      body.appendChild(labels);
      section.appendChild(body);
      map.appendChild(section);
      function paint() {
        const heights = {};
        Array.from(labels.children).forEach(function (item, i) {
          heights[panel.nodes[i].id] = item.getBoundingClientRect().height;
        });
        const measured = M.panelLayout(stations, spine.lines, heights).find(function (p) { return p.line === panel.line; });
        T.clear(canvas);
        canvas.setAttribute('height', measured.height);
        canvas.setAttribute('viewBox', '0 0 ' + measured.textX + ' ' + measured.height);
        measured.edges.forEach(function (edge) {
          const station = byId.get(edge.to);
          const classes = 'track track-evidence-' + (station.parent_kind || 'unstated') + (edge.reception ? ' track-reception' : '') +
            ((station.via_unrepresented || []).length ? ' track-gap' : '');
          const path = svg('path', {d:edge.path, class:classes, 'data-from':edge.from, 'data-to':edge.to,
            'aria-label': (edge.reception ? 'Documented reception' : 'Recorded parent link') +
              ' from ' + edge.fromTitle + ' to ' + edge.toTitle});
          canvas.appendChild(path);
          if (edge.reception) canvas.appendChild(svg('path', {d:edge.path, class:'track-reception-core'}));
        });
        measured.nodes.forEach(function (node) {
          const station = byId.get(node.id);
          const group = svg('g', {class:'kind-' + M.kindOf(station, kindsStated)});
          if (receptionsOf(station).length) group.appendChild(svg('circle', {cx:node.x,cy:node.y,r:14,class:'station-interchange-ring'}));
          group.appendChild(svg('circle', {cx:node.x,cy:node.y,r:8,class:'station-mark'}));
          canvas.appendChild(group);
        });
      }
      paint();
      if (typeof ResizeObserver !== 'undefined') new ResizeObserver(paint).observe(labels);
    });
    map.setAttribute('aria-busy', 'false');
  }

  /* What the count under a station means depends on what kind of station it is.
   * At a promulgated station an authority changed the book, and `changed` is
   * the right word. At a printed one nobody has located an act, so the count is
   * a difference between what two books hold and no more than that. Printing
   * the same word over both would launder the weaker claim into the stronger. */
  function changeSummary(station) {
    const changed = station.changed;
    if (!changed) return 'what it changed is not carried in this file';
    if (M.kindOf(station, kindsStated) !== M.PROMULGATED) {
      const moved = magnitude(station);
      if (!moved) return 'nothing in this slice differs from what stood before';
      return moved + (moved === 1 ? ' difference' : ' differences') +
        ' from what stood before, with no act behind them';
    }
    const parts = [];
    if (changed.units_entered) parts.push(changed.units_entered + ' entered');
    if (changed.units_gone) parts.push(changed.units_gone + ' gone');
    if (changed.units_changed) parts.push(changed.units_changed + ' altered');
    const touched = groupsTouched(changed);
    if (touched) parts.push(tallyOf(touched, groupWord()) + ' touched');
    if (changed.unestablished) parts.push(changed.unestablished + ' left unestablished');
    if (!parts.length) return 'nothing in this slice changed here';
    return parts.join(', ');
  }

  /* ------------------------------------------------------------------------
   * The station panel
   * --------------------------------------------------------------------- */

  function section(title) {
    const node = T.el('section', 'detail-section');
    node.appendChild(T.el('h3', 'detail-section-title', title));
    return node;
  }

  /* Every value `act_citation` takes, glossed. `none-claimed` was missing here
   * and present in `law.js`, and this table is a copy of that one: 26 of the 59
   * stations in the default slice are printed stations whose `act_citation` is
   * `none-claimed`, and every one of them rendered `none-claimed — ` with
   * nothing after the dash. The wording is `law.js`'s, unchanged, because the
   * two pages gloss one vocabulary and must not gloss it two ways. It is also
   * the distinction the record insists on: `none-claimed` is NOT `not-found` —
   * not-found means an instrument is believed to exist and nobody has read it;
   * none-claimed means no instrument is asserted at all, which is what a
   * printed station says and the only value such a station may carry
   * (guidance/act-histories.md, section 10). */
  const CITATION_WORDS = {
    'cited-in-corpus': 'the instrument was read in this project’s own corpus',
    'cited-externally': 'the instrument was read, in a witness held elsewhere',
    'not-found': 'the instrument was searched for and not found',
    'none-claimed': 'no instrument is claimed at all'
  };

  function facts(station) {
    const kind = M.kindOf(station, kindsStated);
    const rows = [
      ['Date', station.date + (station.date_precision && station.date_precision !== 'day'
        ? ' (' + station.date_precision + ')' : '')],
      ['Station', kind],
      ['Authority', station.authority],
      ['Instrument', station.instrument],
      ['Act', station.kind],
      ['Printing', station.printing],
      ['Line', lineLabel(station.line)],
      ['Descent', station.parent_kind],
      ['Instrument read', station.act_citation
        ? station.act_citation + ' — ' + (CITATION_WORDS[station.act_citation] || '')
        : null],
      ['Citation', station.citation],
      ['Effect', station.effect
        ? station.effect + (station.effect_established
          ? '' : ' (what it changed here is not established)')
        : null]
    ];
    const list = T.el('dl', 'detail-list');
    rows.forEach(function (row) {
      if (!row[1]) return;
      list.appendChild(T.el('dt', null, row[0]));
      list.appendChild(T.el('dd', null, String(row[1])));
    });
    return list;
  }

  /** What a word in the record means, said once, where it is used. */
  function kindNote(kind) {
    if (kind === M.PRINTED) {
      // NOT "a missal survives". This page draws whatever act-keyed slice it
      // is handed, and on the Code slice the artifact behind a printed station
      // is Friedberg's Decretum or the Editio Romana — calling either one a
      // missal is simply false. The slice declares no word for the artifact
      // and none is invented here: what every printed station does carry, and
      // what `act-history check` requires of it, is the PRINTING it stands on,
      // which is the word the row above already prints.
      return T.el('p', 'detail-weak',
        'A printed station. The printing it stands on survives and no act has ' +
        'been located for it, so nothing here claims one. That is a statement ' +
        'about the evidence and not about the size of the change: the printing ' +
        'is present, the instrument is missing.');
    }
    if (kind === M.UNSTATED) {
      return T.el('p', 'detail-weak',
        'This file states which kind the other stations are and states nothing ' +
        'for this one, so it is left unsaid rather than assumed.');
    }
    return null;
  }

  /* Three states, never two. Words present; words this record never read; and
   * words that exist and may not be printed here. A renderer that showed the
   * last two alike would tell a reader nobody had looked, which is false, or
   * that the prayer was blank, which is worse. */
  function value(text, missing, withheld) {
    if (text) return T.el('span', 'value', text);
    if (withheld) {
      return T.el('span', 'value value-absent', 'withheld here: ' + withheld);
    }
    return T.el('span', 'value value-absent', missing);
  }

  const FIELD_NAMES = {
    mass: 'liturgy', slot: 'place', name: 'heading', incipit: 'incipit',
    text: 'text', order: 'order', title: 'title', day: 'day', hour: 'hour',
    withheld: 'withheld because'
  };

  function fieldRow(field, before, after, wasSide, nowSide) {
    const row = T.el('div', 'change-field');
    row.appendChild(T.el('span', 'change-field-name', FIELD_NAMES[field] || field));
    const pair = T.el('div', 'change-field-pair');
    const long = field === 'text' || field === 'incipit';
    const missing = long
      ? 'this record does not carry these words'
      : 'not established';
    const shown = function (raw, side) {
      const text = raw === undefined || raw === null ? '' : String(raw);
      return value(text, missing, long ? (side || {}).withheld : '');
    };
    const was = T.el('div', 'change-field-side change-field-before');
    was.appendChild(shown(before, wasSide));
    const now = T.el('div', 'change-field-side change-field-after');
    now.appendChild(shown(after, nowSide));
    pair.appendChild(was);
    pair.appendChild(T.el('div', 'change-field-arrow', '→'));
    pair.appendChild(now);
    if (long) pair.className = 'change-field-pair change-field-pair-long';
    row.appendChild(pair);
    return row;
  }

  const STATE_WORDS = {
    entered: 'enters the record',
    gone: 'leaves the liturgy',
    changed: 'altered'
  };

  function whatHappened(row) {
    if (row.kinds && row.kinds.length) return row.kinds.join(', ');
    if (row.state === 'entered') {
      // No departure stands behind it: this is the earliest act for which the
      // tracer read the unit, which is a statement about the reading and not a
      // claim that the act introduced it.
      return 'first carried here';
    }
    return STATE_WORDS[row.state] || row.state;
  }

  function citations(row) {
    const held = (row.cited || []).filter(function (entry) { return entry.basis || entry.note; });
    if (!held.length) return null;
    const wrap = T.el('div', 'basis');
    held.forEach(function (entry) {
      const block = T.el('p', 'basis-entry');
      block.appendChild(T.el('span', 'basis-kind', entry.kind || 'basis'));
      block.appendChild(document.createTextNode(' ' + (entry.basis || entry.note)));
      wrap.appendChild(block);
    });
    return wrap;
  }

  function unitCard(row) {
    const card = T.el('article', 'change change-' + row.state);
    const head = T.el('h4', 'change-head');
    const after = row.after || {};
    const before = row.before || {};
    head.appendChild(T.el('span', 'change-title', after.name || before.name || row.unit));
    head.appendChild(T.el('span', 'change-kinds', whatHappened(row)));
    card.appendChild(head);
    card.appendChild(T.el('p', 'change-where',
      (after.mass || before.mass || '') + ' · ' + (after.slot || before.slot || '') +
      ' · ' + row.unit));

    if (row.state === 'changed') {
      (row.fields || []).forEach(function (field) {
        card.appendChild(fieldRow(field, before[field], after[field], before, after));
      });
      if (!(row.fields || []).length) {
        card.appendChild(T.el('p', 'detail-weak',
          'The act records a departure here and the state it leaves is the same ' +
          'in every field this record carries.'));
      }
    } else {
      const side = row.state === 'gone' ? before : after;
      card.appendChild(standing(side));
    }

    // Rule 3 of guidance/recensions.md on screen: where an act left a unit's
    // state unestablished, the marker prints in place of the inherited words.
    if (row.marker) card.appendChild(T.el('pre', 'marker', row.marker));

    const basis = citations(row);
    if (basis) card.appendChild(basis);

    const link = T.el('button', 'link-button', 'Follow this ' + followWord());
    link.type = 'button';
    link.addEventListener('click', function () { openUnit(row.unit); });
    card.appendChild(link);
    return card;
  }

  /** One side of a unit, printed whole — used where there is no other side. */
  function standing(side) {
    const wrap = T.el('div', 'standing');
    const line = T.el('p', 'standing-incipit');
    line.appendChild(value(side.incipit || '',
      'this record does not carry these words', side.withheld));
    wrap.appendChild(line);
    if (side.text) wrap.appendChild(T.el('p', 'standing-text', side.text));
    return wrap;
  }

  function massCard(row) {
    const card = T.el('article', 'change change-' + row.state);
    const head = T.el('h4', 'change-head');
    const after = row.after || {};
    const before = row.before || {};
    head.appendChild(T.el('span', 'change-title', after.title || before.title || row.mass));
    head.appendChild(T.el('span', 'change-kinds', whatHappened(row)));
    card.appendChild(head);
    card.appendChild(T.el('p', 'change-where', row.mass));
    (row.fields || []).forEach(function (field) {
      card.appendChild(fieldRow(field, before[field], after[field]));
    });
    const basis = citations(row);
    if (basis) card.appendChild(basis);
    return card;
  }

  const EDGE_WORDS = {
    root_basis: 'Why the record starts here',
    parent_basis: 'Why it descends from what it descends from',
    reception_basis: 'The reception this merge asserts',
    via_unrepresented_basis: 'What sits in the gap',
    printing_basis: 'What is known of this printing',
    act_citation_note: 'On the instrument'
  };

  function renderReceptions(host, rows) {
    T.clear(host);
    host.appendChild(T.el('h3', 'detail-section-title', 'Documented reception'));
    host.appendChild(T.el('p', 'detail-weak',
      'These links record reception between lines. They carry ancestry, not a ' +
      'copy of the received parent’s text; this station’s own changes are shown below.'));
    rows.forEach(function (row) {
      const head = T.el('h4', 'edge-title', 'Receives from ');
      head.appendChild(stationLink(row.from));
      host.appendChild(head);
      const list = T.el('dl', 'detail-list');
      [['Relationship', RECEPTION_WORDS[row.kind] || row.kind],
        ['Instrument', row.instrument], ['Citation', row.citation], ['Basis', row.basis]]
        .forEach(function (entry) {
          if (!entry[1]) return;
          list.appendChild(T.el('dt', null, entry[0]));
          list.appendChild(T.el('dd', null, entry[1]));
        });
      host.appendChild(list);
    });
  }

  function renderChanges(host, payload, station) {
    T.clear(host);
    const totals = payload.totals || {};
    host.appendChild(T.el('p', 'detail-summary', changeSummary(station) + '.'));

    // A printed station's diff is a difference between two books, and this
    // project's own measurement of that is unsparing: a comparison of two text
    // layers is worth nothing on its own as evidence about the printings, and
    // is worth something only where an act stands behind it. So the caveat is
    // printed above the differences rather than left for a reader to supply.
    if (M.kindOf(station, kindsStated) !== M.PROMULGATED) {
      host.appendChild(T.el('p', 'detail-weak',
        'No act has been located for this station, so nothing below was ordered ' +
        'by anybody as far as this record knows. What is shown is how this book ' +
        'differs from the one before it — a difference between printings, which ' +
        'is a far weaker thing than a change an authority made, and is not ' +
        'evidence that anyone decided it.'));
    }

    const edges = payload.edges || {};
    const named = Object.keys(EDGE_WORDS).filter(function (key) { return edges[key]; });
    if (named.length) {
      const block = section('On what this station rests');
      named.forEach(function (key) {
        block.appendChild(T.el('h4', 'edge-title', EDGE_WORDS[key]));
        block.appendChild(T.el('p', 'edge-basis', edges[key]));
      });
      host.appendChild(block);
    }

    const groups = groupsIn(payload);
    if (groups.length) {
      const block = section('The ' + plural(groupWord()));
      groups.forEach(function (row) { block.appendChild(massCard(row)); });
      host.appendChild(block);
    }
    if (payload.units && payload.units.length) {
      const block = section('The ' + plural(unitWord()));
      payload.units.forEach(function (row) { block.appendChild(unitCard(row)); });
      host.appendChild(block);
    }
    if (payload.unestablished && payload.unestablished.length) {
      const block = section('Left unestablished');
      block.appendChild(T.el('p', 'detail-weak',
        'The act is known to have acted on these and this record does not know ' +
        'what it left. They are removed rather than carried forward, because ' +
        'carrying them forward would assert that nothing changed.'));
      payload.unestablished.forEach(function (row) {
        const card = T.el('article', 'change change-unestablished');
        card.appendChild(T.el('h4', 'change-head', row.unit));
        card.appendChild(T.el('pre', 'marker', row.marker));
        card.appendChild((function () {
          const link = T.el('button', 'link-button', 'Follow this ' + followWord());
          link.type = 'button';
          link.addEventListener('click', function () { openUnit(row.unit); });
          return link;
        }()));
        block.appendChild(card);
      });
      host.appendChild(block);
    }
    if (!groups.length && !(payload.units || []).length &&
        !(payload.unestablished || []).length) {
      const standing = totals.standing || 0;
      const held = tallyOf(standing, unitWord()) +
        (standing === 1 ? ' stands after it.' : ' stand after it.');
      host.appendChild(T.el('p', 'detail-weak',
        M.kindOf(station, kindsStated) === M.PROMULGATED
          ? 'This act moved nothing in this slice. It keeps its station because ' +
            'an authority acted: a history keyed on diffs would have dropped it, ' +
            'and a history keyed on acts records that the authority spoke and ' +
            'this part of the book did not move. ' + held
          : 'Nothing in this slice differs from what stood before. The book is ' +
            'here because it survives, and this part of it reads as the last one ' +
            'did. ' + held));
    }
  }

  function renderState(host, payload) {
    T.clear(host);
    const totals = payload.totals || {};
    const groups = groupsIn(payload);
    host.appendChild(T.el('p', 'detail-summary',
      tallyOf(totals.units || 0, unitWord()) + ' across ' +
      tallyOf(totals[words.group_key] || 0, groupWord()) +
      ', as this record holds them after ' + payload.title + '.'));
    host.appendChild(T.el('p', 'detail-weak',
      'These counts describe recorded units, not complete transcriptions. ' +
      'A unit may carry only its heading or incipit; unread and withheld words ' +
      'are marked where the text would stand.'));
    if (payload.station_kind && payload.station_kind !== M.PROMULGATED) {
      host.appendChild(T.el('p', 'detail-weak',
        'This is what the surviving book prints at this point. No act stands ' +
        'behind it in this record, so it is a state witnessed and not a state ' +
        'ordered.'));
    }
    groups.forEach(function (mass) {
      const block = T.el('section', 'mass');
      block.appendChild(T.el('h4', 'mass-title',
        mass.title || mass[groupWord()] || ''));
      const meta = [mass.day, mass.hour].filter(Boolean).join(' · ');
      if (meta) block.appendChild(T.el('p', 'mass-meta', meta));
      if (!(mass.units || []).length) {
        block.appendChild(T.el('p', 'detail-weak',
          'This record carries no ' + unitWord() + ' standing in this ' +
          groupWord() + ' at this point.'));
      }
      (mass.units || []).forEach(function (unit) {
        const row = T.el('article', 'held');
        const head = T.el('h5', 'held-name');
        head.appendChild(document.createTextNode(unit.name || unit.slot));
        head.appendChild(T.el('span', 'held-slot', unit.slot));
        row.appendChild(head);
        const line = T.el('p', 'held-incipit');
        line.appendChild(value(unit.incipit || '',
          'this record read the heading of this unit and not its words',
          unit.withheld));
        row.appendChild(line);
        if (unit.text) row.appendChild(T.el('p', 'held-text', unit.text));
        const link = T.el('button', 'link-button', 'Follow this ' + followWord());
        link.type = 'button';
        link.addEventListener('click', function () { openUnit(unit.unit); });
        row.appendChild(link);
        block.appendChild(row);
      });
      host.appendChild(block);
    });
    if ((payload.unestablished || []).length) {
      const block = section('Not established at this point');
      payload.unestablished.forEach(function (row) {
        block.appendChild(T.el('pre', 'marker', row.marker));
      });
      host.appendChild(block);
    }
  }

  /** A fold that fetches its own fragment the first time it is opened. */
  function lazyBlock(summaryText, path, render) {
    const block = T.el('details', 'fold');
    const summary = T.el('summary', 'fold-summary', summaryText);
    block.appendChild(summary);
    const host = T.el('div', 'fold-body');
    const progress=T.el('p','panel-note fragment-status');
    progress.setAttribute('role','status'); progress.setAttribute('aria-live','polite');
    block.appendChild(progress);
    host.appendChild(T.el('p', 'placeholder', 'Not fetched yet.'));
    block.appendChild(host);
    let started = false;
    block.addEventListener('toggle', function () {
      if (!block.open || started) return;
      started = true;
      progress.textContent='Loading source text…'; host.setAttribute('aria-busy','true');
      T.clear(host);
      host.appendChild(T.el('p', 'placeholder', 'Loading…'));
      fragment(path).then(function (payload) {
        if (block.isConnected === false) return;
        render(host, payload);
        host.setAttribute('aria-busy','false'); progress.textContent='Source text loaded.';
      }).catch(function (error) {
        if (block.isConnected === false) return;
        T.clear(host);
        host.appendChild(T.el('p', 'error',
          path + ' could not be read: ' + String(error.message || error)));
        host.setAttribute('aria-busy','false'); progress.textContent='Source text could not be loaded.';
      });
    });
    return block;
  }

  /**
   * A station id this record does not carry.
   *
   * It is NOT the newest station. Falling through to the last row answered a
   * stale or mistyped citation with a real act and then rewrote the hash to
   * name that act, so the address bar came to agree with a page the reader had
   * never asked for and nothing on screen said the citation had failed. This
   * refuses in the same terms the law page refuses a canon its record does not
   * carry: the id is quoted back, nothing is opened, and nothing is written to
   * the hash, so the link the reader followed stays exactly as they sent it.
   */
  function reportUnknownStation(id) {
    selected = null;
    Array.prototype.forEach.call(document.querySelectorAll('.station'), function (node) {
      node.classList.remove('station-selected');
    });
    T.clear(detail);
    detail.hidden = false;
    detail.appendChild(T.el('h2', 'detail-title', id));
    detail.appendChild(T.el('p', 'error',
      'This record carries no station with the id “' + id + '”. That is a ' +
      'statement about this record and not about the history: nothing here ' +
      'hands you a neighbouring act instead, because a neighbouring act is a ' +
      'different act.'));
    T.statusLine('This record carries no station with the id ' + id + '.');
  }

  function revealDetail() {
    detail.tabIndex = -1;
    detail.scrollIntoView({block:'start'});
    detail.focus();
  }

  function open(id) {
    const station = byId.get(id);
    if (!station) return;
    selected = id;
    Array.prototype.forEach.call(document.querySelectorAll('.station'), function (node) {
      node.classList.toggle('station-selected', node.getAttribute('data-station') === id);
    });

    T.clear(detail);
    detail.hidden = false;
    const returnToMap = T.el('button', 'link-button', 'Back to this station on the map');
    returnToMap.type = 'button';
    returnToMap.addEventListener('click', function () {
      const button = Array.from(document.querySelectorAll('.route-title')).find(function (node) {
        return node.getAttribute('data-station') === id;
      });
      if (button) { button.scrollIntoView({block:'center'}); button.focus(); }
    });
    detail.appendChild(returnToMap);
    detail.appendChild(T.el('h2', 'detail-title', nameOf(station)));
    detail.appendChild(facts(station));
    const received = receptionsOf(station);
    const receptionHost = received.length ? T.el('section', 'detail-section detail-receptions') : null;
    if (receptionHost) {
      renderReceptions(receptionHost, received);
      detail.appendChild(receptionHost);
    }
    const note = kindNote(M.kindOf(station, kindsStated));
    if (note) detail.appendChild(note);
    if ((station.via_unrepresented || []).length) {
      detail.appendChild(T.el('p', 'detail-gap',
        'The descent into this station runs through ' +
        station.via_unrepresented.join(', ') +
        ', which this record does not carry. The connector is drawn broken for ' +
        'that reason: the edge means “descends from”, not “immediately follows”.'));
    }
    if ((station.departures || []).length) {
      detail.appendChild(T.el('p', 'detail-departures',
        'Departures recorded at this act: ' + station.departures.join(', ') + '.'));
    }

    if ((station.parents || []).length > 1) {
      const note = T.el('p', 'detail-weak');
      note.appendChild(document.createTextNode(
        'This station records ' + station.parents.length + ' parents. Its own ' +
        'changes are shown below; the parent stations are '));
      station.parents.forEach(function (parent, index) {
        if (index) note.appendChild(document.createTextNode(index === station.parents.length - 1
          ? ' and ' : ', '));
        note.appendChild(stationLink(parent));
      });
      note.appendChild(document.createTextNode('.'));
      detail.appendChild(note);
    }

    // The generator names the fragment; the page never composes its path. Two
    // naming rules is one naming rule too many.
    const changes = T.el('div', 'detail-changes');
    changes.appendChild(T.el('p', 'placeholder', 'Loading what changed…'));
    detail.appendChild(changes);
    if (station.station_path) {
      fragment('structure/act-history/' + station.station_path).then(function (payload) {
        if (receptionHost && (payload.edges || {}).receptions) {
          renderReceptions(receptionHost, payload.edges.receptions);
        }
        renderChanges(changes, payload, station);
      }).catch(function (error) {
        T.clear(changes);
        changes.appendChild(T.el('p', 'error',
          'What changed here could not be read: ' + String(error.message || error)));
      });
    } else {
      T.clear(changes);
      changes.appendChild(T.el('p', 'detail-weak',
        'This map file names no change set for this station, so none is shown. ' +
        'Working one out here would be a second answer to a question the ' +
        'generator already answers.'));
    }

    if (station.state_path) {
      detail.appendChild(lazyBlock(
        words.unit_named
          ? 'Read the ' + plural(words.unit_named) + ' as they stood after this act'
          : 'Read the recorded units as they stood after this act',
        'structure/act-history/' + station.state_path,
        renderState));
    }

    T.statusLine(nameOf(station) + ': ' + changeSummary(station));
    T.writeHash([['station', id], ['unit', openedUnit]]);
  }

  /* ------------------------------------------------------------------------
   * One prayer through time
   * --------------------------------------------------------------------- */

  function renderUnit(payload) {
    T.clear(unitView);
    const head = T.el('p', 'detail-summary');
    head.appendChild(document.createTextNode(
      (payload.name || payload.unit) + ' — ' +
      payload.stations.length + ' act' + (payload.stations.length === 1 ? '' : 's') +
      ' touched it. It enters this record at ' + payload.entered_at + '. '));
    head.appendChild(document.createTextNode(payload.standing
      ? 'It still stands at the end of the line drawn here.'
      : 'It leaves the liturgy at ' + payload.left_at + '.'));
    unitView.appendChild(head);

    payload.stations.forEach(function (stop) {
      const card = T.el('article', 'stop change-' + stop.state);
      const title = T.el('h4', 'change-head');
      title.appendChild(T.el('span', 'change-title', stop.title || stop.act));
      title.appendChild(T.el('span', 'change-kinds', whatHappened(stop)));
      card.appendChild(title);
      card.appendChild(T.el('p', 'change-where',
        stop.date + ' · ' + (stop.instrument || 'instrument not carried here')));
      if (stop.state === 'changed') {
        (stop.fields || []).forEach(function (field) {
          card.appendChild(fieldRow(field, (stop.before || {})[field],
            (stop.after || {})[field], stop.before, stop.after));
        });
      } else {
        card.appendChild(standing(stop.state === 'gone' ? (stop.before || {}) : (stop.after || {})));
      }
      const basis = citations(stop);
      if (basis) card.appendChild(basis);
      const go = T.el('button', 'link-button', 'Go to this station');
      go.type = 'button';
      go.addEventListener('click', function () {
        open(stop.act);
        detail.scrollIntoView({ block: 'start' });
      });
      card.appendChild(go);
      unitView.appendChild(card);
    });
  }

  function openUnit(id) {
    openedUnit = id;
    follow.hidden = false;
    T.clear(unitView);
    unitView.appendChild(T.el('p', 'placeholder', 'Loading ' + id + '…'));
    const row = unitIndex.get(id);
    const path = row && row.path ? row.path : SLICE + '/unit/' + id + '.json';
    fragment('structure/act-history/' + path).then(renderUnit).catch(function (error) {
      T.clear(unitView);
      unitView.appendChild(T.el('p', 'error',
        'That unit’s history could not be read: ' + String(error.message || error)));
    });
    if (unitSelect.value !== id) unitSelect.value = id;
    T.writeHash([['station', selected], ['unit', id]]);
    follow.scrollIntoView({ block: 'nearest' });
  }

  /* The index of every unit is itself a file, and it grows with the record, so
   * it is fetched when a reader asks to browse rather than at load. Following a
   * prayer from a station needs no index at all: that path is on the row the
   * station already carries. */
  let indexPending = null;

  function loadIndex() {
    if (indexPending) return indexPending;
    indexButton.hidden = true;
    indexPending = fragment(ROOT + '/units.json').then(function (payload) {
      const units = payload.units || [];
      units.forEach(function (unit) { unitIndex.set(unit.unit, unit); });
      T.fillSelect(unitSelect, units.map(function (unit) {
        return {
          value: unit.unit,
          group: unit.mass,
          label: (unit.name || unit.slot) + ' — ' + unit.slot +
            (unit.standing ? '' : ' (absent by ' + unit.left_at + ')')
        };
      }));
      unitSelect.disabled = !units.length;
      return units;
    });
    return indexPending;
  }

  function fillUnits() {
    follow.hidden = false;
    unitSelect.addEventListener('change', function () { openUnit(unitSelect.value); });
    const wake = function () {
      loadIndex().catch(function (error) {
        T.clear(unitView);
        unitView.appendChild(T.el('p', 'error',
          'The unit index could not be read: ' + String(error.message || error)));
      });
    };
    ['mousedown', 'focus', 'keydown'].forEach(function (event) {
      unitSelect.addEventListener(event, wake);
    });
    indexButton.addEventListener('click', wake);
  }

  /* ------------------------------------------------------------------------
   * Where the lines part
   *
   * A fork's shared base is its parent, by construction, so this needs no table
   * and computes none: it reads the same edges the map draws, and points at the
   * base station's own state for what the two lines held in common.
   * --------------------------------------------------------------------- */

  function stationLink(id) {
    const button = T.el('button', 'link-button', nameOf(byId.get(id)) || id);
    button.type = 'button';
    button.addEventListener('click', function () {
      open(id);
      detail.scrollIntoView({ block: 'start' });
    });
    return button;
  }

  function sideOfJunction(base, line) {
    const block = T.el('div', 'junction-side');
    const stations = spine.stations || [];
    block.appendChild(T.el('h4', 'junction-side-title', lineLabel(line)));
    // With no shared base there is nothing to stand below, so the line is shown
    // whole: what it holds is what it holds independently.
    const after = base
      ? M.afterBase(stations, base, line)
      : stations.filter(function (station) { return station.line === line; })
        .map(function (station) { return station.id; });
    if (!after.length) {
      block.appendChild(T.el('p', 'detail-weak',
        'Nothing below the base stands on this line in this record. An empty ' +
        'branch that is honestly empty measures what this corpus holds, not ' +
        'what happened.'));
      return block;
    }
    const list = T.el('ul', 'junction-list');
    after.forEach(function (id) {
      const item = T.el('li', null);
      item.appendChild(stationLink(id));
      const station = byId.get(id);
      item.appendChild(T.el('span', 'junction-count', station ? changeSummary(station) : ''));
      list.appendChild(item);
    });
    block.appendChild(list);
    return block;
  }

  function renderJunctions() {
    const pairs = spine.commonality || [];
    T.clear(linesView);
    linesPanel.hidden = false;
    if (!pairs.length) {
      linesView.appendChild(T.el('p', 'detail-weak',
        'This record holds one line, so there is no pair to compare.'));
      return;
    }
    const unconnected = pairs.filter(function (pair) { return !(pair.shared_base || []).length; });
    if (unconnected.length) {
      const fold = T.el('details', 'unconnected-pairs');
      fold.appendChild(T.el('summary', null, unconnected.length + ' line pairs have no shared act recorded'));
      fold.appendChild(T.el('p', 'panel-note', 'Earlier ancestry and shared wording are not established by this graph. ' +
        'These are gaps in the encoded evidence, not proof of isolation. The traditions and connections overview ' +
        'carries separate source-cited research claims and bounded text comparisons.'));
      const list = T.el('ul', null);
      unconnected.forEach(function (pair) {
        list.appendChild(T.el('li', null, lineLabel(pair.a) + ' / ' + lineLabel(pair.b)));
      });
      fold.appendChild(list);
      linesView.appendChild(fold);
    }
    pairs.filter(function (pair) { return (pair.shared_base || []).length; }).forEach(function (pair) {
      const card = T.el('article', 'junction');
      card.appendChild(T.el('h3', 'junction-head',
        lineLabel(pair.a) + ' and ' + lineLabel(pair.b)));

      const bases = pair.shared_base || [];
      const parted = pair.diverged_at || bases[bases.length - 1];
      const base = T.el('p', 'junction-base');
      base.appendChild(document.createTextNode(
        'The last act both lines descend from is '));
      base.appendChild(stationLink(parted));
      base.appendChild(document.createTextNode(
        '. This is shared ancestry in the recorded graph. A reception does ' +
        'not copy text between lines, so a shared ancestor alone does not ' +
        'establish identical texts. The stations below show each line’s later record.'));
      card.appendChild(base);
      if (bases.length > 1) {
        card.appendChild(T.el('p', 'detail-weak',
          'This pair has more than one best common ancestor — ' +
          bases.join(', ') + ' — which means the descent above them is itself ' +
          'branched. All of them are shown as bases rather than one being ' +
          'picked.'));
      }

      card.appendChild(sideOfJunction(parted, pair.a));
      card.appendChild(sideOfJunction(parted, pair.b));

      const at = byId.get(parted);
      if (at && at.state_path) {
        card.appendChild(lazyBlock(
          'Read the recorded state at this shared ancestor',
          'structure/act-history/' + at.state_path,
          renderState));
      }
      linesView.appendChild(card);
    });
  }

  /* ------------------------------------------------------------------------
   * Boot
   * --------------------------------------------------------------------- */

  function describeLegend() {
    T.clear(legend);
    const stations = spine.stations || [];
    const counts = new Map();
    stations.forEach(function (station) {
      const kind = M.kindOf(station, kindsStated);
      counts.set(kind, (counts.get(kind) || 0) + 1);
    });
    const shown = [M.PROMULGATED, M.PRINTED, M.UNSTATED].filter(function (kind) {
      return counts.get(kind);
    });
    shown.forEach(function (kind) {
      const item = T.el('span', 'legend-item legend-' + kind);
      item.appendChild(T.el('span', 'legend-mark'));
      item.appendChild(document.createTextNode(
        counts.get(kind) + ' ' + kind +
        (kind === M.PROMULGATED ? ' — an act stands behind it'
          : kind === M.PRINTED ? ' — a printing survives and no act has been located'
            : ' — this file says nothing about which')));
      legend.appendChild(item);
    });
    const receptionCount = stations.reduce(function (count, station) {
      return count + receptionsOf(station).length;
    }, 0);
    if (receptionCount) {
      const item = T.el('span', 'legend-item legend-reception');
      const mark = T.el('span', 'legend-mark');
      mark.setAttribute('aria-hidden', 'true');
      item.appendChild(mark);
      item.appendChild(document.createTextNode(
        receptionCount + ' documented reception' + (receptionCount === 1 ? '' : 's') +
        ' — a hollow track enters a double-ring station; open it for the instrument and evidence'));
      legend.appendChild(item);
    }
    legend.appendChild(T.el('span', 'legend-item',
      'A crossing without a station marker asserts no connection. Parent links ' +
      'follow the recorded evidence; order alone does not establish textual descent.'));
    [['stated', 'Wider line: an act or book states the parent link'],
      ['attributed', 'Medium line: a cited scholarly attribution'],
      ['sequence', 'Narrower line: recorded sequence; textual descent not established']].forEach(function (entry) {
      const item = T.el('span', 'legend-item legend-' + entry[0]);
      item.appendChild(T.el('span', 'legend-mark'));
      item.appendChild(document.createTextNode(entry[1]));
      legend.appendChild(item);
    });
    const broken = stations.filter(function (station) {
      return (station.via_unrepresented || []).length;
    }).length;
    if (broken) {
      const item = T.el('span', 'legend-item legend-gap');
      item.appendChild(T.el('span', 'legend-mark'));
      item.appendChild(document.createTextNode(
        broken + ' broken connector' + (broken === 1 ? '' : 's') +
        ' — the descent crosses an edition this record does not carry'));
      legend.appendChild(item);
    }
  }

  function fromHash(params) {
    const state = params || T.readHash();
    return { station: state.get('station'), unit: state.get('unit') };
  }

  function start(data) {
    spine = data;
    readVocabulary(data);
    const scope = document.getElementById('map-scope');
    if (scope) scope.hidden = data.vocabulary !== 'liturgy';
    const stations = data.stations || [];
    byId = new Map(stations.map(function (station) { return [station.id, station]; }));
    kindsStated = M.kindsAreStated(stations);
    draw();
    describeLegend();

    const lines = (data.lines || []).map(function (line) { return line.label; });
    const roots = stations.filter(function (station) {
      return !(station.parents || []).length;
    }).length;
    tally.textContent = stations.length + ' stations on ' + (data.lines || []).length +
      ' recorded lines; ' + roots + ' unconnected starting points in this record. ' +
      'This is the selected historical slice, not a comprehensive history.';

    fillUnits();
    renderJunctions();

    // The last station in topological order is the furthest the record reaches,
    // which is where a reader with no other instruction should arrive.
    const wanted = fromHash();
    if (wanted.unit) openUnit(wanted.unit);
    if (wanted.station) {
      if (byId.has(wanted.station)) open(wanted.station);
      else reportUnknownStation(wanted.station);
      revealDetail();
    }
    else if (stations.length) open(stations[stations.length - 1].id);

    T.onHashChange(function (params) {
      const next = fromHash(params);
      if (next.unit && next.unit !== openedUnit) openUnit(next.unit);
      if (!next.station || next.station === selected) return;
      if (byId.has(next.station)) open(next.station);
      else reportUnknownStation(next.station);
      revealDetail();
    });
  }

  /**
   * Which slice this page opens on.
   *
   * `act-history structure` writes the manifest beside the map files it writes,
   * naming exactly the slices that are THERE, and declaring which one to open.
   * This page used to name one in its own source, which meant the landing slice
   * was a fact about a browser file rather than about the record: it opened on
   * the twelve-station tracer, two lines and one fork, which is the shape this
   * drawing is least needed for.
   *
   * `default` is read, NEVER inferred from row order. The manifest does put the
   * landing slice first, and relying on that would work today and break
   * silently the day the rows were sorted for some unrelated reason.
   *
   * `?slice=` still overrides, and overrides without consulting the manifest —
   * a slice built into a data root of one's own is reachable before anything
   * lists it, which is what the parameter was for.
   */
  async function chosenSlice() {
    if (/^[a-z0-9][a-z0-9-]*$/.test(ASKED || '')) return ASKED;
    const file = await T.loadJSON(MANIFEST);
    const slices = (file && file.slices) || [];
    const declared = (file && file.default) || '';
    if (slices.some(function (row) { return row && row.id === declared; })) return declared;
    return (slices.length && slices[0] && slices[0].id) || '';
  }

  /* The catalogue is a second view of the research, not another act graph.
   * Its chronology and source states come from the generator. In particular,
   * sorting records never supplies a parent edge or admits a new station. */
  const CATALOGUE = 'structure/act-history/catalogue.json';
  let catalogueData = null;

  function catalogueValid(data) {
    const object = function (value) { return value && typeof value === 'object' && !Array.isArray(value); };
    const string = function (value) { return typeof value === 'string'; };
    const ids = new Set();
    if (!object(data) || data.schema !== 'triptych-eucharistic-history/v1' ||
        !Array.isArray(data.entries) || !Array.isArray(data.limitations) ||
        !data.limitations.every(string) || !Array.isArray(data.text_sets)) return false;
    const entriesValid = data.entries.every(function (row) {
      if (!object(row) || !row.id || ids.has(row.id)) return false;
      ids.add(row.id);
      if (!['id', 'family', 'title', 'date_label', 'record_kind', 'evidence_status',
        'text_status', 'substantive_status'].every(function (key) { return string(row[key]); })) return false;
      if (!object(row.origin) || !object(row.source_record) || !Array.isArray(row.sources) ||
          !Array.isArray(row.links)) return false;
      if (!row.sources.every(object) || !row.links.every(object)) return false;
      if (row.chronology !== null && (!object(row.chronology) ||
          !Number.isFinite(row.chronology.start) || !Number.isFinite(row.chronology.end) ||
          row.chronology.end < row.chronology.start)) return false;
      if (row.act_ref !== null && (!object(row.act_ref) ||
          !/^[a-z0-9][a-z0-9-]*$/.test(row.act_ref.slice || '') ||
          !/^[a-z0-9][a-z0-9-]*$/.test(row.act_ref.station_id || ''))) return false;
      return true;
    }) && data.text_sets.every(object);
    if (!entriesValid) return false;
    if (data.presentation_groups !== undefined && (!Array.isArray(data.presentation_groups) ||
        !data.presentation_groups.every(function (g) { return object(g) && string(g.id) && string(g.label); }))) return false;
    for (const entity of data.relationship_entities || []) {
      if (!object(entity) || !string(entity.id) || ids.has(entity.id) ||
          entity.kind !== 'textual-tradition' || entity.chronology !== null ||
          !string(entity.label) || !string(entity.family) || !Array.isArray(entity.evidence)) return false;
      ids.add(entity.id);
    }
    if (data.relationships === undefined) return true;
    if (!Array.isArray(data.relationships)) return false;
    const relationshipIds = new Set();
    return data.relationships.every(function (row) {
      if (!object(row) || !string(row.id) || relationshipIds.has(row.id)) return false;
      relationshipIds.add(row.id);
      return ids.has(row.from) && ids.has(row.to) && row.from !== row.to &&
        ['borrowing','reception','shared-text','common-ancestry','edition-succession'].includes(row.kind) &&
        ['sourced','attributed','disputed','unresolved'].includes(row.certainty) &&
        row.directed === ['borrowing','reception','edition-succession'].includes(row.kind) && row.git_ancestry === false && row.text_inheritance === false &&
        ['scope','basis','limitations'].every(function (key) { return string(row[key]) && row[key].trim(); }) &&
        Array.isArray(row.evidence) && row.evidence.length > 0 && row.evidence.every(function (e) {
          return object(e) && string(e.source_id) && string(e.locus) && object(e.source) &&
            string(e.source.title) && ['inspected','not-inspected'].includes(e.source.inspection_status) &&
            (row.certainty !== 'sourced' || e.source.inspection_status === 'inspected');
        }) && Array.isArray(row.comparison_links) && row.comparison_links.every(function (c) {
          return object(c) && /^[a-z0-9][a-z0-9-]*$/.test(c.id || '') &&
            c.projection_path === 'comparisons/' + c.id + '.json';
        });
    });
  }

  function catalogueText(value) {
    if (value === null || value === undefined || value === '') return 'Not recorded';
    return typeof value === 'object' ? JSON.stringify(value, null, 2) : String(value);
  }

  function catalogueURL(value) {
    // Source-controlled URLs still cross a trust boundary. Reject executable
    // schemes, credentials, local file paths, and protocol-relative URLs.
    if (typeof value !== 'string' || !/^https?:\/\//i.test(value)) return null;
    try {
      const url = new URL(value);
      return !url.username && !url.password ? url.href : null;
    } catch (_) { return null; }
  }

  function catalogueLink(url, label) {
    const safe = catalogueURL(url);
    if (!safe) return T.el('span', null, catalogueText(label) + ' — link unavailable');
    const link = T.el('a', null, catalogueText(label));
    link.href = safe;
    link.rel = 'noopener noreferrer';
    return link;
  }

  function sourceLibraryLink(link, row) {
    const id=link.edition_id, label='Open edition in the Source Library';
    if (typeof id!=='string' || id!==id.trim() || !/^edition\.[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$/.test(id) ||
        id!==row.source_record.source_library_edition_id || link.url!=='../sources/#edition='+encodeURIComponent(id))
      return T.el('span',null,label+' — link unavailable');
    const anchor=T.el('a',null,label);
    anchor.href=link.url;
    return anchor;
  }

  function historyURL(view, slice, hash) {
    const query = new URLSearchParams(window.location.search);
    query.set('view', view);
    if (slice) query.set('slice', slice);
    // Relative to this route, including under a project-path deployment.
    return '?' + query.toString() + (hash || '');
  }

  function catalogueHash(family, query, record) {
    const params = new URLSearchParams();
    if (family) params.set('family', family);
    if (query) params.set('q', query);
    if (record) params.set('record', record);
    return '#' + params.toString();
  }

  function catalogueRecord(row, target) {
    T.clear(target);
    target.hidden = false;
    const back = T.el('button', 'link-button', 'Back to source results');
    back.type = 'button';
    back.addEventListener('click', function () {
      const previous = document.getElementById('catalogue-entry-' + row.id);
      (previous || document.getElementById('catalogue-family')).focus();
    });
    target.appendChild(back);
    target.appendChild(T.el('h3', 'panel-title', row.title));
    const fields = T.el('dl', 'catalogue-facts');
    const add = function (label, value) {
      fields.appendChild(T.el('dt', null, label));
      fields.appendChild(T.el('dd', null, catalogueText(value)));
    };
    add('Record group', row.presentation_group ? row.presentation_group.label : row.family);
    add('Family in source inventory', row.family);
    add('Language as recorded', row.source_record.language || row.source_record.languages);
    if (row.source_record.language_scope || row.source_record.inclusion_status) {
      add('Language scope', row.source_record.language_scope || row.source_record.inclusion_status);
    }
    add('Date as recorded', row.date_label);
    if (row.chronology) {
      add('Date interpretation', [row.chronology.kind, row.chronology.certainty].filter(Boolean).join(' · '));
    } else add('Chronology', 'Undated or unresolved; no year has been inferred.');
    add('Record kind', row.record_kind);
    add('Evidence status', row.evidence_status);
    add('Source acquisition', row.acquisition_status);
    add('Text status', row.text_status);
    add('Substantive-version status', row.substantive_status);
    target.appendChild(fields);
    target.appendChild(T.el('p', 'detail-weak',
      'The statuses above are separate findings. A catalogue identification or a held scan does not ' +
      'establish a substantive version, a collated text, or a complete book. The original record below ' +
      'preserves the stated basis and unresolved work.'));
    if (row.act_ref) {
      const paragraph = T.el('p', null);
      const link = T.el('a', null, 'Open the recorded station in the historical map');
      link.href = historyURL('map', row.act_ref.slice,
        '#station=' + encodeURIComponent(row.act_ref.station_id));
      paragraph.appendChild(link);
      target.appendChild(paragraph);
    } else target.appendChild(T.el('p', 'panel-note',
      'No accepted act-history station is linked to this record.'));
    appendRecordRelations(row, target);
    target.appendChild(T.el('h4', null, 'Sources and access'));
    const sources = T.el('ul', 'catalogue-sources');
    row.sources.forEach(function (source) {
      const item = T.el('li', null);
      item.appendChild(catalogueLink(source.url, source.label || source.id || source.url));
      item.appendChild(T.el('p', 'panel-note', 'Inspection: ' + catalogueText(source.inspection)));
      sources.appendChild(item);
    });
    row.links.forEach(function (link) {
      if (link.kind!=='source-library-edition' && row.sources.some(function (source) { return source.url === link.url; })) return;
      const item = T.el('li', null);
      item.appendChild(link.kind==='source-library-edition' ? sourceLibraryLink(link,row)
        : catalogueLink(link.url, link.label || link.kind || link.url));
      sources.appendChild(item);
    });
    if (!sources.childNodes.length) sources.appendChild(T.el('li', null, 'No source access link is recorded.'));
    target.appendChild(sources);
    const original = T.el('details', 'catalogue-original');
    original.appendChild(T.el('summary', null, 'Original inventory metadata'));
    original.appendChild(T.el('p', 'panel-note', [row.origin.inventory, row.origin.table, row.origin.id]
      .map(catalogueText).join(' · ')));
    original.appendChild(T.el('pre', null, JSON.stringify(row.source_record, null, 2)));
    target.appendChild(original);
  }

  const RELATION_WORDS = {
    borrowing:'Borrowing', reception:'Reception', 'shared-text':'Shared wording',
    'common-ancestry':'Common ancestry', 'edition-succession':'Edition succession'
  };

  function endpointLink(endpoint) {
    if (endpoint.entity) return T.el('span', 'relation-entity', endpoint.title);
    const link = T.el('a', null, endpoint.title);
    link.href = historyURL('catalogue', null, catalogueHash('', '', endpoint.id));
    return link;
  }

  function relationshipEvidence(relation, target, data) {
    const row = relation.record;
    target.appendChild(T.el('p', 'relation-claim', row.basis));
    target.appendChild(T.el('p', 'panel-note', 'Scope: ' + row.scope));
    target.appendChild(T.el('p', 'detail-weak', row.limitations));
    target.appendChild(T.el('p', 'panel-note',
      'This research relationship does not create a historical station, a Git parent, or inherited text.'));
    const citations = T.el('ul', 'catalogue-sources');
    row.evidence.forEach(function (evidence) {
      const item = T.el('li', null);
      item.appendChild(catalogueLink(evidence.source.url, evidence.source.title));
      item.appendChild(T.el('p', null, evidence.locus));
      item.appendChild(T.el('p', 'panel-note', 'Source inspection: ' + evidence.source.inspection_status +
        ' · ' + catalogueText(evidence.source.inspection)));
      citations.appendChild(item);
    });
    target.appendChild(citations);
    (row.comparison_links || []).forEach(function (link) {
      const declaration = (data.comparisons || []).find(function (c) { return c.id === link.id; });
      if (!declaration) return;
      const fold = lazyBlock('Read linked text comparison: ' + (declaration.label || declaration.title || declaration.id),
        'structure/act-history/' + link.projection_path, function (host,payload) {
          renderComparison(host,payload,declaration);
        });
      fold.classList.add('comparison-fold');
      target.appendChild(fold);
    });
    target.appendChild(T.el('p', 'panel-note', 'Relationship ID: ' + row.id));
  }

  function relationDiagram(relation, data, overviewAnchor) {
    const row = relation.record;
    const article = T.el('article', 'research-connection relation-' + row.kind);
    article.setAttribute('data-relationship', row.id);
    if (overviewAnchor) article.id = 'research-R' + String(relation.number).padStart(2,'0');
    const caption = T.el('h4', null, 'R' + String(relation.number).padStart(2,'0') + ' · ' +
      RELATION_WORDS[row.kind] + ' · ' + row.certainty);
    article.appendChild(caption);
    if (row.label && row.label !== row.kind) article.appendChild(T.el('p', 'relation-subtitle', row.label));
    const diagram = T.el('div', 'relationship-diagram');
    [relation.from,relation.to].forEach(function (endpoint,i) {
      if (i) {
        const bridge = T.el('span', 'relationship-bridge' + (row.directed ? ' directed' : ''));
        bridge.setAttribute('aria-label', row.directed ? 'directed relationship' : 'symmetric relationship');
        bridge.appendChild(T.el('span', null, row.directed ? '→' : '↔'));
        diagram.appendChild(bridge);
      }
      const stop = T.el('div', 'relationship-endpoint' + (endpoint.entity ? ' conceptual-endpoint' : ''));
      stop.appendChild(T.el('p', 'endpoint-group', endpoint.group));
      stop.appendChild(endpointLink(endpoint));
      stop.appendChild(T.el('p', 'panel-note', endpoint.date));
      if (endpoint.entity) {
        const qualification = T.el('details', 'entity-evidence');
        qualification.appendChild(T.el('summary', null, 'Why this textual tradition is named'));
        ['scope','basis','limitations'].forEach(function (key) {
          if (endpoint.record[key]) qualification.appendChild(T.el('p', 'panel-note', endpoint.record[key]));
        });
        (endpoint.record.evidence || []).forEach(function (evidence) {
          if (!evidence.source) return;
          const source = T.el('p', 'panel-note');
          source.appendChild(catalogueLink(evidence.source.url, evidence.source.title));
          source.appendChild(T.el('span', null, ' · ' + evidence.locus + ' · ' + evidence.source.inspection_status));
          qualification.appendChild(source);
        });
        stop.appendChild(qualification);
      }
      stop.appendChild(T.el('p', 'endpoint-status', endpoint.entity
        ? 'Textual reference, shown without a date axis'
        : endpoint.record.act_ref ? 'Recorded edition or reform'
          : 'Historical book candidate'));
      if (!endpoint.entity) stop.appendChild(T.el('p', 'panel-note',
        endpoint.record.record_kind + ' · Evidence: ' + endpoint.record.evidence_status));
      diagram.appendChild(stop);
    });
    article.appendChild(diagram);
    const evidence = T.el('details', 'relation-evidence');
    evidence.appendChild(T.el('summary', null, 'Evidence, scope, and limits' +
      (row.comparison_links.length ? ' · linked text comparison' : '')));
    relationshipEvidence(relation,evidence,data);
    article.appendChild(evidence);
    return article;
  }

  function appendRecordRelations(row, target) {
    if (!catalogueData) return;
    const relations = M.overviewModel(catalogueData).relations.filter(function (r) {
      return r.from.id === row.id || r.to.id === row.id;
    });
    target.appendChild(T.el('h4', null, 'Recorded research connections'));
    if (!relations.length) target.appendChild(T.el('p', 'panel-note',
      'Connections for this record have not yet been investigated or established here. This does not establish historical isolation.'));
    relations.forEach(function (r) { target.appendChild(relationDiagram(r,catalogueData)); });
  }

  function renderNetwork(data, selectedFamily) {
    const host = document.getElementById('overview-network');
    if (!host) return;
    T.clear(host);
    const panels = M.networkLayout(data);
    host.appendChild(T.el('h3', null, 'Traditions and documented connections'));
    host.appendChild(T.el('p', 'panel-note',
      'Follow the colored routes between named groups, then open an R reference for the exact books, evidence, and text comparisons. ' +
      'Positions show connections, not dates or historical origins. A crossing without a circle is not a connection. ' +
      'Groups without a recorded relationship remain in the coverage index; their connections have not yet been investigated or established here.'));
    const legend = T.el('ul', 'network-legend');
    ['borrowing','reception','shared-text','common-ancestry','edition-succession'].forEach(function (kind) {
      const style = M.networkStyle(kind), item = T.el('li');
      const sample = svg('svg',{viewBox:'0 0 64 14',width:64,height:14,'aria-hidden':'true'});
      sample.appendChild(svg('path',{d:'M 2 7 L 62 7',stroke:style.color,'stroke-width':style.width,'stroke-dasharray':style.dash,fill:'none'}));
      item.appendChild(sample); item.appendChild(T.el('span',null,style.label)); legend.appendChild(item);
    });
    host.appendChild(legend);
    host.appendChild(T.el('p','panel-note',
      'Arrowheads mark direction of borrowing, reception, or edition succession. Shared wording and common ancestry have no arrow. ' +
      'Each route lists its evidence qualification: sourced, attributed, disputed, or unresolved. Within-group references describe relationships inside one named group.'));
    panels.forEach(function (panel) {
      const section = T.el('section','network-component');
      section.appendChild(T.el('h4',null,'Network ' + panel.number + ' · ' + panel.nodes.length + ' connected groups · ' + panel.relations.length + ' relationships'));
      const viewport = T.el('div','network-viewport');
      viewport.setAttribute('tabindex','0');
      viewport.setAttribute('aria-label','Connected traditions map; scroll horizontally on a narrow screen. Full route references follow the diagram.');
      const drawing = svg('svg',{viewBox:'0 0 '+panel.width+' '+panel.height,'class':'tradition-network',role:'group','aria-label':'Connected traditions; positions do not represent dates'});
      const defs = svg('defs',{});
      ['borrowing','reception','edition-succession'].forEach(function (kind) {
        const marker = svg('marker',{id:'network-arrow-'+panel.number+'-'+kind,viewBox:'0 0 10 10',refX:9,refY:5,markerWidth:6,markerHeight:6,orient:'auto-start-reverse'});
        marker.appendChild(svg('path',{d:'M 0 0 L 10 5 L 0 10 z',fill:M.networkStyle(kind).color})); defs.appendChild(marker);
      });
      drawing.appendChild(defs);
      panel.nodes.forEach(function (node) { if (node.leader) drawing.appendChild(svg('path',{d:node.leader,stroke:'#a6a19a','stroke-width':2,fill:'none'})); });
      const focusRelation = function (number,event) {
        event.preventDefault();
        const key = 'research-R'+String(number).padStart(2,'0');
        let target = document.getElementById(key);
        if (!target) {
          const relation = M.overviewModel(data).relations.find(function (r) { return r.number === number; });
          if (relation) {
            target = relationDiagram(relation,data,true);
            document.getElementById('overview-connections').appendChild(target);
          }
        }
        if (target) { target.setAttribute('tabindex','-1'); target.scrollIntoView({block:'start'}); target.focus({preventScroll:true}); }
      };
      panel.edges.forEach(function (edge) {
        const style = M.networkStyle(edge.kind), link = svg('a',{'href':'#research-R'+String(edge.numbers[0]).padStart(2,'0'),'aria-label':edge.label});
        const path = svg('path',{d:edge.path,stroke:style.color,'stroke-width':style.width,'stroke-dasharray':style.dash,fill:'none','data-relationships':edge.ids.join(' ')});
        if (edge.directed) path.setAttribute('marker-end','url(#network-arrow-'+panel.number+'-'+edge.kind+')');
        const title = svg('title',{}); title.textContent=edge.label; path.appendChild(title); link.appendChild(path);
        link.addEventListener('click',function (event) { focusRelation(edge.numbers[0],event); }); drawing.appendChild(link);
      });
      panel.nodes.forEach(function (node) {
        const link = svg('a',{href:historyURL('catalogue',null,catalogueHash('group:'+node.id,'','')),'aria-label':node.label+'; '+node.caption});
        link.appendChild(svg('circle',{cx:node.x,cy:node.y,r:13,fill:'#fffdf8',stroke:'#34302c','stroke-width':4}));
        node.labelLines.forEach(function (line,i) {
          const text = svg('text',{x:node.labelX,y:node.labelY+i*31,'text-anchor':node.anchor,'font-size':26,'font-weight':600,'class':'network-node-label'});
          text.textContent=line; link.appendChild(text);
        });
        const caption = svg('text',{x:node.labelX,y:node.labelY+node.labelLines.length*31,'text-anchor':node.anchor,'font-size':20,'class':'network-node-label'});
        caption.textContent=node.caption; link.appendChild(caption);
        drawing.appendChild(link);
      });
      viewport.appendChild(drawing); section.appendChild(viewport);
      const references = T.el('details','network-references');
      references.appendChild(T.el('summary',null,'Route references and evidence qualifications ('+panel.edges.length+' routes)'));
      const list = T.el('ul');
      panel.edges.forEach(function (edge) {
        const item = T.el('li'), link = T.el('a',null,edge.label);
        link.href='#research-R'+String(edge.numbers[0]).padStart(2,'0');
        link.addEventListener('click',function (event) { focusRelation(edge.numbers[0],event); }); item.appendChild(link); list.appendChild(item);
      });
      panel.nodes.filter(function (node) { return node.within.length; }).forEach(function (node) {
        const item = T.el('li',null,node.label+' · within group: ');
        node.within.forEach(function (number) {
          const link = T.el('a',null,' R'+String(number).padStart(2,'0'));
          link.href='#research-R'+String(number).padStart(2,'0');
          link.addEventListener('click',function (event) { focusRelation(number,event); }); item.appendChild(link);
        }); list.appendChild(item);
      });
      references.appendChild(list); section.appendChild(references); host.appendChild(section);
    });
    if (selectedFamily) host.appendChild(T.el('p','panel-note','The network retains the full context. The evidence diagrams below follow your selected group.'));
  }

  function renderOverview(data, selectedFamily) {
    const host = document.getElementById('history-overview');
    if (!host) return;
    host.hidden = !overviewMode;
    if (!overviewMode) return;
    const model = M.overviewModel(data);
    renderNetwork(data,selectedFamily);
    const connections = document.getElementById('overview-connections');
    T.clear(connections);
    const matches = function (endpoint) {
      return !selectedFamily || 'group:' + endpoint.groupId === selectedFamily || endpoint.record.family === selectedFamily;
    };
    const relations = model.relations.filter(function (r) { return matches(r.from) || matches(r.to); });
    if (!relations.length) connections.appendChild(T.el('p', 'panel-note',
      'Cross-tradition relationships have not yet been investigated or established in this projection.'));
    relations.forEach(function (relation) { connections.appendChild(relationDiagram(relation,data,true)); });
    const groups = document.getElementById('overview-groups');
    T.clear(groups);
    model.groups.filter(function (group) {
      return !selectedFamily || 'group:' + group.id === selectedFamily || group.entries.some(function (r) { return r.family === selectedFamily; });
    }).forEach(function (group) {
      const item = T.el('li', 'overview-group');
      const link = T.el('a', 'overview-group-title', group.label);
      link.href = historyURL('catalogue', null, catalogueHash('group:' + group.id, '', ''));
      item.appendChild(link);
      const linked = model.relations.filter(function (r) { return r.from.groupId === group.id || r.to.groupId === group.id; });
      item.appendChild(T.el('p', 'panel-note', group.entries.length + ' catalogue records' +
        (group.entities.length ? ' · ' + group.entities.length + ' undated textual-tradition references' : '')));
      const dated = group.entries.filter(function (row) { return row.chronology; });
      if (dated.length) item.appendChild(T.el('p', 'panel-note', 'Recorded date bounds: ' +
        Math.min.apply(null,dated.map(function (r) { return r.chronology.start; })) + '–' +
        Math.max.apply(null,dated.map(function (r) { return r.chronology.end; })) +
        '; ' + (group.entries.length-dated.length) + ' undated or unresolved. Coverage dates, not a historical lifespan.'));
      else item.appendChild(T.el('p', 'panel-note', 'No catalogue dates are positioned in this group.'));
      const accepted = group.entries.filter(function (r) { return r.act_ref; }).length;
      item.appendChild(T.el('p', 'panel-note', accepted + ' linked to historical stations · ' +
        (group.entries.length-accepted) + ' research records without an accepted station link'));
      ['acquisition_status','text_status'].forEach(function (key) {
        const statuses = new Map();
        group.entries.forEach(function (row) { const value = row[key] || 'not recorded'; statuses.set(value,(statuses.get(value)||0)+1); });
        item.appendChild(T.el('p', 'panel-note', (key === 'text_status' ? 'Text: ' : 'Acquisition: ') +
          Array.from(statuses.entries()).map(function (pair) { return pair[1] + ' ' + pair[0]; }).join('; ')));
      });
      item.appendChild(T.el('p', 'panel-note', linked.length
        ? 'Connections: ' + linked.map(function (r) { return 'R' + String(r.number).padStart(2,'0'); }).join(', ')
        : 'Connections not yet investigated or established here.'));
      if (group.note) item.appendChild(T.el('p', 'panel-note', group.note));
      groups.appendChild(item);
    });
  }

  function comparisonValid(payload, declared) {
    if (!payload || payload.schema !== 'triptych-eucharistic-witness-comparison/v1' ||
        payload.id !== declared.id || (declared.kind && payload.kind !== declared.kind) || !['same-prayer-witness-comparison','parallel-liturgical-unit-comparison'].includes(payload.kind) ||
        (payload.kind === 'parallel-liturgical-unit-comparison' && payload.identity_claim !== 'parallel-function-not-same-composition') ||
        payload.membership_status !== 'established' || payload.historical_ancestry_claimed !== false ||
        payload.historical_act_claimed !== false || payload.introduction_date_inferred !== false ||
        typeof payload.basis !== 'string' || !payload.basis.trim() ||
        typeof payload.apparatus_caveat !== 'string' || !payload.apparatus_caveat.trim() ||
        typeof payload.unified_diff !== 'string' || !Array.isArray(payload.sources) ||
        !Array.isArray(payload.limitations) || !payload.limitations.every(function (text) { return typeof text === 'string'; })) return false;
    return ['left', 'right'].every(function (name) {
      const side = payload[name];
      const selection = declared[name];
      return side && selection && side.text_set === selection.text_set &&
        typeof side.title === 'string' && typeof side.joined_source_text === 'string' &&
        side.join_rule === 'insert-one-space-between-exact-source-bodies' &&
        Array.isArray(side.members) && side.members.length > 0 && Array.isArray(selection.unit_ids) &&
        side.members.length === selection.unit_ids.length && side.members.every(function (member, index) {
          return member && member.unit_id === selection.unit_ids[index] &&
            typeof member.source_text === 'string' && typeof member.source_id === 'string' &&
            typeof member.text_edition_id === 'string' &&
            typeof member.language === 'string' && member.publication && member.publication.status === 'permitted';
        });
    });
  }

  function renderComparison(host, payload, declared) {
    if (!comparisonValid(payload, declared)) throw new Error('The witness comparison is malformed or does not match its declared source members.');
    T.clear(host);
    host.appendChild(T.el('p', 'comparison-identity', payload.kind === 'parallel-liturgical-unit-comparison'
      ? 'Parallel liturgical function; different compositions. This is not a same-prayer revision comparison.'
      : 'Witnesses of the same prayer; differences do not establish an act of revision.'));
    host.appendChild(T.el('p', 'comparison-basis', payload.basis));
    host.appendChild(T.el('p', 'detail-weak comparison-caveat', payload.apparatus_caveat));
    const pair = T.el('div', 'comparison-pair');
    ['left', 'right'].forEach(function (name) {
      const side = payload[name];
      const column = T.el('section', 'comparison-witness');
      const heading = T.el('h4', null, (name === 'left' ? 'Left witness: ' : 'Right witness: ') + side.title);
      heading.id = 'comparison-' + payload.id + '-' + name;
      column.setAttribute('aria-labelledby', heading.id);
      column.appendChild(heading);
      column.appendChild(T.el('p', 'panel-note', 'Printed edition / target date: ' + catalogueText(side.target_date) +
        '. Represented witness date: ' + catalogueText(side.witness_date) + '.'));
      const text = T.el('p', 'held-text comparison-text', side.joined_source_text);
      const languages = Array.from(new Set(side.members.map(function (member) { return member.language; })));
      if (languages.length === 1) text.lang = languages[0];
      column.appendChild(text);
      column.appendChild(T.el('p', 'panel-note', side.members.length === 1
        ? 'One source unit; exact stored wording.'
        : side.members.length + ' source units in their declared order, joined with one space. Source wording is unchanged.'));
      const members = T.el('ol', 'comparison-members');
      side.members.forEach(function (member) {
        const item = T.el('li', null);
        item.appendChild(T.el('p', 'panel-note', 'Source: ' + member.source_id +
          ' · Edition: ' + member.text_edition_id + ' · Artifact: ' + catalogueText(member.source_artifact_id ||
            (member.provenance && member.provenance.artifact_provenance_source_id))));
        if (member.printed_page) item.appendChild(T.el('p', 'panel-note', 'Printed page: ' + member.printed_page));
        item.appendChild(T.el('p', 'panel-note', 'Transcription: ' + catalogueText(member.provenance && member.provenance.status) +
          ' · Publication basis: ' + catalogueText(member.publication.basis)));
        const evidence = T.el('details', 'catalogue-original');
        evidence.appendChild(T.el('summary', null, 'Unit identity, wording, and provenance'));
        evidence.appendChild(T.el('pre', null, JSON.stringify(member, null, 2)));
        item.appendChild(evidence);
        members.appendChild(item);
      });
      column.appendChild(members);
      pair.appendChild(column);
    });
    host.appendChild(pair);
    const diff = T.el('details', 'catalogue-original comparison-diff');
    diff.appendChild(T.el('summary', null, 'Show the generated unified text diff'));
    diff.appendChild(T.el('p', 'panel-note',
      'Minus marks the left witness; plus marks the right. Lines follow the generator’s mechanical clause breaks. ' +
      'These marks compare wording, spelling, and punctuation; they do not establish historical additions or deletions.'));
    diff.appendChild(T.el('pre', null, payload.unified_diff || 'The serialized texts are identical.'));
    host.appendChild(diff);
    payload.limitations.forEach(function (limit) { host.appendChild(T.el('p', 'panel-note', limit)); });
    const sources = T.el('details', 'catalogue-original');
    sources.appendChild(T.el('summary', null, 'Source records and access'));
    payload.sources.forEach(function (source) {
      if (!source || typeof source !== 'object') return;
      if (source.source_url) {
        const item = T.el('p', null);
        item.appendChild(catalogueLink(source.source_url, source.title || source.id));
        sources.appendChild(item);
      }
    });
    sources.appendChild(T.el('pre', null, JSON.stringify(payload.sources, null, 2)));
    host.appendChild(sources);
  }

  function nativeTextBindings(stage) {
    const routed=function (row) {
      if (!row || typeof row.text_binding!=='string') return false;
      const id=row.text_binding.replace(/^native-book:/,'');
      return /^[a-z0-9][a-z0-9-]*$/.test(id) && row.text_binding==='native-book:'+id &&
        row.text_projection_path==='native-texts/'+id+'.json' && /^[0-9a-f]{64}$/.test(row.text_binding_sha256);
    };
    if (Object.hasOwn(stage,'text_bindings')) {
      if (Object.hasOwn(stage,'text_binding') || stage.text_coverage!=='partial' ||
          !Array.isArray(stage.text_bindings) || !stage.text_bindings.length ||
          new Set(stage.text_bindings).size!==stage.text_bindings.length ||
          !Array.isArray(stage.text_projections) || stage.text_projections.length!==stage.text_bindings.length ||
          !stage.text_projections.every(function (row,index) {
            return routed(row) && row.text_binding===stage.text_bindings[index] &&
              typeof row.title==='string' && row.title.trim().length>0;
          })) throw Error('invalid native text routing metadata');
      return stage.text_projections;
    }
    if (Object.hasOwn(stage,'text_projections') || (Object.hasOwn(stage,'text_binding') && !routed(stage)))
      throw Error('invalid native text routing metadata');
    return stage.text_binding ? [stage] : [];
  }

  function nativeTextValid(payload, stage, binding) {
    binding=binding || stage;
    const strings=function (items) { return Array.isArray(items) && items.every(function (s) { return typeof s==='string' && s.length>0; }); };
    const unique=function (items) { return strings(items) && new Set(items).size===items.length; };
    if (!payload || payload.schema!=='triptych-eucharistic-native-text/v1' ||
        payload.adapter_id!==binding.text_binding || payload.adapter_id!=='native-book:'+payload.id ||
        !/^[0-9a-f]{64}$/.test(binding.text_binding_sha256) || payload.binding_sha256!==binding.text_binding_sha256 ||
        (binding!==stage && payload.title!==binding.title) ||
        typeof payload.title!=='string' || !unique(payload.stage_ids) || !payload.stage_ids.includes(stage.id) ||
        !unique(payload.catalogue_witness_ids) || JSON.stringify(payload.catalogue_witness_ids.slice().sort())!==JSON.stringify(stage.witness_ids.slice().sort()) ||
        !payload.scope || payload.scope.complete_declared_extent!==true ||
        !['constituent','whole-book'].includes(payload.scope.extent_kind) ||
        payload.scope.whole_book_complete!==(payload.scope.extent_kind==='whole-book') ||
        stage.text_coverage!==(payload.scope.whole_book_complete ? 'complete' : 'partial') ||
        typeof payload.scope.description!=='string' || !strings(payload.scope.omitted_book_divisions) ||
        (payload.scope.whole_book_complete ? payload.scope.omitted_book_divisions.length!==0 : payload.scope.omitted_book_divisions.length===0) ||
        !Array.isArray(payload.sources) || !unique(payload.sources.map(function (s) { return s && s.id; })) ||
        !Array.isArray(payload.witnesses) || !unique(payload.witnesses.map(function (w) { return w && w.id; })) ||
        !Array.isArray(payload.units) || !payload.units.length || !unique(payload.units.map(function (u) { return u && u.unit_id; })) ||
        !payload.counts || payload.counts.units!==payload.units.length || payload.scope.known_extent_units!==payload.units.length) return false;
    const sources=new Map(payload.sources.map(function (s) { return [s.id,s]; }));
    const witnesses=new Map(payload.witnesses.map(function (w) { return [w.id,w]; }));
    return payload.units.every(function (unit,index) {
      const artifact=sources.get(unit.source_artifact_id),edition=sources.get(unit.text_edition_id),witness=witnesses.get(unit.witness_id),passage=sources.get(unit.source_id);
      return unit.source_order===index+1 && typeof unit.text==='string' && unit.text.trim().length>0 &&
        typeof unit.kind==='string' && strings(unit.native_path) && typeof unit.source_locator==='string' &&
        /^[a-z]{2,3}(?:-[A-Za-z0-9]+)*$/.test(unit.language) &&
        unit.direction===(['ar','he','syr','arc'].includes(unit.language.split('-')[0]) ? 'rtl' : 'ltr') &&
        artifact && artifact.record_type==='artifact' && artifact.rights_status==='public-domain' &&
        artifact.edition_id===unit.text_edition_id &&
        artifact.rights_jurisdiction==='United States' && typeof artifact.rights_basis==='string' && artifact.rights_basis.length>0 &&
        edition && edition.record_type==='edition' && typeof edition.title==='string' &&
        witness && witness.edition_id===unit.text_edition_id && sources.has(witness.artifact_id) &&
        sources.get(witness.artifact_id).record_type==='artifact' &&
        passage && passage.record_type==='passage' && passage.edition_id===unit.text_edition_id && passage.artifact_id===unit.source_artifact_id &&
        unit.publication && unit.publication.status==='permitted' && unit.publication.basis==='public-domain' &&
        unit.publication.jurisdiction==='United States' && Array.isArray(unit.publication.surfaces) &&
        ['public-git','corpus-data'].every(function (surface) { return unit.publication.surfaces.includes(surface); });
    });
  }

  function renderNativeText(host,payload,stage,binding) {
    if (!nativeTextValid(payload,stage,binding)) throw Error('The source text is malformed or does not match this state’s accepted binding and extent.');
    T.clear(host);
    const sources=new Map(payload.sources.map(function (s) { return [s.id,s]; }));
    const witnesses=new Map(payload.witnesses.map(function (w) { return [w.id,w]; }));
    host.appendChild(T.el('h4',null,payload.title));
    host.appendChild(T.el('p','native-text-extent',
      'Complete declared '+payload.scope.extent_kind+': '+payload.counts.units+' source unit'+(payload.counts.units===1 ? '' : 's')+
      '. Whole-book text coverage: '+(payload.scope.whole_book_complete ? 'complete.' : 'partial.')));
    host.appendChild(T.el('p','native-text-scope',payload.scope.description));
    if (payload.scope.omitted_book_divisions.length) {
      host.appendChild(T.el('p',null,'Excluded book divisions:'));
      const exclusions=T.el('ul','native-text-exclusions');
      payload.scope.omitted_book_divisions.forEach(function (text) { exclusions.appendChild(T.el('li',null,text)); });
      host.appendChild(exclusions);
    }
    payload.units.forEach(function (unit) {
      const part=T.el('section','native-text-unit');
      part.appendChild(T.el('h5',null,unit.source_order+' · '+unit.kind.replace(/-/g,' ')));
      const text=T.el('p','held-text native-text-body',unit.text);
      text.setAttribute('data-unit-id',unit.unit_id);
      text.setAttribute('lang',unit.language); text.setAttribute('dir',unit.direction);
      part.appendChild(text);
      const edition=sources.get(unit.text_edition_id),witness=witnesses.get(unit.witness_id),facsimile=sources.get(witness.artifact_id);
      const citation=T.el('p','panel-note native-text-source');
      citation.appendChild(catalogueLink(facsimile.source_url,edition.title+(edition.date ? ' ('+edition.date+')' : '')));
      citation.appendChild(T.el('span',null,' · '+unit.source_locator));
      part.appendChild(citation); host.appendChild(part);
    });
    Array.from(new Set(payload.units.map(function (u) { return u.source_artifact_id; }))).forEach(function (id) {
      const source=sources.get(id);
      host.appendChild(T.el('p','panel-note native-text-rights','Public domain · United States. '+source.rights_basis));
      if (source.transformation) {
        const normalization=T.el('details','catalogue-original native-text-normalization');
        normalization.appendChild(T.el('summary',null,'Transcription and normalization'));
        normalization.appendChild(T.el('p',null,source.transformation)); host.appendChild(normalization);
      }
    });
  }

  function catalogueComparisons(data) {
    const rows = data.comparisons;
    if (!Array.isArray(rows) || !rows.length) return;
    const container = document.getElementById('catalogue-comparisons');
    const list = document.getElementById('catalogue-comparison-list');
    container.hidden = false;
    rows.forEach(function (row) {
      if (!row || !/^[a-z0-9][a-z0-9-]*$/.test(row.id || '') ||
          !row.left || !row.right || typeof row.apparatus_caveat !== 'string' ||
          row.projection_path !== 'comparisons/' + row.id + '.json') {
        list.appendChild(T.el('p', 'error', 'A configured witness comparison has invalid metadata and cannot be opened.'));
        return;
      }
      const title = row.title || row.label || row.id.replace(/-/g, ' ');
      const path = 'structure/act-history/' + row.projection_path;
      const fold = lazyBlock('Read comparison: ' + title, path, function (host, payload) {
        renderComparison(host, payload, row);
      });
      fold.classList.add('comparison-fold');
      list.appendChild(fold);
      list.appendChild(T.el('p', 'panel-note', row.apparatus_caveat));
    });
  }

  async function startCatalogue() {
    const results = document.getElementById('catalogue-results');
    const status = document.getElementById('catalogue-status');
    const family = document.getElementById('catalogue-family');
    const query = document.getElementById('catalogue-query');
    const panel = document.getElementById('catalogue-detail');
    try {
      const data = await T.loadJSON(CATALOGUE);
      if (!catalogueValid(data)) throw new Error('The source catalogue has an unsupported or malformed record.');
      T.doneBootstrapping();
      catalogueData = data;
      catalogueComparisons(data);
      const groups = M.overviewModel(data).groups;
      const families = groups.map(function (g) { return 'group:' + g.id; });
      groups.forEach(function (group) {
        const option = T.el('option', null, group.label);
        option.value = 'group:' + group.id;
        family.appendChild(option);
      });
      family.disabled = query.disabled = document.getElementById('catalogue-search').disabled = false;
      tally.textContent = data.entries.length + ' source records across ' + families.length +
        ' source-defined record groups. These are navigation groups, not a census of rites and not a count of complete books.';
      const limits = document.getElementById('catalogue-limits');
      data.limitations.forEach(function (limit) { limits.appendChild(T.el('p', null, limit)); });
      limits.appendChild(T.el('h3', null, 'Configured text sets'));
      limits.appendChild(T.el('p', null, 'Configuration does not mean that a text set has been generated or verified.'));
      const sets = T.el('ul', null);
      data.text_sets.forEach(function (set) {
        sets.appendChild(T.el('li', null, catalogueText(set.id) + ' · ' + catalogueText(set.adapter) +
          ' · ' + catalogueText(set.status)));
      });
      if (!data.text_sets.length) sets.appendChild(T.el('li', null, 'No text sets are configured.'));
      limits.appendChild(sets);
      document.getElementById('catalogue-coverage').hidden = false;

      function render(params, focusRecord) {
        const selectedFamily = params.get('family') || '';
        renderOverview(data, selectedFamily);
        const search = (params.get('q') || '').slice(0, 200);
        const record = params.get('record');
        // Preserve unknown filters visibly, rather than silently broadening a
        // shared URL to all traditions.
        let unknown = document.getElementById('catalogue-unknown-family');
        if (unknown) unknown.remove();
        if (selectedFamily && families.indexOf(selectedFamily) === -1) {
          const legacy = data.entries.some(function (row) { return row.family === selectedFamily; });
          unknown = T.el('option', null, selectedFamily + (legacy ? ' (source family)' : ' (not in this catalogue)'));
          unknown.id = 'catalogue-unknown-family';
          unknown.value = selectedFamily;
          family.appendChild(unknown);
        }
        family.value = selectedFamily;
        query.value = search;
        const terms = search.toLocaleLowerCase().split(/\s+/).filter(Boolean);
        const rows = data.entries.filter(function (row) {
          const haystack = [row.title, row.family, row.presentation_group && row.presentation_group.label, row.date_label, row.id,
            JSON.stringify(row.source_record)].join(' ').toLocaleLowerCase();
          return (!selectedFamily || row.family === selectedFamily ||
            'group:' + (row.presentation_group ? row.presentation_group.id : 'unmapped:' + row.family) === selectedFamily) &&
            terms.every(function (term) { return haystack.indexOf(term) !== -1; });
        });
        T.clear(results);
        status.textContent = rows.length + ' of ' + data.entries.length + ' source records shown.';
        if (!rows.length) results.appendChild(T.el('p', null, 'No records match these filters. Clear the search or choose another tradition.'));
        const sections = [
          { title: 'Chronological books and reforms', rows: rows.filter(function (row) { return row.chronology; })
            .sort(function (a, b) { return a.chronology.start - b.chronology.start || a.title.localeCompare(b.title); }) },
          { title: 'Undated or unresolved', rows: rows.filter(function (row) { return !row.chronology; }) }
        ];
        sections.forEach(function (section) {
          if (!section.rows.length) return;
          results.appendChild(T.el('h3', 'catalogue-period', section.title + ' (' + section.rows.length + ')'));
          if (section.title === 'Chronological books and reforms') results.appendChild(T.el('p','panel-note',
            'Read from earlier to later recorded dates. ○ marks a historical book candidate; ● marks an edition or reform linked to a historical line. ' +
            'Date ranges retain their source qualifications. Adjacent entries do not imply descent.'));
          const list = T.el('ul', 'catalogue-list');
          section.rows.forEach(function (row) {
            const item = T.el('li', 'catalogue-entry');
            item.appendChild(T.el('span', 'catalogue-date', row.date_label || 'Date unresolved'));
            const body = T.el('div', 'catalogue-entry-body');
            const link = T.el('a', 'catalogue-title', row.title);
            link.id = 'catalogue-entry-' + row.id;
            link.href = catalogueHash(selectedFamily, search, row.id);
            if (record === row.id) link.setAttribute('aria-current', 'true');
            link.addEventListener('click', function (event) {
              if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || event.button) return;
              event.preventDefault();
              T.writeHash([['family', selectedFamily], ['q', search], ['record', row.id]]);
              // Keep the list's DOM and keyboard focus intact on selection.
              catalogueRecord(row, panel);
              results.querySelectorAll('[aria-current]').forEach(function (node) { node.removeAttribute('aria-current'); });
              link.setAttribute('aria-current', 'true');
              panel.focus();
            });
            body.appendChild(link);
            body.appendChild(T.el('p','catalogue-entry-meta',row.act_ref ? '● Recorded edition or reform' : '○ Historical book candidate'));
            if (row.chronology) body.appendChild(T.el('p','catalogue-entry-meta',
              'Date basis: '+[row.chronology.kind,row.chronology.certainty].filter(Boolean).join(' · ')));
            body.appendChild(T.el('p', 'catalogue-entry-meta', (row.presentation_group ? row.presentation_group.label : row.family) + ' · ' + row.record_kind));
            body.appendChild(T.el('p', 'catalogue-entry-meta', 'Evidence: ' + row.evidence_status + ' · Acquisition: '+(row.acquisition_status || 'not recorded')+
              ' · Text: ' + row.text_status + ' · Version: ' + row.substantive_status));
            item.appendChild(body);
            list.appendChild(item);
          });
          results.appendChild(list);
        });
        const selectedRow = data.entries.find(function (row) { return row.id === record; });
        T.clear(panel);
        panel.hidden = !record;
        if (selectedRow) {
          catalogueRecord(selectedRow, panel);
          if (!rows.some(function (row) { return row.id === record; })) {
            panel.appendChild(T.el('p', 'detail-weak', 'This linked record is outside the current filters.'));
          }
          if (focusRecord) panel.focus();
        } else if (record) panel.appendChild(T.el('p', null, 'This source record is not in the catalogue: ' + record));
      }

      function filter(event) {
        event.preventDefault();
        T.writeHash([['family', family.value], ['q', query.value.trim()]]);
        render(T.readHash(), false);
      }
      document.getElementById('catalogue-filter').addEventListener('submit', filter);
      family.addEventListener('change', filter);
      T.onHashChange(function (params) { render(params, false); });
      render(T.readHash(), false);
    } catch (error) {
      T.doneBootstrapping();
      T.clear(results);
      status.textContent = 'Source catalogue unavailable.';
      results.appendChild(T.el('p', null, 'The source catalogue could not be loaded: ' + String(error.message || error)));
      const retry = T.el('a', null, 'Reload the source catalogue');
      retry.href = historyURL('catalogue', null, window.location.hash);
      results.appendChild(retry);
      tally.textContent = 'Catalogue coverage could not be read; no completeness claim is available.';
    } finally {
      results.setAttribute('aria-busy', 'false');
    }
  }

  function stageHistoryValid(history) {
    if (!history || history.schema !== 'triptych-eucharistic-stages/v1' ||
        !['traditions','sources','stages','transitions','gaps'].every(function (key) { return Array.isArray(history[key]); })) return false;
    const unique = function (rows) { return rows.every(function (r) { return r && typeof r.id==='string'; }) && new Set(rows.map(function (r) { return r.id; })).size===rows.length; };
    if (!['traditions','sources','stages','transitions','gaps'].every(function (key) { return unique(history[key]); })) return false;
    const traditions=new Set(history.traditions.map(function (t) { return t.id; }));
    const sources=new Set(history.sources.map(function (s) { return s.id; }));
    const stages=new Set(history.stages.map(function (s) { return s.id; }));
    const evidence=function (items) { return Array.isArray(items) && items.length>0 && items.every(function (e) {
      return e && sources.has(e.source_id) && typeof e.locus==='string' && typeof e.claim==='string';
    }); };
    return history.traditions.every(function (t) { return typeof t.label==='string' && typeof t.scope==='string'; }) &&
      history.sources.every(function (s) { return typeof s.title==='string' && typeof s.inspection==='string' && ['inspected','lead'].includes(s.status); }) &&
      history.stages.every(function (s) {
        return traditions.has(s.tradition_id) && ['documented','provisional'].includes(s.status) &&
          ['attestation','publication','approval','effective','reconstruction'].includes(s.date_kind) &&
          ['not-transcribed','partial','complete'].includes(s.text_coverage) &&
          ['label','date_label','scope','summary','witness_label','limitations','reception'].every(function (key) { return typeof s[key]==='string'; }) &&
          Array.isArray(s.components) && Array.isArray(s.witness_ids) && evidence(s.evidence) &&
          ((s.start_year===null && s.end_year===null) || (Number.isInteger(s.start_year) && Number.isInteger(s.end_year) && s.end_year>=s.start_year));
      }) && history.transitions.every(function (t) {
        return stages.has(t.from_stage) && stages.has(t.to_stage) && t.from_stage!==t.to_stage &&
          ['revision','recension-branch','reception','witness-succession'].includes(t.kind) &&
          ['documented','provisional'].includes(t.status) &&
          ['text-collated','primary-description','scholarly-description','bibliographic-only'].includes(t.evidence_level) &&
          ['established','attributed','unestablished'].includes(t.historical_parentage) &&
          t.git_ancestry===false && t.text_inheritance===false && typeof t.summary==='string' &&
          typeof t.limitations==='string' && Array.isArray(t.components) && Array.isArray(t.comparison_ids) && evidence(t.evidence) &&
          Array.isArray(t.changes) && t.changes.every(function (c) {
            return c && ['component','before','after','locus_before','locus_after'].every(function (key) { return typeof c[key]==='string'; }) && evidence(c.evidence);
          });
      }) && history.gaps.every(function (g) { return traditions.has(g.tradition_id) && ['period','missing','next_source','consequence'].every(function (key) { return typeof g[key]==='string'; }); });
  }

  function timelineState(params) {
    const number=function (raw) { return raw !== null && /^-?\d+$/.test(raw) ? Number(raw) : null; };
    return {tradition:params.get('tradition'),start:number(params.get('start')),end:number(params.get('end')),
      stage:params.get('stage'),transition:params.get('transition'),leads:params.get('leads')==='1',
      presentation:params.get('presentation')};
  }

  function timelinePairs(state) {
    return [['tradition',state.tradition],['start',state.start===null ? '' : String(state.start)],
      ['end',state.end===null ? '' : String(state.end)],['leads',state.leads ? '1' : ''],
      ['stage',state.stage],['transition',state.transition],['presentation',state.presentation]];
  }

  async function startTimeline() {
    const chart=document.getElementById('timeline-chart'), list=document.getElementById('timeline-list');
    const status=document.getElementById('timeline-status'), detail=document.getElementById('timeline-detail');
    const traditionControl=document.getElementById('timeline-tradition');
    const startControl=document.getElementById('timeline-start'),endControl=document.getElementById('timeline-end');
    const leadControl=document.getElementById('timeline-leads'),presentation=document.getElementById('timeline-presentation');
    let data,history,current,model;
    try {
      data=await T.loadJSON(CATALOGUE); T.doneBootstrapping();
      if (!catalogueValid(data) || !stageHistoryValid(data.stage_history)) throw Error('The historical stage projection is missing or malformed.');
      history=data.stage_history;
      if (!history.stages.length) {
        status.textContent='No historical book stages have yet been established in this projection.';
        T.clear(chart); chart.setAttribute('aria-busy','false'); return;
      }
      const byStage=new Map(history.stages.map(function (s) { return [s.id,s]; }));
      const byTransition=new Map(history.transitions.map(function (t) { return [t.id,t]; }));
      const bySource=new Map(history.sources.map(function (s) { return [s.id,s]; }));
      const words=function (value) { return String(value || '').replace(/-/g,' '); };
      const keys=M.stageLayout(history);
      const allOption=T.el('option',null,'All traditions on a shared year axis'); allOption.value='all'; traditionControl.appendChild(allOption);
      history.traditions.forEach(function (t) { const o=T.el('option',null,t.label); o.value=t.id; traditionControl.appendChild(o); });
      ['timeline-tradition','timeline-start','timeline-end','timeline-leads','timeline-apply','timeline-all-years','timeline-local-years','timeline-earlier','timeline-later','timeline-zoom-in','timeline-zoom-out']
        .forEach(function (id) { document.getElementById(id).disabled=false; });
      const defaultPresentation=window.matchMedia && window.matchMedia('(max-width: 800px)').matches ? 'list' : 'chart';
      presentation.value=defaultPresentation;

      function citation(items,target) {
        const citations=T.el('ul','stage-citations');
        (items || []).forEach(function (e) {
          const source=bySource.get(e.source_id), item=T.el('li');
          if (!source) return;
          item.appendChild(catalogueLink(source.url,source.title));
          item.appendChild(T.el('p',null,e.locus+' — '+e.claim));
          item.appendChild(T.el('p','panel-note',words(source.kind)+' · '+source.status+' · '+source.inspection));
          if (source.limitations) item.appendChild(T.el('p','panel-note',source.limitations));
          citations.appendChild(item);
        });
        target.appendChild(citations);
      }

      function select(kind,id) {
        current={...current,stage:kind==='stage' ? id : null,transition:kind==='transition' ? id : null};
        if (kind==='stage') {
          const selected=byStage.get(id);
          if (selected) {
            const anotherLane=current.tradition!=='all' && current.tradition!==selected.tradition_id;
            const outside=Number.isFinite(selected.start_year) && (selected.end_year<current.start || selected.start_year>current.end);
            if (anotherLane || outside) current={...current,tradition:anotherLane ? selected.tradition_id : current.tradition,start:null,end:null};
          }
        }
        render(current); T.writeHash(timelinePairs(current));
        revealSelection();
      }

      function revealSelection() {
        if (detail.hidden) return;
        detail.scrollIntoView({block:'start'}); detail.focus({preventScroll:true});
      }

      function stageButton(stage,label) {
        const button=T.el('button','stage-select',label || stage.label);
        button.type='button'; button.setAttribute('data-stage',stage.id);
        button.addEventListener('click',function () { select('stage',stage.id); }); return button;
      }

      function transitionContent(transition,target) {
        const from=byStage.get(transition.from_stage),to=byStage.get(transition.to_stage);
        target.appendChild(T.el('h4',null,keys.transitionKeys[transition.id]+' · '+words(transition.kind)));
        target.appendChild(T.el('p','stage-transition-summary',transition.summary));
        target.appendChild(T.el('p','panel-note',words(transition.evidence_level)+' · '+transition.status+
          ' · historical parentage: '+transition.historical_parentage));
        const endpoints=T.el('p','stage-endpoints');
        endpoints.appendChild(stageButton(from,from.date_label+' · '+from.label));
        endpoints.appendChild(T.el('span',null,' → '));
        endpoints.appendChild(stageButton(to,to.date_label+' · '+to.label)); target.appendChild(endpoints);
        (transition.changes || []).forEach(function (change) {
          const part=T.el('section','stage-change');
          part.appendChild(T.el('h5',null,words(change.component)));
          part.appendChild(T.el('p',null,'Before: '+change.before));
          part.appendChild(T.el('p','panel-note','Before locus: '+change.locus_before));
          part.appendChild(T.el('p',null,'After: '+change.after));
          part.appendChild(T.el('p','panel-note','After locus: '+change.locus_after));
          citation(change.evidence,part); target.appendChild(part);
        });
        if (!transition.changes.length) target.appendChild(T.el('p','panel-note','No component-level before/after collation is recorded for this transition.'));
        target.appendChild(T.el('p','detail-weak',transition.limitations));
        citation(transition.evidence,target);
        (transition.comparison_ids || []).forEach(function (id) {
          const declaration=(data.comparisons || []).find(function (c) { return c.id===id; });
          if (!declaration) return;
          const fold=lazyBlock('Read linked source-text comparison: '+(declaration.label || declaration.title || id),
            'structure/act-history/'+declaration.projection_path,function (host,payload) { renderComparison(host,payload,declaration); });
          fold.classList.add('comparison-fold'); target.appendChild(fold);
        });
      }

      function showDetail() {
        T.clear(detail); detail.hidden=!current.stage && !current.transition;
        detail.setAttribute('aria-label','Selected state or transition evidence');
        if (detail.hidden) return;
        const back=T.el('button','link-button','Back to the timeline'); back.type='button';
        back.addEventListener('click',function () {
          const host=presentation.value==='list' ? list : chart;
          const kind=current.transition ? 'transition' : 'stage';
          const id=current.transition || current.stage;
          let target=document.getElementById(host.id+'-'+kind+'-'+id);
          if (!target) ['timeline-unpositioned','timeline-provisional'].some(function (context) {
            target=document.getElementById(context+'-list-'+kind+'-'+id);
            if (target) document.getElementById(context).open=true;
            return !!target;
          });
          target=target || host;
          if (target===host) target.setAttribute('tabindex','-1');
          target.focus(); target.scrollIntoView({block:'center',inline:'center'});
        }); detail.appendChild(back);
        if (current.transition) {
          const transition=byTransition.get(current.transition);
          if (!transition) { detail.appendChild(T.el('p',null,'This transition is not in the current record: '+current.transition)); return; }
          detail.setAttribute('aria-label','Selected transition: '+transition.summary);
          transitionContent(transition,detail); return;
        }
        const stage=byStage.get(current.stage);
        if (!stage) { detail.appendChild(T.el('p',null,'This stage is not in the current record: '+current.stage)); return; }
        detail.setAttribute('aria-label','Selected state: '+stage.label+'; '+stage.date_label);
        detail.appendChild(T.el('h3',null,keys.stageKeys[stage.id]+' · '+stage.label));
        detail.appendChild(T.el('p',null,stage.date_label+' · '+stage.date_kind+' · '+stage.status));
        detail.appendChild(T.el('p','panel-note',stage.start_year===null ? 'No year is positioned for this state.'
          : 'Date bounds: '+stage.start_year+'–'+stage.end_year+'. These date this attestation; they are not a period of validity.'));
        detail.appendChild(T.el('p','stage-coverage','Text coverage: '+words(stage.text_coverage)+'. This is independent of historical evidence.'));
        try {
          nativeTextBindings(stage).forEach(function (binding) {
            const label=binding===stage ? 'Read available source text' : 'Read available source text: '+binding.title;
            const fold=lazyBlock(label,'structure/act-history/'+binding.text_projection_path,
              function (host,payload) { renderNativeText(host,payload,stage,binding); });
            fold.classList.add('native-text-fold'); fold.setAttribute('data-text-binding',binding.text_binding);
            detail.appendChild(fold);
          });
        } catch (error) {
          detail.appendChild(T.el('p','error','The available source text has invalid routing metadata and cannot be opened.'));
        }
        detail.appendChild(T.el('p',null,stage.summary));
        detail.appendChild(T.el('p',null,'Scope: '+stage.scope));
        detail.appendChild(T.el('p',null,'Parts represented: '+stage.components.map(words).join(', ')));
        detail.appendChild(T.el('p',null,'Identified witness: '+stage.witness_label));
        detail.appendChild(T.el('p',null,'Community reception: '+stage.reception));
        detail.appendChild(T.el('p','detail-weak',stage.limitations));
        citation(stage.evidence,detail);
        const witnessLinks=T.el('ul','stage-witness-links');
        stage.witness_ids.forEach(function (id) {
          const row=data.entries.find(function (entry) { return entry.id===id; });
          const item=T.el('li');
          if (row) {
            const link=T.el('a',null,row.title+' · '+row.date_label); link.href=historyURL('catalogue',null,catalogueHash('','',id)); item.appendChild(link);
            if (row.act_ref) { const act=T.el('a',null,' Recorded act and text state'); act.href=historyURL('map',row.act_ref.slice,'#'+new URLSearchParams([['station',row.act_ref.station_id]])); item.appendChild(act); }
          } else item.appendChild(T.el('span',null,'Witness reference not available in this catalogue: '+id));
          witnessLinks.appendChild(item);
        });
        if (witnessLinks.childNodes.length) detail.appendChild(witnessLinks);
        const incoming=history.transitions.filter(function (t) { return t.to_stage===stage.id; });
        detail.appendChild(T.el('h3',null,'What changed into this state'));
        if (!incoming.length) detail.appendChild(T.el('p','panel-note','No transition into this state has been established here. Its position in date order does not supply a parent.'));
        incoming.forEach(function (transition) { transitionContent(transition,detail); });
        const outgoing=history.transitions.filter(function (t) { return t.from_stage===stage.id; });
        detail.appendChild(T.el('h3',null,'What follows from this state'));
        if (!outgoing.length) detail.appendChild(T.el('p','panel-note','No onward transition is established here. This does not establish an end to its use.'));
        outgoing.forEach(function (transition) { transitionContent(transition,detail); });
        if (!model.lanes.some(function (lane) { return lane.nodes.some(function (node) { return node.id===stage.id; }); }) && Number.isFinite(stage.start_year)) {
          detail.appendChild(stageButton(stage,'Show this state on its timeline'));
        }
      }

      function readingCard(stage,context) {
        context=context || 'timeline-list';
        const article=T.el('article','timeline-list-card'); article.setAttribute('data-stage',stage.id);
        const selection=stageButton(stage,keys.stageKeys[stage.id]+' · '+stage.label);
        selection.id=context+'-stage-'+stage.id;
        if (current.stage===stage.id) selection.setAttribute('aria-current','true');
        article.appendChild(selection);
        article.appendChild(T.el('p','stage-date',stage.date_label+' · '+stage.date_kind));
        article.appendChild(T.el('p','panel-note',stage.status+' · Parts: '+stage.components.map(words).join(', ')+' · Text: '+words(stage.text_coverage)));
        article.appendChild(T.el('p',null,stage.scope));
        history.transitions.filter(function (t) { return t.to_stage===stage.id && (current.leads || t.status==='documented'); }).forEach(function (transition) {
          const summary=T.el('button','timeline-change-link',keys.transitionKeys[transition.id]+' · '+words(transition.kind)+' · '+transition.summary);
          summary.type='button'; summary.setAttribute('data-transition',transition.id);
          summary.id=context+'-transition-'+transition.id;
          if (current.transition===transition.id) summary.setAttribute('aria-current','true');
          summary.addEventListener('click',function () { select('transition',transition.id); }); article.appendChild(summary);
          article.appendChild(T.el('p','panel-note',words(transition.evidence_level)+' · '+transition.status+' · parentage '+transition.historical_parentage));
        }); return article;
      }

      function dateBounds(tradition,global) {
        const dated=history.stages.filter(function (s) { return (s.status==='documented' || (current && current.leads)) && Number.isFinite(s.start_year) && (global || tradition==='all' || s.tradition_id===tradition); });
        if (!dated.length) return {start:keys.start,end:keys.end};
        const first=Math.min.apply(null,dated.map(function (s) { return s.start_year; }));
        const last=Math.max.apply(null,dated.map(function (s) { return s.end_year; }));
        return {start:Math.floor(first/50)*50,end:Math.max(Math.floor(first/50)*50+50,Math.ceil(last/50)*50)};
      }

      function update(state) { current=state; T.writeHash(timelinePairs(state)); render(state); }

      function render(state) {
        current={...state};
        presentation.value=['chart','list'].includes(current.presentation) ? current.presentation : defaultPresentation;
        current.presentation=presentation.value;
        if (!current.tradition) {
          const selectedTransition=byTransition.get(current.transition);
          const selected=byStage.get(current.stage) || (selectedTransition && byStage.get(selectedTransition.to_stage));
          current.tradition=selected ? selected.tradition_id : history.default_tradition_id ||
            (history.traditions.find(function (t) { return history.stages.some(function (s) { return s.tradition_id===t.id && s.status==='documented'; }); }) || history.traditions[0]).id;
        }
        if (current.start===null || current.end===null) {
          const bounds=dateBounds(current.tradition,false); current.start=bounds.start; current.end=bounds.end;
          if (current.tradition!=='all' && current.end-current.start>600) {
            current.start=current.end-600;
            const selected=byStage.get(current.stage);
            if (selected && Number.isFinite(selected.start_year) && selected.end_year<current.start) {
              current.start=Math.floor(selected.start_year/50)*50;
              current.end=Math.max(current.start+600,Math.ceil(selected.end_year/50)*50);
            }
          }
        }
        if ((current.start!==null || current.end!==null) && (!Number.isFinite(current.start) || !Number.isFinite(current.end) || current.end<=current.start)) {
          T.clear(detail); detail.hidden=true;
          detail.setAttribute('aria-label','Selected state or transition evidence');
          status.textContent='Choose an ending year later than the starting year.';
          status.setAttribute('tabindex','-1'); status.focus(); return;
        }
        const options={start:current.start,end:current.end,includeProvisional:current.leads,width:1600,compact:true,inlineSummary:true};
        if (current.tradition!=='all') options.tradition=current.tradition;
        model=M.stageLayout(history,options);
        ['timeline-start','timeline-end','timeline-apply','timeline-all-years','timeline-local-years','timeline-earlier','timeline-later','timeline-zoom-in','timeline-zoom-out'].forEach(function (id) {
          document.getElementById(id).disabled=model.start===null;
        });
        traditionControl.value=current.tradition; startControl.value=current.start===null ? '' : String(current.start); endControl.value=current.end===null ? '' : String(current.end); leadControl.checked=current.leads;
        T.clear(chart); T.clear(list);
        const inScope=function (s) { return current.tradition==='all' || s.tradition_id===current.tradition; };
        const scopedIds=new Set(history.stages.filter(inScope).map(function (s) { return s.id; }));
        const documented=history.transitions.filter(function (t) { return t.status==='documented' && scopedIds.has(t.to_stage); });
        const substantive=documented.filter(function (t) { return t.kind!=='witness-succession'; }).length;
        tally.textContent=model.counts.documented+' documented states · '+substantive+' documented revisions, branches or receptions · '+
          (documented.length-substantive)+' witness successions · '+model.counts.provisional+' provisional leads in the selected history.';
        status.textContent=(current.start===null ? 'No dated states; see unpositioned records below. ' : 'Showing '+current.start+'–'+current.end+': ')+model.counts.visible+' dated states; '+model.counts.outsideWindow+' dated states outside this window. '+
          'Date brackets are uncertainty bounds, not lifespans.';
        if (!model.lanes.length) status.textContent='This tradition is not in the current stage record: '+current.tradition;
        const drawing=svg('svg',{viewBox:'0 0 '+model.width+' '+model.height,width:model.width,height:model.height,'class':'stage-timeline',role:'group','aria-label':'Book states on a proportional year axis'});
        const defs=svg('defs',{}),marker=svg('marker',{id:'stage-arrow',viewBox:'0 0 12 12',refX:21,refY:6,markerWidth:12,markerHeight:12,markerUnits:'userSpaceOnUse',orient:'auto'});
        marker.appendChild(svg('path',{d:'M 0 0 L 12 6 L 0 12 z',fill:'#666'})); defs.appendChild(marker); drawing.appendChild(defs);
        model.axis.ticks.forEach(function (tick) {
          drawing.appendChild(svg('path',{d:'M '+tick.x+' 60 V '+model.height,stroke:'#ddd','stroke-width':1}));
          const label=svg('text',{x:tick.x,y:40,'text-anchor':'middle','font-size':18}); label.textContent=String(tick.year); drawing.appendChild(label);
        });
        const axisTitle=svg('text',{x:24,y:40,'font-size':18}); axisTitle.textContent='Year · same scale in every lane'; drawing.appendChild(axisTitle);
        model.lanes.forEach(function (lane) {
          drawing.appendChild(svg('path',{d:'M 15 '+lane.top+' H '+(model.width-15),stroke:'#aaa','stroke-width':1}));
          lane.labelLines.forEach(function (line,i) { const label=svg('text',{x:18,y:lane.top+28+i*22,'font-size':18,'font-weight':600}); label.textContent=line; drawing.appendChild(label); });
          const count=svg('text',{x:18,y:lane.top+40+lane.labelLines.length*22,'font-size':14}); count.textContent=lane.visibleCount+' dated states in this window'; drawing.appendChild(count);
          const section=T.el('section','timeline-list-lane'); section.appendChild(T.el('h3',null,lane.label));
          section.appendChild(T.el('p','panel-note',lane.tradition.scope));
          if (lane.tradition.coverage_note) section.appendChild(T.el('p','panel-note',lane.tradition.coverage_note));
          lane.nodes.forEach(function (node) { section.appendChild(readingCard(node.stage)); }); list.appendChild(section);
        });
        const transitionKeys=svg('g',{'data-layer':'transition-keys'});
        model.edges.forEach(function (edge) {
          const linkAttrs={href:'#'+new URLSearchParams(timelinePairs({...current,stage:null,transition:edge.id}).filter(function (p) { return p[1]; })),
            'aria-label':edge.key+' '+words(edge.transition.kind)+': '+edge.transition.summary+'; '+edge.style.label};
          const link=svg('a',linkAttrs);
          link.addEventListener('click',function (event) { event.preventDefault(); select('transition',edge.id); });
          link.appendChild(svg('path',{d:edge.path,fill:'none',stroke:'#666','stroke-width':edge.style.width,'stroke-dasharray':edge.style.dash,'marker-end':'url(#stage-arrow)','data-transition':edge.id}));
          const title=svg('title',{}); title.textContent=edge.key+' · '+edge.transition.summary+' · '+edge.style.label; link.appendChild(title);
          const keyLink=svg('a',linkAttrs);
          keyLink.id='timeline-chart-transition-'+edge.id;
          if (current.transition===edge.id) keyLink.setAttribute('aria-current','true');
          keyLink.addEventListener('click',function (event) { event.preventDefault(); select('transition',edge.id); });
          keyLink.appendChild(svg('rect',{x:edge.keyLabel.x-34,y:edge.keyLabel.y-13,width:38,height:17,fill:'#fffdf8'}));
          const key=svg('text',{x:edge.keyLabel.x,y:edge.keyLabel.y,'text-anchor':'end','font-size':12,fill:'#444','data-transition-key':edge.id}); key.textContent=edge.key; keyLink.appendChild(key);
          transitionKeys.appendChild(keyLink);
          [['from',edge.fromOutside,edge.fromPoint,edge.fromStage,edge.fromKey],['to',edge.toOutside,edge.toPoint,edge.toStage,edge.toKey]].forEach(function (end) {
            if (!end[1]) return;
            const point=end[2],stage=end[3],left=point.x+230>model.width;
            const year=stage.start_year===null ? 'undated' : stage.start_year===stage.end_year ? String(stage.start_year) : stage.start_year+'–'+stage.end_year;
            link.appendChild(svg('circle',{cx:point.x,cy:point.y,r:4,fill:'#fffdf8',stroke:'#666','data-continuation':stage.id}));
            const label=svg('text',{x:point.x+(left ? -8 : 8),y:point.y-10,'font-size':12,'text-anchor':left ? 'end' : 'start'});
            label.textContent=(end[0]==='from' ? 'From ' : 'To ')+end[4]+' · '+year+' · outside this view'; link.appendChild(label);
          });
          drawing.appendChild(link);
        });
        drawing.appendChild(transitionKeys);
        model.lanes.forEach(function (lane) { lane.nodes.forEach(function (node) {
          const stage=node.stage,link=svg('a',{href:'#'+new URLSearchParams(timelinePairs({...current,stage:stage.id,transition:null}).filter(function (p) { return p[1]; })),
            'data-stage':stage.id,'aria-label':stage.label+'; '+stage.date_label+'; '+stage.status+'; text '+stage.text_coverage});
          link.id='timeline-chart-stage-'+stage.id;
          if (current.stage===stage.id) link.setAttribute('aria-current','true');
          link.addEventListener('click',function (event) { event.preventDefault(); select('stage',stage.id); });
          link.appendChild(svg('rect',{x:node.labelX-7,y:node.labelY-17,width:node.cardWidth+14,height:node.cardHeight,rx:4,fill:'#fffdf8',stroke:'#ded8cb'}));
          if (stage.start_year!==stage.end_year) link.appendChild(svg('path',{
            d:(node.clippedStart ? 'M '+(node.xStart+4)+' '+(node.y-5)+' l -4 5 4 5' : 'M '+node.xStart+' '+(node.y-6)+' V '+(node.y+6))+
              ' M '+node.xStart+' '+node.y+' H '+node.xEnd+
              (node.clippedEnd ? ' M '+(node.xEnd-4)+' '+(node.y-5)+' l 4 5 -4 5' : ' M '+node.xEnd+' '+(node.y-6)+' V '+(node.y+6)),
            fill:'none',stroke:'#7a5230','stroke-width':2,'stroke-dasharray':'4 3','data-date-range':'date-uncertainty','data-date-clipped':(node.clippedStart ? 'start ' : '')+(node.clippedEnd ? 'end' : '')}));
          link.appendChild(svg(stage.status==='provisional' ? 'path' : 'circle',stage.status==='provisional'
            ? {d:'M '+node.x+' '+(node.y-7)+' l 7 7 -7 7 -7 -7 z',fill:'#fff',stroke:'#7a5230','stroke-width':2}
            : {cx:node.x,cy:node.y,r:6,fill:'#7a5230'}));
          const keyLeft=node.x+48>model.width;
          const key=svg('text',{x:node.x+(keyLeft ? -14 : 14),y:node.y-10,'text-anchor':keyLeft ? 'end' : 'start','font-size':12}); key.textContent=node.key; link.appendChild(key);
          let y=node.labelY;
          [node.labelLines,node.dateLines,node.scopeLines,node.coverageLines,node.changeLines].forEach(function (lines,group) {
            lines.forEach(function (line) { const text=svg('text',{x:node.labelX,y:y,'font-size':group===0 ? 16 : 14,'font-weight':group===0 ? 600 : 400}); text.textContent=line; link.appendChild(text); y+=node.leading; });
          });
          drawing.appendChild(link);
        }); });
        chart.appendChild(drawing); chart.setAttribute('aria-busy','false');
        chart.hidden=presentation.value==='list'; list.hidden=presentation.value!=='list';
        [['timeline-unpositioned-list',model.unpositioned],['timeline-provisional-list',model.provisional]].forEach(function (pair) {
          const host=document.getElementById(pair[0]); T.clear(host);
          if (!pair[1].length) host.appendChild(T.el('p','panel-note','None recorded in this selection.'));
          pair[1].forEach(function (stage) { host.appendChild(readingCard(stage,pair[0])); });
        });
        const gaps=document.getElementById('timeline-gaps'); T.clear(gaps); gaps.appendChild(T.el('h3',null,'What this history does not yet establish'));
        const selectedGaps=history.gaps.filter(function (g) { return current.tradition==='all' || g.tradition_id===current.tradition; });
        selectedGaps.forEach(function (gap) {
          const section=T.el('section','timeline-gap'); section.appendChild(T.el('h4',null,gap.period));
          section.appendChild(T.el('p',null,gap.missing)); section.appendChild(T.el('p',null,gap.consequence));
          section.appendChild(T.el('p','panel-note','Next source to examine: '+gap.next_source)); gaps.appendChild(section);
        });
        if (!selectedGaps.length) gaps.appendChild(T.el('p','panel-note','No specific gap is listed for this selection. This does not establish complete coverage.'));
        showDetail();
      }

      document.getElementById('timeline-filter').addEventListener('submit',function (event) {
        event.preventDefault();
        const first=Number(startControl.value),last=Number(endControl.value);
        if (!startControl.value || !endControl.value || !Number.isInteger(first) || !Number.isInteger(last) || last<=first) { status.textContent='Enter whole years, with the ending year later than the starting year.'; return; }
        update({...current,tradition:traditionControl.value,start:first,end:last,leads:leadControl.checked});
      });
      traditionControl.addEventListener('change',function () { update({...current,tradition:traditionControl.value,start:null,end:null,stage:null,transition:null}); });
      leadControl.addEventListener('change',function () { update({...current,leads:leadControl.checked}); });
      presentation.addEventListener('change',function () { update({...current,presentation:presentation.value}); });
      document.getElementById('timeline-all-years').addEventListener('click',function () { update({...current,...dateBounds(current.tradition,true)}); });
      document.getElementById('timeline-local-years').addEventListener('click',function () { update({...current,...dateBounds(current.tradition,false)}); });
      [['timeline-earlier',-1],['timeline-later',1]].forEach(function (pair) { document.getElementById(pair[0]).addEventListener('click',function () {
        const step=Math.max(1,Math.round((current.end-current.start)/2))*pair[1]; update({...current,start:current.start+step,end:current.end+step});
      }); });
      [['timeline-zoom-in',0.5],['timeline-zoom-out',2]].forEach(function (pair) { document.getElementById(pair[0]).addEventListener('click',function () {
        const span=Math.max(10,Math.round((current.end-current.start)*pair[1])),center=(current.end+current.start)/2;
        update({...current,start:Math.floor(center-span/2),end:Math.ceil(center+span/2)});
      }); });
      T.onHashChange(function (params) { render(timelineState(params)); revealSelection(); });
      render(timelineState(T.readHash())); revealSelection();
    } catch(error) {
      T.doneBootstrapping(); T.clear(chart); chart.setAttribute('aria-busy','false');
      status.textContent='Historical timeline unavailable: '+String(error.message || error);
    }
  }

  const catalogueMode = new URLSearchParams(window.location.search).get('view') === 'catalogue';
  const overviewMode = new URLSearchParams(window.location.search).get('view') === 'overview';
  const requestedView = new URLSearchParams(window.location.search).get('view');
  const legacyMapAddress = new URLSearchParams(window.location.search).has('slice') || T.readHash().has('station') || T.readHash().has('unit');
  const timelineMode = requestedView==='timeline' || (!requestedView && !legacyMapAddress);
  const timelineNav=document.getElementById('history-timeline-link');
  if (timelineNav) timelineNav.href=historyURL('timeline');
  const mapLink = document.getElementById('history-map-link');
  const catalogueNav = document.getElementById('history-catalogue-link');
  if (mapLink && catalogueNav) {
    mapLink.href = historyURL('map');
    catalogueNav.href = historyURL('catalogue');
    (catalogueMode ? catalogueNav : mapLink).setAttribute('aria-current', 'page');
    (catalogueMode ? mapLink : catalogueNav).removeAttribute('aria-current');
  }
  const overviewNav = document.getElementById('history-overview-link');
  const overviewScope = document.getElementById('map-overview-link');
  if (overviewScope) overviewScope.href = historyURL('overview');
  if (overviewNav) {
    overviewNav.href = historyURL('overview');
    if (overviewMode) {
      overviewNav.setAttribute('aria-current','page');
      mapLink.removeAttribute('aria-current');
    }
  }
  if (catalogueMode || overviewMode) {
    document.getElementById('historical-map').hidden = true;
    document.getElementById('catalogue').hidden = false;
    T.setInlineNotice('The source catalogue could not be reached. Serve this page over HTTP with its generated data.');
    startCatalogue();
    return;
  }
  if (timelineMode) {
    document.getElementById('historical-map').hidden=true;
    document.getElementById('catalogue').hidden=true;
    document.getElementById('timeline').hidden=false;
    if (timelineNav) timelineNav.setAttribute('aria-current','page');
    if (mapLink) mapLink.removeAttribute('aria-current');
    T.setInlineNotice('The historical timeline could not be reached. Serve this page with its generated source data.');
    startTimeline();
    return;
  }

  document.getElementById('history-act-note').hidden=false;
  T.setInlineNotice(
    'The act history could not be reached, so this page has nothing to show. ' +
    'Serve the pages over HTTP with the data at "' + T.dataRoot + '".'
  );
  chosenSlice().then(function (slice) {
    if (!slice) throw new Error(T.dataPath(MANIFEST) + ' names no slice to open');
    SLICE = slice;
    ROOT = 'structure/act-history/' + SLICE;
    return T.loadJSON(ROOT + '.json').then(function (data) {
      // Bootstrapping ends the moment the spine is in hand, exactly as the
      // other pages end it. Left on, the shared loader treats EVERY later
      // fetch failure as proof that no data root exists and banners it, so a
      // station fragment that goes missing halfway through a session was
      // reported as a missing corpus rather than as the error it was.
      T.doneBootstrapping();
      start(data);
    });
  }).catch(function (error) {
    T.doneBootstrapping();
    T.clear(map);
    map.setAttribute('aria-busy', 'false');
    map.appendChild(T.el('p', 'placeholder',
      'The line could not be loaded: ' + String(error.message || error)));
  });
}());
