'use strict';
/*
 * The Code, Canon by Canon (`src/web/browser/law/`), as law.js assembles it.
 *
 * Canon identity, grouping, lookup, the three states of a canon's words and
 * the wording of an authentic interpretation are `code-model.js`'s, loaded as
 * the law page loads it (window.TriptychCode over the real stationKind rule).
 * The page's glossaries, its kind rule and its extent sentence are sliced out
 * of law.js itself (page-slice.js), so they are the page's and not a copy.
 *
 * What lives only in law.js closures — the lookup flow, the assembly of a
 * canon around its paragraphs, an act's change set grouped by division — is
 * repeated as `PORT:` with its law.js lines, and the page's prose as `page:`.
 *
 * The record is always the code-of-canon-law slice, as the page's default
 * (law.js:72-74). No canon is mapped from one body of law to another, a
 * number the record does not carry is never answered with a neighbour, and
 * words the record withholds are never fetched from anywhere else.
 */
const extract = require('./page-slice.js');

module.exports = function law(realm) {
  const L = extract.law(realm);
  const C = L.C;
  const SLICE = 'code-of-canon-law'; // page: law.js:73
  const ROOT = 'structure/act-history/';

  const files = new Map();
  function file(relative) {
    if (!files.has(relative)) {
      const value = realm.read(ROOT + relative);
      if (value === undefined) throw new Error(ROOT + relative + ' could not be read');
      files.set(relative, value);
    }
    return files.get(relative);
  }

  let held = null;
  /* As law.js start() (1311-1316): the vocabulary first, then the kind rule. */
  function spine() {
    if (held) return held;
    const data = file(SLICE + '.json');
    const shape = C.readVocabulary(data);
    const stations = data.stations || [];
    L.setKindsStated(C.KIND.stated(stations));
    held = { data, shape, stations, byId: new Map(stations.map((s) => [s.id, s])) };
    return held;
  }

  let indexed = null;
  function index() { // PORT: law.js:548-559 loadIndex
    spine();
    if (indexed) return indexed;
    const payload = file(SLICE + '/units.json');
    C.learnGroups(payload);
    const rows = payload.units || [];
    indexed = { rows, byUnit: new Map(rows.map((row) => [row.unit, row])) };
    return indexed;
  }

  function lineLabel(id) { // page: law.js:110-113
    const line = (spine().data.lines || []).find((row) => row.id === id);
    return (line && line.label) || id || '';
  }
  const stationName = (station) => (station && (station.title || station.id)) || ''; // page: law.js:115-117
  function actRef(id) {
    if (!id) return null;
    const station = spine().byId.get(id);
    return { id, title: stationName(station) || id, date: (station && station.date) || '' };
  }

  /* ------------------------------------------------------------------------
   * Three states, never two, and the establishing act beside them
   * --------------------------------------------------------------------- */

  function established(id) { // PORT: law.js:133-145 establishedNote
    if (!id) return null;
    const act = actRef(id);
    return { act: id, title: act.title, sentence: 'Text established by ' + act.title + (act.date ? ' (' + act.date + ')' : '') +
      '. The words are not here; which act put them there is.' };
  }

  // page: law.js:163
  const UNREAD = 'This record carries this canon’s identity and place and has not read its words.';

  function body(found, unreadWords) { // PORT: law.js:147-168 bodyNode
    if (found.state === C.PRESENT) return { state: 'present', text: found.text };
    if (found.state === C.WITHHELD) {
      return { state: 'withheld', lead: 'Text withheld here. ', reason: found.reason, established: established(found.established) };
    }
    return { state: 'unread', text: unreadWords || UNREAD, established: established(found.established) };
  }

  function side(found, unreadWords) { // PORT: law.js:170-194 sideNode
    if (!found) return { nothing: 'Nothing stood here.' };
    const editions = C.editionsOf(found);
    if (editions.length) {
      return { editions: editions.map((edition) => ({ label: edition.label, language: edition.language, body: body(edition.body, unreadWords) })) };
    }
    return { body: body(C.bodyOf(found), unreadWords) };
  }

  function basis(stop) { // PORT: law.js:237-248 citations
    return (stop.cited || []).filter((entry) => entry.basis || entry.note).map((entry) => ({ kind: entry.kind || 'basis', text: entry.basis || entry.note }));
  }

  function interpretation(row) { // PORT: law.js:264-310 interpretationNode
    const card = { force: C.forceWords(row.force) };
    if (row.papal_act) card.papal = C.papalActWords(row.papal_act);
    if (row.withheld) card.withheld = 'The words of this responsum are not printed here: ' + row.withheld;
    if (row.dubium) card.question = { label: 'Dubium', text: row.dubium };
    else if (row.question) card.question = { label: 'The question asked, in this record’s words', text: row.question };
    if (row.responsum) card.answer = { label: 'Responsum', text: row.responsum };
    else if (row.answer) card.answer = { label: 'The answer given, in this record’s words', text: row.answer };
    card.notes = [row.citation, row.basis, row.note, row.read_from ? 'read from: ' + row.read_from : ''].filter(Boolean);
    return card;
  }

  function stopCard(stop) { // PORT: law.js:360-415 stopCard
    const interpreted = C.isInterpretation(stop);
    const meta = [stop.date, stop.instrument || 'instrument not carried here'];
    if (stop.station_kind && stop.station_kind !== C.KIND.PROMULGATED) meta.push(stop.station_kind);
    const card = { act: stop.act, title: stop.title || stop.act, what: L.whatHappened(stop), meta: meta.join(' · '),
      state: interpreted ? 'interpreted' : stop.state, basis: basis(stop), marker: stop.marker || '',
      link: 'Everything this act reached' };
    if (interpreted) {
      card.note = 'The canon did not change. An authentic interpretation settles what it ' +
        'means and alters not one word of what it says, so nothing is shown ' +
        'here as a before and an after.';
      if (stop.interpretation) card.interpretation = interpretation(stop.interpretation);
    } else if (stop.state === 'changed') {
      card.before = side(stop.before);
      card.after = side(stop.after);
      card.fields = (stop.fields || []).length ? 'Fields that differ: ' + stop.fields.join(', ') + '.'
        : 'The act records a departure here and the state it leaves is the same in every field this record carries.';
    } else card.standing = side(stop.state === 'gone' ? stop.before : stop.after);
    return card;
  }

  function paragraph(row, history, marked) { // PORT: law.js:312-358 paragraphSection
    const stops = (history && history.stations) || [];
    const changes = stops.filter((stop) => !C.isInterpretation(stop));
    const readings = stops.filter(C.isInterpretation);
    const last = changes.length ? changes[changes.length - 1] : null;
    const standing = history && history.standing !== false;
    const entered = actRef(history && history.entered_at);
    const left = !standing && history.left_at ? actRef(history.left_at) : null;
    return {
      citation: C.citationOf(row.name ? row : history), unit: row.unit, asked: marked,
      asked_mark: marked ? 'the paragraph you cited' : '',
      state: changes.length + (changes.length === 1 ? ' act touches it' : ' acts touch it') +
        (readings.length ? ', and ' + readings.length + (readings.length === 1 ? ' interpretation settles' : ' interpretations settle') +
          ' what it means' : '') + '. It enters at ' + (entered ? entered.title : '') +
        (standing ? '. It still stands at the end of the line this record draws.' : '. It ceases at ' + (left ? left.title + '.' : '')),
      entered, left, standing,
      now_heading: standing ? 'As it stands' : 'As it last stood',
      now: side(last && (last.after || last.before),
        'This record carries this canon’s identity and its place in the Code, and has not read its words.'),
      through: stops.map(stopCard),
      through_none: stops.length ? '' : 'No act in this record touches it.',
    };
  }

  function correspondence(rows) { // PORT: law.js:417-461
    const { byUnit } = index();
    const claims = rows.reduce((all, row) => all.concat(row.correspondence || []), []);
    if (!claims.length) {
      return { heading: 'Against the other body of law', note: 'This record maps this canon onto no canon of any other Code. The 1917 ' +
        'and 1983 numberings do not correspond — c. 1095 of one is not c. 1095 ' +
        'of the other, and there is no arithmetic that turns one into the other. ' +
        'Where a correspondence exists it is a scholarly claim with an author, ' +
        'and this page prints it only when the record carries one.', claims: [] };
    }
    return { heading: 'Against the other body of law', note: 'A correspondence between two Codes is a scholarly claim and never a ' +
      'mapping this page derived. Each one below is shown with the source that makes it.',
      claims: claims.map((claim) => {
        const other = byUnit.get(claim.unit);
        return { unit: other ? claim.unit : '', heading: (other ? C.citationOf(other) : claim.unit) + (other && other.line ? ' — ' + lineLabel(other.line) : ''),
          note: claim.note || '', source: claim.source || 'The record names no source for this claim.' };
      }) };
  }

  function canonView(entry) { // PORT: law.js:463-512 openCanon
    const paragraphs = entry.rows.map((row) => {
      const where = row.path || (SLICE + '/unit/' + row.unit + '.json'); // page: law.js:472 — the record's path first
      let history;
      try { history = file(where); } catch (error) {
        return { citation: C.citationOf(row), error: 'Its history could not be read: ' + String(error.message || error) };
      }
      return paragraph(row, history, Boolean(entry.asked) && C.paragraphOf(row) === String(entry.asked));
    });
    const first = entry.rows[0];
    const line = entry.line || '';
    return {
      view: 'canon', key: entry.key, canon: entry.canon, citation: C.canonCitation(entry.canon), line, line_label: lineLabel(line),
      place: C.chainOf(first).map((step) => ({ kind: step.kind, label: step.label })),
      place_none: C.chainOf(first).length ? '' : 'This record does not place this canon in the Code’s structure.',
      count: entry.rows.length === 1 ? 'One base unit in this record.'
        : entry.rows.length + ' paragraphs, each a base unit of this record with its own history.',
      correspondence: correspondence(entry.rows),
      paragraphs,
      status: C.canonCitation(entry.canon) + ': ' + entry.rows.length + (entry.rows.length === 1 ? ' base unit.' : ' paragraphs.'),
      asked: entry.asked || null,
    };
  }

  /* ------------------------------------------------------------------------
   * Looking a canon up
   * --------------------------------------------------------------------- */

  function lookup(text, line) { // PORT: law.js:581-608 lookUp
    const typed = String(text || '').trim();
    if (!typed) return { view: 'none', heading: '', message: '' };
    const { rows } = index();
    const cited = C.parseCitation(typed);
    let found = cited ? C.find(rows, cited) : [];
    let searched = false;
    if (!found.length) {
      found = C.canons(rows.filter((row) => C.matches(row, typed)));
      searched = true;
    }
    line = line || '';
    const chosen = line ? found.filter((entry) => L.inLine(entry, line)) : found;
    // The reader's own note, not the page's: the page falls through silently (law.js:636-641).
    const fell = searched && cited ? 'This record carries no canon numbered ' + cited.canon + '. As the page does, the ' +
      'lookup then searched for “' + typed + '” as text in each canon’s identity and division; what answers here ' +
      'matched that text, not that number.' : '';
    if (chosen.length === 1) return { ...canonView(chosen[0]), query: typed, fell_through: fell };
    // PORT: law.js:610-670 renderChoices
    const within = line ? ' in ' + lineLabel(line) : '';
    if (!chosen.length) {
      return { view: 'none', heading: typed, message: cited
        ? 'This record carries no canon numbered ' + cited.canon + within +
          '. That is a statement about this record and not about the Code: ' +
          'nothing here offers you a neighbouring canon instead' +
          (line ? ', and nothing hands you that number out of another body of law, ' +
            'because each body of law numbers independently and another ' +
            'body’s canon is the wrong law.'
            : ', because a neighbouring canon is the wrong law.')
        : 'Nothing' + (within || ' in this record') + ' answers to that. The ' +
          'lookup takes a citation — c. 1095, can. 1095 §2, or the number alone ' +
          '— or any word carried in a canon’s identity or in the division it ' +
          'stands in.',
      status: 'Nothing found for ' + typed + within + '.' };
    }
    const bodies = new Set(chosen.map((entry) => entry.line).filter(Boolean));
    return {
      view: 'choices', heading: typed, fell_through: fell,
      note: bodies.size > 1
        ? 'More than one canon answers to that. Each body of law numbers ' +
          'independently, so one number stands in more than one of them, and ' +
          'they are not the same canon.'
        : 'More than one canon answers to that, and they are not the same canon.',
      choices: chosen.map((entry) => ({
        key: entry.key, asked: entry.asked || null, citation: C.canonCitation(entry.canon), line: entry.line, line_label: lineLabel(entry.line),
        place: entry.group ? C.groupLabel(entry.group) : '', size: entry.rows.length === 1 ? '1 base unit' : entry.rows.length + ' paragraphs',
      })),
      status: chosen.length + ' canons answer to ' + typed + '.',
    };
  }

  /* Open one canon by the key a list of choices or the structure handed out. */
  function canon(key, asked) {
    const entry = C.canons(index().rows).find((candidate) => candidate.key === key);
    if (!entry) return { view: 'none', heading: key, message: 'This record carries no canon under ' + key + '.' };
    return canonView({ ...entry, asked: asked || null });
  }

  function unit(id) { // PORT: law.js:515-546 openUnit — the whole canon is assembled around the unit.
    const { rows, byUnit } = index();
    const row = byUnit.get(id);
    if (!row) return { view: 'none', heading: id, message: 'This record carries no unit called ' + id + '.' };
    const entry = C.canons([row])[0];
    const whole = C.canons(rows).filter((candidate) => candidate.key === entry.key)[0];
    return canonView({ ...(whole || entry), asked: C.paragraphOf(row) || null });
  }

  /* ------------------------------------------------------------------------
   * The acts, and what each one reached
   * --------------------------------------------------------------------- */

  function opening() {
    const { data, shape, stations } = spine();
    const lines = data.lines || [];
    return {
      slice: SLICE,
      heading: 'The Code, Canon by Canon',
      // page: law.js:1320-1325
      tally: stations.length + (stations.length === 1 ? ' act' : ' acts') + ' across ' + lines.length +
        (lines.length === 1 ? ' body of law' : ' bodies of law') +
        (lines.length ? ' — ' + lines.map((line) => line.label || line.id).join('; ') : ''),
      lines: lines.map((line) => ({ id: line.id, label: line.label || line.id, note: line.note || '',
        acts: stations.filter((s) => s.line === line.id).length })),
      // page: law.js:1349-1353
      banner: shape.vocabulary !== 'law' ? 'This record is not a body of law: its base units are ' + shape.unit_word +
        's standing in ' + shape.group_word + 's, and it says so itself. It is drawn here because the shape is the same, ' +
        'and nothing on this page calls them canons.' : '',
      // The record's own as-of date, if it declares one; it is never supplied.
      recorded_on: data.recorded_on || null,
      // page: law.js:1300-1302, its first words fitted to a box reached by a key
      invite: 'Press g and type a citation — c. 1095, can. 1095 §2, or the number alone — and ' +
        'this page will show that canon, where it sits in the Code, every act that ' +
        'touched it, and the text on both sides of each change.',
      // page: law/index.html, the rights paragraph under "The words are often not here, and that is a stated position."
      rights_heading: 'The words are often not here, and that is a stated position.',
      rights: 'The 1917 Code is in the public domain and its text may be shown. The Latin of ' +
        'the 1983 Code is a work of the Holy See later than 1929 and is protected, as ' +
        'are the standard English translations, and this project holds no licence for ' +
        'either. So for many canons this page carries the citation, the place in the ' +
        'structure, the acts that touched it and the dates — and, in place of the ' +
        'words, the reason they are withheld. A canon whose words nobody here has read ' +
        'is a different thing again and is said differently: an unread canon is not a ' +
        'withheld one, and neither is a canon that did not change.',
      acts: C.byDate(stations).map((station) => ({ // PORT: law.js:795-817 renderActs
        id: station.id, title: stationName(station), kind: L.kindOf(station), line: station.line,
        meta: [station.date, station.authority, lineLabel(station.line)].filter(Boolean).join(' · '),
        extent: L.extentWords(station),
      })),
      extent: data.extent || '',
    };
  }

  function act(id) { // PORT: law.js:1124-1192 openStation, 819-846 facts, 908-1040 renderStationChanges
    const { byId } = spine();
    const { byUnit } = index();
    const station = byId.get(id);
    if (!station) return { missing: 'This record carries no act called ' + id + '.' };
    const kind = L.kindOf(station);
    const view = {
      id, title: stationName(station), kind, line: station.line,
      facts: [
        ['Date', station.date + (station.date_precision && station.date_precision !== 'day' ? ' (' + station.date_precision + ')' : '')],
        ['Station', kind], ['Authority', station.authority], ['Instrument', station.instrument], ['Act', station.kind],
        ['Witness', station.printing], ['Body of law', lineLabel(station.line)], ['Descent', station.parent_kind],
        ['Instrument read', station.act_citation ? station.act_citation + ' — ' + (L.CITATION_WORDS[station.act_citation] || '') : null],
        ['Citation', station.citation],
        ['Effect', station.effect ? station.effect + (station.effect_established ? '' : ' (what it changed here is not established)') : null],
      ].filter((row) => row[1]).map((row) => [row[0], String(row[1])]),
      extent: L.extentWords(station) + '.',
    };
    if (kind === C.KIND.PRINTED) view.kind_note = 'A printed station. A witness survives and no act has been located for ' +
      'it, so nothing here claims one. That is a statement about the evidence ' +
      'and not about the size of the change.';
    else if (kind === C.KIND.UNSTATED) view.kind_note = 'This file states which kind the other stations are and states nothing ' +
      'for this one, so it is left unsaid rather than assumed.';
    if ((station.via_unrepresented || []).length) {
      view.gap_note = 'The descent into this station runs through ' + station.via_unrepresented.join(', ') +
        ', which this record does not carry. The edge means “descends from”, not “immediately follows”.';
    }
    if ((station.departures || []).length) view.departures = 'Departures recorded at this act: ' + station.departures.join(', ') + '.';
    if (!station.station_path) {
      view.change_error = 'This map file names no change set for this station, so none is shown. ' +
        'Working one out here would be a second answer to a question the generator already answers.';
      return view;
    }
    let payload;
    try { payload = file(station.station_path); } catch (error) {
      view.change_error = 'What this act reached could not be read: ' + String(error.message || error);
      return view;
    }
    C.learnGroups(payload);
    if (kind !== C.KIND.PROMULGATED) {
      view.printed_caveat = 'No act has been located for this station, so nothing below was ordered ' +
        'by anybody as far as this record knows. What is shown is how this ' +
        'witness differs from the one before it, which is a far weaker thing ' +
        'than a change an authority made.';
    }
    const edges = payload.edges || {};
    view.rests_on = Object.keys(L.EDGE_WORDS).filter((key) => edges[key]).map((key) => [L.EDGE_WORDS[key], String(edges[key])]);
    const containers = C.groupsIn(payload);
    view.divisions_heading = C.words().group_word === 'division' ? 'The divisions' : 'The ' + C.words().group_word + 's';
    view.divisions = containers.map((row) => {
      const after = row.after || {}, before = row.before || {};
      return { title: after.title || before.title || C.groupOf(row),
        meta: [L.whatHappened(row), after.designation || before.designation].filter(Boolean).join(' · '),
        note: after.note || before.note || '', basis: basis(row) };
    });
    const units = payload.units || [];
    const word = C.words().unit_word;
    view.units_heading = units.length ? L.many(units.length, word) + ' touched' : '';
    const identity = (row) => byUnit.get(row.unit) || row.after || row.before || { unit: row.unit };
    const groups = new Map(); // PORT: law.js:897-906 byContainer
    units.forEach((row) => {
      const where = C.groupOf(byUnit.get(row.unit) || row.after || row.before || {}) || '';
      if (!groups.has(where)) groups.set(where, []);
      groups.get(where).push(row);
    });
    view.groups = Array.from(groups.keys()).sort().map((where) => {
      const rows = groups.get(where).slice().sort((a, b) => C.byOrder(byUnit.get(a.unit) || a.after || a.before || a,
        byUnit.get(b.unit) || b.after || b.before || b));
      return {
        heading: (where ? C.groupLabel(where) : 'Placed in no ' + C.words().group_word + ' by this record') + ' — ' + L.many(rows.length, word),
        canons: rows.map((row) => { // PORT: law.js:858-895 touchedCanon
          const card = { unit: row.unit, citation: C.citationOf(identity(row)), what: L.whatHappened(row), state: row.state,
            marker: row.marker || '', basis: basis(row) };
          if (row.state === 'changed') { card.before = side(row.before); card.after = side(row.after); }
          else card.standing = side(row.state === 'gone' ? row.before : row.after);
          return card;
        }),
      };
    });
    const interpretations = payload.interpretations || [];
    if (interpretations.length) {
      view.interpretations_heading = interpretations.length + (interpretations.length === 1 ? ' authentic interpretation' : ' authentic interpretations');
      view.interpretations_note = 'These settle what a canon means and alter no word of what it says, so ' +
        'they are not in the count of canons touched above and no canon’s text moved for them.';
      view.interpretations = interpretations.map((row) => ({ unit: row.unit, citation: C.citationOf(byUnit.get(row.unit) || { unit: row.unit }),
        card: interpretation(row) }));
    }
    const orphaned = payload.unestablished || [];
    if (orphaned.length) {
      view.unestablished_note = 'The act is known to have acted on these and this record does not know ' +
        'what it left. They are removed rather than carried forward, because ' +
        'carrying them forward would assert that nothing changed.';
      view.unestablished = orphaned.map((row) => ({ unit: row.unit, marker: row.marker || '' }));
    }
    if (!containers.length && !units.length && !orphaned.length && !interpretations.length) {
      const standing = (payload.totals || {}).standing;
      view.empty = kind === C.KIND.PROMULGATED
        ? 'This act moved nothing in this record. It keeps its station because ' +
          'an authority acted: a history keyed on diffs would have dropped it, ' +
          'and a history keyed on acts records that the authority spoke and ' +
          'this part of the law did not move.' + (standing ? ' ' + L.many(standing, C.words().unit_word) + ' stand after it.' : '')
        : 'Nothing in this record differs from what stood before.';
    }
    if (station.state_path) view.state_label = 'Read the law as it stood after this act';
    return view;
  }

  function state(id) { // PORT: law.js:1042-1099 renderState
    const { byId } = spine();
    const { byUnit } = index();
    const station = byId.get(id);
    if (!station || !station.state_path) return { error: 'This record names no recorded state after that act.' };
    let payload;
    try { payload = file(station.state_path); } catch (error) {
      return { error: ROOT + station.state_path + ' could not be read: ' + String(error.message || error) };
    }
    C.learnGroups(payload);
    const totals = payload.totals || {};
    const containers = C.groupsIn(payload);
    return {
      title: payload.title,
      summary: L.many(totals.units || 0, C.words().unit_word) + ' across ' +
        L.many(totals[C.words().group_key] || containers.length, C.words().group_word) + ', as this record holds them after ' + payload.title + '.',
      divisions: containers.map((container) => ({
        title: container.title || C.groupOf(container), designation: container.designation || '',
        empty: (container.units || []).length ? '' : 'This record carries no ' + C.words().unit_word + ' standing here at this point.',
        units: (container.units || []).map((one) => ({ citation: C.citationOf(one), unit: one.unit, side: side(one) })),
      })),
      unestablished: (payload.unestablished || []).map((row) => row.marker),
      interpretations: (payload.interpretations || []).map((row) => ({ citation: C.citationOf(byUnit.get(row.unit) || { unit: row.unit }), record: row.record })),
    };
  }

  function structure() { // PORT: law.js:707-742 renderStructure and 676-705 structureNode
    const { data } = spine();
    const { rows } = index();
    const lines = (data.lines || []).map((line) => line.id);
    const splits = rows.some((row) => row.line) ? lines : [''];
    const node = (n) => n.unplaced
      ? { unplaced: 'Placed nowhere by this record: ', canons: n.canons.map((entry) => ({ key: entry.key, citation: C.canonCitation(entry.canon) })) }
      : { kind: n.kind, label: n.label || n.id, count: C.countIn(n) + (C.countIn(n) === 1 ? ' canon' : ' canons'),
        children: n.children.map(node),
        canons: n.canons.map((entry) => ({ key: entry.key, citation: C.canonCitation(entry.canon),
          size: entry.rows.length > 1 ? entry.rows.length + ' §§' : '',
          gone: entry.rows.every((row) => row.standing === false) ? 'no longer stands' : '' })) };
    return {
      view: 'structure',
      bodies: splits.map((line) => {
        const held = line ? rows.filter((row) => row.line === line) : rows;
        if (!held.length && line) return null;
        const roots = C.tree(held);
        return { line, label: line ? lineLabel(line) : '', none: roots.length ? '' : 'This record carries no canon here.', tree: roots.map(node) };
      }).filter(Boolean),
    };
  }

  function bodies() { // PORT: law.js:1194-1247 renderBodies
    const { data, stations, byId } = spine();
    return {
      view: 'bodies',
      lines: (data.lines || []).map((line) => {
        const count = stations.filter((s) => s.line === line.id).length;
        return { heading: line.label || line.id, meta: count + (count === 1 ? ' act' : ' acts') + ' in this record', note: line.note || '' };
      }),
      pairs: (data.commonality || []).map((pair) => {
        const bases = pair.shared_base || [];
        const parted = bases.length ? pair.diverged_at || bases[bases.length - 1] : null;
        return {
          heading: lineLabel(pair.a) + ' and ' + lineLabel(pair.b),
          text: !bases.length
            ? 'No act in this record stands behind both, so they share no station ' +
              'here. That is a finding and not a gap. It also means the two number ' +
              'their canons independently: nothing joins c. 1095 of one to c. 1095 ' +
              'of the other, and this page draws no such join.'
            : 'The last act both descend from is ' + (stationName(byId.get(parted)) || parted) +
              '. Everything standing there is what the two held in common.',
          parted,
        };
      }),
    };
  }

  return { opening, lookup, canon, unit, act, state, structure, bodies };
};
