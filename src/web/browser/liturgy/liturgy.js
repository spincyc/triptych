/* ===========================================================================
 * The propers page — Missal, then Type, then Mass, then Translation
 * ===========================================================================
 *
 * THE SELECTION ORDER IS THE DESIGN. The missal comes first and everything
 * else hangs off it: choosing a missal loads that missal's structure file and
 * repopulates the type list from the kinds it actually contains, and choosing a
 * type repopulates the Mass list. There is no calendar-shaped assumption
 * anywhere below — the missals are whatever structure files the data root
 * offers under structure/propers/, and a third one needs no change here beyond
 * being discovered.
 *
 * This page does one thing. It does not offer the reading plan, share a
 * dropdown with it, or link the reader into it mid-task; the reading plan is
 * its own page at ../scripture/. What the two pages share is the machinery in
 * ../shared/browser-core.js, which is where the chapter cache, the four failure
 * renderings, the numbering-aware loci, the URL state and the render token all
 * live. Nothing in this file may re-implement any of them.
 *
 *   ?data=<root>       where the corpus lives (default ../browse; ?data=fixture
 *                      serves the sample corpus in ../fixture)
 *   ?missals=<a,b>     the missals to offer, overriding discovery
 *   #missal=<id>&type=<kind>&mass=<key>&bible=<id>
 *                      the current selection; shareable, and survives reload
 * ======================================================================== */

'use strict';

