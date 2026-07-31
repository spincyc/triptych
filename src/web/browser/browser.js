/* ===========================================================================
 * Scripture browser — fragment architecture
 * ===========================================================================
 *
 * WHAT THIS PAGE DOES
 *
 * It loads four kinds of file and joins them in the browser:
 *
 *   bibles.json                                 the translations on offer
 *   structure/propers/<calendar>.json           the Masses, with each citation
 *                                               already resolved to loci per
 *                                               numbering system
 *   structure/readings/<plan>.json              a reading plan: periods, each
 *                                               holding readings whose loci are
 *                                               resolved exactly the same way
 *   <bible-id>/chapters/<BookToken>/<n>.json    one chapter of verse text
 *
 * Choosing a Mass — or a reading — and a translation costs exactly the chapter
 * fragments that selection cites, fetched once each and cached in memory for
 * the rest of the session. Switching translation re-uses the same structure;
 * switching Mass or reading re-uses every chapter already held; switching
 * between the two modes re-uses the whole cache, because a chapter is a chapter
 * whoever asked for it.
 *
 * WHY IT IS NOT PRE-RENDERED — READ THIS BEFORE "OPTIMISING"
 *
 * The obvious-looking improvement is to bake every Mass-and-translation pair
 * into a static page at build time. That is a combinatorial explosion, and it
 * gets worse with exactly the thing this project intends to do more of.
 *
 *   masses x translations = pages
 *
 * The 1962 seasonal cycle alone is on the order of 10^2 Masses; the full
 * calendar with sanctoral entries is larger again. Two translations is already
 * a multiple of that; the repository tracks more editions than two, and the
 * point of the corpus is to keep adding them. Every new translation would
 * multiply the entire calendar afresh — one edition added, hundreds of pages
 * regenerated, every one of them a near-duplicate carrying the same structural
 * text with different verse bodies. The same chapter of the Psalter would be
 * copied into every page that cites it, in every edition, forever.
 *
 * Fragments make the cost additive instead of multiplicative:
 *
 *   masses + readings + (translations x chapters cited) = files
 *
 * Adding a translation adds its chapters and one line in bibles.json. It adds
 * no pages. Adding a Mass adds no files at all beyond the structure entry —
 * the chapters it cites are almost always already there, shared with every
 * other Mass that cites them, and now shared with the reading plan as well.
 *
 * So: do not turn this into static pages, do not inline verse text into the
 * structure file, and do not build a per-pair cache on disk. The join belongs
 * here, at read time, where it is O(1) files per new edition.
 *
 * TWO MODES, ONE PAGE — READ THIS BEFORE SPLITTING IT
 *
 * The page renders two structures: Mass propers (masses -> propers ->
 * citations) and reading plans (periods -> readings). They differ only in how
 * the citations are grouped and labelled. Everything underneath is the same
 * code and must stay that way:
 *
 *   the translation list and the numbering-aware choice of loci
 *   the chapter cache, which is the whole point of the design
 *   the four failure renderings — unresolved citation, absent numbering,
 *     missing fragment, missing verses — each of which states its reason
 *   the render token that discards a selection overtaken by a newer one
 *   prev/next stepping, the arrow keys, the hash state, the focus handling
 *
 * A second page would begin as a copy of this one and would then drift: a fix
 * to the failure rendering would land on one of them, the cache would be warm
 * in one tab and cold in the other, and the same chapter would be fetched
 * twice by the same reader. Mode is a variable, not a file.
 *
 * OPERATING NOTES
 *
 *   ?data=<root>       where the files live (default: alongside this page).
 *                      `?data=fixture` serves the sample data in fixture/ so
 *                      the page can be demonstrated without the real corpus.
 *   ?calendar=<id>     which propers structure to load (default: roman-1962).
 *   ?plan=<id>         which reading plan to load (default: narrative-spine).
 *   ?mode=<propers|readings>   which one to open on (default: propers).
 *   #mode=propers&mass=<key>&bible=<id>
 *   #mode=readings&reading=<order>&tier=<tier>&bible=<id>
 *                      current selection; shareable and survives reload. A
 *                      hash written before the reading plan existed still
 *                      works: no mode and a mass key means propers.
 *
 * Neither structure is fetched until a mode is opened, and a failure to load
 * one leaves the other alone — a site that publishes the propers and no plan
 * says so in the reading area and keeps working.
 *
 * If no data root can be reached at start-up — opening the file straight off
 * disk, where fetch is refused — the page falls back to the small
 * INLINE_FIXTURE below and says so in a banner. That fixture exists so this
 * file can be demonstrated offline; it is not the data contract.
 *
 * No frameworks, no build step, no external requests of any kind. All output
 * is built with createElement/textContent, never innerHTML, so Latin
 * orthography and any other non-ASCII text passes through untouched.
 * ======================================================================== */

'use strict';

/* --------------------------------------------------------------------------
 * Configuration
 * ----------------------------------------------------------------------- */

const PARAMS = new URLSearchParams(window.location.search);
const DATA_ROOT = normaliseRoot(PARAMS.get('data') || '.');
const CALENDAR = PARAMS.get('calendar') || 'roman-1962';
const PLAN = PARAMS.get('plan') || 'narrative-spine';

function normaliseRoot(root) {
  return root.replace(/\/+$/, '') || '.';
}

function dataPath(path) {
  return DATA_ROOT + '/' + path;
}

