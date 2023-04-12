from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("mf_jupyter")
except PackageNotFoundError:
    # package is not installed
    pass
