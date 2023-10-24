""" This module generate commandlines to run the conversions and provides a single function to convert a notebook
"""
import os
import pkg_resources
from typing import List


def _get_nbconvert_cmd(
    notebook_path: str, template: str = "tufte", debug: bool = True
) -> str:
    """Get commandline to run nbconvert

    Parameters
    ----------
    notebook_path: str
        path to notebook to convert
    template: str
        name of the template to use
    debug: bool
        set to True to enable debug mode of nbconvert

    Returns
    -------
    cmd: str
        the commandline to run nbconvert
    """
    mf_nbconvert_pkg_path = os.path.abspath(
        os.path.join(pkg_resources.resource_filename("mf_jupyter", "nbconvert"))
    )
    config = os.path.join(mf_nbconvert_pkg_path, "config.py")
    templates_dir = os.path.join(mf_nbconvert_pkg_path, "templates")

    args = [
        """jupyter nbconvert """,
        f"""--config={config:s}""",
        """--to=latex""",
        f"""--template={template:s}""",
        f"""--TemplateExporter.extra_template_basedirs={templates_dir:s}""",
        f"""{notebook_path:s}""",
    ]

    if debug:
        args.append("--debug")

    return " ".join(args)


def _get_pdflatex_cmd(
    latexfile_path: str,
    texdirs: List[str] = [],
) -> str:
    """Get commandline to run pdflatex

    Parameters
    ----------
    latexfile_path: str
        path to latex file to convert
    texdirs: list[str]
        optional directories to include for latex

    Returns
    -------
    cmd: str
        the commandline to run pdflatex
    """
    mf_nbconvert_pkg_path = os.path.abspath(
        os.path.join(pkg_resources.resource_filename("mf_jupyter", "nbconvert"))
    )
    TEXMFLOCAL = os.path.join(mf_nbconvert_pkg_path, "texlibs", "texmf//")
    PDFLATEX = f"pdflatex -enable-write18 -shell-escape -interaction=nonstopmode"

    TEXEXPORTS = [f"{TEXMFLOCAL:s}"]
    if texdirs:
        for k in texdirs:
            if k[-2] != "//":  # add anything recurrently
                TEXEXPORTS.append(k + "//")
            else:
                TEXEXPORTS.append(k)

    TEXEXPORTS = ":".join(TEXEXPORTS)

    cmd = f"""export TEXINPUTS=.:{TEXEXPORTS:s}:
    {PDFLATEX:s} {latexfile_path:s}"""

    return cmd


def _get_bibtex_cmd(
    latexfile_path: str,
    texdirs: List[str] = [],
) -> str:
    """Get commandline to run bibtex

    Parameters
    ----------
    latexfile_path: str
        path to latex file to convert
    texdirs: list[str]
        optional directories to include for latex

    Returns
    -------
    cmd: str
        the commandline to run pdflatex
    """
    mf_nbconvert_pkg_path = os.path.abspath(
        os.path.join(pkg_resources.resource_filename("mf_jupyter", "nbconvert"))
    )
    TEXMFLOCAL = os.path.join(mf_nbconvert_pkg_path, "texlibs", "texmf//")
    BIBTEX = f"bibtex"

    TEXEXPORTS = [f"{TEXMFLOCAL:s}"]
    if texdirs:
        for k in texdirs:
            if k[-2] != "//":  # add anything recurrently
                TEXEXPORTS.append(k + "//")
            else:
                TEXEXPORTS.append(k)

    TEXEXPORTS = ":".join(TEXEXPORTS)

    # bibtex can raise issues when no bib file or no citations etc.
    # This is not so useful here. We bypass the exit status.
    cmd = f"""export BSTINPUTS=.:{TEXEXPORTS:s}:
    {BIBTEX:s} {latexfile_path:s} || true"""

    return cmd


def convert_notebook(
    filename: str, template: str = "tufte", silent: bool = True, texdirs: list = []
):
    """This function compiles a notebook into a DPAC latex document and its PDF.

    Parameters
    ----------
    filename: str
        name of the notebook without extension

    template: str
        mf_jupyter template to use

    silent: bool
        do not show the stdout/stderr of the compilation if set.

    texdirs: list[str]
        optional directories to include for latex
    """
    from subprocess import Popen, PIPE, STDOUT

    def run_command(cmd, stepname=""):
        if not silent:
            print("\n", cmd, "\n")
        with Popen(
            cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True
        ) as p:
            for line in p.stdout:
                if not silent:
                    print(line.decode().rstrip())
                # else:
                #    print(".", end="")
            if p.poll() != 0:
                raise RuntimeError(f"{stepname} step failed. Command line was \n {cmd}")
            print(f"step {stepname}: ", "success" if int(p.poll()) == 0 else "fail")

    # Make sure we have a filename without extension
    filename = filename.replace(".ipynb", "")

    # step 1: convert notebook to latex
    cmd = _get_nbconvert_cmd(filename, template=template, debug=~silent)
    run_command(cmd, stepname="nbconvert")

    # step 2: convert latex to pdf
    pdflatex_cmd = _get_pdflatex_cmd(filename, texdirs=texdirs).replace("\n", "; ")
    run_command(pdflatex_cmd, stepname="pdflatex")

    # step 3: bibtex
    bibtex_cmd = _get_bibtex_cmd(filename, texdirs=texdirs).replace("\n", "; ")
    run_command(bibtex_cmd, stepname="bibtex")

    # step 4: rerun pdflatex
    run_command(pdflatex_cmd, stepname="pdflatex")
    run_command(pdflatex_cmd, stepname="pdflatex")

    print(f"\nconversion finished. Check {filename:s}.pdf")
