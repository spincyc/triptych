PDFLATEX ?= pdflatex
PYTHON ?= python3
PROVIDER ?= gpt
PDF_JOBS ?= 4
PDFLATEX_MAX_PASSES ?= 5
SHA256 ?= sha256sum
INSTALL ?= install

# Arch Linux dependency manifest (the only supported local host for now).
# Keep direct owner packages explicit even when pacman currently installs one
# through another package. This makes the project/tool boundary reviewable and
# prevents a future dependency-graph change from silently removing a tool.
#
#   make, /bin/sh, /usr/bin/env, find, sort, comm, cmp, id and core utilities
#   (cat, install, mkdir, mv, realpath, rm and sha256sum):
#     make bash findutils coreutils diffutils
#   Python >= 3.11, stdlib (including fcntl/tomllib/zoneinfo), IANA timezone data, and
#   the public renderer's version-locked third-party module:
#     python tzdata python-markdown (exact version in requirements-public-alpha.txt)
#   pdflatex, kpsewhich/kpathsea and every directly loaded class/package/font:
#     texlive-bin texlive-basic texlive-latex texlive-latexrecommended
#     texlive-latexextra texlive-pictures texlive-fontsrecommended
#     texlive-fontsextra
#     article, geometry, fontenc, inputenc, lmodern, microtype, array,
#     booktabs, longtable, tabularx, enumitem, needspace, multicol, xcolor,
#     hyperref, tcolorbox, tikz/PGF, pdflscape, ragged2e, titlesec, endnotes,
#     and Atkinson Hyperlegible (atkinson.sty)
#   PDF metadata/text/raster and bounded PNG/contact-sheet processing:
#     poppler (pdfinfo, pdftotext, pdftoppm) and imagemagick (magick 7)
#   LaTeX-to-Markdown conversion for the web editions built with the site
#   (the products refuse any version but src/common/web-edition-toolchain.toml's):
#     pandoc
#   repository/review/isolated-agent workflow:
#     git github-cli openai-codex ripgrep
# pacman supplies the native shared-library closure and TeX package
# transitives. poppler-data is optional for non-Latin CMaps and is not needed
# by the current embedded-font corpus. pacman and either root access or sudo
# are bootstrap requirements for the installer target, not project runtime
# dependencies. GitHub Actions and its hosted Python/pip environment are
# CI-only. npm, Ghostscript and qpdf are not used here.
#   PyYAML, and the reason it is declared rather than left to chance:
#     five targets read the calendars through it and SKIP rather than fail when
#     it is absent, so a host without it runs `make check` to a clean exit
#     having validated no calendar at all. A silent skip is the one failure this
#     list can prevent outright.
#   node, which the comment above this one denied for months while
#     `tools/calendar-rubrics` spawned it directly and told the operator to
#     install it: the rubric and catena checks run the browser's own derivation
#     under node against each source's solved cases, and both are documented as
#     failures rather than skips without it.
# A browser is NOT in that list and is declared separately below. It is wanted
# only to run the four `*_browser.mjs` harnesses, it costs an order of magnitude
# more to install than anything above, and a clone that only builds PDFs should
# not pay for it.
# pdfLaTeX remains necessary for the shared preamble's pdfTeX primitives;
# XeLaTeX, LuaLaTeX and Tectonic are not drop-in replacements. latexmk from
# texlive-binextra is a free, more robust pass controller, but is not currently
# used. Poppler plus ImageMagick 7 remains the smallest purpose-fit PDF review
# stack; MuPDF or GraphicsMagick would not eliminate an existing dependency.
ARCH_CORE_PACKAGES := make bash findutils coreutils diffutils
ARCH_PYTHON_PACKAGES := python tzdata python-markdown python-yaml
ARCH_TEX_PACKAGES := texlive-bin texlive-basic texlive-latex \
	texlive-latexrecommended texlive-latexextra texlive-pictures \
	texlive-fontsrecommended texlive-fontsextra texlive-langeuropean gnu-free-fonts
ARCH_PDF_PACKAGES := poppler imagemagick
ARCH_WEB_PACKAGES := pandoc
# The browser's own derivation, replayed under node against each source's
# solved cases by `calendar-rubrics check` and `catena check`.
ARCH_DERIVATION_PACKAGES := nodejs
ARCH_WORKFLOW_PACKAGES := git github-cli openai-codex ripgrep
ARCH_DEPENDENCY_PACKAGES := $(ARCH_CORE_PACKAGES) $(ARCH_PYTHON_PACKAGES) \
	$(ARCH_TEX_PACKAGES) $(ARCH_PDF_PACKAGES) $(ARCH_WEB_PACKAGES) \
	$(ARCH_DERIVATION_PACKAGES) $(ARCH_WORKFLOW_PACKAGES)
# Chromium and not google-chrome-stable: the latter is in no official
# repository, and this installer never fetches a standalone binary. The
# harnesses launch `--headless=new --disable-gpu`, so no display is involved
# and a headless host is not a limitation. Point TRIPTYCH_CHROME at the binary.
ARCH_BROWSER_PACKAGES := chromium
# The terminal reader, `tools/lectern`, and only it. Like the browser it is not in
# the list above: a clone that builds PDFs or runs the checks does not need it,
# and its tests say by name that they did not run where it is absent. The pin
# in requirements-tui.txt is the version this package ships. Its web editions
# are set by the site's own renderer, which holds the Markdown pin in
# requirements-public-alpha.txt and refuses any other version.
ARCH_TUI_PACKAGES := python-textual
ARCH_CANONICAL_COMMANDS := make:/usr/bin/make sh:/usr/bin/sh \
	env:/usr/bin/env id:/usr/bin/id find:/usr/bin/find sort:/usr/bin/sort \
	comm:/usr/bin/comm cmp:/usr/bin/cmp \
	cat:/usr/bin/cat chmod:/usr/bin/chmod cp:/usr/bin/cp install:/usr/bin/install \
	mkdir:/usr/bin/mkdir mv:/usr/bin/mv realpath:/usr/bin/realpath rm:/usr/bin/rm \
	sha256sum:/usr/bin/sha256sum python3:/usr/bin/python3 \
	pdflatex:/usr/bin/pdflatex kpsewhich:/usr/bin/kpsewhich \
	pdfinfo:/usr/bin/pdfinfo pdftotext:/usr/bin/pdftotext \
	pdftoppm:/usr/bin/pdftoppm magick:/usr/bin/magick pandoc:/usr/bin/pandoc \
	git:/usr/bin/git \
	gh:/usr/bin/gh codex:/usr/bin/codex rg:/usr/bin/rg
ARCH_PACMAN ?= /usr/bin/pacman
ARCH_SUDO ?= /usr/bin/sudo
ARCH_ID ?= /usr/bin/id
ARCH_PYTHON ?= /usr/bin/python3
ARCH_OS_RELEASE ?= /etc/os-release

SOURCE_ROOT := src/$(PROVIDER)
BUILD_ROOT := build/$(PROVIDER)
WEB_BUILD_ROOT := build/web/$(PROVIDER)
# src/common holds shared sources and document-type templates, never a provider:
# a template named main.tex is not a publication entrypoint.
ALL_MAIN_SOURCES := $(shell find src -mindepth 2 -path 'src/common/*' -prune -o -type f -name main.tex -print 2>/dev/null | sort)
PROVIDERS := $(sort $(foreach path,$(ALL_MAIN_SOURCES),$(word 2,$(subst /, ,$(path)))))

MAIN_SOURCES := $(shell find $(SOURCE_ROOT) -type f -name main.tex 2>/dev/null | sort)
CANONICAL_DOCUMENTS := $(patsubst $(SOURCE_ROOT)/%/main.tex,%,$(MAIN_SOURCES))
PROPER_SYNTHESIS_DOCUMENTS := $(shell \
	$(PYTHON) tools/tpt check-proper-components --provider $(PROVIDER) \
		--phase scope --list-synthesis 2>/dev/null)
PROPER_HOMILY_DOCUMENTS := $(shell \
	$(PYTHON) tools/tpt check-proper-components --provider $(PROVIDER) \
		--phase scope --list-homily 2>/dev/null)
PROPER_DERIVED_DOCUMENTS := $(PROPER_SYNTHESIS_DOCUMENTS) $(PROPER_HOMILY_DOCUMENTS)
DOCUMENTS := $(CANONICAL_DOCUMENTS) $(PROPER_DERIVED_DOCUMENTS)
SOURCE_METADATA_CHECKS := $(addprefix $(BUILD_ROOT)/.metadata/,$(addsuffix .source-check,$(sort $(DOCUMENTS) $(DOC))))
BUILD_PDFS := $(addprefix $(BUILD_ROOT)/,$(addsuffix .pdf,$(DOCUMENTS)))
BUILD_METADATA_STAMPS := $(addprefix $(BUILD_ROOT)/.metadata/,$(addsuffix .ok,$(DOCUMENTS)))
BUILD_METADATA_VERIFICATIONS := $(addprefix $(BUILD_ROOT)/.metadata/,$(addsuffix .verify,$(DOCUMENTS)))
METADATA_CHECKER := tools/tpt check-generation-metadata
# Every contents line and bookmark must own its heading's anchor; see the tool.
PDF_ANCHOR_CHECKER := tools/tpt check-pdf-anchors
# A launcher invocation is two words. Make would read it as two prerequisites
# and sha256sum would look for a file whose name contains a space, so
# prerequisite and hash sites must name the implementation file instead.
METADATA_CHECKER_IMPL := tools/check-generation-metadata
CURRICULUM_STRUCTURE_CHECKER_IMPL := tools/check-curriculum-structure
PROPER_COMPONENT_CHECKER := tools/tpt check-proper-components
WEB_EDITION_CHECKER := tools/tpt check-web-edition
WEB_EDITION_TOOL := tools/tpt web-edition
CURRICULUM_STRUCTURE_CHECKER := tools/tpt check-curriculum-structure
PDF_REVIEW_TOOL := tools/tpt pdf-review
DOCUMENT_LIBRARY_TOOL := tools/tpt document-library
SOURCE_READER_TOOL := tools/tpt source-reader
PUBLIC_ALPHA_TOOL := tools/tpt public-alpha
RELEASE_BINDINGS_TOOL := tools/tpt release-bindings
RESEARCH_STALENESS_TOOL := tools/tpt research-staleness
SOURCE_LIBRARY_TOOL := tools/tpt source-library
SOURCE_INVENTORY_TOOL := tools/tpt source-inventory
SOURCE_FAMILY_MIGRATION_TOOL := tools/tpt source-family-migration
DOCUMENT_SCHEMA_TOOL := tools/tpt document-schema
ARTIFACT_STORE_TOOL := tools/tpt artifact-store
SNAPSHOT_STORE_TOOL := tools/tpt snapshot-store
BROWSER_PRODUCTS_TOOL := tools/tpt browser-products
PRINT_DOCUMENT_TOOL := tools/tpt print-document
PRINT_EDITION ?= main
PRINT_OUT ?= .scratch/print-document
# Complete-text bible editions. These are build artifacts, not publications:
# they are generated from the tracked verse text of the source library.
BIBLE_TYPESET_TOOL := tools/tpt typeset-bible
BIBLE_TYPESET_IMPL := tools/typeset-bible
BIBLE_BUILD_ROOT := build/bibles
# Tracks of a tracked abridged plan: one tier of the plan in one edition, set
# from the same verse text and the same typesetter as a whole bible, into
# build/ like every other local print output.
READING_PLAN_TOOL := tools/tpt reading-plan
READING_BUILD_ROOT := build/reading-plans
# The one tracked plan. `typeset-bible list --plan $(PLAN) --format ids` names
# its volumes; nothing here restates how many there are or what they cover.
PLAN ?= narrative-spine

COMMON_SOURCES := $(shell find src/common -type f 2>/dev/null | sort)
ECCLESIASTICAL_LATIN_ROOT := $(SOURCE_ROOT)/curriculums/ecclesiastical-latin
ECCLESIASTICAL_LATIN_SHARED := $(shell find $(ECCLESIASTICAL_LATIN_ROOT)/shared -type f \( \
	-name '*.tex' -o -name '*.sty' -o -name '*.cls' -o -name '*.bib' -o \
	-name '*.bst' -o -name '*.png' -o -name '*.jpg' -o -name '*.jpeg' -o \
	-name '*.pdf' -o -name '*.eps' \) 2>/dev/null | sort)
ECCLESIASTICAL_LATIN_BUILD_PDFS := $(filter \
	$(BUILD_ROOT)/curriculums/ecclesiastical-latin/%,$(BUILD_PDFS))
ECCLESIASTICAL_LATIN_DOCUMENTS := $(filter \
	curriculums/ecclesiastical-latin/%,$(DOCUMENTS))
ECCLESIASTICAL_LATIN_METADATA_VERIFICATIONS := $(addprefix \
	$(BUILD_ROOT)/.metadata/,$(addsuffix .verify,$(ECCLESIASTICAL_LATIN_DOCUMENTS)))
ALTAR_SERVER_GUIDES_ROOT := $(SOURCE_ROOT)/liturgy/roman-rite/1962/reference/altar-server-guides
ALTAR_SERVER_GUIDES_SHARED := $(shell find $(ALTAR_SERVER_GUIDES_ROOT)/shared -type f \( \
	-name '*.tex' -o -name '*.sty' -o -name '*.cls' -o -name '*.bib' -o \
	-name '*.bst' -o -name '*.png' -o -name '*.jpg' -o -name '*.jpeg' -o \
	-name '*.pdf' -o -name '*.eps' \) 2>/dev/null | sort)
ALTAR_SERVER_GUIDES_BUILD_PDFS := $(filter \
	$(BUILD_ROOT)/liturgy/roman-rite/1962/reference/altar-server-guides/%,$(BUILD_PDFS))
ALTAR_SERVER_GUIDES_DOCUMENTS := $(filter \
	liturgy/roman-rite/1962/reference/altar-server-guides/%,$(DOCUMENTS))
ALTAR_SERVER_GUIDES_METADATA_VERIFICATIONS := $(addprefix \
	$(BUILD_ROOT)/.metadata/,$(addsuffix .verify,$(ALTAR_SERVER_GUIDES_DOCUMENTS)))
ROMAN_SANCTUARY_DICTIONARY_ROOT := $(SOURCE_ROOT)/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary
ALTAR_SERVER_GUIDES_SHARED += $(addprefix $(ROMAN_SANCTUARY_DICTIONARY_ROOT)/shared/artwork/pencil/,\
  books/RPD-FIG-books-0001-in-use-missal-on-stand-v3-alpha.png \
  RPD-FIG-service-objects-0103-paired-cruets-v2-alpha.png \
  RPD-FIG-service-objects-0106-lavabo-basin-manuterge-v2-alpha.png \
  RPD-FIG-sacred-vessels-0007-iso-communion-plate.png \
  compositions/RPD-FIG-prepared-chalice-0001-formation-alpha.png)
ROMAN_SANCTUARY_DICTIONARY_SHARED := $(shell find $(ROMAN_SANCTUARY_DICTIONARY_ROOT)/shared -type f \( \
	-name '*.tex' -o -name '*.sty' -o -name '*.cls' -o -name '*.bib' -o \
	-name '*.bst' -o -name '*.toml' -o -name '*.png' -o -name '*.jpg' -o \
	-name '*.jpeg' -o -name '*.pdf' -o -name '*.eps' \) 2>/dev/null | sort)
ROMAN_SANCTUARY_DICTIONARY_BUILD_PDFS := $(filter \
	$(BUILD_ROOT)/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/%,$(BUILD_PDFS))
ROMAN_SANCTUARY_DICTIONARY_GENERATED := \
	$(BUILD_ROOT)/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/shared/generated
ROMAN_SANCTUARY_DICTIONARY_GENERATOR := tools/tpt render-sanctuary-dictionary
# 1962 proper full-text editions: each imports its study edition's sections and
# format from the sibling leaf at the same id without the -full-text suffix.
ROMAN_1962_FULL_TEXT_DOCUMENTS := $(filter \
	liturgy/roman-rite/1962/propers/%-full-text,$(DOCUMENTS))
