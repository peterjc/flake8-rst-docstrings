flake8-rst-docstrings
=====================

This is a flake8 plugin using docutils to check Python docstrings markup
validates as reStructuredText (RST).

This is based heavily off ``pydocstyle`` (which is also MIT licensed) which
also has a flake8 plugin called ``flake8-docstrings``, see:

- https://github.com/PyCQA/pydocstyle
- https://github.com/PyCQA/flake8-docstrings

The reStructuredText (RST) validation is done by calling ``docutils`` based
on public domain code from Todd Wolfson's ``restructuredtext-lint`` code:

- http://docutils.sourceforge.net/
- https://github.com/twolfson/restructuredtext-lint
