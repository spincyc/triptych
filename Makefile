override CODEX_LIFECYCLE_GOALS := integrate resolve continue abort final-diff

# These targets are convenience wrappers for exact run IDs emitted by the
# launcher. GNU Make processes options and command-line variable assignments
# before reading this file, so never forward arbitrary data here; use
# scripts/triptych-codex directly when the value is external or untrusted. Once
# Make has parsed a value as the second goal, validate it without a parse-time
# shell command. Ordinary command-line variable assignments cannot replace
# these override functions.
override codex_make_strip_decimal = $(subst 9,,$(subst 8,,$(subst 7,,$(subst 6,,$(subst 5,,$(subst 4,,$(subst 3,,$(subst 2,,$(subst 1,,$(subst 0,,$(1)))))))))))
override codex_make_strip_hex = $(subst f,,$(subst e,,$(subst d,,$(subst c,,$(subst b,,$(subst a,,$(call codex_make_strip_decimal,$(1))))))))
override codex_make_hex_to_words = $(subst f,x ,$(subst e,x ,$(subst d,x ,$(subst c,x ,$(subst b,x ,$(subst a,x ,$(subst 9,x ,$(subst 8,x ,$(subst 7,x ,$(subst 6,x ,$(subst 5,x ,$(subst 4,x ,$(subst 3,x ,$(subst 2,x ,$(subst 1,x ,$(subst 0,x ,$(1)))))))))))))))))
override codex_make_character_count = $(words $(call codex_make_hex_to_words,$(1)))

# Opaque lifecycle commands present the run ID as a second Make goal. Limit the
# fallback rule to those invocations so ordinary unknown targets still fail.
ifeq ($(filter undefined default,$(origin MAKECMDGOALS)),)
$(error MAKECMDGOALS may not be overridden)
endif
# MAKECMDGOALS is meaningful only to the current Make process. In particular,
# do not leak an empty automatic value into the bounded recursive default build,
# where it would look like an environment override and trip the guard above.
unexport MAKECMDGOALS
ifneq ($(filter $(CODEX_LIFECYCLE_GOALS),$(MAKECMDGOALS)),)
ifneq ($(firstword $(MAKECMDGOALS)),$(firstword $(filter $(CODEX_LIFECYCLE_GOALS),$(MAKECMDGOALS))))
$(error Usage: make $(firstword $(filter $(CODEX_LIFECYCLE_GOALS),$(MAKECMDGOALS))) <run-id>)
endif
ifneq ($(words $(MAKECMDGOALS)),2)
$(error Usage: make $(firstword $(MAKECMDGOALS)) <run-id>)
endif
override CODEX_MAKE_RUN_ID := $(word 2,$(MAKECMDGOALS))
override CODEX_MAKE_RUN_ID_DATE := $(word 1,$(subst t, ,$(CODEX_MAKE_RUN_ID)))
override CODEX_MAKE_RUN_ID_AFTER_T := $(word 2,$(subst t, ,$(CODEX_MAKE_RUN_ID)))
override CODEX_MAKE_RUN_ID_TIME := $(word 1,$(subst z, ,$(CODEX_MAKE_RUN_ID_AFTER_T)))
override CODEX_MAKE_RUN_ID_AFTER_Z := $(word 2,$(subst z, ,$(CODEX_MAKE_RUN_ID_AFTER_T)))
override CODEX_MAKE_RUN_ID_HEX := $(patsubst -%,%,$(CODEX_MAKE_RUN_ID_AFTER_Z))
override CODEX_MAKE_RUN_ID_RECONSTRUCTED := $(CODEX_MAKE_RUN_ID_DATE)t$(CODEX_MAKE_RUN_ID_TIME)z-$(CODEX_MAKE_RUN_ID_HEX)
override CODEX_MAKE_RUN_ID_INVALID := $(strip \
	$(call codex_make_strip_decimal,$(CODEX_MAKE_RUN_ID_DATE)) \
	$(if $(filter 8,$(call codex_make_character_count,$(CODEX_MAKE_RUN_ID_DATE))),,date-length) \
	$(call codex_make_strip_decimal,$(CODEX_MAKE_RUN_ID_TIME)) \
	$(if $(filter 6,$(call codex_make_character_count,$(CODEX_MAKE_RUN_ID_TIME))),,time-length) \
	$(call codex_make_strip_hex,$(CODEX_MAKE_RUN_ID_HEX)) \
	$(if $(filter 12,$(call codex_make_character_count,$(CODEX_MAKE_RUN_ID_HEX))),,hex-length) \
	$(subst $(CODEX_MAKE_RUN_ID_RECONSTRUCTED),,$(CODEX_MAKE_RUN_ID)))