SACRAMENT_ROOT := $(SOURCE_ROOT)/theology/sacraments
SACRAMENT_SHARED := \
	$(SACRAMENT_ROOT)/summary-preamble.tex \
	$(wildcard $(SACRAMENT_ROOT)/fragments/*.tex) \
	$(wildcard $(SACRAMENT_ROOT)/summaries/*.tex)
SACRAMENT_INITIATION_TABLE := $(SACRAMENT_ROOT)/sections/14-churches-initiation.tex
NOVENA_ROOT := $(SOURCE_ROOT)/devotions/novenas
NOVENA_SHARED := $(wildcard $(NOVENA_ROOT)/shared/*.tex)
NOVENA_BUILD_PDFS := $(filter $(BUILD_ROOT)/devotions/novenas/%,$(BUILD_PDFS))
POSTCONCILIAR_US_ROOT := $(SOURCE_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers
POSTCONCILIAR_US_FORMAT := $(POSTCONCILIAR_US_ROOT)/shared/exposition-format.tex
POSTCONCILIAR_US_REGISTRY := $(wildcard $(POSTCONCILIAR_US_ROOT)/registry/*.md)
POSTCONCILIAR_US_BUILD_PDFS := $(filter $(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/%,$(BUILD_PDFS))
BIOGRAPHY_ROOT := $(SOURCE_ROOT)/biographies
BIOGRAPHY_SHARED := $(wildcard $(BIOGRAPHY_ROOT)/shared/*.tex)
BIOGRAPHY_BUILD_PDFS := $(filter $(BUILD_ROOT)/biographies/%,$(BUILD_PDFS))
HISTORICAL_TRANSLATION_ROOT := $(SOURCE_ROOT)/history/biblical-translations
HISTORICAL_TRANSLATION_SHARED := $(HISTORICAL_TRANSLATION_ROOT)/account-format.tex
HISTORICAL_TRANSLATION_BUILD_PDFS := $(filter $(BUILD_ROOT)/history/biblical-translations/%,$(BUILD_PDFS))
PARISH_HISTORY_ROOT := $(SOURCE_ROOT)/history/catholic-parish-histories
PARISH_HISTORY_SHARED := $(PARISH_HISTORY_ROOT)/parish-history-format.tex
PARISH_HISTORY_BUILD_PDFS := $(filter $(BUILD_ROOT)/history/catholic-parish-histories/%,$(BUILD_PDFS))
TRADITIONAL_INSTITUTE_ROOT := $(SOURCE_ROOT)/history/traditional-priestly-institutes
TRADITIONAL_INSTITUTE_SHARED := $(TRADITIONAL_INSTITUTE_ROOT)/institution-format.tex
TRADITIONAL_INSTITUTE_BUILD_PDFS := $(filter $(BUILD_ROOT)/history/traditional-priestly-institutes/%,$(BUILD_PDFS))
FIRST_NOVENA_ROOT := $(NOVENA_ROOT)/00-ascension-to-pentecost
CARMEL_NOVENA_ROOT := $(NOVENA_ROOT)/10-our-lady-of-mount-carmel
FIRST_NOVENA_PRAYERS := $(wildcard $(FIRST_NOVENA_ROOT)/prayers/*.tex)
CARMEL_NOVENA_PRAYERS := $(wildcard $(CARMEL_NOVENA_ROOT)/prayers/*.tex)
MARIOLOGY_PRAYER_FORMAT := $(SOURCE_ROOT)/theology/mariology/shared/prayer-reference-format.tex
ANGELUS_HAIL_MARY := $(CARMEL_NOVENA_ROOT)/prayers/hail-mary.tex

.DEFAULT_GOAL := all

# A top-level invocation without -j has no jobserver for document builds to
# share. Bootstrap aggregate builds with a bounded recursive Make in that case.
# If a caller already supplied -j (including an inherited jobserver), keep the
# complete graph in this Make process so combined goals cannot race one another.
override _TRIPTYCH_MAKE_PARALLEL_FLAGS := $(filter -j% j% --jobs% --jobserver-auth=% --jobserver-fds=%,$(MAKEFLAGS))
override _triptych_make_strip_decimal = $(subst 9,,$(subst 8,,$(subst 7,,$(subst 6,,$(subst 5,,$(subst 4,,$(subst 3,,$(subst 2,,$(subst 1,,$(subst 0,,$(1)))))))))))
override _TRIPTYCH_PDF_JOBS_INVALID = $(strip \
	$(call _triptych_make_strip_decimal,$(PDF_JOBS)) \
	$(if $(strip $(PDF_JOBS)),,empty) \
	$(if $(subst 0,,$(strip $(PDF_JOBS))),,zero))
override _TRIPTYCH_BOUNDED_PDF_JOB_OPTION = $(if $(strip $(_TRIPTYCH_MAKE_PARALLEL_FLAGS)),,\
	$(if $(_TRIPTYCH_PDF_JOBS_INVALID),$(error PDF_JOBS requires a positive integer),--jobs=$(PDF_JOBS)))

.PHONY: all pdf _pdf review-pdfs review-all-pdfs list help clean \
	distclean check-tools check-tool-registry check-calendar-days \
	check-calendar-masses check-act-history \
	check-propers-census check-propers-structure \
	check-metadata check-web-editions \
	check-proper-components \
	web-editions web-figures check-web-edition-conversions \
	check-sources check-research-sources check-deployment-sources check-source-library \
	check-document-schemas check-document-content check-artifact-delivery \
	check-snapshot-delivery check-papal-inputs \
	prepare-browser-data check-browser-products deployment-source-gates \
	check-source-evidence print-document \
	check-source-inventory check-source-inventory-tool \
	check-source-family-migration check-source-family-migration-tool \
	check-source-family-screening check-source-containment \
	check-commentator-inventories check-commentary-corpus \
	check-source-graph check-publication-inventories check-proper-chronology-current \
	check-generated-documents-current \
	check-artwork-manifests \
	check-catena check-catena-structure check-catena-paragraphs \
	check-expensive \
	check-promised-deliverables \
	check-public-alpha prepare-public-alpha \
	check-pdf-review check-curriculum-rights check-curriculum-source-rights check-curriculum-sources \
	check-curriculum-structure check-source-reader source-projection \
	check-document-catalogue document-catalogue encyclicals-catalogue \
	public-site public-preview \
	dependencies-arch dependencies-arch-browser dependencies-arch-tui install-dependencies-arch \
	verify-public-site verify-public-preview \
	check-mass-ordinary check-scripture-chronology \
	check-release-bindings refresh-release-bindings approve-release \
	add-publication doc review-doc check check-typeset _typeset-tree \
	check-all check-tests \
	check-browser-static check-browser-gate check-browser-harnesses \
	check-native-print-compile \
	check-examples recapture-examples \
	altar-server-guides review-altar-server-guides \
	check-staleness measure-staleness explain-staleness rebaseline-doc \
	bibles bible review-bible check-bibles \
	tracks track review-track check-plan-sources reading-structure \
	FORCE_METADATA_VERIFICATION FORCE_BIBLE_RENDER $(SOURCE_METADATA_CHECKS)
.DELETE_ON_ERROR:
.SECONDARY: $(BUILD_METADATA_STAMPS)

all: public-site

# `review-pdfs` rasters only the built PDFs whose bytes differ from the ones
# its previous successful run rastered. It used to compare against copies
# installed under pdf/, a tree nothing fills any more; a hash ledger beside the
# build stamps answers the same question without keeping a second copy of any
# PDF. The ledger is replaced only after pdf-review succeeds, so a failed or
# interrupted review selects the same PDFs again. It records what was rastered,
# not what a reviewer approved.
REVIEW_PDFS_LEDGER := $(BUILD_ROOT)/.metadata/review-pdfs.sha256

define _review_changed_pdfs
@set -eu; \
	ledger='$(REVIEW_PDFS_LEDGER)'; \
	mkdir -p "$${ledger%/*}"; \
	current="$$ledger.current.$$$$"; \
	trap 'rm -f -- "$$current"' 0 1 2 15; \
	$(if $(strip $(BUILD_PDFS)),$(SHA256) -- $(BUILD_PDFS),:) > "$$current"; \
	if [ -f "$$ledger" ]; then \
		changed=$$(grep -vxF -f "$$ledger" -- "$$current" | sed 's/^[0-9a-f]*  //' || :); \
	else \
		changed=$$(sed 's/^[0-9a-f]*  //' "$$current"); \
	fi; \
	if [ -z "$$changed" ]; then \
		echo 'review-pdfs: every built PDF is byte-identical to the ones last rastered'; \
	else \
		$(PYTHON) $(PDF_REVIEW_TOOL) $$changed; \
	fi; \
	mv -f -- "$$current" "$$ledger"; \
	trap - 0 1 2 15
endef

ifeq ($(strip $(_TRIPTYCH_MAKE_PARALLEL_FLAGS)),)
pdf:
	+@$(MAKE) --no-print-directory $(_TRIPTYCH_BOUNDED_PDF_JOB_OPTION) _pdf

review-pdfs:
	+@$(MAKE) --no-print-directory $(_TRIPTYCH_BOUNDED_PDF_JOB_OPTION) pdf
	$(_review_changed_pdfs)

review-all-pdfs:
	+@$(MAKE) --no-print-directory $(_TRIPTYCH_BOUNDED_PDF_JOB_OPTION) pdf
	@$(PYTHON) $(PDF_REVIEW_TOOL) $(BUILD_PDFS)
else
pdf: _pdf

review-pdfs: pdf
	$(_review_changed_pdfs)

review-all-pdfs: pdf
	@$(PYTHON) $(PDF_REVIEW_TOOL) $(BUILD_PDFS)
endif

_pdf: check-metadata $(BUILD_METADATA_VERIFICATIONS)

list:
	@printf '%s\n' $(DOCUMENTS)

dependencies-arch:
	@printf '%s\n' $(ARCH_DEPENDENCY_PACKAGES)

# What `install-dependencies-arch` deliberately does not install. Named by its
# own target so that "which browser, and why is it not in the list" has one
# answer a reader can run, rather than a comment they have to find.
dependencies-arch-browser:
	@printf '%s\n' $(ARCH_BROWSER_PACKAGES)

dependencies-arch-tui:
	@printf '%s\n' $(ARCH_TUI_PACKAGES)

# Arch does not support partial upgrades: synchronize and upgrade the system in
# the same transaction that installs the canonical repository packages. This
# target never downloads standalone GitHub release binaries or writes ~/.local.
install-dependencies-arch:
	@set -eu; \
	if [ ! -r '$(ARCH_OS_RELEASE)' ]; then \
		printf '%s\n' 'Cannot verify Arch Linux: unreadable $(ARCH_OS_RELEASE)' >&2; \
		exit 2; \
	fi; \
	. '$(ARCH_OS_RELEASE)'; \
	if [ "$${ID:-}" != arch ]; then \
		printf '%s\n' "Unsupported host OS: $${ID:-unknown} (Arch Linux required)" >&2; \
		exit 2; \
	fi; \
	if [ ! -x '$(ARCH_PACMAN)' ]; then \
		printf '%s\n' 'Missing canonical pacman executable: $(ARCH_PACMAN)' >&2; \
		exit 2; \
	fi; \
	if [ ! -x '$(ARCH_ID)' ]; then \
		printf '%s\n' 'Missing canonical id executable: $(ARCH_ID)' >&2; \
		exit 2; \
	fi; \
	if [ "$$('$(ARCH_ID)' -u)" -eq 0 ]; then \
		'$(ARCH_PACMAN)' -Syu --needed $(ARCH_DEPENDENCY_PACKAGES); \
	else \
		if [ ! -x '$(ARCH_SUDO)' ]; then \
			printf '%s\n' 'Run as root or install/configure sudo at $(ARCH_SUDO)' >&2; \
			exit 2; \
		fi; \
		'$(ARCH_SUDO)' -- '$(ARCH_PACMAN)' -Syu --needed $(ARCH_DEPENDENCY_PACKAGES); \
	fi; \
	if [ ! -x '$(ARCH_PYTHON)' ]; then \
		printf '%s\n' 'Missing canonical Python executable after installation: $(ARCH_PYTHON)' >&2; \
		exit 2; \
	fi; \
	'$(ARCH_PYTHON)' -c 'import importlib.metadata as metadata, pathlib; lines = pathlib.Path("requirements-public-alpha.txt").read_text(encoding="utf-8").splitlines(); matches = [line.removeprefix("Markdown==") for line in lines if line.startswith("Markdown==")]; actual = metadata.version("Markdown"); expected = matches[0] if len(matches) == 1 else "invalid lock"; raise SystemExit(0 if actual == expected else f"Installed Markdown {actual} does not match requirements-public-alpha.txt ({expected})")'; \
	for specification in $(ARCH_CANONICAL_COMMANDS); do \
		name=$${specification%%:*}; \
		canonical=$${specification#*:}; \
		effective=$$(command -v "$$name" 2>/dev/null || :); \
		if [ -n "$$effective" ] && [ "$$effective" != "$$canonical" ]; then \
			printf '%s\n' "Warning: $$effective shadows canonical $$canonical" >&2; \
		fi; \
	done

check-pdf-review:
	@$(PYTHON) -m unittest discover -s tools/tests -p 'test_pdf_review.py' -v

# `-v`, for the same reason `check-pdf-review` passes it: this suite skips its
# built-PDF assertions on a checkout that has not been built, and the skip
# carries a reason naming what did not run and how to run it. Without `-v` an
# unbuilt run prints `s` and `OK (skipped=1)` and the reason never reaches the
# operator, which is the whole point of making the skip visible.
check-curriculum-rights:
	@$(PYTHON) -m unittest tools.tests.test_curriculum_liturgical_rights -v

# Keep publication independent of locally built PDFs and Poppler even on a
# workstation that happens to have the optional print corpus built.
check-curriculum-source-rights:
	@$(PYTHON) -m unittest -v \
		tools.tests.test_curriculum_liturgical_rights.CurriculumLiturgicalRightsTests.test_hash_only_registry_is_complete_and_well_formed \
		tools.tests.test_curriculum_liturgical_rights.CurriculumLiturgicalRightsTests.test_allowlist_exactly_matches_tracked_curriculum_sources \
		tools.tests.test_curriculum_liturgical_rights.CurriculumLiturgicalRightsTests.test_unavailable_dispositions_cover_affected_stable_ids \
		tools.tests.test_curriculum_liturgical_rights.CurriculumLiturgicalRightsTests.test_scanner_is_location_and_surface_sensitive \
		tools.tests.test_curriculum_liturgical_rights.CurriculumLiturgicalRightsTests.test_tex_control_words_cannot_hide_a_window

# Full derivation belongs to the explicit research lane. Publication authenticates
# the same projection's inputs and outputs through the browser-product descriptor.
check-act-history: | prepare-browser-data
	@$(PYTHON) tools/tpt act-history structure --check

# The committed descriptor binds exact canonical inputs and output membership.
# Warm builds verify cached bytes; misses derive only missing families offline.
prepare-browser-data:
	@$(PYTHON) $(BROWSER_PRODUCTS_TOOL) build

# A strictly read-only diagnostic; publication preparation already performs this
# verification, so it does not run a duplicate full cache check here.
check-browser-products:
	@$(PYTHON) $(BROWSER_PRODUCTS_TOOL) check

# Default validation checks logical identities, rights, bindings and the exact
# external-delivery metadata without hydrating optional evidence bytes.
check-source-graph:
	@$(PYTHON) $(SOURCE_LIBRARY_TOOL) validate

check-source-evidence:
	@$(PYTHON) $(SOURCE_LIBRARY_TOOL) validate --full-evidence

check-document-schemas: | prepare-browser-data
	@$(PYTHON) $(DOCUMENT_SCHEMA_TOOL) check --include-sources
	@test -z "$$(git ls-files -- ':(icase)*.pdf')" || { printf '%s\n' 'Generated PDFs must remain untracked; keep their canonical sources and shared styles in Git.' >&2; exit 1; }
	@test -z "$$(git ls-files -- ':(icase)*.zip' ':(icase)*.zip.part-*')" || { printf '%s\n' 'Tracked binary archives must be preserved outside Git and replaced by exact manifests.' >&2; exit 1; }
	@test -z "$$(git ls-files -- src/web/data)" || { printf '%s\n' 'Generated browser products must live in the validated content cache, not Git.' >&2; exit 1; }
	@test -z "$$(git ls-files -- release/papal-documents/inputs)" || { printf '%s\n' 'Historical papal input snapshots must be preserved outside Git and replaced by exact delivery and extraction records.' >&2; exit 1; }
	@test -z "$$(git ls-files -- build/browser-data)" || { printf '%s\n' 'Browser product caches must remain untracked under build/.' >&2; exit 1; }

# This deeper phase reports inherited content/profile gaps separately from a
# successful source publication. A source/schema pass never certifies them.
check-document-content:
	@$(PYTHON) $(DOCUMENT_SCHEMA_TOOL) check --phase content --run-gates

check-artifact-delivery:
	@$(PYTHON) $(ARTIFACT_STORE_TOOL) check

# Frozen original snapshots stay outside the ordinary checkout. These gates
# validate their exact delivery declarations and extracted release records;
# neither opens the archives nor fetches original bytes.
check-snapshot-delivery:
	@$(PYTHON) $(SNAPSHOT_STORE_TOOL) check

check-papal-inputs:
	@$(PYTHON) scripts/_papal_input_receipt.py check

check-publication-inventories: check-source-graph
	@set -eu; for inventory in src/sources/inventories/*publications-v1.toml; do \
		[ -e "$$inventory" ] || continue; \
		case "$$inventory" in \
			*/claude-publications-v1.toml) \
				review=src/sources/inventories/claude-classification-review-v1.toml ;; \
			*) review=src/sources/inventories/classification-review-v1.toml ;; \
		esac; \
		$(PYTHON) $(SOURCE_INVENTORY_TOOL) check --review "$$review" "$$inventory"; \
	done