(function () {
  const T = window.Triptych;

  /* ------------------------------------------------------------------------
   * Which missals exist
   *
   * There is no generated list of missals in the data root today, so discovery
   * runs in three steps, most authoritative first:
   *
   *   1. ?missals=roman-1962,postconciliar — an explicit override
   *   2. structure/propers/index.json — a manifest, if one is ever generated
   *      (see the report accompanying this page: `mass-propers structure`
   *      writing one would retire step 3 entirely)
   *   3. the candidates below, probed with HEAD so that discovering a missal
   *      never downloads one
   *
   * Step 3 is a list of ids, not a hardcoded calendar: the page never assumes
   * which of them it will find, offers every one it does find, and reads its
   * name out of the file rather than out of this list.
   * --------------------------------------------------------------------- */

  const MISSAL_CANDIDATES = ['roman-1962', 'postconciliar'];
  const MISSAL_MANIFEST = 'structure/propers/index.json';

  function structurePath(id) {
    return 'structure/propers/' + id + '.json';
  }

  /* ------------------------------------------------------------------------
   * Order
   *
   * Every list on this page is in a meaningful order, never an alphabetical
   * one. Alphabetical order would interleave Advent with Pentecost and file
   * the sanctoral by the spelling of a saint's name.
   * --------------------------------------------------------------------- */

  // Types in the order a missal is read in, not the order they were declared.
  const KIND_SEQUENCE = ['seasonal', 'christological', 'marian', 'saintly'];

  const KIND_LABELS = {
    seasonal: 'Seasonal',
    christological: 'Christological',
    marian: 'Marian',
    saintly: 'Saintly'
  };

  const MONTHS = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  /**
   * The calendar date a Mass is kept on, as [month, day], or null.
   *
   * A sanctoral entry carries it either as `date` ("08-15") or inside
   * `registry` ("1962-08-15", "pc-08-15"). A seasonal entry carries neither —
   * its registry is a position in the temporal cycle ("39", "pc-s01", "T02") —
   * and must not be mistaken for one.
   */
  function massDate(mass) {
    const raw = String((mass && (mass.date || mass.registry)) || '');
    const found = /(?:^|[^\d])(\d{2})-(\d{2})$/.exec(raw);
    if (!found) return null;
    const month = Number(found[1]);
    const day = Number(found[2]);
    if (month < 1 || month > 12 || day < 1 || day > 31) return null;
    return [month, day];
  }

  /**
   * Put one type's Masses in reading order.
   *
   * Dated Masses — the sanctoral — go in calendar-date order, which the
   * structure files are not already in. Everything else keeps the order of the
   * structure file, which is the temporal cycle for the seasonal Masses and is
   * the compiler's own sequence for anything else. Never alphabetical.
   *
   * A type holding both is sorted date-first and file-order-after, so that
   * neither half is scrambled by the other.
   */
  function orderMasses(masses) {
    const dated = [];
    const undated = [];
    masses.forEach((mass, index) => {
      const date = massDate(mass);
      (date ? dated : undated).push({ mass: mass, index: index, date: date });
    });
    dated.sort((a, b) => {
      return (a.date[0] - b.date[0]) || (a.date[1] - b.date[1]) || (a.index - b.index);
    });
    return dated.concat(undated).map((held) => held.mass);
  }

  /** The optgroup a Mass belongs in: its season, or the month it is kept in. */
  function massGroup(mass) {
    if (mass.season) return T.titleCase(mass.season);
    const date = massDate(mass);
    if (date) return MONTHS[date[0] - 1];
    return null;
  }

  /** Types present in a missal, in reading order, each with its Masses. */
  function groupByKind(masses) {
    const held = new Map();
    for (const mass of masses) {
      const kind = mass.kind || 'other';
      if (!held.has(kind)) held.set(kind, []);
      held.get(kind).push(mass);
    }

    const known = KIND_SEQUENCE.filter((kind) => held.has(kind));
    // A kind the sequence above does not name is still offered, after the ones
    // it does, in the order the file introduced it — never dropped.
    const rest = Array.from(held.keys()).filter((kind) => KIND_SEQUENCE.indexOf(kind) < 0);

    return known.concat(rest).map((kind) => ({
      kind: kind,
      label: KIND_LABELS[kind] || T.titleCase(kind),
      masses: orderMasses(held.get(kind))
    }));
  }

  /* ------------------------------------------------------------------------
   * State
   * --------------------------------------------------------------------- */

  const state = {
    bibles: [],
    bibleId: null,
    missals: [],
    missalId: null,
    structure: null,
    kinds: [],
    kind: null,
    masses: [],
    massKey: null
  };

  /* ------------------------------------------------------------------------
   * Elements
   * --------------------------------------------------------------------- */

  const missalSelect = document.getElementById('missal-select');
  const typeSelect = document.getElementById('type-select');
  const massSelect = document.getElementById('mass-select');
  const bibleSelect = document.getElementById('bible-select');
  const prevButton = document.getElementById('prev-button');
  const nextButton = document.getElementById('next-button');
  const reading = document.getElementById('reading');
  const controls = document.getElementById('controls');

  /* ------------------------------------------------------------------------
   * Discovery
   * --------------------------------------------------------------------- */

  function described(id, label, edition) {
    return {
      id: id,
      label: label || T.titleCase(id),
      edition: edition || null
    };
  }

  async function discoverMissals() {
    const listed = T.params.get('missals');
    if (listed) {
      return listed.split(',').map((id) => id.trim()).filter(Boolean).map((id) => described(id));
    }

    try {
      const file = await T.loadJSON(MISSAL_MANIFEST);
      const entries = (file && (file.missals || file.calendars)) || [];
      if (entries.length) {
        return entries.map((entry) => {
          if (typeof entry === 'string') return described(entry);
          return described(entry.id, entry.label || entry.edition, entry.edition);
        });
      }
    } catch (error) {
      // No manifest is the normal case today; fall through to the probe.
    }

    const present = await Promise.all(
      MISSAL_CANDIDATES.map((id) => T.exists(structurePath(id)))
    );
    return MISSAL_CANDIDATES.filter((id, index) => present[index]).map((id) => described(id));
  }

  // One attempt per missal, remembered — including a failed one, so a missal
  // that cannot be loaded is not fetched again every time it is chosen.
  const structures = new Map();

  function ensureStructure(id) {
    const held = structures.get(id);
    if (held) return held;

    const attempt = (async () => {
      let file;
      try {
        file = await T.loadJSON(structurePath(id));
      } catch (error) {
        return {
          ok: false,
          message: 'The missal "' + id + '" could not be loaded: ' +
            (error.message || error)
        };
      }
      const masses = (file && file.masses) || [];
      if (!masses.length) {
        return { ok: false, message: 'The missal "' + id + '" lists no Masses.' };
      }
      return { ok: true, file: file };
    })();

    structures.set(id, attempt);
    return attempt;
  }

  /* ------------------------------------------------------------------------
   * Controls
   * --------------------------------------------------------------------- */

  /**
   * Fill the missal select, naming each missal as its own file names it.
   *
   * Before a missal is loaded the only name available is its id, so the id is
   * shown, made readable. Once its structure has been read the file's `edition`
   * replaces it, which is why this is called again after every load.
   */
  function fillMissalSelect() {
    T.fillSelect(missalSelect, state.missals.map((missal) => ({
      value: missal.id,
      label: missal.edition || missal.label,
      title: missal.id
    })));
    if (state.missalId) missalSelect.value = state.missalId;
  }

  function fillTypeSelect() {
    T.fillSelect(typeSelect, state.kinds.map((group) => ({
      value: group.kind,
      label: group.label + ' — ' + group.masses.length +
        (group.masses.length === 1 ? ' Mass' : ' Masses')
    })));
    if (state.kind) typeSelect.value = state.kind;
  }

  function fillMassSelect() {
    T.fillSelect(massSelect, state.masses.map((mass) => ({
      value: mass.key,
      label: mass.name || mass.key,
      group: massGroup(mass)
    })));
    if (state.massKey) massSelect.value = state.massKey;
  }

  function currentMissal() {
    return state.missals.find((missal) => missal.id === state.missalId) || null;
  }

  function currentBible() {
    return state.bibles.find((bible) => bible.id === state.bibleId) || null;
  }

  function currentMass() {
    return state.masses.find((mass) => mass.key === state.massKey) || null;
  }

  function massIndex() {
    return state.masses.findIndex((mass) => mass.key === state.massKey);
  }

  function syncControls() {
    if (state.missalId) missalSelect.value = state.missalId;
    if (state.kind) typeSelect.value = state.kind;
    if (state.massKey) massSelect.value = state.massKey;
    if (state.bibleId) bibleSelect.value = state.bibleId;

    const index = massIndex();
    prevButton.disabled = index <= 0;
    nextButton.disabled = index < 0 || index >= state.masses.length - 1;
  }

  function writeHash() {
    T.writeHash([
      ['missal', state.missalId],
      ['type', state.kind],
      ['mass', state.massKey],
      ['bible', state.bibleId]
    ]);
  }

  /* ------------------------------------------------------------------------
   * Rendering
   * --------------------------------------------------------------------- */

  /** Every citation a Mass carries, including each cycle's. */
  function citationsOf(mass) {
    const found = [];
    for (const proper of (mass && mass.propers) || []) {
      for (const citation of proper.citations || []) found.push(citation);
      const cycles = proper.cycles || {};
      for (const key of Object.keys(cycles)) {
        for (const citation of cycles[key] || []) found.push(citation);
      }
    }
    return found;
  }

  /** A cycle's readable name: "Year A" for the Sunday cycles, else the key. */
  function cycleLabel(key) {
    return /^[A-C]$/.test(key) ? 'Year ' + key : 'Cycle ' + key;
  }

  function renderProper(proper, bible, fragments) {
    const section = T.el('section', 'proper');

    const heading = T.el('h3', 'proper-name', proper.name || 'Proper');
    // "Vigil Mass", "Mass at Dawn" — the form this proper belongs to, where a
    // day carries more than one.
    if (proper.form) heading.appendChild(T.el('span', 'proper-form', proper.form));
    section.appendChild(heading);

    if (proper.incipit) {
      section.appendChild(T.el('p', 'proper-incipit', proper.incipit));
    }

    // Composed propers — Collects, Secrets, Postcommunions — are not scripture
    // and have no citation to resolve. Where the structure file carries the
    // text, it is shown; where it carries only the incipit, that is said, once
    // and quietly. It is not a failure: the corpus indexes these propers by
    // their opening words and does not hold their bodies.
    if (proper.text) {
      const composed = T.el('p', 'composed');
      composed.appendChild(
        T.el('span', 'composed-label', 'Composed text — not scripture')
      );
      composed.appendChild(document.createTextNode(proper.text));
      // The structure file names no language for it, so none is asserted here.
      if (proper.language) composed.lang = proper.language;
      section.appendChild(composed);
    } else if (proper.incipit && proper.source === 'composed') {
      section.appendChild(
        T.el('p', 'composed-note',
          'Composed text — not scripture. The corpus carries its incipit only.')
      );
    }

    const numbering = (state.structure && state.structure.numbering) || null;
    const citations = proper.citations || [];
    for (const citation of citations) {
      section.appendChild(T.renderCitation(citation, bible, fragments, numbering));
    }

    // A cycle-varying proper reads differently in each year of the lectionary.
    // The structure file keeps the years apart, and so does this: merging them
    // would hand the reader three readings with no way to tell which is this
    // year's.
    const cycles = proper.cycles || {};
    const cycleKeys = Object.keys(cycles).filter((key) => (cycles[key] || []).length).sort();
    for (const key of cycleKeys) {
      const block = T.el('div', 'cycle');
      block.appendChild(T.el('h4', 'cycle-name', cycleLabel(key)));
      for (const citation of cycles[key]) {
        block.appendChild(T.renderCitation(citation, bible, fragments, numbering));
      }
      section.appendChild(block);
    }

    if (!proper.text && !proper.incipit && !citations.length && !cycleKeys.length) {
      section.appendChild(
        T.notice('this proper carries neither a citation nor a text.')
      );
    }

    return section;
  }

  /**
   * Does this Mass carry anything to read?
   *
   * Most of the sanctoral is presently a registry entry and a placeholder
   * proper: the calendar knows the day, and the propers for it have not been
   * compiled yet. That is worth saying once, plainly, rather than repeating
   * "this proper carries neither a citation nor a text" down an empty page.
   */
  function hasContent(mass) {
    for (const proper of (mass && mass.propers) || []) {
      if (proper.text || proper.incipit) return true;
      if ((proper.citations || []).length) return true;
      const cycles = proper.cycles || {};
      for (const key of Object.keys(cycles)) {
        if ((cycles[key] || []).length) return true;
      }
    }
    return false;
  }

  function renderMass(mass, bible, fragments, chapterCount) {
    reading.appendChild(T.el('h2', 'entry-title', mass.name || mass.key));

    const missal = currentMissal();
    const meta = [];
    if (missal) meta.push(missal.edition || missal.label);
    const group = state.kinds.find((held) => held.kind === state.kind);
    if (group) meta.push(group.label);
    if (mass.season) meta.push('Season: ' + T.titleCase(mass.season));
    const date = massDate(mass);
    if (date) meta.push(MONTHS[date[0] - 1] + ' ' + date[1]);
    reading.appendChild(
      T.el('p', 'entry-meta', meta.concat(T.bibleMeta(bible)).join(' · '))
    );

    const propers = mass.propers || [];
    const empty = !hasContent(mass);
    if (empty) {
      reading.appendChild(
        T.el('p', 'placeholder',
          'This missal keeps the day, and its structure file carries no propers ' +
          'for it yet' + (mass.registry ? ' (registry ' + mass.registry + ')' : '') +
          '. Nothing is hidden here: there is nothing compiled to show.')
      );
    } else {
      for (const proper of propers) {
        reading.appendChild(renderProper(proper, bible, fragments));
      }
    }

    const position = massIndex() + 1;
    T.statusLine(
      (mass.name || mass.key) + ', ' + bible.label + '. Mass ' + position +
      ' of ' + state.masses.length + ', ' +
      (empty ? 'no propers compiled yet' : propers.length + ' propers, ' +
        chapterCount + ' chapters') + '.'
    );
  }

  async function render(options) {
    const mass = currentMass();
    const bible = currentBible();
    if (!mass || !bible) return;

    const token = T.beginRender();
    reading.setAttribute('aria-busy', 'true');

    const held = await T.fetchFragments(bible, citationsOf(mass));

    // A later selection may have overtaken this one while fragments were in
    // flight; the newest render wins.
    if (!T.isCurrentRender(token)) return;

    T.clear(reading);
    renderMass(mass, bible, held.fragments, held.chapters.length);
    reading.setAttribute('aria-busy', 'false');

    if (options && options.moveFocus) reading.focus();
  }

  /* ------------------------------------------------------------------------
   * Selection
   * --------------------------------------------------------------------- */

  function select(massKey, bibleId, options) {
    if (massKey) state.massKey = massKey;
    if (bibleId) state.bibleId = bibleId;
    syncControls();
    writeHash();
    render(options);
  }

  function step(delta, options) {
    const index = massIndex();
    const next = index + delta;
    if (index < 0 || next < 0 || next >= state.masses.length) return;
    select(state.masses[next].key, null, options);
  }

  function setKind(kind, preferredMass, options) {
    const group = state.kinds.find((held) => held.kind === kind);
    if (!group) return;

    state.kind = kind;
    state.masses = group.masses;
    fillTypeSelect();
    fillMassSelect();

    const key = state.masses.some((mass) => mass.key === preferredMass)
      ? preferredMass
      : (state.masses.some((mass) => mass.key === state.massKey)
        ? state.massKey
        : (state.masses[0] && state.masses[0].key));

    if (!key) {
      state.massKey = null;
      syncControls();
      T.fail('This missal holds no Masses of the "' + kind + '" type.');
      return;
    }
    select(key, null, options);
  }

  /**
   * Open a missal: load its structure, then rebuild the type list and the Mass
   * list from it. Everything downstream of the missal is discarded first, so a
   * failed load cannot leave the previous missal's Masses on screen under the
   * new missal's name.
   */
  async function setMissal(id, prefer, options) {
    if (!state.missals.some((missal) => missal.id === id)) return;

    state.missalId = id;
    state.structure = null;
    state.kinds = [];
    state.masses = [];
    state.massKey = null;
    syncControls();

    const loaded = await ensureStructure(id);
    // A reader who chose again while the structure was in flight wins.
    if (state.missalId !== id) return;

    if (!loaded.ok) {
      T.fillSelect(typeSelect, []);
      T.fillSelect(massSelect, []);
      syncControls();
      T.fail(loaded.message);
      return;
    }

    state.structure = loaded.file;

    const missal = currentMissal();
    if (missal && loaded.file.edition) {
      missal.edition = String(loaded.file.edition);
      fillMissalSelect();
    }

    state.kinds = groupByKind(loaded.file.masses || []);
    if (!state.kinds.length) {
      T.fillSelect(typeSelect, []);
      T.fillSelect(massSelect, []);
      T.fail('The missal "' + id + '" holds no Masses of any type.');
      return;
    }

    const wanted = prefer && prefer.kind;
    const kind = state.kinds.some((held) => held.kind === wanted)
      ? wanted
      : (state.kinds.some((held) => held.kind === state.kind)
        ? state.kind
        : state.kinds[0].kind);

    setKind(kind, prefer && prefer.mass, options);
  }

  /* ------------------------------------------------------------------------
   * Start-up
   * --------------------------------------------------------------------- */

  T.setInlineNotice(
    'No data root could be reached at "' + T.dataRoot + '", so this page is ' +
    'showing its built-in fallback: one missal, one Mass and a diagnostics ' +
    'entry. Serve the pages over HTTP with the corpus at that path, or try ' +
    '?data=fixture.'
  );

  // The fallback's own missal, for a page opened straight off disk. It is not
  // the data contract; the diagnostics entry is labelled so that no real Mass
  // can be mistaken for carrying invented data.
  T.addInlineFiles({
    'structure/propers/roman-1962.json': {
      schema: 'triptych-propers-structure/v1',
      calendar: 'roman-1962',
      edition: 'Built-in fallback (not the missal)',
      numbering: 'vulgate',
      masses: [
        {
          key: 'advent-1',
          name: 'First Sunday of Advent',
          season: 'advent',
          kind: 'seasonal',
          registry: '39',
          propers: [
            {
              name: 'Introit',
              incipit: 'Ad te levavi',
              source: 'scripture',
              citations: [
                {
                  ref: 'Psalm 24:1-3',
                  token: 'Ps',
                  loci: {
                    vulgate: [{ chapter: 24, first: 1, last: 3 }],
                    hebrew: [{ chapter: 25, first: 1, last: 3 }]
                  },
                  unresolved: null
                }
              ]
            },
            {
              name: 'Collect',
              incipit: 'Excita, quaesumus',
              source: 'composed',
              text:
                'Excita, quaesumus, Domine, potentiam tuam, et veni: ut ab ' +
                'imminentibus peccatorum nostrorum periculis, te mereamur ' +
                'protegente eripi, te liberante salvari: Qui vivis...'
            },
            {
              name: 'Epistle',
              incipit: null,
              source: 'scripture',
              citations: [
                {
                  ref: 'Romans 13:11-12',
                  token: 'Rom',
                  loci: {
                    vulgate: [{ chapter: 13, first: 11, last: 12 }],
                    hebrew: [{ chapter: 13, first: 11, last: 12 }]
                  },
                  unresolved: null
                }
              ]
            }
          ]
        },
        {
          key: 'fallback-diagnostics',
          name: 'Fallback diagnostics (not a Mass)',
          season: null,
          kind: 'diagnostic',
          registry: 'x00',
          propers: [
            {
              name: 'Unresolved citation',
              incipit: 'the reason is shown instead of the text',
              source: 'scripture',
              citations: [
                { ref: 'Psalm 151:1', token: 'Ps', loci: {}, unresolved: 'Ps has no chapter 151' }
              ]
            },
            {
              name: 'Missing fragment',
              incipit: 'no chapter file for Tob 3 in the fallback',
              source: 'scripture',
              citations: [
                {
                  ref: 'Tobias 3:1-2',
                  token: 'Tob',
                  loci: {
                    vulgate: [{ chapter: 3, first: 1, last: 2 }],
                    hebrew: [{ chapter: 3, first: 1, last: 2 }]
                  },
                  unresolved: null
                }
              ]
            },
            {
              name: 'Numbering absent',
              incipit: 'hebrew-only loci, read by a vulgate-numbered edition',
              source: 'scripture',
              citations: [
                {
                  ref: 'Psalm 24:1',
                  token: 'Ps',
                  loci: { hebrew: [{ chapter: 25, first: 1, last: 1 }] },
                  unresolved: null
                }
              ]
            },
            {
              name: 'Verses absent from a fragment that is present',
              incipit: 'Ps 24 is held, and has no verse 40',
              source: 'scripture',
              citations: [
                {
                  ref: 'Psalm 24:40-41',
                  token: 'Ps',
                  loci: {
                    vulgate: [{ chapter: 24, first: 40, last: 41 }],
                    hebrew: [{ chapter: 25, first: 40, last: 41 }]
                  },
                  unresolved: null
                }
              ]
            }
          ]
        }
      ]
    }
  });

  function preferenceFrom(hash) {
    return { kind: hash.get('type'), mass: hash.get('mass') };
  }

  async function start() {
    const loaded = await T.loadBibles();
    if (!loaded.ok) {
      T.fail(loaded.message);
      return;
    }
    state.bibles = loaded.bibles;
    T.fillBibleSelect(bibleSelect, state.bibles);

    const hash = T.readHash();
    const wantedBible = hash.get('bible');
    state.bibleId = state.bibles.some((bible) => bible.id === wantedBible)
      ? wantedBible
      : state.bibles[0].id;
    bibleSelect.value = state.bibleId;

    state.missals = await discoverMissals();
    if (!state.missals.length) {
      T.fail(
        'No missal could be found under "' + T.dataPath('structure/propers/') +
        '". Name one with ?missals=<id>, or serve the corpus at ?data=.'
      );
      return;
    }
    fillMissalSelect();

    const wantedMissal = hash.get('missal');
    const missalId = state.missals.some((missal) => missal.id === wantedMissal)
      ? wantedMissal
      : state.missals[0].id;

    await setMissal(missalId, preferenceFrom(hash), { moveFocus: false });
  }

  /* ------------------------------------------------------------------------
   * Events
   * --------------------------------------------------------------------- */

  missalSelect.addEventListener('change', () => {
    setMissal(missalSelect.value, null, { moveFocus: false });
  });

  typeSelect.addEventListener('change', () => {
    setKind(typeSelect.value, null, { moveFocus: false });
  });

  massSelect.addEventListener('change', () => {
    select(massSelect.value, null, { moveFocus: false });
  });

  bibleSelect.addEventListener('change', () => {
    select(null, bibleSelect.value, { moveFocus: false });
  });

  prevButton.addEventListener('click', () => step(-1, { moveFocus: true }));
  nextButton.addEventListener('click', () => step(1, { moveFocus: true }));

  controls.addEventListener('submit', (event) => event.preventDefault());

  T.onArrowStep((delta) => step(delta, { moveFocus: false }));

  T.onHashChange((hash) => {
    const wantedBible = hash.get('bible');
    if (state.bibles.some((bible) => bible.id === wantedBible)) {
      state.bibleId = wantedBible;
    }

    const wantedMissal = hash.get('missal');
    if (wantedMissal && wantedMissal !== state.missalId) {
      setMissal(wantedMissal, preferenceFrom(hash), { moveFocus: false });
      return;
    }

    const wantedKind = hash.get('type');
    if (wantedKind && wantedKind !== state.kind) {
      setKind(wantedKind, hash.get('mass'), { moveFocus: false });
      return;
    }

    const wantedMass = hash.get('mass');
    const key = state.masses.some((mass) => mass.key === wantedMass)
      ? wantedMass
      : state.massKey;
    select(key, state.bibleId, { moveFocus: false });
  });

  start();
}());
