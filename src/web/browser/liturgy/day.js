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
 *     &ordinary=1&ordinary-lang=<lang>&rubrics=0&why=1
 *
 * Four controls govern the frame, and each of them reads a declaration rather
 * than holding one. `ordinary-lang` offers the languages the Ordinary's own
 * file declares, including one it holds no word of, because choosing an empty
 * language is how a reader is shown, at every element, the reason it is empty.
 * `rubrics` paints or does not paint the priest's actions, and never removes
 * them, because they are the elements the propers are seated against. The
 * Eucharistic Prayer comes from the file's `variants`. And `why` puts the
 * whole apparatus — the rubrical account, the transcriber's notes, how the
 * frame was derived — into the margin, off the page the Mass is read from.
 * ======================================================================== */

'use strict';

(function () {
  const T = window.Triptych;
  const Model = window.MassAssembly;
  const Seating = window.OrdinarySeating;

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

  // The celebration is the page's h1. A major division of its Ordinary is h2,
  // and every part said is h3, whether it is an element of the frame or a
  // proper of the day. Those two are the same kind of thing to a reader moving
  // by headings; making a Proper outrank the division it stands in would state
  // a hierarchy the Mass does not have.
  const DIVISION_HEADING = 'h2';
  const PART_HEADING = 'h3';

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
    // The language the Ordinary is read in, held as the reader asked for it
    // rather than as the file offers it: the hash is read before any Ordinary
    // is fetched, so it is resolved against the file in `chosenLanguage`.
    ordinaryLang: null,
    // The rubrics of the Ordinary — what the priest does. ON, because a missal
    // prints them and they are how a reader following along knows where the
    // Mass has got to; a page that opened without them would open showing less
    // than the book it is standing in for. Named `showRubrics` because
    // `state.rubrics` above is the rules of precedence, which are a different
    // thing entirely.
    showRubrics: true,
    // group id -> chosen option id, so a missal that grows a second choice
    // needs a row in its inventory and no line here.
    variants: {},
    // The formulary the reader has asked to see, by mass key. Null is "the one
    // that is said". Cleared on every date change, because a selection belongs
    // to the day it was made on and carrying yesterday's onto today would put a
    // Mass on a date that never carried it.
    shownMass: null
  };

  const dateInput = document.getElementById('date-input');
  const missalSelect = document.getElementById('missal-select');
  const bibleSelect = document.getElementById('bible-select');
  const orationsSelect = document.getElementById('orations-select');
  const whyToggle = document.getElementById('why-toggle');
  const ordinaryToggle = document.getElementById('ordinary-toggle');
  const ordinaryLangField = document.getElementById('ordinary-lang-field');
  const ordinaryLangSelect = document.getElementById('ordinary-lang-select');
  const rubricsField = document.getElementById('rubrics-field');
  const rubricsToggle = document.getElementById('rubrics-toggle');
  const variantField = document.getElementById('variant-field');
  const variantLabel = document.getElementById('variant-label');
  const variantSelect = document.getElementById('variant-select');
  const prevButton = document.getElementById('prev-button');
  const nextButton = document.getElementById('next-button');
  const todayButton = document.getElementById('today-button');
  const celebrationTitle = document.getElementById('celebration-title');
  const celebrationDate = document.getElementById('celebration-date');
  const celebrationMeta = document.getElementById('celebration-meta');
  const noticesDisclosure = document.getElementById('notices-disclosure');
  const banner = document.getElementById('banner');
  const renderedNotices = document.getElementById('rendered-notices');
  const contentsDisclosure = document.getElementById('contents-disclosure');
  const contentsNav = document.getElementById('contents-nav');
  const formularyControls = document.getElementById('formulary-controls');
  const reading = document.getElementById('reading');
  const controls = document.getElementById('controls');

  function rebuildContents() {
    ReadingContents.rebuild({
      beginning: celebrationTitle,
      reading: reading,
      disclosure: contentsDisclosure,
      nav: contentsNav,
      selector: '.ordinary-division, ' +
        '.ordinary-frame > .annotated > .annotated-text > .proper > .proper-name'
    });
  }

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

  function missalNamed(id) {
    return state.missals.find((one) => one.id === id) || null;
  }

  function currentMissal() {
    return missalNamed(state.missalId);
  }

  function currentBible() {
    return state.bibles.find((one) => one.id === state.bibleId) || null;
  }

  /* ------------------------------------------------------------------------
   * The head: what day this is
   * --------------------------------------------------------------------- */

  function renderHead(derived, bible) {
    const first = derived.options[0];
    celebrationTitle.textContent = first && first.winner
      ? first.winner.name
      : 'No day is settled here';
    celebrationDate.textContent = longDate(derived.date, derived.weekday);

    const missal = currentMissal();
    const meta = [];
    if (missal) meta.push(missal.edition || missal.label);
    if (derived.season) meta.push(T.titleCase(derived.season));
    if (derived.week) meta.push('Week ' + derived.week);
    const cycle = derived.liturgicalYear && derived.liturgicalYear.lectionary;
    if (cycle) meta.push('Lectionary ' + cycle.sunday + '/' + cycle.weekday);
    celebrationMeta.textContent = meta.concat(T.bibleMeta(bible)).join(' · ');

    // A year the calendar computation itself refused to resolve is a fact about
    // this whole year, not about one proper, so it is said once here.
    const unresolved = (derived.liturgicalYear && derived.liturgicalYear.unresolved) || [];
    for (const row of unresolved) {
      renderedNotices.appendChild(
        T.notice('unresolved this year: ' + row.what + ' — ' + row.why));
    }
  }

  function updateNoticesDisclosure() {
    noticesDisclosure.hidden = banner.hidden && renderedNotices.children.length === 0;
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

  /**
   * Which Mass this day's text is drawn from, and on whose authority.
   *
   * Three cases, and the page must not flatten them. A day inscribed in the
   * calendar prints its own formulary. A day constituted from the season
   * ordinarily borrows the preceding Sunday's Mass under RGMR 299. And the
   * Office of Our Lady on Saturday has a Mass of its own, because it is not a
   * feria at all but row 27 of the table, so RGMR 299 never reaches it.
   *
   * Where the rubrics offer a choice, the reader's answer wins over all three —
   * that is what the selector is for.
   */
  /** The entry of `branch.readable` the reader is looking at. */
  function shownEntry(branch) {
    const rows = branch.readable || [];
    if (!rows.length) return null;
    const wanted = state.shownMass && rows.find((one) => one.key === state.shownMass);
    return wanted || rows.find((one) => one.state === 'said') || rows[0];
  }

  function formularyOf(branch) {
    if (!branch.winner) return null;
    const entry = shownEntry(branch);
    if (entry && entry.state !== 'said') {
      return { key: entry.key, name: entry.label, kind: 'chosen', entry: entry };
    }
    if (branch.winner.formulary) return branch.winner.formulary;
    return branch.winner.key ? { key: branch.winner.key, kind: 'own' } : null;
  }

  /**
   * The selector itself, and the rubric that creates it.
   *
   * A choice the rubrics state is NOT a day this repository could not settle.
   * The unsettled warning is a red box saying the page has no answer; this is a
   * control saying the book has two. They are rendered as different things on
   * purpose, and this one never sets or clears `settled`.
   */
  // The heading each standing is offered under. These are the labels that keep
  // "may be said instead" apart from "is certainly not said", so they are
  // written out rather than derived from the state name.
  const STANDING_GROUPS = {
    said: 'Said today',
    option: 'The rubrics permit either',
    additional: 'Also said today, at another hour',
    commemorated: 'Commemorated within today’s Mass',
    displaced: 'Not said today — displaced',
    unresolved: 'Candidates; this date is not settled here'
  };
  const STANDING_ORDER = ['said', 'option', 'additional', 'commemorated', 'displaced', 'unresolved'];

  /**
   * One control for every formulary the date carries, grouped by standing.
   *
   * Grouped, and never a flat list. A flat list of Masses is precisely the thing
   * that lets a reader take a displaced Mass for the day's — the failure this
   * whole page is built to refuse. The `<optgroup>` label is the guard, and the
   * notice below is the second one.
   */
  function formularySelector(branch, onPick) {
    const rows = branch.readable || [];
    if (rows.length < 2) return null;

    const node = T.el('div', 'mass-choice');
    const field = T.el('p', 'mass-choice-field');
    const id = 'mass-shown';

    const label = T.el('label', 'mass-choice-label', 'Show the Mass of');
    label.setAttribute('for', id);
    field.appendChild(label);

    const select = document.createElement('select');
    select.id = id;
    select.className = 'mass-choice-select';
    for (const standing of STANDING_ORDER) {
      const held = rows.filter((one) => one.state === standing);
      if (!held.length) continue;
      const group = document.createElement('optgroup');
      group.label = STANDING_GROUPS[standing];
      for (const row of held) {
        const item = document.createElement('option');
        item.value = row.key;
        item.textContent = row.label;
        group.appendChild(item);
      }
      select.appendChild(group);
    }
    const entry = shownEntry(branch);
    if (entry) select.value = entry.key;
    select.addEventListener('change', function () {
      state.shownMass = select.value;
      writeHash();
      onPick();
    });
    field.appendChild(select);
    node.appendChild(field);
    return node;
  }

  /**
   * What a reader who has selected something other than today's Mass must see.
   *
   * Shown on ARRIVAL and not only on selection, because the hash carries the
   * choice: a link to a displaced Mass must state its displacement to the
   * person who follows the link, who did not choose it and has no reason to
   * suspect it.
   */
  function standingNotice(branch) {
    const entry = shownEntry(branch);
    if (!entry || entry.state === 'said') return null;
    const said = (branch.readable || []).find((one) => one.state === 'said');

    const node = T.el('div', 'day-warning is-standing is-' + entry.state);
    node.appendChild(T.el('h3', null, entry.state === 'option'
      ? 'This is one of two Masses the rubrics permit'
      : entry.state === 'additional'
        ? 'This is a further Mass of the same day'
        : entry.state === 'commemorated'
          ? 'This Mass is not said today; its collect is'
          : entry.state === 'displaced'
            ? 'This Mass is NOT said on this date'
            : 'This date is not settled here'));

    if (said && entry.state !== 'option' && entry.state !== 'additional') {
      node.appendChild(T.el('p', null,
        'What is said on this date is ' + said.label + '. You are reading ' +
        entry.label + ', which is shown here to be read and not to be celebrated.'));
    } else if (said && entry.state === 'additional') {
      node.appendChild(T.el('p', null,
        'It is said on this date in addition to ' + said.label +
        ', at another hour. It competes for the day with nothing.'));
    }
    const why = T.el('p', null, entry.why || '');
    node.appendChild(withLocus(why, entry.locus));
    return node;
  }

  /** The rubrical account of a choice, set in the margin like every other. */
  function choiceMargin(node, choice) {
    node.appendChild(T.el('h4', 'margin-heading', 'The choice the rubrics make'));
    node.appendChild(paragraph('margin-why', choice.why, choice.locus));
    if (choice.latin) node.appendChild(T.el('p', 'margin-latin', choice.latin));
    if (!choice.preferred && choice.openBecause) {
      node.appendChild(T.el('p', 'margin-why', choice.openBecause));
    }
    const list = T.el('ul', 'margin-list');
    for (const option of choice.among || []) {
      const item = T.el('li');
      item.appendChild(T.el('span', 'margin-name', option.label));
      if (choice.preferred === option.id) {
        item.appendChild(T.el('span', 'tag tag-commemorated', 'ordinarily said'));
      }
      item.appendChild(paragraph('margin-why', option.why, option.locus));
      list.appendChild(item);
    }
    node.appendChild(list);
  }

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
      // Which Mass is said on it, where that is not simply the day's own.
      const held = branch.winner.formulary;
      if (held && held.kind === 'borrowed') {
        node.appendChild(T.el('h4', 'margin-heading', 'The Mass it takes'));
        node.appendChild(T.el('p', 'margin-why',
          'This day prints no formulary of its own and takes ' + held.name + '.'));
        if (held.rule && held.rule.rule) {
          node.appendChild(T.el('p', 'margin-why', held.rule.rule));
        }
      } else if (held && held.kind === 'own' && held.printed) {
        node.appendChild(T.el('h4', 'margin-heading', 'The Mass it takes'));
        node.appendChild(paragraph('margin-why', held.why, held.locus));
        if (held.latin) node.appendChild(T.el('p', 'margin-latin', held.latin));
        node.appendChild(T.el('p', 'margin-why',
          'The Missal prints it under the heading “' + held.printed + '”.'));
        if (held.note) node.appendChild(T.el('p', 'margin-why', held.note));
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
    for (const choice of branch.massChoices || []) choiceMargin(node, choice);
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

  /**
   * Where the words under this heading were transcribed from.
   *
   * A recension is held as its DEPARTURES from another calendar and never as a
   * second copy of it, so on all but a handful of days the text below was read
   * out of the BASE's printing and out of no other. The heading names this
   * recension's own edition — "Missale Romanum, editio typica Vaticana 1920" —
   * and that name standing alone over a page every word of which came from a
   * 1962 printing is a claim about provenance that nobody made. So the mass
   * carries its own stamp, and the stamp is printed here beside the Mass it
   * belongs to rather than in the margin: it qualifies the TEXT, not the
   * reasoning about which text, and a reader who has the apparatus turned off
   * still needs it.
   *
   * Every field is read and none is inferred from another. `stated` says
   * whether this recension prints the entry itself; `text_from` names the
   * calendar that supplied it where it does not; `kind` and `basis` are the
   * departure as the source recorded it; and `also` carries the further kinds
   * of the SAME departure, each with its own basis, because one liturgy can
   * depart in several ways at once — the pre-1955 Holy Saturday is moved,
   * renamed, replaced and reslotted at the same time. A mass carrying no stamp
   * is a calendar that is nobody's recension, and nothing is said.
   *
   * The kind is printed as the source spells it. The vocabulary is closed in
   * `scripts/_calendars.py`, which is where its definitions live; a table of
   * friendlier words here would be a second copy of them, and it would drift
   * from the first the day a kind is added.
   *
   * Nothing on the page moves today, and that is the point: the missal control
   * is built from `structure/rubrics/index.json`, and a recension with no
   * rubrics source is not offered there. This is written now so that the day
   * the recension IS offered, its first reader is not shown a 1920 heading over
   * a 1962 transcription with nothing between them.
   */
  function departureRow(lead, row) {
    return T.el('p', 'row-meta',
      lead + ': ' + row.kind + (row.basis ? ' — ' + row.basis : ''));
  }

  function recensionRows(head, mass) {
    const held = mass && mass.recension;
    if (!held) return;
    if (held.text_from) {
      const base = missalNamed(held.text_from);
      head.appendChild(T.el('p', 'row-meta',
        'Text served from ' + ((base && (base.edition || base.label)) || held.text_from) +
        '. This recension states no text of its own here.'));
    } else if (held.stated) {
      head.appendChild(T.el('p', 'row-meta',
        'Text stated by this recension itself, and served from no other calendar.'));
    }
    if (held.kind) head.appendChild(departureRow('Departure', held));
    for (const row of held.also || []) {
      if (row && row.kind) head.appendChild(departureRow('Also', row));
    }
  }

  function renderBranch(branch, rubrics, derived, structure, bible, fragments, ordinary) {
    const section = T.el('section', 'branch');

    if (branch.option) {
      section.appendChild(T.el('h3', 'branch-option',
        'Where the option is “' + branch.option + '”'));
    }

    const warning = renderVerdictNotice(branch);
    if (warning) section.appendChild(warning);

    // The celebration name is the page title. This block now carries only the
    // source and resolution apparatus, which follows the Mass below.
    const head = T.el('div', 'mass-head');
    // The formulary said on the day, where it is not the day's own name. The
    // heading stays the DAY — "the Office of Our Lady on Saturday" — because
    // that is what the day is; the Mass is named under it.
    const taken = formularyOf(branch);
    // Resolved here rather than after the head, because the head is where the
    // Mass says where its text came from and it cannot say that without it.
    const mass = taken && taken.key
      ? (structure.masses || []).find((one) => one.key === taken.key)
      : null;
    if (taken && taken.key && taken.key !== (branch.winner && branch.winner.key)) {
      head.appendChild(T.el('p', 'row-meta', 'Mass: ' + (taken.name || taken.key)));
    }
    recensionRows(head, mass);
    // One control for everything the date carries, grouped by standing; the
    // reasoning goes to the margin with every other rubrical decision. The
    // control itself belongs in Settings, not in the ordered Mass.
    const selector = formularySelector(branch, () => render({ moveFocus: false }));
    if (selector) formularyControls.appendChild(selector);
    const apparatus = annotated(head, massMargin(branch, rubrics, derived));

    // A selected displaced or optional formulary must still qualify the words
    // immediately. This is a safety notice, not a generic "Not shown" notice.
    const standing = standingNotice(branch);
    if (standing) section.appendChild(standing);

    if (!branch.winner) {
      section.appendChild(apparatus);
      return section;
    }

    const series = branch.orations.all || branch.orations.low_mass || [];
    const subordinate = series.filter((one) => one.position > 1);
    // The oration slots — Collect, Secret, Postcommunion — under which a
    // commemoration is said. A different thing entirely from the Ordinary's
    // seats below, which are places in the frame; these are places in a series.
    const orationSlots = trackedSlots(branch, rubrics);
    const orationSlotFor = (name) => orationSlots.find((one) => one.slot === name) || null;

    /**
     * One proper of the day, with whatever the margin has to say beside it.
     *
     * `level` is the heading it sets at: h3 standing alone, and h5 inside the
     * Ordinary, where the divisions of the rite stand above it.
     */
    function renderMassProper(proper, seat, level) {
      const body = T.renderProper(proper, bible, fragments, {
        numbering: (structure && structure.numbering) || null,
        orations: state.orations,
        heading: level || 'h3',
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
      note.appendChild(document.createTextNode(taken && taken.key
        ? 'The propers structure carries no mass keyed ' + taken.key + '.'
        : 'It is constituted from its season and the calendar index carries no ' +
          'formulary of its own for it, and the year file appoints none for it ' +
          'to take.'));
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
    section.appendChild(apparatus);
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

  const variantGroupOf = Seating.variantGroupOf;

  /** The option chosen in each group, defaulting to the one the source marks. */
  function chosenOption(file, group) {
    return Seating.chosenOption(group, state.variants[group.group]);
  }

  /**
   * Whether an element is shown at all.
   *
   * An element with no `variant` belongs to the frame and always shows. One that
   * names an option shows only under that option — which is what makes the
   * control a choice between prayers rather than a filter over a list of them.
   */
  function elementShows(element, file) {
    const group = variantGroupOf(file);
    return Seating.elementShows(
      element, file, group && state.variants[group.group]
    );
  }

  /** A witness's acknowledgement, printed where its words are, never in a footer. */
  function witnessNote(file, sourceId) {
    return (file.translations || []).find((one) => one.source_id === sourceId) || null;
  }

  /** The languages this Ordinary speaks of, as its own file declares them. */
  function languagesOf(file) {
    return (file && file.languages) || [];
  }

  /** How many elements this frame carries, as its own file counts them. */
  function frameSize(file) {
    const first = languagesOf(file)[0];
    return first ? first.elements : 0;
  }

  /**
   * The language the Ordinary is read in.
   *
   * The reader's choice where the file offers it, and otherwise the first
   * language the file actually holds anything in — never simply the first
   * declared, which for a missal whose English is withheld would open the page
   * on a language it has not one word of.
   */
  function chosenLanguage(file) {
    const offered = languagesOf(file);
    return offered.find((one) => one.lang === state.ordinaryLang) ||
      offered.find((one) => one.held > 0) || offered[0] || null;
  }

  /**
   * How an element names the reason it is silent.
   *
   * The reason itself is stated once, in the preamble, with how many elements
   * it covers; here the element names it and no more. Printing the reason in
   * full at every element put a 700-character paragraph on the page 39 times
   * over the postconciliar frame, and would have put a 400-character one there
   * 195 times the moment a reader asked the 1962 Ordinary for its Latin. The
   * key is the handle this whole project withholds under — `absent: icel` —
   * and it is the thing a reader can carry back to the account above.
   */
  function absenceWord(file, key) {
    if (!key) {
      return 'This Ordinary holds none here and records no reason, which is a ' +
        'defect in its source rather than a silence about the rite.';
    }
    const found = (file.absences || []).find((one) => one.key === key);
    return found
      ? 'Withheld under “' + key + '”, which is stated above.'
      : 'Withheld under “' + key + '”.';
  }

  /**
   * The heading an element gets, or none.
   *
   * A rubric and a section head are printed matter and not prayers with names:
   * they carry no `name`, and the page used to fall back to the last segment
   * of the storage key, so `rubrica-sacerdos-ad-pedes-altaris` stood over the
   * priest's words as though the book had printed it. It did not. An element
   * with nothing to be called is set without a title, exactly as the missal
   * sets it, and its page or number rides with the text instead.
   */
  function elementHeading(element) {
    if (!element.name) return null;
    const heading = T.el(PART_HEADING, 'proper-name', element.name);
    // The speaker is deliberately NOT set here any more. It rode in the heading
    // as a small grey span, which meant the 9 elements that carry a speaker and
    // no name showed none at all, and the rest showed it where a reader looking
    // at the words was not looking. It is now set against the words themselves.
    if (element.locus) heading.appendChild(T.el('span', 'proper-ref', element.locus));
    return heading;
  }

  /* ------------------------------------------------------------------------
   * Who is speaking
   *
   * THE 1861 BOOK MIXES TWO AXES AND THIS IS WHY THE PAGE WAS HARD TO READ.
   * `P.` marks the PRIEST — a person. `R.` marks a RESPONSE — a position in a
   * dialogue, whoever makes it. They are not two values of one thing, and the
   * book prints them in one column as though they were:
   *
   *   priest   P. I confess to Almighty God, &c.
   *   server   R. May Almighty God be merciful to thee…
   *   server   R. I confess to Almighty God…
   *   priest   P. May Almighty God be merciful unto you…
   *
   * In the fourth row the priest's `P.` line IS the response to the server. So
   * setting every `P.` as ℣ would put "versicle" over a response — and in two
   * rubric elements `P.` is not a speaker mark at all but an abbreviation
   * inside running text ("is said the P. COMMUNION"). Neither letter can be
   * mapped onto the ℣/℟ axis, and this renders each as the word it abbreviates.
   *
   * THE MARKS ARE NOT MERELY DROPPED, and this is the part that is easy to get
   * wrong. 28 of the 39 marked elements hold a two-party dialogue inside ONE
   * element — "P. The Lord be with you. R. And with thy spirit." carries
   * `speaker: priest`, which names the first line only. Drop every mark and the
   * server's responses are printed as the priest's words. So a LEADING mark,
   * which only repeats the element's own speaker, goes; an INTERIOR mark, which
   * is the one thing recording that the speaker changed mid-element, stays and
   * is set as a speaker tag like the first.
   *
   * Nothing upstream is edited: the artifacts keep what the book prints.
   * --------------------------------------------------------------------- */

  const SPEAKER_WORDS = { priest: 'Priest', server: 'Server', all: 'All' };
  const MARK_WORDS = { 'P.': 'Priest', 'R.': 'Response' };
  // Only where a mark can be a speaker at all. A rubric is printed matter about
  // the Mass, not words said in it, and it is where both false positives live.
  const SPOKEN_KINDS = { dialogue: true, prayer: true, form: true };
  const A_MARK = /(^|[.;:,!?)\]"'’”]\s+|\n\s*)(P\.|R\.)(?=\s|$)/g;

  function speakerTag(word, speaker) {
    return T.el('span', 'speaker-tag' + (speaker ? ' is-' + speaker : ''), word);
  }

  /**
   * One element's words, with every change of speaker made plain.
   *
   * Returns a fragment. The element's own speaker opens it; a mark inside the
   * text opens each further turn.
   */
  function spoken(element, text) {
    const source = String(text === null || text === undefined ? '' : text);
    if (!SPOKEN_KINDS[element.kind]) return T.versicled(source);

    const fragment = document.createDocumentFragment();
    const opening = SPEAKER_WORDS[element.speaker] || null;
    if (opening) fragment.appendChild(speakerTag(opening, element.speaker));

    let at = 0;
    let found;
    let first = true;
    A_MARK.lastIndex = 0;
    while ((found = A_MARK.exec(source)) !== null) {
      const word = MARK_WORDS[found[2]];
      const start = found.index + found[1].length;
      // A mark at the head of an element whose speaker is already announced is
      // furniture and goes — including `R.` on the server's own lines, where
      // "Server" and "Response" are both true and printing both said one thing
      // twice. An INTERIOR mark is never dropped: it is the only record that
      // the speaker changed inside the element.
      const leading = first && source.slice(0, start).trim() === '';
      first = false;
      if (leading && opening) { at = start + found[2].length; continue; }
      // Genuine V./R. marks inside the words still become ℣/℟. Returning
      // early to `T.versicled` for unspoken kinds only meant a prayer, a form
      // or a dialogue never reached it, and every versicle the book prints
      // inside one lost its glyph.
      if (start > at) fragment.appendChild(T.versicled(source.slice(at, start)));
      fragment.appendChild(speakerTag(word, word === 'Priest' ? 'priest' : null));
      at = start + found[2].length;
    }
    // The space that followed the mark is the mark's own spacing, and left in
    // place it opened every turn with a double space.
    const rest = source.slice(at);
    const tail = at === 0 ? rest : rest.replace(/^[ \t]+/, '');
    if (tail) fragment.appendChild(T.versicled(tail));
    return fragment;
  }

  function renderElement(element, file) {
    // The kind rides on the class, because how a missal sets an element is
    // decided by what kind of thing it is: a rubric in italic, a head across
    // the measure, a prayer in the reading face. Who says it is on the heading,
    // where the reader is looking when they want to know.
    const section = T.el('section', 'proper ordinary-element is-' + element.kind);

    const heading = elementHeading(element);
    if (heading) section.appendChild(heading);

    const language = chosenLanguage(file);
    const translations = element.translations || [];
    const held = language
      ? translations.find((one) => one.lang === language.lang) || null
      : null;
    if (held) {
      // No label above the words. "Composed text — not scripture" is true of
      // every element of an Ordinary, so saying it 195 times said nothing 194
      // of those times; what distinguishes a rubric from a prayer here is how
      // it is set, which is what distinguishes them in the book.
      const body = T.el('p', element.kind === 'heading' ? 'ordinary-head' : 'composed');
      if (!heading && element.locus) {
        body.appendChild(T.el('span', 'ordinary-locus', element.locus));
      }
      // Speaker tags are set here and nowhere upstream: the artifacts hold what
      // the book prints, and the book prints "P." and "R." in one column.
      body.appendChild(spoken(element, held.text));
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
    // is then the sole thing identifying which prayer this is. And only where
    // it is not already the heading: an element the artifact names by its own
    // incipit carries one string in both fields, and printing it twice says the
    // same thing twice under two settings.
    if (!held && element.latin_incipit && element.latin_incipit !== element.name) {
      const incipit = T.el('p', 'proper-incipit', element.latin_incipit);
      incipit.lang = 'la';
      section.appendChild(incipit);
    }

    // Which languages this element does not answer, and under what reason.
    //
    // The one the reader asked for is always said, so a chosen language that
    // is empty here can never be silently empty — which is the whole of the
    // postconciliar case, where 39 of 48 elements are withheld under ICEL. The
    // others are said only where the element holds nothing in any language at
    // all; there the reader is looking at an incipit and is owed the entire
    // account of why, and everywhere else the count stands in the preamble
    // rather than under 195 elements that do have their words.
    const anywhere = translations.length > 0;
    for (const one of languagesOf(file)) {
      if (translations.some((row) => row.lang === one.lang)) continue;
      if (anywhere && (!language || one.lang !== language.lang)) continue;
      section.appendChild(T.notice(
        'its ' + T.languageName(one.lang) + '. ' +
        absenceWord(file, (element.absent || {})[one.absent])));
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
   *
   * Two kinds of thing were mixed here and are now separated, because a reader
   * opening the page to follow the Mass met about three thousand characters
   * before a word of any prayer. What the reader must see is the standing —
   * what this book is, whose English it is, on what condition, and what is
   * withheld and how much of it. How the file was arrived at is apparatus: it
   * goes in the margin with the rest of the reasoning, where the same toggle
   * governs it as governs everything else of that kind.
   */
  function ordinaryPreamble(file) {
    const body = T.el('div', 'mass-head');
    // Named for where it now stands. It used to head the page, so "The Ordinary
    // of the Mass" was a title; at the foot it is a note about the frame the
    // reader has just read the Mass in, and it says so.
    body.appendChild(T.el('h3', 'mass-name', 'About this Ordinary: ' + file.title));

    const language = chosenLanguage(file);
    body.appendChild(T.el('p', 'entry-meta', [
      file.edition_short || file.edition,
      'the frame the day’s propers are set into',
      language ? 'read in ' + T.languageName(language.lang) : null
    ].filter(Boolean).join(' · ')));

    body.appendChild(T.el('p', 'row-meta', file.advisory));

    // One line per witness, carrying its label and the caution it travels
    // under. The label used to be printed twice — once as "Translation: …" and
    // again at the head of its own caution — which is one fact in two places
    // and the first step towards two facts.
    for (const witness of file.translations || []) {
      if (!witness.label) continue;
      body.appendChild(T.el('p', 'row-meta',
        witness.label + (witness.caution ? ' — ' + witness.caution : '')));
    }

    // What this Ordinary withholds, said once, with how many elements each
    // reason covers. Every element that is silent names one of these, so the
    // account is on the page exactly once and every silence points at it.
    for (const absence of file.absences || []) {
      const line = T.el('p', 'row-meta ordinary-absence');
      line.appendChild(T.el('span', 'ordinary-absence-key', absence.key));
      line.appendChild(document.createTextNode(
        absence.count + ' of ' + frameSize(file) + ' elements. ' + absence.what));
      body.appendChild(line);
    }

    const group = variantGroupOf(file);
    const chosen = group && chosenOption(file, group);
    if (group && chosen) {
      body.appendChild(T.el('p', 'row-meta',
        group.name + ': ' + chosen.name + '. ' + group.what));
    }

    const wrapper = T.el('section', 'ordinary-preamble');
    wrapper.appendChild(annotated(body, ordinaryMargin(file)));
    return wrapper;
  }

  /** How this frame was arrived at: apparatus, and behind the same toggle. */
  function ordinaryMargin(file) {
    const node = margin('Ordinary resolution');
    if (file.derived_from) node.appendChild(T.el('p', 'margin-why', file.derived_from));
    // Where the seats came from. A page that sets one book's propers into
    // another book's frame owes the reader that sentence.
    if (file.slots_derived_from) {
      node.appendChild(T.el('p', 'margin-why', file.slots_derived_from));
    }
    return node;
  }

  /**
   * The elements this frame is actually showing, in order.
   *
   * Which they are depends on the reader's choice of Eucharistic Prayer, which
   * is why a seat is resolved against this list and not against the file.
   */
  function shownElements(file) {
    const group = variantGroupOf(file);
    return Seating.shownElements(file, group && state.variants[group.group]);
  }

  /**
   * The declared seats, resolved to positions among the elements on screen.
   *
   * `at[n]` is the index a proper seated by slot `n` is inserted at: an `after`
   * puts it one place further on than a `before` on the same element, which is
   * how two slots on neighbouring elements land in one position without either
   * being ambiguous about which element it named.
   */
  const seats = Seating.seats;

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
    return Seating.seatPropers(propers, seating, T.isPlaceholder);
  }

  const massEvents = Seating.massEvents;

  /** The frame, with the day's propers set into it. */
  function renderFrame(file, propers, renderMassProper) {
    const wrapper = T.el('section', 'ordinary-frame');
    const shown = shownElements(file);
    const placed = seatPropers(propers, seats(file, shown));

    const announced = { before: false, after: false };
    for (const event of massEvents(shown, placed)) {
      if (event.kind === 'begin_section') {
        wrapper.appendChild(T.el(DIVISION_HEADING, 'mass-subheading ordinary-division',
          event.section.name));
      } else if (event.kind === 'ordinary_element') {
        wrapper.appendChild(renderElement(event.element, file));
      } else if (event.kind === 'proper') {
        if (event.placement === 'before' && !announced.before) {
          announced.before = true;
          wrapper.appendChild(T.el('p', 'row-meta ordinary-aside',
            'This Mass opens with propers the Ordinary appoints no place for. They ' +
            'are shown first, in the missal’s own order.'));
        } else if (event.placement === 'after' && !announced.after) {
          announced.after = true;
          wrapper.appendChild(T.el('p', 'row-meta ordinary-aside',
            'From here the day’s propers no longer run forward through the Ordinary: ' +
            'this day carries more than one formulary, or its rite departs from the ' +
            'frame. The rest is shown in the missal’s own order, unseated and ' +
            'unreordered.'));
        }
        // Inside the frame a proper is a part of the Mass beside the parts that
        // never change, so both set at the same heading level.
        wrapper.appendChild(
          renderMassProper(event.proper, event.seat, PART_HEADING));
      }
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
   * The Ordinary's language control, filled from the Ordinary's own file.
   *
   * A language nothing is held in is still offered, and says so in its label.
   * That is not an oversight: the postconciliar frame holds nine elements of
   * forty-eight and the Latin of neither missal is here at all, and choosing an
   * empty language is how a reader sees, element by element and at the place
   * each falls due, under what recorded reason it is empty. A control that
   * hid them would leave the reader to conclude the texts do not exist.
   */
  function fillOrdinaryLanguageSelect(file) {
    const offered = languagesOf(file);
    if (!state.ordinary || offered.length < 2) {
      ordinaryLangField.hidden = true;
      return;
    }
    T.fillSelect(ordinaryLangSelect, offered.map((one) => ({
      value: one.lang,
      label: T.languageName(one.lang) + (one.held
        ? ' — ' + one.held + ' of ' + one.elements
        : ' — none held'),
      title: one.lang
    })));
    const chosen = chosenLanguage(file);
    if (chosen) ordinaryLangSelect.value = chosen.lang;
    ordinaryLangField.hidden = false;
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
    rubricsToggle.checked = state.showRubrics;
    applyWhy();
    applyRubrics();
  }

  // The margins stay in the DOM and are hidden by a class rather than removed,
  // so toggling costs no re-render and a reader turning them back on lands on
  // the same page rather than a rebuilt one.
  function applyWhy() {
    document.body.classList.toggle('shows-why', state.why);
  }

  /**
   * The priest's actions, shown or hidden.
   *
   * By a class on the body, for the same reason the margins are, and for one
   * more that matters here: the rubrics are what the slots are anchored to.
   * `praeparatio/rubrica-benedictio-incensi-et-introitus` is the element the
   * Introit is seated after. Filtering the rubrics out of the frame before it
   * was seated would take those anchors with them and unseat the propers they
   * carry — the Mass would still render, in a plausible and wrong order. So
   * they are seated first and hidden afterwards, and hiding is only ever a
   * matter of what is painted.
   *
   * The class marks the DEPARTURE and not the default, unlike `shows-why`,
   * because the defaults are opposite: the reasoning is off until asked for and
   * the rubrics are on until turned off. A class meaning "show" with a default
   * of shown would have hidden the priest's actions in the moment before this
   * ran, and on any page where it never ran at all.
   */
  function applyRubrics() {
    document.body.classList.toggle('hides-rubrics', !state.showRubrics);
  }

  function writeHash() {
    const pairs = [
      ['date', state.date],
      ['missal', state.missalId],
      ['bible', state.bibleId],
      ['orations', state.orations === T.SOURCE_LANGUAGE ? null : state.orations],
      ['why', state.why ? '1' : null],
      ['ordinary', state.ordinary ? '1' : null],
      ['ordinary-lang', state.ordinaryLang],
      // Only when turned off: the hash carries departures from the page as it
      // opens, and the rubrics are on as it opens.
      ['rubrics', state.showRubrics ? null : '0'],
      // So a displaced Mass can be linked to. `standingNotice` is what makes
      // that safe: it states the displacement to whoever follows the link.
      ['mass', state.shownMass]
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

    // Every citation every branch's Mass needs, fetched in one pass. EVERY
    // formulary the date carries is fetched, not only the one on screen:
    // switching the selector must not send the reader back to the network for a
    // Mass the page already knew it might be asked for.
    const wanted = [];
    for (const branch of derived.options) {
      for (const row of branch.readable || []) {
        const mass = (structure.masses || []).find((one) => one.key === row.key);
        if (mass) for (const citation of T.citationsOf(mass)) wanted.push(citation);
      }
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
    T.clear(renderedNotices);
    T.clear(formularyControls);
    renderHead(derived, bible);

    // The frame is settled before a word of any Mass is drawn, because each
    // Mass is drawn inside it. Where there is no frame the Masses render as
    // they always did — a missing Ordinary withholds nothing but itself.
    const frame = ordinary && ordinary.ok ? ordinary.value : null;
    fillOrdinaryLanguageSelect(frame);
    fillVariantSelect(frame);
    // The rubrics belong to the frame, so the control for them appears with it.
    rubricsField.hidden = !frame;
    if (!frame && ordinary) {
      renderedNotices.appendChild(T.notice(
        'the Ordinary of this missal. It could not be loaded: ' + ordinary.message));
    } else if (state.ordinary) {
      renderedNotices.appendChild(T.notice(
        'the Ordinary of this missal. This corpus carries none for “' +
        state.missalId + '”.'));
    }

    for (const branch of derived.options) {
      reading.appendChild(
        renderBranch(branch, rubrics, derived, structure, bible, held.fragments, frame));
    }
    // The standing matter goes UNDER the Mass, not over it. What this book is,
    // whose English it is, on what condition and what it withholds are all true
    // and none of them is what a reader opened the page for: this page is meant
    // to be usable at Mass, and three thousand characters of provenance before
    // the first prayer is a page you cannot use at Mass. Facts first.
    if (frame) reading.appendChild(ordinaryPreamble(frame));
    updateNoticesDisclosure();
    rebuildContents();
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
    // A choice belongs to the day it was offered on. Carrying an answer across
    // a date or a missal change would apply a reader's decision to a rubric
    // that never asked the question.
    if ((date && date !== state.date) || (missalId && missalId !== state.missalId)) {
      state.shownMass = null;
    }
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
    // A language asked for is taken as asked and checked when the Ordinary
    // arrives: no Ordinary has been fetched yet, and the set of languages is
    // the file's to state, not this function's to assume.
    state.ordinaryLang = hash.get('ordinary-lang') || null;
    state.showRubrics = hash.get('rubrics') !== '0';
    // Taken as asked and resolved against the date's own formularies in
    // `shownEntry`; nothing here knows yet what this date carries.
    state.shownMass = hash.get('mass') || null;
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

  // A re-render, because the words themselves change: which text an element
  // holds, and what it says where it holds none, are both settled at build.
  ordinaryLangSelect.addEventListener('change', () => {
    state.ordinaryLang = ordinaryLangSelect.value;
    select(null, null, { moveFocus: false });
  });

  // No re-render: the rubrics stay in the DOM, still anchoring the seats, and
  // only stop being painted.
  rubricsToggle.addEventListener('change', () => {
    state.showRubrics = rubricsToggle.checked;
    applyRubrics();
    rebuildContents();
    writeHash();
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
    state.ordinaryLang = hash.get('ordinary-lang') || null;
    state.showRubrics = hash.get('rubrics') !== '0';
    // Taken as asked and resolved against the date's own formularies in
    // `shownEntry`; nothing here knows yet what this date carries.
    state.shownMass = hash.get('mass') || null;
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
