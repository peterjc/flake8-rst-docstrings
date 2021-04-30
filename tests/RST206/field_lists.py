"""Example with broken RST field list.

This is taken from the RST documentation, with the
final line added *without* the expected indentation
(if a continuation of the final field) or a blank
line (if a new paragraph):

:Date: 2001-08-16
:Version: 1
:Authors: - Me
          - Myself
          - I
:Indentation: Since the field marker may be quite long, the second
   and subsequent lines of the field body do not have to line up
   with the first line, but they must be indented relative to the
   field name marker, and they must line up with each other.
:Parameter i: integer
Using i for an integer index is common in mathematics and physics.

Because the line above is not indented or separated from
the field list by a blank line, it is not valid RST:

    $ flake8 --select RST RST206/fields_list.py
    RST206/field_lists.py:18:1: RST206 Field list ends without a blank line; unexpected unindent.

The end.
"""  # noqa: E501

pass
