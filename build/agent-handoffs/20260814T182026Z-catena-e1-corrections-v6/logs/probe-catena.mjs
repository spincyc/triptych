/* probe-catena.mjs — real-Chromium DOM evidence for the Catena browser page.
 *
 * CONTRACT
 *
 *   node probe-catena.mjs <site-root> <out.json> <label> [shot-dir] [prefix]
 *
 * <site-root> is a BUILT site. This tool reads it and writes nothing into it:
 * it starts its own static server over that root and substitutes fixtures IN
 * THE RESPONSE PATH, so the artifact on disk is byte-identical before and
 * after a run. It then drives headless Chromium over the DevTools Protocol,
 * reads the live DOM and the live resource log at each probed state, and
 * writes <out.json>. With [shot-dir] it also writes PNGs named
 * <prefix>catena--<state>--<WxH>.png plus <prefix>probe-index.json.
 *
 * WHAT IT READS, AND WHY EACH FIELD
 *
 *   document.activeElement  — id, tag name, and whether it lies inside
 *       `#reading`. Focus is a terminal-state obligation of this page and is
 *       invisible in a raster. Recorded at the terminal moment of every state
 *       and after every intermediate step.
 *   `lang` CONTENT ATTRIBUTES under `#reading` — read as attributes, not
 *       properties, because the defect this evidences is a value coerced into
 *       the attribute.
 *   `#bible-select` OPTION TEXT — the edition control's own labels.
 *   the RESOURCE LOG — every `.json` URL the page requested, page-side from
 *       `performance.getEntriesByType('resource')` and server-side from this
 *       tool's own request log with its status. Two pages can reach the same
 *       visible state and differ entirely in what they asked the network for.
 *   `aria-busy`, the reference line, the status region, the tally and the
 *       rendered records — the terminal state the page owes a reader.
 *
 * SELF-LABELLING IS A REQUIREMENT OF THIS TOOL, NOT A COURTESY
 *
 * Most states here are driven by FABRICATED ADVERSARIAL FIXTURES that
 * represent no holding of this project. The report root, every state record,
 * every screenshot-index entry and every PNG (as a PNG `iTXt` chunk) carry
 * `fabricated` and `represents` fields. A reader who opens ONE artifact in
 * isolation is told what it is. States driven by the real built corpus are
 * labelled `fabricated: false` and say what, if anything, was manipulated —
 * real and fabricated evidence are never mixed under one banner.
 *
 * SCREENSHOTS ARE OFFERED ONLY WHERE THE DIFFERENCE IS IN THE RASTER
 *
 * A `lang` attribute, a URL that was or was not requested, `aria-busy` and
 * the focused element cannot appear in a picture. States whose whole finding
 * is one of those carry no `picture` field and are not captured. Where a
 * picture IS taken, the index records the PNG's SHA-256 and a description of
 * WHAT THIS RUN RENDERS — never a claim that it differs from another run.
 * Establishing difference is `pair-audit.py`'s job, over two runs.
 *
 * REUSE
 *
 * The engine below the DATA block is not V6-specific. Set
 * TRIPTYCH_PROBE_STATES=<file.json> to replace the state list wholesale; the
 * schema is the STATES array below. Chromium is $TRIPTYCH_CHROME or
 * /usr/bin/chromium. No network and no npm dependencies are used.
 */

import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { createServer } from 'node:http';
import { spawn } from 'node:child_process';
import { join, normalize } from 'node:path';
import { createHash } from 'node:crypto';

const [ROOT, OUT, LABEL, SHOTS, PREFIX] = process.argv.slice(2);
if (!ROOT || !OUT || !LABEL) {
  console.error('usage: probe-catena.mjs <site-root> <out.json> <label> [shot-dir] [prefix]');
  process.exit(2);
}

const CHROME = process.env.TRIPTYCH_CHROME || '/usr/bin/chromium';
const VIEWPORTS = [[1440, 900], [393, 852]];

/* The two banners. Nothing in this tool may describe a fabricated state with
 * the real one, or the reverse. */
const FABRICATED = 'ADVERSARIAL TEST FIXTURE — NOT REAL CORPUS DATA';
const REAL = 'REAL CORPUS DATA from the built site under test — no record was ' +
  'fabricated; only the TIMING of responses was manipulated.';

/* ======================================================================= *
 * DATA — the fixtures and the states. V6-specific; replaceable wholesale
 * through TRIPTYCH_PROBE_STATES. Every fixture root below is transcribed
 * from tools/tests/test_catena_wave_1.py and carries that file's own
 * `_adversarial` stamp, so the fabricated JSON denies itself even when it is
 * read straight off this tool's server.
 * ======================================================================= */

