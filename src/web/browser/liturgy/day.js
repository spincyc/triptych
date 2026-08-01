/* ===========================================================================
 * Today’s Missal — the day's Mass, with the propers resolution in the margin
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
 * WITH THE ORDINARY ON, this is a missal to follow the Mass in: the Ordinary is
 * the frame and the day's propers are set into it in the order they are said —
 * Introit, Kyrie, Gloria, Collect, Epistle, Gradual, Gospel, Credo, Offertory,
 * Secret, Preface, Canon, Pater, Agnus, Communion, Postcommunion, Ite. WHERE
 * EACH PROPER SITS IS NOT DECIDED HERE. It is declared in the missal's own
 * ordo-missae inventory, carried through `structure/ordinary/<calendar>.json`
 * as `slots`, and each slot cites the rubric that puts it there. This file
 * resolves those declarations against the elements actually on screen and
 * refuses to invent a seat for a proper that has none.
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
  const ORDINARY_INDEX = 'structure/ordinary/index.json';

  function rubricsPath(id) { return 'structure/rubrics/' + id + '.json'; }
  function yearPath(id, year) { return 'structure/calendar/' + id + '/' + year + '.json'; }
  function propersPath(id) { return 'structure/propers/' + id + '.json'; }
  function ordinaryPath(id) { return 'structure/ordinary/' + id + '.json'; }

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
    orationLanguages: [],
    why: false,
    // The Ordinary is a second document, not an annotation on the first, so it
    // is fetched and drawn only when it is asked for rather than hidden by a
    // class the way the margins are.
    ordinary: false,
    ordinaryIndex: [],
    // group id -> chosen option id, so a missal that grows a second choice
    // needs a row in its inventory and no line here.
    variants: {}
  };

  const dateInput = document.getElementById('date-input');
  const missalSelect = document.getElementById('missal-select');
  const bibleSelect = document.getElementById('bible-select');
  const orationsSelect = document.getElementById('orations-select');
  const whyToggle = document.getElementById('why-toggle');
  const ordinaryToggle = document.getElementById('ordinary-toggle');
  const variantField = document.getElementById('variant-field');
  const variantLabel = document.getElementById('variant-label');
  const variantSelect = document.getElementById('variant-select');
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
  const ordinaryCache = new Map();

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
    const node = margin('Propers resolution');

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
    // `branch.conditions` deliberately does not appear here. The model still
    // derives them and `assembly-model.js` still carries them for anyone asking
    // it directly; the page does not print them, because a rubric that holds
    // "unless" something rare is the ordinary shape of nearly every rubric, so
    // printing each one filled the page with qualifications a reader could act
    // on in none of them. What genuinely blocks an answer — an unsettled day, a
    // missing index entry — still shows.
    if (!branch.unsettled.length && !blocking.length) return null;

    // Only one branch survives the gate above, so the conditional wording that
    // stood here is unreachable and is gone rather than left to read as though
    // it could still fire.
    const node = T.el('div', 'day-warning is-unsettled');
    node.appendChild(T.el('h3', null, 'This day is not settled here'));
    node.appendChild(T.el('p', null,
      'The rules as this repository holds them do not decide this date. What ' +
      'follows is shown so the state of the question is visible; it is not an ' +
      'answer and must not be read as one.'));
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
    node.appendChild(list);
    return node;
  }

  function renderBranch(branch, rubrics, derived, structure, bible, fragments, ordinary) {
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
    // The oration slots — Collect, Secret, Postcommunion — under which a
    // commemoration is said. A different thing entirely from the Ordinary's
    // seats below, which are places in the frame; these are places in a series.
    const orationSlots = trackedSlots(branch, rubrics);
    const orationSlotFor = (name) => orationSlots.find((one) => one.slot === name) || null;

    const mass = branch.winner.key
      ? (structure.masses || []).find((one) => one.key === branch.winner.key)
      : null;

    /** One proper of the day, with whatever the margin has to say beside it. */
    function renderMassProper(proper, seat) {
      const body = T.renderProper(proper, bible, fragments, {
        numbering: (structure && structure.numbering) || null,
        orations: state.orations,
        cycle: cycleKeyFor(
          proper, (derived.liturgicalYear && derived.liturgicalYear.lectionary) || null)
      });
      // The rubric that seats this proper in the frame, shown with the rest of
      // the reasoning rather than in the body: a reader following the Mass
      // wants the prayer, and a reader checking the page wants the citation.
      if (seat && state.why) {
        body.appendChild(T.el('p', 'composed-note element-apparatus',
          'Seated here by ' + seat.locus + '.'));
      }
      const oration = orationSlotFor(proper.name);
      const note = (oration && subordinate.length)
        ? properMargin(oration, subordinate, branch, structure)
        : null;
      return annotated(body, note);
    }

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
    }

    const propers = (mass && !T.massIsUncompiled(mass) && mass.propers) || [];
    if (ordinary) {
      // The Ordinary is the frame and the propers go into it. A Mass with no
      // formulary still gets the frame: the reader is following the same rite,
      // and the line above has already said what is not transcribed.
      section.appendChild(renderFrame(ordinary, propers, renderMassProper));
    } else {
      for (const proper of propers) {
        if (T.isPlaceholder(proper)) continue;
        section.appendChild(renderMassProper(proper, null));
      }
    }

    // A commemoration that found no slot to sit under is still said. It is put
    // once, after the Mass, rather than dropped.
    const anySlot = propers.some((one) => orationSlotFor(one.name));
    if (subordinate.length && !anySlot) {
      const held = T.el('div', 'mass-head');
      held.appendChild(T.el('h4', 'mass-subheading',
        subordinate.length === 1 ? 'A commemoration is said with this Mass'
          : subordinate.length + ' commemorations are said with this Mass'));
      held.appendChild(T.el('p', 'row-meta',
        'This corpus carries no oration slot for the day’s own Mass, so the page ' +
        'cannot say which proper each follows. They are appointed, not absent.'));
      section.appendChild(annotated(held,
        properMargin(orationSlots[0] || { slot: 'Collect' }, subordinate, branch, structure)));
    }
    return section;
  }

  /* ------------------------------------------------------------------------
   * The Ordinary
   *
   * The unvarying frame the day's propers are set into — literally so: with the
   * Ordinary on, the propers are rendered inside it, each at the place its
   * missal declares, so the page reads down the Mass in the order it is said.
   *
   * NOTHING ABOUT RIGHTS IS DECIDED HERE. The generator has already dropped
   * every witness it may not publish and has written, on each element, which of
   * its two texts is absent and under which recorded reason. This code prints
   * what it is handed. That matters most where it would be easiest to be
   * careless: one missal's English is freely given and another's is withheld by
   * a licence, and a reader must be able to tell those two apart on sight.
   *
   * NOR IS ANY PLACEMENT DECIDED HERE. `file.slots` is the missal's own
   * statement of where each proper stands, each with the rubric that puts it
   * there. Thirty-nine of the postconciliar frame's forty-eight elements carry
   * no text at all, and that changes nothing: an element that names its absence
   * still marks the place, and the day's Collect is seated after the withheld
   * one rather than in its stead.
   * --------------------------------------------------------------------- */

  function variantGroupOf(file) {
    return (file.variants || [])[0] || null;
  }

  /** The option chosen in each group, defaulting to the one the source marks. */
  function chosenOption(file, group) {
    const wanted = state.variants[group.group];
    const found = (group.options || []).find((one) => one.id === wanted);
    return found || (group.options || []).find((one) => one.default) || null;
  }

  /**
   * Whether an element is shown at all.
   *
   * An element with no `variant` belongs to the frame and always shows. One that
   * names an option shows only under that option — which is what makes the
   * control a choice between prayers rather than a filter over a list of them.
   */
  function elementShows(element, file) {
    if (!element.variant) return true;
    const group = variantGroupOf(file);
    const chosen = group && chosenOption(file, group);
    return Boolean(chosen && chosen.id === element.variant);
  }

  /** A witness's acknowledgement, printed where its words are, never in a footer. */
  function witnessNote(file, sourceId) {
    return (file.translations || []).find((one) => one.source_id === sourceId) || null;
  }

  function absenceWord(file, key) {
    const found = (file.absences || []).find((one) => one.key === key);
    return found ? found.what : key;
  }

  function renderElement(element, file) {
    const section = T.el('section', 'proper ordinary-element');

    const heading = T.el('h4', 'proper-name', element.name || element.key.split('/').pop());
    if (element.speaker) heading.appendChild(T.el('span', 'proper-form', element.speaker));
    if (element.locus) heading.appendChild(T.el('span', 'proper-ref', element.locus));
    section.appendChild(heading);

    const held = (element.translations || [])[0] || null;
    if (held) {
      const body = T.el('p', 'composed');
      body.appendChild(T.el('span', 'composed-label',
        element.kind === 'rubric' ? 'Rubric — the book’s own words'
          : 'Composed text — not scripture'));
      body.appendChild(document.createTextNode(held.text));
      body.lang = held.lang;
      section.appendChild(body);

      const witness = witnessNote(file, held.source_id);
      if (witness) {
        // The condition the licence attaches travels with the words it
        // licenses. Printing it once at the foot of the page would let the two
        // be separated by any reader who copied a prayer out of it.
        //
        // Which witness supplied the words is different: it is the same answer
        // for every element of an Ordinary served from one printing, and
        // repeating it 195 times said nothing 194 of those times. It is named
        // once, above, where the Ordinary declares what it was taken from.
        if (witness.acknowledgement) {
          section.appendChild(T.el('p', 'composed-note ordinary-grant', witness.acknowledgement));
        }
      }
    }

    // The Latin incipit earns its place only where the words are not shown: it
    // is then the sole thing identifying which prayer this is.
    if (!held && element.latin_incipit) {
      const incipit = T.el('p', 'proper-incipit', element.latin_incipit);
      incipit.lang = 'la';
      section.appendChild(incipit);
    }

    const absent = element.absent || {};
    if (absent.english) {
      section.appendChild(T.notice('its English. ' + absenceWord(file, absent.english)));
    }
    if (absent.latin && !held) {
      section.appendChild(T.notice('its Latin. ' + absenceWord(file, absent.latin)));
    }
    // The note is the transcriber's apparatus — which capital is a drop, where
    // the Latin column prints a cross, which leaf a reading came from. It is
    // 48,000 characters across this Ordinary and none of it is the Mass, so it
    // stays in the record and off the page a reader follows the Mass with.
    // It reappears with the rest of the reasoning when that is asked for.
    if (element.note && state.why) {
      section.appendChild(T.el('p', 'composed-note element-apparatus', element.note));
    }
    return section;
  }

  /**
   * What the Ordinary says about itself, once for the page.
   *
   * It is the same file for every branch on the date, so saying it per branch
   * would say it twice about one thing. It stands above the Masses because it
   * governs all of them.
   */
  function ordinaryPreamble(file) {
    const wrapper = T.el('section', 'ordinary-preamble');
    wrapper.appendChild(T.el('h3', 'mass-name', file.title));
    wrapper.appendChild(T.el('p', 'entry-meta',
      [file.edition_short || file.edition, 'the frame the day’s propers are set into']
        .filter(Boolean).join(' · ')));
    wrapper.appendChild(T.el('p', 'row-meta', file.advisory));

    // Named once, here, rather than under every element it supplied.
    const named = (file.translations || []).filter((one) => one.label);
    if (named.length) {
      wrapper.appendChild(T.el('p', 'row-meta',
        (named.length === 1 ? 'Translation: ' : 'Translations: ') +
        named.map((one) => one.label).join('; ')));
    }

    for (const witness of file.translations || []) {
      if (witness.caution) {
        wrapper.appendChild(T.el('p', 'row-meta', witness.label + ' — ' + witness.caution));
      }
    }

    const group = variantGroupOf(file);
    const chosen = group && chosenOption(file, group);
    if (group && chosen) {
      wrapper.appendChild(T.el('p', 'row-meta',
        group.name + ': ' + chosen.name + '. ' + group.what));
    }

    // Where the seats came from. A page that sets one book's propers into
    // another book's frame owes the reader that sentence.
    if (file.slots_derived_from) {
      wrapper.appendChild(T.el('p', 'row-meta', file.slots_derived_from));
    }
    return wrapper;
  }

  /**
   * The elements this frame is actually showing, in order.
   *
   * Which they are depends on the reader's choice of Eucharistic Prayer, which
   * is why a seat is resolved against this list and not against the file.
   */
  function shownElements(file) {
    const held = [];
    for (const section of file.sections || []) {
      for (const element of section.elements || []) {
        if (elementShows(element, file)) held.push({ section: section, element: element });
      }
    }
    return held;
  }

  /**
   * The declared seats, resolved to positions among the elements on screen.
   *
   * `at[n]` is the index a proper seated by slot `n` is inserted at: an `after`
   * puts it one place further on than a `before` on the same element, which is
   * how two slots on neighbouring elements land in one position without either
   * being ambiguous about which element it named.
   */
  function seats(file, shown) {
    const where = new Map();
    shown.forEach((row, index) => where.set(row.element.key, index));
    const slots = file.slots || [];
    const at = [];
    const byName = new Map();
    slots.forEach((slot, ordinal) => {
      const anchor = where.get(slot.anchor);
      // A file the generator accepted cannot get here; a file from somewhere
      // else can, and an unresolvable anchor must lose the seat, not the proper.
      if (anchor === undefined) return;
      at[ordinal] = anchor + (slot.where === 'after' ? 1 : 0);
      for (const name of slot.propers || []) byName.set(name, ordinal);
    });
    return { slots: slots, at: at, byName: byName };
  }

  /**
   * Which propers go where, without ever reordering the missal.
   *
   * The rule is one sentence and it is worth stating exactly, because the
   * tempting alternatives all quietly rearrange a book. Walk the day's propers
   * in the order the missal prints them. A proper whose name a slot claims is
   * seated there, PROVIDED that seat is not behind the last one used. A proper
   * no slot claims rides with the one before it, which is where the missal put
   * it. And the first proper that would send the reading backwards ends the
   * interleaving: it and everything after it are shown after the frame, in the
   * missal's own order.
   *
   * That last clause is the whole of the honesty here. A day carrying four
   * Masses — Christmas — or a rite that departs from the frame — Good Friday,
   * the paschal Vigil — cannot be poured into one Ordinary, and a page that
   * tried would interleave two formularies into one Mass that was never said.
   * Nothing is dropped, nothing is reordered, and the break is stated.
   */
  function seatPropers(propers, seating) {
    const before = [];
    const buckets = new Map();
    const after = [];
    let reached = -1;
    let riding = null;
    let broke = false;
    for (const proper of propers) {
      if (T.isPlaceholder(proper)) continue;
      if (broke) { after.push({ proper: proper, seat: null }); continue; }
      const ordinal = seating.byName.has(proper.name) ? seating.byName.get(proper.name) : -1;
      if (ordinal < 0) { (riding || before).push({ proper: proper, seat: null }); continue; }
      if (ordinal < reached) { broke = true; after.push({ proper: proper, seat: null }); continue; }
      reached = ordinal;
      const index = seating.at[ordinal];
      riding = buckets.get(index) || [];
      buckets.set(index, riding);
      riding.push({ proper: proper, seat: seating.slots[ordinal] });
    }
    return { before: before, buckets: buckets, after: after, broke: broke };
  }

  /** The frame, with the day's propers set into it. */
  function renderFrame(file, propers, renderMassProper) {
    const wrapper = T.el('section', 'ordinary-frame');
    const shown = shownElements(file);
    const placed = seatPropers(propers, seats(file, shown));

    const pour = (held) => {
      for (const row of held) wrapper.appendChild(renderMassProper(row.proper, row.seat));
    };

    if (placed.before.length) {
      wrapper.appendChild(T.el('p', 'row-meta ordinary-aside',
        'This Mass opens with propers the Ordinary appoints no place for. They ' +
        'are shown first, in the missal’s own order.'));
      pour(placed.before);
    }

    let current = null;
    for (let index = 0; index < shown.length; index += 1) {
      if (shown[index].section !== current) {
        current = shown[index].section;
        wrapper.appendChild(T.el('h3', 'mass-subheading', current.name));
      }
      pour(placed.buckets.get(index) || []);
      wrapper.appendChild(renderElement(shown[index].element, file));
    }
    pour(placed.buckets.get(shown.length) || []);

    if (placed.after.length) {
      wrapper.appendChild(T.el('p', 'row-meta ordinary-aside',
        'From here the day’s propers no longer run forward through the Ordinary: ' +
        'this day carries more than one formulary, or its rite departs from the ' +
        'frame. The rest is shown in the missal’s own order, unseated and ' +
        'unreordered.'));
      pour(placed.after);
    }
    return wrapper;
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

  /**
   * The variant control, filled from the chosen missal's own Ordinary.
   *
   * Hidden where there is nothing to choose — which is the 1962 Missal, with one
   * Canon — and hidden while the Ordinary is not showing, because a control for
   * something invisible is a control that does nothing.
   */
  function fillVariantSelect(file) {
    const group = file && variantGroupOf(file);
    if (!state.ordinary || !group) {
      variantField.hidden = true;
      return;
    }
    variantLabel.textContent = group.name;
    T.fillSelect(variantSelect, (group.options || []).map((one) => ({
      value: one.id,
      label: one.name,
      title: one.id
    })));
    const chosen = chosenOption(file, group);
    if (chosen) variantSelect.value = chosen.id;
    variantField.hidden = false;
  }

  function syncControls() {
    dateInput.value = state.date || '';
    if (state.missalId) missalSelect.value = state.missalId;
    if (state.bibleId) bibleSelect.value = state.bibleId;
    if (state.orations) orationsSelect.value = state.orations;
    whyToggle.checked = state.why;
    ordinaryToggle.checked = state.ordinary;
    applyWhy();
  }

  // The margins stay in the DOM and are hidden by a class rather than removed,
  // so toggling costs no re-render and a reader turning them back on lands on
  // the same page rather than a rebuilt one.
  function applyWhy() {
    document.body.classList.toggle('shows-why', state.why);
  }

  function writeHash() {
    const pairs = [
      ['date', state.date],
      ['missal', state.missalId],
      ['bible', state.bibleId],
      ['orations', state.orations === T.SOURCE_LANGUAGE ? null : state.orations],
      ['why', state.why ? '1' : null],
      ['ordinary', state.ordinary ? '1' : null]
    ];
    // Keyed by the group's own id, so a second choice in some later missal
    // rides in the hash without a line being added here.
    for (const group of Object.keys(state.variants).sort()) {
      pairs.push([group, state.variants[group]]);
    }
    T.writeHash(pairs);
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

    // The Ordinary, only if it was asked for. The fetch is after the Mass's,
    // and its failure is reported in place rather than replacing the Mass: a
    // missing Ordinary is no reason to withhold the propers of the day.
    let ordinary = null;
    if (state.ordinary && state.ordinaryIndex.some((one) => one.calendar === state.missalId)) {
      ordinary = await once(ordinaryCache, state.missalId,
        () => T.loadJSON(ordinaryPath(state.missalId)));
      if (!T.isCurrentRender(token)) return;
    }

    T.clear(reading);
    renderHead(derived, bible);

    // The frame is settled before a word of any Mass is drawn, because each
    // Mass is drawn inside it. Where there is no frame the Masses render as
    // they always did — a missing Ordinary withholds nothing but itself.
    const frame = ordinary && ordinary.ok ? ordinary.value : null;
    fillVariantSelect(frame);
    if (frame) {
      reading.appendChild(ordinaryPreamble(frame));
    } else if (ordinary) {
      reading.appendChild(T.notice(
        'the Ordinary of this missal. It could not be loaded: ' + ordinary.message));
    } else if (state.ordinary) {
      reading.appendChild(T.notice(
        'the Ordinary of this missal. This corpus carries none for “' +
        state.missalId + '”.'));
    }

    for (const branch of derived.options) {
      reading.appendChild(
        renderBranch(branch, rubrics, derived, structure, bible, held.fragments, frame));
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

    // One fetch, at start-up, for which missals have an Ordinary at all. It is
    // ~1 KB; the Ordinary itself is not fetched until it is asked for. A corpus
    // built before this layer existed simply has none, which is not an error.
    try {
      const file = await T.loadJSON(ORDINARY_INDEX);
      state.ordinaryIndex = (file && file.calendars) || [];
    } catch (error) {
      state.ordinaryIndex = [];
    }

    const hash = T.readHash();
    state.orations = hash.get('orations') || T.SOURCE_LANGUAGE;
    const wantedBible = hash.get('bible');
    state.bibleId = state.bibles.some((one) => one.id === wantedBible)
      ? wantedBible
      : state.bibles[0].id;
    state.why = hash.get('why') === '1';
    state.ordinary = hash.get('ordinary') === '1';
    for (const row of state.ordinaryIndex) {
      for (const group of row.variants || []) {
        const wanted = hash.get(group);
        if (wanted) state.variants[group] = wanted;
      }
    }
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

  whyToggle.addEventListener('change', () => {
    state.why = whyToggle.checked;
    applyWhy();
    writeHash();
  });

  ordinaryToggle.addEventListener('change', () => {
    state.ordinary = ordinaryToggle.checked;
    select(null, null, { moveFocus: false });
  });

  variantSelect.addEventListener('change', () => {
    const held = ordinaryCache.get(state.missalId);
    // The select's own options came from this missal's groups, so the group is
    // read back from the file rather than assumed from the control's id.
    Promise.resolve(held).then((resolved) => {
      const group = resolved && resolved.ok && variantGroupOf(resolved.value);
      if (!group) return;
      state.variants[group.group] = variantSelect.value;
      select(null, null, { moveFocus: false });
    });
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
    state.ordinary = hash.get('ordinary') === '1';
    for (const row of state.ordinaryIndex) {
      for (const group of row.variants || []) {
        const wanted = hash.get(group);
        if (wanted) state.variants[group] = wanted;
      }
    }
    const wantedDate = hash.get('date');
    select(validDate(wantedDate) ? wantedDate : state.date, null, { moveFocus: false });
  });

  start();
}());
