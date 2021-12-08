"""Example of invalid nested bullets in RST.

This file should fail RST validation:

    $ flake8 --select RST RST301/nesting.py
    RST301/nesting.py:21:1: RST301 Unexpected indentation.

See below.
"""


def function(args):
    """Do something.

    This looks like a nested bullet point list,
    doesn't it?

    - aaaa
      - bb1
      - bb2
        - ccc
    - aaaa
    - aaaa

    However, RST would require blank lines between the
    different levels of nesting.
    """
    pass
