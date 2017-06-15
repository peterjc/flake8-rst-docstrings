flake8-rst-docstrings
=====================

Introduction
------------

This is an MIT licensed flake8 plugin for validating Python docstrings markup
as reStructuredText (RST) using the Python library ``docutils``.

This is based heavily off ``pydocstyle`` (which is also MIT licensed), which
has a flake8 plugin called ``flake8-docstrings``, see:

- https://github.com/PyCQA/pydocstyle
- https://github.com/PyCQA/flake8-docstrings

The reStructuredText (RST) validation is done by calling ``docutils`` via
Todd Wolfson's ``restructuredtext-lint`` code:

- http://docutils.sourceforge.net/
- https://github.com/twolfson/restructuredtext-lint

Validation codes
----------------

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

The ``docutils`` "DEBUG" level messages are not reported. Apart from that,
within each category, the individual messages are mapped to ``flake8`` codes
using one hundred times the level. i.e. Validation codes ``RST4##`` are
severe or critical errors in RST validation, ``RST3##`` are major errors,
``RST2##`` are warnings, while ``RST1##`` are information only.

Codes ending ``99``, for example ``RST499``, indicate a previously unseen
validation error for which we have yet to assign a unique validation code
in the assocated range, which would be``RST4##`` in this example.

Codes starting ``RST9##`` indicate there was a problem parsing the Python
file in order to extract the docstrings.

TODO: Silence the ``RST1##`` information level codes by default?
