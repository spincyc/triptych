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
     *   promulgated  an act stands behind it and its instrument is cited
     *   printed      a missal survives and no act has been located
     *
     * The difference is one of EVIDENCE, not of importance, and it is READ, never
     * inferred. Working it out from whether an instrument string happens to be
     * present is the guess this whole apparatus exists to prevent: a station
     * whose act is merely unread would come out looking like a station whose act
     * is not claimed at all, and the two are different claims.
     *
     * One allowance, and it is about the schema rather than about any station.
     * A file written before the distinction existed carries the field nowhere,
     * and every station in such a file is an act by the generator's own rule --
     * `act-history check` refuses a station without one. So a file that names the
     * field NOWHERE is read as all-promulgated; a file that names it ANYWHERE is
     * read literally, and a station missing it there is `unstated` and says so.
     * --------------------------------------------------------------------- */

    const PROMULGATED = 'promulgated';
    const PRINTED = 'printed';
    const UNSTATED = 'unstated';

    function statedKind(station) {
      const value = station && (station.station_kind || station.station);
      return typeof value === 'string' && value ? value : null;
    }

    /** Does this file speak the two-kinds vocabulary at all? */
    function kindsAreStated(stations) {
      return (stations || []).some(function (station) { return statedKind(station) !== null; });
    }

    function kindOf(station, stated) {
      const value = statedKind(station);
      if (value) return value;
      return stated ? UNSTATED : PROMULGATED;
    }

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
        extent: extent,
        afterBase: afterBase,
        shortName: shortName,
        year: year
      };
  }());
  const SLICE = 'roman-holy-week';
  const ROOT = 'structure/act-history/' + SLICE;
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

  function magnitude(station) {
    const changed = station.changed || {};
    return (changed.units_entered || 0) + (changed.units_gone || 0) +
      (changed.units_changed || 0) + (changed.masses_touched || 0) +
      (changed.unestablished || 0);
  }

  function draw() {
    const stations = spine.stations || [];
    if (!stations.length) {
      T.clear(map);
      map.setAttribute('aria-busy', 'false');
      map.appendChild(T.el('p', 'placeholder', 'This slice records no stations.'));
      return;
    }
    const at = M.layout(stations);
    const size = M.extent(at);
    const width = PAD * 2 + Math.max(size.cols - 1, 0) * COL;
    const height = PAD * 2 + Math.max(size.rows - 1, 0) * ROW + 46;

    const canvas = svg('svg', {
      viewBox: '0 0 ' + width + ' ' + height,
      width: width,
      height: height,
      role: 'img',
      'aria-label': 'The acts that changed this missal, drawn as a line with ' +
        stations.length + ' stations on ' + size.rows + ' tracks'
    });

    // Connectors first, so a station always sits above its own track.
    stations.forEach(function (station) {
      const kind = M.kindOf(station, kindsStated);
      (station.parents || []).forEach(function (parent) {
        if (!at.has(parent)) return;
        const classes = ['track', 'track-to-' + kind];
        // The record says the descent crosses an edition it does not hold, so
        // the connector says so rather than joining the ends.
        if ((station.via_unrepresented || []).length) classes.push('track-gap');
        canvas.appendChild(svg('path', {
          d: connector(at.get(parent), at.get(station.id)),
          class: classes.join(' '),
          fill: 'none'
        }));
      });
    });

    stations.forEach(function (station) {
      const where = at.get(station.id);
      const x = PAD + where.col * COL;
      const y = PAD + where.row * ROW;
      const kind = M.kindOf(station, kindsStated);
      const group = svg('g', {
        class: 'station line-' + station.line + ' kind-' + kind,
        tabindex: '0',
        role: 'button',
        'data-station': station.id,
        'aria-label': nameOf(station) + ', ' + station.date + ', ' + kind +
          ', ' + changeSummary(station)
      });
      group.appendChild(svg('circle', { cx: x, cy: y, r: 9, class: 'station-mark' }));
      const name = svg('text', { x: x, y: y - 24, class: 'station-name' });
      name.textContent = M.shortName(station.id);
      const when = svg('text', { x: x, y: y + 32, class: 'station-year' });
      when.textContent = M.year(station.date);
      const count = svg('text', { x: x, y: y + 48, class: 'station-count' });
      const moved = magnitude(station);
      count.textContent = moved ? moved + ' changed' : 'nothing changed';
      group.appendChild(name);
      group.appendChild(when);
      group.appendChild(count);
      group.addEventListener('click', function () { open(station.id); });
      group.addEventListener('keydown', function (event) {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          open(station.id);
        }
      });
      canvas.appendChild(group);
    });

    T.clear(map);
    const scroller = T.el('div', 'map-scroll');
    scroller.appendChild(canvas);
    map.appendChild(scroller);
    map.setAttribute('aria-busy', 'false');
  }

  function changeSummary(station) {
    const changed = station.changed;
    if (!changed) return 'what it changed is not carried in this file';
    const parts = [];
    if (changed.units_entered) parts.push(changed.units_entered + ' entered');
    if (changed.units_gone) parts.push(changed.units_gone + ' gone');
    if (changed.units_changed) parts.push(changed.units_changed + ' altered');
    if (changed.masses_touched) parts.push(changed.masses_touched + ' liturgies touched');
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

  const CITATION_WORDS = {
    'cited-in-corpus': 'the instrument was read in this project’s own corpus',
    'cited-externally': 'the instrument was read, in a witness held elsewhere',
    'not-found': 'the instrument was searched for and not found'
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
      return T.el('p', 'detail-weak',
        'A printed station. A missal survives and no act has been located for ' +
        'it, so nothing here claims one. That is a statement about the ' +
        'evidence and not about the size of the change: the book is present, ' +
        'the instrument is missing.');
    }
    if (kind === M.UNSTATED) {
      return T.el('p', 'detail-weak',
        'This file states which kind the other stations are and states nothing ' +
        'for this one, so it is left unsaid rather than assumed.');
    }
    return null;
  }

  function value(text, missing) {
    if (text) return T.el('span', 'value', text);
    const node = T.el('span', 'value value-absent', missing);
    return node;
  }

  const FIELD_NAMES = {
    mass: 'liturgy', slot: 'place', name: 'heading', incipit: 'incipit',
    text: 'text', order: 'order', title: 'title', day: 'day', hour: 'hour'
  };

  function fieldRow(field, before, after) {
    const row = T.el('div', 'field');
    row.appendChild(T.el('span', 'field-name', FIELD_NAMES[field] || field));
    const pair = T.el('div', 'field-pair');
    const long = field === 'text' || field === 'incipit';
    const missing = long
      ? 'the tracer does not carry these words'
      : 'not established';
    const was = T.el('div', 'field-side field-before');
    was.appendChild(value(before === undefined || before === null || before === ''
      ? '' : String(before), missing));
    const now = T.el('div', 'field-side field-after');
    now.appendChild(value(after === undefined || after === null || after === ''
      ? '' : String(after), missing));
    pair.appendChild(was);
    pair.appendChild(T.el('div', 'field-arrow', '→'));
    pair.appendChild(now);
    if (long) pair.className = 'field-pair field-pair-long';
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
        card.appendChild(fieldRow(field, before[field], after[field]));
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

    const link = T.el('button', 'link-button', 'Follow this prayer');
    link.type = 'button';
    link.addEventListener('click', function () { openUnit(row.unit); });
    card.appendChild(link);
    return card;
  }

  /** One side of a unit, printed whole — used where there is no other side. */
  function standing(side) {
    const wrap = T.el('div', 'standing');
    const line = T.el('p', 'standing-incipit');
    line.appendChild(value(side.incipit || '', 'the tracer does not carry these words'));
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

  function renderChanges(host, payload, station) {
    T.clear(host);
    const totals = payload.totals || {};
    host.appendChild(T.el('p', 'detail-summary', changeSummary(station) + '.'));

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

    if (payload.masses && payload.masses.length) {
      const block = section('The liturgies');
      payload.masses.forEach(function (row) { block.appendChild(massCard(row)); });
      host.appendChild(block);
    }
    if (payload.units && payload.units.length) {
      const block = section('The units');
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
          const link = T.el('button', 'link-button', 'Follow this prayer');
          link.type = 'button';
          link.addEventListener('click', function () { openUnit(row.unit); });
          return link;
        }()));
        block.appendChild(card);
      });
      host.appendChild(block);
    }
    if (!(payload.masses || []).length && !(payload.units || []).length &&
        !(payload.unestablished || []).length) {
      host.appendChild(T.el('p', 'detail-weak',
        'This act moved nothing in this slice. It keeps its station because an ' +
        'authority acted: a history keyed on diffs would have dropped it, and a ' +
        'history keyed on acts records that the authority spoke and this part of ' +
        'the book did not move. ' + (totals.standing || 0) +
        ' units stand after it.'));
    }
  }

  function renderState(host, payload) {
    T.clear(host);
    const totals = payload.totals || {};
    host.appendChild(T.el('p', 'detail-summary',
      totals.units + ' units across ' + totals.masses +
      ' liturgies, as this record holds them after ' + payload.title + '.'));
    (payload.masses || []).forEach(function (mass) {
      const block = T.el('section', 'mass');
      block.appendChild(T.el('h4', 'mass-title', mass.title || mass.mass));
      const meta = [mass.day, mass.hour].filter(Boolean).join(' · ');
      if (meta) block.appendChild(T.el('p', 'mass-meta', meta));
      if (!mass.units.length) {
        block.appendChild(T.el('p', 'detail-weak',
          'This record carries no unit standing in this liturgy at this point.'));
      }
      mass.units.forEach(function (unit) {
        const row = T.el('article', 'held');
        const head = T.el('h5', 'held-name');
        head.appendChild(document.createTextNode(unit.name || unit.slot));
        head.appendChild(T.el('span', 'held-slot', unit.slot));
        row.appendChild(head);
        const line = T.el('p', 'held-incipit');
        line.appendChild(value(unit.incipit || '',
          'the tracer read this unit’s heading and not its words'));
        row.appendChild(line);
        if (unit.text) row.appendChild(T.el('p', 'held-text', unit.text));
        const link = T.el('button', 'link-button', 'Follow this prayer');
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
    host.appendChild(T.el('p', 'placeholder', 'Not fetched yet.'));
    block.appendChild(host);
    let started = false;
    block.addEventListener('toggle', function () {
      if (!block.open || started) return;
      started = true;
      T.clear(host);
      host.appendChild(T.el('p', 'placeholder', 'Loading…'));
      fragment(path).then(function (payload) {
        render(host, payload);
      }).catch(function (error) {
        T.clear(host);
        host.appendChild(T.el('p', 'error',
          path + ' could not be read: ' + String(error.message || error)));
      });
    });
    return block;
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
    detail.appendChild(T.el('h2', 'detail-title', nameOf(station)));
    detail.appendChild(facts(station));
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
        'Two descents converge here, and a merge asserts that a reception ' +
        'happened. What this station shows below is what IT changed; what it ' +
        'received stands at '));
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
        'Read the missal as it stood after this act',
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
          card.appendChild(fieldRow(field, (stop.before || {})[field], (stop.after || {})[field]));
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
    pairs.forEach(function (pair) {
      const card = T.el('article', 'junction');
      card.appendChild(T.el('h3', 'junction-head',
        lineLabel(pair.a) + ' and ' + lineLabel(pair.b)));

      const bases = pair.shared_base || [];
      if (!bases.length) {
        // The commonest answer in liturgical history, and a finding rather than
        // a failure: two rites with no act in common in this record.
        card.appendChild(T.el('p', 'detail-weak',
          'No act in this record stands behind both lines, so they share no ' +
          'station here. That is a finding and not a gap: an edge drawn ' +
          'between them would be an invention. They may still hold the same ' +
          'prayer word for word — inheritance older than anything this record ' +
          'carries — and that comparison is made by the generator against the ' +
          'repository it emits, not here.'));
        card.appendChild(sideOfJunction(null, pair.a));
        card.appendChild(sideOfJunction(null, pair.b));
        linesView.appendChild(card);
        return;
      }

      const parted = pair.diverged_at || bases[bases.length - 1];
      const base = T.el('p', 'junction-base');
      base.appendChild(document.createTextNode(
        'The last act both lines descend from is '));
      base.appendChild(stationLink(parted));
      base.appendChild(document.createTextNode(
        '. Everything standing there is what the two lines held in common; ' +
        'everything below it is what each did afterwards.'));
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
          'Read what both lines held in common',
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
          : kind === M.PRINTED ? ' — a missal survives and no act has been located'
            : ' — this file says nothing about which')));
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
      ' lines, from ' + roots + (roots === 1 ? ' origin' : ' separate origins') +
      (lines.length ? ' — ' + lines.join('; ') : '');

    fillUnits();
    renderJunctions();

    // The last station in topological order is the furthest the record reaches,
    // which is where a reader with no other instruction should arrive.
    const wanted = fromHash();
    if (wanted.unit) openUnit(wanted.unit);
    if (wanted.station && byId.has(wanted.station)) open(wanted.station);
    else if (stations.length) open(stations[stations.length - 1].id);

    T.onHashChange(function (params) {
      const next = fromHash(params);
      if (next.unit && next.unit !== openedUnit) openUnit(next.unit);
      if (next.station && next.station !== selected && byId.has(next.station)) open(next.station);
    });
  }

  T.loadJSON(ROOT + '.json').then(start).catch(function (error) {
    T.clear(map);
    map.setAttribute('aria-busy', 'false');
    map.appendChild(T.el('p', 'placeholder',
      'The line could not be loaded: ' + String(error.message || error)));
  });
}());
