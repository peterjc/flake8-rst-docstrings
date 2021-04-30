"""Print 'Hello world' to the terminal.

RST uses double colons to indicate the following
indented text is a literal block. The following
code snippet is a typical usage::

    $ flake8 --select RST RST218/no_literal_block.py
    RST218/no_literal_block.py:13:1: RST218 Literal block expected; none found.

This file triggers an error because this paragraph
says there should be a following literal block, but
there is none::
"""

print("Hello world")
