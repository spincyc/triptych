# Reproduction commands

Run from the repository root. `DOC` below is
`liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost`.

```sh
tools/web-edition --provider claude \
  --output .scratch/claude-tlm-web-review-final/fresh "$DOC"

sha256sum \
  .scratch/claude-tlm-web-review-final/fresh/claude/$DOC.md \
  build/web/claude/$DOC.md \
  web/claude/$DOC.md

cat src/claude/$DOC/research/web-artifact.json
diff -u .scratch/claude-tlm-web-review-final/fresh/claude/$DOC.md \
  web/claude/$DOC.md
rg -n '[ \t]+$' \
  .scratch/claude-tlm-web-review-final/fresh/claude/$DOC.md \
  web/claude/$DOC.md

tools/tpt check-web-edition --provider claude --document "$DOC"
tools/tpt check-proper-components --provider claude --document "$DOC" --phase scope
tools/tpt check-proper-components --provider claude --document "$DOC" --phase content
tools/tpt check-proper-components --provider claude --document "$DOC" \
  --phase artifacts --build-root build/claude

python3 -c 'import sys; from pathlib import Path; sys.path.insert(0,"scripts"); from _proper_components import include_graph; root=Path(".").resolve(); leaf=root/"src/claude/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost"; print("\n".join(p.relative_to(root).as_posix() for p in sorted(include_graph(leaf/"main.tex", leaf, root/"src/claude"))))'

tools/tpt check-content-preflight --root . --provider claude \
  --document "$DOC" --edition research
tools/tpt proper-chronology record --provider claude --document "$DOC" --check
tools/tpt proper-chronology annotations --provider claude --document "$DOC" --check
tools/tpt proper-chronology loci --provider claude --document "$DOC" --json

python3 -m unittest tools.tests.test_web_edition_conversion
python3 -m unittest tools.tests.test_proper_components_v2
python3 -m unittest tools.tests.test_propers_format
```

The corrected Markdown was rendered with the repository's own
`tools/public-alpha` `render_page` function into `site/`. Chromium captures used
`/usr/bin/chromium --headless=new --no-sandbox --disable-gpu` at 1440×1000 and
393×852. The exact scratch render is:

```text
site/web/claude/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost.html
```
