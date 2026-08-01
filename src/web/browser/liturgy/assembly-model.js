/* ===========================================================================
 * How a day's Mass is assembled — the derivation, and nothing else
 * ===========================================================================
 *
 * THIS FILE IS NOT A PAGE. It takes three plain objects — a civil date, the
 * calendar year file that says which masses the arithmetic puts on it, and the
 * rubrics file that says how they are ranked — and returns the argument that
 * gets from one to the other. It touches no DOM, fetches nothing, and knows
 * nothing about the browser. `day.js` renders what it returns; `calendar-rubrics
 * check` runs it under node against the solved cases each rubrics source
 * carries. One implementation, so the page and the check cannot drift.
 *
 * IT ASSERTS NO RULE OF ITS OWN. Every rank, every disposition and every
 * ceiling below is read out of the rubrics file, which carries the rubric
 * number beside it. What lives here is only the order in which the questions
 * are asked — the five decisions of `guidance/liturgy/roman-1962-assembly.md` —
 * and the arithmetic of comparing two numbers. If a result here is wrong, the
 * fix is in `src/sources/calendars/<calendar>/rubrics.yaml`, where it can be
 * argued with.
 *
 * WHAT IT REFUSES TO DO, AND WHY THAT IS THE POINT
 *
 * The standing failure of a tool like this is to resolve successfully and
 * wrongly: to hand back a confident answer that a competent Ordo would not
 * recognise. So every path that cannot be settled from the rules the repository
 * actually holds ends in `settled: false` with a reason, and never in a guess:
 *
 *   - two candidates that land on the same row, where the table orders within
 *     the row by a property no mass key carries;
 *   - a candidate the rubrics source has no assignment rule for;
 *   - a day constituted from its season where this repository cannot exclude a
 *     competing identity for it — the Ember Days it does not date;
 *   - a transfer destination, which is stated as a rule and computed only at
 *     the two seats the rubric itself names.
 *
 * A result carrying `conditions` is one that holds only if those conditions do.
 * A renderer that drops them is misrepresenting it.
 * ======================================================================== */

'use strict';

