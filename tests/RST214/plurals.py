"""Print 'Hello world' to the terminal.

RST uses double backticks for ``literals`` like code
snippets. Surprisingly ``literal``s is not valid,
something you might see in examples like ``int``s
talking about plurals of a datatype.

That is considered to be an error, and should fail::

    $ flake8 --select RST RST214/plurals.py
    RST214/plurals.py:3:1: RST214 Inline literal start-string without end-string.
    RST214/plurals.py:3:1: RST214 Inline literal start-string without end-string.

Note the line number is unfortunately given as the
start of the paragraph. The same happens with single
backticks, see RST215.
"""

print("Hello world")
