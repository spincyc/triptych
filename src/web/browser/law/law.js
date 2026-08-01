/* ===========================================================================
 * The Code, canon by canon — lookup, history, extent, structure
 * ===========================================================================
 *
 * THE CANON IS THE ENTRANCE, AND THAT IS WHAT MAKES THIS PAGE DIFFERENT FROM
 * THE MISSAL MAP. A reader of the Missal arrives with a date and asks what
 * changed. A reader of the Code arrives with a CITATION and asks what c. 1095
 * says, what it said before, and which act changed it. So the canon is the
 * primary view and the timeline is the second axis, and the deep link a reader
 * copies out of the address bar is a citation.
 *
 * WHAT A READER PAYS FOR. The spine is the acts and their counts: no canon, no
 * text, no diff. The index of every canon is a second file and is fetched the
 * moment a reader means to look something up, which is honest rather than free
 * — a Code is several thousand canons and the index is what citing one costs.
 * What an act reached arrives when that act is opened; a canon's history
 * arrives, one file per paragraph, when that canon is opened; the Code as it
 * stood arrives only when it is asked for.
 *
 * WHAT THIS FILE DOES NOT DO, AND MUST NOT START DOING:
 *
 *   It does not work out what an act changed. `act-history structure` derives
 *   that from the same state computation `emit` commits, and writes it. Two
 *   answers to "what did Pascite gregem Dei do to c. 1364" inside one artifact
 *   means the wrong one ends up on screen.
 *
 *   It does not decide whether a station is `promulgated` or `printed`. That is
 *   read, through the shared rule. Inferring it from whether an instrument
 *   string happens to be present would turn "nobody has read the decree" into
 *   "no decree is claimed", which are different statements about evidence.
 *
 *   It does not map a canon of one Code onto a canon of another. The 1917 and
 *   1983 numberings do not correspond. Where the record carries a
 *   correspondence it is a scholarly claim and is printed with its source;
 *   where it carries none this page says so, and it never derives one.
 *
 *   It does not model the Code's structure, and it does not name the Code's
 *   parts. Books, Parts, Titles and Chapters are whatever the record places a
 *   canon in, under whatever words the record's vocabulary uses.
 *
 *   It does not treat an authentic interpretation as a change. An
 *   interpretation settles what a canon MEANS without altering a syllable of
 *   what it says; the generator gives it its own kind of stop, and this draws it
 *   as its own kind of stop.
 *
 * RIGHTS ARE PART OF THE RECORD, NOT AN ACCIDENT OF IT. The 1917 Code is in the
 * public domain. The Latin of the 1983 Code is a work of the Holy See later
 * than 1929 and is protected, as are the standard English translations. So for
 * many canons this page carries the identity, the place in the structure, the
 * history and the acts — and not the words. That reads as a stated withholding
 * with its reason. It never reads as an empty box, and never as though the
 * canon were unchanged or unimportant.
 *
 * AND WHERE THE WORDS ARE WITHHELD, THE ESTABLISHING ACT IS THE ANSWER THE PAGE
 * CAN STILL GIVE. The record carries which act established the text now in
 * force, because that is the canon's legal state and not provenance about a
 * reading. It is how a lawyer cites a canon he cannot quote here: c. 1671 as
 * substituted by Mitis Iudex. It is shown in place of the words, not beside a
 * blank.
 * ======================================================================== */

