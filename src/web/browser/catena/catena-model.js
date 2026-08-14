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
   * A chapter file's fragments, each rejoined to what it shares with its edition.
   *
   * The spine writes the author, the work, the date, the language, the printing,
   * the translators and the rights ONCE per distinct set of them, under
   * `sources`, and gives every fragment the key of its set. Written per fragment
   * they cost more than everything else in the file put together — on Genesis 1,
   * 107 copies of ten fields — and every copy was a chance for two of them to
   * disagree about one edition.
   *
   * The join happens here and at read time, which is where `browser-core.js`
   * says joins belong. `text_path` is composed the same way, from the file's own
   * one statement of where fragment texts live, so the page never carries a
   * directory layout the generator can change underneath it.
   */
  function chapterFragments(file) {
    const sources = bag(bag(file).sources);
    // `trail`, not `sound`: the prefix is the head of a URL this page requests.
    const prefix = trail(bag(file).text_prefix);
    // `records` rather than `file.fragments || []`: a spine whose `fragments`
    // is a record or a string is a broken record, and mapping over it threw out
    // of the render tail — past `aria-busy`, past the tally, past the
    // announcement. Its MEMBERS are asked the same question, because a `null`
    // among them threw on the very next line and took every valid sibling with
    // it, and a scalar among them became a blank row that was still counted.
    return records(bag(file).fragments).map(function (fragment) {
      // THE SOURCE KEY IS A PROPERTY LOOKUP, and V6's review proved a
      // lookup is a coercion: `sources[["1"]]` is `sources["1"]`, so a
      // one-member LIST silently took a real edition's author, rights and
      // language for a fragment that named no edition at all — and
      // `sources["constructor"]` is a function, which `bag` refuses but the
      // raw index did not. Only a string that the record itself carries as
      // its own key joins anything.
      const key = fragment.source;
      const shared = typeof key === 'string' && Object.hasOwn(sources, key)
        ? bag(sources[key])
        : {};
      const joined = {};
      for (const name in shared) if (Object.hasOwn(shared, name)) joined[name] = shared[name];
      for (const name in fragment) if (Object.hasOwn(fragment, name)) joined[name] = fragment[name];
      // THE ID BECOMES A FETCHED PATH AND A LINK. A truthy test let a record
      // through and composed `…/[object Object].json`, which the page then
      // requested; sound text alone still let arbitrary prose and a path-like
      // string through. A fragment whose id is not an identity of this corpus
      // carries no text file and no cross-entrance link.
      const id = ident(fragment.id);
      joined.id = id;
      if (id && prefix) joined.text_path = prefix + id + '.json';
      return joined;
    });
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
    // EVERY entry for this book, not the first object-shaped one. The V5
    // review proved a malformed same-token record masked a valid sibling
    // standing behind it: `find` stopped at the broken one and the whole book
    // became an unreadable record, though the index stated it perfectly well
    // one member later. Nothing here depends on which order they arrive in.
    const held = wanted
      ? records(bag(index).held).filter((entry) => bookToken(entry.token) === wanted)
      : [];
    // The index holds nothing at all in this book, and says so of every
    // chapter in it. That is a real, recorded emptiness.
    if (!held.length) return '';
    const number = whole(chapter);
    if (number === null) return null;
    const digits = whole(bag(index).chapter_digits) || 1;
    // '' only if some entry could be read and truthfully recorded no chapter
    // here; `null` if none could be read at all. An absence is a claim, so it
    // is drawn only from a record that states one.
    let recorded = null;
    for (const entry of held) {
      const prefix = trail(entry.path);
      if (!prefix || !Array.isArray(entry.present)) continue;
      let readable = true;
      let present = false;
      for (const one of entry.present) {
        // A member this page cannot read makes THAT list unreadable, because
        // a chapter's absence from an unreadable list proves nothing.
        if (whole(one) === null) { readable = false; break; }
        if (one === number) present = true;
      }
      if (!readable) continue;
      if (present) return prefix + String(number).padStart(digits, '0') + '.json';
      recorded = '';
    }
    return recorded;
  }

  /**
   * Where this edition opens paragraphs in one chapter, or `''`.
   *
   * `''` is not a claim: the layer is the edition's own, and a chapter that
   * runs on has no file. What it does mean is that no request is made — a
   * malformed edition record or book path never becomes a fetched URL.
   */
  function paragraphPath(layer, edition, bookPath, chapter) {
    const index = bag(layer);
    // The EDITION KEY is a property lookup again, so it is an identity this
    // corpus issued or it is nothing: `editions[["douay-rheims"]]` resolved a
    // real layer for a value that named no edition.
    const editions = bag(index.editions);
    const key = ident(edition);
    const prefix = key && Object.hasOwn(editions, key)
      ? trail(bag(editions[key]).path)
      : '';
    const book = ident(bookPath);
    const number = whole(chapter);
    if (!prefix || !book || number === null) return '';
    return prefix + book + '/' +
      String(number).padStart(whole(index.chapter_digits) || 1, '0') + '.json';
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
      const same = records(recorded[workId])
        .filter((one) => tongue(one.language) === wanted);
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
      for (const one of same) {
        const said = sound(one.finding);
        if (Object.hasOwn(FINDINGS, said) && !stated.includes(said)) stated.push(said);
      }
      const finding = stated.length === 1 ? stated[0] : '';
      // Which record's PROSE stands for the row, chosen without reference to
      // position: among the records that carry the chosen finding (or, where
      // none is recognized, among all of them) the one that states the most,
      // and where two state as much, the one that sorts first. The same set
      // yields the same row in any order.
      const carriers = finding
        ? same.filter((one) => sound(one.finding) === finding)
        : same;
      const rank = (one) => sound(one.reason) + ' ' + sound(one.partial);
      const found = carriers.slice().sort(function (a, b) {
        const x = rank(a);
        const y = rank(b);
        if (x.length !== y.length) return y.length - x.length;
        return x < y ? -1 : x > y ? 1 : 0;
      })[0] || {};
      rows.push({
        author: sound(source.author),
        work: sound(source.work),
        finding: finding,
        // The one value the page's sentences are built from. '' is not a
        // default: it is the page declining to speak for a record it cannot
        // read, and a row holding it enters no count.
        stands: finding ? FINDINGS[finding] : '',
        reason: sound(found.reason),
        // `partial` REFINES A FINDING AND NEVER ESTABLISHES ONE. The V5
        // review proved a stray `partial` string on an unknown or
        // `not-surveyed` row was still printed as "Partly public domain" — a
        // rights claim about somebody's text, manufactured out of a field
        // beside a finding that supports no such thing. Only the finding that
        // says it in its own name licenses the words.
        partial: finding === 'partial-public-domain' ? sound(found.partial) : '',
        // The words themselves, derived beside the value that licenses them:
        // a partial not yet taken is an offer, not an excuse.
        offer: finding === 'partial-public-domain' && sound(found.partial)
          ? 'Partly public domain — ' + sound(found.partial)
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
    const out = [];
    for (const one of records(value)) {
      const record = bibleRecord(one);
      if (record) out.push(record);
    }
    return out;
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

  /**
   * The sentence one edition's recorded refusal opens with, or ''.
   *
   * A refusal is Rule 4: where the projection refuses, the page refuses. It is
   * therefore a claim the RECORD makes, and the record makes it by stating why
   * — the note is the whole of what this page can say about a boundary it will
   * not guess at. A refusal list holding no member that states one refuses
   * nothing, and the first member that does states it, whatever position the
   * malformed members occupy around it.
   */
  function refusalNote(file, edition) {
    const key = ident(edition);
    const held = bag(bag(file).refusals);
    if (!key || !Object.hasOwn(held, key)) return '';
    for (const one of records(held[key])) {
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
    formatExtent: formatExtent,
    spansChapters: spansChapters,
    chapterVoices: chapterVoices,
    matchesVoice: matchesVoice,
    voiceKey: voiceKey,
    parseVoiceKey: parseVoiceKey,
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
    absenceRows: absenceRows,
    absenceCount: absenceCount,
    absenceSummary: absenceSummary,
    bibleRecord: bibleRecord,
    bibles: bibles,
    leadRow: leadRow,
    leadRows: leadRows,
    blockedRow: blockedRow,
    blockedRows: blockedRows,
    refusalNote: refusalNote,
    LANGUAGE_NAMES: LANGUAGE_NAMES,
    FINDINGS: FINDINGS,
    TESTAMENTS: TESTAMENTS,
    BREAK_KINDS: BREAK_KINDS,
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
    records: records,
    ORIGINAL: ORIGINAL,
    TRANSLATION: TRANSLATION
  };
}));
