from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("sql-datalineage")
except PackageNotFoundError:
    # package is not installed
    pass
