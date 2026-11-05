# Write the speakable homily

Read both reviewed studies. Write the homily-only components as a finished homily to `ARGS.audience` (default adult parish assembly), ordinarily 10–12 minutes at
an unhurried pace. Choose one coherent reading or a demonstrably compatible
combination. The speech need not inventory every minor proper, but its
exegetical argument must meaningfully join the Gospel, other appointed
Scripture, and the Mass's prayer.

Explain what the texts say and what follows from them for this assembly. Move
from attention and understanding toward conversion and hope. Teach plainly:
tell the scene, explain a difficult word, set side by side the texts the Mass
sets side by side. One practicable response may close the application, drawn
from the text and said once. Devices are not requirements; follow the
profile's homily section and `guidance/editorial.md`, "Say what the texts say,
plainly". The speech has no maxim closers, recurring tag or motif, relatable
inventory of the listeners' lives, slogan, stock call, emphatic fragment, or
question answered in the next breath. Nor is it a lecture: the preacher's own
voice carries the argument, quotations are few and short, Latin appears only
where the speech explains it, authorities' dates stay in the note, and the
speech ends on its conclusion, spoken to the assembly. Write for one hearing,
gloss only what a regular congregation would not know, and let the one
response grow from the argument the speech has made. Do not manufacture anecdotes, personal
experience, clerical identity, miraculous stories, or attributed quotations.

Apply the three-document profile's test of how the appointed text changes the
listener's understanding; record the decisive textual detail in the production
audit.

The body is ready to read verbatim: continuous preaching, no outline, stage
directions, advice to a preacher, or inline scholarly apparatus. Attribute a
Father naturally when useful. Put exact loci, the relation to reviewed
interpretations, audience, spoken word count, and timing estimate in a brief
terminal note and `research/production-review.md`. A word-count estimate is not
a timed human delivery. Give exact sources the terminal `References` heading
so the used-reference check can read them, entirely outside the speech.
Rehearse the prose for sense and oral clarity; do not
claim an audible or human rehearsal that did not happen. End as preaching;
any recited prayer must reproduce an exact received human witness.

Declare `[document.homily]` in `publication.toml` -- its metadata fields, the
`homily` region holding the spoken component and the `apparatus` region holding
the terminal note, each placed by component key without repeating its path --
and run `tools/tpt document-types refresh --leaf
{provider}/{proper}`, which writes `homily.tex`; never write it by hand. The
type imports `common/preamble`, `common/propers-format` and
`common/propers-homily`, sets the full-width shared title, and encloses only
the `homily` region in `properhomily`: two Latin Modern columns at the shared
11-point baseline, with the terminal apparatus after the environment's closing
page break. Never put columns in the studies.
Do not add local font, geometry or title overrides. Keep
components local and record actual contributions; revision timestamps are
derived from Git. Add no new
source-dependent claims or repairs to the accepted study. Report upstream
defects for the independent homily reviewer to route to their true owner.
