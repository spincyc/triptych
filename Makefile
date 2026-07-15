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
FIRST_NOVENA_ROOT := $(NOVENA_ROOT)/00-ascension-to-pentecost
CARMEL_NOVENA_ROOT := $(NOVENA_ROOT)/10-our-lady-of-mount-carmel
FIRST_NOVENA_PRAYERS := $(wildcard $(FIRST_NOVENA_ROOT)/prayers/*.tex)
CARMEL_NOVENA_PRAYERS := $(wildcard $(CARMEL_NOVENA_ROOT)/prayers/*.tex)

.PHONY: all pdf install list help clean distclean check-tools check-metadata \
	check-public-alpha public-site public-preview verify-public-site verify-public-preview
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

help:
	@printf '%s\n' \
		'make          Build every discovered src/$(PROVIDER)/**/main.tex document' \
		'make install  Publish built PDFs into the mirrored tracked doc/ tree' \
		'make list     List discovered document IDs' \
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
$(NOVENA_BUILD_PDFS): $(NOVENA_SHARED)
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
