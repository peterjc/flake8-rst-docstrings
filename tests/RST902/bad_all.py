"""Silly test case for a bad __all__ entry.

This example catches a technical issue with the Python code, not
an RST error directly - but since API documentation usually looks
at the ``__all__`` value this is still relevant.

The ``__all__`` value should be a tuple, even when it has a single
entry - not a string. This file is considered to be in error, and
should fail::

    $ flake8 --select RST RST902/bad_all.py
    RST902/bad_all.py:0:1: RST902 Failed to parse __all__ entry.

Note that currently it does not report the actual line number.
"""


def hello(name="Dave"):
    """Print hello message."""
    print("Hello %s" % name)


__all__ = "hello"  # Should be a single element tuple
