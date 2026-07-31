/* ===========================================================================
 * The reading-plan page — Tier, then Reading, then Translation
 * ===========================================================================
 *
 * This page does one thing. It does not offer the Mass propers, share a
 * dropdown with them, or link the reader into them mid-task; the propers are
 * their own page at ../liturgy/. What the two pages share is the machinery in
 * ../shared/browser-core.js — the chapter cache, the four failure renderings,
 * the numbering-aware loci, the URL state and the render token — and nothing in
 * this file may re-implement any of it.
 *
 *   ?data=<root>   where the corpus lives (default ../browse; ?data=fixture
 *                  serves the sample corpus in ../fixture)
 *   ?plan=<id>     which plan to read (default: narrative-spine)
 *   #tier=<tier>&reading=<order>&bible=<id>
 *                  the current selection; shareable, and survives reload
 * ======================================================================== */

'use strict';

(function () {
  const T = window.Triptych;

  const PLAN = T.params.get('plan') || 'narrative-spine';
  const PLAN_PATH = 'structure/readings/' + PLAN + '.json';

  /* ------------------------------------------------------------------------
   * Tiers
   *
   * TIERS ARE CUMULATIVE, AND THE DIRECTION MATTERS. `overview` is the smallest
   * set and `year` is everything; each reading is marked with the tier at which
   * it FIRST appears, and appears in no other. So reading a tier means taking
   * every reading marked at that tier AND at every tier above it — overview at
   * the narrative tier, overview and narrative at the year tier — in `order`
   * sequence.
   *
   * Getting this backwards inverts the plan without erroring: the reader asks
   * for the 36-reading overview and is handed the 357-reading year, or asks for
   * the year and is handed the skeleton. Both look like a working plan. Hence
   * the explicit sequence below, ranked smallest-first, and the check that the
   * count computed here matches the count the plan's own `tiers` block declares.
   * --------------------------------------------------------------------- */

  const TIER_SEQUENCE = ['overview', 'narrative', 'year'];

  const state = {
    bibles: [],
    bibleId: null,
    plan: null,
    tier: null,
    entries: [],
    readingKey: null
  };

  /**
   * Where a tier sits in the nesting, smallest first.
   *
   * An unrecognised tier is a data problem, not a reason to drop readings on
   * the floor: it ranks with the widest known tier, so the reading is still
   * offered at the fullest reading of the plan, and the mismatch is reported.
   */
  function tierRank(tier) {
    const rank = TIER_SEQUENCE.indexOf(tier);
    return rank < 0 ? TIER_SEQUENCE.length - 1 : rank;
  }

  function planPeriods() {
    return (state.plan && state.plan.periods) || [];
  }

  function planTierBlock(tier) {
    const tiers = (state.plan && state.plan.tiers) || {};
    return tiers[tier] || {};
  }

  function tierLabel(tier) {
    const declared = planTierBlock(tier).label;
    if (declared) return String(declared);
    return tier ? T.titleCase(tier) : 'All';
  }

  /** The tiers this plan offers, smallest first. */
  function planTiers() {
    const declared = (state.plan && state.plan.tiers) || {};
    const present = new Set();
    for (const period of planPeriods()) {
      for (const entry of period.readings || []) present.add(entry.tier);
    }
    const offered = TIER_SEQUENCE.filter((tier) => {
      return Object.prototype.hasOwnProperty.call(declared, tier) || present.has(tier);
    });
    return offered.length ? offered : [TIER_SEQUENCE[TIER_SEQUENCE.length - 1]];
  }

  /** Every reading at or above `tier`, in `order` sequence. */
  function readingsAtTier(tier) {
    const wanted = tierRank(tier);
    const chosen = [];
    for (const period of planPeriods()) {
      for (const entry of period.readings || []) {
        if (tierRank(entry.tier) <= wanted) {
          chosen.push({ reading: entry, period: period });
        }
      }
    }
    chosen.sort((a, b) => Number(a.reading.order) - Number(b.reading.order));
    return chosen;
  }

  /**
   * Check the file against itself: the cumulative count at each tier, computed
   * from the readings, against the count the `tiers` block declares. A plan
   * that disagrees with its own summary is the failure the comment above exists
   * to catch, so it is said out loud rather than logged.
   */
  function tierWarnings() {
    const problems = [];
    for (const tier of planTiers()) {
      const declared = planTierBlock(tier).readings;
      const computed = readingsAtTier(tier).length;
      if (typeof declared === 'number' && declared !== computed) {
        problems.push(
          'the ' + tier + ' tier declares ' + declared + ' readings but holds ' + computed
        );
      }
    }
    const unknown = new Map();
    for (const period of planPeriods()) {
      for (const entry of period.readings || []) {
        if (TIER_SEQUENCE.indexOf(entry.tier) >= 0) continue;
        const name = String(entry.tier);
        unknown.set(name, (unknown.get(name) || 0) + 1);
      }
    }
    for (const [name, count] of unknown) {
      problems.push(
        count + ' reading' + (count === 1 ? '' : 's') + ' marked at the ' +
        'unrecognised tier "' + name + '", shown at the fullest tier'
      );
    }
    return problems;
  }

  /* ------------------------------------------------------------------------
   * Elements
   * --------------------------------------------------------------------- */

  const tierSelect = document.getElementById('tier-select');
  const readingSelect = document.getElementById('reading-select');
  const bibleSelect = document.getElementById('bible-select');
  const prevButton = document.getElementById('prev-button');
  const nextButton = document.getElementById('next-button');
  const reading = document.getElementById('reading');
  const controls = document.getElementById('controls');

  /* ------------------------------------------------------------------------
   * Readings
   * --------------------------------------------------------------------- */

  /** A citation-shaped view of a reading, so the shared renderer serves it. */
  function readingCitation(entry) {
    return {
      ref: null,
      book: entry.book || null,
      token: entry.token || null,
      loci: entry.loci || {},
      unresolved: entry.unresolved || null
    };
  }

  /** A reading's reference in the plan's own numbering, for labels. */
  function readingReference(entry) {
    const numbering = (state.plan && state.plan.numbering) || 'vulgate';
    const picked = T.lociFor(readingCitation(entry), numbering);
    if (!picked.loci) return entry.book || entry.token || '';
    return T.formatLoci(picked.loci);
  }

  function rebuildEntries() {
    state.entries = readingsAtTier(state.tier).map((held) => ({
      key: String(held.reading.order),
      order: Number(held.reading.order),
      label: held.reading.title || readingReference(held.reading) ||
        String(held.reading.order),
      group: held.period.label || held.period.key || 'Readings',
      reading: held.reading,
      period: held.period
    }));
  }

  function currentEntry() {
    return state.entries.find((entry) => entry.key === state.readingKey) || null;
  }

  function currentBible() {
    return state.bibles.find((bible) => bible.id === state.bibleId) || null;
  }

  function entryIndex() {
    return state.entries.findIndex((entry) => entry.key === state.readingKey);
  }

  /* ------------------------------------------------------------------------
   * Controls
   * --------------------------------------------------------------------- */

  function fillTierSelect() {
    T.fillSelect(tierSelect, planTiers().map((tier) => {
      const count = readingsAtTier(tier).length;
      return {
        value: tier,
        label: tierLabel(tier) + ' — ' + count + ' reading' + (count === 1 ? '' : 's')
      };
    }));
    if (state.tier) tierSelect.value = state.tier;
  }

  function fillReadingSelect() {
    // The plan's own order, grouped by period. Never sorted by title: the plan
    // is a sequence, and its sequence is the point of it.
    T.fillSelect(readingSelect, state.entries.map((entry) => ({
      value: entry.key,
      label: entry.label,
      group: entry.group
    })));
    if (state.readingKey) readingSelect.value = state.readingKey;
  }

  function syncControls() {
    if (state.tier) tierSelect.value = state.tier;
    if (state.readingKey) readingSelect.value = state.readingKey;
    if (state.bibleId) bibleSelect.value = state.bibleId;

    const index = entryIndex();
    prevButton.disabled = index <= 0;
    nextButton.disabled = index < 0 || index >= state.entries.length - 1;
  }

  function writeHash() {
    T.writeHash([
      ['tier', state.tier],
      ['reading', state.readingKey],
      ['bible', state.bibleId]
    ]);
  }

  /* ------------------------------------------------------------------------
   * Rendering
   * --------------------------------------------------------------------- */

  function renderReading(entry, bible, fragments, chapterCount) {
    const held = entry.reading;
    const position = entryIndex() + 1;

    reading.appendChild(
      T.el('h2', 'entry-title', held.title || readingReference(held) || entry.key)
    );

    const meta = ['Period: ' + entry.group];
    meta.push(tierLabel(held.tier) + ' tier');
    meta.push('Reading ' + position + ' of ' + state.entries.length);
    reading.appendChild(
      T.el('p', 'entry-meta', meta.concat(T.bibleMeta(bible)).join(' · '))
    );

    if (entry.period && entry.period.summary) {
      reading.appendChild(
        T.el('p', 'period-summary', String(entry.period.summary).trim())
      );
    }

    if (held.note) {
      const note = T.el('p', 'reading-note');
      note.appendChild(T.el('span', 'reading-note-label', 'Note'));
      note.appendChild(document.createTextNode(String(held.note).trim()));
      reading.appendChild(note);
    }

    const section = T.el('section', 'proper');
    section.appendChild(T.renderCitation(
      readingCitation(held), bible, fragments,
      (state.plan && state.plan.numbering) || null
    ));
    reading.appendChild(section);

    // An abridgement that hides what it drops is the thing this plan refuses to
    // be, so its own account of its omissions travels with it — collapsed, but
    // never absent.
    if (state.plan && state.plan.omissions) {
      const details = document.createElement('details');
      details.className = 'omissions';
      details.appendChild(T.el('summary', null, 'What this plan does not read'));
      details.appendChild(
        T.el('p', 'omissions-body', String(state.plan.omissions).trim())
      );
      reading.appendChild(details);
    }

    T.statusLine(
      (held.title || entry.key) + ', ' + entry.group + ', ' + bible.label + '. ' +
      'Reading ' + position + ' of ' + state.entries.length + ' at the ' +
      tierLabel(state.tier) + ' tier, ' + chapterCount + ' chapters.'
    );
  }

  async function render(options) {
    const entry = currentEntry();
    const bible = currentBible();
    if (!entry || !bible) return;

    const token = T.beginRender();
    reading.setAttribute('aria-busy', 'true');

    const held = await T.fetchFragments(bible, [readingCitation(entry.reading)]);

    // A later selection may have overtaken this one while fragments were in
    // flight; the newest render wins.
    if (!T.isCurrentRender(token)) return;

    T.clear(reading);
    renderReading(entry, bible, held.fragments, held.chapters.length);
    reading.setAttribute('aria-busy', 'false');

    if (options && options.moveFocus) reading.focus();
  }

  /* ------------------------------------------------------------------------
   * Selection
   * --------------------------------------------------------------------- */

  function select(readingKey, bibleId, options) {
    if (readingKey) state.readingKey = readingKey;
    if (bibleId) state.bibleId = bibleId;
    syncControls();
    writeHash();
    render(options);
  }

  function step(delta, options) {
    const index = entryIndex();
    const next = index + delta;
    if (index < 0 || next < 0 || next >= state.entries.length) return;
    select(state.entries[next].key, null, options);
  }

  /**
   * Change tier without losing the reader's place.
   *
   * Narrowing to a smaller tier usually drops the reading in view, since the
   * tiers nest. Landing on the nearest earlier reading keeps the reader where
   * they were in the story; jumping back to Genesis 1 would not.
   */
  function setTier(tier, prefer, options) {
    if (planTiers().indexOf(tier) < 0) return;

    const previous = currentEntry();
    state.tier = tier;
    rebuildEntries();
    fillTierSelect();
    fillReadingSelect();

    let key = state.entries.some((entry) => entry.key === prefer) ? prefer : null;
    if (!key && state.entries.some((entry) => entry.key === state.readingKey)) {
      key = state.readingKey;
    }
    if (!key && previous) {
      let nearest = null;
      for (const entry of state.entries) {
        if (entry.order <= previous.order) nearest = entry;
      }
      key = nearest ? nearest.key : null;
    }
    if (!key && state.entries.length) key = state.entries[0].key;
    if (!key) {
      T.fail('The "' + tier + '" tier holds no readings.');
      return;
    }
    select(key, null, options);
  }

  /* ------------------------------------------------------------------------
   * Start-up
   * --------------------------------------------------------------------- */

  T.setInlineNotice(
    'No data root could be reached at "' + T.dataRoot + '", so this page is ' +
    'showing its built-in fallback: three readings and a diagnostics entry, ' +
    'which is not a reading plan. Serve the pages over HTTP with the corpus at ' +
    'that path, or try ?data=fixture.'
  );

  // The fallback's own plan, for a page opened straight off disk. It is not the
  // published plan and says so; the diagnostics are in an entry labelled as
  // such, so that no real reading carries invented data.
  T.addInlineFiles({
    'structure/readings/narrative-spine.json': {
      schema: 'triptych-reading-structure/v1',
      plan: 'Built-in fallback (not the published reading plan)',
      canon: 'catholic-73',
      numbering: 'vulgate',
      tiers: {
        overview: { label: 'Overview', readings: 5, description: 'The fallback\'s smallest set.' },
        narrative: { label: 'Narrative', readings: 6, description: 'The overview, plus one.' },
        year: { label: 'Year', readings: 7, description: 'Everything this fallback holds.' }
      },
      omissions:
        'This is the page\'s built-in fallback, not a reading plan. It holds ' +
        'three readings over the three chapters compiled into the shared ' +
        'script, plus a diagnostics period. Serve the corpus, or ?data=fixture, ' +
        'for a plan.',
      periods: [
        {
          key: 'demonstration',
          label: 'Demonstration',
          summary: 'Three readings over the chapters this fallback carries.',
          readings: [
            {
              order: 1,
              tier: 'overview',
              title: 'Creation',
              book: 'Genesis',
              token: 'Gen',
              note: 'The first lesson of the Easter Vigil.',
              loci: {
                vulgate: [{ chapter: 1, first: 1, last: 3 }],
                hebrew: [{ chapter: 1, first: 1, last: 3 }]
              },
              unresolved: null
            },
            {
              order: 2,
              tier: 'narrative',
              title: 'Lifting up the soul',
              book: 'Psalms',
              token: 'Ps',
              note: 'The Introit of the First Sunday of Advent draws on these verses.',
              loci: {
                vulgate: [{ chapter: 24, first: 1, last: 3 }],
                hebrew: [{ chapter: 25, first: 1, last: 3 }]
              },
              unresolved: null
            },
            {
              order: 3,
              tier: 'year',
              title: 'The night is passed',
              book: 'Romans',
              token: 'Rom',
              note: null,
              loci: {
                vulgate: [{ chapter: 13, first: 11, last: 12 }],
                hebrew: [{ chapter: 13, first: 11, last: 12 }]
              },
              unresolved: null
            }
          ]
        },
        {
          key: 'fallback-diagnostics',
          label: 'Fallback diagnostics (not part of any plan)',
          summary:
            'Synthetic entries, marked at the overview tier so that they appear ' +
            'at every tier. Each exercises a failure the page must explain ' +
            'rather than swallow.',
          readings: [
            {
              order: 9001,
              tier: 'overview',
              title: 'Diagnostic: unresolved reading',
              book: 'Psalms',
              token: 'Ps',
              note: 'The reason is shown in place of the text.',
              loci: {},
              unresolved: 'Ps has no chapter 151'
            },
            {
              order: 9002,
              tier: 'overview',
              title: 'Diagnostic: missing fragment',
              book: 'Tobias',
              token: 'Tob',
              note: 'No chapter file for Tob 3 exists in this fallback.',
              loci: {
                vulgate: [{ chapter: 3, first: 1, last: 2 }],
                hebrew: [{ chapter: 3, first: 1, last: 2 }]
              },
              unresolved: null
            },
            {
              order: 9003,
              tier: 'overview',
              title: 'Diagnostic: numbering absent',
              book: 'Psalms',
              token: 'Ps',
              note: 'Hebrew-only loci, read by a vulgate-numbered edition.',
              loci: { hebrew: [{ chapter: 25, first: 1, last: 1 }] },
              unresolved: null
            },
            {
              order: 9004,
              tier: 'overview',
              title: 'Diagnostic: verses absent from the fragment',
              book: 'Genesis',
              token: 'Gen',
              note: 'Genesis 1 is present in the fallback and has no verse 300.',
              loci: {
                vulgate: [
                  { chapter: 1, first: 1, last: 3 },
                  { chapter: 1, first: 300, last: 302 }
                ],
                hebrew: [
                  { chapter: 1, first: 1, last: 3 },
                  { chapter: 1, first: 300, last: 302 }
                ]
              },
              unresolved: null
            }
          ]
        }
      ]
    }
  });

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

    let file;
    try {
      file = await T.loadJSON(PLAN_PATH);
    } catch (error) {
      T.fail(
        'The reading plan "' + PLAN + '" could not be loaded: ' +
        (error.message || error)
      );
      return;
    }

    state.plan = file || null;
    if (!planPeriods().length) {
      T.fail('The reading plan "' + PLAN + '" lists no periods.');
      return;
    }

    const problems = tierWarnings();
    if (problems.length) {
      T.showBanner(
        'The reading plan "' + PLAN + '" does not agree with itself: ' +
        problems.join('; ') + '.'
      );
    }

    const tiers = planTiers();
    const wantedTier = hash.get('tier');
    const tier = tiers.indexOf(wantedTier) >= 0 ? wantedTier : tiers[0];

    setTier(tier, hash.get('reading'), { moveFocus: false });
  }

  /* ------------------------------------------------------------------------
   * Events
   * --------------------------------------------------------------------- */

  tierSelect.addEventListener('change', () => {
    setTier(tierSelect.value, null, { moveFocus: false });
  });

  readingSelect.addEventListener('change', () => {
    select(readingSelect.value, null, { moveFocus: false });
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

    const wantedTier = hash.get('tier');
    if (wantedTier && wantedTier !== state.tier) {
      setTier(wantedTier, hash.get('reading'), { moveFocus: false });
      return;
    }

    const wantedReading = hash.get('reading');
    const key = state.entries.some((entry) => entry.key === wantedReading)
      ? wantedReading
      : state.readingKey;
    select(key, state.bibleId, { moveFocus: false });
  });

  start();
}());
