"""Deterministic projections a document-type template can slot.

Each module here is one projection, discovered by file name: no list to edit.
A module declares ``NAME`` (its file name with ``-`` for ``_``), ``OUTPUTS``
(output key -> leaf-relative generated path) and ``render(context)``, which
returns every file it owns for one leaf as ``{leaf-relative path: text}``:
at least the outputs named in ``context.outputs`` (those the leaf's templates
slot) and any support files it regenerates. A file left under the leaf's
``generated/`` that no projection returns any more is removed by ``refresh``
and refused by ``refresh --check``.
``scripts/_document_types.py`` runs a projection for each leaf whose templates
contain a ``%@ slot <NAME>/<output>`` line, and ``tools/tpt document-types
refresh --check`` holds every returned file to its regeneration.
"""
