"""Exact original-expression rights predicates shared by checker and reader."""

import re

# The United States nonrenewal finding reaches only this original expression,
# not later Lasance matter or an arbitrary post-1930 claim.
LASANCE_1945_EDITION = (
    "edition.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945"
)
LASANCE_1945_RIGHTS_ARTIFACT = (
    "artifact.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945."
    "new-roman-missal-text-80b34759"
)
LASANCE_1945_RIGHTS_SHA256 = (
    "80b34759fb18ec60f6205460c2ac24dc9e4a861938a94ef1f8e04a08a398ac9a"
)
LASANCE_1945_PAGE_ARTIFACT = (
    "artifact.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945."
    "internet-archive-facsimile-pdf-6cf3c3d0"
)
LASANCE_1945_PAGE_SHA256 = (
    "6cf3c3d01b853bc4a35c1cc9b0a4e54a0489a5ccf5d9a742bb681ac10608ce70"
)


def _approved_lasance_1945_publication(
    entry: dict, artifact: dict, records: dict, witnesses: dict[str, dict] | None,
) -> bool:
    """Recognize the settled rights owner without clearing the facsimile PDF.

    The excluded-insert OCR owns the registered publication basis. A checked
    transcription may derive from the separate, unresolved PDF used only for
    page inspection. Neither freeform rights prose nor PDF bytes are cleared.
    """
    if (
        artifact.get("edition_id") != LASANCE_1945_EDITION
        or entry.get("witness") != "lasance-1945"
    ):
        return False
    witness = (witnesses or {}).get("lasance-1945")
    if witness is None:
        # Consumers may key the same source row by edition/artifact aliases.
        # The alias must still resolve the named source row.
        witness = (witnesses or {}).get(LASANCE_1945_EDITION)
        if not isinstance(witness, dict) or witness.get("id") != "lasance-1945":
            return False
    if (
        not isinstance(witness, dict)
        or witness.get("source_id") != LASANCE_1945_EDITION
        or witness.get("artifact_id") != LASANCE_1945_RIGHTS_ARTIFACT
        or witness.get("rights") != "public-domain"
    ):
        return False
    rights = records.get(LASANCE_1945_RIGHTS_ARTIFACT)
    if rights is None or rights.record_type != "artifact":
        return False
    expected = {
        "edition_id": LASANCE_1945_EDITION,
        "sha256": LASANCE_1945_RIGHTS_SHA256,
        "rights_status": "public-domain",
        "rights_jurisdiction": "United States",
        "storage": "tracked",
    }
    if any(rights.data.get(key) != value for key, value in expected.items()):
        return False
    page = records.get(LASANCE_1945_PAGE_ARTIFACT)
    return (
        entry.get("artifact_id") == LASANCE_1945_PAGE_ARTIFACT
        and page is not None
        and page.record_type == "artifact"
        and page.data.get("edition_id") == LASANCE_1945_EDITION
        and page.data.get("sha256") == LASANCE_1945_PAGE_SHA256
        and artifact.get("derived_from") in {
            LASANCE_1945_PAGE_ARTIFACT, LASANCE_1945_RIGHTS_ARTIFACT,
        }
    )


# This physically identified printing retains its actual date and unresolved
# whole-scan status. Only checked original-expression transcriptions qualify.
LASANCE_1946_EDITION = (
    "edition.francis-xavier-lasance.the-new-roman-missal."
    "benziger-revised-1945-printing-1946"
)
LASANCE_1946_PAGE_ARTIFACT = (
    "artifact.francis-xavier-lasance.the-new-roman-missal."
    "benziger-revised-1945-printing-1946.ia-google-facsimile-pdf-4573991d"
)
LASANCE_1946_PAGE_SHA256 = (
    "4573991d962eb6a6391bc2555b8445bdfebd84de1ccffd7828f84e74d308ca77"
)
LASANCE_1946_WITNESS = "lasance-1945-printing-1946"
LASANCE_PUBLICATION_EDITIONS = frozenset((LASANCE_1945_EDITION, LASANCE_1946_EDITION))
LASANCE_PUBLICATION_RECORD_IDS = (
    LASANCE_1945_EDITION, LASANCE_1946_EDITION,
    LASANCE_1945_RIGHTS_ARTIFACT,
    LASANCE_1945_PAGE_ARTIFACT, LASANCE_1946_PAGE_ARTIFACT,
)


def numbered_page_match(value):
    """Match positive, ordered literal page labels, keeping both endpoints."""
    match = (
        re.fullmatch(r"([0-9]+[a-z]?)(?:-([0-9]+[a-z]?))?", value)
        if isinstance(value, str) else None
    )
    if match is None:
        return None
    first = _page_key(match.group(1))
    last = _page_key(match.group(2) or match.group(1))
    return match if first[0] > 0 and first <= last else None


def _page_key(label):
    """An inserted lettered leaf follows its unlettered numbered page."""
    number = label.rstrip("abcdefghijklmnopqrstuvwxyz")
    return int(number), label[len(number):]


