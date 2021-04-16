# -*- coding: iso-8859-1 -*-
"""This file is not using UTF-8, but Western European.

It works fine using the Windows-1252 or iso-8859-1 encoding,
but not using UTF-8 which is the Python default.

RST docstring validation is expected to pass:

    $ flake8 --select RST test_cases/not_utf8.py
    (no errors)

"""


class Name:
    """Trivial class for a person's name."""

    def __init__(self, first, last):
        """Initialize name instance.

        >>> fred = Name("Frédéric", "François")
        >>> print(fred)
        """
        self.first = first
        self.last = last

    def __str__(self):
        """Return European style name, First Last."""
        return "%s %s" % (self.first, self.last)
