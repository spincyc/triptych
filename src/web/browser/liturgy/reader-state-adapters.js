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

  function semanticSlot(proper) {
    const id = Seating.semanticProperId(proper, false);
    return id ? { state: 'mapped', identity: { id: id } } : {
      state: 'edition-local-unmapped',
      reason: 'generated Proper data has no cross-edition semantic slot identity'
    };
  }

  function qualifiedSemanticId(proper) {
    return Seating.semanticProperId(proper, true);
  }

  /**
   * Resolve only source-authored Mass-form identities. The legacy flat Proper
   * list is retained for old consumers, but it is never a selection mechanism:
   * a multi-form Mass must carry the additive ordered `forms` manifest.
   */
  /**
   * The forms a Day may offer on the formulary's own date.  A form its book
   * says is celebrated on the evening BEFORE (`celebrated.when`, the vigil
   * Mass of a solemnity: Normae universales n. 11 and the Missal's rubric at
   * the vigil itself) is not a coequal choice on the solemnity's date, so the
   * Day entrance leaves it out there; it stays reachable by an explicit form.
   * The Propers entrance is date-independent and offers every form.
   */
  function dayOfferedForms(forms) {
    const own = forms.filter(function (form) {
      return !(form.celebrated && form.celebrated.when === 'evening-before');
    });
    return own.length ? own : forms;
  }

  function properFormSelection(mass, request, dayEntrance) {
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
    const offered = dayEntrance ? dayOfferedForms(forms) : forms;
    if (wanted === null && offered.length === 1 && forms.length > 1) {
      const only = offered[0];
      return {
        id: only.id, rows: rowsById.get(only.id), choice: null, forms: forms,
        form: only, appointedBy: 'celebrated'
      };
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

  // Enumeration has one owner shared with source-path admission. It validates
  // every authored course without choosing a calendar or material year.
  function cycleSelections(proper) {
    return Seating.properCycleSelections(proper);
  }

  function sundayCycleKeys(proper) {
    return cycleSelections(proper).filter(function (one) {
      return one.dimension === 'sunday';
    }).map(function (one) { return one.key; });
  }

  function weekdayCycleKeys(proper) {
    return cycleSelections(proper).filter(function (one) {
      return one.dimension === 'weekday';
    }).map(function (one) { return one.key; });
  }

  // Only copies admitted by the shared source-path owner can carry this
  // override. Reader URL state cannot attest actual-use conditions or rewrite
  // the calendar course. Weak keys keep one reader projection isolated.
  const admittedMaterialCycles = new WeakMap();

  function admittedCycle(proper) {
    if (!admittedMaterialCycles.has(proper)) return undefined;
    const selector = admittedMaterialCycles.get(proper);
    return selector.family === null ? null : {
      key: selector.cycle, family: selector.family,
      dimension: selector.family === 'cycles' ? 'sunday' : 'weekday'
    };
  }

  function dayCycle(proper, lectionary, allowInapplicable) {
    const sunday = sundayCycleKeys(proper);
    const weekday = weekdayCycleKeys(proper);
    if (!sunday.length && !weekday.length) return null;
    if (!lectionary) throw new Error('cycle-bearing Proper has no resolved Lectionary year');
    if (sunday.length && weekday.length) {
      throw new Error('Proper carries both Sunday and weekday Lectionary cycle families');
    }
    if (sunday.length) {
      if (SUNDAY_CYCLE_KEYS.indexOf(lectionary.sunday) < 0) {
        throw new Error('resolved Sunday Lectionary year is not held for this Proper');
      }
      if (sunday.indexOf(lectionary.sunday) < 0) {
        if (allowInapplicable) return false;
        throw new Error('resolved Sunday Lectionary year is not held for this Proper');
      }
      return { key: lectionary.sunday, dimension: 'sunday', family: 'cycles' };
    }
    if (WEEKDAY_CYCLE_KEYS.indexOf(lectionary.weekday) < 0) {
      throw new Error('resolved weekday Lectionary year is not held for this Proper');
    }
    if (weekday.indexOf(lectionary.weekday) < 0) {
      if (allowInapplicable) return false;
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

  function properWitnessId(owner, language, translation) {
    const actual = translation.source_id || translation.source || '';
    const entry = owner.coverage && (owner.coverage.languages || []).find(function (row) {
      return row.lang === language;
    });
    const witness = entry && (entry.witnesses || []).find(function (row) {
      return row.id === actual || (row.aliases || []).indexOf(actual) >= 0;
    });
    return witness ? witness.id : actual || 'project-created';
  }

  function properWitnessMatches(owner, language, requested, translation) {
    const actual = translation.source_id || translation.source || '';
    if (requested === actual || requested === 'project-created' && !actual) return true;
    const entry = owner.coverage && (owner.coverage.languages || []).find(function (row) {
      return row.lang === language;
    });
    return Boolean(entry && (entry.witnesses || []).some(function (row) {
      return (row.id === requested || (row.aliases || []).indexOf(requested) >= 0) &&
        (row.id === actual || (row.aliases || []).indexOf(actual) >= 0);
    }));
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

  function languageBodyAbsence(proper, wanted, selection, request) {
    const owner = selectedOwner(proper, selection);
    const coverage = owner.coverage;
    if (!coverage) return false;
    if (hasOwn(coverage, 'body_languages') &&
        (!Array.isArray(coverage.body_languages) || coverage.body_languages.length !== 1 ||
         coverage.body_languages[0] !== 'en' || coverage.component !== 'proper-body' ||
         !coverage.scripture_component || typeof coverage.scripture_component !== 'object' ||
         Array.isArray(coverage.scripture_component))) {
      throw new Error('language-only body coverage requires English scope and a separate Scripture component');
    }
    if (wanted === 'la' || !coverage.body_languages || !coverage.body_languages.includes(wanted)) return false;
    return (owner.untranslated || []).some(function (row) {
      const target = row && row.target || {};
      if (row.lang !== wanted || target.extent !== 'body') return false;
      function identity(parts) {
        return parts.map(function (one) {
          return encodeURIComponent(String(one)).replace(/[!'()*]/g, function (c) {
            return '%' + c.charCodeAt(0).toString(16).toUpperCase();
          });
        }).join(':');
      }
      const source = identity([request.edition.id, 'proper', target.mass,
        target.form_id, target.proper, target.occurrence]);
      const id = identity([source, selection ? selection.family : 'all',
        selection ? selection.key : 'all']);
      return id === coverage.target_id && target.proper === proper.name &&
        target.cycle === (selection ? selection.key : 'all');
    });
  }

  function materialForCycleValue(proper, request, structure, selection) {
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
    const owner = selectedOwner(proper, selection);
    const wanted = request.languages && request.languages.orations || 'la';
    const hasLanguageBody = languageBodyAbsence(proper, wanted, selection, request);
    if (references.length && (owner.source || proper.source) !== 'mixed' && !hasLanguageBody) {
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
      const ownerHasBodyState = cycleText || ownerTranslations.length ||
        (owner.unavailable_translations || []).length || (owner.untranslated || []).length ||
        owner.latin || owner.text_status;
      const rawTranslations = owner !== proper && ownerHasBodyState
        ? ownerTranslations : parentTranslations;
      const grouped = new Map();
      const conflicts = new Set();
      rawTranslations.forEach(function (translation) {
        const id = properWitnessId(owner, wanted, translation);
        if (grouped.has(id) && grouped.get(id).text !== translation.text) conflicts.add(id);
        else grouped.set(id, translation);
      });
      const translations = Array.from(grouped.values());
      const typed = typedUnavailableFor(proper, wanted, selection);
      // A public body has its own publication basis. A redacted absence row
      // for another witness cannot withdraw that body or identify its witness.
      if (typed && !translations.length) return Object.assign(typed, {
        cycle: typed.cycle || cycle,
        cycles: cycleRows,
        weekdayCycles: weekdayCycleRows,
        cycleDimension: selection ? selection.dimension : null
      });
      if (translations.some(function (translation) {
        return conflicts.has(properWitnessId(owner, wanted, translation)) &&
          (!witness || properWitnessMatches(owner, wanted, witness, translation));
      })) return {
        kind: 'composed', language: wanted, cycle: cycle, cycles: cycleRows,
        weekdayCycles: weekdayCycleRows,
        cycleDimension: selection ? selection.dimension : null,
        sourceId: null, rights: null, missing: true, availability: 'unavailable',
        held: false, text: null, reason: 'conflicting-witness'
      };
      const translation = witness
        ? translations.find(function (one) {
            return properWitnessMatches(owner, wanted, witness, one);
          })
        : (translations.length === 1 ? translations[0] : null);
      if (translation) {
        return {
          kind: 'composed', language: wanted, cycle: cycle, cycles: cycleRows,
          weekdayCycles: weekdayCycleRows,
          cycleDimension: selection ? selection.dimension : null,
          sourceId: witness || translation.source_id || translation.source || null,
          rights: translation.rights || null, missing: false,
          availability: 'held', text: translation.text
        };
      }
      if (translations.length > 1 && !witness) {
        const witnessIds = Array.from(new Set(translations.map(function (one) {
          return properWitnessId(owner, wanted, one);
        })));
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
        held: false, text: null, reason: witness ? 'absent-in-witness' : 'translation-missing'
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

  function materialForCycle(proper, request, structure, selection) {
    const material = materialForCycleValue(proper, request, structure, selection);
    const owner = selectedOwner(proper, selection);
    const wanted = request.languages && request.languages.orations || 'la';
    if ((owner.source || proper.source) !== 'mixed' &&
        !languageBodyAbsence(proper, wanted, selection, request)) return material;
    const citations = (proper.citations || []).concat(
      owner === proper ? [] : owner.citations || []
    );
    // Scripture references identify components of this exact mixed body. They
    // cannot supply its composed portion or make an unavailable witness held.
    material.scriptureComponents = {
      bible: request.bible && request.bible.id || null,
      numbering: request.bible && request.bible.numbering || null,
      references: citations.map(function (one) { return one.ref; }).filter(Boolean),
      unresolved: citations.filter(function (one) { return one.unresolved; }).map(function (one) {
        return { reference: one.ref, reason: one.unresolved };
      })
    };
    return material;
  }

  function selectedMaterial(proper, request, structure, cycleMode) {
    const selections = cycleSelections(proper);
    const admitted = admittedCycle(proper);
    if (admitted !== undefined) return materialForCycle(proper, request, structure, admitted);
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

  function ordinaryTranslationApplicability(scope, context) {
    const keys = scope && typeof scope === 'object' && !Array.isArray(scope) ? Object.keys(scope).sort() : [];
    const id = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
    if (keys.join(',') !== 'basis,calendar,formularies,kind' || scope.kind !== 'formulary' ||
        typeof scope.calendar !== 'string' || !id.test(scope.calendar) ||
        typeof scope.basis !== 'string' || !scope.basis.trim() ||
        !Array.isArray(scope.formularies) || !scope.formularies.length ||
        scope.formularies.some(function (one) { return typeof one !== 'string' || !id.test(one); }) ||
        new Set(scope.formularies).size !== scope.formularies.length) {
      throw new Error('malformed Ordinary translation applicability');
    }
    const fields = context && typeof context === 'object' && !Array.isArray(context) ? Object.keys(context).sort() : [];
    if (fields.join(',') !== 'calendar,formulary' ||
        typeof context.calendar !== 'string' || !id.test(context.calendar) ||
        typeof context.formulary !== 'string' || !id.test(context.formulary)) return 'unresolved';
    return context.calendar === scope.calendar && scope.formularies.indexOf(context.formulary) >= 0
      ? 'applicable' : 'inapplicable';
  }

  function ordinaryTranslation(element, ordinary, language, witness, context) {
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
      if (Object.prototype.hasOwnProperty.call(found, 'applicability')) {
        const state = ordinaryTranslationApplicability(found.applicability, context);
        const applicability = { state: state, scope: found.applicability,
          context: state === 'unresolved' ? null : { calendar: context.calendar, formulary: context.formulary } };
        if (state !== 'applicable') return {
          kind: 'ordinary-text', language: language, sourceId: null, rights: null,
          absenceKey: null, availability: 'unavailable', text: null,
          reason: 'applicability-' + state, unavailableState: state === 'unresolved' ? 'unresolved' : 'unavailable',
          applicability: applicability
        };
        return { kind: 'ordinary-text', language: language,
          sourceId: found.source_id || found.source || null, rights: found.rights || null,
          relation: found.relation || null, collation: found.collation || null,
          absenceKey: null, availability: 'held', text: found.text, applicability: applicability };
      }
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

  /**
   * The formulary's own printed Ordinary appointments, for the seating's
   * appointment context.  A form's rows replace the Mass's by variable.  A
   * feria that BORROWS a formulary takes none of them: the proper
   * Communicantes is said "suo loco in propriis Missis" (RGMR 501) and the
   * Epiphany form "in festo tantum", so the borrowed day falls through to the
   * dated spans and defaults the Ordinary declares.
   */
  function formularyAppointments(mass, form, winner) {
    const borrowed = Boolean(winner && winner.formulary &&
      winner.formulary.kind === 'borrowed' && winner.formulary.key === mass.key);
    if (borrowed) return {};
    const held = {};
    [mass && mass.ordinary_appointments, form && form.ordinary_appointments].forEach(
      function (rows) {
        Object.keys(rows || {}).forEach(function (variable) {
          const row = rows[variable];
          if (row && typeof row.option === 'string') held[variable] = row.option;
        });
      });
    return held;
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
        const disposition = row.proper.ordinary_disposition;
        const id = disposition && disposition.anchor && disposition.seat || qualifiedSemanticId(row.proper);
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

  function properChoiceCycleApplies(proper, request) {
    if (request.entrance === 'day') {
      return dayCycle(proper, request.lectionary, true) !== false;
    }
    const selections = cycleSelections(proper);
    return !hasOwn(request, 'cycle') || request.cycle === null ||
      !selections.length || Boolean(explicitCycleSelection(proper, request.cycle));
  }

  function projectProperChoice(event, mass, request, projectMember) {
    const id = 'proper-choice/' + request.edition.id + '/' + mass.key + '/' +
      event.formId + '/' + event.group;
    const seat = projectedSeat(event.seat, event.placement, mass, request);
    const semantic = sharedChoiceSemanticSlot(event);
    const authored = event.options || [];
    if (authored.length < 2 || new Set(authored.map(function (one) { return one.id; })).size !== authored.length) {
      throw new Error('alternative Proper choice must carry distinct options');
    }
    const options = authored.map(function (option) {
      const rows = option.rows || [];
      // Check every member before dropping a whole inapplicable source option.
      const applicable = rows.map(function (row) {
        return properChoiceCycleApplies(row.proper, request);
      });
      if (!rows.length) throw new Error('alternative Proper option must conserve distinct source events');
      if (!applicable.every(Boolean)) return null;
      const events = rows.map(function (row) { return projectMember(row, seat, semantic); });
      if (new Set(events.map(function (one) { return one.id; })).size !== events.length) {
        throw new Error('alternative Proper option must conserve distinct source events');
      }
      return { id: option.id, events: events };
    }).filter(Boolean);
    if (!options.length) throw new Error('alternative Proper choice has no option for the selected cycle');
    const selection = event.selection || {state: 'required', option: null};
    if (selection.state === 'selected' && !options.some(function (option) {
      return option.id === selection.option;
    })) throw new Error(request.alternative
      ? 'explicit Propers alternative is not held by the exact selected formulary and form'
      : 'explicit Proper choice is not applicable to the selected cycle');
    if (options.length === 1) {
      const option = options[0];
      return option.events.map(function (member) {
        return Object.assign({}, member, { sourceHooks: member.sourceHooks.concat([
          { kind: 'proper-choice-option', id: id + '/' + option.id }
        ]) });
      });
    }
    if (selection.state === 'selected') {
      const chosen = options.find(function (option) { return option.id === selection.option; });
      chosen.events = chosen.events.map(function (member) {
        return Object.assign({}, member, {sourceHooks: member.sourceHooks.concat([
          {kind: 'proper-choice-option', id: id + '/' + chosen.id}
        ])});
      });
    }
    const memberEvents = options.reduce(function (all, option) {
      return all.concat(option.events);
    }, []);
    return [{
      id: id, kind: 'proper-choice', group: event.group,
      selection: selection,
      seat: seat, options: options, sourceHooks: uniqueSourceHooks(memberEvents),
      choiceBasis: event.basis
    }];
  }

  function projectSeatingEvents(events, mass, request, projectMember, projectOrdinary) {
    return (events || []).flatMap(function (event) {
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

  function prepareAppointments(mass, properRows, request, structure, dayContext) {
    // Validate every authored body state before applicability can suppress an
    // inactive candidate; only the later active pass contributes coverage.
    properRows.forEach(function (row) {
      const proper = row.proper;
      const selections = cycleSelections(proper);
      properBodyStatus(proper);
      selections.forEach(function (selection) { properBodyStatus(selectedOwner(proper, selection)); });
      // Path-qualified rows are checked against their exact source member
      // selector by Seating. Other rows retain the existing calendar guard.
      if (!proper.source_path_relation && request.entrance === 'day') {
        dayCycle(proper, request.lectionary,
          proper.ordinary_disposition && proper.ordinary_disposition.kind === 'alternative');
      }
    });
    const choices = {};
    const prefix = 'proper-choice/' + request.edition.id + '/' + mass.key + '/';
    Object.keys(request.properChoices || {}).forEach(function (id) {
      if (!id.startsWith(prefix) || id.slice(prefix.length).split('/').length !== 2) {
        throw new Error('explicit Proper choice belongs to another edition, formulary or form');
      }
      choices[id.slice(prefix.length)] = request.properChoices[id];
    });
    if (request.alternative) {
      const id = request.alternative.id;
      const parts = id.startsWith(prefix) ? id.slice(prefix.length).split('/') : [];
      if (parts.length !== 3) throw new Error('explicit Propers alternative is not held by the exact selected formulary and form');
      const group = parts.slice(0, 2).join('/');
      if (hasOwn(choices, group)) throw new Error('duplicate explicit Proper choice declaration');
      choices[group] = parts[2];
    }
    const prepared = Seating.prepareProperAppointments(properRows, {
      calendar: request.edition.id, entrance: request.entrance,
      mass: mass.key,
      formId: properRows.length ? properRows[0].proper.form_id || 'main' : request.form || 'main',
      sourcePaths: hasOwn(mass, 'proper_source_paths') ? mass.proper_source_paths : [],
      calendarCycles: request.lectionary ? {
        sunday: request.lectionary.sunday,
        weekday: request.lectionary.weekday
      } : {
        sunday: SUNDAY_CYCLE_KEYS.indexOf(request.cycle) >= 0 ? request.cycle : null,
        weekday: WEEKDAY_CYCLE_KEYS.indexOf(request.cycle) >= 0 ? request.cycle : null
      },
      conditionFacts: dayContext ? dayContext.conditionFacts : undefined,
      date: dayContext && dayContext.date || null,
      season: dayContext && dayContext.season || null,
      usageContext: dayContext && dayContext.usageContext,
      facts: structure.proper_appointment_facts || {}, choices: choices
    });
    prepared.rows.forEach(function (row) {
      if (hasOwn(row, 'materialCycle')) admittedMaterialCycles.set(row.proper, row.materialCycle);
    });
    prepared.activeRows = prepared.rows.filter(function (row) {
      const disposition = row.proper.ordinary_disposition;
      if (!disposition || disposition.kind !== 'alternative') return true;
      const selection = prepared.selections[(row.proper.form_id || 'main') + '/' + disposition.group];
      return selection && selection.state === 'selected' && selection.option === disposition.option;
    });
    return prepared;
  }

  function appointmentChoices(prepared, mass, request, structure) {
    return (prepared.unresolved || []).map(function (condition) {
      const fact = structure.proper_appointment_facts[condition.when.fact];
      return Contract.unresolvedChoice(
        'proper-condition/' + request.edition.id + '/' + mass.key + '/' +
          condition.appointment.form_id + '/' + condition.group,
        condition.basis,
        fact.values.map(function (value) {
          return {id: value, identity: {id: condition.when.fact + '/' + value}};
        }),
        [{kind: 'proper-appointment', id: JSON.stringify(condition.appointment)}]
      );
    });
  }

  function sourcePathChoices(prepared, mass, request, events) {
    const prefix = 'proper-choice/' + request.edition.id + '/' + mass.key + '/';
    const eventIds = new Set();
    function collect(items) {
      (items || []).forEach(function (event) {
        eventIds.add(event.id);
        if (event.kind === 'proper-choice') {
          (event.options || []).forEach(function (option) { collect(option.events); });
        }
      });
    }
    collect(events);
    return (mass.proper_source_paths || []).filter(function (relation) {
      return hasOwn(prepared.sourcePathSelections, relation.form_id + '/' + relation.id);
    }).map(function (relation) {
      const key = relation.form_id + '/' + relation.id;
      const selection = prepared.sourcePathSelections[key];
      const member = prepared.rows.find(function (row) {
        return row.materialCycle && relation.paths.some(function (path) {
          return path.id === selection.option && path.members.some(function (one) {
            const actual = row.proper.appointment_identity || {};
            return ['mass', 'form_id', 'proper', 'occurrence'].every(function (key) {
              return one.appointment[key] === actual[key];
            });
          });
        });
      });
      const focus = member && properEventId(request.edition.id, mass.key, member.sourceIndex);
      const existing = focus && eventIds.has(focus) ? focus : null;
      const groups = new Set();
      const paths = relation.paths.map(function (path) {
        const tuple = {};
        Object.keys(path.choices).forEach(function (group) {
          const id = prefix + relation.form_id + '/' + group;
          tuple[id] = path.choices[group]; groups.add(id);
        });
        return {id: path.id, standing: path.standing, choices: tuple,
          condition: path.when || null,
          applicability: prepared.sourcePathAvailability[key][path.id]};
      });
      return {id: prefix + key, basis: relation.basis, selection: selection,
        ownedChoiceIds: Array.from(groups), beforeEventId: existing, focusEventId: existing,
        paths: paths};
    });
  }

  function sourcePathUnresolvedChoices(prepared, mass, request) {
    const prefix = 'proper-choice/' + request.edition.id + '/' + mass.key + '/';
    return (prepared.sourcePathUnresolved || []).map(function (unresolved) {
      const relation = mass.proper_source_paths.find(function (one) {
        return one.id === unresolved.relation && one.form_id === unresolved.form_id;
      });
      const id = prefix + relation.form_id + '/' + relation.id;
      return Contract.unresolvedChoice(id, relation.basis, relation.paths.map(function (path) {
        return {id: path.id, identity: {id: path.id}};
      }), [{kind: 'proper-source-path', id: id}]);
    });
  }

  function seatedEvents(
    mass, properRows, request, structure, ordinary, cycleMode, predicateFacts, dayContext
  ) {
    const prepared = prepareAppointments(mass, properRows, request, structure, dayContext);
    properRows = prepared.rows;
    if (!ordinary) {
      const unframed = Seating.unframedEvents(
        properRows, function (proper) { return proper && proper.name === 'Placeholder'; },
        prepared.selections
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
        ordinaryUnresolved: [], prepared: prepared
      };
    }
    const resolution = ordinaryElements(
      ordinary, request, properRows.map(function (row) { return row.proper; }),
      predicateFacts
    );
    const placed = Seating.seatPropers(
      properRows,
      Seating.seats(ordinary, resolution.shown),
      function (proper) { return proper && proper.name === 'Placeholder'; },
      prepared.selections
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
          request.languages && request.languages.ordinaryWitness || null,
          { calendar: request.edition.id, formulary: mass.key }
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
    return { events: events, ordinaryUnresolved: resolution.unresolved, prepared: prepared };
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
      const admitted = admittedCycle(proper);
      if (admitted !== undefined) {
        activeSelections = admitted ? [admitted] : [];
      } else if (request.entrance === 'day') {
        const selected = dayCycle(proper, request.lectionary,
          proper.ordinary_disposition && proper.ordinary_disposition.kind === 'alternative');
        includeProper = selected !== false;
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

  function orationExecutionAbsences(events) {
    const out = [];
    function visit(event) {
      if (event.kind === 'proper-choice') {
        (event.options || []).filter(function (option) {
          return event.selection.state === 'selected' && event.selection.option === option.id;
        }).forEach(function (option) { (option.events || []).forEach(visit); });
      }
      const reasons = new Set();
      (event.orationGroups || []).forEach(function (group) {
        (group.execution && group.execution.unresolved || []).forEach(function (reason) {
          if (reasons.has(reason)) return;
          reasons.add(reason);
          out.push({kind: 'explicit-semantic-absence', scope: 'oration-execution',
            repositoryTerm: 'unresolved', event: event.id, reason: reason,
            sourceHooks: [{kind: 'locus', id: group.execution.basis}]});
        });
      });
    }
    (events || []).forEach(visit);
    return out;
  }

  function coverageFor(
    structure, mass, propers, request, ordinary, events, ordinaryUnresolved, selectedForm,
    appointmentUnresolved
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
    const pendingAppointments = alternativeChoices(events).length + (appointmentUnresolved || []).length;
    if (pendingAppointments) claimReasons.push({
      kind: 'unresolved-choice', count: pendingAppointments,
      repositoryTerm: 'proper-appointment'
    });
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
    const orationAbsences = orationExecutionAbsences(events);
    if (orationAbsences.length) rows.push(Contract.coverage('unsupported', 'oration-execution', null,
      orationAbsences.map(function (absence) {return {kind: 'unsupported-object', basis: absence.reason, event: absence.event};})));
    return rows;
  }

  function branchFor(derived, request) {
    const branches = derived.options || [];
    const territory = territoryId(request);
    if (branches.length === 1 && branches[0].option === territory) {
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
    // The sole ferial reading course can be read while its oration owner stays
    // unresolved. Retain that standing; this does not appoint a Mass or prayer.
    if (rows.length === 1 && rows[0].state === 'unresolved' &&
        branch.settled === false && branch.winner === null &&
        !(branch.massChoices || []).length && (branch.unsettled || []).length &&
        branch.unsettled.every(function (one) { return one.scope === 'oration-owner'; })) {
      return rows[0];
    }
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
      return event && event.kind === 'proper-choice' && event.selection.state === 'required';
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

  function assertExplicitWitnesses(events, request, structure) {
    const languages = request.languages || {};
    if (languages.translationWitness) {
      // A witness may supply a reachable source option which the reader has
      // deliberately left unresolved. Validate that held offer without choosing
      // an option or changing the active text/coverage projection. An explicit
      // option continues to admit only its selected members.
      const witnessEvents = (events || []).flatMap(function (event) {
        return event && event.kind === 'proper-choice' && event.selection.state === 'required'
          ? (event.options || []).flatMap(function (option) { return option.events || []; })
          : [event];
      });
      const held = selectedRows(witnessEvents).some(function (row) {
        if (row.event.nameExecution && row.event.nameExecution.state === 'name-bound' && row.event.nameExecution.relation.source_aliases.indexOf(languages.translationWitness) >= 0) return true;
        if (row.event.executionSource && row.event.executionSource.source.source_aliases.indexOf(languages.translationWitness) >= 0) return true;
        if (row.selected.sourceId === languages.translationWitness) return true;
        // Citation-led units and conflicting readings retain the authored
        // witness validation without selecting a conflicting body.
        if (row.selected.kind !== 'scripture' && row.selected.reason !== 'conflicting-witness') return false;
        const hook = (row.event.sourceHooks || []).find(function (one) { return one.kind === 'proper-structure'; });
        if (!hook || !structure) return false;
        const mass = (structure.masses || []).find(function (one) {
          return hook.id.slice(0, hook.id.lastIndexOf('/')) === structure.calendar + '/' + one.key;
        });
        const proper = mass && mass.propers[Number(hook.id.slice(hook.id.lastIndexOf('/') + 1)) - 1];
        if (!proper) return false;
        const selection = row.selected.cycle ? explicitCycleSelection(proper, row.selected.cycle) : null;
        const owner = selectedOwner(proper, selection);
        return (owner.translations || []).some(function (translation) {
          return translation.lang === languages.orations && translation.text &&
            properWitnessMatches(owner, languages.orations, languages.translationWitness, translation);
        });
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
    function visit(event) {
      if (event && event.kind === 'proper-choice') {
        (event.options || []).filter(function (option) {
          return event.selection.state === 'selected' && event.selection.option === option.id;
        }).forEach(function (option) { (option.events || []).forEach(visit); });
      } else {
        properEvents.push(event);
        (event.orationGroups || []).forEach(function (group) {
          (group.members || []).forEach(function (member) { if (member.id !== event.id) visit(member); });
        });
      }
    }
    (events || []).forEach(visit);
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
    const formSelection = properFormSelection(mass, request, true);
    if (formSelection.choice) {
      if (request.properChoices) throw new Error('explicit Proper choices require an exact selected Mass form');
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
        season: derived.season, nature: branch.winner && branch.winner.nature,
        date: derived.date,
        anchors: derived.liturgicalYear && derived.liturgicalYear.anchors || null,
        appointments: formularyAppointments(mass, formSelection.form, branch.winner)
      }), {date: derived.date, season: derived.season, conditionFacts: input.conditionFacts, usageContext: {
        calendar: derived.calendar, entrance: request.entrance, branch: branch, readable: readable,
        mass: mass, formId: formSelection.id || 'main'
      }}
    );
    let events = withOrationGroups(
      seated.events, branch, readable, mass, adaptedRequest, input.structure, null, {season: derived.season}
    );
    events = withFiniteNameExecution(events, branch, readable, mass, adaptedRequest, input.structure, input.nameExecutionUse || null);
    assertExplicitWitnesses(events, adaptedRequest, input.structure);
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
      ...(nameExecutionCoverage(events).occurrences ? {nameExecutionCoverage: nameExecutionCoverage(events)} : {}),
      ...(executionSourceCoverage(events).petitions ? {executionSourceCoverage: executionSourceCoverage(events)} : {}),
      ...(hasOwn(seated.prepared, 'usage') ? {properAppointmentUsage: seated.prepared.usage} : {}),
      sourcePathChoices: sourcePathChoices(seated.prepared, mass, request, events),
      coverage: coverageFor(
        input.structure, mass, seated.prepared.activeRows.map(function (row) { return row.proper; }),
        adaptedRequest, ordinary, events, seated.ordinaryUnresolved, formSelection.form, seated.prepared.unresolved.concat(seated.prepared.sourcePathUnresolved)
      ),
      explicitAbsences: explicitAbsencesFor(branch, lectionary).concat(orationExecutionAbsences(events),
        claimLocalCollectAbsences(mass, request, formSelection.form)
      ),
      unresolvedChoices: choices.concat(
        unresolvedCommonSetChoices(input.structure, mass, request),
        appointmentChoices(seated.prepared, mass, request, input.structure),
        sourcePathUnresolvedChoices(seated.prepared, mass, request),
        alternativeChoices(events), translationChoices(events)
      ),
      ordinaryUnresolved: seated.ordinaryUnresolved
    };
  }

  /**
   * Keep a counted oration as one semantic slot while retaining both exact
   * source owners. The frame seats that slot once; its ordered members follow
   * within it. A selected raw/displaced formulary never acquires this Day use.
   */
  // Finite source/execution joins. Whole historical English remains immutable;
  // the applied planner, never a date-only shortcut, supplies the two owners.
  const EXECUTION_METHOD = 'roman-1962-rg110-six-source-execution-20261026';
  const EXECUTION_PUBLIC_PINS = {"[\"cathedrae-s-petri-apostoli\",\"main\",\"Collect\",\"all\",1]":"e1fc8c67f2269f58ed6ef2c3d061644eb33f47445695f41445c76dfcd8ce56ea","[\"cathedrae-s-petri-apostoli\",\"main\",\"Postcommunion\",\"all\",1]":"600592c94ff0e7c21dda833935c9c57b4a70ea06c54998256ea146e2ec179263","[\"cathedrae-s-petri-apostoli\",\"main\",\"Secret\",\"all\",1]":"a7047d1593aaae79225319ca5ab2371eb888774e64538e5e96537eda3d74e2d7","[\"commemoratione-s-pauli-apostoli\",\"main\",\"Collect\",\"all\",1]":"3c75b67e589114900c586eb99de8c7fd916bc71453ae30f4c26b48e3b0f218a4","[\"commemoratione-s-pauli-apostoli\",\"main\",\"Postcommunion\",\"all\",1]":"ccb29c2fb66eecc9794db9dd316d73f74556848ab20ca6dc0619d5fe5c1c9d53","[\"commemoratione-s-pauli-apostoli\",\"main\",\"Secret\",\"all\",1]":"df93a225d7903bf7488026484e23edd43cccdce1ccb6bdbe8fde488eaf14ed6d"};
  function executionCanonical(value) {
    if (Array.isArray(value)) return '[' + value.map(executionCanonical).join(',') + ']';
    if (value && typeof value === 'object') return '{' + Object.keys(value).sort().map(function (key) {
      return JSON.stringify(key) + ':' + executionCanonical(value[key]);
    }).join(',') + '}';
    return JSON.stringify(value);
  }
  function executionSha(text) {
    const bytes = unescape(encodeURIComponent(text));
    const words = [], constants = [], initial = [];
    let prime = 2;
    while (constants.length < 64) {
      let isPrime = true;
      for (let divisor = 2; divisor * divisor <= prime; divisor++) if (prime % divisor === 0) { isPrime = false; break; }
      if (isPrime) {
        if (initial.length < 8) initial.push((Math.sqrt(prime) % 1 * 4294967296) | 0);
        constants.push((Math.cbrt(prime) % 1 * 4294967296) | 0);
      }
      prime++;
    }
    for (let index = 0; index < bytes.length; index++) words[index >> 2] = (words[index >> 2] || 0) | bytes.charCodeAt(index) << (24 - index % 4 * 8);
    words[bytes.length >> 2] = (words[bytes.length >> 2] || 0) | 128 << (24 - bytes.length % 4 * 8);
    words[(((bytes.length + 8) >> 6) + 1) * 16 - 1] = bytes.length * 8;
    const rotate = function (value, count) { return value >>> count | value << (32 - count); };
    let hash = initial.slice();
    for (let start = 0; start < words.length; start += 16) {
      const schedule = [], work = hash.slice();
      for (let index = 0; index < 64; index++) {
        if (index < 16) schedule[index] = words[start + index] | 0;
        else {
          const a = schedule[index - 15], b = schedule[index - 2];
          schedule[index] = (schedule[index - 16] + (rotate(a, 7) ^ rotate(a, 18) ^ a >>> 3) + schedule[index - 7] + (rotate(b, 17) ^ rotate(b, 19) ^ b >>> 10)) | 0;
        }
        const a = work[0], b = work[1], c = work[2], d = work[3], e = work[4], f = work[5], g = work[6], h = work[7];
        const t1 = (h + (rotate(e, 6) ^ rotate(e, 11) ^ rotate(e, 25)) + (e & f ^ ~e & g) + constants[index] + schedule[index]) | 0;
        const t2 = ((rotate(a, 2) ^ rotate(a, 13) ^ rotate(a, 22)) + (a & b ^ a & c ^ b & c)) | 0;
        work.splice(0, 8, (t1 + t2) | 0, a, b, c, (d + t1) | 0, e, f, g);
      }
      hash = hash.map(function (value, index) { return (value + work[index]) | 0; });
    }
    return hash.map(function (value) { return (value >>> 0).toString(16).padStart(8, '0'); }).join('');
  }
  function validateExecutionSource(source, proper, group, request, structure) {
    const key = source && JSON.stringify(source.target);
    if (!source || source.schema !== 'triptych-oration-execution-source/v1' || source.method_id !== EXECUTION_METHOD ||
        executionSha(executionCanonical(source)) !== EXECUTION_PUBLIC_PINS[key]) throw new Error('unrecognized or changed execution source');
    if (request.edition.id !== 'roman-1962' || request.languages.orations !== 'en' || source.lang !== 'en' ||
        source.target[1] !== 'main' || source.target[3] !== 'all' || source.target[4] !== 1 ||
        String(request.civilDate).slice(5) !== source.fixed_date || source.scope !== 'dated-mass-of-office' ||
        group.kind !== 'inseparable' || group.count !== 1 || group.members.length !== 2 ||
        group.members[0].key !== source.target[0] || group.members[1].key !== source.companion.target[0] ||
        group.slot !== source.target[2]) throw new Error('execution source outside exact applied RG110 context');
    if (executionSha(proper.text || '') !== source.target_latin_sha256 ||
        executionSha(group.members[1].proper.text || '') !== source.companion.latin_sha256) throw new Error('execution source current Latin owner changed');
    if (source.offset_units !== 'utf16' || source.ranges.length !== 3) throw new Error('execution source range units differ');
    let end = 0;
    source.ranges.forEach(function (range, index) {
      if (range.kind !== ['petition', 'separator', 'printed-conclusion-cue'][index] || range.start !== end ||
          !Number.isInteger(range.end) || range.end < end || range.end > source.source_text.length ||
          (range.end > 0 && range.end < source.source_text.length && /[\uD800-\uDBFF]/.test(source.source_text[range.end - 1]) && /[\uDC00-\uDFFF]/.test(source.source_text[range.end]))) throw new Error('execution source range splits source characters');
      end = range.end;
    });
    if (end !== source.source_text.length || executionSha(source.source_text) !== source.source_sha256) throw new Error('execution source full text changed');
    const companion = structure.masses.find(function (one) { return one.key === source.companion.target[0]; });
    const matches = (companion && companion.propers || []).filter(function (one) { return one.name === source.target[2] && one.form_id === 'main'; });
    if (matches.length !== 1 || !(matches[0].translations || []).some(function (translation) {
      return translation.lang === 'en' && translation.source_id === source.companion.source_id && translation.text === source.companion.source_text;
    })) throw new Error('execution companion literal English owner changed');
  }
  function executionSourceCoverage(events) {
    const seen = new Map();
    function visit(event) {
      if (event.executionSource) seen.set(event.id, event.executionSource);
      (event.orationGroups || []).forEach(function (group) { group.members.forEach(visit); });
      if (event.kind === 'proper-choice') (event.options || []).filter(function (option) {
        return event.selection.state === 'selected' && option.id === event.selection.option;
      }).forEach(function (option) { (option.events || []).forEach(visit); });
    }
    (events || []).forEach(visit);
    return {schema: 'triptych-selected-execution-coverage/v1', count_basis: 'distinct-appointed-source-targets',
      petitions: seen.size, unresolved: Array.from(seen.values()).filter(function (one) { return one.state === 'unresolved'; }).length,
      whole_body_translations_added: 0, complete_English_claim: false};
  }

  function withOrationExecutionSource(projected, proper, group, request, structure) {
    if (!(proper.execution_sources || []).length || request.languages.orations !== 'en') return projected;
    if (proper.execution_sources.length !== 1) throw new Error('execution source conflict requires explicit settlement');
    const source = proper.execution_sources[0];
    validateExecutionSource(source, proper, group, request, structure);
    const wanted = request.languages.translationWitness;
    if (wanted && source.source_aliases.indexOf(wanted) < 0) return projected;
    const unresolved = [];
    if (source.companion.cue_state !== 'printed') unresolved.push('companion-English-conclusion-unbound');
    if (source.companion.unbound_name || /\bN\./.test(source.source_text)) unresolved.push('source-name-placeholder-unbound');
    if (wanted && wanted !== source.companion.source_id) unresolved.push('companion-English-unavailable-in-selected-witness');
    if (group.conclusion_final === false) unresolved.push('later-shared-conclusion-unbound');
    return Object.assign({}, projected, {
      sourceHooks: uniqueSourceHooks([projected]).concat([
        {kind: 'publication', id: source.provenance.publication_passage_id},
        {kind: 'publication', id: source.provenance.companion_publication_passage_id}
      ]),
      executionSource: {schema: 'triptych-selected-execution-source/v1', source: source,
        selected_witness: wanted || source.source_id,
        state: unresolved.length ? 'unresolved' : 'petition-and-printed-companion-cue', unresolved: unresolved}
    });
  }

  const NAME_METHOD = 'roman-1962-finite-name-two-20261026';
  const NAME_PUBLIC_PINS = {"[\"s-antonii-abbatis\",\"main\",\"Collect\",\"all\",1]":"5aa4eea80cc659402cf279a6628844a0c8b548331d55fc0b66881414f84a1549","[\"s-patricii-episcopi-confessoris\",\"main\",\"Postcommunion\",\"all\",1]":"4cd09387c699424aec180b9c942a31e10bd2ce6b3d0ce75146e6aab8c8668a74"};
  function withFiniteNameExecution(events, branch, readable, mass, request, structure, useContext) {
    const seen = new Set();
    function apply(event, proper, ownerKey, group) {
      const sources = proper.name_execution_sources || [];
      if (!sources.length || request.languages.orations !== 'en') return event;
      if (sources.length !== 1) throw new Error('finite name source requires one settled relation');
      const source = sources[0], target = source.target;
      if (source.schema !== 'triptych-finite-name-execution-source/v1' || source.method_id !== NAME_METHOD ||
          executionSha(executionCanonical(source)) !== NAME_PUBLIC_PINS[JSON.stringify(target)]) throw new Error('changed or unknown finite name source');
      if (target[0] !== ownerKey || target[1] !== proper.form_id || target[2] !== proper.name || target[3] !== 'all' || target[4] !== 1 ||
          executionSha(proper.text || '') !== source.canonical_latin_sha256) throw new Error('finite name current recipient/form/body differs');
      const referral = proper.taken_from === undefined ? null : proper.taken_from;
      if (executionCanonical(referral) !== executionCanonical(source.recipient_source_relation)) throw new Error('finite name exact recipient/Common referral differs');
      const recipient = structure.masses.find(function (one) { return one.key === ownerKey; });
      if (!recipient || recipient.propers.filter(function (one) { return one.form_id === target[1] && one.name === target[2]; }).length !== 1) throw new Error('finite name recipient slot/occurrence is ambiguous');
      const common = structure.masses.find(function (one) { return one.key === source.terminal_common[0]; });
      const donors = (common && common.propers || []).filter(function (one) {
        return one.form_id === source.terminal_common[1] && one.name === source.terminal_common[2];
      });
      if (donors.length !== 1 || executionSha(donors[0].text || '') !== source.common_latin_sha256 ||
          !(donors[0].translations || []).some(function (one) { return one.lang === 'en' && one.source_id === source.source_id && one.text === source.template.text; })) throw new Error('finite name terminal Common/template differs');
      const wanted = request.languages.translationWitness;
      if (wanted && source.source_aliases.indexOf(wanted) < 0) return event;
      const errors = [], hold = function (reason) { if (errors.indexOf(reason) < 0) errors.push(reason); };
      if (request.edition.id !== 'roman-1962' || request.civilDate !== source.accepted_date) hold('exact-dated-occurrence-not-adopted');
      if (!branch.settled || readable.state !== 'said' || !branch.oration_execution || branch.oration_execution.scope !== 'dated-mass-of-office') hold('accepted-Mass-of-Office-use-unbound');
      const series = branch.orations && (branch.orations.all || branch.orations.low_mass) || [];
      if (source.required_role === 'own-Mass-of-Office') {
        if (useContext) hold('unexpected-use-context-for-own-Mass-of-Office');
        if (group || mass.key !== ownerKey || !branch.winner || branch.winner.key !== ownerKey ||
            !series[0] || series[0].position !== 1 || series[0].source_key !== ownerKey) hold('exact-own-Mass-of-Office-not-selected');
      } else {
        const unit = series.find(function (one) { return one.source_key === ownerKey; });
        const loser = (branch.losers || []).find(function (one) {
          return (one.id === ownerKey || one.key === ownerKey) && one.disposition === 'commemorated' && one.kind === 'ordinary';
        });
        if (!group || group.kind !== 'commemoration' || group.members.length !== 1 || group.members[0].id !== event.id ||
            !unit || unit.position !== group.position || unit.position < 2 || !loser) hold('accepted-ordinary-commemoration-not-applied');
        if (!useContext) hold('explicit-Mass-form-and-conventual-context-unbound');
        else {
          const keys = Object.keys(useContext).sort().join('|');
          if (keys !== 'calendar|conventual|date|mass_form|recipient|role|schema|selected_oration|source_rule' ||
              useContext.schema !== 'triptych-finite-name-use-context/v1' || useContext.calendar !== 'roman-1962' ||
              useContext.date !== source.accepted_date || JSON.stringify(useContext.recipient) !== JSON.stringify(target) ||
              useContext.role !== 'ordinary-commemoration' || ['low', 'sung'].indexOf(useContext.mass_form) < 0 || typeof useContext.conventual !== 'boolean' ||
              executionCanonical(useContext.source_rule) !== executionCanonical(source.applicability_rule) ||
              !unit || executionCanonical(useContext.selected_oration) !== executionCanonical({source_key: ownerKey, position: unit.position, kind: 'ordinary', series: 'low_mass'})) hold('source-backed-Mass-use-context-differs');
          else if (useContext.mass_form === 'sung' && !useContext.conventual) hold('ordinary-commemoration-not-applicable-in-nonconventual-sung-Mass');
        }
        if (group && group.conclusion_final !== true) hold('later-shared-conclusion-unbound');
      }
      const text = source.template.text, name = source.name_controller;
      if (source.offset_units !== 'utf16' || text.slice(source.template.placeholder.start, source.template.placeholder.end) !== 'N.' ||
          executionSha(text) !== source.template.sha256 || executionSha(name.text) !== name.sha256 ||
          text.slice(source.conclusion.cue_span.start, source.conclusion.cue_span.end) !== 'Through our Lord.' ||
          source.conclusion.state !== 'separately-proved-source-prefix' || source.conclusion.family !== 'through-our-lord') throw new Error('finite name source ranges or independent conclusion changed');
      const value = {schema: 'triptych-selected-name-execution/v1', relation: source,
        state: errors.length ? 'unresolved' : 'name-bound', unresolved: errors,
        use: source.required_role === 'own-Mass-of-Office' ? 'own-Mass-of-Office' :
          (useContext && !errors.length ? (useContext.conventual ? 'conventual-Mass' : 'Low-Mass') : null)};
      seen.add(event.id);
      return Object.assign({}, event, {nameExecution: value, sourceHooks: uniqueSourceHooks([event]).concat([
        {kind: 'publication', id: source.template.publication_passage_id},
        {kind: 'publication', id: source.name_controller.publication_passage_id},
        {kind: 'inference', id: NAME_METHOD + '/' + source.accepted_date + '/' + ownerKey + '/' + target[2]}
      ])});
    }
    function visit(event) {
      if (event.kind === 'proper-choice') return Object.assign({}, event, {options: event.options.map(function (option) {
        return event.selection.state === 'selected' && event.selection.option === option.id
          ? Object.assign({}, option, {events: option.events.map(visit)}) : option;
      })});
      if (event.kind !== 'proper') return event;
      const hook = (event.sourceHooks || []).find(function (one) { return one.kind === 'proper-structure'; });
      if (!hook) return event;
      const parts = hook.id.split('/'), owner = structure.masses.find(function (one) { return one.key === parts[1]; });
      const proper = owner && owner.propers[Number(parts[2]) - 1];
      if (!proper) throw new Error('name execution lacks exact production source coordinate');
      let projected = apply(event, proper, owner.key, null);
      if (event.orationGroups) projected = Object.assign({}, projected, {orationGroups: event.orationGroups.map(function (group) {
        return Object.assign({}, group, {members: group.members.map(function (member) {
          const h = member.sourceHooks.find(function (one) { return one.kind === 'proper-structure'; }).id.split('/');
          const m = structure.masses.find(function (one) { return one.key === h[1]; });
          return apply(member, m.propers[Number(h[2]) - 1], m.key, group);
        })});
      })});
      return projected;
    }
    return events.map(visit);
  }
  function nameExecutionCoverage(events) {
    const found = new Map();
    function visit(event) {
      if (event.nameExecution) found.set(event.id, event.nameExecution);
      (event.orationGroups || []).forEach(function (group) { group.members.forEach(visit); });
      if (event.kind === 'proper-choice') (event.options || []).filter(function (option) {
        return event.selection.state === 'selected' && option.id === event.selection.option;
      }).forEach(function (option) { option.events.forEach(visit); });
    }
    (events || []).forEach(visit);
    return {schema: 'triptych-name-execution-coverage/v1', occurrences: found.size,
      bound: Array.from(found.values()).filter(function (one) { return one.state === 'name-bound'; }).length,
      unresolved: Array.from(found.values()).filter(function (one) { return one.state === 'unresolved'; }).length,
      historical_named_translations_added: 0, complete_English_claim: false};
  }

  function withOrationGroups(events, branch, readable, mass, request, structure, projectMember, dayContext) {
    if (!branch.settled || readable.state !== 'said' || !branch.oration_execution) {
      return withInseparableGroups(events, branch, readable, mass, request, structure);
    }
    const properEvents = [];
    function collect(event) {
      if (event.kind === 'proper') properEvents.push(event);
      else if (event.kind === 'proper-choice' && event.selection.state === 'selected') {
        const selected = event.options.find(function (one) { return one.id === event.selection.option; });
        (selected.events || []).forEach(collect);
      }
    }
    events.forEach(collect);
    const indexFor = function (event) {
      const hook = (event.sourceHooks || []).find(function (one) { return one.kind === 'proper-structure'; });
      const match = hook && /\/(\d{3})$/.exec(hook.id);
      if (!match) throw new Error('oration placement requires an exact principal source coordinate');
      return Number(match[1]) - 1;
    };
    const rows = properEvents.map(function (event) {
      const sourceIndex = indexFor(event);
      const proper = (mass.propers || [])[sourceIndex];
      if (!proper) throw new Error('oration principal source coordinate is not held');
      return {proper: proper, sourceIndex: sourceIndex};
    });
    const plan = Seating.orationPlan(rows, {
      active: true, calendar: request.edition.id, mainKey: mass.key, execution: branch.oration_execution,
      date: request.civilDate, season: dayContext && dayContext.season || null,
      facts: structure.proper_appointment_facts || {},
      series: branch.orations.all || branch.orations.low_mass || [],
      owners: (structure.masses || []).map(function (owner) {
        return {key: owner.key, sourcePaths: owner.proper_source_paths || [], rows: (owner.propers || []).map(function (proper, sourceIndex) {
          return {proper: proper, sourceIndex: sourceIndex};
        })};
      })
    });
    const byIndex = new Map(plan.map(function (one) { return [one.sourceIndex, one]; }));
    function attach(event) {
      if (event.kind === 'proper-choice') {
        return Object.assign({}, event, {options: event.options.map(function (option) {
          return event.selection.state === 'selected' && event.selection.option === option.id
            ? Object.assign({}, option, {events: option.events.map(attach)}) : option;
        })});
      }
      if (event.kind !== 'proper') return event;
      const seatPlan = byIndex.get(indexFor(event));
      if (!seatPlan) return event;
      const groups = seatPlan.groups.map(function (group) {
        return Object.assign({}, group, {members: group.members.map(function (member) {
          const owner = structure.masses.find(function (one) { return one.key === member.key; });
          const projected = projectMember ? projectMember(member, event) : projectProper(
            member.proper, member.sourceIndex, owner, request, structure, 'day',
            event.seat, semanticSlot({name: group.slot}));
          projected.of_name = member.of_name;
          if (member.applicability) projected.sourceHooks.push({
            kind: 'proper-appointment', id: JSON.stringify(member.applicability)
          });
          return withOrationExecutionSource(projected, member.proper, group, request, structure);
        })});
      });
      groups.forEach(function (group) {
        const bounded = group.members.find(function (member) { return member.executionSource; });
        if (!bounded) return;
        const unresolved = Array.from(new Set((group.execution && group.execution.unresolved || [])
          .concat(bounded.executionSource.unresolved)));
        group.execution = Object.assign({}, group.execution, {state: unresolved.length ? 'unresolved' : 'petition-and-printed-companion-cue',
          unresolved: unresolved, source_method: EXECUTION_METHOD});
      });
      const own = groups.flatMap(function (group) { return group.members; }).find(function (member) {
        return member.id === event.id && member.executionSource;
      });
      return Object.assign({}, event, own ? {executionSource: own.executionSource} : {}, {orationGroups: groups,
        sourceHooks: uniqueSourceHooks([event].concat(groups.flatMap(function (group) {
          return group.members;
        }))).concat(groups.map(function (group) { return {kind: 'locus', id: group.locus}; }))});
    }
    return events.map(attach);
  }

  function withInseparableGroups(events, branch, readable, mass, request, structure) {
    if (!branch.settled || readable.state !== 'said') return events;
    const series = branch.orations && (branch.orations.all || branch.orations.low_mass) || [];
    const groups = series.filter(function (one) { return one.group === 'inseparable'; });
    if (!groups.length) return events;
    groups.forEach(function (group) {
      (group.slots || []).forEach(function (slot) {
        if (events.filter(function (event) {
          return event.kind === 'proper' && event.editionSlotLabel === slot;
        }).length !== 1) {
          throw new Error('inseparable group lacks a unique principal source slot: ' + slot);
        }
      });
    });
    return events.map(function (event) {
      if (event.kind !== 'proper') return event;
      const applicable = groups.filter(function (group) {
        return group.slots.indexOf(event.editionSlotLabel) >= 0;
      });
      if (!applicable.length) return event;
      const attached = applicable.map(function (group) {
        if (group.count !== 1 || !Array.isArray(group.members) || group.members.length !== 2) {
          throw new Error('invalid counted inseparable oration group');
        }
        return {
          kind: 'inseparable', count: group.count, position: group.position,
          conclusion: group.conclusion, locus: group.group_locus,
          members: group.members.map(function (member) {
            const owner = (structure.masses || []).find(function (one) { return one.key === member.of; });
            const matching = owner && (owner.propers || []).map(function (proper, index) {
              return {proper: proper, index: index};
            }).filter(function (row) {
              return row.proper.name === event.editionSlotLabel && row.proper.form_id === 'main';
            });
            if (!matching || matching.length !== 1) {
              throw new Error('inseparable oration lacks an exact source-owned slot: ' + member.of);
            }
            const row = matching[0];
            const projected = projectProper(row.proper, row.index, owner, request, structure,
              'day', event.seat, event.semanticSlot);
            projected.of_name = member.of_name;
            return projected;
          })
        };
      });
      return Object.assign({}, event, {orationGroups: attached,
        sourceHooks: uniqueSourceHooks([event].concat(attached.flatMap(function (group) {
          return group.members;
        }))).concat(attached.map(function (group) {
          return {kind: 'locus', id: group.locus};
        }))});
    });
  }

  function adaptPropers(input) {
    const request = input.request;
    const checked = Contract.validateReaderState(request);
    if (!checked.ok || request.entrance !== 'propers') throw new Error('invalid Propers reader state');
    if (!input.structure || input.structure.calendar !== request.edition.id) {
      throw new Error('Propers structure does not match requested edition');
    }
    if (input.ordinary && input.ordinary.calendar !== request.edition.id) {
      throw new Error('Propers Ordinary does not match requested edition');
    }
    const mass = (input.structure.masses || []).find(function (one) {
      return one.key === request.formulary.id;
    });
    if (!mass) throw new Error('requested Propers formulary is not held');
    if (request.formulary.type && request.formulary.type !== (mass.kind || null)) {
      throw new Error('requested Propers formulary type does not match the held object');
    }
    const formSelection = properFormSelection(mass, request);
    if (formSelection.choice) {
      if (hasOwn(request, 'alternative') || request.properChoices) {
        throw new Error('an explicit alternative requires an exact selected Mass form');
      }
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
    const frame = ordinaryFrame(mass, formSelection.form);
    const wantsOrdinary = request.options && request.options.ordinary === true;
    if (wantsOrdinary && frame.applicability === 'full' && !input.ordinary) {
      throw new Error('the selected edition has no production Ordinary to render');
    }
    const ordinary = wantsOrdinary && frame.applicability === 'full'
      ? input.ordinary : null;
    const seated = seatedEvents(
      mass, formSelection.rows, request, input.structure, ordinary, 'propers',
      Seating.predicateFacts({
        appointments: formularyAppointments(mass, formSelection.form, null)
      }), {conditionFacts: input.conditionFacts}
    );
    const relation = mass.oration_relation;
    if (relation && (Object.keys(relation).sort().join(',') !== 'companion,host,locus,scope,slots' ||
        relation.scope !== 'dated-mass-of-office' ||
        typeof relation.host !== 'string' || !relation.host ||
        typeof relation.companion !== 'string' || !relation.companion ||
        typeof relation.locus !== 'string' || !relation.locus ||
        [relation.host, relation.companion].indexOf(mass.key) < 0 ||
        relation.host === relation.companion ||
        ![relation.host, relation.companion].every(function (key) {
          return (input.structure.masses || []).some(function (one) { return one.key === key; });
        }) ||
        JSON.stringify(relation.slots) !== JSON.stringify(['Collect', 'Secret', 'Postcommunion']))) {
      throw new Error('invalid source-qualified inseparable oration relation');
    }
    const events = relation ? seated.events.map(function (event) {
      if (event.kind !== 'proper' || relation.slots.indexOf(event.editionSlotLabel) < 0) return event;
      return Object.assign({}, event, {orationContext: {
        kind: 'inseparable-use-context-unresolved', relation: relation,
        reason: 'date-independent-propers-does-not-establish-mass-of-office'
      }});
    }) : seated.events;
    assertExplicitWitnesses(events, request, input.structure);
    const resolved = {
      edition: request.edition.id, formulary: mass.key, type: mass.kind || null
    };
    if (formSelection.id !== null) resolved.form = formSelection.id;
    if (request.alternative) resolved.alternative = request.alternative.id;
    return {
      entrance: 'propers',
      request: request,
      calendarResult: null,
      resolved: resolved,
      events: events,
      ...(nameExecutionCoverage(events).occurrences ? {nameExecutionCoverage: nameExecutionCoverage(events)} : {}),
      ...(executionSourceCoverage(events).petitions ? {executionSourceCoverage: executionSourceCoverage(events)} : {}),
      ...(hasOwn(seated.prepared, 'usage') ? {properAppointmentUsage: seated.prepared.usage} : {}),
      sourcePathChoices: sourcePathChoices(seated.prepared, mass, request, events),
      coverage: coverageFor(
        input.structure, mass, seated.prepared.activeRows.map(function (row) { return row.proper; }),
        request, ordinary, events, seated.ordinaryUnresolved, formSelection.form, seated.prepared.unresolved.concat(seated.prepared.sourcePathUnresolved)
      ).concat(relation ? [Contract.coverage('unsupported', 'inseparable-oration-assembly', null,
        [{kind: 'unsupported-object', basis: 'mass-of-office-use-context-not-established'}])] : []),
      explicitAbsences: [{
        kind: 'explicit-semantic-absence',
        scope: 'civil-date-and-calendar-result',
        repositoryTerm: 'semantic-absence',
        reason: 'propers-entrance-is-date-independent'
      }].concat(relation ? [{kind: 'explicit-semantic-absence', scope: 'inseparable-oration-assembly',
        repositoryTerm: 'unresolved', reason: 'mass-of-office-use-context-not-established',
        sourceHooks: [{kind: 'locus', id: relation.locus}], relation: relation}] : [],
        claimLocalCollectAbsences(mass, request, formSelection.form)),
      unresolvedChoices: (request.unresolvedChoices || []).concat(
        unresolvedCommonSetChoices(input.structure, mass, request),
        appointmentChoices(seated.prepared, mass, request, input.structure),
        sourcePathUnresolvedChoices(seated.prepared, mass, request),
        alternativeChoices(events), translationChoices(events)
      ),
      ordinaryUnresolved: seated.ordinaryUnresolved
    };
  }

  function sameJson(left, right) {
    return JSON.stringify(jsonIdentity(left)) === JSON.stringify(jsonIdentity(right));
  }

  function jsonIdentity(value) {
    // Mapping order is not identity. Array order, value types and exact keys are.
    if (Array.isArray(value)) return ['array', value.map(jsonIdentity)];
    if (value && typeof value === 'object') return ['object', Object.keys(value).sort().map(function (key) {
      return [key, jsonIdentity(value[key])];
    })];
    return [typeof value, value];
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
    const admitted = generatedProper && admittedCycle(generatedProper);
    const selection = admitted !== undefined ? admitted : generatedProper ? dayCycle(generatedProper, request.lectionary) : null;
    const cycle = selection ? selection.key : null;
    const cycles = selection && selection.dimension === 'sunday' ? [cycle] : [];
    const weekdayCycles = selection && selection.dimension === 'weekday' ? [cycle] : [];
    const references = (proper.verses || []).map(function (one) { return one.ref; }).filter(Boolean);
    const generated = selectedMaterial(generatedProper, request, { numbering: null }, 'day');
    if (generated.scriptureComponents && languageBodyAbsence(
        generatedProper, request.languages && request.languages.orations || 'la',
        selection, request)) {
      generated.scriptureComponents.unresolved = (proper.verses || []).filter(function (one) {
        return one && one.ref && !one.text;
      }).map(function (one) {
        return { reference: one.ref, reason: one.note || 'text-not-held' };
      });
    }
    if (generated.scriptureComponents &&
        !sameJson(references, generated.scriptureComponents.references)) {
      throw new Error('mass-today mixed scripture components disagree with generated structure');
    }
    if (references.length && !generated.scriptureComponents) {
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
      return generated;
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

  function assertCliProperIdentity(generatedProper, proper, pathOwned) {
    if (hasOwn(generatedProper, 'appointment_applicability') !== hasOwn(proper, 'appointment_applicability') ||
        !sameJson(generatedProper.appointment_applicability, proper.appointment_applicability)) {
      throw new Error('mass-today Proper applicability metadata disagrees with generated structure');
    }
    if (!generatedProper || !proper || generatedProper.name !== proper.name ||
        (generatedProper.form || null) !== (proper.form || null) ||
        generatedProper.form_id !== proper.form_id ||
        (generatedProper.source || null) !== (proper.source || null) ||
        !sameJson(generatedProper.taken_from || null, proper.taken_from || null) ||
        !sameJson(generatedProper.appointment_identity || null, proper.appointment_identity || null) ||
        !sameJson(generatedProper.appointment_replacement || null, proper.appointment_replacement || null) ||
        !sameJson(generatedProper.appointment_applicability || null, proper.appointment_applicability || null) ||
        hasOwn(generatedProper, 'source_path_relation') !== hasOwn(proper, 'source_path_relation') ||
        !sameJson(generatedProper.source_path_relation, proper.source_path_relation) ||
        !sameJson(generatedProper.ordinary_disposition || null, proper.ordinary_disposition || null)) {
      throw new Error('mass-today Proper order disagrees with generated structure or source appointment metadata');
    }
    function references(owner) {
      return (owner.citations || owner.verses || []).map(function (one) { return one.ref; });
    }
    if (pathOwned && !sameJson(references(generatedProper), references(proper))) {
      throw new Error('mass-today raw source path references disagree with generated structure');
    }
    cycleSelections(proper);
    properBodyStatus(proper);
    for (const family of ['cycles', 'weekday_cycles']) {
      const generatedKeys = Object.keys(generatedProper[family] || {}).sort();
      const payloadKeys = Object.keys(proper[family] || {}).sort();
      if (!sameJson(payloadKeys, generatedKeys)) {
        throw new Error('mass-today ' + family + ' inventory disagrees with generated structure');
      }
      payloadKeys.forEach(function (cycle) {
        const owner = proper[family][cycle];
        properBodyStatus(owner);
        if (pathOwned && !sameJson(references(generatedProper[family][cycle]), references(owner))) {
          throw new Error('mass-today raw source path material references disagree with generated structure');
        }
      });
    }
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
    if (!sameJson(mass.proper_appointment_facts || {},
        input.structure.proper_appointment_facts || {})) {
      throw new Error('mass-today Proper appointment facts disagree with the source structure');
    }
    if (!sameJson(mass.proper_source_paths || [], generatedMass.proper_source_paths || [])) {
      throw new Error('mass-today source path relations disagree with the source structure');
    }
    const formSelection = properFormSelection(generatedMass, request, true);
    if (formSelection.choice) {
      if (request.properChoices) throw new Error('explicit Proper choices require an exact selected Mass form');
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
    generatedRows.forEach(function (row, index) {
      assertCliProperIdentity(row.proper, (mass.propers || [])[index], Boolean(generatedMass.proper_source_paths));
    });
    const lectionary = input.derived && input.derived.liturgicalYear &&
      input.derived.liturgicalYear.lectionary || null;
    const payloadLectionary = day.why && hasOwn(day.why, 'lectionary')
      ? day.why.lectionary : null;
    if (!sameJson(payloadLectionary, lectionary)) {
      throw new Error('mass-today lectionary result disagrees with calendar assembly');
    }
    const adaptedRequest = Object.assign({}, request, { lectionary: lectionary });
    const prepared = prepareAppointments(generatedMass, generatedRows, adaptedRequest, input.structure, {
      date: input.derived.date, season: input.derived.season, conditionFacts: input.conditionFacts, usageContext: {
        calendar: input.derived.calendar, entrance: request.entrance, branch: branch, readable: readable,
        mass: generatedMass, formId: formSelection.id || 'main'
      }
    });
    if (hasOwn(mass, 'proper_appointment_usage') !== hasOwn(prepared, 'usage') ||
        !sameJson(mass.proper_appointment_usage, prepared.usage)) {
      throw new Error('mass-today Proper usage context disagrees with the original calendar owner');
    }
    if ((generatedMass.proper_source_paths || []).length) {
      [['source_path_selections', 'sourcePathSelections'], ['source_path_unresolved', 'sourcePathUnresolved'],
        ['source_path_availability', 'sourcePathAvailability'], ['material_selections', 'materialSelections']]
        .forEach(function (fields) {
          if (!sameJson(mass[fields[0]], prepared[fields[1]])) {
            throw new Error('mass-today ' + fields[0] + ' disagrees with shared source path admission');
          }
        });
    }
    const payloadBySourceIndex = new Map();
    generatedRows.forEach(function (generatedRow, cliIndex) {
      payloadBySourceIndex.set(generatedRow.sourceIndex, {
        proper: (mass.propers || [])[cliIndex], generated: generatedRow.proper
      });
    });
    function cliProper(row, seat, semanticSlotOverride) {
      const sourceIndex = row.sourceIndex;
      const held = payloadBySourceIndex.get(sourceIndex) || {};
      const rawProper = held.proper;
      const rawGenerated = held.generated;
      // Full raw parity ran before path filtering. Material and body rights
      // now use only the exact admitted source owner, keeping calendar cycle.
      const generatedProper = row.proper;
      const selector = prepared.materialSelections[sourceIndex];
      const proper = selector && selector.family !== null
        ? Object.assign({}, rawProper, rawProper[selector.family][selector.cycle]) : rawProper;
      if (!rawGenerated) throw new Error('mass-today has no raw source row for admitted appointment');
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
        prepared.rows.map(function (row) { return row.proper; }),
        Seating.predicateFacts({
          settled: branch.settled, weekday: input.derived.weekday,
          season: input.derived.season,
          nature: branch.winner && branch.winner.nature,
          date: input.derived.date,
          anchors: input.derived.liturgicalYear &&
            input.derived.liturgicalYear.anchors || null,
          appointments: formularyAppointments(
            generatedMass, formSelection.form, branch.winner)
        })
      );
      ordinaryUnresolved = resolution.unresolved;
      const placed = Seating.seatPropers(
        prepared.rows, Seating.seats(ordinary, resolution.shown), null, prepared.selections
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
            request.languages && request.languages.ordinaryWitness || null,
            { calendar: request.edition.id, formulary: generatedMass.key }
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
        Seating.unframedEvents(prepared.rows, null, prepared.selections), generatedMass, adaptedRequest,
        function (row, seat, semantic) {
          return cliProper(row, seat, semantic);
        },
        function () { throw new Error('unframed Proper sequence carried an Ordinary event'); }
      );
    }
    events = withOrationGroups(events, branch, readable, generatedMass, adaptedRequest, input.structure,
      function (member, anchor) {
        const owners = (day.masses || []).filter(function (one) { return one.key === member.key; });
        if (owners.length !== 1) throw new Error('mass-today oration member lacks one exact raw source owner');
        const owner = owners[0];
        const generatedOwner = input.structure.masses.find(function (one) { return one.key === member.key; });
        const generatedRows = generatedOwner.propers.map(function (proper, sourceIndex) {
          return {proper: proper, sourceIndex: sourceIndex};
        }).filter(function (row) { return row.proper.form_id === member.proper.form_id && row.proper.name !== 'Placeholder'; });
        const forms = (owner.forms || []).filter(function (one) { return one.id === member.proper.form_id; });
        if (forms.length > 1) throw new Error('mass-today oration member has ambiguous raw source forms');
        const rows = forms.length ? forms[0].propers : owner.propers;
        if (!rows || rows.length !== generatedRows.length) throw new Error('mass-today oration source row count drifted');
        const ordinal = generatedRows.findIndex(function (row) { return row.sourceIndex === member.sourceIndex; });
        if (ordinal < 0) throw new Error('mass-today oration member lacks its exact raw source ordinal');
        const proper = rows[ordinal];
        assertCliProperIdentity(member.proper, proper, false);
        const selected = cliMaterial(proper, adaptedRequest, member.proper);
        return {
          id: properEventId(request.edition.id, member.key, member.sourceIndex), kind: 'proper',
          semanticSlot: semanticSlot(member.proper), editionSlotLabel: proper.name,
          form: proper.form || null, sourceKind: proper.source || null, selected: selected,
          seat: anchor.seat || null,
          sourceHooks: sourceHooks(proper, selected, request.edition.id, member.key, member.sourceIndex)
        };
      }, {season: input.derived.season});
    events = withFiniteNameExecution(events, branch, readable, generatedMass, adaptedRequest, input.structure, input.nameExecutionUse || null);
    assertExplicitWitnesses(events, adaptedRequest, input.structure);
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
      ...(nameExecutionCoverage(events).occurrences ? {nameExecutionCoverage: nameExecutionCoverage(events)} : {}),
      ...(executionSourceCoverage(events).petitions ? {executionSourceCoverage: executionSourceCoverage(events)} : {}),
      ...(hasOwn(prepared, 'usage') ? {properAppointmentUsage: prepared.usage} : {}),
      sourcePathChoices: sourcePathChoices(prepared, generatedMass, request, events),
      coverage: coverageFor(
        input.structure, generatedMass,
        prepared.activeRows.map(function (row) { return row.proper; }), adaptedRequest,
        request.options && request.options.ordinary && frame.applicability === 'full' &&
          day.ordinary && !day.ordinary.refused
          ? day.ordinary : null,
        events, ordinaryUnresolved, formSelection.form, prepared.unresolved.concat(prepared.sourcePathUnresolved)
      ),
      explicitAbsences: explicitAbsencesFor(branch, lectionary).concat(orationExecutionAbsences(events),
        claimLocalCollectAbsences(generatedMass, request, formSelection.form)
      ),
      unresolvedChoices: choices.concat(
        unresolvedCommonSetChoices(input.structure, generatedMass, request),
        appointmentChoices(prepared, generatedMass, request, input.structure),
        sourcePathUnresolvedChoices(prepared, generatedMass, request),
        alternativeChoices(events), translationChoices(events)
      ),
      ordinaryUnresolved: ordinaryUnresolved
    };
  }

  function browseState(prepared, context) {
    if (Object.prototype.hasOwnProperty.call(prepared.parsed.recognized, 'proper-choices')) {
      return {ok: false, errors: [{code: 'incomplete-explicit-identity', path: 'proper-choices',
        message: 'explicit Proper choices require an exact formulary'}]};
    }
    const requestedMode = Object.prototype.hasOwnProperty.call(prepared.parsed.recognized, 'mode')
      ? prepared.parsed.recognized.mode : 'read';
    const ordinaryLanguage = Object.prototype.hasOwnProperty.call(
      prepared.parsed.recognized, 'ordinary-lang'
    ) ? prepared.parsed.recognized['ordinary-lang'] : (requestedMode === 'missal' ? 'en' : null);
    const ordinaryLanguages = context.missals[prepared.missal] &&
      context.missals[prepared.missal].ordinaryLanguages || [];
    if (ordinaryLanguage && ordinaryLanguages.indexOf(ordinaryLanguage) < 0) {
      return { ok: false, errors: [{
        code: 'invalid-explicit-value', path: 'ordinary-lang',
        message: 'the selected edition does not hold this Ordinary language'
      }] };
    }
    const variants = (prepared.parsed.variantKeys || []).filter(function (key) {
      return prepared.parsed.present.indexOf(key) >= 0;
    });
    if (variants.length) {
      return { ok: false, errors: [{
        code: 'incomplete-explicit-identity', path: variants[0],
        message: 'an Ordinary option requires an exact formulary'
      }] };
    }
    const state = {
      schema: Contract.STATE_SCHEMA,
      entrance: 'propers',
      civilDate: null,
      edition: { id: prepared.missal },
      browse: { kind: 'browse-entry' },
      bible: {
        id: prepared.bible,
        numbering: context.bibles[prepared.bible] && context.bibles[prepared.bible].numbering || null
      },
      languages: { orations: prepared.orations },
      requestedMode: requestedMode,
      options: { ordinary: requestedMode === 'missal', legitimate: {} },
      coverage: [],
      unresolvedChoices: [],
      sourceHooks: []
    };
    if (Object.prototype.hasOwnProperty.call(prepared.parsed.recognized, 'text-display')) {
      state.textDisplay = prepared.parsed.recognized['text-display'];
    }
    if (Object.prototype.hasOwnProperty.call(prepared.parsed.recognized, 'scripture-companion')) {
      const id = prepared.parsed.recognized['scripture-companion'];
      const bible = context.bibles[id];
      if (!bible || bible.language !== 'la') return { ok: false, errors: [{
        code: 'invalid-explicit-value', path: 'scripture-companion',
        message: 'the companion must name a held Latin Bible edition'
      }] };
      state.scriptureCompanion = { id: id, numbering: bible.numbering || null };
    }
    if ((prepared.parsed.duplicates || []).some(function (row) {
      return row.key === 'scripture-companion';
    })) return { ok: false, errors: [{ code: 'duplicate-explicit-key',
      path: 'scripture-companion', message: 'a semantic URL key may not occur more than once' }] };
    if (ordinaryLanguage) state.languages.ordinary = ordinaryLanguage;
    if (Object.prototype.hasOwnProperty.call(prepared.parsed.recognized, 'location')) {
      state.semanticLocation = { eventId: prepared.parsed.recognized.location };
    }
    return { ok: Contract.validateReaderState(state).ok, state: state, legacy: {
      sources: {}, unknown: (prepared.parsed.unknown || []).slice(), inert: [], variants: {}
    }, errors: Contract.validateReaderState(state).errors };
  }

  function validationContext(input) {
    const context = { missals: {}, bibles: {} };
    for (const bible of (input.bibles && input.bibles.bibles) || []) {
      context.bibles[bible.id] = { numbering: bible.numbering || null, language: bible.language || null };
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
      for (const translation of structure.coverage && structure.coverage.languages || structure.translations || []) {
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
    browseState: browseState,
    selectOrdinaryTranslation: ordinaryTranslation,
    validationContext: validationContext,
    adaptDay: adaptDay,
    adaptPropers: adaptPropers,
    adaptCli: adaptCli
  });
}));
