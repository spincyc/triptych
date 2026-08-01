/* ===========================================================================
 * The Code, canon by canon — the model
 * ===========================================================================
 *
 * Arithmetic and lookup only. It knows nothing about the DOM, and it decides
 * nothing about canon law.
 *
 * THE RECORD DECLARES ITS OWN VOCABULARY, AND THIS READS IT. `act-history`
 * emits one shape for two kinds of slice: a missal's units are prayers standing
 * in a Mass, a code's are canons standing in a division. The slice says which
 * it is — `vocabulary`, `group_key`, `group_word`, `unit_word` on the spine —
 * and everything below asks the record rather than assuming a Code. A page that
 * guessed would be the same defect as a page that called a title of the Code a
 * `mass`: a reference that resolves successfully and wrongly.
 *
 * A CANON'S NUMBER IS READ FROM THE FORMS THE GENERATOR WRITES, and from
 * nothing else. `act-history` derives a canon unit's identity from one typed
 * number, and writes it in three places whose shapes are fixed:
 *
 *     name  "can. 1012 §1"      the citation, as a lawyer says it
 *     slot  "can-0012-01"       zero-padded, so a listing sorts as the Code reads
 *     unit  "cic17-c-1012-1"    the id, unpadded, because ids are read by people
 *
 * Those three are matched exactly. Anything else is NOT a canon as far as this
 * page is concerned, and is findable by its words rather than by a number.
 * There is deliberately no "last run of digits" fallback: it would read
 * `cic17-c-1012-1` as canon 1, which is a citation to the wrong law, and a
 * wrong citation is worse than no citation.
 *
 * PARAGRAPHS ARE BASE UNITS, SO A CANON IS A GROUP OF THEM. `c. 1095 §2` is one
 * row in the record; `c. 1095` is the three rows that share a number and a
 * division. Assembling them is grouping the record's own rows and is not a
 * claim about the law; nothing here invents a paragraph that has no row.
 *
 * IT DERIVES NO CHANGE, AND NO CORRESPONDENCE. What an act did to a canon is
 * `act-history structure`'s answer, written into the fragments. Whether a canon
 * of one Code answers to a canon of another is a scholarly claim carried with
 * its source, or it is nothing.
 * ======================================================================== */

