/* Prepare complete, source-bound editions before opening browser Print. */
(function () {
  'use strict';
  const SCHEMA = 'triptych-web-print-document/v1';
  const HEX = /^[a-f0-9]{64}$/;
  const KEY = /^[a-zA-Z0-9][a-zA-Z0-9_.:/-]*$/;
  const semanticId = (id) => typeof id === 'string' && id.length > 0 && !/[\s\u0000-\u001f\u007f]/u.test(id);
  const TYPES = new Set(['flow', 'proper', 'curriculum', 'guide', 'cards', 'plates', 'bible', 'source-volume', 'server-guide', 'server-cards']);
  const words = (value) => new Set(value.split(' ').filter(Boolean));
  const FLOW_TAGS = 'ARTICLE SECTION HEADER FOOTER ASIDE DIV P H1 H2 H3 H4 H5 H6 SPAN SUP SUB STRONG EM I B SMALL BR HR BLOCKQUOTE UL OL LI DL DT DD TABLE CAPTION COLGROUP COL THEAD TBODY TFOOT TR TH TD A ABBR CITE CODE PRE FIGURE FIGCAPTION IMG DETAILS SUMMARY';
  const TABLE_CLASSES = [83,85,87,92,93,95,96].map((n) => 'print-table-width-' + n).concat([7,8,9,10,11,12,13,14,15,17,18,19,20,21,25,26,27,31,34].map((n) => 'print-column-width-' + n)).join(' ');
  const RESPONSE_BLOCKS = ['022','038','065','070','080','090','100','110','115','120','130','140'];
  const RESPONSE_STRUTS = ['050','052','055','062','065','072','076','078','082'];
  const RESPONSE_VARIANTS = words('response-blank-short response-blank-long response-cell response-lines-2 response-lines-4 response-rule response-block-baseline110 ' + RESPONSE_BLOCKS.map((n) => 'response-block-' + n).join(' ') + ' ' + RESPONSE_STRUTS.map((n) => 'response-strut-' + n).join(' '));
  const FLOW_CLASSES = 'source-reader source-apparatus source-note source-bounds source-text source-line scripture-reference reading-refusal footnotes footnote footnote-ref footnote-backref print-local-notes toc nodecor smallcaps sans-serif print-flow-block print-flow print-table print-columns print-callout print-reference print-title print-subtitle print-rights print-revision print-align-left print-align-center print-align-right print-form-field-row print-fill-line print-fill-line-20 print-fill-line-28 print-fill-gap ' + TABLE_CLASSES;
  const PROFILES = {
    flow: {tags: words(FLOW_TAGS), classes: words(FLOW_CLASSES)},
    proper: {tags: words(FLOW_TAGS), classes: words(FLOW_CLASSES + ' chronology chronology-table timeline verse verse-number')},
    curriculum: {tags: words(FLOW_TAGS + ' math mrow mtext mo munder'), classes: words(FLOW_CLASSES + ' minipage unnumbered curriculum-part worksheet worksheet-prompt worksheet-answer worksheet-response poetry-source-window poetry-verse-line poetry-scansion response-space response-ruled-line ' + Array.from(RESPONSE_VARIANTS).join(' '))},
    guide: {tags: words(FLOW_TAGS), classes: words(FLOW_CLASSES + ' print-trainer-pair print-trainer-lane')},
    cards: {tags: words('ARTICLE SECTION HEADER FOOTER DIV P H1 H2 H3 H4 SPAN SUP STRONG EM I B SMALL BR HR UL OL LI FIGURE FIGCAPTION IMG'), classes: words(FLOW_CLASSES + ' print-sheet print-card-grid print-card-face print-card-front print-card-back')},
    plates: {tags: words('ARTICLE SECTION HEADER FOOTER ASIDE DIV P H1 H2 H3 H4 SPAN SUP STRONG EM I B SMALL BR HR UL OL LI A CODE FIGURE FIGCAPTION IMG'), classes: words(FLOW_CLASSES + ' print-plate print-plate-artwork print-plate-caption print-object print-claim print-scope dictionary-print dictionary-plate dictionary-object dictionary-title latin object-artwork object-description audience-note symbolism canonical-qualifications reference-call title-caption title-artwork opening-composition canonical-plate-header plate-objects plate-heading plate-footer reader-appendix source-notes print-review revision source-center source-minipage source-uppercase')},
    bible: {tags: words('ARTICLE SECTION HEADER FOOTER DIV P H1 H2 H3 H4 SPAN SUP STRONG EM BR'), classes: words('source-reader source-apparatus source-note source-bounds bible-division bible-book bible-chapter bible-paragraph verse verse-number print-title print-subtitle print-rights print-revision')},
    'source-volume': {tags: words('ARTICLE SECTION HEADER FOOTER ASIDE DIV P H1 H2 H3 H4 SPAN SUP STRONG EM BR A'), classes: words('source-reader reading-plan source-extent source-apparatus source-note source-bounds source-text source-line scripture-reference reading-refusal bible-paragraph verse verse-number')},
    'server-guide': {tags: words('ARTICLE SECTION HEADER FOOTER ASIDE DIV P H1 H2 H3 H4 SPAN STRONG EM BR A CODE DD DL DT FIGURE IMG LI OL UL TABLE TBODY TD TH THEAD TR BLOCKQUOTE'), classes: words(TABLE_CLASSES + ' print-align-left print-align-center print-align-right server-action server-branch server-continuation server-diagram server-guide-part server-minipage server-paired-lanes server-response server-scene server-titlepage server-trainer-layout server-trainer-rail server-center server-description server-role server-smallcaps server-uri server-samepage server-unnumbered server-align-left')},
    'server-cards': {tags: words('ARTICLE SECTION HEADER FOOTER DIV P H1 H2 H3 H4 SPAN STRONG EM BR A CODE'), classes: words('server-sheet server-low server-sung server-grid server-face server-blank server-answer server-apparatus server-face-header server-sheet-notice server-sheet-duplex server-action-body server-dense server-face-footer server-field server-field-label server-learner server-meaning server-minipage server-response server-smallcaps server-sound server-source-size-6 server-source-size-8 server-source-size-9 server-source-size-10 server-source-size-11')}
  };
  const PLATE_LAYOUTS = words('RSDBalancedFourPlateStart RSDBalancedThreeTallPlateStart RSDBalancedTwoTallPlateStart RSDDensePlateStart RSDDenseSevenPlateStart RSDHeterodoxFivePlateStart RSDRelationshipThreePlateStart RSDStoryPlateStart RSDStoryTallPlateStart');
  const COMMON_ATTRS = new Set(['id', 'class', 'lang', 'dir', 'title', 'data-print-unit', 'data-verse-key', 'data-print-book']);
  const installations = new WeakMap();
  const normalize = (value) => value.replace(/\s+/gu, ' ').trim();
  const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
  const need = (condition, message) => { if (!condition) throw new Error(message); };
  const hash = async (value) => {
    need(window.crypto && crypto.subtle, 'Source verification is unavailable.');
    const data = typeof value === 'string' ? new TextEncoder().encode(value) : value;
    return Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', data)), (n) => n.toString(16).padStart(2, '0')).join('');
  };
  const localURL = (href, base) => {
    const url = new URL(href, base || location.href);
    need(url.origin === location.origin && !url.search && !url.hash && /^https?:$/.test(url.protocol), 'A print resource has an unsafe address.');
    return url.href;
  };
  const styleState = (doc) => JSON.stringify({
    sheets: Array.from(doc.styleSheets, (sheet) => ({disabled: sheet.disabled, media: sheet.media.mediaText, rules: Array.from(sheet.cssRules, (rule) => rule.cssText)})),
    adopted: Array.from(doc.adoptedStyleSheets || [], (sheet) => ({disabled: sheet.disabled, rules: Array.from(sheet.cssRules, (rule) => rule.cssText)}))
  });
  const fontState = (doc) => JSON.stringify(Array.from(doc.fonts, (face) => [face.family, face.style, face.weight, face.stretch, face.unicodeRange, face.featureSettings, face.variationSettings, face.display, face.ascentOverride, face.descentOverride, face.lineGapOverride, face.sizeAdjust, face.status]));
  const inventoryCount = (value) => Array.isArray(value) ? value.length : value && value.count;
  const inventoryCheck = (value) => Array.isArray(value)
    ? value.every(semanticId) && new Set(value).size === value.length
    : Boolean(value && Number.isSafeInteger(value.count) && value.count >= 0 && HEX.test(value.sha256 || ''));
  const inventoryMatches = async (actual, expected) => Array.isArray(expected)
    ? same(actual, expected)
    : actual.length === expected.count && await hash(JSON.stringify(actual)) === expected.sha256;
  const structureEvents = (part) => {
    const events = [];
    const visit = (node) => {
      const attributes = Array.from(node.attributes, (attribute) => [attribute.name, attribute.value]);
      attributes.sort((a, b) => a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : 0);
      events.push(['start', node.localName.toLowerCase(), attributes]);
      for (const child of node.children) visit(child);
      events.push(['end', node.localName.toLowerCase()]);
    };
    visit(part);
    return events;
  };

  function descriptorCheck(d) {
    need(d && d.schema === SCHEMA && KEY.test(d.id || '') && TYPES.has(d.print_type), 'The print edition identity or type is invalid.');
    need(d.page_format === undefined || ['letter-portrait', 'letter-landscape', 'letter-full-bleed'].includes(d.page_format), 'The print page format is unsupported.');
    need(HEX.test(d.source_digest || '') && HEX.test(d.selection_digest || '') && HEX.test(d.style_sha256 || '') && typeof d.title === 'string' && d.title.trim(), 'Source, selection or print-style identity is missing.');
    const compact = d.unit_inventory !== undefined;
    need((d.availability === undefined || d.availability === 'available') && Array.isArray(d.parts) && d.parts.length && (compact ? inventoryCheck(d.unit_inventory) && !Array.isArray(d.unit_inventory) && d.unit_inventory.count > 0 : Array.isArray(d.expected_units) && d.expected_units.length), 'This output is unavailable or its complete part and unit inventories are missing.');
    if (d.print_type === 'server-cards') need(d.page_format === 'letter-full-bleed', 'The card edition is missing its source page contract.');
    const proof = d.coverage_result;
    need(proof && proof.status === 'pass' && proof.output_id === d.id && proof.source_digest === d.source_digest && proof.selection_digest === d.selection_digest && (compact ? same(proof.unit_inventory, d.unit_inventory) : same(proof.expected_units, d.expected_units)), 'Canonical source coverage has not passed for this exact output.');
    const unitIds = new Set();
    for (const unit of compact ? [] : d.expected_units) {
      const occurrence = unit && ((typeof unit.occurrence === 'string' && unit.occurrence) || (Number.isSafeInteger(unit.occurrence) && unit.occurrence > 0));
      need(unit && semanticId(unit.id) && !unitIds.has(unit.id) && typeof unit.source === 'string' && unit.source && occurrence, 'Canonical source units are incomplete or duplicated.');
      unitIds.add(unit.id);
    }
    const parts = new Set();
    const allUnits = [];
    let partUnitCount = 0;
    for (const part of d.parts) {
      need(part && KEY.test(part.id || '') && !parts.has(part.id) && Boolean(part.href) !== Boolean(part.selector) && HEX.test(part.text_sha256 || '') && inventoryCheck(part.expected_ids) && inventoryCheck(part.units), 'A print part declaration is invalid.');
      need((!compact && part.structure_sha256 === undefined) || HEX.test(part.structure_sha256 || ''), 'A print part has no canonical structure identity.');
      parts.add(part.id);
      if (Array.isArray(part.units)) allUnits.push(...part.units);
      partUnitCount += inventoryCount(part.units);
      for (const [selector, count] of Object.entries(part.counts || {})) need(/^(?:[a-z][a-z0-9-]*|\.[a-z][a-z0-9-]*|\[data-print-[a-z-]+\])$/.test(selector) && Number.isSafeInteger(count) && count >= 0, 'A semantic count is invalid.');
    }
    need(partUnitCount === (compact ? d.unit_inventory.count : d.expected_units.length), 'The declared parts do not cover the complete canonical selection.');
    if (!compact && d.parts.every((part) => Array.isArray(part.units))) need(same(allUnits, d.expected_units.map((unit) => unit.id)), 'The declared parts do not cover the complete canonical selection in order.');
    const assets = new Set();
    for (const asset of d.assets || []) {
      need(asset && KEY.test(asset.id || '') && !assets.has(asset.id) && HEX.test(asset.sha256 || '') && /^image\/(?:png|jpeg|webp|svg\+xml)$/.test(asset.mime || ''), 'A required illustration declaration is invalid.');
      localURL(asset.href);
      assets.add(asset.id);
    }
    for (const font of d.fonts || []) need(font && typeof font.family === 'string' && font.family && HEX.test(font.sha256 || '') && font.href && (font.unicode_range === undefined || (font.family === 'Triptych Punctus Elevatus' && font.unicode_range === 'U+2E4E') || (font.family === 'Triptych Source Marks' && font.unicode_range === 'U+211F,U+2123,U+21A9,U+2610,U+2720')), 'A required font declaration is invalid.');
    return d;
  }

  function validatePart(part, expected, descriptor) {
    const profile = PROFILES[descriptor.print_type];
    need(['ARTICLE', 'SECTION', 'DIV'].includes(part.tagName) && part.dataset.printPart === expected.id && part.dataset.printDocument === descriptor.id && part.dataset.printSource === descriptor.source_digest, 'A part does not belong to this exact print edition.');
    const ids = [];
    const units = [];
    for (const node of [part, ...part.querySelectorAll('*')]) {
      need(profile.tags.has(node.tagName), 'A print part contains markup outside its print-type profile.');
      for (const attribute of node.attributes) {
        const name = attribute.name;
        let allowed = COMMON_ATTRS.has(name);
        if (node === part && ['data-print-part', 'data-print-document', 'data-print-source'].includes(name)) allowed = true;
        if (node.tagName === 'A' && ['href', 'rel'].includes(name)) allowed = true;
        if (['TH', 'TD'].includes(node.tagName) && ['colspan', 'rowspan', 'scope', 'headers'].includes(name)) allowed = true;
        if (node.tagName === 'OL' && ['start', 'type'].includes(name)) allowed = true;
        if (node.tagName === 'IMG' && ['src', 'alt', 'width', 'height', 'data-print-asset'].includes(name)) allowed = true;
        if (node.tagName === 'DETAILS' && name === 'open') allowed = true;
        if (node.tagName === 'DIV' && name === 'data-print-grid') allowed = ['six', 'eight'].includes(attribute.value);
        if (['flow','proper','curriculum','guide'].includes(descriptor.print_type)) {
          if (['data-label','data-semantic-minipage'].includes(name)) allowed = semanticId(attribute.value);
          if (node.tagName === 'A') {
            if (name === 'data-reference') allowed = semanticId(attribute.value);
            if (name === 'data-reference-type') allowed = attribute.value === 'ref';
            if (name === 'role') allowed = ['doc-backlink','doc-noteref'].includes(attribute.value);
          }
          if (node.tagName === 'SECTION' && name === 'role') allowed = attribute.value === 'doc-endnotes';
          if (node.tagName === 'LI' && name === 'data-semantic-note') allowed = semanticId(attribute.value);
          if (name === 'data-print-type') allowed = (node.tagName === 'SECTION' && attribute.value === 'minipage' && node.classList.contains('print-flow-block')) || (node.tagName === 'SPAN' && attribute.value === 'write-in-line' && node.classList.contains('print-fill-line')) || (node.tagName === 'SPAN' && attribute.value === 'fill-gap' && node.classList.contains('print-fill-gap'));
          if (node.tagName === 'SPAN' && (node.classList.contains('print-fill-line') || node.classList.contains('print-fill-gap')) && name === 'data-semantic-form-line') allowed = semanticId(attribute.value);
          if (node.tagName === 'SPAN' && node.classList.contains('print-fill-line')) {
            if (name === 'data-source-width') allowed = ['0.20\\linewidth','0.28\\linewidth'].includes(attribute.value);
            if (name === 'data-source-thickness') allowed = attribute.value === '0.4pt';
          }
          if (node.tagName === 'FIGURE' && name === 'data-semantic-asset') allowed = /^tikz-[a-f0-9]{24}$/.test(attribute.value);
          if (node.tagName === 'IMG') {
            if (['data-semantic-diagram','data-source-asset'].includes(name)) allowed = /^tikz-[a-f0-9]{24}$/.test(attribute.value);
            if (['data-svg-sha256','data-source-tex-sha256','data-selection-digest','data-source-labels-sha256'].includes(name)) allowed = HEX.test(attribute.value);
          }
        }
        if (descriptor.print_type === 'curriculum') {
          if (['data-poetry-window','data-poetry-line'].includes(name)) allowed = /^[1-9][0-9]*$/.test(attribute.value);
          if (['data-poetry-window-name','data-semantic-unit'].includes(name)) allowed = semanticId(attribute.value);
          if (name === 'aria-label') allowed = node.classList.contains('response-space') && attribute.value === 'Response space';
          if (node.tagName === 'SPAN' && node.classList.contains('response-space')) {
            if (name === 'data-response-id') allowed = /^response-[1-9][0-9]*$/.test(attribute.value);
            if (name === 'data-response-origin') allowed = ['Blank','LongBlank','memory@blankcell','memory@twolines','memory@fourlines','hrulefill','rule','Exercise','ShortExercise','LongExercise','PassageExercise','AssessmentItem','RuleLine','vspace'].includes(attribute.value);
          }
          if (name === 'xmlns') allowed = node.tagName === 'math' && attribute.value === 'http://www.w3.org/1998/Math/MathML';
          if (name === 'display') allowed = node.tagName === 'math' && ['block','inline'].includes(attribute.value);
        }
        if (descriptor.print_type === 'source-volume' && node.tagName === 'SECTION') {
          if (name === 'data-volume-id') allowed = semanticId(attribute.value);
          if (name === 'data-volume-period') allowed = /^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(attribute.value);
          if (name === 'data-volume-digest') allowed = HEX.test(attribute.value);
        }
        if (descriptor.print_type === 'plates') {
          if (node.tagName === 'ARTICLE' && name === 'data-source-record') allowed = KEY.test(attribute.value);
          if (['FIGURE', 'LI'].includes(node.tagName) && name === 'data-source-object') allowed = KEY.test(attribute.value);
          if (node.tagName === 'SECTION' && name === 'data-layout') allowed = PLATE_LAYOUTS.has(attribute.value);
          if (node.tagName === 'HEADER' && name === 'role') allowed = attribute.value === 'heading';
          if (node.tagName === 'HEADER' && name === 'aria-level') allowed = attribute.value === '2';
        }
        if (descriptor.print_type === 'server-cards') {
          if (node.tagName === 'SECTION' && name === 'data-side') allowed = ['front', 'back'].includes(attribute.value);
          if (node.tagName === 'SECTION' && name === 'data-sheet') allowed = /^[1-9][0-9]*$/.test(attribute.value);
          if (node.tagName === 'ARTICLE' && name === 'data-pair-id') allowed = KEY.test(attribute.value);
        }
        if (descriptor.print_type === 'server-guide') {
          if (['data-scene', 'data-source-action', 'data-diagram-id'].includes(name)) allowed = KEY.test(attribute.value);
          if (name === 'data-dialogue') allowed = /^[0-9]{2}(?: AGAIN)?$/.test(attribute.value);
        }
        need(allowed, 'A print part contains an unexpected attribute that could hide or change content.');
      }
      for (const name of node.classList) need(profile.classes.has(name), 'A print part contains a presentation class outside its print-type profile.');
      if (['math','mrow','mtext','mo','munder'].includes(node.tagName)) need(node.namespaceURI === 'http://www.w3.org/1998/Math/MathML', 'The mathematical source namespace changed.');
      if (node.classList.contains('server-blank')) need(node.tagName === 'DIV' && node.className === 'server-face server-blank' && node.attributes.length === 1 && !node.childNodes.length && node.parentElement.className === 'server-grid', 'A blank card slot contains undeclared content or attributes.');
      if (node.hasAttribute('dir')) need(['ltr', 'rtl'].includes(node.dir), 'Text direction is invalid.');
      if (node !== part && node.id) ids.push(node.id);
      if (node.hasAttribute('data-print-unit')) units.push(node.dataset.printUnit);
      if (node.tagName === 'A') {
        const href = node.getAttribute('href') || '';
        need(href.startsWith('#') || ['http:', 'https:', 'mailto:', 'urn:'].includes(new URL(href, location.href).protocol), 'A source link has an unsafe protocol.');
      }
      if (node.tagName === 'IMG') need(node.dataset.printAsset && node.hasAttribute('alt'), 'An illustration is not identified or described.');
    }
    need(ids.length === inventoryCount(expected.expected_ids) && units.length === inventoryCount(expected.units), 'A print part is missing or duplicated.');
    if (Array.isArray(expected.expected_ids)) need(same(ids, expected.expected_ids), 'A print part identity is missing, duplicated or out of order.');
    if (Array.isArray(expected.units)) need(same(units, expected.units), 'A print part unit is missing, duplicated or out of order.');
    for (const [selector, count] of Object.entries(expected.counts || {})) need(part.querySelectorAll(selector).length === count, 'A print part has incomplete semantic content.');
    return {ids, units};
  }

  function validateResponseGeometry(paper, proof) {
    const roots = Array.from(paper.querySelectorAll('.response-space'));
    const counts = {};
    const kinds = {};
    const ids = new Set();
    const win = paper.ownerDocument.defaultView;
    const near = (actual, expected) => Math.abs(actual - expected) < 1;
    const sorted = (value) => JSON.stringify(Object.entries(value).sort(([a], [b]) => a < b ? -1 : a > b ? 1 : 0));
    const visibleRule = (css) => {
      const ink = (css.borderBottomColor.match(/[\d.]+/g) || []).map(Number);
      return css.borderBottomStyle === 'solid' && (ink.length < 4 || ink[3] > 0.01) && ink.slice(0, 3).some((value) => value < 254);
    };
    if (!roots.length && !proof) {
      need(!Array.from(paper.querySelectorAll('[class]')).some((node) => Array.from(node.classList).some((name) => name.startsWith('response-'))), 'An unbound writing-space class is present.');
      return;
    }
    need(proof && proof.status === 'pass' && proof.complete === true && Number.isSafeInteger(proof.unit_count) && proof.unit_count === roots.length && HEX.test(proof.expected_digest || ''), 'The complete writing-space source proof is missing.');
    for (const root of roots) {
      const variants = Array.from(root.classList).filter((name) => name !== 'response-space');
      need(root.tagName === 'SPAN' && variants.length === 1 && RESPONSE_VARIANTS.has(variants[0]) && root.attributes.length === 4 && root.getAttribute('aria-label') === 'Response space' && /^response-[1-9][0-9]*$/.test(root.dataset.responseId || '') && !ids.has(root.dataset.responseId), 'A writing space is missing its source variant or occurrence.');
      ids.add(root.dataset.responseId);
      const name = variants[0];
      const origin = root.dataset.responseOrigin;
      const css = win.getComputedStyle(root);
      const box = root.getBoundingClientRect();
      const baseline = Number.parseFloat(css.lineHeight);
      const rule = Number.parseFloat(css.borderBottomWidth);
      const lines = name === 'response-lines-2' ? 2 : name === 'response-lines-4' ? 4 : 0;
      const strut = name.startsWith('response-strut-');
      const block = name.startsWith('response-block-');
      let kind;
      let expectedOrigin;
      if (name === 'response-blank-short' || name === 'response-blank-long') {
        kind = 'inline-rule'; expectedOrigin = name === 'response-blank-short' ? 'Blank' : 'LongBlank';
        need(near(box.width, (name === 'response-blank-short' ? 1.3 : 2.6) * 96) && near(box.height, rule), 'An inline writing line has lost its source width.');
      } else if (name === 'response-rule') {
        kind = 'inline-rule'; expectedOrigin = 'hrulefill';
        need(box.width > 1 && near(box.height, rule), 'A remaining-line writing space has no writable width.');
      } else if (name === 'response-cell') {
        kind = 'blank-cell'; expectedOrigin = 'memory@blankcell';
        need(near(box.height, baseline * 2.2) && box.width > 1, 'A writing cell has lost its source height.');
      } else if (lines) {
        kind = 'ruled-lines'; expectedOrigin = lines === 2 ? 'memory@twolines' : 'memory@fourlines';
        need(root.children.length === lines && root.childNodes.length === lines && near(Number.parseFloat(css.marginTop), 8) && box.width > 1, 'A multiline writing space has lost its rules or initial spacing.');
        let last;
        for (const line of root.children) {
          const lineCss = win.getComputedStyle(line);
          const lineBox = line.getBoundingClientRect();
          need(line.tagName === 'SPAN' && line.className === 'response-ruled-line' && line.attributes.length === 1 && !line.childNodes.length && visibleRule(lineCss) && near(Number.parseFloat(lineCss.borderBottomWidth), 0.4 * 96 / 72) && near(lineBox.width, box.width) && near(lineBox.height, Number.parseFloat(lineCss.borderBottomWidth)) && (!last || near(lineBox.top - last.bottom, baseline * 1.1)), 'A source writing rule is missing or its spacing changed.');
          last = lineBox;
        }
      } else if (strut) {
        kind = 'table-row-space'; expectedOrigin = 'rule';
        need(near(box.height, Number(name.slice(-3)) / 100 * 96) && box.width < 1 && rule === 0, 'A source writing-row strut has lost its height.');
      } else if (block) {
        kind = 'response-block';
        need(['Exercise','ShortExercise','LongExercise','PassageExercise','AssessmentItem','RuleLine','vspace'].includes(origin), 'A block writing space has no source origin.');
        const height = name === 'response-block-baseline110' ? baseline * 1.1 : Number(name.slice(-3)) / 100 * 96;
        need(css.boxSizing === 'content-box' && near(box.height, height + rule) && box.width > 1, 'A writing block has lost its source gap before the rule.');
      }
      need(kind && (!expectedOrigin || expectedOrigin === origin), 'A writing-space variant disagrees with its source origin.');
      if (!lines) need(!root.childNodes.length, 'A writing space contains undeclared content.');
      if (!strut && !lines) need(near(rule, 0.4 * 96 / 72) && visibleRule(css), 'A source writing rule is missing.');
      counts[name] = (counts[name] || 0) + 1;
      kinds[kind] = (kinds[kind] || 0) + 1;
    }
    for (const node of paper.querySelectorAll('[class]')) {
      const response = Array.from(node.classList).filter((name) => name.startsWith('response-'));
      if (!response.length || node.classList.contains('response-space')) continue;
      need(node.className === 'response-ruled-line' && node.parentElement.classList.contains('response-space') && /^response-lines-[24]$/.test(Array.from(node.parentElement.classList).find((name) => name !== 'response-space') || ''), 'An unbound writing-space class is present.');
    }
    need(proof.variants && proof.kinds && sorted(counts) === sorted(proof.variants) && sorted(kinds) === sorted(proof.kinds), 'The writing-space inventory differs from the complete source plan.');
  }

  function validateCardDeck(paper) {
    const sheets = Array.from(paper.querySelectorAll('.server-sheet'));
    need(sheets.length > 0 && sheets.length % 2 === 0, 'The complete card deck needs every front and mirrored back.');
    let finalBack;
    for (let index = 0; index < sheets.length; index += 2) {
      const pair = sheets.slice(index, index + 2);
      const faces = [];
      let variant;
      for (const [sideIndex, sheet] of pair.entries()) {
        const side = sideIndex ? 'back' : 'front';
        const low = sheet.className === 'server-sheet server-low';
        need(low || sheet.className === 'server-sheet server-sung', 'The card sheet profile is invalid.');
        need(variant === undefined || variant === low, 'A front and back use different source card dimensions.');
        variant = low;
        need(sheet.dataset.side === side && Number(sheet.dataset.sheet) === index + sideIndex + 1, 'Card fronts and backs are missing, duplicated or out of order.');
        const children = Array.from(sheet.children);
        const grid = children[0];
        need(grid && grid.className === 'server-grid', 'A source card sheet contains an unexpected grid.');
        let footerIndex = 1;
        if (low && index + sideIndex > 0) {
          const duplex = children[footerIndex++];
          need(duplex && duplex.tagName === 'FOOTER' && duplex.className === 'server-sheet-duplex' && duplex.dataset.printUnit === 'sheet-' + String(index + sideIndex + 1).padStart(2, '0') + '-duplex-instruction', 'A canonical outside-grid duplex instruction is missing.');
        }
        if (index + sideIndex === sheets.length - 1) need(children[footerIndex++] && children[footerIndex - 1].className === 'server-sheet-notice', 'The canonical final-back notice is missing.');
        need(children.length === footerIndex, 'A source card sheet contains an unexpected footer or content.');
        const slots = Array.from(grid.children);
        need(slots.length === (low ? 8 : 6), 'A source card sheet is missing a physical slot.');
        const sheetBox = sheet.getBoundingClientRect();
        const gridBox = grid.getBoundingClientRect();
        const close = (actual, expected) => Math.abs(actual - expected) < 1;
        need(close(sheetBox.width, 816) && close(sheetBox.height, 1056) && close(gridBox.left - sheetBox.left, low ? 24 : 48) && close(gridBox.top - sheetBox.top, low ? 25.92 : 48) && close(gridBox.width, low ? 768 : 720) && close(gridBox.height, low ? 960.96 : 877.44), 'The source card page or grid dimensions changed.');
        const identities = [];
        for (const slot of slots) {
          const blank = slot.className === 'server-face server-blank';
          need(blank || (slot.tagName === 'ARTICLE' && slot.className === 'server-face' && slot.dataset.pairId && slot.dataset.printUnit === slot.dataset.pairId + ':' + side), 'A card face does not match its declared pair and side.');
          const box = slot.getBoundingClientRect();
          need(close(box.width, low ? 379.2 : 354.72) && close(box.height, low ? 235.2 : 286.656), 'A source card face changed physical size.');
          identities.push(blank ? null : slot.dataset.pairId);
        }
        faces.push(identities);
        if (sideIndex) finalBack = sheet;
      }
      const mirrored = faces[0].flatMap((_, slot, all) => slot % 2 ? [] : [all[slot + 1], all[slot]]);
      need(same(faces[1], mirrored), 'A card back is missing or no longer mirrors its front.');
    }
    const rights = Array.from(paper.querySelectorAll('[data-print-unit="card-revision-rights"]'));
    need(rights.length === 1 && rights[0].tagName === 'FOOTER' && rights[0].className === 'server-sheet-notice' && rights[0].parentElement === finalBack, 'The canonical final-back revision and rights are missing.');
    for (const appendix of paper.querySelectorAll('.server-apparatus')) need(!appendix.closest('.server-sheet') && (finalBack.compareDocumentPosition(appendix) & Node.DOCUMENT_POSITION_FOLLOWING), 'The canonical terminal apparatus is out of order.');
  }

  function visibleAndUnclipped(paper) {
    const doc = paper.ownerDocument;
    const win = doc.defaultView;
    const bounds = paper.getBoundingClientRect();
    const serverCards = doc.body.dataset.printType === 'server-cards';
    if (serverCards) validateCardDeck(paper);
    const styleChecks = new Set();
    const styles = new WeakMap();
    const backgrounds = new WeakMap();
    const cssOf = (node) => { if (!styles.has(node)) styles.set(node, win.getComputedStyle(node)); return styles.get(node); };
    const channels = (value) => (value.match(/[\d.]+/g) || []).map(Number);
    const background = (node) => {
      if (!node || node === paper.parentElement) return [255, 255, 255];
      if (backgrounds.has(node)) return backgrounds.get(node);
      const own = channels(cssOf(node).backgroundColor);
      const below = background(node.parentElement);
      const alpha = own.length === 4 ? own[3] : 1;
      const result = below.map((value, index) => (own[index] || 0) * alpha + value * (1 - alpha));
      backgrounds.set(node, result);
      return result;
    };
    const inspect = (node) => {
      if (styleChecks.has(node)) return;
      styleChecks.add(node);
      const css = cssOf(node);
      const blank = serverCards && node.classList.contains('server-blank') && node.className === 'server-face server-blank' && !node.childNodes.length && node.attributes.length === 1;
      if (blank) return;
      need(css.display !== 'none' && css.visibility !== 'hidden' && css.visibility !== 'collapse' && Number(css.opacity) > 0.01 && css.contentVisibility !== 'hidden', 'Some required content is hidden.');
      const fixedCardLayout = serverCards && css.position === 'absolute' && ['server-grid','server-sheet-notice','server-sheet-duplex'].includes(node.className) && node.closest('.server-sheet');
      need((!['fixed', 'sticky', 'absolute'].includes(css.position) || fixedCardLayout) && css.animationName === 'none', 'The print layout contains an uncontrolled overlay or animation.');
      if (fixedCardLayout) {
        const sheet = node.closest('.server-sheet').getBoundingClientRect();
        const box = node.getBoundingClientRect();
        need(box.left >= sheet.left - 1 && box.right <= sheet.right + 1 && box.top >= sheet.top - 1 && box.bottom <= sheet.bottom + 1, 'A controlled card element falls outside its source sheet.');
      }
      need(css.clipPath === 'none' && css.maskImage === 'none' && (css.clip === 'auto' || !css.clip), 'Some required content is clipped.');
      need(css.filter === 'none' && css.transform === 'none' && (!css.backdropFilter || css.backdropFilter === 'none'), 'The print layout contains an uncontrolled visual effect.');
      const clipped = (value) => ['hidden', 'clip', 'auto', 'scroll'].includes(value);
      need(!(clipped(css.overflowX) && node.scrollWidth > node.clientWidth + 2) && !(clipped(css.overflowY) && node.scrollHeight > node.clientHeight + 2), 'Some required content is truncated by an overflow box.');
      if (node.classList.contains('print-card-face') || node.classList.contains('server-face')) need(node.scrollHeight <= node.clientHeight + 2 && node.scrollWidth <= node.clientWidth + 2, 'A card face overflows its physical cell.');
    };
    for (const node of [paper, ...paper.querySelectorAll('*')]) inspect(node);
    const walker = doc.createTreeWalker(paper, NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) {
      const text = walker.currentNode;
      if (!text.textContent.trim()) continue;
      const ink = channels(cssOf(text.parentElement).color);
      const behind = background(text.parentElement);
      need(Number.parseFloat(cssOf(text.parentElement).fontSize) >= 5 && (ink.length < 4 || ink[3] > 0.01) && ink.some((value, index) => index < 3 && Math.abs(value - behind[index]) > 1), 'Some required text has no visible ink.');
      let node = text.parentElement;
      while (node && node !== paper.parentElement) { inspect(node); node = node.parentElement; }
      const range = doc.createRange();
      range.selectNodeContents(text);
      const rects = Array.from(range.getClientRects()).filter((rect) => rect.width > 0.1 && rect.height > 0.1);
      const cell = text.parentElement.closest('td, th, .print-card-face, .server-face, .dictionary-object, .print-trainer-lane, .server-trainer-rail');
      const cellBounds = cell ? cell.getBoundingClientRect() : bounds;
      need(rects.length && rects.every((rect) => rect.left >= Math.max(bounds.left, cellBounds.left) - 2 && rect.right <= Math.min(bounds.right, cellBounds.right) + 2), 'Some required text falls outside its printable column or cell.');
      let column = text.parentElement;
      while (column && column !== paper && !(Number.parseInt(cssOf(column).columnCount, 10) > 1)) column = column.parentElement;
      if (column && column !== paper) {
        const box = column.getBoundingClientRect();
        const count = Number.parseInt(cssOf(column).columnCount, 10);
        const gap = Number.parseFloat(cssOf(column).columnGap) || 0;
        const width = (box.width - gap * (count - 1)) / count;
        need(rects.every((rect) => Array.from({length: count}, (_, index) => box.left + index * (width + gap)).some((left) => rect.left >= left - 2 && rect.right <= left + width + 2)), 'Some required text overflows a print column.');
      }
    }
    for (const picture of paper.querySelectorAll('img')) {
      inspect(picture);
      const rect = picture.getBoundingClientRect();
      need(picture.complete && picture.naturalWidth > 0 && rect.width > 0 && rect.height > 0 && rect.left >= bounds.left - 2 && rect.right <= bounds.right + 2, 'A required illustration is missing or clipped.');
    }
  }

  function install(root, descriptor, options) {
    if (installations.has(root)) return installations.get(root);
    options = options || {};
    need(root.dataset.webPrintDocument === descriptor.id, 'The controls identify a different output.');
    const startButton = root.querySelector('[data-web-print-start]');
    const cancelButton = root.querySelector('[data-web-print-cancel]');
    const status = root.querySelector('[data-web-print-status]');
    const notice = root.querySelector('[data-web-print-notice]');
    need(startButton && cancelButton && status && notice, 'The print controls are incomplete.');
    let generation = 0;
    let active = null;
    let frame = null;
    let prepared = null;
    let state = 'idle';
    const urls = [];
    const update = (next, message) => {
      state = next;
      root.dataset.webPrintState = next;
      status.textContent = message || '';
      root.dispatchEvent(new CustomEvent('webprintstate', {detail: {state: next}}));
    };
    function reset(message, next) {
      generation += 1;
      if (active) active.abort();
      active = null;
      prepared = null;
      if (frame) frame.remove();
      frame = null;
      for (const url of urls.splice(0)) URL.revokeObjectURL(url);
      startButton.disabled = false;
      cancelButton.hidden = true;
      root.removeAttribute('aria-busy');
      update(next || 'idle', message);
    }
    function ready() {
      try {
        need(prepared && root.isConnected && root.dataset.webPrintDocument === descriptor.id && prepared.address === location.href && frame && frame.isConnected && !active, 'The selected edition changed.');
        descriptorCheck(descriptor);
        need(frame.contentDocument.documentElement.outerHTML === prepared.document, 'The prepared print document, wrappers or stylesheet changed.');
        need(styleState(frame.contentDocument) === prepared.styles && fontState(frame.contentDocument) === prepared.fontState && Array.from(frame.contentDocument.fonts).every((face, index) => face === prepared.fontFaces[index]) && frame.contentDocument.fonts.size === prepared.fontFaces.length, 'The prepared print styles or fonts changed.');
        need(frame.contentDocument.getAnimations().length === 0, 'The prepared edition contains an uncontrolled animation.');
        const paper = frame.contentDocument.querySelector('[data-web-print-paper]');
        need(JSON.stringify(descriptor) === prepared.descriptor && Math.abs(paper.getBoundingClientRect().width - prepared.width) < 1, 'The selected print data or printable width changed.');
        const parts = Array.from(paper.querySelector('[data-web-print-parts]').children);
        need(parts.length === descriptor.parts.length, 'The prepared part count changed.');
        need(frame.contentDocument.fonts.status === 'loaded', 'Required fonts are not ready.');
        need(Array.from(paper.querySelectorAll('img')).every((picture) => picture.complete && picture.naturalWidth > 0), 'A required illustration is no longer ready.');
        if (!prepared.layoutVerified) { visibleAndUnclipped(paper); validateResponseGeometry(paper, descriptor.response_geometry_coverage); prepared.layoutVerified = true; }
        return true;
      } catch (error) {
        if (prepared) prepared.problem = error.message;
        return false;
      }
    }
    async function start() {
      reset();
      const ownGeneration = generation;
      const address = location.href;
      const abort = new AbortController();
      let requested;
      active = abort;
      startButton.disabled = true;
      cancelButton.hidden = false;
      root.setAttribute('aria-busy', 'true');
      update('loading', 'Preparing the complete edition…');
      const unchanged = () => need(generation === ownGeneration && location.href === address && !abort.signal.aborted && root.isConnected && requested && root.dataset.webPrintDocument === requested.id && descriptor.id === requested.id && descriptor.source_digest === requested.source && descriptor.selection_digest === requested.selection, 'Preparation was cancelled or the selected edition changed.');
      const fetchResource = async (href) => {
        const url = localURL(href);
        const response = await fetch(url, {credentials: 'same-origin', cache: 'no-store', signal: abort.signal});
        unchanged();
        need(response.ok && (!response.url || response.url === url), 'A required print resource could not be loaded.');
        return response;
      };
      try {
        descriptorCheck(descriptor);
        requested = {id: descriptor.id, source: descriptor.source_digest, selection: descriptor.selection_digest, json: JSON.stringify(descriptor)};
        const sourceParts = [];
        const rootResource = new URL(location.href);
        rootResource.search = ''; rootResource.hash = '';
        const sourceResources = new Set([rootResource.href]);
        const ids = new Set();
        const unitIds = new Set();
        const completeUnits = [];
        for (const [index, expected] of descriptor.parts.entries()) {
          unchanged();
          update('loading', 'Loading part ' + (index + 1) + ' of ' + descriptor.parts.length + '…');
          let part;
          let base = location.href;
          if (expected.href) {
            base = localURL(expected.href);
            const response = await fetchResource(base);
            const document = new DOMParser().parseFromString(await response.text(), 'text/html');
            const found = document.querySelectorAll('[data-print-part]');
            need(found.length === 1, 'A print part response is incomplete or ambiguous.');
            part = found[0];
          } else {
            const found = root.querySelectorAll(expected.selector);
            need(found.length === 1, 'The complete inline print content is missing or ambiguous.');
            part = found[0].cloneNode(true);
          }
          unchanged();
          for (const details of part.querySelectorAll('details')) details.removeAttribute('open');
          const actual = validatePart(part, expected, descriptor);
          const [validIds, validUnits, validText, validStructure] = await Promise.all([inventoryMatches(actual.ids, expected.expected_ids), inventoryMatches(actual.units, expected.units), hash(normalize(part.textContent)).then((digest) => digest === expected.text_sha256), expected.structure_sha256 ? hash(JSON.stringify(structureEvents(part))).then((digest) => digest === expected.structure_sha256) : true]);
          need(validIds && validUnits, 'A print part is missing, duplicated or out of order.');
          need(validText, 'A print part failed source-text verification.');
          need(validStructure, 'A print part failed source-structure verification.');
          if (expected.href) sourceResources.add(base);
          unchanged();
          for (const id of [part.id, ...actual.ids].filter(Boolean)) { need(semanticId(id) && !ids.has(id), 'Two print parts repeat or omit a semantic identity.'); ids.add(id); }
          for (const unit of actual.units) { need(semanticId(unit) && !unitIds.has(unit), 'Two print parts repeat a canonical source unit.'); unitIds.add(unit); completeUnits.push(unit); }
          for (const link of part.querySelectorAll('a[href]')) if (!link.getAttribute('href').startsWith('#')) link.href = new URL(link.getAttribute('href'), base).href;
          for (const image of part.querySelectorAll('img')) {
            const asset = (descriptor.assets || []).find((item) => item.id === image.dataset.printAsset);
            need(asset && localURL(image.getAttribute('src'), base) === localURL(asset.href), 'An illustration does not match its canonical resource.');
            image.removeAttribute('src');
          }
          sourceParts.push(part);
        }
        need(await inventoryMatches(completeUnits, descriptor.unit_inventory || descriptor.expected_units.map((unit) => unit.id)), 'The prepared content does not cover the complete canonical selection in order.');
        // Verified parts become one paper document. Keep their exact source
        // fragment destinations local; citations to any other resource stay web links.
        for (const part of sourceParts) for (const link of part.querySelectorAll('a[href]')) {
          const href = link.getAttribute('href');
          if (href.startsWith('#')) continue;
          const target = new URL(href);
          if (!target.hash || target.search) continue;
          const fragment = target.hash;
          let id;
          try { id = decodeURIComponent(fragment.slice(1)); } catch (_) { continue; }
          target.hash = '';
          if (sourceResources.has(target.href) && ids.has(id)) link.setAttribute('href', fragment);
        }
        if (sourceParts.some((part) => part.textContent.includes('\u2e4e'))) need((descriptor.fonts || []).some((font) => font.family === 'Triptych Punctus Elevatus' && font.unicode_range === 'U+2E4E'), 'The font for a required source character is missing.');
        if (sourceParts.some((part) => /[\u211f\u2123\u21a9\u2610\u2720]/u.test(part.textContent))) need((descriptor.fonts || []).some((font) => font.family === 'Triptych Source Marks' && font.unicode_range === 'U+211F,U+2123,U+21A9,U+2610,U+2720'), 'The font for required source marks is missing.');
        if (sourceParts.some((part) => part.querySelector('math'))) need((descriptor.fonts || []).some((font) => font.family === 'Libertinus Math'), 'The font for the mathematical source is missing.');
        unchanged();
        const stylesheet = options.styleHref || root.dataset.webPrintStyle;
        need(stylesheet, 'The reviewed print stylesheet is missing.');
        const css = await (await fetchResource(stylesheet)).text();
        need(await hash(css) === descriptor.style_sha256, 'The print stylesheet failed verification.');
        unchanged();
        frame = document.createElement('iframe');
        frame.dataset.webPrintFrame = descriptor.id;
        frame.title = 'Complete print edition: ' + descriptor.title;
        frame.setAttribute('aria-hidden', 'true');
        Object.assign(frame.style, {position: 'absolute', left: '-10000px', top: '0', width: descriptor.page_format === 'letter-landscape' ? '1056px' : '816px', height: '1056px', border: '0'});
        document.body.appendChild(frame);
        const printed = frame.contentDocument;
        printed.open(); printed.write('<!doctype html><html><head><meta charset="utf-8"><title></title></head><body></body></html>'); printed.close();
        printed.title = descriptor.title;
        printed.documentElement.lang = descriptor.language || 'en';
        printed.body.dataset.printType = descriptor.print_type;
        printed.body.dataset.printPage = descriptor.page_format || 'letter-portrait';
        const style = printed.createElement('style'); style.textContent = css; printed.head.appendChild(style);
        const paper = printed.createElement('main'); paper.dataset.webPrintPaper = '';
        const identity = printed.createElement('header'); identity.className = 'web-print-identity';
        const edition = descriptor.edition && !normalize(descriptor.title).toLowerCase().includes(normalize(descriptor.edition).toLowerCase()) ? ' — ' + descriptor.edition : '';
        identity.textContent = descriptor.title + edition +
          (descriptor.revision ? ' — ' + descriptor.revision : '') + ' — Browser print. ' + address;
        if (descriptor.print_type !== 'server-cards') paper.appendChild(identity);
        const holder = printed.createElement('div'); holder.dataset.webPrintParts = ''; paper.appendChild(holder);
        for (const part of sourceParts) holder.appendChild(printed.importNode(part, true));
        for (const details of holder.querySelectorAll('details')) details.open = true;
        printed.body.appendChild(paper);
        const refusal = printed.createElement('p'); refusal.className = 'web-print-frame-refusal';
        refusal.textContent = 'This edition is not ready to print. Return to the document and prepare the complete edition again.';
        printed.body.appendChild(refusal);
        const images = Array.from(holder.querySelectorAll('img'));
        for (const asset of descriptor.assets || []) {
          const uses = images.filter((image) => image.dataset.printAsset === asset.id);
          need(uses.length, 'A declared required illustration is missing from the edition.');
          const sourceURL = localURL(asset.href);
          need(uses.every((image) => !image.hasAttribute('src') && (image.alt.trim() || asset.role === 'decorative')), 'An illustration does not match its declared source or description.');
          const bytes = await (await fetchResource(sourceURL)).arrayBuffer();
          need(await hash(bytes) === asset.sha256, 'A required illustration failed verification.');
          unchanged();
          const url = URL.createObjectURL(new Blob([bytes], {type: asset.mime})); urls.push(url);
          await Promise.all(uses.map(async (image) => { image.src = url; await image.decode(); }));
          unchanged();
        }
        need(images.every((image) => (descriptor.assets || []).some((asset) => asset.id === image.dataset.printAsset)), 'An illustration was not declared by the canonical selection.');
        for (const font of descriptor.fonts || []) {
          const bytes = await (await fetchResource(font.href)).arrayBuffer();
          need(await hash(bytes) === font.sha256, 'A required font failed verification.');
          unchanged();
          const face = new frame.contentWindow.FontFace(font.family, bytes, {weight: font.weight || 'normal', style: font.style || 'normal', unicodeRange: font.unicode_range || 'U+0-10FFFF'});
          printed.fonts.add(await face.load());
        }
        await printed.fonts.ready;
        await new Promise((resolve) => frame.contentWindow.requestAnimationFrame(() => frame.contentWindow.requestAnimationFrame(resolve)));
        unchanged();
        need(JSON.stringify(descriptor) === requested.json, 'The selected print data changed during preparation.');
        active = null;
        prepared = {address, document: printed.documentElement.outerHTML, styles: styleState(printed), fontState: fontState(printed), fontFaces: Array.from(printed.fonts), descriptor: requested.json, width: paper.getBoundingClientRect().width, layoutVerified: false};
        need(ready(), prepared.problem || 'The complete edition is hidden, clipped or incomplete.');
        frame.contentWindow.addEventListener('beforeprint', () => {
          const valid = ready();
          printed.body.classList.toggle('web-print-frame-blocked', !valid);
          if (!valid) update('error', 'Print unavailable: ' + (prepared && prepared.problem || 'the prepared edition changed.'));
        });
        frame.contentWindow.addEventListener('afterprint', () => { if (generation === ownGeneration) startButton.focus({preventScroll: true}); });
        update('ready', 'The complete styled edition is ready.');
        cancelButton.hidden = true;
        root.removeAttribute('aria-busy');
        root.dispatchEvent(new CustomEvent('webprintready', {detail: {frame, descriptor}}));
        unchanged();
        need(ready(), prepared.problem || 'The prepared edition changed.');
        update('printing', 'Opening the complete edition in Print…');
        frame.contentWindow.focus();
        frame.contentWindow.print();
        if (generation === ownGeneration) update('ready', 'The complete edition was sent to Print.');
        return true;
      } catch (error) {
        if (generation === ownGeneration) reset('Print unavailable: ' + (error.message || error), 'error');
        return false;
      } finally {
        if (generation === ownGeneration) startButton.disabled = false;
      }
    }
    const controller = {start, cancel: () => reset('Preparation cancelled. No partial edition will print.', 'cancelled'), ready, state: () => state, frame: () => frame};
    installations.set(root, controller);
    startButton.addEventListener('click', () => { start(); });
    cancelButton.addEventListener('click', controller.cancel);
    for (const event of ['hashchange', 'popstate', 'pagehide']) window.addEventListener(event, () => reset('The selected address changed. Prepare the edition again.', 'cancelled'));
    window.addEventListener('beforeprint', () => { notice.textContent = 'Use the page’s Print action to prepare and print the complete styled edition.'; });
    startButton.hidden = false;
    cancelButton.hidden = true;
    update('idle');
    if (options.auto || new URLSearchParams(location.search).get('print') === '1') queueMicrotask(() => { start(); });
    return controller;
  }

  function bootstrap() {
    for (const root of document.querySelectorAll('[data-web-print-document]')) {
      try {
        const manifest = root.querySelector('script[data-web-print-manifest]');
        need(manifest && manifest.type === 'application/json', 'The canonical print descriptor is missing.');
        install(root, JSON.parse(manifest.textContent));
      } catch (error) {
        const status = root.querySelector('[data-web-print-status]');
        if (status) status.textContent = 'Print unavailable: ' + error.message;
        root.dataset.webPrintState = 'error';
      }
    }
  }
  window.TriptychWebPrint = Object.freeze({install, normalize, hash, structureEvents, validatePart, validateCardDeck, validateResponseGeometry, visibleAndUnclipped, descriptorCheck});
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', bootstrap, {once: true});
  else bootstrap();
}());
