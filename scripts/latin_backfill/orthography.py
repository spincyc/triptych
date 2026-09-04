"""J-orthography normalisation for 1962 calendar bodies.

The calendar declares "j retained" and states at propers.yaml:11391 that the
typica's `iugiter` is normalised to `jugiter`.  Only CONSONANTAL i becomes j.
Vocalic i (gloria, hostia, propitius, nullius) must never be touched, so this
uses an explicit map and refuses anything it has not been taught.
"""
import re

MAP = {
    # Divine and proper names
    "Iesu": "Jesu", "Iesum": "Jesum", "Iesus": "Jesus", "Iesui": "Jesui",
    "Ioseph": "Joseph", "Ioannes": "Joannes", "Ioannis": "Joannis",
    "Ioannem": "Joannem", "Iacob": "Jacob", "Iacobi": "Jacobi",
    "Ierusalem": "Jerusalem", "Iudaeae": "Judaeae", "Iudas": "Judas",
    "Ioannae": "Joannae",
    # Pronoun genitives
    "eius": "ejus", "eiusdem": "ejusdem", "cuius": "cujus", "huius": "hujus",
    "ipsius": "ipsius",  # vocalic, identity, kept so it is never flagged
    # Consonantal i in stems and compounds
    "iugiter": "jugiter", "iuge": "juge", "iugum": "jugum", "iuges": "juges",
    "iuvene": "juvene", "iuventam": "juventam", "iuventus": "juventus",
    "maiestas": "majestas", "maiestatis": "majestatis", "maiestatem": "majestatem",
    "adiuvante": "adjuvante", "adiuva": "adjuva", "adiuvet": "adjuvet",
    "adiuvemur": "adjuvemur", "adiuvamur": "adjuvamur", "adiuvent": "adjuvent",
    "adiutor": "adjutor", "adiutorium": "adjutorium", "adiuvari": "adjuvari",
    "adicias": "adjicias", "adiiciantur": "adjiciantur", "adiicientur": "adjicientur",
    "iustitia": "justitia", "iustitiam": "justitiam", "iustitiae": "justitiae",
    "iustus": "justus", "iusti": "justi", "iuste": "juste", "iustos": "justos",
    "iudicium": "judicium", "iudicii": "judicii", "iudex": "judex",
    "ieiunium": "jejunium", "ieiunii": "jejunii", "ieiunio": "jejunio",
    "ieiuniis": "jejuniis", "ieiunia": "jejunia",
    "iam": "jam", "iure": "jure", "iussu": "jussu", "iubilate": "jubilate",
    "coniunctus": "conjunctus", "coniunctione": "conjunctione",
    "coniuge": "conjuge", "iniuria": "injuria", "iniquitas": "iniquitas",
    "obiectum": "objectum", "subiectum": "subjectum", "subiectorum": "subjectorum",
    "subiectis": "subjectis", "traiectus": "trajectus",
    "peius": "pejus", "seiunctus": "sejunctus",
    "Iob": "Job", "eiusdemque": "ejusdemque", "eiusque": "ejusque",
    "Iesse": "Jesse", "Caietano": "Cajetano", "Caietanus": "Cajetanus", "Ianuarii": "Januarii", "Ianuario": "Januario",
    "Ianuarius": "Januarius", "Iosaphat": "Josaphat", "Iosephi": "Josephi",
    "Iosephus": "Josephus", "Iuda": "Juda", "Iudae": "Judae", "Iudam": "Judam",
    "iugem": "jugem", "Ioachim": "Joachim", "Iosepho": "Josepho",
    "Iosephum": "Josephum", "adiutorem": "adjutorem", "iusta": "justa",
    "iuventutem": "juventutem", "maius": "majus",
    "maior": "major", "maiora": "majora", "maiorem": "majorem",
    "subiacere": "subjacere", "subiaceat": "subjaceat",
    "adiungere": "adjungere", "coniungere": "conjungere",
    "iucundemur": "jucundemur", "iucunditas": "jucunditas",
    "iubilatio": "jubilatio", "iucunda": "jucunda", "iucundus": "jucundus",
    "iucundam": "jucundam", "iucundo": "jucundo", "iucundos": "jucundos",
    "Iuxta": "Juxta", "iuxta": "juxta", "maiestati": "majestati",
    "iudicem": "judicem", "iudicare": "judicare", "iudicaturus": "judicaturus",
    "Iuvenale": "Juvenale", "Iuvenalis": "Juvenalis",
    "Ioannam": "Joannam", "Ioannem": "Joannem", "Ioanne": "Joanne",
    "Iulianam": "Julianam", "Iuliana": "Juliana", "Iuliani": "Juliani",
    "Iustina": "Justina", "Iustinae": "Justinae", "Iustinus": "Justinus",
    "adiuvetur": "adjuvetur",
    "iurgia": "jurgia", "iurgium": "jurgium",
    "iustificatarum": "justificatarum", "iustificatio": "justificatio",
    "iustificet": "justificet", "iustorum": "justorum",
}
# Words that LOOK consonantal to a naive rule but are vocalic and must not change.
KNOWN_VOCALIC = {
    "illius", "nullius", "unius", "utriusque", "interius", "exteriusque",
    "puriores", "prius", "alius", "totius", "solius", "Israel", "Israelis",
    # The calendar's house form is Alleluia, 249 occurrences against 5 Alleluja.
    "alleluia", "Alleluia", "Eia", "eia",
}
# Only three shapes are reliably consonantal in this Latin:
#   word-initial i before a vowel   (Iesus, iustus, iugiter, iam)
#   a recognised prefix + i + vowel (adiuvante, coniunctus, subiectum)
#   true intervocalic i             (eius, cuius, huius, maiestas)
# Everything else -- the vast -tio/-tia/-ius families, gloria, hostia,
# sacrificium, nullius -- is vocalic and must never be touched.  The `qu`
# digraph is excluded so quia and quiescat do not read as intervocalic.
SUSPICIOUS = re.compile(
    r"^[Ii][aeouAEOU]"
    r"|^(?:ad|con|in|ob|sub|tra|Ad|Con|In|Ob|Sub|Tra)[Ii][aeou]"
    r"|[aeoAEO][Ii][aeou]"
    r"|(?<![qQ])[uU][Ii][aeou]"
)

def normalise(text: str) -> tuple[str, list[str]]:
    """Return (normalised text, list of unmapped suspicious words)."""
    unmapped: list[str] = []
    def repl(m: re.Match) -> str:
        w = m.group(0)
        if w in MAP:
            return MAP[w]
        if w in KNOWN_VOCALIC or w.lower() in KNOWN_VOCALIC:
            return w
        if SUSPICIOUS.search(w):
            low = w.lower()
            if low in MAP:
                out = MAP[low]
                return out.capitalize() if w[0].isupper() else out
            unmapped.append(w)
        return w
    out = re.sub(r"[A-Za-z]+", repl, text)
    return out, unmapped
