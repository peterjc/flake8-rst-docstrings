"""Example of invalid RST explicit markup.

This should fail validation:

    $ flake8 --select RST RST205/explicit_markup.py
    RST205/explicit_markup.py:21:1: RST205 Explicit markup ends without a blank line; unexpected unindent.

See below.
"""  # noqa: E501


def function(args):
    """Do something.

    This is a malformed explicit markup block in RST:

    ..
      Alpha
      Beta
      Gamma
    and so on to Omega.

    That line about Omega should be indented or preceded
    by a blank line.
    """
    pass