# The two-build product descriptor covers the complete input, policy and output
# closure. Publication verifies it once before consumers.
DEPLOYMENT_SOURCE_MEMBERS := check-curriculum-source-rights check-document-schemas \
	check-artifact-delivery check-snapshot-delivery check-papal-inputs \
	check-document-catalogue check-source-graph check-proper-chronology-current \
	check-generated-documents-current

# Bootstrap bounded concurrency when the caller supplied no jobserver. Keep
# ordinary liturgical derivation and rights checks in the source publication
# gate; neither this target nor its prerequisites installs or fetches PDFs.
ifeq ($(strip $(_TRIPTYCH_MAKE_PARALLEL_FLAGS)),)
check-deployment-sources:
	+@$(MAKE) --no-print-directory $(_TRIPTYCH_BOUNDED_PDF_JOB_OPTION) deployment-source-gates
else
check-deployment-sources: deployment-source-gates
endif

deployment-source-gates: $(DEPLOYMENT_SOURCE_MEMBERS) | prepare-browser-data
	@$(PYTHON) tools/tpt calendar-days check
	@$(PYTHON) tools/tpt check-calendar-masses
	@$(PYTHON) tools/tpt mass-propers structure --check
	@$(PYTHON) tools/tpt calendar-rubrics check
	@$(PYTHON) tools/tpt mass-ordinary check

# Research replay is explicit and may require already hydrated evidence. It
# never downloads it automatically. The publication gate above remains useful
# in a source-only checkout while this lane verifies the complete research set.
check-research-sources: check-deployment-sources check-source-evidence \
		check-publication-inventories check-source-reader check-act-history \
		check-source-containment check-commentator-inventories check-commentary-corpus
	@$(PYTHON) $(SOURCE_FAMILY_MIGRATION_TOOL) check

# Ordinary source maintenance validates the metadata graph, inventory and
# reviewed ledgers without requiring optional acquired binary evidence.
check-sources: check-source-graph check-publication-inventories \
		check-source-containment check-commentator-inventories check-commentary-corpus \
		check-proper-chronology-current check-generated-documents-current
	@$(PYTHON) $(SOURCE_FAMILY_MIGRATION_TOOL) check

# Adopted proper chronology remains current with the canonical corpus, including
# older dossiers. This source-only gate neither migrates legacy prose nor prints.
check-proper-chronology-current:
	@$(PYTHON) -m unittest tools.tests.test_generated_proper_chronology_freshness -v

# Every leaf that opts into a document type (src/common/document-types/) must
# assemble current entrypoints and deterministic pages without authored copies.
# Saved generated snapshots need not be refreshed. One check for every projection.
check-generated-documents-current:
	@$(PYTHON) -m unittest tools.tests.test_generated_documents_freshness -v

# A work held only inside another record -- a Migne volume, an NPNF anthology,
# a whole-volume optical layer filed under one of its constituents -- is
# invisible to a sweep that asks each commentary lead by its own record, and
# was reported absent that way three review rounds running. The containment
# inventory is what `commentary-work-index discover` reads to report it held.
# This refuses a container-shaped record nobody has entered, an entry naming a
# record the library does not have, a malformed extent, and an entry whose
# container record changed since it was reviewed, so a new container cannot be
# registered silently. `guidance/catena.md` section 11 owns the rule.
check-source-containment:
	@$(PYTHON) tools/tpt commentary-work-index containment

# Who each author is -- Father, Doctor, saint, Blessed, or an ecclesiastical
# writer -- and which liturgical commentaries expound a Mass, recorded by the
# elements each commentator names rather than by his Sunday number, which drifts.
# This refuses a standing without a cited basis and a locus whose heading is not
# in the lines it names; `guidance/catena.md` section 12 owns both files.
check-commentator-inventories:
	@$(PYTHON) tools/tpt commentary-work-index standing
	@$(PYTHON) tools/tpt commentary-work-index formulary

# Re-derive the research worklist without repairing it: a stale snapshot once
# omitted daily Masses and hid the passages that had never been harvested.
check-commentary-corpus:
	@if $(PYTHON) -c 'import yaml' 2>/dev/null; then \
		$(PYTHON) tools/tpt harvest promote --check --json >/dev/null && \
		$(PYTHON) tools/tpt commentary-work-index build-corpus --check >/dev/null && \
		$(PYTHON) -m unittest tools.tests.test_harvest_work_identity \
			tools.tests.test_commentary_mass_inheritance; \
	else echo "PyYAML missing; skipping commentary corpus check"; fi

check-source-library:
	@$(PYTHON) -m unittest discover -s tools/tests -p 'test_source_library.py' -v
	@$(PYTHON) -m unittest discover -s tools/tests -p 'test_source_delivery.py' -v

check-source-inventory:
	@$(PYTHON) $(SOURCE_INVENTORY_TOOL) check

check-source-inventory-tool:
	@$(PYTHON) -m unittest discover -s tools/tests -p 'test_source_inventory.py' -v

check-source-family-migration:
	@$(PYTHON) $(SOURCE_FAMILY_MIGRATION_TOOL) check

check-source-family-migration-tool:
	@$(PYTHON) -m unittest discover -s tools/tests -p 'test_source_family_migration.py' -v

check-source-family-screening:
	@$(PYTHON) $(SOURCE_FAMILY_MIGRATION_TOOL) check --require-family-screened

check-roman-sanctuary-artwork:
	@$(PYTHON) tools/tpt check-roman-sanctuary-artwork

# The publication size policy in `guidance/repository.md` --- monochrome
# publishing art as stripped 8-bit grayscale, no embedded colour profile, and
# the recorded dimensions, mode, bytes and sha256 --- is implemented by
# `artwork-library check`, and until this target existed nothing ran it:
# `grep -c artwork-library Makefile` returned 0 while the tool was registered,
# tested and passing. The manifest is what says which PNG is canonical and
# what it is allowed to be, so an asset renormalized without amending it, or a
# manifest amended without renormalizing the asset, reached the site with
# nothing reporting it.
#
# Discovered rather than listed, so a publication that gains a manifest is
# covered without anyone remembering this line. An empty discovery is a
# failure and not a pass: a gate that validated nothing must not report
# success. One manifest is found today. The altar-server guides keep their
# artwork record as prose --- `altar-server-guides/research/artwork-manifest.md`,
# 1,248 lines of provenance --- and there is no machine-readable manifest to
# check there; none is invented here.
#
# In `check` and not `check-typeset`: the manifests and every asset they
# name are tracked under `src/`, and nothing here opens `build/`.
# `artwork-library check-pdf --strict-review-triggers` is the half that does
# read a built PDF and it is deliberately absent. Measured on 2026-09-05
# against the installed altar-server edition of the sanctuary dictionary it
# reports 50 embedded images above the 450 dpi trigger and exits 1, and
# `guidance/repository.md` calls those thresholds review triggers rather than
# quotas. It belongs behind a review verb, not in front of a deploy.
check-artwork-manifests:
	@set -eu; \
		manifests=$$(find src -type f -name artwork-manifest.toml | sort); \
		if [ -z "$$manifests" ]; then \
			echo 'No artwork manifest was discovered under src/' >&2; \
			exit 1; \
		fi; \
		for manifest in $$manifests; do \
			$(PYTHON) tools/tpt artwork-library check "$$manifest"; \
		done

check-curriculum-sources: check-tools
	@$(PYTHON) $(CURRICULUM_STRUCTURE_CHECKER) \
		--curriculum-root '$(ECCLESIASTICAL_LATIN_ROOT)' --sources-only

check-curriculum-structure: \
	check-tools check-curriculum-sources $(ECCLESIASTICAL_LATIN_BUILD_PDFS)
	@set -u; \
		status=0; \
		if [ -z '$(strip $(ECCLESIASTICAL_LATIN_DOCUMENTS))' ]; then \
			echo 'No Ecclesiastical Latin publications were discovered' >&2; \
			exit 1; \
		fi; \
		for document in $(ECCLESIASTICAL_LATIN_DOCUMENTS); do \
			$(PYTHON) $(CURRICULUM_STRUCTURE_CHECKER) \
				--curriculum-root '$(ECCLESIASTICAL_LATIN_ROOT)' \
				--skip-source-audit \
				--document "$$document" \
				--toc "$(BUILD_ROOT)/$$document.toc" \
				--out "$(BUILD_ROOT)/$$document.out" \
				--pdf "$(BUILD_ROOT)/$$document.pdf" || status=1; \
		done; \
		exit $$status

help:
	@printf '%s\n' \
		'Every build, review, list, and metadata target honors PROVIDER=<p> (default gpt; claude is the peer branch)' \
		'make          Validate sources and build the public website without PDFs' \
		'make pdf      Explicitly build every document with at most $(PDF_JOBS) parallel jobs, or the current Make jobserver' \
		'make review-pdfs  Build with at most $(PDF_JOBS) jobs, then raster PDFs changed since the last review-pdfs' \
		'make review-all-pdfs  Build with at most $(PDF_JOBS) jobs, then raster every PDF' \
		'make doc DOC=<id>  Build one document below src/$$PROVIDER/' \
		'make review-doc DOC=<id>  Build one document and raster it for page review' \
		'make altar-server-guides  Build the complete seven-publication altar-server series' \
		'make review-altar-server-guides  Build and raster all seven altar-server publications' \
		'make list     List discovered document IDs' \
		'make dependencies-arch  List canonical Arch package dependencies' \
		'make install-dependencies-arch  Run a full Arch upgrade and install canonical packages' \
		'make dependencies-arch-browser  List the browser package the harnesses need and this installer omits' \
		'make dependencies-arch-tui  List the package the terminal reader (tools/lectern) needs and this installer omits' \
		'make check-pdf-review  Test memory-bounded PDF inspection tooling' \
		'make check-sources  Validate the source library, inventory, and migration ledger' \
		'make check-research-sources  Replay full evidence, source projections, and research inventories without automatic downloads' \
		'make check-deployment-sources  Validate source publication, rights, and schemas without PDFs' \
		'make prepare-browser-data  Verify exact cached browser products or derive missing families offline' \
		'make check-browser-products  Check current browser product inputs and cached bytes without generation' \
		'make check-document-schemas  Validate every publication type, identity, and source/output ownership' \
		'make check-document-content  Audit deeper profile/content requirements and run their source gates' \
		'make check-artifact-delivery  Validate external evidence delivery metadata without hydration' \
		'make check-snapshot-delivery  Validate exact historical-input delivery metadata without archives or network' \
		'make check-papal-inputs  Validate mechanically extracted release records against current canonical selections' \
		'make check-source-library  Test reusable source-library tooling' \
		'make check-source-inventory  Replay the exhaustive legacy-source inventory' \
		'make check-source-inventory-tool  Test legacy-source inventory tooling' \
		'make check-source-family-migration  Check the reviewed family migration ledger' \
		'make check-source-family-migration-tool  Test family migration ledger tooling' \
		'make check-source-family-screening  Require every migration review unit to be screened' \
		'make check-source-containment  Require every container record to say which works it holds' \
		'make check-commentator-inventories  Validate author standing and the Mass-keyed commentary loci' \
		'make check-curriculum-structure  Build and audit every Ecclesiastical Latin publication hierarchy' \
		'make check-metadata  Validate structured and inherited AI provenance' \
		'make check-web-editions  Validate per-leaf web-edition eligibility declarations' \
		'make web-editions  Generate Markdown for every eligible leaf of $$PROVIDER into build/web for inspection' \
		'make web-figures  Compile every web edition figure (TikZ to SVG) for the site build' \
		'make check-web-edition-conversions  Convert every web reader from its TeX with all fidelity audits' \
		'make check-document-catalogue  Confirm titles, identities, and the catalogue against authoritative sources' \
		'make document-catalogue  Rewrite the browser catalogue of every document' \
		'make source-projection  Rewrite the browser reading of the source library' \
		'make encyclicals-catalogue [INDEX=<path>]  Rewrite the browser catalogue of encyclicals from its index' \
		'make check-source-reader  Prove no withheld source text is served, and no reading is stale' \
		'make check-public-alpha  Validate the exhaustive public-release policy' \
		'make prepare-public-alpha  Print current candidate hashes; grants no approval' \
		'make public-preview  Build a private no-index preview with review candidates' \
		'make public-site  Build the fail-closed, history-free public artifact' \
		'make print-document DOCUMENT=<qualified-id> [PRINT_EDITION=main] [PRINT_OUT=.scratch/print-document]  Build one optional PDF and receipt' \
		'make verify-public-preview  Recheck the existing private preview artifact' \
		'make verify-public-site  Recheck the existing public artifact' \
		'make check-release-bindings  Report stale shared site and authorization-record bindings' \
		'make refresh-release-bindings [ADOPT=1] [ONLY="path ..."]  Refresh shared site-authorization inputs; ONLY restricts it to your own paths' \
		'make approve-release NOTE="..."  Record a dated supplement with the operator instruction, then refresh' \
		'make add-publication ID=<leaf> CATALOG=<page> [PROVIDER=<p>] [STATUS=hold]  Add an independent alpha record' \
		'make bibles   Typeset every publishable bible edition complete into build/bibles' \
		'make bible BIBLE=<edition>  Typeset one publishable edition complete' \
		'make review-bible BIBLE=<edition>  Typeset one edition and raster it for page review' \
		'make check-bibles [PLAN=<plan>]  Prove every publishable edition and every track of the plan can be set, writing nothing' \
		'make tracks [PLAN=<plan>]  Typeset every track of the abridged plan into build/reading-plans' \
		'make track VOLUME=<id>  Typeset one track' \
		'make review-track VOLUME=<id>  Typeset one track and raster it for page review' \
		'make reading-structure  Rewrite the browser structure of every abridged plan' \
		'make check    Run every policy check over tracked sources; names the ones it leaves' \
		'make check-typeset  Build the typeset outputs the rights scan reads, then run it' \
		'make check-all  Run all source/research checks without building PDFs' \
		'make check-calendar-days  Refuse stale generated calendar-day structures' \
		'make check-calendar-rubrics  Validate the rubrical precedence sources and their solved cases' \
		'make check-propers-census  Refuse a document whose derived count table has gone stale' \
		'make check-propers-structure  Refuse a reader projection the calendar has outgrown' \
		'make check-tests  Run the complete script unit-test suite' \
		'make check-staleness  Suspended 2026-07-31; reports the suspension and exits clean' \
		'make measure-staleness  Run the suspended signal anyway, without acting on it' \
		'make explain-staleness DOC=<leaf> [PROVIDER=<p>]  Name the changed research inputs' \
		'make rebaseline-doc DOC=<leaf> [PROVIDER=<p>]  Clear a staleness flag after re-evaluation' \
		'make clean    Remove transient build artifacts only'

check-metadata:
	@$(METADATA_CHECKER) --provider $(PROVIDER)

check-promised-deliverables: | prepare-browser-data
	@$(PYTHON) tools/tpt check-promised-deliverables

# Absence of a leaf's declaration is an error: nothing defaults to eligible.
check-web-editions:
	@$(PYTHON) $(WEB_EDITION_CHECKER) --provider $(PROVIDER)

check-proper-components:
	@$(PYTHON) $(PROPER_COMPONENT_CHECKER) --provider $(PROVIDER)

