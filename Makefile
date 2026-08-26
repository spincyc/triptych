PDFLATEX ?= pdflatex
PYTHON ?= python3
PROVIDER ?= gpt
PDF_JOBS ?= 4
SHA256 ?= sha256sum
INSTALL ?= install

# Arch Linux dependency manifest (the only supported local host for now).
# Keep direct owner packages explicit even when pacman currently installs one
# through another package. This makes the project/tool boundary reviewable and
# prevents a future dependency-graph change from silently removing a tool.
#
#   make, /bin/sh, /usr/bin/env, find, sort, cmp, id and core utilities
#   (cat, install, mkdir, mv, rm and sha256sum):
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
#   LaTeX-to-Markdown conversion for the tracked web editions:
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
	texlive-fontsrecommended texlive-fontsextra
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
ARCH_CANONICAL_COMMANDS := make:/usr/bin/make sh:/usr/bin/sh \
	env:/usr/bin/env id:/usr/bin/id find:/usr/bin/find sort:/usr/bin/sort \
	cmp:/usr/bin/cmp \
	cat:/usr/bin/cat chmod:/usr/bin/chmod cp:/usr/bin/cp install:/usr/bin/install \
	mkdir:/usr/bin/mkdir mv:/usr/bin/mv rm:/usr/bin/rm \
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
PDF_ROOT := pdf/$(PROVIDER)
WEB_BUILD_ROOT := build/web/$(PROVIDER)
WEB_ROOT := web/$(PROVIDER)
# The drift gate compares every provider's tracked tree, not only $(PROVIDER).
WEB_CURRENT_ROOT := build/.web-current
ALL_MAIN_SOURCES := $(shell find src -mindepth 2 -type f -name main.tex 2>/dev/null | sort)
PROVIDERS := $(sort $(foreach path,$(ALL_MAIN_SOURCES),$(word 2,$(subst /, ,$(path)))))

MAIN_SOURCES := $(shell find $(SOURCE_ROOT) -type f -name main.tex 2>/dev/null | sort)
CANONICAL_DOCUMENTS := $(patsubst $(SOURCE_ROOT)/%/main.tex,%,$(MAIN_SOURCES))
PROPER_SYNTHESIS_DOCUMENTS := $(shell \
	$(PYTHON) tools/tpt check-proper-components --provider $(PROVIDER) \
		--list-synthesis 2>/dev/null)
DOCUMENTS := $(CANONICAL_DOCUMENTS) $(PROPER_SYNTHESIS_DOCUMENTS)
BUILD_PDFS := $(addprefix $(BUILD_ROOT)/,$(addsuffix .pdf,$(DOCUMENTS)))
BUILD_METADATA_STAMPS := $(addprefix $(BUILD_ROOT)/.metadata/,$(addsuffix .ok,$(DOCUMENTS)))
BUILD_METADATA_VERIFICATIONS := $(addprefix $(BUILD_ROOT)/.metadata/,$(addsuffix .verify,$(DOCUMENTS)))
INSTALLED_PDFS := $(addprefix $(PDF_ROOT)/,$(addsuffix .pdf,$(DOCUMENTS)))
METADATA_CHECKER := tools/tpt check-generation-metadata
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
# Complete-text bible editions. These are build artifacts, not publications:
# they are generated from the tracked verse text of the source library and are
# never installed into pdf/.
BIBLE_TYPESET_TOOL := tools/tpt typeset-bible
BIBLE_TYPESET_IMPL := tools/typeset-bible
BIBLE_BUILD_ROOT := build/bibles
# Tracks of a tracked abridged plan: one tier of the plan in one edition, set
# from the same verse text and the same typesetter as a whole bible. Unlike a
# whole bible these are installed, because a track carries the plan's own
# periods, titles and notes and is a publication of this project.
READING_PLAN_TOOL := tools/tpt reading-plan
READING_BUILD_ROOT := build/reading-plans
READING_PDF_ROOT := pdf/reading-plans
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

.PHONY: all pdf review-pdfs review-all-pdfs install list help clean \
	distclean check-tools check-tool-registry check-calendar-masses \
	check-propers-census \
	check-metadata check-web-editions \
	check-proper-components \
	web-editions install-web-editions check-web-editions-current \
	check-sources check-deployment-sources check-source-library \
	check-source-inventory check-source-inventory-tool \
	check-source-family-migration check-source-family-migration-tool \
	check-source-family-screening \
	check-promised-deliverables \
	check-public-alpha prepare-public-alpha \
	check-pdf-review check-curriculum-sources \
	check-curriculum-structure check-source-reader source-projection \
	check-document-catalogue document-catalogue \
	public-site public-preview \
	dependencies-arch dependencies-arch-browser install-dependencies-arch \
	verify-public-site verify-public-preview \
	check-mass-ordinary check-scripture-chronology \
	check-release-bindings refresh-release-bindings approve-release \
	add-publication doc review-doc install-doc check check-tests \
	check-browser-static check-browser-gate check-browser-harnesses \
	check-examples recapture-examples \
	altar-server-guides review-altar-server-guides install-altar-server-guides \
	check-staleness measure-staleness explain-staleness rebaseline-doc \
	bibles bible review-bible check-bibles \
	tracks track review-track check-tracks check-plan-sources reading-structure \
	FORCE_METADATA_VERIFICATION FORCE_BIBLE_RENDER
