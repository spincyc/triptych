PDFLATEX ?= pdflatex

WEEKS := \
	01-trinity-sunday \
	02-second-after-pentecost \
	03-third-after-pentecost \
	04-fourth-after-pentecost \
	05-fifth-after-pentecost \
	06-sixth-after-pentecost \
	07-seventh-after-pentecost

PDFS := $(addprefix build/,$(addsuffix .pdf,$(WEEKS)))
COMMON := common/preamble.tex

.PHONY: all pdf clean distclean check-tools

all: pdf

pdf: $(PDFS)

build:
	mkdir -p build

build/%.pdf: %/main.tex $(COMMON) | build
	$(PDFLATEX) -interaction=nonstopmode -halt-on-error -output-directory=build $<
	$(PDFLATEX) -interaction=nonstopmode -halt-on-error -output-directory=build $<
	mv build/main.pdf $@

check-tools:
	@command -v $(PDFLATEX) >/dev/null || { echo "Missing $(PDFLATEX)"; exit 1; }

clean:
	rm -f build/*.aux build/*.log build/*.out build/*.toc

distclean: clean
	rm -f $(PDFS)
