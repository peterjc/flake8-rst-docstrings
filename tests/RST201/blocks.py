"""Example with bad RST blocks.

This should fail RST validation:

    $ flake8 --select RST RST201/blocks.py
    RST201/blocks.py:18:1: RST201 Block quote ends without a blank line; unexpected unindent.

"""  # noqa: E501


class Example:
    """Some class.

    Standard paragraph

       * List
       * in a quote
    next paragraph (not nested - needs a blank line above)

    next paragraph (not nested)
    """
