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
    return rows.map((row) => ({
      id: row.calendar,
      label: row.edition || T.titleCase(row.calendar),
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

  function orationSet(title, note, series, rubrics, ceiling) {
    const node = T.el('div', 'oration-set');
    node.appendChild(T.el('h5', null, title));
    node.appendChild(T.el('p', 'count',
      series.length === 1 ? 'One oration.' : series.length + ' orations.' +
        (note ? ' ' + note : '')));
    if (note && series.length === 1) node.appendChild(T.el('p', 'count', note));
    const list = T.el('ol');
    for (const oration of series) {
      const item = T.el('li');
      item.appendChild(T.el('span', 'oration-label', oration.label));
      item.appendChild(T.el('span', 'oration-of', oration.of_name));
      const why = T.el('div', 'oration-why', oration.kind + ' — ' + oration.why);
      withLocus(why, oration.locus);
      item.appendChild(why);
      if (oration.conclusion) {
        item.appendChild(T.el('div', 'oration-why', 'Said under ' + oration.conclusion + '.'));
      }
      if (oration.alternative) {
        const alt = T.el('div', 'oration-why',
          'The collect of ' + oration.alternative.of_name + ' may be said in its place: ' +
          oration.alternative.what);
        withLocus(alt, oration.alternative.locus);
        item.appendChild(alt);
      }
      list.appendChild(item);
    }
    node.appendChild(list);
    // The ceiling is the answer to "why this many", so it is stated whether or
    // not it turned anything away.
    if (ceiling) {
      const rule = T.el('p', 'oration-why', ceiling.what ||
        ('This day admits ' + ceiling.max + ' commemoration' + (ceiling.max === 1 ? '' : 's') +
         (ceiling.privileged_only ? ', and only a privileged one.' : '.')));
      withLocus(rule, ceiling.locus);
      node.appendChild(rule);
    }
    return node;
  }

  function renderStepFive(branch, rubrics) {
    const orations = rubrics.orations || {};
    const commemorates = !(rubrics.commemoration && rubrics.commemoration.exists === false);
    const held = step(5, 'Assembly: the orations, and what is read out of the book',
      commemorates
        ? 'The collects are where the days that lost survive. The number is capped by ' +
          'the class of the day that won, and again by how the Mass is celebrated.'
        : 'One collect, whatever else fell on the day. This rite does not commemorate, ' +
          'and that is the sharpest difference between the two books.');

    const sets = T.el('div', 'orations');
    const ceilings = branch.ceilings || {};
    if (branch.orations.all) {
      sets.appendChild(orationSet('Every Mass', orations.what || null, branch.orations.all, rubrics, null));
    } else {
      sets.appendChild(orationSet(
        'Low Mass, and the conventual Mass',
        null,
        branch.orations.low_mass, rubrics, ceilings.low_mass));
      sets.appendChild(orationSet(
        'A sung Mass that is not the conventual Mass',
        branch.sungDiffers
          ? 'Fewer than at the Low Mass an hour earlier: an ordinary commemoration is ' +
            'made only at Lauds, at the conventual Mass and at Low Masses.'
          : (branch.orations.low_mass.length > 1
              ? 'The same, because every commemoration due here is privileged, and a ' +
                'privileged commemoration is made in every Mass.'
              : 'The same: nothing on this day was commemorated.'),
        branch.orations.sung_non_conventual, rubrics, ceilings.sung_non_conventual));
    }
    held.body.appendChild(sets);

    if (commemorates) {
      const order = (rubrics.commemoration && rubrics.commemoration.order) || null;
      if (order) held.body.appendChild(paragraph('row-meta', order.gloss, order.locus));
      const cap = orations.absolute_cap;
      if (cap) held.body.appendChild(paragraph('row-meta', cap.gloss, cap.locus));
      for (const row of orations.tracked_by || []) {
        held.body.appendChild(paragraph('row-meta',
          'The ' + row.slot + 's follow the collects: ' + row.what, row.locus));
      }
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

  function renderFormulary(node, branch, structure, rubrics) {
    T.clear(node);
    if (!branch.winner) {
      node.appendChild(T.el('p', 'row-meta',
        'No formulary is shown: no day was settled above.'));
      return;
    }
    if (!branch.winner.key) {
      node.appendChild(T.el('p', 'row-meta',
        'The day that won is constituted from its season and this calendar index ' +
        'carries no formulary of its own for it. Most ferias take the preceding ' +
        'Sunday’s Mass, which the index does not repeat.'));
      return;
    }

    const mass = (structure.masses || []).find((one) => one.key === branch.winner.key);
    if (!mass) {
      node.appendChild(T.el('p', 'row-meta',
        'The propers structure carries no mass keyed ' + branch.winner.key + '.'));
      return;
    }

    node.appendChild(T.el('h5', 'oration-label', 'The formulary, in the order the missal appoints it'));

    const commemorated = branch.losers.filter((one) => one.disposition === 'commemorated');
    const added = new Map();
    for (const row of commemorated) {
      const held = (structure.masses || []).find((one) => one.key === row.id);
      added.set(row.id, { loser: row, mass: held || null });
    }

    const list = T.el('ul', 'formulary-list');
    // The Secret and the Postcommunion track the collects in number and order,
    // so a commemoration is inserted after each of the three, not only after
    // the Collect. Anything else would print a Mass nobody says.
    const TRACKS = { Collect: 'Collect', Secret: 'Secret', Postcommunion: 'Postcommunion' };
    let placed = false;

    for (const proper of mass.propers || []) {
      const item = T.el('li', 'formulary-item');
      item.appendChild(T.el('span', 'formulary-slot', proper.name || 'Proper'));
      const detail = T.el('span', 'formulary-detail');
      const refs = (proper.citations || []).map((one) => one.ref).filter(Boolean);
      if (proper.incipit) detail.appendChild(T.el('em', null, proper.incipit));
      if (refs.length) {
        if (proper.incipit) detail.appendChild(document.createTextNode(' · '));
        detail.appendChild(document.createTextNode(refs.join('; ')));
      }
      if (!proper.incipit && !refs.length) {
        detail.appendChild(document.createTextNode(
          proper.text ? 'composed text' : 'no citation or text is compiled here'));
      }
      item.appendChild(detail);
      list.appendChild(item);

      const tracked = TRACKS[proper.name];
      if (!tracked) continue;
      placed = true;
      let position = 2;
      for (const [key, row] of added) {
        const extra = T.el('li', 'formulary-item is-added');
        extra.appendChild(T.el('span', 'formulary-slot',
          (position === 2 ? 'Second ' : 'Third ') + tracked.toLowerCase()));
        const say = T.el('span', 'formulary-detail');
        say.appendChild(document.createTextNode('of ' + row.loser.name));
        const held = row.mass;
        const matching = held && (held.propers || []).find((one) => one.name === tracked);
        if (matching && matching.incipit) {
          say.appendChild(document.createTextNode(' — '));
          say.appendChild(T.el('em', null, matching.incipit));
        } else if (held) {
          say.appendChild(document.createTextNode(
            ' — its ' + tracked.toLowerCase() + ' is not compiled in this corpus'));
        } else {
          say.appendChild(document.createTextNode(
            ' — this day has no formulary in the index, so its oration is taken ' +
            'from the season’s own Mass'));
        }
        extra.appendChild(say);
        list.appendChild(extra);
        position += 1;
      }
    }
    node.appendChild(list);

    if (!(mass.propers || []).length) {
      node.appendChild(T.el('p', 'row-meta',
        'This missal keeps the day and the corpus carries no propers for it yet.'));
    }
    // A commemoration with nowhere to sit must be said, not dropped. Many of
    // this corpus's seasonal ferias carry only their scripture-bearing propers,
    // so the slot the second collect belongs in is not written down here — which
    // is a gap in the corpus and not a fact about the Mass.
    if (added.size && !placed) {
      node.appendChild(T.el('p', 'row-meta',
        'The ' + (added.size === 1 ? 'commemoration' : 'commemorations') + ' derived above ' +
        (added.size === 1 ? 'has' : 'have') + ' no place to sit in the list: this corpus ' +
        'carries no Collect, Secret or Postcommunion for the day’s own Mass, so the slots ' +
        'the second orations follow are not written down. The orations are appointed, not ' +
        'absent.'));
    }
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
      renderFormulary(one.formulary, one.branch, propersHeld.value, rubrics);
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
      title: one.code || one.id
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
