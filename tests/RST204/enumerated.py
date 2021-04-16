"""Example breaking RST204.

This should fail RST validation:

    $ flake8 --select RST RST204/enumerated.py
    RST204/enumerated.py:21:1: RST204 Enumerated list ends without a blank line; unexpected unindent.

The end.
"""  # noqa: E501


class Example:
    """Placeholder."""

    def method(self):
        """Do stuff.

        Does the following:

        1. Wibble
        2. Wobble
        And falls over.

        To be valid RST there should be a blank line before
        "And falls over." to terminate the enumeration.
        """
        pass
