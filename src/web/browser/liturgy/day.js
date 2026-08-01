/* ===========================================================================
 * The assembly page — a date, a missal, and the argument between them
 * ===========================================================================
 *
 * This file renders. It decides nothing. Every rank, disposition, ceiling and
 * rubric number below arrives from `assembly-model.js`, which reads them out of
 * the rubrics file the repository tracks; the same model is run under node by
 * `calendar-rubrics check` against the solved cases, so what a reader sees here
 * is what the check holds.
 *
 * WHAT IT FETCHES, AND WHY IT IS SO LITTLE
 *
 *   structure/rubrics/index.json      which missals have rules   ~1 KB
 *   structure/rubrics/<missal>.json   the rules themselves       ~45-75 KB
 *   structure/calendar/<missal>/<year>.json   the day's candidates   ~30 KB
 *
 * Three small files, and the argument is complete. The formulary is a fourth
 * fetch, deferred: `structure/propers/<missal>.json` is most of a megabyte and
 * the reasoning does not need it, so the five decisions render first and the
 * propers are appended when they land. A reader who never scrolls that far
 * never pays for them.
 *
 * Nothing is stored per day. An assembly for every date of every year in both
 * missals would be some seventy-four thousand objects, and correcting one
 * rubric would invalidate all of them at once.
 *
 *   ?data=<root>        where the corpus lives (default ../browse)
 *   #date=<YYYY-MM-DD>&missal=<id>    the current selection; shareable
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

  const state = {
    missals: [],
    missalId: null,
    rubrics: null,
    date: null,
    derived: null
  };

  const dateInput = document.getElementById('date-input');
  const missalSelect = document.getElementById('missal-select');
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
   * Discovery
   * --------------------------------------------------------------------- */

  async function discoverMissals() {
    const file = await T.loadJSON(RUBRICS_INDEX);
    const rows = (file && file.calendars) || [];
    // The short name for the control and the edition for the hover, the same
    // two names the propers page shows and out of the same calendar source, so
    // a reader moving between the pages is choosing between the same two words.
    // The full identification is not lost: the derivation prints it as the
    // first fact of every day.
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

  /* ------------------------------------------------------------------------
   * Rendering: the head
   * --------------------------------------------------------------------- */

  function renderHead(derived) {
    const head = T.el('div', 'day-head');
    head.appendChild(T.el('h2', null, longDate(derived.date, derived.weekday)));

    const facts = T.el('ul', 'day-facts');
    function fact(label, value) {
      if (value === null || value === undefined || value === '') return;
      const item = T.el('li');
      item.appendChild(T.el('b', null, label));
      item.appendChild(document.createTextNode(String(value)));
      facts.appendChild(item);
    }
    fact('Missal', derived.edition);
    if (derived.liturgicalYear) fact('Liturgical year', derived.liturgicalYear.label);
    fact('Season', derived.season ? T.titleCase(derived.season) : 'not stated for this date');
    if (derived.week) fact('Week', derived.week);
    if (derived.liturgicalYear && derived.liturgicalYear.lectionary) {
      const cycle = derived.liturgicalYear.lectionary;
      fact('Lectionary', 'Sunday ' + cycle.sunday + ', weekday ' + cycle.weekday);
    }
    head.appendChild(facts);

    // A year the calendar computation itself refused to resolve is a fact about
    // this date's whole year, and it belongs above the argument rather than
    // inside it.
    const unresolved = (derived.liturgicalYear && derived.liturgicalYear.unresolved) || [];
    for (const row of unresolved) {
      head.appendChild(
        paragraph('row-meta', 'Unresolved this year: ' + row.what + ' — ' + row.why)
      );
    }
    return head;
  }

  /* ------------------------------------------------------------------------
   * Rendering: the verdict
   *
   * Three states, and they must never look alike. A conditional result is not a
   * settled one with a note attached: it is an answer that may be wrong, and
   * the condition is what would make it wrong.
   * --------------------------------------------------------------------- */

  function renderVerdict(branch, rubrics) {
    const blocking = (branch.absent || []).filter((one) => one.blocks_result);
    const bad = branch.unsettled.length || blocking.length;
    const kind = bad ? 'unsettled' : (branch.conditions.length ? 'conditional' : 'settled');
    const node = T.el('div', 'verdict verdict-' + kind);

    if (kind === 'settled') {
      node.appendChild(T.el('h5', null, 'The rules reach an answer'));
      node.appendChild(T.el('p', null,
        'Every step below follows from a numbered rubric this repository has ' +
        'transcribed and checked. It is still not an Ordo: a particular calendar ' +
        'you have not told this page about can change the answer.'));
      return node;
    }

    if (kind === 'conditional') {
      node.appendChild(T.el('h5', null, 'This answer holds only conditionally'));
      node.appendChild(T.el('p', null,
        'One of the days below was constituted from its season because the ' +
        'calendar index carries no formulary for it, and this repository cannot ' +
        'rule out a competing identity for it. If the condition fails, the answer ' +
        'changes.'));
      const list = T.el('ul');
      for (const row of branch.conditions) {
        const item = T.el('li');
        item.appendChild(T.el('strong', null, row.what + ' — unless '));
        item.appendChild(document.createTextNode(row.unless));
        list.appendChild(item);
      }
      node.appendChild(list);
      return node;
    }

    node.appendChild(T.el('h5', null, 'This day is not settled here'));
    node.appendChild(T.el('p', null,
      'The rules as this repository holds them do not decide this date. What ' +
      'follows is shown so the state of the question is visible; it is not an ' +
      'answer, and it must not be read as one.'));
    const list = T.el('ul');
    for (const row of branch.unsettled) {
      const item = T.el('li');
      item.appendChild(T.el('strong', null, row.what + ': '));
      item.appendChild(document.createTextNode(row.why));
      for (const also of row.seeAlso || []) {
        const note = T.el('div', 'row-meta', also.why || '');
        withLocus(note, also.locus);
        item.appendChild(note);
      }
      list.appendChild(item);
    }
    for (const row of blocking) {
      const item = T.el('li');
      item.appendChild(T.el('strong', null, row.what + ' is missing from this calendar index: '));
      item.appendChild(document.createTextNode(row.effect));
      withLocus(item, row.locus);
      list.appendChild(item);
    }
    node.appendChild(list);
    return node;
  }

  /* ------------------------------------------------------------------------
   * Rendering: the five steps
   * --------------------------------------------------------------------- */

  function step(number, title, lede) {
    const section = T.el('section', 'step');
    const head = T.el('div', 'step-head');
    head.appendChild(T.el('span', 'step-number', String(number)));
    head.appendChild(T.el('h4', null, title));
    section.appendChild(head);
    if (lede) section.appendChild(T.el('p', 'step-lede', lede));
    const body = T.el('div', 'step-body');
    section.appendChild(body);
    return { section: section, body: body };
  }

  const SOURCE_WORDS = {
    index: 'in the calendar',
    implied: 'constituted from the season',
    arrived: 'transferred here'
  };

  function rowItem(candidate, rubrics, options) {
    const held = options || {};
    const item = T.el('li', 'row-item' +
      (held.winner ? ' is-winner' : '') +
      (candidate.certain === false ? ' is-uncertain' : ''));

    const title = T.el('div', 'row-title');
    title.appendChild(T.el('span', 'name', candidate.name));
    if (candidate.row != null) {
      title.appendChild(T.el('span', 'row-place',
        Model.placeWord(rubrics) + ' ' + candidate.row +
        (candidate.class ? ' · class ' + candidate.class : '')));
    } else {
      title.appendChild(T.el('span', 'row-place', 'no row of the table'));
    }
    title.appendChild(T.el('span', 'tag tag-source', SOURCE_WORDS[candidate.source] || candidate.source));
    item.appendChild(title);

    if (candidate.rowLabel) item.appendChild(T.el('p', 'row-why', candidate.rowLabel));
    item.appendChild(paragraph('row-meta', candidate.why, candidate.locus));

    // How the date came to carry it at all — the calendar layer's own rule.
    if (candidate.rule) {
      item.appendChild(T.el('p', 'row-meta',
        'Placed here because: ' + candidate.rule.rule + ' (' + candidate.rule.origin + ')'));
    }
    if (candidate.arrivedFrom && candidate.seat) {
      const note = T.el('p', 'row-meta',
        'Moved here from ' + candidate.arrivedFrom + ', as to its own proper seat: ' +
        candidate.seat.destination);
      withLocus(note, candidate.seat.locus);
      item.appendChild(note);
      if (candidate.seat.latin) item.appendChild(T.el('p', 'latin', candidate.seat.latin));
    }
    if (candidate.office) {
      const note = T.el('p', 'row-meta', candidate.office.why);
      withLocus(note, candidate.office.locus);
      item.appendChild(note);
    }
    if (candidate.note) item.appendChild(T.el('p', 'row-meta', candidate.note));
    if (candidate.caveat) {
      item.appendChild(T.el('p', 'row-meta', 'Not certain: unless ' + candidate.caveat));
    }
    if (candidate.territorial) {
      item.appendChild(T.el('p', 'row-meta',
        'Holds only where the competent authority has taken the option “' +
        candidate.territorial + '”.'));
    }
    if ((candidate.alsoInscribedAs || []).length) {
      item.appendChild(T.el('p', 'row-meta',
        'The index inscribes this celebration twice, also as ' +
        candidate.alsoInscribedAs.join(', ') + '; they are one day, not two.'));
    }
    if (!candidate.competes && candidate.row == null) {
      item.appendChild(T.el('p', 'row-meta',
        'It occupies no row, so it never takes the day.'));
    }
    return item;
  }

  function renderStepOne(branch, rubrics) {
    const held = step(1, 'The day: what falls on this date',
      'Write down every Sunday, feria, vigil, feast and octave day that lands here, ' +
      'in every calendar that binds you. The list below is the universal calendar ' +
      'only; a particular calendar adds to it and can outrank everything on it.');
    const list = T.el('ul', 'rows');
    for (const candidate of branch.candidates) {
      list.appendChild(rowItem(candidate, rubrics, { winner: branch.winner && branch.winner.id === candidate.id }));
    }
    if (!branch.candidates.length) {
      list.appendChild(T.el('li', 'row-item',
        'This calendar index carries no mass for this date, and no rule in the ' +
        'rubrics source constitutes a day for it.'));
    }
    held.body.appendChild(list);

    for (const row of branch.folded || []) {
      held.body.appendChild(T.el('p', 'row-meta',
        'The index also carries ' + row.key + ' here; it is the same celebration as ' +
        row.into + ' (' + row.what + ') and is counted once.'));
    }
    return held.section;
  }

  function renderStepTwo(branch, rubrics) {
    const table = rubrics.precedence || {};
    const held = step(2, 'Precedence: which of them takes the day',
      'Apply the table, and nothing else.');

    const rule = T.el('div', 'row-item');
    rule.appendChild(withLocus(T.el('span', 'row-place', 'The governing sentence'), table.locus));
    if (table.latin) rule.appendChild(T.el('p', 'latin', table.latin));
    if (table.gloss) rule.appendChild(T.el('p', 'row-why', table.gloss));
    held.body.appendChild(rule);

    if (branch.winner) {
      const winner = T.el('p', 'row-why');
      winner.appendChild(T.el('strong', null, branch.winner.name));
      winner.appendChild(document.createTextNode(
        (branch.winner.optional ? ' stands highest' : ' takes the day') +
        '. It stands at ' + Model.placeWord(rubrics) + ' ' +
        branch.winner.row + ' — ' + (branch.winner.rowLabel || '') + ' — and every ' +
        'other candidate stands lower.'));
      held.body.appendChild(winner);
      // Outranking the day is not the same as being obligatory.
      if (branch.winner.optional) {
        const note = T.el('p', 'row-why');
        note.appendChild(T.el('strong', null, 'It is optional. '));
        note.appendChild(document.createTextNode(
          branch.winner.why + '. The day below it may be kept instead, and where ' +
          'several optional memorials fall together only one of them may be kept.'));
        withLocus(note, branch.winner.locus);
        held.body.appendChild(note);
      }
    } else if (branch.choice) {
      const node = T.el('p', 'row-why');
      node.appendChild(T.el('strong', null, 'The choice belongs to the celebrant. '));
      node.appendChild(document.createTextNode(
        branch.choice.what + ' — ' +
        branch.choice.among.map((one) => one.name).join('; ') + '.'));
      held.body.appendChild(node);
    } else {
      held.body.appendChild(T.el('p', 'row-why',
        'No winner is named, for the reason stated above. Nothing below should be ' +
        'read as the day’s assembly.'));
    }

    // Occurrence and concurrence are different questions, and the confusion is
    // common enough that the page says so at the step rather than in a footnote.
    const occurrence = table.occurrence || null;
    const concurrence = table.concurrence || null;
    if (occurrence) {
      held.body.appendChild(paragraph('row-meta', occurrence.gloss, occurrence.locus));
    }
    if (concurrence) {
      held.body.appendChild(paragraph('row-meta', concurrence.gloss, concurrence.locus));
    }
    return held.section;
  }

  const DISPOSITION_WORDS = {
    commemorated: 'commemorated',
    transferred: 'transferred',
    omitted: 'omitted',
    reduced: 'reduced'
  };

  function renderStepThree(branch, rubrics) {
    const impediment = rubrics.impediment || {};
    const held = step(3, 'The impeded day: what becomes of the ones that lost',
      'The outcome is decided by its own rule, never inferred from the margin of ' +
      'defeat. A first-class feast beaten by a hair is transferred; a feast one row ' +
      'lower may be commemorated, or simply lost for the year.');

    if (impediment.outcomes) {
      held.body.appendChild(paragraph('row-meta',
        'The only outcomes are ' + impediment.outcomes.join(', ') + '.',
        impediment.outcomes_locus));
    }

    if (!branch.losers.length) {
      held.body.appendChild(T.el('p', 'row-why', 'Nothing else stood on this date.'));
      return held.section;
    }

    const list = T.el('ul', 'rows');
    for (const loser of branch.losers) {
      const item = T.el('li', 'row-item');
      const title = T.el('div', 'row-title');
      title.appendChild(T.el('span', 'name', loser.name));
      title.appendChild(T.el('span', 'tag tag-' + loser.disposition,
        DISPOSITION_WORDS[loser.disposition] || loser.disposition));
      if (loser.kind) title.appendChild(T.el('span', 'row-place', loser.kind));
      item.appendChild(title);
      item.appendChild(paragraph('row-why', loser.why, loser.locus));
      if (loser.latin) item.appendChild(T.el('p', 'latin', loser.latin));
      if (loser.defeatedBy) {
        item.appendChild(paragraph('row-meta', loser.defeatedBy.why, loser.defeatedBy.locus));
      }
      if (loser.destination) {
        item.appendChild(T.el('p', 'row-meta',
          'It is kept on ' + longDate(loser.destination, Model.weekdayOf(loser.destination)) + '.'));
      }
      if (loser.destinationNotComputed) {
        item.appendChild(T.el('p', 'row-meta',
          'This page does not compute where it goes. ' + loser.destinationNotComputed));
      }
      list.appendChild(item);
    }
    held.body.appendChild(list);

    const sunday = impediment.sunday_not_resumed;
    if (sunday && branch.losers.some((one) => one.name && /sunday/i.test(one.name))) {
      held.body.appendChild(paragraph('row-meta', sunday.gloss, sunday.locus));
    }
    return held.section;
  }

  function renderStepFour(rubrics) {
    const category = rubrics.mass_category || {};
    const held = step(4, 'The Mass category: which Mass may be said',
      'A day’s rank tells you only that a category is not excluded. What admits ' +
      'one is a separate fact, and permission is never inferred from rank.');
    held.body.appendChild(paragraph('row-why',
      'This page assumes ' + (category.assumed || 'the Mass of the day') + '.',
      category.locus));
    if (category.latin) held.body.appendChild(T.el('p', 'latin', category.latin));
    if (category.warning) held.body.appendChild(T.el('p', 'row-meta', category.warning));

    const list = T.el('ul', 'rows');
    for (const row of category.not_tested || []) {
      const item = T.el('li', 'row-item');
      const title = T.el('div', 'row-title');
      title.appendChild(T.el('span', 'name', row.category));
      title.appendChild(T.el('span', 'tag tag-omitted', 'not tested here'));
      item.appendChild(title);
      item.appendChild(paragraph('row-meta', 'Its conditions are stated at', row.locus));
      list.appendChild(item);
    }
    if (list.childNodes.length) held.body.appendChild(list);
    return held.section;
  }

  function renderStepFive(branch, rubrics) {
    const orations = rubrics.orations || {};
    const commemorates = !(rubrics.commemoration && rubrics.commemoration.exists === false);
    const held = step(5, 'The Mass that is said',
      commemorates
        ? 'The day’s own propers, and under each oration the days that lost, which ' +
          'survive as the second and third collects.'
        : 'One collect, whatever else fell on the day. This rite does not commemorate, ' +
          'and that is the sharpest difference between the two books.');

    // The orations used to be listed twice here, as a rank-and-reason table, and
    // then a third time in the formulary below with their words. One tree now
    // carries all of it: the slot, the words, the rank and the rubric together,
    // which is the only arrangement in which a reader can see what is said and
    // why in the same glance. Where the sung Mass differs, the affected orations
    // say so on themselves.

    if (commemorates) {
      const order = (rubrics.commemoration && rubrics.commemoration.order) || null;
      if (order) held.body.appendChild(paragraph('row-meta', order.gloss, order.locus));
      const cap = orations.absolute_cap;
      if (cap) held.body.appendChild(paragraph('row-meta', cap.gloss, cap.locus));
      // `orations.tracked_by` is not restated here: the formulary below prints
      // each of those rules at the slot it governs, which is where it can be
      // checked against what is actually said.
      const abolished = (rubrics.commemoration || {}).abolished;
      if (abolished) held.body.appendChild(paragraph('row-meta', abolished.what, abolished.locus));
    } else {
      const surviving = (rubrics.commemoration || {}).surviving_qualification;
      if (surviving) held.body.appendChild(paragraph('row-meta', surviving.what, surviving.locus));
      const gap = orations.general_rule_not_collated;
      if (gap) held.body.appendChild(paragraph('row-meta', gap.what, gap.locus));
    }

    for (const extra of branch.extras || []) {
      held.body.appendChild(paragraph('row-meta', extra.slot + ': ' + extra.what, extra.locus));
    }
    for (const remark of branch.remarks || []) {
      held.body.appendChild(paragraph('row-meta', remark.what, remark.locus));
    }

    // The formulary lands here once the propers structure has been fetched.
    const formulary = T.el('div', 'formulary');
    formulary.appendChild(T.el('p', 'row-meta', 'Fetching the formulary…'));
    held.body.appendChild(formulary);
    held.section.dataset.formulary = branch.option === null ? '' : branch.option;
    return { section: held.section, formulary: formulary };
  }

  /* ------------------------------------------------------------------------
   * The formulary, fetched after the argument is on screen
   * --------------------------------------------------------------------- */

  /**
   * The year of a cycle-varying proper that this date actually falls in.
   *
   * A structure file keeps the years apart under `cycles`, each one an object
   * carrying that year's citations and, where the year is composed rather than
   * read, its own words. The Sunday cycles are keyed A, B and C and the ferial
   * ones I and II, which is what the calendar layer states for the date; a key
   * the lectionary does not name is not this date's, and returning nothing is
   * right — this page shows one day, not three.
   */
  function cycleFor(proper, lectionary) {
    const cycles = (proper && proper.cycles) || {};
    const keys = Object.keys(cycles);
    if (!keys.length || !lectionary) return null;
    const wanted = keys.indexOf(lectionary.sunday) >= 0
      ? lectionary.sunday
      : (keys.indexOf(lectionary.weekday) >= 0 ? lectionary.weekday : null);
    if (!wanted) return null;
    const held = cycles[wanted] || {};
    const refs = (held.citations || []).map((one) => one.ref).filter(Boolean);
    const what = refs.length ? refs.join('; ') : (held.text ? 'composed text' : null);
    if (!what) return null;
    return { label: /^[A-C]$/.test(wanted) ? 'Year ' + wanted : 'Cycle ' + wanted, what: what };
  }

  /**
   * The proper slots a subordinate oration is said in, and the rubric for each.
   *
   * The collect is the slot the derivation ranks; the rest are read from
   * `orations.tracked_by`, which is where the source states that the Secret and
   * the Postcommunion follow the collects in number and order. Naming them here
   * instead would be a list of slots standing beside the rule that governs
   * them, free to disagree with it — and a rite that added a fourth tracked
   * slot, or a rite that tracks none, would not reach this page.
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

  // Position in a series of orations, said the way the rubrics say it. Three is
  // the absolute cap in both rites, and a fourth would be a defect upstream, so
  // an unnamed position falls back to its number rather than inventing a word.
  const ORDINALS = { 2: 'Second', 3: 'Third' };

  function ordinalOf(position) {
    return ORDINALS[position] || ('Oration ' + position);
  }

  /** Is this mass a day the calendar keeps and the corpus has not compiled? */
  function isUncompiled(mass) {
    const propers = (mass && mass.propers) || [];
    return propers.length > 0 && propers.every((one) => one.name === 'Placeholder');
  }

  /** What a proper says of itself: its incipit, its reference, or its absence. */
  function properDetail(proper, lectionary) {
    const detail = T.el('span', 'formulary-detail');
    const refs = (proper.citations || []).map((one) => one.ref).filter(Boolean);
    if (proper.incipit) detail.appendChild(T.el('em', null, proper.incipit));
    if (refs.length) {
      if (proper.incipit) detail.appendChild(document.createTextNode(' · '));
      detail.appendChild(document.createTextNode(refs.join('; ')));
    }
    // A proper that varies with the lectionary carries its reading under the
    // year rather than on the proper, and this page knows which year the date
    // falls in. Reading only the proper's own citations printed "no citation or
    // text is compiled here" against five readings the corpus holds.
    const cycle = cycleFor(proper, lectionary);
    if (cycle) {
      if (refs.length || proper.incipit) detail.appendChild(document.createTextNode(' · '));
      detail.appendChild(T.el('span', 'formulary-cycle', cycle.label));
      detail.appendChild(document.createTextNode(' ' + cycle.what));
    }
    if (!proper.incipit && !refs.length && !cycle) {
      detail.appendChild(document.createTextNode(
        proper.text ? 'composed text' : 'no citation or text is compiled here'));
    }
    return detail;
  }

  /**
   * One subordinate oration, under the slot it is said in.
   *
   * Everything about it is derived: which celebration it is of, what kind of
   * commemoration, the rubric that admits it, and the conclusion it takes, all
   * from the oration series the model built out of the tracked precedence
   * tables. The only thing looked up here is its words, from the propers
   * structure, and their absence is stated rather than passed over.
   */
  function subordinateItem(oration, slot, structure, sungDiffers) {
    const item = T.el('li', 'formulary-item is-subordinate');

    const head = T.el('div', 'subordinate-head');
    head.appendChild(T.el('span', 'formulary-slot',
      ordinalOf(oration.position) + ' ' + String(slot.slot).toLowerCase()));
    head.appendChild(T.el('span', 'subordinate-of', 'of ' + oration.of_name));
    if (oration.kind) head.appendChild(T.el('span', 'tag tag-commemorated', oration.kind));
    item.appendChild(head);

    // Its words, where the corpus holds them. A commemoration whose own
    // formulary is a placeholder is not a broken row: the day is kept and its
    // three orations are appointed; this repository has not transcribed them.
    const of = (structure.masses || []).find((one) => one.key === oration.of);
    const matching = of && (of.propers || []).find((one) => one.name === slot.slot);
    const words = T.el('p', 'subordinate-words');
    if (matching && (matching.incipit || matching.text)) {
      words.appendChild(T.el('em', null, matching.incipit || 'composed text'));
    } else if (of) {
      words.appendChild(document.createTextNode(
        'Its ' + String(slot.slot).toLowerCase() + ' is appointed and is not compiled here.'));
    } else {
      words.appendChild(document.createTextNode(
        'It is constituted from its season and the calendar index carries no ' +
        'formulary of its own, so this oration is taken from the season’s Mass.'));
    }
    item.appendChild(words);

    // Why it is said at all, and under what conclusion.
    item.appendChild(paragraph('row-meta', oration.why, oration.locus));
    if (oration.conclusion) {
      item.appendChild(T.el('p', 'row-meta', 'Said under ' + oration.conclusion + '.'));
    }
    if (oration.alternative) {
      const alt = T.el('p', 'row-meta',
        'The collect of ' + oration.alternative.of_name + ' may be said in its place: ' +
        oration.alternative.what);
      withLocus(alt, oration.alternative.locus);
      item.appendChild(alt);
    }
    if (sungDiffers) {
      item.appendChild(T.el('p', 'row-meta',
        'Not said at a sung Mass that is not the conventual Mass.'));
    }
    return item;
  }

  /** The days that stood here and are not said, with the rule that disposed of them. */
  function renderNotSaid(node, branch) {
    const silent = (branch.losers || []).filter((one) => one.disposition !== 'commemorated');
    if (!silent.length) return;
    node.appendChild(T.el('h5', 'formulary-heading', 'What stood here and is not said'));
    const list = T.el('ul', 'formulary-list');
    for (const loser of silent) {
      const item = T.el('li', 'formulary-item is-silent');
      const head = T.el('div', 'subordinate-head');
      head.appendChild(T.el('span', 'subordinate-of', loser.name));
      head.appendChild(T.el('span', 'tag tag-' + loser.disposition,
        DISPOSITION_WORDS[loser.disposition] || loser.disposition));
      item.appendChild(head);
      item.appendChild(paragraph('row-meta', loser.why, loser.locus));
      if (loser.destination) {
        item.appendChild(T.el('p', 'row-meta',
          'It is kept on ' + longDate(loser.destination, Model.weekdayOf(loser.destination)) + '.'));
      }
      list.appendChild(item);
    }
    node.appendChild(list);
  }

  function renderFormulary(node, branch, structure, rubrics, lectionary) {
    T.clear(node);
    if (!branch.winner) {
      node.appendChild(T.el('p', 'row-meta',
        'No formulary is shown: no day was settled above.'));
      return;
    }

    // Why these texts and not others, said once, at the head of them, out of the
    // same ranking that chose them.
    const why = T.el('p', 'formulary-why');
    why.appendChild(T.el('strong', null, branch.winner.name));
    why.appendChild(document.createTextNode(
      branch.winner.row != null
        ? ' took the day at ' + Model.placeWord(rubrics) + ' ' + branch.winner.row +
          (branch.winner.rowLabel ? ' — ' + branch.winner.rowLabel : '') + '.'
        : ' takes the day.'));
    withLocus(why, branch.winner.locus);
    node.appendChild(why);

    const series = branch.orations.all || branch.orations.low_mass || [];
    const subordinate = series.filter((one) => one.position > 1);
    const slots = trackedSlots(branch, rubrics);
    const slotFor = (name) => slots.find((one) => one.slot === name) || null;

    /**
     * The commemorations, where there is no list of the day's own propers for
     * them to sit under.
     *
     * They are still said. A page that showed nothing here because the day's own
     * Mass is not written down would be reporting that the day carries one
     * oration when the rubrics give it three, which is the same class of wrong
     * answer as omitting a proper.
     */
    function renderOrphans(into) {
      if (!subordinate.length) return;
      into.appendChild(T.el('p', 'row-meta',
        'The ' + (subordinate.length === 1 ? 'commemoration' : 'commemorations') +
        ' below ' + (subordinate.length === 1 ? 'is' : 'are') + ' still appointed, and ' +
        (subordinate.length === 1 ? 'follows' : 'follow') + ' each of the day’s own orations.'));
      const orphans = T.el('ul', 'formulary-list subordinates');
      for (const oration of subordinate) {
        orphans.appendChild(
          subordinateItem(oration, slots[0] || { slot: 'Collect' }, structure, false));
      }
      into.appendChild(orphans);
    }

    if (!branch.winner.key) {
      node.appendChild(T.el('p', 'row-meta',
        'It is constituted from its season and this calendar index carries no ' +
        'formulary of its own for it. Most ferias take the preceding Sunday’s ' +
        'Mass, which the index does not repeat.'));
      renderOrphans(node);
      renderNotSaid(node, branch);
      return;
    }

    const mass = (structure.masses || []).find((one) => one.key === branch.winner.key);
    if (!mass) {
      node.appendChild(T.el('p', 'row-meta',
        'The propers structure carries no mass keyed ' + branch.winner.key + '.'));
      renderOrphans(node);
      renderNotSaid(node, branch);
      return;
    }

    // A day the calendar keeps whose formulary this repository has not
    // transcribed. It is stated as the one fact it is, rather than drawn as a
    // list of empty slots: a reader must not count the parts of this Mass off a
    // page that invented them, and must not read the absence as a page that
    // failed to load.
    if (isUncompiled(mass)) {
      const held = T.el('div', 'formulary-uncompiled');
      held.appendChild(T.el('h5', null, 'The formulary is not compiled here'));
      held.appendChild(T.el('p', null,
        'This missal keeps the day and appoints its Mass; this repository has not ' +
        'yet transcribed the propers of it. Nothing has failed to load and nothing ' +
        'is hidden — the texts are simply not held yet, so the page will not say ' +
        'how many parts this Mass has or what they are.'));
      node.appendChild(held);
      renderOrphans(node);
      renderNotSaid(node, branch);
      return;
    }

    node.appendChild(T.el('h5', 'formulary-heading',
      'The formulary, in the order the missal appoints it'));

    const list = T.el('ul', 'formulary-list');
    let placed = false;

    for (const proper of mass.propers || []) {
      const item = T.el('li', 'formulary-item');
      item.appendChild(T.el('span', 'formulary-slot', proper.name || 'Proper'));
      item.appendChild(properDetail(proper, lectionary));
      list.appendChild(item);

      // What is said under this proper, and why. A slot that tracks the collects
      // carries the whole subordinate series, so the reader sees the Mass that
      // is actually said rather than the day's own texts alone.
      const slot = slotFor(proper.name);
      if (!slot || !subordinate.length) continue;
      placed = true;
      const nested = T.el('ul', 'subordinates');
      if (slot.what) {
        nested.appendChild(paragraph('row-meta subordinates-rule', slot.what, slot.locus));
      }
      for (const oration of subordinate) {
        nested.appendChild(
          subordinateItem(oration, slot, structure, Boolean(branch.sungDiffers)));
      }
      item.appendChild(nested);
    }
    node.appendChild(list);

    // A commemoration with nowhere to sit must be said, not dropped. Many of this
    // corpus's seasonal ferias carry only their scripture-bearing propers, so the
    // slot a second collect would follow is not written down — a gap in the
    // corpus and not a fact about the Mass. The orations are still shown; only
    // their place in the list is unknown.
    if (subordinate.length && !placed) {
      node.appendChild(T.el('p', 'row-meta',
        'This corpus carries no oration slot for the day’s own Mass, so the page ' +
        'cannot say which proper each of these follows. They are appointed, not absent.'));
      renderOrphans(node);
    }

    // Why this many, whether or not it turned anything away.
    const ceiling = (branch.ceilings || {}).low_mass;
    if (ceiling) {
      node.appendChild(paragraph('row-meta', ceiling.what ||
        ('This day admits ' + ceiling.max + ' commemoration' + (ceiling.max === 1 ? '' : 's') +
         (ceiling.privileged_only ? ', and only a privileged one.' : '.')), ceiling.locus));
    }

    renderNotSaid(node, branch);
    node.appendChild(T.el('p', 'row-meta',
      'The texts themselves, with their translations, are on the propers page.'));
  }

  /* ------------------------------------------------------------------------
   * Rendering: one branch, and the closing apparatus
   * --------------------------------------------------------------------- */

  function renderBranch(branch, rubrics, derived) {
    const node = T.el('section', 'branch');
    const head = T.el('div', 'branch-head');
    if (branch.option) {
      head.appendChild(T.el('h3', null, 'Where the option is “' + branch.option + '”'));
      const family = derived.territorial || {};
      const note = (family && family.note) || null;
      head.appendChild(T.el('p', null,
        note || 'This branch holds only where the competent authority has taken that option.'));
    } else {
      head.appendChild(T.el('h3', null, 'The derivation'));
    }
    node.appendChild(head);

    node.appendChild(renderVerdict(branch, rubrics));
    node.appendChild(renderStepOne(branch, rubrics));
    node.appendChild(renderStepTwo(branch, rubrics));
    node.appendChild(renderStepThree(branch, rubrics));
    node.appendChild(renderStepFour(rubrics));
    const five = renderStepFive(branch, rubrics);
    node.appendChild(five.section);
    return { node: node, formulary: five.formulary, branch: branch };
  }

  function renderApparatus(rubrics) {
    const node = T.el('section', 'apparatus');

    node.appendChild(T.el('h3', null, 'What this page does not decide'));
    const notDecided = T.el('ul');
    for (const row of rubrics.not_decided_here || []) {
      notDecided.appendChild(T.el('li', null, row));
    }
    node.appendChild(notDecided);

    if ((rubrics.unsettled || []).length) {
      node.appendChild(T.el('h3', null, 'Questions this repository leaves open'));
      const open = T.el('ul');
      for (const row of rubrics.unsettled) {
        const item = T.el('li');
        item.appendChild(T.el('strong', null, row.what + ': '));
        item.appendChild(document.createTextNode(row.why));
        if (row.effect) item.appendChild(document.createTextNode(' ' + row.effect));
        open.appendChild(item);
      }
      node.appendChild(open);
    }

    if ((rubrics.divergences || []).length) {
      node.appendChild(T.el('h3', null, 'Where this file departs from the study it was taken from'));
      const diverge = T.el('ul');
      for (const row of rubrics.divergences) {
        const item = T.el('li');
        item.appendChild(T.el('strong', null, row.what + ': '));
        item.appendChild(document.createTextNode(
          'the study reads “' + row.publication_reads + '”; this file reads “' +
          row.this_file_reads + '”. ' + row.why));
        diverge.appendChild(item);
      }
      node.appendChild(diverge);
    }

    node.appendChild(T.el('h3', null, 'Where the rules came from'));
    const from = rubrics.derived_from || {};
    node.appendChild(T.el('p', null,
      'The rules are ' + (rubrics.code || 'the governing code') +
      ', transcribed from this repository’s own collated study at ' +
      (from.publication || 'an in-repository publication') +
      '. Not one of them was read for this page; each carries the locus the study ' +
      'recorded against it.'));
    for (const witness of from.witnesses || []) {
      node.appendChild(T.el('p', null, witness.role + ': ' + witness.what));
    }
    if (rubrics.source_advisory) node.appendChild(T.el('p', null, rubrics.source_advisory));
    return node;
  }

  /* ------------------------------------------------------------------------
   * Putting it on screen
   * --------------------------------------------------------------------- */

  async function render(options) {
    if (!state.date || !state.missalId) return;
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
    const yearKey = state.missalId + '/' + civilYear;
    const yearHeld = await once(yearCache, yearKey,
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

    T.clear(reading);
    reading.appendChild(renderHead(derived));

    const rendered = derived.options.map((branch) => renderBranch(branch, rubrics, derived));
    for (const one of rendered) reading.appendChild(one.node);
    reading.appendChild(renderApparatus(rubrics));
    reading.setAttribute('aria-busy', 'false');

    // The spoken summary must not claim a settled day where there is none: an
    // unsettled derivation still names a leading candidate, and reading that out
    // as "takes the day" would be the page's own failure mode in one sentence.
    const first = derived.options[0];
    const blocked = !first.settled;
    const held = first.orations.all || first.orations.low_mass;
    const count = held.length === 1 ? 'one oration' : held.length + ' orations';
    T.statusLine(
      longDate(derived.date, derived.weekday) + ', ' + derived.calendar + '. ' +
      (derived.options.length > 1 ? derived.options.length + ' territorial branches. ' : '') +
      (first.winner
        ? (blocked
            ? first.winner.name + ' stands highest, but this day is not settled here'
            : first.winner.name + (first.winner.optional ? ' stands highest, and is optional' : ' takes the day'))
        : 'the day is not settled here') +
      ', ' + count + (first.orations.all ? '.' : ' at Low Mass.'));

    if (options && options.moveFocus) reading.focus();

    // The formulary is a megabyte and the argument does not need it, so it is
    // fetched only after the argument is readable.
    const propersHeld = await once(propersCache, state.missalId,
      () => T.loadJSON(propersPath(state.missalId)));
    if (!T.isCurrentRender(token)) return;
    for (const one of rendered) {
      if (!propersHeld.ok) {
        T.clear(one.formulary);
        one.formulary.appendChild(T.el('p', 'row-meta',
          'The formulary could not be fetched: ' + propersHeld.message));
        continue;
      }
      renderFormulary(
        one.formulary, one.branch, propersHeld.value, rubrics,
        (derived.liturgicalYear && derived.liturgicalYear.lectionary) || null);
    }
  }

  /* ------------------------------------------------------------------------
   * Selection
   * --------------------------------------------------------------------- */

  function syncControls() {
    dateInput.value = state.date || '';
    if (state.missalId) missalSelect.value = state.missalId;
  }

  function writeHash() {
    T.writeHash([['date', state.date], ['missal', state.missalId]]);
  }

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
    const wantedDate = hash.get('date');
    state.date = validDate(wantedDate) ? wantedDate : todayISO();
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

  prevButton.addEventListener('click', () => step_(-1, { moveFocus: true }));
  nextButton.addEventListener('click', () => step_(1, { moveFocus: true }));
  todayButton.addEventListener('click', () => select(todayISO(), null, { moveFocus: true }));

  controls.addEventListener('submit', (event) => event.preventDefault());

  T.onArrowStep((delta) => step_(delta, { moveFocus: false }));

  T.onHashChange((hash) => {
    const wantedMissal = hash.get('missal');
    if (state.missals.some((one) => one.id === wantedMissal)) state.missalId = wantedMissal;
    const wantedDate = hash.get('date');
    select(validDate(wantedDate) ? wantedDate : state.date, null, { moveFocus: false });
  });

  start();
}());
