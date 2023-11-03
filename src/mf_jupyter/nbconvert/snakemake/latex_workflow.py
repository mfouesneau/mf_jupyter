""" Generate the snakefile workflow that converts and compiles the notebook to latex """
import os
import pkg_resources
from glob import glob


def generate(
    notebook_name: str,
    template: str,
    bibliography_files: list = None,
    workflow_file: str = None,
) -> str:
    """Generate the snakefile workflow that converts and compiles the notebook to latex"""

    if bibliography_files is None:
        bibliography_files = glob("*.bib")

    if workflow_file is None:
        workflow_file = os.path.abspath(
            os.path.join(
                pkg_resources.resource_filename("mf_jupyter", "nbconvert"),
                "snakemake",
                "snakefile.latex_template",
            )
        )

    params = dict(
        input_file=notebook_name.replace(".ipynb", ""),
        output_file=notebook_name.replace(".ipynb", ".pdf"),
        output_template=template,
        bibliography_files=bibliography_files,
    )
    header = [
        f'{key} = "{value}"'
        for key, value in params.items()
        if key != "bibliography_files"
    ]
    header.append(
        "bibliography_files = ["
        + ", ".join([f'"{bib}"' for bib in bibliography_files])
        + "]"
    )
    header = "\n".join(header)

    with open(workflow_file, "r") as f:
        workflow = f.read()

    split = "# ==== No need to edit below this line ===="
    _, content = workflow.split(split)
    return "\n\n".join([header, split, content])
