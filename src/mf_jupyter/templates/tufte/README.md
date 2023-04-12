Latex/Tufte template for nbconvert 6
====================================

This template works with the version 6 of nbconvert. 
(The API changed generating incompatibility with 5.x)

Structure
---------

This is the structure and dependencies of the template

* index.tex.j2: contains the tufte definitions (default)

`index` <-- `base` <-- `document_contents` <-- `display_priority` <-- `null`


Usage 
-----

Below an example of script

```bash
#!/bin/bash
MF_JUPYTER="../"
INPUT_NOTEBOOK="vstprep.ipynb"
DOCNAME="${INPUT_NOTEBOOK%.*}"
TEMPLATE="tufte"

TEXCOMPILER="pdflatex"
BIBCOMPILER="bibtex"
TEXOPTIONS="-enable-write18 -shell-escape -interaction=nonstopmode"
TEXADDLIBS="${MF_JUPYTER}/texlibs:"

jupyter nbconvert \
        --config=${MF_JUPYTER}/config.py --to=latex --template=${TEMPLATE} \
        --TemplateExporter.extra_template_basedirs=${MF_JUPYTER}/templates \
        ${INPUT_NOTEBOOK}

TEXINPUTS="${TEXADDLIBS}" ${TEXCOMPILER} ${TEXOPTIONS} ${DOCNAME}.tex
${BIBCOMPILER} ${DOCNAME}
TEXINPUTS="${TEXADDLIBS}" ${TEXCOMPILER} ${TEXOPTIONS} ${DOCNAME}.tex
TEXINPUTS="${TEXADDLIBS}" ${TEXCOMPILER} ${TEXOPTIONS} ${DOCNAME}.tex
```

using latexmk

```bash
#!/bin/bash
MF_JUPYTER="../"
INPUT_NOTEBOOK="vstprep.ipynb"
DOCNAME="${INPUT_NOTEBOOK%.*}"
TEMPLATE="dpac"

# additional libraries
TEXADDLIBS="${MF_JUPYTER}/texlibs:"

# USE latexmk
TEXCOMPILER="latexmk"
TEXOPTIONS="-enable-write18 -shell-escape -interaction=nonstopmode" -f -pdf

jupyter nbconvert \
        --config=${MF_JUPYTER}/config.py --to=latex --template=${TEMPLATE} \
        --TemplateExporter.extra_template_basedirs=${MF_JUPYTER}/templates \
        ${INPUT_NOTEBOOK}

# latexmk
TEXINPUTS="${TEXADDLIBS}" ${TEXCOMPILER} ${TEXOPTIONS} ${DOCNAME}
