from importlib.metadata import version, PackageNotFoundError
import pkg_resources
import os

try:
    __version__ = version("mf_jupyter")
    pkg_dir = os.path.abspath(pkg_resources.resource_filename('mf_jupyter', ''))
except PackageNotFoundError:
    # package is not installed
    pass