const F = {
  "V6_BIBLE_LANGUAGES": {
    "bibles": [
      {
        "id": "douay-rheims",
        "label": "Douay-Rheims",
        "language": {
          "code": "en"
        },
        "numbering": "vulgate",
        "psalter": "gallican",
        "psalm_titles": "numbered",
        "edition": "Synthetic edition record",
        "rights": "public-domain"
      },
      {
        "id": "list-language",
        "label": "List Language",
        "language": [
          "en"
        ],
        "numbering": "vulgate",
        "psalter": "gallican",
        "psalm_titles": "numbered",
        "edition": "Synthetic edition record",
        "rights": "public-domain"
      },
      {
        "id": "number-language",
        "label": "Number Language",
        "language": 42,
        "numbering": "vulgate",
        "psalter": "gallican",
        "psalm_titles": "numbered",
        "edition": "Synthetic edition record",
        "rights": "public-domain"
      },
      {
        "id": "boolean-language",
        "label": "Boolean Language",
        "language": true,
        "numbering": "vulgate",
        "psalter": "gallican",
        "psalm_titles": "numbered",
        "edition": "Synthetic edition record",
        "rights": "public-domain"
      },
      {
        "id": "null-language",
        "label": "Null Language",
        "language": null,
        "numbering": "vulgate",
        "psalter": "gallican",
        "psalm_titles": "numbered",
        "edition": "Synthetic edition record",
        "rights": "public-domain"
      },
      {
        "id": "empty-language",
        "label": "Empty Language",
        "language": "",
        "numbering": "vulgate",
        "psalter": "gallican",
        "psalm_titles": "numbered",
        "edition": "Synthetic edition record",
        "rights": "public-domain"
      },
      {
        "id": "blank-language",
        "label": "Blank Language",
        "language": "   ",
        "numbering": "vulgate",
        "psalter": "gallican",
        "psalm_titles": "numbered",
        "edition": "Synthetic edition record",
        "rights": "public-domain"
      },
      {
        "id": "prose-language",
        "label": "Prose Language",
        "language": "not a language code",
        "numbering": "vulgate",
        "psalter": "gallican",
        "psalm_titles": "numbered",
        "edition": "Synthetic edition record",
        "rights": "public-domain"
      },
      {
        "id": "clementine-vulgate",
        "label": "Clementine Vulgate",
        "language": "la",
        "numbering": "vulgate",
        "psalter": "gallican",
        "psalm_titles": "numbered",
        "edition": "Synthetic edition record",
        "rights": "public-domain"
      }
    ],
    "_adversarial": "ADVERSARIAL TEST FIXTURE — NOT REAL CORPUS DATA"
  },
  "V6_TESTAMENT_INDEX": {
    "canon": [
      {
        "token": "Gen",
        "name": "Genesis",
        "chapters": 50,
        "testament": {
          "half": "old"
        },
        "path": "01-gen"
      }
    ]
  },
  "V6_MIXED_REORDERED": {
    "token": "Gen",
    "chapter": 1,
    "text_prefix": "structure/catena/text/",
    "sources": {
      "1": {
        "author": "First Author",
        "work": "First Work",
        "work_id": "typed.work1",
        "date": 301,
        "language": "la",
        "voice": "original",
        "rights": "public-domain",
        "edition": "Edition 1",
        "edition_published": "1900",
        "translators": [],
        "container": ""
      },
      "5": {
        "author": "Last Author",
        "work": "Last Work",
        "work_id": "typed.work5",
        "date": 305,
        "language": "la",
        "voice": "original",
        "rights": "public-domain",
        "edition": "Edition 5",
        "edition_published": "1900",
        "translators": [],
        "container": ""
      }
    },
    "fragments": [
      null,
      {
        "id": "mixed-first",
        "locator": "1",
        "source": "1",
        "review": "verified",
        "text_words": 4,
        "extent": {
          "token": "Gen",
          "first_chapter": 1,
          "first_verse": 1,
          "last_chapter": 1,
          "last_verse": 1
        }
      },
      7,
      {
        "id": {
          "not": "an id"
        },
        "locator": "2",
        "source": "1",
        "review": "verified",
        "text_words": 4,
        "extent": {
          "token": "Gen",
          "first_chapter": 1,
          "first_verse": 2,
          "last_chapter": 1,
          "last_verse": 2
        }
      },
      {
        "id": "mixed-last",
        "locator": "5",
        "source": "5",
        "review": "verified",
        "text_words": 4,
        "extent": {
          "token": "Gen",
          "first_chapter": 1,
          "first_verse": 5,
          "last_chapter": 1,
          "last_verse": 5
        }
      }
    ],
    "leads": [
      13,
      {
        "author": "Lead One",
        "title": "Lead Work One",
        "date": "500"
      },
      null,
      {
        "author": "Lead Two",
        "title": "Lead Work Two",
        "date": "600"
      },
      {
        "author": {
          "n": 1
        },
        "title": [
          "x"
        ],
        "date": {}
      }
    ],
    "blocked": [
      {
        "author": 5,
        "work": [],
        "reason": {}
      },
      null,
      {
        "author": "Blocked One",
        "work": "Blocked Work One",
        "reason": "rights"
      },
      21,
      {
        "author": "Blocked Two",
        "work": "Blocked Work Two",
        "reason": "rights"
      }
    ],
    "refusals": {
      "douay-rheims": [
        {},
        {
          "note": {
            "broken": true
          }
        },
        {
          "kind": "displaced"
        },
        {
          "chapter": 1,
          "verse": null,
          "kind": "displaced",
          "note": "the numbering of this chapter is displaced in this edition"
        }
      ]
    },
    "_adversarial": "ADVERSARIAL TEST FIXTURE — NOT REAL CORPUS DATA"
  },
  "TYPED_ABSENCE_FIXTURE": {
    "token": "Gen",
    "chapter": 1,
    "text_prefix": "structure/catena/text/",
    "sources": {
      "1": {
        "author": "Author 1",
        "work": "Work 1",
        "work_id": "typed.work1",
        "date": 301,
        "language": "la",
        "voice": "original",
        "rights": "public-domain",
        "edition": "Edition 1",
        "edition_published": "1900",
        "translators": [],
        "container": ""
      },
      "2": {
        "author": "Author 2",
        "work": "Work 2",
        "work_id": "typed.work2",
        "date": 302,
        "language": "la",
        "voice": "original",
        "rights": "public-domain",
        "edition": "Edition 2",
        "edition_published": "1900",
        "translators": [],
        "container": ""
      },
      "3": {
        "author": "Author 3",
        "work": "Work 3",
        "work_id": "typed.work3",
        "date": 303,
        "language": "la",
        "voice": "original",
        "rights": "public-domain",
        "edition": "Edition 3",
        "edition_published": "1900",
        "translators": [],
        "container": ""
      },
      "4": {
        "author": "Author 4",
        "work": "Work 4",
        "work_id": "typed.work4",
        "date": 304,
        "language": "la",
        "voice": "original",
        "rights": "public-domain",
        "edition": "Edition 4",
        "edition_published": "1900",
        "translators": [],
        "container": ""
      },
      "5": {
        "author": "Author 5",
        "work": "Work 5",
        "work_id": "typed.work5",
        "date": 305,
        "language": "la",
        "voice": "original",
        "rights": "public-domain",
        "edition": "Edition 5",
        "edition_published": "1900",
        "translators": [],
        "container": ""
      }
    },
    "fragments": [
      {
        "id": "typed-1",
        "locator": "1",
        "source": "1",
        "review": "verified",
        "text_words": 4,
        "extent": {
          "token": "Gen",
          "first_chapter": 1,
          "first_verse": 1,
          "last_chapter": 1,
          "last_verse": 1
        }
      },
      {
        "id": "typed-2",
        "locator": "2",
        "source": "2",
        "review": "verified",
        "text_words": 4,
        "extent": {
          "token": "Gen",
          "first_chapter": 1,
          "first_verse": 2,
          "last_chapter": 1,
          "last_verse": 2
        }
      },
      {
        "id": "typed-3",
        "locator": "3",
        "source": "3",
        "review": "verified",
        "text_words": 4,
        "extent": {
          "token": "Gen",
          "first_chapter": 1,
          "first_verse": 3,
          "last_chapter": 1,
          "last_verse": 3
        }
      },
      {
        "id": "typed-4",
        "locator": "4",
        "source": "4",
        "review": "verified",
        "text_words": 4,
        "extent": {
          "token": "Gen",
          "first_chapter": 1,
          "first_verse": 4,
          "last_chapter": 1,
          "last_verse": 4
        }
      },
      {
        "id": "typed-5",
        "locator": "5",
        "source": "5",
        "review": "verified",
        "text_words": 4,
        "extent": {
          "token": "Gen",
          "first_chapter": 1,
          "first_verse": 5,
          "last_chapter": 1,
          "last_verse": 5
        }
      }
    ],
    "leads": [],
    "blocked": [],
    "refusals": {}
  },
  "FINDING_ORDER": {
    "absences": {
      "typed.work1": [
        {
          "language": "en",
          "finding": "none-published",
          "reason": "No English translation has been published."
        },
        {
          "language": "en",
          "finding": {
            "kind": "in-copyright"
          },
          "reason": "A reason standing beside an unreadable finding."
        }
      ],
      "typed.work2": [
        {
          "language": "en",
          "finding": "partial-public-domain",
          "reason": "Only part of it is out of copyright.",
          "partial": "the 1893 selection"
        },
        {
          "language": "en",
          "finding": {
            "kind": "in-copyright"
          },
          "reason": "A reason standing beside an unreadable finding."
        }
      ],
      "typed.work3": [
        {
          "language": "en",
          "finding": "not-surveyed",
          "reason": ""
        },
        {
          "language": "en",
          "finding": {
            "kind": "in-copyright"
          },
          "reason": "A reason standing beside an unreadable finding."
        }
      ],
      "typed.work4": [
        {
          "language": "en",
          "finding": "none-published",
          "reason": "No English translation has been published."
        },
        {
          "language": "en",
          "finding": "partial-public-domain",
          "reason": "Only part of it is out of copyright.",
          "partial": "the 1893 selection"
        }
      ],
      "typed.work5": [
        {
          "language": "en",
          "finding": "no-such-finding",
          "reason": "A finding this project does not define."
        },
        {
          "language": "en",
          "finding": "none-published",
          "reason": "No English translation has been published."
        }
      ]
    },
    "_adversarial": "ADVERSARIAL TEST FIXTURE — NOT REAL CORPUS DATA"
  },
  "FINDING_ORDER_REVERSED": {
    "absences": {
      "typed.work1": [
        {
          "language": "en",
          "finding": {
            "kind": "in-copyright"
          },
          "reason": "A reason standing beside an unreadable finding."
        },
        {
          "language": "en",
          "finding": "none-published",
          "reason": "No English translation has been published."
        }
      ],
      "typed.work2": [
        {
          "language": "en",
          "finding": {
            "kind": "in-copyright"
          },
          "reason": "A reason standing beside an unreadable finding."
        },
        {
          "language": "en",
          "finding": "partial-public-domain",
          "reason": "Only part of it is out of copyright.",
          "partial": "the 1893 selection"
        }
      ],
      "typed.work3": [
        {
          "language": "en",
          "finding": {
            "kind": "in-copyright"
          },
          "reason": "A reason standing beside an unreadable finding."
        },
        {
          "language": "en",
          "finding": "not-surveyed",
          "reason": ""
        }
      ],
      "typed.work4": [
        {
          "language": "en",
          "finding": "partial-public-domain",
          "reason": "Only part of it is out of copyright.",
          "partial": "the 1893 selection"
        },
        {
          "language": "en",
          "finding": "none-published",
          "reason": "No English translation has been published."
        }
      ],
      "typed.work5": [
        {
          "language": "en",
          "finding": "none-published",
          "reason": "No English translation has been published."
        },
        {
          "language": "en",
          "finding": "no-such-finding",
          "reason": "A finding this project does not define."
        }
      ]
    },
    "_adversarial": "ADVERSARIAL TEST FIXTURE — NOT REAL CORPUS DATA"
  },
  "V6_STRAY_PARTIAL_INDEX": {
    "absences": {
      "typed.work1": [
        {
          "language": "en",
          "finding": "not-surveyed",
          "partial": "a stray offer beside an admission"
        }
      ],
      "typed.work2": [
        {
          "language": "en",
          "finding": "no-such-finding",
          "partial": "a stray offer beside an unknown finding"
        }
      ],
      "typed.work3": [
        {
          "language": "en",
          "partial": "a stray offer beside no finding at all"
        }
      ],
      "typed.work4": [
        {
          "language": "en",
          "finding": "partial-public-domain",
          "reason": "Only part of it is out of copyright.",
          "partial": "the 1893 selection"
        }
      ],
      "typed.work5": [
        {
          "language": "en",
          "finding": "in-copyright",
          "reason": "A living author's rendering.",
          "partial": "a stray offer beside a closed finding"
        }
      ]
    },
    "_adversarial": "ADVERSARIAL TEST FIXTURE — NOT REAL CORPUS DATA"
  },
  "V6_PADDED_VERSES": {
    "book": "Gen",
    "chapter": 1,
    "verses": {
      "1": "The first verse, sound.",
      "2": "The second verse, sound.",
      "01": "A padded encoding of verse one.",
      "001": "A twice-padded encoding of verse one.",
      "0002": "A padded encoding of verse two.",
      "03": "A padded verse three, with no canonical sibling."
    },
    "_adversarial": "ADVERSARIAL TEST FIXTURE — NOT REAL CORPUS DATA"
  },
  "V6_UNSAFE_IDENTITY_FIXTURE": {
    "token": "Gen",
    "chapter": 1,
    "text_prefix": "structure/catena/text/",
    "sources": {
      "1": {
        "author": "Author 1",
        "work": "Work 1",
        "work_id": "typed.work1",
        "date": 301,
        "language": "la",
        "voice": "original",
        "rights": "public-domain",
        "edition": "Edition 1",
        "edition_published": "1900",
        "translators": [],
        "container": ""
      },
      "2": {
        "author": "Author 2",
        "work": "Work 2",
        "work_id": "typed.work2",
        "date": 302,
        "language": "la",
        "voice": "original",
        "rights": "public-domain",
        "edition": "Edition 2",
        "edition_published": "1900",
        "translators": [],
        "container": ""
      },
      "3": {
        "author": "Author 3",
        "work": "Work 3",
        "work_id": "typed.work3",
        "date": 303,
        "language": "la",
        "voice": "original",
        "rights": "public-domain",
        "edition": "Edition 3",
        "edition_published": "1900",
        "translators": [],
        "container": ""
      },
      "4": {
        "author": "Author 4",
        "work": "Work 4",
        "work_id": "typed.work4",
        "date": 304,
        "language": "la",
        "voice": "original",
        "rights": "public-domain",
        "edition": "Edition 4",
        "edition_published": "1900",
        "translators": [],
        "container": ""
      },
      "5": {
        "author": "Author 5",
        "work": "Work 5",
        "work_id": "typed.work5",
        "date": 305,
        "language": "la",
        "voice": "original",
        "rights": "public-domain",
        "edition": "Edition 5",
        "edition_published": "1900",
        "translators": [],
        "container": ""
      },
      "6": {
        "author": "Author 6",
        "work": "Work 6",
        "work_id": "typed.work6",
        "date": 306,
        "language": "la",
        "voice": "original",
        "rights": "public-domain",
        "edition": "Edition 6",
        "edition_published": "1900",
        "translators": [],
        "container": ""
      },
      "7": {
        "author": "Author 7",
        "work": "Work 7",
        "work_id": "typed.work7",
        "date": 307,
        "language": "la",
        "voice": "original",
        "rights": "public-domain",
        "edition": "Edition 7",
        "edition_published": "1900",
        "translators": [],
        "container": ""
      },
      "8": {
        "author": "Author 8",
        "work": "Work 8",
        "work_id": "typed.work8",
        "date": 308,
        "language": "la",
        "voice": "original",
        "rights": "public-domain",
        "edition": "Edition 8",
        "edition_published": "1900",
        "translators": [],
        "container": ""
      },
      "9": {
        "author": "Author 9",
        "work": "Work 9",
        "work_id": "typed.work9",
        "date": 309,
        "language": "la",
        "voice": "original",
        "rights": "public-domain",
        "edition": "Edition 9",
        "edition_published": "1900",
        "translators": [],
        "container": ""
      },
      "10": {
        "author": "Author 10",
        "work": "Work 10",
        "work_id": "typed.work10",
        "date": 310,
        "language": "la",
        "voice": "original",
        "rights": "public-domain",
        "edition": "Edition 10",
        "edition_published": "1900",
        "translators": [],
        "container": ""
      }
    },
    "fragments": [
      {
        "id": "safe-first",
        "locator": "1",
        "source": "1",
        "review": "verified",
        "text_words": 4,
        "extent": {
          "token": "Gen",
          "first_chapter": 1,
          "first_verse": 1,
          "last_chapter": 1,
          "last_verse": 1
        }
      },
      {
        "id": "../../../etc/passwd",
        "locator": "2",
        "source": "2",
        "review": "verified",
        "text_words": 4,
        "extent": {
          "token": "Gen",
          "first_chapter": 1,
          "first_verse": 2,
          "last_chapter": 1,
          "last_verse": 2
        }
      },
      {
        "id": "a space is not an id",
        "locator": "3",
        "source": "3",
        "review": "verified",
        "text_words": 4,
        "extent": {
          "token": "Gen",
          "first_chapter": 1,
          "first_verse": 3,
          "last_chapter": 1,
          "last_verse": 3
        }
      },
      {
        "id": "Upper.Case",
        "locator": "4",
        "source": "4",
        "review": "verified",
        "text_words": 4,
        "extent": {
          "token": "Gen",
          "first_chapter": 1,
          "first_verse": 4,
          "last_chapter": 1,
          "last_verse": 4
        }
      },
      {
        "id": "   ",
        "locator": "5",
        "source": "5",
        "review": "verified",
        "text_words": 4,
        "extent": {
          "token": "Gen",
          "first_chapter": 1,
          "first_verse": 5,
          "last_chapter": 1,
          "last_verse": 5
        }
      },
      {
        "id": "trailing/",
        "locator": "6",
        "source": "6",
        "review": "verified",
        "text_words": 4,
        "extent": {
          "token": "Gen",
          "first_chapter": 1,
          "first_verse": 6,
          "last_chapter": 1,
          "last_verse": 6
        }
      },
      {
        "id": "%2e%2e%2fsecret",
        "locator": "7",
        "source": "7",
        "review": "verified",
        "text_words": 4,
        "extent": {
          "token": "Gen",
          "first_chapter": 1,
          "first_verse": 7,
          "last_chapter": 1,
          "last_verse": 7
        }
      },
      {
        "id": "coerced-source",
        "locator": "8",
        "source": [
          "1"
        ],
        "review": "verified",
        "text_words": 4,
        "extent": {
          "token": "Gen",
          "first_chapter": 1,
          "first_verse": 8,
          "last_chapter": 1,
          "last_verse": 8
        }
      },
      {
        "id": "proto-source",
        "locator": "9",
        "source": "constructor",
        "review": "verified",
        "text_words": 4,
        "extent": {
          "token": "Gen",
          "first_chapter": 1,
          "first_verse": 9,
          "last_chapter": 1,
          "last_verse": 9
        }
      },
      {
        "id": "safe-last",
        "locator": "10",
        "source": "10",
        "review": "verified",
        "text_words": 4,
        "extent": {
          "token": "Gen",
          "first_chapter": 1,
          "first_verse": 10,
          "last_chapter": 1,
          "last_verse": 10
        }
      }
    ],
    "leads": [],
    "blocked": [],
    "refusals": {},
    "_adversarial": "ADVERSARIAL TEST FIXTURE — NOT REAL CORPUS DATA"
  }
};

