"""Setup file for building/installing flake8-rst-docstrings."""
from __future__ import print_function
from __future__ import with_statement

from setuptools import setup


def get_version(fname="flake8_rst_docstrings.py"):
    """Parse our source code to get the current version number."""
    with open(fname) as f:
        for line in f:
            if line.startswith("__version__"):
                return eval(line.split("=")[-1])


setup(
    name="flake8-rst-docstrings",
    version=get_version(),
    description="Python docstring reStructuredText (RST) validator",
    long_description=open("README.rst").read(),
    license="MIT",
    author="Peter J. A. Cock",
    author_email="p.j.a.cock@googlemail.com",
    url="https://github.com/peterjc/flake8-rst-docstrings",
    project_urls={
        "Documentation": (
            "https://github.com/peterjc/flake8-rst-docstrings/blob/master/README.rst"
        ),
        "Source": "https://github.com/peterjc/flake8-rst-docstrings/",
        "Tracker": "https://github.com/peterjc/flake8-rst-docstrings/issues",
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Framework :: Flake8",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
    keywords="PEP 287, pep287, docstrings, rst, reStructuredText",
    py_modules=["flake8_rst_docstrings"],
    python_requires=">=3.6",
    install_requires=[
        "flake8 >= 3.0.0",
        "restructuredtext_lint",
        "pygments",
    ],
    entry_points={
        "flake8.extension": ["RST = flake8_rst_docstrings:reStructuredTextChecker"]
    },
)
