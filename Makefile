PDFLATEX ?= pdflatex
PYTHON ?= python3
PROVIDER ?= gpt
PDF_JOBS ?= 4
SHA256 ?= sha256sum
INSTALL ?= install
CODEX ?= /usr/bin/codex

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
#     article, geometry, fontenc, inputenc, lmodern, microtype, array,
#     booktabs, longtable, tabularx, enumitem, needspace, multicol, xcolor,
#     hyperref, tcolorbox, tikz/PGF, pdflscape, ragged2e, titlesec and endnotes
#   PDF metadata/text/raster and bounded PNG/contact-sheet processing:
#     poppler (pdfinfo, pdftotext, pdftoppm) and imagemagick (magick 7)
#   LaTeX-to-Markdown conversion for the tracked web editions:
#     pandoc
#   repository/review/isolated-agent workflow:
#     git github-cli openai-codex ripgrep
#
# pacman supplies the native shared-library closure and TeX package
# transitives. poppler-data is optional for non-Latin CMaps and is not needed
# by the current embedded-font corpus. pacman and either root access or sudo
# are bootstrap requirements for the installer target, not project runtime
# dependencies. GitHub Actions and its hosted Python/pip environment are
# CI-only. Node/npm, Ghostscript and qpdf are not used here.
# pdfLaTeX remains necessary for the shared preamble's pdfTeX primitives;
# XeLaTeX, LuaLaTeX and Tectonic are not drop-in replacements. latexmk from
# texlive-binextra is a free, more robust pass controller, but is not currently
# used. Poppler plus ImageMagick 7 remains the smallest purpose-fit PDF review
# stack; MuPDF or GraphicsMagick would not eliminate an existing dependency.
ARCH_CORE_PACKAGES := make bash findutils coreutils diffutils
ARCH_PYTHON_PACKAGES := python tzdata python-markdown
ARCH_TEX_PACKAGES := texlive-bin texlive-basic texlive-latex \
	texlive-latexrecommended texlive-latexextra texlive-pictures \
	texlive-fontsrecommended
ARCH_PDF_PACKAGES := poppler imagemagick
ARCH_WEB_PACKAGES := pandoc
ARCH_WORKFLOW_PACKAGES := git github-cli openai-codex ripgrep
ARCH_DEPENDENCY_PACKAGES := $(ARCH_CORE_PACKAGES) $(ARCH_PYTHON_PACKAGES) \
	$(ARCH_TEX_PACKAGES) $(ARCH_PDF_PACKAGES) $(ARCH_WEB_PACKAGES) \
	$(ARCH_WORKFLOW_PACKAGES)
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
DOC_ROOT := doc/$(PROVIDER)
WEB_BUILD_ROOT := build/web/$(PROVIDER)
WEB_ROOT := web/$(PROVIDER)
# The drift gate compares every provider's tracked tree, not only $(PROVIDER).
WEB_CURRENT_ROOT := build/.web-current
ALL_MAIN_SOURCES := $(shell find src -mindepth 2 -type f -name main.tex 2>/dev/null | sort)
PROVIDERS := $(sort $(foreach path,$(ALL_MAIN_SOURCES),$(word 2,$(subst /, ,$(path)))))