const GEN1 = '#book=Gen&chapter=1&bible=douay-rheims';
const GEN1_EN = GEN1 + '&voice=translation:en';
const INDEX = 'structure/catena/index.json';
const CHAPTER = 'structure/catena/01-gen/001.json';

const STATES = [
  {
    name: 'bible-language-forms',
    class: 'a. root/Bible language',
    hash: GEN1,
    fabricated: true,
    files: { 'bibles.json': F.V6_BIBLE_LANGUAGES },
    fixtures: ['bibles.json = V6_BIBLE_LANGUAGES'],
    reads: 'the #bible-select option labels and every lang content attribute under #reading',
    // ONE VIEWPORT ONLY, AND THAT IS A FINDING ABOUT THE PAGE. At 64rem and
    // below the page folds its controls disclosure shut on load, so the
    // edition control — the whole visible half of this class — is not
    // rendered at 393x852. A capture there frames none of it and could
    // support no description of it, so none is taken.
    viewports: [[1440, 900]],
    picture: 'the edition control and the passage as this run renders them under V6_BIBLE_LANGUAGES'
  },
  {
    name: 'bible-language-forms-voice',
    class: 'a. root/Bible language (under a supported translation)',
    hash: GEN1_EN,
    fabricated: true,
    files: { 'bibles.json': F.V6_BIBLE_LANGUAGES },
    fixtures: ['bibles.json = V6_BIBLE_LANGUAGES'],
    reads: 'the same, with the fragment sink, the chip and the absence view rendered'
    /* no picture: the second reading of the same class adds an attribute, not
     * a visible state, over the state above. */
  },
  {
    name: 'malformed-testament',
    class: 'b. testament',
    hash: GEN1,
    fabricated: true,
    patch: { [INDEX]: F.V6_TESTAMENT_INDEX },
    fixtures: [INDEX + ' canon patched with V6_TESTAMENT_INDEX (testament: {"half":"old"})'],
    reads: '#reference-book, the words the page prints for a testament nobody can read',
    picture: 'the reference line and the book/testament label beside it'
  },
  {
    name: 'mixed-collection-members',
    class: 'c. collection members',
    hash: GEN1,
    fabricated: true,
    files: { [CHAPTER]: F.V6_MIXED_REORDERED },
    fixtures: [CHAPTER + ' = V6_MIXED_REORDERED (valid / malformed / scalar / null / valid, reordered)'],
    reads: 'the tally, the lead rows, the blocked rows and the refusal sentence',
    picture: 'the tally, the acquisition list, the blocked list and the refusal note'
  },
  {
    name: 'finding-order',
    class: 'd. order-independent findings (given order)',
    hash: GEN1_EN,
    fabricated: true,
    files: { [CHAPTER]: F.TYPED_ABSENCE_FIXTURE },
    patch: { [INDEX]: F.FINDING_ORDER },
    fixtures: [CHAPTER + ' = TYPED_ABSENCE_FIXTURE',
               INDEX + ' absences patched with _finding_order(False)'],
    reads: 'the absence summary and every absence row',
    fullPage: true,
    picture: 'the absence disclosure: its summary sentence and its rows'
  },
  {
    name: 'finding-order-reversed',
    class: 'd. order-independent findings (same set, reversed)',
    hash: GEN1_EN,
    fabricated: true,
    files: { [CHAPTER]: F.TYPED_ABSENCE_FIXTURE },
    patch: { [INDEX]: F.FINDING_ORDER_REVERSED },
    fixtures: [CHAPTER + ' = TYPED_ABSENCE_FIXTURE',
               INDEX + ' absences patched with _finding_order(True)'],
    reads: 'the same, over the SAME finding set listed in the opposite order',
    compareWith: 'finding-order',
    fullPage: true,
    picture: 'the absence disclosure: its summary sentence and its rows'
  },
  {
    name: 'stray-partial',
    class: 'e. stray `partial`',
    hash: GEN1_EN,
    fabricated: true,
    files: { [CHAPTER]: F.TYPED_ABSENCE_FIXTURE },
    patch: { [INDEX]: F.V6_STRAY_PARTIAL_INDEX },
    fixtures: [CHAPTER + ' = TYPED_ABSENCE_FIXTURE',
               INDEX + ' absences patched with V6_STRAY_PARTIAL_INDEX'],
    reads: 'the absence-partial lines, and which finding licensed each',
    fullPage: true,
    picture: 'the absence disclosure and any partial-offer line under it'
  },
  {
    name: 'padded-verse-keys',
    class: 'f. padded verse keys',
    hash: GEN1,
    fabricated: true,
    files: { 'douay-rheims/chapters/Gen/1.json': F.V6_PADDED_VERSES },
    fixtures: ['douay-rheims/chapters/Gen/1.json = V6_PADDED_VERSES'],
    reads: 'every rendered .verse-num',
    picture: 'the printed verse numbers of the chapter'
  },
  {
    name: 'unsafe-textual-identity',
    class: 'g. unsafe textual identity',
    hash: GEN1,
    fabricated: true,
    files: { [CHAPTER]: F.V6_UNSAFE_IDENTITY_FIXTURE },
    fixtures: [CHAPTER + ' = V6_UNSAFE_IDENTITY_FIXTURE'],
    steps: [{ do: 'openAllFragments', label: 'opened' }],
    reads: 'the resource log — which URLs the page requested once every fragment is opened'
    /* NO PICTURE ON PURPOSE. The finding is which URL was requested. A
     * request is not in the raster; offering a PNG for it would be offering
     * evidence that cannot bear on the claim. */
  },
  {
    name: 'null-bootstrap',
    class: 'h. null bootstrap (200 whose body is JSON null)',
    hash: GEN1,
    fabricated: true,
    raw: { [INDEX]: null },
    fixtures: [INDEX + ' answered 200 with the body `null`'],
    reads: 'aria-busy, the reference line, the status region, the tally and the focused element',
    picture: 'the reference line and the reading region at their terminal state'
  },
  {
    name: 'late-stale-work',
    class: 'i. genuinely late stale work',
    hash: GEN1,
    fabricated: false,
    fixtures: [],
    manipulated: 'Responses under structure/catena/text/ are HELD by this ' +
      'tool’s server until released. No record is altered.',
    defer: ['structure/catena/text/'],
    steps: [
      { do: 'openFirstFragment', label: 'a-held' },
      { do: 'selectChapter', value: '2', label: 'b-settled' },
      { do: 'release', path: 'structure/catena/text/', label: 'a-late' }
    ],
    reads: 'hash, status, tally, aria-busy, focus and the visible records ' +
      'before the late completion (a-held, b-settled) and after it (a-late)'
    /* NO PICTURE ON PURPOSE. The finding is whether a late response commits:
     * it shows in the hash, the tally, `aria-busy` and the focused element,
     * and the page a reader sees is chapter 2 either way. */
  }
];

