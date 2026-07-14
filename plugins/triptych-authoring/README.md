# Triptych Authoring Commands

This repository plugin turns the collection's editorial and genre profiles into focused slash-command workflows. Each command accepts labeled fields or ordinary prose. Everything supplied with the invocation remains available as added context, guidance, emphasis, or limitation.

## Commands

| Command | Outcome | What the user should supply |
| --- | --- | --- |
| [`/authoring-help`](commands/authoring-help.md) | Choose the correct workflow without changing files | A goal, document idea, or target path |
| [`/article`](commands/article.md) | Create or substantially revise a faith, theology, canon-law, or mixed article | Question or target; desired thesis or change; audience; relevant authorities, jurisdiction, and as-of date |
| [`/novena`](commands/novena.md) | Create a full bilingual novena and its condensed daily prayer book | Devotion, mystery, saint, feast, or event; calendar placement; received prayers or traditions; desired emphases |
| [`/mariology`](commands/mariology.md) | Create or revise a Rosary, Marian-dogma, devotional, or other Mariological reference | Subject and governing question; corpus; desired depth; authorities and boundaries |
| [`/apparition`](commands/apparition.md) | Create or revise an authority-qualified apparition monograph or corpus | Event or corpus; place and dates; known recipients, messages, decrees, sources, and as-of date |
| [`/proper-1962`](commands/proper-1962.md) | Create a 1962 temporal, ritual, votive, or other proper guide | Exact formulary and catalog identity; occurrence context; known Missal loci; sacramental or seasonal variables |
| [`/proper-postconciliar`](commands/proper-postconciliar.md) | Create a postconciliar proper guide | Latin and vernacular editions; territory; Lectionary; calendar; cycle; celebration; selected options |
| [`/ordinary`](commands/ordinary.md) | Create or revise an exposition of an Ordinary, Order of Mass, or defined unit | Exact edition or comparison; language and territory; textual boundary; analytical purpose |
| [`/assembly-1962`](commands/assembly-1962.md) | Create or revise a 1962 Mass-assembly reference | Rubrical problem; calendar assumptions; Mass categories; desired worked cases and limits |
| [`/sacrament`](commands/sacrament.md) | Revise the canonical sacramental treatise and every derived consumer | Sacrament or shared topic; requested correction or expansion; governing sources; affected summaries or tables |
| [`/revise`](commands/revise.md) | Revise any existing collection document under its actual profile | Target title or path; requested changes; sources, emphasis, exclusions, currentness, and desired staging |
| [`/audit`](commands/audit.md) | Report on, or explicitly remediate, an existing document | Target; audit dimensions; `report` or `fix`; as-of date and any special standard |
| [`/publish`](commands/publish.md) | Build, inspect, install, catalog, and optionally commit completed work | Target documents; desired stage boundary; whether a commit is authorized; any release constraints |

Suggested fields are prompts, not syntax. For example:

```text
/novena Our Lady of Sorrows. Principal annual placement before 15 September;
include the Stabat Mater in Latin and a public-domain poetic English version;
avoid unverified promises; create and commit the condensed companion separately.
```

The shared command contract is in [`commands/_conventions.md`](commands/_conventions.md). Every workflow begins by reading the repository instructions and the controlling profile, preserves unrelated changes, verifies mutable claims from official sources, updates required research records and generation metadata, and completes the applicable build and publication checks.

## Repository installation

The plugin is registered in `.agents/plugins/marketplace.json`. From the repository root, add the local marketplace once and install the plugin from its recorded marketplace name:

```sh
codex plugin marketplace add .
codex plugin add triptych-authoring@personal
```

Start a new Codex task after installation or after reinstalling an updated plugin so the command catalog is refreshed.
