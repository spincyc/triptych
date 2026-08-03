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
   *
   * THE ORDER ARRIVES WITH THE DATA, AND THIS PAGE DOES NOT RE-SORT IT. Each
   * structure file lists a kind's Masses in the order its calendar source
   * compiles them: the temporal cycle for the seasonal Masses, beginning at the
   * First Sunday of Advent, and the civil date for everything dated. Sorting
   * here would put a second ordering beside that one, free to disagree with it
   * — and the sort that used to stand here did disagree. It read a calendar
   * date out of each registry id with a pattern, so the three dated days of the
   * Christmas octave, whose ids are "1962-12-29" and its two fellows but whose
   * place is in the temporal cycle, were hoisted to the head of the seasonal
   * list ahead of Advent, and the sixty commemorations whose ids end "-comm"
   * were read as undated and exiled to the tail of the sanctoral.
   * --------------------------------------------------------------------- */

  // Types in the order a missal is read in, not the order they were declared.
  const KIND_SEQUENCE = ['seasonal', 'christological', 'marian', 'sanctoral'];

  const KIND_LABELS = {
    seasonal: 'Seasonal',
    christological: 'Christological',
    marian: 'Marian',
    sanctoral: 'Sanctoral'
  };

  const MONTHS = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  /**
   * The calendar date a Mass is kept on, as [month, day], or null.
   *
   * Read from the Mass's own `date` ("08-15"), which the structure file carries
   * because its calendar source records it. It is never read back out of the
   * registry id: the registry conventions belong to the calendar and not to
   * this page, a date-shaped id is not always a date and a dated entry does not
   * always end in one.
   */
  function massDate(mass) {
    const found = /^(\d{2})-(\d{2})$/.exec(String((mass && mass.date) || ''));
    if (!found) return null;
    const month = Number(found[1]);
    const day = Number(found[2]);
    if (month < 1 || month > 12 || day < 1 || day > 31) return null;
    return [month, day];
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
      // In the file's own order, which is the missal's; see Order above.
      masses: held.get(kind)
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
    massKey: null,
    // The language the composed propers are asked for. T.SOURCE_LANGUAGE means
    // "as the missal prints them", which is the only setting guaranteed to
    // have a text behind it for every proper.
    orations: null,
    orationLanguages: []
  };

  /* ------------------------------------------------------------------------
   * Elements
   * --------------------------------------------------------------------- */

  const missalSelect = document.getElementById('missal-select');
  const typeSelect = document.getElementById('type-select');
  const massSelect = document.getElementById('mass-select');
  const bibleSelect = document.getElementById('bible-select');
  const orationsSelect = document.getElementById('orations-select');
  const prevButton = document.getElementById('prev-button');
  const nextButton = document.getElementById('next-button');
  const reading = document.getElementById('reading');
  const controls = document.getElementById('controls');
  const formularyTitle = document.getElementById('formulary-title');
  const formularyMeta = document.getElementById('formulary-meta');
  const noticesDisclosure = document.getElementById('notices-disclosure');
  const banner = document.getElementById('banner');

  function syncNoticesDisclosure() {
    const shown = banner && !banner.hidden && banner.textContent.trim();
    noticesDisclosure.hidden = !shown;
    if (!shown) noticesDisclosure.open = false;
  }

  if (banner) {
    new MutationObserver(syncNoticesDisclosure).observe(banner, {
      attributes: true,
      childList: true,
      characterData: true
    });
    syncNoticesDisclosure();
  }

  /* ------------------------------------------------------------------------
   * Discovery
   * --------------------------------------------------------------------- */

  /**
   * A missal has three names, and they are not interchangeable.
   *
   *   short    "1962 Missal" — what a reader would say, and what the control
   *            shows. Authored in the calendar source beside the edition it
   *            shortens, never composed here.
   *   edition  "Missale Romanum, editio typica 1962" — the bibliographic
   *            identification. It is what the page prints against the texts
   *            themselves, because a page serving prayers must say which book
   *            they were read out of.
   *   label    the id made readable, and only until the file has been fetched.
   */
  function described(id, label, edition, short) {
    return {
      id: id,
      label: label || T.titleCase(id),
      edition: edition || null,
      short: short || null
    };
  }

  /**
   * Which missals this corpus holds, and which one to open on.
   *
   * `mass-propers structure` writes the manifest beside the structure files it
   * writes, listing exactly the missals that are THERE. The page used to probe
   * a hand-typed pair of ids instead — a restatement of what those files
   * already declare, which cost a 404 on every load and would have gone stale
   * the moment a third missal landed, as one now has.
   *
   * `landing` is read, never inferred from row order. The manifest does put it
   * first, and relying on that would work today and break silently the day the
   * order changed for some unrelated reason.
   */
  async function discoverMissals() {
    const listed = T.params.get('missals');
    if (listed) {
      const named = listed.split(',').map((id) => id.trim()).filter(Boolean).map((id) => described(id));
      return { missals: named, landing: named.length ? named[0].id : '' };
    }

    const file = await T.loadJSON(MISSAL_MANIFEST);
    const entries = (file && (file.missals || file.calendars)) || [];
    const missals = entries.map((entry) => {
      if (typeof entry === 'string') return described(entry);
      return described(
        entry.id, entry.label || entry.edition, entry.edition, entry.edition_short);
    });
    const declared = (file && file.default) || '';
    return {
      missals: missals,
      landing: missals.some((missal) => missal.id === declared)
        ? declared
        : (missals.length ? missals[0].id : '')
    };
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
      // The short name where the file offers one. A missal whose source has not
      // been given one falls back to the edition string rather than to the id:
      // long is better than cryptic, and the fallback is visible enough to get
      // the source fixed.
      label: missal.short || missal.edition || missal.label,
      // The full identification is a hover away, and is printed in full against
      // the propers themselves.
      title: missal.edition || missal.id
    })));
    if (state.missalId) missalSelect.value = state.missalId;
  }

  function fillTypeSelect() {
    T.fillSelect(typeSelect, state.kinds.map((group) => ({
      value: group.kind,
      label: group.label
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

  function fillOrationsSelect() {
    T.fillSelect(orationsSelect, state.orationLanguages.map((entry) => ({
      value: entry.lang,
      // The source language needs no coverage figure: it is what the missal
      // prints, so it is complete by definition. Every other entry states how
      // far it reaches, because none of them reaches everywhere.
      label: T.orationLanguageLabel(entry),
      title: entry.lang
    })));
    orationsSelect.disabled = state.orationLanguages.length < 2;
    if (state.orations) orationsSelect.value = state.orations;
  }

  function massIndex() {
    return state.masses.findIndex((mass) => mass.key === state.massKey);
  }

  function syncControls() {
    if (state.missalId) missalSelect.value = state.missalId;
    if (state.kind) typeSelect.value = state.kind;
    if (state.massKey) massSelect.value = state.massKey;
    if (state.bibleId) bibleSelect.value = state.bibleId;
    if (state.orations) orationsSelect.value = state.orations;

    const index = massIndex();
    prevButton.disabled = index <= 0;
    nextButton.disabled = index < 0 || index >= state.masses.length - 1;
  }

  function writeHash() {
    T.writeHash([
      ['missal', state.missalId],
      ['type', state.kind],
      ['mass', state.massKey],
      ['bible', state.bibleId],
      // Only when it is not the default, so an ordinary link stays short.
      ['orations', state.orations === T.SOURCE_LANGUAGE ? null : state.orations]
    ]);
  }

  /* ------------------------------------------------------------------------
   * Rendering
   * --------------------------------------------------------------------- */

  function renderMass(mass, bible, fragments, chapterCount) {
    formularyTitle.textContent = mass.name || mass.key;

    const missal = currentMissal();
    const meta = [];
    if (missal) meta.push(missal.edition || missal.label);
    const group = state.kinds.find((held) => held.kind === state.kind);
    if (group) meta.push(group.label);
    if (mass.season) meta.push('Season: ' + T.titleCase(mass.season));
    const date = massDate(mass);
    if (date) meta.push(MONTHS[date[0] - 1] + ' ' + date[1]);
    formularyMeta.textContent = meta.concat(T.bibleMeta(bible)).join(' · ');

    const propers = mass.propers || [];
    const empty = !T.massHasContent(mass);
    if (empty) {
      // One line, and the same line the assembly page shows, because it is the
      // same fact about the same Mass.
      reading.appendChild(T.uncompiledNote(mass));
    } else {
      for (const proper of propers) {
        reading.appendChild(T.renderProper(proper, bible, fragments, {
          numbering: (state.structure && state.structure.numbering) || null,
          orations: state.orations,
          heading: 'h2'
        }));
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

    const held = await T.fetchFragments(bible, T.citationsOf(mass));

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

    // Both names come out of the file the missal itself ships, so the control
    // renames itself once the missal is open and the site holds no opinion of
    // its own about what either book is called.
    const missal = currentMissal();
    if (missal && (loaded.file.edition || loaded.file.edition_short)) {
      if (loaded.file.edition) missal.edition = String(loaded.file.edition);
      if (loaded.file.edition_short) missal.short = String(loaded.file.edition_short);
      fillMissalSelect();
    }

    // Which languages the orations can be read in is a property of the missal,
    // not of the site: the two differ, and a language offered for one may be
    // absent from the other. A selection that the new missal cannot honour
    // falls back to what it prints rather than silently showing Latin under an
    // English label.
    state.orationLanguages = T.orationLanguagesOf(loaded.file);
    if (!state.orationLanguages.some((entry) => entry.lang === state.orations)) {
      state.orations = T.SOURCE_LANGUAGE;
    }
    fillOrationsSelect();

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
    // Settled before the first missal loads, so the first render already
    // honours it; setMissal drops it if that missal cannot offer it.
    state.orations = hash.get('orations') || T.SOURCE_LANGUAGE;
    const wantedBible = hash.get('bible');
    state.bibleId = state.bibles.some((bible) => bible.id === wantedBible)
      ? wantedBible
      : state.bibles[0].id;
    bibleSelect.value = state.bibleId;

    const discovered = await discoverMissals();
    state.missals = discovered.missals;
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
      : discovered.landing;

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

  orationsSelect.addEventListener('change', () => {
    state.orations = orationsSelect.value;
    select(null, null, { moveFocus: false });
  });

  prevButton.addEventListener('click', () => step(-1, { moveFocus: true }));
  nextButton.addEventListener('click', () => step(1, { moveFocus: true }));

  controls.addEventListener('submit', (event) => event.preventDefault());

  T.onArrowStep((delta) => step(delta, { moveFocus: false }));

  T.onHashChange((hash) => {
    const wantedOrations = hash.get('orations') || T.SOURCE_LANGUAGE;
    if (state.orationLanguages.some((entry) => entry.lang === wantedOrations)) {
      state.orations = wantedOrations;
    }

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
