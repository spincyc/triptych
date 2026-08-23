# Source + Formulary Audit

## Your task

Audit the sources and formulary for the target proper. Verify the appointed
texts against the controlling witnesses.

## Steps

1. Read the `propers/verified.md` file if it exists. This contains the
   facsimile-collated appointed text in liturgical order.
2. Read the `propers/retrieved.txt` file if it exists. This is the
   machine-readable pull from the controlling edition.
3. If neither exists, retrieve the formulary from the CMAA 1962 Missale
   Romanum facsimile (the controlling witness for Latin text, rubrics,
   rank, references, and formulary boundaries).
4. Collate every Latin form, rubric, citation, and boundary against the
   controlling facsimile.
5. Check unclear readings against the Internet Archive image item
   (secondary witness).
6. Record any unresolved discrepancies.
7. Verify that the English translations follow the repository rules:
   - Scriptural elements: Douay-Rheims (Challoner)
   - Orations: registered public-domain hand missal
8. Read `guidance/sources.md` before adding or reusing any external source.

## Result

Return a worker result with `disposition: "PASS"` and a summary of the
audit, including:
- whether verified.md and retrieved.txt exist
- any discrepancies found
- the rights status of the appointed texts
- whether the English translations follow repository rules
