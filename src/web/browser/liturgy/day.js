/* ===========================================================================
 * Why this Mass today — the day's Mass, with the reasoning in the margin
 * ===========================================================================
 *
 * THIS PAGE SHOWS THE TEXT. It is the propers page reached by a different
 * route: there a reader chooses a Mass, here a reader chooses a date and the
 * rubrics choose the Mass. What is on the screen in both cases is the same
 * thing — the propers, in order, in the reader's translation, set by the same
 * shared code in ../shared/browser-core.js.
 *
 * The rubrical account is why the reader is being shown THAT Mass rather than
 * another, so it belongs beside the text and not in front of it. It renders
 * into the margin: `<details class="margin">` beside each proper it explains.
 * The page used to render that reasoning as the body — a verdict box, five
 * numbered step blocks and nine to eleven bordered rows on every date, before
 * a word of any prayer — and it read as a wall of error boxes.
 *
 * NOTHING IS DECIDED HERE. Every rank, disposition, ceiling and rubric number
 * arrives from `assembly-model.js`, which reads them out of the rubrics file
 * the repository tracks; `calendar-rubrics check` runs that same model under
 * node against the solved cases, so what a reader sees is what the check holds.
 *
 *   structure/rubrics/index.json      which missals have rules   ~1 KB
 *   structure/rubrics/<missal>.json   the rules themselves       ~45-75 KB
 *   structure/calendar/<missal>/<year>.json   the day's candidates   ~30 KB
 *   structure/propers/<missal>.json   the texts                  ~1 MB
 *
 * The propers file is the big one and is fetched last, after the day is named,
 * so the reader is not looking at nothing while a megabyte lands.
 *
 *   ?data=<root>        where the corpus lives (default ../browse)
 *   #date=<YYYY-MM-DD>&missal=<id>&bible=<id>&orations=<lang>
 * ======================================================================== */

'use strict';