window.TriptychCode = (function () {
  'use strict';

  /* Two kinds of station — `promulgated` against `printed` — is a statement
   * about evidence, is read and never inferred, and the rule lives in the
   * shared machinery because more than one page reads it. */
  const KIND = window.Triptych.stationKind;

  /* ------------------------------------------------------------------------
   * What this slice calls things
   *
   * Read from the spine, with the missal's words as the fallback because that
   * is what a slice written before the vocabulary existed holds. Both names are
   * accepted everywhere a container is looked for, so a page never has to know
   * which kind of slice it was handed.
   * --------------------------------------------------------------------- */

  const DEFAULT_VOCABULARY = {
    vocabulary: 'liturgy',
    group_key: 'masses',
    group_word: 'mass',
    unit_word: 'unit'
  };

  let vocabulary = DEFAULT_VOCABULARY;

  function readVocabulary(spine) {
    vocabulary = {
      vocabulary: (spine && spine.vocabulary) || DEFAULT_VOCABULARY.vocabulary,
      group_key: (spine && spine.group_key) || DEFAULT_VOCABULARY.group_key,
      group_word: (spine && spine.group_word) || DEFAULT_VOCABULARY.group_word,
      unit_word: (spine && spine.unit_word) || DEFAULT_VOCABULARY.unit_word
    };
    return vocabulary;
  }

  function words() {
    return vocabulary;
  }

  /** The containers a fragment carries, under whichever key it keeps them. */
  function groupsIn(payload) {
    if (!payload) return [];
    const stated = payload[vocabulary.group_key];
    if (Array.isArray(stated)) return stated;
    if (Array.isArray(payload.divisions)) return payload.divisions;
    if (Array.isArray(payload.masses)) return payload.masses;
    return [];
  }

  /** The container one row stands in, under whichever key it keeps it. */
  function groupOf(row) {
    if (!row) return '';
    const stated = row[vocabulary.group_word];
    if (stated) return String(stated);
    return String(row.division || row.mass || '');
  }

  /* ------------------------------------------------------------------------
   * A citation is how this material is referenced
   *
   * A canon lawyer arrives with `c. 1095 §2`, `can. 1095, § 2`, `1095.2` or
   * plain `1095`. All of them mean the same place. What comes back is the
   * number and, where one was given, the paragraph — never a canon, because
   * whether that canon exists is the record's answer and not this function's.
   * --------------------------------------------------------------------- */

  const TYPED = new RegExp(
    '^\\s*(?:canons|canon|cann|can|cc|c)?\\.?\\s*' +      // c. / can. / canon, or nothing
    '(\\d{1,4})' +                                        // the number
    '(?:\\s*,?\\s*(?:§+|par\\.|n\\.|\\.)\\s*(\\d{1,2}))?' +  // § 2 / , § 2 / .2 / par. 2
    '\\s*$',
    'i'
  );

  function parseCitation(text) {
    const found = TYPED.exec(String(text || ''));
    if (!found) return null;
    return { canon: found[1], paragraph: found[2] || null };
  }

  /* The three forms the generator writes, matched whole. Order is by how
   * directly each states the number, not by how likely it is to be there. */
  const FROM_NAME = /^\s*cann?\.\s*(\d{1,4})(?:\s*§\s*(\d{1,3}))?\s*$/i;
  const FROM_SLOT = /^can-0*(\d{1,4})(?:-0*(\d{1,3}))?$/;
  const FROM_ID = /-c-(\d{1,4})(?:-(\d{1,3}))?$/;

  /** The canon and paragraph a row stands at, or nulls where it is not a canon. */
  function numberOf(row) {
    if (!row) return { canon: null, paragraph: null };
    if (row.canon !== undefined && row.canon !== null && row.canon !== '') {
      const paragraph = row.paragraph;
      return {
        canon: String(row.canon),
        paragraph: paragraph === undefined || paragraph === null || paragraph === ''
          ? null : String(paragraph)
      };
    }
    const tries = [
      [FROM_NAME, row.name],
      [FROM_SLOT, row.slot],
      [FROM_ID, row.unit]
    ];
    for (let index = 0; index < tries.length; index += 1) {
      const found = tries[index][0].exec(String(tries[index][1] || ''));
      if (found) {
        return {
          canon: String(Number(found[1])),
          paragraph: found[2] === undefined ? null : String(Number(found[2]))
        };
      }
    }
    return { canon: null, paragraph: null };
  }

  function canonOf(row) {
    return numberOf(row).canon || '';
  }

  function paragraphOf(row) {
    return numberOf(row).paragraph;
  }

  /** How one row is cited. The record's own form wins; `c. n §p` is composed
   *  only where the record writes none. */
  function citationOf(row) {
    if (!row) return '';
    if (row.name) return String(row.name);
    const at = numberOf(row);
    if (at.canon) return 'c. ' + at.canon + (at.paragraph ? ' §' + at.paragraph : '');
    return String(row.slot || row.unit || '');
  }

  /** How a whole canon is cited, paragraphs left off. */
  function canonCitation(canon) {
    return canon ? 'c. ' + canon : '';
  }

  function orderOf(row) {
    if (row && typeof row.order === 'number') return row.order;
    const at = numberOf(row);
    if (!at.canon) return Number.MAX_SAFE_INTEGER;
    return Number(at.canon) * 100 + Number(at.paragraph || 0);
  }

  function byOrder(a, b) {
    const left = orderOf(a);
    const right = orderOf(b);
    if (left !== right) return left - right;
    return String((a && a.unit) || '').localeCompare(String((b && b.unit) || ''));
  }

  /* ------------------------------------------------------------------------
   * A canon is the rows that share its number within one division
   *
   * The division, not the whole record: two Codes number independently, so
   * c. 1012 of one and c. 1012 of the other are different canons and must never
   * fall into one group. Which body of law each belongs to is the record's to
   * say — `line` on the row where the record carries it, and the division
   * otherwise.
   * --------------------------------------------------------------------- */

  function canonKey(row) {
    return (row.line || groupOf(row) || '') + '/' + canonOf(row);
  }

  /** Group index rows into canons, each with its paragraph rows in order. */
  function canons(rows) {
    const found = new Map();
    (rows || []).forEach(function (row) {
      const canon = canonOf(row);
      if (!canon) return;
      const key = canonKey(row);
      if (!found.has(key)) {
        found.set(key, {
          key: key,
          canon: canon,
          line: row.line || '',
          group: groupOf(row),
          rows: []
        });
      }
      found.get(key).rows.push(row);
    });
    found.forEach(function (entry) { entry.rows.sort(byOrder); });
    return Array.from(found.values());
  }

  /**
   * The canons a citation names.
   *
   * Exact, never nearest. A citation that matches nothing is a citation this
   * record does not carry, and saying so is the answer; offering a neighbouring
   * canon instead would put a reader on the wrong law. A citation that names a
   * paragraph MARKS that paragraph and drops none of the others: a canon is
   * read whole even when §2 is the one being argued about.
   */
  function find(rows, cited) {
    if (!cited) return [];
    return canons(rows)
      .filter(function (entry) { return entry.canon === cited.canon; })
      .map(function (entry) {
        return cited.paragraph
          ? Object.assign({}, entry, { asked: cited.paragraph })
          : entry;
      });
  }

  /** Free-text search, for the reader who is not citing but looking. */
  function matches(row, query) {
    const needle = String(query || '').trim().toLowerCase();
    if (!needle) return true;
    return [row.unit, row.slot, row.name, groupOf(row), row.line]
      .join(' ').toLowerCase().indexOf(needle) !== -1;
  }

  /* ------------------------------------------------------------------------
   * The Code's own structure, as navigation
   *
   * Built from what each row states about where it stands and from nothing
   * else. Where the record states a chain of ancestors — Book, Part, Title,
   * Chapter — the tree is that deep. Where it names one container, the tree is
   * one level deep, and that flatness is the honest picture of a record that
   * names no hierarchy. An identifier is never split to guess a hierarchy: that
   * would be this page modelling the Code, which is the one thing it must not
   * do.
   * --------------------------------------------------------------------- */

  /** Titles for containers, wherever the record has told us any. */
  const titles = new Map();

  function learnGroups(payload) {
    groupsIn(payload).forEach(function (group) {
      const id = groupOf(group) || group.id;
      if (!id) return;
      const label = group.title || group.designation || '';
      if (label) titles.set(String(id), label);
    });
  }

  function groupLabel(id) {
    return titles.get(String(id)) || String(id || '');
  }

  function chainOf(row) {
    const stated = row && (row.divisions || row.ancestors);
    if (Array.isArray(stated) && stated.length) {
      return stated.map(function (step, position) {
        const id = step.id || step.division || step.mass || String(position);
        return {
          kind: step.kind || step.designation || '',
          id: String(id),
          label: step.label || step.title || groupLabel(id)
        };
      });
    }
    const only = groupOf(row);
    if (!only) return [];
    return [{ kind: '', id: only, label: groupLabel(only) }];
  }

  function tree(rows) {
    const roots = [];
    const at = new Map();

    canons(rows).sort(function (a, b) { return byOrder(a.rows[0], b.rows[0]); })
      .forEach(function (entry) {
        const chain = chainOf(entry.rows[0]);
        if (!chain.length) {
          roots.push({
            id: 'unplaced', key: 'unplaced', kind: '', label: '',
            children: [], canons: [entry], unplaced: true
          });
          return;
        }
        let siblings = roots;
        let key = '';
        let node = null;
        chain.forEach(function (step) {
          key = key ? key + ' ' + step.id : step.id;
          node = at.get(key);
          if (!node) {
            node = {
              id: step.id, key: key, kind: step.kind, label: step.label,
              children: [], canons: []
            };
            at.set(key, node);
            siblings.push(node);
          }
          siblings = node.children;
        });
        node.canons.push(entry);
      });
    return roots;
  }

  /** How many canons stand at or below a node. */
  function countIn(node) {
    return node.canons.length + node.children.reduce(function (total, child) {
      return total + countIn(child);
    }, 0);
  }

  /* ------------------------------------------------------------------------
   * The other axis: the acts
   * --------------------------------------------------------------------- */

  /**
   * The extent of one act, as a single number, read off the counts the
   * generator wrote. The container count arrives under the slice's own name, so
   * both are looked for: a page that knew one name would silently undercount.
   */
  function magnitude(station) {
    const changed = (station && station.changed) || {};
    const containers = changed[vocabulary.group_key + '_touched'];
    return (changed.units_entered || 0) + (changed.units_gone || 0) +
      (changed.units_changed || 0) + (changed.unestablished || 0) +
      (containers || changed.divisions_touched || changed.masses_touched || 0) +
      (changed.interpretations || 0);
  }

  function containersTouched(changed) {
    if (!changed) return 0;
    return changed[vocabulary.group_key + '_touched'] ||
      changed.divisions_touched || changed.masses_touched || 0;
  }

  /** Stations by date, earliest first, ties broken by the graph's own order. */
  function byDate(stations) {
    return (stations || []).map(function (station, position) {
      return { station: station, position: position };
    }).sort(function (a, b) {
      const left = String(a.station.date || '');
      const right = String(b.station.date || '');
      if (left !== right) return left < right ? -1 : 1;
      return a.position - b.position;
    }).map(function (row) { return row.station; });
  }

  /* ------------------------------------------------------------------------
   * One side of a canon
   *
   * Three states, never two: words present; words this record never carried;
   * and words that exist and may not be published here. The last two look
   * identical in the data — both are an empty string — and are told apart only
   * by whether a reason is carried. A page that collapsed them would report a
   * rights position as ignorance, or an absence as a blank canon.
   * --------------------------------------------------------------------- */

  const PRESENT = 'present';
  const WITHHELD = 'withheld';
  const UNREAD = 'unread';

  function bodyOf(side) {
    if (!side) return { state: UNREAD, text: '', reason: '', established: '' };
    const text = side.text || side.incipit || '';
    const established = side.established_at || '';
    if (text) return { state: PRESENT, text: String(text), reason: '', established: established };
    if (side.withheld) {
      return { state: WITHHELD, text: '', reason: String(side.withheld), established: established };
    }
    return { state: UNREAD, text: '', reason: '', established: established };
  }

  /** Where a canon is carried in more than one edition, each of them. */
  function editionsOf(side) {
    const held = side && side.editions;
    if (!Array.isArray(held) || !held.length) return [];
    return held.map(function (edition, position) {
      return {
        id: edition.edition || edition.id || String(position),
        label: edition.label || edition.edition || edition.language || edition.id || '',
        language: edition.language || '',
        body: bodyOf(edition)
      };
    });
  }

  /* ------------------------------------------------------------------------
   * An interpretation is not a change
   *
   * An authentic interpretation settles what a canon MEANS without altering a
   * syllable of what it says, so the generator gives it its own stop in a
   * canon's history with no before, no after and no departure kind. Drawing it
   * as a change would say the legislator rewrote a canon nobody rewrote. Its
   * FORCE decides whether it binds retroactively, so it is carried and shown
   * rather than averaged into "an interpretation was given".
   * --------------------------------------------------------------------- */

  const INTERPRETED = 'interpreted';

  const FORCE_WORDS = {
    declarative: 'declarative — it declares words certain in themselves, and is ' +
      'retroactive; it needed no promulgation',
    restrictive: 'restrictive — it narrows the law, and is not retroactive',
    extensive: 'extensive — it widens the law, and is not retroactive',
    'explaining-a-doubt': 'explaining a doubtful law — it is not retroactive',
    unstated: 'the record does not state which force this interpretation has'
  };

  function forceWords(force) {
    return FORCE_WORDS[force] || FORCE_WORDS.unstated;
  }

  function isInterpretation(stop) {
    // Boolean, not the field itself: a stop that is a change carries no
    // `interpretation`, so the bare `||` returned `undefined` and a caller
    // asking "is this an interpretation" got neither yes nor no.
    return Boolean(stop && (stop.state === INTERPRETED || stop.interpretation));
  }

  return {
    KIND: KIND,
    PRESENT: PRESENT,
    WITHHELD: WITHHELD,
    UNREAD: UNREAD,
    INTERPRETED: INTERPRETED,

    readVocabulary: readVocabulary,
    words: words,
    groupsIn: groupsIn,
    groupOf: groupOf,
    learnGroups: learnGroups,
    groupLabel: groupLabel,

    parseCitation: parseCitation,
    numberOf: numberOf,
    canonOf: canonOf,
    paragraphOf: paragraphOf,
    citationOf: citationOf,
    canonCitation: canonCitation,
    orderOf: orderOf,
    byOrder: byOrder,
    canons: canons,
    find: find,
    matches: matches,

    chainOf: chainOf,
    tree: tree,
    countIn: countIn,

    magnitude: magnitude,
    containersTouched: containersTouched,
    byDate: byDate,

    bodyOf: bodyOf,
    editionsOf: editionsOf,

    forceWords: forceWords,
    isInterpretation: isInterpretation
  };
}());