def approved_lasance_printed_page(entry):
    """Keep later inserts out even when the general locator admits letters."""
    witness = entry.get("witness")
    if witness not in {"lasance-1945", LASANCE_1946_WITNESS}:
        return True
    match = numbered_page_match(entry.get("printed_page"))
    if match is None:
        return False
    first = _page_key(match.group(1))
    last = _page_key(match.group(2) or match.group(1))
    if witness == LASANCE_1946_WITNESS and (first[1] or last[1]):
        # The separately reviewed printing route covers ordinary numbered
        # pages only; physical PDF bounds are checked separately below.
        return False
    return not any(
        first <= excluded_last and excluded_first <= last
        for excluded_first, excluded_last in (
            ((1298, "a"), (1298, "n")),
            ((1302, "a"), (1302, "d")),
        )
    )


def _approved_lasance_1946_publication(entry, artifact, records, witnesses):
    if (
        artifact.get("edition_id") != LASANCE_1946_EDITION
        or entry.get("witness") != LASANCE_1946_WITNESS
    ):
        return False
    witness = (witnesses or {}).get(LASANCE_1946_WITNESS)
    if witness is None:
        witness = (witnesses or {}).get(LASANCE_1946_EDITION)
        if not isinstance(witness, dict) or witness.get("id") != LASANCE_1946_WITNESS:
            return False
    if (
        not isinstance(witness, dict)
        or witness.get("id") != LASANCE_1946_WITNESS
        or witness.get("source_id") != LASANCE_1946_EDITION
        or witness.get("artifact_id") != LASANCE_1945_RIGHTS_ARTIFACT
        or witness.get("rights") != "public-domain"
        or witness.get("rights_jurisdiction") != "United States"
        or not str(witness.get("caution") or "").strip()
    ):
        return False
    rights = records.get(LASANCE_1945_RIGHTS_ARTIFACT)
    if rights is None or rights.record_type != "artifact":
        return False
    expected_rights = {
        "edition_id": LASANCE_1945_EDITION,
        "sha256": LASANCE_1945_RIGHTS_SHA256,
        "rights_status": "public-domain",
        "rights_jurisdiction": "United States",
        "storage": "tracked",
    }
    if any(rights.data.get(key) != value for key, value in expected_rights.items()):
        return False
    page = records.get(LASANCE_1946_PAGE_ARTIFACT)
    expected_page = {
        "edition_id": LASANCE_1946_EDITION,
        "sha256": LASANCE_1946_PAGE_SHA256,
        "artifact_type": "facsimile-pdf",
        "media_type": "application/pdf",
        "storage": "remote",
        "rights_status": "unresolved",
        "indexable": False,
        "byte_size": 135628123,
        "page_count": 1884,
    }
    leaves = entry.get("ia_leaf_range")
    return (
        entry.get("artifact_id") == LASANCE_1946_PAGE_ARTIFACT
        and page is not None
        and page.record_type == "artifact"
        and all(page.data.get(key) == value for key, value in expected_page.items())
        and artifact.get("derived_from") == LASANCE_1946_PAGE_ARTIFACT
        and isinstance(leaves, list) and len(leaves) == 2
        and all(isinstance(n, int) and not isinstance(n, bool) for n in leaves)
        and 0 <= leaves[0] <= leaves[1] < 1884
    )


def approved_lasance_publication(entry, artifact, records, witnesses):
    """Recognize only the registered expression and exact verified printing."""
    edition_id = artifact.get("edition_id")
    edition = records.get(edition_id)
    if edition is None or edition.record_type != "edition":
        return False
    if not approved_lasance_printed_page(entry):
        return False
    if edition_id == LASANCE_1945_EDITION and edition.data.get("date") == "1945":
        return _approved_lasance_1945_publication(entry, artifact, records, witnesses)
    if (
        edition_id == LASANCE_1946_EDITION
        and edition.data.get("date") == "1946"
        and edition.data.get("language") == "en"
        and edition.data.get("work_id") == "work.francis-xavier-lasance.the-new-roman-missal"
    ):
        return _approved_lasance_1946_publication(entry, artifact, records, witnesses)
    return False


def shared_lasance_rights_owner(alias, first, second):
    """Keep the original artifact alias for the one proved shared rights pair."""
    if alias != LASANCE_1945_RIGHTS_ARTIFACT:
        return None
    rows = (first, second)
    if not all(isinstance(row, dict) for row in rows):
        return None
    if {(row.get("id"), row.get("source_id")) for row in rows} != {
        ("lasance-1945", LASANCE_1945_EDITION),
        (LASANCE_1946_WITNESS, LASANCE_1946_EDITION),
    }:
        return None
    if not all(
        row.get("artifact_id") == alias
        and row.get("rights") == "public-domain"
        and row.get("rights_jurisdiction") == "United States"
        and str(row.get("caution") or "").strip()
        for row in rows
    ):
        return None
    return next(row for row in rows if row["id"] == "lasance-1945")
