/* Consumer projections for the shared liturgy reader-state contract.
 *
 * These adapters do not resolve a calendar, fetch a source, render a DOM, or
 * format a terminal. They project the existing MassAssembly result, generated
 * Proper/Ordinary structures, and mass-today JSON into one compact semantic
 * shape. OrdinarySeating remains the sole seating and event-order engine.
 */

'use strict';

(function (root, factory) {
  let api;
  if (typeof module === 'object' && module && module.exports) {
    api = factory(require('./reader-state.js'), require('./ordinary-seating.js'));
    module.exports = api;
  } else {
    api = factory(root.LiturgyReaderState, root.OrdinarySeating);
    root.LiturgyReaderStateAdapters = api;
  }
}(typeof globalThis !== 'undefined' ? globalThis : this, function (Contract, Seating) {
  if (!Contract || !Seating) throw new Error('reader-state adapters require contract and seating');

  function pad(value) {
    return String(value + 1).padStart(3, '0');
  }

  function properEventId(editionId, formularyId, index) {
    return 'proper/' + editionId + '/' + formularyId + '/' + pad(index);
  }

  const SEMANTIC_SLOTS = Object.freeze({
    'Introit': 'entrance-antiphon',
    'Entrance Antiphon': 'entrance-antiphon',
    'Collect': 'collect',
    'Epistle': 'reading-1',
    'First Reading': 'reading-1',
    'Gradual': 'gradual',
    'Responsorial Psalm': 'responsorial-psalm',
    'Second Reading': 'reading-2',
    'Alleluia': 'gospel-acclamation',
    'Tract': 'gospel-acclamation',
    'Gospel Acclamation': 'gospel-acclamation',
    'Gospel': 'gospel',
    'Offertory': 'offertory-chant',
    'Secret': 'prayer-over-offerings',
    'Prayer over the Offerings': 'prayer-over-offerings',
    'Communion': 'communion-antiphon',
    'Communion Antiphon': 'communion-antiphon',
    'Postcommunion': 'prayer-after-communion',
    'Prayer after Communion': 'prayer-after-communion'
  });

  function semanticSlot(proper) {
    const id = proper && SEMANTIC_SLOTS[proper.name];
    return id ? { state: 'mapped', identity: { id: id } } : {
      state: 'edition-local-unmapped',
      reason: 'generated Proper data has no cross-edition semantic slot identity'
    };
  }

  /**
   * Resolve only source-authored Mass-form identities. The legacy flat Proper
   * list is retained for old consumers, but it is never a selection mechanism:
   * a multi-form Mass must carry the additive ordered `forms` manifest.
   */
  function properFormSelection(mass, request) {
    const flat = (mass.propers || []).map(function (proper, sourceIndex) {
      return { proper: proper, sourceIndex: sourceIndex };
    });
    const forms = mass.forms || [];
    if (!Array.isArray(forms)) throw new Error('Mass forms manifest must be an array');

    if (!forms.length) {
      const legacyLabels = new Set(flat.map(function (row) {
        return row.proper && row.proper.form || null;
      }).filter(Boolean));
      if (legacyLabels.size) {
        throw new Error('explicit legacy form labels lack source-authored stable form identities');
      }
      if (flat.some(function (row) { return !row.proper; })) {
        throw new Error('no-form Proper rows must be mappings');
      }
      const explicitIds = new Set(flat.map(function (row) {
        return row.proper.form_id || null;
      }).filter(Boolean));
      if (Array.from(explicitIds).some(function (id) { return id !== 'main'; })) {
        throw new Error('explicit form identity lacks a forms manifest');
      }
      // Structure v1 predates form_id.  A payload with no manifest, no form
      // labels, and no non-main identity has only one defensible reading, so
      // normalize that legacy shape at the consumer boundary.  Any authored
      // form evidence above remains fail-closed.
      const normalized = flat.map(function (row) {
        if (row.proper.form_id === 'main') return row;
        return {
          proper: Object.assign({}, row.proper, { form_id: 'main' }),
          sourceIndex: row.sourceIndex
        };
      });
      if (hasOwn(request, 'form')) {
        throw new Error('explicit form is unsupported by this Mass');
      }
      return { id: null, rows: normalized, choice: null, forms: [] };
    }

    const ids = [];
    const rowsById = new Map();
    let offset = 0;
    forms.forEach(function (form, index) {
      if (!form || typeof form.id !== 'string' || !form.id ||
          !Array.isArray(form.propers) || form.ordinal !== index + 1) {
        throw new Error('Mass forms manifest has an invalid identity, ordinal, or Proper list');
      }
      if (ids.indexOf(form.id) >= 0) throw new Error('Mass form identities must be unique');
      ids.push(form.id);
      const rows = form.propers.map(function (proper, localIndex) {
        if (!proper || proper.form_id !== form.id) {
          throw new Error('form Proper must reference its source-authored form identity');
        }
        return { proper: proper, sourceIndex: offset + localIndex };
      });
      rowsById.set(form.id, rows);
      offset += rows.length;
    });
    const nested = forms.reduce(function (all, form) {
      return all.concat(form.propers);
    }, []);
    if (flat.length !== nested.length || flat.some(function (row, index) {
      return !sameJson(row.proper, nested[index]);
    })) {
      throw new Error('Mass forms manifest does not partition the legacy Proper sequence');
    }

    const wanted = hasOwn(request, 'form') ? request.form : null;
    if (wanted !== null && ids.indexOf(wanted) < 0) {
      throw new Error('unsupported form; valid form ids: ' + ids.join(', '));
    }
    if (wanted === null && forms.length > 1) {
      const choiceId = 'proper-form:' + request.edition.id + '/' + mass.key;
      return {
        id: null,
        rows: [],
        forms: forms,
        choice: Contract.unresolvedChoice(
          choiceId,
          'this Mass carries several source-appointed forms and none is a default',
          ids.map(function (id) {
            return {
              id: id,
              identity: { id: id },
              sourceHooks: [{ kind: 'proper-form', id: request.edition.id + '/' + mass.key + '/' + id }]
            };
          }),
          [{ kind: 'proper-form-manifest', id: request.edition.id + '/' + mass.key }]
        )
      };
    }
    const selected = wanted === null ? forms[0].id : wanted;
    return { id: selected, rows: rowsById.get(selected), choice: null, forms: forms };
  }

  function ordinaryFrame(mass) {
    if (!mass || !Object.prototype.hasOwnProperty.call(mass, 'ordinary_frame')) {
      return { applicability: 'full' };
    }
    const frame = mass.ordinary_frame;
    if (!frame || typeof frame !== 'object' || Array.isArray(frame)) {
      throw new Error('Mass Ordinary frame must be an exact mapping');
    }
    const keys = Object.keys(frame).sort();
    if (keys.some(function (key) { return ['applicability', 'basis'].indexOf(key) < 0; }) ||
        !Object.prototype.hasOwnProperty.call(frame, 'applicability')) {
      throw new Error('present Ordinary frame may carry only applicability and basis');
    }
    if (!frame || ['full', 'none', 'unavailable'].indexOf(frame.applicability) < 0) {
      throw new Error('Mass carries an unsupported Ordinary-frame applicability');
    }
    if (frame.applicability !== 'full' &&
        (typeof frame.basis !== 'string' || !frame.basis.trim())) {
      throw new Error('an exceptional Ordinary frame must carry its source basis');
    }
    if (Object.prototype.hasOwnProperty.call(frame, 'basis') &&
        (typeof frame.basis !== 'string' || !frame.basis.trim())) {
      throw new Error('Mass Ordinary frame basis must be a nonempty string');
    }
    return Object.prototype.hasOwnProperty.call(frame, 'basis')
      ? { applicability: frame.applicability, basis: frame.basis }
      : { applicability: frame.applicability };
  }

  const SUNDAY_CYCLE_KEYS = Object.freeze(['A', 'B', 'C']);
  const WEEKDAY_CYCLE_KEYS = Object.freeze(['I', 'II']);

  function cycleKeysFor(proper, family, allowed) {
    const rows = (proper && proper[family]) || {};
    const keys = Object.keys(rows);
    const invalid = keys.filter(function (key) { return allowed.indexOf(key) < 0; });
    if (invalid.length) {
      throw new Error(family + ' carries unsupported Lectionary cycle keys: ' + invalid.join(', '));
    }
    return keys.sort().filter(function (key) {
      const row = rows[key] || {};
      return Boolean(
        (row.citations || []).length || row.text ||
        (row.unavailable_translations || []).length ||
        (row.untranslated || []).length ||
        (row.latin && row.latin.withheld)
      );
    });
  }

  function sundayCycleKeys(proper) {
    return cycleKeysFor(proper, 'cycles', SUNDAY_CYCLE_KEYS);
  }

  function weekdayCycleKeys(proper) {
    return cycleKeysFor(proper, 'weekday_cycles', WEEKDAY_CYCLE_KEYS);
  }

  function cycleSelections(proper) {
    return sundayCycleKeys(proper).map(function (key) {
      return { key: key, dimension: 'sunday', family: 'cycles' };
    }).concat(weekdayCycleKeys(proper).map(function (key) {
      return { key: key, dimension: 'weekday', family: 'weekday_cycles' };
    }));
  }

  function dayCycle(proper, lectionary) {
    const sunday = sundayCycleKeys(proper);
    const weekday = weekdayCycleKeys(proper);
    if (!sunday.length && !weekday.length) return null;
    if (!lectionary) throw new Error('cycle-bearing Proper has no resolved Lectionary year');
    if (sunday.length && weekday.length) {
      throw new Error('Proper carries both Sunday and weekday Lectionary cycle families');
    }
    if (sunday.length) {
      if (SUNDAY_CYCLE_KEYS.indexOf(lectionary.sunday) < 0 ||
          sunday.indexOf(lectionary.sunday) < 0) {
        throw new Error('resolved Sunday Lectionary year is not held for this Proper');
      }
      return { key: lectionary.sunday, dimension: 'sunday', family: 'cycles' };
    }
    if (WEEKDAY_CYCLE_KEYS.indexOf(lectionary.weekday) < 0 ||
        weekday.indexOf(lectionary.weekday) < 0) {
      throw new Error('resolved weekday Lectionary year is not held for this Proper');
    }
    return { key: lectionary.weekday, dimension: 'weekday', family: 'weekday_cycles' };
  }

  function explicitCycleSelection(proper, key) {
    const selected = cycleSelections(proper).filter(function (row) { return row.key === key; });
    if (selected.length > 1) throw new Error('cycle key belongs to more than one family');
    if (selected.length === 1) return selected[0];
    return null;
  }

  function selectedOwner(proper, selection) {
    return selection && proper && proper[selection.family] &&
      proper[selection.family][selection.key] || proper || {};
  }

  function typedUnavailableFor(proper, wanted, selection) {
    const owner = selectedOwner(proper, selection);
    const latinOwner = owner.latin ? owner : proper;
    const latin = latinOwner.latin || {};
    if (wanted === 'la' && latin.withheld) {
      if (latinOwner.text || latin.held !== false || latin.available !== false ||
          ['rights-restricted', 'unavailable'].indexOf(latin.state) < 0) {
        throw new Error('withheld Latin original must use the exact public unavailable shape');
      }
      return {
        kind: 'composed', language: 'la', sourceId: null, source: null,
        rights: null, missing: true, text: null, availability: 'unavailable',
        held: false,
        reason: 'latin-withheld',
        unavailableState: ['rights-restricted', 'unavailable'].indexOf(latin.state) >= 0
          ? latin.state : 'unavailable'
      };
    }

    const unavailable = [];
    for (const holder of owner === proper ? [proper] : [owner, proper]) {
      for (const row of holder.unavailable_translations || []) {
        if (!row || row.lang !== wanted) continue;
        const target = row.target || {};
        const targetCycle = target.cycle || 'all';
        if (targetCycle !== 'all' &&
            (!selection || targetCycle !== selection.key)) continue;
        unavailable.push(row);
      }
    }
    if (unavailable.length) {
      const row = unavailable[0];
      const state = row.state || 'unavailable';
      const target = row.target || {};
      return {
        kind: 'composed', language: wanted, sourceId: null, source: null,
        rights: null, missing: true, text: null, availability: 'unavailable',
        held: false,
        reason: state,
        unavailableState: state,
        extent: target.extent || null,
        cycle: selection ? selection.key :
          (target.cycle && target.cycle !== 'all' ? target.cycle : null)
      };
    }

    const ledgered = [];
    for (const holder of owner === proper ? [proper] : [owner, proper]) {
      for (const row of holder.untranslated || []) {
        if (!row || row.lang !== wanted) continue;
        const target = row.target || {};
        const targetCycle = target.cycle || 'all';
        if (targetCycle !== 'all' &&
            (!selection || targetCycle !== selection.key)) continue;
        ledgered.push(row);
      }
    }
    if (!ledgered.length) return null;
    const row = ledgered[0];
    const target = row.target || {};
    const unavailableState = row.state || 'unavailable';
    return {
      kind: 'composed', language: wanted, sourceId: null, source: null,
      rights: null, missing: true, text: null, availability: 'unavailable',
      held: false,
      reason: 'ledgered-untranslated',
      unavailableState: unavailableState,
      extent: target.extent || null,
      cycle: selection ? selection.key :
        (target.cycle && target.cycle !== 'all' ? target.cycle : null)
    };
  }

  function materialForCycle(proper, request, structure, selection) {
    const cycle = selection ? selection.key : null;
    const cycleRows = selection && selection.dimension === 'sunday' ? [cycle] : [];
    const weekdayCycleRows = selection && selection.dimension === 'weekday' ? [cycle] : [];
    const citations = (proper.citations || []).slice();
    let cycleText = null;
    if (selection) {
      const row = (proper[selection.family] || {})[cycle] || {};
      for (const citation of row.citations || []) citations.push(citation);
      if (row.text) cycleText = row.text;
    }
    const references = citations.map(function (one) { return one.ref; }).filter(Boolean);
    if (references.length) {
      const unresolved = citations.filter(function (one) { return one.unresolved; }).map(function (one) {
        return { reference: one.ref, reason: one.unresolved };
      });
      return {
        kind: 'scripture',
        bible: request.bible && request.bible.id || null,
        numbering: request.bible && request.bible.numbering || null,
        cycle: cycle,
        cycles: cycleRows,
        weekdayCycles: weekdayCycleRows,
        cycleDimension: selection ? selection.dimension : null,
        references: references,
        availability: unresolved.length ? 'unavailable' : 'held',
        rights: null,
        unresolved: unresolved
      };
    }
    const wanted = request.languages && request.languages.orations || 'la';
    if (wanted === 'la') {
      const withheldLatin = typedUnavailableFor(proper, wanted, selection);
      if (withheldLatin) return Object.assign(withheldLatin, {
        cycle: withheldLatin.cycle || cycle,
        cycles: cycleRows,
        weekdayCycles: weekdayCycleRows,
        cycleDimension: selection ? selection.dimension : null
      });
    }
    if (proper.text || cycleText || wanted !== 'la') {
      if (wanted === 'la') {
        return {
          kind: 'composed', language: 'la', cycle: cycle,
          cycles: cycleRows, weekdayCycles: weekdayCycleRows,
          cycleDimension: selection ? selection.dimension : null,
          sourceId: null, rights: null, missing: false,
          availability: 'held', text: cycleText || proper.text
        };
      }
      const owner = selectedOwner(proper, selection);
      const typed = typedUnavailableFor(proper, wanted, selection);
      if (typed) return Object.assign(typed, {
        cycle: typed.cycle || cycle,
        cycles: cycleRows,
        weekdayCycles: weekdayCycleRows,
        cycleDimension: selection ? selection.dimension : null
      });
      const ownerTranslations = (owner.translations || []).filter(function (one) {
        return one && one.lang === wanted && one.text;
      });
      const parentTranslations = (proper.translations || []).filter(function (one) {
        return one && one.lang === wanted && one.text;
      });
      const translations = owner !== proper && (cycleText || ownerTranslations.length)
        ? ownerTranslations : parentTranslations;
      const witness = request.languages && request.languages.translationWitness || null;
      const translation = witness
        ? translations.find(function (one) {
            return (one.source_id || one.source || null) === witness;
          })
        : (translations.length === 1 ? translations[0] : null);
      if (translation) {
        return {
          kind: 'composed', language: wanted, cycle: cycle, cycles: cycleRows,
          weekdayCycles: weekdayCycleRows,
          cycleDimension: selection ? selection.dimension : null,
          sourceId: translation.source_id || translation.source || null,
          rights: translation.rights || null, missing: false,
          availability: 'held', text: translation.text
        };
      }
      if (translations.length > 1 && !witness) {
        const witnessIds = translations.map(function (one) {
          return one.source_id || one.source || null;
        });
        if (witnessIds.some(function (id) { return !id; })) {
          return {
            kind: 'composed', language: wanted, cycle: cycle, cycles: cycleRows,
            weekdayCycles: weekdayCycleRows,
            cycleDimension: selection ? selection.dimension : null,
            sourceId: null, rights: null, missing: true, availability: 'unavailable',
            reason: 'translation-witness-identity-missing'
          };
        }
        return {
          kind: 'composed', language: wanted, cycle: cycle, cycles: cycleRows,
          weekdayCycles: weekdayCycleRows,
          cycleDimension: selection ? selection.dimension : null,
          sourceId: null, rights: null, missing: false, availability: 'choice-required',
          unresolvedWitnesses: witnessIds.slice().sort()
        };
      }
      return {
        kind: 'composed', language: wanted, cycle: cycle, cycles: cycleRows,
        weekdayCycles: weekdayCycleRows,
        cycleDimension: selection ? selection.dimension : null,
        sourceId: null, rights: null, missing: true, availability: 'unavailable',
        reason: 'translation-missing'
      };
    }
    const typed = typedUnavailableFor(proper, wanted, selection);
    if (typed) return Object.assign(typed, {
      cycle: typed.cycle || cycle,
      cycles: cycleRows,
      weekdayCycles: weekdayCycleRows,
      cycleDimension: selection ? selection.dimension : null
    });
    if (proper.incipit) {
      return {
        kind: 'incipit-only', language: 'la', cycle: cycle, cycles: cycleRows,
        weekdayCycles: weekdayCycleRows,
        cycleDimension: selection ? selection.dimension : null,
        rights: null, availability: 'held'
      };
    }
    return {
      kind: 'absent', rights: null, availability: 'absent',
      reason: proper.name === 'Placeholder' ? 'not-transcribed' : 'semantic-absence'
    };
  }

  function selectedMaterial(proper, request, structure, cycleMode) {
    const selections = cycleSelections(proper);
    if (cycleMode === 'day') {
      return materialForCycle(proper, request, structure, dayCycle(proper, request.lectionary));
    }
    const hasExplicitCycle = hasOwn(request, 'cycle') && request.cycle !== null;
    if (hasExplicitCycle) {
      const selection = explicitCycleSelection(proper, request.cycle);
      if (selections.length && !selection) {
        return {
          kind: 'absent', rights: null, availability: 'absent',
          reason: 'cycle-not-applicable'
        };
      }
      return materialForCycle(proper, request, structure, selection);
    }
    if (selections.length === 0) return materialForCycle(proper, request, structure, null);
    if (selections.length === 1) return materialForCycle(proper, request, structure, selections[0]);
    return {
      kind: 'cycle-alternatives',
      cycle: null,
      availability: 'choice-required',
      rights: null,
      alternatives: selections.map(function (selection) {
        return {
          id: selection.key,
          cycle: selection.key,
          cycleDimension: selection.dimension,
          material: materialForCycle(proper, request, structure, selection),
          sourceHooks: []
        };
      })
    };
  }

  function sourceHooks(proper, selected, editionId, formularyId, index) {
    const hooks = [{
      kind: 'proper-structure',
      id: editionId + '/' + formularyId + '/' + pad(index)
    }];
    if (selected && selected.sourceId) hooks.push({ kind: 'translation', id: selected.sourceId });
    const taken = proper.taken_from;
    if (taken) {
      hooks.push({
        kind: 'taken-from',
        id: [taken.mass, taken.proper, taken.form, taken.citation].filter(Boolean).join('|')
      });
    }
    return hooks;
  }

  function projectProper(proper, index, mass, request, structure, cycleMode, seat) {
    const selected = selectedMaterial(proper, request, structure, cycleMode);
    if (selected.kind === 'cycle-alternatives') {
      selected.alternatives.forEach(function (alternative) {
        alternative.sourceHooks = sourceHooks(
          proper, alternative.material, request.edition.id, mass.key, index
        ).concat([{
          kind: 'proper-cycle',
          id: request.edition.id + '/' + mass.key + '/' + pad(index) + '/' + alternative.cycle
        }]);
      });
    }
    return {
      id: properEventId(request.edition.id, mass.key, index),
      kind: 'proper',
      semanticSlot: semanticSlot(proper),
      editionSlotLabel: proper.name || null,
      form: proper.form || null,
      sourceKind: proper.source || null,
      selected: selected,
      seat: seat || null,
      sourceHooks: sourceHooks(proper, selected, request.edition.id, mass.key, index)
    };
  }

  function ordinaryTranslation(element, ordinary, language, witness) {
    const candidates = (element.translations || []).filter(function (one) {
      return one && one.lang === language && one.text;
    });
    const found = witness ? candidates.find(function (one) {
      return (one.source_id || one.source || null) === witness;
    }) : (candidates.length === 1 ? candidates[0] : null);
    if (found) {
      return {
        kind: 'ordinary-text',
        language: language,
        sourceId: found.source_id || null,
        rights: found.rights || null,
        absenceKey: null,
        availability: 'held',
        text: found.text
      };
    }
    if (!witness && candidates.length > 1) {
      const ids = candidates.map(function (one) {
        return one.source_id || one.source || null;
      });
      if (ids.every(Boolean)) {
        return {
          kind: 'ordinary-text', language: language, sourceId: null, rights: null, absenceKey: null,
          availability: 'choice-required', text: null,
          unresolvedWitnesses: ids.slice().sort()
        };
      }
    }
    const row = (ordinary.languages || []).find(function (one) { return one.lang === language; });
    return {
      kind: 'ordinary-text', language: language,
      sourceId: null,
      rights: null,
      absenceKey: row && element.absent && element.absent[row.absent] || 'language-not-held',
      availability: 'unavailable',
      text: null
    };
  }

  function seatedEvents(mass, properRows, request, structure, ordinary, cycleMode) {
    if (!ordinary) {
      return properRows.filter(function (row) {
        return row.proper.name !== 'Placeholder';
      }).map(function (row) {
        return projectProper(
          row.proper, row.sourceIndex, mass, request, structure, cycleMode, null
        );
      });
    }
    const variant = request.options && request.options.legitimate || {};
    const group = Seating.variantGroupOf(ordinary);
    const wanted = group && variant[group.group] || null;
    if (wanted && !(group.options || []).some(function (one) { return one.id === wanted; })) {
      throw new Error('explicit Ordinary option is not held by this edition');
    }
    const shown = Seating.shownElements(ordinary, wanted);
    const placed = Seating.seatPropers(
      properRows.map(function (row) { return row.proper; }), Seating.seats(ordinary, shown),
      function (proper) { return proper && proper.name === 'Placeholder'; }
    );
    const indexes = new Map(properRows.map(function (row) {
      return [row.proper, row.sourceIndex];
    }));
    return Seating.massEvents(shown, placed).map(function (event) {
      if (event.kind === 'begin_section') {
        return {
          id: 'ordinary-section/' + event.section.key,
          kind: 'ordinary-section',
          sourceHooks: [{
            kind: 'ordinary-structure', id: request.edition.id + '/' + event.section.key
          }]
        };
      }
      if (event.kind === 'ordinary_element') {
        const selected = ordinaryTranslation(
          event.element, ordinary,
          request.languages && request.languages.ordinary || 'en',
          request.languages && request.languages.ordinaryWitness || null
        );
        return {
          id: 'ordinary-element/' + event.element.key,
          kind: 'ordinary-element',
          speaker: event.element.speaker || null,
          action: event.element.kind === 'rubric',
          locus: event.element.locus || null,
          selected: selected,
          sourceHooks: [{
            kind: 'ordinary-structure',
            id: request.edition.id + '/' + event.element.key
          }].concat(selected.sourceId ? [{ kind: 'translation', id: selected.sourceId }] : [])
        };
      }
      return projectProper(
        event.proper,
        indexes.get(event.proper),
        mass,
        request,
        structure,
        cycleMode,
        event.seat ? {
          id: event.seat.key,
          anchor: event.seat.anchor,
          where: event.seat.where,
          locus: event.seat.locus,
          placement: event.placement
        } : null
      );
    });
  }

  function partialRecensionReason(structure, mass) {
    const coverage = structure && structure.recension_coverage;
    const stamp = mass && mass.recension;
    if (!coverage || typeof coverage !== 'object' || Array.isArray(coverage)) {
      if (!stamp || typeof stamp !== 'object' || Array.isArray(stamp)) return null;
      return {
        kind: 'partial-recension',
        recensionStatus: null,
        domain: 'propers',
        domainState: null,
        sourceCalendar: stamp.text_from || stamp.calendar || null,
        inheritanceStatus: null
      };
    }
    const domains = coverage.domains && typeof coverage.domains === 'object'
      ? coverage.domains : {};
    const propers = domains.propers && typeof domains.propers === 'object'
      ? domains.propers : {};
    const inheritance = coverage.inheritance && typeof coverage.inheritance === 'object'
      ? coverage.inheritance : {};
    if (coverage.status === 'complete' && propers.state === 'complete' &&
        inheritance.status === 'complete') return null;
    return {
      kind: 'partial-recension',
      recensionStatus: coverage.status || null,
      domain: 'propers',
      domainState: propers.state || null,
      sourceCalendar: inheritance.source_calendar || null,
      inheritanceStatus: inheritance.status || null
    };
  }

  function coverageFor(structure, mass, propers, request, ordinary, events) {
    const rows = [];
    const placeholders = propers.filter(function (one) { return one.name === 'Placeholder'; });
    const textStatus = mass && mass.text_status;
    const partialRecension = partialRecensionReason(structure, mass);
    if (textStatus && textStatus.state === 'partial' &&
        textStatus.scope === 'missal-formulary') {
      const reasons = (textStatus.reasons && textStatus.reasons.length
        ? textStatus.reasons : [{ kind: 'source-declared-partial' }]).map(function (reason) {
        return {
          kind: 'text-not-held',
          sourceKind: reason.kind,
          sourceId: reason.source_id || null
        };
      });
      if (partialRecension) reasons.push(partialRecension);
      rows.push(Contract.coverage(
        'supported', 'formulary:' + mass.key, 'partial',
        reasons
      ));
    } else if (textStatus && textStatus.state === 'unavailable' &&
               textStatus.scope === 'missal-formulary') {
      rows.push(Contract.coverage(
        'unavailable', 'formulary:' + mass.key, null,
        [{ kind: 'text-not-held', sourceState: 'unavailable' }]
      ));
    } else if (placeholders.length) {
      const reasons = [
        { kind: 'text-not-held', count: placeholders.length, repositoryTerm: 'Placeholder' }
      ];
      if (partialRecension) reasons.push(partialRecension);
      rows.push(Contract.coverage(
        'supported', 'formulary:' + mass.key, 'partial',
        reasons
      ));
    } else if (partialRecension) {
      rows.push(Contract.coverage(
        'supported', 'formulary:' + mass.key, 'partial', [partialRecension]
      ));
    } else {
      rows.push(Contract.coverage('supported', 'formulary:' + mass.key, 'complete', []));
    }
    const selections = selectedRows(events);
    const unavailableOriginals = selections.filter(function (row) {
      return row.selected.missing && row.selected.language === 'la' &&
        row.selected.reason === 'latin-withheld';
    });
    if (unavailableOriginals.length) {
      rows.push(Contract.coverage(
        'unavailable', 'proper-original:la', null,
        [{ kind: 'text-withheld', count: unavailableOriginals.length }]
      ));
    }
    const restrictedTranslations = selections.filter(function (row) {
      return row.selected.missing &&
        row.selected.reason !== 'latin-withheld' &&
        (row.selected.reason === 'rights-restricted' ||
         row.selected.unavailableState === 'rights-restricted');
    });
    if (restrictedTranslations.length) {
      rows.push(Contract.coverage(
        'unavailable', 'proper-translation:' + request.languages.orations, null,
        [{ kind: 'text-withheld', count: restrictedTranslations.length }]
      ));
    }
    const missingTranslations = selections.filter(function (row) {
      return row.selected.missing &&
        row.selected.reason !== 'latin-withheld' &&
        row.selected.reason !== 'rights-restricted' &&
        row.selected.unavailableState !== 'rights-restricted';
    });
    if (missingTranslations.length) {
      rows.push(Contract.coverage(
        'unavailable', 'proper-translation:' + request.languages.orations, null,
        [{ kind: 'translation-missing', count: missingTranslations.length }]
      ));
    }
    const unresolvedCitations = selections.filter(function (row) {
      return (row.selected.unresolved || []).length;
    });
    if (unresolvedCitations.length) {
      rows.push(Contract.coverage(
        'unavailable', 'proper-scripture-text', null,
        [{ kind: 'unresolved-citation', count: unresolvedCitations.length }]
      ));
    }
    if (request.options && request.options.ordinary) {
      const frame = ordinaryFrame(mass);
      if (frame.applicability === 'none') {
        rows.push(Contract.coverage(
          'absent', 'ordinary-frame:' + request.edition.id, null,
          [{
            kind: 'semantic-absence',
            basis: frame.basis,
            applicability: frame.applicability
          }]
        ));
      } else if (frame.applicability === 'unavailable') {
        rows.push(Contract.coverage(
          'unavailable', 'ordinary-frame:' + request.edition.id, null,
          [{
            kind: 'text-not-held',
            basis: frame.basis,
            applicability: frame.applicability
          }]
        ));
      } else if (!ordinary) {
        rows.push(Contract.coverage(
          'unsupported', 'ordinary:' + request.edition.id, null,
          [{ kind: 'ordinary-missing' }]
        ));
      } else {
        const language = request.languages && request.languages.ordinary || 'en';
        const declared = (ordinary.languages || []).find(function (one) { return one.lang === language; });
        if (!declared || declared.held === 0) {
          rows.push(Contract.coverage(
            'unavailable', 'ordinary:' + request.edition.id + ':' + language, null,
            [{ kind: 'language-missing', absenceKey: declared && declared.absent || 'language-not-held' }]
          ));
        } else {
          const incomplete = declared.held < declared.elements;
          rows.push(Contract.coverage(
            'supported', 'ordinary:' + request.edition.id + ':' + language,
            incomplete ? 'partial' : 'complete',
            incomplete ? [{ kind: 'language-missing', absenceKey: declared.absent }] : []
          ));
        }
      }
    }
    return rows;
  }

  function branchFor(derived, request) {
    const branches = derived.options || [];
    const territory = territoryId(request);
    if (branches.length === 1 && (branches[0].option === null || branches[0].option === territory)) {
      return branches[0];
    }
    if (territory === null) throw new Error('territorial Day branch must be explicit');
    const found = branches.find(function (one) { return one.option === territory; });
    if (!found) throw new Error('requested territorial Day branch is not held');
    return found;
  }

  function unresolvedTerritoryChoice(derived, request) {
    const branches = derived.options || [];
    if (branches.length < 2 || territoryId(request) !== null) return null;
    return Contract.unresolvedChoice(
      'calendar-territory',
      'this calendar has more than one source-authored territorial branch and none is a default',
      branches.map(function (branch) {
        const id = branch && branch.option;
        if (!id) throw new Error('territorial branch has no stable source-authored id');
        return { id: id, identity: { id: id } };
      }),
      []
    );
  }

  function hasOwn(value, key) {
    return Object.prototype.hasOwnProperty.call(value || {}, key);
  }

  function territoryId(request) {
    const territory = request.calendar && hasOwn(request.calendar, 'territory')
      ? request.calendar.territory : null;
    return territory && territory.id || null;
  }

  function readableFor(branch, request) {
    const rows = branch.readable || [];
    if (request.selectedReadableFormulary) {
      const exact = rows.find(function (one) {
        return one.key === request.selectedReadableFormulary.id;
      });
      if (!exact) throw new Error('requested readable formulary is not held on this Day branch');
      return exact;
    }
    const said = rows.filter(function (one) { return one.state === 'said'; });
    if (said.length === 1) return said[0];
    if (said.length > 1 || branch.choice) return null;
    return null;
  }

  function branchChoices(branch, request) {
    const out = [];
    if (branch.choice && (branch.choice.among || []).length > 1) {
      const selected = request && request.selectedReadableFormulary &&
        request.selectedReadableFormulary.id;
      const resolved = selected && branch.choice.among.some(function (one) {
        return (one.key || one.id) === selected;
      });
      if (!resolved) {
        out.push(Contract.unresolvedChoice(
          branch.choice.id || 'calendar-precedence',
          branch.choice.what || 'the calendar source leaves the celebrations coequal',
          branch.choice.among.map(function (one) {
            const id = one.key || one.id;
            return { id: id, identity: { id: id } };
          }),
          branch.choice.locus ? [{ kind: 'locus', id: branch.choice.locus }] : []
        ));
      }
    }
    for (const choice of branch.massChoices || []) {
      if ((choice.among || []).length < 2) continue;
      const selected = request && request.selectedReadableFormulary &&
        request.selectedReadableFormulary.id;
      if (selected && choice.among.some(function (one) {
        return (one.key || one.id) === selected;
      })) continue;
      if (choice.preferred) {
        const held = choice.among.some(function (one) {
          return one.id === choice.preferred || one.key === choice.preferred;
        });
        if (!held) throw new Error('source-preferred formulary is not among the authorized options');
        continue;
      }
      out.push(Contract.unresolvedChoice(
        choice.id || 'authorized-formulary-choice',
        choice.openBecause || choice.what || 'the source authorizes coequal options',
        choice.among.map(function (one) { return {
          id: one.key || one.id,
          identity: { id: one.key || one.id }
        }; }),
        choice.locus ? [{ kind: 'locus', id: choice.locus }] : []
      ));
    }
    return out;
  }

  function translationChoices(events) {
    return selectedRows(events).filter(function (row) {
      return row.selected.availability === 'choice-required' &&
        (row.selected.unresolvedWitnesses || []).length > 1;
    }).map(function (row) {
      const event = row.event;
      return Contract.unresolvedChoice(
        'translation-witness:' + event.id + (row.cycle ? ':' + row.cycle : ''),
        'more than one held witness supplies the requested translation language',
        row.selected.unresolvedWitnesses.map(function (id) {
          return {
            id: id,
            identity: { id: id },
            sourceHooks: [{ kind: 'translation', id: id }]
          };
        }),
        row.sourceHooks
      );
    });
  }

  function selectedRows(events) {
    const rows = [];
    (events || []).forEach(function (event) {
      if (event.kind !== 'proper' || !event.selected) return;
      if (event.selected.kind !== 'cycle-alternatives') {
        rows.push({
          event: event, selected: event.selected, cycle: null,
          sourceHooks: event.sourceHooks || []
        });
        return;
      }
      event.selected.alternatives.forEach(function (alternative) {
        rows.push({
          event: event, selected: alternative.material, cycle: alternative.cycle,
          sourceHooks: alternative.sourceHooks || []
        });
      });
    });
    return rows;
  }

  function explicitAbsencesFor(branch, lectionary) {
    return (branch.absent || []).map(function (one) {
      return {
        kind: 'explicit-semantic-absence', scope: 'calendar-result',
        repositoryTerm: 'absent', value: one
      };
    }).concat(lectionary ? [] : [{
      kind: 'explicit-semantic-absence',
      scope: 'lectionary-cycle',
      repositoryTerm: 'semantic-absence',
      reason: 'not-applicable-to-edition'
    }]);
  }

  function unresolvedDayResult(request, calendar, date, branch, choices) {
    return {
      entrance: 'day',
      request: request,
      calendarResult: {
        calendar: calendar, date: date, territory: branch.option,
        winner: branch.winner && branch.winner.id || null,
        selectedBranch: branch.option,
        settled: branch.settled
      },
      resolved: null,
      events: [],
      coverage: [Contract.coverage(
        'absent', 'resolved-formulary', null,
        [{ kind: 'semantic-absence', repositoryTerm: 'unresolved' }]
      )],
      unresolvedChoices: choices
    };
  }

  function adaptDay(input) {
    const request = input.request;
    const checked = Contract.validateReaderState(request);
    if (!checked.ok || request.entrance !== 'day') throw new Error('invalid Day reader state');
    const derived = input.derived;
    if (!derived || derived.date !== request.civilDate || derived.calendar !== request.calendar.id) {
      throw new Error('Day adapter requires the matching existing MassAssembly result');
    }
    const territoryChoice = unresolvedTerritoryChoice(derived, request);
    if (territoryChoice) {
      return unresolvedDayResult(
        request, derived.calendar, derived.date,
        { option: null, winner: null, settled: null },
        [territoryChoice]
      );
    }
    const branch = branchFor(derived, request);
    const choices = branchChoices(branch, request);
    const readable = readableFor(branch, request);
    if (!readable && choices.length) {
      return unresolvedDayResult(
        request, derived.calendar, derived.date, branch, choices
      );
    }
    if (!readable) throw new Error('Day branch has no deterministic or explicitly selected formulary');
    const mass = (input.structure.masses || []).find(function (one) { return one.key === readable.key; });
    if (!mass) throw new Error('resolved Day formulary is absent from the selected edition structure');
    const formSelection = properFormSelection(mass, request);
    if (formSelection.choice) {
      const unresolved = choices.concat([formSelection.choice]);
      const result = unresolvedDayResult(
        request, derived.calendar, derived.date, branch, unresolved
      );
      result.resolved = {
        edition: request.edition.id, formulary: mass.key, standing: readable.state
      };
      return result;
    }
    const lectionary = derived.liturgicalYear && derived.liturgicalYear.lectionary || null;
    const adaptedRequest = Object.assign({}, request, { lectionary: lectionary });
    const frame = ordinaryFrame(mass);
    const ordinary = request.options && request.options.ordinary && frame.applicability === 'full'
      ? (input.ordinary || null) : null;
    const events = seatedEvents(
      mass, formSelection.rows, adaptedRequest, input.structure, ordinary, 'day'
    );
    const resolved = {
      edition: request.edition.id, formulary: mass.key, standing: readable.state
    };
    if (formSelection.id !== null) resolved.form = formSelection.id;
    return {
      entrance: 'day',
      request: request,
      calendarResult: {
        calendar: derived.calendar,
        date: derived.date,
        territory: branch.option,
        winner: branch.winner && branch.winner.id || null,
        selectedBranch: branch.option,
        settled: branch.settled,
        season: derived.season || null,
        week: derived.week || null,
        lectionary: lectionary
      },
      resolved: resolved,
      events: events,
      coverage: coverageFor(
        input.structure, mass, formSelection.rows.map(function (row) { return row.proper; }),
        request, ordinary, events
      ),
      explicitAbsences: explicitAbsencesFor(branch, lectionary),
      unresolvedChoices: choices.concat(translationChoices(events))
    };
  }

  function adaptPropers(input) {
    const request = input.request;
    const checked = Contract.validateReaderState(request);
    if (!checked.ok || request.entrance !== 'propers') throw new Error('invalid Propers reader state');
    if (input.structure.calendar !== request.edition.id) {
      throw new Error('Propers structure does not match requested edition');
    }
    const mass = (input.structure.masses || []).find(function (one) {
      return one.key === request.formulary.id;
    });
    if (!mass) throw new Error('requested Propers formulary is not held');
    if (request.formulary.type && request.formulary.type !== (mass.kind || null)) {
      throw new Error('requested Propers formulary type does not match the held object');
    }
    if (hasOwn(request, 'alternative')) {
      throw new Error('explicit Propers alternative has no held stable generated identity');
    }
    const formSelection = properFormSelection(mass, request);
    if (formSelection.choice) {
      return {
        entrance: 'propers', request: request, calendarResult: null,
        resolved: { edition: request.edition.id, formulary: mass.key, type: mass.kind || null },
        events: [],
        coverage: [Contract.coverage(
          'absent', 'resolved-form', null,
          [{ kind: 'semantic-absence', repositoryTerm: 'form_choice_required' }]
        )],
        explicitAbsences: [{
          kind: 'explicit-semantic-absence',
          scope: 'civil-date-and-calendar-result',
          repositoryTerm: 'semantic-absence',
          reason: 'propers-entrance-is-date-independent'
        }],
        unresolvedChoices: (request.unresolvedChoices || []).concat([formSelection.choice])
      };
    }
    const heldCycles = new Set();
    formSelection.rows.forEach(function (row) {
      const proper = row.proper;
      cycleSelections(proper).forEach(function (selection) { heldCycles.add(selection.key); });
    });
    if (hasOwn(request, 'cycle') && request.cycle !== null && !heldCycles.has(request.cycle)) {
      throw new Error('explicit cycle is not held by this Propers formulary');
    }
    const events = seatedEvents(
      mass, formSelection.rows, request, input.structure, null, 'propers'
    );
    const resolved = {
      edition: request.edition.id, formulary: mass.key, type: mass.kind || null
    };
    if (formSelection.id !== null) resolved.form = formSelection.id;
    return {
      entrance: 'propers',
      request: request,
      calendarResult: null,
      resolved: resolved,
      events: events,
      coverage: coverageFor(
        input.structure, mass, formSelection.rows.map(function (row) { return row.proper; }),
        request, null, events
      ),
      explicitAbsences: [{
        kind: 'explicit-semantic-absence',
        scope: 'civil-date-and-calendar-result',
        repositoryTerm: 'semantic-absence',
        reason: 'propers-entrance-is-date-independent'
      }],
      unresolvedChoices: (request.unresolvedChoices || []).concat(translationChoices(events))
    };
  }

  function sameJson(left, right) {
    return JSON.stringify(left) === JSON.stringify(right);
  }

  function cliLanguageMaterial(proper, request, generated) {
    const language = request.languages && request.languages.orations || 'la';
    if (language === 'la') return null;
    const projected = proper.language_selection;
    if (!projected || projected.requested !== language) {
      throw new Error('mass-today payload lacks the requested language projection');
    }
    if ((projected.available === true) !== (projected.status === 'full-text')) {
      throw new Error('mass-today language capability contradicts its status');
    }
    if (projected.status === 'full-text') {
      const texts = (projected.texts || []).filter(function (one) {
        return one && one.lang === language && one.text;
      });
      if (!texts.length || projected.held !== true || projected.complete !== true ||
          ['held', 'choice-required'].indexOf(generated.availability) < 0) {
        throw new Error('mass-today held translation disagrees with generated structure');
      }
      if (generated.availability === 'held') {
        const exact = texts.find(function (one) {
          return (one.source_id || one.source || null) === generated.sourceId;
        });
        if (!exact || exact.text !== generated.text) {
          throw new Error('mass-today selected translation text or witness drifted');
        }
      } else {
        const ids = texts.map(function (one) {
          return one.source_id || one.source || null;
        }).filter(Boolean).sort();
        if (!sameJson(ids, (generated.unresolvedWitnesses || []).slice().sort())) {
          throw new Error('mass-today translation choices disagree with generated witnesses');
        }
      }
      return generated;
    }
    if (projected.held !== false || projected.available !== false ||
        (projected.texts || []).some(function (one) { return one && one.text; })) {
      throw new Error('mass-today unavailable language projection claims held text');
    }
    if (projected.status === 'fallback-latin') {
      if (!projected.fallback || projected.fallback.lang !== 'la' ||
          projected.fallback.text !== proper.text ||
          generated.availability !== 'unavailable' || !generated.missing) {
        throw new Error('mass-today Latin fallback disagrees with generated absence');
      }
      return generated;
    }
    if (projected.status === 'withheld') {
      if (generated.availability !== 'unavailable' || !generated.missing ||
          generated.held !== false) {
        throw new Error('mass-today withheld translation disagrees with generated absence');
      }
      return generated;
    }
    if (projected.status === 'incipit-only') {
      if (generated.kind !== 'incipit-only') {
        throw new Error('mass-today incipit-only state disagrees with generated structure');
      }
      return generated;
    }
    if (projected.status === 'absent') {
      if (generated.availability !== 'absent' && generated.availability !== 'unavailable') {
        throw new Error('mass-today absent language state disagrees with generated structure');
      }
      return generated;
    }
    throw new Error('mass-today exposes an unsupported requested-language status');
  }

  function cliMaterial(proper, request, generatedProper) {
    const selection = generatedProper ? dayCycle(generatedProper, request.lectionary) : null;
    const cycle = selection ? selection.key : null;
    const cycles = selection && selection.dimension === 'sunday' ? [cycle] : [];
    const weekdayCycles = selection && selection.dimension === 'weekday' ? [cycle] : [];
    const references = (proper.verses || []).map(function (one) { return one.ref; }).filter(Boolean);
    if (references.length) {
      const generated = selectedMaterial(generatedProper, request, { numbering: null }, 'day');
      if (generated.kind !== 'scripture' || !sameJson(references, generated.references)) {
        throw new Error('mass-today scripture references disagree with generated structure');
      }
      const unresolved = (proper.verses || []).filter(function (one) {
        return !one.text;
      }).map(function (one) {
        return { reference: one.ref, reason: one.note || 'text-not-held' };
      });
      return {
        kind: 'scripture', bible: request.bible && request.bible.id || null,
        numbering: request.bible && request.bible.numbering || null,
        cycle: cycle, cycles: cycles, weekdayCycles: weekdayCycles,
        cycleDimension: selection ? selection.dimension : null,
        availability: unresolved.length ? 'unavailable' : 'held', rights: null,
        references: references,
        unresolved: unresolved
      };
    }
    const generated = selectedMaterial(generatedProper, request, { numbering: null }, 'day');
    const projected = cliLanguageMaterial(proper, request, generated);
    if (projected) return projected;
    const latin = proper.latin || {};
    if (latin.withheld) {
      if (proper.text || latin.held !== false || latin.available !== false ||
          ['rights-restricted', 'unavailable'].indexOf(latin.state) < 0) {
        throw new Error('mass-today withheld Latin capability is not fail-closed');
      }
      if (!generated || generated.availability !== 'unavailable' ||
          generated.reason !== 'latin-withheld' || generated.held !== false ||
          generated.unavailableState !== latin.state) {
        throw new Error('mass-today withheld Latin state disagrees with generated structure');
      }
      return generated;
    }
    if (proper.text) {
      const language = request.languages && request.languages.orations || 'la';
      if (language !== 'la') {
        throw new Error('mass-today payload does not expose a selected non-Latin oration witness');
      }
      const generatedText = selection && generatedProper[selection.family] &&
        generatedProper[selection.family][cycle] &&
        generatedProper[selection.family][cycle].text || generatedProper.text;
      if (proper.text !== generatedText) {
        throw new Error('mass-today composed text disagrees with generated structure');
      }
      return {
        kind: 'composed', language: 'la', cycle: cycle, cycles: cycles,
        weekdayCycles: weekdayCycles,
        cycleDimension: selection ? selection.dimension : null,
        sourceId: null, rights: null, missing: false, availability: 'held', text: proper.text
      };
    }
    if (generated && generated.availability === 'unavailable' && generated.missing) {
      const language = proper.language_selection || {};
      if ((language.texts || []).some(function (one) { return one && one.text; })) {
        throw new Error('mass-today unavailable language selection unexpectedly carries text');
      }
      return generated;
    }
    return { kind: 'absent', rights: null, availability: 'absent', reason: 'semantic-absence' };
  }

  function adaptCli(input) {
    const request = input.request;
    const checked = Contract.validateReaderState(request);
    if (!checked.ok || request.entrance !== 'day') throw new Error('invalid Day reader state');
    if (!input.derived || input.derived.date !== request.civilDate ||
        input.derived.calendar !== request.calendar.id) {
      throw new Error('CLI adapter requires the matching existing MassAssembly result');
    }
    const payload = input.payload;
    if (payload.date !== request.civilDate) {
      throw new Error('mass-today payload date does not match the requested Day state');
    }
    const day = (payload.days || []).find(function (one) {
      return one.calendar === request.calendar.id;
    });
    if (!day) throw new Error('mass-today payload does not carry the requested calendar');
    if (!payload.scripture || payload.scripture.id !== (request.bible && request.bible.id)) {
      throw new Error('mass-today payload Bible does not match the requested Day state');
    }
    const territoryChoice = unresolvedTerritoryChoice(input.derived, request);
    if (territoryChoice) {
      if (day.territory_choice_required !== true || day.selected_territory !== null ||
          (day.masses || []).length) {
        throw new Error('mass-today must expose territorial choice without a flat fallback');
      }
      return unresolvedDayResult(
        request, day.calendar, payload.date,
        { option: null, winner: null, settled: null },
        [territoryChoice]
      );
    }
    const branch = branchFor(input.derived, request);
    const territory = territoryId(request);
    if (territory !== null && day.selected_territory !== territory) {
      throw new Error('mass-today selected territory disagrees with the explicit reader state');
    }
    const choices = branchChoices(branch, request);
    const readable = readableFor(branch, request);
    if (!readable && choices.length) {
      return unresolvedDayResult(request, day.calendar, payload.date, branch, choices);
    }
    if (!readable) throw new Error('CLI branch has no deterministic or explicitly selected formulary');
    const wanted = readable.key;
    const candidates = (day.masses || []).filter(function (one) {
      return one.key === wanted;
    });
    if (candidates.length !== 1) throw new Error('mass-today payload has no unique requested formulary');
    const mass = candidates[0];
    if (mass.standing !== readable.state) {
      throw new Error('mass-today formulary standing disagrees with calendar assembly');
    }
    if (!mass.bible || mass.bible.id !== request.bible.id) {
      throw new Error('mass-today formulary Bible does not match the request');
    }
    const generatedMass = input.structure && (input.structure.masses || []).find(function (one) {
      return one.key === mass.key;
    });
    if (!generatedMass) throw new Error('mass-today parity requires the matching generated formulary');
    const frame = ordinaryFrame(generatedMass);
    if (!sameJson(ordinaryFrame(mass), frame)) {
      throw new Error('mass-today Ordinary-frame applicability disagrees with generated structure');
    }
    const formSelection = properFormSelection(generatedMass, request);
    if (formSelection.choice) {
      if (mass.form_choice_required !== true || hasOwn(mass, 'selected_form') ||
          (mass.propers || []).length || (day.ordinary && !day.ordinary.refused)) {
        throw new Error('mass-today must expose an unseated form choice without fallback');
      }
      const unresolved = choices.concat([formSelection.choice]);
      const result = unresolvedDayResult(
        request, day.calendar, payload.date, branch, unresolved
      );
      result.resolved = {
        edition: request.edition.id, formulary: mass.key, standing: mass.standing
      };
      return result;
    }
    if (formSelection.id === null) {
      if (mass.selected_form !== 'main') {
        throw new Error('mass-today no-form formulary must expose selected_form main');
      }
    } else if (mass.selected_form !== formSelection.id || mass.form_choice_required === true) {
      throw new Error('mass-today selected form disagrees with the explicit reader state');
    }
    const generatedRows = formSelection.rows.filter(function (row) {
      return row.proper.name !== 'Placeholder';
    });
    if (generatedRows.length !== (mass.propers || []).length) {
      throw new Error('mass-today held Proper count disagrees with generated structure');
    }
    const lectionary = input.derived && input.derived.liturgicalYear &&
      input.derived.liturgicalYear.lectionary || null;
    const payloadLectionary = day.why && hasOwn(day.why, 'lectionary')
      ? day.why.lectionary : null;
    if (!sameJson(payloadLectionary, lectionary)) {
      throw new Error('mass-today lectionary result disagrees with calendar assembly');
    }
    const adaptedRequest = Object.assign({}, request, { lectionary: lectionary });
    function cliProper(proper, cliIndex, seat) {
      const generatedRow = generatedRows[cliIndex] || {};
      const generatedProper = generatedRow.proper || null;
      const sourceIndex = generatedRow.sourceIndex;
      if (!generatedProper || generatedProper.name !== proper.name ||
          (generatedProper.form || null) !== (proper.form || null) ||
          generatedProper.form_id !== proper.form_id ||
          (generatedProper.source || null) !== (proper.source || null) ||
          !sameJson(generatedProper.taken_from || null, proper.taken_from || null)) {
        throw new Error('mass-today Proper order disagrees with generated structure');
      }
      for (const family of ['cycles', 'weekday_cycles']) {
        const generatedKeys = Object.keys(generatedProper[family] || {}).sort();
        const payloadKeys = Object.keys(proper[family] || {}).sort();
        if (!sameJson(payloadKeys, generatedKeys)) {
          throw new Error('mass-today ' + family + ' inventory disagrees with generated structure');
        }
      }
      const selected = cliMaterial(proper, adaptedRequest, generatedProper);
      return {
        id: properEventId(request.edition.id, mass.key, sourceIndex),
        kind: 'proper',
        semanticSlot: semanticSlot(generatedProper),
        editionSlotLabel: proper.name || null,
        form: proper.form || null,
        sourceKind: proper.source || null,
        selected: selected,
        seat: seat || null,
        sourceHooks: sourceHooks(
          proper, selected, request.edition.id, mass.key, sourceIndex
        )
      };
    }
    let events;
    if (request.options && request.options.ordinary && frame.applicability === 'full' &&
        day.ordinary && !day.ordinary.refused) {
      const ordinary = day.ordinary;
      const group = Seating.variantGroupOf(ordinary);
      const variants = request.options.legitimate || {};
      const wantedVariant = group && variants[group.group] || null;
      const shown = Seating.shownElements(ordinary, wantedVariant);
      const placed = Seating.seatPropers(mass.propers || [], Seating.seats(ordinary, shown));
      const indexes = new Map((mass.propers || []).map(function (proper, index) {
        return [proper, index];
      }));
      events = Seating.massEvents(shown, placed).map(function (event) {
        if (event.kind === 'begin_section') {
          return {
            id: 'ordinary-section/' + event.section.key,
            kind: 'ordinary-section',
            sourceHooks: [{
              kind: 'ordinary-structure', id: request.edition.id + '/' + event.section.key
            }]
          };
        }
        if (event.kind === 'ordinary_element') {
          const selected = ordinaryTranslation(
            event.element, ordinary, request.languages && request.languages.ordinary || 'en',
            request.languages && request.languages.ordinaryWitness || null
          );
          return {
            id: 'ordinary-element/' + event.element.key,
            kind: 'ordinary-element',
            speaker: event.element.speaker || null,
            action: event.element.kind === 'rubric',
            locus: event.element.locus || null,
            selected: selected,
            sourceHooks: [{
              kind: 'ordinary-structure',
              id: request.edition.id + '/' + event.element.key
            }].concat(selected.sourceId ? [{ kind: 'translation', id: selected.sourceId }] : [])
          };
        }
        return cliProper(event.proper, indexes.get(event.proper), event.seat ? {
          id: event.seat.key,
          anchor: event.seat.anchor,
          where: event.seat.where,
          locus: event.seat.locus,
          placement: event.placement
        } : null);
      });
    } else {
      events = (mass.propers || []).map(function (proper, index) {
        return cliProper(proper, index, null);
      });
    }
    const resolved = {
      edition: request.edition.id, formulary: mass.key, standing: mass.standing
    };
    if (formSelection.id !== null) resolved.form = formSelection.id;
    return {
      entrance: 'day',
      request: request,
      calendarResult: {
        calendar: day.calendar, date: payload.date, territory: branch.option,
        winner: branch.winner && branch.winner.id || null,
        selectedBranch: branch.option, settled: day.settled, season: day.season || null,
        week: day.week || null,
        lectionary: lectionary
      },
      resolved: resolved,
      events: events,
      coverage: coverageFor(
        input.structure, generatedMass,
        formSelection.rows.map(function (row) { return row.proper; }), request,
        request.options && request.options.ordinary && frame.applicability === 'full' &&
          day.ordinary && !day.ordinary.refused
          ? day.ordinary : null,
        events
      ),
      explicitAbsences: explicitAbsencesFor(branch, lectionary),
      unresolvedChoices: choices.concat(translationChoices(events))
    };
  }

  function validationContext(input) {
    const context = { missals: {}, bibles: {} };
    for (const bible of (input.bibles && input.bibles.bibles) || []) {
      context.bibles[bible.id] = { numbering: bible.numbering || null };
    }
    const dayCalendars = new Set(
      ((input.rubricsIndex && input.rubricsIndex.calendars) || []).map(function (one) {
        return one.calendar;
      })
    );
    const properEntries = ((input.properIndex && input.properIndex.missals) || []).filter(
      function (entry) {
        return input.entrance !== 'day' || dayCalendars.has(entry.id);
      }
    );
    for (const entry of properEntries) {
      const structure = input.structures && input.structures[entry.id];
      if (!structure) continue;
      const types = {};
      const formsByMass = {};
      for (const mass of structure.masses || []) {
        const type = mass.kind || 'other';
        if (!types[type]) types[type] = [];
        types[type].push(mass.key);
        formsByMass[mass.key] = (mass.forms || []).map(function (form) { return form.id; });
      }
      const languages = ['la'];
      for (const translation of structure.translations || []) {
        if (translation.lang && languages.indexOf(translation.lang) < 0) languages.push(translation.lang);
      }
      context.missals[entry.id] = {
        calendar: structure.calendar || entry.id,
        types: types,
        formsByMass: formsByMass,
        orationLanguages: languages,
        ordinaryLanguages: [],
        variantGroups: {}
      };
    }
    for (const row of (input.ordinaryIndex && input.ordinaryIndex.calendars) || []) {
      if (!context.missals[row.calendar]) continue;
      const ordinary = input.ordinaries && input.ordinaries[row.calendar];
      if (!ordinary) continue;
      context.missals[row.calendar].ordinaryLanguages = (ordinary.languages || []).map(function (one) {
        return one.lang;
      });
      for (const group of ordinary.variants || []) {
        context.missals[row.calendar].variantGroups[group.group] = (group.options || []).map(function (one) {
          return one.id;
        });
      }
    }
    if (input.derived) {
      const branches = input.derived.options || [];
      const selectedBranches = input.territory === undefined
        ? branches
        : branches.filter(function (one) { return one.option === input.territory; });
      const readable = new Map();
      selectedBranches.forEach(function (branch) {
        (branch.readable || []).forEach(function (one) {
          if (!readable.has(one.key)) {
            readable.set(one.key, { id: one.key, state: one.state });
          }
        });
      });
      context.dayReadableFormularies = Array.from(readable.values());
    }
    return context;
  }

  return Object.freeze({
    properEventId: properEventId,
    validationContext: validationContext,
    adaptDay: adaptDay,
    adaptPropers: adaptPropers,
    adaptCli: adaptCli
  });
}));