# Source titles and identities are checked independently of the descriptor's
# exact catalogue projection. PDF metadata belongs to the optional print lane.
check-document-catalogue: | prepare-browser-data
	@$(PYTHON) $(DOCUMENT_LIBRARY_TOOL) check

# Two claims again, and the first is the one that governs. `check` proves that
# no passage the rights records withhold carries any text in what is emitted,
# that every withheld passage states its reason, and that a licensed text never
# reaches the page without the acknowledgement its licence requires. It then
# replays the browser's own narrowing against the spine's facet counts.
# `structure --check` proves the cached projection is what the records produce
# now, so a source record added, corrected or withdrawn without regenerating it
# cannot reach the site as a stale reading.
check-source-reader: | prepare-browser-data
	@$(PYTHON) $(SOURCE_READER_TOOL) check
	@$(PYTHON) $(SOURCE_READER_TOOL) structure --check

# Web readers are browser products: `tools/browser-products` converts every
# reader output from its canonical TeX (the `web-editions` family) and no copy
# of their text is tracked. This target writes Markdown under build/web for
# inspecting one provider's eligible leaves; it is never an input.
web-editions:
	@set -eu; \
		leaves=$$($(PYTHON) $(WEB_EDITION_CHECKER) --provider '$(PROVIDER)' --list-eligible); \
		[ -n "$$leaves" ] || { echo 'No eligible leaf declares a web edition: $(PROVIDER)' >&2; exit 1; }; \
		$(PYTHON) $(WEB_EDITION_TOOL) --provider '$(PROVIDER)' $$leaves

# Figures are compiled from the TikZ sources the web-edition products name, and
# left alone while current. Locally they compile with the host's TeX; Pages sets
# WEB_FIGURES_RUNNER=docker:<pinned TEXLIVE_IMAGE> (.github/workflows/pages.yml).
WEB_FIGURES_RUNNER ?= host
WEB_FIGURES = $(PYTHON) $(WEB_EDITION_TOOL) figures --runner '$(WEB_FIGURES_RUNNER)'
web-figures: | prepare-browser-data
	@$(WEB_FIGURES)

# Every reader output converts from its current TeX with every fidelity audit,
# whatever state the product cache is in. Nothing is written.
check-web-edition-conversions:
	@$(PYTHON) $(WEB_EDITION_TOOL) check

check-public-alpha: check-curriculum-source-rights | prepare-browser-data
	@$(PYTHON) $(PUBLIC_ALPHA_TOOL) check

prepare-public-alpha: check-curriculum-source-rights | prepare-browser-data
	@$(PYTHON) $(PUBLIC_ALPHA_TOOL) prepare

# check-deployment-sources has verified the products, in a sub-make when the
# caller gave no jobserver, so the site compiles its figures in its own recipe:
# web-figures would verify the products a second time.
public-preview: check-deployment-sources
	@$(WEB_FIGURES)
	@$(PYTHON) $(PUBLIC_ALPHA_TOOL) build --preview

public-site: check-deployment-sources
	@$(WEB_FIGURES)
	@$(PYTHON) $(PUBLIC_ALPHA_TOOL) build

verify-public-preview: check-curriculum-source-rights | prepare-browser-data
	@$(PYTHON) $(PUBLIC_ALPHA_TOOL) verify --preview

verify-public-site: check-curriculum-source-rights | prepare-browser-data
	@$(PYTHON) $(PUBLIC_ALPHA_TOOL) verify

# Release bookkeeping; approval text is the operator's act, never invented.
check-release-bindings: | prepare-browser-data
	@$(PYTHON) $(RELEASE_BINDINGS_TOOL) status

# ONLY="path [path ...]" re-records just those paths and carries every other
# entry forward. Use it whenever anything else is uncommitted in the tree: an
# unfiltered refresh signs the authorization for whatever a sibling happens to
# have mid-flight, and the authorization means someone reviewed those bytes.
refresh-release-bindings:
	@$(PYTHON) $(RELEASE_BINDINGS_TOOL) refresh \
		$(if $(ADOPT),--adopt-new-site-sources,) \
		$(foreach path,$(ONLY),--only $(path))

approve-release:
	@if [ -z '$(NOTE)' ]; then \
		echo 'approve-release requires NOTE="<operator instruction text>"' >&2; \
		exit 1; \
	fi
	@$(PYTHON) $(RELEASE_BINDINGS_TOOL) approve --note '$(NOTE)'

add-publication:
	@if [ -z '$(ID)' ] || [ -z '$(CATALOG)' ]; then \
		echo 'add-publication requires ID=<leaf-id> CATALOG=<library page> [PROVIDER=$(PROVIDER)] [STATUS=hold]' >&2; \
		exit 1; \
	fi
	@$(PYTHON) $(RELEASE_BINDINGS_TOOL) add-publication --provider '$(PROVIDER)' \
		--id '$(ID)' --catalog '$(CATALOG)' --status '$(or $(STATUS),hold)'

# Single-document convenience wrappers: make doc DOC=<id> [PROVIDER=<p>]
# The qualified print route writes exactly one selected result and its receipt
# under scratch. It preserves DOC's existing unqualified provider-leaf meaning.
print-document:
	@if [ -z '$(DOCUMENT)' ]; then \
		echo 'print-document requires DOCUMENT=<publication:provider/leaf|bible:edition|reading-plan:volume|papal:selection/lang> [PRINT_EDITION=main|research|synthesis|homily] [PRINT_OUT=.scratch/print-document]' >&2; \
		exit 2; \
	fi
	@$(PYTHON) $(PRINT_DOCUMENT_TOOL) build --document '$(DOCUMENT)' \
		--edition '$(PRINT_EDITION)' --out '$(PRINT_OUT)'

doc:
	@if [ -z '$(DOC)' ]; then \
		echo 'doc requires DOC=<document id below src/$(PROVIDER)/>' >&2; \
		exit 1; \
	fi
	@$(MAKE) --no-print-directory '$(BUILD_ROOT)/.metadata/$(DOC).verify'

review-doc: doc
	@$(PYTHON) $(PDF_REVIEW_TOOL) '$(BUILD_ROOT)/$(DOC).pdf'

# The altar-server profile makes the seven leaves one review unit whenever a
# shared render source changes. Keep an explicit series lifecycle so a change
# to one member is built, metadata-validated and rastered with the other six.
altar-server-guides: check-metadata $(ALTAR_SERVER_GUIDES_METADATA_VERIFICATIONS)
	@test '$(words $(ALTAR_SERVER_GUIDES_DOCUMENTS))' -eq 7 || { \
		echo 'Expected exactly seven altar-server publications; found $(words $(ALTAR_SERVER_GUIDES_DOCUMENTS))' >&2; \
		exit 1; \
	}

review-altar-server-guides: altar-server-guides
	@$(PYTHON) $(PDF_REVIEW_TOOL) $(ALTAR_SERVER_GUIDES_BUILD_PDFS)

# Cross-provider research staleness (policy in guidance/staleness.md).
#
# SUSPENDED on 31 July 2026 by the maintainer. Nothing is flagged stale until
# the tooling settles. The signal is not merely noisy — it measures library
# growth rather than dependency, so a paper on the virtues reported 156 changed
# inputs, every one a Clementine verse table it does not bind — and the tooling
# that will keep changing under these papers has further to go, so a baseline
# taken now would be taken against a moving one. The papers are to be left
# exactly as they are; one full pass back through the research happens when the
# tooling has matured.
#
# Suspended rather than rebaselined on purpose. Rebaselining writes down that
# the research WAS re-read against the changed inputs, which is a review that
# did not happen. Suspension says the true thing: measurement has stopped.
# `measure-staleness` still runs it for anyone who wants to look.
check-staleness:
	@echo 'staleness: suspended 2026-07-31; papers are left as they are until the tooling settles'
	@echo 'staleness: nothing is rebaselined, so no paper claims a review it did not have'
	@echo 'staleness: run `make measure-staleness` to see the raw signal'

# The raw signal, for looking at rather than acting on. It exits non-zero when
# anything is stale, which is right for a gate and wrong for a diagnostic, so
# the status is reported and not propagated while the suspension stands.
measure-staleness:
	@$(PYTHON) $(RESEARCH_STALENESS_TOOL) status || \
		echo 'staleness: the signal above is suspended; do not act on it (see check-staleness)'

explain-staleness:
	@if [ -z '$(DOC)' ]; then \
		echo 'explain-staleness requires DOC=<leaf-id> [PROVIDER=$(PROVIDER)]' >&2; \
		exit 1; \
	fi
	@$(PYTHON) $(RESEARCH_STALENESS_TOOL) explain '$(PROVIDER)' '$(DOC)'

rebaseline-doc:
	@if [ -z '$(DOC)' ]; then \
		echo 'rebaseline-doc requires DOC=<leaf-id> [PROVIDER=$(PROVIDER)]' >&2; \
		exit 1; \
	fi
	@$(PYTHON) $(RESEARCH_STALENESS_TOOL) rebaseline --provider '$(PROVIDER)' --id '$(DOC)'

# Optional typeset-artifact QA over local builds. The build validates every
# selected render's metadata; this additional scan reads the built curriculum
# PDFs under build/gpt/. None of these builds are prerequisites of source
# publication or check-all.
TYPESET_TREE_CHECKS := check-curriculum-rights

# The third list: gates over tracked sources that are cheap to state and
# expensive to run. They belong in neither of the two above --- they read
# `src/` and want no build, so `check-typeset` would order a seven-minute
# corpus build in front of a check that needs none --- but a member that turns
# `make check` from seconds into minutes forfeits the property the next comment
# says `check` is kept for, and a gate nobody can afford to run is not a gate.
#
# `check-catena-structure` is here on measurement, not principle: 348s on
# 2026-09-05 against a warm tree, because `--check` regenerates the whole
# catena to compare and spawns node once per book. Its sibling
# `check-catena-paragraphs` answers the same kind of question over 5,548 files
# in 0.8s and stays in `check`. If that derivation ever stops paying per book,
# this member belongs back in `check` and this list can go with it.
EXPENSIVE_SOURCE_CHECKS := check-catena-structure

check-expensive: $(EXPENSIVE_SOURCE_CHECKS)

# Source types and logical output ownership are checked independently of render
# metadata. Deep evidence replay and optional print inspection have named lanes;
# a successful publication check does not assert their results.
check: check-document-schemas check-artifact-delivery check-snapshot-delivery \
	check-papal-inputs check-metadata \
	check-web-editions check-web-edition-conversions \
	check-proper-components \
	check-roman-sanctuary-artwork check-artwork-manifests \
	check-release-bindings check-promised-deliverables check-public-alpha \
	check-tool-registry \
	check-browser-static \
	check-calendar-days check-calendar-masses check-calendar-rubrics \
	check-propers-census check-propers-structure \
	check-mass-ordinary check-bible-indexes check-catena \
	check-catena-paragraphs \
	check-commentary-coverage check-commentary-corpus check-scripture-chronology check-examples
	@printf '%s\n' \
		'check covers source schemas, publication metadata and browser projections.' \
		'`make check-research-sources` replays full evidence and source projections.' \
		'`make check-expensive` runs: $(EXPENSIVE_SOURCE_CHECKS).' \
		'`make check-all` includes those source/research lanes; it never builds PDFs.' \
		'`make check-document-content` audits deeper profile/content requirements.' \
		'`make check-typeset` separately builds and checks optional typeset outputs.'

# The same gates, with the build that produces what they read ordered ahead of
# them. From a clone that has never been built this is correct without a manual
# step. Recursion rather than a prerequisite list: every one of them must see a
# finished build, and prerequisites of one target may run in any order,
# including alongside the build. The curriculum is a gpt publication, so its
# build is asked of gpt whatever PROVIDER this invocation names.
#
# This target was `check-installed`, which first copied every provider's PDFs
# into pdf/ and scanned the copies. The copies were never what a reader
# received, and on 2026-11-04 the maintainer retired the pdf/ tree; the scan
# now reads the same bytes where the build leaves them.
check-typeset:
	+@$(MAKE) --no-print-directory $(_TRIPTYCH_BOUNDED_PDF_JOB_OPTION) PROVIDER=gpt _typeset-tree
	@$(MAKE) --no-print-directory $(TYPESET_TREE_CHECKS)

_typeset-tree: check-metadata $(ECCLESIASTICAL_LATIN_METADATA_VERIFICATIONS)

check-all: check check-expensive check-research-sources

# Seven of the browser scripts are parsed by nothing: no Python test loads
# them, no node harness runs them, and their only protection is a sha256 pin in
# release/public-alpha.json, which proves a file did not change rather than
# that it is a program. This also runs the build's own page split at check
# time, because a browser page the layout cannot take apart currently fails
# during `make public-site`, which `check` does not run. Half a second, and it
# needs no browser.
check-browser-static:
	@$(PYTHON) -m unittest discover -s tools/tests -p 'test_browser_static.py'

# Real Chromium over the built artifact, which is the only place the publish
# step's own defects exist: the four harnesses beside it all load the
# repository copies, so a second `<main>` or a stripped skip link introduced by
# `wrap_in_layout` is invisible to every one of them. Deliberately outside
# `check`: it needs a browser the installer does not install and an artifact
# `check` does not build. Run `make public-site` first, and set TRIPTYCH_CHROME
# unless google-chrome-stable is the browser present. It asserts nothing about
# how the site looks, because no visual contract has been accepted.
check-browser-gate:
	@node tools/tests/corpus_browser_gate.mjs

# Every admitted native print edition, compiled from the exact source bundle
# the site serves and the engine that bundle names, under the browser's pass
# policy. It fails on any compile failure, missing PDF, unsettled edition,
# admitted/materialized set difference, or file opened outside the bundle and
# the pinned browser runtime's `texFiles`. Pages runs this as its own job in the
# pinned TeX Live image before deploying; here it needs host pdfTeX, XeTeX,
# xdvipdfmx and poppler, with Latin Babel support. Outside `check` because it
# typesets the whole print universe (about 12 CPU-minutes).
NATIVE_PRINT_COMPILE_OUT ?= .scratch/native-print-compile
check-native-print-compile:
	@$(PYTHON) tools/tpt native-print-compile prepare --out '$(NATIVE_PRINT_COMPILE_OUT)'
	@$(PYTHON) tools/tpt native-print-compile compile --out '$(NATIVE_PRINT_COMPILE_OUT)'

# The five reader harnesses drive real Chromium over the preview build, and
# until this target existed nothing ran them: the suite only syntax-checked
# them, so they were read as broken for months when what they wanted was a
# build. All five address `build/public-alpha/preview` as their data root, so
# without `public-preview` every request 404s and the failure wears the costume
# of a code defect — "Timed out waiting for ... readiness". Hence the
# prerequisite. Outside `check` for the same reasons as `check-browser-gate`,
# and because it takes two minutes rather than half a second. The contract is
# exact and all-green: `ASSERTION_COUNTS` in `test_browser_harnesses.py` names
# every harness's assertion count, and each must pass all of them with a zero
# exit and no console, request or HTTP problem. A partial pass fails, and so
# does an assertion added or removed without changing that count.
check-browser-harnesses: public-preview
	@TRIPTYCH_BROWSER_HARNESSES=1 $(PYTHON) -m unittest discover -s tools/tests -p 'test_browser_harnesses.py'

# Every tool carries a table of captured invocations, and until this target
# existed nothing ran one: the registry test counted lines beginning with a
# "$$ " prompt. This runs each captured invocation and holds the transcript to
# what it prints. The transcripts are no longer printed in `--help` — a reader
# wants the command, not a page of output — which makes this the only reader
# they have and the only thing standing behind the claim that they are real.
# It is in `check` rather than behind a flag
# because an example nobody replays is the defect it exists to catch; it takes
# about two minutes, which is the price of the claim.
check-examples:
	@$(PYTHON) scripts/replay_examples.py

# The only way a transcript should ever change: re-run the invocation and write
# down what it printed, keeping the elisions the author chose.
recapture-examples:
	@$(PYTHON) scripts/replay_examples.py --recapture

# tmt.json indexes the repo's tools; invoke them through tpt.
# tools dispatch through tmt entries to their implementation under tools/.
# Skipped rather than failed where tmt is not installed, so a plain clone
# still runs `check`.
check-tool-registry:
	@if command -v tmt >/dev/null; then tmt check; \
	else echo "tmt not installed; skipping tool-registry check"; fi

