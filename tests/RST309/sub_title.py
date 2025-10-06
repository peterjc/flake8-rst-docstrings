"""Example breaking RST401.

This should fail validation:

    $ flake8 --select RST RST309/sub_title.py
    RST309/sub_title.py:20:1: RST309 Unexpected section title.

See below.
"""


def function(args):
    """Do something.

    Paragraph here, then an indented chunk...

        Indented text.

        Unexpected Subtitle
        -------------------

        More indented text.

    Back to the main level.
    """
    pass
