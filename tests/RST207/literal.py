"""Example breaking RST208.

This should fail RST validation:

    $ flake8 --select RST RST207/literal.py
    RST207/literal.py:21:1: RST207 Literal block ends without a blank line; unexpected unindent.

The end.
"""  # noqa: E501


def function(a, b):
    """Run some analysis.

    Consider the following network::

        A --> B
              ^
              |
              C
    There are two inputs to B, from A and C.

    There should be a blank line ending the literal block.
    """
    pass
