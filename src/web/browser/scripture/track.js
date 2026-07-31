/* ===========================================================================
 * One track of the reading plan, read as a course
 * ===========================================================================
 *
 * A track is a tier — overview, narrative, year — and this page is the whole of
 * it: an orientation, twelve periods, and the readings in order. It is not a
 * lookup tool with a dropdown of tiers. A reader arrives at a track, is told
 * what it is, how long it takes and what it refuses to include, and then walks
 * it, always able to say where they are.
 *
 * THREE VIEWS, ONE PAGE, NO PRE-RENDERING
 *
 *   orientation   the track: what it is, its pace, its omissions, its periods
 *   period        one period: its summary and its readings in sequence
 *   reading       one reading: its note, its text, and its neighbours
 *
 * They are views and not files. 357 readings times three tracks times every
 * translation is a number that grows every time the plan changes; the shared
 * machinery's header says why that was refused, and this page does not
 * reintroduce it. Every view is instead addressable through the hash, so a
 * reading can be bookmarked, linked and shared exactly as a file could:
 *
 *   #tier=narrative                          the orientation
 *   #tier=narrative&period=exile             one period
 *   #tier=narrative&reading=47&bible=douay-rheims   one reading
 *
 * Nothing in this file re-implements the shared machinery: the chapter cache,
 * the numbering-aware loci, the four failure renderings, the render token and
 * the hash mechanics are all ../shared/browser-core.js. What is here is the
 * vocabulary of a course — tracks, periods, position, continuity — and the
 * plan's own arithmetic is in plan-model.js, which the front door shares.
 *
 *   ?data=<root>   where the corpus lives (default ../browse; ?data=fixture
 *                  serves the sample corpus in ../fixture)
 *   ?plan=<id>     which plan to read (default: narrative-spine)
 * ======================================================================== */

'use strict';

