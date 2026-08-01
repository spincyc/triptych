/* The missal line, drawn as a transit map.
 *
 * The map is derived from structure/act-history/<slice>.json and from nothing
 * else. Stations arrive in the graph's own topological order, so a station can
 * be placed to the right of the act it descends from without this file
 * deciding anything the history does not already state.
 *
 * Two things the drawing must not smooth over, because they are the record:
 * a line that forks and rejoins really did fork, and a connector marked
 * unrepresented really does cross an edition this tracer does not carry.
 */
(function () {
  'use strict';

  const T = window.Triptych;
  const SLICE = 'roman-holy-week';
  const NS = 'http://www.w3.org/2000/svg';

  const COL = 190;   // horizontal distance between stations
  const ROW = 96;    // vertical distance between tracks
  const PAD = 64;

  const map = document.getElementById('map');
  const tally = document.getElementById('tally');
  const detail = document.getElementById('detail');

  function svg(name, attrs) {
    const node = document.createElementNS(NS, name);
    for (const key of Object.keys(attrs || {})) {
      node.setAttribute(key, String(attrs[key]));
    }
    return node;
  }

  /* A station's short name is taken from its id rather than composed: the id
   * is the act's own slug, and the trailing year is already shown beneath. */
  function shortName(station) {
    const parts = String(station.id).split('-');
    if (/^\d{4}$/.test(parts[parts.length - 1])) parts.pop();
    const words = parts.join(' ');
    return words.charAt(0).toUpperCase() + words.slice(1);
  }

  function year(station) {
    return String(station.date).slice(0, 4);
  }

  /* Lane assignment, the same shape a git graph uses.
   *
   * A station continues the track of a parent that is still that track's head
   * and stands on its own line; among several it takes the lowest such track,
   * which is what pulls a rejoining branch back toward the trunk instead of
   * leaving the trunk stranded. Anything else opens a new track, and that is
   * how a fork becomes visible rather than being drawn through.
   */
  function layout(stations) {
    const at = new Map();
    const head = [];          // row -> id currently at the end of that row
    const lineOf = new Map();
    stations.forEach(function (station) { lineOf.set(station.id, station.line); });

    stations.forEach(function (station, col) {
      let row = -1;
      (station.parents || []).forEach(function (parent) {
        const found = head.indexOf(parent);
        if (found === -1) return;
        if (lineOf.get(parent) !== station.line) return;
        if (row === -1 || found < row) row = found;
      });
      if (row === -1) row = head.length;
      head[row] = station.id;
      at.set(station.id, { col: col, row: row });
    });
    return at;
  }

  function connector(from, to, unrepresented) {
    const x1 = PAD + from.col * COL;
    const y1 = PAD + from.row * ROW;
    const x2 = PAD + to.col * COL;
    const y2 = PAD + to.row * ROW;
    let d;
    if (y1 === y2) {
      d = 'M ' + x1 + ' ' + y1 + ' L ' + x2 + ' ' + y2;
    } else {
      // One bend, at the octilinear 45°, then straight in. A curve here would
      // suggest a gradual change where the record has a single act.
      const step = Math.min(Math.abs(y2 - y1), Math.abs(x2 - x1) / 2);
      const turn = y2 > y1 ? step : -step;
      d = 'M ' + x1 + ' ' + y1 +
          ' L ' + (x1 + step) + ' ' + (y1 + turn) +
          ' L ' + (x2 - step) + ' ' + y2 +
          ' L ' + x2 + ' ' + y2;
    }
    return svg('path', {
      d: d,
      class: 'track' + (unrepresented ? ' track-gap' : ''),
      fill: 'none'
    });
  }

  function show(station) {
    T.clear(detail);
    detail.hidden = false;
    detail.appendChild(T.el('h2', 'detail-title', station.title || shortName(station)));
    const rows = [
      ['Date', station.date + (station.date_precision && station.date_precision !== 'day'
        ? ' (' + station.date_precision + ')' : '')],
      ['Authority', station.authority],
      ['Instrument', station.instrument],
      ['Kind', station.kind],
      ['Line', station.line]
    ];
    const list = T.el('dl', 'detail-list');
    rows.forEach(function (row) {
      if (!row[1]) return;
      list.appendChild(T.el('dt', null, row[0]));
      list.appendChild(T.el('dd', null, String(row[1])));
    });
    detail.appendChild(list);
    if (station.departures && station.departures.length) {
      detail.appendChild(T.el('p', 'detail-departures',
        'Departures recorded at this act: ' + station.departures.join(', ') + '.'));
    }
    if (station.via_unrepresented && station.via_unrepresented.length) {
      detail.appendChild(T.el('p', 'detail-gap',
        'The descent runs through ' + station.via_unrepresented.join(', ') +
        ', which this tracer does not represent.'));
    }
  }

  function draw(data) {
    const stations = data.stations || [];
    const at = layout(stations);
    const cols = stations.length;
    const rows = Math.max.apply(null, stations.map(function (s) { return at.get(s.id).row; })) + 1;
    const width = PAD * 2 + (cols - 1) * COL;
    const height = PAD * 2 + (rows - 1) * ROW + 90;

    const canvas = svg('svg', {
      viewBox: '0 0 ' + width + ' ' + height,
      width: width,
      height: height,
      role: 'img',
      'aria-label': 'The acts of the Roman Holy Week, drawn as a line with ' +
        cols + ' stations'
    });

    const byId = new Map();
    stations.forEach(function (s) { byId.set(s.id, s); });

    // Connectors first, so a station always sits above its own track.
    stations.forEach(function (station) {
      (station.parents || []).forEach(function (parent) {
        if (!at.has(parent)) return;
        const gap = (station.via_unrepresented || []).length > 0;
        canvas.appendChild(connector(at.get(parent), at.get(station.id), gap));
      });
    });

    stations.forEach(function (station) {
      const where = at.get(station.id);
      const x = PAD + where.col * COL;
      const y = PAD + where.row * ROW;
      const group = svg('g', {
        class: 'station line-' + station.line,
        tabindex: '0',
        role: 'button',
        'aria-label': (station.title || shortName(station)) + ', ' + station.date
      });
      group.appendChild(svg('circle', { cx: x, cy: y, r: 9, class: 'station-mark' }));
      const name = svg('text', { x: x, y: y - 22, class: 'station-name' });
      name.textContent = shortName(station);
      const when = svg('text', { x: x, y: y + 32, class: 'station-year' });
      when.textContent = year(station);
      group.appendChild(name);
      group.appendChild(when);
      group.addEventListener('click', function () { show(station); });
      group.addEventListener('keydown', function (event) {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          show(station);
        }
      });
      canvas.appendChild(group);
    });

    T.clear(map);
    const scroller = T.el('div', 'map-scroll');
    scroller.appendChild(canvas);
    map.appendChild(scroller);
    map.setAttribute('aria-busy', 'false');

    const lines = (data.lines || []).map(function (line) { return line.label; });
    tally.textContent = stations.length + ' stations on ' +
      (data.lines || []).length + ' lines' +
      (lines.length ? ' — ' + lines.join('; ') : '');

    show(stations[stations.length - 1]);
  }

  T.loadJSON('structure/act-history/' + SLICE + '.json').then(draw).catch(function (error) {
    T.clear(map);
    map.setAttribute('aria-busy', 'false');
    map.appendChild(T.el('p', 'placeholder',
      'The line could not be loaded: ' + String(error.message || error)));
  });
}());
