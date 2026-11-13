/* Exact source-local actor sequences. No prayer appointment or ending rules.
 * The supplied utilities are canonical JSON and SHA256 only; no conclusion
 * executor is invoked. Source text stays separate from its execution view. */
(function (root, factory) {
  const exported = factory();
  if (typeof module === 'object' && module.exports) module.exports = exported;
  else root.TriptychSourceLocalActorSequences = exported;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const METHOD_ID = 'postconciliar-finite-source-local-actor-sequences-20261113';
  const SOURCE_SCHEMA = 'triptych-source-local-actor-source/v1';
  const RESULT_SCHEMA = 'triptych-source-local-actor-sequence/v1';
  const ACTIVE_AUTHORITY_SHA256 = '7185d96774336bf3172878119419bef8465ba696b483cd6af296f64cb53cda8d';
  // BEGIN GENERATED SOURCE ACTOR PINS
  const GENERATED_AUTHORITY_SHA256 = "7185d96774336bf3172878119419bef8465ba696b483cd6af296f64cb53cda8d";
  const PUBLIC_PINS = Object.freeze({
  "[\"postconciliar\",\"good-friday\",\"main\",\"Solemn Intercession IV: For catechumens\",\"all\",1]": "a55e59d9d8101eebc8c5ed6414a906b864d6c3cd72a72bc7bc132eaab08543e1",
  "[\"postconciliar\",\"lent-4\",\"main\",\"Prayer after Communion\",\"all\",1]": "ef1673f800057d0be6e6eaf693c1e8081f74bb0cb51e47de6ca58260a188fbd7"
});
  // END GENERATED SOURCE ACTOR PINS
  function create(utilities) {
    const canonical = utilities.canonical, sha = utilities.sha;
    if (typeof canonical !== 'function' || typeof sha !== 'function') throw new Error('Canonical JSON and SHA256 utilities are required');
    const equal = (left,right) => canonical(left) === canonical(right);
    function requireValue(condition, reason) {if (!condition) throw new Error(reason);}
    function sourceSpan(text, value) {
      requireValue(value && value.offset_units === 'utf16' && Number.isInteger(value.start) && Number.isInteger(value.end) && 0 <= value.start && value.start < value.end && value.end <= text.length, 'invalid source span');
      return text.slice(value.start,value.end);
    }
    function execute(context) {
      try {
        requireValue(ACTIVE_AUTHORITY_SHA256 && ACTIVE_AUTHORITY_SHA256 === GENERATED_AUTHORITY_SHA256, 'authority inactive');
        requireValue(context && context.calendar === 'postconciliar' && context.executionScope === 'source-local-1970', 'unbound source-local context');
        const member=context.member, source=member.source;
        requireValue(typeof member.id === 'string' && member.id, 'unbound member');
        requireValue(source.schema === SOURCE_SCHEMA && source.method_id === METHOD_ID && Array.isArray(source.target) && source.target.length === 5, 'unknown source projection');
        const key=JSON.stringify([source.calendar,...source.target]);
        requireValue(sha(canonical(source)) === PUBLIC_PINS[key], 'unlisted or changed source projection');
        requireValue(source.calendar === context.calendar && equal(source.target,member.target), 'different source owner');
        requireValue(source.source_preserved === true && source.target_2008_authenticated === false && source.context.execution_scope === context.executionScope, 'source scope changed');
        const selected=context.selection;
        requireValue(selected && equal(selected.target,source.target) && equal(selected.source_selection,source.context.source_selection), 'different source-local selection');
        const language=member.language, text=member.text, part=source.languages[language];
        requireValue(['en','la'].includes(language) && typeof text === 'string' && part && sha(text) === part.body_sha256 && member.publication_passage_id === part.publication_passage_id, 'body or publication owner changed');
        const sequence=[], accounted=[];
        for (const spec of part.sequence) {
          const unit=JSON.parse(JSON.stringify(spec));
          requireValue(Array.isArray(unit.source_hooks) && unit.source_hooks.length, 'unbound sequence source');
          if (unit.kind === 'action') {
            requireValue(unit.role === 'silent-prayer' && unit.action === 'silent-prayer' && unit.participants === 'all' && unit.speaker === null && unit.dialogue_role === null && unit.text === null && unit.spoken_text === null && unit.source_span === null, 'unbound silent action');
          } else {
            requireValue(unit.kind === 'spoken' && [null,'priest','people'].includes(unit.speaker), 'unbound spoken actor');
            if (unit.source_span !== null) {
              unit.text=sourceSpan(text,unit.source_span);
              accounted.push([unit.source_span.start,unit.source_span.end]);
            } else requireValue(unit.role === 'response' && unit.dialogue_role === 'response' && unit.speaker === 'people' && unit.response_source === 'separately-sourced-response' && unit.text === 'Amen.', 'unbound external response');
            const marker=unit.nonspoken_role_marker;
            if (marker) {
              requireValue(unit.dialogue_role === 'response' && marker.text === 'R.' && sourceSpan(text,marker) === marker.text, 'printed response marker changed');
              accounted.push([marker.start,marker.end]);
            }
          }
          sequence.push(unit);
        }
        requireValue(sequence.filter(unit=>unit.dialogue_role === 'response').length === 1 && sequence[sequence.length-1].role === 'response', 'response count or order changed');
        let previous=0;
        for (const [start,end] of accounted.sort((a,b)=>a[0]-b[0])) {
          requireValue(start >= previous && !text.slice(previous,start).trim(), 'source words omitted or repeated');
          previous=end;
        }
        requireValue(!text.slice(previous).trim(), 'source tail omitted');
        return {schema:RESULT_SCHEMA,state:'source-derived-complete',execution_extent:{state:'source-derived-complete',method_id:METHOD_ID},execution_scope:'source-local-1970',calendar:source.calendar,target:source.target,language,source_text:text,body_sha256:part.body_sha256,source_preserved:true,target_2008_authenticated:false,qualification:source.qualification,source_selection:source.context.source_selection,sequence};
      } catch (error) {
        return {schema:RESULT_SCHEMA,state:'unresolved',execution_extent:{state:'unresolved',method_id:METHOD_ID},reasons:['source-local-actor-source-or-context-unbound'],sequence:[]};
      }
    }
    return Object.freeze({execute});
  }
  return Object.freeze({METHOD_ID,ACTIVE_AUTHORITY_SHA256,GENERATED_AUTHORITY_SHA256,PUBLIC_PINS,create});
});