# Replays date computation against the prepared, sealed browser projection and
# writes nothing. Needs PyYAML, skipped rather than failed without it.
check-calendar-days: | prepare-browser-data
	@if $(PYTHON) -c 'import yaml' 2>/dev/null; then \
		$(PYTHON) tools/tpt calendar-days check; \
	else echo "PyYAML missing; skipping calendar-day check"; fi

# Needs PyYAML (requirements-tools.txt); skipped rather than failed without it.
# Two claims. The first is that the sources are valid; the second is that what
# the browser is served is what those sources produce NOW. `make check` proved
# tracked web/**/*.md current and proved nothing about src/web/data/structure,
# so on 2026-08-07 regenerating the propers with unchanged tools rewrote 4,269
# lines of roman-pre-1955.json that no source change accounted for — the served
# recension had drifted that far with nothing reporting it. `structure --check`
# writes nothing; `mass-propers structure` is what fixes a failure.
check-calendar-masses: | prepare-browser-data
	@if $(PYTHON) -c 'import yaml' 2>/dev/null; then \
		$(PYTHON) tools/tpt check-calendar-masses && \
		$(PYTHON) -m unittest tools.tests.test_lasance_source_printing_1946 -v && \
		$(PYTHON) tools/tpt mass-propers structure --check; \
	else echo "PyYAML missing; skipping calendar-mass check"; fi

# Validates the rubrical precedence sources, refuses a stale generated layer,
# and runs the browser's own derivation over each source's solved cases. Needs
# PyYAML for the sources and node for the derivation. A missing node is a
# failure inside the tool and not a skip: the solved cases are the only thing
# holding assembly-model.js to the tracked tables, and a run that could not
# exercise them has confirmed nothing to report as a pass.
check-calendar-rubrics: | prepare-browser-data
	@if $(PYTHON) -c 'import yaml' 2>/dev/null; then \
		$(PYTHON) tools/tpt calendar-rubrics check; \
	else echo "PyYAML missing; skipping calendar-rubric check"; fi

# The count of both calendars is derived, not typed: one census, written into
# the one document that carries it, which the others link to. This refuses a
# block that has drifted from the calendars or a copy of it elsewhere, and
# writes nothing — `mass-propers census --write` is what fixes a drifted block.
# Needs PyYAML, skipped rather than failed without it.
check-propers-census:
	@if $(PYTHON) -c 'import yaml' 2>/dev/null; then \
		$(PYTHON) tools/tpt mass-propers census --check; \
	else echo "PyYAML missing; skipping propers-census check"; fi

# The browser and the day reader read the descriptor's derived propers JSON.
# `mass-propers structure --check` has
# always known that, but it lived only in `check-deployment-sources`, which
# `check` does not reach -- so on 2026-09-03 the seasonal backfill landed 198
# Latin bodies with `check-calendar-masses`, `check-propers-census` and 175
# rights tests all passing while every reader still showed the old
# rights-withheld shape. Nothing reported it. `mass-propers structure` writes
# the fix; this only refuses the drift.
check-propers-structure: | prepare-browser-data
	@if $(PYTHON) -c 'import yaml' 2>/dev/null; then \
		$(PYTHON) tools/tpt mass-propers structure --check; \
	else echo "PyYAML missing; skipping propers-structure check"; fi

# The Ordinary of the Mass: validates the two ordo-missae inventories against
# the artifacts they draw on and against the source library's own rights record,
# and refuses a browser file that no longer matches. Needs no third-party
# module, so it is a plain failure and never a skip.
check-mass-ordinary: | prepare-browser-data
	@$(PYTHON) tools/tpt mass-ordinary check

# An indexed bible is keyed by the reference strings the calendars actually
# make, so a calendar that gains a citation leaves every index stale, and
# nothing said so. All seven were stale on 2026-08-20: over two liturgical
# years the same days that render with 6 scripture absences against a current
# index showed 128 against the tracked one, and the Commune Confessoris
# Pontificis' Lesson printed `Sirach 45:3-20` with nothing under it while
# every source-side gate stayed green. Unresolved references are reported and
# are not a failure; a stale index is.
check-bible-indexes:
	@set -e; for bible in $$(ls src/sources/bibles); do \
		test -d src/sources/bibles/$$bible || continue; \
		$(PYTHON) tools/tpt index-bible check --bible $$bible >/dev/null; \
	done; echo "bible indexes current"

# Validates the scripture edge every catena fragment hangs from, and replays
# the browser's own chapter derivation over the solved cases. Until this target
# existed the edge was checked only by running the script by hand, which meant a
# fragment pointing at a passage that no longer existed, or at a work whose
# alias group had moved, would have reached the site rather than the check.
# Needs PyYAML for the sources; node is exercised inside the tool and a missing
# node is a failure there rather than a skip here, for the same reason it is in
# check-calendar-rubrics.
check-catena:
	@if $(PYTHON) -c 'import yaml' 2>/dev/null; then \
		$(PYTHON) scripts/_catena.py check; \
	else echo "PyYAML missing; skipping catena check"; fi

# `check-catena` proves the scripture edge; these two prove that what the
# browser is served over it is what the generator produces NOW. `structure`
# and `paragraphs` write 12,049 hash-bound files under
# src/web/data/structure/, and nothing gated them: a change to the derivation
# moved every one of them silently. That is the same defect
# `check-propers-structure` was added for on 2026-09-03, at four orders of
# magnitude more files. Both verbs write nothing under `--check`;
# `scripts/_catena.py structure` and `... paragraphs` are what fix a failure.
#
# Both read and compare tracked files under `src/` and neither wants a build,
# so neither belongs in `check-typeset`. They part company on cost, which is
# measured rather than assumed: `paragraphs --check` compares 5,548 files in
# 0.8s and is a `check` member; `structure --check` takes 348s over 1,914,
# because it regenerates the catena to compare and spawns node once per book,
# so it is in $(EXPENSIVE_SOURCE_CHECKS) and `make check` names it as not run.
# Guarded on PyYAML for the reason `check-catena` above them is --- the script
# reads the calendars through it --- and the skip says so rather than
# reporting a check that did not run.
check-catena-structure: | prepare-browser-data
	@if $(PYTHON) -c 'import yaml' 2>/dev/null; then \
		$(PYTHON) scripts/_catena.py structure --check; \
	else echo "PyYAML missing; skipping catena structure check"; fi

check-catena-paragraphs: | prepare-browser-data
	@if $(PYTHON) -c 'import yaml' 2>/dev/null; then \
		$(PYTHON) scripts/_catena.py paragraphs --check; \
	else echo "PyYAML missing; skipping catena paragraph check"; fi

# A GAP NEVER FAILS THIS. An unacquired work is not a defect, and a build that
# refused to go green until someone had gone and got the rest of De civitate Dei
# would be a build nobody could ship. What fails is the extent RECORD being
# unusable — a row naming no work, an extent past the end of a book, or an
# extent a held fragment of the same work already reaches past, which means one
# of the two is wrong and subtracting either from the other reports a clean
# corpus regardless.
#
# But it prints on every run, because the whole reason De civitate Dei sat held
# on Genesis 1-2 while its fifteenth book expounds Cain and Abel was that every
# gate passed and none of them said anything about where the fragments were not.
# `guidance/the-shape.md` §4: absence is data and has to have somewhere to live.
# The line names the verb that expands it rather than listing the works, so the
# summary stays one line and the detail stays one command away.
check-commentary-coverage:
	@if $(PYTHON) -c 'import yaml' 2>/dev/null; then \
		$(PYTHON) scripts/_coverage.py; \
	else echo "PyYAML missing; skipping commentary coverage"; fi

# Two questions, and the second is the one a corpus of dates quietly fails.
# `validate` asks whether the authored chronology is well-formed: every claim
# sourced, every referenced event and profile declared, no year zero, no
# inverted range, no two composition units of the same width over one verse.
# `check` asks whether the derived coverage table is what a fresh derivation
# produces, and REFUSES A STALE ONE RATHER THAN REBUILDING IT — a verification
# that repairs what it was meant to detect reports success either way, and
# `guidance/the-shape.md` §1 records what this project has already paid for
# apparatus that is not exempt from the defect it exists to catch.
#
# A locus with no date is NOT a failure here. Most of Scripture is
# research-pending and saying so is the honest report; what fails is a corpus
# that cannot say it — an assertion citing a source this repository does not
# hold, a scope naming a verse past its chapter's end, or a gap standing over a
# verse that carries an assertion. Needs PyYAML; a missing PyYAML skips, and
# says it skipped, because a silent green line asserts a check that did not run.
check-scripture-chronology:
	@if $(PYTHON) -c 'import yaml' 2>/dev/null; then \
		$(PYTHON) tools/tpt scripture-chronology validate && \
		$(PYTHON) tools/tpt scripture-chronology check; \
	else echo "PyYAML missing; skipping scripture chronology check"; fi

# One worker process per core, because the suite's time is overwhelmingly one
# process waiting on another rather than arithmetic. `scripts/run_tests.py`
# says how the work is divided and why the split is per module. It asserts
# exactly what `python -m unittest discover -s tools/tests` asserts, and that
# command still works unchanged --- use it, or `TEST_JOBS=-j1`, when a failure
# wants a debugger and a single process.
check-tests:
	@$(PYTHON) scripts/run_tests.py $(TEST_JOBS)

# Register only render-capable files owned by a document leaf. Research and
# retrieval records remain authoritative tracked sources, but changing one does
# not recompile an unchanged TeX publication. Cross-document sources are
# declared separately below.
define REGISTER_DOCUMENT_SOURCES
$(BUILD_ROOT)/$(1).pdf: $(shell find $(SOURCE_ROOT)/$(1) -type f \( \
	-name '*.tex' -o -name '*.sty' -o -name '*.cls' -o -name '*.bib' -o \
	-name '*.bst' -o -name '*.png' -o -name '*.jpg' -o -name '*.jpeg' -o \
	-name '*.pdf' -o -name '*.eps' \) | sort)
endef
$(foreach document,$(CANONICAL_DOCUMENTS),$(eval $(call REGISTER_DOCUMENT_SOURCES,$(document))))

# Each provider's Four Last Things series imports its own shared format.
ifneq ($(filter $(PROVIDER),gpt claude),)
FOUR_LAST_THINGS_DOCUMENTS := $(addprefix articles/faith/four-last-things-,01-death 02-judgment 03-hell 04-heaven)
$(addprefix $(BUILD_ROOT)/,$(addsuffix .pdf,$(FOUR_LAST_THINGS_DOCUMENTS))): \
	$(SOURCE_ROOT)/articles/faith/four-last-things-shared/format.tex
endif

# `evaluations/` is pruned because nothing in it is rendered and the engine
# writes into it while a run is in flight: the standing-findings record an
# evaluation stage writes is a `.toml` under the leaf, so registering it made
# every derived PDF stale between the artifact build and installation. The
# retypeset that follows is byte-identical in the PDF and not in the log,
# whose first line carries pdfTeX's clock, and that log is sealed as this
# workflow's pagination evidence -- so a record of what a reviewer found
# invalidated the proof the reviewer had read.
define REGISTER_PROPER_DERIVED_SOURCES
$(BUILD_ROOT)/$(1).pdf: $(shell find $(SOURCE_ROOT)/$(patsubst %-homily,%,$(patsubst %-synthesis,%,$(1))) \
	-type d -name evaluations -prune -o \
	-type f \( -name '*.tex' -o -name '*.toml' -o -name '*.sty' -o -name '*.bib' \) \
	-print 2>/dev/null | sort)
endef
$(foreach document,$(PROPER_DERIVED_DOCUMENTS),\
	$(eval $(call REGISTER_PROPER_DERIVED_SOURCES,$(document))))

$(foreach document,$(PROPER_SYNTHESIS_DOCUMENTS),\
	$(eval $(BUILD_ROOT)/$(document).pdf: \
		$(SOURCE_ROOT)/$(patsubst %-synthesis,%,$(document))/synthesis.tex))

$(foreach document,$(PROPER_HOMILY_DOCUMENTS),\
	$(eval $(BUILD_ROOT)/$(document).pdf: \
		$(SOURCE_ROOT)/$(patsubst %-homily,%,$(document))/homily.tex))

# Each edition's "Last revised" stamp is derived from git, never tracked
# (scripts/_edition_revision.py states the rule). The stamp file is written
# beside the job, as $(BUILD_ROOT)/<document>.revision.tex, and the shared
# preamble reads it as \jobname.revision.tex through the job's output
# directory on TEXINPUTS. Its rule runs on every invocation but rewrites the
# file only when the stamp changes, so a PDF is retypeset exactly when its
# derived stamp moves: a commit, or an edit that leaves the tree uncommitted.
# It shares the job's prefix, so the declared-input check below treats it as
# the job's own file, and it is precious so that Make does not delete it as an
# intermediate and retypeset next time.
EDITION_REVISION_SUFFIX := .revision.tex
EDITION_REVISION_TOOL := scripts/_edition_revision.py
FORCE_EDITION_REVISION:
.PRECIOUS: $(BUILD_ROOT)/%$(EDITION_REVISION_SUFFIX)
$(BUILD_ROOT)/%$(EDITION_REVISION_SUFFIX): FORCE_EDITION_REVISION
	@$(PYTHON) $(EDITION_REVISION_TOOL) write --provider '$(PROVIDER)' --document '$*' --out '$@'

# Templates and deterministic pages are assembled at use, without rewriting
# the carried source snapshots. Recheck the projection on every invocation;
# its manifest's mtime changes only when its actual rendered bytes change.
# Consequently a shared corpus/template edit rebuilds exactly the affected
# print outputs, while the untouched source checkout stays untouched.
FORCE_DOCUMENT_ASSEMBLY:
.PRECIOUS: $(BUILD_ROOT)/.assembly/%/manifest.json
$(BUILD_ROOT)/.assembly/%/manifest.json: FORCE_DOCUMENT_ASSEMBLY
	@set -eu; \
		document='$*'; entry="$$document/main.tex"; \
		case "$$document" in \
			*-synthesis) entry="$${document%-synthesis}/synthesis.tex" ;; \
			*-homily) entry="$${document%-homily}/homily.tex" ;; \
		esac; \
		$(PYTHON) scripts/_document_types.py stage --provider '$(PROVIDER)' \
			--entrypoint "$$entry" --out '$(@D)'

# Run pdfLaTeX until the document stops moving under it.
#
# Two passes settle most documents and settle none reliably. A table of
# contents that grows a page moves the pages it is naming, so the pass that
# writes a corrected contents entry is not the pass that typesets it, and a
# third pass can still change the PDF. `assembling-the-mass` is the worked
# case: from a clean tree its second pass emits no "Rerun to get
# cross-references right" and still prints a contents page number one short.
# Grepping the log is therefore not a test of convergence. The auxiliary
# files are.
#
# Each pass reads the auxiliary files the pass before it wrote. When a pass
# writes back exactly what it read, the next pass would be handed identical
# input and the preamble's \pdfinfoomitdate and \pdftrailerid{} leave nothing
# else to vary, so the fixed point is reached and the PDF in hand is final.
# The .log is excluded because it carries the run's timestamp and is never
# read back; the .pdf because it is the output rather than an input, and
# waiting for two equal PDFs would only ever cost one pass more.
#
# Fail rather than publish a document whose contents point at the wrong
# pages. latexmk would keep this loop for us, and lives in texlive-binextra,
# which ARCH_TEX_PACKAGES deliberately does not name; this is that loop in
# the shell the recipe already runs.
#
# The .fls is excluded for the same reason as the .log: `-recorder` writes it
# on every pass and nothing ever reads it back, but unlike the .log it would
# also differ between the first pass and the second --- the first opens no
# .aux because none exists yet --- and so would cost an extra pass on every
# document that settles in two.
#
# Argument 1 is the -jobname, argument 2 the TeX input relative to
# $(SOURCE_ROOT), and argument 3 the build-tree prefix the job's auxiliary
# files share.
# Dictionary generated inputs follow BUILD_ROOT, including isolated print jobs;
# their source default remains the virtual build tree used by browser bundles.
define PDFLATEX_TO_FIXED_POINT
set -eu; \
	rm -f -- '$(3).fls'; \
	assembly='$(abspath $(BUILD_ROOT)/.assembly/$(patsubst $(BUILD_ROOT)/%,%,$(3)))'; \
	entry=$$(cat "$$assembly/entrypoint"); \
	pass=0; \
	fingerprint=''; \
	settled=0; \
	while [ "$$pass" -lt $(PDFLATEX_MAX_PASSES) ]; do \
		pass=$$((pass + 1)); \
		( cd $(SOURCE_ROOT) && TEXINPUTS="$$assembly/src/$(PROVIDER):..:$(abspath $(@D)):" $(PDFLATEX) -no-shell-escape -recorder \
			-interaction=nonstopmode \
			-halt-on-error -jobname='$(1)' \
			-output-directory='$(abspath $(@D))' "$(if $(filter $@,$(ROMAN_SANCTUARY_DICTIONARY_BUILD_PDFS)),\def\RSDGeneratedRoot{$(abspath $(ROMAN_SANCTUARY_DICTIONARY_GENERATED))}\input{$$entry},$$entry)" ); \
		previous="$$fingerprint"; \
		fingerprint=''; \
		for auxiliary in '$(3).'*; do \
			[ -f "$$auxiliary" ] || continue; \
			case "$$auxiliary" in \
				*.log|*.pdf|*.fls|*.fls-*|*.synctex.gz) continue ;; \
			esac; \
			fingerprint="$$fingerprint $$($(SHA256) -- "$$auxiliary")"; \
		done; \
		if [ "$$pass" -ge 2 ] && [ "$$fingerprint" = "$$previous" ]; then \
			settled=1; \
			break; \
		fi; \
	done; \
	if [ "$$settled" -eq 0 ]; then \
		echo 'References did not settle in $(PDFLATEX_MAX_PASSES) passes: $(3)' >&2; \
		exit 1; \
	fi; \
	$(call ASSERT_DECLARED_INPUTS,$(3))