/**
 * The two modes, and everything that differs between them. Anything not in
 * this table is shared code; see the note at the top of the file.
 */
const MODES = {
  propers: {
    label: 'Mass propers',
    entryLabel: 'Mass',
    path: 'structure/propers/' + CALENDAR + '.json',
    what: 'The calendar "' + CALENDAR + '"'
  },
  readings: {
    label: 'Reading plan',
    entryLabel: 'Reading',
    path: 'structure/readings/' + PLAN + '.json',
    what: 'The reading plan "' + PLAN + '"'
  }
};

const DEFAULT_MODE = MODES[PARAMS.get('mode')] ? PARAMS.get('mode') : 'propers';

/* --------------------------------------------------------------------------
 * Inline fixture — the offline fallback only. Abridged on purpose: two
 * translations, one Mass, three readings, two chapters, plus the failure
 * cases, which are kept in entries labelled as diagnostics so that nothing
 * here can be mistaken for a Mass or for a reading of the real plan.
 * ----------------------------------------------------------------------- */

const INLINE_FIXTURE = {
  'bibles.json': {
    bibles: [
      {
        id: 'douay-rheims',
        label: 'Douay-Rheims (Challoner)',
        language: 'en',
        numbering: 'vulgate',
        psalter: 'gallican'
      },
      {
        id: 'clementine-vulgate',
        label: 'Clementine Vulgate',
        language: 'la',
        numbering: 'vulgate',
        psalter: 'gallican'
      }
    ]
  },

  'structure/propers/roman-1962.json': {
    calendar: 'roman-1962',
    masses: [
      {
        key: 'advent-1',
        name: 'First Sunday of Advent',
        season: 'advent',
        kind: 'seasonal',
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
                  vulgate: [{ book: 'Ps', chapter: 24, first: 1, last: 3 }],
                  hebrew: [{ book: 'Ps', chapter: 25, first: 1, last: 3 }]
                },
                unresolved: null
              },
              {
                ref: 'Psalm 24:4',
                token: 'Ps',
                loci: {
                  vulgate: [{ book: 'Ps', chapter: 24, first: 4, last: 4 }],
                  hebrew: [{ book: 'Ps', chapter: 25, first: 4, last: 4 }]
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
                  vulgate: [{ book: 'Rom', chapter: 13, first: 11, last: 12 }],
                  hebrew: [{ book: 'Rom', chapter: 13, first: 11, last: 12 }]
                },
                unresolved: null
              }
            ]
          }
        ]
      },
      {
        key: 'fixture-diagnostics',
        name: 'Fixture diagnostics (not a Mass)',
        season: 'none',
        kind: 'fixture',
        propers: [
          {
            name: 'Unresolved citation',
            incipit: 'reason shown instead of text',
            source: 'scripture',
            citations: [
              { ref: 'Psalm 151:1', loci: {}, unresolved: 'Ps has no chapter 151' }
            ]
          },
          {
            name: 'Missing fragment',
            incipit: 'chapter file absent from this fixture',
            source: 'scripture',
            citations: [
              {
                ref: 'Tobias 3:1-2',
                token: 'Tob',
                loci: {
                  vulgate: [{ book: 'Tob', chapter: 3, first: 1, last: 2 }],
                  hebrew: [{ book: 'Tob', chapter: 3, first: 1, last: 2 }]
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
                loci: { hebrew: [{ book: 'Ps', chapter: 25, first: 1, last: 1 }] },
                unresolved: null
              }
            ]
          }
        ]
      }
    ]
  },

  // Not the real Narrative Spine: three readings over the two chapters this
  // inline fixture carries, enough to show the shape and the tier filter.
  'structure/readings/narrative-spine.json': {
    schema: 'triptych-reading-structure/v1',
    plan: 'Inline demonstration plan (not the published reading plan)',
    canon: 'catholic-73',
    numbering: 'vulgate',
    tiers: {
      overview: { label: 'Overview', readings: 4, description: 'The inline fixture\'s smallest set.' },
      narrative: { label: 'Narrative', readings: 5, description: 'Overview, plus one.' },
      year: { label: 'Year', readings: 6, description: 'Everything this fixture holds.' }
    },
    omissions:
      'This is the page\'s built-in fallback, not a reading plan. It holds ' +
      'three readings over the only two chapters compiled into this file, ' +
      'plus a diagnostics period. Serve the real data, or ?data=fixture, for ' +
      'a plan.',
    periods: [
      {
        key: 'demonstration',
        label: 'Demonstration',
        summary: 'Three readings over the two chapters this file carries.',
        readings: [
          {
            order: 1,
            tier: 'overview',
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
            order: 2,
            tier: 'narrative',
            title: 'Shew, O Lord, thy ways',
            book: 'Psalms',
            token: 'Ps',
            note: null,
            loci: {
              vulgate: [{ chapter: 24, first: 4, last: 4 }],
              hebrew: [{ chapter: 25, first: 4, last: 4 }]
            },
            unresolved: null
          },
          {
            order: 3,
            tier: 'year',
            title: 'The night is passed',
            book: 'Romans',
            token: 'Rom',
            note: 'Read at Advent; the same chapter the Epistle above cites.',
            loci: {
              vulgate: [{ chapter: 13, first: 11, last: 12 }],
              hebrew: [{ chapter: 13, first: 11, last: 12 }]
            },
            unresolved: null
          }
        ]
      },
      {
        key: 'fixture-diagnostics',
        label: 'Fixture diagnostics (not part of any plan)',
        summary:
          'Synthetic entries, marked at the overview tier so they appear at ' +
          'every tier. Each one exercises a failure the page must explain ' +
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
            note: 'No chapter file for Tob 3 exists in this fixture.',
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
          }
        ]
      }
    ]
  },

  'douay-rheims/chapters/Ps/24.json': {
    book: 'Ps',
    chapter: 24,
    verses: {
      1: 'Unto the end, a psalm for David. To thee, O Lord, have I lifted up my soul.',
      2: 'In thee, O my God, I put my trust; let me not be ashamed.',
      3: 'Neither let my enemies laugh at me: for none of them that wait on thee shall be confounded.',
      4: 'Let all them be confounded that act unjust things without cause. Shew, O Lord, thy ways to me, and teach me thy paths.'
    }
  },

  'douay-rheims/chapters/Rom/13.json': {
    book: 'Rom',
    chapter: 13,
    verses: {
      11: 'And that, knowing the season, that it is now the hour for us to rise from sleep. For now our salvation is nearer than when we believed.',
      12: 'The night is passed And the day is at hand. Let us, therefore cast off the works of darkness and put on the armour of light.'
    }
  },

  'clementine-vulgate/chapters/Ps/24.json': {
    book: 'Ps',
    chapter: 24,
    verses: {
      1: 'In finem. Psalmus David. Ad te, Domine, levavi animam meam:',
      2: 'Deus meus, in te confido; non erubescam.',
      3: 'Neque irrideant me inimici mei: etenim universi qui sustinent te, non confundentur.',
      4: 'Confundantur omnes iniqua agentes supervacue. Vias tuas, Domine, demonstra mihi, et semitas tuas edoce me.'
    }
  },

  'clementine-vulgate/chapters/Rom/13.json': {
    book: 'Rom',
    chapter: 13,
    verses: {
      11: 'Et hoc scientes tempus: quia hora est jam nos de somno surgere. Nunc enim propior est nostra salus, quam cum credidimus.',
      12: 'Nox præcessit, dies autem appropinquavit. Abjiciamus ergo opera tenebrarum, et induamur arma lucis.'
    }
  }
};

