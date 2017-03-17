MF_JUPYTER_DIR=$(shell echo `python -c "import mf_jupyter; print(mf_jupyter.get_package_path())"`)
CONFIG=config.py
NBCONVERT=jupyter nbconvert
LATEXOPTS=--to latex --config ${MF_JUPYTER_DIR}/config.py
TEMPLATEOPTS=--template ${MF_JUPYTER_DIR}/templates
.PHONY: clean all 

default:
	@echo ${SOURCE}
	@echo "Usage: SOURCE=<documentname> make "

all: tufte pdf

apj:
	${NBCONVERT}  ${LATEXOPTS} ${SOURCE}.ipynb ${TEMPLATEOPTS}/mf_emulateapj.tplx;

tufte:
	${NBCONVERT} ${LATEXOPTS} ${SOURCE}.ipynb ${TEMPLATEOPTS}/mf_tufte.tplx;

mnras:
	${NBCONVERT} ${LATEXOPTS} ${SOURCE}.ipynb ${TEMPLATEOPTS}/mf_mnras.tplx;

aa:
	${NBCONVERT} ${LATEXOPTS} ${SOURCE}.ipynb ${TEMPLATEOPTS}/mf_aa.tplx;

dpac:
	${NBCONVERT} ${LATEXOPTS} ${SOURCE}.ipynb ${TEMPLATEOPTS}/mf_dpac.tplx;

pdf:
	pdflatex ${SOURCE}; bibtex ${SOURCE}; pdflatex ${SOURCE}; pdflatex ${SOURCE}

html:
	${NBCONVERT} --to html ${SOURCE}.ipynb

clean:
	rm -f *.dvi *.aux *.bbl *.blg *.log *.toc *.lot *.lof *.cb *.bak *.out