(function () {
  'use strict';

  const T = window.Triptych;
  const C = window.TriptychCode;

  /* One slice is served at a time and which one is a parameter, not a fact
   * about this file. The record is meant to grow — a second code, the Eastern
   * canons, a particular law — and a further slice should be reachable by
   * asking for it rather than by editing a page. */
  const ASKED = new URLSearchParams(window.location.search).get('slice');
  const SLICE = /^[a-z0-9][a-z0-9-]*$/.test(ASKED || '') ? ASKED : 'code-of-canon-law';
  const ROOT = 'structure/act-history/' + SLICE;

  const tally = document.getElementById('tally');
  const form = document.getElementById('lookup');
  const citationInput = document.getElementById('citation-input');
  const lineSelect = document.getElementById('line-select');
  const canonView = document.getElementById('canon');
  const structurePanel = document.getElementById('structure');
  const structureButton = document.getElementById('structure-button');
  const structureView = document.getElementById('structure-view');
  const actsPanel = document.getElementById('acts');
  const actsView = document.getElementById('acts-view');
  const stationView = document.getElementById('station');
  const bodiesPanel = document.getElementById('bodies');
  const bodiesView = document.getElementById('bodies-view');
  const extentPanel = document.getElementById('extent');
  const extentView = document.getElementById('extent-view');

  // One promise per fragment, so a reader who walks back and forth across the
  // Code pays for each canon and each act once.
  const fragments = new Map();

  function fragment(path) {
    if (!fragments.has(path)) fragments.set(path, T.loadJSON(path));
    return fragments.get(path);
  }

  let spine = null;
  let byId = new Map();
  let kindsStated = false;
  let index = [];
  let indexPending = null;
  let byUnit = new Map();
  let opened = null;          // {canon, line, asked} — what the address bar says
  let openedStation = null;

  function lineLabel(id) {
    const line = ((spine && spine.lines) || []).find(function (row) { return row.id === id; });
    return (line && line.label) || id || '';
  }

  function stationName(station) {
    return (station && (station.title || station.id)) || '';
  }

  function kindOf(station) {
    return C.KIND.of(station, kindsStated);
  }

  /* The slice supplies the noun and this supplies the number. A count printed
   * as "1 divisions" reads as a page that does not know what it is counting. */
  function many(count, word) {
    return count + ' ' + word + (count === 1 ? '' : 's');
  }

  /* ------------------------------------------------------------------------
   * Three states, never two, and a fourth thing beside them
   * --------------------------------------------------------------------- */

  function establishedNote(body) {
    if (!body.established) return null;
    const station = byId.get(body.established);
    const node = T.el('p', 'canon-established');
    node.appendChild(document.createTextNode('Text established by '));
    node.appendChild(actLink(body.established));
    if (station && station.date) {
      node.appendChild(document.createTextNode(' (' + station.date + ')'));
    }
    node.appendChild(document.createTextNode(
      '. The words are not here; which act put them there is.'));
    return node;
  }

  function bodyNode(body, unreadWords) {
    const wrap = T.el('div', 'canon-body');
    if (body.state === C.PRESENT) {
      wrap.appendChild(T.el('p', 'canon-text', body.text));
      return wrap;
    }
    if (body.state === C.WITHHELD) {
      const node = T.el('p', 'canon-withheld');
      node.appendChild(T.el('strong', null, 'Text withheld here. '));
      node.appendChild(document.createTextNode(body.reason));
      wrap.appendChild(node);
      const established = establishedNote(body);
      if (established) wrap.appendChild(established);
      return wrap;
    }
    wrap.appendChild(T.el('p', 'canon-unread', unreadWords ||
      'This record carries this canon’s identity and place and has not read its words.'));
    const established = establishedNote(body);
    if (established) wrap.appendChild(established);
    return wrap;
  }

  /** One side of a canon: every edition the record carries, or its one body. */
  function sideNode(side, unreadWords) {
    const wrap = T.el('div', 'canon-side');
    if (!side) {
      wrap.appendChild(T.el('p', 'canon-unread', 'Nothing stood here.'));
      return wrap;
    }
    const editions = C.editionsOf(side);
    if (editions.length) {
      editions.forEach(function (edition) {
        const block = T.el('div', 'canon-edition');
        const head = T.el('p', 'canon-edition-name', edition.label);
        if (edition.language) head.appendChild(T.el('span', 'canon-language', edition.language));
        block.appendChild(head);
        block.appendChild(bodyNode(edition.body, unreadWords));
        wrap.appendChild(block);
      });
      return wrap;
    }
    wrap.appendChild(bodyNode(C.bodyOf(side), unreadWords));
    return wrap;
  }

  /* ------------------------------------------------------------------------
   * Where a canon sits
   * --------------------------------------------------------------------- */

  function breadcrumb(row) {
    const chain = C.chainOf(row);
    const wrap = T.el('p', 'canon-place');
    if (!chain.length) {
      wrap.appendChild(T.el('span', 'canon-place-none',
        'This record does not place this canon in the Code’s structure.'));
      return wrap;
    }
    chain.forEach(function (step, position) {
      if (position) wrap.appendChild(T.el('span', 'canon-place-sep', ' › '));
      const item = T.el('span', 'canon-place-step');
      if (step.kind) item.appendChild(T.el('span', 'canon-place-kind', step.kind));
      item.appendChild(document.createTextNode(step.label));
      wrap.appendChild(item);
    });
    return wrap;
  }

  /* ------------------------------------------------------------------------
   * Shared pieces of a station and of a stop
   * --------------------------------------------------------------------- */

  const CITATION_WORDS = {
    'cited-in-corpus': 'the instrument was read in this project’s own corpus',
    'cited-externally': 'the instrument was read, in a witness held elsewhere',
    'not-found': 'the instrument was searched for and not found',
    'none-claimed': 'no instrument is claimed at all'
  };

  const STATE_WORDS = {
    entered: 'first carried here',
    gone: 'ceases to bind',
    changed: 'altered',
    interpreted: 'interpreted, not altered'
  };

  function whatHappened(stop) {
    if (stop.kinds && stop.kinds.length) return stop.kinds.join(', ');
    return STATE_WORDS[stop.state] || stop.state;
  }

  function citations(stop) {
    const held = (stop.cited || []).filter(function (entry) { return entry.basis || entry.note; });
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

  function actLink(id, words) {
    const button = T.el('button', 'link-button',
      words || stationName(byId.get(id)) || id);
    button.type = 'button';
    button.addEventListener('click', function () {
      openStation(id);
      stationView.scrollIntoView({ block: 'start' });
    });
    return button;
  }

  /** An authentic interpretation, printed whole: the doubt, the answer, the
   *  force it has, and where it is published. A count of them would be useless
   *  to the only reader who wants them. */
  function interpretationNode(row) {
    const card = T.el('article', 'interpretation');
    card.appendChild(T.el('p', 'interpretation-force', C.forceWords(row.force)));
    if (row.dubium) {
      card.appendChild(T.el('h5', 'interpretation-label', 'Dubium'));
      card.appendChild(T.el('p', 'interpretation-text', row.dubium));
    }
    if (row.responsum) {
      card.appendChild(T.el('h5', 'interpretation-label', 'Responsum'));
      card.appendChild(T.el('p', 'interpretation-text', row.responsum));
    }
    if (row.citation) card.appendChild(T.el('p', 'interpretation-cite', row.citation));
    if (row.basis) card.appendChild(T.el('p', 'interpretation-cite', row.basis));
    if (row.note) card.appendChild(T.el('p', 'interpretation-cite', row.note));
    if (row.read_from) {
      card.appendChild(T.el('p', 'interpretation-cite', 'read from: ' + row.read_from));
    }
    return card;
  }

  /* ------------------------------------------------------------------------
   * One paragraph of a canon, through time
   *
   * The record's base unit. A canon with three paragraphs is three of these,
   * and they are gathered under one heading rather than flattened into one
   * body, because §2 is what a citation names and what an act replaces.
   * --------------------------------------------------------------------- */

  function paragraphSection(row, history, marked) {
    const block = T.el('section', 'paragraph' + (marked ? ' paragraph-asked' : ''));
    const head = T.el('h3', 'paragraph-head');
    head.appendChild(document.createTextNode(C.citationOf(row.name ? row : history)));
    if (marked) head.appendChild(T.el('span', 'paragraph-asked-mark', 'the paragraph you cited'));
    block.appendChild(head);

    const stops = (history && history.stations) || [];
    const changes = stops.filter(function (stop) { return !C.isInterpretation(stop); });
    const readings = stops.filter(C.isInterpretation);
    const last = changes.length ? changes[changes.length - 1] : null;
    const standing = history && history.standing !== false;

    const state = T.el('p', 'paragraph-state');
    state.appendChild(document.createTextNode(
      changes.length + (changes.length === 1 ? ' act touches it' : ' acts touch it') +
      (readings.length
        ? ', and ' + readings.length +
          (readings.length === 1 ? ' interpretation settles' : ' interpretations settle') +
          ' what it means'
        : '') + '. It enters at '));
    if (history && history.entered_at) state.appendChild(actLink(history.entered_at));
    state.appendChild(document.createTextNode(standing
      ? '. It still stands at the end of the line this record draws.'
      : '. It ceases at '));
    if (!standing && history.left_at) {
      state.appendChild(actLink(history.left_at));
      state.appendChild(document.createTextNode('.'));
    }
    block.appendChild(state);

    const now = T.el('section', 'panel-block');
    now.appendChild(T.el('h4', 'block-title', standing ? 'As it stands' : 'As it last stood'));
    now.appendChild(sideNode(last && (last.after || last.before),
      'This record carries this canon’s identity and its place in the Code, and ' +
      'has not read its words.'));
    block.appendChild(now);

    const through = T.el('section', 'panel-block');
    through.appendChild(T.el('h4', 'block-title', 'Through time'));
    if (!stops.length) {
      through.appendChild(T.el('p', 'weak', 'No act in this record touches it.'));
    }
    stops.forEach(function (stop) { through.appendChild(stopCard(stop)); });
    block.appendChild(through);
    return block;
  }

  function stopCard(stop) {
    const interpretation = C.isInterpretation(stop);
    const card = T.el('article', 'stop stop-' + (interpretation ? 'interpreted' : stop.state));
    const title = T.el('h5', 'stop-head');
    title.appendChild(T.el('span', 'stop-title', stop.title || stop.act));
    title.appendChild(T.el('span', 'stop-kinds', whatHappened(stop)));
    card.appendChild(title);

    const meta = [stop.date, stop.instrument || 'instrument not carried here'];
    if (stop.station_kind && stop.station_kind !== C.KIND.PROMULGATED) {
      meta.push(stop.station_kind);
    }
    card.appendChild(T.el('p', 'stop-meta', meta.join(' · ')));

    if (interpretation) {
      card.appendChild(T.el('p', 'weak',
        'The canon did not change. An authentic interpretation settles what it ' +
        'means and alters not one word of what it says, so nothing is shown ' +
        'here as a before and an after.'));
      if (stop.interpretation) card.appendChild(interpretationNode(stop.interpretation));
    } else if (stop.state === 'changed') {
      const pair = T.el('div', 'stop-pair');
      const was = T.el('div', 'stop-was');
      was.appendChild(T.el('h6', 'stop-side-title', 'Before'));
      was.appendChild(sideNode(stop.before));
      const now = T.el('div', 'stop-now');
      now.appendChild(T.el('h6', 'stop-side-title', 'After'));
      now.appendChild(sideNode(stop.after));
      pair.appendChild(was);
      pair.appendChild(now);
      card.appendChild(pair);
      if ((stop.fields || []).length) {
        card.appendChild(T.el('p', 'stop-fields',
          'Fields that differ: ' + stop.fields.join(', ') + '.'));
      } else {
        card.appendChild(T.el('p', 'weak',
          'The act records a departure here and the state it leaves is the same ' +
          'in every field this record carries.'));
      }
    } else {
      card.appendChild(sideNode(stop.state === 'gone' ? stop.before : stop.after));
    }

    // A canon an act left unestablished prints its marker rather than falling
    // back to the words it inherited.
    if (stop.marker) card.appendChild(T.el('pre', 'marker', stop.marker));
    const basis = citations(stop);
    if (basis) card.appendChild(basis);
    card.appendChild(actLink(stop.act, 'Everything this act reached'));
    return card;
  }

  /* ------------------------------------------------------------------------
   * The canon a reader asked for — the page's primary view
   * --------------------------------------------------------------------- */

  /** What the record carries about this canon answering to another. */
  function correspondence(rows) {
    const claims = rows.reduce(function (all, row) {
      return all.concat(row.correspondence || []);
    }, []);
    const block = T.el('section', 'panel-block');
    block.appendChild(T.el('h3', 'block-title', 'Against the other body of law'));
    if (!claims.length) {
      block.appendChild(T.el('p', 'weak',
        'This record maps this canon onto no canon of any other Code. The 1917 ' +
        'and 1983 numberings do not correspond — c. 1095 of one is not c. 1095 ' +
        'of the other, and there is no arithmetic that turns one into the other. ' +
        'Where a correspondence exists it is a scholarly claim with an author, ' +
        'and this page prints it only when the record carries one.'));
      return block;
    }
    block.appendChild(T.el('p', 'weak',
      'A correspondence between two Codes is a scholarly claim and never a ' +
      'mapping this page derived. Each one below is shown with the source that ' +
      'makes it.'));
    claims.forEach(function (claim) {
      const card = T.el('article', 'claim');
      const other = byUnit.get(claim.unit);
      card.appendChild(T.el('h4', 'claim-head',
        (other ? C.citationOf(other) : claim.unit) +
        (other && other.line ? ' — ' + lineLabel(other.line) : '')));
      if (claim.note) card.appendChild(T.el('p', 'claim-note', claim.note));
      card.appendChild(T.el('p', 'claim-source',
        claim.source || 'The record names no source for this claim.'));
      if (other) {
        const go = T.el('button', 'link-button', 'Open that canon');
        go.type = 'button';
        go.addEventListener('click', function () { openUnit(claim.unit); });
        card.appendChild(go);
      }
      block.appendChild(card);
    });
    return block;
  }

  /**
   * Open one canon: its heading, its place, and each of its paragraphs whole.
   *
   * One fetch per paragraph, because a paragraph is the record's base unit and
   * its history is its own file. A three-paragraph canon costs three small
   * files and nothing else in the Code.
   */
  function openCanon(entry) {
    opened = { canon: entry.canon, line: entry.line, asked: entry.asked || null };
    T.clear(canonView);
    canonView.setAttribute('aria-busy', 'true');
    canonView.appendChild(T.el('p', 'placeholder',
      'Loading ' + C.canonCitation(entry.canon) + '…'));

    const first = entry.rows[0];
    Promise.all(entry.rows.map(function (row) {
      const path = row.path || (SLICE + '/unit/' + row.unit + '.json');
      return fragment('structure/act-history/' + path)
        .then(function (history) { return { row: row, history: history }; })
        .catch(function (error) { return { row: row, error: error }; });
    })).then(function (loaded) {
      T.clear(canonView);
      canonView.setAttribute('aria-busy', 'false');

      const head = T.el('header', 'canon-head');
      head.appendChild(T.el('h2', 'canon-citation', C.canonCitation(entry.canon)));
      const where = entry.line || (loaded[0].history && loaded[0].history.line);
      if (where) head.appendChild(T.el('p', 'canon-line', lineLabel(where)));
      head.appendChild(breadcrumb(first));
      head.appendChild(T.el('p', 'canon-count',
        entry.rows.length === 1
          ? 'One base unit in this record.'
          : entry.rows.length + ' paragraphs, each a base unit of this record ' +
            'with its own history.'));
      canonView.appendChild(head);

      canonView.appendChild(correspondence(entry.rows));

      loaded.forEach(function (held) {
        if (held.error) {
          const failed = T.el('section', 'paragraph');
          failed.appendChild(T.el('h3', 'paragraph-head', C.citationOf(held.row)));
          failed.appendChild(T.el('p', 'error',
            'Its history could not be read: ' + String(held.error.message || held.error)));
          canonView.appendChild(failed);
          return;
        }
        const marked = Boolean(entry.asked) &&
          C.paragraphOf(held.row) === String(entry.asked);
        canonView.appendChild(paragraphSection(held.row, held.history, marked));
      });

      T.statusLine(C.canonCitation(entry.canon) + ': ' + entry.rows.length +
        (entry.rows.length === 1 ? ' base unit.' : ' paragraphs.'));
      writeState();
    });
  }

  /** Open one base unit by its id — the exact-row form of a deep link. */
  function openUnit(unit) {
    const row = byUnit.get(unit);
    if (row) {
      const entry = C.canons([row])[0];
      // Reached by id, so the whole canon is assembled around it rather than
      // the one row being shown alone: a paragraph read out of its canon is
      // how a citation goes wrong.
      const whole = C.canons(index).filter(function (candidate) {
        return candidate.key === entry.key;
      })[0];
      openCanon(Object.assign({}, whole || entry, {
        asked: C.paragraphOf(row) || null
      }));
      return;
    }
    // The index has not been fetched. Fetch it, then resolve properly; the
    // alternative is composing a path and showing a paragraph with no canon
    // around it.
    loadIndex().then(function () {
      if (byUnit.has(unit)) openUnit(unit);
      else {
        T.clear(canonView);
        canonView.setAttribute('aria-busy', 'false');
        canonView.appendChild(T.el('p', 'weak',
          'This record carries no unit called ' + unit + '.'));
      }
    }).catch(reportIndexFailure);
  }

  /* ------------------------------------------------------------------------
   * Looking a canon up
   * --------------------------------------------------------------------- */

  function loadIndex() {
    if (indexPending) return indexPending;
    indexPending = fragment(ROOT + '/units.json').then(function (payload) {
      index = payload.units || [];
      byUnit = new Map(index.map(function (row) { return [row.unit, row]; }));
      // A record that names its containers in the index names them here too;
      // one that does not leaves the ids standing, which is what it has.
      C.learnGroups(payload);
      return index;
    });
    return indexPending;
  }

  function reportIndexFailure(error) {
    T.clear(canonView);
    canonView.setAttribute('aria-busy', 'false');
    canonView.appendChild(T.el('p', 'error',
      'The index of canons could not be read: ' + String(error.message || error)));
  }

  function askedLine() {
    return lineSelect && lineSelect.value ? lineSelect.value : '';
  }

  function inLine(entry, line) {
    if (!line) return true;
    if (entry.line) return entry.line === line;
    // The index does not say which body of law this canon stands in, so the
    // filter cannot honestly exclude it. Everything is shown rather than a
    // canon being hidden by a narrowing the record cannot support.
    return true;
  }

  function lookUp(text) {
    const typed = String(text || '').trim();
    if (!typed) return;
    canonView.setAttribute('aria-busy', 'true');
    T.clear(canonView);
    canonView.appendChild(T.el('p', 'placeholder', 'Looking up ' + typed + '…'));
    loadIndex().then(function (rows) {
      const cited = C.parseCitation(typed);
      let found = cited ? C.find(rows, cited) : [];
      if (!found.length) {
        found = C.canons(rows.filter(function (row) { return C.matches(row, typed); }));
      }
      const line = askedLine();
      const narrowed = found.filter(function (entry) { return inLine(entry, line); });
      const chosen = narrowed.length ? narrowed : found;
      if (chosen.length === 1) {
        openCanon(chosen[0]);
        return;
      }
      renderChoices(typed, cited, chosen);
    }).catch(reportIndexFailure);
  }

  function renderChoices(typed, cited, entries) {
    T.clear(canonView);
    canonView.setAttribute('aria-busy', 'false');
    if (!entries.length) {
      const none = T.el('div', 'lookup-none');
      none.appendChild(T.el('h2', 'canon-citation', typed));
      none.appendChild(T.el('p', 'weak', cited
        ? 'This record carries no canon numbered ' + cited.canon + '. That is a ' +
          'statement about this record and not about the Code: nothing here ' +
          'offers you a neighbouring canon instead, because a neighbouring ' +
          'canon is the wrong law.'
        : 'Nothing in this record answers to that. The lookup takes a citation ' +
          '— c. 1095, can. 1095 §2, or the number alone — or any word carried in ' +
          'a canon’s identity or in the division it stands in.'));
      canonView.appendChild(none);
      T.statusLine('Nothing found for ' + typed + '.');
      return;
    }
    const list = T.el('div', 'lookup-choices');
    list.appendChild(T.el('h2', 'canon-citation', typed));
    list.appendChild(T.el('p', 'weak',
      'More than one canon answers to that. Each body of law numbers ' +
      'independently, so one number stands in more than one of them, and they ' +
      'are not the same canon.'));
    entries.forEach(function (entry) {
      const item = T.el('article', 'choice');
      const open = T.el('button', 'link-button', C.canonCitation(entry.canon));
      open.type = 'button';
      open.addEventListener('click', function () { openCanon(entry); });
      item.appendChild(open);
      if (entry.line) item.appendChild(T.el('span', 'choice-line', lineLabel(entry.line)));
      if (entry.group) {
        item.appendChild(T.el('span', 'choice-place', C.groupLabel(entry.group)));
      }
      item.appendChild(T.el('span', 'choice-place',
        entry.rows.length === 1 ? '1 base unit' : entry.rows.length + ' paragraphs'));
      list.appendChild(item);
    });
    canonView.appendChild(list);
    T.statusLine(entries.length + ' canons answer to ' + typed + '.');
  }

  /* ------------------------------------------------------------------------
   * The structure of the Code, as navigation
   * --------------------------------------------------------------------- */

  function structureNode(node) {
    const block = T.el('details', 'division');
    const summary = T.el('summary', 'division-summary');
    if (node.kind) summary.appendChild(T.el('span', 'division-kind', node.kind));
    summary.appendChild(document.createTextNode(node.label || node.id));
    const count = C.countIn(node);
    summary.appendChild(T.el('span', 'division-count',
      count + (count === 1 ? ' canon' : ' canons')));
    block.appendChild(summary);
    node.children.forEach(function (child) { block.appendChild(structureNode(child)); });
    if (node.canons.length) {
      const list = T.el('ul', 'division-canons');
      node.canons.forEach(function (entry) {
        const item = T.el('li', null);
        const open = T.el('button', 'link-button', C.canonCitation(entry.canon));
        open.type = 'button';
        open.addEventListener('click', function () { openCanon(entry); });
        item.appendChild(open);
        if (entry.rows.length > 1) {
          item.appendChild(T.el('span', 'choice-place', entry.rows.length + ' §§'));
        }
        if (entry.rows.every(function (row) { return row.standing === false; })) {
          item.appendChild(T.el('span', 'choice-gone', 'no longer stands'));
        }
        list.appendChild(item);
      });
      block.appendChild(list);
    }
    return block;
  }

  function renderStructure() {
    T.clear(structureView);
    const lines = (spine.lines || []).map(function (line) { return line.id; });
    // Split by body of law only where the index says which body each canon
    // stands in. A split made on a field the record does not carry would file
    // every canon under the first line and read as a claim.
    const splits = index.some(function (row) { return row.line; }) ? lines : [''];
    splits.forEach(function (line) {
      const rows = line
        ? index.filter(function (row) { return row.line === line; })
        : index;
      if (!rows.length && line) return;
      const block = T.el('section', 'structure-line');
      if (line) block.appendChild(T.el('h3', 'block-title', lineLabel(line)));
      const roots = C.tree(rows);
      if (!roots.length) {
        block.appendChild(T.el('p', 'weak', 'This record carries no canon here.'));
      }
      roots.forEach(function (node) {
        if (node.unplaced) {
          const loose = T.el('p', 'weak');
          loose.appendChild(document.createTextNode('Placed nowhere by this record: '));
          node.canons.forEach(function (entry) {
            const open = T.el('button', 'link-button', C.canonCitation(entry.canon));
            open.type = 'button';
            open.addEventListener('click', function () { openCanon(entry); });
            loose.appendChild(open);
          });
          block.appendChild(loose);
          return;
        }
        block.appendChild(structureNode(node));
      });
      structureView.appendChild(block);
    });
  }

  function wakeStructure() {
    structureButton.disabled = true;
    structureButton.textContent = 'Loading the structure…';
    loadIndex().then(function () {
      structureButton.hidden = true;
      renderStructure();
    }).catch(function (error) {
      structureButton.disabled = false;
      structureButton.textContent = 'Load the structure of the Code';
      T.clear(structureView);
      structureView.appendChild(T.el('p', 'error',
        'The index of canons could not be read: ' + String(error.message || error)));
    });
  }

  /* ------------------------------------------------------------------------
   * The second axis: the acts, and the extent of each
   * --------------------------------------------------------------------- */

  /* What the counts mean depends on what kind of station it is. At a
   * promulgated station an authority changed the law. At a printed one nobody
   * has located an act, so a count is a difference between what two witnesses
   * hold and no more than that. One word over both would launder the weaker
   * claim into the stronger. */
  function extentWords(station) {
    const changed = station.changed;
    if (!changed) return 'what it reached is not carried in this file';
    if (kindOf(station) !== C.KIND.PROMULGATED) {
      const moved = C.magnitude(station);
      if (!moved) return 'nothing in this record differs from what stood before';
      return moved + (moved === 1 ? ' difference' : ' differences') +
        ' from what stood before, with no act behind them';
    }
    const unit = C.words().unit_word;
    const group = C.words().group_word;
    const parts = [];
    if (changed.units_entered) {
      parts.push(many(changed.units_entered, unit) + ' first carried');
    }
    if (changed.units_changed) parts.push(many(changed.units_changed, unit) + ' altered');
    if (changed.units_gone) parts.push(many(changed.units_gone, unit) + ' gone');
    const containers = C.containersTouched(changed);
    if (containers) parts.push(many(containers, group) + ' touched');
    if (changed.interpretations) {
      parts.push(changed.interpretations + ' interpreted');
    }
    if (changed.unestablished) parts.push(changed.unestablished + ' left unestablished');
    if (!parts.length) return 'nothing in this record changed here';
    return parts.join(' · ');
  }

  function renderActs() {
    T.clear(actsView);
    const stations = C.byDate(spine.stations || []);
    if (!stations.length) {
      actsView.appendChild(T.el('p', 'weak', 'This slice records no acts.'));
      return;
    }
    const list = T.el('ol', 'acts-list');
    stations.forEach(function (station) {
      const item = T.el('li', 'act act-' + kindOf(station));
      item.setAttribute('data-station', station.id);
      const open = T.el('button', 'act-open', stationName(station));
      open.type = 'button';
      open.addEventListener('click', function () { openStation(station.id); });
      item.appendChild(open);
      item.appendChild(T.el('p', 'act-meta', [
        station.date, station.authority, lineLabel(station.line)
      ].filter(Boolean).join(' · ')));
      item.appendChild(T.el('p', 'act-extent', extentWords(station)));
      list.appendChild(item);
    });
    actsView.appendChild(list);
  }

  function facts(station) {
    const rows = [
      ['Date', station.date + (station.date_precision && station.date_precision !== 'day'
        ? ' (' + station.date_precision + ')' : '')],
      ['Station', kindOf(station)],
      ['Authority', station.authority],
      ['Instrument', station.instrument],
      ['Act', station.kind],
      ['Witness', station.printing],
      ['Body of law', lineLabel(station.line)],
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

  const EDGE_WORDS = {
    root_basis: 'Why the record starts here',
    parent_basis: 'Why it descends from what it descends from',
    reception_basis: 'The reception this merge asserts',
    via_unrepresented_basis: 'What sits in the gap',
    printing_basis: 'What is known of this witness',
    act_citation_note: 'On the instrument'
  };

  /** One canon in an act's change set, folded shut until it is opened. */
  function touchedCanon(row) {
    const identity = byUnit.get(row.unit) || row.after || row.before || { unit: row.unit };
    const block = T.el('details', 'touched');
    const summary = T.el('summary', 'touched-summary');
    summary.appendChild(T.el('span', 'touched-citation', C.citationOf(identity)));
    summary.appendChild(T.el('span', 'touched-kinds', whatHappened(row)));
    block.appendChild(summary);

    if (row.state === 'changed') {
      const pair = T.el('div', 'stop-pair');
      const was = T.el('div', 'stop-was');
      was.appendChild(T.el('h6', 'stop-side-title', 'Before'));
      was.appendChild(sideNode(row.before));
      const now = T.el('div', 'stop-now');
      now.appendChild(T.el('h6', 'stop-side-title', 'After'));
      now.appendChild(sideNode(row.after));
      pair.appendChild(was);
      pair.appendChild(now);
      block.appendChild(pair);
    } else {
      block.appendChild(sideNode(row.state === 'gone' ? row.before : row.after));
    }
    if (row.marker) block.appendChild(T.el('pre', 'marker', row.marker));
    const basis = citations(row);
    if (basis) block.appendChild(basis);

    const go = T.el('button', 'link-button', 'Follow this canon');
    go.type = 'button';
    go.addEventListener('click', function () { openUnit(row.unit); });
    block.appendChild(go);
    return block;
  }

  /** The canons an act touched, gathered under the divisions they stand in.
   *
   * An act that rewrote a whole Book touches hundreds of canons, and a flat
   * list of them is neither readable nor citeable. The grouping is by the
   * container each row itself states: reading the record, not deriving a
   * structure. A row that states none is gathered under none and says so. */
  function byContainer(rows) {
    const groups = new Map();
    rows.forEach(function (row) {
      const identity = byUnit.get(row.unit) || row.after || row.before || {};
      const where = C.groupOf(identity) || '';
      if (!groups.has(where)) groups.set(where, []);
      groups.get(where).push(row);
    });
    return groups;
  }

  function renderStationChanges(host, payload, station) {
    T.clear(host);
    C.learnGroups(payload);
    host.appendChild(T.el('p', 'detail-summary', extentWords(station) + '.'));

    if (kindOf(station) !== C.KIND.PROMULGATED) {
      host.appendChild(T.el('p', 'weak',
        'No act has been located for this station, so nothing below was ordered ' +
        'by anybody as far as this record knows. What is shown is how this ' +
        'witness differs from the one before it, which is a far weaker thing ' +
        'than a change an authority made.'));
    }

    const edges = payload.edges || {};
    const named = Object.keys(EDGE_WORDS).filter(function (key) { return edges[key]; });
    if (named.length) {
      const block = T.el('section', 'panel-block');
      block.appendChild(T.el('h3', 'block-title', 'On what this station rests'));
      named.forEach(function (key) {
        block.appendChild(T.el('h4', 'edge-title', EDGE_WORDS[key]));
        block.appendChild(T.el('p', 'edge-basis', edges[key]));
      });
      host.appendChild(block);
    }

    const containers = C.groupsIn(payload);
    if (containers.length) {
      const block = T.el('section', 'panel-block');
      block.appendChild(T.el('h3', 'block-title',
        C.words().group_word === 'division' ? 'The divisions'
          : 'The ' + C.words().group_word + 's'));
      containers.forEach(function (row) {
        const after = row.after || {};
        const before = row.before || {};
        const card = T.el('article', 'touched-division');
        card.appendChild(T.el('h4', 'block-subtitle',
          after.title || before.title || C.groupOf(row)));
        const meta = [whatHappened(row), after.designation || before.designation]
          .filter(Boolean).join(' · ');
        card.appendChild(T.el('p', 'stop-meta', meta));
        if (after.note || before.note) {
          card.appendChild(T.el('p', 'body-note', after.note || before.note));
        }
        const basis = citations(row);
        if (basis) card.appendChild(basis);
        block.appendChild(card);
      });
      host.appendChild(block);
    }

    const units = payload.units || [];
    if (units.length) {
      const word = C.words().unit_word;
      const block = T.el('section', 'panel-block');
      block.appendChild(T.el('h3', 'block-title',
        many(units.length, word) + ' touched'));
      const groups = byContainer(units);
      Array.from(groups.keys()).sort().forEach(function (where) {
        const rows = groups.get(where).slice().sort(function (a, b) {
          return C.byOrder(byUnit.get(a.unit) || a.after || a.before || a,
            byUnit.get(b.unit) || b.after || b.before || b);
        });
        const group = T.el('section', 'touched-group');
        group.appendChild(T.el('h4', 'block-subtitle',
          (where ? C.groupLabel(where) : 'Placed in no ' + C.words().group_word +
            ' by this record') + ' — ' + many(rows.length, word)));
        rows.forEach(function (row) { group.appendChild(touchedCanon(row)); });
        block.appendChild(group);
      });
      host.appendChild(block);
    }

    const interpretations = payload.interpretations || [];
    if (interpretations.length) {
      const block = T.el('section', 'panel-block');
      block.appendChild(T.el('h3', 'block-title',
        interpretations.length +
        (interpretations.length === 1 ? ' authentic interpretation' :
          ' authentic interpretations')));
      block.appendChild(T.el('p', 'weak',
        'These settle what a canon means and alter no word of what it says, so ' +
        'they are not in the count of canons touched above and no canon’s text ' +
        'moved for them.'));
      interpretations.forEach(function (row) {
        const card = T.el('article', 'touched-division');
        const identity = byUnit.get(row.unit) || { unit: row.unit };
        const head = T.el('h4', 'block-subtitle');
        head.appendChild(document.createTextNode(C.citationOf(identity)));
        card.appendChild(head);
        card.appendChild(interpretationNode(row));
        const go = T.el('button', 'link-button', 'Follow this canon');
        go.type = 'button';
        go.addEventListener('click', function () { openUnit(row.unit); });
        card.appendChild(go);
        block.appendChild(card);
      });
      host.appendChild(block);
    }

    const orphaned = payload.unestablished || [];
    if (orphaned.length) {
      const block = T.el('section', 'panel-block');
      block.appendChild(T.el('h3', 'block-title', 'Left unestablished'));
      block.appendChild(T.el('p', 'weak',
        'The act is known to have acted on these and this record does not know ' +
        'what it left. They are removed rather than carried forward, because ' +
        'carrying them forward would assert that nothing changed.'));
      orphaned.forEach(function (row) {
        const card = T.el('article', 'touched');
        card.appendChild(T.el('h4', 'block-subtitle', row.unit));
        if (row.marker) card.appendChild(T.el('pre', 'marker', row.marker));
        const go = T.el('button', 'link-button', 'Follow this canon');
        go.type = 'button';
        go.addEventListener('click', function () { openUnit(row.unit); });
        card.appendChild(go);
        block.appendChild(card);
      });
      host.appendChild(block);
    }

    if (!containers.length && !units.length && !orphaned.length && !interpretations.length) {
      const standing = (payload.totals || {}).standing;
      host.appendChild(T.el('p', 'weak',
        kindOf(station) === C.KIND.PROMULGATED
          ? 'This act moved nothing in this record. It keeps its station because ' +
            'an authority acted: a history keyed on diffs would have dropped it, ' +
            'and a history keyed on acts records that the authority spoke and ' +
            'this part of the law did not move.' +
            (standing ? ' ' + many(standing, C.words().unit_word) +
              ' stand after it.' : '')
          : 'Nothing in this record differs from what stood before.'));
    }
  }

  function renderState(host, payload) {
    T.clear(host);
    C.learnGroups(payload);
    const totals = payload.totals || {};
    const containers = C.groupsIn(payload);
    const groupKey = C.words().group_key;
    host.appendChild(T.el('p', 'detail-summary',
      many(totals.units || 0, C.words().unit_word) + ' across ' +
      many(totals[groupKey] || containers.length, C.words().group_word) +
      ', as this record holds them after ' + payload.title + '.'));
    containers.forEach(function (container) {
      const block = T.el('section', 'held-division');
      block.appendChild(T.el('h4', 'block-subtitle',
        container.title || C.groupOf(container)));
      if (container.designation) {
        block.appendChild(T.el('p', 'stop-meta', container.designation));
      }
      const units = container.units || [];
      if (!units.length) {
        block.appendChild(T.el('p', 'weak',
          'This record carries no ' + C.words().unit_word +
          ' standing here at this point.'));
      }
      units.forEach(function (unit) {
        const row = T.el('article', 'held');
        row.appendChild(T.el('h5', 'held-name', C.citationOf(unit)));
        row.appendChild(sideNode(unit));
        const go = T.el('button', 'link-button', 'Follow this canon');
        go.type = 'button';
        go.addEventListener('click', function () { openUnit(unit.unit); });
        row.appendChild(go);
        block.appendChild(row);
      });
      host.appendChild(block);
    });
    if ((payload.unestablished || []).length) {
      const block = T.el('section', 'panel-block');
      block.appendChild(T.el('h3', 'block-title', 'Not established at this point'));
      payload.unestablished.forEach(function (row) {
        block.appendChild(T.el('pre', 'marker', row.marker));
      });
      host.appendChild(block);
    }
    if ((payload.interpretations || []).length) {
      const block = T.el('section', 'panel-block');
      block.appendChild(T.el('h3', 'block-title',
        'Interpretations standing at this point'));
      payload.interpretations.forEach(function (row) {
        const card = T.el('article', 'touched-division');
        card.appendChild(T.el('h4', 'block-subtitle',
          C.citationOf(byUnit.get(row.unit) || { unit: row.unit })));
        card.appendChild(T.el('pre', 'marker', row.record));
        block.appendChild(card);
      });
      host.appendChild(block);
    }
  }

  /** A fold that fetches its own fragment the first time it is opened. */
  function lazyBlock(summaryText, path, render) {
    const block = T.el('details', 'fold');
    block.appendChild(T.el('summary', 'fold-summary', summaryText));
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

  function openStation(id) {
    const station = byId.get(id);
    if (!station) return;
    openedStation = id;
    Array.prototype.forEach.call(document.querySelectorAll('.act'), function (node) {
      node.classList.toggle('act-selected', node.getAttribute('data-station') === id);
    });

    T.clear(stationView);
    stationView.hidden = false;
    stationView.appendChild(T.el('h3', 'detail-title', stationName(station)));
    stationView.appendChild(facts(station));

    if (kindOf(station) === C.KIND.PRINTED) {
      stationView.appendChild(T.el('p', 'weak',
        'A printed station. A witness survives and no act has been located for ' +
        'it, so nothing here claims one. That is a statement about the evidence ' +
        'and not about the size of the change.'));
    } else if (kindOf(station) === C.KIND.UNSTATED) {
      stationView.appendChild(T.el('p', 'weak',
        'This file states which kind the other stations are and states nothing ' +
        'for this one, so it is left unsaid rather than assumed.'));
    }

    if ((station.via_unrepresented || []).length) {
      stationView.appendChild(T.el('p', 'weak',
        'The descent into this station runs through ' +
        station.via_unrepresented.join(', ') + ', which this record does not ' +
        'carry. The edge means “descends from”, not “immediately follows”.'));
    }
    if ((station.departures || []).length) {
      stationView.appendChild(T.el('p', 'stop-fields',
        'Departures recorded at this act: ' + station.departures.join(', ') + '.'));
    }

    const changes = T.el('div', 'detail-changes');
    changes.appendChild(T.el('p', 'placeholder', 'Loading what this act reached…'));
    stationView.appendChild(changes);
    if (station.station_path) {
      // The generator names the fragment; the page never composes its path.
      fragment('structure/act-history/' + station.station_path).then(function (payload) {
        renderStationChanges(changes, payload, station);
      }).catch(function (error) {
        T.clear(changes);
        changes.appendChild(T.el('p', 'error',
          'What this act reached could not be read: ' + String(error.message || error)));
      });
    } else {
      T.clear(changes);
      changes.appendChild(T.el('p', 'weak',
        'This map file names no change set for this station, so none is shown. ' +
        'Working one out here would be a second answer to a question the ' +
        'generator already answers.'));
    }

    if (station.state_path) {
      stationView.appendChild(lazyBlock(
        'Read the law as it stood after this act',
        'structure/act-history/' + station.state_path,
        renderState));
    }

    T.statusLine(stationName(station) + ': ' + extentWords(station));
    writeState();
  }

  /* ------------------------------------------------------------------------
   * Two bodies of law, and what stands between them
   * --------------------------------------------------------------------- */

  function renderBodies() {
    T.clear(bodiesView);
    const lines = spine.lines || [];
    const stations = spine.stations || [];
    lines.forEach(function (line) {
      const card = T.el('article', 'body-of-law');
      card.appendChild(T.el('h3', 'block-title', line.label || line.id));
      const held = stations.filter(function (station) { return station.line === line.id; });
      card.appendChild(T.el('p', 'stop-meta',
        held.length + (held.length === 1 ? ' act' : ' acts') + ' in this record'));
      if (line.note) card.appendChild(T.el('p', 'body-note', line.note));
      bodiesView.appendChild(card);
    });

    (spine.commonality || []).forEach(function (pair) {
      const card = T.el('article', 'body-of-law');
      card.appendChild(T.el('h3', 'block-title',
        lineLabel(pair.a) + ' and ' + lineLabel(pair.b)));
      const bases = pair.shared_base || [];
      if (!bases.length) {
        card.appendChild(T.el('p', 'weak',
          'No act in this record stands behind both, so they share no station ' +
          'here. That is a finding and not a gap. It also means the two number ' +
          'their canons independently: nothing joins c. 1095 of one to c. 1095 ' +
          'of the other, and this page draws no such join.'));
      } else {
        const parted = pair.diverged_at || bases[bases.length - 1];
        const note = T.el('p', 'body-note');
        note.appendChild(document.createTextNode('The last act both descend from is '));
        note.appendChild(actLink(parted));
        note.appendChild(document.createTextNode(
          '. Everything standing there is what the two held in common.'));
        card.appendChild(note);
        const at = byId.get(parted);
        if (at && at.state_path) {
          card.appendChild(lazyBlock(
            'Read what both held in common',
            'structure/act-history/' + at.state_path,
            renderState));
        }
      }
      bodiesView.appendChild(card);
    });
  }

  /* ------------------------------------------------------------------------
   * Deep links
   *
   * A citation is how this material is referenced, so a citation is what the
   * address bar carries: `#canon=1095`, with `&par=2` where a paragraph was
   * cited and `&line=` where more than one body of law carries that number.
   * `#unit=` is the exact base unit and is accepted too, because an id is what
   * one page hands another.
   * --------------------------------------------------------------------- */

  function writeState() {
    T.writeHash([
      ['canon', opened ? opened.canon : ''],
      ['par', opened ? opened.asked : ''],
      ['line', opened ? opened.line : ''],
      ['act', openedStation]
    ]);
  }

  function fromHash(params) {
    const state = params || T.readHash();
    return {
      canon: state.get('canon'),
      paragraph: state.get('par'),
      unit: state.get('unit'),
      act: state.get('act'),
      line: state.get('line')
    };
  }

  function applyHash(wanted) {
    if (wanted.line && lineSelect) lineSelect.value = wanted.line;
    if (wanted.unit) {
      openUnit(wanted.unit);
    } else if (wanted.canon) {
      citationInput.value = wanted.canon +
        (wanted.paragraph ? ' §' + wanted.paragraph : '');
      lookUp(citationInput.value);
    }
    if (wanted.act && wanted.act !== openedStation && byId.has(wanted.act)) {
      openStation(wanted.act);
    }
  }

  /* ------------------------------------------------------------------------
   * Boot
   * --------------------------------------------------------------------- */

  function invite() {
    T.clear(canonView);
    canonView.setAttribute('aria-busy', 'false');
    const block = T.el('div', 'lookup-invite');
    block.appendChild(T.el('p', 'lookup-invite-lede',
      'Type a citation above — c. 1095, can. 1095 §2, or the number alone — and ' +
      'this page will show that canon, where it sits in the Code, every act that ' +
      'touched it, and the text on both sides of each change.'));
    block.appendChild(T.el('p', 'weak',
      'Nothing has been fetched for a canon yet. The index of every canon is a ' +
      'file of its own and arrives the first time you look one up; the acts ' +
      'below arrived with the page, and each one’s change set arrives when you ' +
      'open it.'));
    canonView.appendChild(block);
  }

  function start(data) {
    T.doneBootstrapping();
    spine = data;
    const shape = C.readVocabulary(data);
    const stations = data.stations || [];
    byId = new Map(stations.map(function (station) { return [station.id, station]; }));
    kindsStated = C.KIND.stated(stations);

    const lines = data.lines || [];
    tally.textContent = stations.length +
      (stations.length === 1 ? ' act' : ' acts') + ' across ' +
      lines.length + (lines.length === 1 ? ' body of law' : ' bodies of law') +
      (lines.length ? ' — ' + lines.map(function (line) {
        return line.label || line.id;
      }).join('; ') : '');

    T.fillSelect(lineSelect, [{ value: '', label: 'Any' }].concat(
      lines.map(function (line) {
        return { value: line.id, label: line.label || line.id };
      })));
    lineSelect.disabled = false;
    citationInput.disabled = false;

    renderActs();
    actsPanel.hidden = false;
    renderBodies();
    bodiesPanel.hidden = false;
    structurePanel.hidden = false;
    if (data.extent) {
      extentView.textContent = data.extent;
      extentPanel.hidden = false;
    }

    // A slice that is a history of something other than a body of law will
    // still draw — the shape is the same — but it says so rather than calling a
    // Mass a canon.
    if (shape.vocabulary !== 'law') {
      T.showBanner(
        'This record is not a body of law: its base units are ' +
        shape.unit_word + 's standing in ' + shape.group_word + 's, and it says ' +
        'so itself. It is drawn here because the shape is the same, and nothing ' +
        'on this page calls them canons.');
    }

    const wanted = fromHash();
    if (wanted.unit || wanted.canon) applyHash(wanted);
    else invite();
    if (wanted.act && byId.has(wanted.act)) openStation(wanted.act);

    T.onHashChange(function (params) { applyHash(fromHash(params)); });
  }

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    lookUp(citationInput.value);
  });
  structureButton.addEventListener('click', wakeStructure);
  // The index is what a lookup costs, and it is fetched as soon as a reader
  // shows they mean to look something up rather than after they have typed a
  // whole citation and pressed a button.
  ['mousedown', 'focus', 'keydown'].forEach(function (event) {
    citationInput.addEventListener(event, function () {
      loadIndex().catch(function () { /* reported when a lookup is actually run */ });
    });
  });
  lineSelect.addEventListener('change', function () {
    if (citationInput.value.trim()) lookUp(citationInput.value);
  });

  T.loadJSON(ROOT + '.json').then(start).catch(function (error) {
    T.doneBootstrapping();
    T.clear(canonView);
    canonView.setAttribute('aria-busy', 'false');
    const block = T.el('div', 'lookup-none');
    block.appendChild(T.el('p', 'error',
      'The record for “' + SLICE + '” could not be read: ' +
      String(error.message || error)));
    block.appendChild(T.el('p', 'weak',
      'This page draws whatever act-keyed slice it is pointed at, and it was ' +
      'pointed at ' + ROOT + '.json. A slice written under another name is ' +
      'reached by asking for it — add ?slice=<name> to this page’s address — ' +
      'and no canon law is invented here to stand in for a record that is not ' +
      'present.'));
    canonView.appendChild(block);
    T.statusLine('The record for ' + SLICE + ' could not be read.');
  });
}());