.DELETE_ON_ERROR:
.SECONDARY: $(BUILD_METADATA_STAMPS)

ifeq ($(strip $(_TRIPTYCH_MAKE_PARALLEL_FLAGS)),)
all:
	+@$(MAKE) --no-print-directory $(_TRIPTYCH_BOUNDED_PDF_JOB_OPTION) pdf

review-pdfs:
	+@$(MAKE) --no-print-directory $(_TRIPTYCH_BOUNDED_PDF_JOB_OPTION) pdf
	@if [ -d '$(PDF_ROOT)' ]; then \
		$(PYTHON) $(PDF_REVIEW_TOOL) --changed-against $(PDF_ROOT) $(BUILD_PDFS); \
	else \
		$(PYTHON) $(PDF_REVIEW_TOOL) $(BUILD_PDFS); \
	fi

review-all-pdfs:
	+@$(MAKE) --no-print-directory $(_TRIPTYCH_BOUNDED_PDF_JOB_OPTION) pdf
	@$(PYTHON) $(PDF_REVIEW_TOOL) $(BUILD_PDFS)
else
all: pdf

review-pdfs: pdf
	@if [ -d '$(PDF_ROOT)' ]; then \
		$(PYTHON) $(PDF_REVIEW_TOOL) --changed-against $(PDF_ROOT) $(BUILD_PDFS); \
	else \
		$(PYTHON) $(PDF_REVIEW_TOOL) $(BUILD_PDFS); \
	fi

review-all-pdfs: pdf
	@$(PYTHON) $(PDF_REVIEW_TOOL) $(BUILD_PDFS)
endif

pdf: check-metadata $(BUILD_METADATA_VERIFICATIONS)

install: check-metadata $(INSTALLED_PDFS)
	@set -eu; \
	for document in $(DOCUMENTS); do \
		pdf='$(BUILD_ROOT)/'$$document.pdf; \
		stamp='$(BUILD_ROOT)/.metadata/'$$document.ok; \
		pdf_line=$$($(SHA256) -- "$$pdf"); \
		pdf_hash=$${pdf_line%% *}; \
		validator_line=$$($(SHA256) -- '$(METADATA_CHECKER_IMPL)'); \
		validator_hash=$${validator_line%% *}; \
		expected=$$(printf 'schema=1\nprovider=%s\ndocument=%s\npdf_sha256=%s\nvalidator_sha256=%s' \
			'$(PROVIDER)' "$$document" "$$pdf_hash" "$$validator_hash"); \
		actual=$$(cat "$$stamp"); \
		[ "$$actual" = "$$expected" ] || { echo "Validation stamp does not match current PDF/checker: $$document" >&2; exit 1; }; \
		cmp -s "$$pdf" "$(PDF_ROOT)/$$document.pdf" || { echo "Installed PDF differs from reviewed build: $$document"; exit 1; }; \
	done

list:
	@printf '%s\n' $(DOCUMENTS)

dependencies-arch:
	@printf '%s\n' $(ARCH_DEPENDENCY_PACKAGES)

# What `install-dependencies-arch` deliberately does not install. Named by its
# own target so that "which browser, and why is it not in the list" has one
# answer a reader can run, rather than a comment they have to find.
dependencies-arch-browser:
	@printf '%s\n' $(ARCH_BROWSER_PACKAGES)

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

check-deployment-sources:
	@$(PYTHON) $(SOURCE_LIBRARY_TOOL) validate
	@set -eu; for inventory in src/sources/inventories/*publications-v1.toml; do \
		[ -e "$$inventory" ] || continue; \
		case "$$inventory" in \
			*/claude-publications-v1.toml) \
				review=src/sources/inventories/claude-classification-review-v1.toml ;; \
			*) review=src/sources/inventories/classification-review-v1.toml ;; \
		esac; \
		$(PYTHON) $(SOURCE_INVENTORY_TOOL) check --review "$$review" "$$inventory"; \
	done

check-sources: check-deployment-sources
	@$(PYTHON) $(SOURCE_FAMILY_MIGRATION_TOOL) check