/* --------------------------------------------------------------------------
 * Fetch layer
 * ----------------------------------------------------------------------- */

class NotFound extends Error {}

let inlineMode = false;

// The inline fixture stands in only when the page cannot reach its data root
// at all, which is knowable at start-up. Once the corpus has loaded, a later
// transport failure is reported against the citation that hit it rather than
// silently replacing the reader's corpus with the demonstration one.
let bootstrapping = true;

/** Serve a path from the inline fixture, or report it absent. */
function fromInline(path) {
  const found = INLINE_FIXTURE[path];
  if (found === undefined) {
    throw new NotFound(path + ' is not in the built-in fixture');
  }
  return JSON.parse(JSON.stringify(found));
}

/**
 * Load one JSON file from the data root.
 *
 * A 404 raises NotFound, which callers handle per file — a missing chapter is
 * a reportable gap, not a broken page. A transport failure (no server, file://
 * origin) switches the whole page to the inline fixture once and says so.
 */
async function loadJSON(path) {
  if (inlineMode) return fromInline(path);

  const url = dataPath(path);
  let response;
  try {
    response = await fetch(url, { credentials: 'same-origin' });
  } catch (error) {
    if (!bootstrapping) {
      throw new Error(url + ' could not be reached: ' + (error.message || error));
    }
    enterInlineMode();
    return fromInline(path);
  }

  if (response.status === 404) throw new NotFound(url + ' was not found (404)');
  if (!response.ok) throw new Error(url + ' — HTTP ' + response.status);

  try {
    return await response.json();
  } catch (error) {
    throw new Error(url + ' — the response was not valid JSON');
  }
}

function enterInlineMode() {
  if (inlineMode) return;
  inlineMode = true;
  showBanner(
    'No data root could be reached at "' + DATA_ROOT + '", so this page is ' +
    'showing its built-in demonstration fixture: two translations, one Mass, ' +
    'three readings and a diagnostics entry in each mode. Serve the page over ' +
    'HTTP with the real data alongside it, or try ?data=fixture, for the full ' +
    'corpus.'
  );
}

/* --------------------------------------------------------------------------
 * Chapter cache — the point of the whole design. One promise per
 * bible/book/chapter, resolved once, re-used by every citation that lands in
 * it, in either mode. The promise never rejects; it resolves to a result the
 * renderer can display either way.
 * ----------------------------------------------------------------------- */

const chapterCache = new Map();

function chapterKey(bibleId, book, chapter) {
  return bibleId + '|' + book + '|' + chapter;
}

function loadChapter(bibleId, book, chapter) {
  const key = chapterKey(bibleId, book, chapter);
  const held = chapterCache.get(key);
  if (held) return held;

  const path = bibleId + '/chapters/' + book + '/' + chapter + '.json';
  const pending = loadJSON(path).then(
    (fragment) => {
      const verses = fragment && fragment.verses;
      if (!verses || typeof verses !== 'object') {
        return { ok: false, problem: path + ' carries no verses' };
      }
      return { ok: true, verses: verses };
    },
    (error) => {
      if (error instanceof NotFound) {
        return {
          ok: false,
          problem:
            'This edition has no fragment for ' + book + ' ' + chapter +
            ' (' + path + ').'
        };
      }
      return { ok: false, problem: String(error.message || error) };
    }
  );

  chapterCache.set(key, pending);
  return pending;
}

