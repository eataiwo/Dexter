from setuptools import setup


__project__ = "Dexter"
__version__ = "0.0.1"
__description__ = "Not really sure yet"
__packages__ = ["utils","src", "src/powertrain"]

setup(
    name = __project__,
    version = __version__,
    description = __description__,
    packages = __packages__,
)
