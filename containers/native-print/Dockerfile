# SPDX-License-Identifier: MIT
# The baseline and archive date match .github/workflows/pages.yml. The final
# stage is the print-only service image. The `toolchain` stage alone is the
# compiler the Pages print-compile job builds (`--target toolchain`, passing
# both pins from pages.yml) to typeset every admitted edition before deploying;
# that job never runs the service stage or its source checkout.
ARG PRINT_BASE=ghcr.io/spincyc/triptych-texlive@sha256:45dbaaa9ba1eccff8621c8ed5ff614363384ccd5bc1b72d3b708f8eb2d2d057a
FROM ${PRINT_BASE} AS toolchain

ARG PRINT_BASE
ARG ARCH_SNAPSHOT=2026/09/04

# As in the existing manual print workflow, prepare XeTeX and Latin Babel
# support before compiling anything. No package installer runs at request time.
RUN printf '%s\n' "$PRINT_BASE" | grep -Eq '^ghcr\.io/[a-z0-9._/-]+@sha256:[0-9a-f]{64}$' \
 && printf '%s\n' "$ARCH_SNAPSHOT" | grep -Eq '^[0-9]{4}/[0-9]{2}/[0-9]{2}$' \
 && if ! pacman -Q texlive-langeuropean texlive-xetex > /dev/null 2>&1; then \
      printf 'Server=https://archive.archlinux.org/repos/%s/$repo/os/$arch\n' "$ARCH_SNAPSHOT" > /etc/pacman.d/mirrorlist \
      && pacman -Sy --noconfirm --needed archlinux-keyring \
      && pacman -Syu --noconfirm --needed texlive-langeuropean texlive-xetex; \
    fi \
 && { test -n "$(kpsewhich -engine=xetex xelatex.fmt)" || fmtutil-sys --byfmt xelatex; } \
 && fc-cache -f \
 && command -v pdflatex xelatex pdfinfo pdftotext pdffonts make git python \
 && python -c 'import yaml' \
 && test -n "$(kpsewhich latin.ldf)" \
 && test -n "$(kpsewhich hyph-la.tex)" \
 && for package in accsupp amsbsy amsmath amssymb array babel bookmark booktabs \
      endnotes enumitem environ etoolbox fancyhdr fontenc fontspec geometry \
      graphicx hyperref inputenc libertinus lmodern longtable microtype multicol \
      needspace parskip pdflscape ragged2e tabularx tcolorbox tikz tipa titlesec \
      xcolor xltabular xstring xurl zref-abspage zref-user; do \
      test -n "$(kpsewhich "$package.sty")" || exit 1; \
    done \
 && for family in 'Latin Modern Roman' 'Libertinus Serif' 'Libertinus Sans' \
      'Libertinus Mono' Junicode FreeSerif; do \
      test "$(fc-match --format '%{family[0]}' "$family")" = "$family" || exit 1; \
    done \
 && install -d /usr/share/triptych-print \
 && pacman -Q > /usr/share/triptych-print/packages.txt \
 && pdflatex --version > /usr/share/triptych-print/pdflatex.txt \
 && xelatex --version > /usr/share/triptych-print/xelatex.txt \
 && printf '%s\n' '\documentclass{article}' \
      '\usepackage[T1]{fontenc}\usepackage[utf8]{inputenc}' \
      '\usepackage{libertinus}\usepackage{tipa}' \
      '\begin{document}Agnus Dei, qui tollis peccata mundi.' \
      '\textbf{Bold}\textit{Italic}\textsc{Small Caps}\textsf{Sans}\texttt{Mono}' \
      '{\fontfamily{cmr}\selectfont\textipa{/aNUs dei/}}\end{document}' \
      > /tmp/triptych-fonts-pdftex.tex \
 && pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error \
      -output-directory=/tmp /tmp/triptych-fonts-pdftex.tex > /dev/null \
 && printf '%s\n' '\documentclass{article}\usepackage{fontspec}' \
      '\setmainfont[Ligatures=TeXOff]{Latin Modern Roman}' \
      '\newfontfamily\PapalUnicodeFont[Ligatures=TeXOff]{Junicode}' \
      '\newfontfamily\PapalCyrillicFont[Ligatures=TeXOff]{FreeSerif}' \
      '\usepackage[shorthands=off,latin]{babel}' \
      '\makeatletter\ifnum\l@latin=0\PackageError{probe}{Latin hyphenation absent}{}\fi\makeatother' \
      '\begin{document}Agnus Dei. {\PapalUnicodeFont Θεός ℣ ℟ ✠}' \
      '{\PapalCyrillicFont Бог}\end{document}' \
      > /tmp/triptych-fonts-xetex.tex \
 && xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error \
      -output-directory=/tmp /tmp/triptych-fonts-xetex.tex > /dev/null \
 && ! grep -E 'Missing character|LaTeX Font Warning' /tmp/triptych-fonts-*.log \
 && pdffonts /tmp/triptych-fonts-pdftex.pdf > /usr/share/triptych-print/pdftex-fonts.txt \
 && pdffonts /tmp/triptych-fonts-xetex.pdf > /usr/share/triptych-print/xetex-fonts.txt \
 && python -c 'from pathlib import Path; reports = Path("/usr/share/triptych-print").glob("*-fonts.txt"); assert all(row.split()[-5:-2] == ["yes", "yes", "yes"] for report in reports for row in report.read_text().splitlines()[2:])' \
 && rm /tmp/triptych-fonts-pdftex.* /tmp/triptych-fonts-xetex.* \
 && pacman -Scc --noconfirm