check-source-library:
	@$(PYTHON) -m unittest discover -s tools/tests -p 'test_source_library.py' -v

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
		'Every build, install, review, list, and metadata target honors PROVIDER=<p> (default gpt; claude is the peer branch)' \
		'make          Build every document with at most $(PDF_JOBS) parallel jobs' \
		'make pdf      Build incrementally in the current Make jobserver' \
		'make review-pdfs  Build with at most $(PDF_JOBS) jobs, then raster changed PDFs' \
		'make review-all-pdfs  Build with at most $(PDF_JOBS) jobs, then raster every PDF' \
		'make install  Publish built PDFs into the mirrored tracked pdf/ tree' \
		'make doc DOC=<id>  Build one document below src/$$PROVIDER/' \
		'make review-doc DOC=<id>  Build one document and raster it for page review' \
		'make install-doc DOC=<id>  Build, gate, and install one document' \
		'make altar-server-guides  Build the complete seven-publication altar-server series' \
		'make review-altar-server-guides  Build and raster all seven altar-server publications' \
		'make install-altar-server-guides  Review, validate, stage, and install the complete altar-server series' \
		'make list     List discovered document IDs' \
		'make dependencies-arch  List canonical Arch package dependencies' \
		'make install-dependencies-arch  Run a full Arch upgrade and install canonical packages' \
		'make dependencies-arch-browser  List the browser package the harnesses need and this installer omits' \
		'make check-pdf-review  Test memory-bounded PDF inspection tooling' \
		'make check-sources  Validate the source library, inventory, and migration ledger' \
		'make check-deployment-sources  Validate deployable sources and publication inventories' \
		'make check-source-library  Test reusable source-library tooling' \
		'make check-source-inventory  Replay the exhaustive legacy-source inventory' \
		'make check-source-inventory-tool  Test legacy-source inventory tooling' \
		'make check-source-family-migration  Check the reviewed family migration ledger' \
		'make check-source-family-migration-tool  Test family migration ledger tooling' \
		'make check-source-family-screening  Require every migration review unit to be screened' \
		'make check-curriculum-structure  Build and audit every Ecclesiastical Latin publication hierarchy' \
		'make check-metadata  Validate structured and inherited AI provenance' \
		'make check-web-editions  Validate per-leaf web-edition eligibility declarations' \
		'make web-editions  Generate Markdown for every eligible leaf of $$PROVIDER' \
		'make install-web-editions  Publish reviewed Markdown into the tracked web/ tree' \
		'make check-web-editions-current  Prove every tracked web edition matches current sources' \
		'make check-document-catalogue  Confirm each derived title against its PDF and the catalogue against the sources' \
		'make document-catalogue  Rewrite the browser catalogue of every document' \
		'make source-projection  Rewrite the browser reading of the source library' \
		'make check-source-reader  Prove no withheld source text is served, and no reading is stale' \
		'make check-public-alpha  Validate the exhaustive public-release policy' \
		'make prepare-public-alpha  Print current candidate hashes; grants no approval' \
		'make public-preview  Build a private no-index preview with review candidates' \
		'make public-site  Build the fail-closed, history-free public artifact' \
		'make verify-public-preview  Recheck the existing private preview artifact' \
		'make verify-public-site  Recheck the existing public artifact' \
		'make check-release-bindings  Report stale shared site and authorization-record bindings' \
		'make refresh-release-bindings [ADOPT=1] [ONLY="path ..."]  Refresh shared site-authorization inputs; ONLY restricts it to your own paths' \
		'make approve-release NOTE="..."  Record a dated supplement with the operator instruction, then refresh' \
		'make add-publication ID=<leaf> CATALOG=<page> [PROVIDER=<p>] [STATUS=hold]  Add an independent alpha record' \
		'make bibles   Typeset every publishable bible edition complete into build/bibles' \
		'make bible BIBLE=<edition>  Typeset one publishable edition complete' \
		'make review-bible BIBLE=<edition>  Typeset one edition and raster it for page review' \
		'make check-bibles  Prove every publishable edition can be set, writing nothing' \
		'make tracks [PLAN=<plan>]  Typeset and install every track of the abridged plan' \
		'make track VOLUME=<id>  Typeset and install one track' \
		'make review-track VOLUME=<id>  Typeset one track and raster it for page review' \
		'make check-tracks [PLAN=<plan>]  Prove every track can be set and is installed current' \
		'make reading-structure  Rewrite the browser structure of every abridged plan' \
		'make check    Run every repository policy check' \
		'make check-calendar-rubrics  Validate the rubrical precedence sources and their solved cases' \
		'make check-propers-census  Refuse a document whose derived count table has gone stale' \
		'make check-tests  Run the complete script unit-test suite' \
		'make check-staleness  Suspended 2026-07-31; reports the suspension and exits clean' \
		'make measure-staleness  Run the suspended signal anyway, without acting on it' \
		'make explain-staleness DOC=<leaf> [PROVIDER=<p>]  Name the changed research inputs' \
		'make rebaseline-doc DOC=<leaf> [PROVIDER=<p>]  Clear a staleness flag after re-evaluation' \
		'make clean    Remove transient build artifacts only'

check-metadata: check-tools
	@$(METADATA_CHECKER) --provider $(PROVIDER)

check-promised-deliverables:
	@$(PYTHON) tools/tpt check-promised-deliverables

# Absence of a leaf's declaration is an error: nothing defaults to eligible.
check-web-editions:
	@$(PYTHON) $(WEB_EDITION_CHECKER) --provider $(PROVIDER)

check-proper-components:
	@$(PYTHON) $(PROPER_COMPONENT_CHECKER) --provider $(PROVIDER)

# Two claims, and the second is the one worth having. `check` re-derives every
# document's title out of its own preamble and holds it against the title the
# built PDF actually carries, because a catalogue's characteristic failure is a
# name that resolves and resolves wrongly. `structure --check` then proves the
# tracked catalogue is what those sources produce now, so a document added or
# retitled without regenerating it cannot reach the site as a stale row.
check-document-catalogue:
	@$(PYTHON) $(DOCUMENT_LIBRARY_TOOL) check
	@$(PYTHON) $(DOCUMENT_LIBRARY_TOOL) structure --check

