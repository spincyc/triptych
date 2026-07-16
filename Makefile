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
INTEGRATE_RUN_ID := $(word 2,$(MAKECMDGOALS))

# These lifecycle commands present the run ID as a second Make goal. Limit the
# fallback rule to those invocations so ordinary unknown targets still fail.
ifneq ($(filter $(firstword $(MAKECMDGOALS)),integrate resolve continue abort),)
.DEFAULT:
	@:
endif

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
	verify-public-site verify-public-preview integrate resolve continue abort
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

integrate: export TRIPTYCH_MAKE_FIRST_GOAL := $(firstword $(MAKECMDGOALS))
integrate: export TRIPTYCH_MAKE_INTEGRATE_RUN_ID := $(INTEGRATE_RUN_ID)
integrate:
	@if [ "$$TRIPTYCH_MAKE_FIRST_GOAL" != integrate ] || [ "$(words $(MAKECMDGOALS))" -ne 2 ]; then \
		printf '%s\n' 'Usage: make integrate <run-id>' >&2; \
		exit 2; \
	fi
	@$(CODEX_LAUNCHER) --triptych-integrate "$$TRIPTYCH_MAKE_INTEGRATE_RUN_ID"

resolve: export TRIPTYCH_MAKE_FIRST_GOAL := $(firstword $(MAKECMDGOALS))
resolve: export TRIPTYCH_MAKE_RESOLVE_RUN_ID := $(INTEGRATE_RUN_ID)
resolve:
	@if [ "$$TRIPTYCH_MAKE_FIRST_GOAL" != resolve ] || [ "$(words $(MAKECMDGOALS))" -ne 2 ]; then \
		printf '%s\n' 'Usage: make resolve <run-id>' >&2; \
		exit 2; \
	fi
	@$(CODEX_LAUNCHER) --triptych-resolve "$$TRIPTYCH_MAKE_RESOLVE_RUN_ID"

continue: export TRIPTYCH_MAKE_FIRST_GOAL := $(firstword $(MAKECMDGOALS))
continue: export TRIPTYCH_MAKE_CONTINUE_RUN_ID := $(INTEGRATE_RUN_ID)
continue:
	@if [ "$$TRIPTYCH_MAKE_FIRST_GOAL" != continue ] || [ "$(words $(MAKECMDGOALS))" -ne 2 ]; then \
		printf '%s\n' 'Usage: make continue <run-id>' >&2; \
		exit 2; \
	fi
	@$(CODEX_LAUNCHER) --triptych-continue "$$TRIPTYCH_MAKE_CONTINUE_RUN_ID"

abort: export TRIPTYCH_MAKE_FIRST_GOAL := $(firstword $(MAKECMDGOALS))
abort: export TRIPTYCH_MAKE_ABORT_RUN_ID := $(INTEGRATE_RUN_ID)
abort:
	@if [ "$$TRIPTYCH_MAKE_FIRST_GOAL" != abort ] || [ "$(words $(MAKECMDGOALS))" -ne 2 ]; then \
		printf '%s\n' 'Usage: make abort <run-id>' >&2; \
		exit 2; \
	fi
	@$(CODEX_LAUNCHER) --triptych-abort "$$TRIPTYCH_MAKE_ABORT_RUN_ID"

check-agent-isolation:
	@$(PYTHON) -m unittest discover -s scripts/tests -p 'test_triptych_codex.py' -v

help:
	@printf '%s\n' \
		'make          Build every discovered src/$(PROVIDER)/**/main.tex document' \
		'make install  Publish built PDFs into the mirrored tracked doc/ tree' \
		'make list     List discovered document IDs' \
		'make codex    Start Codex in an automatically isolated task checkout' \
		'make integrate <run-id>  Rebase if needed, fast-forward, and clean an approved run' \
		'make resolve <run-id>  Open the fixed stage-only resolver for a retained conflict' \
		'make continue <run-id>  Continue a retained integration rebase' \
		'make abort <run-id>  Abort a retained integration rebase' \
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
