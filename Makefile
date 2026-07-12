PDFLATEX ?= pdflatex

SOURCE_ROOT := src/gpt
BUILD_ROOT := build/gpt
DOC_ROOT := doc/gpt

DOCUMENTS := \
	15-trinity-sunday \
	16-second-after-pentecost \
	17-third-after-pentecost \
	18-fourth-after-pentecost \
	19-fifth-after-pentecost \
	20-sixth-after-pentecost \
	21-seventh-after-pentecost \
	sacraments-at-a-glance \
	sacraments

BUILD_PDFS := $(addprefix $(BUILD_ROOT)/,$(addsuffix .pdf,$(DOCUMENTS)))
DOC_PDFS := $(addprefix $(DOC_ROOT)/,$(addsuffix .pdf,$(DOCUMENTS)))
COMMON := $(SOURCE_ROOT)/common/preamble.tex
SACRAMENT_SUMMARIES := $(wildcard $(SOURCE_ROOT)/sacraments/summaries/*.tex)
SACRAMENT_SOURCES := $(wildcard \
	$(SOURCE_ROOT)/sacraments/*.tex \
	$(SOURCE_ROOT)/sacraments/fragments/*.tex \
	$(SOURCE_ROOT)/sacraments/sections/*.tex) \
	$(SACRAMENT_SUMMARIES)
AT_A_GLANCE_SOURCES := \
	$(SOURCE_ROOT)/sacraments/summary-preamble.tex \
	$(SOURCE_ROOT)/sacraments/fragments/full-matrix.tex \
	$(SOURCE_ROOT)/sacraments/fragments/lexicon.tex \
	$(SOURCE_ROOT)/sacraments/sections/14-churches-initiation.tex \
	$(SACRAMENT_SUMMARIES)

.PHONY: all pdf install clean distclean check-tools
.DELETE_ON_ERROR:

all: pdf

pdf: $(BUILD_PDFS)

install: $(DOC_PDFS)

$(BUILD_ROOT) $(DOC_ROOT):
	mkdir -p $@

$(BUILD_ROOT)/%.pdf: $(SOURCE_ROOT)/%/main.tex $(COMMON) | $(BUILD_ROOT)
	@command -v $(PDFLATEX) >/dev/null || { echo "Missing $(PDFLATEX)"; exit 1; }
	cd $(SOURCE_ROOT) && $(PDFLATEX) -interaction=nonstopmode -halt-on-error -jobname=$* -output-directory=$(abspath $(BUILD_ROOT)) $*/main.tex
	cd $(SOURCE_ROOT) && $(PDFLATEX) -interaction=nonstopmode -halt-on-error -jobname=$* -output-directory=$(abspath $(BUILD_ROOT)) $*/main.tex

$(BUILD_ROOT)/sacraments.pdf: $(SACRAMENT_SOURCES)
$(BUILD_ROOT)/sacraments-at-a-glance.pdf: $(AT_A_GLANCE_SOURCES)

$(DOC_ROOT)/%.pdf: $(BUILD_ROOT)/%.pdf | $(DOC_ROOT)
	install -m 0644 $< $@

check-tools:
	@command -v $(PDFLATEX) >/dev/null || { echo "Missing $(PDFLATEX)"; exit 1; }

clean:
	rm -rf build

distclean: clean
