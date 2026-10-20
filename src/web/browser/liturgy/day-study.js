/* Attach Study evidence to the already rendered Day Read document. */
'use strict';

(function (root) {
  function attach(row) {
    const view = root.LiturgyReaderStudyView;
    if (!view || typeof view.attach !== 'function') {
      throw new Error('Day Study needs the production Study view');
    }
    const rendered = view.attach({
      result: row.result,
      fragment: row.fragment,
      contents: row.contents,
      locationPrefix: row.prefix || ''
    });
    row.fragment = rendered.fragment;
    row.contents = rendered.contents;
    return rendered;
  }

  root.TriptychDayStudy = Object.freeze({ attach: attach });
}(typeof globalThis !== 'undefined' ? globalThis : this));
