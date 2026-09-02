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

  function qualifiedSemanticId(proper) {
    const name = proper && proper.name || '';
    if (SEMANTIC_SLOTS[name]) return SEMANTIC_SLOTS[name];
    const family = /^(.+?) \(.+\)$/.exec(name);
    return family && SEMANTIC_SLOTS[family[1]] || null;
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
      return { id: null, rows: normalized, choice: null, forms: [], form: null };
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
        form: null,
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
    return {
      id: selected, rows: rowsById.get(selected), choice: null, forms: forms,
      form: forms.find(function (form) { return form.id === selected; })
    };
  }

  function ordinaryFrame(mass, selectedForm) {
    const owner = selectedForm &&
      Object.prototype.hasOwnProperty.call(selectedForm, 'ordinary_frame')
      ? selectedForm : mass;
    if (!owner || !Object.prototype.hasOwnProperty.call(owner, 'ordinary_frame')) {
      return { applicability: 'full' };
    }
    const frame = owner.ordinary_frame;
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
        (row.translations || []).some(function (translation) {
          return translation && translation.text;
        }) ||
        (row.unavailable_translations || []).length ||
        (row.untranslated || []).length ||
        (row.latin && row.latin.withheld) || row.text_status
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

  function exactPublicTextStatus(value, owner) {
    if (value === null || value === undefined) return null;
    if (!value || typeof value !== 'object' || Array.isArray(value) ||
        !sameJson(Object.keys(value).sort(), ['scope', 'state'])) {
      throw new Error(owner + ' text_status must use the exact public state/scope shape');
    }
    return value;
  }

  function properBodyStatus(owner) {
    const status = exactPublicTextStatus(owner && owner.text_status, 'Proper');
    if (!status) return null;
    if (status.state !== 'unavailable' || status.scope !== 'proper-body') {
      throw new Error('Proper text_status must be unavailable/proper-body');
    }
    if (typeof owner.text === 'string' && owner.text.length) {
      throw new Error('proper-body text_status may not coexist with Proper text');
    }
    return status;
  }

  function massTextStatus(mass) {
    const status = exactPublicTextStatus(mass && mass.text_status, 'Mass');
    if (!status) return null;
    const identity = status.state + '/' + status.scope;
    if (['partial/missal-formulary', 'unavailable/missal-formulary',
         'unavailable/proper-collect'].indexOf(identity) < 0) {
      throw new Error('Mass text_status uses an unsupported public state/scope pair');
    }
    return status;
  }

  function typedUnavailableFor(proper, wanted, selection) {
    const owner = selectedOwner(proper, selection);
    const ownerBodyStatus = properBodyStatus(owner);
    const properBodyFallback = owner === proper ? null : properBodyStatus(proper);
    const bodyStatus = ownerBodyStatus || properBodyFallback;
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
    if (wanted === 'la' && bodyStatus) {
      return {
        kind: 'composed', language: 'la', sourceId: null, source: null,
        rights: null, missing: true, text: null, availability: 'unavailable',
        held: false, reason: 'proper-body-unavailable',
        unavailableState: 'unavailable'
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
    const witness = request.languages && request.languages.translationWitness || null;
    if (wanted === 'la') {
      if (witness) {
        throw new Error('a translation witness cannot select the Latin source language');
      }
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
      const ownerTranslations = (owner.translations || []).filter(function (one) {
        return one && one.lang === wanted && one.text;
      });
      const parentTranslations = (proper.translations || []).filter(function (one) {
        return one && one.lang === wanted && one.text;
      });
      const translations = owner !== proper && (cycleText || ownerTranslations.length)
        ? ownerTranslations : parentTranslations;
      if (witness && translations.length && !translations.some(function (one) {
        return (one.source_id || one.source || null) === witness;
      })) {
        throw new Error('explicit translation witness is not held for an appointed Proper');
      }
      const typed = typedUnavailableFor(proper, wanted, selection);
      if (typed) return Object.assign(typed, {
        cycle: typed.cycle || cycle,
        cycles: cycleRows,
        weekdayCycles: weekdayCycleRows,
        cycleDimension: selection ? selection.dimension : null
      });
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
            held: false, text: null, reason: 'translation-witness-identity-missing'
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
        held: false, text: null, reason: 'translation-missing'
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

  function projectProper(
    proper, index, mass, request, structure, cycleMode, seat, semanticSlotOverride
  ) {
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
      semanticSlot: semanticSlotOverride || semanticSlot(proper),
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
    if (witness && candidates.length && !found) {
      throw new Error('explicit Ordinary witness is not held for an appointed element');
    }
    if (found) {
      return {
        kind: 'ordinary-text',
        language: language,
        sourceId: found.source_id || found.source || null,
        rights: found.rights || null,
        relation: found.relation || null,
        collation: found.collation || null,
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
    const absenceKey = row && element.absent && element.absent[row.absent] ||
      'language-not-held';
    const typedAbsence = (ordinary.language_absences || []).find(function (one) {
      return one && one.lang === language && one.key === absenceKey;
    }) || (ordinary.absences || []).find(function (one) {
      return one && one.key === absenceKey;
    }) || null;
    const unavailableState = typedAbsence && typedAbsence.state || 'unavailable';
    return {
      kind: 'ordinary-text', language: language,
      sourceId: null,
      rights: null,
      held: false,
      reason: unavailableState,
      unavailableState: unavailableState,
      absenceKey: absenceKey,
      availability: 'unavailable',
      text: null
    };
  }

  function ordinarySelections(ordinary, request) {
    const wanted = request.options && request.options.legitimate || {};
    const groups = Seating.variantGroupsOf(ordinary);
    const byId = new Map(groups.map(function (group) { return [group.group, group]; }));
    Object.keys(wanted).forEach(function (groupId) {
      const group = byId.get(groupId);
      if (!group || !(group.options || []).some(function (one) {
        return one.id === wanted[groupId];
      })) {
        throw new Error('explicit Ordinary option is not held by this edition');
      }
    });
    return Seating.selectionMap(ordinary, wanted);
  }

  function ordinaryElements(ordinary, request, propers, predicateFacts) {
    const predicates = Object.assign({}, predicateFacts || {});
    if ((propers || []).some(function (proper) {
      return proper && proper.name === 'Second Reading';
    })) predicates['second-reading-appointed'] = true;
    const resolution = Seating.resolveElements(
      ordinary, ordinarySelections(ordinary, request), predicates
    );
    return {
      shown: resolution.shown,
      unresolved: resolution.unresolved.map(function (row) {
        return {
          kind: 'ordinary-unresolved', state: 'unresolved',
          section: row.section, element: row.element,
          condition: Object.assign({}, row.condition)
        };
      })
    };
  }

  function assertSeatingComplete(placed) {
    const rows = (placed.before || []).concat(placed.after || []);
    for (const bucket of placed.buckets.values()) {
      rows.push.apply(rows, bucket);
    }
    const conserved = rows.reduce(function (count, row) {
      return count + (row && row.kind === 'proper_choice'
        ? (row.options || []).reduce(function (held, option) {
            return held + (option.rows || []).length;
          }, 0) : 1);
    }, 0);
    const unusable = rows.some(function (row) {
      if (!row || !row.seat) return true;
      if (row.seat.placement !== 'unseated') return !row.seat.key;
      return !row.seat.key || !row.seat.group || !row.seat.basis ||
        ['before-frame', 'after-frame'].indexOf(row.seat.region) < 0;
    });
    if (placed.broke || unusable || conserved !== placed.sourceCount) {
      throw new Error('appointed Proper has no usable semantic Ordinary seat');
    }
  }

  function projectedSeat(seat, placement, mass, request) {
    if (!seat) return null;
    if (seat.placement === 'unseated') {
      return {
        id: 'unplaced/' + request.edition.id + '/' + mass.key + '/' +
          seat.formId + '/' + seat.group,
        placement: 'unseated', region: seat.region, basis: seat.basis
      };
    }
    if (!seat.key || placement !== 'seated') {
      throw new Error('appointed Proper has no usable semantic Ordinary seat');
    }
    return {
      id: seat.key, anchor: seat.anchor, where: seat.where,
      locus: seat.locus, placement: 'seated'
    };
  }

  function uniqueSourceHooks(events) {
    const seen = new Set();
    const hooks = [];
    (events || []).forEach(function (event) {
      (event.sourceHooks || []).forEach(function (hook) {
        const key = hook.kind + '\u0000' + hook.id;
        if (seen.has(key)) return;
        seen.add(key);
        hooks.push(hook);
      });
    });
    return hooks;
  }

  function sharedChoiceSemanticSlot(event) {
    const ids = new Set();
    (event.options || []).forEach(function (option) {
      (option.rows || []).forEach(function (row) {
        const id = qualifiedSemanticId(row.proper);
        if (id) ids.add(id);
      });
    });
    if (ids.size > 1) {
      throw new Error('alternative Proper group has no unique cross-edition semantic slot');
    }
    if (ids.size === 0) {
      return {
        state: 'edition-local-unmapped',
        reason: 'source choice has no cross-edition semantic slot identity'
      };
    }
    return { state: 'mapped', identity: { id: Array.from(ids)[0] } };
  }

  function projectProperChoice(event, mass, request, projectMember) {
    const id = 'proper-choice/' + request.edition.id + '/' + mass.key + '/' +
      event.formId + '/' + event.group;
    const seat = projectedSeat(event.seat, event.placement, mass, request);
    const semantic = sharedChoiceSemanticSlot(event);
    const options = (event.options || []).map(function (option) {
      const events = (option.rows || []).map(function (row) {
        return projectMember(row, seat, semantic);
      });
      if (!events.length || new Set(events.map(function (one) { return one.id; })).size !== events.length) {
        throw new Error('alternative Proper option must conserve distinct source events');
      }
      return { id: option.id, events: events };
    });
    if (options.length < 2 || new Set(options.map(function (one) { return one.id; })).size !== options.length) {
      throw new Error('alternative Proper choice must carry distinct options');
    }
    const memberEvents = options.reduce(function (all, option) {
      return all.concat(option.events);
    }, []);
    return {
      id: id, kind: 'proper-choice', group: event.group,
      selection: { state: 'required', option: null },
      seat: seat, options: options, sourceHooks: uniqueSourceHooks(memberEvents),
      choiceBasis: event.basis
    };
  }

  function projectSeatingEvents(events, mass, request, projectMember, projectOrdinary) {
    return (events || []).map(function (event) {
      if (event.kind === 'proper_choice') {
        return projectProperChoice(event, mass, request, projectMember);
      }
      if (event.kind === 'proper') {
        return projectMember(
          event,
          projectedSeat(event.seat, event.placement, mass, request),
          null
        );
      }
      return projectOrdinary(event);
    });
  }

  function seatedEvents(
    mass, properRows, request, structure, ordinary, cycleMode, predicateFacts
  ) {
    if (!ordinary) {
      const unframed = Seating.unframedEvents(
        properRows, function (proper) { return proper && proper.name === 'Placeholder'; }
      );
      return {
        events: projectSeatingEvents(
          unframed, mass, request,
          function (row, seat, semantic) {
            return projectProper(
              row.proper, row.sourceIndex, mass, request, structure, cycleMode,
              seat, semantic
            );
          },
          function () { throw new Error('unframed Proper sequence carried an Ordinary event'); }
        ),
        ordinaryUnresolved: []
      };
    }
    const resolution = ordinaryElements(
      ordinary, request, properRows.map(function (row) { return row.proper; }),
      predicateFacts
    );
    const placed = Seating.seatPropers(
      properRows,
      Seating.seats(ordinary, resolution.shown),
      function (proper) { return proper && proper.name === 'Placeholder'; }
    );
    assertSeatingComplete(placed);
    const events = projectSeatingEvents(
      Seating.massEvents(resolution.shown, placed), mass, request,
      function (row, seat, semantic) {
        return projectProper(
          row.proper, row.sourceIndex, mass, request, structure, cycleMode,
          seat, semantic
        );
      },
      function (event) {
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
      throw new Error('Ordinary seating emitted an unsupported semantic event');
    });
    return { events: events, ordinaryUnresolved: resolution.unresolved };
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

  function ordinaryRelationRows(ordinary, language) {
    if (Object.prototype.hasOwnProperty.call(ordinary, 'relation_coverage')) {
      if (!Array.isArray(ordinary.relation_coverage)) {
        throw new Error('Ordinary relation coverage must be an array');
      }
      return ordinary.relation_coverage.filter(function (row) {
        return row && row.lang === language;
      }).map(function (row) {
        if (['own', 'antecedent'].indexOf(row.relation) < 0 ||
            ['not-applicable', 'collated', 'uncollated'].indexOf(row.collation) < 0 ||
            !Number.isInteger(row.count) || row.count < 1 ||
            (row.relation === 'own') !== (row.collation === 'not-applicable')) {
          throw new Error('Ordinary relation coverage carries an invalid grade');
        }
        return {
          lang: row.lang, relation: row.relation,
          collation: row.collation, count: row.count
        };
      });
    }
    const grouped = new Map();
    for (const section of ordinary.sections || []) {
      for (const element of section.elements || []) {
        for (const translation of element.translations || []) {
          if (!translation || translation.lang !== language || !translation.text) continue;
          const relation = translation.relation || 'antecedent';
          const collation = translation.collation ||
            (relation === 'own' ? 'not-applicable' : 'uncollated');
          const key = relation + '|' + collation;
          grouped.set(key, (grouped.get(key) || 0) + 1);
        }
      }
    }
    return Array.from(grouped.entries()).map(function (entry) {
      const parts = entry[0].split('|');
      return {
        lang: language, relation: parts[0], collation: parts[1], count: entry[1]
      };
    });
  }

  function ordinaryAbsenceReasons(ordinary, languageDeclaration, language) {
    const counts = new Map();
    for (const section of ordinary.sections || []) {
      for (const element of section.elements || []) {
        const key = element && element.absent && element.absent[languageDeclaration.absent];
        if (key) counts.set(key, (counts.get(key) || 0) + 1);
      }
    }
    if (Object.prototype.hasOwnProperty.call(ordinary, 'language_absences')) {
      if (!Array.isArray(ordinary.language_absences)) {
        throw new Error('Ordinary language absences must be an array');
      }
      return ordinary.language_absences.filter(function (row) {
        return row && row.lang === language;
      }).map(function (row) {
        if (typeof row.key !== 'string' || !row.key ||
            !Number.isInteger(row.count) || row.count < 1 ||
            ['rights-restricted', 'unresolved', 'unavailable'].indexOf(row.state) < 0 ||
            counts.get(row.key) !== row.count) {
          throw new Error('Ordinary typed language absence contradicts element coverage');
        }
        return {
          kind: row.state === 'rights-restricted' ? 'text-withheld' : 'text-not-held',
          absenceKey: row.key,
          sourceState: row.state,
          sourceKind: row.kind || null,
          count: row.count
        };
      });
    }
    const definitions = new Map((ordinary.absences || []).filter(Boolean).map(function (row) {
      return [row.key, row];
    }));
    return Array.from(counts.entries()).map(function (entry) {
      const definition = definitions.get(entry[0]) || {};
      const state = definition.state || 'unavailable';
      return {
        kind: state === 'rights-restricted' ? 'text-withheld' : 'text-not-held',
        absenceKey: entry[0],
        sourceState: state,
        sourceKind: definition.kind || null,
        count: entry[1]
      };
    });
  }

  function ordinaryLanguageCoverage(ordinary, request, ordinaryUnresolved) {
    const language = request.languages && request.languages.ordinary;
    const languageDeclaration = (ordinary.languages || []).find(function (one) {
      return one && one.lang === language;
    });
    if (Object.prototype.hasOwnProperty.call(ordinary, 'language_coverage') &&
        !Array.isArray(ordinary.language_coverage)) {
      throw new Error('Ordinary language coverage must be an array');
    }
    const canonicalCoverage = ordinary.language_coverage &&
      ordinary.language_coverage.find(function (one) { return one && one.lang === language; });
    if (ordinary.language_coverage && languageDeclaration && !canonicalCoverage) {
      throw new Error('Ordinary canonical language coverage omits a declared language');
    }
    const declared = canonicalCoverage || languageDeclaration;
    const scope = 'ordinary:' + request.edition.id + ':' + language;
    if (!declared || !languageDeclaration) {
      return Contract.coverage(
        'unavailable', scope, null,
        [{ kind: 'language-missing', absenceKey: 'language-not-held' }]
      );
    }
    if (!Number.isInteger(declared.held) || declared.held < 0 ||
        !Number.isInteger(declared.elements) || declared.elements < declared.held) {
      throw new Error('Ordinary language coverage carries invalid held counts');
    }
    const missing = declared.elements - declared.held;
    if (Object.prototype.hasOwnProperty.call(declared, 'missing') &&
        declared.missing !== missing) {
      throw new Error('Ordinary language missing count contradicts held coverage');
    }
    if (canonicalCoverage && canonicalCoverage.absent !== missing) {
      throw new Error('Ordinary language absent count contradicts missing coverage');
    }
    const relations = ordinaryRelationRows(ordinary, language);
    const relationCount = relations.reduce(function (count, row) { return count + row.count; }, 0);
    if (relationCount !== declared.held) {
      throw new Error('Ordinary relation grades contradict held language coverage');
    }
    const absenceReasons = ordinaryAbsenceReasons(ordinary, languageDeclaration, language);
    const absenceCount = absenceReasons.reduce(function (count, reason) {
      return count + reason.count;
    }, 0);
    if (absenceCount !== missing) {
      throw new Error('Ordinary typed absences contradict missing language coverage');
    }
    if (declared.held === 0) {
      const unavailableReasons = absenceReasons.length ? absenceReasons.slice() : [{
        kind: 'language-missing',
        absenceKey: languageDeclaration.absent || 'language-not-held'
      }];
      if ((ordinaryUnresolved || []).length) {
        unavailableReasons.push({
          kind: 'text-not-held', sourceState: 'unresolved',
          sourceKind: 'applicability-unresolved',
          count: ordinaryUnresolved.length,
          elements: ordinaryUnresolved.map(function (row) { return row.element; })
        });
      }
      return Contract.coverage(
        'unavailable', scope, null, unavailableReasons,
        { relationCoverage: relations }
      );
    }
    const antecedents = relations.filter(function (row) { return row.relation !== 'own'; });
    const reasons = absenceReasons.slice();
    antecedents.forEach(function (row) {
      reasons.push({
        kind: 'partial-recension', domain: 'ordinary', language: language,
        relation: row.relation, collation: row.collation, count: row.count
      });
    });
    if ((ordinaryUnresolved || []).length) {
      reasons.push({
        kind: 'text-not-held', sourceState: 'unresolved',
        sourceKind: 'applicability-unresolved',
        count: ordinaryUnresolved.length,
        elements: ordinaryUnresolved.map(function (row) { return row.element; })
      });
    }
    const incomplete = missing > 0 || antecedents.length > 0 ||
      (ordinaryUnresolved || []).length > 0;
    return Contract.coverage(
      'supported', scope, incomplete ? 'partial' : 'complete', reasons,
      {
        relationCoverage: relations,
        exclusions: (ordinary.exclusions || []).map(function (row) {
          const rawSources = row && row.sources;
          const legacyEvidence = Array.isArray(rawSources)
            ? rawSources.filter(function (source) {
                return source && typeof source === 'object' && !Array.isArray(source);
              }) : [];
          const evidence = row && Array.isArray(row.evidence) ? row.evidence : legacyEvidence;
          function carriesText(value) {
            if (!value || typeof value !== 'object') return false;
            return Object.keys(value).some(function (key) {
              return key === 'text' || carriesText(value[key]);
            });
          }
          const sources = Array.isArray(rawSources) ? rawSources.map(function (source) {
            return typeof source === 'string' ? source : source && source.source_id;
          }) : [];
          if (!row || typeof row.key !== 'string' || !row.key ||
              row.state !== 'not-in-target-recension' ||
              typeof row.basis !== 'string' || !row.basis.trim() ||
              !sources.length || sources.some(function (source) {
                return typeof source !== 'string' || !source;
              }) || evidence.some(carriesText)) {
            throw new Error('Ordinary exclusion lacks exact target-recension evidence');
          }
          return {
            key: row.key, state: row.state, basis: row.basis,
            sources: Array.from(new Set(sources)),
            evidence: JSON.parse(JSON.stringify(evidence))
          };
        })
      }
    );
  }

  function activeProperBodyClaims(propers, request) {
    const claims = [];
    (propers || []).forEach(function (proper, properIndex) {
      const selections = cycleSelections(proper);
      let activeSelections = selections;
      let includeProper = true;
      if (request.entrance === 'day') {
        const selected = dayCycle(proper, request.lectionary);
        activeSelections = selected ? [selected] : [];
      } else if (hasOwn(request, 'cycle') && request.cycle !== null) {
        const selected = explicitCycleSelection(proper, request.cycle);
        if (selections.length && !selected) includeProper = false;
        activeSelections = selected ? [selected] : [];
      }

      const topStatus = properBodyStatus(proper);
      if (topStatus && includeProper) {
        claims.push({
          proper: proper.name || null,
          cycle: null,
          properIndex: properIndex,
          latinWithheld: Boolean(proper.latin && proper.latin.withheld)
        });
      }
      selections.forEach(function (selection) {
        const owner = selectedOwner(proper, selection);
        // Validate every projected branch even when the current reader request
        // selects a different cycle. A malformed absence may never become an
        // implicit fallback merely because it is temporarily out of view.
        properBodyStatus(owner);
      });
      if (!includeProper) return;
      activeSelections.forEach(function (selection) {
        const owner = selectedOwner(proper, selection);
        if (!properBodyStatus(owner)) return;
        const latinOwner = owner.latin ? owner : proper;
        claims.push({
          proper: proper.name || null,
          cycle: selection.key,
          properIndex: properIndex,
          latinWithheld: Boolean(latinOwner.latin && latinOwner.latin.withheld)
        });
      });
    });
    return claims;
  }

  function commonSetDispositions(structure, mass) {
    const reference = mass && mass.takes_from;
    const selections = reference && reference.common_sets;
    if (selections === null || selections === undefined) return [];
    if (!selections || typeof selections !== 'object' || Array.isArray(selections) ||
        !Object.keys(selections).length) {
      throw new Error('takes_from.common_sets must be a nonempty mapping');
    }
    if (!reference || typeof reference.mass !== 'string' || !reference.mass) {
      throw new Error('takes_from.common_sets requires a stable target Common');
    }
    const target = ((structure && structure.masses) || []).find(function (candidate) {
      return candidate.key === reference.mass;
    });
    const definitions = target && target.common_sets;
    if (!definitions || typeof definitions !== 'object' || Array.isArray(definitions)) {
      throw new Error('takes_from.common_sets targets no projected Common-set definitions');
    }
    const selectedGroups = Object.keys(selections).sort();
    const definedGroups = Object.keys(definitions).sort();
    if (!sameJson(selectedGroups, definedGroups)) {
      throw new Error('takes_from.common_sets must disposition every target Common set');
    }

    return selectedGroups.map(function (group) {
      if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(group)) {
        throw new Error('takes_from.common_sets group has no stable lowercase id');
      }
      const disposition = selections[group];
      const definition = definitions[group];
      const options = definition && definition.options;
      if (!disposition || typeof disposition !== 'object' || Array.isArray(disposition) ||
          !options || typeof options !== 'object' || Array.isArray(options)) {
        throw new Error('takes_from.common_sets carries a malformed disposition or definition');
      }
      if (disposition.state === 'selected') {
        if (!sameJson(Object.keys(disposition).sort(), ['option', 'state']) ||
            typeof disposition.option !== 'string' || !disposition.option ||
            !hasOwn(options, disposition.option)) {
          throw new Error('selected Common set must name exactly one held option');
        }
        return {
          group: group, state: 'selected', candidates: [disposition.option],
          target: reference.mass, citation: reference.citation || null
        };
      }
      if (disposition.state !== 'unresolved' ||
          !sameJson(Object.keys(disposition).sort(), ['candidates', 'state']) ||
          !Array.isArray(disposition.candidates) || disposition.candidates.length < 2 ||
          disposition.candidates.some(function (candidate) {
            return typeof candidate !== 'string' || !candidate || !hasOwn(options, candidate);
          }) || new Set(disposition.candidates).size !== disposition.candidates.length) {
        throw new Error('unresolved Common set must name at least two unique held candidates');
      }
      return {
        group: group, state: 'unresolved', candidates: disposition.candidates.slice(),
        target: reference.mass, citation: reference.citation || null
      };
    });
  }

  function unresolvedCommonSetChoices(structure, mass, request) {
    return commonSetDispositions(structure, mass).filter(function (row) {
      return row.state === 'unresolved';
    }).map(function (row) {
      const claim = request.edition.id + '/' + mass.key + '/' + row.group;
      return Contract.unresolvedChoice(
        'common-set:' + claim,
        'the source leaves this inherited Common set unresolved',
        row.candidates.map(function (candidate) {
          const identity = row.target + '/' + row.group + '/' + candidate;
          return {
            id: candidate,
            identity: { id: identity },
            sourceHooks: [{ kind: 'common-set-option', id: identity }]
          };
        }),
        [{ kind: 'common-set-disposition', id: claim }]
      );
    });
  }

  function claimLocalCollectAbsences(mass, request, selectedForm) {
    const status = massTextStatus(mass);
    if (!status || status.scope !== 'proper-collect') return [];
    const formId = selectedForm && selectedForm.id || 'main';
    return [{
      kind: 'explicit-semantic-absence',
      scope: 'proper:' + request.edition.id + '/' + mass.key + '/' + formId + '/collect',
      repositoryTerm: 'proper-collect',
      value: 'Collect',
      claimOwner: mass.key,
      formId: formId,
      proper: 'Collect'
    }];
  }

  function coverageFor(
    structure, mass, propers, request, ordinary, events, ordinaryUnresolved, selectedForm
  ) {
    const rows = [];
    const effectiveFrame = ordinaryFrame(mass, selectedForm);
    const placeholders = propers.filter(function (one) { return one.name === 'Placeholder'; });
    const textStatus = massTextStatus(mass);
    const properBodyClaims = activeProperBodyClaims(propers, request);
    const unresolvedCommonSets = commonSetDispositions(structure, mass).filter(function (row) {
      return row.state === 'unresolved';
    });
    const partialRecension = partialRecensionReason(structure, mass);
    const claimReasons = [];
    if (properBodyClaims.length) {
      claimReasons.push({
        kind: 'text-not-held', count: properBodyClaims.length,
        repositoryTerm: 'proper-body',
        claims: properBodyClaims.map(function (claim) {
          return { proper: claim.proper, cycle: claim.cycle };
        })
      });
    }
    if (textStatus && textStatus.scope === 'proper-collect') {
      claimReasons.push({
        kind: 'text-not-held', count: 1, repositoryTerm: 'proper-collect',
        claimOwner: mass.key, proper: 'Collect'
      });
    }
    if (unresolvedCommonSets.length) {
      claimReasons.push({
        kind: 'unresolved-choice', count: unresolvedCommonSets.length,
        repositoryTerm: 'takes_from.common_sets',
        groups: unresolvedCommonSets.map(function (row) { return row.group; })
      });
    }
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
      reasons.push.apply(reasons, claimReasons);
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
      reasons.push.apply(reasons, claimReasons);
      rows.push(Contract.coverage(
        'supported', 'formulary:' + mass.key, 'partial',
        reasons
      ));
    } else if (partialRecension) {
      const reasons = [partialRecension].concat(claimReasons);
      rows.push(Contract.coverage(
        'supported', 'formulary:' + mass.key, 'partial', reasons
      ));
    } else if (claimReasons.length) {
      rows.push(Contract.coverage(
        'supported', 'formulary:' + mass.key, 'partial', claimReasons
      ));
    } else {
      rows.push(Contract.coverage('supported', 'formulary:' + mass.key, 'complete', []));
    }
    const selections = selectedRows(events);
    const unavailableOriginals = selections.filter(function (row) {
      return row.selected.missing && row.selected.language === 'la' &&
        row.selected.reason === 'latin-withheld';
    });
    const unheldOriginals = selections.filter(function (row) {
      return row.selected.missing && row.selected.language === 'la' &&
        row.selected.reason === 'proper-body-unavailable';
    });
    const withheldOriginalCount = Math.max(
      unavailableOriginals.length,
      properBodyClaims.filter(function (claim) { return claim.latinWithheld; }).length
    );
    const unheldOriginalCount = Math.max(
      unheldOriginals.length,
      properBodyClaims.filter(function (claim) { return !claim.latinWithheld; }).length
    );
    if (withheldOriginalCount || unheldOriginalCount) {
      const reasons = [];
      if (withheldOriginalCount) {
        reasons.push({ kind: 'text-withheld', count: withheldOriginalCount });
      }
      if (unheldOriginalCount) {
        reasons.push({ kind: 'text-not-held', count: unheldOriginalCount });
      }
      rows.push(Contract.coverage(
        'unavailable', 'proper-original:la', null,
        reasons
      ));
    }
    const restrictedTranslations = selections.filter(function (row) {
      return row.selected.missing && row.selected.language !== 'la' &&
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
      return row.selected.missing && row.selected.language !== 'la' &&
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
    if (textStatus && textStatus.scope === 'proper-collect') {
      const formId = selectedForm && selectedForm.id || 'main';
      rows.push(Contract.coverage(
        'unavailable',
        'proper-body:' + request.edition.id + '/' + mass.key + '/' + formId + '/collect',
        null,
        [{
          kind: 'text-not-held', repositoryTerm: 'proper-collect',
          claimOwner: mass.key, proper: 'Collect'
        }]
      ));
    }
    const unplaced = [];
    const unseatedChoices = [];
    (events || []).forEach(function (event) {
      if (event && event.kind === 'proper' && event.seat &&
          event.seat.placement === 'unseated') {
        unplaced.push({ id: event.seat.id, region: event.seat.region });
      } else if (event && event.kind === 'proper-choice' && event.seat === null) {
        unseatedChoices.push(event.id);
      }
    });
    if (unplaced.length || (request.options && request.options.ordinary &&
        effectiveFrame.applicability !== 'full')) {
      rows.push(Contract.coverage(
        'unsupported', 'ordinary-placement:' + request.edition.id, null,
        [{
          kind: 'ordinary-placement-unavailable',
          applicability: effectiveFrame.applicability,
          basis: effectiveFrame.basis || null,
          unplaced: unplaced,
          choices: unseatedChoices
        }]
      ));
    }
    if (request.options && request.options.ordinary) {
      const frame = effectiveFrame;
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
        rows.push(ordinaryLanguageCoverage(ordinary, request, ordinaryUnresolved));
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

  function selectedTextRows(events) {
    const rows = selectedRows(events);
    (events || []).forEach(function (event) {
      if (event.kind !== 'ordinary-element' || !event.selected) return;
      rows.push({
        event: event, selected: event.selected, cycle: null,
        sourceHooks: event.sourceHooks || []
      });
    });
    return rows;
  }

  function alternativeChoices(events) {
    return (events || []).filter(function (event) {
      return event && event.kind === 'proper-choice';
    }).map(function (event) {
      return Contract.unresolvedChoice(
        event.id,
        event.choiceBasis,
        (event.options || []).map(function (option) {
          return {
            id: option.id,
            identity: { id: event.id + '/' + option.id },
            sourceHooks: uniqueSourceHooks(option.events || [])
          };
        }),
        event.sourceHooks || []
      );
    });
  }

  function translationChoices(events) {
    return selectedTextRows(events).filter(function (row) {
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

  function assertExplicitWitnesses(events, request) {
    const languages = request.languages || {};
    if (languages.translationWitness) {
      const held = selectedRows(events).some(function (row) {
        return row.selected.sourceId === languages.translationWitness;
      });
      if (!held) throw new Error('explicit translation witness selected no appointed text');
    }
    if (languages.ordinaryWitness) {
      const held = (events || []).some(function (event) {
        return event.kind === 'ordinary-element' && event.selected &&
          event.selected.sourceId === languages.ordinaryWitness;
      });
      if (!held) throw new Error('explicit Ordinary witness selected no appointed text');
    }
  }

  function selectedRows(events) {
    const rows = [];
    const properEvents = [];
    (events || []).forEach(function (event) {
      if (event && event.kind === 'proper-choice') {
        (event.options || []).forEach(function (option) {
          properEvents.push.apply(properEvents, option.events || []);
        });
      } else {
        properEvents.push(event);
      }
    });
    properEvents.forEach(function (event) {
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
      unresolvedChoices: choices,
      ordinaryUnresolved: []
    };
  }

  function adaptDay(input) {
    const request = input.request;
    const checked = Contract.validateReaderState(request);
    if (!checked.ok || request.entrance !== 'day') throw new Error('invalid Day reader state');
    if (!input.structure || input.structure.calendar !== request.edition.id) {
      throw new Error('Day structure does not match requested edition');
    }
    if (input.ordinary && input.ordinary.calendar !== request.edition.id) {
      throw new Error('Day Ordinary does not match requested edition');
    }
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
      if (request.languages && (request.languages.translationWitness ||
          request.languages.ordinaryWitness)) {
        throw new Error('an explicit witness requires an exact selected Mass form');
      }
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
    const frame = ordinaryFrame(mass, formSelection.form);
    const ordinary = request.options && request.options.ordinary && frame.applicability === 'full'
      ? (input.ordinary || null) : null;
    const seated = seatedEvents(
      mass, formSelection.rows, adaptedRequest, input.structure, ordinary, 'day',
      Seating.predicateFacts({
        settled: branch.settled, weekday: derived.weekday,
        season: derived.season, nature: branch.winner && branch.winner.nature
      })
    );
    const events = seated.events;
    assertExplicitWitnesses(events, adaptedRequest);
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
        adaptedRequest, ordinary, events, seated.ordinaryUnresolved, formSelection.form
      ),
      explicitAbsences: explicitAbsencesFor(branch, lectionary).concat(
        claimLocalCollectAbsences(mass, request, formSelection.form)
      ),
      unresolvedChoices: choices.concat(
        unresolvedCommonSetChoices(input.structure, mass, request),
        alternativeChoices(events), translationChoices(events)
      ),
      ordinaryUnresolved: seated.ordinaryUnresolved
    };
  }

  function adaptPropers(input) {
    const request = input.request;
    const checked = Contract.validateReaderState(request);
    if (!checked.ok || request.entrance !== 'propers') throw new Error('invalid Propers reader state');
    if (!input.structure || input.structure.calendar !== request.edition.id) {
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
      if (request.languages && request.languages.translationWitness) {
        throw new Error('an explicit witness requires an exact selected Mass form');
      }
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
        unresolvedChoices: (request.unresolvedChoices || []).concat([formSelection.choice]),
        ordinaryUnresolved: []
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
    const seated = seatedEvents(
      mass, formSelection.rows, request, input.structure, null, 'propers'
    );
    const events = seated.events;
    assertExplicitWitnesses(events, request);
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
        request, null, events, seated.ordinaryUnresolved, formSelection.form
      ),
      explicitAbsences: [{
        kind: 'explicit-semantic-absence',
        scope: 'civil-date-and-calendar-result',
        repositoryTerm: 'semantic-absence',
        reason: 'propers-entrance-is-date-independent'
      }].concat(claimLocalCollectAbsences(mass, request, formSelection.form)),
      unresolvedChoices: (request.unresolvedChoices || []).concat(
        unresolvedCommonSetChoices(input.structure, mass, request),
        alternativeChoices(events), translationChoices(events)
      ),
      ordinaryUnresolved: seated.ordinaryUnresolved
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
    if (!input.structure || input.structure.calendar !== request.edition.id) {
      throw new Error('CLI Proper structure does not match requested edition');
    }
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
    if (day.ordinary && day.ordinary.calendar !== request.edition.id) {
      throw new Error('mass-today Ordinary does not match requested edition');
    }
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
    const formSelection = properFormSelection(generatedMass, request);
    if (formSelection.choice) {
      if (request.languages && (request.languages.translationWitness ||
          request.languages.ordinaryWitness)) {
        throw new Error('an explicit witness requires an exact selected Mass form');
      }
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
    const frame = ordinaryFrame(generatedMass, formSelection.form);
    if (!sameJson(ordinaryFrame(mass), frame)) {
      throw new Error('mass-today Ordinary-frame applicability disagrees with generated structure');
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
    const payloadBySourceIndex = new Map();
    generatedRows.forEach(function (generatedRow, cliIndex) {
      payloadBySourceIndex.set(generatedRow.sourceIndex, {
        proper: (mass.propers || [])[cliIndex], generated: generatedRow.proper
      });
    });
    function cliProper(row, seat, semanticSlotOverride) {
      const sourceIndex = row.sourceIndex;
      const held = payloadBySourceIndex.get(sourceIndex) || {};
      const proper = held.proper;
      const generatedProper = row.proper;
      if (!generatedProper || generatedProper.name !== proper.name ||
          (generatedProper.form || null) !== (proper.form || null) ||
          generatedProper.form_id !== proper.form_id ||
          (generatedProper.source || null) !== (proper.source || null) ||
          !sameJson(generatedProper.taken_from || null, proper.taken_from || null) ||
          !sameJson(
            generatedProper.ordinary_disposition || null,
            proper.ordinary_disposition || null
          )) {
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
        semanticSlot: semanticSlotOverride || semanticSlot(generatedProper),
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
    let ordinaryUnresolved = [];
    if (request.options && request.options.ordinary && frame.applicability === 'full' &&
        day.ordinary && !day.ordinary.refused) {
      const ordinary = day.ordinary;
      const resolution = ordinaryElements(
        ordinary, adaptedRequest,
        generatedRows.map(function (row) { return row.proper; }),
        Seating.predicateFacts({
          settled: branch.settled, weekday: input.derived.weekday,
          season: input.derived.season,
          nature: branch.winner && branch.winner.nature
        })
      );
      ordinaryUnresolved = resolution.unresolved;
      const placed = Seating.seatPropers(
        generatedRows, Seating.seats(ordinary, resolution.shown)
      );
      assertSeatingComplete(placed);
      events = projectSeatingEvents(
        Seating.massEvents(resolution.shown, placed), generatedMass, adaptedRequest,
        function (row, seat, semantic) {
          return cliProper(row, seat, semantic);
        },
        function (event) {
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
        throw new Error('Ordinary seating emitted an unsupported semantic event');
      });
    } else {
      events = projectSeatingEvents(
        Seating.unframedEvents(generatedRows), generatedMass, adaptedRequest,
        function (row, seat, semantic) {
          return cliProper(row, seat, semantic);
        },
        function () { throw new Error('unframed Proper sequence carried an Ordinary event'); }
      );
    }
    assertExplicitWitnesses(events, adaptedRequest);
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
        formSelection.rows.map(function (row) { return row.proper; }), adaptedRequest,
        request.options && request.options.ordinary && frame.applicability === 'full' &&
          day.ordinary && !day.ordinary.refused
          ? day.ordinary : null,
        events, ordinaryUnresolved, formSelection.form
      ),
      explicitAbsences: explicitAbsencesFor(branch, lectionary).concat(
        claimLocalCollectAbsences(generatedMass, request, formSelection.form)
      ),
      unresolvedChoices: choices.concat(
        unresolvedCommonSetChoices(input.structure, generatedMass, request),
        alternativeChoices(events), translationChoices(events)
      ),
      ordinaryUnresolved: ordinaryUnresolved
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