endef

# Prove the declared graph complete, against what pdfTeX actually opened.
#
# Make reuses a built PDF while every prerequisite this makefile declares for
# it is unchanged, and the Pages deploy once keyed a PDF cache on the same
# prerequisites. Either is only as good as the graph, and the graph is written
# by hand. An \input that reaches a file no prerequisite names leaves that file
# outside it, so editing it would keep the old PDF --- and since a body-text edit need
# not move a page count, neither `document-library structure --check` nor the
# corpus digest binding would notice. Every other gate here fails closed. This
# is the one that would not, made to.
#
# `-recorder` has each pass write a .fls beside the PDF naming every file it
# opened. The settled pass is the one compared: it is the pass that produced
# the PDF in hand, and an input reached only before the references converged is
# not a case this corpus has. What the comparison excludes, and why none of the
# exclusions is a hole:
#
#   Outside the repository. The format file, the font map, and the TeX
#   distribution's own classes, packages, fonts and encodings. None is this
#   project's to declare and none is a cache key input: the toolchain is keyed
#   separately, by the container image digest and package snapshot.
#
#   The job's own auxiliary files --- the .aux, .toc, .out and the rest that
#   share argument 1's prefix --- which every pass after the first reads back
#   from the pass before. They are this
#   build's output being re-read, never an input to it, and no source
#   prerequisite could name them.
#
#   Rendered .tex under $(ROMAN_SANCTUARY_DICTIONARY_GENERATED), and only when
#   the target declares a prerequisite that is not a file --- the phony that
#   generates it. That tree is named rather than all of build/ because it is
#   the one the deploy hashes wholesale into the affected cache keys, so it is
#   the one whose contents are covered without being declared. A generated file
#   anywhere else under build/ is undeclared like any other and is reported:
#   the exemption is a statement about a tree the key already covers, not about
#   the target having a generator.
#
# Everything else opened inside the repository must appear in $^. Paths are
# compared through realpath because TEXINPUTS=..: makes the shared preamble
# reachable as ../common/preamble.tex from the pdfTeX working directory and as
# src/common/preamble.tex from here, and those are one file. Directory
# prerequisites are expanded to their files so a declared tree covers what is
# read out of it.
#
# A missing .fls beside a written .log means pdfTeX ran without `-recorder`,
# which is a build defect and fails. Neither file means the run was not pdfTeX
# at all --- the build-graph tests substitute a stub that writes only the PDF
# --- and there is nothing recorded to check.
#
# Argument 1 is the build-tree prefix the job's auxiliary files share.
define ASSERT_DECLARED_INPUTS
recorded='$(1).fls'; \
	if [ ! -f "$$recorded" ]; then \
		if [ -f '$(1).log' ]; then \
			echo 'pdfTeX wrote $(1).log but no $(1).fls: -recorder is not in effect, so declared inputs cannot be checked' >&2; \
			exit 1; \
		fi; \
		exit 0; \
	fi; \
	declared='$(1).fls-declared'; \
	opened='$(1).fls-opened'; \
	undeclared='$(1).fls-undeclared'; \
	trap 'rm -f -- "$$declared" "$$opened" "$$undeclared"' 0 1 2 15; \
	set -f; \
	set -- $^; \
	generator=0; \
	for prerequisite in "$$@"; do \
		[ -e "$$prerequisite" ] || generator=1; \
	done; \
	for prerequisite in "$$@"; do \
		if [ -d "$$prerequisite" ]; then \
			find "$$prerequisite" -type f; \
		else \
			printf '%s\n' "$$prerequisite"; \
		fi; \
	done > "$$declared"; \
	cat '$(BUILD_ROOT)/.assembly/$(patsubst $(BUILD_ROOT)/%,%,$(1))/files' >> "$$declared"; \
	set -- $$(cat "$$declared"); \
	{ [ "$$#" -eq 0 ] || realpath -m -- "$$@"; } | LC_ALL=C sort -u > "$$declared"; \
	while read -r role path; do \
		[ "$$role" = 'INPUT' ] || continue; \
		case "$$path" in \
			/*) printf '%s\n' "$$path" ;; \
			*) printf '%s/%s\n' '$(abspath $(SOURCE_ROOT))' "$$path" ;; \
		esac; \
	done < "$$recorded" | LC_ALL=C sort -u > "$$opened"; \
	set -- $$(cat "$$opened"); \
	{ [ "$$#" -eq 0 ] || realpath -m -- "$$@"; } | LC_ALL=C sort -u > "$$opened"; \
	own=$$(realpath -m -- '$(1)'); \
	generated=$$(realpath -m -- '$(ROMAN_SANCTUARY_DICTIONARY_GENERATED)'); \
	LC_ALL=C comm -23 -- "$$opened" "$$declared" | while read -r path; do \
		case "$$path" in '$(CURDIR)'/*) ;; *) continue ;; esac; \
		case "$$path" in "$$own".*) continue ;; esac; \
		case "$$path" in \
			"$$generated"/*) \
				if [ "$$generator" -eq 1 ]; then continue; fi ;; \
		esac; \
		printf '%s\n' "$$path"; \
	done > "$$undeclared"; \
	if [ -s "$$undeclared" ]; then \
		echo 'Undeclared input: $(1).pdf opened repository files that no' >&2; \
		echo 'prerequisite of that target names, so the deploy PDF cache key' >&2; \
		echo 'does not cover them and editing one could publish a stale PDF:' >&2; \
		while read -r path; do echo "  $$path" >&2; done < "$$undeclared"; \
		echo 'Declare each as a prerequisite of $(1).pdf in this makefile.' >&2; \
		exit 1; \
	fi
endef

# $(COMMON_SOURCES) because a synthesis is a document like any other and opens
# the shared preamble. REGISTER_PROPER_DERIVED_SOURCES already declares each
# synthesis's own sources per target; what this pattern rule was missing was
# the shared preamble alone, so a preamble edit rebuilt no synthesis at all.
# ASSERT_DECLARED_INPUTS below found it. When it did, synthesis PDFs were not
# cached by the deploy and this was an incremental-build defect rather than a
# stale-publish one. They are cached now -- check-generation-metadata learned
# to resolve a <leaf>-synthesis id to <leaf>/synthesis.tex, which is what had
# excluded them -- so this rule's prerequisites are part of a cache key, and a
# missing one would publish a stale PDF rather than merely fail to rebuild.
# A deleted source disappears from find-based prerequisites. Audit the owner
# even when its PDF is cached, without making that PDF need typesetting again.
ifneq ($(strip $(SOURCE_METADATA_CHECKS)),)
$(SOURCE_METADATA_CHECKS): $(BUILD_ROOT)/.metadata/%.source-check: | check-tools
	@$(METADATA_CHECKER) --provider '$(PROVIDER)' --document '$*'
endif

$(BUILD_ROOT)/%-synthesis.pdf: $(COMMON_SOURCES) $(BUILD_ROOT)/%-synthesis$(EDITION_REVISION_SUFFIX) $(BUILD_ROOT)/.assembly/%-synthesis/manifest.json | $(BUILD_ROOT)/.metadata/%-synthesis.source-check
	@mkdir -p $(@D) '$(BUILD_ROOT)/.metadata/$(dir $*)'
	@rm -f -- '$(BUILD_ROOT)/.metadata/$*-synthesis.ok'
	@$(call PDFLATEX_TO_FIXED_POINT,$(notdir $*)-synthesis,$*/synthesis.tex,$(BUILD_ROOT)/$*-synthesis)
	@$(PDF_ANCHOR_CHECKER) '$(BUILD_ROOT)/$*-synthesis'
	@$(PROPER_COMPONENT_CHECKER) --provider '$(PROVIDER)' --document '$*' \
		--edition synthesis --aux '$(BUILD_ROOT)/$*-synthesis.aux'
	@$(METADATA_CHECKER) --provider '$(PROVIDER)' --pdf '$*-synthesis' '$@'
	@set -eu; \
		pdf_line=$$($(SHA256) -- '$@'); pdf_hash=$${pdf_line%% *}; \
		validator_line=$$($(SHA256) -- '$(METADATA_CHECKER_IMPL)'); \
		validator_hash=$${validator_line%% *}; \
		printf 'schema=1\nprovider=%s\ndocument=%s\npdf_sha256=%s\nvalidator_sha256=%s\n' \
			'$(PROVIDER)' '$*-synthesis' "$$pdf_hash" "$$validator_hash" \
			> '$(BUILD_ROOT)/.metadata/$*-synthesis.ok'

$(BUILD_ROOT)/%-homily.pdf: $(COMMON_SOURCES) $(BUILD_ROOT)/%-homily$(EDITION_REVISION_SUFFIX) $(BUILD_ROOT)/.assembly/%-homily/manifest.json | $(BUILD_ROOT)/.metadata/%-homily.source-check
	@mkdir -p $(@D) '$(BUILD_ROOT)/.metadata/$(dir $*)'
	@rm -f -- '$(BUILD_ROOT)/.metadata/$*-homily.ok'
	@$(call PDFLATEX_TO_FIXED_POINT,$(notdir $*)-homily,$*/homily.tex,$(BUILD_ROOT)/$*-homily)
	@$(PDF_ANCHOR_CHECKER) '$(BUILD_ROOT)/$*-homily'
	@$(PROPER_COMPONENT_CHECKER) --provider '$(PROVIDER)' --document '$*' \
		--edition homily --aux '$(BUILD_ROOT)/$*-homily.aux'
	@$(METADATA_CHECKER) --provider '$(PROVIDER)' --pdf '$*-homily' '$@'
	@set -eu; \
		pdf_line=$$($(SHA256) -- '$@'); pdf_hash=$${pdf_line%% *}; \
		validator_line=$$($(SHA256) -- '$(METADATA_CHECKER_IMPL)'); \
		validator_hash=$${validator_line%% *}; \
		printf 'schema=1\nprovider=%s\ndocument=%s\npdf_sha256=%s\nvalidator_sha256=%s\n' \
			'$(PROVIDER)' '$*-homily' "$$pdf_hash" "$$validator_hash" \
			> '$(BUILD_ROOT)/.metadata/$*-homily.ok'

