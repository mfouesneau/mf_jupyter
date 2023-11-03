import pkg_resources
import os

def get_data_dir() -> str:
    """ Fast access to the package data directory. """
    return os.path.abspath(
        os.path.join(pkg_resources.resource_filename("mf_jupyter", ""))
    )