# Two claims again, and the first is the one that governs. `check` proves that
# no passage the rights records withhold carries any text in what is emitted,
# that every withheld passage states its reason, and that a licensed text never
# reaches the page without the acknowledgement its licence requires. It then
# replays the browser's own narrowing against the spine's facet counts.
# `structure --check` proves the tracked projection is what the records produce
# now, so a source record added, corrected or withdrawn without regenerating it
# cannot reach the site as a stale reading.
check-source-reader:
	@$(PYTHON) $(SOURCE_READER_TOOL) check
	@$(PYTHON) $(SOURCE_READER_TOOL) structure --check

# Generation is tier one: reproducible Markdown for review, never installed here.
web-editions:
	@set -eu; \
		leaves=$$($(PYTHON) $(WEB_EDITION_CHECKER) --provider '$(PROVIDER)' --list-eligible); \
		[ -n "$$leaves" ] || { echo 'No eligible leaf declares a web edition: $(PROVIDER)' >&2; exit 1; }; \
		$(PYTHON) $(WEB_EDITION_TOOL) --provider '$(PROVIDER)' $$leaves

# Installation is tier two: the reviewed Markdown becomes the tracked artifact.
install-web-editions:
	@set -eu; \
		for leaf in $$($(PYTHON) $(WEB_EDITION_CHECKER) --provider '$(PROVIDER)' --list-eligible); do \
			generated='$(WEB_BUILD_ROOT)/'"$$leaf.md"; \
			destination='$(WEB_ROOT)/'"$$leaf.md"; \
			[ -f "$$generated" ] || { echo "Missing generated web edition: $$generated" >&2; exit 1; }; \
			mkdir -p "$${destination%/*}"; \
			temporary="$$destination.tmp.$$$$"; \
			trap 'rm -f -- "$$temporary"' 0 1 2 15; \
			$(INSTALL) -m 0644 "$$generated" "$$temporary"; \
			mv -f -- "$$temporary" "$$destination"; \
			trap - 0 1 2 15; \
		done

# Anti-drift: the tracked artifact must be exactly what current sources produce.
check-web-editions-current:
	@set -eu; \
		rm -rf -- '$(WEB_CURRENT_ROOT)'; \
		status=0; \
		for provider in $(PROVIDERS); do \
			leaves=$$($(PYTHON) $(WEB_EDITION_CHECKER) --provider "$$provider" --list-eligible); \
			$(PYTHON) $(WEB_EDITION_TOOL) --provider "$$provider" \
				--output '$(WEB_CURRENT_ROOT)' $$leaves > /dev/null; \
			for leaf in $$leaves; do \
				tracked="web/$$provider/$$leaf.md"; \
				if [ ! -f "$$tracked" ]; then \
					echo "Missing tracked web edition: $$tracked" >&2; status=1; \
				elif ! cmp -s -- "$$tracked" '$(WEB_CURRENT_ROOT)'"/$$provider/$$leaf.md"; then \
					echo "Tracked web edition is stale: $$tracked" >&2; status=1; \
				fi; \
			done; \
		done; \
		for tracked in $$(find web -type f -name '*.md' 2>/dev/null | sort); do \
			[ -f '$(WEB_CURRENT_ROOT)/'"$${tracked#web/}" ] || { \
				echo "Tracked web edition has no eligible source: $$tracked" >&2; status=1; }; \
		done; \
		rm -rf -- '$(WEB_CURRENT_ROOT)'; \
		[ "$$status" -eq 0 ] || exit 1; \
		echo 'Tracked web editions match current sources.'

check-public-alpha:
	@$(PYTHON) $(PUBLIC_ALPHA_TOOL) check

prepare-public-alpha:
	@$(PYTHON) $(PUBLIC_ALPHA_TOOL) prepare

public-preview:
	@$(PYTHON) $(PUBLIC_ALPHA_TOOL) build --preview

public-site:
	@$(PYTHON) $(PUBLIC_ALPHA_TOOL) build

verify-public-preview:
	@$(PYTHON) $(PUBLIC_ALPHA_TOOL) verify --preview

verify-public-site:
	@$(PYTHON) $(PUBLIC_ALPHA_TOOL) verify

# Release bookkeeping; approval text is the operator's act, never invented.
check-release-bindings:
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
doc:
	@if [ -z '$(DOC)' ]; then \
		echo 'doc requires DOC=<document id below src/$(PROVIDER)/>' >&2; \
		exit 1; \
	fi
	@$(MAKE) --no-print-directory '$(BUILD_ROOT)/$(DOC).pdf'

review-doc: doc
	@$(PYTHON) $(PDF_REVIEW_TOOL) '$(BUILD_ROOT)/$(DOC).pdf'

