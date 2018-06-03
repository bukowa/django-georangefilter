"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md")) as fh:
    long_description = fh.read()


setup(
    name="django-georangefilter",  # Required # TODO
    version="0.0.1",  # Required
    description="",  # Required
    author="Mateusz Kurowski",
    license="The Unlicense",
    packages=["georangefilter"],  # Required
    install_requires=["Django>=2.0.0"],  # Optional
)
