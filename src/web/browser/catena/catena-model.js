/* ===========================================================================
 * The catena, as a model — the chapter view, derived, and derived only here
 * ===========================================================================
 *
 * THE ONE THING THIS FILE OWNS: which fragments stand under a chapter.
 *
 * `guidance/catena.md` Rule 5 stores a fragment at its natural extent — the
 * range the commentator actually addressed — and derives the chapter view.
 * Rule 6 then says a fragment whose extent crosses a chapter boundary appears
 * under every chapter it touches, once, at its full extent, and is never split
 * there, because splitting would attribute to one chapter words written about
 * another.
 *
 * Both are questions a reader asks, so both are answered here, at read time,
 * from the per-book file. NOTHING KEYED BY CHAPTER IS WRITTEN TO DISK. That is
 * not an optimisation, it is the point: a stored chapter table and a stored
 * extent are two representations of one fact, and this repository has already
 * been bitten by the pair disagreeing — `passage-commentary-index.yaml` answers
 * the same question at two granularities today and the answers differ.
 *
 * `catena check` runs THIS FILE under node against the solved cases in
 * `src/sources/commentary/fragment-loci.yaml`, exactly as `calendar-rubrics
 * check` runs the liturgy assembly model. So there is one derivation, and a
 * check that would fail if a second one were written beside it.
 *
 * It loads both as a browser global and as a node module, because the harness
 * needs the second and the page needs the first.
 * ======================================================================== */

'use strict';

