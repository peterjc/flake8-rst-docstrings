"""Print 'Hello world' to the terminal.

RST uses single backticks or back-quotes for various
things including interpreted text roles and references.

Here `example is missing a closing backtick.

That is considered to be an error, and should fail::

    $ flake8 --select RST RST215/backticks.py
    RST215/backticks.py:6:1: RST215 Inline interpreted text or phrase reference start-string without end-string.

"""  # noqa: E501

print("Hello world")