(function () {
  const T = window.Triptych;
  const P = window.ScripturePlan;

  const state = {
    bibles: [],
    bibleId: null,
    plan: null,
    tier: null,
    view: 'orient',
    readingKey: null,
    periodKey: null,
    // A one-off explanation owed to the reader when the track they asked for
    // could not hold the reading they named. Consumed by the next render.
    notice: null
  };

  const trackSelect = document.getElementById('track-select');
  const readingSelect = document.getElementById('reading-select');
  const bibleSelect = document.getElementById('bible-select');
  const prevButton = document.getElementById('prev-button');
  const nextButton = document.getElementById('next-button');
  const content = document.getElementById('reading');
  const controls = document.getElementById('controls');
  const rail = document.getElementById('rail');
  const railList = document.getElementById('rail-list');
  const trackName = document.getElementById('track-name');
  const trackLede = document.getElementById('track-lede');
  const planLink = document.getElementById('plan-link');

  /* ------------------------------------------------------------------------
   * Where we are
   * --------------------------------------------------------------------- */

  function currentTrack() {
    return P.track(state.plan, state.tier);
  }

  function currentEntry() {
    if (!state.readingKey) return null;
    return P.entryAt(currentTrack(), state.readingKey);
  }

  function currentPeriod() {
    if (state.view === 'reading') {
      const entry = currentEntry();
      return entry ? entry.period : null;
    }
    if (state.view === 'period' && state.periodKey) {
      return P.periodAt(currentTrack(), state.periodKey);
    }
    return null;
  }

  function currentBible() {
    return state.bibles.find((bible) => bible.id === state.bibleId) || null;
  }

  /* ------------------------------------------------------------------------
   * Addresses
   *
   * Every internal link is an ordinary href built here, and every link the page
   * writes into the hash is built from the same pairs, so that a link a reader
   * copies out of the address bar and a link they copy off the page are the
   * same link.
   * --------------------------------------------------------------------- */

  function hashPairs(over) {
    const at = {
      tier: state.tier,
      view: state.view,
      reading: state.readingKey,
      period: state.periodKey,
      bible: state.bibleId
    };
    if (over) for (const key of Object.keys(over)) at[key] = over[key];

    const pairs = [['tier', at.tier]];
    if (at.view === 'reading') pairs.push(['reading', at.reading]);
    else if (at.view === 'period') pairs.push(['period', at.period]);
    pairs.push(['bible', at.bible]);
    return pairs;
  }

  function href(over) {
    const parts = [];
    for (const [key, value] of hashPairs(over)) {
      if (value === null || value === undefined || value === '') continue;
      parts.push(key + '=' + encodeURIComponent(value));
    }
    return '#' + parts.join('&');
  }

  function link(text, over, className) {
    const anchor = T.el('a', className || null, text);
    anchor.href = href(over);
    return anchor;
  }

  /* ------------------------------------------------------------------------
   * Controls
   * --------------------------------------------------------------------- */

  function fillTrackSelect() {
    T.fillSelect(trackSelect, P.tiers(state.plan).map((tier) => {
      const view = P.track(state.plan, tier);
      return {
        value: tier,
        label: view.label + ' — ' + P.plural(view.count, 'reading')
      };
    }));
    if (state.tier) trackSelect.value = state.tier;
  }

  function fillReadingSelect() {
    // The plan's own order, grouped by period. Never sorted by title: the plan
    // is a sequence, and its sequence is the point of it.
    T.fillSelect(readingSelect, currentTrack().readings.map((entry) => ({
      value: entry.key,
      label: entry.index + '. ' + entry.title,
      group: entry.period.label,
      title: entry.reference
    })));
    if (state.readingKey) readingSelect.value = state.readingKey;
  }

  function syncControls() {
    const view = currentTrack();
    if (state.tier) trackSelect.value = state.tier;
    if (state.readingKey) readingSelect.value = state.readingKey;
    if (state.bibleId) bibleSelect.value = state.bibleId;

    // The step buttons step through whatever the reader is looking at: readings
    // inside a reading, periods inside a period. On the orientation there is no
    // sequence to step through, and saying so beats a button that does nothing.
    let at = -1;
    let total = 0;
    let unit = '';
    if (state.view === 'reading') {
      const entry = currentEntry();
      at = entry ? entry.index - 1 : -1;
      total = view.count;
      unit = 'reading';
    } else if (state.view === 'period') {
      const period = currentPeriod();
      at = period ? period.index - 1 : -1;
      total = view.periods.length;
      unit = 'period';
    }

    prevButton.disabled = at <= 0;
    nextButton.disabled = at < 0 || at >= total - 1;
    prevButton.setAttribute('aria-label', unit ? 'Previous ' + unit : 'Previous');
    nextButton.setAttribute('aria-label', unit ? 'Next ' + unit : 'Next');
  }

  /* ------------------------------------------------------------------------
   * The period rail — the map, on screen whatever the reader is looking at
   * --------------------------------------------------------------------- */

  function renderRail(view) {
    T.clear(railList);
    const here = currentPeriod();

    for (const period of view.periods) {
      const item = T.el('li', 'rail-item');
      const anchor = link('', { view: 'period', period: period.key }, 'rail-link');

      const number = T.el('span', 'rail-num', String(period.index));
      number.setAttribute('aria-hidden', 'true');
      anchor.appendChild(number);
      anchor.appendChild(T.el('span', 'rail-label', period.label));
      anchor.appendChild(T.el('span', 'visually-hidden',
        ', ' + P.plural(period.readings.length, 'reading')));
      anchor.setAttribute('title',
        period.label + ' — ' + P.plural(period.readings.length, 'reading'));

      if (here && here.key === period.key) {
        item.classList.add('is-here');
        anchor.setAttribute('aria-current', 'true');
      } else if (here && period.index < here.index) {
        item.classList.add('is-earlier');
      }

      item.appendChild(anchor);
      railList.appendChild(item);
    }
    rail.hidden = false;
  }

  /* ------------------------------------------------------------------------
   * Shared furniture
   * --------------------------------------------------------------------- */

  function crumbs(view, here) {
    const nav = T.el('nav', 'crumbs');
    nav.setAttribute('aria-label', 'Breadcrumb');
    nav.appendChild(link(view.label + ' track', { view: 'orient' }, 'crumb'));
    if (here) {
      nav.appendChild(T.el('span', 'crumb-sep', '›'));
      nav.appendChild(link(here.label, { view: 'period', period: here.key }, 'crumb'));
    }
    return nav;
  }

  function heading(level, text, className) {
    return T.el(level, className || 'view-title', text);
  }

  function section(title) {
    const node = T.el('section', 'orient-block');
    node.appendChild(T.el('h3', 'orient-title', title));
    return node;
  }

  /* ------------------------------------------------------------------------
   * The orientation
   *
   * A track opens with what it is, how long it takes, and what it deliberately
   * leaves out — in that order, and before any scripture. The omissions prose
   * is here in full and not behind a disclosure: an abridgement that hides its
   * own account of itself is the thing this plan refuses to be.
   * --------------------------------------------------------------------- */

  function figuresLine(view) {
    return [
      P.plural(view.count, 'reading'),
      P.plural(view.chapters, 'chapter'),
      P.plural(view.books, 'book')
    ].join(' · ');
  }

  function nestingLine(view) {
    const all = P.tiers(state.plan).map((tier) => P.track(state.plan, tier));
    const at = all.findIndex((held) => held.tier === view.tier);
    const wider = all.slice(at + 1);
    if (!wider.length) {
      return 'This is the fullest of the plan\'s tracks: nothing the plan holds ' +
        'is kept back from it. The plan itself is still an abridgement, and ' +
        'what follows is its own account of what it does not read at any depth.';
    }
    const said = wider.map((held) => {
      return 'the ' + held.label.toLowerCase() + ' track reads ' + held.count +
        ', ' + (held.count - view.count) + ' more than this one';
    });
    return 'This track holds ' + view.count + ' of the plan\'s ' +
      all[all.length - 1].count + ' readings: ' + said.join(', and ') +
      '. Beyond that, the plan itself is an abridgement, and what follows is ' +
      'its own account of what it does not read at any depth.';
  }

  function pacingTable(view) {
    const table = T.el('table', 'pacing');
    const caption = T.el('caption', 'visually-hidden',
      'How long the ' + view.label + ' track takes at three paces');
    table.appendChild(caption);

    const head = T.el('thead');
    const headRow = T.el('tr');
    const pace = T.el('th', null, 'Pace');
    pace.setAttribute('scope', 'col');
    const takes = T.el('th', null, 'Finishes in');
    takes.setAttribute('scope', 'col');
    headRow.appendChild(pace);
    headRow.appendChild(takes);
    head.appendChild(headRow);
    table.appendChild(head);

    const body = T.el('tbody');
    for (const row of P.pacing(view.count)) {
      const line = T.el('tr');
      const label = T.el('th', null, row.pace);
      label.setAttribute('scope', 'row');
      line.appendChild(label);
      line.appendChild(T.el('td', null, row.takes));
      body.appendChild(line);
    }
    table.appendChild(body);
    return table;
  }

  function contentsList(view) {
    const list = T.el('ol', 'contents');
    for (const period of view.periods) {
      const item = T.el('li', 'contents-item');

      const head = T.el('p', 'contents-head');
      head.appendChild(
        link(period.label, { view: 'period', period: period.key }, 'contents-link')
      );
      item.appendChild(head);

      item.appendChild(T.el('p', 'contents-meta', [
        'Period ' + period.index + ' of ' + period.total,
        P.plural(period.readings.length, 'reading') +
          ' (' + period.first + '–' + period.last + ' of ' + view.count + ')',
        P.plural(period.chapters, 'chapter')
      ].join(' · ')));

      if (period.summary) {
        item.appendChild(
          T.el('p', 'contents-line', P.firstSentence(period.summary))
        );
      }
      list.appendChild(item);
    }
    return list;
  }

  function renderOrientation(view) {
    content.appendChild(heading('h2', 'Before you begin'));

    const what = section('What this track is');
    what.appendChild(T.el('p', 'figures', figuresLine(view)));
    if (view.description) what.appendChild(P.prose(view.description));
    content.appendChild(what);

    const first = view.readings.length ? view.readings[0] : null;
    if (first) {
      const start = T.el('p', 'begin');
      start.appendChild(link(
        'Begin at reading 1 — ' + first.title,
        { view: 'reading', reading: first.key },
        'begin-link'
      ));
      const held = currentEntry();
      if (held && held.index > 1) {
        const again = T.el('p', 'begin-again');
        again.appendChild(document.createTextNode('Or return to reading '));
        again.appendChild(link(
          held.index + ' — ' + held.title,
          { view: 'reading', reading: held.key }
        ));
        again.appendChild(document.createTextNode('.'));
        start.appendChild(again);
      }
      content.appendChild(start);
    }

    const pace = section('How long it takes');
    pace.appendChild(T.el('p', 'orient-lead',
      'At one reading a sitting, and counting nothing else.'));
    pace.appendChild(pacingTable(view));
    content.appendChild(pace);

    const cost = section('What it leaves out');
    cost.appendChild(T.el('p', 'orient-lead', nestingLine(view)));
    if (state.plan.omissions) cost.appendChild(P.prose(state.plan.omissions));
    content.appendChild(cost);

    if (state.plan.precedents) {
      const from = section('Where the selection comes from');
      from.appendChild(P.prose(state.plan.precedents));
      content.appendChild(from);
    }

    const periods = section('The twelve periods');
    periods.appendChild(T.el('p', 'orient-lead',
      'The periods are the spine of the story. Each holds its own readings in ' +
      'sequence, and each opens with an account of the arc it covers.'));
    periods.appendChild(contentsList(view));
    content.appendChild(periods);

    document.title = view.label + ' track — The Story of Salvation — Triptych';
    T.statusLine(
      'The ' + view.label + ' track: ' + figuresLine(view) + ', in ' +
      view.periods.length + ' periods.'
    );
  }

  /* ------------------------------------------------------------------------
   * A period
   * --------------------------------------------------------------------- */

  function tierBadge(view, entry) {
    if (P.tierRank(entry.tier) >= P.tierRank(view.tier)) return null;
    const badge = T.el('span', 'tier-badge', P.tierLabel(state.plan, entry.tier));
    badge.setAttribute('title',
      'First appears at the ' + P.tierLabel(state.plan, entry.tier) + ' track');
    return badge;
  }

  function entryItem(view, entry) {
    const item = T.el('li', 'entry-item');

    const head = T.el('p', 'entry-item-head');
    head.appendChild(link(entry.title, { view: 'reading', reading: entry.key },
      'entry-item-link'));
    const badge = tierBadge(view, entry);
    if (badge) head.appendChild(badge);
    item.appendChild(head);

    item.appendChild(T.el('p', 'entry-item-ref', entry.reference));
    if (entry.note) item.appendChild(T.el('p', 'entry-item-note', entry.note));
    return item;
  }

  function periodSteps(view, period) {
    const nav = T.el('nav', 'period-steps');
    nav.setAttribute('aria-label', 'The periods either side');

    const before = view.periods[period.index - 2];
    const after = view.periods[period.index];

    const back = T.el('p', 'period-step');
    if (before) {
      back.appendChild(T.el('span', 'period-step-label', 'Before'));
      back.appendChild(link(before.label, { view: 'period', period: before.key }));
    } else {
      back.appendChild(T.el('span', 'period-step-label', 'Before'));
      back.appendChild(T.el('span', 'period-step-none', 'The story starts here.'));
    }
    nav.appendChild(back);

    const on = T.el('p', 'period-step period-step-on');
    on.appendChild(T.el('span', 'period-step-label', 'After'));
    if (after) {
      on.appendChild(link(after.label, { view: 'period', period: after.key }));
    } else {
      on.appendChild(T.el('span', 'period-step-none', 'The story ends here.'));
    }
    nav.appendChild(on);

    return nav;
  }

  function renderPeriod(view, period) {
    content.appendChild(crumbs(view, null));
    content.appendChild(heading('h2', period.label, 'entry-title'));

    content.appendChild(T.el('p', 'entry-meta', [
      'Period ' + period.index + ' of ' + period.total,
      P.plural(period.readings.length, 'reading') +
        ' — ' + period.first + '–' + period.last + ' of ' + view.count +
        ' in the ' + view.label + ' track',
      P.plural(period.chapters, 'chapter')
    ].join(' · ')));

    if (period.summary) content.appendChild(P.prose(period.summary, 'period-summary'));

    const badged = period.readings.some((entry) => tierBadge(view, entry));
    if (badged) {
      content.appendChild(T.el('p', 'legend',
        'A badge marks a reading that also belongs to a smaller track: those ' +
        'are the hinges the shorter readings of the plan are built from.'));
    }

    const list = T.el('ol', 'entry-list');
    for (const entry of period.readings) list.appendChild(entryItem(view, entry));
    content.appendChild(list);

    content.appendChild(periodSteps(view, period));

    document.title = period.label + ' — ' + view.label + ' track — Triptych';
    T.statusLine(
      period.label + ', period ' + period.index + ' of ' + period.total +
      ', ' + P.plural(period.readings.length, 'reading') + ' in the ' +
      view.label + ' track.'
    );
  }

  /* ------------------------------------------------------------------------
   * A reading
   *
   * Position, then the teaching, then the text, then the thread. The note is
   * not a footnote: 106 of the plan's readings carry one, and it is the only
   * place the plan says why a passage is here and what to watch for.
   * --------------------------------------------------------------------- */

  function progressBar(view, entry) {
    const bar = T.el('div', 'progress');
    bar.setAttribute('aria-hidden', 'true');
    const fill = T.el('span', 'progress-fill');
    fill.style.width = (entry.index / view.count * 100).toFixed(2) + '%';
    bar.appendChild(fill);
    return bar;
  }

  function neighbourSide(label, neighbour, entry) {
    const box = T.el('div', 'continuity-side');
    box.appendChild(T.el('p', 'continuity-label', label));
    if (!neighbour) {
      box.appendChild(T.el('p', 'continuity-none',
        label === 'Before' ? 'This is where the track begins.'
          : 'This is where the track ends.'));
      return box;
    }
    const title = T.el('p', 'continuity-title');
    title.appendChild(link(neighbour.title, { view: 'reading', reading: neighbour.key }));
    box.appendChild(title);
    box.appendChild(T.el('p', 'continuity-ref', neighbour.reference));
    if (neighbour.period.key !== entry.period.key) {
      box.appendChild(T.el('p', 'continuity-cross',
        (label === 'Before' ? 'Last of ' : 'First of ') + neighbour.period.label));
    }
    return box;
  }

  function continuity(view, entry) {
    const nav = T.el('nav', 'continuity');
    nav.setAttribute('aria-label', 'What comes before and after this reading');
    nav.appendChild(neighbourSide('Before', view.readings[entry.index - 2], entry));
    nav.appendChild(neighbourSide('After', view.readings[entry.index], entry));
    return nav;
  }

  function renderReading(view, entry, bible, held) {
    content.appendChild(crumbs(view, entry.period));

    if (state.notice) {
      content.appendChild(T.el('p', 'diverted', state.notice));
      state.notice = null;
    }

    content.appendChild(heading('h2', entry.title, 'entry-title'));
    content.appendChild(T.el('p', 'entry-ref', entry.reference));

    content.appendChild(T.el('p', 'entry-meta', [
      'Reading ' + entry.indexInPeriod + ' of ' + entry.period.readings.length +
        ' in ' + entry.period.label,
      entry.index + ' of ' + view.count + ' in the ' + view.label + ' track'
    ].concat(T.bibleMeta(bible)).join(' · ')));

    content.appendChild(progressBar(view, entry));

    if (entry.note) {
      const note = T.el('div', 'reading-note');
      note.appendChild(T.el('p', 'reading-note-label', 'Why this reading is here'));
      note.appendChild(T.el('p', 'reading-note-body', entry.note));
      content.appendChild(note);
    }

    const passage = T.el('section', 'proper');
    passage.setAttribute('aria-label', 'The text of ' + entry.reference);
    passage.appendChild(T.renderCitation(
      P.readingCitation(entry.reading),
      bible,
      held.fragments,
      state.plan.numbering || null,
      { book: entry.book, showRef: false }
    ));
    content.appendChild(passage);

    content.appendChild(continuity(view, entry));

    const foot = T.el('p', 'reading-foot');
    foot.appendChild(link('What this track leaves out', { view: 'orient' }));
    foot.appendChild(document.createTextNode(' · '));
    foot.appendChild(link('All of ' + entry.period.label,
      { view: 'period', period: entry.period.key }));
    content.appendChild(foot);

    document.title = entry.title + ' — ' + entry.period.label + ' — ' +
      view.label + ' track — Triptych';
    T.statusLine(
      entry.title + ', ' + entry.reference + ', ' + bible.label + '. Reading ' +
      entry.indexInPeriod + ' of ' + entry.period.readings.length + ' in ' +
      entry.period.label + ', ' + entry.index + ' of ' + view.count +
      ' in the ' + view.label + ' track.'
    );
  }

  /* ------------------------------------------------------------------------
   * Rendering
   * --------------------------------------------------------------------- */

  function updateChrome(view) {
    trackName.textContent = 'The ' + view.label + ' track';
    trackLede.textContent = view.description
      ? P.firstSentence(view.description)
      : P.plural(view.count, 'reading') + ' in ' + view.periods.length + ' periods.';
    planLink.href = './' + window.location.search;
  }

  /** A view that names something the track does not hold falls back, quietly. */
  function normalise() {
    const view = currentTrack();
    if (state.view === 'reading' && !currentEntry()) state.view = 'orient';
    if (state.view === 'period' && !P.periodAt(view, state.periodKey)) {
      state.view = 'orient';
    }
  }

  async function render(options) {
    const view = currentTrack();
    const bible = currentBible();
    const token = T.beginRender();

    updateChrome(view);
    renderRail(view);

    if (state.view === 'reading' && bible) {
      const entry = currentEntry();
      content.setAttribute('aria-busy', 'true');
      const held = await T.fetchFragments(bible, [P.readingCitation(entry.reading)]);

      // A later selection may have overtaken this one while fragments were in
      // flight; the newest render wins.
      if (!T.isCurrentRender(token)) return;

      T.clear(content);
      renderReading(view, entry, bible, held);
    } else if (state.view === 'period') {
      T.clear(content);
      renderPeriod(view, currentPeriod());
    } else {
      T.clear(content);
      renderOrientation(view);
    }

    content.setAttribute('aria-busy', 'false');
    if (options && options.moveFocus) content.focus();
  }

  /* ------------------------------------------------------------------------
   * Navigation
   * --------------------------------------------------------------------- */

  function commit(options) {
    normalise();
    syncControls();
    T.writeHash(hashPairs());
    render(options);
  }

  function showReading(key, options) {
    const entry = P.entryAt(currentTrack(), key);
    if (!entry) return;
    state.view = 'reading';
    state.readingKey = entry.key;
    state.periodKey = entry.period.key;
    commit(options);
  }

  function showPeriod(key, options) {
    state.view = 'period';
    state.periodKey = String(key);
    commit(options);
  }

  function step(delta, options) {
    const view = currentTrack();
    if (state.view === 'reading') {
      const entry = currentEntry();
      if (!entry) return;
      const next = view.readings[entry.index - 1 + delta];
      if (next) showReading(next.key, options);
      return;
    }
    if (state.view === 'period') {
      const period = currentPeriod();
      if (!period) return;
      const next = view.periods[period.index - 1 + delta];
      if (next) showPeriod(next.key, options);
    }
  }

  /**
   * Change track without losing the reader's place.
   *
   * The tracks nest, so narrowing usually drops the reading in view: reading 5
   * of the year track exists at no smaller track at all. Landing on the nearest
   * earlier reading keeps the reader where they were in the story, and saying
   * so keeps them from believing the plan renumbered itself. Jumping back to
   * Genesis 1 would do neither.
   */
  function setTrack(tier, prefer, options) {
    if (P.tiers(state.plan).indexOf(tier) < 0) return;

    const previous = currentEntry();
    state.tier = tier;
    const view = currentTrack();
    fillTrackSelect();
    fillReadingSelect();

    let key = null;
    if (prefer && P.entryAt(view, prefer)) key = String(prefer);
    if (!key && state.readingKey && P.entryAt(view, state.readingKey)) {
      key = state.readingKey;
    }

    if (!key) {
      const wanted = prefer !== null && prefer !== undefined && prefer !== ''
        ? Number(prefer)
        : (previous ? previous.order : NaN);
      if (Number.isFinite(wanted)) {
        let nearest = null;
        for (const entry of view.readings) {
          if (entry.order <= wanted) nearest = entry;
        }
        if (nearest) {
          key = nearest.key;
          // Only worth saying where the reader is actually looking at a
          // reading; on an orientation it would sit unread until some later
          // reading wore it, and explain nothing.
          if (state.view === 'reading') {
            state.notice = 'That reading is not in the ' + view.label +
              ' track, which is the smaller selection. This is the nearest ' +
              'reading before it.';
          }
        }
      }
    }

    if (!key && view.readings.length) key = view.readings[0].key;
    if (!key) {
      T.fail('The "' + tier + '" track holds no readings.');
      return;
    }

    state.readingKey = key;
    if (state.periodKey && !P.periodAt(view, state.periodKey)) state.periodKey = null;
    if (state.view === 'reading') {
      const entry = P.entryAt(view, key);
      if (entry) state.periodKey = entry.period.key;
    }
    commit(options);
  }

  /* ------------------------------------------------------------------------
   * Start-up
   * --------------------------------------------------------------------- */

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

    const plan = await P.load();
    if (!plan.ok) {
      T.fail(plan.message);
      return;
    }
    state.plan = plan.plan;

    const problems = P.warnings(state.plan);
    if (problems.length) {
      T.showBanner(
        'The reading plan "' + P.id + '" does not agree with itself: ' +
        problems.join('; ') + '.'
      );
    }

    const tiers = P.tiers(state.plan);
    const wantedTier = hash.get('tier');
    const tier = tiers.indexOf(wantedTier) >= 0 ? wantedTier : tiers[0];

    const wantedReading = hash.get('reading');
    const wantedPeriod = hash.get('period');
    state.view = wantedReading ? 'reading' : (wantedPeriod ? 'period' : 'orient');
    state.periodKey = wantedPeriod || null;

    setTrack(tier, wantedReading, { moveFocus: false });
  }

  /* ------------------------------------------------------------------------
   * Events
   * --------------------------------------------------------------------- */

  trackSelect.addEventListener('change', () => {
    setTrack(trackSelect.value, null, { moveFocus: false });
  });

  readingSelect.addEventListener('change', () => {
    showReading(readingSelect.value, { moveFocus: false });
  });

  bibleSelect.addEventListener('change', () => {
    state.bibleId = bibleSelect.value;
    commit({ moveFocus: false });
  });

  prevButton.addEventListener('click', () => step(-1, { moveFocus: false }));
  nextButton.addEventListener('click', () => step(1, { moveFocus: false }));

  controls.addEventListener('submit', (event) => event.preventDefault());

  T.onArrowStep((delta) => step(delta, { moveFocus: false }));

  // A link inside the content is destroyed by the render it causes, so focus
  // moves to the content that replaced it rather than being dropped on the body.
  T.onHashChange((hash) => {
    if (!state.plan) return;

    // A hash that names none of this page's keys is not a place in the track:
    // it is the skip link jumping to #reading, or an anchor of some other kind.
    // Treating it as a navigation would throw the reader out of their reading
    // and back to the orientation, which is the opposite of skipping to it.
    if (!hash.get('tier') && !hash.get('reading') && !hash.get('period') &&
        !hash.get('bible')) {
      return;
    }

    const wantedBible = hash.get('bible');
    if (state.bibles.some((bible) => bible.id === wantedBible)) {
      state.bibleId = wantedBible;
    }

    const wantedReading = hash.get('reading');
    const wantedPeriod = hash.get('period');
    state.view = wantedReading ? 'reading' : (wantedPeriod ? 'period' : 'orient');
    if (wantedPeriod) state.periodKey = wantedPeriod;

    const wantedTier = hash.get('tier');
    if (wantedTier && wantedTier !== state.tier) {
      setTrack(wantedTier, wantedReading, { moveFocus: true });
      return;
    }

    if (wantedReading && P.entryAt(currentTrack(), wantedReading)) {
      const entry = P.entryAt(currentTrack(), wantedReading);
      state.readingKey = entry.key;
      state.periodKey = entry.period.key;
    }
    commit({ moveFocus: true });
  });

  start();
}());
