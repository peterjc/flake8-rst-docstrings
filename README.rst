flake8-rst-docstrings
=====================

.. image:: https://img.shields.io/pypi/v/flake8-rst-docstrings.svg
   :alt: Released on the Python Package Index (PyPI)
   :target: https://pypi.org/project/flake8-rst-docstrings/
.. image:: https://img.shields.io/conda/vn/conda-forge/flake8-rst-docstrings.svg
   :alt: Released on Conda
   :target: https://anaconda.org/conda-forge/flake8-rst-docstrings
.. image:: https://results.pre-commit.ci/badge/github/peterjc/flake8-rst-docstrings/master.svg
   :target: https://results.pre-commit.ci/latest/github/peterjc/flake8-rst-docstrings/master
   :alt: pre-commit.ci status
.. image:: https://img.shields.io/github/actions/workflow/status/peterjc/flake8-rst-docstrings/test.yml?logo=github-actions
   :alt: GitHub workflow status
   :target: https://github.com/peterjc/flake8-rst-docstrings/actions
.. image:: https://img.shields.io/pypi/dm/flake8-rst-docstrings.svg
   :alt: PyPI downloads
   :target: https://pypistats.org/packages/flake8-rst-docstrings
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :alt: Code style: black
   :target: https://github.com/python/black

Introduction
------------

This is an MIT licensed flake8 plugin for validating Python docstrings markup
as reStructuredText (RST) using the Python library ``docutils``. It is
available to install from the `Python Package Index (PyPI)
<https://pypi.org/project/flake8-rst-docstrings/>`_.

This is based heavily off ``pydocstyle`` (which is also MIT licensed), which
has a flake8 plugin called ``flake8-docstrings``, see:

- https://github.com/PyCQA/pydocstyle
- https://github.com/PyCQA/flake8-docstrings

The reStructuredText (RST) validation is done by calling ``docutils`` via
Todd Wolfson's ``restructuredtext-lint`` code:

- http://docutils.sourceforge.net/
- https://github.com/twolfson/restructuredtext-lint

I recommend you *also* install the related `flake8-docstrings
<https://gitlab.com/pycqa/flake8-docstrings>`_ plugin, which brings
the `pydocstyle <https://github.com/pycqa/pydocstyle>`_ checks into flake8.
This checks things like missing docstrings, and other recommendations from
`PEP 257 Docstring Conventions <https://www.python.org/dev/peps/pep-0257/>`_.

You may *also* wish to install the related flake8 plugin `flake8-rst
<https://github.com/kataev/flake8-rst>`_ which can check the Python style
of doctest formatted snippets of Python code within your ``*.rst`` files
or the docstrings within your ``*.py`` files.

Flake8 Validation codes
-----------------------

Early versions of flake8 assumed a single character prefix for the validation
codes, which became problematic with collisions in the plugin ecosystem. Since
v3.0, flake8 has supported longer prefixes therefore this plugin uses ``RST``
as its prefix.

Internally we use ``docutils`` for RST validation, which has this to say in
`PEP258 <https://www.python.org/dev/peps/pep-0258/#error-handling>`_:

* Level-0, "DEBUG": an internal reporting issue. There is no effect on the
  processing. Level-0 system messages are handled separately from the others.
* Level-1, "INFO": a minor issue that can be ignored. There is little or no
  effect on the processing. Typically level-1 system messages are not
  reported.
* Level-2, "WARNING": an issue that should be addressed. If ignored, there may
  be minor problems with the output. Typically level-2 system messages are
  reported but do not halt processing
* Level-3, "ERROR": a major issue that should be addressed. If ignored, the
  output will contain unpredictable errors. Typically level-3 system messages
  are reported but do not halt processing
* Level-4, "SEVERE": a critical error that must be addressed. Typically
  level-4 system messages are turned into exceptions which halt processing.
  If ignored, the output will contain severe errors.

The ``docutils`` "DEBUG" level messages are not reported, and the plugin
currently ignores the "INFO" level messages.

Within each category, the individual messages are mapped to ``flake8`` codes
using one hundred times the level. i.e. Validation codes ``RST4##`` are
severe or critical errors in RST validation, ``RST3##`` are major errors,
``RST2##`` are warnings, and while currently not yet used, ``RST1##`` would
be information only.

Warning codes:

