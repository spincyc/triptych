/* Generate a native TeX PDF from source and runtime bytes admitted by the publisher. */
(function (global) {
  'use strict';

  const BUNDLE_SCHEMA = 'triptych-native-print-source-bundle/v1';
  const RUNTIME_SCHEMA = 'triptych-native-tex-runtime/v1';
  const MAX_RESOURCE = 256 * 1024 * 1024;
  const MAX_PROJECT = 256 * 1024 * 1024;
  const HASH = /^[a-f0-9]{64}$/;
  const encoder = new TextEncoder();

  function stop(signal) {
    if (signal && signal.aborted) throw new DOMException('PDF generation cancelled.', 'AbortError');
  }

  function sameOrigin(value, base) {
    const url = new URL(value, base);
    const origin = new URL(document.baseURI).origin;
    if (url.origin !== origin || !/^https?:$/.test(url.protocol) || url.username || url.password || url.hash) {
      throw new Error('The print source and runtime must be served by this website.');
    }
    return url.href;
  }

  function relativePath(value) {
    if (typeof value !== 'string' || !value || value.length > 4096 ||
        value.startsWith('/') || /[\\\x00-\x1f\x7f]/.test(value) ||
        value.split('/').some(part => !part || part === '.' || part === '..')) {
      throw new Error('Invalid native print source path.');
    }
    return value;
  }

  async function sha256(bytes) {
    const hash = await crypto.subtle.digest('SHA-256', bytes);
    return Array.from(new Uint8Array(hash), n => n.toString(16).padStart(2, '0')).join('');
  }

  async function verified(url, sha, size, signal, limit = MAX_RESOURCE) {
    if (!HASH.test(sha || '') || !Number.isSafeInteger(size) || size < 1 || size > limit) {
      throw new Error('The native print download has no valid size and SHA-256 commitment.');
    }
    stop(signal);
    const response = await fetch(url, { signal, credentials: 'omit', redirect: 'error', cache: 'default' });
    if (!response.ok) throw new Error('A required native print resource could not be loaded (' + response.status + ').');
    const length = response.headers.get('content-length');
    if (length && Number(length) > limit) throw new Error('A native print resource exceeds its permitted size.');
    const bytes = new Uint8Array(await response.arrayBuffer());
    stop(signal);
    if (bytes.byteLength !== size || await sha256(bytes) !== sha) {
      throw new Error('A native print resource changed. Reload the edition before printing.');
    }
    return bytes;
  }

  function json(bytes, name) {
    try { return JSON.parse(new TextDecoder('utf-8', { fatal: true }).decode(bytes)); }
    catch (_) { throw new Error('The ' + name + ' is not valid UTF-8 JSON.'); }
  }

  function canonical(value) {
    if (Array.isArray(value)) return '[' + value.map(canonical).join(',') + ']';
    if (value && typeof value === 'object') {
      return '{' + Object.keys(value).sort().map(key => JSON.stringify(key) + ':' + canonical(value[key])).join(',') + '}';
    }
    return JSON.stringify(value);
  }

  async function sourceFiles(bundle, bundleURL, signal) {
    if (!bundle || bundle.schema !== BUNDLE_SCHEMA || !/^[a-f0-9]{40}$/.test(bundle.source_revision || '') ||
        !['pdftex', 'xetex'].includes(bundle.engine) || !Array.isArray(bundle.files) ||
        !bundle.files.length || bundle.files.length > 20000) {
      throw new Error('Unsupported or incomplete native print source bundle.');
    }
    const cwd = relativePath(bundle.cwd);
    const entrypoint = relativePath(bundle.entrypoint);
    if (!entrypoint.startsWith(cwd + '/')) throw new Error('The native print entrypoint is outside its working directory.');
    if (!bundle.options || bundle.options.shell_escape !== false ||
        bundle.options.max_passes !== 8 || bundle.options.minimum_passes !== 2 ||
        bundle.options.settle_auxiliary_files !== true) {
      throw new Error('Unsupported native print compilation policy.');
    }
    const texinputs = bundle.environment && bundle.environment.TEXINPUTS !== undefined ? bundle.environment.TEXINPUTS : '';
    if (typeof texinputs !== 'string' || texinputs.length > 4096 ||
        /[\x00-\x1f\x7f;\\$!{}]/.test(texinputs) || texinputs.split(':').some(part =>
          part && part !== '.' && part !== '..' && !/^[A-Za-z0-9_./-]+$/.test(part))) {
      throw new Error('Unsupported native TeX input search path.');
    }
    if (bundle.content_sha256) {
      const unsigned = Object.assign({}, bundle);
      delete unsigned.content_sha256;
      if (!HASH.test(bundle.content_sha256) || await sha256(encoder.encode(canonical(unsigned))) !== bundle.content_sha256) {
        throw new Error('The native source bundle identity does not match its contents.');
      }
    }
    const paths = new Set();
    const files = [];
    let total = 0;
    for (const file of bundle.files) {
      stop(signal);
      const path = relativePath(file.path);
      if (paths.has(path) || (file.encoding !== 'url' && typeof file.content !== 'string')) throw new Error('Duplicate or incomplete native source file.');
      paths.add(path);
      let bytes;
      if (file.encoding === 'url') {
        bytes = await verified(sameOrigin(file.href, bundleURL), file.sha256, file.bytes, signal);
      } else if (file.encoding === 'utf8') bytes = encoder.encode(file.content);
      else if (file.encoding === 'base64' && /^[A-Za-z0-9+/]*={0,2}$/.test(file.content)) {
        let decoded;
        try { decoded = atob(file.content); } catch (_) { throw new Error('Invalid native source binary encoding.'); }
        bytes = Uint8Array.from(decoded, c => c.charCodeAt(0));
      } else throw new Error('Unsupported native source encoding.');
      total += bytes.byteLength;
      if (total > MAX_PROJECT || bytes.byteLength !== file.bytes || !HASH.test(file.sha256 || '') ||
          await sha256(bytes) !== file.sha256) throw new Error('A canonical TeX source or illustration failed verification.');
      files.push({ path, bytes });
    }
    if (!paths.has(entrypoint)) throw new Error('The native print entrypoint is missing.');
    return { files, cwd, entrypoint: entrypoint.slice(cwd.length + 1), texinputs };
  }

  async function pool(items, action, count = 4) {
    let cursor = 0;
    const result = new Array(items.length);
    const settled = await Promise.allSettled(Array.from({ length: Math.min(count, items.length) }, async () => {
      while (cursor < items.length) {
        const i = cursor++;
        result[i] = await action(items[i], i);
      }
    }));
    const failure = settled.find(item => item.status === 'rejected');
    if (failure) throw failure.reason;
    return result;
  }

  /* The bridge preserves the original project hierarchy, cwd and TEXINPUTS.
     TeX can read only verified files in this disposable worker's filesystem. */
  const WORKER_BRIDGE = String.raw`
;(function(){
  const originalMessage=self.onmessage;
  const originalCnf=typeof writeTexmfCnf==='function'?writeTexmfCnf:null;
  const originalRun=typeof runMain==='function'?runMain:null;
  let configured=false;
  if(originalRun)runMain=function(program,args){return originalRun(program,['-no-shell-escape','-halt-on-error'].concat(args));};
  self.onmessage=function(event){
    const data=event.data;
    if(data.cmd==='triptych-mkdir'){
      try{FS.mkdirTree('/work/'+data.path);self.postMessage({cmd:data.cmd,result:'ok'});}
      catch(error){self.postMessage({cmd:data.cmd,result:'failed',error:String(error.message)});}
      return;
    }
    if(data.cmd==='triptych-preload'){
      try{
        for(const file of data.files){
          if(typeof texlive200_cache!=='undefined'){
            originalMessage.call(self,{data:{cmd:'preloadtexlive',format:file.format,filename:file.filename,data:file.data}});
          }else{
            let name=file.filename;
            if(file.format===3&&!name.endsWith('.tfm'))name+='.tfm';
            if(file.format===33&&!name.endsWith('.vf'))name+='.vf';
            const path='/tex/'+name;
            FS.writeFile(path,new Uint8Array(file.data));
            texlive200[file.format+'/'+file.filename]=path;
          }
        }
        self.postMessage({cmd:data.cmd,result:'ok'});
      }catch(error){self.postMessage({cmd:data.cmd,result:'failed',error:String(error.message)});}
      return;
    }
    if(data.cmd==='triptych-configure'){
      try{
        WORKROOT='/work/'+data.cwd;
        FS.chdir(WORKROOT);
        const inputs='.;'+data.texinputs.split(':').filter(Boolean).join(';')+';/tex//';
        if(originalCnf)writeTexmfCnf=function(building){
          originalCnf(building);
          const path=WORKROOT+'/texmf.cnf';
          const value=FS.readFile(path,{encoding:'utf8'}).replace(/^TEXINPUTS\s*=.*$/m,'TEXINPUTS = '+inputs)
            +'\nshell_escape = f\nshell_escape_commands = ,\nfont_max = 9000\n';
          FS.writeFile(path,value);
          if(typeof texlive200_cache==='undefined')FS.writeFile('/work/texmf.cnf',value);
        };
        if(typeof texlive200_cache==='undefined'){
          FS.writeFile('/work/xetex','');
          FS.writeFile('/work/xdvipdfmx','');
          const config=texlive200['26/dvipdfmx.cfg'];
          if(config){
            const bytes=FS.readFile(config,{encoding:'binary'});
            FS.writeFile(WORKROOT+'/dvipdfmx.cfg',bytes);
            FS.writeFile('/work/dvipdfmx.cfg',bytes);
          }
        }
        configured=true;
        if(data.icu)self.icuData=new Uint8Array(data.icu);
        self.postMessage({cmd:data.cmd,result:'ok'});
      }catch(error){self.postMessage({cmd:data.cmd,result:'failed',error:String(error.message)});}
      return;
    }
    if(data.cmd==='triptych-state'){
      const files=[];let size=0;
      function visit(dir){for(const name of FS.readdir(dir)){
        if(name==='.'||name==='..')continue;
        const path=dir+'/'+name;const stat=FS.stat(path);
        if(FS.isDir(stat.mode)){visit(path);continue;}
        if(/\.(aux|toc|out|lof|lot|lol|ent|idx|ind|bbl|bcf|nav|snm)$/.test(name)){
          const bytes=FS.readFile(path,{encoding:'binary'});size+=bytes.byteLength;
          if(size>67108864)throw Error('Auxiliary files exceed the print limit.');
          files.push({path:path.slice(WORKROOT.length+1),bytes:bytes});
        }
      }}
      try{visit(WORKROOT);self.postMessage({cmd:data.cmd,result:'ok',files:files});}
      catch(error){self.postMessage({cmd:data.cmd,result:'failed',error:String(error.message)});}
      return;
    }
    if(data.cmd==='compilelatex'&&!configured){self.postMessage({cmd:'compile',result:'failed',error:'Native working directory was not configured.'});return;}
    return originalMessage.call(self,event);
  };
})();`;

  async function engineWorker(descriptor, runtimeBase, signal, progress, blobs) {
    if (!descriptor || !descriptor.worker || !descriptor.core || !descriptor.wasm) {
      throw new Error('The selected native TeX engine is not available.');
    }
    const assets = {};
    const listed = ['worker', 'core', 'wasm'].map(name => [name, descriptor[name]]);
    for (const item of descriptor.support || []) listed.push(['support', item]);
    const values = await pool(listed, async entry => {
      const [name, item] = entry;
      const url = sameOrigin(item.url, runtimeBase);
      const bytes = await verified(url, item.sha256, item.bytes, signal);
      const mime = name === 'wasm' ? 'application/wasm' : 'text/javascript';
      const blob = URL.createObjectURL(new Blob([bytes], { type: mime }));
      blobs.push(blob);
      assets[new URL(url).pathname.split('/').pop()] = blob;
      return [name, bytes];
    });
    const workerBytes = values.find(item => item[0] === 'worker')[1];
    const prelude = 'const __nativeAssets=' + JSON.stringify(assets) + ';\n' + String.raw`
const __nativeImport=self.importScripts.bind(self);
const __nativeFetch=self.fetch.bind(self);
self.fetch=function(url,options){
  if(!Object.values(__nativeAssets).includes(String(url)))return Promise.reject(Error('Unverified native engine resource.'));
  return __nativeFetch(url,options);
};
/* A missing optional package is a normal kpathsea miss. Report it locally;
   never make a network request and never unwind the native engine's stack. */
self.XMLHttpRequest=class{
  constructor(){this.status=404;this.response=new ArrayBuffer(0);}
  open(){}
  send(){}
  getResponseHeader(){return null;}
};
self.importScripts=function(...urls){
  for(const url of urls){
    const name=String(url).split('/').pop();
    if(!Object.hasOwn(__nativeAssets,name))throw Error('Unverified native engine script.');
    if(self.Module)self.Module.locateFile=function(file){
      const target=__nativeAssets[file.split('/').pop()];
      if(!target)throw Error('Unverified native engine binary.');
      return target;
    };
    __nativeImport(__nativeAssets[name]);
  }
};
`;
    let controller = new TextDecoder('utf-8', { fatal: true }).decode(workerBytes);
    /* The Unicode controllers declare a fixed cwd constant. Make only this
       binding configurable so the canonical project need not be rewritten. */
    if (controller.includes("const WORKROOT = '/work'")) {
      controller = controller.replace("const WORKROOT = '/work'", "var WORKROOT = '/work'");
    }
    const source = prelude + '\n' + controller + '\n' + WORKER_BRIDGE;
    const url = URL.createObjectURL(new Blob([source], { type: 'text/javascript' }));
    blobs.push(url);
    stop(signal);
    const worker = new Worker(url);
    let active = null;
    let closed = false;
    let readyResolve;
    let readyReject;
    const ready = new Promise((resolve, reject) => { readyResolve = resolve; readyReject = reject; });
    function fail(error) {
      readyReject(error);
      if (active) { const pending = active; active = null; clearTimeout(pending.timer); pending.reject(error); }
    }
    function abort() { fail(new DOMException('PDF generation cancelled.', 'AbortError')); worker.terminate(); closed = true; }
    if (signal) signal.addEventListener('abort', abort, { once: true });
    worker.onerror = event => fail(new Error('The native TeX engine stopped: ' + (event.message || 'worker failure')));
    worker.onmessage = event => {
      const data = event.data;
      if (data.result === 'ok' && !data.cmd) { readyResolve(); return; }
      if (active && data.cmd === active.expected) {
        const pending = active; active = null; clearTimeout(pending.timer);
        if (data.result === 'failed') {
          const error = new Error(data.error || 'Native TeX compilation failed.');
          error.log = data.log;
          pending.reject(error);
        }
        else pending.resolve(data);
      }
    };
    const startTimer = setTimeout(() => fail(new Error('The native TeX engine did not start in time.')), 60000);
    try { await ready; stop(signal); } catch (error) {
      worker.terminate();
      if (signal) signal.removeEventListener('abort', abort);
      throw error;
    }
    finally { clearTimeout(startTimer); }
    return {
      async ask(payload, expected = payload.cmd, timeout = 900000) {
        stop(signal);
        if (closed || active) throw new Error('The native TeX worker is unavailable.');
        return new Promise((resolve, reject) => {
          const timer = setTimeout(() => { fail(new Error('Native TeX compilation exceeded its time limit.')); worker.terminate(); closed = true; }, timeout);
          active = { resolve, reject, expected, timer };
          try { worker.postMessage(payload); }
          catch (error) { clearTimeout(timer); active = null; reject(error); }
        });
      },
      tell(payload) { stop(signal); worker.postMessage(payload); },
      close() {
        closed = true;
        fail(new DOMException('The native print worker was closed.', 'AbortError'));
        if (signal) signal.removeEventListener('abort', abort);
        worker.terminate();
      }
    };
  }

  async function auxiliaryState(worker) {
    const state = await worker.ask({ cmd: 'triptych-state' });
    if (!Array.isArray(state.files)) throw new Error('The native TeX auxiliary state could not be verified.');
    const identities = [];
    for (const file of state.files) identities.push([file.path, await sha256(new Uint8Array(file.bytes))]);
    identities.sort((a, b) => a[0].localeCompare(b[0], 'en'));
    return sha256(encoder.encode(JSON.stringify(identities)));
  }

  async function formatBytes(pin, base, signal) {
    const bytes = await verified(sameOrigin(pin.url, base), pin.sha256, pin.bytes, signal);
    if (pin.compression !== 'gzip' && !new URL(pin.url, base).pathname.endsWith('.gz')) return bytes;
    if (typeof DecompressionStream !== 'function') throw new Error('This browser cannot unpack the native TeX format.');
    const stream = new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'));
    const expanded = new Uint8Array(await new Response(stream).arrayBuffer());
    if (!expanded.length || expanded.length > 64 * 1024 * 1024) throw new Error('The native TeX format exceeds its permitted size.');
    return expanded;
  }

  async function mountProject(worker, project, texFiles, icu) {
    await worker.ask({ cmd: 'triptych-preload', files: texFiles });
    const directories = new Set();
    for (const file of project.files) {
      const directory = file.path.split('/').slice(0, -1).join('/');
      if (directory && !directories.has(directory)) {
        await worker.ask({ cmd: 'triptych-mkdir', path: directory });
        directories.add(directory);
      }
      await worker.ask({ cmd: 'writefile', url: file.path, src: file.bytes });
    }
    await worker.ask({ cmd: 'triptych-configure', cwd: project.cwd, texinputs: project.texinputs, icu });
  }

  function checkLog(log, final) {
    if (typeof log !== 'string' || /(?:^|\n)!|Fatal error|Emergency stop|no output PDF file|Missing character:|Font .*not loadable|font .*not found|Font shape[\s\S]{0,300}?undefined|Some font shapes were not available,\s*defaults substituted/i.test(log)) {
      throw new Error('The native TeX edition could not be typeset completely. No substitute PDF was created.');
    }
    if (final && /undefined references|undefined citations|There were undefined|Rerun to get|Label\(s\) may have changed|Please (?:re)?run|Rerun .*get .*right/i.test(log)) {
      return false;
    }
    return true;
  }

  async function generate(options) {
    const outer = new AbortController();
    const signal = outer.signal;
    const upstream = options.signal;
    const relay = () => outer.abort();
    if (upstream) upstream.addEventListener('abort', relay, { once: true });
    if (upstream && upstream.aborted) outer.abort();
    const timer = setTimeout(() => outer.abort(), 20 * 60 * 1000);
    const progress = message => { if (typeof options.onProgress === 'function') options.onProgress({ message }); };
    const blobs = [];
    let worker;
    let converter;
    try {
      stop(signal);
      const bundleURL = sameOrigin(options.bundleURL, document.baseURI);
      const runtimeURL = sameOrigin(options.runtimeURL, document.baseURI);
      progress('Checking the original TeX sources and print runtime…');
      const [bundleBody, runtimeBody] = await Promise.all([
        verified(bundleURL, options.bundleSHA256, options.bundleBytes, signal),
        verified(runtimeURL, options.runtimeSHA256, options.runtimeBytes, signal)
      ]);
      const bundle = json(bundleBody, 'native source bundle');
      const project = await sourceFiles(bundle, bundleURL, signal);
      const runtime = json(runtimeBody, 'native print runtime');
      if (runtime.schema !== RUNTIME_SCHEMA || !runtime.engines || !Array.isArray(runtime.texFiles) || runtime.texFiles.length > 50000) {
        throw new Error('Unsupported native TeX runtime manifest.');
      }
      const kind = bundle.engine === 'xetex' ? 'xelatex' : 'pdflatex';
      const descriptor = runtime.engines[kind];
      if (!descriptor || !descriptor.format) throw new Error('The selected native TeX format is unavailable.');
      /* Runtime payload routes are site-root relative, independent of the root's depth. */
      const assetBase = runtime.asset_base ? sameOrigin(runtime.asset_base, runtimeURL) : new URL('/', runtimeURL).href;
      progress('Loading the original fonts and TeX packages…');
      const downloads = new Map();
      const keys = new Set();
      const texFiles = await pool(runtime.texFiles, async file => {
        if (!Number.isSafeInteger(file.format) || file.format < 0 || file.format > 100 ||
            typeof file.name !== 'string' || !file.name || /[\/\\\x00-\x1f]/.test(file.name)) {
          throw new Error('Invalid native TeX package lookup.');
        }
        const key = file.format + '/' + file.name;
        if (keys.has(key)) throw new Error('Duplicate native TeX package lookup.');
        keys.add(key);
        const url = sameOrigin(file.url, assetBase);
        const identity = file.sha256 + ':' + file.bytes;
        if (!downloads.has(identity)) downloads.set(identity, verified(url, file.sha256, file.bytes, signal));
        return { format: file.format, filename: file.name, data: (await downloads.get(identity)).buffer, fileId: file.name };
      });
      worker = await engineWorker(descriptor, assetBase, signal, progress, blobs);
      let icu = null;
      if (kind === 'xelatex') {
        if (!descriptor.icu) throw new Error('The native Unicode font data is unavailable.');
        icu = await verified(sameOrigin(descriptor.icu.url, assetBase), descriptor.icu.sha256, descriptor.icu.bytes, signal);
      } else {
        await worker.ask({ cmd: 'setpreamblesnapshot', enabled: false });
      }
      await mountProject(worker, project, texFiles, icu);
      const format = await formatBytes(descriptor.format, assetBase, signal);
      if (kind === 'xelatex') await worker.ask({ cmd: 'writefile', url: 'wasmtex-xetex.fmt', src: format });
      else await worker.ask({ cmd: 'loadformat', data: format });
      worker.tell({ cmd: 'setmainfile', url: project.entrypoint });
      let previous = null;
      let result = null;
      let passes = 0;
      for (passes = 1; passes <= 8; passes++) {
        progress('Typesetting with the original TeX layout (pass ' + passes + ')…');
        result = await worker.ask({ cmd: 'compilelatex' }, 'compile');
        checkLog(result.log, false);
        if (result.status !== 0 || !result.pdf) throw new Error('The native TeX edition did not compile successfully.');
        const current = await auxiliaryState(worker);
        if (passes >= 2 && current === previous && checkLog(result.log, true)) break;
        previous = current;
      }
      if (passes > 8) throw new Error('The TeX references or contents did not settle. No incomplete PDF was offered.');
      if (kind === 'xelatex') {
        progress('Embedding the original fonts in the typeset PDF…');
        converter = await engineWorker(runtime.engines.dvipdfmx, assetBase, signal, progress, blobs);
        await mountProject(converter, project, texFiles, null);
        const stem = project.entrypoint.split('/').pop().replace(/\.[^.]+$/, '');
        await converter.ask({ cmd: 'writefile', url: stem + '.xdv', src: new Uint8Array(result.pdf) });
        converter.tell({ cmd: 'setmainfile', url: stem + '.xdv' });
        const converted = await converter.ask({ cmd: 'compilepdf' }, 'compile');
        if (converted.status !== 0 || !converted.pdf) throw new Error('The typeset Unicode edition could not be converted to PDF.');
        checkLog(converted.log, false);
        converted.log = result.log + '\n' + converted.log;
        result = converted;
      }
      const bytes = new Uint8Array(result.pdf);
      if (bytes.length < 5 || new TextDecoder().decode(bytes.slice(0, 5)) !== '%PDF-' || bytes.length > MAX_RESOURCE) {
        throw new Error('The native TeX engine did not produce a valid PDF.');
      }
      stop(signal);
      progress('The typeset PDF is ready.');
      return { bytes, sha256: await sha256(bytes), byteLength: bytes.byteLength, passes, log: result.log,
        document: bundle.document, output_id: bundle.output_id, source_revision: bundle.source_revision, runtime: runtime.id };
    } finally {
      if (worker) worker.close();
      if (converter) converter.close();
      outer.abort();
      for (const url of blobs) URL.revokeObjectURL(url);
      clearTimeout(timer);
      if (upstream) upstream.removeEventListener('abort', relay);
    }
  }

  global.TriptychNativeTeX = Object.freeze({ generate });
})(window);