$(if $(CODEX_MAKE_RUN_ID_INVALID),$(error invalid Triptych Codex run ID))
.DEFAULT:
	@:
endif

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
#   Python >= 3.10, stdlib (including fcntl/zoneinfo), IANA timezone data, and
#   the public renderer's version-locked third-party module:
#     python tzdata python-markdown (exact version in requirements-public-alpha.txt)
#   pdflatex, kpsewhich/kpathsea and every directly loaded class/package/font:
#     texlive-bin texlive-basic texlive-latex texlive-latexrecommended
#     texlive-latexextra texlive-pictures texlive-fontsrecommended
#     article, geometry, fontenc, inputenc, lmodern, microtype, array,
#     booktabs, longtable, tabularx, enumitem, needspace, multicol, xcolor,
#     hyperref, tcolorbox, tikz/PGF, pdflscape, ragged2e and titlesec
#   PDF metadata/text/raster and bounded PNG/contact-sheet processing:
#     poppler (pdfinfo, pdftotext, pdftoppm) and imagemagick (magick 7)
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
ARCH_WORKFLOW_PACKAGES := git github-cli openai-codex ripgrep
ARCH_DEPENDENCY_PACKAGES := $(ARCH_CORE_PACKAGES) $(ARCH_PYTHON_PACKAGES) \
	$(ARCH_TEX_PACKAGES) $(ARCH_PDF_PACKAGES) $(ARCH_WORKFLOW_PACKAGES)
ARCH_CANONICAL_COMMANDS := make:/usr/bin/make sh:/usr/bin/sh \
	env:/usr/bin/env id:/usr/bin/id find:/usr/bin/find sort:/usr/bin/sort \
	cmp:/usr/bin/cmp \
	cat:/usr/bin/cat chmod:/usr/bin/chmod cp:/usr/bin/cp install:/usr/bin/install \
	mkdir:/usr/bin/mkdir mv:/usr/bin/mv rm:/usr/bin/rm \
	sha256sum:/usr/bin/sha256sum python3:/usr/bin/python3 \
	pdflatex:/usr/bin/pdflatex kpsewhich:/usr/bin/kpsewhich \
	pdfinfo:/usr/bin/pdfinfo pdftotext:/usr/bin/pdftotext \
	pdftoppm:/usr/bin/pdftoppm magick:/usr/bin/magick git:/usr/bin/git \
	gh:/usr/bin/gh codex:/usr/bin/codex rg:/usr/bin/rg
ARCH_PACMAN ?= /usr/bin/pacman
ARCH_SUDO ?= /usr/bin/sudo
ARCH_ID ?= /usr/bin/id
ARCH_PYTHON ?= /usr/bin/python3
ARCH_OS_RELEASE ?= /etc/os-release

SOURCE_ROOT := src/$(PROVIDER)
BUILD_ROOT := build/$(PROVIDER)
DOC_ROOT := doc/$(PROVIDER)

MAIN_SOURCES := $(shell find $(SOURCE_ROOT) -type f -name main.tex | sort)
DOCUMENTS := $(patsubst $(SOURCE_ROOT)/%/main.tex,%,$(MAIN_SOURCES))
BUILD_PDFS := $(addprefix $(BUILD_ROOT)/,$(addsuffix .pdf,$(DOCUMENTS)))
BUILD_METADATA_STAMPS := $(addprefix $(BUILD_ROOT)/.metadata/,$(addsuffix .ok,$(DOCUMENTS)))
BUILD_METADATA_VERIFICATIONS := $(addprefix $(BUILD_ROOT)/.metadata/,$(addsuffix .verify,$(DOCUMENTS)))
DOC_PDFS := $(addprefix $(DOC_ROOT)/,$(addsuffix .pdf,$(DOCUMENTS)))
METADATA_CHECKER := scripts/check-generation-metadata
PDF_REVIEW_TOOL := scripts/pdf-review
PUBLIC_ALPHA_TOOL := scripts/public-alpha
CODEX_LAUNCHER := scripts/triptych-codex