(function () {
  const T = window.Triptych;
  const Model = window.MassAssembly;

  const RUBRICS_INDEX = 'structure/rubrics/index.json';

  function rubricsPath(id) { return 'structure/rubrics/' + id + '.json'; }
  function yearPath(id, year) { return 'structure/calendar/' + id + '/' + year + '.json'; }
  function propersPath(id) { return 'structure/propers/' + id + '.json'; }

  const MONTHS = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];
  const WEEKDAY_NAMES = {
    sunday: 'Sunday', monday: 'Monday', tuesday: 'Tuesday', wednesday: 'Wednesday',
    thursday: 'Thursday', friday: 'Friday', saturday: 'Saturday'
  };

  // Above this the margin is a margin. Below it there is no room for one, and
  // what it becomes is decided in `openMargins` rather than left to reflow.
  const WIDE = '(min-width: 60rem)';

  const state = {
    missals: [],
    missalId: null,
    rubrics: null,
    date: null,
    derived: null,
    bibles: [],
    bibleId: null,
    structure: null,
    orations: null,
    orationLanguages: []
  };

  const dateInput = document.getElementById('date-input');
  const missalSelect = document.getElementById('missal-select');
  const bibleSelect = document.getElementById('bible-select');
  const orationsSelect = document.getElementById('orations-select');
  const prevButton = document.getElementById('prev-button');
  const nextButton = document.getElementById('next-button');
  const todayButton = document.getElementById('today-button');
  const reading = document.getElementById('reading');
  const controls = document.getElementById('controls');

  /* ------------------------------------------------------------------------
   * Small helpers
   * --------------------------------------------------------------------- */

  function todayISO() {
    const now = new Date();
    return [
      now.getFullYear(),
      String(now.getMonth() + 1).padStart(2, '0'),
      String(now.getDate()).padStart(2, '0')
    ].join('-');
  }

  function longDate(isoDate, weekday) {
    const parts = isoDate.split('-');
    return (WEEKDAY_NAMES[weekday] || '') + ' ' + Number(parts[2]) + ' ' +
      MONTHS[Number(parts[1]) - 1] + ' ' + parts[0];
  }

  /** A rubric number, set as a citation. Absent rather than empty when unknown. */
  function locus(text) {
    return text ? T.el('span', 'locus', text) : null;
  }

  function withLocus(node, text) {
    const held = locus(text);
    if (held) { node.appendChild(document.createTextNode(' ')); node.appendChild(held); }
    return node;
  }

  function paragraph(className, text, locusText) {
    const node = T.el('p', className, text || '');
    return locusText ? withLocus(node, locusText) : node;
  }

  /* ------------------------------------------------------------------------
   * The margin
   *
   * A margin is a `<details>` so that it works with no script at all and so
   * that on a narrow screen it is one line the reader may open, sitting AFTER
   * the text it annotates rather than before it. Stacking it above the text is
   * what the wide layout is there to avoid, and a narrow screen must not undo
   * that by another route.
   *
   * On a wide screen the disclosure is opened and its summary hidden, so it
   * reads as a marginal note and not as a control. That is done here rather
   * than in CSS because `details` hides its own content when it is closed, and
   * no stylesheet can overrule that.
   * --------------------------------------------------------------------- */

  function margin(summaryText) {
    const node = document.createElement('details');
    node.className = 'margin';
    const summary = document.createElement('summary');
    summary.className = 'margin-summary';
    summary.textContent = summaryText;
    node.appendChild(summary);
    return node;
  }

  function openMargins(root) {
    const wide = window.matchMedia ? window.matchMedia(WIDE).matches : true;
    const found = root.querySelectorAll ? root.querySelectorAll('details.margin') : [];
    for (const one of found) one.open = wide;
  }

  /* ------------------------------------------------------------------------
   * Discovery
   * --------------------------------------------------------------------- */

  async function discoverMissals() {
    const file = await T.loadJSON(RUBRICS_INDEX);
    const rows = (file && file.calendars) || [];
    // The short name for the control and the edition for the hover, the same
    // two names the propers page shows and out of the same calendar source.
    return rows.map((row) => ({
      id: row.calendar,
      label: row.edition_short || row.edition || T.titleCase(row.calendar),
      edition: row.edition || null,
      code: row.code || null,
      commemorates: row.commemorates !== false
    }));
  }

  // One attempt per file, remembered, including a failure: a missal that cannot
  // be loaded is not fetched again on every date change.
  const rubricsCache = new Map();
  const yearCache = new Map();
  const propersCache = new Map();

  function once(cache, key, load) {
    const held = cache.get(key);
    if (held) return held;
    const attempt = load().then(
      (value) => ({ ok: true, value: value }),
      (error) => ({ ok: false, message: error.message || String(error) })
    );
    cache.set(key, attempt);
    return attempt;
  }

  function currentMissal() {
    return state.missals.find((one) => one.id === state.missalId) || null;
  }

  function currentBible() {
    return state.bibles.find((one) => one.id === state.bibleId) || null;
  }

  /* ------------------------------------------------------------------------
   * The head: what day this is
   * --------------------------------------------------------------------- */

  function renderHead(derived, bible) {
    reading.appendChild(T.el('h2', 'entry-title', longDate(derived.date, derived.weekday)));

    const missal = currentMissal();
    const meta = [];
    if (missal) meta.push(missal.edition || missal.label);
    if (derived.season) meta.push(T.titleCase(derived.season));
    if (derived.week) meta.push('Week ' + derived.week);
    const cycle = derived.liturgicalYear && derived.liturgicalYear.lectionary;
    if (cycle) meta.push('Lectionary ' + cycle.sunday + '/' + cycle.weekday);
    reading.appendChild(
      T.el('p', 'entry-meta', meta.concat(T.bibleMeta(bible)).join(' · '))
    );

    // A year the calendar computation itself refused to resolve is a fact about
    // this whole year, not about one proper, so it is said once here.
    const unresolved = (derived.liturgicalYear && derived.liturgicalYear.unresolved) || [];
    for (const row of unresolved) {
      reading.appendChild(
        T.notice('unresolved this year: ' + row.what + ' — ' + row.why));
    }
  }

  /* ------------------------------------------------------------------------
   * The margin beside the Mass: why this Mass and not another
   * --------------------------------------------------------------------- */

  const DISPOSITION_WORDS = {
    commemorated: 'commemorated',
    transferred: 'transferred',
    omitted: 'omitted',
    reduced: 'reduced'
  };

  const SOURCE_WORDS = {
    index: 'in the calendar',
    implied: 'constituted from the season',
    arrived: 'transferred here'
  };

  function massMargin(branch, rubrics, derived) {
    const node = margin('Why this Mass');

    if (branch.winner) {
      const took = T.el('p', 'margin-lead');
      took.appendChild(T.el('strong', null, branch.winner.name));
      took.appendChild(document.createTextNode(
        branch.winner.row != null
          ? (branch.winner.optional ? ' stands highest at ' : ' takes the day at ') +
            Model.placeWord(rubrics) + ' ' + branch.winner.row +
            (branch.winner.class ? ', class ' + branch.winner.class : '') + '.'
          : ' takes the day.'));
      node.appendChild(took);
      if (branch.winner.rowLabel) {
        node.appendChild(paragraph('margin-why', branch.winner.rowLabel, branch.winner.locus));
      }
      node.appendChild(T.el('p', 'margin-why',
        SOURCE_WORDS[branch.winner.source] || branch.winner.source));
      if (branch.winner.optional) {
        node.appendChild(paragraph('margin-why',
          'It is optional; the day below it may be kept instead.', branch.winner.locus));
      }
      if (branch.winner.territorial) {
        node.appendChild(T.el('p', 'margin-why',
          'Holds only where the competent authority has taken the option “' +
          branch.winner.territorial + '”.'));
      }
    } else if (branch.choice) {
      const held = T.el('p', 'margin-lead');
      held.appendChild(T.el('strong', null, 'The choice belongs to the celebrant. '));
      held.appendChild(document.createTextNode(
        branch.choice.what + ' — ' + branch.choice.among.map((one) => one.name).join('; ') + '.'));
      node.appendChild(held);
    }

    // What else stood on the date, and what became of it. This is the whole of
    // the old steps one and three, said in the space it deserves.
    const others = (branch.candidates || []).filter(
      (one) => !branch.winner || one.id !== branch.winner.id);
    if (others.length) {
      node.appendChild(T.el('h4', 'margin-heading', 'Also on this date'));
      const list = T.el('ul', 'margin-list');
      for (const candidate of others) {
        const loser = (branch.losers || []).find((one) => one.id === candidate.id) || null;
        const item = T.el('li');
        item.appendChild(T.el('span', 'margin-name', candidate.name));
        if (loser) {
          item.appendChild(T.el('span', 'tag tag-' + loser.disposition,
            DISPOSITION_WORDS[loser.disposition] || loser.disposition));
        }
        const why = loser ? loser.why : candidate.why;
        const where = loser ? loser.locus : candidate.locus;
        if (why) item.appendChild(paragraph('margin-why', why, where));
        if (loser && loser.destination) {
          item.appendChild(T.el('p', 'margin-why',
            'Kept on ' + longDate(loser.destination, Model.weekdayOf(loser.destination)) + '.'));
        }
        if (loser && loser.destinationNotComputed) {
          item.appendChild(T.el('p', 'margin-why',
            'This page does not compute where it goes. ' + loser.destinationNotComputed));
        }
        list.appendChild(item);
      }
      node.appendChild(list);
    }

    // Why this many orations, whether or not it turned anything away.
    const ceiling = (branch.ceilings || {}).low_mass;
    if (ceiling) {
      node.appendChild(paragraph('margin-why', ceiling.what ||
        ('This day admits ' + ceiling.max + ' commemoration' +
         (ceiling.max === 1 ? '' : 's') + '.'), ceiling.locus));
    }

    const category = rubrics.mass_category || {};
    if (category.assumed) {
      node.appendChild(paragraph('margin-why',
        'This page assumes ' + category.assumed + '; it does not test whether a ' +
        'votive, ritual, requiem or festive Mass is admitted.', category.locus));
    }

    for (const extra of branch.extras || []) {
      node.appendChild(paragraph('margin-why', extra.slot + ': ' + extra.what, extra.locus));
    }
    for (const remark of branch.remarks || []) {
      node.appendChild(paragraph('margin-why', remark.what, remark.locus));
    }
    return node;
  }

  /* ------------------------------------------------------------------------
   * The margin beside a proper: what is said under it
   * --------------------------------------------------------------------- */

  /**
   * The proper slots a subordinate oration is said in, and the rubric for each.
   *
   * The collect is the slot the derivation ranks; the rest are read from
   * `orations.tracked_by`, which is where the source states that the Secret and
   * the Postcommunion follow the collects in number and order. A rite that
   * tracks none — the postconciliar one, which does not commemorate at all —
   * therefore gets no subordinate anywhere, without this page knowing that.
   */
  function trackedSlots(branch, rubrics) {
    const series = branch.orations.all || branch.orations.low_mass || [];
    const slots = [];
    if (series.length && series[0].label) {
      slots.push({ slot: series[0].label, what: null, locus: null });
    }
    for (const row of (rubrics.orations || {}).tracked_by || []) {
      if (row && row.slot) slots.push(row);
    }
    return slots;
  }

  // Three is the absolute cap in both rites; a fourth would be a defect upstream,
  // so an unnamed position falls back to its number rather than inventing a word.
  const ORDINALS = { 2: 'Second', 3: 'Third' };

  function ordinalOf(position) {
    return ORDINALS[position] || ('Oration ' + position);
  }

  function subordinateItem(oration, slot, structure, sungDiffers) {
    const item = T.el('li');
    item.appendChild(T.el('span', 'margin-name',
      ordinalOf(oration.position) + ' ' + String(slot.slot).toLowerCase()));
    item.appendChild(T.el('span', 'margin-of', 'of ' + oration.of_name));
    if (oration.kind) item.appendChild(T.el('span', 'tag tag-commemorated', oration.kind));

    // Its words, where the corpus holds them.
    const of = (structure.masses || []).find((one) => one.key === oration.of);
    const matching = of && (of.propers || []).find((one) => one.name === slot.slot);
    if (matching && matching.incipit) {
      item.appendChild(T.el('p', 'margin-incipit', matching.incipit));
    } else if (of && !T.massIsUncompiled(of)) {
      item.appendChild(T.el('p', 'margin-why',
        'Its ' + String(slot.slot).toLowerCase() + ' is appointed and is not transcribed here.'));
    }

    item.appendChild(paragraph('margin-why', oration.why, oration.locus));
    if (oration.conclusion) {
      item.appendChild(T.el('p', 'margin-why', 'Said under ' + oration.conclusion + '.'));
    }
    if (oration.alternative) {
      item.appendChild(paragraph('margin-why',
        'The collect of ' + oration.alternative.of_name + ' may be said in its place: ' +
        oration.alternative.what, oration.alternative.locus));
    }
    if (sungDiffers) {
      item.appendChild(T.el('p', 'margin-why',
        'Not said at a sung Mass that is not the conventual Mass.'));
    }
    return item;
  }

  function properMargin(slot, subordinate, branch, structure) {
    const node = margin('What follows this');
    if (slot.what) node.appendChild(paragraph('margin-why', slot.what, slot.locus));
    const list = T.el('ul', 'margin-list');
    for (const oration of subordinate) {
      list.appendChild(
        subordinateItem(oration, slot, structure, Boolean(branch.sungDiffers)));
    }
    node.appendChild(list);
    return node;
  }

  /* ------------------------------------------------------------------------
   * The Mass
   * --------------------------------------------------------------------- */

  /** An annotated block: the text, and the margin beside it. */
  function annotated(body, note) {
    const node = T.el('div', 'annotated');
    const text = T.el('div', 'annotated-text');
    text.appendChild(body);
    node.appendChild(text);
    if (note) node.appendChild(note);
    return node;
  }

  /**
   * The year of a cycle-varying proper that this date actually falls in.
   *
   * The Sunday cycles are keyed A, B and C and the ferial ones I and II, which
   * is what the calendar layer states for the date. Narrowing to the one year
   * is the whole point of reaching a Mass by its date: the propers page cannot
   * know which year it is and shows all three.
   */
  function cycleKeyFor(proper, lectionary) {
    if (!lectionary) return null;
    const keys = T.cycleKeysOf(proper);
    if (keys.indexOf(lectionary.sunday) >= 0) return lectionary.sunday;
    if (keys.indexOf(lectionary.weekday) >= 0) return lectionary.weekday;
    return null;
  }

  function renderVerdictNotice(branch) {
    const blocking = (branch.absent || []).filter((one) => one.blocks_result);
    if (!branch.unsettled.length && !blocking.length && !branch.conditions.length) return null;

    const unsettled = branch.unsettled.length || blocking.length;
    const node = T.el('div', 'day-warning' + (unsettled ? ' is-unsettled' : ''));
    node.appendChild(T.el('h3', null, unsettled
      ? 'This day is not settled here'
      : 'This answer holds only conditionally'));
    node.appendChild(T.el('p', null, unsettled
      ? 'The rules as this repository holds them do not decide this date. What ' +
        'follows is shown so the state of the question is visible; it is not an ' +
        'answer and must not be read as one.'
      : 'One of the days below was constituted from its season because the calendar ' +
        'index carries no formulary for it, and a competing identity cannot be ruled ' +
        'out. If the condition fails, the answer changes.'));
    const list = T.el('ul');
    for (const row of branch.unsettled) {
      const item = T.el('li');
      item.appendChild(T.el('strong', null, row.what + ': '));
      item.appendChild(document.createTextNode(row.why));
      list.appendChild(item);
    }
    for (const row of blocking) {
      const item = T.el('li');
      item.appendChild(T.el('strong', null, row.what + ' is missing from this calendar index: '));
      item.appendChild(document.createTextNode(row.effect));
      withLocus(item, row.locus);
      list.appendChild(item);
    }
    for (const row of branch.conditions) {
      const item = T.el('li');
      item.appendChild(T.el('strong', null, row.what + ' — unless '));
      item.appendChild(document.createTextNode(row.unless));
      list.appendChild(item);
    }
    node.appendChild(list);
    return node;
  }

  function renderBranch(branch, rubrics, derived, structure, bible, fragments) {
    const section = T.el('section', 'branch');

    if (branch.option) {
      section.appendChild(T.el('h3', 'branch-option',
        'Where the option is “' + branch.option + '”'));
    }

    const warning = renderVerdictNotice(branch);
    if (warning) section.appendChild(warning);

    // The Mass's own heading carries the margin that says why it is this Mass.
    const head = T.el('div', 'mass-head');
    head.appendChild(T.el('h3', 'mass-name',
      branch.winner ? branch.winner.name : 'No day is settled here'));
    section.appendChild(annotated(head, massMargin(branch, rubrics, derived)));

    if (!branch.winner) return section;

    const series = branch.orations.all || branch.orations.low_mass || [];
    const subordinate = series.filter((one) => one.position > 1);
    const slots = trackedSlots(branch, rubrics);
    const slotFor = (name) => slots.find((one) => one.slot === name) || null;

    const mass = branch.winner.key
      ? (structure.masses || []).find((one) => one.key === branch.winner.key)
      : null;

    if (!mass) {
      const note = T.el('p', 'uncompiled');
      note.appendChild(T.el('span', 'uncompiled-mark', 'No formulary of its own'));
      note.appendChild(document.createTextNode(branch.winner.key
        ? 'The propers structure carries no mass keyed ' + branch.winner.key + '.'
        : 'It is constituted from its season and the calendar index carries no ' +
          'formulary of its own for it. Most ferias take the preceding Sunday’s ' +
          'Mass, which the index does not repeat.'));
      section.appendChild(note);
    } else if (T.massIsUncompiled(mass)) {
      // One line for the Mass, never one per slot, and never dressed as a
      // failure: nothing failed, and the Mass is not shorter than it is.
      section.appendChild(T.uncompiledNote(mass));
    } else {
      const lectionary = (derived.liturgicalYear && derived.liturgicalYear.lectionary) || null;
      const numbering = (structure && structure.numbering) || null;
      for (const proper of mass.propers || []) {
        if (T.isPlaceholder(proper)) continue;
        const body = T.renderProper(proper, bible, fragments, {
          numbering: numbering,
          orations: state.orations,
          cycle: cycleKeyFor(proper, lectionary)
        });
        const slot = slotFor(proper.name);
        const note = (slot && subordinate.length)
          ? properMargin(slot, subordinate, branch, structure)
          : null;
        section.appendChild(annotated(body, note));
      }
    }

    // A commemoration that found no slot to sit under is still said. It is put
    // once, after the Mass, rather than dropped.
    const anySlot = mass && !T.massIsUncompiled(mass) &&
      (mass.propers || []).some((one) => slotFor(one.name));
    if (subordinate.length && !anySlot) {
      const held = T.el('div', 'mass-head');
      held.appendChild(T.el('h4', 'mass-subheading',
        subordinate.length === 1 ? 'A commemoration is said with this Mass'
          : subordinate.length + ' commemorations are said with this Mass'));
      held.appendChild(T.el('p', 'row-meta',
        'This corpus carries no oration slot for the day’s own Mass, so the page ' +
        'cannot say which proper each follows. They are appointed, not absent.'));
      section.appendChild(
        annotated(held, properMargin(slots[0] || { slot: 'Collect' }, subordinate, branch, structure)));
    }
    return section;
  }

  /* ------------------------------------------------------------------------
   * Controls
   * --------------------------------------------------------------------- */

  function fillOrationsSelect() {
    T.fillSelect(orationsSelect, state.orationLanguages.map((entry) => ({
      value: entry.lang,
      label: T.orationLanguageLabel(entry),
      title: entry.lang
    })));
    orationsSelect.disabled = state.orationLanguages.length < 2;
    if (state.orations) orationsSelect.value = state.orations;
  }

  function syncControls() {
    dateInput.value = state.date || '';
    if (state.missalId) missalSelect.value = state.missalId;
    if (state.bibleId) bibleSelect.value = state.bibleId;
    if (state.orations) orationsSelect.value = state.orations;
  }

  function writeHash() {
    T.writeHash([
      ['date', state.date],
      ['missal', state.missalId],
      ['bible', state.bibleId],
      ['orations', state.orations === T.SOURCE_LANGUAGE ? null : state.orations]
    ]);
  }

  /* ------------------------------------------------------------------------
   * Putting it on screen
   * --------------------------------------------------------------------- */

  async function render(options) {
    if (!state.date || !state.missalId) return;
    const bible = currentBible();
    if (!bible) return;
    const token = T.beginRender();
    reading.setAttribute('aria-busy', 'true');

    const rubricsHeld = await once(rubricsCache, state.missalId,
      () => T.loadJSON(rubricsPath(state.missalId)));
    if (!T.isCurrentRender(token)) return;
    if (!rubricsHeld.ok) {
      T.fail('The rules for “' + state.missalId + '” could not be loaded: ' + rubricsHeld.message);
      return;
    }
    const rubrics = rubricsHeld.value;
    state.rubrics = rubrics;

    const civilYear = state.date.slice(0, 4);
    const yearHeld = await once(yearCache, state.missalId + '/' + civilYear,
      () => T.loadJSON(yearPath(state.missalId, civilYear)));
    if (!T.isCurrentRender(token)) return;
    if (!yearHeld.ok) {
      T.fail(
        'No calendar file for ' + civilYear + ' in “' + state.missalId + '”: ' +
        yearHeld.message + ' The calendar layer covers a stated span of years and ' +
        'this date is outside it.');
      return;
    }

    let derived;
    try {
      derived = Model.derive({ date: state.date, year: yearHeld.value, rubrics: rubrics });
    } catch (error) {
      T.fail('The derivation could not run: ' + (error.message || error));
      return;
    }
    state.derived = derived;

    // The propers are a megabyte; the day's name is not. Both are needed before
    // anything is drawn, but the fetch is cached per missal, so it is paid once.
    const propersHeld = await once(propersCache, state.missalId,
      () => T.loadJSON(propersPath(state.missalId)));
    if (!T.isCurrentRender(token)) return;
    if (!propersHeld.ok) {
      T.fail('The propers for “' + state.missalId + '” could not be loaded: ' +
        propersHeld.message);
      return;
    }
    const structure = propersHeld.value;
    if (state.structure !== structure) {
      state.structure = structure;
      state.orationLanguages = T.orationLanguagesOf(structure);
      if (!state.orationLanguages.some((entry) => entry.lang === state.orations)) {
        state.orations = T.SOURCE_LANGUAGE;
      }
      fillOrationsSelect();
    }

    // Every citation every branch's Mass needs, fetched in one pass.
    const wanted = [];
    for (const branch of derived.options) {
      const mass = branch.winner && branch.winner.key
        ? (structure.masses || []).find((one) => one.key === branch.winner.key)
        : null;
      if (mass) for (const citation of T.citationsOf(mass)) wanted.push(citation);
    }
    const held = await T.fetchFragments(bible, wanted);
    if (!T.isCurrentRender(token)) return;

    T.clear(reading);
    renderHead(derived, bible);
    for (const branch of derived.options) {
      reading.appendChild(
        renderBranch(branch, rubrics, derived, structure, bible, held.fragments));
    }
    openMargins(reading);
    reading.setAttribute('aria-busy', 'false');

    const first = derived.options[0];
    T.statusLine(
      longDate(derived.date, derived.weekday) + ', ' + derived.calendar + '. ' +
      (derived.options.length > 1 ? derived.options.length + ' territorial branches. ' : '') +
      (first.winner
        ? (first.settled ? first.winner.name + ' takes the day'
            : first.winner.name + ' stands highest, but this day is not settled here')
        : 'the day is not settled here') + '.');

    if (options && options.moveFocus) reading.focus();
  }

  /* ------------------------------------------------------------------------
   * Selection
   * --------------------------------------------------------------------- */

  function select(date, missalId, options) {
    if (date) state.date = date;
    if (missalId) state.missalId = missalId;
    syncControls();
    writeHash();
    render(options);
  }

  function step_(delta, options) {
    if (!state.date) return;
    select(Model.shift(state.date, delta), null, options);
  }

  /* ------------------------------------------------------------------------
   * Start-up
   * --------------------------------------------------------------------- */

  T.setInlineNotice(
    'No data root could be reached at "' + T.dataRoot + '", so this page has ' +
    'nothing to derive from. Serve the pages over HTTP with the corpus at that ' +
    'path, or try ?data=fixture.'
  );

  function validDate(value) {
    return /^\d{4}-\d{2}-\d{2}$/.test(value || '') && !Number.isNaN(Date.parse(value + 'T00:00:00Z'));
  }

  async function start() {
    const loaded = await T.loadBibles();
    if (!loaded.ok) {
      T.fail(loaded.message);
      return;
    }
    state.bibles = loaded.bibles;
    T.fillBibleSelect(bibleSelect, state.bibles);

    let missals;
    try {
      missals = await discoverMissals();
    } catch (error) {
      T.fail(
        'No rules layer could be found at "' + T.dataPath(RUBRICS_INDEX) + '": ' +
        (error.message || error) + ' Run `tools/tpt calendar-rubrics structure` to ' +
        'write it, or serve the corpus at ?data=.');
      return;
    }
    if (!missals.length) {
      T.fail('The rules layer offers no missal.');
      return;
    }
    state.missals = missals;
    T.fillSelect(missalSelect, missals.map((one) => ({
      value: one.id,
      label: one.label,
      title: one.edition || one.code || one.id
    })));

    const hash = T.readHash();
    state.orations = hash.get('orations') || T.SOURCE_LANGUAGE;
    const wantedBible = hash.get('bible');
    state.bibleId = state.bibles.some((one) => one.id === wantedBible)
      ? wantedBible
      : state.bibles[0].id;
    state.date = validDate(hash.get('date')) ? hash.get('date') : todayISO();
    const wantedMissal = hash.get('missal');
    state.missalId = missals.some((one) => one.id === wantedMissal) ? wantedMissal : missals[0].id;

    syncControls();
    writeHash();
    await render({ moveFocus: false });
  }

  /* ------------------------------------------------------------------------
   * Events
   * --------------------------------------------------------------------- */

  dateInput.addEventListener('change', () => {
    if (validDate(dateInput.value)) select(dateInput.value, null, { moveFocus: false });
  });

  missalSelect.addEventListener('change', () => {
    select(null, missalSelect.value, { moveFocus: false });
  });

  bibleSelect.addEventListener('change', () => {
    state.bibleId = bibleSelect.value;
    select(null, null, { moveFocus: false });
  });

  orationsSelect.addEventListener('change', () => {
    state.orations = orationsSelect.value;
    select(null, null, { moveFocus: false });
  });

  prevButton.addEventListener('click', () => step_(-1, { moveFocus: true }));
  nextButton.addEventListener('click', () => step_(1, { moveFocus: true }));
  todayButton.addEventListener('click', () => select(todayISO(), null, { moveFocus: true }));

  controls.addEventListener('submit', (event) => event.preventDefault());

  T.onArrowStep((delta) => step_(delta, { moveFocus: false }));

  // A margin is a margin only while there is room for one. Re-deciding on the
  // breakpoint rather than on every resize keeps a reader's own disclosure
  // choices intact while they are reading at one width.
  if (window.matchMedia) {
    const wide = window.matchMedia(WIDE);
    const listen = wide.addEventListener
      ? wide.addEventListener.bind(wide, 'change')
      : wide.addListener.bind(wide);
    listen(() => openMargins(reading));
  }

  T.onHashChange((hash) => {
    const wantedMissal = hash.get('missal');
    if (state.missals.some((one) => one.id === wantedMissal)) state.missalId = wantedMissal;
    const wantedBible = hash.get('bible');
    if (state.bibles.some((one) => one.id === wantedBible)) state.bibleId = wantedBible;
    const wantedOrations = hash.get('orations') || T.SOURCE_LANGUAGE;
    if (state.orationLanguages.some((entry) => entry.lang === wantedOrations)) {
      state.orations = wantedOrations;
    }
    const wantedDate = hash.get('date');
    select(validDate(wantedDate) ? wantedDate : state.date, null, { moveFocus: false });
  });

  start();
}());
