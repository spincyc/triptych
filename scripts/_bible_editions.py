"""Source-index Bible registry, shared without importing a CLI or resolver.

Optional verse_aliases_artifact_id and book_index_artifact_id: each a nonempty
exact artifact ID for its reference-table role. It selects
one alias interpretation while preserving every historical artifact identity.
The selection contract is validated by _bible_artifacts. No source-library
manifest schema or fingerprint input is changed.
"""
from __future__ import annotations

# One entry per indexed edition. `artifacts` is the tracked artifact directory
# of the edition in the source library; the verse files, book index, and verse
# aliases are selected inside it by the exact optional verse_aliases_artifact_id.
# With no active ID, exactly one legacy alias table must exist. See _bible_artifacts.
#
# `psalm_titles` says whether the edition gives a psalm's inscription a verse
# number of its own. That is not a second numbering system — the chapters and
# the body agree — but it shifts every numbered verse of most psalms, so an
# edition that leaves the inscription unnumbered cannot be addressed by the
# numbers a title-numbering calendar prints. See `unnumber_titles`.
EDITIONS: dict[str, dict[str, object]] = {
    "douay-rheims": {
        "rank": 10,
        "label": "Douay-Rheims (Challoner)",
        "edition": "The Holy Bible, Douay-Rheims (Challoner revision), "
        "Project Gutenberg eBook 1581",
        "source_id": "edition.english-college-of-douay.douay-rheims-bible"
        ".challoner-gutenberg-1581",
        "rights": "public-domain",
        "publishable": True,
        "numbering": "vulgate",
        "language": "en",
        # Challoner translated the Clementine text, whose psalter is Gallican.
        "psalter": "gallican",
        "psalm_titles": "numbered",
        "artifacts": "english-college-of-douay/douay-rheims-bible/editions"
        "/challoner-gutenberg-1581/artifacts",
    },
    # The other electronic Douay-Rheims. It is registered as a textual control
    # on the Challoner e-text, not as a second reading text, and it is offered
    # because a reader matching a printed American Bible needs it; see the
    # edition record before preferring either.
    "douay-rheims-american-1899": {
        "rank": 15,
        "label": "Douay-Rheims (American 1899)",
        "edition": "The Holy Bible in English, Douay-Rheims American Edition of 1899, "
        "eBible.org engDRA",
        "source_id": "edition.english-college-of-douay.douay-rheims-bible.american-1899-ebible",
        "rights": "public-domain",
        "publishable": True,
        "numbering": "vulgate",
        "language": "en",
        "psalter": "gallican",
        "psalm_titles": "numbered",
        "artifacts": "english-college-of-douay/douay-rheims-bible/editions"
        "/american-1899-ebible/artifacts",
        "verse_aliases_artifact_id": "artifact.english-college-of-douay.douay-rheims-bible.american-1899-ebible.verse-aliases-6aa4a25e",
    },
    "clementine-vulgate": {
        "rank": 20,
        "label": "Clementine Vulgate (Latin)",
        "edition": "Biblia Sacra Vulgatae Editionis Clementina, eBible.org latVUC",
        "source_id": "edition.catholic-church.vulgata-clementina.ebible-latvuc",
        "rights": "public-domain",
        "publishable": True,
        "numbering": "vulgate",
        "language": "la",
        # The 1962 books print the Gallican psalter. It is not the psalter the
        # Mass chants sing; see this edition's record before matching an incipit.
        "psalter": "gallican",
        "psalm_titles": "numbered",
        "artifacts": "catholic-church/vulgata-clementina/editions/ebible-latvuc/artifacts",
    },
    "king-james-version": {
        "rank": 40,
        "label": "King James, with Apocrypha",
        "edition": "The Holy Bible, King James Version with the Apocrypha, "
        "eBible.org eng-kjv",
        "source_id": "edition.church-of-england.king-james-version.ebible-engkjv",
        "rights": "public-domain",
        "publishable": True,
        "numbering": "hebrew",
        "language": "en",
        # Not one of the Latin recensions: the King James psalter was Englished
        # from the Hebrew, so the text it witnesses is the Masoretic one. A
        # Latin value here would read as a match against editions it does not
        # match.
        "psalter": "masoretic",
        # This edition prints a psalm's inscription unnumbered, so its verse
        # numbers run one or two lower than the Hebrew numbering through the
        # body of most psalms.
        "psalm_titles": "unnumbered",
        "artifacts": "church-of-england/king-james-version/editions/ebible-engkjv/artifacts",
        "verse_aliases_artifact_id": "artifact.church-of-england.king-james-version.ebible-engkjv.verse-aliases-4c994ba5",
        "book_index_artifact_id": "artifact.church-of-england.king-james-version.ebible-engkjv.book-index-a902065b",
    },
    "world-english-bible-catholic": {
        "rank": 30,
        "label": "World English, Catholic Edition",
        "edition": "The World English Bible, Catholic Edition, eBible.org eng-web-c",
        "source_id": "edition.ebible-org.world-english-bible.catholic-eng-web-c",
        "rights": "public-domain",
        "publishable": True,
        "numbering": "hebrew",
        "language": "en",
        # An update of the American Standard Version of 1901 revised against
        # the Biblia Hebraica Stuttgartensia, so its psalter witnesses the
        # Masoretic text and no Latin recension. It is the only modern-English
        # text of the whole Catholic canon this library may redistribute, and
        # it is still not a witness to the Latin the 1962 Missal prints.
        "psalter": "masoretic",
        # Psalm inscriptions are printed as headings without a verse number, so
        # the body of most psalms runs one or two lower than Hebrew numbering.
        "psalm_titles": "unnumbered",
        "artifacts": "ebible-org/world-english-bible/editions/catholic-eng-web-c/artifacts",
        "verse_aliases_artifact_id": "artifact.ebible-org.world-english-bible.catholic-eng-web-c.verse-aliases-748c36dc",
        "book_index_artifact_id": "artifact.ebible-org.world-english-bible.catholic-eng-web-c.book-index-6e42c682",
    },
    # A modern-English translation made from the Sixto-Clementine Latin, so
    # unlike the other modern English editions here it carries the Vulgate's own
    # chapter and verse numbers. It is a one-man translation without
    # ecclesiastical approbation; see the edition record before resting a claim
    # on it.
    "catholic-public-domain-version": {
        "rank": 25,
        "label": "Catholic Public Domain Version",
        "edition": "The Sacred Bible, Catholic Public Domain Version, Original Edition, "
        "sacredbible.org",
        "source_id": "edition.ronald-conte.catholic-public-domain-version"
        ".sacredbible-original-web-2026-07-31",
        "rights": "public-domain",
        "publishable": True,
        "numbering": "vulgate",
        "language": "en",
        # Englished from the Clementine, whose psalter is Gallican.
        "psalter": "gallican",
        "psalm_titles": "numbered",
        "artifacts": "ronald-conte/catholic-public-domain-version/editions"
        "/sacredbible-original-web-2026-07-31/artifacts",
        "verse_aliases_artifact_id": "artifact.ronald-conte.catholic-public-domain-version.sacredbible-original-web-2026-07-31.verse-aliases-31d31383",
    },
    "revised-version-1895": {
        "rank": 50,
        "label": "Revised Version, with Apocrypha",
        "edition": "The Revised Version of the Holy Bible with Apocrypha (1895), "
        "eBible.org eng-rv",
        "source_id": "edition.convocation-of-canterbury.revised-version.ebible-eng-rv",
        # Public domain in the United States and everywhere outside the United
        # Kingdom; inside it the Crown's perpetual letters patent in the
        # Authorized Version and its revisions still run. The edition record
        # states the limit and every manifest names the jurisdiction.
        "rights": "public-domain",
        "publishable": True,
        "numbering": "hebrew",
        "language": "en",
        # Revised from the Hebrew, so the psalter it witnesses is Masoretic.
        "psalter": "masoretic",
        "psalm_titles": "unnumbered",
        "artifacts": "convocation-of-canterbury/revised-version/editions/ebible-eng-rv/artifacts",
        "verse_aliases_artifact_id": "artifact.convocation-of-canterbury.revised-version.ebible-eng-rv.verse-aliases-cb6721c1",
        "book_index_artifact_id": "artifact.convocation-of-canterbury.revised-version.ebible-eng-rv.book-index-063751e5",
    },
    # Licensed and not redistributable: its artifacts live outside this
    # repository and are reached with --source-root, and its index must be
    # written outside it too with --bible-root. `publishable: false` keeps it
    # out of the public artifact even if an index is built by mistake.
    "knox": {
        "rank": 90,
        "label": "Knox",
        "edition": "The Holy Bible, translated by Monsignor Ronald Knox",
        "source_id": "edition.westminster-diocese.knox-translation.baronius-2012",
        "rights": "licensed",
        "publishable": False,
        "numbering": "vulgate",
        "language": "en",
        "psalter": "gallican",
        "psalm_titles": "numbered",
        "artifacts": "knox/artifacts",
    },
}