MAIN_SOURCES := $(shell find $(SOURCE_ROOT) -type f -name main.tex 2>/dev/null | sort)
DOCUMENTS := $(patsubst $(SOURCE_ROOT)/%/main.tex,%,$(MAIN_SOURCES))
BUILD_PDFS := $(addprefix $(BUILD_ROOT)/,$(addsuffix .pdf,$(DOCUMENTS)))
BUILD_METADATA_STAMPS := $(addprefix $(BUILD_ROOT)/.metadata/,$(addsuffix .ok,$(DOCUMENTS)))
BUILD_METADATA_VERIFICATIONS := $(addprefix $(BUILD_ROOT)/.metadata/,$(addsuffix .verify,$(DOCUMENTS)))
DOC_PDFS := $(addprefix $(DOC_ROOT)/,$(addsuffix .pdf,$(DOCUMENTS)))
METADATA_CHECKER := scripts/check-generation-metadata
WEB_EDITION_CHECKER := scripts/check-web-edition
WEB_EDITION_TOOL := scripts/web-edition
CURRICULUM_STRUCTURE_CHECKER := scripts/check-curriculum-structure
PDF_REVIEW_TOOL := scripts/pdf-review
PUBLIC_ALPHA_TOOL := scripts/public-alpha
RELEASE_BINDINGS_TOOL := scripts/release-bindings
RESEARCH_STALENESS_TOOL := scripts/research-staleness
override CODEX_LAUNCHER := scripts/triptych-codex
SOURCE_LIBRARY_TOOL := scripts/source-library
SOURCE_INVENTORY_TOOL := scripts/source-inventory
SOURCE_FAMILY_MIGRATION_TOOL := scripts/source-family-migration

# Triptych consumes the reusable Worktree Marshal Make API through the existing
# compatibility launcher. Keep target names plain; lifecycle IDs are supplied
# only as validated RUN=<run-id> command-line assignments.
override WORKTREE_MARSHAL := $(CODEX_LAUNCHER)
override WORKTREE_MARSHAL_DISPLAY_NAME := Triptych Codex
override WORKTREE_MARSHAL_GLOBAL_ARGUMENTS :=
override WORKTREE_MARSHAL_RUN_TARGET := codex
override WORKTREE_MARSHAL_STATUS_TARGET := status
override WORKTREE_MARSHAL_REOPEN_TARGET := reopen
override WORKTREE_MARSHAL_DIFF_TARGET := final-diff
override WORKTREE_MARSHAL_INTEGRATE_TARGET := integrate
override WORKTREE_MARSHAL_RESOLVE_TARGET := resolve
override WORKTREE_MARSHAL_CONTINUE_TARGET := continue
override WORKTREE_MARSHAL_ABORT_TARGET := abort
override WORKTREE_MARSHAL_CLEAN_TARGET := clean-run
override WORKTREE_MARSHAL_POSITIONAL_RUN_ID_COMPAT := 1
override WORKTREE_MARSHAL_RUN_ARGUMENTS :=
override WORKTREE_MARSHAL_STATUS_ARGUMENTS := --triptych-status
override WORKTREE_MARSHAL_REOPEN_ARGUMENTS := --triptych-reopen
override WORKTREE_MARSHAL_DIFF_ARGUMENTS := --triptych-final-diff
override WORKTREE_MARSHAL_INTEGRATE_ARGUMENTS := --triptych-integrate
override WORKTREE_MARSHAL_RESOLVE_ARGUMENTS := --triptych-resolve
override WORKTREE_MARSHAL_CONTINUE_ARGUMENTS := --triptych-continue
override WORKTREE_MARSHAL_ABORT_ARGUMENTS := --triptych-abort
override WORKTREE_MARSHAL_CLEAN_ARGUMENTS := --triptych-clean
include tools/worktree-marshal/src/worktree_marshal/resources/worktree-marshal.mk

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
	distclean check-tools check-metadata check-web-editions \
	web-editions install-web-editions check-web-editions-current \
	check-sources check-source-library \
	check-source-inventory check-source-inventory-tool \
	check-source-family-migration check-source-family-migration-tool \
	check-source-family-screening \
	check-public-alpha prepare-public-alpha \
	check-pdf-review check-agent-isolation check-curriculum-sources \
	check-curriculum-structure \
	public-site public-preview \
	dependencies-arch install-dependencies-arch \
	verify-public-site verify-public-preview \
	check-release-bindings refresh-release-bindings approve-release \
	add-publication doc review-doc install-doc check check-tests \
	check-staleness explain-staleness rebaseline-doc \
	FORCE_METADATA_VERIFICATION
.DELETE_ON_ERROR:
.SECONDARY: $(BUILD_METADATA_STAMPS)

