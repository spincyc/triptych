"""Exact original-expression rights predicate shared by checker and reader."""

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


def approved_lasance_publication(
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