COMMON_SOURCES := $(shell find $(SOURCE_ROOT)/common -type f | sort)
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

.DEFAULT_GOAL := all

# A top-level invocation without -j has no jobserver for document builds to
# share. Bootstrap aggregate builds with a bounded recursive Make in that case.
# If a caller already supplied -j (including an inherited jobserver), keep the
# complete graph in this Make process so combined goals cannot race one another.
MAKE_PARALLEL_FLAGS := $(filter -j% j% --jobs% --jobserver-auth=% --jobserver-fds=%,$(MAKEFLAGS))
PDF_JOBS_INVALID = $(strip \
	$(call codex_make_strip_decimal,$(PDF_JOBS)) \
	$(if $(strip $(PDF_JOBS)),,empty) \
	$(if $(subst 0,,$(strip $(PDF_JOBS))),,zero))
BOUNDED_PDF_JOB_OPTION = $(if $(strip $(MAKE_PARALLEL_FLAGS)),,\
	$(if $(PDF_JOBS_INVALID),$(error PDF_JOBS requires a positive integer),--jobs=$(PDF_JOBS)))

.PHONY: all pdf review-pdfs review-all-pdfs install list help clean \
	distclean check-tools check-metadata check-public-alpha prepare-public-alpha \
	check-pdf-review check-agent-isolation codex public-site public-preview \
	dependencies-arch install-dependencies-arch \
	verify-public-site verify-public-preview integrate resolve continue abort final-diff \
	FORCE_METADATA_VERIFICATION
.DELETE_ON_ERROR:
.SECONDARY: $(BUILD_METADATA_STAMPS)

ifeq ($(strip $(MAKE_PARALLEL_FLAGS)),)
all:
	+@$(MAKE) --no-print-directory $(BOUNDED_PDF_JOB_OPTION) pdf

review-pdfs:
	+@$(MAKE) --no-print-directory $(BOUNDED_PDF_JOB_OPTION) pdf
	@$(PYTHON) $(PDF_REVIEW_TOOL) --changed-against $(DOC_ROOT) $(BUILD_PDFS)

review-all-pdfs:
	+@$(MAKE) --no-print-directory $(BOUNDED_PDF_JOB_OPTION) pdf
	@$(PYTHON) $(PDF_REVIEW_TOOL) $(BUILD_PDFS)
else
all: pdf

review-pdfs: pdf
	@$(PYTHON) $(PDF_REVIEW_TOOL) --changed-against $(DOC_ROOT) $(BUILD_PDFS)

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

codex resolve: private export TRIPTYCH_CODEX_REAL := $(CODEX)

codex:
	@$(CODEX_LAUNCHER)

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

integrate resolve continue abort final-diff: private override export TRIPTYCH_MAKE_FIRST_GOAL := $(firstword $(MAKECMDGOALS))
integrate resolve continue abort final-diff: private override export TRIPTYCH_MAKE_RUN_ID := $(word 2,$(MAKECMDGOALS))
integrate resolve continue abort final-diff: private override CODEX_LAUNCHER := scripts/triptych-codex
integrate:
	@if [ "$$TRIPTYCH_MAKE_FIRST_GOAL" != integrate ]; then \
		printf '%s\n' 'Usage: make integrate <run-id>' >&2; \
		exit 2; \
	fi
	@$(CODEX_LAUNCHER) --triptych-integrate "$$TRIPTYCH_MAKE_RUN_ID"

resolve:
	@if [ "$$TRIPTYCH_MAKE_FIRST_GOAL" != resolve ]; then \
		printf '%s\n' 'Usage: make resolve <run-id>' >&2; \
		exit 2; \
	fi
	@$(CODEX_LAUNCHER) --triptych-resolve "$$TRIPTYCH_MAKE_RUN_ID"