ifeq ($(strip $(_TRIPTYCH_MAKE_PARALLEL_FLAGS)),)
all:
	+@$(MAKE) --no-print-directory $(_TRIPTYCH_BOUNDED_PDF_JOB_OPTION) pdf

review-pdfs:
	+@$(MAKE) --no-print-directory $(_TRIPTYCH_BOUNDED_PDF_JOB_OPTION) pdf
	@if [ -d '$(DOC_ROOT)' ]; then \
		$(PYTHON) $(PDF_REVIEW_TOOL) --changed-against $(DOC_ROOT) $(BUILD_PDFS); \
	else \
		$(PYTHON) $(PDF_REVIEW_TOOL) $(BUILD_PDFS); \
	fi

review-all-pdfs:
	+@$(MAKE) --no-print-directory $(_TRIPTYCH_BOUNDED_PDF_JOB_OPTION) pdf
	@$(PYTHON) $(PDF_REVIEW_TOOL) $(BUILD_PDFS)
else
all: pdf

review-pdfs: pdf
	@if [ -d '$(DOC_ROOT)' ]; then \
		$(PYTHON) $(PDF_REVIEW_TOOL) --changed-against $(DOC_ROOT) $(BUILD_PDFS); \
	else \
		$(PYTHON) $(PDF_REVIEW_TOOL) $(BUILD_PDFS); \
	fi

review-all-pdfs: pdf
	@$(PYTHON) $(PDF_REVIEW_TOOL) $(BUILD_PDFS)
endif

pdf: check-metadata $(BUILD_METADATA_VERIFICATIONS)

install: check-metadata $(DOC_PDFS)
	@set -eu; \
	for document in $(DOCUMENTS); do \
		pdf='$(BUILD_ROOT)/'$$document.pdf; \
		stamp='$(BUILD_ROOT)/.metadata/'$$document.ok; \
		pdf_line=$$($(SHA256) -- "$$pdf"); \
		pdf_hash=$${pdf_line%% *}; \
		validator_line=$$($(SHA256) -- '$(METADATA_CHECKER)'); \
		validator_hash=$${validator_line%% *}; \
		expected=$$(printf 'schema=1\nprovider=%s\ndocument=%s\npdf_sha256=%s\nvalidator_sha256=%s' \
			'$(PROVIDER)' "$$document" "$$pdf_hash" "$$validator_hash"); \
		actual=$$(cat "$$stamp"); \
		[ "$$actual" = "$$expected" ] || { echo "Validation stamp does not match current PDF/checker: $$document" >&2; exit 1; }; \
		cmp -s "$$pdf" "$(DOC_ROOT)/$$document.pdf" || { echo "Installed PDF differs from reviewed build: $$document"; exit 1; }; \
	done

list:
	@printf '%s\n' $(DOCUMENTS)

codex reopen resolve: private export TRIPTYCH_CODEX_REAL := $(CODEX)

dependencies-arch:
	@printf '%s\n' $(ARCH_DEPENDENCY_PACKAGES)

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

check-agent-isolation:
	@$(PYTHON) -m unittest discover -s tools/worktree-marshal/tests -t tools/worktree-marshal -v
	@$(PYTHON) -m unittest discover -s scripts/tests -p 'test_triptych_codex.py' -v

check-pdf-review:
	@$(PYTHON) -m unittest discover -s scripts/tests -p 'test_pdf_review.py' -v

