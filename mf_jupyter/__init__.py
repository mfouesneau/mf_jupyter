from . ipython_notebook import *
from . import (figrc, setup_mpl)


def get_package_path():
    import os
    import inspect

    mf_jupyter_path = '/'.join(os.path.abspath(inspect.getfile(inspect.currentframe())).split('/')[:-1])
    return mf_jupyter_path



def mf_jupyter_convert(filename: str, template: str = "dpac", silent: bool = True, texdirs: list = []):
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

    import subprocess
    import mf_jupyter
    from subprocess import Popen, PIPE, STDOUT

    MF_JUPYTER_DIR = mf_jupyter.get_package_path()
    CONFIG_FILE = f"{MF_JUPYTER_DIR:s}/config.py"
    LATEXOPTS = f"--to latex --config {CONFIG_FILE:s}"
    TEMPLATEOPTS = f"--template {MF_JUPYTER_DIR:s}/templates"
    PDFLATEX = f"pdflatex -enable-write18 -shell-escape -interaction=nonstopmode"
    if template == 'dpac':
        TEMPLATE = f"mf_dpac.tplx"
    else:
        TEMPLATE = template


    cmd = f"jupyter nbconvert {LATEXOPTS:s} {filename:s}.ipynb {TEMPLATEOPTS:s}/{TEMPLATE:s}"
    print(cmd)
    
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    for line in p.stdout:
        if not silent:
            print(line.decode().rstrip())
        else:
            print('.', end='')
    print("\nconversion to tex: ", "success" if int(p.poll()) == 0 else "fail")

    TEXEXPORTS = [f"{MF_JUPYTER_DIR:s}"]
    if texdirs:
        for k in texdirs:
            if k[-2] != '//':
                TEXEXPORTS.append(k + '//')
            else:
                TEXEXPORT.append(k)
    
    TEXEXPORT = ':'.join(TEXEXPORT)    
        
    cmd = f"""export TEXINPUTS=.:{TEXEXPORT:s}:
    {PDFLATEX:s} {filename:s}
    bibtex {filename:s}
    {PDFLATEX:s} {filename:s}
    {PDFLATEX:s} {filename:s}"""
    print(cmd)
    p = Popen(cmd.replace('\n', '; '), shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    for line in p.stdout:
        if not silent:
            print(line.decode().rstrip())
        else:
            print('.', end='')
    print(f"\nconversion finished. Check {filename:s}.pdf")
