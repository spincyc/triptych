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
ifneq ($(origin MAKECMDGOALS),default)
$(error MAKECMDGOALS may not be overridden)
endif
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

SOURCE_ROOT := src/$(PROVIDER)
BUILD_ROOT := build/$(PROVIDER)
DOC_ROOT := doc/$(PROVIDER)

MAIN_SOURCES := $(shell find $(SOURCE_ROOT) -type f -name main.tex | sort)
DOCUMENTS := $(patsubst $(SOURCE_ROOT)/%/main.tex,%,$(MAIN_SOURCES))
BUILD_PDFS := $(addprefix $(BUILD_ROOT)/,$(addsuffix .pdf,$(DOCUMENTS)))
DOC_PDFS := $(addprefix $(DOC_ROOT)/,$(addsuffix .pdf,$(DOCUMENTS)))
METADATA_CHECKER := scripts/check-generation-metadata
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
POSTCONCILIAR_US_BUILD_PDFS := $(filter $(BUILD_ROOT)/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/%,$(BUILD_PDFS))
BIOGRAPHY_ROOT := $(SOURCE_ROOT)/biographies
BIOGRAPHY_SHARED := $(wildcard $(BIOGRAPHY_ROOT)/shared/*.tex)
BIOGRAPHY_BUILD_PDFS := $(filter $(BUILD_ROOT)/biographies/%,$(BUILD_PDFS))
HISTORICAL_TRANSLATION_ROOT := $(SOURCE_ROOT)/history/biblical-translations
HISTORICAL_TRANSLATION_SHARED := $(HISTORICAL_TRANSLATION_ROOT)/account-format.tex
HISTORICAL_TRANSLATION_BUILD_PDFS := $(filter $(BUILD_ROOT)/history/biblical-translations/%,$(BUILD_PDFS))
FIRST_NOVENA_ROOT := $(NOVENA_ROOT)/00-ascension-to-pentecost
CARMEL_NOVENA_ROOT := $(NOVENA_ROOT)/10-our-lady-of-mount-carmel
FIRST_NOVENA_PRAYERS := $(wildcard $(FIRST_NOVENA_ROOT)/prayers/*.tex)
CARMEL_NOVENA_PRAYERS := $(wildcard $(CARMEL_NOVENA_ROOT)/prayers/*.tex)

.PHONY: all pdf install list help clean distclean check-tools check-metadata \
	check-public-alpha check-agent-isolation codex public-site public-preview \
	verify-public-site verify-public-preview integrate resolve continue abort final-diff
.DELETE_ON_ERROR:

all: pdf

pdf: check-metadata $(BUILD_PDFS)
	@for document in $(DOCUMENTS); do \
		$(METADATA_CHECKER) --provider $(PROVIDER) --pdf "$$document" "$(BUILD_ROOT)/$$document.pdf"; \
	done

install: check-metadata $(DOC_PDFS)
	@for document in $(DOCUMENTS); do \
		$(METADATA_CHECKER) --provider $(PROVIDER) --pdf "$$document" "$(DOC_ROOT)/$$document.pdf"; \
		cmp -s "$(BUILD_ROOT)/$$document.pdf" "$(DOC_ROOT)/$$document.pdf" || { echo "Installed PDF differs from reviewed build: $$document"; exit 1; }; \
	done

list:
	@printf '%s\n' $(DOCUMENTS)

codex:
	@$(CODEX_LAUNCHER)

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

help:
	@printf '%s\n' \
		'make          Build every discovered src/$(PROVIDER)/**/main.tex document' \
		'make install  Publish built PDFs into the mirrored tracked doc/ tree' \
		'make list     List discovered document IDs' \
		'make codex    Start Codex in an automatically isolated task checkout' \
		'make integrate <run-id>  Integrate a clean run or land an unchanged review-pending candidate' \
		'make resolve <run-id>  Open Codex to resolve and stage a managed rebase conflict' \
		'make continue <run-id>  Continue staged resolutions to a review-pending candidate' \
		'make abort <run-id>  Abort a managed rebase and restore its exact audited source' \
		'make final-diff <run-id>  Show the complete review-pending diff without a worktree path' \
		'Lifecycle Make wrappers require a launcher-produced ID; use scripts/triptych-codex directly for external input' \
		'make check-agent-isolation  Test the transparent Codex launcher' \
		'make check-metadata  Validate structured and inherited AI provenance' \
		'make check-public-alpha  Validate the exhaustive public-release policy' \
		'make public-preview  Build a private no-index preview with review candidates' \
		'make public-site  Build the fail-closed, history-free public artifact' \
		'make verify-public-preview  Recheck the existing private preview artifact' \
		'make verify-public-site  Recheck the existing public artifact' \
		'make clean    Remove transient build artifacts only'

check-metadata: check-tools
	@$(METADATA_CHECKER) --provider $(PROVIDER)

check-public-alpha:
	@$(PYTHON) $(PUBLIC_ALPHA_TOOL) check

public-preview:
	@$(PYTHON) $(PUBLIC_ALPHA_TOOL) build --preview

public-site:
	@$(PYTHON) $(PUBLIC_ALPHA_TOOL) build

verify-public-preview:
	@$(PYTHON) $(PUBLIC_ALPHA_TOOL) verify --preview

verify-public-site:
	@$(PYTHON) $(PUBLIC_ALPHA_TOOL) verify

# Register every file owned by a document leaf as a dependency without requiring
# a flat manifest. Cross-document shared fragments are declared separately below.
define REGISTER_DOCUMENT_SOURCES
$(BUILD_ROOT)/$(1).pdf: $(shell find $(SOURCE_ROOT)/$(1) -type f | sort)
endef
$(foreach document,$(DOCUMENTS),$(eval $(call REGISTER_DOCUMENT_SOURCES,$(document))))

$(BUILD_ROOT)/%.pdf: $(SOURCE_ROOT)/%/main.tex $(COMMON_SOURCES) $(METADATA_CHECKER) | check-metadata
	@mkdir -p $(@D)
	cd $(SOURCE_ROOT) && $(PDFLATEX) -interaction=nonstopmode -halt-on-error -jobname=$(notdir $*) -output-directory=$(abspath $(@D)) $*/main.tex
	cd $(SOURCE_ROOT) && $(PDFLATEX) -interaction=nonstopmode -halt-on-error -jobname=$(notdir $*) -output-directory=$(abspath $(@D)) $*/main.tex
	@$(METADATA_CHECKER) --provider $(PROVIDER) --pdf '$*' '$@'

$(BUILD_ROOT)/theology/sacraments-at-a-glance.pdf: $(SACRAMENT_SHARED) $(SACRAMENT_INITIATION_TABLE)
$(BUILD_ROOT)/liturgy/roman-rite/1962/propers/ritual/m01-nuptial-mass.pdf: \
	$(SACRAMENT_ROOT)/summary-preamble.tex \
	$(SACRAMENT_ROOT)/summaries/matrimony.tex
$(POSTCONCILIAR_US_BUILD_PDFS): $(POSTCONCILIAR_US_FORMAT)
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
$(BUILD_ROOT)/devotions/novenas/00-ascension-to-pentecost-daily-prayer.pdf: \
	$(FIRST_NOVENA_PRAYERS) \
	$(FIRST_NOVENA_ROOT)/generation-metadata.tex
$(BUILD_ROOT)/devotions/novenas/10-our-lady-of-mount-carmel-daily-prayer.pdf: \
	$(CARMEL_NOVENA_PRAYERS) \
	$(CARMEL_NOVENA_ROOT)/generation-metadata.tex

$(DOC_ROOT)/%.pdf: $(BUILD_ROOT)/%.pdf | check-metadata
	@mkdir -p $(@D)
	install -m 0644 $< $@

check-tools:
	@command -v $(PDFLATEX) >/dev/null || { echo "Missing $(PDFLATEX)"; exit 1; }
	@command -v python3 >/dev/null || { echo "Missing python3"; exit 1; }
	@command -v pdftotext >/dev/null || { echo "Missing pdftotext"; exit 1; }
	@command -v pdfinfo >/dev/null || { echo "Missing pdfinfo"; exit 1; }

clean:
	rm -rf build

distclean: clean