# A proper leaf's research edition keeps the same fixed pages as its synthesis
# companion, so it gets the same settled-aux check. Without it Claude leaf 54's
# research edition sat with its themes on page 4 for weeks and nothing failed.
# The checker, not this rule, reads the manifest and exempts a legacy order;
# a document without a manifest is not a proper leaf and is never checked.
$(BUILD_ROOT)/%.pdf: $(SOURCE_ROOT)/%/main.tex $(COMMON_SOURCES) $(BUILD_ROOT)/%$(EDITION_REVISION_SUFFIX) $(BUILD_ROOT)/.assembly/%/manifest.json | $(BUILD_ROOT)/.metadata/%.source-check
	@mkdir -p $(@D)
	@mkdir -p '$(BUILD_ROOT)/.metadata/$(dir $*)'
	@rm -f -- '$(BUILD_ROOT)/.metadata/$*.ok'
	@$(call PDFLATEX_TO_FIXED_POINT,$(notdir $*),$*/main.tex,$(BUILD_ROOT)/$*)
	@$(PDF_ANCHOR_CHECKER) '$(BUILD_ROOT)/$*'
	$(if $(wildcard $(SOURCE_ROOT)/$*/proper-components.toml),@$(PROPER_COMPONENT_CHECKER) \
		--provider '$(PROVIDER)' --document '$*' \
		--edition research --aux '$(BUILD_ROOT)/$*.aux')
	@case '$*' in \
		curriculums/ecclesiastical-latin/*) \
			$(PYTHON) $(CURRICULUM_STRUCTURE_CHECKER) \
				--curriculum-root '$(ECCLESIASTICAL_LATIN_ROOT)' \
				--skip-source-audit \
				--document '$*' \
				--toc '$(BUILD_ROOT)/$*.toc' \
				--out '$(BUILD_ROOT)/$*.out' \
				--pdf '$@' ;; \
	esac
	@set -eu; \
		pdf='$@'; \
		stamp='$(BUILD_ROOT)/.metadata/$*.ok'; \
		pdf_line=$$($(SHA256) -- "$$pdf"); \
		pdf_hash=$${pdf_line%% *}; \
		validator_line=$$($(SHA256) -- '$(METADATA_CHECKER_IMPL)'); \
		validator_hash=$${validator_line%% *}; \
		$(METADATA_CHECKER) --provider '$(PROVIDER)' --pdf '$*' "$$pdf"; \
		pdf_after_line=$$($(SHA256) -- "$$pdf"); \
		pdf_after_hash=$${pdf_after_line%% *}; \
		validator_after_line=$$($(SHA256) -- '$(METADATA_CHECKER_IMPL)'); \
		validator_after_hash=$${validator_after_line%% *}; \
		if [ "$$pdf_hash" != "$$pdf_after_hash" ] || [ "$$validator_hash" != "$$validator_after_hash" ]; then \
			echo 'PDF or metadata checker changed during validation: $*' >&2; \
			exit 1; \
		fi; \
		temporary="$$stamp.tmp.$$$$"; \
		trap 'rm -f -- "$$temporary"' 0 1 2 15; \
		printf 'schema=1\nprovider=%s\ndocument=%s\npdf_sha256=%s\nvalidator_sha256=%s\n' \
			'$(PROVIDER)' '$*' "$$pdf_hash" "$$validator_hash" > "$$temporary"; \
		mv -f -- "$$temporary" "$$stamp"; \
		trap - 0 1 2 15

$(BUILD_ROOT)/.metadata/%.ok: $(BUILD_ROOT)/%.pdf $(METADATA_CHECKER_IMPL)
	@set -eu; \
		pdf='$<'; \
		stamp='$@'; \
		pdf_line=$$($(SHA256) -- "$$pdf"); \
		pdf_hash=$${pdf_line%% *}; \
		validator_line=$$($(SHA256) -- '$(METADATA_CHECKER_IMPL)'); \
		validator_hash=$${validator_line%% *}; \
		expected=$$(printf 'schema=1\nprovider=%s\ndocument=%s\npdf_sha256=%s\nvalidator_sha256=%s' \
			'$(PROVIDER)' '$*' "$$pdf_hash" "$$validator_hash"); \
		if [ -f "$$stamp" ] && [ "$$(cat "$$stamp")" = "$$expected" ]; then \
			exit 0; \
		fi; \
		$(METADATA_CHECKER) --provider '$(PROVIDER)' --pdf '$*' "$$pdf"; \
		pdf_after_line=$$($(SHA256) -- "$$pdf"); \
		pdf_after_hash=$${pdf_after_line%% *}; \
		validator_after_line=$$($(SHA256) -- '$(METADATA_CHECKER_IMPL)'); \
		validator_after_hash=$${validator_after_line%% *}; \
		if [ "$$pdf_hash" != "$$pdf_after_hash" ] || [ "$$validator_hash" != "$$validator_after_hash" ]; then \
			echo 'PDF or metadata checker changed during validation: $*' >&2; \
			exit 1; \
		fi; \
		mkdir -p '$(@D)'; \
		temporary="$$stamp.tmp.$$$$"; \
		trap 'rm -f -- "$$temporary"' 0 1 2 15; \
		printf 'schema=1\nprovider=%s\ndocument=%s\npdf_sha256=%s\nvalidator_sha256=%s\n' \
			'$(PROVIDER)' '$*' "$$pdf_hash" "$$validator_hash" > "$$temporary"; \
		mv -f -- "$$temporary" "$$stamp"; \
		trap - 0 1 2 15

FORCE_METADATA_VERIFICATION:

$(BUILD_ROOT)/.metadata/%.verify: $(BUILD_ROOT)/.metadata/%.ok FORCE_METADATA_VERIFICATION | $(BUILD_ROOT)/.metadata/%.source-check
	@set -eu; \
		pdf='$(BUILD_ROOT)/$*.pdf'; \
		stamp='$<'; \
		pdf_line=$$($(SHA256) -- "$$pdf"); \
		pdf_hash=$${pdf_line%% *}; \
		validator_line=$$($(SHA256) -- '$(METADATA_CHECKER_IMPL)'); \
		validator_hash=$${validator_line%% *}; \
		expected=$$(printf 'schema=1\nprovider=%s\ndocument=%s\npdf_sha256=%s\nvalidator_sha256=%s' \
			'$(PROVIDER)' '$*' "$$pdf_hash" "$$validator_hash"); \
		actual=$$(cat "$$stamp"); \
		if [ "$$actual" = "$$expected" ]; then \
			exit 0; \
		fi; \
		stamp_schema=; \
		IFS= read -r stamp_schema < "$$stamp" || :; \
		if [ "$$stamp_schema" = 'schema=1' ]; then \
			echo 'Validation stamp does not match current PDF/checker: $*' >&2; \
			exit 1; \
		fi; \
		$(METADATA_CHECKER) --provider '$(PROVIDER)' --pdf '$*' "$$pdf"; \
		pdf_after_line=$$($(SHA256) -- "$$pdf"); \
		pdf_after_hash=$${pdf_after_line%% *}; \
		validator_after_line=$$($(SHA256) -- '$(METADATA_CHECKER_IMPL)'); \
		validator_after_hash=$${validator_after_line%% *}; \
		if [ "$$pdf_hash" != "$$pdf_after_hash" ] || [ "$$validator_hash" != "$$validator_after_hash" ]; then \
			echo 'PDF or metadata checker changed during validation: $*' >&2; \
			exit 1; \
		fi; \
		temporary="$$stamp.tmp.$$$$"; \
		trap 'rm -f -- "$$temporary"' 0 1 2 15; \
		printf 'schema=1\nprovider=%s\ndocument=%s\npdf_sha256=%s\nvalidator_sha256=%s\n' \
			'$(PROVIDER)' '$*' "$$pdf_hash" "$$validator_hash" > "$$temporary"; \
		mv -f -- "$$temporary" "$$stamp"; \
		trap - 0 1 2 15

$(ECCLESIASTICAL_LATIN_BUILD_PDFS): \
	$(ECCLESIASTICAL_LATIN_SHARED) \
	$(CURRICULUM_STRUCTURE_CHECKER_IMPL) | check-curriculum-sources
$(ALTAR_SERVER_GUIDES_BUILD_PDFS): $(ALTAR_SERVER_GUIDES_SHARED)
.PHONY: generate-roman-sanctuary-dictionary
generate-roman-sanctuary-dictionary:
	@$(PYTHON) $(ROMAN_SANCTUARY_DICTIONARY_GENERATOR) \
		--schema '$(ROMAN_SANCTUARY_DICTIONARY_ROOT)/shared/schema/inventory-schema.toml' \
		--selections '$(ROMAN_SANCTUARY_DICTIONARY_ROOT)/shared/schema/edition-selections.toml' \
		--artwork-manifest '$(ROMAN_SANCTUARY_DICTIONARY_ROOT)/research/artwork-manifest.toml' \
		--records '$(ROMAN_SANCTUARY_DICTIONARY_ROOT)/shared/objects' \
		--output '$(ROMAN_SANCTUARY_DICTIONARY_GENERATED)'

$(ROMAN_SANCTUARY_DICTIONARY_BUILD_PDFS): \
	$(ROMAN_SANCTUARY_DICTIONARY_SHARED) generate-roman-sanctuary-dictionary
# A 1962 proper is published as a study edition at the bare leaf id and a
# full-text edition at the same id with a -full-text suffix. The full-text leaf
# owns only its own main.tex, format.tex, generation metadata and appointed-text
# sheet; every other section and the shared format come from the study leaf by
# \input. REGISTER_DOCUMENT_SOURCES sees only the files inside one leaf, so the
# cross-leaf import is declared here: editing a study-edition section must
# rebuild both PDFs.
define REGISTER_ROMAN_1962_FULL_TEXT_SOURCES
$(BUILD_ROOT)/$(1).pdf: $(shell find $(SOURCE_ROOT)/$(patsubst %-full-text,%,$(1)) -type f \( \
	-name '*.tex' -o -name '*.sty' -o -name '*.cls' -o -name '*.bib' -o \
	-name '*.bst' -o -name '*.png' -o -name '*.jpg' -o -name '*.jpeg' -o \
	-name '*.pdf' -o -name '*.eps' \) 2>/dev/null | sort)
endef
$(foreach document,$(ROMAN_1962_FULL_TEXT_DOCUMENTS),\
	$(eval $(call REGISTER_ROMAN_1962_FULL_TEXT_SOURCES,$(document))))
$(BUILD_ROOT)/theology/sacraments-at-a-glance.pdf: $(SACRAMENT_SHARED) $(SACRAMENT_INITIATION_TABLE)
$(BUILD_ROOT)/liturgy/roman-rite/1962/propers/ritual/m01-nuptial-mass.pdf: \
	$(SACRAMENT_ROOT)/summary-preamble.tex \
	$(SACRAMENT_ROOT)/summaries/matrimony.tex
$(POSTCONCILIAR_US_BUILD_PDFS): $(POSTCONCILIAR_US_FORMAT) $(POSTCONCILIAR_US_REGISTRY)
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s26-most-holy-trinity-year-a.pdf: \
	$(POSTCONCILIAR_US_ROOT)/temporal/shared/formularies/pc-s26-most-holy-trinity/propers/verified.md
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s27-most-holy-body-and-blood-of-christ-year-a.pdf: \
	$(POSTCONCILIAR_US_ROOT)/temporal/shared/formularies/pc-s27-most-holy-body-and-blood-of-christ/propers/verified.md
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s37-eleventh-sunday-in-ordinary-time-year-a.pdf: \
	$(POSTCONCILIAR_US_ROOT)/temporal/shared/ordinary-time/weeks/11/propers/verified.md
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s38-twelfth-sunday-in-ordinary-time-year-a.pdf: \
	$(POSTCONCILIAR_US_ROOT)/temporal/shared/ordinary-time/weeks/12/propers/verified.md
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s39-thirteenth-sunday-in-ordinary-time-year-a.pdf: \
	$(POSTCONCILIAR_US_ROOT)/temporal/shared/ordinary-time/weeks/13/propers/verified.md
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s40-fourteenth-sunday-in-ordinary-time-year-a.pdf: \
	$(POSTCONCILIAR_US_ROOT)/temporal/shared/ordinary-time/weeks/14/propers/verified.md
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s41-fifteenth-sunday-in-ordinary-time-year-a.pdf: \
	$(POSTCONCILIAR_US_ROOT)/temporal/shared/ordinary-time/weeks/15/propers/verified.md
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s42-sixteenth-sunday-in-ordinary-time-year-a.pdf: \
	$(POSTCONCILIAR_US_ROOT)/temporal/shared/ordinary-time/weeks/16/propers/verified.md
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s43-seventeenth-sunday-in-ordinary-time-year-a.pdf \
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s43-seventeenth-sunday-in-ordinary-time-year-a-synthesis.pdf: \
	$(POSTCONCILIAR_US_ROOT)/temporal/shared/ordinary-time/weeks/17/propers/verified.md
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s44-eighteenth-sunday-in-ordinary-time-year-a.pdf \
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s44-eighteenth-sunday-in-ordinary-time-year-a-synthesis.pdf \
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s44-eighteenth-sunday-in-ordinary-time-year-b.pdf \
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s44-eighteenth-sunday-in-ordinary-time-year-b-synthesis.pdf \
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s44-eighteenth-sunday-in-ordinary-time-year-c.pdf \
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s44-eighteenth-sunday-in-ordinary-time-year-c-synthesis.pdf: \
	$(POSTCONCILIAR_US_ROOT)/temporal/shared/ordinary-time/weeks/18/propers/verified.md
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s51-twenty-fifth-sunday-in-ordinary-time-year-a.pdf \
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s51-twenty-fifth-sunday-in-ordinary-time-year-a-synthesis.pdf \
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s51-twenty-fifth-sunday-in-ordinary-time-year-a-homily.pdf: \
	$(POSTCONCILIAR_US_ROOT)/temporal/shared/ordinary-time/weeks/25/propers/verified.md
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s52-twenty-sixth-sunday-in-ordinary-time-year-a.pdf \
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s52-twenty-sixth-sunday-in-ordinary-time-year-a-synthesis.pdf \
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s52-twenty-sixth-sunday-in-ordinary-time-year-a-homily.pdf: \
	$(POSTCONCILIAR_US_ROOT)/temporal/shared/ordinary-time/weeks/26/propers/verified.md
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s53-twenty-seventh-sunday-in-ordinary-time-year-a.pdf \
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s53-twenty-seventh-sunday-in-ordinary-time-year-a-synthesis.pdf \
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s53-twenty-seventh-sunday-in-ordinary-time-year-a-homily.pdf: \
	$(POSTCONCILIAR_US_ROOT)/temporal/shared/ordinary-time/weeks/27/propers/verified.md
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s54-twenty-eighth-sunday-in-ordinary-time-year-a.pdf \
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s54-twenty-eighth-sunday-in-ordinary-time-year-a-synthesis.pdf \
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s54-twenty-eighth-sunday-in-ordinary-time-year-a-homily.pdf: \
	$(POSTCONCILIAR_US_ROOT)/temporal/shared/ordinary-time/weeks/28/propers/verified.md
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s55-twenty-ninth-sunday-in-ordinary-time-year-a.pdf \
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s55-twenty-ninth-sunday-in-ordinary-time-year-a-synthesis.pdf \
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s55-twenty-ninth-sunday-in-ordinary-time-year-a-homily.pdf: \
	$(POSTCONCILIAR_US_ROOT)/temporal/shared/ordinary-time/weeks/29/propers/verified.md
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s58-thirty-second-sunday-in-ordinary-time-year-a.pdf \
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s58-thirty-second-sunday-in-ordinary-time-year-a-synthesis.pdf \
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s58-thirty-second-sunday-in-ordinary-time-year-a-homily.pdf: \
	$(POSTCONCILIAR_US_ROOT)/temporal/shared/ordinary-time/weeks/32/propers/verified.md
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/general-calendar/pc-r07-all-saints-abc.pdf \
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/general-calendar/pc-r07-all-saints-abc-synthesis.pdf \
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/general-calendar/pc-r07-all-saints-abc-homily.pdf: \
	$(POSTCONCILIAR_US_ROOT)/general-calendar/shared/formularies/pc-r07-all-saints/propers/verified.md
$(NOVENA_BUILD_PDFS): $(NOVENA_SHARED)
$(BIOGRAPHY_BUILD_PDFS): $(BIOGRAPHY_SHARED)
$(HISTORICAL_TRANSLATION_BUILD_PDFS): $(HISTORICAL_TRANSLATION_SHARED)
# A history outside that collection imports its account format across leaves,
# so REGISTER_DOCUMENT_SOURCES --- which sees only one leaf --- never named it.
# Found by the recorder check in PDFLATEX_TO_FIXED_POINT, which is what that
# check is for.
$(BUILD_ROOT)/history/catholic-exorcism/01-history-and-current-practice.pdf: \
	$(HISTORICAL_TRANSLATION_SHARED)
$(PARISH_HISTORY_BUILD_PDFS): $(PARISH_HISTORY_SHARED)
$(TRADITIONAL_INSTITUTE_BUILD_PDFS): $(TRADITIONAL_INSTITUTE_SHARED)
$(BUILD_ROOT)/theology/mariology/angelus.pdf: \
	$(MARIOLOGY_PRAYER_FORMAT) \
	$(ANGELUS_HAIL_MARY)
$(BUILD_ROOT)/theology/mariology/regina-coeli.pdf: $(MARIOLOGY_PRAYER_FORMAT)
$(BUILD_ROOT)/devotions/novenas/00-ascension-to-pentecost-daily-prayer.pdf: \
	$(FIRST_NOVENA_PRAYERS) \
	$(FIRST_NOVENA_ROOT)/generation-metadata.tex
$(BUILD_ROOT)/devotions/novenas/10-our-lady-of-mount-carmel-daily-prayer.pdf: \
	$(CARMEL_NOVENA_PRAYERS) \
	$(CARMEL_NOVENA_ROOT)/generation-metadata.tex

# Complete-text bible editions.
#
# Which editions exist is asked of `typeset-bible list`, which reads the
# publishable flag from the registered edition table, and never of a directory
# listing: the source library also holds a licensed edition that must not be
# typeset. A rendered edition is a reproducible artifact and stays in build/.
bibles:
	@set -eu; \
		editions=$$($(PYTHON) $(BIBLE_TYPESET_TOOL) list --format ids); \
		[ -n "$$editions" ] || { echo 'No publishable bible edition is registered' >&2; exit 1; }; \
		for edition in $$editions; do \
			$(MAKE) --no-print-directory '$(BIBLE_BUILD_ROOT)/'"$$edition"'.pdf'; \
		done

bible:
	@if [ -z '$(BIBLE)' ]; then \
		echo 'bible requires BIBLE=<edition id from `tools/tpt typeset-bible list`>' >&2; \
		exit 1; \
	fi
	@$(MAKE) --no-print-directory '$(BIBLE_BUILD_ROOT)/$(BIBLE).pdf'

review-bible: bible
	@$(PYTHON) $(PDF_REVIEW_TOOL) '$(BIBLE_BUILD_ROOT)/$(BIBLE).pdf'

check-bibles: check-plan-sources
	@$(PYTHON) $(BIBLE_TYPESET_TOOL) check
	@$(PYTHON) $(BIBLE_TYPESET_TOOL) check --plan '$(PLAN)'

FORCE_BIBLE_RENDER:

# Keep the rendered TeX: it is the compiler's input and the diffable record of
# what was set, and Make would otherwise delete it as a chained intermediate
# and recompile the whole edition on the next run.
.PRECIOUS: $(BIBLE_BUILD_ROOT)/%.tex

# The render is deterministic and rewrites the TeX only when its bytes change,
# so asking every time cannot recompile an unchanged thousand-page edition.
$(BIBLE_BUILD_ROOT)/%.tex: $(BIBLE_TYPESET_IMPL) FORCE_BIBLE_RENDER
	@$(PYTHON) $(BIBLE_TYPESET_TOOL) render --bible '$*' --out '$(BIBLE_BUILD_ROOT)'

# Two passes: the list of books carries the page each book begins on.
$(BIBLE_BUILD_ROOT)/%.pdf: $(BIBLE_BUILD_ROOT)/%.tex | check-tools
	$(PDFLATEX) -no-shell-escape -interaction=nonstopmode -halt-on-error \
		-output-directory='$(BIBLE_BUILD_ROOT)' '$<'
	$(PDFLATEX) -no-shell-escape -interaction=nonstopmode -halt-on-error \
		-output-directory='$(BIBLE_BUILD_ROOT)' '$<'
	@if grep -q 'undefined references' '$(BIBLE_BUILD_ROOT)/$*.log'; then \
		echo 'Undefined references remain after two passes: $*' >&2; \
		exit 1; \
	fi

# Tracks of the abridged plan.
#
# Six volumes today: three tiers in two editions. Which they are is asked of
# `typeset-bible list --plan`, which reads the tiers from the plan file and the
# editions from the registered edition table, so neither the count nor the
# publishable flag is restated here.
#
# A track carries this project's plan — its periods, its titles, its notes and
# its account of what it leaves out — around the source library's text, so the
# plan file is validated before a verse of it is set. Like a whole bible, a
# set track stays in build/; readers get the plan's print route instead.
tracks: check-plan-sources
	@set -eu; \
		volumes=$$($(PYTHON) $(BIBLE_TYPESET_TOOL) list --plan '$(PLAN)' --format ids); \
		[ -n "$$volumes" ] || { echo 'No track is declared for plan $(PLAN)' >&2; exit 1; }; \
		for volume in $$volumes; do \
			$(MAKE) --no-print-directory '$(READING_BUILD_ROOT)/'"$$volume"'.pdf'; \
		done

track:
	@if [ -z '$(VOLUME)' ]; then \
		echo 'track requires VOLUME=<id from `tools/tpt typeset-bible list --plan $(PLAN) --format ids`>' >&2; \
		exit 1; \
	fi
	@$(MAKE) --no-print-directory '$(READING_BUILD_ROOT)/$(VOLUME).pdf'

review-track: track
	@$(PYTHON) $(PDF_REVIEW_TOOL) '$(READING_BUILD_ROOT)/$(VOLUME).pdf'

# `check-tracks` is retired. It rebuilt every track into pdf/reading-plans and
# required each to hash to a `"pdf/reading-plans/<volume>.pdf":` binding in
# release/public-alpha.json. Six such bindings existed at 2f23107c10 and none
# remain: tracks are no longer published as files, so no current record binds
# their bytes and the gate could only fail. The archived bytes of the last
# published volumes are historical-publication rows of
# src/sources/artifact-delivery.json; reproducing them would only prove the
# plan never changed. Its other question, whether every volume still resolves
# against its edition, is asked by `check-bibles`.

# The plan file is validated by the tool that owns it before a single verse of
# it is set. A track built from a plan that does not validate would be a
# publication of unchecked references.
check-plan-sources:
	@$(PYTHON) $(READING_PLAN_TOOL) check

# Producer diagnostics write an unsealed working tree. Only browser-products
# record may update the two-build descriptor; prepare-browser-data reproduces it.
reading-structure:
	@$(PYTHON) $(READING_PLAN_TOOL) structure

# The catalogue's unsealed working projection, derived from canonical sources.
document-catalogue:
	@$(PYTHON) $(DOCUMENT_LIBRARY_TOOL) structure

# The reading projection of the source library, rewritten from the work,
# edition, artifact, segment and passage records into the unsealed working tree.
source-projection:
	@$(PYTHON) $(SOURCE_READER_TOOL) structure

# The catalogue of every encyclical, rewritten from the tracked index and
# checked reader by reader against release/papal-documents.json, into the
# unsealed working tree. INDEX=<path> reads another index, for a trial run.
encyclicals-catalogue:
	@$(PYTHON) scripts/_encyclicals.py structure $(if $(INDEX),--index '$(INDEX)',)

$(READING_BUILD_ROOT)/%.tex: $(BIBLE_TYPESET_IMPL) FORCE_BIBLE_RENDER
	@$(PYTHON) $(BIBLE_TYPESET_TOOL) render --volume '$*' --out '$(READING_BUILD_ROOT)'

# Both are kept: the TeX is the compiler's input and the diffable record of
# what was set, and the built PDF is what `review-track` rasters. Make would
# otherwise delete each as a chained intermediate and recompile the volume.
.PRECIOUS: $(READING_BUILD_ROOT)/%.tex $(READING_BUILD_ROOT)/%.pdf

# The list of readings carries the page each reading begins on, and a list
# twenty pages long moves the pages it is naming, so two passes do not always
# settle a track of three hundred pages. Run until LaTeX stops asking, and fail
# rather than keep a volume whose contents point at the wrong pages.
$(READING_BUILD_ROOT)/%.pdf: $(READING_BUILD_ROOT)/%.tex | check-tools
	@set -eu; \
		log='$(READING_BUILD_ROOT)/$*.log'; \
		pass=0; \
		while [ "$$pass" -lt 5 ]; do \
			pass=$$((pass + 1)); \
			$(PDFLATEX) -no-shell-escape -interaction=nonstopmode -halt-on-error \
				-output-directory='$(READING_BUILD_ROOT)' '$<' >/dev/null; \
			if ! grep -q 'Rerun to get cross-references right' "$$log" \
				&& ! grep -q 'undefined references' "$$log" \
				&& [ "$$pass" -ge 2 ]; then \
				echo "set $* in $$pass passes"; \
				exit 0; \
			fi; \
		done; \
		echo "References did not settle in $$pass passes: $*" >&2; \
		exit 1

check-tools:
	@command -v $(PDFLATEX) >/dev/null || { echo "Missing $(PDFLATEX)"; exit 1; }
	@command -v $(PYTHON) >/dev/null || { echo "Missing $(PYTHON)"; exit 1; }
	@command -v pdftotext >/dev/null || { echo "Missing pdftotext"; exit 1; }
	@command -v pdfinfo >/dev/null || { echo "Missing pdfinfo"; exit 1; }
	@command -v $(SHA256) >/dev/null || { echo "Missing $(SHA256)"; exit 1; }
	@command -v $(INSTALL) >/dev/null || { echo "Missing $(INSTALL)"; exit 1; }

clean:
	rm -rf build

distclean: clean

PAPAL_OUT ?= .scratch/papal-pdfs
PAPAL_JOBS ?= 4
PAPAL_MANIFEST_ROOT ?= src/sources/papal-documents
PAPAL_HISTORICAL_SERIES := bullarium-continuatio benedict-xiv-bullarium gregory-xvi-acta pius-ix-acta
PAPAL_ENGLISH_ADDITIONS := historical-english-supplement historical-english-journal historical-english-book historical-english-completion
PAPAL_BASE_MANIFESTS ?= latin=typeset-manifest.json \
	english=historical-english-manifest.json \
	quanta-syllabus=quanta-syllabus-manifest.json \
	bullarium=bullarium-manifest.json \
	bullarium-fragments=bullarium-fragment-manifest.json \
	acta=acta-manifest.json \
	$(foreach series,$(PAPAL_ENGLISH_ADDITIONS),$(if $(wildcard $(PAPAL_MANIFEST_ROOT)/$(series)-manifest.json),$(series)=$(series)-manifest.json)) \
	$(foreach series,$(PAPAL_ENGLISH_ADDITIONS),$(if $(wildcard $(PAPAL_MANIFEST_ROOT)/$(series)-fragment-manifest.json),$(series)-fragments=$(series)-fragment-manifest.json)) \
	$(if $(wildcard $(PAPAL_MANIFEST_ROOT)/bullarium-rescue-manifest.json),bullarium-rescue=bullarium-rescue-manifest.json) \
	$(if $(wildcard $(PAPAL_MANIFEST_ROOT)/bullarium-rescue-fragment-manifest.json),bullarium-rescue-fragments=bullarium-rescue-fragment-manifest.json) \
	$(if $(wildcard $(PAPAL_MANIFEST_ROOT)/bullarium-geometry-manifest.json),bullarium-geometry=bullarium-geometry-manifest.json) \
	$(if $(wildcard $(PAPAL_MANIFEST_ROOT)/bullarium-geometry-fragment-manifest.json),bullarium-geometry-fragments=bullarium-geometry-fragment-manifest.json) \
	$(foreach series,$(PAPAL_HISTORICAL_SERIES),$(if $(wildcard $(PAPAL_MANIFEST_ROOT)/$(series)-manifest.json),$(series)=$(series)-manifest.json)) \
	$(foreach series,$(PAPAL_HISTORICAL_SERIES),$(if $(wildcard $(PAPAL_MANIFEST_ROOT)/$(series)-fragment-manifest.json),$(series)-fragments=$(series)-fragment-manifest.json))
PAPAL_CORRECTION_MANIFESTS ?= \
	$(if $(wildcard $(PAPAL_MANIFEST_ROOT)/historical-english-corrections-manifest.json),historical-english-corrections=historical-english-corrections-manifest.json) \
	$(if $(wildcard $(PAPAL_MANIFEST_ROOT)/vatican-corrections-manifest.json),vatican-corrections=vatican-corrections-manifest.json) \
	$(if $(wildcard $(PAPAL_MANIFEST_ROOT)/bullarium-corrections-manifest.json),bullarium-corrections=bullarium-corrections-manifest.json) \
	$(if $(wildcard $(PAPAL_MANIFEST_ROOT)/acta-title-corrections-manifest.json),acta-title-corrections=acta-title-corrections-manifest.json) \
	$(if $(wildcard $(PAPAL_MANIFEST_ROOT)/acta-layout-corrections-manifest.json),acta-layout-corrections=acta-layout-corrections-manifest.json) \
	$(if $(wildcard $(PAPAL_MANIFEST_ROOT)/acta-visual-corrections-manifest.json),acta-visual-corrections=acta-visual-corrections-manifest.json) \
	$(if $(wildcard $(PAPAL_MANIFEST_ROOT)/historical-series-corrections-manifest.json),historical-series-corrections=historical-series-corrections-manifest.json) \
	$(if $(wildcard $(PAPAL_MANIFEST_ROOT)/bullarium-reading-order-corrections-manifest.json),bullarium-reading-order-corrections=bullarium-reading-order-corrections-manifest.json) \
	$(if $(wildcard $(PAPAL_MANIFEST_ROOT)/bullarium-reading-order-withdrawals-manifest.json),bullarium-reading-order-withdrawals=bullarium-reading-order-withdrawals-manifest.json) \
	$(if $(wildcard $(PAPAL_MANIFEST_ROOT)/bullarium-active-withdrawals.json),bullarium-active-withdrawals=bullarium-active-withdrawals.json) \
	$(if $(wildcard $(PAPAL_MANIFEST_ROOT)/encyclicals-classic-manifest.json),encyclicals-classic=encyclicals-classic-manifest.json) \
	$(if $(wildcard $(PAPAL_MANIFEST_ROOT)/encyclicals-source-corrections-manifest.json),encyclicals-source-corrections=encyclicals-source-corrections-manifest.json)
PAPAL_CURRENT_MANIFEST ?= $(PAPAL_OUT)/current-manifest.json
PAPAL_CURRENT_BATCH ?= $(PAPAL_OUT)/current
PAPAL_COLLECTION_OUT ?= $(PAPAL_OUT)/collection
PAPAL_REVIEW_MANIFESTS ?= $(wildcard $(PAPAL_MANIFEST_ROOT)/*-visual-review.json)
# The typesetter refuses an empty selection. Validate the outer contract first
# so an honestly empty batch is skipped while malformed JSON still fails.
PAPAL_MANIFEST_COUNT = $(PYTHON) -c 'import datetime,json,re,sys; \
	d=json.load(open(sys.argv[1],encoding="utf-8"),object_pairs_hook=lambda p: dict(p) if len(dict(p)) == len(p) else sys.exit("duplicate JSON key"),parse_constant=lambda s: sys.exit("non-finite JSON number")); \
	(isinstance(d,dict) and d.get("schema") == "triptych-papal-typeset/v1") or sys.exit("invalid papal manifest schema"); \
	r=d.get("revision"); \
	(isinstance(r,str) and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z",r)) or sys.exit("invalid papal manifest revision"); \
	datetime.datetime.strptime(r,"%Y-%m-%dT%H:%M:%SZ"); \
	isinstance(d.get("documents"),list) or sys.exit("papal manifest requires a documents array"); \
	print(len(d["documents"]))'

.PHONY: check-papal check-papal-manifests papal-plan papal-catalog papal-pdfs papal-collection

check-papal: check-papal-manifests
	@$(PYTHON) tools/tpt papal-documents check --json
	@$(PYTHON) tools/tpt bullarium check --json
	@$(PYTHON) tools/tpt papal-acta check --json
	@$(PYTHON) -m unittest discover -s tools/tests -p 'test_papal_*.py'
	@$(PYTHON) -m unittest discover -s tools/tests -p 'test_bullarium*.py'
	@$(PYTHON) -m unittest discover -s tools/tests -p 'test_typeset_papal.py'

papal-plan:
	@set -eu; \
	set --; \
	for batch in $(PAPAL_BASE_MANIFESTS); do \
		name=$${batch%%=*}; \
		manifest='$(PAPAL_MANIFEST_ROOT)'/$${batch#*=}; \
		count=$$($(PAPAL_MANIFEST_COUNT) "$$manifest"); \
		if [ "$$count" -eq 0 ]; then printf '%s: 0 admitted editions; no readers selected\n' "$$name"; fi; \
		set -- "$$@" --base "$$name" "$$manifest"; \
	done; \
	for batch in $(PAPAL_CORRECTION_MANIFESTS); do \
		name=$${batch%%=*}; \
		manifest='$(PAPAL_MANIFEST_ROOT)'/$${batch#*=}; \
		count=$$($(PAPAL_MANIFEST_COUNT) "$$manifest"); \
		if [ "$$count" -eq 0 ]; then printf '%s: no replacement readers; source-selection directives still apply\n' "$$name"; fi; \
		set -- "$$@" --correction "$$name" "$$manifest"; \
	done; \
	$(PYTHON) tools/tpt typeset-papal plan "$$@" --out '$(PAPAL_CURRENT_MANIFEST)' --json

check-papal-manifests: papal-plan
	@set -eu; count=$$($(PAPAL_MANIFEST_COUNT) '$(PAPAL_CURRENT_MANIFEST)'); \
	if [ "$$count" -eq 0 ]; then \
		printf '%s\n' 'current: 0 admitted editions; skipped'; \
	else \
		$(PYTHON) tools/tpt typeset-papal check --manifest '$(PAPAL_CURRENT_MANIFEST)' --json; \
	fi

papal-catalog:
	@$(PYTHON) tools/tpt papal-documents export --format json --out '$(PAPAL_OUT)/catalog.json'
	@$(PYTHON) tools/tpt papal-documents export --format csv --out '$(PAPAL_OUT)/catalog.csv'
	@$(PYTHON) tools/tpt papal-documents export --format biblatex --out '$(PAPAL_OUT)/papal.bib'
	@cp -- '$(PAPAL_MANIFEST_ROOT)/archives.json' '$(PAPAL_OUT)/archives.json'
	@cp -- '$(PAPAL_MANIFEST_ROOT)/bullarium-catalog.json' '$(PAPAL_OUT)/bullarium-catalog.json'
	@cp -- '$(PAPAL_MANIFEST_ROOT)/acta-catalog.json' '$(PAPAL_OUT)/acta-catalog.json'
	@set -eu; for series in $(PAPAL_HISTORICAL_SERIES); do \
		catalog='$(PAPAL_MANIFEST_ROOT)'/"$$series"-catalog.json; \
		if [ -f "$$catalog" ]; then \
			cp -- "$$catalog" '$(PAPAL_OUT)'/"$$series"-catalog.json; \
		fi; \
	done

papal-pdfs: check-papal-manifests papal-catalog
	@set -eu; count=$$($(PAPAL_MANIFEST_COUNT) '$(PAPAL_CURRENT_MANIFEST)'); \
	if [ "$$count" -eq 0 ]; then \
		printf '%s\n' 'current: no readers selected; no PDFs rendered'; \
	else \
		$(PYTHON) tools/tpt typeset-papal render --manifest '$(PAPAL_CURRENT_MANIFEST)' \
			--out '$(PAPAL_CURRENT_BATCH)' --compile --jobs '$(PAPAL_JOBS)' --json; \
	fi
	@$(MAKE) --no-print-directory papal-collection

# Collection reads existing outputs only; it never starts a render or installs PDFs.
papal-collection: papal-plan
	@set -eu; count=$$($(PAPAL_MANIFEST_COUNT) '$(PAPAL_CURRENT_MANIFEST)'); \
	if [ "$$count" -eq 0 ]; then \
		$(PYTHON) tools/tpt typeset-papal collect --empty-plan '$(PAPAL_CURRENT_MANIFEST)' --out '$(PAPAL_COLLECTION_OUT)' --json; \
		exit 0; \
	fi; \
	set -- --batch current '$(PAPAL_CURRENT_BATCH)/receipt.json' '$(PAPAL_CURRENT_MANIFEST)'; \
	for manifest in $(PAPAL_REVIEW_MANIFESTS); do \
		set -- "$$@" --review "$$manifest"; \
	done; \
	$(PYTHON) tools/tpt typeset-papal collect "$$@" --out '$(PAPAL_COLLECTION_OUT)' --json

