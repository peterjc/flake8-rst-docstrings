"""Print 'Hello world' to the terminal.

RST uses double backticks for ``literals`` like code
snippets.

Here ``literal is missing the closing backticks.

That is considered to be an error, and should fail::

    $ flake8 --select RST RST214/literal.py
    RST214/literal.py:6:1: RST214 Inline literal start-string without end-string.

"""

print("Hello world")
