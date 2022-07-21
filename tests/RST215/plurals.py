"""Print 'Hello world' to the terminal.

RST uses single backticks for inline `interpreted text`,
and like inline literals with double backticks, this is
often used for code snippets. Surprisingly trying to
write plurals like `int`s is not valid RST.

That is considered to be an error, and should fail::

    $ flake8 --select RST RST215/plurals.py
    RST215/plurals.py:3:1: RST215 Inline interpreted text or phrase reference start-string without end-string.

Note the line number is unfortunately given as the start
of the paragraph. The same happens with double backticks
for in-line literals, see RST214.
"""  # noqa: E501

print("Hello world")
