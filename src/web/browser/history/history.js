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
      // A group preserves the station buttons in the accessibility tree.
      role: 'group',
      'aria-describedby': 'legend',
      'aria-label': 'The acts this record carries, drawn as a line with ' +
        stations.length + ' stations on ' + size.rows + ' tracks'
    });

    // Connectors first, so a station always sits above its own track.
    stations.forEach(function (station) {
      const kind = M.kindOf(station, kindsStated);
      (station.parents || []).forEach(function (parent) {
        if (!at.has(parent)) return;
        const reception = receptionsOf(station).find(function (row) { return row.from === parent; });
        const classes = ['track', 'track-to-' + kind];
        if (reception) classes.push('track-reception');
        // The record says the descent crosses an edition it does not hold, so
        // the connector says so rather than joining the ends.
        if ((station.via_unrepresented || []).length) classes.push('track-gap');
        const path = svg('path', {
          d: connector(at.get(parent), at.get(station.id)),
          class: classes.join(' '),
          fill: 'none',
          'data-from': parent,
          'data-to': station.id,
          role: 'img',
          'aria-label': (reception ? 'Documented reception' : 'Recorded parent link') +
            ' from ' + nameOf(byId.get(parent)) + ' to ' + nameOf(station) +
            (reception ? ': ' + (RECEPTION_WORDS[reception.kind] || reception.kind)
              : station.parent_kind ? ': ' + station.parent_kind : '')
        });
        canvas.appendChild(path);
        // A hollow band distinguishes reception without borrowing the broken
        // stroke that already means an unrepresented edition.
        if (reception) canvas.appendChild(svg('path', {
          d: path.getAttribute('d'),
          class: 'track-reception-core' + (classes.includes('track-gap') ? ' track-gap' : ''),
          'aria-hidden': 'true'
        }));
      });
    });

    stations.forEach(function (station) {
      const where = at.get(station.id);
      const x = PAD + where.col * COL;
      const y = PAD + where.row * ROW;
      const kind = M.kindOf(station, kindsStated);
      const received = receptionsOf(station);
      const group = svg('g', {
        class: 'station line-' + station.line + ' kind-' + kind +
          (received.length ? ' station-interchange' : ''),
        tabindex: '0',
        role: 'button',
        'data-station': station.id,
        'aria-label': nameOf(station) + ', ' + station.date + ', ' + kind +
          ', ' + changeSummary(station) +
          (received.length ? ', documented reception from ' + received.map(function (row) {
            return nameOf(byId.get(row.from));
          }).join('; ') : '')
      });
      if (received.length) group.appendChild(svg('circle', {
        cx: x, cy: y, r: 16, class: 'station-interchange-ring', 'aria-hidden': 'true'
      }));
      group.appendChild(svg('circle', { cx: x, cy: y, r: 9, class: 'station-mark' }));
      const name = svg('text', { x: x, y: y - 24, class: 'station-name' });
      name.textContent = M.shortName(station.id);
      const when = svg('text', { x: x, y: y + 32, class: 'station-year' });
      when.textContent = M.year(station.date);
      const count = svg('text', { x: x, y: y + 48, class: 'station-count' });
      const moved = magnitude(station);
      count.textContent = kind === M.PROMULGATED
        ? (moved ? moved + ' changed' : 'nothing changed')
        : (moved ? moved + ' differ' : 'nothing differs');
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
    scroller.tabIndex = 0;
    scroller.setAttribute('role', 'region');
    scroller.setAttribute('aria-label', 'History map; scroll horizontally to reach further stations');
    scroller.appendChild(canvas);
    map.appendChild(scroller);
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
    else if (wanted.station) reportUnknownStation(wanted.station);
    else if (stations.length) open(stations[stations.length - 1].id);

    T.onHashChange(function (params) {
      const next = fromHash(params);
      if (next.unit && next.unit !== openedUnit) openUnit(next.unit);
      if (!next.station || next.station === selected) return;
      if (byId.has(next.station)) open(next.station);
      else reportUnknownStation(next.station);
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

  function catalogueValid(data) {
    const object = function (value) { return value && typeof value === 'object' && !Array.isArray(value); };
    const string = function (value) { return typeof value === 'string'; };
    const ids = new Set();
    if (!object(data) || data.schema !== 'triptych-eucharistic-history/v1' ||
        !Array.isArray(data.entries) || !Array.isArray(data.limitations) ||
        !data.limitations.every(string) || !Array.isArray(data.text_sets)) return false;
    return data.entries.every(function (row) {
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
    add('Tradition or use', row.family);
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
    target.appendChild(T.el('h4', null, 'Sources and access'));
    const sources = T.el('ul', 'catalogue-sources');
    row.sources.forEach(function (source) {
      const item = T.el('li', null);
      item.appendChild(catalogueLink(source.url, source.label || source.id || source.url));
      item.appendChild(T.el('p', 'panel-note', 'Inspection: ' + catalogueText(source.inspection)));
      sources.appendChild(item);
    });
    row.links.forEach(function (link) {
      if (row.sources.some(function (source) { return source.url === link.url; })) return;
      const item = T.el('li', null);
      item.appendChild(catalogueLink(link.url, link.label || link.kind || link.url));
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

  function comparisonValid(payload, declared) {
    if (!payload || payload.schema !== 'triptych-eucharistic-witness-comparison/v1' ||
        payload.id !== declared.id || payload.kind !== 'same-prayer-witness-comparison' ||
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
      catalogueComparisons(data);
      const families = Array.from(new Set(data.entries.map(function (row) { return row.family; }))).sort();
      families.forEach(function (name) {
        const option = T.el('option', null, name);
        option.value = name;
        family.appendChild(option);
      });
      family.disabled = query.disabled = document.getElementById('catalogue-search').disabled = false;
      tally.textContent = data.entries.length + ' source records across ' + families.length +
        ' traditions and uses. This is research coverage, not a count of complete missals.';
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
        const search = (params.get('q') || '').slice(0, 200);
        const record = params.get('record');
        // Preserve unknown filters visibly, rather than silently broadening a
        // shared URL to all traditions.
        let unknown = document.getElementById('catalogue-unknown-family');
        if (unknown) unknown.remove();
        if (selectedFamily && families.indexOf(selectedFamily) === -1) {
          unknown = T.el('option', null, selectedFamily + ' (not in this catalogue)');
          unknown.id = 'catalogue-unknown-family';
          unknown.value = selectedFamily;
          family.appendChild(unknown);
        }
        family.value = selectedFamily;
        query.value = search;
        const terms = search.toLocaleLowerCase().split(/\s+/).filter(Boolean);
        const rows = data.entries.filter(function (row) {
          const haystack = [row.title, row.family, row.date_label, row.id,
            JSON.stringify(row.source_record)].join(' ').toLocaleLowerCase();
          return (!selectedFamily || row.family === selectedFamily) &&
            terms.every(function (term) { return haystack.indexOf(term) !== -1; });
        });
        T.clear(results);
        status.textContent = rows.length + ' of ' + data.entries.length + ' source records shown.';
        if (!rows.length) results.appendChild(T.el('p', null, 'No records match these filters. Clear the search or choose another tradition.'));
        const sections = [
          { title: 'Dated records', rows: rows.filter(function (row) { return row.chronology; })
            .sort(function (a, b) { return a.chronology.start - b.chronology.start || a.title.localeCompare(b.title); }) },
          { title: 'Undated or unresolved', rows: rows.filter(function (row) { return !row.chronology; }) }
        ];
        sections.forEach(function (section) {
          if (!section.rows.length) return;
          results.appendChild(T.el('h3', 'catalogue-period', section.title + ' (' + section.rows.length + ')'));
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
            body.appendChild(T.el('p', 'catalogue-entry-meta', row.family + ' · ' + row.record_kind));
            body.appendChild(T.el('p', 'catalogue-entry-meta', 'Evidence: ' + row.evidence_status +
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

  const catalogueMode = new URLSearchParams(window.location.search).get('view') === 'catalogue';
  const mapLink = document.getElementById('history-map-link');
  const catalogueNav = document.getElementById('history-catalogue-link');
  if (mapLink && catalogueNav) {
    mapLink.href = historyURL('map');
    catalogueNav.href = historyURL('catalogue');
    (catalogueMode ? catalogueNav : mapLink).setAttribute('aria-current', 'page');
    (catalogueMode ? mapLink : catalogueNav).removeAttribute('aria-current');
  }
  if (catalogueMode) {
    document.getElementById('historical-map').hidden = true;
    document.getElementById('catalogue').hidden = false;
    T.setInlineNotice('The source catalogue could not be reached. Serve this page over HTTP with its generated data.');
    startCatalogue();
    return;
  }

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