install-doc:
	@if [ -z '$(DOC)' ]; then \
		echo 'install-doc requires DOC=<document id below src/$(PROVIDER)/>' >&2; \
		exit 1; \
	fi
	@case '$(DOC)' in \
		liturgy/roman-rite/1962/reference/altar-server-guides/*) \
			$(MAKE) --no-print-directory install-altar-server-guides ;; \
		*) \
			$(MAKE) --no-print-directory '$(PDF_ROOT)/$(DOC).pdf' ;; \
	esac

# The altar-server profile makes the seven leaves one review unit whenever a
# shared render source changes. Keep an explicit series lifecycle so the
# single-document convenience wrapper cannot silently install only one member.
altar-server-guides: check-metadata $(ALTAR_SERVER_GUIDES_BUILD_PDFS)
	@test '$(words $(ALTAR_SERVER_GUIDES_DOCUMENTS))' -eq 7 || { \
		echo 'Expected exactly seven altar-server publications; found $(words $(ALTAR_SERVER_GUIDES_DOCUMENTS))' >&2; \
		exit 1; \
	}

review-altar-server-guides: altar-server-guides
	@$(PYTHON) $(PDF_REVIEW_TOOL) $(ALTAR_SERVER_GUIDES_BUILD_PDFS)

# Validate the complete set before replacing any installed member, then stage
# every exact build byte before the short same-filesystem move phase. This
# prevents build or metadata failures from leaving a partially updated series.
install-altar-server-guides: review-altar-server-guides \
		$(ALTAR_SERVER_GUIDES_METADATA_VERIFICATIONS)
	@set -eu; \
		stage='$(BUILD_ROOT)/.install-stage/altar-server-guides.'$$$$; \
		trap 'rm -rf -- "$$stage"' 0 1 2 15; \
		for document in $(ALTAR_SERVER_GUIDES_DOCUMENTS); do \
			pdf='$(BUILD_ROOT)/'$$document.pdf; \
			stamp='$(BUILD_ROOT)/.metadata/'$$document.ok; \
			pdf_line=$$($(SHA256) -- "$$pdf"); pdf_hash=$${pdf_line%% *}; \
			validator_line=$$($(SHA256) -- '$(METADATA_CHECKER_IMPL)'); \
			validator_hash=$${validator_line%% *}; \
			expected=$$(printf 'schema=1\nprovider=%s\ndocument=%s\npdf_sha256=%s\nvalidator_sha256=%s' \
				'$(PROVIDER)' "$$document" "$$pdf_hash" "$$validator_hash"); \
			actual=$$(cat "$$stamp"); \
			[ "$$actual" = "$$expected" ] || { \
				echo "Validation stamp does not match current PDF/checker: $$document" >&2; exit 1; }; \
		done; \
		for document in $(ALTAR_SERVER_GUIDES_DOCUMENTS); do \
			source='$(BUILD_ROOT)/'$$document.pdf; \
			staged="$$stage/$$document.pdf"; \
			mkdir -p "$${staged%/*}"; \
			$(INSTALL) -m 0644 "$$source" "$$staged"; \
			cmp -s -- "$$source" "$$staged" || { \
				echo "Staged PDF differs from reviewed build: $$document" >&2; exit 1; }; \
		done; \
		for document in $(ALTAR_SERVER_GUIDES_DOCUMENTS); do \
			staged="$$stage/$$document.pdf"; \
			destination='$(PDF_ROOT)/'$$document.pdf; \
			mkdir -p "$${destination%/*}"; \
			mv -f -- "$$staged" "$$destination"; \
		done; \
		rm -rf -- "$$stage"; \
		trap - 0 1 2 15

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

# Staleness stays out of `check`: it flags re-evaluation work, not breakage.
check: check-metadata check-web-editions check-web-editions-current \
	check-proper-components check-document-catalogue check-source-reader \
	check-sources check-roman-sanctuary-artwork check-promised-deliverables \
	check-public-alpha check-release-bindings check-tool-registry \
	check-browser-static \
	check-calendar-masses check-calendar-rubrics check-propers-census \
	check-mass-ordinary check-bible-indexes check-catena \
	check-commentary-coverage check-scripture-chronology check-examples

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

# The four reader harnesses drive real Chromium over the preview build, and
# until this target existed nothing ran them: the suite only syntax-checked
# them, so they were read as broken for months when what they wanted was a
# build. Three address `build/public-alpha/preview` as their data root, so
# without `public-preview` every request 404s and the failure wears the costume
# of a code defect — "Timed out waiting for ... readiness". Hence the
# prerequisite. Outside `check` for the same reasons as `check-browser-gate`,
# and because it takes two minutes rather than half a second. Three harnesses
# exit non-zero on a real finding about absence and coverage notices, so this
# holds them to a recorded pass floor rather than to a zero exit; raising the
# floor is the point of it.
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

# Needs PyYAML (requirements-tools.txt); skipped rather than failed without it.
# Two claims. The first is that the sources are valid; the second is that what
# the browser is served is what those sources produce NOW. `make check` proved
# tracked web/**/*.md current and proved nothing about src/web/data/structure,
# so on 2026-08-07 regenerating the propers with unchanged tools rewrote 4,269
# lines of roman-pre-1955.json that no source change accounted for — the served
# recension had drifted that far with nothing reporting it. `structure --check`
# writes nothing; `mass-propers structure` is what fixes a failure.
check-calendar-masses:
	@if $(PYTHON) -c 'import yaml' 2>/dev/null; then \
		$(PYTHON) tools/tpt check-calendar-masses; \
		$(PYTHON) tools/tpt mass-propers structure --check; \
	else echo "PyYAML missing; skipping calendar-mass check"; fi