====== =======================================================================
Code   Description
------ -----------------------------------------------------------------------
RST201 Block quote ends without a blank line; unexpected unindent.
RST202 Bullet list ends without a blank line; unexpected unindent.
RST203 Definition list ends without a blank line; unexpected unindent.
RST204 Enumerated list ends without a blank line; unexpected unindent.
RST205 Explicit markup ends without a blank line; unexpected unindent.
RST206 Field list ends without a blank line; unexpected unindent.
RST207 Literal block ends without a blank line; unexpected unindent.
RST208 Option list ends without a blank line; unexpected unindent.
RST210 Inline strong start-string without end-string.
RST211 Blank line required after table.
RST212 Title underline too short.
RST213 Inline emphasis start-string without end-string.
RST214 Inline literal start-string without end-string.
RST215 Inline interpreted text or phrase reference start-string without end-string.
RST216 Multiple roles in interpreted text (both prefix and suffix present; only one allowed).
RST217 Mismatch: both interpreted text role suffix and reference suffix.
RST218 Literal block expected; none found.
RST219 Inline substitution_reference start-string without end-string.
RST220 Duplicate explicit target name: "XXX".
RST299 Previously unseen warning, not yet assigned a unique code.
====== =======================================================================

Major error codes:

====== =======================================================================
Code   Description
------ -----------------------------------------------------------------------
RST301 Unexpected indentation.
RST302 Malformed table.
RST303 Unknown directive type "XXX".
RST304 Unknown interpreted text role "XXX".
RST305 Undefined substitution referenced: "XXX".
RST306 Unknown target name: "XXX".
RST307 Error in "XXX" directive:
RST399 Previously unseen major error, not yet assigned a unique code.
====== =======================================================================

Severe or critical error codes:

====== =======================================================================
Code   Description
------ -----------------------------------------------------------------------
RST401 Unexpected section title.
RST499 Previously unseen severe error, not yet assigned a unique code.
====== =======================================================================

Codes ending ``99``, for example ``RST499``, indicate a previously unseen
validation error for which we have yet to assign a unique validation code
in the associated range, which would be ``RST4##`` in this example. If you see
one of these codes, please report it on our GitHub issue tracker, ideally with
an example we can use for testing.

Codes starting ``RST9##`` indicate there was a problem parsing the Python
file in order to extract the docstrings, or in processing the contents.

====== =======================================================================
Code   Description (and notes)
------ -----------------------------------------------------------------------
RST900 Failed to load file
RST901 Failed to parse file (*No longer used*)
RST902 Failed to parse __all__ entry (*No longer used*)
RST903 Failed to lint docstring
====== =======================================================================


Installation and usage
----------------------

Python 3.8 or later now required. Earlier versions did support Python 2.7, use
v0.0.14 if required.

We recommend installing the plugin using pip, which handles the dependencies::

    $ pip install flake8-rst-docstrings

Alternatively, if you are using the Anaconda packaging system, the following
command will install the plugin with its dependencies::

    $ conda install -c conda-forge flake8-rst-docstrings

The new validator should be automatically included when using ``flake8`` which
may now report additional validation codes starting with ``RST`` (as defined
above). For example::

    $ flake8 example.py

You can request only the ``RST`` codes be shown using::

    $ flake8 --select RST example.py

Similarly you might add particular RST validation codes to your flake8
configuration file's select or ignore list.

Note in addition to the ``RST`` prefix alone you can use partial codes
like ``RST2`` meaning ``RST200``, ``RST201``, ... and so on.

Normally flake8 violations are to a specific line *and* column. Unfortuntatley,
docutils only gives us a line number, and occasionally this only points to the
start of a paragraph - not the exact line with an issue.


Configuration
-------------

We assume you are familiar with `flake8 configuration
<http://flake8.pycqa.org/en/latest/user/configuration.html>`_.

If you are using Sphinx or other extensions to reStructuredText, you will
want to define any additional directives or roles you are using to avoid
false positive ``RST303``, ``RST304`` and ``RST305`` violations. You may also
need to ignore ``RST307`` if using Sphinx directives with arguments.

You can set these at the command line if you wish::

    $ flake8 --rst-roles class,func,ref --rst-directives envvar,exception ...

We recommend recording these settings in your ``flake8`` configuration,
for example in your ``.flake8``, ``setup.cfg``, or ``tox.ini`` file, e.g.::

    [flake8]
    rst-roles =
        class,
        func,
        ref,
    rst-directives =
        envvar,
        exception,
    rst-substitutions =
        version,
    extend-ignore =
        RST307,
        # ...

Note that flake8 allows splitting the comma separated lists over multiple
lines, and allows including of hash comment lines.

If you are using the `Google Python Style
<https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings>`_
you will sometimes get unwanted warnings from this plugin - particularly in the
argument descriptions - as it does not use strict RST. We therefore currently
suggest ignoring some of the violation codes::

    [flake8]
    extend-ignore =
        # Google Python style is not RST until after processed by Napoleon
        # See https://github.com/peterjc/flake8-rst-docstrings/issues/17
        RST201,RST203,RST301,


