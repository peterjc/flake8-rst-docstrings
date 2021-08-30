"""Example breaking RST208 with bad option list.

RST supports option lists, blocks of text in the style
of command line tool help text. This example is based
on the RST documentation.

-a         Output all.
-b         Output both (this description is
           quite long).
-c arg     Output just arg.
--long     Output all day long.

-p         This option has two paragraphs in the description.
           This is the first.

           This is the second.  Blank lines may be omitted between
           options (as above) or left in (as here and below).

--very-long-option  A VMS-style option.  Note the adjustment for
                    the required two spaces.

--an-even-longer-option
           The description can also start on the next line.

-2, --two  This option has two variants.
Note there is no -3 option!

There ought to be a blank line before that final comment,
there isn't so this fails validation:

    $ flake8 --select RST RST208/option_list.py
    RST208/option_list.py:26:1: RST208 Option list ends without a blank line; unexpected unindent.

The end.
"""  # noqa: E501
import sys

print("Called with %i command line arguments" % (len(sys.argv) - 1))