/* --------------------------------------------------------------------------
 * State
 * ----------------------------------------------------------------------- */

const state = {
  mode: DEFAULT_MODE,
  bibles: [],
  bibleId: null,

  masses: [],
  calendarName: CALENDAR,

  plan: null,
  planName: PLAN,
  tier: null,

  // The list the passage select, the prev/next buttons and the arrow keys all
  // work over, whichever mode is open. Rebuilt on a mode or tier change.
  entries: [],

  // Each mode remembers where the reader was, so switching back and forth does
  // not lose the place.
  selected: { propers: null, readings: null }
};

let renderToken = 0;
let suppressHashEvent = false;

/* --------------------------------------------------------------------------
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
 * the explicit sequence below, ranked smallest-first, and the assertion in the
 * status line that the count shown matches the count the file declares.
 * ----------------------------------------------------------------------- */

const TIER_SEQUENCE = ['overview', 'narrative', 'year'];

/**
 * Where a tier sits in the nesting, smallest first.
 *
 * An unrecognised tier is a data problem, not a reason to drop readings on the
 * floor: it ranks with the widest known tier, so the reading is still offered
 * at the fullest reading of the plan, and the mismatch is reported in a banner.
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
  return tier ? tier.charAt(0).toUpperCase() + tier.slice(1) : 'All';
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
      if (tierRank(entry.tier) <= wanted) chosen.push({ reading: entry, period: period });
    }
  }
  chosen.sort((a, b) => Number(a.reading.order) - Number(b.reading.order));
  return chosen;
}

/**
 * Check the file against itself: the cumulative count at each tier, computed
 * from the readings, against the count the `tiers` block declares. A plan that
 * disagrees with its own summary is the failure this whole comment exists to
 * catch, so it is said out loud rather than logged.
 */