continue:
	@if [ "$$TRIPTYCH_MAKE_FIRST_GOAL" != continue ]; then \
		printf '%s\n' 'Usage: make continue <run-id>' >&2; \
		exit 2; \
	fi
	@$(CODEX_LAUNCHER) --triptych-continue "$$TRIPTYCH_MAKE_RUN_ID"

abort:
	@if [ "$$TRIPTYCH_MAKE_FIRST_GOAL" != abort ]; then \
		printf '%s\n' 'Usage: make abort <run-id>' >&2; \
		exit 2; \
	fi
	@$(CODEX_LAUNCHER) --triptych-abort "$$TRIPTYCH_MAKE_RUN_ID"

final-diff:
	@if [ "$$TRIPTYCH_MAKE_FIRST_GOAL" != final-diff ]; then \
		printf '%s\n' 'Usage: make final-diff <run-id>' >&2; \
		exit 2; \
	fi
	@$(CODEX_LAUNCHER) --triptych-final-diff "$$TRIPTYCH_MAKE_RUN_ID"

check-agent-isolation:
	@$(PYTHON) -m unittest discover -s scripts/tests -p 'test_triptych_codex.py' -v

check-pdf-review:
	@$(PYTHON) -m unittest discover -s scripts/tests -p 'test_pdf_review.py' -v

help:
	@printf '%s\n' \
		'make          Build every document with at most $(PDF_JOBS) parallel jobs' \
		'make pdf      Build incrementally in the current Make jobserver' \
		'make review-pdfs  Build with at most $(PDF_JOBS) jobs, then raster changed PDFs' \
		'make review-all-pdfs  Build with at most $(PDF_JOBS) jobs, then raster every PDF' \
		'make install  Publish built PDFs into the mirrored tracked doc/ tree' \
		'make list     List discovered document IDs' \
		'make dependencies-arch  List canonical Arch package dependencies' \
		'make install-dependencies-arch  Run a full Arch upgrade and install canonical packages' \
		'make codex    Start Codex in an automatically isolated task checkout' \
		'make integrate <run-id>  Integrate a clean run or land an unchanged review-pending candidate' \
		'make resolve <run-id>  Open Codex to resolve and stage a managed rebase conflict' \
		'make continue <run-id>  Continue staged resolutions to a review-pending candidate' \
		'make abort <run-id>  Abort a managed rebase and restore its exact audited source' \
		'make final-diff <run-id>  Show the complete review-pending diff without a worktree path' \
		'Lifecycle Make wrappers require a launcher-produced ID; use scripts/triptych-codex directly for external input' \
		'make check-agent-isolation  Test the transparent Codex launcher' \
		'make check-pdf-review  Test memory-bounded PDF inspection tooling' \
		'make check-metadata  Validate structured and inherited AI provenance' \
		'make check-public-alpha  Validate the exhaustive public-release policy' \
		'make prepare-public-alpha  Print current candidate hashes; grants no approval' \
		'make public-preview  Build a private no-index preview with review candidates' \
		'make public-site  Build the fail-closed, history-free public artifact' \
		'make verify-public-preview  Recheck the existing private preview artifact' \
		'make verify-public-site  Recheck the existing public artifact' \
		'make clean    Remove transient build artifacts only'

check-metadata: check-tools
	@$(METADATA_CHECKER) --provider $(PROVIDER)

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
	cd $(SOURCE_ROOT) && $(PDFLATEX) -interaction=nonstopmode -halt-on-error -jobname=$(notdir $*) -output-directory=$(abspath $(@D)) $*/main.tex
	cd $(SOURCE_ROOT) && $(PDFLATEX) -interaction=nonstopmode -halt-on-error -jobname=$(notdir $*) -output-directory=$(abspath $(@D)) $*/main.tex
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
$(NOVENA_BUILD_PDFS): $(NOVENA_SHARED)
$(BIOGRAPHY_BUILD_PDFS): $(BIOGRAPHY_SHARED)
$(HISTORICAL_TRANSLATION_BUILD_PDFS): $(HISTORICAL_TRANSLATION_SHARED)
$(PARISH_HISTORY_BUILD_PDFS): $(PARISH_HISTORY_SHARED)
$(TRADITIONAL_INSTITUTE_BUILD_PDFS): $(TRADITIONAL_INSTITUTE_SHARED)
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
