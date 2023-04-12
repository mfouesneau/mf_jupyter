from importlib.metadata import version, PackageNotFoundError
import pkg_resources

try:
    __version__ = version("mf_jupyter")
    templates_dir = pkg_resources.resource_filename('mf_jupyter', 'templates')
except PackageNotFoundError:
    # package is not installed
    pass