(function (root, factory) {
  const api = factory();
  root.MassAssembly = api;
  if (typeof module === 'object' && module && module.exports) module.exports = api;
}(typeof globalThis !== 'undefined' ? globalThis : this, function () {

  /* ------------------------------------------------------------------------
   * Dates
   *
   * Everything is UTC. A civil date here is a label on a calendar, not an
   * instant, and reading "2027-03-17" through a local timezone turns it into
   * the 16th for half the world.
   * --------------------------------------------------------------------- */

  const DAY = 86400000;
  const WEEKDAYS = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'];

  function stamp(iso) {
    return Date.parse(iso + 'T00:00:00Z');
  }

  function iso(value) {
    return new Date(value).toISOString().slice(0, 10);
  }

  function shift(isoDate, days) {
    return iso(stamp(isoDate) + days * DAY);
  }

  function weekdayOf(isoDate) {
    return WEEKDAYS[new Date(stamp(isoDate)).getUTCDay()];
  }

  function monthDay(isoDate) {
    return isoDate.slice(5);
  }

  /** Is MM-DD inside [from, to], where the window may cross the year end? */
  function inWindow(md, from, to) {
    if (from && to) return from <= to ? (md >= from && md <= to) : (md >= from || md <= to);
    if (from) return md >= from;
    if (to) return md <= to;
    return true;
  }

  /* ------------------------------------------------------------------------
   * Reading the year file
   * --------------------------------------------------------------------- */

  /**
   * The liturgical year that owns a civil date.
   *
   * A civil-year file carries two of them — the one running out in November and
   * the one beginning in Advent — and the anchors differ between them. Picking
   * the wrong one puts Easter in the wrong April.
   */
  function liturgicalYearFor(year, isoDate) {
    const held = year.liturgical_years || [];
    for (const row of held) {
      if (row.begins <= isoDate && isoDate <= row.ends) return row;
    }
    return held[held.length - 1] || null;
  }

  function seasonOf(owner, isoDate) {
    for (const span of (owner && owner.seasons) || []) {
      if (span.from <= isoDate && isoDate <= span.to) return span.season;
    }
    return null;
  }

  function weekOf(owner, isoDate) {
    for (const span of (owner && owner.ordinary_time_weeks) || []) {
      if (span.from <= isoDate && isoDate <= span.to) return span.week;
    }
    return null;
  }

  function anchor(owner, name) {
    return (owner && owner.anchors && owner.anchors[name]) || null;
  }

  /* ------------------------------------------------------------------------
   * Candidates
   * --------------------------------------------------------------------- */

  function basisOf(rubrics, index) {
    return (rubrics.bases || [])[index] || null;
  }

  const UNCLASSIFIED = {
    id: 'not-classified',
    row: null,
    nature: 'unknown',
    commemoration: 'none',
    competes: false,
    certain: false,
    why: 'this key is not in the rubrics file at all, so nothing here classifies it',
    locus: null
  };

  function classify(rubrics, key) {
    const held = (rubrics.keys || {})[key];
    if (!held) return { basis: UNCLASSIFIED, name: null, known: false };
    return { basis: basisOf(rubrics, held.basis) || UNCLASSIFIED, name: held.name, known: true };
  }

  function rowLabel(rubrics, row) {
    for (const entry of (rubrics.precedence && rubrics.precedence.rows) || []) {
      if (entry.row === row) return entry;
    }
    return null;
  }

  /**
   * The celebrations the calendar index puts on this date.
   *
   * Three of the postconciliar celebrations are inscribed twice, once as a
   * temporal key that a territorial decision can move and once as a fixed-date
   * key. They are one celebration; left uncollapsed they would tie with
   * themselves and the day would be reported unsettled.
   */
  function indexCandidates(year, rubrics, isoDate) {
    const rows = (year.days || {})[isoDate] || [];
    const collapsed = [];
    const folded = [];
    const groups = rubrics.same_celebration || [];

    for (const row of rows) {
      const group = groups.find(
        (one) => one.keep === row.key || (one.also || []).indexOf(row.key) >= 0
      );
      if (group && group.keep !== row.key && rows.some((other) => other.key === group.keep)) {
        folded.push({ key: row.key, into: group.keep, what: group.what });
        continue;
      }
      const found = classify(rubrics, row.key);
      collapsed.push({
        id: row.key,
        key: row.key,
        name: found.name || row.key,
        known: found.known,
        basis: found.basis,
        row: found.basis.row,
        source: 'index',
        rule: (year.rules || [])[row.rule] || null,
        territorial: row.territorial || null,
        certain: found.basis.certain !== false,
        alsoInscribedAs: group && group.keep === row.key
          ? (group.also || []).filter((other) => rows.some((one) => one.key === other))
          : []
      });
    }
    return { candidates: collapsed, folded: folded };
  }

  /**
   * The Mass a feria borrows, where nothing else on the date supplies one.
   *
   * RGMR 299 gives most ferias the preceding Sunday's Mass rather than one of
   * their own, and the year file records which under `ferial_formulary`.
   * Nothing read it, so on 77 dates of 2026 the page showed a commemoration
   * alone or nothing at all where the missal appoints a whole formulary — a
   * commemoration is said within a Mass, never instead of one.
   *
   * This is decided against the index AND the arrivals together. Deciding it
   * against the index alone put the borrowed Mass on All Souls, whose own
   * celebration arrives rather than being inscribed, and it beat the day.
   */
  function ferialCandidates(year, rubrics, isoDate, present) {
    const holdsAMass = present.some(
      (one) => !(one.basis && one.basis.nature === 'commemoration')
    );
    if (holdsAMass) return [];
    return ((year.ferial_formulary || {})[isoDate] || []).map(function (row) {
      const found = classify(rubrics, row.key);
      return {
        id: row.key,
        key: row.key,
        name: found.name || row.key,
        known: found.known,
        basis: found.basis,
        row: found.basis.row,
        source: 'ferial',
        borrowed: true,
        rule: (year.rules || [])[row.rule] || null,
        territorial: row.territorial || null,
        certain: found.basis.certain !== false,
        alsoInscribedAs: []
      };
    });
  }

  /**
   * The day the rubrics constitute where the index carries no formulary.
   *
   * RGMR 299 gives most ferias the preceding Sunday's Mass rather than one of
   * their own, so on a great many dates the day that a feast is measured
   * against has no mass key at all. Skipping it would silently hand every such
   * date to the saint. These rules reconstruct it from the season the year file
   * already computed and from the civil date, which is how the rubrics
   * themselves state it; no season boundary is recomputed here.
   *
   * Fires only when the date carries no temporal candidate of its own.
   */
  function impliedCandidate(rubrics, owner, isoDate, season, present) {
    // Suppressed when the day's own temporal identity is already on the date.
    // Testing the rule's origin alone was not enough: this calendar files the
    // fifth, sixth and seventh days within the Christmas octave under a fixed
    // date, so the implied octave day was constituted a second time and the two
    // tied at row 17 on every 29, 30 and 31 December in the span.
    if (present.some((one) => one.basis && one.basis.constitutes_the_day)) return null;
    if (present.some((one) => one.rule && one.rule.origin === 'temporal')) return null;

    const weekday = weekdayOf(isoDate);
    const md = monthDay(isoDate);

    for (const rule of rubrics.implied || []) {
      if (rule.season && rule.season !== season) continue;
      if (rule.weekday_only && weekday === 'sunday') continue;
      if (rule.on_anchor && anchor(owner, rule.on_anchor) !== isoDate) continue;
      if ((rule.from || rule.to) && !inWindow(md, rule.from, rule.to)) continue;
      if (rule.from_anchor) {
        const from = anchor(owner, rule.from_anchor.anchor);
        if (!from || isoDate < shift(from, rule.from_anchor.offset_days || 0)) continue;
      }
      if (rule.to_anchor) {
        const to = anchor(owner, rule.to_anchor.anchor);
        if (!to || isoDate > shift(to, rule.to_anchor.offset_days || 0)) continue;
      }
      if (rule.before_anchor) {
        const before = anchor(owner, rule.before_anchor.anchor);
        if (!before || isoDate >= shift(before, rule.before_anchor.offset_days || 0)) continue;
      }

      let basis = basisOf(rubrics, rule.basis);
      let office = null;
      // RG 78: on a Saturday carrying a fourth-class feria the Office is of Our
      // Lady on Saturday. It is an Office and not a feast, and it sits below
      // every third-class feast, so naming it changes what the day is called
      // without changing what wins.
      const saturday = rubrics.saturday_office;
      if (
        saturday && !saturday.stated_only && weekday === 'saturday' &&
        basis && saturday.when_implied_basis === basis.id
      ) {
        office = { underlying: basis, locus: saturday.locus, why: saturday.why };
        basis = basisOf(rubrics, saturday.basis) || basis;
      }
      if (!basis) continue;

      return {
        id: 'implied:' + rule.id,
        key: null,
        // The rule's own label where it has one, because "Ash Wednesday" is a
        // better name for the day than "a weekday of Holy Week or Ash Wednesday".
        name: rule.label || basis.label || basis.why,
        known: true,
        basis: basis,
        row: basis.row,
        source: 'implied',
        impliedBy: rule,
        rule: null,
        territorial: null,
        certain: rule.certain !== false,
        caveat: rule.certain === false ? rule.unless : null,
        note: rule.note || null,
        office: office
      };
    }
    return null;
  }

  /**
   * A celebration that a named rubric moves onto this date from another.
   *
   * Only the seats the rubric itself fixes by name are computed. The general
   * destination rule — the next following day that is not first or second class
   * — depends on the class of every intervening day and on the order in which
   * several transferred feasts are placed, and guessing it would be asserting
   * an Ordo result nobody here has checked. So the page states that rule and
   * computes these two.
   */
  function arrivals(rubrics, owner, isoDate) {
    const transfer = (rubrics.impediment && rubrics.impediment.transfer) || {};
    const found = [];
    const civilYear = isoDate.slice(0, 4);

    for (const seat of transfer.proper_seats || []) {
      const ownDate = civilYear + '-' + seat.own_date;
      let seatDate = null;
      let impeded = false;

      if (seat.seat_easter_offset != null) {
        const easter = anchor(owner, 'easter');
        if (!easter) continue;
        seatDate = shift(easter, seat.seat_easter_offset);
        const window = seat.impeded_when_easter_offset_between || [];
        const offset = Math.round((stamp(ownDate) - stamp(easter)) / DAY);
        impeded = offset >= window[0] && offset <= window[1];
      } else if (seat.seat_offset_days != null) {
        seatDate = shift(ownDate, seat.seat_offset_days);
        impeded = !seat.impeded_when_weekday || weekdayOf(ownDate) === seat.impeded_when_weekday;
      }

      if (!impeded || seatDate !== isoDate) continue;
      const held = classify(rubrics, seat.key);
      found.push({
        id: seat.key,
        key: seat.key,
        name: held.name || seat.key,
        known: held.known,
        basis: held.basis,
        row: held.basis.row,
        source: 'arrived',
        arrivedFrom: ownDate,
        seat: seat,
        rule: null,
        territorial: null,
        certain: true
      });
    }
    return found;
  }

  /**
   * Celebrations the Missal carries that this calendar index does not.
   *
   * A missing formulary is not a neutral gap. On the last Sunday of October the
   * derivation would otherwise announce a numbered Sunday after Pentecost as
   * the day, which Christ the King displaces — a confident, wrong answer of
   * exactly the kind this file exists to refuse. So the absences are dated in
   * the rubrics source and reported at the date they would have occupied.
   */
  function absencesOn(rubrics, isoDate) {
    const md = monthDay(isoDate);
    const weekday = weekdayOf(isoDate);
    return (rubrics.known_absences || []).filter(function (entry) {
      const match = entry.match || {};
      if (match.weekday && match.weekday !== weekday) return false;
      if ((match.from || match.to) && !inWindow(md, match.from, match.to)) return false;
      if (match.on && match.on !== md) return false;
      return true;
    });
  }

  /* ------------------------------------------------------------------------
   * The territorial split
   *
   * A candidate tagged with an option holds only where the competent authority
   * has taken that option. The derivation is therefore run once per option
   * present, and the page shows both. Choosing one here would be inventing a
   * territorial decision out of arithmetic, which is exactly what the calendar
   * layer refuses to do.
   * --------------------------------------------------------------------- */

  /**
   * Every option the day must be derived under, not merely the ones tagged here.
   *
   * The trap: on 14 May 2026 the Ascension is tagged `ascension-thursday` and
   * Saint Matthias is tagged with nothing. Branching only over the tags present
   * would derive the Thursday form alone — and the whole point of the other
   * branch is that the Ascension is *absent* from that date, which leaves the
   * feast standing. So the families are read from the year file, and every
   * option of an involved family gets a branch, including the ones under which
   * a candidate simply does not hold.
   */
  function optionsToDerive(year, candidates) {
    const present = [];
    for (const one of candidates) {
      if (one.territorial && present.indexOf(one.territorial) < 0) present.push(one.territorial);
    }
    if (!present.length) return [];

    const held = [];
    for (const family of Object.keys(year.territorial || {})) {
      const options = (year.territorial[family] || {}).options;
      if (!Array.isArray(options)) continue;
      if (!options.some((option) => present.indexOf(option) >= 0)) continue;
      for (const option of options) if (held.indexOf(option) < 0) held.push(option);
    }
    // A tag whose family the year file does not describe still gets its branch,
    // rather than being quietly dropped into the untagged case.
    for (const option of present) if (held.indexOf(option) < 0) held.push(option);
    return held;
  }

  /* ------------------------------------------------------------------------
   * Decision two: which day takes the day
   * --------------------------------------------------------------------- */

  function competes(one) {
    return one.basis && one.basis.competes !== false && one.row != null;
  }

  function rank(rubrics, candidates, unsettled) {
    const contest = [];
    const defeated = [];
    // An entry the calendar inscribes as a commemoration occupies no row of the
    // table, so it can never take the day — but it is still due its collect.
    // Dropping it here for not competing is how a third collect goes missing.
    const standingAside = [];

    for (const one of candidates) {
      if (!one.known) {
        unsettled.push({
          what: one.id,
          why: 'the rubrics source carries no assignment rule for this mass, so it cannot be ranked'
        });
        continue;
      }
      if (!competes(one)) {
        if (one.basis.commemoration && one.basis.commemoration !== 'none') standingAside.push(one);
        continue;
      }
      contest.push(one);
    }

    // Overrides run before the comparison, because each of them defeats a
    // candidate that the row numbers alone would have made the winner.
    for (const override of rubrics.overrides || []) {
      if (override.stated_only || !override.key) continue;
      const target = contest.find((one) => one.key === override.key);
      if (!target) continue;

      if (override.yields_to) {
        const beats = contest.find((one) => one !== target && one.basis.nature === override.yields_to);
        if (!beats) continue;
        target.defeatedBy = { override: override, by: beats.id };
        defeated.push(target);
        continue;
      }
      // The other direction: a named celebration that takes a slot from
      // whatever else the arithmetic put in it.
      if (override.over_key_matches) {
        const pattern = new RegExp(override.over_key_matches);
        for (const one of contest) {
          if (one === target || !one.key || !pattern.test(one.key)) continue;
          if (override.when_same_row && one.row !== target.row) continue;
          one.defeatedBy = { override: override, by: target.id };
          defeated.push(one);
        }
      }
    }

    const standing = contest.filter((one) => defeated.indexOf(one) < 0);
    if (!standing.length) return { winner: null, contest: contest, defeated: defeated, aside: standingAside };

    let best = standing[0];
    for (const one of standing) if (one.row < best.row) best = one;
    const tied = standing.filter((one) => one.row === best.row);

    if (tied.length > 1) {
      // A tie at a row the rubrics mark optional is not a gap in the rules: the
      // rules say the choice belongs to the celebrant. Anywhere else it is a
      // gap, and the derivation stops.
      if (tied.every((one) => one.basis.optional)) {
        return { winner: null, contest: contest, defeated: defeated, aside: standingAside, choice: tied };
      }
      // Naming the rule that would settle it is the useful part. Several of
      // the real ties turn on the identity of a divine Person or of a saint,
      // which the source declares and deliberately never applies.
      const stated = (rubrics.overrides || []).filter((one) => one.stated_only);
      unsettled.push({
        // The NAME, not the id. A mass key is `ss-septem-fratrum-martyrum-ac-ss`,
        // and this is the one place the model put one into a sentence the page
        // prints — so a tied day rendered what read as corrupted text in the
        // margin. Every other candidate here is named; this was the outlier.
        what: tied.map((one) => one.name || one.id).join(' and '),
        why:
          'both stand at ' + placeWord(rubrics) + ' ' + best.row +
          ', and the table orders within a row by a property — movable before fixed, ' +
          'proper before indulted — that a mass key does not carry. This repository ' +
          'does not choose between them.',
        seeAlso: stated.map((one) => ({ locus: one.locus, why: one.why }))
      });
      return { winner: null, contest: contest, defeated: defeated, aside: standingAside, tied: tied };
    }
    return { winner: best, contest: contest, defeated: defeated, aside: standingAside };
  }

  function placeWord(rubrics) {
    return rubrics.calendar === 'roman-1962' ? 'row' : 'place';
  }

  /* ------------------------------------------------------------------------
   * Decision three: what becomes of the day that lost
   * --------------------------------------------------------------------- */

  function seatFor(rubrics, key) {
    const transfer = (rubrics.impediment && rubrics.impediment.transfer) || {};
    return (transfer.proper_seats || []).find((seat) => seat.key === key) || null;
  }

  /** Is this loser carried away by a transfer rather than left on the day? */
  function transferOf(rubrics, loser, winner, owner, isoDate) {
    const transfer = (rubrics.impediment && rubrics.impediment.transfer) || {};
    const seat = seatFor(rubrics, loser.key);
    if (seat) {
      // The seat's own condition decides; it is why `arrivals` finds the feast
      // on the other end.
      let destination = null;
      if (seat.seat_easter_offset != null) {
        const easter = anchor(owner, 'easter');
        const offset = easter ? Math.round((stamp(isoDate) - stamp(easter)) / DAY) : null;
        const window = seat.impeded_when_easter_offset_between || [];
        if (easter && offset >= window[0] && offset <= window[1]) {
          destination = shift(easter, seat.seat_easter_offset);
        }
      } else if (seat.seat_offset_days != null) {
        if (!seat.impeded_when_weekday || weekdayOf(isoDate) === seat.impeded_when_weekday) {
          destination = shift(isoDate, seat.seat_offset_days);
        }
      }
      if (destination) {
        return {
          disposition: 'transferred',
          locus: seat.locus,
          why: 'transferred as to its own proper seat: ' + seat.destination,
          destination: destination,
          latin: seat.latin || null
        };
      }
    }

    const eligible = (transfer.applies_to || '').indexOf('solemnit') >= 0
      ? loser.basis.nature === 'solemnity'
      : (loser.basis.class || classOfRow(rubrics, loser.row)) === 'I' && loser.basis.nature === 'feast';

    if (!eligible) return null;
    return {
      disposition: 'transferred',
      locus: transfer.locus,
      why: transfer.destination && transfer.destination.rule
        ? 'transferred to ' + transfer.destination.rule
        : 'transferred',
      destination: null,
      destinationNotComputed: transfer.destination ? transfer.destination.why_not : null
    };
  }

  function classOfRow(rubrics, row) {
    const found = rowLabel(rubrics, row);
    return found ? found.class || null : null;
  }

  function ceilingFor(rubrics, winner, sung) {
    const block = (rubrics.commemoration && rubrics.commemoration.ceilings) || null;
    if (!block) return null;
    if (sung && block.sung_non_conventual) return block.sung_non_conventual;
    const winnerClass = winner ? (winner.basis.class || classOfRow(rubrics, winner.row)) : null;
    for (const rule of block.rules || []) {
      const wanted = Array.isArray(rule.when_class) ? rule.when_class : [rule.when_class];
      if (wanted.indexOf(winnerClass) < 0) continue;
      if (rule.when_nature && rule.when_nature !== winner.basis.nature) continue;
      return rule;
    }
    return null;
  }

  /**
   * Every exclusion the rubrics say to apply, with the clause that applies it.
   *
   * The clauses the source marks `applied: false` are the ones that turn on the
   * identity of a divine Person or of a saint, which cannot be read off a mass
   * key. They are returned as remarks so the page can name them at the step and
   * are never used to drop anything.
   */
  function excluded(rubrics, winner, loser) {
    const block = (rubrics.commemoration && rubrics.commemoration.exclusions) || null;
    if (!block || !winner) return null;
    for (const clause of block.list || []) {
      if (!clause.applied) continue;
      if (clause.clause === 'b') {
        const sundayThenLord = winner.basis.nature === 'sunday' && loser.basis.of_the_lord;
        const lordThenSunday = winner.basis.of_the_lord && loser.basis.nature === 'sunday';
        if (sundayThenLord || lordThenSunday) {
          return { locus: block.locus + ' ' + clause.clause, what: clause.what };
        }
      }
    }
    return null;
  }

  function dispose(rubrics, winner, losers, owner, isoDate, sung, remarks) {
    const out = [];
    const admitted = [];
    const ceiling = ceilingFor(rubrics, winner, sung);
    const ceilingLocus = (rubrics.commemoration && rubrics.commemoration.ceilings || {}).locus || null;
    const impediment = rubrics.impediment || {};
    const reduction = impediment.reduction || null;
    const season = seasonOf(owner, isoDate);
    const commemorates = !(rubrics.commemoration && rubrics.commemoration.exists === false);

    // First pass: everything that leaves the day entirely.
    const remaining = [];
    for (const loser of losers) {
      const moved = transferOf(rubrics, loser, winner, owner, isoDate);
      if (moved) { out.push(Object.assign({ candidate: loser, id: loser.id }, moved)); continue; }

      if (loser.defeatedBy) {
        remaining.push(loser);
        continue;
      }

      if (
        reduction && winner &&
        (reduction.applies_when_loser_basis || []).indexOf(loser.basis.id) >= 0 &&
        (reduction.applies_when_winner_basis || []).indexOf(winner.basis.id) >= 0 &&
        (!reduction.only_in_season || reduction.only_in_season.indexOf(season) >= 0)
      ) {
        out.push({
          candidate: loser,
          id: loser.id,
          disposition: 'reduced',
          locus: reduction.locus,
          why: reduction.what,
          latin: reduction.latin || null
        });
        continue;
      }
      remaining.push(loser);
    }

    if (!commemorates) {
      const omission = impediment.omission || {};
      for (const loser of remaining) {
        out.push({
          candidate: loser,
          id: loser.id,
          disposition: 'omitted',
          locus: omission.locus || null,
          why: omission.gloss || 'omitted for the year',
          latin: omission.latin || null
        });
      }
      return { losers: out, commemorations: [], ceiling: null };
    }

    // Second pass: which of the rest may be commemorated, in the order RG 113
    // gives — the season first, then the table.
    const eligible = [];
    for (const loser of remaining) {
      if (loser.basis.commemoration === 'none') {
        out.push({
          candidate: loser,
          id: loser.id,
          disposition: 'omitted',
          locus: loser.basis.commemoration_locus || null,
          why: 'a day of this kind is never commemorated'
        });
        continue;
      }
      const vigilDropped = dropVigil(rubrics, winner, loser);
      if (vigilDropped) { out.push(Object.assign({ candidate: loser, id: loser.id }, vigilDropped)); continue; }

      const bar = excluded(rubrics, winner, loser);
      if (bar) {
        out.push({
          candidate: loser,
          id: loser.id,
          disposition: 'omitted',
          locus: bar.locus,
          why: bar.what
        });
        continue;
      }
      eligible.push(loser);
    }

    // RG 113: the season first, then the order of the table. An entry with no
    // row of its own — a commemoration the calendar inscribes — has no place in
    // the table and goes last.
    const LAST = Number.MAX_SAFE_INTEGER;
    eligible.sort(function (a, b) {
      const seasonal = (b.basis.de_tempore ? 1 : 0) - (a.basis.de_tempore ? 1 : 0);
      return seasonal || ((a.row == null ? LAST : a.row) - (b.row == null ? LAST : b.row));
    });

    const order = (rubrics.commemoration && rubrics.commemoration.order) || {};
    const surplus = (rubrics.commemoration && rubrics.commemoration.surplus) || {};
    let seasonalTaken = false;

    for (const loser of eligible) {
      const privileged = loser.basis.commemoration === 'privileged';
      let refusal = null;

      if (!ceiling) {
        refusal = { locus: null, why: 'no ceiling in the rubrics source matches this day' };
      } else if (admitted.length >= (ceiling.max || 0)) {
        refusal = { locus: surplus.locus || ceiling.clause, why: surplus.latin
          ? 'beyond the number this day admits, and so omitted (' + surplus.latin + ')'
          : 'beyond the number this day admits, and so omitted' };
      } else if (ceiling.privileged_only && !privileged) {
        refusal = {
          locus: (rubrics.commemoration.ceilings.locus || '') + (ceiling.clause ? ' ' + ceiling.clause : ''),
          why: sung
            ? 'an ordinary commemoration is made only at Lauds, at the conventual Mass and at Low Masses, so a sung Mass that is not conventual drops it'
            : 'this day admits one privileged commemoration only, and this one is ordinary'
        };
      } else if (ceiling.second_class_feasts_only && !(loser.basis.nature === 'feast' && (loser.basis.class || classOfRow(rubrics, loser.row)) === 'II') && !privileged) {
        refusal = {
          locus: (rubrics.commemoration.ceilings.locus || '') + ' ' + (ceiling.clause || ''),
          why: 'a second-class Sunday admits a commemoration of a second-class feast and of nothing else'
        };
      } else if (loser.basis.de_tempore && seasonalTaken) {
        refusal = { locus: 'exclusion c', why: 'a commemoration de Tempore excludes another de Tempore' };
      }

      if (refusal) {
        out.push({ candidate: loser, id: loser.id, disposition: 'omitted', locus: refusal.locus, why: refusal.why });
        continue;
      }

      if (loser.basis.de_tempore) seasonalTaken = true;
      admitted.push(loser);
      out.push({
        candidate: loser,
        id: loser.id,
        disposition: 'commemorated',
        kind: privileged ? 'privileged' : 'ordinary',
        locus: loser.basis.commemoration_locus || (rubrics.commemoration.privileged || {}).locus || null,
        why: privileged
          ? 'a privileged commemoration, made in every Mass'
          : 'an ordinary commemoration, made at Lauds, at the conventual Mass and at every Low Mass'
      });
    }

    if (order.gloss && admitted.length > 1) {
      remarks.push({ locus: order.locus, what: order.gloss });
    }
    return {
      losers: out,
      commemorations: admitted,
      // The ceiling that applied, whether or not it refused anything: "how many
      // collects, and why" is the question this page exists to answer, and the
      // answer is this rule even on a day where nothing was turned away.
      ceiling: ceiling
        ? {
            clause: ceiling.clause || null,
            max: ceiling.max,
            privileged_only: Boolean(ceiling.privileged_only),
            what: ceiling.what || null,
            locus: ceilingLocus + (ceiling.clause ? ' ' + ceiling.clause : '')
          }
        : null
    };
  }

  /** RG 33: a second- or third-class vigil is dropped outright, not commemorated. */
  function dropVigil(rubrics, winner, loser) {
    const rule = (rubrics.impediment && rubrics.impediment.vigil_dropped) || null;
    if (!rule || !winner || loser.basis.nature !== 'vigil') return null;
    const loserClass = loser.basis.class || classOfRow(rubrics, loser.row);
    if (loserClass !== 'II' && loserClass !== 'III') return null;
    const winnerClass = winner.basis.class || classOfRow(rubrics, winner.row);
    const beaten = winner.basis.nature === 'sunday' || (winnerClass === 'I' && winner.basis.nature === 'feast');
    if (!beaten) return null;
    return { disposition: 'omitted', locus: rule.locus, why: rule.gloss };
  }

  /* ------------------------------------------------------------------------
   * Decision five, as far as the orations
   * --------------------------------------------------------------------- */

  const ORDINALS = ['Collect', 'Second collect', 'Third collect', 'Fourth collect'];

  function orationsFrom(rubrics, winner, commemorations) {
    if (!winner) return [];
    const cap = ((rubrics.orations || {}).absolute_cap || {}).value || null;
    const series = [{
      position: 1,
      label: ORDINALS[0],
      of: winner.id,
      of_name: winner.name,
      kind: 'of the Mass',
      why: 'the oration of the Mass being celebrated',
      locus: (rubrics.orations || {}).what_counts ? rubrics.orations.what_counts.locus : null,
      conclusion: 'its own'
    }];
    commemorations.forEach(function (one, index) {
      series.push({
        position: index + 2,
        label: ORDINALS[index + 1] || 'Further collect',
        of: one.id,
        of_name: one.name,
        kind: one.basis.commemoration === 'privileged' ? 'privileged commemoration' : 'ordinary commemoration',
        why: one.basis.why,
        locus: one.basis.commemoration_locus || null,
        conclusion: 'a second conclusion'
      });
    });
    return cap ? series.slice(0, cap) : series;
  }

  /* ------------------------------------------------------------------------
   * One branch of the derivation
   * --------------------------------------------------------------------- */

  function deriveBranch(rubrics, owner, isoDate, candidates, option, folded) {
    const unsettled = [];
    const remarks = [];
    const season = seasonOf(owner, isoDate);
    const absent = absencesOn(rubrics, isoDate);

    const ranked = rank(rubrics, candidates, unsettled);
    // A date can carry entries and still constitute no day: a commemoration the
    // calendar inscribes occupies no row, and three formularies this calendar
    // index is known to be missing leave some Sundays with nothing at all. That
    // must be said, not rendered as an empty argument.
    if (!ranked.winner && !ranked.choice && !unsettled.length) {
      unsettled.push({
        what: isoDate,
        why: candidates.length
          ? 'nothing on this date competes for the day: what the index carries here ' +
            'occupies no row of the table, and no rule in this source constitutes a ' +
            'day for it. The calendar index, not the rubrics, is what is missing.'
          : 'this calendar index carries no mass for this date, and no rule in this ' +
            'source constitutes a day for it.'
      });
    }
    const winner = ranked.winner;
    const losers = (ranked.contest || []).filter((one) => one !== winner)
      .concat(ranked.aside || []);

    const low = winner ? dispose(rubrics, winner, losers, owner, isoDate, false, remarks)
                       : { losers: [], commemorations: [] };
    const commemorates = !(rubrics.commemoration && rubrics.commemoration.exists === false);
    const sung = winner && commemorates
      ? dispose(rubrics, winner, losers, owner, isoDate, true, [])
      : null;

    const conditions = candidates
      .filter((one) => one.certain === false && one.caveat)
      .map((one) => ({
        id: one.impliedBy ? one.impliedBy.id : one.id,
        what: one.name,
        unless: one.caveat
      }));

    const orations = commemorates
      ? {
          low_mass: orationsFrom(rubrics, winner, low.commemorations),
          sung_non_conventual: orationsFrom(rubrics, winner, sung ? sung.commemorations : [])
        }
      : { all: orationsFrom(rubrics, winner, []) };
    const ceilings = commemorates
      ? { low_mass: low.ceiling, sung_non_conventual: sung ? sung.ceiling : null }
      : null;

    // The postconciliar rite adds nothing to its one collect, but a memorial
    // reduced on a privileged weekday may supply it. That is a substitution and
    // must never be rendered as a second oration.
    if (!commemorates && orations.all.length) {
      const reduced = low.losers.filter((one) => one.disposition === 'reduced');
      const qualification = (rubrics.commemoration || {}).surviving_qualification || null;
      if (reduced.length && qualification) {
        orations.all[0].alternative = {
          of: reduced[0].id,
          of_name: reduced[0].candidate.name,
          locus: qualification.locus,
          what: qualification.what
        };
      }
    }

    const overOfThePeople = (rubrics.orations || {}).prayer_over_the_people || null;
    const extras = [];
    if (
      overOfThePeople && winner &&
      (overOfThePeople.applies_when_winner_basis || []).indexOf(winner.basis.id) >= 0
    ) {
      extras.push({
        slot: 'Prayer over the people',
        locus: overOfThePeople.locus,
        what: overOfThePeople.what
      });
    }

    return {
      option: option,
      season: season,
      candidates: candidates.map(function (one) {
        return {
          id: one.id,
          key: one.key,
          name: one.name,
          source: one.source,
          row: one.row,
          rowLabel: one.row != null ? (rowLabel(rubrics, one.row) || {}).label || null : null,
          class: one.basis.class || classOfRow(rubrics, one.row),
          nature: one.basis.nature,
          basis: one.basis.id,
          basisLabel: one.basis.label || null,
          why: one.basis.why,
          locus: one.basis.locus,
          competes: competes(one),
          certain: one.certain !== false,
          caveat: one.caveat || null,
          note: one.note || null,
          rule: one.rule,
          territorial: one.territorial,
          arrivedFrom: one.arrivedFrom || null,
          seat: one.seat ? { locus: one.seat.locus, destination: one.seat.destination, latin: one.seat.latin } : null,
          office: one.office ? { locus: one.office.locus, why: one.office.why, underlying: one.office.underlying.why } : null,
          alsoInscribedAs: one.alsoInscribedAs || []
        };
      }),
      folded: folded,
      winner: winner
        ? {
            id: winner.id,
            key: winner.key,
            name: winner.name,
            row: winner.row,
            rowLabel: (rowLabel(rubrics, winner.row) || {}).label || null,
            class: winner.basis.class || classOfRow(rubrics, winner.row),
            nature: winner.basis.nature,
            basis: winner.basis.id,
            basisLabel: winner.basis.label || null,
            // Standing highest is not the same as being kept. An optional
            // memorial outranks the weekday it is joined to and is still
            // optional, and a page that says it "takes the day" has quietly
            // turned a permission into an obligation.
            optional: Boolean(winner.basis.optional),
            source: winner.source,
            why: winner.basis.why,
            locus: winner.basis.locus
          }
        : null,
      winnerRule: {
        locus: (rubrics.precedence || {}).locus || null,
        latin: (rubrics.precedence || {}).latin || null,
        what: 'precedence among liturgical days is governed by this table and by nothing else'
      },
      choice: ranked.choice
        ? {
            among: ranked.choice.map((one) => ({ id: one.id, name: one.name })),
            locus: (rubrics.precedence.rows.find((r) => r.row === ranked.choice[0].row) || {}).note || null,
            what: 'neither displaces the other; one may be kept and the rest are omitted'
          }
        : null,
      losers: low.losers.map(function (one) {
        return {
          id: one.id,
          name: one.candidate.name,
          row: one.candidate.row,
          disposition: one.disposition,
          kind: one.kind || null,
          locus: one.locus,
          why: one.why,
          latin: one.latin || null,
          destination: one.destination || null,
          destinationNotComputed: one.destinationNotComputed || null,
          defeatedBy: one.candidate.defeatedBy
            ? { locus: one.candidate.defeatedBy.override.locus, why: one.candidate.defeatedBy.override.why }
            : null
        };
      }),
      sungDiffers: Boolean(
        sung && low.commemorations.length !== sung.commemorations.length
      ),
      orations: orations,
      ceilings: ceilings,
      extras: extras,
      remarks: remarks,
      conditions: conditions,
      absent: absent,
      unsettled: unsettled,
      settled:
        unsettled.length === 0 &&
        conditions.length === 0 &&
        !absent.some((one) => one.blocks_result) &&
        (Boolean(winner) || Boolean(ranked.choice))
    };
  }

  /* ------------------------------------------------------------------------
   * The entry point
   * --------------------------------------------------------------------- */

  function derive(input) {
    const year = input.year;
    const rubrics = input.rubrics;
    const isoDate = input.date;

    if (!year || !rubrics) throw new Error('derive needs both a year file and a rubrics file');
    if (!/^\d{4}-\d{2}-\d{2}$/.test(isoDate || '')) throw new Error('derive needs a YYYY-MM-DD date');

    const owner = liturgicalYearFor(year, isoDate);
    const season = seasonOf(owner, isoDate);
    const held = indexCandidates(year, rubrics, isoDate);
    const arrived = arrivals(rubrics, owner, isoDate);
    const inscribed = held.candidates.concat(arrived);
    const all = inscribed.concat(ferialCandidates(year, rubrics, isoDate, inscribed));

    // The implied day is computed per branch, not once. Under the branch where
    // the Ascension has moved to the Sunday it is absent from its Thursday, and
    // that Thursday is then an ordinary weekday that has to be constituted —
    // computing the implied day before the split would have suppressed it.
    function branchOf(option) {
      const set = option === null
        ? all.slice()
        : all.filter((one) => !one.territorial || one.territorial === option);
      const implied = impliedCandidate(rubrics, owner, isoDate, season, set);
      if (implied) set.unshift(implied);
      return deriveBranch(rubrics, owner, isoDate, set, option, held.folded);
    }

    const options = optionsToDerive(year, all);
    const branches = options.length ? options.map(branchOf) : [branchOf(null)];

    return {
      date: isoDate,
      weekday: weekdayOf(isoDate),
      calendar: rubrics.calendar,
      edition: rubrics.edition,
      advisory: rubrics.advisory,
      sourceAdvisory: rubrics.source_advisory || null,
      dayAdvisory: year.advisory || null,
      season: season,
      week: weekOf(owner, isoDate),
      liturgicalYear: owner
        ? {
            label: owner.label,
            begins: owner.begins,
            ends: owner.ends,
            lectionary: owner.lectionary || null,
            unresolved: owner.unresolved || []
          }
        : null,
      territorial: year.territorial || null,
      options: branches
    };
  }

  return {
    derive: derive,
    // Exposed for the page's own labelling; not part of the derivation.
    weekdayOf: weekdayOf,
    shift: shift,
    placeWord: placeWord
  };
}));
