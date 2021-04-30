"""Example with bullet points.

This example has some bad bullets.

* Apples
* Pears
Other fruit.

It should therefore fail RST validation::

    $ flake8 --select RST RST202/bullets.py
    RST202/bullets.py:7:1: RST202 Bullet list ends without a blank line; unexpected unindent.
    RST202/bullets.py:38:1: RST202 Bullet list ends without a blank line; unexpected unindent.

The end.
"""  # noqa: E501


class Base:
    """Meaningless base class."""

    pass


class Example(
    dict,  # comment to stop black squeezing the class statement into one line
    Base,  # meaningless multiple-subclassing to trigger multi-line statement
):
    """Meaningless class."""

    def method(self):
        """Do stuff.

        Standard paragraph, then intendation as a quote...

           * Alpha
           * Beta
           next paragraph (nested)

        next paragraph (not nested)
        """
        pass
