"""Deterministic projections a document-type template can slot.

Each module here is one projection, discovered by file name: no list to edit.
A module declares ``NAME`` (its file name with ``-`` for ``_``), ``OUTPUTS``
(output key -> leaf-relative generated path) and ``render(context)``, which
returns every file it owns for one leaf as ``{leaf-relative path: text}``.
``scripts/_document_types.py`` runs a projection for each leaf whose templates
contain a ``%@ slot <NAME>/<output>`` line, and ``tools/tpt document-types
refresh --check`` holds every returned file to its regeneration.
"""