# Validates the rubrical precedence sources, refuses a stale generated layer,
# and runs the browser's own derivation over each source's solved cases. Needs
# PyYAML for the sources and node for the derivation. A missing node is a
# failure inside the tool and not a skip: the solved cases are the only thing
# holding assembly-model.js to the tracked tables, and a run that could not
# exercise them has confirmed nothing to report as a pass.
check-calendar-rubrics:
	@if $(PYTHON) -c 'import yaml' 2>/dev/null; then \
		$(PYTHON) tools/tpt calendar-rubrics check; \
	else echo "PyYAML missing; skipping calendar-rubric check"; fi

# The count of both calendars is derived, not typed: one census, written into
# every document that carries it. This refuses a document whose block has
# drifted from the calendars, and writes nothing — `mass-propers census --write`
# is what fixes it. Needs PyYAML, skipped rather than failed without it.
check-propers-census:
	@if $(PYTHON) -c 'import yaml' 2>/dev/null; then \
		$(PYTHON) tools/tpt mass-propers census --check; \
	else echo "PyYAML missing; skipping propers-census check"; fi

# The Ordinary of the Mass: validates the two ordo-missae inventories against
# the artifacts they draw on and against the source library's own rights record,
# and refuses a browser file that no longer matches. Needs no third-party
# module, so it is a plain failure and never a skip.
check-mass-ordinary:
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

check-tests:
	@$(PYTHON) -m unittest discover -s tools/tests

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

define REGISTER_PROPER_SYNTHESIS_SOURCES
$(BUILD_ROOT)/$(1).pdf: $(shell find $(SOURCE_ROOT)/$(patsubst %-synthesis,%,$(1)) \
	-type f \( -name '*.tex' -o -name '*.toml' -o -name '*.sty' -o -name '*.bib' \) \
	2>/dev/null | sort)
endef
$(foreach document,$(PROPER_SYNTHESIS_DOCUMENTS),\
	$(eval $(call REGISTER_PROPER_SYNTHESIS_SOURCES,$(document))))

$(foreach document,$(PROPER_SYNTHESIS_DOCUMENTS),\
	$(eval $(BUILD_ROOT)/$(document).pdf: \
		$(SOURCE_ROOT)/$(patsubst %-synthesis,%,$(document))/synthesis.tex))

$(BUILD_ROOT)/%-synthesis.pdf:
	@mkdir -p $(@D) '$(BUILD_ROOT)/.metadata/$(dir $*)'
	@rm -f -- '$(BUILD_ROOT)/.metadata/$*-synthesis.ok'
	cd $(SOURCE_ROOT) && TEXINPUTS=..: $(PDFLATEX) -interaction=nonstopmode -halt-on-error \
		-jobname=$(notdir $*)-synthesis -output-directory=$(abspath $(@D)) $*/synthesis.tex
	cd $(SOURCE_ROOT) && TEXINPUTS=..: $(PDFLATEX) -interaction=nonstopmode -halt-on-error \
		-jobname=$(notdir $*)-synthesis -output-directory=$(abspath $(@D)) $*/synthesis.tex
	@$(PROPER_COMPONENT_CHECKER) --provider '$(PROVIDER)' --document '$*' \
		--aux '$(BUILD_ROOT)/$*-synthesis.aux'
	@$(METADATA_CHECKER) --provider '$(PROVIDER)' --pdf '$*' '$@'
	@set -eu; \
		pdf_line=$$($(SHA256) -- '$@'); pdf_hash=$${pdf_line%% *}; \
		validator_line=$$($(SHA256) -- '$(METADATA_CHECKER_IMPL)'); \
		validator_hash=$${validator_line%% *}; \
		printf 'schema=1\nprovider=%s\ndocument=%s\npdf_sha256=%s\nvalidator_sha256=%s\n' \
			'$(PROVIDER)' '$*-synthesis' "$$pdf_hash" "$$validator_hash" \
			> '$(BUILD_ROOT)/.metadata/$*-synthesis.ok'

$(BUILD_ROOT)/%.pdf: $(SOURCE_ROOT)/%/main.tex $(COMMON_SOURCES) | check-metadata
	@mkdir -p $(@D)
	@mkdir -p '$(BUILD_ROOT)/.metadata/$(dir $*)'
	@rm -f -- '$(BUILD_ROOT)/.metadata/$*.ok'
	cd $(SOURCE_ROOT) && TEXINPUTS=..: $(PDFLATEX) -interaction=nonstopmode -halt-on-error -jobname=$(notdir $*) -output-directory=$(abspath $(@D)) $*/main.tex
	cd $(SOURCE_ROOT) && TEXINPUTS=..: $(PDFLATEX) -interaction=nonstopmode -halt-on-error -jobname=$(notdir $*) -output-directory=$(abspath $(@D)) $*/main.tex
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