check-sources:
	@$(PYTHON) $(SOURCE_LIBRARY_TOOL) validate
	@set -eu; for inventory in src/sources/inventories/*publications-v1.toml; do \
		[ -e "$$inventory" ] || continue; \
		$(PYTHON) $(SOURCE_INVENTORY_TOOL) check "$$inventory"; \
	done
	@$(PYTHON) $(SOURCE_FAMILY_MIGRATION_TOOL) check

check-source-library:
	@$(PYTHON) -m unittest discover -s scripts/tests -p 'test_source_library.py' -v

check-source-inventory:
	@$(PYTHON) $(SOURCE_INVENTORY_TOOL) check

check-source-inventory-tool:
	@$(PYTHON) -m unittest discover -s scripts/tests -p 'test_source_inventory.py' -v

check-source-family-migration:
	@$(PYTHON) $(SOURCE_FAMILY_MIGRATION_TOOL) check

check-source-family-migration-tool:
	@$(PYTHON) -m unittest discover -s scripts/tests -p 'test_source_family_migration.py' -v

check-source-family-screening:
	@$(PYTHON) $(SOURCE_FAMILY_MIGRATION_TOOL) check --require-family-screened

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
		'make install  Publish built PDFs into the mirrored tracked doc/ tree' \
		'make doc DOC=<id>  Build one document below src/$$PROVIDER/' \
		'make review-doc DOC=<id>  Build one document and raster it for page review' \
		'make install-doc DOC=<id>  Build, gate, and install one document' \
		'make list     List discovered document IDs' \
		'make dependencies-arch  List canonical Arch package dependencies' \
		'make install-dependencies-arch  Run a full Arch upgrade and install canonical packages' \
		'make codex    Start Codex in an automatically isolated task checkout' \
		'make status [RUN=<run-id>]  List runs needing attention or inspect one exact record' \
		'make reopen RUN=<run-id>  Start a new Codex process in a retained task checkout' \
		'make clean-run RUN=<run-id>  Safely clean an eligible retained run' \
		'make integrate RUN=<run-id>  Integrate a clean run or land an unchanged review-pending candidate' \
		'make resolve RUN=<run-id>  Open Codex to resolve and stage a managed rebase conflict' \
		'make continue RUN=<run-id>  Continue staged resolutions to a review-pending candidate' \
		'make abort RUN=<run-id>  Abort a managed rebase and restore its exact audited source' \
		'make final-diff RUN=<run-id>  Show the complete review-pending diff without a worktree path' \
		'Run-ID Make wrappers require a launcher-produced ID; use scripts/triptych-codex directly for external input' \
		'make check-agent-isolation  Test the transparent Codex launcher' \
		'make check-pdf-review  Test memory-bounded PDF inspection tooling' \
		'make check-sources  Validate the source library, inventory, and migration ledger' \
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
		'make check-public-alpha  Validate the exhaustive public-release policy' \
		'make prepare-public-alpha  Print current candidate hashes; grants no approval' \
		'make public-preview  Build a private no-index preview with review candidates' \
		'make public-site  Build the fail-closed, history-free public artifact' \
		'make verify-public-preview  Recheck the existing private preview artifact' \
		'make verify-public-site  Recheck the existing public artifact' \
		'make check-release-bindings  Report stale exact PDF, site-source, and rights-record bindings' \
		'make refresh-release-bindings [ADOPT=1]  Mechanically re-derive every exact release binding from current bytes' \
		'make approve-release NOTE="..."  Record a dated supplement with the operator instruction, then refresh' \
		'make add-publication ID=<leaf> CATALOG=<page> [PROVIDER=<p>] [STATUS=hold]  Add a manifest entry' \
		'make check    Run every repository policy check' \
		'make check-tests  Run the complete script unit-test suite' \
		'make check-staleness  Report editions whose research inputs changed (any provider)' \
		'make explain-staleness DOC=<leaf> [PROVIDER=<p>]  Name the changed research inputs' \
		'make rebaseline-doc DOC=<leaf> [PROVIDER=<p>]  Clear a staleness flag after re-evaluation' \
		'make clean    Remove transient build artifacts only'

check-metadata: check-tools
	@$(METADATA_CHECKER) --provider $(PROVIDER)

# Absence of a leaf's declaration is an error: nothing defaults to eligible.
check-web-editions:
	@$(PYTHON) $(WEB_EDITION_CHECKER) --provider $(PROVIDER)

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

refresh-release-bindings:
	@$(PYTHON) $(RELEASE_BINDINGS_TOOL) refresh \
		$(if $(ADOPT),--adopt-new-site-sources,)

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

install-doc: doc
	@$(MAKE) --no-print-directory '$(DOC_ROOT)/$(DOC).pdf'

# Cross-provider research staleness (policy in guidance/staleness.md).
check-staleness:
	@$(PYTHON) $(RESEARCH_STALENESS_TOOL) status

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
	check-sources check-public-alpha check-release-bindings

check-tests:
	@$(PYTHON) -m unittest discover -s scripts/tests

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
$(foreach document,$(DOCUMENTS),$(eval $(call REGISTER_DOCUMENT_SOURCES,$(document))))

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
		validator_line=$$($(SHA256) -- '$(METADATA_CHECKER)'); \
		validator_hash=$${validator_line%% *}; \
		$(METADATA_CHECKER) --provider '$(PROVIDER)' --pdf '$*' "$$pdf"; \
		pdf_after_line=$$($(SHA256) -- "$$pdf"); \
		pdf_after_hash=$${pdf_after_line%% *}; \
		validator_after_line=$$($(SHA256) -- '$(METADATA_CHECKER)'); \
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

$(BUILD_ROOT)/.metadata/%.ok: $(BUILD_ROOT)/%.pdf $(METADATA_CHECKER)
	@set -eu; \
		pdf='$<'; \
		stamp='$@'; \
		pdf_line=$$($(SHA256) -- "$$pdf"); \
		pdf_hash=$${pdf_line%% *}; \
		validator_line=$$($(SHA256) -- '$(METADATA_CHECKER)'); \
		validator_hash=$${validator_line%% *}; \
		expected=$$(printf 'schema=1\nprovider=%s\ndocument=%s\npdf_sha256=%s\nvalidator_sha256=%s' \
			'$(PROVIDER)' '$*' "$$pdf_hash" "$$validator_hash"); \
		if [ -f "$$stamp" ] && [ "$$(cat "$$stamp")" = "$$expected" ]; then \
			exit 0; \
		fi; \
		$(METADATA_CHECKER) --provider '$(PROVIDER)' --pdf '$*' "$$pdf"; \
		pdf_after_line=$$($(SHA256) -- "$$pdf"); \
		pdf_after_hash=$${pdf_after_line%% *}; \
		validator_after_line=$$($(SHA256) -- '$(METADATA_CHECKER)'); \
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
		validator_line=$$($(SHA256) -- '$(METADATA_CHECKER)'); \
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
		validator_after_line=$$($(SHA256) -- '$(METADATA_CHECKER)'); \
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
	$(CURRICULUM_STRUCTURE_CHECKER) | check-curriculum-sources
$(ALTAR_SERVER_GUIDES_BUILD_PDFS): $(ALTAR_SERVER_GUIDES_SHARED)
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

$(DOC_ROOT)/%.pdf: $(BUILD_ROOT)/%.pdf | check-metadata $(BUILD_ROOT)/.metadata/%.verify
	@set -eu; \
		pdf='$(BUILD_ROOT)/$*.pdf'; \
		stamp='$(BUILD_ROOT)/.metadata/$*.ok'; \
		destination='$@'; \
		mkdir -p '$(@D)'; \
		pdf_line=$$($(SHA256) -- "$$pdf"); \
		pdf_hash=$${pdf_line%% *}; \
		validator_line=$$($(SHA256) -- '$(METADATA_CHECKER)'); \
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
		validator_after_line=$$($(SHA256) -- '$(METADATA_CHECKER)'); \
		validator_after_hash=$${validator_after_line%% *}; \
		if [ "$$temporary_hash" != "$$pdf_hash" ] || [ "$$pdf_after_hash" != "$$pdf_hash" ] || [ "$$validator_after_hash" != "$$validator_hash" ]; then \
			echo 'PDF or metadata checker changed during install: $*' >&2; \
			exit 1; \
		fi; \
		mv -f -- "$$temporary" "$$destination"; \
		trap - 0 1 2 15

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