FROM toolchain

ARG PRINT_BASE
ARG ARCH_SNAPSHOT=2026/09/04
ARG SOURCE_REVISION

LABEL org.opencontainers.image.source="https://github.com/spincyc/triptych" \
      org.opencontainers.image.description="Single-edition native TeX PDF service for Triptych" \
      org.opencontainers.image.revision="${SOURCE_REVISION}" \
      triptych.print-base="${PRINT_BASE}" \
      triptych.arch-snapshot="${ARCH_SNAPSHOT}"

# Fetch one public, committed tree instead of sending a developer checkout,
# credentials, old Git history or .scratch through the Docker build context.
# The real shallow Git checkout lets the service verify its revision and dirt.
RUN printf '%s\n' "$SOURCE_REVISION" | grep -Eq '^[0-9a-f]{40}$' \
 && git init /app \
 && git -C /app remote add origin https://github.com/spincyc/triptych.git \
 && git -C /app fetch --depth=1 origin "$SOURCE_REVISION" \
 && git -C /app checkout --detach FETCH_HEAD \
 && test "$(git -C /app rev-parse HEAD)" = "$SOURCE_REVISION" \
 && test -z "$(git -C /app status --porcelain --untracked-files=no)" \
 && test -f /app/tools/native-print-service \
 && git config --system --add safe.directory /app \
 && install -d -o 10001 -g 10001 -m 0750 /app/.scratch /var/lib/triptych-print

ENV PYTHONDONTWRITEBYTECODE=1 \
    GIT_OPTIONAL_LOCKS=0 \
    TEXMFHOME=/var/lib/triptych-print/texmf \
    TEXMFVAR=/var/lib/triptych-print/texmf-var \
    TEXMFCONFIG=/var/lib/triptych-print/texmf-config \
    XDG_CACHE_HOME=/var/lib/triptych-print/font-cache

WORKDIR /app
USER 10001:10001
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=15s --start-period=120s --retries=3 \
  CMD ["python", "-c", "import json, urllib.request; r = urllib.request.urlopen('http://127.0.0.1:8080/v1/health', timeout=10); assert r.status == 200 and json.load(r)['status'] == 'ok'"]
ENTRYPOINT ["python", "/app/tools/native-print-service"]
CMD ["serve", "--host", "0.0.0.0", "--port", "8080", "--cache-root", "/var/lib/triptych-print", "--origin", "https://mystago.gy", "--workers", "1"]
