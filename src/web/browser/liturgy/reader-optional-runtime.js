/* Load presentation dependencies only when validated reader state uses them. */
'use strict';

(function (root) {
  const doc = root.document;
  const source = new URL('day.js', doc.currentScript.src).href;
  let pending = null;

  function loadOrdinary() {
    if (root.TriptychOrdinaryRenderer) return Promise.resolve(root.TriptychOrdinaryRenderer);
    if (pending) return pending;
    pending = new Promise(function (resolve, reject) {
      const script = doc.createElement('script');
      script.src = source;
      script.onload = function () {
        if (root.TriptychOrdinaryRenderer) resolve(root.TriptychOrdinaryRenderer);
        else { pending = null; script.remove(); reject(new Error('The Ordinary presenter did not initialize')); }
      };
      script.onerror = function () {
        pending = null;
        script.remove();
        reject(new Error('The Ordinary presenter could not be loaded'));
      };
      doc.head.appendChild(script);
    });
    return pending;
  }

  const modules = {
    compare: [
      ['reader-comparison.js', 'LiturgyReaderComparison', 'compare'],
      ['reader-compare-view.js', 'LiturgyReaderCompareView', 'render']
    ],
    study: [['reader-study-view.js', 'LiturgyReaderStudyView', 'attach']]
  };
  const pendingModules = new Map();

  function loadModule(descriptor) {
    const [file, name, method] = descriptor;
    function initialized() { return root[name] && typeof root[name][method] === 'function'; }
    if (initialized()) return Promise.resolve(root[name]);
    if (pendingModules.has(file)) return pendingModules.get(file);
    const promise = new Promise(function (resolve, reject) {
      const script = doc.createElement('script');
      script.src = new URL(file, source).href;
      function fail(problem) {
        pendingModules.delete(file);
        script.remove();
        reject(new Error(file + problem));
      }
      script.onload = function () {
        if (initialized()) resolve(root[name]);
        else fail(' did not initialize');
      };
      script.onerror = function () { fail(' could not be loaded'); };
      doc.head.appendChild(script);
    });
    pendingModules.set(file, promise);
    return promise;
  }

  function forState(state) {
    const selected = modules[state.requestedMode];
    if (!selected) return state.options.ordinary ? loadOrdinary() : Promise.resolve(null);
    const ordinary = state.options.ordinary ? loadOrdinary() : Promise.resolve(null);
    return Promise.all([ordinary].concat(selected.map(loadModule)))
      .then(function (loaded) { return loaded[0]; });
  }

  root.TriptychReaderOptionalRuntime = Object.freeze({ loadOrdinary: loadOrdinary, forState: forState });
}(window));
