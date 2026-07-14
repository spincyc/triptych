# Triptych Authoring Skills

This repository plugin turns the collection's editorial and genre profiles into focused bundled skills. Each skill accepts labeled fields or ordinary prose. Everything supplied in the request and thread remains controlling context, guidance, emphasis, or limitation.

Explicitly mention a skill with `$triptych-authoring:<name>`. Enabled skills also appear in Codex's skill and slash-command pickers.

## Skills

| Skill | Outcome | What the user should supply |
| --- | --- | --- |
| [`$triptych-authoring:authoring-help`](skills/authoring-help/SKILL.md) | Choose the correct workflow without changing files | A goal, document idea, or target path |
| [`$triptych-authoring:article`](skills/article/SKILL.md) | Create or substantially revise a faith, theology, canon-law, or mixed article | Question or target; desired thesis or change; audience; relevant authorities, jurisdiction, and as-of date |
| [`$triptych-authoring:novena`](skills/novena/SKILL.md) | Create a full bilingual novena and its condensed daily prayer book | Devotion, mystery, saint, feast, or event; calendar placement; received prayers or traditions; desired emphases |
| [`$triptych-authoring:mariology`](skills/mariology/SKILL.md) | Create or revise a Rosary, Marian-dogma, devotional, or other Mariological reference | Subject and governing question; corpus; desired depth; authorities and boundaries |
| [`$triptych-authoring:apparition`](skills/apparition/SKILL.md) | Create or revise an authority-qualified apparition monograph or corpus | Event or corpus; place and dates; known recipients, messages, decrees, sources, and as-of date |
| [`$triptych-authoring:proper-1962`](skills/proper-1962/SKILL.md) | Create a 1962 temporal, ritual, votive, or other proper guide | Exact formulary and catalog identity; occurrence context; known Missal loci; sacramental or seasonal variables |
| [`$triptych-authoring:proper-postconciliar`](skills/proper-postconciliar/SKILL.md) | Create a postconciliar proper guide | Latin and vernacular editions; territory; Lectionary; calendar; cycle; celebration; selected options |
| [`$triptych-authoring:ordinary`](skills/ordinary/SKILL.md) | Create or revise an exposition of an Ordinary, Order of Mass, or defined unit | Exact edition or comparison; language and territory; textual boundary; analytical purpose |
| [`$triptych-authoring:assembly-1962`](skills/assembly-1962/SKILL.md) | Create or revise a 1962 Mass-assembly reference | Rubrical problem; calendar assumptions; Mass categories; desired worked cases and limits |
| [`$triptych-authoring:sacrament`](skills/sacrament/SKILL.md) | Revise the canonical sacramental treatise and every derived consumer | Sacrament or shared topic; requested correction or expansion; governing sources; affected summaries or tables |
| [`$triptych-authoring:revise`](skills/revise/SKILL.md) | Revise any existing collection document under its actual profile | Target title or path; requested changes; sources, emphasis, exclusions, currentness, and desired staging |
| [`$triptych-authoring:audit`](skills/audit/SKILL.md) | Report on, or explicitly remediate, an existing document | Target; audit dimensions; `report` or `fix`; as-of date and any special standard |
| [`$triptych-authoring:publish`](skills/publish/SKILL.md) | Build, inspect, install, catalog, and optionally commit completed work | Target documents; desired stage boundary; whether a commit is authorized; any release constraints |

Suggested fields are prompts, not syntax. For example:

```text
$triptych-authoring:novena Our Lady of Sorrows. Principal annual placement before 15 September;
include the Stabat Mater in Latin and a public-domain poetic English version;
avoid unverified promises; create and commit the condensed companion separately.
```

The shared skill contract is in [`references/conventions.md`](references/conventions.md). Every workflow begins by reading the repository instructions and the controlling profile, preserves unrelated changes, verifies mutable claims from official sources, updates required research records and generation metadata, and completes the applicable build and publication checks.

## Repository installation

The plugin is registered in `.agents/plugins/marketplace.json`. From the repository root, add the local marketplace once and install the plugin from its recorded marketplace name:

```sh
codex plugin marketplace add .
codex plugin add triptych-authoring@personal
```

Start a new Codex task after installation or after reinstalling an updated plugin so the bundled skills are loaded.
