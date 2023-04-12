""" This module generate commandlines to run the conversions and provides a single function to convert a notebook
"""
import os
import pkg_resources
from typing import List


def _get_nbconvert_cmd(notebook_path: str,
                       template: str = 'tufte',
                       debug: bool = True) -> str:
    """ Get commandline to run nbconvert

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
    config = os.path.abspath(pkg_resources.resource_filename('mf_jupyter', 'config.py'))
    templates_dir = os.path.abspath(pkg_resources.resource_filename('mf_jupyter', 'templates'))

    args = [
        """jupyter nbconvert """,
        f"""--config={config:s}""",
        """--to=latex""",
        f"""--template={template:s}""",
        f"""--TemplateExporter.extra_template_basedirs={templates_dir:s}""",
        f"""{notebook_path:s}"""]

    if debug:
        args.append('--debug')

    return ' '.join(args)

def _get_pdflatex_cmd(latexfile_path: str,
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
    TEXMFLOCAL = os.path.join(
                        os.path.abspath(pkg_resources.resource_filename('mf_jupyter', 'texlibs')),
                        'texmf//')
    PDFLATEX = f"pdflatex -enable-write18 -shell-escape -interaction=nonstopmode"

    TEXEXPORTS = [f"{TEXMFLOCAL:s}"]
    if texdirs:
        for k in texdirs:
            if k[-2] != '//': #add anything recurrently
                TEXEXPORTS.append(k + '//')
            else:
                TEXEXPORTS.append(k)

    TEXEXPORTS = ':'.join(TEXEXPORTS)

    cmd = f"""export TEXINPUTS=.:{TEXEXPORTS:s}:
    {PDFLATEX:s} {latexfile_path:s}
    bibtex {latexfile_path:s}
    {PDFLATEX:s} {latexfile_path:s}
    {PDFLATEX:s} {latexfile_path:s}"""

    return cmd


def convert_notebook(filename: str,
                     template: str = "tufte",
                     silent: bool = True,
                     texdirs: list = []):
    """ This function compiles a notebook into a DPAC latex document and its PDF.

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

    # Make sure we have a filename without extension
    filename = filename.replace('.ipynb', '')

    # step 1: convert notebook to latex
    cmd = _get_nbconvert_cmd(filename, template=template, debug=~silent)
    print(cmd)

    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    for line in p.stdout:
        if not silent:
            print(line.decode().rstrip())
        else:
            print('.', end='')
    print("\nconversion to tex: ", "success" if int(p.poll()) == 0 else "fail")
    if p.poll()!= 0:
        raise RuntimeError("nbconvert step failed")

    # step 2: convert latex to pdf
    cmd = _get_pdflatex_cmd(filename, texdirs=texdirs)
    print(cmd)

    p = Popen(cmd.replace('\n', '; '), shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    for line in p.stdout:
        if not silent:
            print(line.decode().rstrip())
        else:
            print('.', end='')

    print(f"\nconversion finished. Check {filename:s}.pdf")