(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.CatenaModel = api;
}(typeof self !== 'undefined' ? self : this, function () {

  /* ------------------------------------------------------------------------
   * The typed boundary — asked once, for the page and the model alike
   *
   * UNKNOWN OR MALFORMED STRUCTURED DATA MUST NOT BECOME visible prose, a
   * filter, a label, a count, or terminal state through implicit coercion or an
   * unchecked shape assumption. `String(x)` and `x || []` are both such
   * assumptions: the first turns a record into "[object Object]" and an array
   * into accidental comma-joined text, the second turns a string into a
   * container whose `.length` then counts characters as though they were works.
   *
   * A handful of questions answer that for every field this page displays.
   * They live HERE, beside the derivation, so the page and the model cannot
   * answer them differently — and because this file carries no byte ceiling,
   * asking them properly costs the composition nothing.
   *
   * V5 adds the three the V4.1 review proved were missing, and they are the
   * three that were being answered by coercion instead: what a NUMBER of this
   * corpus is, what a LANGUAGE CODE is, and what the MEMBERS of a collection
   * are. The last is the one that matters most. A container was validated and
   * its members were not, so a single malformed neighbour could throw out of
   * the render and take every valid sibling with it, or count itself into a
   * tally, or manufacture a refusal — and none of those is a fact the record
   * established.
   * --------------------------------------------------------------------- */

  /**
   * "Latin, Greek and English" — names joined as English joins them.
   *
   * Non-mutating: V3 rewrote this to `pop()` to buy bytes in the page, which
   * left a caller's array emptied as a side effect and the precondition pinned
   * by a test rather than by the code. This file carries no ceiling, so the
   * safe form is simply affordable here.
   */
  function joinNames(names) {
    const said = list(names).map(sound).filter(Boolean);
    if (said.length < 2) return said[0] || '';
    return said.slice(0, -1).join(', ') + ' and ' + said[said.length - 1];
  }

  // ISO 639 codes the shared language table lacks. Data, so the page spends no
  // ceiling carrying it; the shared fallback still names everything else.
  const LANGUAGE_NAMES = { grc: 'Greek', el: 'Greek', he: 'Hebrew', syr: 'Syriac' };

  // How a code becomes a name. The page installs the shared table's namer as
  // the fallback; this file never reaches for `window.Triptych`, because it is
  // loaded under node by `catena check` where no such global exists.
  let nameLanguage = (code) => LANGUAGE_NAMES[code] || sound(code);

  function useLanguageNames(namer) {
    nameLanguage = (code) => LANGUAGE_NAMES[code] || namer(code);
  }

  /** The original is named only by itself; a translation, by its language. */
  function voicePhrase(entry) {
    if (!entry) return '';
    if (entry.voice === ORIGINAL) return 'the author\u2019s own language';
    return nameLanguage(entry.language) + ' translation';
  }

  /** The same, opening a label. */
  function voiceLabel(entry) {
    const phrase = voicePhrase(entry);
    return phrase.charAt(0).toUpperCase() + phrase.slice(1);
  }

  /** One code, named. The page asked this two ways and they must not differ. */
  function sayLanguage(code) {
    return nameLanguage(code);
  }

  /**
   * The chip beside a fragment: "Latin — the author's own", "English
   * translation", the bare name where the voice was never established, or ''
   * where the language was not one. Prose derived from a typed record, so it
   * is derived HERE, beside `voicePhrase` and `voiceLabel`, which already are.
   */
  function languageChip(entry) {
    const record = bag(entry);
    const code = tongue(record.language);
    if (!code) return '';
    const said = nameLanguage(code);
    const voice = sound(record.voice);
    return voice === ORIGINAL
      ? said + ' — the author’s own'
      : voice === TRANSLATION ? said + ' translation' : said;
  }

  /** Text, trimmed, or nothing. Never a coerced record, list, number or flag. */
  function sound(value) {
    return typeof value === 'string' ? value.trim() : '';
  }

  /** A container, or nothing. A SCALAR IS NOT A ONE-ITEM LIST. */
  function list(value) {
    return Array.isArray(value) ? value : [];
  }

  /** A record, or nothing. A list and a string are both refused. */
  function bag(value) {
    return value && typeof value === 'object' && !Array.isArray(value) ? value : {};
  }

  /**
   * A number AS THE DATA CARRIES IT, or nothing.
   *
   * Not `Number(value)`: that coercion accepts `"1"` and, worse, accepts `[1]`,
   * because a one-member list numifies to its member. Every extent member in
   * the tracked corpus is an integer, so a member that is not one is a
   * malformed record and not a locus to be printed.
   */
  function count(value) {
    return typeof value === 'number' && Number.isFinite(value) ? value : null;
  }

  /** A fact that may legitimately arrive as a finite number, or else as text. */
  function say(value) {
    return Number.isFinite(value) ? String(value) : sound(value);
  }

  /**
   * A number this corpus COUNTS BY — a positive safe integer — or nothing.
   *
   * `count` asks only whether a number arrived. This asks whether it is one of
   * the things this corpus writes as whole positive numbers: a chapter, a
   * verse, a word tally, a digit width. `0`, `-3`, `1.5`, `1e21`, `"4"`, `[4]`
   * and `true` are each a malformed record in those places, and a malformed
   * record is not floored, rounded or coerced into a number to print. The
   * distinction is not pedantry: `Number(x) > 0` accepted `true` and printed
   * "1 words", and accepted `[4]` for a chapter, which put a fragment into a
   * chapter's count that the same record could not give a locus for.
   */
  function whole(value) {
    return typeof value === 'number' && Number.isSafeInteger(value) && value > 0
      ? value
      : null;
  }

  /**
   * A language code fit to be named, shown, or written into a DOM `lang`.
   *
   * NONEMPTY TEXT IS NOT ENOUGH HERE, and this is the one gate in the file
   * that tests a shape rather than a type. `lang` is machine-read metadata: a
   * browser picks a font and hyphenation from it, a screen reader picks a
   * voice, a search engine picks an index. A value that is not a language
   * subtag must therefore not be written at all — least of all
   * `[object Object]`, which is exactly what an unchecked record became when
   * it reached the attribute, in real Chromium, on an otherwise complete page.
   *
   * The form is the one the corpus writes and the route grammar already
   * enforces: two or three letters, and the subtags a code may legitimately
   * carry after them.
   */
  function tongue(value) {
    const code = sound(value);
    return /^[A-Za-z]{2,3}(-[A-Za-z0-9]{2,8})*$/.test(code) ? code : '';
  }

  /**
   * The narrower form a VOICE KEY may carry, and the one authority for it.
   *
   * Narrower than `tongue` on purpose. A voice key becomes a control value
   * and a URL, and the page must accept back the addresses it issues: the
   * published route grammar is two or three lowercase letters and nothing
   * else. Composed from anything wider — `en-GB`, an uppercase code, a
   * record — the page writes a link into history and then refuses it on the
   * way back in, which is the self-refusing address V4 recorded and fixed for
   * records alone. The grammar is stated HERE so `voiceKey`, `chapterVoices`
   * and the route's own validation cannot come to hold three opinions of it.
   */
  function voiceLanguage(value) {
    const code = sound(value);
    return /^[a-z]{2,3}$/.test(code) ? code : '';
  }

  /**
   * A TEXTUAL IDENTITY OF THIS CORPUS'S OWN GRAMMAR, or ''.
   *
   * V6, and the one the V5 review proved was still missing. `sound()` asks
   * whether text arrived; it does not ask whether the text NAMES anything
   * here. A fragment id becomes a fetched path and a Source Library href, a
   * book path becomes a directory in a URL, an edition id becomes both a route
   * value and a request — so `"../../etc/passwd"`, `"a b"` and arbitrary prose
   * are each sound text and none of them is an identity this corpus issued.
   *
   * The form is the one the generator writes and every tracked identity
   * satisfies: lowercase alphanumeric runs joined by a single `.` or `-`.
   * 1,351 fragment ids, 12 work ids, 73 canon paths and 7 edition ids pass it
   * unchanged, so it refuses nothing the corpus holds.
   */
  function ident(value) {
    const said = sound(value);
    return /^[a-z0-9]+([.-][a-z0-9]+)*$/.test(said) ? said : '';
  }

  /**
   * A BOOK TOKEN, or ''. Wider than `ident` because the canon writes them as
   * the abbreviations a reader cites — `Gen`, `1Kings`, `Philem` — and they
   * are the one identity the published hash grammar carries verbatim. Wider,
   * and still closed: a token reaches `loadChapter` and becomes a directory in
   * a request, so it may hold no separator but the hyphen and no case but the
   * letters. All 73 tracked tokens pass.
   */
  function bookToken(value) {
    const said = sound(value);
    return /^[A-Za-z0-9]+(-[A-Za-z0-9]+)*$/.test(said) ? said : '';
  }

  /**
   * A RELATIVE DIRECTORY this page may compose a request against, or ''.
   *
   * Segments of `ident`'s grammar, each closed by one slash. No leading slash,
   * no `..`, no empty segment, no query and no scheme: a path that is not one
   * of this data root's own directories is not made into a URL at all. Every
   * tracked `path` and `text_prefix` passes.
   */
  function trail(value) {
    const said = sound(value);
    return /^([a-z0-9]+([.-][a-z0-9]+)*\/)+$/.test(said) ? said : '';
  }

  /**
   * A RELATIVE JSON FILE this page may request, or ''.
   *
   * V7, and the sink the V6 review proved was still open. `trail` states what a
   * DIRECTORY of this data root looks like; nothing stated what a FILE looks
   * like, so a `text_path` the record carried was handed to `fetch` on the
   * strength of being truthy. A trail of `trail`'s own segments, one `ident`
   * stem, and the `.json` suffix the corpus writes: an object, a list, a
   * number, a flag, `''`, `'   '`, `'../../etc/passwd'`, `'/etc/passwd'`,
   * `'%2e%2e%2fsecret.json'` and `'a b.json'` are each refused here rather than
   * three guards later, because the guard that was three guards later was the
   * one that did not exist.
   */
  function leaf(value) {
    const said = sound(value);
    return /^([a-z0-9]+([.-][a-z0-9]+)*\/)+[a-z0-9]+([.-][a-z0-9]+)*\.json$/.test(said)
      ? said
      : '';
  }

  /**
   * The members of a list that are RECORDS, and only those.
   *
   * A collection is validated member by member, because a malformed neighbour
   * establishes nothing about its neighbours. A scalar, a list and a null are
   * each refused where a record was written; the valid siblings stand; and
   * whatever is counted afterwards is a count of what stood. `list()` alone
   * left `null` members to throw out of the render tail — one malformed row
   * replacing the whole page with a JavaScript error — and left scalars to
   * render as blank rows that were nonetheless tallied as works.
   */
  function records(value) {
    return list(value).filter(
      (one) => one !== null && typeof one === 'object' && !Array.isArray(one));
  }

  /**
   * Does this extent touch this chapter?
   *
   * Inclusive at both ends and stated over chapters alone. A fragment on
   * Genesis 1:1-2:2 touches chapter 1 and chapter 2; one on Genesis 1:3-1:5
   * touches chapter 1 only. The verses do not enter: a fragment that reaches
   * into a chapter at all is about that chapter, and asking whether it reaches
   * "enough" of it would be a judgment no data here supports.
   */
  function touchesChapter(extent, chapter) {
    // THE SAME NUMBERS THE LOCUS IS PRINTED FROM. `Number()` here and `count()`
    // in `formatExtent` were two answers to one question, and they disagreed:
    // `first_chapter: [1]` coerced to 1 and put the fragment into chapter 1's
    // COUNT, while the label refused the same member and printed the book
    // alone. A fragment whose extent cannot be read stands under no chapter,
    // rather than under one it cannot be shown to address.
    const first = whole(bag(extent).first_chapter);
    const last = whole(bag(extent).last_chapter);
    const wanted = whole(chapter);
    if (first === null || last === null || wanted === null) return false;
    return first <= wanted && wanted <= last;
  }

  /** Every fragment standing under one chapter, in the order it was given. */
  function fragmentsOnChapter(fragments, chapter) {
    return records(fragments).filter(function (fragment) {
      return touchesChapter(fragment.extent, chapter);
    });
  }

  /**
   * "Genesis 1:1-2:2", "Genesis 1:4-5", "Genesis 1:4" — the full extent, always.
   *
   * Rule 6 again, on the label this time. A fragment shown under Genesis 2 must
   * still say it runs from 1:1, or the reader is told Augustine wrote about
   * chapter 2 when he wrote across the seam.
   */
  function formatExtent(extent, bookName) {
    const range = bag(extent);
    const book = sound(bookName) || sound(range.token);
    const firstChapter = whole(range.first_chapter);
    const lastChapter = whole(range.last_chapter);
    const firstVerse = whole(range.first_verse);
    const lastVerse = whole(range.last_verse);
    // A RANGE THIS RENDERER CANNOT STATE IS NOT GUESSED AT. The four members are
    // validated as the numbers the format is written in; anything else — a
    // structured member, an absent one, a list — leaves the book standing alone
    // rather than printing "Genesis [object Object]:1" or "Genesis
    // undefined:undefined" as though a locus had been established. The
    // structure is left for a renderer that understands it, not flattened.
    if (firstChapter === null || lastChapter === null ||
        firstVerse === null || lastVerse === null) {
      return book;
    }
    // AND A RANGE THAT RUNS BACKWARDS IS NOT A RANGE. Four sound numbers in the
    // wrong order describe no passage, and printing "Genesis 5:1-2:3" would
    // hand the reader a locus the record never established.
    if (lastChapter < firstChapter ||
        (lastChapter === firstChapter && lastVerse < firstVerse)) {
      return book;
    }
    const first = firstChapter + ':' + firstVerse;
    if (firstChapter !== lastChapter) {
      return book + ' ' + first + '-' + lastChapter + ':' + lastVerse;
    }
    if (firstVerse === lastVerse) return book + ' ' + first;
    return book + ' ' + first + '-' + lastVerse;
  }

  /** Does this fragment cross a chapter boundary? The page says so when it does. */
  function spansChapters(extent) {
    // A CROSSING IS A CLAIM, so it is made only from two real numbers: two
    // arrays are never `===`, and comparing them coerced announced a boundary
    // crossing for a record that established no boundary at all.
    const first = whole(bag(extent).first_chapter);
    const last = whole(bag(extent).last_chapter);
    return first !== null && last !== null && last > first;
  }

  /**
   * A chapter file's fragments, PROJECTED — one typed record each, or none.
   *
   * =======================================================================
   * V7, AND THE CENTRE OF THE V6 REVIEW. This function used to SHALLOW-COPY.
   * =======================================================================
   *
   * The spine writes the author, the work, the date, the language, the printing,
   * the translators and the rights ONCE per distinct set of them under
   * `sources` — on Genesis 1 that saves 107 copies of ten fields, and every
   * copy was a chance for two of them to disagree. The join happens here, at
   * read time, which is where `browser-core.js` says joins belong.
   *
   * V6 joined by copying every own property of the shared record and then of
   * the fragment, and clearing afterwards the two it knew were dangerous.
   * `text_path` was cleared only when the composed form could be built, so a
   * fragment whose id or prefix was unreadable kept whatever `text_path` the
   * RECORD carried and `openFragment` handed it to the real request sink:
   * `'../../../etc/passwd'` is a string, and a string was all the copy asked
   * for. Every other unknown property came through untouched, so the boundary
   * had to be re-established at every later sink — which is why V4, V5 and V6
   * each found one more sink where it had not been.
   *
   * V7 projects: known fields, each validated for the use the page puts it to,
   * and nothing else crosses. There is no `joined[name] = raw[name]` here and
   * there must not be one again. Everything downstream reads this record.
   *
   * A member naming NOTHING of itself is not a thin fragment; it is not a
   * fragment. `{}` rendered a blank row and was counted into "3 fragments held
   * here" — possession claimed by an empty object.
   */

  /**
   * The fields the fold moves to `sources`, and the ONLY ones a fragment may
   * inherit from its edition.
   *
   * `_fold_shared` in `scripts/_catena.py` writes these once per edition; the
   * identity, the locus, the review state and the word tally are the
   * fragment's own. V7's first draft looked every field up through the
   * fallback, which let a fragment inherit its `id` — and so its Source
   * Library href and the one request it can cause — from its edition, so two
   * fragments of one edition linked to one passage and fetched one file. No
   * tracked source carries an `id`, so nothing real did it; it is a widening
   * of exactly the field this projection guards. `attribution`,
   * `rights_basis` and `acknowledgement` are here because they are terms of
   * the edition, and because V6 already read them that way.
   */
  const SHARED_WITH_EDITION = [
    'work_id', 'author', 'work', 'date', 'language', 'voice', 'edition',
    'edition_published', 'translators', 'container', 'rights', 'attribution',
    'rights_basis', 'acknowledgement'];

  /** One fragment as this page may use it, or null. */
  function fragmentRow(fragment, sources, prefix) {
    // THE SOURCE KEY IS A PROPERTY LOOKUP, and V6's review proved a lookup is a
    // coercion: `sources[["1"]]` is `sources["1"]`, so a one-member LIST
    // silently took a real edition's author, rights and language for a fragment
    // that named no edition at all — and `sources["constructor"]` is a
    // function, which `bag` refuses but the raw index did not. Only a string
    // that the record itself carries as its own key joins anything.
    // `bag`, because this is an exported entry point and a caller is not
    // `chapterFragments`; inside, `records()` has already asked.
    const own = bag(fragment);
    const held = bag(sources);
    const key = own.source;
    const shared = typeof key === 'string' && Object.hasOwn(held, key)
      ? bag(held[key])
      : {};
    // The fragment's own statement wins over its edition's, as the fold
    // intends — and only a field the fold actually shares may be inherited.
    const said = (name) =>
      Object.hasOwn(own, name) ? own[name]
        : SHARED_WITH_EDITION.includes(name) && Object.hasOwn(shared, name)
          ? shared[name] : undefined;

    // THE ID BECOMES A FETCHED PATH AND A LINK. A truthy test let a record
    // through and composed `…/[object Object].json`, which the page then
    // requested; sound text alone still let arbitrary prose and a path-like
    // string through. Read off the fragment ALONE, never off its edition.
    const id = ident(own.id);
    const author = sound(said('author'));
    const work = sound(said('work'));
    // THE LEAST A FRAGMENT MUST SAY. Not "is an object": a fragment row is the
    // page stating that this project holds this commentary here, and a record
    // that can name neither the passage's own identity, nor its author, nor
    // its work states no part of that.
    //
    // The names are read through the JOIN, deliberately. Every fragment of the
    // tracked corpus states its author and its work only through its edition,
    // so asking the fragment's own record for them would refuse all 1,351 of
    // them; and V6 settled, and its review left standing, that a fragment
    // whose id alone is unreadable still renders and still counts — it is a
    // fragment held here minus one fact. The cost is that `{source: "0"}`, a
    // record stating nothing whatever but which edition it belongs to, borrows
    // that edition's author and work and is counted. `REVIEW_REQUEST.md` asks
    // about that case rather than moving the line on it a second time: V6's
    // request asked the same question and the review did not answer it.
    if (!id && !author && !work) return null;

    const extent = bag(said('extent'));
    const voice = sound(said('voice'));
    return {
      id: id,
      // COMPOSED, NEVER CARRIED. The file states once where its fragment texts
      // live and the fragment states its own identity; the request is built
      // from those two validated values and from nothing else. Where the file
      // states no prefix — the sample corpus does not — a `text_path` the
      // record itself carries may stand in, but only when it is a relative
      // JSON file of this data root's own grammar AND its stem is this
      // fragment's own validated id. So the path can address one thing: the
      // text of the fragment that carried it. An injected path names some
      // other file by definition, and is discarded here, before projection
      // completes, rather than guarded at the fetch.
      text_path: id
        ? (prefix ? prefix + id + '.json'
          : leaf(own.text_path).endsWith('/' + id + '.json')
            ? leaf(own.text_path)
            : '')
        : '',
      author: author,
      work: work,
      date: say(said('date')),
      language: tongue(said('language')),
      // The two the corpus derives, and there is no third; anything else
      // establishes no voice and answers no selection.
      voice: voice === ORIGINAL || voice === TRANSLATION ? voice : '',
      // A TALLY IS A NUMBER THE RECORD WROTE, not one `Number()` can make.
      text_words: whole(said('text_words')),
      // The same four numbers the locus is printed from and the chapter
      // membership is decided by, asked once so the two cannot disagree.
      extent: {
        token: bookToken(extent.token),
        first_chapter: whole(extent.first_chapter),
        last_chapter: whole(extent.last_chapter),
        first_verse: whole(extent.first_verse),
        last_verse: whole(extent.last_verse)
      },
      locator: sound(said('locator')),
      edition: sound(said('edition')),
      edition_published: sound(said('edition_published')),
      translators: list(said('translators')).map(sound).filter(Boolean),
      rights: sound(said('rights')),
      attribution: sound(said('attribution')),
      rights_basis: sound(said('rights_basis')),
      review: sound(said('review')),
      // The licence travels above the words, so the two states are kept apart:
      // a note that is sound text, and a note that ARRIVED and is not text.
      // Collapsing them printed nothing where the record had said something
      // unreadable, and the page owes the reader the difference.
      acknowledgement: sound(said('acknowledgement')),
      acknowledgement_broken: broken(said('acknowledgement'))
    };
  }

  /** Was something recorded here that this page cannot read as text? */
  function broken(value) {
    return value !== undefined && value !== null && value !== '' && !sound(value);
  }

  /**
   * Is this chapter spine a document this page cannot read as one?
   *
   * V7, second pass. The correction gave the chapter PAYLOAD a third answer —
   * a 200 carrying `null`, a list or a string is a request that succeeded
   * carrying no spine — and stopped one level too shallow. `fragments` as a
   * record came through as readable, `records()` made it `[]`, and the page
   * printed "No commentary on this chapter is held yet" over a chapter its
   * own index says holds 1,351. `sources` as a list blanked the author, work,
   * edition, printing, translators and RIGHTS of all 107 fragments while
   * still stating possession of them. And an unreadable `refusals` root
   * dropped Rule 4's refusal in silence — the strongest claim this page
   * makes, failing OPEN.
   *
   * `fragments: []` is legitimate and common, so this asks about SHAPE and
   * never about emptiness.
   *
   * `leads`, `blocked`, a per-edition refusal list and `text_prefix` are
   * deliberately NOT here: V5 and V6 each settled those and their reviews
   * accepted them, and reversing an accepted decision is not this file's to
   * do. `REVIEW_REQUEST.md` asks about the one whose copy is imprecise.
   */
  function spineUnreadable(file) {
    const record = bag(file);
    if (record !== file) return true;
    if (!Array.isArray(record.fragments)) return true;
    if (record.sources !== undefined && bag(record.sources) !== record.sources) return true;
    if (record.refusals !== undefined && bag(record.refusals) !== record.refusals) return true;
    return false;
  }

  /** Every fragment of one chapter file that can be one, in the order given. */
  function chapterFragments(file) {
    const sources = bag(bag(file).sources);
    // `trail`, not `sound`: the prefix is the head of a URL this page requests.
    const prefix = trail(bag(file).text_prefix);
    const rows = [];
    // `records` rather than `file.fragments || []`: a spine whose `fragments`
    // is a record or a string is a broken record, and mapping over it threw out
    // of the render tail — past `aria-busy`, past the tally, past the
    // announcement. Its MEMBERS are asked the same question, because a `null`
    // among them threw on the very next line and took every valid sibling with
    // it, and a scalar among them became a blank row that was still counted.
    for (const fragment of records(bag(file).fragments)) {
      const row = fragmentRow(fragment, sources, prefix);
      if (row) rows.push(row);
    }
    return rows;
  }

  /**
   * One fragment's own text payload, projected, or the fact that it is not one.
   *
   * V7. `sound(loaded.text)` normalized a record, a list and a number alike to
   * `''`, so a payload that arrived unreadable rendered as an EMPTY paragraph
   * and the route finished without ever saying the words could not be read.
   * Nothing was shown and nothing was claimed, which reads to a reader exactly
   * like a fragment whose text is blank.
   */
  function textPayload(loaded) {
    const record = bag(loaded);
    const text = sound(record.text);
    return {
      // A payload is a record that states its words. Anything else — a list, a
      // string, a number, a record whose `text` is not text — is a file this
      // page could not read, and it says so instead of showing nothing.
      unreadable: record !== loaded || !text,
      text: text,
      basis: sound(record.basis),
      date_basis: sound(record.date_basis),
      acknowledgement: sound(record.acknowledgement),
      acknowledgement_broken: broken(record.acknowledgement)
    };
  }

  /* ------------------------------------------------------------------------
   * The index, and the addresses derived from it
   *
   * Every one of these answers a question the page used to answer by string
   * concatenation over raw record members — which is how `[object Object]`
   * reached a fetched URL, and how a malformed index member threw during
   * startup and left the page saying "Loading…" for ever.
   * --------------------------------------------------------------------- */

  /**
   * One canon entry as this page may use it, or null.
   *
   * A book must be able to state its own token, its own name and how many
   * chapters it has before the page may put it in a control, range an address
   * against it, or write its name into a heading. A member that cannot is not
   * a book of the canon so far as this page is concerned, and is left out
   * rather than rendered as `undefined` or counted as a book.
   */
  // The two testaments this canon divides itself into, and the words the page
  // is licensed to print for each. There is no third, and no default: an
  // `else` here printed "New Testament" over a book whose record said
  // `{"half": "old"}`, which is a claim about the canon made out of a value
  // nobody could read.
  const TESTAMENTS = { old: 'Old Testament', new: 'New Testament' };

  function canonBook(entry) {
    const record = bag(entry);
    // `bookToken`: the token becomes a directory inside a chapter request.
    const token = bookToken(record.token);
    const name = sound(record.name);
    const chapters = whole(record.chapters);
    if (!token || !name || chapters === null) return null;
    const testament = sound(record.testament);
    const stated = Object.hasOwn(TESTAMENTS, testament);
    return {
      token: token,
      name: name,
      chapters: chapters,
      testament: stated ? testament : '',
      // The words themselves, derived here beside the value that licenses
      // them, so the page cannot say one while holding the other.
      testamentName: stated ? TESTAMENTS[testament] : '',
      // `ident`: the path becomes a directory in a paragraph-layer request.
      path: ident(record.path)
    };
  }

  /** Every book of the canon this page can state, in the order given. */
  function canonBooks(canon) {
    const books = [];
    for (const entry of records(canon)) {
      const book = canonBook(entry);
      if (book) books.push(book);
    }
    return books;
  }

  /** One of them by its token, or null. */
  function bookOf(canon, token) {
    const wanted = sound(token);
    if (!wanted) return null;
    return canonBooks(canon).find((book) => book.token === wanted) || null;
  }

  /**
   * Where one chapter's spine stands: its path, `''` where nothing is held on
   * that chapter, or `null` where the record cannot say either.
   *
   * THE THIRD ANSWER IS THE POINT OF THE FUNCTION. "Nothing held here" is a
   * claim about the corpus, and a record this page cannot read establishes no
   * such claim; a malformed `present` list or a malformed `path` must reach
   * the page's broken-record notice instead, because an absence inferred from
   * a parse failure is precisely the manufactured negative this boundary
   * exists to refuse. The path itself is composed only from sound text and a
   * whole number: a request for `…/[object Object].json` is a request against
   * nothing, and this page does not make it.
   */
  function chapterPath(index, token, chapter) {
    const wanted = bookToken(token);
    // A BOOK THIS PAGE CANNOT NAME IS NOT A BOOK THE INDEX IS EMPTY OF. V6
    // answered `''` here, which the page reads as recorded emptiness.
    if (!wanted) return null;
    const root = bag(index).held;
    // AND NEITHER IS A HOLDINGS RECORD THAT IS NOT A LIST. `records()` turns a
    // string, a number and a record alike into `[]`, so V6 read every one of
    // them as "this index holds nothing in this book", of every book, and the
    // page said `Nothing held here` over a root it had entirely failed to
    // read. The distinction this whole function exists for is exactly that
    // one: we read the corpus and found nothing, against we could not
    // establish what the corpus holds.
    if (!Array.isArray(root)) return null;
    // EVERY entry for this book, not the first object-shaped one. The V5
    // review proved a malformed same-token record masked a valid sibling
    // standing behind it: `find` stopped at the broken one and the whole book
    // became an unreadable record, though the index stated it perfectly well
    // one member later. Nothing here depends on which order they arrive in.
    //
    // A member that cannot state WHICH BOOK it is about is not merely skipped:
    // it might have been this one, so no emptiness can be drawn from the list
    // that carries it.
    // `readable` is carried through BOTH loops below, and that is the whole of
    // it: V7's first draft consulted it only where no entry for this book was
    // found, so once one readable entry existed the second loop could still
    // answer `''` — a recorded emptiness — with an unreadable sibling standing
    // beside it that might have recorded the very chapter being asked for.
    const held = [];
    let readable = true;
    for (const entry of root) {
      const record = bag(entry);
      const named = record === entry ? bookToken(record.token) : '';
      if (!named) readable = false;
      else if (named === wanted) held.push(record);
    }
    // The index holds nothing at all in this book, and says so of every
    // chapter in it. That is a real, recorded emptiness — and only where every
    // member of the list could be read.
    if (!held.length) return readable ? '' : null;
    const number = whole(chapter);
    if (number === null) return null;
    // A DIGIT WIDTH NOBODY CAN READ COMPOSES THE WRONG PATH. V6 fell back to
    // 1, so a malformed `chapter_digits` sent a real request for a file that
    // cannot exist and reported the 404 as a broken record. Absent is the
    // documented default; present and unreadable is an unreadable index.
    const stated = bag(index).chapter_digits;
    if (stated !== undefined && whole(stated) === null) return null;
    const digits = whole(stated) || 1;
    // '' only if some entry could be read and truthfully recorded no chapter
    // here; `null` if none could be read at all. An absence is a claim, so it
    // is drawn only from a record that states one.
    let recorded = null;
    for (const entry of held) {
      const prefix = trail(entry.path);
      if (!prefix || !Array.isArray(entry.present)) { readable = false; continue; }
      let listed = true;
      let present = false;
      for (const one of entry.present) {
        // A member this page cannot read makes THAT list unreadable, because
        // a chapter's absence from an unreadable list proves nothing.
        if (whole(one) === null) { listed = false; break; }
        if (one === number) present = true;
      }
      if (!listed) { readable = false; continue; }
      if (present) return prefix + String(number).padStart(digits, '0') + '.json';
      recorded = '';
    }
    // `''` only where every record that could have spoken for this book did.
    return readable ? recorded : null;
  }

  /**
   * Where this edition opens paragraphs in one chapter: its path, `''` where
   * this edition publishes no such layer, or `null` where the layer root
   * cannot be read at all.
   *
   * `''` is not a claim about the chapter: the layer is the EDITION's own, and
   * an edition that publishes none of it leaves every chapter running on,
   * truthfully. What it does mean is that no request is made — a malformed
   * edition record or book path never becomes a fetched URL.
   *
   * V7 adds the third answer for the reason `chapterPath` has one. The V6
   * review proved that a layer root arriving as a string, a list or a number
   * came through `bag()` as `{}` and then out of here as `''`, and the page
   * printed "No paragraph division is held for this chapter in this edition"
   * — a claim about how an edition sets its text, drawn from a file nobody
   * could read.
   */
  function paragraphPath(layer, edition, bookPath, chapter) {
    // A layer that answered 404 is no layer, and that is the absence the page
    // may speak from. The route marks it, because `null` cannot: JSON `null`
    // is a valid document and a 200 carrying it is a file nobody can read,
    // which V7's first pass read as the 404 and printed as an edition that
    // opens no paragraph here.
    // `undefined` is never fetched; `absent` is the route's mark for the 404.
    // `null` is NOT here: a 200 answering JSON `null` is a file nobody could
    // read, and reading it as the 404 is what printed an edition that opens
    // no paragraph here over a layer root that had failed.
    if (layer === undefined || bag(layer).absent === true) return '';
    const index = bag(layer);
    if (index !== layer) return null;
    // The EDITION KEY is a property lookup again, so it is an identity this
    // corpus issued or it is nothing: `editions[["douay-rheims"]]` resolved a
    // real layer for a value that named no edition.
    const editions = bag(index.editions);
    if (index.editions !== undefined && editions !== index.editions) return null;
    const key = ident(edition);
    // This edition publishes no paragraph layer at all. A real absence, and
    // the one answer here that lets the page say the chapter runs on.
    if (!key || !Object.hasOwn(editions, key)) return '';
    // FROM HERE DOWN EVERY FAILURE IS UNREADABILITY, NOT ABSENCE. V7's first
    // draft answered `''` for an edition record that is not a record and for a
    // `path` that is not a trail, so a member of the layer nobody could read
    // was printed as this edition opening no paragraph here — the same
    // manufactured negative the rest of this function exists to refuse.
    const record = bag(editions[key]);
    if (record !== editions[key]) return null;
    const prefix = trail(record.path);
    const book = ident(bookPath);
    const number = whole(chapter);
    if (!prefix || !book || number === null) return null;
    // AND A DIGIT WIDTH NOBODY CAN READ COMPOSES THE WRONG PATH, exactly as it
    // did in `chapterPath`: the request goes out, 404s, and the 404 is read as
    // an edition that opens no paragraph here.
    const stated = index.chapter_digits;
    if (stated !== undefined && whole(stated) === null) return null;
    return prefix + book + '/' +
      String(number).padStart(whole(stated) || 1, '0') + '.json';
  }

  // The two claims a recorded paragraph break may make, and there is no third.
  const BREAK_KINDS = ['printed', 'projected'];

  /**
   * The verses of one chapter, in order, each with the mark that opens it.
   *
   * Three separate coercions used to live in this loop. The KEY was read with
   * `Number()`, which took `" 3 "`, `"3.0"` and `"1e3"` for verses the chapter
   * never numbered and sorted them among the ones it did. The VALUE was
   * concatenated raw, so a record printed `[object Object]` and a list printed
   * itself comma-joined, as Scripture. And the MARK was tested for truth
   * alone, so any value at all opened a paragraph while counting as neither
   * kind — leaving the page to print paragraphs and, beneath them, the note
   * saying no paragraph division is held for this chapter.
   */
  function chapterLines(verses, breaks) {
    const said = bag(verses);
    const marks = bag(breaks);
    const lines = [];
    for (const key in said) {
      if (!Object.hasOwn(said, key)) continue;
      // THE CANONICAL FORM, AND ONLY IT. `^[0-9]+$` admitted `"01"` and
      // `"001"` beside `"1"`, and `Number()` folded all three onto verse 1 —
      // so a chapter carrying two encodings of one verse rendered verse 1
      // twice, in two paragraphs, each claiming to be the verse the edition
      // numbers 1. There is one way this corpus writes a verse number and a
      // padded key is not it; a noncanonical encoding is a malformed key, not
      // a second verse and not a silent overwrite of the first.
      if (!/^[1-9][0-9]*$/.test(key)) continue;
      const number = whole(Number(key));
      const text = sound(said[key]);
      if (number === null || !text) continue;
      const kind = sound(marks[key]);
      lines.push({
        number: number,
        text: text,
        kind: BREAK_KINDS.includes(kind) ? kind : ''
      });
    }
    return lines.sort((a, b) => a.number - b.number);
  }

  /**
   * One chapter of Scripture, read: its lines, and what could not be read.
   *
   * V7, and the two false claims the V6 review found on this seam. Both come
   * from the same mistake — reading the ABSENCE OF A READABLE VALUE as a
   * recorded fact about the edition.
   *
   *   `versesUnread`  "Carries no verses" and "arrived in a form this page
   *                   cannot read" were told apart by counting the keys of
   *                   `bag(verses)`, which is `{}` for a list, a string and a
   *                   number alike — so a payload whose `verses` was a LIST was
   *                   reported as a chapter of Scripture with no verses in it.
   *                   `loadChapter` admits an array (`typeof [] === 'object'`)
   *                   and belongs to the shared shell, so the distinction is
   *                   drawn here.
   *
   *   `marksUnread`   A paragraph file that arrived unreadable produced no
   *                   marks, and no marks was printed as "No paragraph division
   *                   is held … so it runs on" — a claim about how the edition
   *                   sets its text. `null`, the 404 that means the chapter
   *                   genuinely runs on, is not unread and is the one case that
   *                   may speak.
   */
  function chapterReading(verses, marks) {
    const said = bag(verses);
    const layer = bag(marks);
    const readable = said === verses;
    const lines = chapterLines(verses, layer.breaks);
    const breaks = bag(layer.breaks);
    return {
      lines: lines,
      // Not a record, or a record whose keys yielded no line it could read.
      // A record with no keys at all is the edition recording no verse here,
      // which is a fact about the edition and stays sayable.
      versesUnread: !readable ||
        (!lines.length && Object.keys(said).length > 0),
      // `unfetched` is the route's own word for a record that was expected
      // and would not come — the same one `chapterFile` answers with for the
      // spine — and the paragraph ROOT arriving unreadable is carried here in
      // it. `absent` is the route's mark for a 404, which is the one answer
      // that means the chapter genuinely runs on; `null` cannot carry it,
      // because a 200 answering JSON `null` is a file nobody could read and
      // V7's first pass printed it as an edition that divides nothing.
      //
      // A record with NO `breaks` key is unreadable too. All 5,547 tracked
      // paragraph files carry one and none is empty, so a paragraph file
      // without it states nothing about how this chapter divides.
      marksUnread: !!layer.unfetched ||
        (marks !== undefined && layer.absent !== true &&
          (layer !== marks || breaks !== layer.breaks))
    };
  }

  /* ------------------------------------------------------------------------
   * Why a work standing here is not held in the asked-for language
   *
   * THE FINDING IS THE FACT, and the page had been throwing it away. The
   * generator writes one of four, closed at `scripts/_catena.py` so that a
   * fifth answer has to be argued for rather than typed, and they say
   * different things:
   *
   *   none-published         no translation exists, of any date — about the world
   *   in-copyright           one exists and may not be republished — about the law
   *   partial-public-domain  some public-domain text, not the whole — an offer
   *   not-surveyed           nobody has looked — an admission, and NOT a negative
   *
   * The page used to read none of them. It classified a row by whether a
   * `partial` string happened to be attached, which put `not-surveyed` — the
   * one finding that explicitly declines to make a claim — into the sentence
   * "no English this project may publish". That is a holdings claim the
   * corpus never made, and it is manufactured out of an admission that nobody
   * looked. A finding this file does not recognise is treated the same way an
   * unknown finding must be: it is carried, and it claims nothing.
   * --------------------------------------------------------------------- */

  // What each finding lets the page SAY. No new taxonomy: these are the
  // generator's own four, and the empty answer is the absence of one.
  const FINDINGS = {
    'none-published': 'closed',
    'in-copyright': 'closed',
    'partial-public-domain': 'untaken',
    'not-surveyed': 'unsurveyed'
  };

  /**
   * One row per distinct work standing under this chapter that the record
   * says something about in this language, in the order the spine gives them.
   *
   * Every field is typed at the read, and a malformed neighbour costs its
   * siblings nothing: a valid typed finding survives a malformed `reason`
   * beside it, and a malformed member of the recorded list is passed over
   * rather than allowed to stand in for one.
   */
  /**
   * One recorded absence as this page may reason from it, or null.
   *
   * V7. `records()` asked whether a member was an object and `tongue()` asked
   * whether it named a language; between them `{language: 'en'}` was an
   * absence record, and a hollow object took a real work's selection slot and
   * spoke for it. An absence is a claim about somebody's property rights or
   * about what this project could find, so a member states a claim or it
   * states nothing.
   *
   * A member states the language it is about and one of the four closed
   * findings. The REASON is deliberately not required, though the generator
   * requires it of its own rows: V6 established that `in-copyright` is a fact
   * about the law and survives a malformed reason beside it, and V7 does not
   * reopen that. What a reason may no longer do is speak for a row whose
   * finding could not be read.
   */
  function absenceMember(entry, wanted) {
    const record = bag(entry);
    if (tongue(record.language) !== wanted) return null;
    const finding = sound(record.finding);
    if (!Object.hasOwn(FINDINGS, finding)) return null;
    return {
      finding: finding,
      reason: sound(record.reason),
      // `partial` IS PROSE OR IT IS NOTHING. The contract writes it as a
      // whitespace-collapsed string and omits it when empty, so an object, a
      // list, a number, a flag and a null are each a malformed value and not a
      // rights statement to be coerced into one. It is read here, beside the
      // finding it can only refine, and never on its own.
      partial: sound(record.partial)
    };
  }

  function absenceRows(index, file, language) {
    const wanted = tongue(language);
    const recorded = bag(bag(index).absences);
    const sources = bag(bag(file).sources);
    const named = [];
    const rows = [];
    if (!wanted) return rows;
    for (const key in sources) {
      if (!Object.hasOwn(sources, key)) continue;
      const source = bag(sources[key]);
      // `ident` and `hasOwn`: the work id is a property lookup into the
      // recorded absences, and a lookup answers for the prototype as readily
      // as for the record.
      const workId = ident(source.work_id);
      if (!workId || named.includes(workId) || !Object.hasOwn(recorded, workId)) continue;
      // THE SOURCE IS VALIDATED BEFORE IT CLAIMS THE SLOT. V6 deduplicated on
      // `work_id` first and read the author and the work afterwards, so a
      // source stating neither took the row for that work and rendered it
      // blank — an absence note about a work the page could not name — while
      // the valid sibling standing behind it, carrying the same work id and
      // both its names, was skipped as a duplicate.
      const author = sound(source.author);
      const work = sound(source.work);
      if (!author && !work) continue;
      // TWO QUESTIONS, NOT ONE. `same` is the members that are about this
      // work in this language at all — the ground for the row existing. `said`
      // is the members that state a claim the page may repeat — the ground for
      // anything the row says. V6 asked only the first and then spoke from
      // whatever it had; a record naming the language and nothing else was
      // enough to put its prose on the page. A member that is not a record, or
      // names no language, is neither, so `{}`, a scalar and a null make no
      // row and take no slot.
      const same = [];
      const said = [];
      for (const one of records(recorded[workId])) {
        if (tongue(one.language) !== wanted) continue;
        same.push(one);
        const member = absenceMember(one, wanted);
        if (member) said.push(member);
      }
      if (!same.length) continue;
      named.push(workId);
      // A SET, NOT A SEQUENCE. The V5 review proved selection was
      // first-match: an unreadable same-language record standing before a
      // valid one erased the valid finding, and the same two records in the
      // other order kept it — so the page said two different things about one
      // work's rights depending on how the generator happened to list them.
      //
      // The recognized findings are gathered from every same-language record.
      // Exactly one distinct recognized finding is the record speaking; two
      // different ones are a record contradicting itself, and the page
      // declines rather than choosing the stronger — an absence must never be
      // resolved by picking the harsher of two claims.
      const stated = [];
      for (const one of said) if (!stated.includes(one.finding)) stated.push(one.finding);
      const finding = stated.length === 1 ? stated[0] : '';
      // Which record's PROSE stands for the row, chosen without reference to
      // position: among the records that carry the chosen finding, the one
      // that states the most, and where two state as much, the one that sorts
      // first. The same set yields the same row in any order.
      //
      // WHERE THERE IS NO ONE FINDING THERE ARE NO CARRIERS, AND SO NO PROSE.
      // V6 fell back to ranking every same-language record, so a page that had
      // just declined to state a finding went on to print one record's
      // `reason` beneath the declining — the rights prose of one side of a
      // contradiction, offered as the reason this work is not held in this
      // language, and chosen because it happened to be the longest. A
      // contradiction is the record failing to say one thing; the page says
      // nothing rather than picking a side, and it must not resolve one by
      // length, by order, or by taking the harsher of the two claims.
      const carriers = finding ? said.filter((one) => one.finding === finding) : [];
      const rank = (one) => one.reason + '\u0000' + one.partial;
      const found = carriers.slice().sort(function (a, b) {
        const x = rank(a);
        const y = rank(b);
        if (x.length !== y.length) return y.length - x.length;
        return x < y ? -1 : x > y ? 1 : 0;
      })[0] || { reason: '', partial: '' };
      rows.push({
        author: author,
        work: work,
        finding: finding,
        // The one value the page's sentences are built from. '' is not a
        // default: it is the page declining to speak for a record it cannot
        // read, and a row holding it enters no count.
        stands: finding ? FINDINGS[finding] : '',
        reason: found.reason,
        // `partial` REFINES A FINDING AND NEVER ESTABLISHES ONE. The V5
        // review proved a stray `partial` string on an unknown or
        // `not-surveyed` row was still printed as "Partly public domain" — a
        // rights claim about somebody's text, manufactured out of a field
        // beside a finding that supports no such thing. Only the finding that
        // says it in its own name licenses the words, and only from a record
        // that carries that finding and states its `partial` as the prose the
        // contract writes.
        partial: finding === 'partial-public-domain' ? found.partial : '',
        // The words themselves, derived beside the value that licenses them:
        // a partial not yet taken is an offer, not an excuse.
        offer: finding === 'partial-public-domain' && found.partial
          ? 'Partly public domain — ' + found.partial
          : ''
      });
    }
    return rows;
  }

  /** How many of those rows stand on one finding class. */
  function absenceCount(rows, stands) {
    return list(rows).filter((row) => row.stands === stands).length;
  }

  /**
   * The one line that summarises them — a clause per finding class, and no
   * clause for a class no row stands on.
   *
   * The sentence lives here, beside `voicePhrase` and `joinNames`, for the
   * same reason they do: it is prose DERIVED FROM A TYPED RECORD, and the
   * derivation and the words it licenses must not be able to drift apart.
   * Each clause says only what its own finding says. The first names the
   * works; the rest carry the number alone, because "4 works standing here
   * have … ; 1 has …" is how the sentence reads aloud.
   */
  function absenceSummary(rows, languageName) {
    const parts = [];
    const closed = absenceCount(rows, 'closed');
    if (closed) {
      parts.push(
        (closed === 1 ? 'One work standing here has' : closed + ' works standing here have') +
          ' no ' + languageName + ' this project may publish');
    }
    const rest = (many) =>
      (parts.length ? String(many)
        : many === 1 ? 'one work standing here' : many + ' works standing here') +
      (many === 1 ? ' has' : ' have');
    const untaken = absenceCount(rows, 'untaken');
    if (untaken) {
      parts.push(rest(untaken) +
        ' only a partly public domain ' + languageName + ', not yet taken');
    }
    // The two classes that assert NO negative, and may no longer be spoken as
    // one with the two that do.
    const unsurveyed = absenceCount(rows, 'unsurveyed');
    if (unsurveyed) parts.push(rest(unsurveyed) + ' not been surveyed for ' + languageName);
    const unread = absenceCount(rows, '');
    if (unread) parts.push(rest(unread) + ' a finding this page cannot read');
    return parts.join('; ');
  }

  /* ------------------------------------------------------------------------
   * The collections the page counts, renders and refuses from
   *
   * V6, and the review's sharpest finding. `records()` asks whether a member
   * is an object; it never asked whether the object is a MEMBER OF THIS
   * COLLECTION. The difference showed three ways on one page.
   *
   * A lead record stating nothing rendered an empty `<li>` and was still
   * counted into "3 unreconciled lead entries on the acquisition record". A
   * blocked record stating nothing rendered an empty row, counted into the
   * tally as a work held, and turned the chain's sentence into "No RENDERABLE
   * commentary on this chapter is held" — a claim about what this project
   * possesses, drawn from a record that said nothing whatever. And an empty
   * refusal record manufactured "Boundary not established", which is a claim
   * about Scripture's own numbering, made by `{}`.
   *
   * So each collection states here, once, what one of its members IS: the
   * least a record must say for there to be anything to render or to count. A
   * member saying none of it is not a thin member; it is not a member, and it
   * enters no row, no count, no tally and no derived claim. Its valid siblings
   * are untouched, which is the whole point — refusing the malformed one must
   * cost the record nothing it really states.
   * --------------------------------------------------------------------- */

  /**
   * One edition of Scripture this page may offer, or null.
   *
   * An edition must be able to name itself before it can be an option, a route
   * value and a fetched directory. The LANGUAGE is separate: an edition whose
   * language nobody can read is still an edition, and still has a label — it
   * simply makes no language claim. `|| 'en'` is how such a record became an
   * English Bible, in the option a reader chooses from and in the `lang` a
   * screen reader picks a voice from; and unchecked, the same value reached
   * the option text as `Douay-Rheims ([object Object])`.
   */
  function bibleRecord(entry) {
    const record = bag(entry);
    const id = ident(record.id);
    const label = sound(record.label);
    if (!id || !label) return null;
    const said = {};
    for (const key in record) if (Object.hasOwn(record, key)) said[key] = record[key];
    said.id = id;
    said.label = label;
    said.language = tongue(record.language);
    return said;
  }

  /** Every edition the manifest states, in the order it states them. */
  function bibles(value) {
    return bibleRoot(value).bibles;
  }

  /* ------------------------------------------------------------------------
   * The three roots an address is judged against, and whether each was read whole
   *
   * V7, and the V6 review's semantic-integrity blocker. Each collection is read
   * member by member and an unreadable member is left out, so its valid
   * siblings still serve the reader. That is right, and on its own it is how a
   * parse failure became a claim about the corpus:
   *
   *   an unreadable canon member   -> "book=Gen is not a book of this canon"
   *   an unreadable edition record -> "bible=douay-rheims is not a published edition"
   *   an unreadable voices list    -> "voice=translation:en is not a voice this corpus holds"
   *
   * Three negatives about what this project holds, drawn from values nobody
   * could read and handed to the reader as faults in the address they typed.
   * `whole` is the difference between the two sentences the page is allowed:
   * the corpus does not have this, and this page could not establish what the
   * corpus has. What WAS read is returned beside it, so nothing readable is
   * withheld to punish a malformed neighbour.
   * --------------------------------------------------------------------- */

  /** The editions the manifest states, and whether it stated them all. */
  function bibleRoot(value) {
    const out = [];
    let read = Array.isArray(value);
    for (const one of list(value)) {
      const record = bibleRecord(one);
      if (record) out.push(record);
      else read = false;
    }
    return { bibles: out, whole: read };
  }

  /** The canon this page can state, and whether it could state all of it. */
  function canonRoot(canon) {
    const books = [];
    let read = Array.isArray(canon);
    for (const entry of list(canon)) {
      const book = canonBook(entry);
      if (book) books.push(book);
      else read = false;
    }
    return { books: books, whole: read };
  }

  /**
   * The voice keys this corpus states holding something in, and whether the
   * list could be read whole.
   *
   * The members are held to the published route grammar `voiceKey` composes,
   * because a member outside it names no offer this page could ever match an
   * address against — and a list carrying one cannot be the ground for saying
   * an address names a voice the corpus does not hold.
   */
  function voiceRoot(index) {
    const stated = bag(index).voices;
    const keys = [];
    let read = Array.isArray(stated);
    for (const one of list(stated)) {
      const key = sound(one);
      const parsed = parseVoiceKey(key);
      if (key === ORIGINAL ||
          (parsed && parsed.voice === TRANSLATION && voiceLanguage(parsed.language))) {
        keys.push(key);
      } else {
        read = false;
      }
    }
    return { keys: keys, whole: read };
  }

  /**
   * One row of the acquisition list, or null.
   *
   * A lead entry asserts no distinct work, no possession and nothing
   * renderable — but it does assert that SOMETHING was believed to comment
   * here, and a record naming neither a work nor a man asserts not even that.
   */
  function leadRow(entry) {
    const record = bag(entry);
    const who = sound(record.author);
    const title = sound(record.title);
    if (!who && !title) return null;
    return { who: who, title: title, when: say(record.date) };
  }

  /** The acquisition list, its members alone. */
  function leadRows(value) {
    const rows = [];
    for (const one of records(value)) {
      const row = leadRow(one);
      if (row) rows.push(row);
    }
    return rows;
  }

  /**
   * One held-but-not-renderable row, or null.
   *
   * "Held, and not renderable yet" is a claim of possession. A record that can
   * name neither what is held nor why it cannot be shown supports no part of
   * it, and a page that counted such a record told the reader this project
   * holds a work it cannot name.
   */
  function blockedRow(entry) {
    const record = bag(entry);
    // Each field on its own merit: coupled, a missing author lost the title.
    const named = [sound(record.author), sound(record.work)]
      .filter(Boolean).join(' — ');
    const why = sound(record.reason);
    if (!named && !why) return null;
    return { named: named, why: why };
  }

  /** The held-and-blocked rows, their members alone. */
  function blockedRows(value) {
    const rows = [];
    for (const one of records(value)) {
      const row = blockedRow(one);
      if (row) rows.push(row);
    }
    return rows;
  }

  // The two claims a recorded refusal may make, closed at
  // `scripts/_projection.py` so that a third has to be argued for rather than
  // typed: `displaced` — the numbers agree and the text boundary does not;
  // `unrecorded` — known to diverge, correspondence not established.
  const REFUSAL_KINDS = ['displaced', 'unrecorded'];

  /**
   * The sentence one edition's recorded refusal of THIS chapter opens with, or ''.
   *
   * A refusal is Rule 4: where the projection refuses, the page refuses. It is
   * therefore a claim the RECORD makes, and "Boundary not established" is a
   * claim about Scripture's own numbering — the strongest thing this page says
   * about a text it did not write.
   *
   * V6 required the note alone, and the review proved that too little: a record
   * carrying nothing but a nonempty `note` established the claim without the
   * closed `kind` the source contract writes and without saying which locus it
   * refuses — so a note about anything, filed under any chapter, printed as
   * this chapter's refusal.
   *
   * V7 asks for the whole typed record: the kind the projection recorded, the
   * chapter it stands on MATCHED against the chapter being read, and the note,
   * which remains the whole of what this page may say about a boundary it will
   * not guess at. A list holding no such member refuses nothing, and the first
   * that is one states it, whatever stands around it.
   */
  function refusalNote(file, edition, chapter) {
    const key = ident(edition);
    const held = bag(bag(file).refusals);
    const here = whole(chapter);
    if (!key || here === null || !Object.hasOwn(held, key)) return '';
    for (const one of records(held[key])) {
      if (!REFUSAL_KINDS.includes(sound(one.kind))) continue;
      if (whole(one.chapter) !== here) continue;
      const note = sound(one.note);
      if (note) return note.charAt(0).toUpperCase() + note.slice(1) + '.';
    }
    return '';
  }

  /* ------------------------------------------------------------------------
   * Whose words these are — the axis the commentary control runs along
   *
   * NOT `la / grc / en`. A father may be held in his own Greek, in an ancient
   * Latin version of that Greek, and in a Victorian English of it, and those
   * are three different claims about one page of words. On a language axis the
   * middle one is invisible: it prints "Latin", indistinguishably from Ambrose
   * writing Latin himself, and a reader who asked for the original would be
   * handed a translation with nothing on the page to say so.
   *
   * So the generator derives `voice` per edition — `original` where the
   * edition is in a language the work was written in, `translation` otherwise —
   * from the work record and the edition record together, and refuses to emit a
   * fragment whose two independent signals for it disagree. This file only
   * counts what arrived.
   *
   * The key a selection carries is `original`, or `translation:` and the
   * language, because "English" and "Latin" are different offers and a reader
   * choosing between them is choosing between two translations.
   * --------------------------------------------------------------------- */

  const ORIGINAL = 'original';
  const TRANSLATION = 'translation';

  /** The selectable key for one edition's voice, or '' where it has none. */
  function voiceKey(source) {
    const voice = sound(source && source.voice);
    if (voice === ORIGINAL) return ORIGINAL;
    if (voice === TRANSLATION) {
      // THE KEY BECOMES A CONTROL VALUE AND A URL, so a language that is not
      // of the route's own grammar names no offer at all. Composed from a
      // record this produced `translation:[object Object]`, which the page
      // wrote into history and refused on the way back in — a link the page
      // issued against itself. Sound text alone was not enough to stop it:
      // `translation:not a language code` is sound text.
      const language = voiceLanguage(source && source.language);
      return language ? TRANSLATION + ':' + language : '';
    }
    return '';
  }

  /**
   * Every voice this chapter actually holds, counted rather than assumed.
   *
   * Read off `sources`, which the spine writes with exactly one entry per
   * edition standing under this chapter — so an offer appears here only when
   * something is behind it, and a chapter held in one voice offers one.
   * Originals first, then translations by language, so the control reads
   * outward from the author.
   */
  function chapterVoices(file) {
    const sources = bag(file && file.sources);
    const found = new Map();
    for (const key in sources) {
      if (!Object.hasOwn(sources, key)) continue;
      const source = bag(sources[key]);
      const wanted = voiceKey(source);
      if (!wanted || found.has(wanted)) continue;
      found.set(wanted, {
        key: wanted,
        voice: sound(source.voice),
        // Named for a translation and deliberately blank for an original. The
        // reader asking for the author's own language is asking one question,
        // not one per language: a chapter holding Ambrose's Latin beside
        // Severian's Greek holds both authors' own words, and offering them
        // separately would put the reader back on the axis this replaced.
        language: sound(source.voice) === TRANSLATION ? voiceLanguage(source.language) : ''
      });
    }
    return Array.from(found.values()).sort(function (a, b) {
      if (a.voice !== b.voice) return a.voice === ORIGINAL ? -1 : 1;
      return a.language < b.language ? -1 : a.language > b.language ? 1 : 0;
    });
  }

  /**
   * What the chain says when this selection shows nothing.
   *
   * Prose derived from typed counts, so it is derived here beside them. A
   * held row that cannot be rendered is NOT absence: beside one, an absence
   * claim covers the renderable rows alone.
   *
   * V7 also stops the sentence naming an empty list. `chapterVoices` reads
   * `sources`, and a chapter whose `sources` nobody can read offers none — so
   * `joinNames([])` reached a reader as "held here, in ;". A clause with
   * nothing to say is not said.
   */
  function emptyChainNote(total, blocked, wanted, voices) {
    const many = whole(total) || 0;
    if (!many) {
      return blocked
        ? 'Nothing held on this chapter is renderable yet; what is held, and ' +
          'why it cannot be shown, stands below.'
        : 'No commentary on this chapter is held yet.';
    }
    const named = joinNames(list(voices).map(voicePhrase));
    return 'No ' + (blocked ? 'renderable ' : '') +
      'commentary on this chapter is held in ' +
      voicePhrase(parseVoiceKey(wanted)) + '. ' + many +
      (many === 1 ? ' fragment is' : ' fragments are') + ' held here' +
      (named ? ', in ' + named : '') + '; choose \u201cEverything held\u201d to see ' +
      (many === 1 ? 'it' : 'them') + '.';
  }

  /** A father held only in his own Latin must not vanish under English. */
  function otherVoicesNote(wanted, others) {
    const named = joinNames(list(others).map(voicePhrase));
    return named
      ? 'Showing ' + voicePhrase(parseVoiceKey(wanted)) +
        ' only. This chapter is also held in ' + named + '.'
      : '';
  }

  /**
   * The one typed truth beside the chapter: the tally, and the line spoken.
   *
   * V7 moves this here because `catena.js` had no bytes left, and it belongs
   * here for a better reason: the page's own comment claimed "the same clauses
   * in the same order, so the two cannot disagree" while writing them twice,
   * twenty lines apart. Written once, there is nothing to disagree.
   *
   * `bold` is the number the tally sets in bold and `tail` is the rest of the
   * same sentence, split so the page can mark one without composing the
   * other. `spoken` is every clause in order, for the live region.
   */
  function chapterSummary(state) {
    const said = bag(state);
    const total = whole(said.total) || 0;
    const shown = whole(said.shown) || 0;
    const blocked = whole(said.blocked) || 0;
    const leads = whole(said.leads) || 0;
    const voice = sound(said.voice);
    const blockedClause = blocked + (blocked === 1 ? ' work' : ' works') +
      ' held, not renderable yet';
    if (said.unfetched) {
      return {
        bold: '',
        tail: 'The commentary record did not load',
        spoken: 'commentary record unavailable'
      };
    }
    const head = total
      ? total + (total === 1 ? ' fragment held' : ' fragments held')
      : blocked ? blockedClause : 'Nothing held here';
    const extras = [];
    // "none in X" is provable only with no blocked row standing.
    if (total && voice && shown < total && (shown || !blocked)) {
      extras.push((shown ? shown + ' in ' : 'none in ') +
        voicePhrase(parseVoiceKey(voice)));
    }
    if (total && blocked) extras.push(blockedClause);
    if (leads) {
      extras.push(leads + (leads === 1 ? ' lead entry' : ' lead entries') +
        ' on the acquisition list');
    }
    const bold = String(total || blocked || 'Nothing');
    return {
      bold: bold,
      tail: head.slice(bold.length) + extras.map((one) => ' \u00b7 ' + one).join(''),
      spoken: [head].concat(extras).join(', ')
    };
  }

  /* ------------------------------------------------------------------------
   * The cited state, judged
   *
   * A value the page cannot honour is never traded for a default: the URL keeps
   * the reader's text and recovery is a link and the controls. WHY it cannot be
   * used is prose about this corpus, so the judgment lives here — the sentence
   * and the value that licenses it must not drift apart.
   *
   * Failing closed was never the defect; the sentence was. Each negative is
   * spoken only from a root read WHOLE, per `canonRoot` above; where one could
   * not be, the page says only that it could not match the value.
   * --------------------------------------------------------------------- */

  const UNMATCHED =
    'is not a value this page could match; the record it would be matched ' +
    'against could not be read whole';

  /**
   * Everything wrong with one cited address, in the order the page states it.
   *
   * `canon`, `editions` and `voices` are the roots as `canonRoot`,
   * `bibleRoot` and `voiceRoot` read them; `hash` is any `URLSearchParams`.
   */
  function addressProblems(hash, canon, editions, voices) {
    const bad = [];
    const flag = (key, value, note) => bad.push({ key, value, note });
    const said = (whole, negative) => (whole ? negative : UNMATCHED);
    // Multiplicity first: a recognized key cited twice is refused even when
    // the citations agree; a stranger's key is not judged, and no write keeps
    // one. (An undecodable percent-value stays literal, and fails.)
    for (const key of ['book', 'chapter', 'bible', 'voice']) {
      const all = hash.getAll(key);
      if (all.length > 1) flag(key, all.join(', '), 'is cited more than once');
    }
    const books = list(bag(canon).books);
    // EXACTLY, not trimmed. `sound()` here made `#book=%20Ex` resolve to
    // Exodus and pass the address grammar, while `seedControls` handed the
    // untrimmed `" Ex"` to a control that carries no such option, fell back to
    // the first book of the canon, and REPLACED the reader's address with
    // `book=Gen`. A reader who asked for Exodus 3 was shown Genesis 3 and told
    // by the URL that they had asked for it. `bible` was already compared
    // raw, so this also stops two keys of one grammar being judged two ways.
    const named = (token) => books.find((one) => one.token === token) || null;
    const token = hash.get('book') || '';
    const entry = token ? named(token) : null;
    if (token && !entry) flag('book', token, said(bag(canon).whole, 'is not a book of this canon'));
    const chapter = hash.get('chapter') || '';
    if (chapter) {
      const numeric = /^[0-9]+$/.test(chapter) ? Number(chapter) : NaN;
      // Ranged against the book the ADDRESS resolves to — never a
      // leftover control — so every arrival judges alike.
      const anchor = entry || named('Gen');
      if (!(anchor ? numeric >= 1 && numeric <= anchor.chapters : numeric >= 1)) {
        flag('chapter', chapter, anchor
          ? 'is not a chapter of ' + anchor.name + ', which has ' + anchor.chapters
          : 'is not a chapter number');
      }
    }
    const bible = hash.get('bible') || '';
    if (bible && !list(bag(editions).bibles).some((one) => one.id === bible)) {
      flag('bible', bible, said(bag(editions).whole, 'is not a published edition'));
    }
    const voice = hash.get('voice') || '';
    if (voice) {
      // The WHOLE key, as a closed grammar: `original` alone, or
      // `translation:` plus one lowercase code — no second colon, no
      // whitespace, no suffix. `original:x` would self-contradict.
      const parsed = parseVoiceKey(voice);
      if (voice !== ORIGINAL &&
          !(parsed && parsed.voice === TRANSLATION && voiceLanguage(parsed.language))) {
        flag('voice', voice, 'is not a voice — “original”, or “translation:” plus a language');
      // The keys the ROOT states, read as keys. `list(index.voices)` answered
      // `[]` for a voices value nobody could read, and every address was then
      // told this corpus holds no such voice.
      } else if (!list(bag(voices).keys).includes(voice)) {
        flag('voice', voice, said(bag(voices).whole, 'is not a voice this corpus holds'));
      }
    }
    return bad;
  }

  /**
   * A selection key read back as the voice it names.
   *
   * Composed by `voiceKey` and taken apart only here, so a page that has to
   * NAME a selection the chapter does not hold — which it must, rather than
   * silently widening — never parses the key a second way.
   */
  function parseVoiceKey(wanted) {
    // `sound`, not `String(wanted || '')`: the second turned a record into
    // `[object Object]` and then took it apart as though it were a key.
    const key = sound(wanted);
    if (!key) return null;
    if (key === ORIGINAL) return { key: key, voice: ORIGINAL, language: '' };
    const cut = key.indexOf(':');
    if (cut < 0) return null;
    return {
      key: key,
      voice: key.slice(0, cut),
      language: key.slice(cut + 1)
    };
  }

  /**
   * Does this fragment answer that selection?
   *
   * An empty selection is every fragment. A fragment whose voice could not be
   * derived answers no selection at all rather than the nearest one: it is
   * refused by the generator's check before it reaches here, and if one ever
   * arrives it must not be served as though someone had established whose
   * words it carries.
   */
  function matchesVoice(fragment, wanted) {
    if (!wanted) return true;
    return voiceKey(fragment) === wanted;
  }

  return {
    touchesChapter: touchesChapter,
    fragmentsOnChapter: fragmentsOnChapter,
    chapterFragments: chapterFragments,
    fragmentRow: fragmentRow,
    textPayload: textPayload,
    formatExtent: formatExtent,
    spansChapters: spansChapters,
    chapterVoices: chapterVoices,
    matchesVoice: matchesVoice,
    voiceKey: voiceKey,
    parseVoiceKey: parseVoiceKey,
    spineUnreadable: spineUnreadable,
    addressProblems: addressProblems,
    joinNames: joinNames,
    useLanguageNames: useLanguageNames,
    voicePhrase: voicePhrase,
    voiceLabel: voiceLabel,
    sayLanguage: sayLanguage,
    languageChip: languageChip,
    canonBook: canonBook,
    canonBooks: canonBooks,
    bookOf: bookOf,
    chapterPath: chapterPath,
    paragraphPath: paragraphPath,
    chapterLines: chapterLines,
    chapterReading: chapterReading,
    chapterSummary: chapterSummary,
    emptyChainNote: emptyChainNote,
    otherVoicesNote: otherVoicesNote,
    absenceRows: absenceRows,
    absenceCount: absenceCount,
    absenceSummary: absenceSummary,
    bibleRecord: bibleRecord,
    bibles: bibles,
    bibleRoot: bibleRoot,
    canonRoot: canonRoot,
    voiceRoot: voiceRoot,
    leadRow: leadRow,
    leadRows: leadRows,
    blockedRow: blockedRow,
    blockedRows: blockedRows,
    refusalNote: refusalNote,
    absenceMember: absenceMember,
    LANGUAGE_NAMES: LANGUAGE_NAMES,
    FINDINGS: FINDINGS,
    TESTAMENTS: TESTAMENTS,
    BREAK_KINDS: BREAK_KINDS,
    REFUSAL_KINDS: REFUSAL_KINDS,
    sound: sound,
    list: list,
    bag: bag,
    count: count,
    say: say,
    whole: whole,
    tongue: tongue,
    voiceLanguage: voiceLanguage,
    ident: ident,
    bookToken: bookToken,
    trail: trail,
    leaf: leaf,
    records: records,
    ORIGINAL: ORIGINAL,
    TRANSLATION: TRANSLATION
  };
}));