/* ======================================================================= *
 * ENGINE — not V6-specific below this line.
 * ======================================================================= */

const pause = (ms) => new Promise((go) => setTimeout(go, ms));

const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript',
               '.css': 'text/css', '.json': 'application/json',
               '.svg': 'image/svg+xml', '.png': 'image/png',
               '.woff2': 'font/woff2', '.ico': 'image/x-icon',
               '.txt': 'text/plain; charset=utf-8' };

let active = null;
let serverLog = [];
let held = [];

function releaseHeld(match, outcome) {
  const keep = [];
  let n = 0;
  for (const one of held) {
    if (match === null || one.key.includes(match)) { one.go(outcome || 'ok'); n += 1; }
    else keep.push(one);
  }
  held = keep;
  return n;
}

function serve(root) {
  return createServer(async (request, response) => {
    let path = normalize(decodeURIComponent(
      String(request.url).split('#')[0].split('?')[0]));
    if (path.endsWith('/')) path += 'index.html';
    const relative = path.replace(/^\/+/, '');
    // The data root of these pages is `browse/`; fixture keys are written
    // relative to it, exactly as the test file writes them.
    const key = relative.replace(/^browse\//, '');
    const record = { path: '/' + relative, status: 0 };
    serverLog.push(record);

    const answer = (status, type, body) => {
      record.status = status;
      response.writeHead(status, { 'content-type': type });
      response.end(body);
    };

    // A HELD REQUEST. The socket stays open and the page stays in flight
    // until this state's plan releases it, which is the only way to make
    // work that is GENUINELY late rather than merely reordered.
    if (active && active.defer) {
      const hit = active.defer.find((one) => key.includes(one) || relative.includes(one));
      if (hit) {
        record.held = true;
        const outcome = await new Promise((go) => held.push({ key: key, go: go }));
        record.releasedAs = outcome;
        if (outcome === 'fail') return answer(500, 'text/plain', 'held request released as a failure');
      }
    }

    // FIXTURES ARE SUBSTITUTED HERE, in the response, so the built artifact
    // on disk is never modified and the next run reads it pristine.
    if (active) {
      if (active.raw && Object.prototype.hasOwnProperty.call(active.raw, key)) {
        record.fixture = 'raw';
        return answer(200, 'application/json', JSON.stringify(active.raw[key]));
      }
      if (active.files && Object.prototype.hasOwnProperty.call(active.files, key)) {
        record.fixture = 'files';
        return answer(200, 'application/json', JSON.stringify(active.files[key]));
      }
      if (active.patch && Object.prototype.hasOwnProperty.call(active.patch, key)) {
        try {
          const real = JSON.parse(await readFile(join(root, 'browse', key), 'utf8'));
          record.fixture = 'patch';
          return answer(200, 'application/json',
                        JSON.stringify(Object.assign({}, real, active.patch[key])));
        } catch (error) { /* fall through to the real file */ }
      }
    }

    try {
      const body = await readFile(join(root, relative));
      const dot = relative.lastIndexOf('.');
      return answer(200, MIME[relative.slice(dot)] || 'application/octet-stream', body);
    } catch (error) {
      return answer(404, 'text/plain', 'not found');
    }
  });
}

/* ------------------------------------------------------------------- CDP */

let nextId = 1;
const pending = new Map();

function send(socket, method, params, sessionId) {
  const id = nextId += 1;
  socket.send(JSON.stringify({ id, method, params: params || {}, sessionId }));
  return new Promise((resolve, reject) => pending.set(id, { resolve, reject }));
}

/* ---------------------------------------------------------- what is read
 * Carried inside a template literal: no regex literal and no backslash
 * escape may appear below, because they are eaten before the page sees them.
 */
const READ = `(() => {
  const reading = document.getElementById('reading');
  const text = (node) => (node ? node.textContent.trim() : null);
  const all = (selector) => Array.from(document.querySelectorAll(selector));
  const value = (id) => { const one = document.getElementById(id); return one ? one.value : null; };
  const here = document.activeElement;
  return {
    // THE V5 REVIEW'S FINDING 3. V5 claimed to read this and never did.
    focus: here ? {
      id: here.id || null,
      tagName: here.tagName ? here.tagName.toLowerCase() : null,
      className: (typeof here.className === 'string' && here.className) || null,
      isReadingItself: here === reading,
      insideReading: !!(reading && reading.contains(here)),
      label: (here.getAttribute && here.getAttribute('aria-label')) || null,
      documentHasFocus: document.hasFocus()
    } : null,
    hash: location.hash,
    title: document.title,
    reference: text(document.getElementById('reference')),
    referenceBook: text(document.getElementById('reference-book')),
    tally: text(document.getElementById('tally')),
    status: text(document.getElementById('reading-status')),
    banner: text(document.getElementById('banner')),
    ariaBusy: reading ? reading.getAttribute('aria-busy') : null,
    bibleOptions: all('#bible-select option').map(text),
    bibleValue: value('bible-select'),
    bookOptions: all('#book-select option').map(text),
    chapterValue: value('chapter-select'),
    voiceOptions: all('#language-select option').map(text),
    // Read as the ATTRIBUTE, not the property.
    langAttributes: all('#reading [lang]').map(
      (one) => (one.className || one.localName) + '=' + one.getAttribute('lang')),
    languageChips: all('.fragment-language').map(text),
    fragmentCount: all('.fragment').length,
    fragmentAuthors: all('.fragment-author').map(text),
    fragmentTexts: all('.fragment-text').map(text),
    // A late response that COMMITS shows here as a value other than the
    // placeholder; the full list above is long, this is the question.
    fragmentTextsDistinct: Array.from(new Set(all('.fragment-text').map(text))).sort(),
    wordChips: all('.fragment-length').map(text),
    verseNumbers: all('.verse-num').map(text),
    verseCount: all('.verse').length,
    chapterCounts: all('.chapter-count').map(text),
    passageLang: (() => { const one = document.querySelector('#reading .passage');
                          return one ? one.getAttribute('lang') : null; })(),
    leads: all('.lead').map(text),
    blocked: all('.blocked').map(text),
    refusals: all('.refusal').map(text),
    absenceSummary: text(document.querySelector('.absence-note summary')),
    absenceAuthors: all('.absence-author').map(text),
    absenceWorks: all('.absence-work').map(text),
    absenceReasons: all('.absence-reason').map(text),
    absencePartials: all('.absence-partial').map(text),
    asideNotes: all('.aside-note').map(text),
    notices: all('#reading .notice').map(text),
    sectionHeadings: all('#reading .section-heading').map(text),
    errorHeadings: all('.catena-error .section-heading').map(text),
    dataStates: Array.from(new Set(all('#reading [data-state]').map(
      (one) => one.getAttribute('data-state')))).sort(),
    // EVERY REQUEST THE PAGE ACTUALLY MADE. A URL built by coercion is a
    // request against nothing, and only the log can show it was made.
    requested: performance.getEntriesByType('resource')
      .map((one) => { try { return new URL(one.name).pathname; } catch (error) { return one.name; } })
      .filter((one) => one.endsWith('.json')).sort()
  };
})()`;

const ACTIONS = {
  openFirstFragment: () => `(() => {
    const one = document.querySelector('#reading .fragment-body');
    if (!one) return 'no fragment to open';
    const head = one.querySelector('summary');
    // FOCUS FIRST. A reader who opens a disclosure focuses it; a bare
    // programmatic click does not, and a focus reading taken after one would
    // be a reading of a state no reader is ever in.
    if (head) { head.focus(); head.click(); } else one.open = true;
    const who = one.querySelector('.fragment-author');
    return 'opened ' + (who ? who.textContent : '(unnamed)');
  })()`,
  openAllFragments: () => `(() => {
    const each = Array.from(document.querySelectorAll('#reading .fragment-body'));
    for (const one of each) {
      const head = one.querySelector('summary');
      if (head) { head.focus(); head.click(); } else one.open = true;
    }
    return 'opened ' + each.length + ' fragments';
  })()`,
  selectChapter: (step) => `(() => {
    const one = document.getElementById('chapter-select');
    if (!one) return 'no chapter control';
    one.focus();
    one.value = ${JSON.stringify(String(step.value))};
    one.dispatchEvent(new Event('change', { bubbles: true }));
    return 'chapter-select = ' + one.value;
  })()`,
  hash: (step) => `(() => {
    location.hash = ${JSON.stringify(String(step.value))};
    return location.hash;
  })()`
};

/* ------------------------------------------------------- PNG self-labelling
 * A PNG that reads, on its own, as a record of real corpus data is exactly
 * the V5 review's finding 2. Every capture below carries its own denial in
 * its own bytes, as an `iTXt` chunk (UTF-8; `tEXt` is Latin-1 and cannot
 * hold an em dash). The chunk text is DETERMINISTIC — no label, no path, no
 * timestamp — so two runs of the same state still hash equal if and only if
 * their rasters are equal, and `pair-audit.py` stays honest.
 */
const CRC_TABLE = (() => {
  const table = new Int32Array(256);
  for (let n = 0; n < 256; n += 1) {
    let c = n;
    for (let k = 0; k < 8; k += 1) c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
    table[n] = c;
  }
  return table;
})();

function crc32(buffer) {
  let c = -1;
  for (let i = 0; i < buffer.length; i += 1) c = CRC_TABLE[(c ^ buffer[i]) & 0xFF] ^ (c >>> 8);
  return (c ^ -1) >>> 0;
}

function chunk(type, data) {
  const length = Buffer.alloc(4);
  length.writeUInt32BE(data.length, 0);
  const body = Buffer.concat([Buffer.from(type, 'latin1'), data]);
  const crc = Buffer.alloc(4);
  crc.writeUInt32BE(crc32(body), 0);
  return Buffer.concat([length, body, crc]);
}

function labelPng(png, comment) {
  // 8 signature + 4 length + 4 'IHDR' + 13 data + 4 crc = 33.
  const at = 33;
  const data = Buffer.concat([
    Buffer.from('Comment', 'latin1'),
    Buffer.from([0, 0, 0]),      // null, compression flag 0, compression method 0
    Buffer.from([0]),            // empty language tag
    Buffer.from([0]),            // empty translated keyword
    Buffer.from(comment, 'utf8')
  ]);
  return Buffer.concat([png.subarray(0, at), chunk('iTXt', data), png.subarray(at)]);
}

/* --------------------------------------------------------------- driving */

async function settle(call, cap) {
  for (let tries = 0; tries < (cap || 40); tries += 1) {
    const done = await call('Runtime.evaluate', {
      expression: "document.querySelector('#reading')?.getAttribute('aria-busy') !== 'true'",
      returnByValue: true });
    if (done.result.value) return true;
    await pause(100);
  }
  return false;
}

async function drive(call, origin, state) {
  releaseHeld(null, 'ok');            // never strand a socket from the last state
  active = state;
  serverLog = [];
  await call('Page.navigate', { url: origin + '/catena/index.html' });
  await pause(300);
  if (state.hash) {
    await call('Runtime.evaluate',
               { expression: 'location.hash = ' + JSON.stringify(state.hash) + ';' });
  }
  await pause(1400);
  await settle(call, state.defer ? 15 : 40);

  const steps = [];
  for (const step of state.steps || []) {
    let acted;
    if (step.do === 'release') {
      const n = releaseHeld(step.path, step.outcome || 'ok');
      acted = 'released ' + n + ' held request(s) matching ' + step.path +
              ' as ' + (step.outcome || 'ok');
    } else {
      const done = await call('Runtime.evaluate',
                              { expression: ACTIONS[step.do](step), returnByValue: true });
      acted = done.result.value;
    }
    await pause(step.settle == null ? 1000 : step.settle);
    await settle(call, state.defer ? 15 : 40);
    const seen = await call('Runtime.evaluate', { expression: READ, returnByValue: true });
    steps.push({ label: step.label, did: step.do, acted: acted, read: seen.result.value });
  }

  const last = await call('Runtime.evaluate', { expression: READ, returnByValue: true });
  const requests = serverLog.slice();
  releaseHeld(null, 'ok');
  return { steps: steps, terminal: last.result.value, serverRequests: requests };
}

/** The keys on which two terminal reads differ, deep-compared. */
function differingKeys(one, other) {
  const keys = Array.from(new Set(Object.keys(one || {}).concat(Object.keys(other || {})))).sort();
  return keys.filter((key) => JSON.stringify((one || {})[key]) !== JSON.stringify((other || {})[key]));
}

function stateBanner(state) {
  return state.fabricated
    ? { fabricated: true, represents: FABRICATED }
    : { fabricated: false, represents: REAL,
        manipulated: state.manipulated || 'nothing' };
}

async function main() {
  let states = STATES;
  if (process.env.TRIPTYCH_PROBE_STATES) {
    states = JSON.parse(await readFile(process.env.TRIPTYCH_PROBE_STATES, 'utf8'));
  }

  const server = serve(ROOT);
  await new Promise((go) => server.listen(0, '127.0.0.1', go));
  const origin = 'http://127.0.0.1:' + server.address().port;

  const port = 9200 + (process.pid % 300);
  const chrome = spawn(CHROME, [
    '--headless=new', '--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage',
    '--hide-scrollbars', '--force-device-scale-factor=1',
    '--force-color-profile=srgb', '--remote-debugging-port=' + port, 'about:blank'
  ], { stdio: 'ignore' });

  let version = null;
  for (let tries = 0; tries < 200 && !version; tries += 1) {
    await pause(100);
    try {
      version = await (await fetch('http://127.0.0.1:' + port + '/json/version')).json();
    } catch (error) { /* not up yet */ }
  }
  if (!version) throw new Error('Chromium did not expose a DevTools endpoint');

  const socket = new WebSocket(version.webSocketDebuggerUrl);
  await new Promise((resolve, reject) => {
    socket.addEventListener('open', resolve);
    socket.addEventListener('error', reject);
  });
  socket.addEventListener('message', (event) => {
    const message = JSON.parse(event.data);
    const waiting = pending.get(message.id);
    if (!waiting) return;
    pending.delete(message.id);
    if (message.error) waiting.reject(new Error(JSON.stringify(message.error)));
    else waiting.resolve(message.result);
  });

  const { targetId } = await send(socket, 'Target.createTarget', { url: 'about:blank' });
  const { sessionId } = await send(socket, 'Target.attachToTarget', { targetId, flatten: true });
  const call = (method, params) => send(socket, method, params, sessionId);

  await call('Page.enable');
  await call('Runtime.enable');
  await call('Emulation.setDeviceMetricsOverride',
             { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });

  const fabricatedNames = states.filter((one) => one.fabricated).map((one) => one.name);
  const realNames = states.filter((one) => !one.fabricated).map((one) => one.name);

  const report = {
    tool: 'probe-catena.mjs',
    label: LABEL,
    siteRoot: ROOT,
    browser: version.Browser,
    viewport: '1440x900 for every DOM read',
    // THE ROOT LABEL. Honest about being mixed rather than banner-blanketing.
    fabricated: true,
    represents: 'MIXED EVIDENCE. This report contains states driven by ' +
      FABRICATED + '. Read each state’s own `fabricated` field: a state ' +
      'marked false used the real built corpus and says what, if anything, ' +
      'was manipulated. Nothing here is a picture of the published site.',
    fabricatedStates: fabricatedNames,
    realCorpusStates: realNames,
    states: {}
  };

  for (const state of states) {
    const seen = await drive(call, origin, state);
    report.states[state.name] = Object.assign(stateBanner(state), {
      class: state.class,
      address: state.hash || '(no address)',
      fixtures: state.fixtures || [],
      reads: state.reads,
      captured: !!(SHOTS && state.picture),
      capturedViewports: state.picture
        ? (state.viewports || VIEWPORTS).map((one) => one[0] + 'x' + one[1])
        : [],
      notCapturedBecause: (SHOTS && !state.picture)
        ? 'the finding of this state is not in the raster'
        : undefined,
      steps: seen.steps,
      terminal: seen.terminal,
      serverRequests: seen.serverRequests
    });
  }

  // ORDER INDEPENDENCE, STATED BY THE REPORT ITSELF rather than left for a
  // reader to diff by eye.
  for (const state of states.filter((one) => one.compareWith)) {
    const mine = report.states[state.name];
    const theirs = report.states[state.compareWith];
    if (!mine || !theirs) continue;
    const differing = differingKeys(mine.terminal, theirs.terminal);
    mine.comparison = {
      against: state.compareWith,
      terminalReadsEqual: differing.length === 0,
      differingKeys: differing,
      note: differing.length === 0
        ? 'Every field of the terminal read is equal: the same finding set in ' +
          'the opposite order produced the same page.'
        : 'The two orders produced DIFFERENT pages on the keys listed.'
    };
  }

  if (SHOTS) {
    await mkdir(SHOTS, { recursive: true });
    const index = [];
    for (const state of states.filter((one) => one.picture)) {
      for (const [width, height] of state.viewports || VIEWPORTS) {
        await call('Emulation.setDeviceMetricsOverride',
                   { width, height, deviceScaleFactor: 1, mobile: false });
        await drive(call, origin, state);
        // BEYOND THE VIEWPORT ONLY WHERE THE FINDING IS BELOW THE FOLD. A
        // viewport capture that does not frame the changed region cannot
        // support any description of it, and shipping one is the V5 mistake.
        const shot = await call('Page.captureScreenshot',
                                { format: 'png',
                                  captureBeyondViewport: !!state.fullPage });
        const raw = Buffer.from(shot.data, 'base64');
        const banner = stateBanner(state);
        const bytes = labelPng(raw, (banner.fabricated ? FABRICATED : REAL) +
                               ' | state=' + state.name +
                               ' | fabricated=' + banner.fabricated);
        const file = (PREFIX || 'after--') + 'catena--' + state.name +
                     '--' + width + 'x' + height + '.png';
        await writeFile(join(SHOTS, file), bytes);
        index.push(Object.assign({ file: file }, banner, {
          state: state.name,
          class: state.class,
          address: state.hash || '(no address)',
          viewport: width + 'x' + height,
          frame: state.fullPage ? 'whole document (captureBeyondViewport)'
                                : 'viewport only',
          variant: 'default',
          media: 'screen',
          // WHAT THIS RUN RENDERS. Not a claim that it differs from another
          // run: no single run can establish that.
          renders: state.picture,
          differsFromPartner: null,
          differenceEstablishedBy: 'pair-audit.py over a before--/after-- pair',
          bytes: bytes.length,
          sha256: createHash('sha256').update(bytes).digest('hex'),
          selfLabelledIn: 'PNG iTXt chunk, keyword Comment'
        }));
      }
    }
    await writeFile(join(SHOTS, (PREFIX || 'after--') + 'probe-index.json'),
      JSON.stringify({
        tool: 'probe-catena.mjs',
        label: LABEL,
        fabricated: true,
        represents: report.represents,
        note: 'Each entry carries its own `fabricated` and `represents`. ' +
          'No entry claims a visual difference; `pair-audit.py` establishes that.',
        shots: index
      }, null, 2) + '\n');
    report.screenshots = index.length;
    report.screenshotIndex = (PREFIX || 'after--') + 'probe-index.json';
  }

  await writeFile(OUT, JSON.stringify(report, null, 2) + '\n');
  socket.close();
  chrome.kill();
  server.close();
  const withPicture = states.filter((one) => one.picture);
  const captured = withPicture.length;
  const pngs = withPicture.reduce(
    (total, one) => total + (one.viewports || VIEWPORTS).length, 0);
  console.log('probed ' + states.length + ' states at "' + LABEL + '" -> ' + OUT);
  console.log('  fabricated states: ' + fabricatedNames.length +
              '; real-corpus states: ' + realNames.length);
  console.log('  captured ' + (SHOTS ? captured : 0) + ' of ' + states.length +
              ' states' + (SHOTS ? ' = ' + pngs + ' PNGs' : ' (no shot dir given)'));
  console.log('  not captured: ' + states.filter((one) => !one.picture)
              .map((one) => one.name).join(', ') +
              ' — their findings are not in the raster');
  process.exit(0);
}

main().catch((error) => {
  console.error('PROBE FAILED: ' + ((error && error.stack) || error));
  process.exit(1);
});
