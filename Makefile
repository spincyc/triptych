PDFLATEX ?= pdflatex
PROVIDER ?= gpt

SOURCE_ROOT := src/$(PROVIDER)
BUILD_ROOT := build/$(PROVIDER)
DOC_ROOT := doc/$(PROVIDER)

MAIN_SOURCES := $(shell find $(SOURCE_ROOT) -type f -name main.tex | sort)
DOCUMENTS := $(patsubst $(SOURCE_ROOT)/%/main.tex,%,$(MAIN_SOURCES))
BUILD_PDFS := $(addprefix $(BUILD_ROOT)/,$(addsuffix .pdf,$(DOCUMENTS)))
DOC_PDFS := $(addprefix $(DOC_ROOT)/,$(addsuffix .pdf,$(DOCUMENTS)))

COMMON_SOURCES := $(shell find $(SOURCE_ROOT)/common -type f | sort)
SACRAMENT_ROOT := $(SOURCE_ROOT)/theology/sacraments
SACRAMENT_SHARED := \
	$(SACRAMENT_ROOT)/summary-preamble.tex \
	$(wildcard $(SACRAMENT_ROOT)/fragments/*.tex) \
	$(wildcard $(SACRAMENT_ROOT)/summaries/*.tex)
SACRAMENT_INITIATION_TABLE := $(SACRAMENT_ROOT)/sections/14-churches-initiation.tex

.PHONY: all pdf install list help clean distclean check-tools
.DELETE_ON_ERROR:

all: pdf

pdf: $(BUILD_PDFS)

install: $(DOC_PDFS)

list:
	@printf '%s\n' $(DOCUMENTS)

help:
	@printf '%s\n' \
		'make          Build every discovered src/$(PROVIDER)/**/main.tex document' \
		'make install  Publish built PDFs into the mirrored tracked doc/ tree' \
		'make list     List discovered document IDs' \
		'make clean    Remove transient build artifacts only'

# Register every file owned by a document leaf as a dependency without requiring
# a flat manifest. Cross-document shared fragments are declared separately below.
define REGISTER_DOCUMENT_SOURCES
$(BUILD_ROOT)/$(1).pdf: $(shell find $(SOURCE_ROOT)/$(1) -type f | sort)
endef
$(foreach document,$(DOCUMENTS),$(eval $(call REGISTER_DOCUMENT_SOURCES,$(document))))

$(BUILD_ROOT)/%.pdf: $(SOURCE_ROOT)/%/main.tex $(COMMON_SOURCES)
	@mkdir -p $(@D)
	@command -v $(PDFLATEX) >/dev/null || { echo "Missing $(PDFLATEX)"; exit 1; }
	cd $(SOURCE_ROOT) && $(PDFLATEX) -interaction=nonstopmode -halt-on-error -jobname=$(notdir $*) -output-directory=$(abspath $(@D)) $*/main.tex
	cd $(SOURCE_ROOT) && $(PDFLATEX) -interaction=nonstopmode -halt-on-error -jobname=$(notdir $*) -output-directory=$(abspath $(@D)) $*/main.tex

$(BUILD_ROOT)/theology/sacraments-at-a-glance.pdf: $(SACRAMENT_SHARED) $(SACRAMENT_INITIATION_TABLE)
$(BUILD_ROOT)/liturgy/roman-rite/1962/propers/ritual/m01-nuptial-mass.pdf: \
	$(SACRAMENT_ROOT)/summary-preamble.tex \
	$(SACRAMENT_ROOT)/summaries/matrimony.tex

$(DOC_ROOT)/%.pdf: $(BUILD_ROOT)/%.pdf
	@mkdir -p $(@D)
	install -m 0644 $< $@

check-tools:
	@command -v $(PDFLATEX) >/dev/null || { echo "Missing $(PDFLATEX)"; exit 1; }

clean:
	rm -rf build

distclean: clean
