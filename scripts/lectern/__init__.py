"""A terminal reader for the published Triptych structure.

The package renders what the browser renders, from the same files under
`src/web/data/`, and derives nothing of its own: every derivation is asked of
the shared browser model that already owns it.
"""

SURFACES = (
    ("1", "Day", "day"),
    ("2", "Propers", "propers"),
    ("3", "Catena", "catena"),
    ("4", "Scripture", "scripture"),
    ("5", "Texts", "texts"),
    ("6", "Sources", "sources"),
    ("7", "History", "history"),
    ("8", "Law", "law"),
)
