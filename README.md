# mf Jupyter: Notebook with my suite to easy latex conversion
=============================================================

A package to offer tools to create and convert a notebook into TeX files for further publications (e.g., articles, notes).

This package provides a collection of tools to automate validation procedures in the CU8 activities.

This version relies on `nbconvert >= 6.0`


## Manual command

```bash
jupyter nbconvert \
	--config=config.py --to=latex --template=tufte \
	--TemplateExporter.extra_template_basedirs=${PWD}/templates \
	examples/vstprep.ipynb --debug
```

## Notebook content and meta data

The furnished template contains a few blocks as examples. There are only a few options that are used for converting a notebook. These options are always set through the `metadata` that one can access through the toolbar on each cell. If the toolbar is not visible, use the menu `View > Cell Toolbar > Edit Metadata`.

## Recognized metadata keywords
* `hide`     : set to `true` will tell the converter to skip the cell
* `abstract` : set to indicate to the converter that this cell contains the abstract block content.  (`\begin{abstract} ... \end{abstract}`)

.. note::

   More keywords will be soon available.

## Python tools

To simplify the interface between python notebook and Latex, `mf_jupyter` provides some tools, such as making captions for figures with labels and the pdf associated export. But also some other neat tools. Below is a list of functions (use the Python `help` to know more)

* `Acknowledgements`     : Allows to use text as acknowledgments using the proper environment.
* `AppendixMark`         : set the appendix begin mark
* `LatexFigure`          : generate a caption (with a label) to go with a figure. This will also save the figure to a file (pdf by default) to be included as a floating figure in the latex file
* `LatexNumberFormatter` : formats numbers into scientific notations using Latex representation.
* `LatexSubfigures`      : takes a list of Python figures to create a single floating figure in latex with optional captions per sub-figure.
* `Matrix`               : creates a Latex matrix text that can be used as markdown and in latex.
* `Table`                : Makes a table into a latex table format.
* `add_citation_button`  : add a button in the notebook toolbar to generate Bibtex reference from bibcode.
* `add_hide_button`      : add a button to the cell toolbar to allow a quick set or unset on `hide` metadata. `View > Cell Toolbar > mf_jupyter`.
* `add_input_toggle`     : add a button in the notebook toolbar to hide codes and only keep text and outputs/figures visible.


## Avaiblable templates

All templates are usable with make using their name, for example, `make mnras`.

### Specific
* `dpac`  : Gaia DPAC technical note template
* `tufte` : Tufte handsout conversion

### Journals
* `aa`    : Astronomy & Astrophysics format
* `apj`   : convert into ApJ format
* `mnras` : convert into MNRAS format


## Virtual Environment instead

python has now a built-in virtual environment that can be used similarly to `conda`.

```shell
python -m venv --prompt cu8val venv
source venv/bin/activate
pip install --upgrade pip
pip install .
```