Version History
---------------

======= ========== ===========================================================
Version Released   Changes
------- ---------- -----------------------------------------------------------
v0.3.1  2025-04-29 - Adds ``RST220`` for redefined anonymous links.
                   - Requires Python 3.8 or later (no code changes).
v0.3.0  2022-11-16 - Replaced ``setup.py`` with ``pyproject.toml``.
v0.2.7  2022-07-15 - Fix where function signature occurred in docstring body.
v0.2.6  2022-06-07 - Configuration option to define additional substitutions
                     (e.g. from Sphinx) for ``RST305`` (contribution from
                     `Andreas Thum <https://github.com/andthum>`_).
                   - Requires Python 3.7 or later.
v0.2.5  2021-12-10 - Ignore function signature lines at start of docstrings.
v0.2.4  2021-12-09 - Fixed rare line number problem under Python 3.7 or older.
                   - Updated test framework to use ``pytest``.
                   - Requires Python 3.6 or later.
v0.2.3  2021-05-03 - Fixed line number assert in one-line docstring-only file.
v0.2.2  2021-04-30 - Fixed line number problem under Python 3.8 or later.
                   - Corrected off-by-one line number in module docstrings.
v0.2.1  2021-04-23 - Minor internal style change.
v0.2.0  2021-04-23 - Use AST from flake8, not re-parsing with pydocstyle.
                   - Drops ``RST901`` (internal problem with parser).
                   - Drops ``RST902`` (checking any ``__all__`` entry).
v0.1.2  2021-04-16 - Dropped unused logging module import.
                   - Extended test coverage.
v0.1.1  2021-04-15 - Explicit ``pygments`` dependency for any code blocks.
v0.1.0  2021-04-15 - Import the parser from ``pydocstyle`` directly.
                   - Requires Python 3 (drops support for Python 2).
v0.0.14 2020-09-22 - Adds ``RST307`` for error in directive (eg invalid args).
v0.0.13 2019-12-26 - Adds ``RST218`` and ``RST219``.
v0.0.12 2019-11-18 - Adds ``RST213`` to ``RST217``.
v0.0.11 2019-08-07 - Configuration options to define additional directives and
                     roles (e.g. from Sphinx) for ``RST303`` and ``RST304``.
v0.0.10 2019-06-17 - Fixed flake8 "builtins" parameter warning (contribution
                     from `Ruben Opdebeeck <https://github.com/ROpdebee>`_).
v0.0.9  2019-04-22 - Checks positive and negative examples in test framework.
                   - Adds ``RST212``, ``RST305`` and ``RST306`` (contribution
                     from `Brian Skinn <https://github.com/bskinn>`_).
v0.0.8  2017-10-09 - Adds ``RST303`` and ``RST304`` for unknown directives and
                     interpreted text role as used in Sphinx-Needs extension.
v0.0.7  2017-08-25 - Remove triple-quotes before linting, was causing false
                     positives reporting RST entries ending without a blank
                     line at end of docstrings (bug fix for issue #1).
v0.0.6  2017-08-18 - Support PEP263 style encodings following a hashbang line
                     (bug fix for issue #2).
v0.0.5  2017-06-19 - Support PEP263 style encoding declaration under Python 2.
                   - Introduced ``RST900`` when fail to open the file.
v0.0.4  2017-06-19 - Catch docstring linting failures, report as ``RST903``.
v0.0.3  2017-06-16 - Ensure plugin code and RST files themselves validate.
                   - Removed unused import of ``six`` module.
                   - Basic continuous integration checks with TravisCI.
v0.0.2  2017-06-16 - Explicitly depend on flake8 v3.0.0 or later.
                   - Improved documentation.
v0.0.1  2017-06-16 - Initial public release.
======= ========== ===========================================================


Developers
----------

This plugin is on GitHub at https://github.com/peterjc/flake8-rst-docstrings

Developers may install the plugin from the git repository with optional build
dependencies::

    $ pip install -e .[develop]

For testing install `pytest` and run::

    $ flake8 --select RST setup.py flake8_rst_docstrings.py
    $ pytest --verbose

To make a new release once tested locally and on TravisCI::

    $ git tag vX.Y.Z
    $ python -m build
    $ git push origin master --tags
    $ twine upload dist/flake8?rst?docstrings-X.Y.Z*

The PyPI upload should trigger an automated pull request updating the
`flake8-rst-docstrings conda-forge recipe
<https://github.com/conda-forge/flake8-rst-docstrings-feedstock/blob/master/recipe/meta.yaml>`_.