function tierWarnings() {
  const problems = [];
  for (const tier of planTiers()) {
    const declared = planTierBlock(tier).readings;
    const computed = readingsAtTier(tier).length;
    if (typeof declared === 'number' && declared !== computed) {
      problems.push(
        'the ' + tier + ' tier declares ' + declared + ' readings but holds ' +
        computed
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

/* --------------------------------------------------------------------------
 * Elements
 * ----------------------------------------------------------------------- */

const modeSelect = document.getElementById('mode-select');
const tierField = document.getElementById('tier-field');
const tierSelect = document.getElementById('tier-select');
const entryLabel = document.getElementById('entry-label');
const entrySelect = document.getElementById('entry-select');
const bibleSelect = document.getElementById('bible-select');
const prevButton = document.getElementById('prev-button');
const nextButton = document.getElementById('next-button');
const reading = document.getElementById('reading');
const banner = document.getElementById('banner');
const controls = document.getElementById('controls');

/* --------------------------------------------------------------------------
 * Small DOM helpers — everything goes through textContent.
 * ----------------------------------------------------------------------- */

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined && text !== null) node.textContent = text;
  return node;
}

function clear(node) {
  while (node.firstChild) node.removeChild(node.firstChild);
}

function showBanner(text) {
  banner.textContent = text;
  banner.hidden = false;
}

function statusLine(text) {
  let status = document.getElementById('reading-status');
  if (!status) {
    status = el('p', 'visually-hidden');
    status.id = 'reading-status';
    status.setAttribute('role', 'status');
    status.setAttribute('aria-live', 'polite');
    document.body.appendChild(status);
  }
  status.textContent = text;
}

function notice(text) {
  const node = el('p', 'notice');
  node.appendChild(el('strong', null, 'Not shown: '));
  node.appendChild(document.createTextNode(text));
  return node;
}

/* --------------------------------------------------------------------------
 * Entries — the one list both modes are navigated through
 * ----------------------------------------------------------------------- */

/**
 * Normalise whichever structure is open into {key, label, group} entries.
 *
 * The select, the prev/next buttons, the arrow keys and the hash all work over
 * this list and know nothing about Masses or readings. Only the renderers do.
 */
function rebuildEntries() {
  if (state.mode === 'readings') {
    state.entries = readingsAtTier(state.tier).map((held) => ({
      kind: 'reading',
      key: String(held.reading.order),
      order: Number(held.reading.order),
      label: held.reading.title || readingReference(held.reading) || String(held.reading.order),
      group: held.period.label || held.period.key || 'Readings',
      reading: held.reading,
      period: held.period
    }));
    return;
  }

  state.entries = state.masses.map((mass) => ({
    kind: 'mass',
    key: mass.key,
    label: mass.name || mass.key,
    group: mass.season || 'other',
    mass: mass
  }));
}

function currentEntry() {
  const key = state.selected[state.mode];
  return state.entries.find((entry) => entry.key === key) || null;
}

function currentBible() {
  return state.bibles.find((bible) => bible.id === state.bibleId) || null;
}

function entryIndex() {
  const key = state.selected[state.mode];
  return state.entries.findIndex((entry) => entry.key === key);
}

function readHash() {
  const raw = window.location.hash.replace(/^#/, '');
  const parsed = new URLSearchParams(raw);
  const mode = parsed.get('mode');
  return {
    // A hash written before the reading plan existed carries a mass and no
    // mode, and must keep working.
    mode: MODES[mode] ? mode : (parsed.get('reading') ? 'readings' : 'propers'),
    mass: parsed.get('mass'),
    reading: parsed.get('reading'),
    tier: parsed.get('tier'),
    bible: parsed.get('bible')
  };
}

function writeHash() {
  const key = state.selected[state.mode];
  if (!key || !state.bibleId) return;
  const parts = ['mode=' + state.mode];
  if (state.mode === 'readings') {
    parts.push('reading=' + encodeURIComponent(key));
    if (state.tier) parts.push('tier=' + encodeURIComponent(state.tier));
  } else {
    parts.push('mass=' + encodeURIComponent(key));
  }
  parts.push('bible=' + encodeURIComponent(state.bibleId));
  const next = '#' + parts.join('&');
  if (window.location.hash === next) return;
  suppressHashEvent = true;
  window.location.hash = next;
}

/* --------------------------------------------------------------------------
 * Loci selection
 * ----------------------------------------------------------------------- */

/**
 * Pick the loci a given edition can actually read.
 *
 * Structure files key loci by numbering system because the psalter is numbered
 * differently between the Vulgate and Hebrew traditions and the same citation
 * lands on different chapters. An edition whose numbering has no entry is a
 * gap in the data, and is reported rather than silently guessed at.
 *
 * The book token may sit on the locus or on the citation that owns it — a
 * reading names its book once and lets its loci carry only chapter and verses.
 * The token is what the fragment path is built from, so it is preferred over
 * the display name.
 */
function lociFor(citation, numbering) {
  const loci = citation.loci || {};
  const chosen = loci[numbering];
  const owner = citation.token || citation.book || null;

  if (Array.isArray(chosen) && chosen.length) {
    const resolved = [];
    for (const locus of chosen) {
      const book = locus.book || owner;
      if (!book) {
        return {
          problem:
            'the citation names no book, so there is no fragment to fetch'
        };
      }
      resolved.push({
        book: book,
        chapter: locus.chapter,
        first: locus.first,
        last: locus.last
      });
    }
    return { loci: resolved };
  }

  const offered = Object.keys(loci).filter((key) => {
    return Array.isArray(loci[key]) && loci[key].length;
  });
  if (!offered.length) {
    return {
      problem:
        'the citation carries no loci at all, so there is nothing to fetch'
    };
  }
  return {
    problem:
      'this edition numbers by "' + numbering + '", and the citation carries ' +
      'loci only for ' + offered.map((key) => '"' + key + '"').join(', ') + '.'
  };
}

/** A citation-shaped view of a reading, so one renderer serves both modes. */
function readingCitation(entry) {
  return {
    ref: null,
    book: entry.book || null,
    token: entry.token || null,
    loci: entry.loci || {},
    unresolved: entry.unresolved || null
  };
}

/** Every citation the chosen entry carries, whichever mode is open. */
function citationsOf(entry) {
  if (!entry) return [];
  if (entry.kind === 'reading') return [readingCitation(entry.reading)];
  const found = [];
  for (const proper of (entry.mass && entry.mass.propers) || []) {
    for (const citation of proper.citations || []) found.push(citation);
  }
  return found;
}

/** Every distinct chapter the chosen entry needs, in this edition. */
function chaptersNeeded(entry, numbering) {
  const wanted = new Map();
  for (const citation of citationsOf(entry)) {
    if (citation.unresolved) continue;
    const picked = lociFor(citation, numbering);
    if (!picked.loci) continue;
    for (const locus of picked.loci) {
      wanted.set(locus.book + '|' + locus.chapter, {
        book: locus.book,
        chapter: locus.chapter
      });
    }
  }
  return Array.from(wanted.values());
}

/** "Gen 1:1-2, Gen 2:3-25" — used where the structure names no reference. */
function formatLoci(loci) {
  return loci
    .map((locus) => {
      const range = Number(locus.first) === Number(locus.last)
        ? String(locus.first)
        : locus.first + '-' + locus.last;
      return locus.book + ' ' + locus.chapter + ':' + range;
    })
    .join(', ');
}

/** A reading's reference in the plan's own numbering, for labels and lists. */
function readingReference(entry) {
  const numbering = (state.plan && state.plan.numbering) || 'vulgate';
  const picked = lociFor(readingCitation(entry), numbering);
  if (!picked.loci) return entry.book || entry.token || '';
  return formatLoci(picked.loci);
}

/* --------------------------------------------------------------------------
 * Rendering
 * ----------------------------------------------------------------------- */

/**
 * Render one locus out of an already-fetched chapter.
 *
 * Verses are emitted in ascending numeric order within the locus, but loci are
 * emitted in the order the citation lists them — a chant citation such as
 * "Psalm 138:18, 5-6" is deliberately out of sequence and must stay that way.
 */
function renderLocus(locus, fragment, language) {
  if (!fragment.ok) return notice(fragment.problem);

  const first = Number(locus.first);
  const last = Number(locus.last);
  const numbers = Object.keys(fragment.verses)
    .map(Number)
    .filter((n) => Number.isFinite(n) && n >= first && n <= last)
    .sort((a, b) => a - b);

  if (!numbers.length) {
    return notice(
      'this edition\'s ' + locus.book + ' ' + locus.chapter + ' has no verses ' +
      first + '-' + last + '.'
    );
  }

  const passage = el('p', 'passage');
  if (language) passage.lang = language;

  for (const number of numbers) {
    const verse = el('span', 'verse');
    const marker = el('sup', 'verse-num', String(number));
    marker.setAttribute('aria-hidden', 'true');
    verse.appendChild(marker);
    // The number is repeated for assistive technology, which does not get the
    // typographic cue that a superscript is a verse marker.
    verse.appendChild(el('span', 'visually-hidden', 'Verse ' + number + '. '));
    verse.appendChild(document.createTextNode(fragment.verses[number] + ' '));
    passage.appendChild(verse);
  }

  const gaps = [];
  for (let n = first; n <= last; n += 1) {
    if (!numbers.includes(n)) gaps.push(n);
  }
  if (gaps.length && gaps.length < last - first + 1) {
    const wrapper = document.createDocumentFragment();
    wrapper.appendChild(passage);
    wrapper.appendChild(
      notice(
        'verse' + (gaps.length > 1 ? 's ' : ' ') + gaps.join(', ') +
        ' of ' + locus.book + ' ' + locus.chapter +
        ' — absent from this edition\'s fragment.'
      )
    );
    return wrapper;
  }

  return passage;
}

function renderCitation(citation, bible, fragments) {
  const block = el('div', 'citation');

  // An unresolved citation always says why. It never renders as nothing.
  if (citation.unresolved) {
    block.appendChild(
      el('p', 'citation-ref', citation.ref || citation.book || citation.token ||
        'Unlabelled citation')
    );
    block.appendChild(notice(String(citation.unresolved)));
    return block;
  }

  const picked = lociFor(citation, bible.numbering);
  const label = citation.ref ||
    (picked.loci ? formatLoci(picked.loci) : null) ||
    citation.book || citation.token || 'Unlabelled citation';
  block.appendChild(el('p', 'citation-ref', label));

  if (!picked.loci) {
    block.appendChild(notice(picked.problem));
    return block;
  }

  for (const locus of picked.loci) {
    const fragment = fragments.get(locus.book + '|' + locus.chapter) ||
      { ok: false, problem: locus.book + ' ' + locus.chapter + ' was not loaded.' };
    block.appendChild(renderLocus(locus, fragment, bible.language));
  }

  return block;
}

function renderProper(proper, bible, fragments) {
  const section = el('section', 'proper');

  const heading = el('h3', 'proper-name', proper.name || 'Proper');
  section.appendChild(heading);

  if (proper.incipit) {
    section.appendChild(el('p', 'proper-incipit', proper.incipit));
  }

  const citations = proper.citations || [];

  // Composed propers (Collects, Secrets, Postcommunions) carry their own text
  // rather than a scripture citation. The structure file names no language for
  // it, so none is asserted here.
  if (proper.text) {
    const composed = el('p', 'composed');
    composed.appendChild(
      el('span', 'composed-label', 'Composed text — not scripture')
    );
    composed.appendChild(document.createTextNode(proper.text));
    if (proper.language) composed.lang = proper.language;
    section.appendChild(composed);
  }

  for (const citation of citations) {
    section.appendChild(renderCitation(citation, bible, fragments));
  }

  if (!proper.text && !citations.length) {
    section.appendChild(
      notice('this proper carries neither a citation nor a text.')
    );
  }

  return section;
}

function bibleMeta(bible) {
  const meta = [bible.label + ' — ' + bible.numbering + ' numbering'];
  if (bible.psalter) meta.push(bible.psalter + ' psalter');
  return meta;
}

function renderMass(entry, bible, fragments, chapterCount) {
  const mass = entry.mass;

  reading.appendChild(el('h2', 'entry-title', mass.name || mass.key));

  const meta = [];
  if (mass.season) meta.push('Season: ' + mass.season);
  if (mass.kind) meta.push(mass.kind);
  reading.appendChild(el('p', 'entry-meta', meta.concat(bibleMeta(bible)).join(' · ')));

  const propers = mass.propers || [];
  if (!propers.length) {
    reading.appendChild(
      el('p', 'placeholder', 'This Mass carries no propers in the structure file.')
    );
  }
  for (const proper of propers) {
    reading.appendChild(renderProper(proper, bible, fragments));
  }

  statusLine(
    (mass.name || mass.key) + ', ' + bible.label + '. ' +
    propers.length + ' propers, ' + chapterCount + ' chapters.'
  );
}

function renderReadingEntry(entry, bible, fragments, chapterCount) {
  const held = entry.reading;
  const position = entryIndex() + 1;

  reading.appendChild(
    el('h2', 'entry-title', held.title || readingReference(held) || entry.key)
  );

  const meta = ['Period: ' + entry.group];
  meta.push(tierLabel(held.tier) + ' tier');
  meta.push('Reading ' + position + ' of ' + state.entries.length);
  reading.appendChild(el('p', 'entry-meta', meta.concat(bibleMeta(bible)).join(' · ')));

  if (entry.period && entry.period.summary) {
    reading.appendChild(el('p', 'period-summary', String(entry.period.summary).trim()));
  }

  if (held.note) {
    const note = el('p', 'reading-note');
    note.appendChild(el('span', 'reading-note-label', 'Note'));
    note.appendChild(document.createTextNode(String(held.note).trim()));
    reading.appendChild(note);
  }

  const section = el('section', 'proper');
  section.appendChild(renderCitation(readingCitation(held), bible, fragments));
  reading.appendChild(section);

  // An abridgement that hides what it drops is the thing this plan refuses to
  // be, so its own account of its omissions travels with it — collapsed, but
  // never absent.
  if (state.plan && state.plan.omissions) {
    const details = document.createElement('details');
    details.className = 'omissions';
    details.appendChild(el('summary', null, 'What this plan does not read'));
    details.appendChild(el('p', 'omissions-body', String(state.plan.omissions).trim()));
    reading.appendChild(details);
  }

  statusLine(
    (held.title || entry.key) + ', ' + entry.group + ', ' + bible.label + '. ' +
    'Reading ' + position + ' of ' + state.entries.length + ' at the ' +
    tierLabel(state.tier) + ' tier, ' + chapterCount + ' chapters.'
  );
}

async function render(options) {
  const token = ++renderToken;
  const entry = currentEntry();
  const bible = currentBible();

  if (!entry || !bible) return;

  reading.setAttribute('aria-busy', 'true');

  const wanted = chaptersNeeded(entry, bible.numbering);
  const results = await Promise.all(
    wanted.map((needed) => loadChapter(bible.id, needed.book, needed.chapter))
  );

  // A later selection may have overtaken this one while fragments were in
  // flight; the newest render wins.
  if (token !== renderToken) return;

  const fragments = new Map();
  wanted.forEach((needed, index) => {
    fragments.set(needed.book + '|' + needed.chapter, results[index]);
  });

  clear(reading);

  if (entry.kind === 'reading') {
    renderReadingEntry(entry, bible, fragments, wanted.length);
  } else {
    renderMass(entry, bible, fragments, wanted.length);
  }

  reading.setAttribute('aria-busy', 'false');

  if (options && options.moveFocus) reading.focus();
}

/* --------------------------------------------------------------------------
 * Controls
 * ----------------------------------------------------------------------- */

function fillEntrySelect() {
  clear(entrySelect);
  const byGroup = new Map();
  for (const entry of state.entries) {
    const group = entry.group || 'other';
    if (!byGroup.has(group)) byGroup.set(group, []);
    byGroup.get(group).push(entry);
  }

  // Grouping keeps a long calendar — or a 357-reading plan — navigable from
  // the keyboard.
  const grouped = byGroup.size > 1;
  for (const [group, entries] of byGroup) {
    const parent = grouped
      ? entrySelect.appendChild(Object.assign(document.createElement('optgroup'), { label: group }))
      : entrySelect;
    for (const entry of entries) {
      const option = el('option', null, entry.label);
      option.value = entry.key;
      parent.appendChild(option);
    }
  }
  entrySelect.disabled = !state.entries.length;
}

function fillTierSelect() {
  clear(tierSelect);
  for (const tier of planTiers()) {
    const count = readingsAtTier(tier).length;
    const option = el(
      'option',
      null,
      tierLabel(tier) + ' — ' + count + ' reading' + (count === 1 ? '' : 's')
    );
    option.value = tier;
    tierSelect.appendChild(option);
  }
  tierSelect.disabled = false;
  if (state.tier) tierSelect.value = state.tier;
}

function fillBibleSelect() {
  clear(bibleSelect);
  for (const bible of state.bibles) {
    const label = bible.language
      ? bible.label + ' (' + bible.language + ')'
      : bible.label;
    const option = el('option', null, label);
    option.value = bible.id;
    bibleSelect.appendChild(option);
  }
  bibleSelect.disabled = false;
}

function syncControls() {
  modeSelect.value = state.mode;
  entryLabel.textContent = MODES[state.mode].entryLabel;
  tierField.hidden = state.mode !== 'readings';

  const key = state.selected[state.mode];
  if (key) entrySelect.value = key;
  if (state.tier) tierSelect.value = state.tier;
  if (state.bibleId) bibleSelect.value = state.bibleId;

  const index = entryIndex();
  prevButton.disabled = index <= 0;
  nextButton.disabled = index < 0 || index >= state.entries.length - 1;
}

function select(entryKey, bibleId, options) {
  if (entryKey) state.selected[state.mode] = entryKey;
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
function setTier(tier, options) {
  if (state.mode !== 'readings') return;
  if (planTiers().indexOf(tier) < 0) return;

  const previous = currentEntry();
  state.tier = tier;
  rebuildEntries();
  fillTierSelect();
  fillEntrySelect();

  let key = state.entries.some((entry) => entry.key === state.selected.readings)
    ? state.selected.readings
    : null;
  if (!key && previous) {
    let nearest = null;
    for (const entry of state.entries) {
      if (entry.order <= previous.order) nearest = entry;
    }
    key = nearest ? nearest.key : null;
  }
  if (!key && state.entries.length) key = state.entries[0].key;
  if (!key) {
    fail('The "' + tier + '" tier holds no readings.');
    return;
  }
  select(key, null, options);
}

/* --------------------------------------------------------------------------
 * Start-up
 * ----------------------------------------------------------------------- */

function fail(message) {
  clear(reading);
  reading.appendChild(el('p', 'error', message));
  reading.setAttribute('aria-busy', 'false');
  statusLine(message);
}

// One attempt per mode, remembered — including a failed one, so a site that
// publishes no reading plan is not asked for it again on every switch.
const structureAttempts = new Map();

function ensureStructure(mode) {
  const held = structureAttempts.get(mode);
  if (held) return held;

  const attempt = (async () => {
    let file;
    try {
      file = await loadJSON(MODES[mode].path);
    } catch (error) {
      return {
        ok: false,
        message: MODES[mode].what + ' could not be loaded: ' +
          (error.message || error)
      };
    } finally {
      // Whatever happened, the page has now had its one chance to discover
      // that the data root is unreachable.
      bootstrapping = false;
    }

    if (mode === 'propers') {
      state.masses = (file && file.masses) || [];
      state.calendarName = (file && file.calendar) || CALENDAR;
      if (!state.masses.length) {
        return {
          ok: false,
          message: 'The calendar "' + state.calendarName + '" lists no Masses.'
        };
      }
      return { ok: true };
    }

    state.plan = file || null;
    state.planName = (file && file.plan) || PLAN;
    if (!planPeriods().length) {
      return {
        ok: false,
        message: 'The reading plan "' + PLAN + '" lists no periods.'
      };
    }
    const problems = tierWarnings();
    if (problems.length) {
      showBanner(
        'The reading plan "' + PLAN + '" does not agree with itself: ' +
        problems.join('; ') + '.'
      );
    }
    return { ok: true };
  })();

  structureAttempts.set(mode, attempt);
  return attempt;
}

/**
 * Open a mode, loading its structure the first time it is asked for.
 *
 * `prefer` carries a selection out of the hash, so a shared link opens on the
 * reading it names rather than on the first one.
 */
async function setMode(mode, options, prefer) {
  if (!MODES[mode]) return;

  state.mode = mode;
  syncControls();

  const loaded = await ensureStructure(mode);
  // A reader who switched again while the structure was in flight wins.
  if (state.mode !== mode) return;

  // A mode that cannot load leaves the other one alone: the controls stay
  // live so the reader can switch back, and the reason is on the page.
  if (!loaded.ok) {
    state.entries = [];
    fillEntrySelect();
    tierSelect.disabled = true;
    syncControls();
    fail(loaded.message);
    return;
  }

  if (mode === 'readings') {
    const tiers = planTiers();
    const wanted = prefer && prefer.tier;
    state.tier = tiers.indexOf(wanted) >= 0
      ? wanted
      : (tiers.indexOf(state.tier) >= 0 ? state.tier : tiers[0]);
    fillTierSelect();
  }

  rebuildEntries();
  fillEntrySelect();

  const remembered = state.selected[mode];
  const preferred = prefer && prefer.key;
  const key = state.entries.some((entry) => entry.key === preferred)
    ? preferred
    : (state.entries.some((entry) => entry.key === remembered)
      ? remembered
      : (state.entries[0] && state.entries[0].key));

  if (!key) {
    fail(MODES[mode].what + ' offers nothing to read.');
    return;
  }

  select(key, null, options);
}

function preferenceFromHash(fromHash) {
  return {
    key: fromHash.mode === 'readings' ? fromHash.reading : fromHash.mass,
    tier: fromHash.tier
  };
}

async function start() {
  let biblesFile;
  try {
    biblesFile = await loadJSON('bibles.json');
  } catch (error) {
    bootstrapping = false;
    fail('The translation list could not be loaded: ' + (error.message || error));
    return;
  }

  state.bibles = (biblesFile && biblesFile.bibles) || [];
  if (!state.bibles.length) {
    bootstrapping = false;
    fail('bibles.json lists no translations.');
    return;
  }
  fillBibleSelect();

  const fromHash = readHash();
  state.bibleId = state.bibles.some((bible) => bible.id === fromHash.bible)
    ? fromHash.bible
    : state.bibles[0].id;

  // The hash names the mode when it has one; ?mode= is the fallback, and
  // propers is the default the page has always opened on.
  const mode = window.location.hash ? fromHash.mode : DEFAULT_MODE;
  await setMode(mode, { moveFocus: false }, preferenceFromHash(fromHash));
}

modeSelect.addEventListener('change', () => {
  setMode(modeSelect.value, { moveFocus: false });
});

tierSelect.addEventListener('change', () => {
  setTier(tierSelect.value, { moveFocus: false });
});

entrySelect.addEventListener('change', () => {
  select(entrySelect.value, null, { moveFocus: false });
});

bibleSelect.addEventListener('change', () => {
  select(null, bibleSelect.value, { moveFocus: false });
});

prevButton.addEventListener('click', () => step(-1, { moveFocus: true }));
nextButton.addEventListener('click', () => step(1, { moveFocus: true }));

controls.addEventListener('submit', (event) => event.preventDefault());

// Arrow keys step through the calendar or the plan, but never while a control
// has focus: left and right belong to the select the reader is operating.
document.addEventListener('keydown', (event) => {
  if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
  const target = event.target;
  if (target && target.closest && target.closest('select, input, textarea, button')) return;
  if (event.key === 'ArrowLeft') step(-1, { moveFocus: false });
  if (event.key === 'ArrowRight') step(1, { moveFocus: false });
});

window.addEventListener('hashchange', () => {
  if (suppressHashEvent) {
    suppressHashEvent = false;
    return;
  }
  const fromHash = readHash();
  const bibleId = state.bibles.some((bible) => bible.id === fromHash.bible)
    ? fromHash.bible
    : state.bibleId;
  state.bibleId = bibleId;

  if (fromHash.mode !== state.mode) {
    setMode(fromHash.mode, { moveFocus: false }, preferenceFromHash(fromHash));
    return;
  }

  if (state.mode === 'readings' && fromHash.tier && fromHash.tier !== state.tier) {
    setTier(fromHash.tier, { moveFocus: false });
  }

  const wanted = preferenceFromHash(fromHash).key;
  const key = state.entries.some((entry) => entry.key === wanted)
    ? wanted
    : state.selected[state.mode];
  select(key, bibleId, { moveFocus: false });
});

start();
