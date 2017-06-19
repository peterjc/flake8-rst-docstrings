flake8-rst-docstrings
=====================

.. image:: https://img.shields.io/pypi/v/flake8-rst-docstrings.svg
   :alt: Released on the Python Package Index (PyPI)
   :target: https://pypi.python.org/pypi/flake8-rst-docstrings
.. image:: https://img.shields.io/travis/peterjc/flake8-rst-docstrings/master.svg
   :alt: Testing with TravisCI
   :target: https://travis-ci.org/peterjc/flake8-rst-docstrings/branches
.. image:: https://landscape.io/github/peterjc/flake8-rst-docstrings/master/landscape.svg?style=flat
   :alt: Landscape Code Metrics
   :target: https://landscape.io/github/peterjc/flake8-rst-docstrings/

Introduction
------------

This is an MIT licensed flake8 plugin for validating Python docstrings markup
as reStructuredText (RST) using the Python library ``docutils``. Is is
available to install from the Python Package Index (PyPI):

- https://pypi.python.org/pypi/flake8-rst-docstrings

This is based heavily off ``pydocstyle`` (which is also MIT licensed), which
has a flake8 plugin called ``flake8-docstrings``, see:

- https://github.com/PyCQA/pydocstyle
- https://github.com/PyCQA/flake8-docstrings

The reStructuredText (RST) validation is done by calling ``docutils`` via
Todd Wolfson's ``restructuredtext-lint`` code:

- http://docutils.sourceforge.net/
- https://github.com/twolfson/restructuredtext-lint

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
``RST2##`` are warnings, while if shown ``RST1##`` are information only.

Codes ending ``99``, for example ``RST499``, indicate a previously unseen
validation error for which we have yet to assign a unique validation code
in the assocated range, which would be ``RST4##`` in this example.

Codes starting ``RST9##`` indicate there was a problem parsing the Python
file in order to extract the docstrings, or in processing the contents.

====== =======================================================================
Code   Description (and notes)
------ -----------------------------------------------------------------------
RST900 Failed to load file (e.g. unicode encoding issue under Python 2)
RST901 Failed to parse file
RST902 Failed to parse __all__ entry
RST903 Failed to lint docstring (e.g. unicode encoding issue under Python 2)
====== =======================================================================


Installation and usage
----------------------

Python 3.6 or later is recommended, but Python 2.7 is also supported.

We recommend installing this plugin and ``flake8`` itself using pip::

    $ pip install flake8 flake8-rst-docstrings

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


Version History
---------------

======= ========== ===========================================================
Version Released   Changes
------- ---------- -----------------------------------------------------------
v0.0.1  2017-06-16 - Initial public release.
v0.0.2  2017-06-16 - Explicitly depend on flake8 v3.0.0 or later.
                   - Improved documentation.
v0.0.3  2017-06-16 - Ensure plugin code and RST files themselves validate.
                   - Removed unused import of ``six`` module.
                   - Basic continuous integration checks with TravisCI.
v0.0.4  2017-06-19 - Catch docstring linting failures, report as ``RST903``.
v0.0.5  2017-06-19 - Support PEP263 style encoding declaration under Python 2,
                     introduced ``RST900`` when fail to open the file.
======= ========== ===========================================================


Developers
----------

This plugin is on GitHub at https://github.com/peterjc/flake8-rst-docstrings


TODO
----

- Have the "INFO" level ``RST1##`` codes available but ignored by default?
- Can we call ``docutils`` rather than bundle a copy of their parser code?
- Create a test suite and use this for continuous integration.