$(BUILD_ROOT)/.metadata/%.verify: $(BUILD_ROOT)/.metadata/%.ok FORCE_METADATA_VERIFICATION
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
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s58-most-holy-trinity-year-a.pdf: \
	$(POSTCONCILIAR_US_ROOT)/temporal/shared/formularies/pc-s58-most-holy-trinity/propers/verified.md
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s59-most-holy-body-and-blood-of-christ-year-a.pdf: \
	$(POSTCONCILIAR_US_ROOT)/temporal/shared/formularies/pc-s59-most-holy-body-and-blood-of-christ/propers/verified.md
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s35-eleventh-sunday-in-ordinary-time-year-a.pdf: \
	$(POSTCONCILIAR_US_ROOT)/temporal/shared/ordinary-time/weeks/11/propers/verified.md
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s36-twelfth-sunday-in-ordinary-time-year-a.pdf: \
	$(POSTCONCILIAR_US_ROOT)/temporal/shared/ordinary-time/weeks/12/propers/verified.md
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s37-thirteenth-sunday-in-ordinary-time-year-a.pdf: \
	$(POSTCONCILIAR_US_ROOT)/temporal/shared/ordinary-time/weeks/13/propers/verified.md
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s38-fourteenth-sunday-in-ordinary-time-year-a.pdf: \
	$(POSTCONCILIAR_US_ROOT)/temporal/shared/ordinary-time/weeks/14/propers/verified.md
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s39-fifteenth-sunday-in-ordinary-time-year-a.pdf: \
	$(POSTCONCILIAR_US_ROOT)/temporal/shared/ordinary-time/weeks/15/propers/verified.md
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s40-sixteenth-sunday-in-ordinary-time-year-a.pdf: \
	$(POSTCONCILIAR_US_ROOT)/temporal/shared/ordinary-time/weeks/16/propers/verified.md
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s41-seventeenth-sunday-in-ordinary-time-year-a.pdf: \
	$(POSTCONCILIAR_US_ROOT)/temporal/shared/ordinary-time/weeks/17/propers/verified.md
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s42-eighteenth-sunday-in-ordinary-time-year-a.pdf \
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s42-eighteenth-sunday-in-ordinary-time-year-a-synthesis.pdf \
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s42-eighteenth-sunday-in-ordinary-time-year-b.pdf \
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s42-eighteenth-sunday-in-ordinary-time-year-b-synthesis.pdf \
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s42-eighteenth-sunday-in-ordinary-time-year-c.pdf \
$(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s42-eighteenth-sunday-in-ordinary-time-year-c-synthesis.pdf: \
	$(POSTCONCILIAR_US_ROOT)/temporal/shared/ordinary-time/weeks/18/propers/verified.md
$(NOVENA_BUILD_PDFS): $(NOVENA_SHARED)
$(BIOGRAPHY_BUILD_PDFS): $(BIOGRAPHY_SHARED)
$(HISTORICAL_TRANSLATION_BUILD_PDFS): $(HISTORICAL_TRANSLATION_SHARED)
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

$(PDF_ROOT)/%.pdf: $(BUILD_ROOT)/%.pdf | check-metadata $(BUILD_ROOT)/.metadata/%.verify
	@set -eu; \
		pdf='$(BUILD_ROOT)/$*.pdf'; \
		stamp='$(BUILD_ROOT)/.metadata/$*.ok'; \
		destination='$@'; \
		mkdir -p '$(@D)'; \
		pdf_line=$$($(SHA256) -- "$$pdf"); \
		pdf_hash=$${pdf_line%% *}; \
		validator_line=$$($(SHA256) -- '$(METADATA_CHECKER_IMPL)'); \
		validator_hash=$${validator_line%% *}; \
		expected=$$(printf 'schema=1\nprovider=%s\ndocument=%s\npdf_sha256=%s\nvalidator_sha256=%s' \
			'$(PROVIDER)' '$*' "$$pdf_hash" "$$validator_hash"); \
		actual=$$(cat "$$stamp"); \
		[ "$$actual" = "$$expected" ] || { echo 'Validation stamp does not match current PDF/checker: $*' >&2; exit 1; }; \
		temporary="$$destination.tmp.$$$$"; \
		trap 'rm -f -- "$$temporary"' 0 1 2 15; \
		$(INSTALL) -m 0644 "$$pdf" "$$temporary"; \
		temporary_line=$$($(SHA256) -- "$$temporary"); \
		temporary_hash=$${temporary_line%% *}; \
		pdf_after_line=$$($(SHA256) -- "$$pdf"); \
		pdf_after_hash=$${pdf_after_line%% *}; \
		validator_after_line=$$($(SHA256) -- '$(METADATA_CHECKER_IMPL)'); \
		validator_after_hash=$${validator_after_line%% *}; \
		if [ "$$temporary_hash" != "$$pdf_hash" ] || [ "$$pdf_after_hash" != "$$pdf_hash" ] || [ "$$validator_after_hash" != "$$validator_hash" ]; then \
			echo 'PDF or metadata checker changed during install: $*' >&2; \
			exit 1; \
		fi; \
		mv -f -- "$$temporary" "$$destination"; \
		trap - 0 1 2 15

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

check-bibles:
	@$(PYTHON) $(BIBLE_TYPESET_TOOL) check

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
	$(PDFLATEX) -interaction=nonstopmode -halt-on-error \
		-output-directory='$(BIBLE_BUILD_ROOT)' '$<'
	$(PDFLATEX) -interaction=nonstopmode -halt-on-error \
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
# A track is installed into pdf/ and a whole bible is not. The difference is
# what the artifact carries: a whole bible is the source library's own text
# reset, while a track carries this project's plan — its periods, its titles,
# its notes and its account of what it leaves out — around that text.
tracks: check-plan-sources
	@set -eu; \
		volumes=$$($(PYTHON) $(BIBLE_TYPESET_TOOL) list --plan '$(PLAN)' --format ids); \
		[ -n "$$volumes" ] || { echo 'No track is declared for plan $(PLAN)' >&2; exit 1; }; \
		for volume in $$volumes; do \
			$(MAKE) --no-print-directory '$(READING_PDF_ROOT)/'"$$volume"'.pdf'; \
		done

track:
	@if [ -z '$(VOLUME)' ]; then \
		echo 'track requires VOLUME=<id from `tools/tpt typeset-bible list --plan $(PLAN) --format ids`>' >&2; \
		exit 1; \
	fi
	@$(MAKE) --no-print-directory '$(READING_PDF_ROOT)/$(VOLUME).pdf'

# The installed volume is what a reader downloads, so that is what is rastered.
review-track: track
	@$(PYTHON) $(PDF_REVIEW_TOOL) '$(READING_PDF_ROOT)/$(VOLUME).pdf'

# Two questions, both of which must hold before a track may be published: that
# every volume still resolves against its edition, and that the installed PDF
# is the one the current sources produce. The second is what stops a plan edit
# from reaching the site through a stale artifact.
check-tracks: check-plan-sources
	@$(PYTHON) $(BIBLE_TYPESET_TOOL) check --plan '$(PLAN)' --verbose
	@set -eu; \
		volumes=$$($(PYTHON) $(BIBLE_TYPESET_TOOL) list --plan '$(PLAN)' --format ids); \
		for volume in $$volumes; do \
			installed='$(READING_PDF_ROOT)/'"$$volume"'.pdf'; \
			[ -f "$$installed" ] || { echo "Track is not installed: $$volume; run make tracks" >&2; exit 1; }; \
		done; \
		$(MAKE) --no-print-directory tracks; \
		if ! git diff --quiet -- '$(READING_PDF_ROOT)'; then \
			echo 'Installed tracks are stale; run make tracks and commit them' >&2; \
			exit 1; \
		fi

# The plan file is validated by the tool that owns it before a single verse of
# it is set. A track built from a plan that does not validate would be a
# publication of unchecked references.
check-plan-sources:
	@$(PYTHON) $(READING_PLAN_TOOL) check

# The browser's structure of every abridged plan, rewritten from the plan
# sources. Tracked under src/web/data and served as the site's reading data.
reading-structure:
	@$(PYTHON) $(READING_PLAN_TOOL) structure

# The catalogue of every document, rewritten from the documents' own sources
# and from the PDFs they build. Tracked under src/web/data and served to the
# `texts` reading page, which reads it and walks nothing itself.
document-catalogue:
	@$(PYTHON) $(DOCUMENT_LIBRARY_TOOL) structure

# The reading projection of the source library, rewritten from the work,
# edition, artifact, segment and passage records. Tracked under src/web/data and
# served to the `sources` reading page, which reads it and walks nothing itself.
source-projection:
	@$(PYTHON) $(SOURCE_READER_TOOL) structure

$(READING_BUILD_ROOT)/%.tex: $(BIBLE_TYPESET_IMPL) FORCE_BIBLE_RENDER
	@$(PYTHON) $(BIBLE_TYPESET_TOOL) render --volume '$*' --out '$(READING_BUILD_ROOT)'

# Both are kept: the TeX is the compiler's input and the diffable record of
# what was set, and the built PDF is what `review-track` rasters. Make would
# otherwise delete each as a chained intermediate and recompile the volume.
.PRECIOUS: $(READING_BUILD_ROOT)/%.tex $(READING_BUILD_ROOT)/%.pdf

# The list of readings carries the page each reading begins on, and a list
# twenty pages long moves the pages it is naming, so two passes do not always
# settle a track of three hundred pages. Run until LaTeX stops asking, and fail
# rather than install a volume whose contents point at the wrong pages.
$(READING_BUILD_ROOT)/%.pdf: $(READING_BUILD_ROOT)/%.tex | check-tools
	@set -eu; \
		log='$(READING_BUILD_ROOT)/$*.log'; \
		pass=0; \
		while [ "$$pass" -lt 5 ]; do \
			pass=$$((pass + 1)); \
			$(PDFLATEX) -interaction=nonstopmode -halt-on-error \
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

# Installed only when the bytes differ, so a rebuild that changed nothing does
# not show up as a modified tracked artifact.
$(READING_PDF_ROOT)/%.pdf: $(READING_BUILD_ROOT)/%.pdf
	@set -eu; \
		mkdir -p '$(@D)'; \
		if cmp -s '$<' '$@' 2>/dev/null; then \
			echo "unchanged $@"; \
		else \
			$(INSTALL) -m 0644 -- '$<' '$@'; \
			echo "installed $@"; \
		fi

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
